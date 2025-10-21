<?php
/**
 * debug_logger_db.php - Sistema de Logging para Debug RPA
 * Hospedado em: https://mdmidia.com.br/logging_system/debug_logger_db.php
 * 
 * Funcionalidade:
 * - Recebe logs via POST JSON
 * - Grava em banco de dados MySQL
 * - Suporte a CORS para requisições do Webflow
 * - Identificação completa de usuário e sessão
 * - Validação rigorosa de entrada
 * - Rate limiting para proteção
 */

// Configurar headers para CORS
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type, X-Requested-With');

// Responder a requisições OPTIONS (preflight)
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

// Incluir configurações
require_once __DIR__ . '/config/database.php';
require_once __DIR__ . '/config/security.php';
require_once __DIR__ . '/utils/helpers.php';

try {
    // Verificar rate limiting
    if (!checkRateLimit()) {
        http_response_code(429);
        echo json_encode(['error' => 'Rate limit exceeded']);
        exit;
    }
    
    // Ler dados JSON do corpo da requisição
    $input = json_decode(file_get_contents('php://input'), true);
    
    // Validar entrada
    $validation_result = validateInput($input);
    if (!$validation_result['valid']) {
        http_response_code(400);
        echo json_encode(['error' => 'Invalid input', 'details' => $validation_result['errors']]);
        exit;
    }
    
    // Gerar ID único para este log se não fornecido
    $logId = $input['logId'] ?? uniqid('log_', true);
    
    // Obter informações do cliente
    $clientInfo = getClientInfo();
    
    // Construir entrada do log com informações completas
    $logEntry = [
        'log_id' => $logId,
        'session_id' => $input['sessionId'] ?? uniqid('sess_', true),
        'timestamp' => date('Y-m-d H:i:s'),
        'client_timestamp' => $input['timestamp'] ?? date('c'),
        'level' => strtoupper($input['level']),
        'message' => sanitizeString($input['message']),
        'data' => $input['data'] ?? null,
        'url' => $input['url'] ?? $clientInfo['url'],
        'user_agent' => $input['userAgent'] ?? $clientInfo['user_agent'],
        'ip_address' => $clientInfo['ip_address'],
        'server_time' => microtime(true),
        'request_id' => uniqid('req_', true)
    ];
    
    // Limitar tamanho dos dados para evitar logs muito grandes
    if (isset($logEntry['data']) && is_string($logEntry['data']) && strlen($logEntry['data']) > 10000) {
        $logEntry['data'] = substr($logEntry['data'], 0, 10000) . '...[TRUNCATED]';
    }
    
    // Converter dados para JSON se necessário
    if (is_array($logEntry['data']) || is_object($logEntry['data'])) {
        $logEntry['data'] = json_encode($logEntry['data'], JSON_UNESCAPED_UNICODE);
    }
    
    // Conectar ao banco de dados
    $pdo = getDatabaseConnection();
    
    // Preparar statement para inserção
    $stmt = $pdo->prepare("
        INSERT INTO debug_logs (
            log_id, session_id, timestamp, client_timestamp, level, message, 
            data, url, user_agent, ip_address, server_time, request_id
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ");
    
    // Executar inserção
    $result = $stmt->execute([
        $logEntry['log_id'],
        $logEntry['session_id'],
        $logEntry['timestamp'],
        $logEntry['client_timestamp'],
        $logEntry['level'],
        $logEntry['message'],
        $logEntry['data'],
        $logEntry['url'],
        $logEntry['user_agent'],
        $logEntry['ip_address'],
        $logEntry['server_time'],
        $logEntry['request_id']
    ]);
    
    if (!$result) {
        throw new Exception('Failed to insert log entry');
    }
    
    // Resposta de sucesso
    echo json_encode([
        'success' => true,
        'logged' => $logEntry,
        'log_id' => $logId,
        'timestamp' => $logEntry['timestamp']
    ], JSON_UNESCAPED_UNICODE);
    
    // Log adicional para debug do próprio sistema (opcional)
    logSystemEvent('LOG_RECEIVED', [
        'log_id' => $logId,
        'level' => $logEntry['level'],
        'ip' => $logEntry['ip_address'],
        'session_id' => $logEntry['session_id']
    ]);
    
} catch (Exception $e) {
    // Log de erro interno
    error_log("Logging system error: " . $e->getMessage());
    
    // Resposta de erro
    http_response_code(500);
    echo json_encode([
        'error' => 'Internal server error',
        'message' => 'Failed to process log entry'
    ]);
}

/**
 * Valida entrada do usuário
 */
function validateInput($input) {
    $errors = [];
    
    if (!$input) {
        $errors[] = 'Invalid JSON input';
        return ['valid' => false, 'errors' => $errors];
    }
    
    if (!isset($input['message']) || empty(trim($input['message']))) {
        $errors[] = 'Message is required';
    }
    
    if (!isset($input['level']) || !in_array(strtoupper($input['level']), ['DEBUG', 'INFO', 'WARNING', 'ERROR'])) {
        $errors[] = 'Level must be one of: DEBUG, INFO, WARNING, ERROR';
    }
    
    if (isset($input['message']) && strlen($input['message']) > 1000) {
        $errors[] = 'Message too long (max 1000 characters)';
    }
    
    if (isset($input['data']) && is_string($input['data']) && strlen($input['data']) > 50000) {
        $errors[] = 'Data too large (max 50KB)';
    }
    
    return [
        'valid' => empty($errors),
        'errors' => $errors
    ];
}

/**
 * Obtém informações do cliente
 */
function getClientInfo() {
    $ip_address = getClientIP();
    $user_agent = $_SERVER['HTTP_USER_AGENT'] ?? 'unknown';
    $url = $_SERVER['HTTP_REFERER'] ?? 'unknown';
    
    return [
        'ip_address' => $ip_address,
        'user_agent' => $user_agent,
        'url' => $url
    ];
}

/**
 * Obtém IP real do cliente
 */
function getClientIP() {
    $ipKeys = ['HTTP_X_FORWARDED_FOR', 'HTTP_X_REAL_IP', 'HTTP_CLIENT_IP', 'REMOTE_ADDR'];
    
    foreach ($ipKeys as $key) {
        if (!empty($_SERVER[$key])) {
            $ip = $_SERVER[$key];
            // Se há múltiplos IPs (proxy), pegar o primeiro
            if (strpos($ip, ',') !== false) {
                $ip = trim(explode(',', $ip)[0]);
            }
            // Validar IP
            if (filter_var($ip, FILTER_VALIDATE_IP, FILTER_FLAG_NO_PRIV_RANGE | FILTER_FLAG_NO_RES_RANGE)) {
                return $ip;
            }
        }
    }
    
    return $_SERVER['REMOTE_ADDR'] ?? 'unknown';
}

/**
 * Sanitiza string de entrada
 */
function sanitizeString($string) {
    // Remover caracteres de controle
    $string = preg_replace('/[\x00-\x1F\x7F]/', '', $string);
    
    // Limitar tamanho
    if (strlen($string) > 1000) {
        $string = substr($string, 0, 1000) . '...[TRUNCATED]';
    }
    
    return $string;
}

/**
 * Registra evento do sistema
 */
function logSystemEvent($action, $data = []) {
    try {
        $pdo = getDatabaseConnection();
        
        $stmt = $pdo->prepare("
            INSERT INTO debug_logs (
                log_id, session_id, timestamp, level, message, 
                data, url, user_agent, ip_address, server_time, request_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ");
        
        $stmt->execute([
            uniqid('system_', true),
            'system',
            date('Y-m-d H:i:s'),
            'INFO',
            "System event: $action",
            json_encode($data),
            'system://internal',
            'PHP System',
            '127.0.0.1',
            microtime(true),
            uniqid('sys_', true)
        ]);
    } catch (Exception $e) {
        // Silenciar erros de logging do sistema para não causar loops
        error_log("System logging error: " . $e->getMessage());
    }
}
?>


