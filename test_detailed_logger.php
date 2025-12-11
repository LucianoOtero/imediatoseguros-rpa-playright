<?php
// Teste detalhado da classe Logger
error_reporting(E_ALL);
ini_set('display_errors', 1);

$config = require_once '/var/www/html/logging_system/config/app.php';
require_once '/var/www/html/logging_system/src/Logger.php';

echo "Teste detalhado da classe Logger...\n";

try {
    $logger = new Logger($config);
    
    // Testar com dados mínimos primeiro
    $input = [
        'level' => 'INFO',
        'message' => 'Teste simples',
        'sessionId' => 'test_session',
        'url' => 'https://test.com',
        'userAgent' => 'Test Agent'
    ];
    
    echo "Testando com dados mínimos...\n";
    $result = $logger->log($input);
    echo "Resultado: " . json_encode($result, JSON_PRETTY_PRINT) . "\n";
    
    // Agora testar com dados do Footer Code
    echo "\nTestando com dados do Footer Code...\n";
    $input2 = [
        'level' => 'INFO',
        'message' => '🎯 [CONFIG] RPA habilitado via PHP Log',
        'data' => ['rpaEnabled' => false],
        'timestamp' => '2025-10-20T20:35:20.000Z',
        'sessionId' => 'sess_1761003320_abc123def',
        'url' => 'https://www.segurosimediato.com.br',
        'userAgent' => 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    ];
    
    $result2 = $logger->log($input2);
    echo "Resultado: " . json_encode($result2, JSON_PRETTY_PRINT) . "\n";
    
} catch (Exception $e) {
    echo "❌ Erro: " . $e->getMessage() . "\n";
    echo "Stack trace: " . $e->getTraceAsString() . "\n";
}


































