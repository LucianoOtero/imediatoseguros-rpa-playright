<?php
/**
 * debug_logger.php - Sistema de Logging para Debug RPA
 * Hospedado em: https://mdmidia.com.br/debug_logger.php
 * 
 * Funcionalidade:
 * - Recebe logs via POST JSON
 * - Grava em arquivo debug_rpa.log
 * - Suporte a CORS para requisições do Webflow
 * - Identificação completa de usuário e sessão
 */

// Configurar headers para CORS
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

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

// Ler dados JSON do corpo da requisição
$input = json_decode(file_get_contents('php://input'), true);

// Validar entrada
if (!$input) {
    http_response_code(400);
    echo json_encode(['error' => 'Invalid JSON input']);
    exit;
}

if (!isset($input['message']) || !isset($input['level'])) {
    http_response_code(400);
    echo json_encode(['error' => 'Missing required fields: message and level']);
    exit;
}

// Gerar ID único para este log se não fornecido
$logId = $input['logId'] ?? uniqid('log_', true);

// Construir entrada do log com informações completas
$logEntry = [
    'log_id' => $logId,
    'timestamp' => date('Y-m-d H:i:s'),
    'client_timestamp' => $input['timestamp'] ?? date('c'),
    'level' => strtoupper($input['level']),
    'message' => $input['message'],
    'data' => $input['data'] ?? null,
    'url' => $input['url'] ?? ($_SERVER['HTTP_REFERER'] ?? 'unknown'),
    'session_id' => $input['sessionId'] ?? 'unknown',
    'user_agent' => $input['userAgent'] ?? ($_SERVER['HTTP_USER_AGENT'] ?? 'unknown'),
    'ip_address' => $_SERVER['REMOTE_ADDR'] ?? 'unknown',
    'server_time' => microtime(true),
    'request_id' => uniqid('req_', true)
];

// Nome do arquivo de log
$logFile = 'debug_rpa.log';

// Verificar permissões de escrita
if (!is_writable(dirname($logFile)) && !is_writable($logFile)) {
    http_response_code(500);
    echo json_encode(['error' => 'Log directory not writable']);
    exit;
}

// Limitar tamanho dos dados para evitar logs muito grandes
if (isset($logEntry['data']) && is_string($logEntry['data']) && strlen($logEntry['data']) > 10000) {
    $logEntry['data'] = substr($logEntry['data'], 0, 10000) . '...[TRUNCATED]';
}

// Converter para JSON e adicionar quebra de linha
$logLine = json_encode($logEntry, JSON_UNESCAPED_UNICODE) . "\n";

// Gravar no arquivo de log com lock para evitar conflitos
$result = file_put_contents($logFile, $logLine, FILE_APPEND | LOCK_EX);

if ($result === false) {
    http_response_code(500);
    echo json_encode(['error' => 'Failed to write to log file']);
    exit;
}

// Resposta de sucesso
echo json_encode([
    'success' => true,
    'logged' => $logEntry,
    'bytes_written' => $result,
    'log_file' => $logFile
], JSON_UNESCAPED_UNICODE);

// Log adicional para debug do próprio sistema (opcional)
$systemLog = [
    'timestamp' => date('Y-m-d H:i:s'),
    'type' => 'SYSTEM',
    'action' => 'LOG_RECEIVED',
    'log_id' => $logId,
    'level' => $logEntry['level'],
    'ip' => $logEntry['ip_address'],
    'bytes' => $result
];

$systemLogResult = file_put_contents('debug_system.log', json_encode($systemLog) . "\n", FILE_APPEND | LOCK_EX);

// Log de erro do sistema se falhar (silencioso)
if ($systemLogResult === false) {
    error_log("Failed to write to debug_system.log");
}

?>
