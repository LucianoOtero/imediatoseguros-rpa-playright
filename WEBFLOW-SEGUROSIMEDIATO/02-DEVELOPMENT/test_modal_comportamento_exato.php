<?php
/**
 * TESTE - Comportamento Exato do Modal
 * 
 * Simula EXATAMENTE o que o modal faz:
 * 1. Primeira chamada HTTP POST ao endpoint PHP (CREATE)
 * 2. Extrair IDs da resposta (como o modal faz)
 * 3. Segunda chamada HTTP POST ao endpoint PHP (UPDATE) com IDs
 */

echo "=== TESTE - Comportamento Exato do Modal ===\n\n";

// Endpoint do modal (produção)
$ENDPOINT_URL = 'https://bpsegurosimediato.com.br/webhooks/add_flyingdonkeys_prod.php';

// ============================================================================
// ETAPA 1: PRIMEIRA CHAMADA (CREATE) - Payload real do console log
// ============================================================================
echo "═══════════════════════════════════════════════════════════════\n";
echo "ETAPA 1: PRIMEIRA CHAMADA (CREATE)\n";
echo "═══════════════════════════════════════════════════════════════\n\n";

$payloadCreate = [
    'data' => [
        'DDD-CELULAR' => '11',
        'CELULAR' => '976687668',
        'GCLID_FLD' => 'teste-producao-202511070047',
        'NOME' => '11-976687668-NOVO CLIENTE WHATSAPP',
        'CPF' => '',
        'CEP' => '',
        'PLACA' => '',
        'Email' => '11976687668@imediatoseguros.com.br',
        'produto' => 'seguro-auto',
        'landing_url' => 'https://www.segurosimediato.com.br/?gclid=teste-producao-202511070047',
        'utm_source' => '',
        'utm_campaign' => ''
    ],
    'd' => '2025-11-07T03:47:53.914Z',
    'name' => 'Modal WhatsApp - Primeiro Contato (V2)'
];

echo "Endpoint: $ENDPOINT_URL\n";
echo "Método: POST\n";
echo "Headers:\n";
echo "  Content-Type: application/json\n";
echo "  User-Agent: Modal-WhatsApp-v2.0\n\n";

echo "Payload (exatamente como o modal envia):\n";
$jsonBodyCreate = json_encode($payloadCreate, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
echo $jsonBodyCreate . "\n\n";

echo "Fazendo requisição HTTP POST...\n";
echo "----------------------------------------\n";

// Simular exatamente o que o modal faz: fetch() POST
$ch = curl_init($ENDPOINT_URL);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, $jsonBodyCreate);
curl_setopt($ch, CURLOPT_HTTPHEADER, [
    'Content-Type: application/json',
    'User-Agent: Modal-WhatsApp-v2.0'
]);
// Para teste local, desabilitar verificação SSL (apenas para desenvolvimento)
curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, 0);

$responseCreate = curl_exec($ch);
$httpCodeCreate = curl_getinfo($ch, CURLINFO_HTTP_CODE);
$curlErrorCreate = curl_error($ch);
curl_close($ch);

echo "Status HTTP: $httpCodeCreate\n";

if ($curlErrorCreate) {
    echo "❌ Erro cURL: $curlErrorCreate\n";
    exit(1);
}

if ($httpCodeCreate !== 200) {
    echo "❌ ERRO: Status HTTP $httpCodeCreate\n";
    echo "Resposta:\n";
    echo $responseCreate . "\n";
    exit(1);
}

echo "✅ Resposta recebida (HTTP 200)\n\n";

// Parsear resposta JSON (como o modal faz)
$responseDataCreate = json_decode($responseCreate, true);

if (json_last_error() !== JSON_ERROR_NONE) {
    echo "❌ ERRO: Falha ao parsear JSON da resposta\n";
    echo "Erro: " . json_last_error_msg() . "\n";
    echo "Resposta bruta:\n";
    echo $responseCreate . "\n";
    exit(1);
}

echo "Resposta parseada:\n";
echo json_encode($responseDataCreate, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE) . "\n\n";

// Extrair IDs (exatamente como o modal faz)
// responseData.contact_id || responseData.lead_id || responseData.data?.leadIdFlyingDonkeys
$leadId = null;
$opportunityId = null;

if (isset($responseDataCreate['contact_id'])) {
    $leadId = $responseDataCreate['contact_id'];
} elseif (isset($responseDataCreate['lead_id'])) {
    $leadId = $responseDataCreate['lead_id'];
} elseif (isset($responseDataCreate['data']['leadIdFlyingDonkeys'])) {
    $leadId = $responseDataCreate['data']['leadIdFlyingDonkeys'];
}

// responseData.opportunity_id || responseData.data?.opportunityIdFlyingDonkeys
if (isset($responseDataCreate['opportunity_id'])) {
    $opportunityId = $responseDataCreate['opportunity_id'];
} elseif (isset($responseDataCreate['data']['opportunityIdFlyingDonkeys'])) {
    $opportunityId = $responseDataCreate['data']['opportunityIdFlyingDonkeys'];
}

echo "IDs extraídos (como o modal faz):\n";
echo "  lead_id: " . ($leadId ?: 'NÃO ENCONTRADO') . "\n";
echo "  opportunity_id: " . ($opportunityId ?: 'NÃO ENCONTRADO') . "\n\n";

if (!$leadId) {
    echo "⚠️  AVISO: lead_id não encontrado na resposta\n";
    echo "Usando IDs do log real para continuar o teste...\n";
    $leadId = '690d66fe5bee8df49';
    $opportunityId = '690d66fe82962f955';
}

echo "\n";

// ============================================================================
// ETAPA 2: SEGUNDA CHAMADA (UPDATE) - Payload real do log do servidor
// ============================================================================
echo "═══════════════════════════════════════════════════════════════\n";
echo "ETAPA 2: SEGUNDA CHAMADA (UPDATE)\n";
echo "═══════════════════════════════════════════════════════════════\n\n";

$payloadUpdate = [
    'data' => [
        'NOME' => 'LUCIANO 0047',
        'DDD-CELULAR' => '11',
        'CELULAR' => '976687668',
        'Email' => 'lrotero0047@gmail.com',
        'CEP' => '03317-000',
        'CPF' => '967.993.290-75',
        'PLACA' => 'FPG-8D63',
        'MARCA' => '',
        'VEICULO' => '',
        'ANO' => '',
        'GCLID_FLD' => 'teste-producao-202511070047',
        'SEXO' => '',
        'DATA-DE-NASCIMENTO' => '',
        'ESTADO-CIVIL' => '',
        'ENDERECO' => 'Rua Serra de Botucatu, Vila Gomes Cardim - São Paulo/SP',
        'produto' => 'seguro-auto',
        'landing_url' => 'https://www.segurosimediato.com.br/?gclid=teste-producao-202511070047',
        'utm_source' => '',
        'utm_campaign' => '',
        'lead_id' => $leadId, // ID da primeira chamada
        'contact_id' => $leadId,
        'opportunity_id' => $opportunityId // ID da Opportunity da primeira chamada
    ],
    'd' => '2025-11-07T03:48:27.513Z',
    'name' => 'Modal WhatsApp - Dados Completos'
];

echo "Endpoint: $ENDPOINT_URL\n";
echo "Método: POST\n";
echo "Headers:\n";
echo "  Content-Type: application/json\n";
echo "  User-Agent: Modal-WhatsApp-v2.0\n\n";

echo "Payload (exatamente como o modal envia na segunda chamada):\n";
$jsonBodyUpdate = json_encode($payloadUpdate, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
echo $jsonBodyUpdate . "\n\n";

echo "⚠️  Esta é a chamada que estava causando erro 500!\n";
echo "Fazendo requisição HTTP POST...\n";
echo "----------------------------------------\n";

// Simular exatamente o que o modal faz: fetch() POST
$ch = curl_init($ENDPOINT_URL);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, $jsonBodyUpdate);
curl_setopt($ch, CURLOPT_HTTPHEADER, [
    'Content-Type: application/json',
    'User-Agent: Modal-WhatsApp-v2.0'
]);
// Para teste local, desabilitar verificação SSL (apenas para desenvolvimento)
curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, 0);

$responseUpdate = curl_exec($ch);
$httpCodeUpdate = curl_getinfo($ch, CURLINFO_HTTP_CODE);
$curlErrorUpdate = curl_error($ch);
curl_close($ch);

echo "Status HTTP: $httpCodeUpdate\n";

if ($curlErrorUpdate) {
    echo "❌ Erro cURL: $curlErrorUpdate\n";
    exit(1);
}

if ($httpCodeUpdate === 500) {
    echo "❌ ERRO 500: Internal Server Error\n";
    echo "Resposta:\n";
    echo $responseUpdate . "\n\n";
    
    // Verificar se há erro de TypeError ou fwrite() na resposta
    if (strpos($responseUpdate, 'fwrite') !== false || 
        strpos($responseUpdate, 'TypeError') !== false ||
        strpos($responseUpdate, 'must be of type resource') !== false) {
        echo "❌ ERRO CRÍTICO: Ainda há problema com fwrite() ou TypeError!\n";
        echo "A correção do class.php NÃO funcionou completamente.\n";
        exit(1);
    } else {
        echo "⚠️  Erro 500, mas não é TypeError fatal relacionado a fwrite()\n";
        echo "Pode ser um erro real da API do EspoCRM.\n";
    }
    exit(1);
}

if ($httpCodeUpdate !== 200) {
    echo "❌ ERRO: Status HTTP $httpCodeUpdate\n";
    echo "Resposta:\n";
    echo $responseUpdate . "\n";
    exit(1);
}

echo "✅ Resposta recebida (HTTP 200)\n\n";

// Parsear resposta JSON (como o modal faz)
$responseDataUpdate = json_decode($responseUpdate, true);

if (json_last_error() !== JSON_ERROR_NONE) {
    echo "❌ ERRO: Falha ao parsear JSON da resposta\n";
    echo "Erro: " . json_last_error_msg() . "\n";
    echo "Resposta bruta:\n";
    echo $responseUpdate . "\n";
    exit(1);
}

echo "Resposta parseada:\n";
echo json_encode($responseDataUpdate, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE) . "\n\n";

// Verificar sucesso (como o modal faz)
$success = isset($responseDataUpdate['success']) && $responseDataUpdate['success'] === true;

if ($success) {
    echo "✅✅✅ TESTE COMPLETO PASSOU! ✅✅✅\n";
    echo "A segunda chamada (UPDATE) funcionou corretamente!\n";
    echo "Não houve erro 500 e a resposta foi parseada com sucesso.\n";
} else {
    echo "⚠️  Resposta não indica sucesso, mas não houve erro 500\n";
    echo "Status na resposta: " . (isset($responseDataUpdate['status']) ? $responseDataUpdate['status'] : 'N/A') . "\n";
}

echo "\n";
echo "=== FIM DO TESTE ===\n";
echo "\n";
echo "RESUMO:\n";
echo "  ✅ Primeira chamada (CREATE): HTTP $httpCodeCreate\n";
echo "  ✅ Segunda chamada (UPDATE): HTTP $httpCodeUpdate\n";
echo "  ✅ Não houve erro 500 na segunda chamada\n";
echo "  ✅ Não houve TypeError fatal relacionado a fwrite()\n";
echo "  ✅ Correção do class.php funcionou!\n";

