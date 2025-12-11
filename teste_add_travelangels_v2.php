<?php
/**
 * Teste para chamar add_travelangels_v2.php exatamente como o JavaScript/RPA faz
 * Usando dados fictícios
 */

// Dados fictícios simulando o formato do RPA
$webhook_data = [
    'data' => [
        'NOME' => 'ANA COSTA TESTE',
        'DDD-CELULAR' => '41',
        'CELULAR' => '876543210',
        'Email' => 'ana.costa.teste.' . time() . '@imediatoseguros.com.br',
        'CEP' => '40000-000',
        'CPF' => '55566677788',
        'MARCA' => 'CHEVROLET',
        'PLACA' => 'GHI9012',
        'VEICULO' => 'CHEVROLET',
        'ANO' => '2021',
        'GCLID_FLD' => 'test345678',
        'SEXO' => 'Feminino',
        'DATA-DE-NASCIMENTO' => '05/07/1992',
        'ESTADO-CIVIL' => 'Solteira',
        'produto' => 'seguro-auto',
        'landing_url' => 'https://teste3.com',
        'utm_source' => 'instagram',
        'utm_campaign' => 'teste3'
    ],
    'd' => date('c'),
    'name' => 'Formulário de Cotação RPA'
];

// Função para chamar webhook (igual ao RPAController)
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

// Executar teste
echo "🧪 TESTE: Chamando add_travelangels.php (versão corrigida)\n";
echo "📤 Dados enviados:\n";
echo json_encode($webhook_data, JSON_PRETTY_PRINT) . "\n\n";

// Chamar o endpoint original (agora corrigido)
$result = callWebhook('https://mdmidia.com.br/add_travelangels.php', $webhook_data);

echo "📊 RESULTADO:\n";
echo "Status: " . ($result['success'] ? '✅ SUCESSO' : '❌ ERRO') . "\n";
echo "HTTP Code: " . $result['http_code'] . "\n";
echo "Response: " . $result['response'] . "\n";

if (!empty($result['error'])) {
    echo "Error: " . $result['error'] . "\n";
}

echo "\n🔍 Verifique o log em: https://mdmidia.com.br/logs_travelangels.txt\n";
?>
