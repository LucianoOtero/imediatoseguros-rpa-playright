<?php
/**
 * TESTE HTTP - WINDOWS PARA HETZNER
 * Usa HTTP para comunicação com o servidor Hetzner
 */

// Configurações do servidor
$server_url = 'http://95.216.162.123'; // Ajuste se necessário
$api_endpoints = [
    'start_rpa' => '/executar_rpa.php',
    'get_progress' => '/get_progress.php',
    'test_connection' => '/teste_simples.php'
];

echo "<h1>🌐 Teste HTTP - Windows → Hetzner</h1>";
echo "<hr>";

// Função para fazer requisição HTTP
function makeRequest($url, $data = null, $method = 'GET') {
    $ch = curl_init();
    
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_TIMEOUT, 300); // 5 minutos
    curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 30);
    curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
    
    if ($method === 'POST' && $data) {
        curl_setopt($ch, CURLOPT_POST, true);
        curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
        curl_setopt($ch, CURLOPT_HTTPHEADER, [
            'Content-Type: application/json',
            'Content-Length: ' . strlen(json_encode($data))
        ]);
    }
    
    $response = curl_exec($ch);
    $http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    $error = curl_error($ch);
    
    curl_close($ch);
    
    return [
        'success' => $http_code === 200 && !$error,
        'data' => $response,
        'http_code' => $http_code,
        'error' => $error
    ];
}

// 1. Testar conexão
echo "<h2>1. Testando Conexão HTTP</h2>";
$test_url = $server_url . $api_endpoints['test_connection'];
echo "🔗 <strong>URL:</strong> $test_url<br>";

$connection_test = makeRequest($test_url);

if ($connection_test['success']) {
    echo "✅ <strong>Conexão HTTP estabelecida</strong><br>";
    echo "📊 <strong>Status HTTP:</strong> " . $connection_test['http_code'] . "<br>";
} else {
    echo "❌ <strong>Erro na conexão:</strong> " . $connection_test['error'] . "<br>";
    echo "📊 <strong>Status HTTP:</strong> " . $connection_test['http_code'] . "<br>";
    echo "<p><strong>Solução:</strong> Verifique se o servidor web está rodando no Hetzner</p>";
    exit;
}

// 2. Executar RPA via API
echo "<h2>2. Executando RPA via API</h2>";
$session_id = "teste_http_" . date('Ymd_His');
$start_url = $server_url . $api_endpoints['start_rpa'];

echo "🚀 <strong>Iniciando RPA...</strong><br>";
echo "⏱️ <strong>Iniciando em:</strong> " . date('d/m/Y H:i:s') . "<br>";

$start_time = microtime(true);
$start_result = makeRequest($start_url, [
    'session' => $session_id,
    'action' => 'start'
], 'POST');

$end_time = microtime(true);
$execution_time = round($end_time - $start_time, 2);

echo "⏱️ <strong>Tempo de resposta:</strong> {$execution_time}s<br>";

if ($start_result['success']) {
    $start_data = json_decode($start_result['data'], true);
    if ($start_data && $start_data['success']) {
        echo "✅ <strong>RPA iniciado com sucesso!</strong><br>";
        echo "🆔 <strong>Session ID:</strong> " . $start_data['session_id'] . "<br>";
        echo "🔢 <strong>PID:</strong> " . $start_data['pid'] . "<br>";
    } else {
        echo "❌ <strong>Erro ao iniciar RPA:</strong> " . ($start_data['error'] ?? 'Erro desconhecido') . "<br>";
        exit;
    }
} else {
    echo "❌ <strong>Erro na requisição:</strong> " . $start_result['error'] . "<br>";
    exit;
}

// 3. Monitorar progresso
echo "<h2>3. Monitorando Progresso</h2>";
$progress_url = $server_url . $api_endpoints['get_progress'] . "?session=" . $session_id;

echo "⏳ <strong>Aguardando progresso...</strong><br>";

$max_attempts = 30; // 30 tentativas
$attempt = 0;
$progress_found = false;

while ($attempt < $max_attempts && !$progress_found) {
    $attempt++;
    echo "🔄 <strong>Tentativa $attempt/$max_attempts</strong><br>";
    
    $progress_result = makeRequest($progress_url);
    
    if ($progress_result['success']) {
        $progress_data = json_decode($progress_result['data'], true);
        
        if ($progress_data && $progress_data['success'] && isset($progress_data['data'])) {
            $data = $progress_data['data'];
            echo "📊 <strong>Progresso:</strong> " . $data['etapa_atual'] . "/" . $data['total_etapas'] . 
                 " (" . round($data['percentual']) . "%) - " . $data['status'] . "<br>";
            
            if ($data['etapa_atual'] >= $data['total_etapas']) {
                $progress_found = true;
                echo "🎉 <strong>Execução concluída!</strong><br>";
            }
        } else {
            echo "⏳ <strong>Aguardando dados de progresso...</strong><br>";
        }
    } else {
        echo "❌ <strong>Erro ao obter progresso:</strong> " . $progress_result['error'] . "<br>";
    }
    
    if (!$progress_found) {
        sleep(2); // Aguardar 2 segundos
    }
}

if (!$progress_found) {
    echo "⏰ <strong>Timeout atingido</strong><br>";
}

// 4. Obter dados finais
echo "<h2>4. Dados Finais</h2>";
$final_progress = makeRequest($progress_url);

if ($final_progress['success']) {
    $final_data = json_decode($final_progress['data'], true);
    
    if ($final_data && $final_data['success']) {
        echo "<h3>📊 Progresso Final:</h3>";
        echo "<pre style='background: #e8f5e8; padding: 10px; border-radius: 5px;'>";
        echo json_encode($final_data['data'], JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
        echo "</pre>";
    }
}

// 5. Resumo
echo "<h2>5. Resumo da Execução</h2>";
echo "<div style='background: #f0f8ff; padding: 15px; border-radius: 5px; border-left: 4px solid #2196F3;'>";
echo "🆔 <strong>Session ID:</strong> $session_id<br>";
echo "⏱️ <strong>Tempo Total:</strong> " . round(microtime(true) - $start_time, 2) . "s<br>";
echo "🌐 <strong>Servidor:</strong> $server_url<br>";
echo "🔄 <strong>Tentativas de Progresso:</strong> $attempt<br>";
echo "✅ <strong>Progresso Encontrado:</strong> " . ($progress_found ? 'Sim' : 'Não') . "<br>";
echo "</div>";

echo "<hr>";
echo "<p><strong>✅ Teste HTTP concluído em:</strong> " . date('d/m/Y H:i:s') . "</p>";
?>



























