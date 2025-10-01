<?php
/**
 * TESTE REMOTO - WINDOWS PARA HETZNER
 * Executa PHP no Windows e chama o RPA no servidor Hetzner
 */

// Configurações do servidor
$server_config = [
    'host' => '95.216.162.123',
    'user' => 'root',
    'port' => 22,
    'key_file' => 'C:/Users/Luciano/.ssh/id_rsa', // Ajuste o caminho
    'rpa_path' => '/opt/imediatoseguros-rpa'
];

echo "<h1>🌐 Teste Remoto - Windows → Hetzner</h1>";
echo "<hr>";

// Função para executar comando via SSH
function executeSSH($config, $command) {
    $connection = ssh2_connect($config['host'], $config['port']);
    
    if (!$connection) {
        return ['success' => false, 'error' => 'Falha na conexão SSH'];
    }
    
    // Autenticação por chave
    if (file_exists($config['key_file'])) {
        $auth = ssh2_auth_pubkey_file($connection, $config['user'], $config['key_file'] . '.pub', $config['key_file']);
    } else {
        // Fallback para senha (não recomendado)
        $auth = ssh2_auth_password($connection, $config['user'], 'sua_senha_aqui');
    }
    
    if (!$auth) {
        return ['success' => false, 'error' => 'Falha na autenticação SSH'];
    }
    
    $stream = ssh2_exec($connection, $command);
    stream_set_blocking($stream, true);
    
    $output = '';
    while ($line = fgets($stream)) {
        $output .= $line;
    }
    
    fclose($stream);
    ssh2_disconnect($connection);
    
    return ['success' => true, 'output' => $output];
}

// 1. Verificar conexão SSH
echo "<h2>1. Testando Conexão SSH</h2>";
$test_command = "cd {$server_config['rpa_path']} && pwd && ls -la executar_rpa_modular_telas_1_a_5.py";
$result = executeSSH($server_config, $test_command);

if ($result['success']) {
    echo "✅ <strong>Conexão SSH estabelecida</strong><br>";
    echo "<pre style='background: #f0f0f0; padding: 10px; border-radius: 5px;'>";
    echo htmlspecialchars($result['output']);
    echo "</pre>";
} else {
    echo "❌ <strong>Erro na conexão:</strong> " . $result['error'] . "<br>";
    echo "<p><strong>Solução:</strong> Verifique se o SSH está configurado corretamente</p>";
    exit;
}

// 2. Executar o RPA
echo "<h2>2. Executando RPA no Servidor</h2>";
$session_id = "teste_remoto_" . date('Ymd_His');
$rpa_command = "cd {$server_config['rpa_path']} && xvfb-run -a python executar_rpa_modular_telas_1_a_5.py --progress-tracker json --session $session_id --modo-silencioso 2>&1";

echo "🚀 <strong>Comando:</strong> $rpa_command<br>";
echo "⏱️ <strong>Iniciando em:</strong> " . date('d/m/Y H:i:s') . "<br>";

$start_time = microtime(true);
$rpa_result = executeSSH($server_config, $rpa_command);
$end_time = microtime(true);
$execution_time = round($end_time - $start_time, 2);

echo "⏱️ <strong>Tempo de execução:</strong> {$execution_time}s<br>";

if ($rpa_result['success']) {
    echo "<h3>📋 Saída do RPA:</h3>";
    echo "<pre style='background: #f0f0f0; padding: 10px; border-radius: 5px; max-height: 300px; overflow-y: auto;'>";
    echo htmlspecialchars($rpa_result['output']);
    echo "</pre>";
} else {
    echo "❌ <strong>Erro na execução:</strong> " . $rpa_result['error'] . "<br>";
    exit;
}

// 3. Verificar arquivos de progresso
echo "<h2>3. Verificando Arquivos de Progresso</h2>";
$progress_command = "cd {$server_config['rpa_path']} && ls -la temp/progress_*.json 2>/dev/null | tail -1";
$progress_result = executeSSH($server_config, $progress_command);

if ($progress_result['success'] && trim($progress_result['output'])) {
    $latest_file = trim($progress_result['output']);
    echo "📄 <strong>Arquivo mais recente:</strong> $latest_file<br>";
    
    // Ler conteúdo do arquivo
    $read_command = "cd {$server_config['rpa_path']} && cat temp/progress_*.json | tail -1";
    $read_result = executeSSH($server_config, $read_command);
    
    if ($read_result['success']) {
        $progress_data = json_decode($read_result['output'], true);
        if ($progress_data) {
            echo "<h3>📊 Dados de Progresso:</h3>";
            echo "<pre style='background: #e8f5e8; padding: 10px; border-radius: 5px;'>";
            echo json_encode($progress_data, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
            echo "</pre>";
        }
    }
} else {
    echo "❌ <strong>Nenhum arquivo de progresso encontrado</strong><br>";
}

// 4. Verificar arquivos de dados
echo "<h2>4. Verificando Arquivos de Dados</h2>";

// JSON Compreensivo
$json_command = "cd {$server_config['rpa_path']} && ls -la temp/json_compreensivo_tela_5_*.json 2>/dev/null | tail -1";
$json_result = executeSSH($server_config, $json_command);

if ($json_result['success'] && trim($json_result['output'])) {
    $latest_json = trim($json_result['output']);
    echo "📄 <strong>JSON Compreensivo:</strong> $latest_json<br>";
    
    // Ler conteúdo do JSON
    $read_json_command = "cd {$server_config['rpa_path']} && cat temp/json_compreensivo_tela_5_*.json | tail -1";
    $read_json_result = executeSSH($server_config, $read_json_command);
    
    if ($read_json_result['success']) {
        $json_data = json_decode($read_json_result['output'], true);
        if ($json_data && isset($json_data['coberturas_detalhadas'])) {
            echo "<h3>📋 Coberturas Encontradas:</h3>";
            foreach ($json_data['coberturas_detalhadas'] as $cobertura) {
                echo "• <strong>" . $cobertura['nome_cobertura'] . ":</strong> " . 
                     $cobertura['valores']['de'] . " - " . $cobertura['valores']['ate'] . "<br>";
            }
        }
    }
} else {
    echo "❌ <strong>Nenhum arquivo JSON encontrado</strong><br>";
}

// 5. Resumo
echo "<h2>5. Resumo da Execução</h2>";
echo "<div style='background: #f0f8ff; padding: 15px; border-radius: 5px; border-left: 4px solid #2196F3;'>";
echo "🆔 <strong>Session ID:</strong> $session_id<br>";
echo "⏱️ <strong>Tempo Total:</strong> {$execution_time}s<br>";
echo "🌐 <strong>Servidor:</strong> {$server_config['host']}<br>";
echo "📁 <strong>Diretório:</strong> {$server_config['rpa_path']}<br>";
echo "</div>";

echo "<hr>";
echo "<p><strong>✅ Teste remoto concluído em:</strong> " . date('d/m/Y H:i:s') . "</p>";
?>


