<?php
// Teste isolando o problema
error_reporting(E_ALL);
ini_set('display_errors', 1);

$config = require_once '/var/www/html/logging_system/config/app.php';
require_once '/var/www/html/logging_system/src/Logger.php';

echo "Teste isolando o problema...\n";

try {
    $logger = new Logger($config);
    
    // Teste 1: Sem emoji
    echo "Teste 1: Sem emoji\n";
    $input1 = [
        'level' => 'INFO',
        'message' => '[CONFIG] RPA habilitado via PHP Log',
        'data' => ['rpaEnabled' => false],
        'sessionId' => 'sess_test',
        'url' => 'https://www.segurosimediato.com.br',
        'userAgent' => 'Mozilla/5.0'
    ];
    $result1 = $logger->log($input1);
    echo "Resultado: " . ($result1['method'] ?? 'ERROR') . "\n";
    
    // Teste 2: Com emoji
    echo "\nTeste 2: Com emoji\n";
    $input2 = [
        'level' => 'INFO',
        'message' => '🎯 [CONFIG] RPA habilitado via PHP Log',
        'data' => ['rpaEnabled' => false],
        'sessionId' => 'sess_test',
        'url' => 'https://www.segurosimediato.com.br',
        'userAgent' => 'Mozilla/5.0'
    ];
    $result2 = $logger->log($input2);
    echo "Resultado: " . ($result2['method'] ?? 'ERROR') . "\n";
    
    // Teste 3: Com timestamp ISO
    echo "\nTeste 3: Com timestamp ISO\n";
    $input3 = [
        'level' => 'INFO',
        'message' => '[CONFIG] RPA habilitado via PHP Log',
        'data' => ['rpaEnabled' => false],
        'timestamp' => '2025-10-20T20:35:20.000Z',
        'sessionId' => 'sess_test',
        'url' => 'https://www.segurosimediato.com.br',
        'userAgent' => 'Mozilla/5.0'
    ];
    $result3 = $logger->log($input3);
    echo "Resultado: " . ($result3['method'] ?? 'ERROR') . "\n";
    
    // Teste 4: UserAgent longo
    echo "\nTeste 4: UserAgent longo\n";
    $input4 = [
        'level' => 'INFO',
        'message' => '[CONFIG] RPA habilitado via PHP Log',
        'data' => ['rpaEnabled' => false],
        'sessionId' => 'sess_test',
        'url' => 'https://www.segurosimediato.com.br',
        'userAgent' => 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    ];
    $result4 = $logger->log($input4);
    echo "Resultado: " . ($result4['method'] ?? 'ERROR') . "\n";
    
} catch (Exception $e) {
    echo "❌ Erro: " . $e->getMessage() . "\n";
}


































