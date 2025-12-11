<?php
/**
 * HEALTH CHECK ENDPOINT
 * bpsegurosimediato.com.br/health.php
 * 
 * Sistema de monitoramento para verificar saúde dos webhooks e serviços
 * Implementação segura sem afetar webhooks existentes
 */

// Configurações de segurança
header('Content-Type: application/json; charset=utf-8');
header('X-Health-Check: active');
header('Cache-Control: no-cache, no-store, must-revalidate');

// Classe principal do Health Check
class HealthChecker {
    private $environment;
    private $checks = [];
    private $start_time;
    
    public function __construct($env = 'production') {
        $this->environment = $env;
        $this->start_time = microtime(true);
    }
    
    /**
     * Verificar webhooks existentes
     */
    public function checkWebhooks() {
        $webhooks = [
            'travelangels' => '/var/www/html/add_travelangels.php',
            'octadesk' => '/var/www/html/add_webflow_octa.php',
            'debug_logger' => '/var/www/html/debug_logger_db.php'
        ];
        
        $results = [];
        foreach ($webhooks as $name => $path) {
            $file_exists = file_exists($path);
            $is_readable = $file_exists ? is_readable($path) : false;
            $last_modified = $file_exists ? date('Y-m-d H:i:s', filemtime($path)) : null;
            $file_size = $file_exists ? filesize($path) : 0;
            
            $results[$name] = [
                'status' => $file_exists && $is_readable ? 'ok' : 'error',
                'file_exists' => $file_exists,
                'is_readable' => $is_readable,
                'last_modified' => $last_modified,
                'size_bytes' => $file_size,
                'path' => $path
            ];
        }
        
        return $results;
    }
    
    /**
     * Verificar sistema de logging
     */
    public function checkLoggingSystem() {
        $logging_paths = [
            'main_logs' => '/var/www/html/logs',
            'dev_logs' => '/var/www/html/dev/logs',
            'logging_system' => '/var/www/html/logging_system',
            'travelangels_log' => '/var/www/html/logs_travelangels.txt',
            'octadesk_log' => '/var/www/html/octa_webflow_webhook.log'
        ];
        
        $results = [];
        foreach ($logging_paths as $name => $path) {
            if (is_dir($path)) {
                $files = scandir($path);
                $file_count = count($files) - 2; // Excluir . e ..
                $is_writable = is_writable($path);
                
                $results[$name] = [
                    'status' => $is_writable ? 'ok' : 'warning',
                    'type' => 'directory',
                    'path' => $path,
                    'is_writable' => $is_writable,
                    'files_count' => $file_count,
                    'last_check' => date('Y-m-d H:i:s')
                ];
            } elseif (is_file($path)) {
                $file_size = filesize($path);
                $last_modified = date('Y-m-d H:i:s', filemtime($path));
                $is_readable = is_readable($path);
                
                $results[$name] = [
                    'status' => $is_readable ? 'ok' : 'error',
                    'type' => 'file',
                    'path' => $path,
                    'size_bytes' => $file_size,
                    'last_modified' => $last_modified,
                    'is_readable' => $is_readable
                ];
            } else {
                $results[$name] = [
                    'status' => 'error',
                    'type' => 'missing',
                    'path' => $path,
                    'error' => 'File or directory not found'
                ];
            }
        }
        
        return $results;
    }
    
    /**
     * Verificar conectividade com banco de dados
     */
    public function checkDatabase() {
        try {
            // Tentar conectar ao banco de dados do logging system
            $config_file = '/var/www/html/logging_system/config/app.php';
            if (file_exists($config_file)) {
                $config = include $config_file;
                $db_config = $config['database'];
                
                $dsn = "mysql:host={$db_config['host']};dbname={$db_config['database']};charset=utf8mb4";
                $pdo = new PDO($dsn, $db_config['username'], $db_config['password'], [
                    PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
                    PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC
                ]);
                
                // Testar query simples
                $stmt = $pdo->query('SELECT COUNT(*) as total FROM logs LIMIT 1');
                $result = $stmt->fetch();
                
                return [
                    'status' => 'ok',
                    'connection' => 'success',
                    'host' => $db_config['host'],
                    'database' => $db_config['database'],
                    'test_query' => 'success',
                    'total_logs' => $result['total'] ?? 0
                ];
            } else {
                return [
                    'status' => 'warning',
                    'error' => 'Config file not found',
                    'path' => $config_file
                ];
            }
        } catch (Exception $e) {
            return [
                'status' => 'error',
                'error' => $e->getMessage(),
                'connection' => 'failed'
            ];
        }
    }
    
    /**
     * Verificar espaço em disco
     */
    public function checkDiskSpace() {
        $path = '/var/www/html';
        $free_bytes = disk_free_space($path);
        $total_bytes = disk_total_space($path);
        
        if ($free_bytes === false || $total_bytes === false) {
            return [
                'status' => 'error',
                'error' => 'Unable to get disk space information'
            ];
        }
        
        $used_bytes = $total_bytes - $free_bytes;
        $used_percent = ($used_bytes / $total_bytes) * 100;
        
        $status = 'ok';
        if ($used_percent > 90) {
            $status = 'critical';
        } elseif ($used_percent > 80) {
            $status = 'warning';
        }
        
        return [
            'status' => $status,
            'free_bytes' => $free_bytes,
            'total_bytes' => $total_bytes,
            'used_bytes' => $used_bytes,
            'used_percent' => round($used_percent, 2),
            'path' => $path
        ];
    }
    
    /**
     * Verificar uso de memória
     */
    public function checkMemory() {
        $memory_usage = memory_get_usage(true);
        $memory_peak = memory_get_peak_usage(true);
        $memory_limit = ini_get('memory_limit');
        
        // Converter memory_limit para bytes
        $memory_limit_bytes = $this->convertToBytes($memory_limit);
        $usage_percent = ($memory_usage / $memory_limit_bytes) * 100;
        
        $status = 'ok';
        if ($usage_percent > 90) {
            $status = 'critical';
        } elseif ($usage_percent > 80) {
            $status = 'warning';
        }
        
        return [
            'status' => $status,
            'current_usage_bytes' => $memory_usage,
            'peak_usage_bytes' => $memory_peak,
            'limit_bytes' => $memory_limit_bytes,
            'limit_string' => $memory_limit,
            'usage_percent' => round($usage_percent, 2)
        ];
    }
    
    /**
     * Executar todas as verificações
     */
    public function runAllChecks() {
        $this->checks = [
            'webhooks' => $this->checkWebhooks(),
            'logging_system' => $this->checkLoggingSystem(),
            'database' => $this->checkDatabase(),
            'disk_space' => $this->checkDiskSpace(),
            'memory' => $this->checkMemory()
        ];
        
        // Determinar status geral
        $overall_status = $this->determineOverallStatus();
        
        $execution_time = round((microtime(true) - $this->start_time) * 1000, 2);
        
        return [
            'status' => $overall_status,
            'environment' => $this->environment,
            'timestamp' => date('Y-m-d H:i:s'),
            'execution_time_ms' => $execution_time,
            'server' => $_SERVER['SERVER_NAME'] ?? 'unknown',
            'php_version' => PHP_VERSION,
            'checks' => $this->checks,
            'summary' => $this->generateSummary()
        ];
    }
    
    /**
     * Determinar status geral baseado nas verificações
     */
    private function determineOverallStatus() {
        $critical_errors = 0;
        $warnings = 0;
        
        foreach ($this->checks as $check_group) {
            if (is_array($check_group)) {
                foreach ($check_group as $check) {
                    if (isset($check['status'])) {
                        switch ($check['status']) {
                            case 'critical':
                                $critical_errors++;
                                break;
                            case 'warning':
                                $warnings++;
                                break;
                        }
                    }
                }
            }
        }
        
        if ($critical_errors > 0) {
            return 'critical';
        } elseif ($warnings > 0) {
            return 'warning';
        } else {
            return 'ok';
        }
    }
    
    /**
     * Gerar resumo das verificações
     */
    private function generateSummary() {
        $summary = [
            'total_checks' => 0,
            'ok_checks' => 0,
            'warning_checks' => 0,
            'error_checks' => 0,
            'critical_checks' => 0
        ];
        
        foreach ($this->checks as $check_group) {
            if (is_array($check_group)) {
                foreach ($check_group as $check) {
                    $summary['total_checks']++;
                    if (isset($check['status'])) {
                        switch ($check['status']) {
                            case 'ok':
                                $summary['ok_checks']++;
                                break;
                            case 'warning':
                                $summary['warning_checks']++;
                                break;
                            case 'error':
                                $summary['error_checks']++;
                                break;
                            case 'critical':
                                $summary['critical_checks']++;
                                break;
                        }
                    }
                }
            }
        }
        
        return $summary;
    }
    
    /**
     * Converter string de memória para bytes
     */
    private function convertToBytes($val) {
        $val = trim($val);
        $last = strtolower($val[strlen($val)-1]);
        $val = (int) $val;
        
        switch($last) {
            case 'g':
                $val *= 1024;
            case 'm':
                $val *= 1024;
            case 'k':
                $val *= 1024;
        }
        
        return $val;
    }
}

// Executar health check
$environment = $_GET['env'] ?? 'production';
$health_checker = new HealthChecker($environment);
$result = $health_checker->runAllChecks();

// Definir código HTTP baseado no status
$http_code = 200;
switch ($result['status']) {
    case 'critical':
        $http_code = 503;
        break;
    case 'warning':
        $http_code = 200; // Manter 200 para warnings
        break;
    case 'ok':
    default:
        $http_code = 200;
        break;
}

http_response_code($http_code);

// Retornar resultado
echo json_encode($result, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT);
?>