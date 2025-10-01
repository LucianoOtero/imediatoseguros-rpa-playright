<?php
/**
 * GET PROGRESS - API PHP
 * Obtém o progresso atual do RPA
 */

// Headers básicos de cache (otimização conservadora)
header('Cache-Control: no-cache, must-revalidate');
header('Expires: Mon, 26 Jul 1997 05:00:00 GMT');
header('Content-Type: application/json; charset=utf-8');

$session_id = $_GET['session'] ?? '';

try {
    // Verificar se há arquivos de progresso
    $progress_files = glob("rpa_data/progress_*.json");
    
    if (empty($progress_files)) {
        echo json_encode([
            'success' => false,
            'error' => 'Nenhum arquivo de progresso encontrado',
            'timestamp' => date('Y-m-d H:i:s')
        ], JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
        exit;
    }
    
    // Pegar o arquivo mais recente
    $latest_file = max($progress_files);
    $content = file_get_contents($latest_file);
    $data = json_decode($content, true);
    
    if (!$data) {
        echo json_encode([
            'success' => false,
            'error' => 'Erro ao decodificar dados de progresso',
            'file' => basename($latest_file),
            'timestamp' => date('Y-m-d H:i:s')
        ], JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
        exit;
    }
    
    // Adicionar informações extras
    $data['file'] = basename($latest_file);
    $data['file_path'] = $latest_file;
    $data['file_size'] = filesize($latest_file);
    $data['file_modified'] = date('Y-m-d H:i:s', filemtime($latest_file));
    $data['timestamp'] = date('Y-m-d H:i:s');
    
    echo json_encode([
        'success' => true,
        'data' => $data
    ], JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
    
} catch (Exception $e) {
    echo json_encode([
        'success' => false,
        'error' => $e->getMessage(),
        'timestamp' => date('Y-m-d H:i:s')
    ], JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
}
?>
