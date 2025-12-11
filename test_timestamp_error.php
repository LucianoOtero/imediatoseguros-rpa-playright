<?php
// Teste para capturar o erro exato
error_reporting(E_ALL);
ini_set('display_errors', 1);

$config = require_once '/var/www/html/logging_system/config/app.php';
require_once '/var/www/html/logging_system/src/DatabaseHandler.php';

echo "Teste direto do DatabaseHandler com timestamp ISO...\n";

try {
    $dbHandler = new DatabaseHandler($config['database']);
    
    // Construir log entry como a classe Logger faz
    $timestamp = new DateTime('now', new DateTimeZone($config['server']['timezone']));
    
    $logEntry = [
        'log_id' => 'test_' . time(),
        'session_id' => 'sess_test',
        'timestamp' => $timestamp->format('Y-m-d H:i:s'),
        'client_timestamp' => '2025-10-20T20:35:20.000Z', // Timestamp ISO problemático
        'level' => 'INFO',
        'message' => 'Teste com timestamp ISO',
        'data' => json_encode(['test' => true]),
        'url' => 'https://test.com',
        'user_agent' => 'Test Agent',
        'ip_address' => '127.0.0.1',
        'server_time' => microtime(true),
        'request_id' => 'test_req_' . time()
    ];
    
    echo "Log entry: " . json_encode($logEntry, JSON_PRETTY_PRINT) . "\n";
    
    $result = $dbHandler->save($logEntry);
    echo "Resultado: " . json_encode($result, JSON_PRETTY_PRINT) . "\n";
    
} catch (Exception $e) {
    echo "❌ Erro: " . $e->getMessage() . "\n";
    echo "Stack trace: " . $e->getTraceAsString() . "\n";
}


































