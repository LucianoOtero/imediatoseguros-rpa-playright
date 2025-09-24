<?php
/**
 * TESTE DE MONITORAMENTO SIMPLES
 * Verifica se o arquivo de progresso está sendo atualizado
 */

echo "TESTE DE MONITORAMENTO SIMPLES\n";
echo "==============================\n\n";

// Limpar arquivo anterior
if (file_exists("temp/progress_status.json")) {
    unlink("temp/progress_status.json");
    echo "Arquivo de progresso anterior removido\n";
}

echo "Executando RPA e monitorando arquivo...\n";
echo "Inicio: " . date("H:i:s") . "\n\n";

// Executar RPA em background
$comando = "python executar_rpa_imediato_playwright.py --config parametros.json";
if (strtoupper(substr(PHP_OS, 0, 3)) === "WIN") {
    $processo = popen("start /B $comando", "r");
} else {
    $processo = popen("$comando &", "r");
}

if ($processo) {
    pclose($processo);
    echo "RPA iniciado em background\n\n";
}

// Monitorar arquivo por 2 minutos
$start_time = time();
$ultima_etapa = 0;

while ((time() - $start_time) < 120) { // 2 minutos
    if (file_exists("temp/progress_status.json")) {
        $conteudo = file_get_contents("temp/progress_status.json");
        if ($conteudo) {
            $progresso = json_decode($conteudo, true);
            if ($progresso) {
                $etapa_atual = $progresso["etapa_atual"] ?? 0;
                $status = $progresso["status"] ?? "N/A";
                $percentual = round($progresso["percentual"] ?? 0, 1);
                $tempo_decorrido = round($progresso["tempo_decorrido"] ?? 0, 1);
                
                if ($etapa_atual > $ultima_etapa) {
                    echo "ETAPA $etapa_atual: $status\n";
                    echo "   Progresso: $percentual%\n";
                    echo "   Tempo: {$tempo_decorrido}s\n";
                    echo "   " . date("H:i:s") . "\n\n";
                    
                    $ultima_etapa = $etapa_atual;
                    
                    if ($etapa_atual >= 15) {
                        echo "EXECUCAO CONCLUIDA!\n";
                        break;
                    }
                }
            }
        }
    } else {
        echo "Aguardando arquivo de progresso... (" . date("H:i:s") . ")\n";
    }
    
    sleep(3); // Verificar a cada 3 segundos
}

echo "\nTESTE CONCLUIDO!\n";
echo "Fim: " . date("H:i:s") . "\n";
?>
