<?php
/**
 * EXECUTAR RPA - API PHP
 * Executa o RPA modular e retorna status
 */

// Headers básicos de cache (otimização conservadora)
header('Cache-Control: no-cache, must-revalidate');
header('Expires: Mon, 26 Jul 1997 05:00:00 GMT');
header('Content-Type: application/json; charset=utf-8');

// Configurações
$rpa_script = "executar_rpa_modular_telas_1_a_5.py";
$session_id = $_POST['session'] ?? 'teste_php_' . date('Ymd_His');
$action = $_POST['action'] ?? 'start';

try {
    switch ($action) {
        case 'start':
            $result = startRPA($session_id);
            break;
        case 'status':
            $result = getStatus($session_id);
            break;
        default:
            $result = ['success' => false, 'error' => 'Ação não reconhecida'];
    }
    
    echo json_encode($result, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
    
} catch (Exception $e) {
    echo json_encode([
        'success' => false,
        'error' => $e->getMessage()
    ], JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
}

function startRPA($session_id) {
    global $rpa_script;
    
    // Verificar se o arquivo existe
    if (!file_exists($rpa_script)) {
        return [
            'success' => false,
            'error' => 'Arquivo RPA não encontrado: ' . $rpa_script
        ];
    }
    
    // Comando para executar o RPA
    $command = "xvfb-run -a python $rpa_script --progress-tracker json --session $session_id --modo-silencioso 2>&1";
    
    // Executar em background
    $pid = shell_exec("nohup $command > /dev/null 2>&1 & echo $!");
    
    if ($pid) {
        // Log básico (otimização conservadora)
        $log_entry = date('Y-m-d H:i:s') . " | RPA iniciado | Session: " . $session_id . " | PID: " . trim($pid) . "\n";
        file_put_contents('logs/rpa_basic.log', $log_entry, FILE_APPEND | LOCK_EX);
        
        return [
            'success' => true,
            'message' => 'RPA iniciado com sucesso',
            'session_id' => $session_id,
            'pid' => trim($pid)
        ];
    } else {
        // Log de erro
        $log_entry = date('Y-m-d H:i:s') . " | ERRO: Falha ao iniciar RPA | Session: " . $session_id . "\n";
        file_put_contents('logs/rpa_basic.log', $log_entry, FILE_APPEND | LOCK_EX);
        
        return [
            'success' => false,
            'error' => 'Falha ao iniciar o RPA'
        ];
    }
}

function getStatus($session_id) {
    // Verificar se há arquivos de progresso
    $progress_files = glob("temp/progress_*.json");
    
    if (empty($progress_files)) {
        return [
            'success' => false,
            'error' => 'Nenhum arquivo de progresso encontrado'
        ];
    }
    
    // Pegar o arquivo mais recente
    $latest_file = max($progress_files);
    $content = file_get_contents($latest_file);
    $data = json_decode($content, true);
    
    if (!$data) {
        return [
            'success' => false,
            'error' => 'Erro ao decodificar dados de progresso'
        ];
    }
    
    return [
        'success' => true,
        'data' => $data,
        'file' => basename($latest_file),
        'timestamp' => date('Y-m-d H:i:s')
    ];
}
?>
