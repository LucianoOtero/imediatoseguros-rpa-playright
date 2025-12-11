<?php
/**
 * HEALTH CHECK ESPECÍFICO PARA WEBHOOKS
 * bpsegurosimediato.com.br/webhook_health.php
 * 
 * Health check focado especificamente nos webhooks
 * Verificações detalhadas de funcionalidade
 */

header('Content-Type: application/json; charset=utf-8');
header('X-Webhook-Health: active');
header('Cache-Control: no-cache, no-store, must-revalidate');

class WebhookHealthChecker {
    private $start_time;
    private $webhooks;
    
    public function __construct() {
        $this->start_time = microtime(true);
        $this->webhooks = [
            'travelangels' => [
                'file' => '/var/www/html/add_travelangels.php',
                'log' => '/var/www/html/logs_travelangels.txt',
                'url' => 'https://bpsegurosimediato.com.br/add_travelangels.php'
            ],
            'octadesk' => [
                'file' => '/var/www/html/add_webflow_octa.php',
                'log' => '/var/www/html/octa_webflow_webhook.log',
                'url' => 'https://bpsegurosimediato.com.br/add_webflow_octa.php'
            ],
            'debug_logger' => [
                'file' => '/var/www/html/debug_logger_db.php',
                'log' => '/var/www/html/logging_system/logs',
                'url' => 'https://bpsegurosimediato.com.br/debug_logger_db.php'
            ]
        ];
    }
    
    /**
     * Verificar arquivo do webhook
     */
    public function checkWebhookFile($webhook_name, $webhook_config) {
        $file_path = $webhook_config['file'];
        
        if (!file_exists($file_path)) {
            return [
                'status' => 'error',
                'error' => 'File not found',
                'path' => $file_path
            ];
        }
        
        $file_size = filesize($file_path);
        $last_modified = date('Y-m-d H:i:s', filemtime($file_path));
        $is_readable = is_readable($file_path);
        $is_writable = is_writable($file_path);
        
        // Verificar se contém código PHP válido
        $php_valid = false;
        if ($is_readable) {
            $content = file_get_contents($file_path);
            $php_valid = strpos($content, '<?php') !== false;
            
            // Verificar se contém funções essenciais
            $has_essential_functions = false;
            if ($webhook_name === 'travelangels') {
                $has_essential_functions = strpos($content, 'EspoApiClient') !== false;
            } elseif ($webhook_name === 'octadesk') {
                $has_essential_functions = strpos($content, 'log_rotate') !== false;
            } elseif ($webhook_name === 'debug_logger') {
                $has_essential_functions = strpos($content, 'Logger') !== false;
            }
        }
        
        return [
            'status' => $is_readable && $php_valid ? 'ok' : 'error',
            'path' => $file_path,
            'size_bytes' => $file_size,
            'last_modified' => $last_modified,
            'is_readable' => $is_readable,
            'is_writable' => $is_writable,
            'php_valid' => $php_valid,
            'has_essential_functions' => $has_essential_functions ?? false
        ];
    }
    
    /**
     * Verificar logs do webhook
     */
    public function checkWebhookLogs($webhook_name, $webhook_config) {
        $log_path = $webhook_config['log'];
        
        if (is_file($log_path)) {
            // É um arquivo de log
            $file_size = filesize($log_path);
            $last_modified = date('Y-m-d H:i:s', filemtime($log_path));
            $is_readable = is_readable($log_path);
            $is_writable = is_writable($log_path);
            
            // Verificar se foi modificado recentemente (últimas 24 horas)
            $recently_modified = (time() - filemtime($log_path)) < 86400;
            
            // Contar linhas de log
            $line_count = 0;
            if ($file_size > 0 && $is_readable) {
                $content = file_get_contents($log_path);
                $line_count = substr_count($content, PHP_EOL);
            }
            
            return [
                'status' => $is_readable && $is_writable ? 'ok' : 'warning',
                'type' => 'file',
                'path' => $log_path,
                'size_bytes' => $file_size,
                'last_modified' => $last_modified,
                'is_readable' => $is_readable,
                'is_writable' => $is_writable,
                'recently_modified' => $recently_modified,
                'line_count' => $line_count
            ];
        } elseif (is_dir($log_path)) {
            // É um diretório de logs
            $files = scandir($log_path);
            $log_files = array_filter($files, function($file) {
                return $file !== '.' && $file !== '..' && pathinfo($file, PATHINFO_EXTENSION) === 'txt';
            });
            
            $total_size = 0;
            $recent_files = 0;
            foreach ($log_files as $file) {
                $file_path = $log_path . '/' . $file;
                $total_size += filesize($file_path);
                if ((time() - filemtime($file_path)) < 86400) {
                    $recent_files++;
                }
            }
            
            return [
                'status' => is_writable($log_path) ? 'ok' : 'warning',
                'type' => 'directory',
                'path' => $log_path,
                'total_size_bytes' => $total_size,
                'log_files_count' => count($log_files),
                'recent_files_count' => $recent_files,
                'is_writable' => is_writable($log_path)
            ];
        } else {
            return [
                'status' => 'error',
                'type' => 'missing',
                'path' => $log_path,
                'error' => 'Log file or directory not found'
            ];
        }
    }
    
    /**
     * Verificar conectividade do webhook
     */
    public function checkWebhookConnectivity($webhook_name, $webhook_config) {
        $url = $webhook_config['url'];
        
        // Fazer requisição HEAD para verificar se endpoint responde
        $context = stream_context_create([
            'http' => [
                'method' => 'HEAD',
                'timeout' => 10,
                'ignore_errors' => true
            ]
        ]);
        
        $start_time = microtime(true);
        $headers = @get_headers($url, 1, $context);
        $response_time = round((microtime(true) - $start_time) * 1000, 2);
        
        if ($headers && isset($headers[0])) {
            $http_status = $headers[0];
            $status_code = (int) substr($http_status, 9, 3);
            
            // Para webhooks, esperamos 405 (Method Not Allowed) para HEAD requests
            // ou 200 se aceitar HEAD
            $is_healthy = in_array($status_code, [200, 405]);
            
            return [
                'status' => $is_healthy ? 'ok' : 'warning',
                'url' => $url,
                'http_status' => $http_status,
                'status_code' => $status_code,
                'response_time_ms' => $response_time,
                'is_healthy' => $is_healthy
            ];
        } else {
            return [
                'status' => 'error',
                'url' => $url,
                'response_time_ms' => $response_time,
                'error' => 'Connection failed or timeout'
            ];
        }
    }
    
    /**
     * Executar todas as verificações para um webhook
     */
    public function checkWebhook($webhook_name, $webhook_config) {
        return [
            'name' => $webhook_name,
            'file_check' => $this->checkWebhookFile($webhook_name, $webhook_config),
            'logs_check' => $this->checkWebhookLogs($webhook_name, $webhook_config),
            'connectivity_check' => $this->checkWebhookConnectivity($webhook_name, $webhook_config)
        ];
    }
    
    /**
     * Executar verificações para todos os webhooks
     */
    public function runAllWebhookChecks() {
        $results = [];
        $overall_status = 'ok';
        
        foreach ($this->webhooks as $name => $config) {
            $webhook_result = $this->checkWebhook($name, $config);
            $results[$name] = $webhook_result;
            
            // Determinar status do webhook
            $webhook_status = $this->determineWebhookStatus($webhook_result);
            $results[$name]['overall_status'] = $webhook_status;
            
            // Atualizar status geral
            if ($webhook_status === 'error') {
                $overall_status = 'error';
            } elseif ($webhook_status === 'warning' && $overall_status === 'ok') {
                $overall_status = 'warning';
            }
        }
        
        $execution_time = round((microtime(true) - $this->start_time) * 1000, 2);
        
        return [
            'status' => $overall_status,
            'timestamp' => date('Y-m-d H:i:s'),
            'execution_time_ms' => $execution_time,
            'server' => $_SERVER['SERVER_NAME'] ?? 'unknown',
            'webhooks' => $results,
            'summary' => $this->generateWebhookSummary($results)
        ];
    }
    
    /**
     * Determinar status de um webhook baseado nas verificações
     */
    private function determineWebhookStatus($webhook_result) {
        $checks = [
            $webhook_result['file_check']['status'],
            $webhook_result['logs_check']['status'],
            $webhook_result['connectivity_check']['status']
        ];
        
        if (in_array('error', $checks)) {
            return 'error';
        } elseif (in_array('warning', $checks)) {
            return 'warning';
        } else {
            return 'ok';
        }
    }
    
    /**
     * Gerar resumo das verificações de webhooks
     */
    private function generateWebhookSummary($results) {
        $summary = [
            'total_webhooks' => count($results),
            'ok_webhooks' => 0,
            'warning_webhooks' => 0,
            'error_webhooks' => 0,
            'webhook_details' => []
        ];
        
        foreach ($results as $name => $result) {
            $summary['webhook_details'][$name] = [
                'status' => $result['overall_status'],
                'file_ok' => $result['file_check']['status'] === 'ok',
                'logs_ok' => $result['logs_check']['status'] === 'ok',
                'connectivity_ok' => $result['connectivity_check']['status'] === 'ok'
            ];
            
            switch ($result['overall_status']) {
                case 'ok':
                    $summary['ok_webhooks']++;
                    break;
                case 'warning':
                    $summary['warning_webhooks']++;
                    break;
                case 'error':
                    $summary['error_webhooks']++;
                    break;
            }
        }
        
        return $summary;
    }
}

// Executar verificações de webhooks
$webhook_checker = new WebhookHealthChecker();
$result = $webhook_checker->runAllWebhookChecks();

// Definir código HTTP baseado no status
$http_code = 200;
switch ($result['status']) {
    case 'error':
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