<?php
/**
 * Script de Configuração do Banco de Dados
 * Cria o banco de dados e tabela para o sistema de logging
 */

// Configurações do banco de dados
$db_config = [
    'host' => 'localhost',
    'port' => 3306,
    'database' => 'mdmidiac_rpa_logs',
    'username' => 'mdmidiac',
    'password' => '' // Sem senha por enquanto
];

echo "=== CONFIGURACAO DO BANCO DE DADOS ===\n";
echo "Data: " . date('Y-m-d H:i:s') . "\n\n";

try {
    // Conectar sem especificar database primeiro
    $dsn = "mysql:host={$db_config['host']};port={$db_config['port']};charset=utf8mb4";
    $pdo = new PDO($dsn, $db_config['username'], $db_config['password'], [
        PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
        PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC
    ]);
    
    echo "✓ Conexão MySQL estabelecida\n";
    
    // Criar banco de dados
    $sql = "CREATE DATABASE IF NOT EXISTS {$db_config['database']} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci";
    $pdo->exec($sql);
    echo "✓ Banco de dados '{$db_config['database']}' criado/verificado\n";
    
    // Conectar ao banco específico
    $dsn = "mysql:host={$db_config['host']};port={$db_config['port']};dbname={$db_config['database']};charset=utf8mb4";
    $pdo = new PDO($dsn, $db_config['username'], $db_config['password'], [
        PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
        PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC
    ]);
    
    echo "✓ Conectado ao banco '{$db_config['database']}'\n";
    
    // Criar tabela de logs
    $sql = "
        CREATE TABLE IF NOT EXISTS logs (
            id INT AUTO_INCREMENT PRIMARY KEY,
            log_id VARCHAR(50) NOT NULL,
            timestamp DATETIME NOT NULL,
            client_timestamp VARCHAR(50),
            level ENUM('DEBUG', 'INFO', 'WARNING', 'ERROR') NOT NULL,
            message TEXT NOT NULL,
            data JSON,
            url VARCHAR(500),
            session_id VARCHAR(100),
            user_agent TEXT,
            ip_address VARCHAR(45),
            server_time DECIMAL(15,6),
            request_id VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            INDEX idx_log_id (log_id),
            INDEX idx_timestamp (timestamp),
            INDEX idx_level (level),
            INDEX idx_session_id (session_id),
            INDEX idx_ip_address (ip_address)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    ";
    
    $pdo->exec($sql);
    echo "✓ Tabela 'logs' criada/verificada\n";
    
    // Testar inserção
    $testData = [
        'log_id' => 'test_' . uniqid(),
        'timestamp' => date('Y-m-d H:i:s'),
        'client_timestamp' => date('c'),
        'level' => 'INFO',
        'message' => 'Teste de configuração do banco de dados',
        'data' => json_encode(['test' => true]),
        'url' => 'setup_script',
        'session_id' => 'setup_test',
        'user_agent' => 'SetupScript/1.0',
        'ip_address' => '127.0.0.1',
        'server_time' => microtime(true),
        'request_id' => uniqid('req_', true)
    ];
    
    $sql = "
        INSERT INTO logs (
            log_id, timestamp, client_timestamp, level, message, data,
            url, session_id, user_agent, ip_address, server_time, request_id
        ) VALUES (
            :log_id, :timestamp, :client_timestamp, :level, :message, :data,
            :url, :session_id, :user_agent, :ip_address, :server_time, :request_id
        )
    ";
    
    $stmt = $pdo->prepare($sql);
    $stmt->execute($testData);
    $rowsAffected = $stmt->rowCount();
    
    echo "✓ Teste de inserção realizado ({$rowsAffected} linha inserida)\n";
    
    // Verificar dados
    $sql = "SELECT COUNT(*) as total FROM logs";
    $stmt = $pdo->query($sql);
    $result = $stmt->fetch();
    
    echo "✓ Total de logs no banco: {$result['total']}\n";
    
    echo "\n=== CONFIGURACAO CONCLUIDA COM SUCESSO ===\n";
    echo "Banco de dados: {$db_config['database']}\n";
    echo "Tabela: logs\n";
    echo "Status: Pronto para uso\n";
    
} catch (PDOException $e) {
    echo "✗ ERRO: " . $e->getMessage() . "\n";
    echo "Código: " . $e->getCode() . "\n";
    
    // Tentar fallback sem senha
    if (strpos($e->getMessage(), 'Access denied') !== false) {
        echo "\nTentando conexão sem senha...\n";
        try {
            $dsn = "mysql:host={$db_config['host']};port={$db_config['port']};charset=utf8mb4";
            $pdo = new PDO($dsn, $db_config['username'], '', [
                PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION
            ]);
            echo "✓ Conexão sem senha funcionou!\n";
        } catch (PDOException $e2) {
            echo "✗ Conexão sem senha também falhou: " . $e2->getMessage() . "\n";
        }
    }
} catch (Exception $e) {
    echo "✗ ERRO GERAL: " . $e->getMessage() . "\n";
}
?>




































