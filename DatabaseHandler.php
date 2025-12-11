<?php
/**
 * DatabaseHandler - Manipulação de logs no banco de dados
 * Sistema de Logging RPA - Imediato Seguros
 */

class DatabaseHandler {
    private $pdo;
    private $config;
    
    public function __construct($config) {
        $this->config = $config;
        $this->connect();
    }
    
    private function connect() {
        try {
            $dsn = sprintf(
                'mysql:host=%s;port=%d;dbname=%s;charset=%s',
                $this->config['host'],
                $this->config['port'],
                $this->config['database'],
                $this->config['charset']
            );
            
            $this->pdo = new PDO(
                $dsn,
                $this->config['username'],
                $this->config['password'],
                $this->config['options']
            );
            
        } catch (PDOException $e) {
            throw new Exception('Database connection failed: ' . $e->getMessage());
        }
    }
    
    public function save($logEntry) {
        try {
            $sql = 'INSERT INTO debug_logs (log_id, session_id, timestamp, client_timestamp, level, message, data, url, user_agent, ip_address, server_time, request_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)';
            
            $stmt = $this->pdo->prepare($sql);
            $result = $stmt->execute([
                $logEntry['log_id'],
                $logEntry['session_id'],
                $logEntry['timestamp'],
                $logEntry['client_timestamp'],
                $logEntry['level'],
                $logEntry['message'],
                json_encode($logEntry['data']),
                $logEntry['url'],
                $logEntry['user_agent'],
                $logEntry['ip_address'],
                $logEntry['server_time'],
                $logEntry['request_id']
            ]);
            
            if (!$result) {
                throw new Exception('Log insertion failed');
            }
            
            return [
                'success' => true,
                'method' => 'database',
                'rows_affected' => $stmt->rowCount(),
                'log_id' => $logEntry['log_id']
            ];
            
        } catch (Exception $e) {
            throw new Exception('Database save failed: ' . $e->getMessage());
        }
    }
    
    public function getConnection() {
        return $this->pdo;
    }
}


































