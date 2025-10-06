<?php
/**
 * TESTE RPA V3 - Script de teste para a versão 3
 * 
 * Testa todos os endpoints da API RPA V3
 */

// Configurações
$baseUrl = 'http://localhost/executar_rpa_v3.php';
$testData = [
    'cpf' => '12345678901',
    'nome' => 'João da Silva',
    'data_nascimento' => '1990-01-01',
    'sexo' => 'M',
    'estado_civil' => 'SOLTEIRO',
    'cep' => '01234567',
    'endereco' => 'Rua Teste',
    'numero' => '123',
    'bairro' => 'Centro',
    'cidade' => 'São Paulo',
    'uf' => 'SP',
    'telefone' => '11999999999',
    'email' => 'joao@teste.com',
    'veiculo_placa' => 'ABC1234',
    'veiculo_ano' => '2020',
    'veiculo_combustivel' => 'FLEX'
];

/**
 * Função para fazer requisições HTTP
 */
function makeRequest($url, $method = 'GET', $data = null) {
    $ch = curl_init();
    
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_TIMEOUT, 30);
    curl_setopt($ch, CURLOPT_HTTPHEADER, [
        'Content-Type: application/json',
        'Accept: application/json'
    ]);
    
    if ($method === 'POST') {
        curl_setopt($ch, CURLOPT_POST, true);
        if ($data) {
            curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
        }
    } elseif ($method === 'DELETE') {
        curl_setopt($ch, CURLOPT_CUSTOMREQUEST, 'DELETE');
    }
    
    $response = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    $error = curl_error($ch);
    
    curl_close($ch);
    
    if ($error) {
        return [
            'success' => false,
            'error' => $error,
            'http_code' => $httpCode
        ];
    }
    
    return [
        'success' => true,
        'data' => json_decode($response, true),
        'http_code' => $httpCode,
        'raw_response' => $response
    ];
}

/**
 * Função para exibir resultado
 */
function displayResult($testName, $result) {
    echo "\n" . str_repeat("=", 60) . "\n";
    echo "TESTE: $testName\n";
    echo str_repeat("=", 60) . "\n";
    
    if ($result['success']) {
        echo "Status: SUCESSO\n";
        echo "HTTP Code: " . $result['http_code'] . "\n";
        echo "Resposta:\n";
        echo json_encode($result['data'], JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
    } else {
        echo "Status: ERRO\n";
        echo "HTTP Code: " . $result['http_code'] . "\n";
        echo "Erro: " . $result['error'] . "\n";
    }
    
    echo "\n";
}

// Teste 1: Health Check
echo "INICIANDO TESTES RPA V3\n";
echo "URL Base: $baseUrl\n";

$result = makeRequest($baseUrl . '?action=health');
displayResult('Health Check', $result);

// Teste 2: Listar Sessões (antes)
$result = makeRequest($baseUrl . '?action=sessions');
displayResult('Listar Sessões (antes)', $result);

// Teste 3: Iniciar RPA
$result = makeRequest($baseUrl, 'POST', $testData);
displayResult('Iniciar RPA', $result);

if ($result['success'] && isset($result['data']['session_id'])) {
    $sessionId = $result['data']['session_id'];
    echo "Session ID obtido: $sessionId\n";
    
    // Teste 4: Status (imediatamente após iniciar)
    sleep(2);
    $result = makeRequest($baseUrl . '?action=status&session_id=' . $sessionId);
    displayResult('Status (após 2s)', $result);
    
    // Teste 5: Status (após 10s)
    echo "Aguardando 10 segundos...\n";
    sleep(10);
    $result = makeRequest($baseUrl . '?action=status&session_id=' . $sessionId);
    displayResult('Status (após 10s)', $result);
    
    // Teste 6: Status (após 30s)
    echo "Aguardando mais 20 segundos...\n";
    sleep(20);
    $result = makeRequest($baseUrl . '?action=status&session_id=' . $sessionId);
    displayResult('Status (após 30s)', $result);
    
    // Teste 7: Listar Sessões (depois)
    $result = makeRequest($baseUrl . '?action=sessions');
    displayResult('Listar Sessões (depois)', $result);
    
    // Teste 8: Parar RPA
    $result = makeRequest($baseUrl . '?action=stop&session_id=' . $sessionId, 'DELETE');
    displayResult('Parar RPA', $result);
    
    // Teste 9: Status (após parar)
    sleep(2);
    $result = makeRequest($baseUrl . '?action=status&session_id=' . $sessionId);
    displayResult('Status (após parar)', $result);
    
} else {
    echo "ERRO: Não foi possível obter session_id para continuar os testes\n";
}

echo "\n" . str_repeat("=", 60) . "\n";
echo "TESTES CONCLUÍDOS\n";
echo str_repeat("=", 60) . "\n";
?>















