<?php
/**
 * STATUS BÁSICO - RPA
 * Página de status básica para monitoramento
 */

// Headers básicos
header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-cache, must-revalidate');

// Status básico
$status = [
    'timestamp' => date('Y-m-d H:i:s'),
    'sessions_today' => 0,
    'last_session' => 'N/A',
    'system_status' => 'OK'
];

// Contar sessões do dia
$log_file = 'logs/rpa_basic.log';
if (file_exists($log_file)) {
    $lines = file($log_file, FILE_IGNORE_NEW_LINES);
    $today = date('Y-m-d');
    
    foreach ($lines as $line) {
        if (strpos($line, $today) !== false) {
            $status['sessions_today']++;
        }
    }
    
    if (!empty($lines)) {
        $last_line = end($lines);
        if (preg_match('/Session: (\w+)/', $last_line, $matches)) {
            $status['last_session'] = $matches[1];
        }
    }
} else {
    $status['system_status'] = 'WARNING - Log file not found';
}

// Verificar se há arquivos de progresso recentes
$progress_files = glob("rpa_data/progress_*.json");
if (empty($progress_files)) {
    $status['system_status'] = 'WARNING - No progress files found';
} else {
    $latest_file = max($progress_files);
    $file_age = time() - filemtime($latest_file);
    
    // Se o arquivo mais recente tem mais de 10 minutos, considerar sistema inativo
    if ($file_age > 600) {
        $status['system_status'] = 'INACTIVE - No recent activity';
    }
}

// Adicionar informações do sistema
$status['server_time'] = date('Y-m-d H:i:s');
$status['timezone'] = date_default_timezone_get();
$status['progress_files_count'] = count($progress_files);
$status['log_file_exists'] = file_exists($log_file);

echo json_encode($status, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
?>














