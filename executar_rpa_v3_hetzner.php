<?php
/**
 * EXECUTAR RPA V3 - Sistema de Execução em Background com Systemd
 * 
 * Versão 3.0.0 - Implementação completa com systemd
 * 
 * Funcionalidades:
 * - Execução em background via systemd
 * - Monitoramento em tempo real
 * - JSON tracker automático
 * - Logs progressivos por tela
 * - Múltiplas sessões simultâneas
 * - API REST completa
 * 
 * @author Sistema RPA Imediato
 * @version 3.0.0
 * @date 2024-12-29
 */

class RPAControllerV3 {
    private $sessionsDir = '/opt/imediatoseguros-rpa/sessions';
    private $systemdDir = '/opt/imediatoseguros-rpa/systemd';
    private $scriptsDir = '/opt/imediatoseguros-rpa/scripts';
    private $baseDir = '/opt/imediatoseguros-rpa';
    
    public function __construct() {
        // Criar diretórios se não existirem
        $this->createDirectories();
    }
    
    /**
     * Iniciar execução RPA
     */
    public function startRPA($data = null) {
        try {
            // 1. Gerar session ID simples
            $sessionId = 'rpa_v3_' . date('Ymd_His') . '_' . substr(md5(uniqid()), 0, 8);
            
            // 2. Executar script de start (usando parametros.json existente)
            $command = "{$this->scriptsDir}/start_rpa_v3.sh {$sessionId} {$this->baseDir}/parametros.json 2>&1";
            $output = shell_exec($command);
            
            // 3. Aguardar inicialização
            $this->waitForStartup($sessionId);
            
            return [
                'success' => true,
                'session_id' => $sessionId,
                'message' => 'RPA iniciado com sucesso',
                'timestamp' => date('Y-m-d H:i:s'),
                'output' => $output
            ];
            
        } catch (Exception $e) {
            return [
                'success' => false,
                'error' => $e->getMessage(),
                'timestamp' => date('Y-m-d H:i:s')
            ];
        }
    }
    
    /**
     * Obter status da execução
     */
    public function getStatus($sessionId) {
        try {
            $command = "{$this->scriptsDir}/monitor_rpa_v3.sh {$sessionId} 2>&1";
            $output = shell_exec($command);
            
            $data = json_decode($output, true);
            
            if (!$data) {
                throw new Exception("Erro ao decodificar dados de monitoramento: " . $output);
            }
            
            return [
                'success' => true,
                'data' => $data,
                'timestamp' => date('Y-m-d H:i:s')
            ];
            
        } catch (Exception $e) {
            return [
                'success' => false,
                'error' => $e->getMessage(),
                'timestamp' => date('Y-m-d H:i:s')
            ];
        }
    }
    
    /**
     * Parar execução RPA
     */
    public function stopRPA($sessionId) {
        try {
            // Parar serviço
            shell_exec("systemctl stop rpa-session-{$sessionId} 2>&1");
            
            // Remover service unit
            shell_exec("rm -f /etc/systemd/system/rpa-session-{$sessionId}.service 2>&1");
            shell_exec("systemctl daemon-reload 2>&1");
            
            return [
                'success' => true,
                'message' => 'RPA parado com sucesso',
                'timestamp' => date('Y-m-d H:i:s')
            ];
            
        } catch (Exception $e) {
            return [
                'success' => false,
                'error' => $e->getMessage(),
                'timestamp' => date('Y-m-d H:i:s')
            ];
        }
    }
    
    /**
     * Listar sessões ativas
     */
    public function listSessions() {
        try {
            $sessions = [];
            $dir = opendir($this->sessionsDir);
            
            while (($file = readdir($dir)) !== false) {
                if ($file != '.' && $file != '..' && is_dir("{$this->sessionsDir}/{$file}")) {
                    $statusFile = "{$this->sessionsDir}/{$file}/status.json";
                    if (file_exists($statusFile)) {
                        $status = json_decode(file_get_contents($statusFile), true);
                        $sessions[] = [
                            'session_id' => $file,
                            'status' => $status['status'] ?? 'unknown',
                            'timestamp' => $status['timestamp'] ?? 'unknown'
                        ];
                    }
                }
            }
            closedir($dir);
            
            return [
                'success' => true,
                'sessions' => $sessions,
                'timestamp' => date('Y-m-d H:i:s')
            ];
            
        } catch (Exception $e) {
            return [
                'success' => false,
                'error' => $e->getMessage(),
                'timestamp' => date('Y-m-d H:i:s')
            ];
        }
    }
    
    /**
     * Health check do sistema
     */
    public function healthCheck() {
        try {
            $checks = [];
            
            // Verificar diretórios
            $checks['directories'] = [
                'sessions' => is_dir($this->sessionsDir),
                'systemd' => is_dir($this->systemdDir),
                'scripts' => is_dir($this->scriptsDir)
            ];
            
            // Verificar scripts
            $checks['scripts'] = [
                'start_rpa_v3.sh' => is_executable("{$this->scriptsDir}/start_rpa_v3.sh"),
                'monitor_rpa_v3.sh' => is_executable("{$this->scriptsDir}/monitor_rpa_v3.sh")
            ];
            
            // Verificar Python e venv
            $checks['python'] = [
                'venv_exists' => is_dir("{$this->baseDir}/venv"),
                'python_executable' => is_executable("{$this->baseDir}/venv/bin/python"),
                'modular_script' => file_exists("{$this->baseDir}/executar_rpa_modular_telas_1_a_5.py")
            ];
            
            // Verificar systemd
            $systemdStatus = shell_exec("systemctl is-system-running 2>&1");
            $checks['systemd'] = [
                'running' => trim($systemdStatus) === 'running',
                'status' => trim($systemdStatus)
            ];
            
            $allHealthy = true;
            foreach ($checks as $category => $items) {
                foreach ($items as $item => $status) {
                    if (!$status) {
                        $allHealthy = false;
                        break 2;
                    }
                }
            }
            
            return [
                'success' => true,
                'healthy' => $allHealthy,
                'checks' => $checks,
                'timestamp' => date('Y-m-d H:i:s')
            ];
            
        } catch (Exception $e) {
            return [
                'success' => false,
                'error' => $e->getMessage(),
                'timestamp' => date('Y-m-d H:i:s')
            ];
        }
    }
    
    /**
     * Criar diretórios necessários
     */
    private function createDirectories() {
        $dirs = [
            $this->sessionsDir,
            $this->systemdDir,
            $this->scriptsDir
        ];
        
        foreach ($dirs as $dir) {
            if (!is_dir($dir)) {
                mkdir($dir, 0755, true);
            }
        }
    }
    
    
    /**
     * Aguardar inicialização do serviço
     */
    private function waitForStartup($sessionId, $timeout = 30) {
        $startTime = time();
        
        while (time() - $startTime < $timeout) {
            $status = shell_exec("systemctl is-active rpa-session-{$sessionId} 2>&1");
            
            if (trim($status) === 'active') {
                return true;
            }
            
            sleep(1);
        }
        
        throw new Exception("Timeout aguardando inicialização do RPA (30s)");
    }
}

// API REST
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, PUT, DELETE');
header('Access-Control-Allow-Headers: Content-Type');

$method = $_SERVER['REQUEST_METHOD'];
$action = $_GET['action'] ?? null;
$sessionId = $_GET['session_id'] ?? null;

$controller = new RPAControllerV3();

try {
    switch ($method) {
        case 'POST':
            $result = $controller->startRPA();
            echo json_encode($result, JSON_PRETTY_PRINT);
            break;
            
        case 'GET':
            if ($action === 'status' && $sessionId) {
                $result = $controller->getStatus($sessionId);
                echo json_encode($result, JSON_PRETTY_PRINT);
            } elseif ($action === 'sessions') {
                $result = $controller->listSessions();
                echo json_encode($result, JSON_PRETTY_PRINT);
            } elseif ($action === 'health') {
                $result = $controller->healthCheck();
                echo json_encode($result, JSON_PRETTY_PRINT);
            } else {
                http_response_code(400);
                echo json_encode(['error' => 'Ação não especificada ou parâmetros faltando']);
            }
            break;
            
        case 'DELETE':
            if ($action === 'stop' && $sessionId) {
                $result = $controller->stopRPA($sessionId);
                echo json_encode($result, JSON_PRETTY_PRINT);
            } else {
                http_response_code(400);
                echo json_encode(['error' => 'Ação não especificada ou parâmetros faltando']);
            }
            break;
            
        default:
            http_response_code(405);
            echo json_encode(['error' => 'Método não permitido']);
            break;
    }
    
} catch (Exception $e) {
    http_response_code(500);
    echo json_encode([
        'success' => false,
        'error' => $e->getMessage(),
        'timestamp' => date('Y-m-d H:i:s')
    ]);
}
?>
