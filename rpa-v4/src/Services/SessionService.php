<?php

namespace RPA\Services;

use RPA\Interfaces\SessionServiceInterface;
use RPA\Repositories\SessionRepository;
use RPA\Interfaces\LoggerInterface;

class SessionService implements SessionServiceInterface
{
    private SessionRepository $repository;
    private LoggerInterface $logger;
    private string $scriptsPath;

    public function __construct(
        SessionRepository $repository,
        LoggerInterface $logger,
        string $scriptsPath
    ) {
        $this->repository = $repository;
        $this->logger = $logger;
        $this->scriptsPath = $scriptsPath;
    }

    public function create(array $data): array
    {
        try {
            $this->logger->info('Creating new RPA session', ['data' => $data]);
            
            $sessionId = $this->repository->createSession($data);
            
            // Iniciar processo RPA em background
            $this->startRPABackground($sessionId, $data);
            
            $this->logger->info('RPA session created successfully', ['session_id' => $sessionId]);
            
            return [
                'success' => true,
                'session_id' => $sessionId,
                'message' => 'Sessão RPA criada com sucesso'
            ];
            
        } catch (\Exception $e) {
            $this->logger->error('Failed to create RPA session', [
                'error' => $e->getMessage(),
                'data' => $data
            ]);
            
            return [
                'success' => false,
                'error' => 'Erro ao criar sessão RPA: ' . $e->getMessage()
            ];
        }
    }

    public function getStatus(string $sessionId): array
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
            
            return [
                'success' => true,
                'session' => $session,
                'progress' => $progress
            ];
            
        } catch (\Exception $e) {
            $this->logger->error('Failed to get session status', [
                'session_id' => $sessionId,
                'error' => $e->getMessage()
            ]);
            
            return [
                'success' => false,
                'error' => 'Erro ao obter status da sessão: ' . $e->getMessage()
            ];
        }
    }

    public function list(): array
    {
        try {
            $sessions = $this->repository->listSessions();
            
            return [
                'success' => true,
                'sessions' => $sessions,
                'total' => count($sessions)
            ];
            
        } catch (\Exception $e) {
            $this->logger->error('Failed to list sessions', [
                'error' => $e->getMessage()
            ]);
            
            return [
                'success' => false,
                'error' => 'Erro ao listar sessões: ' . $e->getMessage()
            ];
        }
    }

    public function stop(string $sessionId): array
    {
        try {
            $session = $this->repository->getSession($sessionId);
            
            if (!$session) {
                return [
                    'success' => false,
                    'error' => 'Sessão não encontrada'
                ];
            }
            
            // Parar processo systemd se existir
            $this->stopSystemdService($sessionId);
            
            // Atualizar status da sessão
            $this->repository->updateSession($sessionId, [
                'status' => 'stopped',
                'stopped_at' => date('Y-m-d H:i:s')
            ]);
            
            $this->logger->info('RPA session stopped', ['session_id' => $sessionId]);
            
            return [
                'success' => true,
                'message' => 'Sessão RPA parada com sucesso'
            ];
            
        } catch (\Exception $e) {
            $this->logger->error('Failed to stop RPA session', [
                'session_id' => $sessionId,
                'error' => $e->getMessage()
            ]);
            
            return [
                'success' => false,
                'error' => 'Erro ao parar sessão RPA: ' . $e->getMessage()
            ];
        }
    }

    public function cleanup(): array
    {
        try {
            $cleaned = $this->repository->cleanupOldSessions(7); // 7 dias
            
            $this->logger->info('RPA sessions cleanup completed', ['cleaned' => $cleaned]);
            
            return [
                'success' => true,
                'cleaned' => $cleaned,
                'message' => "Limpeza concluída: {$cleaned} sessões removidas"
            ];
            
        } catch (\Exception $e) {
            $this->logger->error('Failed to cleanup RPA sessions', [
                'error' => $e->getMessage()
            ]);
            
            return [
                'success' => false,
                'error' => 'Erro na limpeza de sessões: ' . $e->getMessage()
            ];
        }
    }

    private function startRPABackground(string $sessionId, array $data): void
    {
        // Criar script de inicialização específico para esta sessão
        $scriptContent = $this->generateStartScript($sessionId, $data);
        $scriptPath = $this->scriptsPath . "/start_rpa_v4_{$sessionId}.sh";
        
        file_put_contents($scriptPath, $scriptContent);
        chmod($scriptPath, 0755);
        
        // Executar em background
        $command = "nohup {$scriptPath} > /dev/null 2>&1 &";
        exec($command);
        
        $this->logger->info('RPA background process started', [
            'session_id' => $sessionId,
            'script_path' => $scriptPath
        ]);
    }

    private function generateStartScript(string $sessionId, array $data): string
    {
        $dataJson = json_encode($data, JSON_UNESCAPED_UNICODE);
        
        return <<<SCRIPT
#!/bin/bash

# Script gerado automaticamente para sessão: {$sessionId}
# Data: $(date)

SESSION_ID="{$sessionId}"
DATA='{$dataJson}'

# Log de início
echo "$(date): Iniciando RPA para sessão \$SESSION_ID" >> /opt/imediatoseguros-rpa/logs/rpa_v4_\$SESSION_ID.log

# Atualizar status para running
echo '{"status": "running", "started_at": "'$(date -Iseconds)'"}' > /opt/imediatoseguros-rpa/sessions/\$SESSION_ID/status.json

# Executar RPA v3 existente (compatibilidade)
cd /opt/imediatoseguros-rpa
/opt/imediatoseguros-rpa/venv/bin/python executar_rpa_modular_telas_1_a_5.py --config /opt/imediatoseguros-rpa/parametros.json --session \$SESSION_ID

# Verificar resultado
if [ \$? -eq 0 ]; then
    echo '{"status": "completed", "completed_at": "'$(date -Iseconds)'"}' > /opt/imediatoseguros-rpa/sessions/\$SESSION_ID/status.json
    echo "$(date): RPA concluído com sucesso para sessão \$SESSION_ID" >> /opt/imediatoseguros-rpa/logs/rpa_v4_\$SESSION_ID.log
else
    echo '{"status": "failed", "failed_at": "'$(date -Iseconds)'"}' > /opt/imediatoseguros-rpa/sessions/\$SESSION_ID/status.json
    echo "$(date): RPA falhou para sessão \$SESSION_ID" >> /opt/imediatoseguros-rpa/logs/rpa_v4_\$SESSION_ID.log
fi

# Limpar script temporário
rm -f "\$0"
SCRIPT;
    }

    private function stopSystemdService(string $sessionId): void
    {
        $serviceName = "rpa-session-{$sessionId}";
        
        // Tentar parar serviço systemd se existir
        exec("systemctl stop {$serviceName} 2>/dev/null", $output, $returnCode);
        
        if ($returnCode === 0) {
            $this->logger->info('Systemd service stopped', [
                'session_id' => $sessionId,
                'service_name' => $serviceName
            ]);
        }
    }
}
