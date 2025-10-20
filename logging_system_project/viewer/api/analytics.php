<?php
/**
 * viewer/api/analytics.php - API para Análise de Logs
 * Sistema de Logging PHP - RPA Imediato Seguros
 */

// Configurar headers
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type, X-Requested-With');

// Responder a requisições OPTIONS
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit(0);
}

// Incluir dependências
require_once __DIR__ . '/../../config/database.php';
require_once __DIR__ . '/../../config/security.php';
require_once __DIR__ . '/../../utils/helpers.php';

try {
    $action = $_GET['action'] ?? '';
    
    switch ($action) {
        case 'stats':
            handleStatsRequest();
            break;
            
        case 'logs':
            handleLogsRequest();
            break;
            
        case 'sessions':
            handleSessionsRequest();
            break;
            
        case 'export':
            handleExportRequest();
            break;
            
        case 'analytics':
            handleAnalyticsRequest();
            break;
            
        default:
            http_response_code(400);
            echo json_encode(['error' => 'Invalid action']);
            break;
    }
    
} catch (Exception $e) {
    http_response_code(500);
    echo json_encode(['error' => 'Internal server error', 'message' => $e->getMessage()]);
}

/**
 * Manipula requisições de estatísticas
 */
function handleStatsRequest() {
    $stats = getDatabaseStats();
    
    if (isset($stats['error'])) {
        http_response_code(500);
        echo json_encode(['error' => $stats['error']]);
        return;
    }
    
    // Calcular estatísticas adicionais
    $stats['error_count'] = 0;
    $stats['warning_count'] = 0;
    
    foreach ($stats['logs_by_level'] as $level) {
        if ($level['level'] === 'ERROR') {
            $stats['error_count'] = $level['count'];
        } elseif ($level['level'] === 'WARNING') {
            $stats['warning_count'] = $level['count'];
        }
    }
    
    echo json_encode([
        'success' => true,
        'stats' => $stats
    ]);
}

/**
 * Manipula requisições de logs
 */
function handleLogsRequest() {
    $filters = getLogFilters();
    $page = intval($_GET['page'] ?? 1);
    $limit = intval($_GET['limit'] ?? 20);
    $offset = ($page - 1) * $limit;
    
    try {
        $pdo = getDatabaseConnection();
        
        // Construir query base
        $whereConditions = [];
        $params = [];
        
        if (!empty($filters['level'])) {
            $whereConditions[] = 'level = ?';
            $params[] = $filters['level'];
        }
        
        if (!empty($filters['session_id'])) {
            $whereConditions[] = 'session_id LIKE ?';
            $params[] = '%' . $filters['session_id'] . '%';
        }
        
        if (!empty($filters['url'])) {
            $whereConditions[] = 'url LIKE ?';
            $params[] = '%' . $filters['url'] . '%';
        }
        
        if (!empty($filters['date_from'])) {
            $whereConditions[] = 'timestamp >= ?';
            $params[] = $filters['date_from'];
        }
        
        if (!empty($filters['date_to'])) {
            $whereConditions[] = 'timestamp <= ?';
            $params[] = $filters['date_to'];
        }
        
        if (!empty($filters['search'])) {
            $whereConditions[] = 'message LIKE ?';
            $params[] = '%' . $filters['search'] . '%';
        }
        
        $whereClause = empty($whereConditions) ? '' : 'WHERE ' . implode(' AND ', $whereConditions);
        
        // Contar total
        $countQuery = "SELECT COUNT(*) as total FROM debug_logs $whereClause";
        $countStmt = $pdo->prepare($countQuery);
        $countStmt->execute($params);
        $total = $countStmt->fetch()['total'];
        
        // Buscar logs
        $query = "
            SELECT log_id, session_id, timestamp, level, message, data, url, user_agent, ip_address
            FROM debug_logs 
            $whereClause
            ORDER BY timestamp DESC 
            LIMIT ? OFFSET ?
        ";
        
        $params[] = $limit;
        $params[] = $offset;
        
        $stmt = $pdo->prepare($query);
        $stmt->execute($params);
        $logs = $stmt->fetchAll();
        
        // Calcular paginação
        $totalPages = ceil($total / $limit);
        
        echo json_encode([
            'success' => true,
            'logs' => $logs,
            'pagination' => [
                'current_page' => $page,
                'per_page' => $limit,
                'total' => $total,
                'total_pages' => $totalPages,
                'has_next' => $page < $totalPages,
                'has_prev' => $page > 1
            ]
        ]);
        
    } catch (Exception $e) {
        http_response_code(500);
        echo json_encode(['error' => $e->getMessage()]);
    }
}

/**
 * Manipula requisições de sessões
 */
function handleSessionsRequest() {
    $sessionId = $_GET['session_id'] ?? '';
    
    if (empty($sessionId)) {
        http_response_code(400);
        echo json_encode(['error' => 'Session ID required']);
        return;
    }
    
    try {
        $pdo = getDatabaseConnection();
        
        // Buscar logs da sessão
        $stmt = $pdo->prepare("
            SELECT log_id, timestamp, level, message, data, url
            FROM debug_logs 
            WHERE session_id = ? 
            ORDER BY timestamp ASC
        ");
        $stmt->execute([$sessionId]);
        $logs = $stmt->fetchAll();
        
        // Buscar informações da sessão
        $stmt = $pdo->prepare("
            SELECT * FROM sessions WHERE session_id = ?
        ");
        $stmt->execute([$sessionId]);
        $session = $stmt->fetch();
        
        echo json_encode([
            'success' => true,
            'session' => $session,
            'logs' => $logs
        ]);
        
    } catch (Exception $e) {
        http_response_code(500);
        echo json_encode(['error' => $e->getMessage()]);
    }
}

/**
 * Manipula requisições de exportação
 */
function handleExportRequest() {
    $format = $_GET['format'] ?? 'csv';
    $filters = getLogFilters();
    
    try {
        $pdo = getDatabaseConnection();
        
        // Construir query
        $whereConditions = [];
        $params = [];
        
        if (!empty($filters['level'])) {
            $whereConditions[] = 'level = ?';
            $params[] = $filters['level'];
        }
        
        if (!empty($filters['session_id'])) {
            $whereConditions[] = 'session_id LIKE ?';
            $params[] = '%' . $filters['session_id'] . '%';
        }
        
        if (!empty($filters['date_from'])) {
            $whereConditions[] = 'timestamp >= ?';
            $params[] = $filters['date_from'];
        }
        
        if (!empty($filters['date_to'])) {
            $whereConditions[] = 'timestamp <= ?';
            $params[] = $filters['date_to'];
        }
        
        $whereClause = empty($whereConditions) ? '' : 'WHERE ' . implode(' AND ', $whereConditions);
        
        $query = "
            SELECT timestamp, level, message, session_id, url, ip_address, data
            FROM debug_logs 
            $whereClause
            ORDER BY timestamp DESC
        ";
        
        $stmt = $pdo->prepare($query);
        $stmt->execute($params);
        $logs = $stmt->fetchAll();
        
        switch ($format) {
            case 'csv':
                exportAsCsv($logs);
                break;
                
            case 'json':
                exportAsJson($logs);
                break;
                
            default:
                http_response_code(400);
                echo json_encode(['error' => 'Unsupported format']);
                break;
        }
        
    } catch (Exception $e) {
        http_response_code(500);
        echo json_encode(['error' => $e->getMessage()]);
    }
}

/**
 * Manipula requisições de análise
 */
function handleAnalyticsRequest() {
    $type = $_GET['type'] ?? 'overview';
    
    try {
        $pdo = getDatabaseConnection();
        
        switch ($type) {
            case 'overview':
                $analytics = getOverviewAnalytics($pdo);
                break;
                
            case 'performance':
                $analytics = getPerformanceAnalytics($pdo);
                break;
                
            case 'errors':
                $analytics = getErrorAnalytics($pdo);
                break;
                
            default:
                http_response_code(400);
                echo json_encode(['error' => 'Invalid analytics type']);
                return;
        }
        
        echo json_encode([
            'success' => true,
            'analytics' => $analytics
        ]);
        
    } catch (Exception $e) {
        http_response_code(500);
        echo json_encode(['error' => $e->getMessage()]);
    }
}

/**
 * Obtém filtros de log
 */
function getLogFilters() {
    return [
        'level' => $_GET['level'] ?? '',
        'session_id' => $_GET['session_id'] ?? '',
        'url' => $_GET['url'] ?? '',
        'date_from' => $_GET['date_from'] ?? '',
        'date_to' => $_GET['date_to'] ?? '',
        'search' => $_GET['search'] ?? ''
    ];
}

/**
 * Exporta dados como CSV
 */
function exportAsCsv($logs) {
    header('Content-Type: text/csv');
    header('Content-Disposition: attachment; filename="logs_' . date('Y-m-d') . '.csv"');
    
    $output = fopen('php://output', 'w');
    
    // Cabeçalho
    fputcsv($output, ['Timestamp', 'Level', 'Message', 'Session ID', 'URL', 'IP Address', 'Data']);
    
    // Dados
    foreach ($logs as $log) {
        fputcsv($output, [
            $log['timestamp'],
            $log['level'],
            $log['message'],
            $log['session_id'],
            $log['url'],
            $log['ip_address'],
            $log['data']
        ]);
    }
    
    fclose($output);
}

/**
 * Exporta dados como JSON
 */
function exportAsJson($logs) {
    header('Content-Type: application/json');
    header('Content-Disposition: attachment; filename="logs_' . date('Y-m-d') . '.json"');
    
    echo json_encode($logs, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT);
}

/**
 * Obtém análise geral
 */
function getOverviewAnalytics($pdo) {
    $analytics = [];
    
    // Logs por dia (últimos 7 dias)
    $stmt = $pdo->query("
        SELECT DATE(timestamp) as date, COUNT(*) as count
        FROM debug_logs 
        WHERE timestamp >= DATE_SUB(NOW(), INTERVAL 7 DAY)
        GROUP BY DATE(timestamp)
        ORDER BY date DESC
    ");
    $analytics['logs_by_day'] = $stmt->fetchAll();
    
    // Logs por nível
    $stmt = $pdo->query("
        SELECT level, COUNT(*) as count
        FROM debug_logs 
        WHERE timestamp >= DATE_SUB(NOW(), INTERVAL 7 DAY)
        GROUP BY level
        ORDER BY count DESC
    ");
    $analytics['logs_by_level'] = $stmt->fetchAll();
    
    // URLs mais frequentes
    $stmt = $pdo->query("
        SELECT url, COUNT(*) as count
        FROM debug_logs 
        WHERE timestamp >= DATE_SUB(NOW(), INTERVAL 7 DAY)
        AND url IS NOT NULL
        GROUP BY url
        ORDER BY count DESC
        LIMIT 10
    ");
    $analytics['top_urls'] = $stmt->fetchAll();
    
    return $analytics;
}

/**
 * Obtém análise de performance
 */
function getPerformanceAnalytics($pdo) {
    $analytics = [];
    
    // Tempo médio entre logs por sessão
    $stmt = $pdo->query("
        SELECT 
            session_id,
            COUNT(*) as log_count,
            TIMESTAMPDIFF(SECOND, MIN(timestamp), MAX(timestamp)) as duration_seconds
        FROM debug_logs 
        WHERE timestamp >= DATE_SUB(NOW(), INTERVAL 24 HOUR)
        GROUP BY session_id
        HAVING log_count > 1
        ORDER BY duration_seconds DESC
        LIMIT 20
    ");
    $analytics['session_performance'] = $stmt->fetchAll();
    
    return $analytics;
}

/**
 * Obtém análise de erros
 */
function getErrorAnalytics($pdo) {
    $analytics = [];
    
    // Erros mais frequentes
    $stmt = $pdo->query("
        SELECT message, COUNT(*) as count
        FROM debug_logs 
        WHERE level = 'ERROR'
        AND timestamp >= DATE_SUB(NOW(), INTERVAL 7 DAY)
        GROUP BY message
        ORDER BY count DESC
        LIMIT 10
    ");
    $analytics['top_errors'] = $stmt->fetchAll();
    
    // Erros por sessão
    $stmt = $pdo->query("
        SELECT session_id, COUNT(*) as error_count
        FROM debug_logs 
        WHERE level = 'ERROR'
        AND timestamp >= DATE_SUB(NOW(), INTERVAL 7 DAY)
        GROUP BY session_id
        ORDER BY error_count DESC
        LIMIT 20
    ");
    $analytics['errors_by_session'] = $stmt->fetchAll();
    
    return $analytics;
}
?>
