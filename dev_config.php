<?php
/**
 * CONFIGURAÇÃO DO AMBIENTE DE DESENVOLVIMENTO
 * bpsegurosimediato.com.br/dev_config.php
 * 
 * Este arquivo contém todas as configurações específicas para o ambiente de desenvolvimento
 * Separado da produção para testes seguros da API V2
 */

// Identificar ambiente de desenvolvimento
$is_dev = strpos($_SERVER['HTTP_HOST'], 'dev.') !== false || 
          strpos($_SERVER['REQUEST_URI'], '/dev/') !== false ||
          isset($_GET['dev']) || isset($_POST['dev']);

// Configurações do ambiente
$DEV_CONFIG = [
    'environment' => 'development',
    'debug' => true,
    'log_level' => 'debug',
    'cors_enabled' => true,
    'rate_limit' => false, // Desabilitado em dev para testes
    'max_log_size' => 1024 * 1024, // 1MB em dev
    'log_backups' => 3
];

// URLs dos webhooks de desenvolvimento
$DEV_WEBHOOK_URLS = [
    'travelangels' => 'https://bpsegurosimediato.com.br/dev/webhooks/add_travelangels.php',
    'octadesk' => 'https://bpsegurosimediato.com.br/dev/webhooks/add_webflow_octa.php',
    'health' => 'https://bpsegurosimediato.com.br/dev/webhooks/health.php'
];

// ⚠️ SECRET KEYS REMOVIDAS - Agora centralizadas em PHP-FPM
// Use getWebflowSecretFlyingDonkeys() e getWebflowSecretOctaDesk() de config.php
// $DEV_WEBFLOW_SECRETS removido - não é mais necessário
// As secret keys agora são definidas em PHP-FPM (variáveis de ambiente) e acessadas via config.php

// Configurações de logging para desenvolvimento
$DEV_LOGGING = [
    'travelangels' => '/var/www/html/dev/logs/travelangels_dev.txt',
    'octadesk' => '/var/www/html/dev/logs/octadesk_dev.txt',
    'general' => '/var/www/html/dev/logs/general_dev.txt',
    'errors' => '/var/www/html/dev/logs/errors_dev.txt'
];

// Dados de teste para desenvolvimento
$DEV_TEST_DATA = [
    'travelangels' => [
        'name' => 'TESTE DEV TRAVELANGELS',
        'email' => 'teste.travelangels@dev.com',
        'phone' => '11999999999',
        'source' => 'webflow_dev_travelangels',
        'test_mode' => true
    ],
    'octadesk' => [
        'name' => 'TESTE DEV OCTADESK',
        'email' => 'teste.octadesk@dev.com',
        'phone' => '11888888888',
        'subject' => 'Teste de Desenvolvimento',
        'message' => 'Este é um teste do ambiente de desenvolvimento',
        'test_mode' => true
    ]
];

// Configurações de API V2 para desenvolvimento
$DEV_API_V2_CONFIG = [
    'signature_validation' => true,
    'fallback_on_error' => true, // Continuar processamento se signature falhar
    'detailed_logging' => true,
    'test_mode' => true,
    'mock_responses' => false // Usar respostas reais mas com logs detalhados
];

// Headers de segurança para desenvolvimento
$DEV_SECURITY_HEADERS = [
    'X-Content-Type-Options' => 'nosniff',
    'X-Frame-Options' => 'SAMEORIGIN', // Mais permissivo em dev
    'X-XSS-Protection' => '1; mode=block',
    'Cache-Control' => 'no-cache, no-store, must-revalidate',
    'Pragma' => 'no-cache',
    'Expires' => '0',
    'X-Environment' => 'development',
    'X-API-Version' => '2.0-dev'
];

// Função para aplicar configurações de desenvolvimento
function applyDevConfig() {
    global $DEV_CONFIG, $DEV_SECURITY_HEADERS, $is_dev;
    
    if (!$is_dev) return;
    
    // Aplicar headers de segurança específicos para dev
    foreach ($DEV_SECURITY_HEADERS as $header => $value) {
        header("$header: $value");
    }
    
    // Configurar error reporting para desenvolvimento
    error_reporting(E_ALL);
    ini_set('display_errors', 1);
    ini_set('log_errors', 1);
    ini_set('error_log', '/var/www/html/dev/logs/php_errors.log');
}

// Função para log específico de desenvolvimento
function logDevEvent($event, $data, $success = true) {
    global $DEV_LOGGING, $is_dev;
    
    if (!$is_dev) return;
    
    $log_data = [
        'timestamp' => date('Y-m-d H:i:s'),
        'environment' => 'development',
        'event' => $event,
        'success' => $success,
        'data' => $data,
        'request_id' => uniqid('dev_', true),
        'memory_usage' => memory_get_usage(true),
        'execution_time' => microtime(true) - $_SERVER['REQUEST_TIME_FLOAT']
    ];
    
    $log_file = $DEV_LOGGING['general'];
    $log_entry = '[DEV] ' . json_encode($log_data, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT) . PHP_EOL;
    
    file_put_contents($log_file, $log_entry, FILE_APPEND | LOCK_EX);
}

// Função para validar ambiente de desenvolvimento
function validateDevEnvironment() {
    global $is_dev, $DEV_CONFIG;
    
    if (!$is_dev) {
        return ['valid' => false, 'message' => 'Não é ambiente de desenvolvimento'];
    }
    
    // Verificar se diretórios existem
    $required_dirs = [
        '/var/www/html/dev',
        '/var/www/html/dev/logs',
        '/var/www/html/dev/webhooks'
    ];
    
    foreach ($required_dirs as $dir) {
        if (!is_dir($dir)) {
            return ['valid' => false, 'message' => "Diretório não encontrado: $dir"];
        }
    }
    
    // Verificar permissões de escrita
    $log_dir = '/var/www/html/dev/logs';
    if (!is_writable($log_dir)) {
        return ['valid' => false, 'message' => "Sem permissão de escrita em: $log_dir"];
    }
    
    return ['valid' => true, 'message' => 'Ambiente de desenvolvimento configurado corretamente'];
}

// Aplicar configurações automaticamente
applyDevConfig();

// Log de inicialização do ambiente de desenvolvimento
if ($is_dev) {
    logDevEvent('environment_init', [
        'config' => $DEV_CONFIG,
        'validation' => validateDevEnvironment()
    ], true);
}
?>