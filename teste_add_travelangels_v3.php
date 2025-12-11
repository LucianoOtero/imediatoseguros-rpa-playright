<?php
/**
 * Teste para add_travelangels_v3.php - Testando lógica de duplicatas
 * Cenário 1: Lead novo (deve criar lead + workflow cria oportunidade)
 * Cenário 2: Lead duplicado (deve atualizar lead + criar oportunidade manualmente)
 */

// Função para chamar webhook
function callWebhook($url, $data) {
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
    curl_setopt($ch, CURLOPT_HTTPHEADER, [
        'Content-Type: application/json',
        'User-Agent: RPA-API-v6.9.1'
    ]);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_TIMEOUT, 30);
    curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 10);
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);

    $response = curl_exec($ch);
    $http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    $error = curl_error($ch);
    curl_close($ch);

    return [
        'success' => $http_code >= 200 && $http_code < 300,
        'http_code' => $http_code,
        'response' => $response,
        'error' => $error
    ];
}

// Função para gerar dados únicos
function generateUniqueData($scenario) {
    $timestamp = time();
    $random = rand(1000, 9999);
    
    return [
        'data' => [
            'NOME' => "TESTE V3 $scenario $random",
            'DDD-CELULAR' => '11',
            'CELULAR' => '9999' . $random,
            'Email' => "teste.v3.$scenario.$timestamp@imediatoseguros.com.br",
            'CEP' => '01234-567',
            'CPF' => '12345678901',
            'MARCA' => 'TOYOTA',
            'PLACA' => 'V3' . $random,
            'VEICULO' => 'TOYOTA',
            'ANO' => '2023',
            'GCLID_FLD' => 'v3test' . $timestamp,
            'SEXO' => 'Masculino',
            'DATA-DE-NASCIMENTO' => '01/01/1990',
            'ESTADO-CIVIL' => 'Solteiro',
            'produto' => 'seguro-auto',
            'landing_url' => 'https://teste-v3.com',
            'utm_source' => 'teste-v3',
            'utm_campaign' => 'cenario-' . $scenario
        ],
        'd' => date('c'),
        'name' => 'Teste V3 - Cenário ' . $scenario
    ];
}

echo "🧪 TESTE FINAL: Lógica de Duplicatas no add_travelangels.php\n";
echo "=" . str_repeat("=", 60) . "\n\n";

// CENÁRIO 1: Lead novo (primeira vez)
echo "📋 CENÁRIO 1: Lead Novo (Primeira vez)\n";
echo "-" . str_repeat("-", 40) . "\n";

$data1 = generateUniqueData('NOVO');
echo "📤 Dados enviados:\n";
echo "   Nome: " . $data1['data']['NOME'] . "\n";
echo "   Email: " . $data1['data']['Email'] . "\n";
echo "   Telefone: " . $data1['data']['DDD-CELULAR'] . $data1['data']['CELULAR'] . "\n";
echo "   Placa: " . $data1['data']['PLACA'] . "\n\n";

$result1 = callWebhook('https://mdmidia.com.br/add_travelangels.php', $data1);

echo "📊 RESULTADO CENÁRIO 1:\n";
echo "Status: " . ($result1['success'] ? '✅ SUCESSO' : '❌ ERRO') . "\n";
echo "HTTP Code: " . $result1['http_code'] . "\n";
echo "Response: " . $result1['response'] . "\n";

if (!empty($result1['error'])) {
    echo "Error: " . $result1['error'] . "\n";
}

echo "\n" . str_repeat("=", 60) . "\n\n";

// Aguardar um pouco entre os testes
sleep(2);

// CENÁRIO 2: Lead duplicado (mesmo email)
echo "📋 CENÁRIO 2: Lead Duplicado (Mesmo email)\n";
echo "-" . str_repeat("-", 40) . "\n";

$data2 = $data1; // Mesmos dados do cenário 1
$data2['data']['NOME'] = "TESTE V3 DUPLICADO " . rand(1000, 9999); // Nome diferente
$data2['data']['PLACA'] = "DUP" . rand(1000, 9999); // Placa diferente
$data2['data']['CELULAR'] = '8888' . rand(1000, 9999); // Telefone diferente

echo "📤 Dados enviados (mesmo email, dados diferentes):\n";
echo "   Nome: " . $data2['data']['NOME'] . "\n";
echo "   Email: " . $data2['data']['Email'] . " (MESMO EMAIL)\n";
echo "   Telefone: " . $data2['data']['DDD-CELULAR'] . $data2['data']['CELULAR'] . "\n";
echo "   Placa: " . $data2['data']['PLACA'] . "\n\n";

$result2 = callWebhook('https://mdmidia.com.br/add_travelangels.php', $data2);

echo "📊 RESULTADO CENÁRIO 2:\n";
echo "Status: " . ($result2['success'] ? '✅ SUCESSO' : '❌ ERRO') . "\n";
echo "HTTP Code: " . $result2['http_code'] . "\n";
echo "Response: " . $result2['response'] . "\n";

if (!empty($result2['error'])) {
    echo "Error: " . $result2['error'] . "\n";
}

echo "\n" . str_repeat("=", 60) . "\n\n";

// RESUMO DOS TESTES
echo "📋 RESUMO DOS TESTES:\n";
echo "-" . str_repeat("-", 20) . "\n";

echo "Cenário 1 (Lead Novo):\n";
if ($result1['success']) {
    $response1 = json_decode($result1['response'], true);
    echo "  ✅ Sucesso: " . ($response1['message'] ?? 'N/A') . "\n";
    echo "  📝 Ação: " . ($response1['action'] ?? 'N/A') . "\n";
    echo "  🆔 Lead ID: " . ($response1['lead_id'] ?? 'N/A') . "\n";
    echo "  🔄 Workflow: " . (isset($response1['workflow_opportunity']) ? 'Sim' : 'Não') . "\n";
} else {
    echo "  ❌ Falhou: " . $result1['response'] . "\n";
}

echo "\nCenário 2 (Lead Duplicado):\n";
if ($result2['success']) {
    $response2 = json_decode($result2['response'], true);
    echo "  ✅ Sucesso: " . ($response2['message'] ?? 'N/A') . "\n";
    echo "  📝 Ação: " . ($response2['action'] ?? 'N/A') . "\n";
    echo "  🆔 Lead ID: " . ($response2['lead_id'] ?? 'N/A') . "\n";
    echo "  🎯 Oportunidade ID: " . ($response2['opportunity_id'] ?? 'N/A') . "\n";
    echo "  🔄 Manual: " . (isset($response2['manual_opportunity']) ? 'Sim' : 'Não') . "\n";
} else {
    echo "  ❌ Falhou: " . $result2['response'] . "\n";
}

echo "\n🔍 Verifique os logs em: https://mdmidia.com.br/logs_travelangels.txt\n";
echo "=" . str_repeat("=", 60) . "\n";
?>
