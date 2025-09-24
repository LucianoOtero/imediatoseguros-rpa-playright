<?php
/**
 * TESTE SSE SIMPLES
 * Testa apenas a conexão Server-Sent Events
 */

// Desabilitar timeout
set_time_limit(0);
ini_set('max_execution_time', 0);

header('Content-Type: text/event-stream');
header('Cache-Control: no-cache');
header('Connection: keep-alive');
header('Access-Control-Allow-Origin: *');

echo "data: " . json_encode(['status' => 'test', 'message' => 'Conexão SSE funcionando!']) . "\n\n";
flush();

// Simular progresso
for ($i = 1; $i <= 5; $i++) {
    sleep(1);
    echo "data: " . json_encode([
        'status' => 'progress',
        'etapa_atual' => $i,
        'total_etapas' => 5,
        'percentual' => ($i / 5) * 100,
        'message' => "Etapa $i de 5"
    ]) . "\n\n";
    flush();
}

echo "data: " . json_encode(['status' => 'completed', 'message' => 'Teste concluído!']) . "\n\n";
flush();

exit();
?>
