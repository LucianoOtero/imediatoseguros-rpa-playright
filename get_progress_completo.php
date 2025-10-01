<?php
/**
 * GET PROGRESS - API PHP COMPLETA
 * Obtém o progresso atual do RPA com histórico, estimativas e resultados finais
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

// Obter parâmetros
$session_id = $_GET['session'] ?? '';
$mode = $_GET['mode'] ?? 'current'; // 'current', 'history', 'both'
$include_history = $_GET['include_history'] ?? 'true';
$history_limit = (int)($_GET['history_limit'] ?? 50);

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
    // Detectar arquivos disponíveis
    $history_file = "/opt/imediatoseguros-rpa/rpa_data/history_{$session_id}.json";
    $progress_file = "/opt/imediatoseguros-rpa/rpa_data/progress_{$session_id}.json";
    
    $use_history = file_exists($history_file);
    $use_progress = file_exists($progress_file) && !$use_history;
    
    if (!$use_history && !$use_progress) {
        // Se nenhum arquivo existe, retorna status inicial
        echo json_encode([
            'success' => true,
            'data' => [
                'etapa_atual' => 0,
                'total_etapas' => 5,
                'percentual' => 0,
                'status' => 'waiting',
                'mensagem' => 'Aguardando início...',
                'timestamp_inicio' => date('Y-m-d\TH:i:s'),
                'timestamp_atualizacao' => date('Y-m-d\TH:i:s'),
                'dados_extra' => [],
                'erros' => [],
                'session_id' => $session_id,
                'historico' => [],
                'timeline' => [],
                'estimativas' => [
                    'capturadas' => false,
                    'encontradas' => false,
                    'dados' => null,
                    'status' => 'not_found',
                    'mensagem' => 'Estimativas não encontradas'
                ],
                'resultados_finais' => [
                    'rpa_finalizado' => false,
                    'status_final' => 'waiting',
                    'timestamp_fim' => null,
                    'dados' => null,
                    'arquivo_resultado' => null
                ],
                'source' => 'none',
                'file_used' => 'none'
            ],
            'timestamp' => date('Y-m-d H:i:s')
        ], JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
        exit();
    }
    
    // Processar dados
    if ($use_history) {
        $data = processarHistorico($history_file, $session_id);
    } else {
        $data = processarProgress($progress_file, $session_id);
    }
    
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

// ========================================
// FUNÇÕES AUXILIARES
// ========================================

function processarHistorico($history_file, $session_id) {
    $content = file_get_contents($history_file);
    $history_data = json_decode($content, true);
    
    if (!$history_data) {
        throw new Exception('Erro ao ler arquivo de histórico');
    }
    
    $historico = $history_data['historico'] ?? [];
    
    // Processar histórico
    $processed = processarHistoricoArray($historico, $history_data);
    
    // Detectar estimativas
    $estimativas_info = detectarEstimativas($historico);
    
    // Detectar resultados finais
    $resultados_info = detectarResultadosFinais($historico);
    
    // Preparar dados de resposta
    $data = [
        'etapa_atual' => $processed['current_etapa'],
        'total_etapas' => $history_data['total_etapas'] ?? 5,
        'percentual' => ($processed['current_etapa'] / ($history_data['total_etapas'] ?? 5)) * 100,
        'status' => $processed['current_status'],
        'mensagem' => $processed['current_mensagem'],
        'timestamp_inicio' => $history_data['timestamp_inicio'] ?? date('Y-m-d\TH:i:s'),
        'timestamp_atualizacao' => $history_data['timestamp_fim'] ?? date('Y-m-d\TH:i:s'),
        'dados_extra' => $processed['dados_extra'],
        'erros' => $processed['erros'],
        'session_id' => $session_id,
        'historico' => array_slice($historico, -10), // Últimas 10 entradas
        'timeline' => array_slice($processed['timeline'], -10),
        'historico_count' => count($historico),
        'estimativas' => [
            'capturadas' => $estimativas_info['estimativas_capturadas'],
            'encontradas' => $estimativas_info['estimativas_encontradas'],
            'dados' => $estimativas_info['estimativas_capturadas'] 
                ? extrairDadosEstimativas($estimativas_info['estimativas_entry'])
                : null,
            'status' => $estimativas_info['estimativas_entry']['status'] ?? 'not_found',
            'mensagem' => $estimativas_info['estimativas_entry']['mensagem'] ?? 'Estimativas não encontradas'
        ],
        'resultados_finais' => [
            'rpa_finalizado' => $resultados_info['rpa_finalizado'],
            'status_final' => $resultados_info['status_final'],
            'timestamp_fim' => $resultados_info['timestamp_fim'],
            'dados' => $resultados_info['rpa_finalizado'] 
                ? processarPlanos(lerResultadosFinais($session_id))
                : null,
            'arquivo_resultado' => $resultados_info['rpa_finalizado'] 
                ? "result_{$session_id}.json"
                : null
        ],
        'source' => 'history',
        'file_used' => basename($history_file)
    ];
    
    return $data;
}

function processarProgress($progress_file, $session_id) {
    $content = file_get_contents($progress_file);
    $progress_data = json_decode($content, true);
    
    if (!$progress_data) {
        throw new Exception('Erro ao ler arquivo de progresso');
    }
    
    return [
        'etapa_atual' => $progress_data['etapa_atual'] ?? 0,
        'total_etapas' => $progress_data['total_etapas'] ?? 5,
        'percentual' => $progress_data['percentual'] ?? 0,
        'status' => $progress_data['status'] ?? 'waiting',
        'mensagem' => $progress_data['mensagem'] ?? 'Aguardando...',
        'timestamp_inicio' => $progress_data['timestamp_inicio'] ?? date('Y-m-d\TH:i:s'),
        'timestamp_atualizacao' => $progress_data['timestamp_atualizacao'] ?? date('Y-m-d\TH:i:s'),
        'dados_extra' => $progress_data['dados_extra'] ?? [],
        'erros' => $progress_data['erros'] ?? [],
        'session_id' => $session_id,
        'historico' => [],
        'timeline' => [],
        'historico_count' => 0,
        'estimativas' => [
            'capturadas' => false,
            'encontradas' => false,
            'dados' => null,
            'status' => 'not_found',
            'mensagem' => 'Histórico não disponível'
        ],
        'resultados_finais' => [
            'rpa_finalizado' => false,
            'status_final' => 'running',
            'timestamp_fim' => null,
            'dados' => null,
            'arquivo_resultado' => null
        ],
        'source' => 'progress',
        'file_used' => basename($progress_file)
    ];
}

function processarHistoricoArray($historico, $history_data) {
    $timeline = [];
    $current_status = 'waiting';
    $current_etapa = 0;
    $current_mensagem = 'Aguardando...';
    $dados_extra = [];
    $erros = [];
    
    foreach ($historico as $entry) {
        $timeline[] = [
            'etapa' => $entry['etapa'],
            'timestamp' => $entry['timestamp'],
            'status' => $entry['status'],
            'mensagem' => $entry['mensagem']
        ];
        
        // Atualizar estado atual
        if ($entry['status'] === 'completed' || $entry['status'] === 'success') {
            $current_status = $entry['status'];
            $current_etapa = is_numeric($entry['etapa']) ? $entry['etapa'] : $current_etapa;
            $current_mensagem = $entry['mensagem'];
        }
        
        // Coletar dados extras
        if ($entry['dados_extra']) {
            $dados_extra = array_merge($dados_extra, $entry['dados_extra']);
        }
        
        // Coletar erros
        if ($entry['erro']) {
            $erros[] = [
                'etapa' => $entry['etapa'],
                'erro' => $entry['erro'],
                'timestamp' => $entry['timestamp']
            ];
        }
    }
    
    return [
        'timeline' => $timeline,
        'current_status' => $current_status,
        'current_etapa' => $current_etapa,
        'current_mensagem' => $current_mensagem,
        'dados_extra' => $dados_extra,
        'erros' => $erros
    ];
}

function detectarEstimativas($historico) {
    $estimativas_idx = null;
    $estimativas_entry = null;
    $execucao_posterior = false;
    
    // Buscar entrada "estimativas"
    foreach ($historico as $index => $entry) {
        if ($entry['etapa'] === 'estimativas') {
            $estimativas_idx = $index;
            $estimativas_entry = $entry;
            break;
        }
    }
    
    // Verificar se há execução posterior
    if ($estimativas_idx !== null && count($historico) > $estimativas_idx + 1) {
        $execucao_posterior = true;
    }
    
    return [
        'estimativas_encontradas' => $estimativas_entry !== null,
        'estimativas_capturadas' => $execucao_posterior,
        'estimativas_entry' => $estimativas_entry,
        'estimativas_idx' => $estimativas_idx,
        'execucao_posterior' => $execucao_posterior
    ];
}

function extrairDadosEstimativas($estimativas_entry) {
    if (!$estimativas_entry || !isset($estimativas_entry['dados_extra'])) {
        return null;
    }
    
    $dados_extra = $estimativas_entry['dados_extra'];
    
    // Extrair coberturas detalhadas
    $coberturas = $dados_extra['coberturas_detalhadas'] ?? [];
    $resumo = $dados_extra['resumo'] ?? [];
    
    // Processar coberturas
    $coberturas_processadas = [];
    foreach ($coberturas as $cobertura) {
        $coberturas_processadas[] = [
            'nome' => $cobertura['nome_cobertura'] ?? 'N/A',
            'valores' => $cobertura['valores'] ?? [],
            'beneficios' => $cobertura['beneficios'] ?? [],
            'indice' => $cobertura['indice'] ?? 0
        ];
    }
    
    return [
        'coberturas' => $coberturas_processadas,
        'resumo' => $resumo,
        'timestamp' => $estimativas_entry['timestamp'],
        'status' => $estimativas_entry['status'],
        'mensagem' => $estimativas_entry['mensagem']
    ];
}

function detectarResultadosFinais($historico) {
    $final_entry = null;
    $rpa_finalizado = false;
    $status_final = 'running';
    
    // Buscar entrada "final"
    foreach ($historico as $entry) {
        if ($entry['etapa'] === 'final') {
            $final_entry = $entry;
            $status_final = $entry['status'];
            $rpa_finalizado = ($entry['status'] === 'success');
            break;
        }
    }
    
    return [
        'rpa_finalizado' => $rpa_finalizado,
        'status_final' => $status_final,
        'final_entry' => $final_entry,
        'timestamp_fim' => $final_entry['timestamp'] ?? null
    ];
}

function lerResultadosFinais($session_id) {
    $result_file = "/opt/imediatoseguros-rpa/rpa_data/result_{$session_id}.json";
    
    if (!file_exists($result_file)) {
        return null;
    }
    
    try {
        $content = file_get_contents($result_file);
        $data = json_decode($content, true);
        
        if (!$data) {
            return null;
        }
        
        return $data;
    } catch (Exception $e) {
        return null;
    }
}

function processarPlanos($dados_finais) {
    if (!$dados_finais || !isset($dados_finais['dados_finais'])) {
        return null;
    }
    
    $dados = $dados_finais['dados_finais'];
    $planos = [];
    
    // Processar plano recomendado
    if (isset($dados['plano_recomendado'])) {
        $planos['recomendado'] = processarPlano($dados['plano_recomendado'], 'recomendado');
    }
    
    // Processar plano alternativo
    if (isset($dados['plano_alternativo'])) {
        $planos['alternativo'] = processarPlano($dados['plano_alternativo'], 'alternativo');
    }
    
    return $planos;
}

function processarPlano($plano_data, $tipo) {
    return [
        'tipo' => $tipo,
        'nome' => $plano_data['plano'] ?? 'N/A',
        'valor' => $plano_data['valor'] ?? 'N/A',
        'forma_pagamento' => $plano_data['forma_pagamento'] ?? 'N/A',
        'parcelamento' => $plano_data['parcelamento'] ?? 'N/A',
        'valor_franquia' => $plano_data['valor_franquia'] ?? 'N/A',
        'valor_mercado' => $plano_data['valor_mercado'] ?? 'N/A',
        'coberturas' => [
            'assistencia' => $plano_data['assistencia'] ?? false,
            'vidros' => $plano_data['vidros'] ?? false,
            'carro_reserva' => $plano_data['carro_reserva'] ?? false
        ],
        'limites' => [
            'danos_materiais' => $plano_data['danos_materiais'] ?? 'N/A',
            'danos_corporais' => $plano_data['danos_corporais'] ?? 'N/A',
            'danos_morais' => $plano_data['danos_morais'] ?? 'N/A',
            'morte_invalidez' => $plano_data['morte_invalidez'] ?? 'N/A'
        ],
        'franquia' => [
            'tipo' => $plano_data['tipo_franquia'] ?? 'N/A'
        ]
    ];
}

?>


