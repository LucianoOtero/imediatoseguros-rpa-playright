<?php
/**
 * config/security.php - Configurações de Segurança
 * Sistema de Logging PHP - RPA Imediato Seguros
 */

// Configurações de segurança
$security_config = [
    'rate_limit' => [
        'enabled' => true,
        'max_requests_per_minute' => 100,
        'max_requests_per_hour' => 1000,
        'ban_duration_minutes' => 60
    ],
    'cors' => [
        'enabled' => true,
        'allowed_origins' => [
            'https://www.segurosimediato.com.br',
            'https://segurosimediato.com.br',
            'https://mdmidia.com.br'
        ],
        'allowed_methods' => ['POST', 'OPTIONS'],
        'allowed_headers' => ['Content-Type', 'X-Requested-With']
    ],
    'input_validation' => [
        'max_message_length' => 1000,
        'max_data_size' => 50000, // 50KB
        'allowed_levels' => ['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        'sanitize_input' => true
    ],
    'logging' => [
        'log_security_events' => true,
        'log_failed_attempts' => true,
        'max_security_logs' => 1000
    ]
];

/**
 * Verifica rate limiting
 * @return bool
 */
function checkRateLimit() {
    global $security_config;
    
    if (!$security_config['rate_limit']['enabled']) {
        return true;
    }
    
    $ip = getClientIP();
    $current_time = time();
    $minute_key = "rate_limit_minute_{$ip}_" . floor($current_time / 60);
    $hour_key = "rate_limit_hour_{$ip}_" . floor($current_time / 3600);
    
    // Verificar limite por minuto
    $minute_count = getRateLimitCount($minute_key);
    if ($minute_count >= $security_config['rate_limit']['max_requests_per_minute']) {
        logSecurityEvent('RATE_LIMIT_EXCEEDED', [
            'ip' => $ip,
            'limit_type' => 'minute',
            'count' => $minute_count,
            'limit' => $security_config['rate_limit']['max_requests_per_minute']
        ]);
        return false;
    }
    
    // Verificar limite por hora
    $hour_count = getRateLimitCount($hour_key);
    if ($hour_count >= $security_config['rate_limit']['max_requests_per_hour']) {
        logSecurityEvent('RATE_LIMIT_EXCEEDED', [
            'ip' => $ip,
            'limit_type' => 'hour',
            'count' => $hour_count,
            'limit' => $security_config['rate_limit']['max_requests_per_hour']
        ]);
        return false;
    }
    
    // Incrementar contadores
    incrementRateLimitCount($minute_key);
    incrementRateLimitCount($hour_key);
    
    return true;
}

/**
 * Obtém contagem de rate limit
 * @param string $key
 * @return int
 */
function getRateLimitCount($key) {
    // Usar arquivo temporário para simplicidade
    // Em produção, usar Redis ou Memcached
    $file = sys_get_temp_dir() . "/rate_limit_{$key}.txt";
    
    if (!file_exists($file)) {
        return 0;
    }
    
    $content = file_get_contents($file);
    $data = json_decode($content, true);
    
    if (!$data || $data['expires'] < time()) {
        return 0;
    }
    
    return $data['count'];
}

/**
 * Incrementa contagem de rate limit
 * @param string $key
 */
function incrementRateLimitCount($key) {
    $file = sys_get_temp_dir() . "/rate_limit_{$key}.txt";
    $current_count = getRateLimitCount($key);
    
    $data = [
        'count' => $current_count + 1,
        'expires' => time() + 3600 // Expira em 1 hora
    ];
    
    file_put_contents($file, json_encode($data), LOCK_EX);
}

/**
 * Verifica política CORS
 * @return bool
 */
function checkCORS() {
    global $security_config;
    
    if (!$security_config['cors']['enabled']) {
        return true;
    }
    
    $origin = $_SERVER['HTTP_ORIGIN'] ?? '';
    
    if (empty($origin)) {
        return true; // Requisições sem origin são permitidas
    }
    
    $allowed_origins = $security_config['cors']['allowed_origins'];
    
    // Verificar se origin está na lista de permitidos
    foreach ($allowed_origins as $allowed_origin) {
        if ($origin === $allowed_origin || 
            (strpos($allowed_origin, '*') !== false && fnmatch($allowed_origin, $origin))) {
            return true;
        }
    }
    
    logSecurityEvent('CORS_VIOLATION', [
        'origin' => $origin,
        'allowed_origins' => $allowed_origins
    ]);
    
    return false;
}

/**
 * Valida entrada de dados
 * @param array $data
 * @return array
 */
function validateSecurityInput($data) {
    global $security_config;
    
    $errors = [];
    
    // Validar tamanho da mensagem
    if (isset($data['message']) && strlen($data['message']) > $security_config['input_validation']['max_message_length']) {
        $errors[] = 'Message too long';
    }
    
    // Validar tamanho dos dados
    if (isset($data['data'])) {
        $data_size = is_string($data['data']) ? strlen($data['data']) : strlen(json_encode($data['data']));
        if ($data_size > $security_config['input_validation']['max_data_size']) {
            $errors[] = 'Data too large';
        }
    }
    
    // Validar nível de log
    if (isset($data['level']) && !in_array(strtoupper($data['level']), $security_config['input_validation']['allowed_levels'])) {
        $errors[] = 'Invalid log level';
    }
    
    // Verificar padrões suspeitos
    if (isset($data['message']) && containsSuspiciousPatterns($data['message'])) {
        $errors[] = 'Suspicious content detected';
        logSecurityEvent('SUSPICIOUS_CONTENT', [
            'message' => substr($data['message'], 0, 100),
            'ip' => getClientIP()
        ]);
    }
    
    return $errors;
}

/**
 * Verifica padrões suspeitos
 * @param string $content
 * @return bool
 */
function containsSuspiciousPatterns($content) {
    $suspicious_patterns = [
        '/<script[^>]*>.*?<\/script>/i',
        '/javascript:/i',
        '/on\w+\s*=/i',
        '/eval\s*\(/i',
        '/expression\s*\(/i',
        '/union\s+select/i',
        '/drop\s+table/i',
        '/insert\s+into/i',
        '/delete\s+from/i',
        '/update\s+set/i'
    ];
    
    foreach ($suspicious_patterns as $pattern) {
        if (preg_match($pattern, $content)) {
            return true;
        }
    }
    
    return false;
}

/**
 * Sanitiza entrada de dados
 * @param mixed $data
 * @return mixed
 */
function sanitizeSecurityInput($data) {
    global $security_config;
    
    if (!$security_config['input_validation']['sanitize_input']) {
        return $data;
    }
    
    if (is_string($data)) {
        // Remover caracteres de controle
        $data = preg_replace('/[\x00-\x1F\x7F]/', '', $data);
        
        // Escapar caracteres especiais
        $data = htmlspecialchars($data, ENT_QUOTES, 'UTF-8');
        
        return $data;
    }
    
    if (is_array($data)) {
        return array_map('sanitizeSecurityInput', $data);
    }
    
    return $data;
}

/**
 * Registra evento de segurança
 * @param string $event
 * @param array $data
 */
function logSecurityEvent($event, $data = []) {
    global $security_config;
    
    if (!$security_config['logging']['log_security_events']) {
        return;
    }
    
    try {
        $pdo = getDatabaseConnection();
        
        $stmt = $pdo->prepare("
            INSERT INTO debug_logs (
                log_id, session_id, timestamp, level, message, 
                data, url, user_agent, ip_address, server_time, request_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ");
        
        $stmt->execute([
            uniqid('security_', true),
            'security',
            date('Y-m-d H:i:s'),
            'WARNING',
            "Security event: $event",
            json_encode($data),
            'security://internal',
            'Security System',
            getClientIP(),
            microtime(true),
            uniqid('sec_', true)
        ]);
        
    } catch (Exception $e) {
        error_log("Security logging error: " . $e->getMessage());
    }
}

/**
 * Obtém IP real do cliente
 * @return string
 */
function getClientIP() {
    $ipKeys = ['HTTP_X_FORWARDED_FOR', 'HTTP_X_REAL_IP', 'HTTP_CLIENT_IP', 'REMOTE_ADDR'];
    
    foreach ($ipKeys as $key) {
        if (!empty($_SERVER[$key])) {
            $ip = $_SERVER[$key];
            // Se há múltiplos IPs (proxy), pegar o primeiro
            if (strpos($ip, ',') !== false) {
                $ip = trim(explode(',', $ip)[0]);
            }
            // Validar IP
            if (filter_var($ip, FILTER_VALIDATE_IP, FILTER_FLAG_NO_PRIV_RANGE | FILTER_FLAG_NO_RES_RANGE)) {
                return $ip;
            }
        }
    }
    
    return $_SERVER['REMOTE_ADDR'] ?? 'unknown';
}

/**
 * Verifica se IP está bloqueado
 * @param string $ip
 * @return bool
 */
function isIPBlocked($ip) {
    // Lista de IPs bloqueados (em produção, usar banco de dados)
    $blocked_ips = [
        // Adicionar IPs bloqueados aqui
    ];
    
    return in_array($ip, $blocked_ips);
}

/**
 * Bloqueia IP temporariamente
 * @param string $ip
 * @param int $minutes
 */
function blockIP($ip, $minutes = 60) {
    $file = sys_get_temp_dir() . "/blocked_ip_{$ip}.txt";
    $data = [
        'blocked_at' => time(),
        'expires_at' => time() + ($minutes * 60)
    ];
    
    file_put_contents($file, json_encode($data), LOCK_EX);
    
    logSecurityEvent('IP_BLOCKED', [
        'ip' => $ip,
        'duration_minutes' => $minutes
    ]);
}

/**
 * Verifica se IP está temporariamente bloqueado
 * @param string $ip
 * @return bool
 */
function isIPTemporarilyBlocked($ip) {
    $file = sys_get_temp_dir() . "/blocked_ip_{$ip}.txt";
    
    if (!file_exists($file)) {
        return false;
    }
    
    $content = file_get_contents($file);
    $data = json_decode($content, true);
    
    if (!$data || $data['expires_at'] < time()) {
        unlink($file); // Remover arquivo expirado
        return false;
    }
    
    return true;
}

/**
 * Obtém estatísticas de segurança
 * @return array
 */
function getSecurityStats() {
    try {
        $pdo = getDatabaseConnection();
        
        $stats = [];
        
        // Eventos de segurança das últimas 24 horas
        $stmt = $pdo->prepare('
            SELECT COUNT(*) as count 
            FROM debug_logs 
            WHERE session_id = "security" 
            AND timestamp > DATE_SUB(NOW(), INTERVAL 24 HOUR)
        ');
        $stmt->execute();
        $stats['security_events_24h'] = $stmt->fetch()['count'];
        
        // Rate limit violations
        $stmt = $pdo->prepare('
            SELECT COUNT(*) as count 
            FROM debug_logs 
            WHERE message LIKE "%Rate limit exceeded%" 
            AND timestamp > DATE_SUB(NOW(), INTERVAL 24 HOUR)
        ');
        $stmt->execute();
        $stats['rate_limit_violations_24h'] = $stmt->fetch()['count'];
        
        // CORS violations
        $stmt = $pdo->prepare('
            SELECT COUNT(*) as count 
            FROM debug_logs 
            WHERE message LIKE "%CORS violation%" 
            AND timestamp > DATE_SUB(NOW(), INTERVAL 24 HOUR)
        ');
        $stmt->execute();
        $stats['cors_violations_24h'] = $stmt->fetch()['count'];
        
        return $stats;
        
    } catch (Exception $e) {
        return [
            'error' => $e->getMessage()
        ];
    }
}
?>




































