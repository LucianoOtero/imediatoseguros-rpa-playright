<?php
// Teste direto da conexão com banco de dados
error_reporting(E_ALL);
ini_set('display_errors', 1);

$config = require_once '/var/www/html/logging_system/config/app.php';

try {
    echo "Testando conexão com banco de dados...\n";
    
    $dsn = sprintf(
        'mysql:host=%s;port=%d;dbname=%s;charset=%s',
        $config['database']['host'],
        $config['database']['port'],
        $config['database']['database'],
        $config['database']['charset']
    );
    
    $pdo = new PDO(
        $dsn,
        $config['database']['username'],
        $config['database']['password'],
        $config['database']['options']
    );
    
    echo "✅ Conexão com banco estabelecida!\n";
    
    // Testar inserção
    $logEntry = [
        'log_id' => 'test_' . time(),
        'session_id' => 'test_session',
        'timestamp' => date('Y-m-d H:i:s'),
        'client_timestamp' => date('c'),
        'level' => 'INFO',
        'message' => 'Teste de conexão',
        'data' => json_encode(['test' => true]),
        'url' => 'https://test.com',
        'user_agent' => 'Test Agent',
        'ip_address' => '127.0.0.1',
        'server_time' => microtime(true),
        'request_id' => 'test_req_' . time()
    ];
    
    $sql = 'INSERT INTO debug_logs (log_id, session_id, timestamp, client_timestamp, level, message, data, url, user_agent, ip_address, server_time, request_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)';
    
    $stmt = $pdo->prepare($sql);
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
    
    if ($result) {
        echo "✅ Inserção no banco bem-sucedida! Rows affected: " . $stmt->rowCount() . "\n";
    } else {
        echo "❌ Falha na inserção\n";
    }
    
} catch (Exception $e) {
    echo "❌ Erro: " . $e->getMessage() . "\n";
}


































