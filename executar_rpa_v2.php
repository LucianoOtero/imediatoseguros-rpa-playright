<?php
/**
 * EXECUTAR RPA V2 - API PHP AVANÇADA
 * Sistema completo com controle de ambiente, logs detalhados e monitoramento
 * Versão: 2.0.0
 * Data: 2025-01-10
 */

// Headers de segurança e cache
header('Cache-Control: no-cache, must-revalidate');
header('Expires: Mon, 26 Jul 1997 05:00:00 GMT');
header('Content-Type: application/json; charset=utf-8');
header('X-Content-Type-Options: nosniff');
header('X-Frame-Options: DENY');

// Configurações globais
define('RPA_SCRIPT', 'executar_rpa_modular_telas_1_a_5.py');
define('BASE_DIR', '/opt/imediatoseguros-rpa');
define('LOGS_DIR', BASE_DIR . '/logs');
define('TEMP_DIR', BASE_DIR . '/temp');
define('PYTHON_VENV', BASE_DIR . '/venv/bin/python');
define('DEFAULT_TIMEOUT', 300); // 5 minutos
define('MAX_RETRIES', 3);

// Classe principal do sistema
class RPAController {
    private $logger;
    private $environment;
    private $sessionId;
    private $startTime;
    
    public function __construct() {
        $this->startTime = microtime(true);
        $this->sessionId = $this->generateSessionId();
        $this->logger = new RPALogger($this->sessionId);
        $this->environment = new EnvironmentController();
        
        $this->logger->info("Sistema RPA V2 inicializado", [
            'session_id' => $this->sessionId,
            'timestamp' => date('Y-m-d H:i:s'),
            'memory_usage' => memory_get_usage(true)
        ]);
    }
    
    public function execute($action, $data = []) {
        try {
            switch ($action) {
                case 'start':
                    return $this->startRPA($data);
                case 'status':
                    return $this->getStatus($data['session_id'] ?? $this->sessionId);
                case 'stop':
                    return $this->stopRPA($data['session_id'] ?? $this->sessionId);
                case 'health':
                    return $this->healthCheck();
                default:
                    throw new Exception("Ação não reconhecida: $action");
            }
        } catch (Exception $e) {
            $this->logger->error("Erro na execução", [
                'action' => $action,
                'error' => $e->getMessage(),
                'trace' => $e->getTraceAsString()
            ]);
            
            return [
                'success' => false,
                'error' => $e->getMessage(),
                'session_id' => $this->sessionId,
                'timestamp' => date('Y-m-d H:i:s')
            ];
        }
    }
    
    private function startRPA($data) {
        $this->logger->info("Iniciando execução RPA", $data);
        
        // 1. Validação de entrada
        $validation = $this->validateInput($data);
        if (!$validation['valid']) {
            throw new Exception("Dados inválidos: " . implode(', ', $validation['errors']));
        }
        
        // 2. Verificação de ambiente
        $envCheck = $this->environment->validateEnvironment();
        if (!$envCheck['valid']) {
            throw new Exception("Ambiente inválido: " . implode(', ', $envCheck['errors']));
        }
        
        // 3. Criação de parâmetros temporários
        $tempParams = $this->createTempParameters($data);
        
        // 4. Execução controlada
        $result = $this->executeWithMonitoring($tempParams);
        
        // 5. Limpeza assíncrona (após 5 minutos)
        $this->scheduleCleanup($tempParams);
        
        return $result;
    }
    
    private function validateInput($data) {
        $errors = [];
        
        // Campos obrigatórios
        $required = ['placa', 'marca', 'modelo', 'ano'];
        foreach ($required as $field) {
            if (empty($data[$field])) {
                $errors[] = "Campo obrigatório ausente: $field";
            }
        }
        
        // Validação de placa
        if (!empty($data['placa']) && !preg_match('/^[A-Z]{3}[0-9]{4}$/', $data['placa'])) {
            $errors[] = "Formato de placa inválido";
        }
        
        // Validação de ano
        if (!empty($data['ano']) && ($data['ano'] < 1990 || $data['ano'] > date('Y') + 1)) {
            $errors[] = "Ano inválido";
        }
        
        return [
            'valid' => empty($errors),
            'errors' => $errors
        ];
    }
    
    private function createTempParameters($data) {
        $tempFile = TEMP_DIR . '/parametros_' . $this->sessionId . '.json';
        
        // Carregar template base
        $template = json_decode(file_get_contents(BASE_DIR . '/parametros.json'), true);
        
        // Atualizar com dados fornecidos
        $template['placa'] = $data['placa'];
        $template['marca'] = $data['marca'];
        $template['modelo'] = $data['modelo'];
        $template['ano'] = $data['ano'];
        
        // Campos opcionais
        if (!empty($data['cep'])) $template['cep'] = $data['cep'];
        if (!empty($data['nome'])) $template['nome'] = $data['nome'];
        if (!empty($data['cpf'])) $template['cpf'] = $data['cpf'];
        if (!empty($data['email'])) $template['email'] = $data['email'];
        if (!empty($data['celular'])) $template['celular'] = $data['celular'];
        
        // Salvar arquivo temporário
        file_put_contents($tempFile, json_encode($template, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE));
        
        $this->logger->info("Arquivo de parâmetros temporário criado", [
            'file' => $tempFile,
            'size' => filesize($tempFile)
        ]);
        
        return $tempFile;
    }
    
    private function executeWithMonitoring($tempParams) {
        $command = $this->buildCommand($tempParams);
        
        $this->logger->info("Executando comando RPA", [
            'command' => $command,
            'timeout' => DEFAULT_TIMEOUT
        ]);
        
        // Executar em background com monitoramento
        $pid = $this->executeBackground($command);
        
        if (!$pid) {
            throw new Exception("Falha ao iniciar processo RPA");
        }
        
        // Aguardar mais tempo para verificar se o processo iniciou corretamente
        sleep(10);
        
        if (!$this->isProcessRunning($pid)) {
            throw new Exception("Processo RPA falhou ao iniciar");
        }
        
        return [
            'success' => true,
            'message' => 'RPA iniciado com sucesso',
            'session_id' => $this->sessionId,
            'pid' => $pid,
            'command' => $command,
            'timestamp' => date('Y-m-d H:i:s')
        ];
    }
    
    private function buildCommand($tempParams) {
        $env = $this->environment->getEnvironmentVariables();
        $envString = '';
        
        foreach ($env as $key => $value) {
            $envString .= "$key=" . escapeshellarg($value) . ' ';
        }
        
        $command = 'xvfb-run -a ' . PYTHON_VENV . ' ' .
                  BASE_DIR . '/' . RPA_SCRIPT . ' ' .
                  '--config ' . escapeshellarg($tempParams) . ' ' .
                  '--session ' . escapeshellarg($this->sessionId) . ' ' .
                  '--progress-tracker json ' .
                  '--modo-silencioso ' .
                  '2>&1';
        
        return $command;
    }
    
    private function executeBackground($command) {
        $logFile = LOGS_DIR . '/rpa_execution_' . $this->sessionId . '.log';
        $env = $this->environment->getEnvironmentVariables();
        
        // Criar script temporário com variáveis de ambiente
        $scriptFile = TEMP_DIR . '/exec_rpa_' . $this->sessionId . '.sh';
        $scriptContent = "#!/bin/bash\n";
        $scriptContent .= "set -e\n"; // Parar em caso de erro
        $scriptContent .= "exec 2>&1\n"; // Redirecionar stderr para stdout
        
        // Adicionar variáveis de ambiente
        foreach ($env as $key => $value) {
            $scriptContent .= "export $key=" . escapeshellarg($value) . "\n";
        }
        
        // Adicionar comando
        $scriptContent .= "$command\n";
        
        // Salvar script
        file_put_contents($scriptFile, $scriptContent);
        chmod($scriptFile, 0755);
        
        // Executar script em background
        $fullCommand = "nohup $scriptFile > $logFile 2>&1 & echo $!";
        
        $pid = trim(shell_exec($fullCommand));
        
        $this->logger->info("Processo iniciado em background", [
            'pid' => $pid,
            'log_file' => $logFile,
            'script_file' => $scriptFile,
            'full_command' => $fullCommand
        ]);
        
        return $pid;
    }
    
    private function isProcessRunning($pid) {
        $result = shell_exec("ps -p $pid -o pid= 2>/dev/null");
        return !empty(trim($result));
    }
    
    private function getStatus($sessionId) {
        $this->logger->info("Verificando status", ['session_id' => $sessionId]);
        
        // Verificar arquivos de progresso em rpa_data
        $progressFiles = glob(BASE_DIR . '/rpa_data/progress_*' . $sessionId . '*.json');
        
        if (empty($progressFiles)) {
            // Tentar também em temp
            $progressFiles = glob(TEMP_DIR . '/progress_*' . $sessionId . '*.json');
        }
        
        if (empty($progressFiles)) {
            return [
                'success' => false,
                'error' => 'Nenhum arquivo de progresso encontrado',
                'session_id' => $sessionId
            ];
        }
        
        // Pegar o arquivo mais recente
        $latestFile = max($progressFiles);
        $content = file_get_contents($latestFile);
        $data = json_decode($content, true);
        
        if (!$data) {
            return [
                'success' => false,
                'error' => 'Erro ao decodificar dados de progresso',
                'session_id' => $sessionId
            ];
        }
        
        // Verificar se há estimativas
        $estimatesFile = glob(TEMP_DIR . '/json_compreensivo_tela_5_*' . $sessionId . '*.json');
        $hasEstimates = !empty($estimatesFile);
        
        return [
            'success' => true,
            'data' => $data,
            'has_estimates' => $hasEstimates,
            'estimates_file' => $hasEstimates ? basename($estimatesFile[0]) : null,
            'progress_file' => basename($latestFile),
            'session_id' => $sessionId,
            'timestamp' => date('Y-m-d H:i:s')
        ];
    }
    
    private function stopRPA($sessionId) {
        $this->logger->info("Parando execução RPA", ['session_id' => $sessionId]);
        
        // Encontrar e matar processo
        $pid = $this->findProcessBySession($sessionId);
        
        if ($pid) {
            shell_exec("kill $pid 2>/dev/null");
            $this->logger->info("Processo parado", ['pid' => $pid]);
        }
        
        return [
            'success' => true,
            'message' => 'RPA parado com sucesso',
            'session_id' => $sessionId,
            'timestamp' => date('Y-m-d H:i:s')
        ];
    }
    
    private function healthCheck() {
        $this->logger->info("Executando health check");
        
        $health = [
            'timestamp' => date('Y-m-d H:i:s'),
            'system' => [
                'php_version' => PHP_VERSION,
                'memory_usage' => memory_get_usage(true),
                'memory_limit' => ini_get('memory_limit'),
                'disk_space' => disk_free_space(BASE_DIR)
            ],
            'environment' => $this->environment->getHealthStatus(),
            'files' => [
                'rpa_script_exists' => file_exists(BASE_DIR . '/' . RPA_SCRIPT),
                'python_venv_exists' => file_exists(PYTHON_VENV),
                'logs_dir_writable' => is_writable(LOGS_DIR),
                'temp_dir_writable' => is_writable(TEMP_DIR)
            ]
        ];
        
        return [
            'success' => true,
            'health' => $health
        ];
    }
    
    private function findProcessBySession($sessionId) {
        $result = shell_exec("ps aux | grep '$sessionId' | grep -v grep | awk '{print $2}'");
        return trim($result);
    }
    
    private function scheduleCleanup($tempParams) {
        // Agendar limpeza assíncrona após 5 minutos
        $scriptFile = TEMP_DIR . '/exec_rpa_' . $this->sessionId . '.sh';
        $cleanupCommand = "(sleep 300; rm -f " . escapeshellarg($tempParams) . " " . escapeshellarg($scriptFile) . ") &";
        
        shell_exec($cleanupCommand);
        
        $this->logger->info("Limpeza assíncrona agendada", [
            'temp_params' => $tempParams,
            'script_file' => $scriptFile,
            'delay' => '300 segundos'
        ]);
    }
    
    private function cleanup($tempParams) {
        if (file_exists($tempParams)) {
            unlink($tempParams);
            $this->logger->info("Arquivo temporário removido", ['file' => $tempParams]);
        }
        
        // Limpar script temporário
        $scriptFile = TEMP_DIR . '/exec_rpa_' . $this->sessionId . '.sh';
        if (file_exists($scriptFile)) {
            unlink($scriptFile);
            $this->logger->info("Script temporário removido", ['file' => $scriptFile]);
        }
    }
    
    private function generateSessionId() {
        return 'rpa_v2_' . date('Ymd_His') . '_' . substr(md5(uniqid()), 0, 8);
    }
}

// Classe de controle de ambiente
class EnvironmentController {
    private $environment;
    
    public function __construct() {
        $this->environment = [
            'PATH' => '/opt/imediatoseguros-rpa/venv/bin:/usr/local/bin:/usr/bin:/bin',
            'PYTHONPATH' => '/opt/imediatoseguros-rpa',
            'DISPLAY' => ':99',
            'HOME' => '/opt/imediatoseguros-rpa',
            'USER' => 'root',
            'PWD' => '/opt/imediatoseguros-rpa',
            'LANG' => 'C',
            'LC_ALL' => 'C'
        ];
    }
    
    public function validateEnvironment() {
        $errors = [];
        
        // Verificar Python
        if (!file_exists(PYTHON_VENV)) {
            $errors[] = 'Python virtual environment não encontrado';
        }
        
        // Verificar arquivo RPA
        if (!file_exists(BASE_DIR . '/' . RPA_SCRIPT)) {
            $errors[] = 'Arquivo RPA não encontrado';
        }
        
        // Verificar diretórios
        if (!is_dir(LOGS_DIR)) {
            $errors[] = 'Diretório de logs não existe';
        }
        
        if (!is_dir(TEMP_DIR)) {
            $errors[] = 'Diretório temporário não existe';
        }
        
        // Verificar permissões
        if (!is_writable(LOGS_DIR)) {
            $errors[] = 'Diretório de logs não é gravável';
        }
        
        if (!is_writable(TEMP_DIR)) {
            $errors[] = 'Diretório temporário não é gravável';
        }
        
        return [
            'valid' => empty($errors),
            'errors' => $errors
        ];
    }
    
    public function getEnvironmentVariables() {
        return $this->environment;
    }
    
    public function getHealthStatus() {
        return [
            'python_available' => file_exists(PYTHON_VENV),
            'rpa_script_available' => file_exists(BASE_DIR . '/' . RPA_SCRIPT),
            'redis_available' => $this->checkRedis(),
            'xvfb_available' => $this->checkXvfb()
        ];
    }
    
    private function checkRedis() {
        $result = shell_exec("redis-cli ping 2>/dev/null");
        return trim($result) === 'PONG';
    }
    
    private function checkXvfb() {
        $result = shell_exec("which xvfb-run 2>/dev/null");
        return !empty(trim($result));
    }
}

// Classe de logging
class RPALogger {
    private $sessionId;
    private $logFile;
    
    public function __construct($sessionId) {
        $this->sessionId = $sessionId;
        $this->logFile = LOGS_DIR . '/rpa_v2_' . date('Y-m-d') . '.log';
        
        // Criar diretório de logs se não existir
        if (!is_dir(LOGS_DIR)) {
            mkdir(LOGS_DIR, 0755, true);
        }
    }
    
    public function info($message, $context = []) {
        $this->log('INFO', $message, $context);
    }
    
    public function error($message, $context = []) {
        $this->log('ERROR', $message, $context);
    }
    
    public function warning($message, $context = []) {
        $this->log('WARNING', $message, $context);
    }
    
    public function debug($message, $context = []) {
        $this->log('DEBUG', $message, $context);
    }
    
    private function log($level, $message, $context = []) {
        $timestamp = date('Y-m-d H:i:s');
        $contextStr = !empty($context) ? ' ' . json_encode($context, JSON_UNESCAPED_UNICODE) : '';
        $logEntry = "[$timestamp] [$level] [SESSION:$this->sessionId] $message$contextStr\n";
        
        file_put_contents($this->logFile, $logEntry, FILE_APPEND | LOCK_EX);
    }
}

// Execução principal
try {
    // Verificar método HTTP
    if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
        throw new Exception('Método não permitido. Use POST.');
    }
    
    // Obter dados
    $input = json_decode(file_get_contents('php://input'), true);
    if (!$input) {
        $input = $_POST;
    }
    
    $action = $input['action'] ?? 'start';
    $data = $input['dados'] ?? $input;
    
    // Criar controlador e executar
    $controller = new RPAController();
    $result = $controller->execute($action, $data);
    
    // Retornar resultado
    echo json_encode($result, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
    
} catch (Exception $e) {
    // Log de erro crítico
    error_log("RPA V2 Critical Error: " . $e->getMessage());
    
    // Resposta de erro
    echo json_encode([
        'success' => false,
        'error' => 'Erro interno do servidor',
        'timestamp' => date('Y-m-d H:i:s')
    ], JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
}
?>
