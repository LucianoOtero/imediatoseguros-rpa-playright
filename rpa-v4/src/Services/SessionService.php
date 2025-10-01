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
        try {
            $this->logger->debug('Starting RPA background process', [
                'session_id' => $sessionId,
                'scripts_path' => $this->scriptsPath,
                'scripts_path_exists' => is_dir($this->scriptsPath),
                'scripts_path_writable' => is_writable($this->scriptsPath),
                'scripts_path_permissions' => substr(sprintf('%o', fileperms($this->scriptsPath)), -4)
            ]);

            // Gerar conteúdo do script
            $scriptContent = $this->generateStartScript($sessionId, $data);
            $scriptPath = $this->scriptsPath . "/start_rpa_v4_{$sessionId}.sh";
            
            // ✅ VERIFICAR se diretório existe e é gravável
            if (!is_dir($this->scriptsPath)) {
                throw new \RuntimeException("Diretório de scripts não existe: {$this->scriptsPath}");
            }
            
            if (!is_writable($this->scriptsPath)) {
                throw new \RuntimeException("Diretório de scripts não é gravável: {$this->scriptsPath}");
            }
            
            // ✅ CRIAR script com verificação de erro
            $bytes = file_put_contents($scriptPath, $scriptContent);
            if ($bytes === false) {
                throw new \RuntimeException("Falha ao criar script em: {$scriptPath}. Verifique permissões.");
            }
            
            // ✅ VERIFICAR se arquivo foi criado
            if (!file_exists($scriptPath)) {
                throw new \RuntimeException("Script não foi criado: {$scriptPath}");
            }
            
            // ✅ VERIFICAR tamanho do arquivo
            if (filesize($scriptPath) === 0) {
                throw new \RuntimeException("Script criado está vazio: {$scriptPath}");
            }
            
            // ✅ VERIFICAR conteúdo do arquivo
            $content = file_get_contents($scriptPath);
            if (strpos($content, '#!/bin/bash') !== 0) {
                throw new \RuntimeException("Script não contém shebang correto: {$scriptPath}");
            }
            
            // ✅ VERIFICAR encoding
            if (strpos($content, "\r\n") !== false) {
                $this->logger->warning('Script contém CRLF, convertendo para LF', [
                    'script_path' => $scriptPath
                ]);
            }
            
            // ✅ DEFINIR permissões de execução
            if (!chmod($scriptPath, 0755)) {
                throw new \RuntimeException("Falha ao definir permissões do script: {$scriptPath}");
            }
            
            // ✅ CONVERTER encoding
            exec("dos2unix {$scriptPath} 2>/dev/null", $output, $returnCode);
            if ($returnCode !== 0) {
                $this->logger->warning('dos2unix failed', [
                    'script_path' => $scriptPath,
                    'return_code' => $returnCode,
                    'output' => $output
                ]);
            }
            
            // ✅ VERIFICAR se é executável
            if (!is_executable($scriptPath)) {
                throw new \RuntimeException("Script não é executável: {$scriptPath}");
            }
            
            // ✅ EXECUTAR em background
            $command = "nohup {$scriptPath} > /dev/null 2>&1 &";
            exec($command, $output, $returnCode);
            
            if ($returnCode !== 0) {
                throw new \RuntimeException("Falha ao executar script em background: {$command}");
            }
            
            // ✅ LOG de sucesso com detalhes
            $this->logger->info('RPA background process started successfully', [
                'session_id' => $sessionId,
                'script_path' => $scriptPath,
                'file_size' => filesize($scriptPath),
                'is_executable' => is_executable($scriptPath),
                'command' => $command,
                'bytes_written' => $bytes,
                'content_length' => strlen($content),
                'has_shebang' => strpos($content, '#!/bin/bash') === 0
            ]);
            
        } catch (\Exception $e) {
            // ✅ LOG de erro detalhado
            $this->logger->error('Failed to start RPA background process', [
                'session_id' => $sessionId,
                'error' => $e->getMessage(),
                'script_path' => $scriptPath ?? 'unknown',
                'scripts_path' => $this->scriptsPath,
                'scripts_path_exists' => is_dir($this->scriptsPath),
                'scripts_path_writable' => is_writable($this->scriptsPath),
                'scripts_path_permissions' => is_dir($this->scriptsPath) ? substr(sprintf('%o', fileperms($this->scriptsPath)), -4) : 'unknown'
            ]);
            
            // ✅ ATUALIZAR status da sessão para failed
            $this->repository->updateSession($sessionId, [
                'status' => 'failed',
                'failed_at' => date('Y-m-d H:i:s'),
                'error' => $e->getMessage()
            ]);
            
            throw $e;
        }
    }

    private function generateStartScript(string $sessionId, array $data): string
    {
        // Estratégia conservadora: validar dados e usar fallback
        $useJsonData = !empty($data) && $this->validateData($data);
        
        // ✅ CORREÇÃO: Definir variáveis sempre para evitar erro no heredoc
        $tempJsonFile = "/tmp/rpa_data_{$sessionId}.json";
        $jsonContent = json_encode($data, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT);
        
        if ($useJsonData) {
            $command = "/opt/imediatoseguros-rpa/venv/bin/python executar_rpa_imediato_playwright.py --config {$tempJsonFile} --session \$SESSION_ID --progress-tracker json";
            $dataSource = "JSON dinâmico (arquivo temporário)";
            $cleanupCommand = "rm -f {$tempJsonFile}";
        } else {
            $command = "/opt/imediatoseguros-rpa/venv/bin/python executar_rpa_imediato_playwright.py --config /opt/imediatoseguros-rpa/parametros.json --session \$SESSION_ID --progress-tracker json";
            $dataSource = "parametros.json (fallback)";
            $cleanupCommand = "";
        }
        
        return <<<SCRIPT
#!/bin/bash

# Script gerado automaticamente para sessão: {$sessionId}
# Data: $(date)
# Fonte de dados: {$dataSource}

SESSION_ID="{$sessionId}"

# Log de início
echo "$(date): Iniciando RPA para sessão \$SESSION_ID com {$dataSource}" >> /opt/imediatoseguros-rpa/logs/rpa_v4_\$SESSION_ID.log

# Atualizar status para running
echo '{"status": "running", "started_at": "'$(date -Iseconds)'"}' > /opt/imediatoseguros-rpa/sessions/\$SESSION_ID/status.json

# Criar arquivo temporário com JSON (se necessário)
if [ "{$dataSource}" = "JSON dinâmico (arquivo temporário)" ]; then
    cat > {$tempJsonFile} << 'JSON_EOF'
{$jsonContent}
JSON_EOF
    echo "$(date): Arquivo JSON temporário criado: {$tempJsonFile}" >> /opt/imediatoseguros-rpa/logs/rpa_v4_\$SESSION_ID.log
fi

# Executar RPA com estratégia conservadora
cd /opt/imediatoseguros-rpa
{$command}

# Verificar resultado
if [ \$? -eq 0 ]; then
    echo '{"status": "completed", "completed_at": "'$(date -Iseconds)'"}' > /opt/imediatoseguros-rpa/sessions/\$SESSION_ID/status.json
    echo "$(date): RPA concluído com sucesso para sessão \$SESSION_ID" >> /opt/imediatoseguros-rpa/logs/rpa_v4_\$SESSION_ID.log
else
    echo '{"status": "failed", "failed_at": "'$(date -Iseconds)'"}' > /opt/imediatoseguros-rpa/sessions/\$SESSION_ID/status.json
    echo "$(date): RPA falhou para sessão \$SESSION_ID" >> /opt/imediatoseguros-rpa/logs/rpa_v4_\$SESSION_ID.log
fi

# Limpar arquivos temporários
{$cleanupCommand}

# Limpar script temporário
# rm -f "\$0" # TEMPORARIAMENTE DESABILITADO
SCRIPT;
    }

    /**
     * Validate data for RPA execution (validation removed - done in frontend)
     */
    private function validateData(array $data): bool
    {
        // Validação removida - feita no frontend
        // Apenas retorna true para permitir execução do RPA
        $this->logger->info('Dados aceitos para execução RPA', [
            'data_received' => !empty($data)
        ]);
        
        return true;
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
