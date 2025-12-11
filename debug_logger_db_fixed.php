<?php
/**
 * Sistema de Logging RPA - Endpoint Principal
 * Baseado na documentação completa do projeto
 * Servidor: bpsegurosimediato.com.br
 * Banco: rpa_logs | Usuário: rpa_user
 */

// Configurações de erro e timezone
error_reporting(E_ALL);
ini_set('display_errors', 0);
ini_set('log_errors', 1);
date_default_timezone_set('America/Sao_Paulo');

// Carregar configuração
$config = require_once __DIR__ . '/config/app.php';

// Carregar Logger
require_once __DIR__ . '/src/Logger.php';

// Headers CORS (baseados na documentação)
header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type, X-Requested-With');
header('Access-Control-Max-Age: 86400');

// Responder a requisições OPTIONS (preflight)
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit(0);
}

// Validar método HTTP
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode([
        'success' => false,
        'error' => 'Method not allowed',
        'method' => $_SERVER['REQUEST_METHOD']
    ]);
    exit(1);
}

// Validar Content-Type
$contentType = $_SERVER['CONTENT_TYPE'] ?? '';
if (strpos($contentType, 'application/json') === false) {
    http_response_code(400);
    echo json_encode([
        'success' => false,
        'error' => 'Content-Type must be application/json',
        'received' => $contentType
    ]);
    exit(1);
}

try {
    // Ler e validar entrada JSON
    $input = json_decode(file_get_contents('php://input'), true);
    
    if (json_last_error() !== JSON_ERROR_NONE) {
        throw new Exception('Invalid JSON: ' . json_last_error_msg());
    }
    
    if (!$input || !is_array($input)) {
        throw new Exception('Invalid input data');
    }
    
    // Adicionar informações do servidor
    $input['ip_address'] = $_SERVER['REMOTE_ADDR'] ?? 'unknown';
    $input['server_time'] = microtime(true);
    
    // Inicializar Logger
    $logger = new Logger($config);
    
    // Processar log
    $result = $logger->log($input);
    
    // Resposta de sucesso
    http_response_code(200);
    echo json_encode([
        'success' => true,
        'logged' => $result,
        'timestamp' => date('Y-m-d H:i:s'),
        'server' => 'bpsegurosimediato.com.br'
    ]);
    
} catch (Exception $e) {
    // Log do erro no sistema
    error_log('Logger Error: ' . $e->getMessage());
    
    // Resposta de erro
    http_response_code(500);
    echo json_encode([
        'success' => false,
        'error' => $e->getMessage(),
        'timestamp' => date('Y-m-d H:i:s'),
        'server' => 'bpsegurosimediato.com.br'
    ]);
}


































