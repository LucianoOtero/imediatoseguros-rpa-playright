<?php
/**
 * GET PROGRESS - API PHP CORRIGIDA
 * Obtém o progresso atual do RPA para uma sessão específica
 */

// Headers CORS
header('Access-Control-Allow-Origin: http://localhost:3000');
header('Access-Control-Allow-Methods: GET, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type, X-Requested-With');
header('Access-Control-Allow-Credentials: true');

// Tratar preflight OPTIONS
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit();
}

// Headers básicos de cache (otimização conservadora)
header('Cache-Control: no-cache, must-revalidate');
header('Expires: Mon, 26 Jul 1997 05:00:00 GMT');
header('Content-Type: application/json; charset=utf-8');

// Obter session ID
$session_id = $_GET['session'] ?? '';

if (empty($session_id)) {
    http_response_code(400);
    echo json_encode([
        'success' => false, 
        'message' => 'Session ID obrigatório',
        'timestamp' => date('Y-m-d H:i:s')
    ], JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
    exit();
}

try {
    // CORREÇÃO: Ler arquivo específico da sessão
    $progress_file = "/opt/imediatoseguros-rpa/rpa_data/progress_{$session_id}.json";
    
    if (!file_exists($progress_file)) {
        // Se o arquivo não existe, retorna um status inicial
        echo json_encode([
            'success' => true,
            'data' => [
                'etapa_atual' => 0,
                'total_etapas' => 5, // Para modular 1-5
                'percentual' => 0,
                'status' => 'waiting',
                'mensagem' => 'Aguardando início...',
                'timestamp_inicio' => date('Y-m-d\TH:i:s'),
                'timestamp_atualizacao' => date('Y-m-d\TH:i:s'),
                'dados_extra' => [],
                'erros' => [],
                'session_id' => $session_id
            ],
            'timestamp' => date('Y-m-d H:i:s')
        ], JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
        exit();
    }
    
    // Ler arquivo de progresso
    $content = file_get_contents($progress_file);
    $data = json_decode($content, true);
    
    if (!$data) {
        http_response_code(500);
        echo json_encode([
            'success' => false,
            'message' => 'Erro ao ler arquivo de progresso',
            'file' => basename($progress_file),
            'timestamp' => date('Y-m-d H:i:s')
        ], JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
        exit();
    }
    
    // Adicionar informações extras
    $data['file'] = basename($progress_file);
    $data['file_path'] = $progress_file;
    $data['file_size'] = filesize($progress_file);
    $data['file_modified'] = date('Y-m-d H:i:s', filemtime($progress_file));
    $data['timestamp'] = date('Y-m-d H:i:s');
    
    // Preparar resposta
    echo json_encode([
        'success' => true,
        'data' => $data
    ], JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
    
} catch (Exception $e) {
    http_response_code(500);
    echo json_encode([
        'success' => false,
        'message' => $e->getMessage(),
        'timestamp' => date('Y-m-d H:i:s')
    ], JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
}
?>
















