<?php

namespace RPA\Controllers;

use RPA\Interfaces\SessionServiceInterface;
use RPA\Interfaces\MonitorServiceInterface;
use RPA\Services\ConfigService;
use RPA\Services\ValidationService;
use RPA\Services\RateLimitService;
use RPA\Interfaces\LoggerInterface;

class RPAController
{
    public function __construct(
        private SessionServiceInterface $sessionService,
        private MonitorServiceInterface $monitorService,
        private ConfigService $configService,
        private ValidationService $validationService,
        private RateLimitService $rateLimitService,
        private LoggerInterface $logger
    ) {}

    public function startRPA(array $data): array
    {
        $start_time = microtime(true);
        
        try {
            $this->logger->info('RPA start request received', ['data' => $data]);
            
            // Rate limiting
            $clientIp = $_SERVER['REMOTE_ADDR'] ?? 'unknown';
            if (!$this->rateLimitService->isAllowed($clientIp)) {
                $this->logger->warning('Rate limit exceeded', ['ip' => $clientIp]);
                return $this->errorResponse('Rate limit exceeded. Try again later.');
            }
            
            // Validação de entrada
            $validation = $this->validationService->validate($data);
            if ($validation->hasErrors()) {
                $this->logger->warning('Validation failed', [
                    'errors' => $validation->getErrors(),
                    'data' => $data
                ]);
                return $this->errorResponse('Dados inválidos: ' . implode(', ', $validation->getErrors()));
            }
            
            // ========================================
            // ETAPA 1: CONSULTAR API PH3A (SE NECESSÁRIO)
            // ========================================
            $ph3a_start = microtime(true);
            $campos_ph3a_vazios = [];
            if (empty($data['sexo'])) $campos_ph3a_vazios[] = 'sexo';
            if (empty($data['data_nascimento'])) $campos_ph3a_vazios[] = 'data_nascimento';
            if (empty($data['estado_civil'])) $campos_ph3a_vazios[] = 'estado_civil';
            
            $ph3a_data = [];
            $ph3a_result = null;
            
            if (!empty($campos_ph3a_vazios) && !empty($data['cpf'])) {
                $this->logger->info('Consulting PH3A API', ['fields' => $campos_ph3a_vazios]);
                $ph3a_result = $this->callPH3AApi($data['cpf']);
                
                if ($ph3a_result['success']) {
                    $ph3a_json = json_decode($ph3a_result['response'], true);
                    
                    if ($ph3a_json && $ph3a_json['codigo'] == 1 && isset($ph3a_json['data'])) {
                        $ph3a_data = $ph3a_json['data'];
                        
                        // Mapear campos PH3A
                        if (empty($data['sexo']) && isset($ph3a_data['sexo'])) {
                            $data['sexo'] = ($ph3a_data['sexo'] == 1) ? 'Masculino' : 'Feminino';
                        }
                        
                        if (empty($data['estado_civil']) && isset($ph3a_data['estado_civil'])) {
                            $estado_civil_map = [0 => 'Solteiro', 1 => 'Casado', 2 => 'Divorciado', 3 => 'Viúvo'];
                            $data['estado_civil'] = $estado_civil_map[$ph3a_data['estado_civil']] ?? '';
                        }
                        
                        if (empty($data['data_nascimento']) && isset($ph3a_data['data_nascimento'])) {
                            try {
                                $date = new \DateTime($ph3a_data['data_nascimento']);
                                $data['data_nascimento'] = $date->format('d/m/Y');
                            } catch (\Exception $e) {
                                $data['data_nascimento'] = $ph3a_data['data_nascimento'];
                            }
                        }
                        
                        $this->logger->info('PH3A data filled successfully');
                    } else {
                        $this->logger->warning('PH3A: CPF válido mas não encontrado na base');
                    }
                } else {
                    // PH3A falhou - verificar se campos obrigatórios estão vazios
                    $campos_obrigatorios_vazios = array_intersect($campos_ph3a_vazios, ['sexo', 'data_nascimento', 'estado_civil']);
                    
                    if (!empty($campos_obrigatorios_vazios)) {
                        $this->logger->error('PH3A failed and required fields empty', [
                            'required_fields' => $campos_obrigatorios_vazios,
                            'ph3a_error' => $ph3a_result['error']
                        ]);
                        
                        return $this->errorResponse('Não foi possível validar o CPF', 9001);
                    }
                    
                    $this->logger->warning('PH3A failed but continuing', [
                        'error' => $ph3a_result['error']
                    ]);
                }
            } else {
                $this->logger->info('PH3A: Campos já preenchidos ou CPF vazio');
            }
            
            $ph3a_time = microtime(true) - $ph3a_start;
            
            // ========================================
            // ETAPA 2: CHAMAR WEBHOOKS PRIMEIRO
            // ========================================
            $webhooks_start = microtime(true);
            
            // Prepare webhook data
            $webhook_data = [
                'data' => [
                    'NOME' => $data['nome'],
                    'DDD-CELULAR' => $data['ddd_celular'] ?? '11',
                    'CELULAR' => $data['celular'] ?? substr($data['telefone'], 2),
                    'Email' => $data['email'],
                    'CEP' => $data['cep'],
                    'CPF' => $data['cpf'],
                    'MARCA' => $data['marca'] ?? '',
                    'PLACA' => $data['placa'],
                    'VEICULO' => $data['marca'] ?? '',
                    'ANO' => $data['ano'] ?? '',
                    'GCLID_FLD' => $data['gclid'] ?? '',
                    'SEXO' => $data['sexo'] ?? '',
                    'DATA-DE-NASCIMENTO' => $data['data_nascimento'] ?? '',
                    'ESTADO-CIVIL' => $data['estado_civil'] ?? '',
                    'produto' => $data['produto'] ?? 'seguro-auto',
                    'landing_url' => $data['landing_url'] ?? '',
                    'utm_source' => $data['utm_source'] ?? '',
                    'utm_campaign' => $data['utm_campaign'] ?? ''
                ],
                'd' => date('c'),
                'name' => 'Formulário de Cotação RPA'
            ];
            
            // Call webhooks
            $webhook_results = [];
            $webhook_success_count = 0;
            
            $this->logger->info('Calling EspoCRM webhook');
            $travelangels_result = $this->callWebhook('https://mdmidia.com.br/add_travelangels.php', $webhook_data);
            $webhook_results['travelangels'] = $travelangels_result;
            
            if ($travelangels_result['success']) {
                $webhook_success_count++;
                $this->logger->info('EspoCRM webhook successful');
            } else {
                $this->logger->error('EspoCRM webhook failed', ['error' => $travelangels_result['error']]);
            }
            
            $this->logger->info('Calling Octadesk webhook');
            $octa_result = $this->callWebhook('https://mdmidia.com.br/add_webflow_octa.php', $webhook_data);
            $webhook_results['octadesk'] = $octa_result;
            
            if ($octa_result['success']) {
                $webhook_success_count++;
                $this->logger->info('Octadesk webhook successful');
            } else {
                $this->logger->error('Octadesk webhook failed', ['error' => $octa_result['error']]);
            }
            
            $webhooks_time = microtime(true) - $webhooks_start;
            
            // ========================================
            // ETAPA 3: INICIAR RPA (SÍNCRONO - AGUARDA DADOS PH3A)
            // ========================================
            $rpa_start = microtime(true);
            
            $this->logger->info('Starting RPA process');
            $rpa_result = $this->startRPAProcess($data);
            
            if ($rpa_result['success']) {
                $this->logger->info('RPA completed successfully');
            } else {
                $this->logger->error('RPA process failed', ['output' => $rpa_result['output']]);
            }
            
            $rpa_time = microtime(true) - $rpa_start;
            $total_time = microtime(true) - $start_time;
            
            // ========================================
            // LOGS E RESPOSTA
            // ========================================
            
            // Log webhook results
            $masked_cpf = substr($data['cpf'], -4);
            $log_data = [
                'session_id' => $session_id ?? 'unknown',
                'timestamp' => date('c'),
                'performance' => [
                    'ph3a_time' => round($ph3a_time, 3),
                    'webhooks_time' => round($webhooks_time, 3),
                    'rpa_time' => round($rpa_time, 3),
                    'total_time' => round($total_time, 3)
                ],
                'ph3a_result' => $ph3a_result ?? null,
                'ph3a_data' => $ph3a_data ?? null,
                'campos_ph3a_vazios' => $campos_ph3a_vazios ?? [],
                'webhook_results' => $webhook_results,
                'webhook_success_count' => $webhook_success_count,
                'rpa_result' => $rpa_result,
                'input_data' => [
                    'cpf' => '***' . $masked_cpf,
                    'nome' => $data['nome'],
                    'placa' => $data['placa'],
                    'cep' => $data['cep'],
                    'email' => $data['email'],
                    'gclid' => $data['gclid'] ?? ''
                ]
            ];
            
            $this->logWebhookResults($session_id ?? 'unknown', $log_data);
            
            // Criar sessão RPA
            $result = $this->sessionService->create($data);
            
            if ($result['success']) {
                $this->logger->info('RPA started successfully', [
                    'session_id' => $result['session_id']
                ]);
                
                // Adicionar dados de webhooks e performance à resposta
                $result['performance'] = [
                    'ph3a_time' => round($ph3a_time, 3),
                    'webhooks_time' => round($webhooks_time, 3),
                    'rpa_time' => round($rpa_time, 3),
                    'total_time' => round($total_time, 3)
                ];
                $result['ph3a_consulted'] = !empty($campos_ph3a_vazios) && !empty($data['cpf']);
                $result['ph3a_fields_filled'] = array_diff(['sexo', 'data_nascimento', 'estado_civil'], $campos_ph3a_vazios ?? []);
                $result['webhook_results'] = $webhook_results;
                $result['webhook_success_count'] = $webhook_success_count;
                $result['rpa_result'] = $rpa_result;
                $result['execution_order'] = 'ph3a_then_webhooks_then_rpa';
            } else {
                $this->logger->error('RPA start failed', [
                    'error' => $result['error'] ?? 'Unknown error'
                ]);
            }
            
            return $result;
            
        } catch (\Exception $e) {
            $this->logger->error('RPA start exception', [
                'error' => $e->getMessage(),
                'trace' => $e->getTraceAsString()
            ]);
            
            return $this->errorResponse('Erro interno: ' . $e->getMessage());
        }
    }

    /**
     * Call PH3A API to fill missing fields
     * Timeout otimizado para 5 segundos baseado no teste de performance
     */
    private function callPH3AApi(string $cpf): array
    {
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, 'https://mdmidia.com.br/cpf-validate.php');
        curl_setopt($ch, CURLOPT_POST, true);
        curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode(['cpf' => $cpf]));
        curl_setopt($ch, CURLOPT_HTTPHEADER, [
            'Content-Type: application/json',
            'User-Agent: RPA-API-v6.9.1'
        ]);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_TIMEOUT, 5);         // ✅ 5 segundos (otimizado)
        curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 2);   // ✅ 2 segundos (otimizado)
        curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
        
        $response = curl_exec($ch);
        $http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        $error = curl_error($ch);
        curl_close($ch);
        
        return [
            'success' => $http_code >= 200 && $http_code < 300,
            'http_code' => $http_code,
            'response' => $response,
            'error' => $error
        ];
    }

    /**
     * Call webhook endpoint
     */
    private function callWebhook(string $url, array $data): array
    {
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, $url);
        curl_setopt($ch, CURLOPT_POST, true);
        curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
        curl_setopt($ch, CURLOPT_HTTPHEADER, [
            'Content-Type: application/json',
            'User-Agent: RPA-API-v6.9.1'
        ]);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_TIMEOUT, 30);
        curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 10);
        curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
        
        $response = curl_exec($ch);
        $http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        $error = curl_error($ch);
        curl_close($ch);
        
        return [
            'success' => $http_code >= 200 && $http_code < 300,
            'http_code' => $http_code,
            'response' => $response,
            'error' => $error
        ];
    }

    /**
     * Start RPA process (síncrono - aguarda dados PH3A)
     */
    private function startRPAProcess(array $data): array
    {
        $rpa_command = "cd /opt/imediatoseguros-rpa && source venv/bin/activate && python executar_rpa_imediato_playwright.py '" . json_encode($data) . "'";
        $output = shell_exec($rpa_command);
        
        return [
            'success' => !empty($output),
            'output' => $output,
            'command' => $rpa_command
        ];
    }

    /**
     * Log webhook results with performance metrics
     */
    private function logWebhookResults(string $sessionId, array $logData): void
    {
        $log_file = "/opt/imediatoseguros-rpa/logs/webhook_calls_" . date('Y-m-d') . ".log";
        if (!is_dir(dirname($log_file))) {
            mkdir(dirname($log_file), 0755, true);
        }
        file_put_contents($log_file, json_encode($logData) . "\n", FILE_APPEND | LOCK_EX);
    }

    /**
     * Validate required PH3A fields
     */
    private function validatePH3AFields(array $data): array
    {
        $campos_obrigatorios = ['sexo', 'data_nascimento', 'estado_civil'];
        $campos_vazios = [];
        
        foreach ($campos_obrigatorios as $campo) {
            if (empty($data[$campo])) {
                $campos_vazios[] = $campo;
            }
        }
        
        return [
            'valid' => empty($campos_vazios),
            'campos_vazios' => $campos_vazios
        ];
    }

    public function getStatus(string $sessionId): array
    {
        try {
            $this->logger->info('Status request received', ['session_id' => $sessionId]);
            
            $result = $this->sessionService->getStatus($sessionId);
            
            if ($result['success']) {
                $this->logger->info('Status retrieved successfully', [
                    'session_id' => $sessionId,
                    'status' => $result['session']['status'] ?? 'unknown'
                ]);
            } else {
                $this->logger->warning('Status retrieval failed', [
                    'session_id' => $sessionId,
                    'error' => $result['error'] ?? 'Unknown error'
                ]);
            }
            
            return $result;
            
        } catch (\Exception $e) {
            $this->logger->error('Status request exception', [
                'session_id' => $sessionId,
                'error' => $e->getMessage()
            ]);
            
            return $this->errorResponse('Erro interno: ' . $e->getMessage());
        }
    }

    public function listSessions(): array
    {
        try {
            $this->logger->info('List sessions request received');
            
            $result = $this->sessionService->list();
            
            if ($result['success']) {
                $this->logger->info('Sessions listed successfully', [
                    'total' => $result['total'] ?? 0
                ]);
            } else {
                $this->logger->error('Sessions list failed', [
                    'error' => $result['error'] ?? 'Unknown error'
                ]);
            }
            
            return $result;
            
        } catch (\Exception $e) {
            $this->logger->error('List sessions exception', [
                'error' => $e->getMessage()
            ]);
            
            return $this->errorResponse('Erro interno: ' . $e->getMessage());
        }
    }

    public function stopSession(string $sessionId): array
    {
        try {
            $this->logger->info('Stop session request received', ['session_id' => $sessionId]);
            
            $result = $this->sessionService->stop($sessionId);
            
            if ($result['success']) {
                $this->logger->info('Session stopped successfully', ['session_id' => $sessionId]);
            } else {
                $this->logger->warning('Session stop failed', [
                    'session_id' => $sessionId,
                    'error' => $result['error'] ?? 'Unknown error'
                ]);
            }
            
            return $result;
            
        } catch (\Exception $e) {
            $this->logger->error('Stop session exception', [
                'session_id' => $sessionId,
                'error' => $e->getMessage()
            ]);
            
            return $this->errorResponse('Erro interno: ' . $e->getMessage());
        }
    }

    public function monitorSession(string $sessionId): array
    {
        try {
            $this->logger->info('Monitor session request received', ['session_id' => $sessionId]);
            
            $result = $this->monitorService->monitor($sessionId);
            
            if ($result['success']) {
                $this->logger->info('Session monitored successfully', [
                    'session_id' => $sessionId
                ]);
            } else {
                $this->logger->warning('Session monitoring failed', [
                    'session_id' => $sessionId,
                    'error' => $result['error'] ?? 'Unknown error'
                ]);
            }
            
            return $result;
            
        } catch (\Exception $e) {
            $this->logger->error('Monitor session exception', [
                'session_id' => $sessionId,
                'error' => $e->getMessage()
            ]);
            
            return $this->errorResponse('Erro interno: ' . $e->getMessage());
        }
    }

    public function getLogs(string $sessionId, int $limit = 100): array
    {
        try {
            $this->logger->info('Get logs request received', [
                'session_id' => $sessionId,
                'limit' => $limit
            ]);
            
            $logs = $this->monitorService->getLogs($sessionId, $limit);
            
            $this->logger->info('Logs retrieved successfully', [
                'session_id' => $sessionId,
                'count' => count($logs)
            ]);
            
            return [
                'success' => true,
                'logs' => $logs,
                'count' => count($logs)
            ];
            
        } catch (\Exception $e) {
            $this->logger->error('Get logs exception', [
                'session_id' => $sessionId,
                'error' => $e->getMessage()
            ]);
            
            return $this->errorResponse('Erro interno: ' . $e->getMessage());
        }
    }

    public function healthCheck(): array
    {
        try {
            $this->logger->info('Health check request received');
            
            $health = $this->monitorService->healthCheck();
            
            $this->logger->info('Health check completed', [
                'status' => $health['status'] ?? 'unknown'
            ]);
            
            return [
                'success' => true,
                'health' => $health
            ];
            
        } catch (\Exception $e) {
            $this->logger->error('Health check exception', [
                'error' => $e->getMessage()
            ]);
            
            return $this->errorResponse('Erro interno: ' . $e->getMessage());
        }
    }

    public function getMetrics(): array
    {
        try {
            $this->logger->info('Get metrics request received');
            
            $metrics = $this->monitorService->getMetrics();
            
            $this->logger->info('Metrics retrieved successfully');
            
            return [
                'success' => true,
                'metrics' => $metrics
            ];
            
        } catch (\Exception $e) {
            $this->logger->error('Get metrics exception', [
                'error' => $e->getMessage()
            ]);
            
            return $this->errorResponse('Erro interno: ' . $e->getMessage());
        }
    }

    /**
     * Get progress for a specific session (real-time monitoring)
     */
    public function getProgress(string $sessionId): array
    {
        try {
            $this->logger->info('Progress request received', ['session_id' => $sessionId]);
            
            // Validate session ID format
            if (empty($sessionId) || !preg_match('/^[a-zA-Z0-9_-]+$/', $sessionId)) {
                return $this->errorResponse('Session ID inválido');
            }
            
            // Get progress from MonitorService
            $result = $this->monitorService->getProgress($sessionId);
            
            if ($result['success']) {
                $this->logger->info('Progress retrieved successfully', [
                    'session_id' => $sessionId,
                    'status' => $result['data']['status'] ?? 'unknown'
                ]);
                
                return [
                    'success' => true,
                    'session_id' => $sessionId,
                    'progress' => $result['data'],
                    'timestamp' => date('Y-m-d H:i:s')
                ];
            } else {
                $this->logger->warning('Failed to get progress', [
                    'session_id' => $sessionId,
                    'error' => $result['error'] ?? 'Unknown error'
                ]);
                
                return $this->errorResponse($result['error'] ?? 'Erro ao obter progresso');
            }
            
        } catch (\Exception $e) {
            $this->logger->error('Failed to get progress', [
                'session_id' => $sessionId,
                'error' => $e->getMessage()
            ]);
            
            return $this->errorResponse('Erro ao obter progresso: ' . $e->getMessage());
        }
    }

    public function cleanup(): array
    {
        try {
            $this->logger->info('Cleanup request received');
            
            $result = $this->sessionService->cleanup();
            
            if ($result['success']) {
                $this->logger->info('Cleanup completed successfully', [
                    'cleaned' => $result['cleaned'] ?? 0
                ]);
            } else {
                $this->logger->error('Cleanup failed', [
                    'error' => $result['error'] ?? 'Unknown error'
                ]);
            }
            
            return $result;
            
        } catch (\Exception $e) {
            $this->logger->error('Cleanup exception', [
                'error' => $e->getMessage()
            ]);
            
            return $this->errorResponse('Erro interno: ' . $e->getMessage());
        }
    }

    private function successResponse(array $data = []): array
    {
        return array_merge([
            'success' => true,
            'timestamp' => date('Y-m-d H:i:s')
        ], $data);
    }

    private function errorResponse(string $message, int $code = 400): array
    {
        return [
            'success' => false,
            'error' => $message,
            'code' => $code,
            'timestamp' => date('Y-m-d H:i:s')
        ];
    }
}






