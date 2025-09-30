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
