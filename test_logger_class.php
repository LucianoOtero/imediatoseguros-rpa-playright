<?php
// Teste específico da classe Logger
error_reporting(E_ALL);
ini_set('display_errors', 1);

$config = require_once '/var/www/html/logging_system/config/app.php';
require_once '/var/www/html/logging_system/src/Logger.php';

echo "Testando classe Logger...\n";
echo "Config default_handler: " . ($config['logging']['default_handler'] ?? 'NOT SET') . "\n";

try {
    $logger = new Logger($config);
    echo "✅ Logger inicializado com sucesso!\n";
    
    // Testar stats
    $stats = $logger->getStats();
    echo "Stats: " . json_encode($stats, JSON_PRETTY_PRINT) . "\n";
    
    // Testar log
    $input = [
        'level' => 'INFO',
        'message' => 'Teste da classe Logger',
        'data' => ['test' => true],
        'sessionId' => 'test_session_' . time(),
        'url' => 'https://test.com',
        'userAgent' => 'Test Agent',
        'timestamp' => date('c')
    ];
    
    echo "Enviando log de teste...\n";
    $result = $logger->log($input);
    echo "Resultado: " . json_encode($result, JSON_PRETTY_PRINT) . "\n";
    
} catch (Exception $e) {
    echo "❌ Erro na classe Logger: " . $e->getMessage() . "\n";
    echo "Stack trace: " . $e->getTraceAsString() . "\n";
}


































