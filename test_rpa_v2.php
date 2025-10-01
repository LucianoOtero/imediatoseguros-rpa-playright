<?php
/**
 * TESTE DO RPA V2
 * Script de teste para validar a implementação
 */

// Configurações de teste
$baseUrl = 'http://localhost/executar_rpa_v2.php';
$testData = [
    'placa' => 'FPG8D63',
    'marca' => 'TOYOTA',
    'modelo' => 'COROLLA XEI 1.8/1.8 FLEX 16V MEC',
    'ano' => '2009',
    'cep' => '03317-000',
    'nome' => 'TESTE RPA V2',
    'cpf' => '12345678901',
    'email' => 'teste@imediatoseguros.com.br',
    'celular' => '11999999999'
];

echo "🧪 TESTE DO RPA V2\n";
echo "==================\n\n";

// Função para fazer requisição
function makeRequest($url, $data) {
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
    curl_setopt($ch, CURLOPT_HTTPHEADER, [
        'Content-Type: application/json',
        'Content-Length: ' . strlen(json_encode($data))
    ]);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_TIMEOUT, 30);
    
    $response = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    $error = curl_error($ch);
    curl_close($ch);
    
    return [
        'response' => $response,
        'http_code' => $httpCode,
        'error' => $error
    ];
}

// Teste 1: Health Check
echo "1. 🔍 Teste de Health Check\n";
echo "---------------------------\n";

$healthResult = makeRequest($baseUrl, ['action' => 'health']);
echo "HTTP Code: " . $healthResult['http_code'] . "\n";

if ($healthResult['error']) {
    echo "❌ Erro cURL: " . $healthResult['error'] . "\n";
} else {
    $healthData = json_decode($healthResult['response'], true);
    if ($healthData && $healthData['success']) {
        echo "✅ Health Check OK\n";
        echo "Python disponível: " . ($healthData['health']['environment']['python_available'] ? 'Sim' : 'Não') . "\n";
        echo "Script RPA disponível: " . ($healthData['health']['environment']['rpa_script_available'] ? 'Sim' : 'Não') . "\n";
        echo "Redis disponível: " . ($healthData['health']['environment']['redis_available'] ? 'Sim' : 'Não') . "\n";
        echo "Xvfb disponível: " . ($healthData['health']['environment']['xvfb_available'] ? 'Sim' : 'Não') . "\n";
    } else {
        echo "❌ Health Check falhou\n";
        echo "Resposta: " . $healthResult['response'] . "\n";
    }
}

echo "\n";

// Teste 2: Iniciar RPA
echo "2. 🚀 Teste de Início do RPA\n";
echo "-----------------------------\n";

$startResult = makeRequest($baseUrl, [
    'action' => 'start',
    'dados' => $testData
]);

echo "HTTP Code: " . $startResult['http_code'] . "\n";

if ($startResult['error']) {
    echo "❌ Erro cURL: " . $startResult['error'] . "\n";
} else {
    $startData = json_decode($startResult['response'], true);
    if ($startData && $startData['success']) {
        echo "✅ RPA iniciado com sucesso\n";
        echo "Session ID: " . $startData['session_id'] . "\n";
        echo "PID: " . $startData['pid'] . "\n";
        
        $sessionId = $startData['session_id'];
        
        // Aguardar um pouco
        echo "⏳ Aguardando 10 segundos...\n";
        sleep(10);
        
        // Teste 3: Verificar Status
        echo "\n3. 📊 Teste de Status\n";
        echo "---------------------\n";
        
        $statusResult = makeRequest($baseUrl, [
            'action' => 'status',
            'session_id' => $sessionId
        ]);
        
        echo "HTTP Code: " . $statusResult['http_code'] . "\n";
        
        if ($statusResult['error']) {
            echo "❌ Erro cURL: " . $statusResult['error'] . "\n";
        } else {
            $statusData = json_decode($statusResult['response'], true);
            if ($statusData && $statusData['success']) {
                echo "✅ Status obtido com sucesso\n";
                echo "Tem estimativas: " . ($statusData['has_estimates'] ? 'Sim' : 'Não') . "\n";
                if ($statusData['has_estimates']) {
                    echo "Arquivo de estimativas: " . $statusData['estimates_file'] . "\n";
                }
                echo "Arquivo de progresso: " . $statusData['progress_file'] . "\n";
                
                // Mostrar dados de progresso
                if (isset($statusData['data'])) {
                    echo "Dados de progresso:\n";
                    echo json_encode($statusData['data'], JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE) . "\n";
                }
            } else {
                echo "❌ Status falhou\n";
                echo "Resposta: " . $statusResult['response'] . "\n";
            }
        }
        
        // Teste 4: Parar RPA
        echo "\n4. 🛑 Teste de Parada\n";
        echo "---------------------\n";
        
        $stopResult = makeRequest($baseUrl, [
            'action' => 'stop',
            'session_id' => $sessionId
        ]);
        
        echo "HTTP Code: " . $stopResult['http_code'] . "\n";
        
        if ($stopResult['error']) {
            echo "❌ Erro cURL: " . $stopResult['error'] . "\n";
        } else {
            $stopData = json_decode($stopResult['response'], true);
            if ($stopData && $stopData['success']) {
                echo "✅ RPA parado com sucesso\n";
            } else {
                echo "❌ Parada falhou\n";
                echo "Resposta: " . $stopResult['response'] . "\n";
            }
        }
        
    } else {
        echo "❌ Início do RPA falhou\n";
        echo "Resposta: " . $startResult['response'] . "\n";
    }
}

echo "\n";
echo "🏁 Teste concluído\n";
echo "==================\n";
?>

