<?php

return [
    'app' => [
        'name' => 'RPA V4',
        'version' => '4.0.0',
        'environment' => $_ENV['APP_ENV'] ?? 'production',
        'debug' => $_ENV['APP_DEBUG'] ?? false,
    ],
    
    'rpa' => [
        'base_path' => '/opt/imediatoseguros-rpa',
        'sessions_path' => '/opt/imediatoseguros-rpa/sessions',
        'data_path' => '/opt/imediatoseguros-rpa/rpa_data',
        'scripts_path' => '/opt/imediatoseguros-rpa/scripts',
        'timeout' => 3600, // 1 hora
        'max_concurrent_sessions' => 5,
    ],
    
    'redis' => [
        'host' => $_ENV['REDIS_HOST'] ?? '127.0.0.1',
        'port' => $_ENV['REDIS_PORT'] ?? 6379,
        'password' => $_ENV['REDIS_PASSWORD'] ?? null,
        'database' => $_ENV['REDIS_DATABASE'] ?? 0,
    ],
    
    'rate_limit' => [
        'enabled' => true,
        'max_requests' => 100,
        'window' => 3600, // 1 hora
    ],
    
    'logging' => [
        'enabled' => true,
        'level' => $_ENV['LOG_LEVEL'] ?? 'info',
        'path' => __DIR__ . '/../logs/rpa/app.log',
        'max_files' => 30,
    ],
    
    'validation' => [
        'cpf' => [
            'required' => true,
            'pattern' => '/^\d{11}$/',
        ],
        'nome' => [
            'required' => true,
            'min_length' => 2,
            'max_length' => 100,
        ],
    ],
];
