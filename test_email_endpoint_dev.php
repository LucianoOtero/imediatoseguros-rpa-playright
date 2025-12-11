<?php
/**
 * TESTE: Endpoint de Envio de Email - Ambiente DEV
 * 
 * Este script testa o endpoint send_email_notification_endpoint.php
 * para verificar se está funcionando corretamente.
 */

echo "🧪 TESTE: Endpoint de Envio de Email - DEV\n";
echo str_repeat("=", 60) . "\n\n";

// URL do endpoint
$endpointUrl = 'https://dev.bpsegurosimediato.com.br/webhooks/send_email_notification_endpoint.php';

// Dados de teste (simulando chamada do modal)
$testData = [
    'ddd' => '11',
    'celular' => '999999999',
    'cpf' => '12345678900',
    'nome' => 'Teste Email DEV',
    'email' => 'teste@example.com',
    'cep' => '01310-100',
    'placa' => 'ABC1234',
    'gclid' => 'test-gclid-dev-2025',
    'momento' => 'initial',
    'momento_descricao' => 'Primeiro Contato - Apenas Telefone',
    'momento_emoji' => '📞',
    'erro' => null  // Sem erro (simulando sucesso)
];

echo "📤 Enviando requisição POST para: {$endpointUrl}\n";
echo "📋 Dados de teste:\n";
echo "   - DDD: {$testData['ddd']}\n";
echo "   - Celular: {$testData['celular']}\n";
echo "   - Nome: {$testData['nome']}\n";
echo "   - Momento: {$testData['momento_descricao']}\n\n";

// Preparar requisição cURL
$ch = curl_init($endpointUrl);

curl_setopt_array($ch, [
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_POST => true,
    CURLOPT_POSTFIELDS => json_encode($testData),
    CURLOPT_HTTPHEADER => [
        'Content-Type: application/json',
        'User-Agent: Test-Script-Email-Notification-v1.0'
    ],
    CURLOPT_SSL_VERIFYPEER => false, // Para dev apenas
    CURLOPT_TIMEOUT => 30,
    CURLOPT_VERBOSE => false
]);

// Executar requisição
echo "⏳ Aguardando resposta...\n\n";
$response = curl_exec($ch);
$httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
$error = curl_error($ch);

curl_close($ch);

// Verificar erros de cURL
if ($error) {
    echo "❌ ERRO cURL: {$error}\n";
    exit(1);
}

// Exibir resultados
echo "📊 RESULTADO:\n";
echo str_repeat("-", 60) . "\n";
echo "HTTP Status Code: {$httpCode}\n";
echo "Resposta bruta: " . substr($response, 0, 500) . "\n\n";

// Tentar parsear JSON
$responseData = json_decode($response, true);

if (json_last_error() === JSON_ERROR_NONE) {
    echo "✅ Resposta JSON válida:\n";
    echo json_encode($responseData, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE) . "\n\n";
    
    // Análise do resultado
    if ($httpCode === 200 && isset($responseData['success'])) {
        if ($responseData['success']) {
            echo "✅ SUCESSO: Email enviado com sucesso!\n";
            if (isset($responseData['total_sent'])) {
                echo "   - Emails enviados: {$responseData['total_sent']}\n";
            }
            if (isset($responseData['total_failed'])) {
                echo "   - Emails falhados: {$responseData['total_failed']}\n";
            }
        } else {
            echo "⚠️ FALHA: Email não foi enviado\n";
            if (isset($responseData['error'])) {
                echo "   - Erro: {$responseData['error']}\n";
            }
            
            // Verificar se é erro de AWS SDK não instalado
            if (isset($responseData['error']) && strpos($responseData['error'], 'AWS SDK não instalado') !== false) {
                echo "\n💡 SOLUÇÃO: Instalar AWS SDK:\n";
                echo "   cd /var/www/html/dev/webhooks && composer require aws/aws-sdk-php\n";
            }
        }
    } else {
        echo "⚠️ Resposta inesperada (HTTP {$httpCode})\n";
    }
} else {
    echo "❌ ERRO: Resposta não é JSON válido\n";
    echo "   Erro JSON: " . json_last_error_msg() . "\n";
    echo "   Resposta: " . substr($response, 0, 200) . "\n";
    exit(1);
}

echo "\n" . str_repeat("=", 60) . "\n";
echo "✅ Teste concluído!\n";


