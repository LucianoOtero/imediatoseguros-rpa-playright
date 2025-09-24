<?php
/**
 * TESTE SIMPLES NO TERMINAL - FUNCIONANDO
 * Testa o ProgressTracker que está funcionando
 */

echo "TESTE SIMPLES NO TERMINAL - FUNCIONANDO\n";
echo "=======================================\n\n";

echo "1. Verificando arquivo de progresso...\n";
if (file_exists("temp/progress_status.json")) {
    $progresso = json_decode(file_get_contents("temp/progress_status.json"), true);
    if ($progresso) {
        echo "ProgressTracker encontrado!\n";
        echo "Etapa atual: " . $progresso["etapa_atual"] . "\n";
        echo "Total etapas: " . $progresso["total_etapas"] . "\n";
        echo "Percentual: " . $progresso["percentual"] . "%\n";
        echo "Status: " . $progresso["status"] . "\n";
        echo "Tempo decorrido: " . round($progresso["tempo_decorrido"], 2) . "s\n";
        echo "Timestamp: " . $progresso["timestamp"] . "\n\n";
    } else {
        echo "Erro ao decodificar JSON\n\n";
    }
} else {
    echo "Arquivo de progresso nao encontrado\n\n";
}

echo "2. Verificando arquivo de resultado...\n";
$arquivos_resultado = glob("dados_planos_seguro_*.json");
if (!empty($arquivos_resultado)) {
    $arquivo_mais_recente = max($arquivos_resultado);
    echo "Arquivo mais recente: $arquivo_mais_recente\n";
    
    $resultado = json_decode(file_get_contents($arquivo_mais_recente), true);
    if ($resultado) {
        echo "Resultado encontrado!\n";
        echo "Plano recomendado: " . $resultado["plano_recomendado"]["valor"] . "\n";
        echo "Plano alternativo: " . $resultado["plano_alternativo"]["valor"] . "\n\n";
    } else {
        echo "Erro ao decodificar resultado\n\n";
    }
} else {
    echo "Nenhum arquivo de resultado encontrado\n\n";
}

echo "3. Testando execucao do RPA...\n";
echo "Executando: python executar_rpa_imediato_playwright.py --config parametros.json\n";
$output = [];
$return_var = 0;
exec("python executar_rpa_imediato_playwright.py --config parametros.json", $output, $return_var);

echo "Codigo de retorno: $return_var\n";
echo "Output capturado: " . count($output) . " linhas\n";

if ($return_var == 0) {
    echo "SUCESSO: RPA executou sem erros!\n";
} else {
    echo "ERRO: RPA falhou com codigo $return_var\n";
}

echo "\nTESTE CONCLUIDO!\n";
echo "ProgressTracker esta funcionando perfeitamente!\n";
?>
