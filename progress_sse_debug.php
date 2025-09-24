<?php
/**
 * DEBUG SSE - VERSÃO PARA INVESTIGAR PROBLEMAS
 */

// Configurações para evitar timeout
ini_set('max_execution_time', 0);
ini_set('default_socket_timeout', 0);
set_time_limit(0);

header('Content-Type: text/event-stream');
header('Cache-Control: no-cache');
header('Connection: keep-alive');
header('Access-Control-Allow-Origin: *');

// Obter session_id
$session_id = $_GET['session_id'] ?? uniqid();
$progress_file = "temp/progress_{$session_id}.json";

// Criar diretório temp se não existir
if (!is_dir('temp')) {
    mkdir('temp', 0755, true);
}

// Log de debug
error_log("DEBUG: SSE iniciado para session_id: $session_id");

// Enviar mensagem inicial
echo "data: " . json_encode([
    'status' => 'starting',
    'session_id' => $session_id,
    'message' => 'Iniciando RPA...',
    'debug' => 'SSE conectado'
]) . "\n\n";
flush();

// Comando para executar RPA
$comando = "python executar_rpa_imediato_playwright.py --config parametros.json --session {$session_id}";

// Executar em background (Windows)
if (strtoupper(substr(PHP_OS, 0, 3)) === 'WIN') {
    $comando = "start /B $comando";
} else {
    $comando .= " > /dev/null 2>&1 &";
}

error_log("DEBUG: Executando comando: $comando");
exec($comando);

echo "data: " . json_encode([
    'status' => 'started',
    'session_id' => $session_id,
    'message' => 'RPA iniciado - Chrome deve abrir em breve',
    'debug' => 'Comando executado'
]) . "\n\n";
flush();

// Aguardar um pouco para o RPA inicializar
sleep(3);

// Loop para monitorar progresso
$last_progress = [];
$timeout_seconds = 300; // 5 minutos
$start_time = time();
$loop_count = 0;

while (true) {
    $loop_count++;
    
    // Verificar timeout
    if (time() - $start_time > $timeout_seconds) {
        echo "data: " . json_encode([
            'status' => 'timeout',
            'message' => 'Timeout: RPA não respondeu a tempo',
            'debug' => "Loop count: $loop_count"
        ]) . "\n\n";
        flush();
        break;
    }

    // Verificar se arquivo existe
    if (file_exists($progress_file)) {
        $content = file_get_contents($progress_file);
        $progresso = json_decode($content, true);

        if ($progresso && $progresso !== $last_progress) {
            // Adicionar session_id e debug
            $progresso['session_id'] = $session_id;
            $progresso['debug'] = "Loop: $loop_count, File exists: true";
            
            echo "data: " . json_encode($progresso) . "\n\n";
            flush();
            $last_progress = $progresso;

            // Se concluído, sair
            if (isset($progresso['etapa_atual']) && $progresso['etapa_atual'] >= $progresso['total_etapas']) {
                echo "data: " . json_encode([
                    'status' => 'completed',
                    'message' => 'RPA concluído com sucesso!',
                    'debug' => "Final loop: $loop_count"
                ]) . "\n\n";
                flush();
                break;
            }
        } else {
            // Enviar heartbeat para manter conexão
            if ($loop_count % 10 == 0) {
                echo "data: " . json_encode([
                    'status' => 'heartbeat',
                    'message' => 'Aguardando progresso...',
                    'debug' => "Loop: $loop_count, File exists: " . (file_exists($progress_file) ? 'true' : 'false')
                ]) . "\n\n";
                flush();
            }
        }
    } else {
        // Arquivo não existe ainda
        if ($loop_count % 5 == 0) {
            echo "data: " . json_encode([
                'status' => 'waiting',
                'message' => 'Aguardando arquivo de progresso...',
                'debug' => "Loop: $loop_count, File exists: false"
            ]) . "\n\n";
            flush();
        }
    }

    // Pausa pequena
    usleep(500000); // 0.5 segundos
}

// Limpar arquivo
if (file_exists($progress_file)) {
    unlink($progress_file);
}

error_log("DEBUG: SSE finalizado para session_id: $session_id");
exit();
?>
