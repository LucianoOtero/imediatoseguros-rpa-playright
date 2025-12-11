<?php
/**
 * Logger - Classe principal do sistema de logging
 * Sistema de Logging RPA - Imediato Seguros
 */

require_once __DIR__ . '/DatabaseHandler.php';
require_once __DIR__ . '/FileHandler.php';

class Logger {
    private $config;
    private $dbHandler;
    private $fileHandler;
    private $rateLimiter;
    
    public function __construct($config) {
        $this->config = $config;
        $this->initializeHandlers();
        $this->initializeRateLimiter();
    }
    
    private function initializeHandlers() {
        try {
            $this->dbHandler = new DatabaseHandler($this->config['database']);
        } catch (Exception $e) {
            error_log('Database handler failed: ' . $e->getMessage());
            $this->dbHandler = null;
        }
        
        $this->fileHandler = new FileHandler(
            $this->config['logging']['fallback_file'],
            $this->config['logging']['max_file_size']
        );
    }
    
    private function initializeRateLimiter() {
        $this->rateLimiter = [
            'enabled' => $this->config['logging']['rate_limit']['enabled'],
            'max_requests' => $this->config['logging']['rate_limit']['max_requests'],
            'time_window' => $this->config['logging']['rate_limit']['time_window'],
            'requests' => []
        ];
    }
    
    public function log($input) {
        try {
            // Validar entrada
            $this->validateInput($input);
            
            // Verificar rate limiting
            if ($this->isRateLimited($input['ip_address'] ?? 'unknown')) {
                throw new Exception('Rate limit exceeded');
            }
            
            // Construir entrada do log
            $logEntry = $this->buildLogEntry($input);
            
            // Tentar salvar no banco primeiro
            $result = $this->saveToDatabase($logEntry);
            
            // Se falhar, usar fallback para arquivo
            if (!$result['success']) {
                $result = $this->saveToFile($logEntry);
            }
            
            return $result;
            
        } catch (Exception $e) {
            // Em caso de erro, tentar fallback para arquivo
            try {
                $logEntry = $this->buildLogEntry($input);
                $logEntry['message'] = 'ERROR: ' . $e->getMessage() . ' | Original: ' . $logEntry['message'];
                return $this->saveToFile($logEntry);
            } catch (Exception $fallbackError) {
                error_log('Logger failed completely: ' . $fallbackError->getMessage());
                return [
                    'success' => false,
                    'error' => $fallbackError->getMessage()
                ];
            }
        }
    }
    
    private function validateInput($input) {
        if (!$input || !is_array($input)) {
            throw new Exception('Invalid input data');
        }
        
        if (!isset($input['message']) || empty($input['message'])) {
            throw new Exception('Message is required');
        }
        
        if (!isset($input['level']) || !in_array(strtoupper($input['level']), $this->config['logging']['levels'])) {
            throw new Exception('Invalid log level');
        }
        
        // Validar tamanho da mensagem
        if (strlen($input['message']) > 1000) {
            throw new Exception('Message too long');
        }
        
        // Validar dados adicionais
        if (isset($input['data']) && strlen(json_encode($input['data'])) > 50000) {
            throw new Exception('Data payload too large');
        }
    }
    
    private function buildLogEntry($input) {
        $timestamp = new DateTime('now', new DateTimeZone($this->config['server']['timezone']));
        
        return [
            'log_id' => $input['logId'] ?? uniqid('log_', true),
            'session_id' => $input['sessionId'] ?? 'unknown',
            'timestamp' => $timestamp->format('Y-m-d H:i:s'),
            'client_timestamp' => $input['timestamp'] ?? $timestamp->format('c'),
            'level' => strtoupper($input['level']),
            'message' => $input['message'],
            'data' => $input['data'] ?? null,
            'url' => $input['url'] ?? ($_SERVER['HTTP_REFERER'] ?? 'unknown'),
            'user_agent' => $input['userAgent'] ?? ($_SERVER['HTTP_USER_AGENT'] ?? 'unknown'),
            'ip_address' => $input['ip_address'] ?? ($_SERVER['REMOTE_ADDR'] ?? 'unknown'),
            'server_time' => microtime(true),
            'request_id' => uniqid('req_', true)
        ];
    }
    
    private function saveToDatabase($logEntry) {
        if (!$this->dbHandler) {
            throw new Exception('Database handler not available');
        }
        
        return $this->dbHandler->save($logEntry);
    }
    
    private function saveToFile($logEntry) {
        return $this->fileHandler->save($logEntry);
    }
    
    private function isRateLimited($ip) {
        if (!$this->rateLimiter['enabled']) {
            return false;
        }
        
        $now = time();
        $windowStart = $now - $this->rateLimiter['time_window'];
        
        // Limpar requisições antigas
        if (isset($this->rateLimiter['requests'][$ip])) {
            $this->rateLimiter['requests'][$ip] = array_filter(
                $this->rateLimiter['requests'][$ip],
                function($timestamp) use ($windowStart) {
                    return $timestamp > $windowStart;
                }
            );
        } else {
            $this->rateLimiter['requests'][$ip] = [];
        }
        
        // Verificar limite
        if (count($this->rateLimiter['requests'][$ip]) >= $this->rateLimiter['max_requests']) {
            return true;
        }
        
        // Adicionar requisição atual
        $this->rateLimiter['requests'][$ip][] = $now;
        
        return false;
    }
    
    public function getStats() {
        $stats = [
            'database_available' => $this->dbHandler !== null,
            'file_handler_available' => $this->fileHandler !== null,
            'rate_limit_enabled' => $this->rateLimiter['enabled'],
            'config_loaded' => !empty($this->config)
        ];
        
        if ($this->dbHandler) {
            try {
                $pdo = $this->dbHandler->getConnection();
                $stmt = $pdo->query('SELECT COUNT(*) as total FROM debug_logs');
                $stats['total_logs'] = $stmt->fetchColumn();
            } catch (Exception $e) {
                $stats['database_error'] = $e->getMessage();
            }
        }
        
        return $stats;
    }
}


































