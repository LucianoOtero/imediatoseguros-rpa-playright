<?php
header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: http://localhost:3000');
header('Access-Control-Allow-Methods: GET, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type, X-Requested-With');
header('Access-Control-Allow-Credentials: true');

// Tratar preflight OPTIONS
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit();
}

// Verificar método
if ($_SERVER['REQUEST_METHOD'] !== 'GET') {
    http_response_code(405);
    echo json_encode(['success' => false, 'message' => 'Método não permitido']);
    exit();
}

// Obter session ID
$session_id = $_GET['session'] ?? '';

if (empty($session_id)) {
    http_response_code(400);
    echo json_encode(['success' => false, 'message' => 'Session ID obrigatório']);
    exit();
}

// Procurar arquivo de progresso
$progress_file = "../rpa_data/progress_{$session_id}.json";

if (!file_exists($progress_file)) {
    echo json_encode([
        'success' => true,
        'progress' => 0,
        'current_step' => [
            'icon' => '🚗',
            'title' => 'Aguardando início...',
            'description' => 'Preparando processamento',
            'progress' => 0,
            'estimated_time' => '--'
        ],
        'estimates' => null,
        'timeline' => []
    ]);
    exit();
}

// Ler arquivo de progresso
$progress_data = json_decode(file_get_contents($progress_file), true);

if (!$progress_data) {
    echo json_encode([
        'success' => false,
        'message' => 'Erro ao ler arquivo de progresso'
    ]);
    exit();
}

// Preparar resposta
$response = [
    'success' => true,
    'progress' => $progress_data['progresso_geral'] ?? 0,
    'current_step' => [
        'icon' => $progress_data['etapa_atual']['icon'] ?? '🚗',
        'title' => $progress_data['etapa_atual']['titulo'] ?? 'Processando...',
        'description' => $progress_data['etapa_atual']['descricao'] ?? 'Aguarde...',
        'progress' => $progress_data['etapa_atual']['progresso'] ?? 0,
        'estimated_time' => $progress_data['etapa_atual']['tempo_estimado'] ?? '--'
    ],
    'estimates' => $progress_data['estimativas'] ?? null,
    'timeline' => $progress_data['timeline'] ?? []
];

echo json_encode($response);
?>
