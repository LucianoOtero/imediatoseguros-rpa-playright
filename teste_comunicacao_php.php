<?php
/**
 * TESTE DE COMUNICAÇÃO PHP - RPA MODULAR TELAS 1-5
 * Testa a comunicação com o RPA e exibe os retornos JSON
 */

// Configurações
$rpa_script = "executar_rpa_modular_telas_1_a_5.py";
$session_id = "teste_php_" . date('Ymd_His');
$progress_tracker = "json";

echo "<h1>🧪 TESTE DE COMUNICAÇÃO PHP - RPA MODULAR</h1>";
echo "<hr>";

// 1. Verificar se o arquivo RPA existe
echo "<h2>1. Verificação do Arquivo RPA</h2>";
if (file_exists($rpa_script)) {
    echo "✅ <strong>Arquivo encontrado:</strong> $rpa_script<br>";
    echo "📊 <strong>Tamanho:</strong> " . number_format(filesize($rpa_script)) . " bytes<br>";
    echo "📅 <strong>Modificado:</strong> " . date('d/m/Y H:i:s', filemtime($rpa_script)) . "<br>";
} else {
    echo "❌ <strong>Arquivo não encontrado:</strong> $rpa_script<br>";
    exit;
}

// 2. Executar o RPA
echo "<h2>2. Execução do RPA</h2>";
echo "🚀 <strong>Comando:</strong> xvfb-run -a python $rpa_script --progress-tracker $progress_tracker --session $session_id<br>";
echo "⏱️ <strong>Iniciando em:</strong> " . date('d/m/Y H:i:s') . "<br>";

$start_time = microtime(true);
$command = "xvfb-run -a python $rpa_script --progress-tracker $progress_tracker --session $session_id 2>&1";
$output = shell_exec($command);
$end_time = microtime(true);
$execution_time = round($end_time - $start_time, 2);

echo "⏱️ <strong>Tempo de execução:</strong> {$execution_time}s<br>";

// 3. Exibir saída do RPA
echo "<h2>3. Saída do RPA</h2>";
echo "<pre style='background: #f5f5f5; padding: 15px; border-radius: 5px; overflow-x: auto;'>";
echo htmlspecialchars($output);
echo "</pre>";

// 4. Verificar arquivos de progresso
echo "<h2>4. Arquivos de Progresso</h2>";
$progress_files = glob("temp/progress_*.json");
if (!empty($progress_files)) {
    echo "📁 <strong>Arquivos encontrados:</strong> " . count($progress_files) . "<br>";
    
    // Pegar o arquivo mais recente
    $latest_file = max($progress_files);
    echo "📄 <strong>Arquivo mais recente:</strong> " . basename($latest_file) . "<br>";
    
    // Ler e exibir conteúdo
    $progress_content = file_get_contents($latest_file);
    $progress_data = json_decode($progress_content, true);
    
    if ($progress_data) {
        echo "<h3>📊 Dados de Progresso:</h3>";
        echo "<pre style='background: #e8f5e8; padding: 15px; border-radius: 5px;'>";
        echo json_encode($progress_data, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
        echo "</pre>";
    }
} else {
    echo "❌ <strong>Nenhum arquivo de progresso encontrado</strong><br>";
}

// 5. Verificar arquivos de dados
echo "<h2>5. Arquivos de Dados</h2>";

// JSON Compreensivo
$json_files = glob("temp/json_compreensivo_tela_5_*.json");
if (!empty($json_files)) {
    $latest_json = max($json_files);
    echo "📄 <strong>JSON Compreensivo:</strong> " . basename($latest_json) . "<br>";
    
    $json_content = file_get_contents($latest_json);
    $json_data = json_decode($json_content, true);
    
    if ($json_data) {
        echo "<h3>📋 Dados da Tela 5:</h3>";
        echo "<pre style='background: #e8f0ff; padding: 15px; border-radius: 5px; max-height: 400px; overflow-y: auto;'>";
        echo json_encode($json_data, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
        echo "</pre>";
    }
} else {
    echo "❌ <strong>Nenhum arquivo JSON encontrado</strong><br>";
}

// Retorno Intermediário
$retorno_files = glob("temp/retorno_intermediario_carrossel_*.json");
if (!empty($retorno_files)) {
    $latest_retorno = max($retorno_files);
    echo "📄 <strong>Retorno Intermediário:</strong> " . basename($latest_retorno) . "<br>";
    
    $retorno_content = file_get_contents($latest_retorno);
    $retorno_data = json_decode($retorno_content, true);
    
    if ($retorno_data) {
        echo "<h3>🔄 Dados do Carrossel:</h3>";
        echo "<pre style='background: #fff3e0; padding: 15px; border-radius: 5px; max-height: 300px; overflow-y: auto;'>";
        echo json_encode($retorno_data, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
        echo "</pre>";
    }
}

// 6. Resumo da Execução
echo "<h2>6. Resumo da Execução</h2>";
echo "<div style='background: #f0f8ff; padding: 15px; border-radius: 5px; border-left: 4px solid #2196F3;'>";
echo "🆔 <strong>Session ID:</strong> $session_id<br>";
echo "⏱️ <strong>Tempo Total:</strong> {$execution_time}s<br>";
echo "📁 <strong>Arquivos de Progresso:</strong> " . count($progress_files) . "<br>";
echo "📄 <strong>Arquivos JSON:</strong> " . count($json_files) . "<br>";
echo "🔄 <strong>Arquivos de Retorno:</strong> " . count($retorno_files) . "<br>";
echo "</div>";

// 7. Teste de Monitoramento em Tempo Real
echo "<h2>7. Teste de Monitoramento em Tempo Real</h2>";
echo "<div style='background: #f9f9f9; padding: 15px; border-radius: 5px;'>";
echo "<p>Para monitorar em tempo real, use:</p>";
echo "<code>tail -f temp/progress_*.json</code><br><br>";
echo "<p>Ou crie um script PHP que leia os arquivos de progresso periodicamente:</p>";
echo "<pre style='background: #fff; padding: 10px; border-radius: 3px;'>";
echo htmlspecialchars('
<?php
// Monitoramento em tempo real
while (true) {
    $files = glob("temp/progress_*.json");
    if (!empty($files)) {
        $latest = max($files);
        $data = json_decode(file_get_contents($latest), true);
        echo "Etapa: " . $data["etapa_atual"] . "/" . $data["total_etapas"] . " - " . $data["status"] . "\n";
    }
    sleep(2);
}
?>');
echo "</pre>";
echo "</div>";

echo "<hr>";
echo "<p><strong>✅ Teste concluído em:</strong> " . date('d/m/Y H:i:s') . "</p>";
?>
















