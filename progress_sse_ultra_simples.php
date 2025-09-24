<?php
/**
 * SSE ULTRA SIMPLES - VERSÃO QUE FUNCIONA
 */

// Configurações para evitar timeout
ini_set('max_execution_time', 0);
set_time_limit(0);

header('Content-Type: text/event-stream');
header('Cache-Control: no-cache');
header('Connection: keep-alive');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

// Obter session_id
$session_id = $_GET['session_id'] ?? uniqid();
$progress_file = "temp/progress_{$session_id}.json";

// Criar diretório temp se não existir
if (!is_dir('temp')) {
    mkdir('temp', 0755, true);
}

// Enviar mensagem inicial
echo "data: " . json_encode([
    'status' => 'starting',
    'session_id' => $session_id,
    'message' => 'Iniciando RPA...'
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

exec($comando);

echo "data: " . json_encode([
    'status' => 'started',
    'session_id' => $session_id,
    'message' => 'RPA iniciado - Chrome deve abrir em breve'
]) . "\n\n";
flush();

// Aguardar um pouco para o RPA inicializar
sleep(2);

// Loop para monitorar progresso
$last_progress = [];
$timeout_seconds = 300;
$start_time = time();
$last_etapa = 0;

while (true) {
    // Verificar timeout
    if (time() - $start_time > $timeout_seconds) {
        echo "data: " . json_encode([
            'status' => 'timeout',
            'message' => 'Timeout: RPA não respondeu a tempo'
        ]) . "\n\n";
        flush();
        break;
    }

    if (file_exists($progress_file)) {
        $content = file_get_contents($progress_file);
        $progresso = json_decode($content, true);

        if ($progresso) {
            $etapa_atual = $progresso['etapa_atual'] ?? 0;
            
            // Enviar se é uma nova etapa ou se mudou significativamente
            if ($etapa_atual > $last_etapa || $progresso !== $last_progress) {
                // Adicionar session_id
                $progresso['session_id'] = $session_id;
                echo "data: " . json_encode($progresso) . "\n\n";
                flush();
                $last_progress = $progresso;
                $last_etapa = $etapa_atual;

                // Se concluído, sair
                if ($etapa_atual >= $progresso['total_etapas']) {
                    break;
                }
            }
        }
    } else {
        // Enviar heartbeat se arquivo não existe ainda
        if ((time() - $start_time) % 5 == 0) {
            echo "data: " . json_encode([
                'status' => 'waiting',
                'message' => 'Aguardando arquivo de progresso...',
                'session_id' => $session_id
            ]) . "\n\n";
            flush();
        }
    }

    // Pausa menor para capturar mais etapas
    usleep(200000); // 0.2 segundos
}

// Limpar arquivo
if (file_exists($progress_file)) {
    unlink($progress_file);
}

exit();
?>
