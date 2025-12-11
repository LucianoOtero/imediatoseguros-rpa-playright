<?php
/**
 * API de Análise de Logs
 * Sistema de Logging RPA - Imediato Seguros
 * Baseado na documentação completa do projeto
 */

// Configurações
error_reporting(E_ALL);
ini_set('display_errors', 0);
ini_set('log_errors', 1);
date_default_timezone_set('America/Sao_Paulo');

// Headers CORS
header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type, X-Requested-With');

// Responder a requisições OPTIONS
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit(0);
}

// Validar método HTTP
if ($_SERVER['REQUEST_METHOD'] !== 'GET') {
    http_response_code(405);
    echo json_encode(['success' => false, 'error' => 'Method not allowed']);
    exit(1);
}

try {
    // Carregar configuração
    $config = require_once '/var/www/html/logging_system/config/app.php';
    
    // Conectar ao banco
    $dsn = sprintf(
        'mysql:host=%s;port=%d;dbname=%s;charset=%s',
        $config['database']['host'],
        $config['database']['port'],
        $config['database']['database'],
        $config['database']['charset']
    );
    
    $pdo = new PDO(
        $dsn,
        $config['database']['username'],
        $config['database']['password'],
        $config['database']['options']
    );
    
    // Obter ação
    $action = $_GET['action'] ?? 'stats';
    
    switch ($action) {
        case 'stats':
            $result = getStats($pdo);
            break;
            
        case 'logs':
            $result = getLogs($pdo);
            break;
            
        case 'sessions':
            $result = getSessions($pdo);
            break;
            
        case 'export':
            $result = exportLogs($pdo);
            break;
            
        default:
            throw new Exception('Invalid action');
    }
    
    echo json_encode($result);
    
} catch (Exception $e) {
    http_response_code(500);
    echo json_encode([
        'success' => false,
        'error' => $e->getMessage()
    ]);
}

function getStats($pdo) {
    $stats = [];
    
    // Total de logs
    $stmt = $pdo->query('SELECT COUNT(*) FROM debug_logs');
    $stats['total_logs'] = $stmt->fetchColumn();
    
    // Total de sessões únicas
    $stmt = $pdo->query('SELECT COUNT(DISTINCT session_id) FROM debug_logs');
    $stats['total_sessions'] = $stmt->fetchColumn();
    
    // Logs de hoje
    $stmt = $pdo->query('SELECT COUNT(*) FROM debug_logs WHERE DATE(timestamp) = CURDATE()');
    $stats['today_logs'] = $stmt->fetchColumn();
    
    // Contagem por nível
    $stmt = $pdo->query('SELECT level, COUNT(*) as count FROM debug_logs GROUP BY level');
    $levelStats = [];
    while ($row = $stmt->fetch()) {
        $levelStats[$row['level']] = $row['count'];
    }
    $stats['level_stats'] = $levelStats;
    
    // Logs por hora (últimas 24h)
    $stmt = $pdo->query('
        SELECT HOUR(timestamp) as hour, COUNT(*) as count 
        FROM debug_logs 
        WHERE timestamp > DATE_SUB(NOW(), INTERVAL 24 HOUR)
        GROUP BY HOUR(timestamp)
        ORDER BY hour
    ');
    $hourlyStats = [];
    while ($row = $stmt->fetch()) {
        $hourlyStats[$row['hour']] = $row['count'];
    }
    $stats['hourly_stats'] = $hourlyStats;
    
    // URLs mais frequentes
    $stmt = $pdo->query('
        SELECT url, COUNT(*) as count 
        FROM debug_logs 
        WHERE url IS NOT NULL AND url != "unknown"
        GROUP BY url 
        ORDER BY count DESC 
        LIMIT 10
    ');
    $urlStats = [];
    while ($row = $stmt->fetch()) {
        $urlStats[] = ['url' => $row['url'], 'count' => $row['count']];
    }
    $stats['top_urls'] = $urlStats;
    
    return [
        'success' => true,
        'stats' => $stats,
        'timestamp' => date('Y-m-d H:i:s')
    ];
}

function getLogs($pdo) {
    $page = (int) ($_GET['page'] ?? 1);
    $limit = (int) ($_GET['limit'] ?? 50);
    $offset = ($page - 1) * $limit;
    
    // Construir query com filtros
    $where = [];
    $params = [];
    
    if (!empty($_GET['level'])) {
        $where[] = 'level = ?';
        $params[] = $_GET['level'];
    }
    
    if (!empty($_GET['session_id'])) {
        $where[] = 'session_id LIKE ?';
        $params[] = '%' . $_GET['session_id'] . '%';
    }
    
    if (!empty($_GET['url'])) {
        $where[] = 'url LIKE ?';
        $params[] = '%' . $_GET['url'] . '%';
    }
    
    if (!empty($_GET['date_from'])) {
        $where[] = 'timestamp >= ?';
        $params[] = $_GET['date_from'];
    }
    
    if (!empty($_GET['date_to'])) {
        $where[] = 'timestamp <= ?';
        $params[] = $_GET['date_to'];
    }
    
    $whereClause = $where ? 'WHERE ' . implode(' AND ', $where) : '';
    
    // Query principal
    $sql = "
        SELECT log_id, session_id, timestamp, level, message, data, url, ip_address
        FROM debug_logs 
        {$whereClause}
        ORDER BY timestamp DESC 
        LIMIT {$limit} OFFSET {$offset}
    ";
    
    $stmt = $pdo->prepare($sql);
    $stmt->execute($params);
    $logs = $stmt->fetchAll();
    
    // Contar total para paginação
    $countSql = "SELECT COUNT(*) FROM debug_logs {$whereClause}";
    $countStmt = $pdo->prepare($countSql);
    $countStmt->execute($params);
    $total = $countStmt->fetchColumn();
    
    return [
        'success' => true,
        'logs' => $logs,
        'pagination' => [
            'page' => $page,
            'limit' => $limit,
            'total' => $total,
            'pages' => ceil($total / $limit)
        ]
    ];
}

function getSessions($pdo) {
    $sessionId = $_GET['session_id'] ?? '';
    
    if (empty($sessionId)) {
        throw new Exception('Session ID is required');
    }
    
    $stmt = $pdo->prepare('
        SELECT log_id, timestamp, level, message, data, url
        FROM debug_logs 
        WHERE session_id = ?
        ORDER BY timestamp ASC
    ');
    $stmt->execute([$sessionId]);
    $logs = $stmt->fetchAll();
    
    return [
        'success' => true,
        'session_id' => $sessionId,
        'logs' => $logs,
        'count' => count($logs)
    ];
}

function exportLogs($pdo) {
    $format = $_GET['format'] ?? 'json';
    
    // Construir query com filtros (mesmo do getLogs)
    $where = [];
    $params = [];
    
    if (!empty($_GET['level'])) {
        $where[] = 'level = ?';
        $params[] = $_GET['level'];
    }
    
    if (!empty($_GET['session_id'])) {
        $where[] = 'session_id LIKE ?';
        $params[] = '%' . $_GET['session_id'] . '%';
    }
    
    if (!empty($_GET['url'])) {
        $where[] = 'url LIKE ?';
        $params[] = '%' . $_GET['url'] . '%';
    }
    
    if (!empty($_GET['date_from'])) {
        $where[] = 'timestamp >= ?';
        $params[] = $_GET['date_from'];
    }
    
    if (!empty($_GET['date_to'])) {
        $where[] = 'timestamp <= ?';
        $params[] = $_GET['date_to'];
    }
    
    $whereClause = $where ? 'WHERE ' . implode(' AND ', $where) : '';
    
    $sql = "
        SELECT log_id, session_id, timestamp, level, message, data, url, ip_address, user_agent
        FROM debug_logs 
        {$whereClause}
        ORDER BY timestamp DESC
    ";
    
    $stmt = $pdo->prepare($sql);
    $stmt->execute($params);
    $logs = $stmt->fetchAll();
    
    if ($format === 'csv') {
        header('Content-Type: text/csv');
        header('Content-Disposition: attachment; filename="rpa_logs_' . date('Y-m-d_H-i-s') . '.csv"');
        
        $output = fopen('php://output', 'w');
        fputcsv($output, ['Log ID', 'Session ID', 'Timestamp', 'Level', 'Message', 'Data', 'URL', 'IP Address', 'User Agent']);
        
        foreach ($logs as $log) {
            fputcsv($output, [
                $log['log_id'],
                $log['session_id'],
                $log['timestamp'],
                $log['level'],
                $log['message'],
                $log['data'],
                $log['url'],
                $log['ip_address'],
                $log['user_agent']
            ]);
        }
        
        fclose($output);
        exit;
    }
    
    // JSON export
    header('Content-Type: application/json');
    header('Content-Disposition: attachment; filename="rpa_logs_' . date('Y-m-d_H-i-s') . '.json"');
    
    echo json_encode([
        'success' => true,
        'export_info' => [
            'timestamp' => date('Y-m-d H:i:s'),
            'total_logs' => count($logs),
            'filters_applied' => $_GET
        ],
        'logs' => $logs
    ], JSON_PRETTY_PRINT);
}
