<?php
/**
 * Sistema de Logging PHP com Banco de Dados
 * Versão: 1.0.0
 * Data: 2025-10-20
 * 
 * Recebe logs via POST JSON e armazena em banco de dados MySQL
 * para análise profunda do fluxo de execução do RPA
 */

// Configurações de segurança
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

// Tratar requisições OPTIONS (CORS preflight)
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit(0);
}

// Verificar método HTTP
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['error' => 'Method not allowed', 'method' => $_SERVER['REQUEST_METHOD']]);
    exit;
}

// Configurações do banco de dados
$db_config = [
    'host' => 'localhost',
    'port' => 3306,
    'database' => 'mdmidiac_rpa_logs',
    'username' => 'mdmidiac',
    'password' => 'senha_temporaria_123'
];

// Função para conectar ao banco
function connectDatabase($config) {
    try {
        $dsn = "mysql:host={$config['host']};port={$config['port']};dbname={$config['database']};charset=utf8mb4";
        $pdo = new PDO($dsn, $config['username'], $config['password'], [
            PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
            PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
            PDO::ATTR_EMULATE_PREPARES => false
        ]);
        return $pdo;
    } catch (PDOException $e) {
        error_log("Database connection failed: " . $e->getMessage());
        return null;
    }
}

// Função para criar tabela se não existir
function createTableIfNotExists($pdo) {
    $sql = "
        CREATE TABLE IF NOT EXISTS logs (
            id INT AUTO_INCREMENT PRIMARY KEY,
            log_id VARCHAR(50) NOT NULL,
            timestamp DATETIME NOT NULL,
            client_timestamp VARCHAR(50),
            level ENUM('DEBUG', 'INFO', 'WARNING', 'ERROR') NOT NULL,
            message TEXT NOT NULL,
            data JSON,
            url VARCHAR(500),
            session_id VARCHAR(100),
            user_agent TEXT,
            ip_address VARCHAR(45),
            server_time DECIMAL(15,6),
            request_id VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            INDEX idx_log_id (log_id),
            INDEX idx_timestamp (timestamp),
            INDEX idx_level (level),
            INDEX idx_session_id (session_id),
            INDEX idx_ip_address (ip_address)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    ";
    
    try {
        $pdo->exec($sql);
        return true;
    } catch (PDOException $e) {
        error_log("Table creation failed: " . $e->getMessage());
        return false;
    }
}

// Função para inserir log no banco
function insertLog($pdo, $logData) {
    $sql = "
        INSERT INTO logs (
            log_id, timestamp, client_timestamp, level, message, data,
            url, session_id, user_agent, ip_address, server_time, request_id
        ) VALUES (
            :log_id, :timestamp, :client_timestamp, :level, :message, :data,
            :url, :session_id, :user_agent, :ip_address, :server_time, :request_id
        )
    ";
    
    try {
        $stmt = $pdo->prepare($sql);
        $stmt->execute($logData);
        return $stmt->rowCount();
    } catch (PDOException $e) {
        error_log("Log insertion failed: " . $e->getMessage());
        return false;
    }
}

// Função para fallback em arquivo
function fallbackToFile($logData) {
    $logFile = 'debug_rpa_fallback.log';
    $logLine = json_encode($logData, JSON_UNESCAPED_UNICODE) . "\n";
    return file_put_contents($logFile, $logLine, FILE_APPEND | LOCK_EX);
}

// Rate limiting simples
function checkRateLimit($ip) {
    $rateFile = 'rate_limit_' . md5($ip) . '.tmp';
    $now = time();
    $window = 60; // 1 minuto
    $maxRequests = 100; // máximo 100 requests por minuto
    
    if (file_exists($rateFile)) {
        $data = json_decode(file_get_contents($rateFile), true);
        if ($now - $data['first_request'] < $window) {
            if ($data['count'] >= $maxRequests) {
                return false;
            }
            $data['count']++;
        } else {
            $data = ['first_request' => $now, 'count' => 1];
        }
    } else {
        $data = ['first_request' => $now, 'count' => 1];
    }
    
    file_put_contents($rateFile, json_encode($data));
    return true;
}

// Início do processamento
try {
    // Ler dados JSON
    $input = json_decode(file_get_contents('php://input'), true);
    
    if (!$input) {
        http_response_code(400);
        echo json_encode(['error' => 'Invalid JSON input']);
        exit;
    }
    
    // Validar campos obrigatórios
    if (!isset($input['message']) || !isset($input['level'])) {
        http_response_code(400);
        echo json_encode(['error' => 'Missing required fields: message and level']);
        exit;
    }
    
    // Rate limiting
    $clientIP = $_SERVER['REMOTE_ADDR'] ?? 'unknown';
    if (!checkRateLimit($clientIP)) {
        http_response_code(429);
        echo json_encode(['error' => 'Rate limit exceeded']);
        exit;
    }
    
    // Preparar dados do log
    $logId = $input['logId'] ?? uniqid('log_', true);
    $logData = [
        'log_id' => $logId,
        'timestamp' => date('Y-m-d H:i:s'),
        'client_timestamp' => $input['timestamp'] ?? date('c'),
        'level' => strtoupper($input['level']),
        'message' => $input['message'],
        'data' => isset($input['data']) ? json_encode($input['data']) : null,
        'url' => $input['url'] ?? ($_SERVER['HTTP_REFERER'] ?? 'unknown'),
        'session_id' => $input['sessionId'] ?? 'unknown',
        'user_agent' => $input['userAgent'] ?? ($_SERVER['HTTP_USER_AGENT'] ?? 'unknown'),
        'ip_address' => $clientIP,
        'server_time' => microtime(true),
        'request_id' => uniqid('req_', true)
    ];
    
    // Tentar conectar ao banco de dados
    $pdo = connectDatabase($db_config);
    
    if ($pdo) {
        // Criar tabela se necessário
        createTableIfNotExists($pdo);
        
        // Inserir log no banco
        $result = insertLog($pdo, $logData);
        
        if ($result !== false) {
            // Sucesso - log inserido no banco
            echo json_encode([
                'success' => true,
                'method' => 'database',
                'logged' => $logData,
                'rows_affected' => $result
            ], JSON_UNESCAPED_UNICODE);
        } else {
            // Falha na inserção - fallback para arquivo
            $fallbackResult = fallbackToFile($logData);
            echo json_encode([
                'success' => true,
                'method' => 'file_fallback',
                'logged' => $logData,
                'bytes_written' => $fallbackResult
            ], JSON_UNESCAPED_UNICODE);
        }
    } else {
        // Falha na conexão - fallback para arquivo
        $fallbackResult = fallbackToFile($logData);
        echo json_encode([
            'success' => true,
            'method' => 'file_fallback',
            'logged' => $logData,
            'bytes_written' => $fallbackResult
        ], JSON_UNESCAPED_UNICODE);
    }
    
} catch (Exception $e) {
    // Erro geral - fallback para arquivo
    $logData = [
        'log_id' => uniqid('log_', true),
        'timestamp' => date('Y-m-d H:i:s'),
        'level' => 'ERROR',
        'message' => 'System error: ' . $e->getMessage(),
        'data' => json_encode($input ?? []),
        'ip_address' => $_SERVER['REMOTE_ADDR'] ?? 'unknown',
        'server_time' => microtime(true),
        'request_id' => uniqid('req_', true)
    ];
    
    $fallbackResult = fallbackToFile($logData);
    
    http_response_code(500);
    echo json_encode([
        'success' => false,
        'error' => 'System error occurred',
        'method' => 'file_fallback',
        'bytes_written' => $fallbackResult
    ], JSON_UNESCAPED_UNICODE);
}
?>
