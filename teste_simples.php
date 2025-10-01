<?php
/**
 * TESTE SIMPLES - COMUNICAÇÃO PHP
 * Teste básico de comunicação com o RPA
 */

echo "<h1>🧪 Teste Simples - Comunicação PHP</h1>";
echo "<hr>";

// 1. Verificar se o arquivo RPA existe
if (file_exists("executar_rpa_modular_telas_1_a_5.py")) {
    echo "✅ Arquivo RPA encontrado<br>";
} else {
    echo "❌ Arquivo RPA não encontrado<br>";
    exit;
}

// 2. Executar o RPA
echo "<h2>Executando RPA...</h2>";
$session_id = "teste_simples_" . date('Ymd_His');
$command = "xvfb-run -a python executar_rpa_modular_telas_1_a_5.py --progress-tracker json --session $session_id --modo-silencioso 2>&1";

echo "Comando: $command<br>";
echo "Session ID: $session_id<br><br>";

$start_time = microtime(true);
$output = shell_exec($command);
$end_time = microtime(true);
$execution_time = round($end_time - $start_time, 2);

echo "⏱️ Tempo de execução: {$execution_time}s<br><br>";

// 3. Verificar arquivos de progresso
echo "<h2>Arquivos de Progresso:</h2>";
$progress_files = glob("temp/progress_*.json");
if (!empty($progress_files)) {
    $latest_file = max($progress_files);
    echo "📄 Arquivo mais recente: " . basename($latest_file) . "<br>";
    
    $content = file_get_contents($latest_file);
    $data = json_decode($content, true);
    
    if ($data) {
        echo "<h3>Dados de Progresso:</h3>";
        echo "<pre style='background: #f0f0f0; padding: 10px; border-radius: 5px;'>";
        print_r($data);
        echo "</pre>";
    }
} else {
    echo "❌ Nenhum arquivo de progresso encontrado<br>";
}

// 4. Verificar arquivos de dados
echo "<h2>Arquivos de Dados:</h2>";

// JSON Compreensivo
$json_files = glob("temp/json_compreensivo_tela_5_*.json");
if (!empty($json_files)) {
    $latest_json = max($json_files);
    echo "📄 JSON Compreensivo: " . basename($latest_json) . "<br>";
    
    $json_content = file_get_contents($latest_json);
    $json_data = json_decode($json_content, true);
    
    if ($json_data && isset($json_data['coberturas_detalhadas'])) {
        echo "<h3>Coberturas Encontradas:</h3>";
        foreach ($json_data['coberturas_detalhadas'] as $cobertura) {
            echo "• " . $cobertura['nome_cobertura'] . ": " . $cobertura['valores']['de'] . " - " . $cobertura['valores']['ate'] . "<br>";
        }
    }
} else {
    echo "❌ Nenhum arquivo JSON encontrado<br>";
}

echo "<hr>";
echo "<p><strong>✅ Teste concluído em:</strong> " . date('d/m/Y H:i:s') . "</p>";
?>


