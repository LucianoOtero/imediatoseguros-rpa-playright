<?php
/**
 * Sistema de Logging PHP - Versão Arquivo
 * Versão: 1.0.1
 * Data: 2025-10-20
 * 
 * Recebe logs via POST JSON e armazena em arquivo
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

// Função para escrever log em arquivo
function writeLogToFile($logData) {
    $logFile = 'debug_rpa_logs.json';
    $logLine = json_encode($logData, JSON_UNESCAPED_UNICODE) . "\n";
    return file_put_contents($logFile, $logLine, FILE_APPEND | LOCK_EX);
}

// Função para escrever log em formato legível
function writeLogToReadableFile($logData) {
    $logFile = 'debug_rpa_readable.log';
    $timestamp = $logData['timestamp'];
    $level = $logData['level'];
    $message = $logData['message'];
    $sessionId = $logData['session_id'];
    $url = $logData['url'];
    
    $logLine = "[{$timestamp}] [{$level}] [{$sessionId}] {$message} | URL: {$url}\n";
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
        'data' => $input['data'] ?? null,
        'url' => $input['url'] ?? ($_SERVER['HTTP_REFERER'] ?? 'unknown'),
        'session_id' => $input['sessionId'] ?? 'unknown',
        'user_agent' => $input['userAgent'] ?? ($_SERVER['HTTP_USER_AGENT'] ?? 'unknown'),
        'ip_address' => $clientIP,
        'server_time' => microtime(true),
        'request_id' => uniqid('req_', true)
    ];
    
    // Escrever logs
    $jsonResult = writeLogToFile($logData);
    $readableResult = writeLogToReadableFile($logData);
    
    if ($jsonResult !== false && $readableResult !== false) {
        // Sucesso
        echo json_encode([
            'success' => true,
            'method' => 'file',
            'logged' => $logData,
            'json_bytes' => $jsonResult,
            'readable_bytes' => $readableResult
        ], JSON_UNESCAPED_UNICODE);
    } else {
        // Falha na escrita
        http_response_code(500);
        echo json_encode([
            'success' => false,
            'error' => 'Failed to write log files'
        ], JSON_UNESCAPED_UNICODE);
    }
    
} catch (Exception $e) {
    // Erro geral
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
    
    $fallbackResult = writeLogToFile($logData);
    
    http_response_code(500);
    echo json_encode([
        'success' => false,
        'error' => 'System error occurred',
        'method' => 'file_fallback',
        'bytes_written' => $fallbackResult
    ], JSON_UNESCAPED_UNICODE);
}
?>




































