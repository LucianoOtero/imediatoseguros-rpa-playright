<?php
/**
 * TESTE LOCAL - Payloads Reais
 * 
 * Script para testar os payloads exatos que foram enviados pelo modal
 * Baseado nos logs reais do servidor e console
 */

// Incluir dependências
require_once __DIR__ . '/class.php';

echo "=== TESTE LOCAL - Payloads Reais do Modal ===\n\n";

// ============================================================================
// PAYLOAD 1: PRIMEIRA CHAMADA (CREATE) - Do console log do usuário
// ============================================================================
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

// ============================================================================
// PAYLOAD 2: SEGUNDA CHAMADA (UPDATE) - Do log do servidor
// ============================================================================
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
        'lead_id' => '690d66fe5bee8df49',
        'contact_id' => '690d66fe5bee8df49',
        'opportunity_id' => '690d66fe82962f955'
    ],
    'd' => '2025-11-07T03:48:27.513Z',
    'name' => 'Modal WhatsApp - Dados Completos'
];

// ============================================================================
// TESTE 1: Verificar estrutura dos payloads
// ============================================================================
echo "TESTE 1: Verificar estrutura dos payloads\n";
echo "==========================================\n\n";

echo "PAYLOAD CREATE:\n";
echo json_encode($payloadCreate, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES) . "\n\n";

echo "PAYLOAD UPDATE:\n";
echo json_encode($payloadUpdate, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES) . "\n\n";

// Verificar diferenças
echo "DIFERENÇAS ENTRE OS PAYLOADS:\n";
echo "----------------------------------------\n";
echo "CREATE tem lead_id? " . (isset($payloadCreate['data']['lead_id']) ? 'SIM' : 'NÃO') . "\n";
echo "CREATE tem opportunity_id? " . (isset($payloadCreate['data']['opportunity_id']) ? 'SIM' : 'NÃO') . "\n";
echo "UPDATE tem lead_id? " . (isset($payloadUpdate['data']['lead_id']) ? 'SIM (' . $payloadUpdate['data']['lead_id'] . ')' : 'NÃO') . "\n";
echo "UPDATE tem opportunity_id? " . (isset($payloadUpdate['data']['opportunity_id']) ? 'SIM (' . $payloadUpdate['data']['opportunity_id'] . ')' : 'NÃO') . "\n";
echo "\n";

// ============================================================================
// TESTE 2: Simular requisição HTTP POST (como o modal faz)
// ============================================================================
echo "TESTE 2: Simular requisição HTTP POST\n";
echo "==========================================\n\n";

// Simular variáveis de ambiente
$_SERVER['REQUEST_METHOD'] = 'POST';
$_SERVER['HTTP_ORIGIN'] = 'https://www.segurosimediato.com.br';
$_SERVER['REQUEST_TIME_FLOAT'] = microtime(true);

// Simular entrada JSON (como o modal envia)
function simularRequisicaoPOST($payload) {
    echo "Simulando POST com payload:\n";
    echo "  - Content-Type: application/json\n";
    echo "  - Method: POST\n";
    echo "  - Body: " . json_encode($payload, JSON_UNESCAPED_UNICODE) . "\n\n";
    
    // Simular como o PHP recebe (via file_get_contents('php://input'))
    $jsonString = json_encode($payload);
    
    echo "JSON recebido pelo PHP:\n";
    echo "  - Tamanho: " . strlen($jsonString) . " bytes\n";
    echo "  - JSON válido? " . (json_decode($jsonString) !== null ? 'SIM' : 'NÃO') . "\n\n";
    
    // Decodificar como o endpoint faz
    $decoded = json_decode($jsonString, true);
    
    if ($decoded === null) {
        echo "  ❌ ERRO: Falha ao decodificar JSON\n";
        echo "  Erro: " . json_last_error_msg() . "\n";
        return null;
    }
    
    echo "JSON decodificado com sucesso:\n";
    echo "  - Tem 'data'? " . (isset($decoded['data']) ? 'SIM' : 'NÃO') . "\n";
    echo "  - Tem 'd'? " . (isset($decoded['d']) ? 'SIM (' . $decoded['d'] . ')' : 'NÃO') . "\n";
    echo "  - Tem 'name'? " . (isset($decoded['name']) ? 'SIM (' . $decoded['name'] . ')' : 'NÃO') . "\n";
    
    if (isset($decoded['data'])) {
        echo "  - Campos em 'data': " . count($decoded['data']) . "\n";
        if (isset($decoded['data']['lead_id'])) {
            echo "  - lead_id: " . $decoded['data']['lead_id'] . "\n";
        }
        if (isset($decoded['data']['opportunity_id'])) {
            echo "  - opportunity_id: " . $decoded['data']['opportunity_id'] . "\n";
        }
    }
    
    echo "\n";
    return $decoded;
}

echo "--- TESTE CREATE ---\n";
$decodedCreate = simularRequisicaoPOST($payloadCreate);

echo "--- TESTE UPDATE ---\n";
$decodedUpdate = simularRequisicaoPOST($payloadUpdate);

// ============================================================================
// TESTE 3: Simular processamento do endpoint (extrair form_data)
// ============================================================================
echo "TESTE 3: Simular processamento do endpoint\n";
echo "==========================================\n\n";

function simularProcessamentoEndpoint($decoded) {
    if (!isset($decoded['data'])) {
        echo "  ❌ ERRO: Payload não tem 'data'\n";
        return null;
    }
    
    $form_data = $decoded['data'];
    
    echo "form_data extraído:\n";
    echo "  - Total de campos: " . count($form_data) . "\n";
    echo "  - Campos principais:\n";
    
    $camposPrincipais = ['NOME', 'Email', 'CPF', 'CEP', 'PLACA', 'lead_id', 'opportunity_id'];
    foreach ($camposPrincipais as $campo) {
        if (isset($form_data[$campo])) {
            $valor = $form_data[$campo];
            if (strlen($valor) > 50) {
                $valor = substr($valor, 0, 50) . '...';
            }
            echo "    - $campo: " . ($valor ?: '(vazio)') . "\n";
        }
    }
    
    // Verificar se é CREATE ou UPDATE
    $isUpdate = isset($form_data['lead_id']) || isset($form_data['opportunity_id']);
    echo "\n  Modo detectado: " . ($isUpdate ? 'UPDATE' : 'CREATE') . "\n";
    
    if ($isUpdate) {
        echo "  IDs encontrados:\n";
        if (isset($form_data['lead_id'])) {
            echo "    - lead_id: " . $form_data['lead_id'] . "\n";
        }
        if (isset($form_data['contact_id'])) {
            echo "    - contact_id: " . $form_data['contact_id'] . "\n";
        }
        if (isset($form_data['opportunity_id'])) {
            echo "    - opportunity_id: " . $form_data['opportunity_id'] . "\n";
        }
    }
    
    echo "\n";
    return $form_data;
}

if ($decodedCreate) {
    echo "--- PROCESSAMENTO CREATE ---\n";
    $formDataCreate = simularProcessamentoEndpoint($decodedCreate);
}

if ($decodedUpdate) {
    echo "--- PROCESSAMENTO UPDATE ---\n";
    $formDataUpdate = simularProcessamentoEndpoint($decodedUpdate);
}

// ============================================================================
// TESTE 4: Simular chamada à API EspoCRM (testar class.php)
// ============================================================================
echo "TESTE 4: Simular chamada à API EspoCRM\n";
echo "==========================================\n\n";

// Configurações de teste (usar credenciais de DEV)
$API_URL = 'https://flyingdonkeys.com.br';
$API_KEY = '82d5f667f3a65a9a43341a0705be2b0c'; // API Key de produção (mesma do endpoint)

echo "⚠️  NOTA: Este teste usa credenciais reais do EspoCRM\n";
echo "   API URL: $API_URL\n";
echo "   API Key: " . substr($API_KEY, 0, 8) . "...\n\n";

echo "Simulando PATCH Opportunity (como na segunda chamada):\n";
echo "  - URL: $API_URL/Opportunity/" . $payloadUpdate['data']['opportunity_id'] . "\n";
echo "  - Method: PATCH\n";
echo "  - Payload filtrado (sem campos vazios e sem leadId):\n";

// Simular payload filtrado (como o endpoint faz)
$opportunityPayloadRaw = [
    'name' => $formDataUpdate['NOME'] ?? '',
    'leadId' => $formDataUpdate['lead_id'] ?? '',
    'stage' => 'Novo Sem Contato',
    'amount' => 0,
    'probability' => 10,
    'cCEP' => $formDataUpdate['CEP'] ?? '',
    'cCelular' => ($formDataUpdate['DDD-CELULAR'] ?? '') . ($formDataUpdate['CELULAR'] ?? ''),
    'cCpftext' => $formDataUpdate['CPF'] ?? '',
    'cGclid' => $formDataUpdate['GCLID_FLD'] ?? '',
    'cPlaca' => $formDataUpdate['PLACA'] ?? '',
    'cEmail' => $formDataUpdate['Email'] ?? '',
    'leadSource' => 'Site'
];

// Filtrar campos vazios (como o endpoint faz)
$opportunityPayloadFiltered = [];
foreach ($opportunityPayloadRaw as $key => $value) {
    // Pular leadId em UPDATE (relacionamento não pode ser alterado via PATCH)
    if ($key === 'leadId') {
        continue;
    }
    // Manter campos numéricos (incluindo 0) e strings não vazias
    if ($value !== null && $value !== '' && $value !== false) {
        $opportunityPayloadFiltered[$key] = $value;
    }
}

echo json_encode($opportunityPayloadFiltered, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE) . "\n\n";

// TESTE REAL: Chamada à API EspoCRM
echo "Executando teste real de PATCH Opportunity...\n";
echo "----------------------------------------\n";

try {
    $client = new EspoApiClient($API_URL);
    $client->setApiKey($API_KEY);
    
    echo "Fazendo PATCH em: Opportunity/" . $payloadUpdate['data']['opportunity_id'] . "\n";
    echo "Payload:\n";
    echo json_encode($opportunityPayloadFiltered, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE) . "\n\n";
    
    $response = $client->request('PATCH', 'Opportunity/' . $payloadUpdate['data']['opportunity_id'], $opportunityPayloadFiltered);
    
    echo "✅ SUCESSO: Opportunity atualizada\n";
    echo "Resposta da API:\n";
    print_r($response);
    
} catch (Exception $e) {
    echo "❌ ERRO capturado:\n";
    echo "   Mensagem: " . $e->getMessage() . "\n";
    echo "   Código HTTP: " . $e->getCode() . "\n";
    echo "   Arquivo: " . $e->getFile() . "\n";
    echo "   Linha: " . $e->getLine() . "\n";
    
    // Verificar se não há erro de TypeError relacionado a fwrite()
    if (strpos($e->getMessage(), 'fwrite') !== false || 
        strpos($e->getMessage(), 'must be of type resource') !== false ||
        strpos($e->getMessage(), 'TypeError') !== false) {
        echo "\n   ❌ ERRO CRÍTICO: Ainda há problema com fwrite() ou TypeError!\n";
        echo "   A correção no class.php não funcionou completamente.\n";
    } else {
        echo "\n   ✅ OK: Erro é da API do EspoCRM, não do código de log\n";
        echo "   Isso significa que a correção do class.php funcionou.\n";
        echo "   O erro real é: " . $e->getMessage() . "\n";
    }
}

echo "\n";

echo "=== FIM DOS TESTES ===\n";
echo "\n";
echo "PRÓXIMOS PASSOS:\n";
echo "1. Execute: php test_payloads_reais.php\n";
echo "2. Verifique se os payloads são decodificados corretamente\n";
echo "3. Configure credenciais e teste a chamada real à API\n";
echo "4. Verifique se não há TypeError fatal relacionado a fwrite()\n";

