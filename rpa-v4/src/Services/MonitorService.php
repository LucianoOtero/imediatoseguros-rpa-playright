<?php

namespace RPA\Services;

use RPA\Interfaces\MonitorServiceInterface;
use RPA\Repositories\SessionRepository;
use RPA\Interfaces\LoggerInterface;

class MonitorService implements MonitorServiceInterface
{
    private SessionRepository $repository;
    private LoggerInterface $logger;

    public function __construct(
        SessionRepository $repository,
        LoggerInterface $logger
    ) {
        $this->repository = $repository;
        $this->logger = $logger;
    }

    public function monitor(string $sessionId): array
    {
        try {
            $session = $this->repository->getSession($sessionId);
            
            if (!$session) {
                return [
                    'success' => false,
                    'error' => 'Sessão não encontrada'
                ];
            }
            
            $progress = $this->repository->getProgress($sessionId);
            $logs = $this->getLogs($sessionId, 50);
            
            return [
                'success' => true,
                'session' => $session,
                'progress' => $progress,
                'logs' => $logs,
                'monitored_at' => date('Y-m-d H:i:s')
            ];
            
        } catch (\Exception $e) {
            $this->logger->error('Failed to monitor session', [
                'session_id' => $sessionId,
                'error' => $e->getMessage()
            ]);
            
            return [
                'success' => false,
                'error' => 'Erro ao monitorar sessão: ' . $e->getMessage()
            ];
        }
    }

    /**
     * Get progress from progress tracker JSON files (real-time monitoring)
     */
    public function getProgress(string $sessionId): array
    {
        try {
            // Detectar arquivos disponíveis
            $history_file = "/opt/imediatoseguros-rpa/rpa_data/history_{$sessionId}.json";
            $progress_file = "/opt/imediatoseguros-rpa/rpa_data/progress_{$sessionId}.json";

            $use_history = file_exists($history_file);
            $use_progress = file_exists($progress_file) && !$use_history;

            if (!$use_history && !$use_progress) {
                // If neither file exists, return initial status
                return [
                    'success' => true,
                    'data' => [
                        'etapa_atual' => 0,
                        'total_etapas' => 5,
                        'percentual' => 0.0,
                        'status' => 'waiting',
                        'mensagem' => 'Aguardando início da execução',
                        'estimativas' => [
                            'capturadas' => false,
                            'dados' => null
                        ],
                        'resultados_finais' => [
                            'rpa_finalizado' => false,
                            'dados' => null
                        ],
                        'timeline' => [],
                        'source' => 'initial'
                    ]
                ];
            }

            // Processar dados
            if ($use_history) {
                $data = $this->processarHistorico($history_file, $sessionId);
            } else {
                $data = $this->processarProgress($progress_file, $sessionId);
            }

            return [
                'success' => true,
                'data' => $data
            ];

        } catch (\Exception $e) {
            $this->logger->error('Failed to get progress', [
                'session_id' => $sessionId,
                'error' => $e->getMessage()
            ]);

            return [
                'success' => false,
                'error' => 'Erro ao obter progresso: ' . $e->getMessage()
            ];
        }
    }

    /**
     * Process history file (complete execution)
     */
    private function processarHistorico(string $history_file, string $session_id): array
    {
        $content = file_get_contents($history_file);
        $history_data = json_decode($content, true);

        if (!$history_data) {
            throw new \Exception('Erro ao ler arquivo de histórico');
        }

        $historico = $history_data['historico'] ?? [];
        $processed = $this->processarHistoricoArray($historico, $history_data);
        
        // Detecta estimativas (Tela 4)
        $estimativas_info = $this->detectarEstimativas($historico);
        
        // Detecta resultados finais (Tela 15)
        $resultados_info = $this->detectarResultadosFinais($historico);

        return [
            'etapa_atual' => $processed['current_etapa'],
            'total_etapas' => $history_data['total_etapas'] ?? 5,
            'percentual' => ($processed['current_etapa'] / 5) * 100,
            'status' => $processed['current_status'],
            'mensagem' => $processed['current_mensagem'],
            'estimativas' => [
                'capturadas' => $estimativas_info['estimativas_capturadas'],
                'dados' => $estimativas_info['estimativas_capturadas'] 
                    ? $this->extrairDadosEstimativas($estimativas_info['estimativas_entry'])
                    : null
            ],
            'resultados_finais' => [
                'rpa_finalizado' => $resultados_info['rpa_finalizado'],
                'dados' => $resultados_info['rpa_finalizado'] 
                    ? $this->processarPlanos($this->lerResultadosFinais($session_id))
                    : null
            ],
            'timeline' => array_slice($processed['timeline'], -10), // Últimas 10 entradas
            'source' => 'history'
        ];
    }

    /**
     * Process progress file (current execution)
     */
    private function processarProgress(string $progress_file, string $session_id): array
    {
        $content = file_get_contents($progress_file);
        $progress_data = json_decode($content, true);

        if (!$progress_data) {
            throw new \Exception('Erro ao ler arquivo de progresso');
        }

        return [
            'etapa_atual' => $progress_data['etapa_atual'] ?? 0,
            'total_etapas' => $progress_data['total_etapas'] ?? 5,
            'percentual' => $progress_data['percentual'] ?? 0.0,
            'status' => $progress_data['status'] ?? 'unknown',
            'mensagem' => $progress_data['mensagem'] ?? 'Status desconhecido',
            'estimativas' => [
                'capturadas' => isset($progress_data['dados_extra']['estimativas_tela_4']),
                'dados' => $progress_data['dados_extra']['estimativas_tela_4'] ?? null
            ],
            'resultados_finais' => [
                'rpa_finalizado' => ($progress_data['status'] ?? '') === 'success',
                'dados' => null
            ],
            'timeline' => [],
            'source' => 'progress'
        ];
    }

    /**
     * Process history array
     */
    private function processarHistoricoArray(array $historico, array $history_data): array
    {
        $current_etapa = 0;
        $current_status = 'waiting';
        $current_mensagem = 'Aguardando início';
        $timeline = [];

        foreach ($historico as $entry) {
            $timeline[] = [
                'etapa' => $entry['etapa'] ?? 'unknown',
                'timestamp' => $entry['timestamp'] ?? '',
                'status' => $entry['status'] ?? 'unknown',
                'mensagem' => $entry['mensagem'] ?? '',
                'dados_extra' => $entry['dados_extra'] ?? null
            ];

            // Atualizar estado atual
            if (is_numeric($entry['etapa'])) {
                $current_etapa = max($current_etapa, (int)$entry['etapa']);
            }
            $current_status = $entry['status'] ?? $current_status;
            $current_mensagem = $entry['mensagem'] ?? $current_mensagem;
        }

        return [
            'current_etapa' => $current_etapa,
            'current_status' => $current_status,
            'current_mensagem' => $current_mensagem,
            'timeline' => $timeline
        ];
    }

    /**
     * Detect estimates in history
     */
    private function detectarEstimativas(array $historico): array
    {
        $estimativas_entry = null;
        $execucao_posterior = false;
        
        // Busca entrada "estimativas" no histórico
        foreach ($historico as $index => $entry) {
            if ($entry['etapa'] === 'estimativas') {
                $estimativas_entry = $entry;
                break;
            }
        }
        
        // Verifica se há execução posterior (estimativas capturadas)
        if ($estimativas_entry !== null && count($historico) > $index + 1) {
            $execucao_posterior = true;
        }
        
        return [
            'estimativas_encontradas' => $estimativas_entry !== null,
            'estimativas_capturadas' => $execucao_posterior,
            'estimativas_entry' => $estimativas_entry
        ];
    }

    /**
     * Detect final results in history
     */
    private function detectarResultadosFinais(array $historico): array
    {
        $rpa_finalizado = false;
        
        // Verifica se há entrada de conclusão
        foreach ($historico as $entry) {
            if (($entry['status'] ?? '') === 'success' || 
                ($entry['status'] ?? '') === 'completed') {
                $rpa_finalizado = true;
                break;
            }
        }
        
        return [
            'rpa_finalizado' => $rpa_finalizado
        ];
    }

    /**
     * Extract estimate data
     */
    private function extrairDadosEstimativas(array $estimativas_entry): array
    {
        return $estimativas_entry['dados_extra'] ?? [];
    }

    /**
     * Read final results
     */
    private function lerResultadosFinais(string $session_id): array
    {
        $result_file = "/opt/imediatoseguros-rpa/rpa_data/result_{$session_id}.json";
        
        if (!file_exists($result_file)) {
            return [];
        }
        
        $content = file_get_contents($result_file);
        return json_decode($content, true) ?? [];
    }

    /**
     * Process plans data
     */
    private function processarPlanos(array $resultados): array
    {
        // Processar dados dos planos conforme necessário
        return $resultados;
    }

    public function getLogs(string $sessionId, int $limit = 100): array
    {
        try {
            $logFile = "/opt/imediatoseguros-rpa/logs/rpa_v4_{$sessionId}.log";
            
            if (!file_exists($logFile)) {
                return [];
            }
            
            $lines = file($logFile, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
            
            if (!$lines) {
                return [];
            }
            
            // Pegar as últimas N linhas
            $lines = array_slice($lines, -$limit);
            
            $logs = [];
            foreach ($lines as $line) {
                // Tentar parsear como JSON (logs estruturados)
                $decoded = json_decode($line, true);
                if ($decoded) {
                    $logs[] = $decoded;
                } else {
                    // Log simples
                    $logs[] = [
                        'timestamp' => date('Y-m-d H:i:s'),
                        'level' => 'INFO',
                        'message' => $line,
                        'raw' => true
                    ];
                }
            }
            
            return $logs;
            
        } catch (\Exception $e) {
            $this->logger->error('Failed to get session logs', [
                'session_id' => $sessionId,
                'error' => $e->getMessage()
            ]);
            
            return [];
        }
    }

    public function healthCheck(): array
    {
        try {
            $health = [
                'status' => 'healthy',
                'timestamp' => date('Y-m-d H:i:s'),
                'checks' => []
            ];
            
            // Verificar diretórios
            $directories = [
                'sessions' => '/opt/imediatoseguros-rpa/sessions',
                'data' => '/opt/imediatoseguros-rpa/rpa_data',
                'scripts' => '/opt/imediatoseguros-rpa/scripts',
                'logs' => '/opt/imediatoseguros-rpa/logs'
            ];
            
            foreach ($directories as $name => $path) {
                $health['checks'][$name] = [
                    'status' => is_dir($path) && is_writable($path) ? 'ok' : 'error',
                    'path' => $path,
                    'writable' => is_writable($path)
                ];
            }
            
            // Verificar processos Python
            exec('pgrep -f "executar_rpa_modular_telas_1_a_5.py"', $processes);
            $health['checks']['python_processes'] = [
                'status' => count($processes) > 0 ? 'ok' : 'warning',
                'count' => count($processes),
                'processes' => $processes
            ];
            
            // Verificar uso de disco
            $diskUsage = disk_free_space('/opt/imediatoseguros-rpa');
            $diskTotal = disk_total_space('/opt/imediatoseguros-rpa');
            $diskPercent = (($diskTotal - $diskUsage) / $diskTotal) * 100;
            
            $health['checks']['disk_space'] = [
                'status' => $diskPercent < 90 ? 'ok' : 'warning',
                'free_bytes' => $diskUsage,
                'total_bytes' => $diskTotal,
                'used_percent' => round($diskPercent, 2)
            ];
            
            // Verificar memória
            $memInfo = file_get_contents('/proc/meminfo');
            preg_match('/MemTotal:\s+(\d+)/', $memInfo, $total);
            preg_match('/MemAvailable:\s+(\d+)/', $memInfo, $available);
            
            if ($total && $available) {
                $memPercent = (($total[1] - $available[1]) / $total[1]) * 100;
                $health['checks']['memory'] = [
                    'status' => $memPercent < 90 ? 'ok' : 'warning',
                    'total_kb' => $total[1],
                    'available_kb' => $available[1],
                    'used_percent' => round($memPercent, 2)
                ];
            }
            
            // Determinar status geral
            $hasErrors = false;
            $hasWarnings = false;
            
            foreach ($health['checks'] as $check) {
                if ($check['status'] === 'error') {
                    $hasErrors = true;
                } elseif ($check['status'] === 'warning') {
                    $hasWarnings = true;
                }
            }
            
            if ($hasErrors) {
                $health['status'] = 'unhealthy';
            } elseif ($hasWarnings) {
                $health['status'] = 'degraded';
            }
            
            return $health;
            
        } catch (\Exception $e) {
            $this->logger->error('Health check failed', [
                'error' => $e->getMessage()
            ]);
            
            return [
                'status' => 'unhealthy',
                'timestamp' => date('Y-m-d H:i:s'),
                'error' => $e->getMessage()
            ];
        }
    }

    public function getMetrics(): array
    {
        try {
            $sessions = $this->repository->listSessions();
            
            $metrics = [
                'timestamp' => date('Y-m-d H:i:s'),
                'sessions' => [
                    'total' => count($sessions),
                    'by_status' => []
                ],
                'performance' => []
            ];
            
            // Contar sessões por status
            foreach ($sessions as $session) {
                $status = $session['status'] ?? 'unknown';
                $metrics['sessions']['by_status'][$status] = 
                    ($metrics['sessions']['by_status'][$status] ?? 0) + 1;
            }
            
            // Métricas de performance (últimas 24 horas)
            $recentSessions = array_filter($sessions, function($session) {
                $created = strtotime($session['created_at'] ?? '');
                return $created > (time() - 24 * 60 * 60);
            });
            
            if (!empty($recentSessions)) {
                $completedSessions = array_filter($recentSessions, function($session) {
                    return ($session['status'] ?? '') === 'completed';
                });
                
                $metrics['performance'] = [
                    'sessions_24h' => count($recentSessions),
                    'completed_24h' => count($completedSessions),
                    'success_rate' => count($recentSessions) > 0 ? 
                        round((count($completedSessions) / count($recentSessions)) * 100, 2) : 0
                ];
            }
            
            return $metrics;
            
        } catch (\Exception $e) {
            $this->logger->error('Failed to get metrics', [
                'error' => $e->getMessage()
            ]);
            
            return [
                'timestamp' => date('Y-m-d H:i:s'),
                'error' => $e->getMessage()
            ];
        }
    }
}
