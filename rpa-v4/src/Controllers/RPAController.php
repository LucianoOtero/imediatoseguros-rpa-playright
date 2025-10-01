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
        try {
            $this->logger->info('RPA start request received', ['data' => $data]);
            
            // Rate limiting
            $clientIp = $_SERVER['REMOTE_ADDR'] ?? 'unknown';
            if (!$this->rateLimitService->isAllowed($clientIp)) {
                $this->logger->warning('Rate limit exceeded', ['ip' => $clientIp]);
                return $this->errorResponse('Rate limit exceeded. Try again later.');
            }
            
            // Validação de entrada (reativada com estratégia conservadora)
            $validation = $this->validationService->validate($data);
            if ($validation->hasErrors()) {
                $this->logger->warning('Validation failed', [
                    'errors' => $validation->getErrors(),
                    'data' => $data
                ]);
                return $this->errorResponse('Dados inválidos: ' . implode(', ', $validation->getErrors()));
            }
            
            // Criar sessão RPA
            $result = $this->sessionService->create($data);
            
            if ($result['success']) {
                $this->logger->info('RPA started successfully', [
                    'session_id' => $result['session_id']
                ]);
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
