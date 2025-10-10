<?php
// Teste do endpoint RPA modificado
// Arquivo: teste-endpoint.php
// Data: 2025-10-09

echo "<h1>🧪 Teste do Endpoint RPA V6.9.0</h1>";
echo "<h2>Teste de Integração com PH3A + Webhooks + RPA</h2>";

// Dados de teste
$test_data = [
    'cpf' => '12345678901',
    'nome' => 'João Silva Teste',
    'placa' => 'ABC1234',
    'cep' => '01234567',
    'email' => 'joao.teste@email.com',
    'telefone' => '11999999999',
    'ddd_celular' => '11',
    'celular' => '999999999',
    'marca' => 'Honda',
    'ano' => '2020',
    'gclid' => 'TesteGCLID123',
    'produto' => 'seguro-auto',
    'landing_url' => 'https://segurosimediato.com.br/cotacao',
    'utm_source' => 'google',
    'utm_campaign' => 'teste-rpa'
];

echo "<h3>📋 Dados de Teste:</h3>";
echo "<pre>" . json_encode($test_data, JSON_PRETTY_PRINT) . "</pre>";

echo "<h3>🚀 Executando Teste...</h3>";

// Simular chamada do endpoint
$url = 'http://localhost/start.php'; // Ajustar conforme necessário
$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $url);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($test_data));
curl_setopt($ch, CURLOPT_HTTPHEADER, [
    'Content-Type: application/json',
    'User-Agent: Teste-RPA-v6.9.0'
]);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_TIMEOUT, 60);

$response = curl_exec($ch);
$http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
$error = curl_error($ch);
curl_close($ch);

echo "<h3>📊 Resultado do Teste:</h3>";
echo "<p><strong>HTTP Code:</strong> $http_code</p>";

if ($error) {
    echo "<p><strong>Erro cURL:</strong> $error</p>";
}

if ($response) {
    echo "<h4>Resposta JSON:</h4>";
    echo "<pre>" . json_encode(json_decode($response), JSON_PRETTY_PRINT) . "</pre>";
} else {
    echo "<p>❌ Nenhuma resposta recebida</p>";
}

echo "<hr>";
echo "<h3>📝 Instruções para Teste Manual:</h3>";
echo "<ol>";
echo "<li>Certifique-se de que o servidor PHP está rodando</li>";
echo "<li>Coloque o arquivo start.php no diretório correto</li>";
echo "<li>Teste com curl ou Postman</li>";
echo "<li>Verifique os logs em /opt/imediatoseguros-rpa/logs/</li>";
echo "</ol>";

echo "<h4>Comando cURL para teste:</h4>";
echo "<pre>";
echo "curl -X POST http://localhost/start.php \\\n";
echo "  -H \"Content-Type: application/json\" \\\n";
echo "  -d '" . json_encode($test_data) . "'";
echo "</pre>";
?>


