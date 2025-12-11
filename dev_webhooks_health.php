<?php
/**
 * HEALTH CHECK - WEBHOOKS DE DESENVOLVIMENTO
 * bpsegurosimediato.com.br/dev/webhooks/health.php
 * 
 * Health check específico para webhooks de desenvolvimento
 * Verificações detalhadas de funcionalidade dos webhooks dev
 */

// Incluir configuração de desenvolvimento
require_once '/var/www/html/dev_config.php';

// Verificar se é ambiente de desenvolvimento
if (!$is_dev) {
    http_response_code(403);
    exit('Acesso negado: Este endpoint é apenas para desenvolvimento');
}

// Headers específicos para desenvolvimento
header('Content-Type: application/json; charset=utf-8');
header('X-Environment: development');
header('X-Health-Check: dev-webhooks');
header('Cache-Control: no-cache, no-store, must-revalidate');

class DevWebhookHealthChecker {
    private $start_time;
    private $environment;
    
    public function __construct() {
        $this->start_time = microtime(true);
        $this->environment = 'development';
    }
    
    /**
     * Verificar webhooks de desenvolvimento
     */
    public function checkDevWebhooks() {
        $dev_webhooks = [
            'travelangels_dev' => '/var/www/html/dev/webhooks/add_travelangels.php',
            'octadesk_dev' => '/var/www/html/dev/webhooks/add_webflow_octa.php',
            'health_dev' => '/var/www/html/dev/webhooks/health.php'
        ];
        
        $results = [];
        foreach ($dev_webhooks as $name => $path) {
            $file_exists = file_exists($path);
            $is_readable = $file_exists ? is_readable($path) : false;
            $last_modified = $file_exists ? date('Y-m-d H:i:s', filemtime($path)) : null;
            $file_size = $file_exists ? filesize($path) : 0;
            
            // Verificar se contém código de desenvolvimento
            $has_dev_code = false;
            if ($file_exists) {
                $content = file_get_contents($path);
                $has_dev_code = strpos($content, 'development') !== false || 
                               strpos($content, 'dev_config') !== false;
            }
            
            $results[$name] = [
                'status' => $file_exists && $is_readable ? 'ok' : 'error',
                'file_exists' => $file_exists,
                'is_readable' => $is_readable,
                'last_modified' => $last_modified,
                'size_bytes' => $file_size,
                'has_dev_code' => $has_dev_code,
                'path' => $path
            ];
        }
        
        return $results;
    }
    
    /**
     * Verificar logs de desenvolvimento
     */
    public function checkDevLogs() {
        $dev_log_files = [
            'travelangels_dev' => '/var/www/html/dev/logs/travelangels_dev.txt',
            'octadesk_dev' => '/var/www/html/dev/logs/octadesk_dev.txt',
            'general_dev' => '/var/www/html/dev/logs/general_dev.txt',
            'errors_dev' => '/var/www/html/dev/logs/errors_dev.txt'
        ];
        
        $results = [];
        foreach ($dev_log_files as $name => $path) {
            if (file_exists($path)) {
                $file_size = filesize($path);
                $last_modified = date('Y-m-d H:i:s', filemtime($path));
                $is_writable = is_writable($path);
                
                // Contar linhas de log
                $line_count = 0;
                if ($file_size > 0) {
                    $content = file_get_contents($path);
                    $line_count = substr_count($content, PHP_EOL);
                }
                
                $results[$name] = [
                    'status' => $is_writable ? 'ok' : 'warning',
                    'type' => 'file',
                    'path' => $path,
                    'size_bytes' => $file_size,
                    'last_modified' => $last_modified,
                    'is_writable' => $is_writable,
                    'line_count' => $line_count
                ];
            } else {
                // Verificar se diretório pai existe e é gravável
                $parent_dir = dirname($path);
                $parent_writable = is_dir($parent_dir) && is_writable($parent_dir);
                
                $results[$name] = [
                    'status' => $parent_writable ? 'warning' : 'error',
                    'type' => 'missing',
                    'path' => $path,
                    'parent_dir_exists' => is_dir($parent_dir),
                    'parent_dir_writable' => $parent_writable,
                    'can_create' => $parent_writable
                ];
            }
        }
        
        return $results;
    }
    
    /**
     * Verificar configurações de desenvolvimento
     */
    public function checkDevConfig() {
        $config_files = [
            'dev_config' => '/var/www/html/dev_config.php',
            'app_config' => '/var/www/html/logging_system/config/app.php'
        ];
        
        $results = [];
        foreach ($config_files as $name => $path) {
            if (file_exists($path)) {
                $file_size = filesize($path);
                $last_modified = date('Y-m-d H:i:s', filemtime($path));
                $is_readable = is_readable($path);
                
                // Verificar se contém configurações específicas
                $content = file_get_contents($path);
                $has_dev_settings = strpos($content, 'development') !== false || 
                                   strpos($content, 'DEBUG') !== false;
                
                $results[$name] = [
                    'status' => $is_readable ? 'ok' : 'error',
                    'path' => $path,
                    'size_bytes' => $file_size,
                    'last_modified' => $last_modified,
                    'is_readable' => $is_readable,
                    'has_dev_settings' => $has_dev_settings
                ];
            } else {
                $results[$name] = [
                    'status' => 'error',
                    'path' => $path,
                    'error' => 'Config file not found'
                ];
            }
        }
        
        return $results;
    }
    
    /**
     * Testar webhooks de desenvolvimento
     */
    public function testDevWebhooks() {
        $webhook_tests = [
            'travelangels_test' => [
                'url' => 'https://bpsegurosimediato.com.br/dev/webhooks/add_travelangels.php',
                'method' => 'POST',
                'test_data' => [
                    'name' => 'TESTE DEV HEALTH CHECK',
                    'email' => 'teste.health@dev.com',
                    'phone' => '11999999999',
                    'test_mode' => true
                ]
            ],
            'octadesk_test' => [
                'url' => 'https://bpsegurosimediato.com.br/dev/webhooks/add_webflow_octa.php',
                'method' => 'POST',
                'test_data' => [
                    'name' => 'TESTE DEV HEALTH CHECK',
                    'email' => 'teste.health@dev.com',
                    'phone' => '11888888888',
                    'subject' => 'Teste de Health Check',
                    'message' => 'Teste automático do health check de desenvolvimento',
                    'test_mode' => true
                ]
            ]
        ];
        
        $results = [];
        foreach ($webhook_tests as $name => $test) {
            $start_time = microtime(true);
            
            // Simular teste (não fazer requisição real para evitar loops)
            $test_result = [
                'status' => 'simulated',
                'url' => $test['url'],
                'method' => $test['method'],
                'test_data' => $test['test_data'],
                'response_time_ms' => round((microtime(true) - $start_time) * 1000, 2),
                'note' => 'Teste simulado para evitar loops de requisição'
            ];
            
            // Verificar se arquivo existe
            $webhook_file = str_replace('https://bpsegurosimediato.com.br/dev/webhooks/', '/var/www/html/dev/webhooks/', $test['url']);
            $test_result['file_exists'] = file_exists($webhook_file);
            $test_result['file_readable'] = file_exists($webhook_file) ? is_readable($webhook_file) : false;
            
            $results[$name] = $test_result;
        }
        
        return $results;
    }
    
    /**
     * Executar verificações específicas de desenvolvimento
     */
    public function runDevChecks() {
        $dev_checks = [
            'dev_webhooks' => $this->checkDevWebhooks(),
            'dev_logs' => $this->checkDevLogs(),
            'dev_config' => $this->checkDevConfig(),
            'dev_webhook_tests' => $this->testDevWebhooks()
        ];
        
        // Determinar status geral para desenvolvimento
        $overall_status = $this->determineDevStatus($dev_checks);
        
        $execution_time = round((microtime(true) - $this->start_time) * 1000, 2);
        
        return [
            'status' => $overall_status,
            'environment' => 'development',
            'timestamp' => date('Y-m-d H:i:s'),
            'execution_time_ms' => $execution_time,
            'server' => $_SERVER['SERVER_NAME'] ?? 'unknown',
            'php_version' => PHP_VERSION,
            'dev_checks' => $dev_checks,
            'summary' => $this->generateDevSummary($dev_checks)
        ];
    }
    
    /**
     * Determinar status específico para desenvolvimento
     */
    private function determineDevStatus($dev_checks) {
        $critical_errors = 0;
        $warnings = 0;
        
        foreach ($dev_checks as $check_group) {
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
        
        // Em desenvolvimento, ser mais tolerante com warnings
        if ($critical_errors > 0) {
            return 'critical';
        } elseif ($warnings > 2) { // Mais tolerante com warnings
            return 'warning';
        } else {
            return 'ok';
        }
    }
    
    /**
     * Gerar resumo específico para desenvolvimento
     */
    private function generateDevSummary($dev_checks) {
        $summary = [
            'total_dev_checks' => 0,
            'ok_dev_checks' => 0,
            'warning_dev_checks' => 0,
            'error_dev_checks' => 0,
            'critical_dev_checks' => 0,
            'dev_environment_ready' => false
        ];
        
        foreach ($dev_checks as $check_group) {
            if (is_array($check_group)) {
                foreach ($check_group as $check) {
                    $summary['total_dev_checks']++;
                    if (isset($check['status'])) {
                        switch ($check['status']) {
                            case 'ok':
                                $summary['ok_dev_checks']++;
                                break;
                            case 'warning':
                                $summary['warning_dev_checks']++;
                                break;
                            case 'error':
                                $summary['error_dev_checks']++;
                                break;
                            case 'critical':
                                $summary['critical_dev_checks']++;
                                break;
                        }
                    }
                }
            }
        }
        
        // Determinar se ambiente de desenvolvimento está pronto
        $summary['dev_environment_ready'] = $summary['critical_dev_checks'] === 0 && 
                                           $summary['error_dev_checks'] <= 1;
        
        return $summary;
    }
}

// Executar health check de desenvolvimento
$dev_health_checker = new DevWebhookHealthChecker();
$result = $dev_health_checker->runDevChecks();

// Log do health check de desenvolvimento
logDevEvent('health_check_dev_webhooks', [
    'status' => $result['status'],
    'execution_time' => $result['execution_time_ms'],
    'summary' => $result['summary']
], $result['status'] === 'ok');

// Definir código HTTP baseado no status
$http_code = 200;
switch ($result['status']) {
    case 'critical':
        $http_code = 503;
        break;
    case 'warning':
        $http_code = 200; // Manter 200 para warnings em dev
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

































