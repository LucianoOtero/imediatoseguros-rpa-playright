<?php
/**
 * Configuração Centralizada - Sistema de Logging RPA
 * Arquivo único com todas as configurações do sistema
 */

return [
    'database' => [
        'host' => 'localhost',
        'port' => 3306,
        'database' => 'rpa_logs',
        'username' => 'rpa_user',
        'password' => 'RpaLogs2025!',
        'charset' => 'utf8mb4',
        'options' => [
            PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
            PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
            PDO::ATTR_EMULATE_PREPARES => false,
        ]
    ],
    
    'server' => [
        'timezone' => 'America/Sao_Paulo',
        'max_execution_time' => 30,
        'memory_limit' => '128M',
        'error_reporting' => E_ALL,
        'display_errors' => false,
        'log_errors' => true
    ],
    
    'cors' => [
        'allowed_origins' => [
            'https://www.segurosimediato.com.br',
            'https://segurosimediato.com.br'
        ],
        'allowed_methods' => ['POST', 'OPTIONS'],
        'allowed_headers' => ['Content-Type', 'X-Requested-With'],
        'max_age' => 86400
    ],
    
    'logging' => [
        'default_handler' => 'database', // CRÍTICO: Usar banco de dados como padrão
        'levels' => ['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        'retention_days' => 30,
        'max_file_size' => '10MB',
        'fallback_file' => '/var/www/html/logging_system/logs/debug_rpa_fallback.log',
        'rate_limit' => [
            'enabled' => true,
            'max_requests' => 100,
            'time_window' => 3600 // 1 hora
        ]
    ],
    
    'security' => [
        'validate_ip' => true,
        'validate_user_agent' => true,
        'max_request_size' => 10240, // 10KB
        'allowed_content_types' => ['application/json']
    ]
];


































