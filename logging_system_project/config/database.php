<?php
/**
 * config/database.php - Configuração de Conexão com Banco de Dados
 * Sistema de Logging PHP - RPA Imediato Seguros
 */

// Configurações do banco de dados
$db_config = [
    'host' => 'localhost',
    'port' => 3306,
    'database' => 'rpa_logs',
    'username' => 'rpa_logger',
    'password' => 'senha_super_segura_123!',
    'charset' => 'utf8mb4',
    'options' => [
        PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
        PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
        PDO::ATTR_EMULATE_PREPARES => false,
        PDO::MYSQL_ATTR_INIT_COMMAND => "SET NAMES utf8mb4 COLLATE utf8mb4_unicode_ci",
        PDO::ATTR_PERSISTENT => false, // Desabilitar conexões persistentes para logging
        PDO::ATTR_TIMEOUT => 10, // Timeout de 10 segundos
    ]
];

/**
 * Estabelece conexão com o banco de dados
 * @return PDO
 * @throws Exception
 */
function getDatabaseConnection() {
    global $db_config;
    
    static $pdo = null;
    
    // Reutilizar conexão existente se disponível
    if ($pdo !== null) {
        return $pdo;
    }
    
    try {
        $dsn = sprintf(
            'mysql:host=%s;port=%d;dbname=%s;charset=%s',
            $db_config['host'],
            $db_config['port'],
            $db_config['database'],
            $db_config['charset']
        );
        
        $pdo = new PDO(
            $dsn,
            $db_config['username'],
            $db_config['password'],
            $db_config['options']
        );
        
        // Verificar se a conexão está funcionando
        $pdo->query('SELECT 1');
        
        return $pdo;
        
    } catch (PDOException $e) {
        // Log do erro de conexão
        error_log("Database connection error: " . $e->getMessage());
        
        throw new Exception('Database connection failed');
    }
}

/**
 * Testa a conexão com o banco de dados
 * @return array
 */
function testDatabaseConnection() {
    try {
        $pdo = getDatabaseConnection();
        
        // Testar query simples
        $stmt = $pdo->query('SELECT COUNT(*) as count FROM debug_logs');
        $result = $stmt->fetch();
        
        return [
            'status' => 'success',
            'message' => 'Database connection successful',
            'total_logs' => $result['count']
        ];
        
    } catch (Exception $e) {
        return [
            'status' => 'error',
            'message' => $e->getMessage()
        ];
    }
}

/**
 * Obtém estatísticas do banco de dados
 * @return array
 */
function getDatabaseStats() {
    try {
        $pdo = getDatabaseConnection();
        
        $stats = [];
        
        // Total de logs
        $stmt = $pdo->query('SELECT COUNT(*) as count FROM debug_logs');
        $stats['total_logs'] = $stmt->fetch()['count'];
        
        // Logs por nível
        $stmt = $pdo->query('
            SELECT level, COUNT(*) as count 
            FROM debug_logs 
            GROUP BY level 
            ORDER BY count DESC
        ');
        $stats['logs_by_level'] = $stmt->fetchAll();
        
        // Sessões únicas
        $stmt = $pdo->query('SELECT COUNT(DISTINCT session_id) as count FROM debug_logs');
        $stats['unique_sessions'] = $stmt->fetch()['count'];
        
        // Logs das últimas 24 horas
        $stmt = $pdo->query('
            SELECT COUNT(*) as count 
            FROM debug_logs 
            WHERE timestamp > DATE_SUB(NOW(), INTERVAL 24 HOUR)
        ');
        $stats['logs_24h'] = $stmt->fetch()['count'];
        
        // Tamanho do banco
        $stmt = $pdo->query('
            SELECT 
                ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) as size_mb
            FROM information_schema.tables 
            WHERE table_schema = ?
        ');
        $stmt->execute([$db_config['database']]);
        $stats['database_size_mb'] = $stmt->fetch()['size_mb'];
        
        return $stats;
        
    } catch (Exception $e) {
        return [
            'error' => $e->getMessage()
        ];
    }
}

/**
 * Executa limpeza de logs antigos
 * @param int $days Número de dias para manter
 * @return array
 */
function cleanupOldLogs($days = 30) {
    try {
        $pdo = getDatabaseConnection();
        
        // Contar logs que serão deletados
        $stmt = $pdo->prepare('
            SELECT COUNT(*) as count 
            FROM debug_logs 
            WHERE created_at < DATE_SUB(NOW(), INTERVAL ? DAY)
        ');
        $stmt->execute([$days]);
        $logs_to_delete = $stmt->fetch()['count'];
        
        // Deletar logs antigos
        $stmt = $pdo->prepare('
            DELETE FROM debug_logs 
            WHERE created_at < DATE_SUB(NOW(), INTERVAL ? DAY)
        ');
        $stmt->execute([$days]);
        
        // Deletar sessões antigas
        $stmt = $pdo->prepare('
            DELETE FROM sessions 
            WHERE created_at < DATE_SUB(NOW(), INTERVAL ? DAY)
        ');
        $stmt->execute([$days]);
        
        return [
            'status' => 'success',
            'message' => "Cleanup completed",
            'logs_deleted' => $logs_to_delete,
            'retention_days' => $days
        ];
        
    } catch (Exception $e) {
        return [
            'status' => 'error',
            'message' => $e->getMessage()
        ];
    }
}

/**
 * Obtém configurações do sistema
 * @return array
 */
function getSystemConfig() {
    try {
        $pdo = getDatabaseConnection();
        
        $stmt = $pdo->query('SELECT config_key, config_value FROM config');
        $configs = $stmt->fetchAll();
        
        $result = [];
        foreach ($configs as $config) {
            $result[$config['config_key']] = $config['config_value'];
        }
        
        return $result;
        
    } catch (Exception $e) {
        return [
            'error' => $e->getMessage()
        ];
    }
}

/**
 * Atualiza configuração do sistema
 * @param string $key
 * @param string $value
 * @return bool
 */
function updateSystemConfig($key, $value) {
    try {
        $pdo = getDatabaseConnection();
        
        $stmt = $pdo->prepare('
            INSERT INTO config (config_key, config_value) 
            VALUES (?, ?) 
            ON DUPLICATE KEY UPDATE 
                config_value = VALUES(config_value),
                updated_at = CURRENT_TIMESTAMP
        ');
        
        return $stmt->execute([$key, $value]);
        
    } catch (Exception $e) {
        error_log("Config update error: " . $e->getMessage());
        return false;
    }
}
?>
