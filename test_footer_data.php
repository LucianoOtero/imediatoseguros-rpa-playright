<?php
// Teste com dados exatos do Footer Code
error_reporting(E_ALL);
ini_set('display_errors', 1);

$config = require_once '/var/www/html/logging_system/config/app.php';
require_once '/var/www/html/logging_system/src/Logger.php';

echo "Testando com dados exatos do Footer Code...\n";

try {
    $logger = new Logger($config);
    
    // Simular exatamente os dados que o Footer Code envia
    $input = [
        'level' => 'INFO',
        'message' => '🎯 [CONFIG] RPA habilitado via PHP Log',
        'data' => ['rpaEnabled' => false],
        'timestamp' => '2025-10-20T20:35:20.000Z',
        'sessionId' => 'sess_1761003320_abc123def',
        'url' => 'https://www.segurosimediato.com.br',
        'userAgent' => 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    ];
    
    echo "Dados enviados: " . json_encode($input, JSON_PRETTY_PRINT) . "\n";
    
    $result = $logger->log($input);
    echo "Resultado: " . json_encode($result, JSON_PRETTY_PRINT) . "\n";
    
} catch (Exception $e) {
    echo "❌ Erro: " . $e->getMessage() . "\n";
    echo "Stack trace: " . $e->getTraceAsString() . "\n";
}


































