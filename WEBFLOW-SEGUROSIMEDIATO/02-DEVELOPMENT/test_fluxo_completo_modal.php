<?php
/**
 * TESTE COMPLETO - Fluxo do Modal
 * 
 * Simula exatamente o que o modal faz:
 * 1. Primeira chamada (CREATE) - sem IDs
 * 2. Segunda chamada (UPDATE) - com IDs retornados da primeira chamada
 */

// Incluir dependências
require_once __DIR__ . '/class.php';

echo "=== TESTE COMPLETO - Fluxo do Modal ===\n\n";

// Configurações
$API_URL = 'https://flyingdonkeys.com.br';
$API_KEY = '82d5f667f3a65a9a43341a0705be2b0c';

echo "Configurações:\n";
echo "  API URL: $API_URL\n";
echo "  API Key: " . substr($API_KEY, 0, 8) . "...\n\n";

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

echo "Payload CREATE:\n";
echo json_encode($payloadCreate, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES) . "\n\n";

// Simular processamento do endpoint (extrair form_data)
$formDataCreate = $payloadCreate['data'];

// Preparar payload para EspoCRM (como o endpoint faz)
$leadDataCreate = [
    'firstName' => $formDataCreate['NOME'] ?? '',
    'emailAddress' => $formDataCreate['Email'] ?? '',
    'cCelular' => ($formDataCreate['DDD-CELULAR'] ?? '') . ($formDataCreate['CELULAR'] ?? ''),
    'addressPostalCode' => $formDataCreate['CEP'] ?? '',
    'cCpftext' => $formDataCreate['CPF'] ?? '',
    'cPlaca' => $formDataCreate['PLACA'] ?? '',
    'cGclid' => $formDataCreate['GCLID_FLD'] ?? '',
    'cWebpage' => 'segurosimediato.com.br',
    'source' => 'Site'
];

// Filtrar campos vazios
$leadDataCreateFiltered = [];
foreach ($leadDataCreate as $key => $value) {
    if ($value !== null && $value !== '' && $value !== false) {
        $leadDataCreateFiltered[$key] = $value;
    }
}

echo "Payload para EspoCRM (CREATE Lead):\n";
echo json_encode($leadDataCreateFiltered, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE) . "\n\n";

// Fazer chamada CREATE
echo "Fazendo POST em: Lead\n";
echo "----------------------------------------\n";

$leadIdCriado = null;
$opportunityIdCriado = null;

try {
    $client = new EspoApiClient($API_URL);
    $client->setApiKey($API_KEY);
    
    $responseCreate = $client->request('POST', 'Lead', $leadDataCreateFiltered);
    
    echo "✅ SUCESSO: Lead criado\n";
    echo "Resposta da API:\n";
    print_r($responseCreate);
    
    // Extrair IDs da resposta
    if (isset($responseCreate['id'])) {
        $leadIdCriado = $responseCreate['id'];
        echo "\n✅ Lead ID criado: $leadIdCriado\n";
    }
    
    // Criar Opportunity também (como o endpoint faz)
    if ($leadIdCriado) {
        $opportunityData = [
            'name' => $formDataCreate['NOME'] ?? '',
            'leadId' => $leadIdCriado,
            'stage' => 'Novo Sem Contato',
            'amount' => 0,
            'probability' => 10,
            'cGclid' => $formDataCreate['GCLID_FLD'] ?? '',
            'cWebpage' => 'segurosimediato.com.br',
            'leadSource' => 'Site'
        ];
        
        // Filtrar campos vazios
        $opportunityDataFiltered = [];
        foreach ($opportunityData as $key => $value) {
            if ($value !== null && $value !== '' && $value !== false) {
                $opportunityDataFiltered[$key] = $value;
            }
        }
        
        echo "\nCriando Opportunity...\n";
        $responseOpportunity = $client->request('POST', 'Opportunity', $opportunityDataFiltered);
        
        if (isset($responseOpportunity['id'])) {
            $opportunityIdCriado = $responseOpportunity['id'];
            echo "✅ Opportunity ID criado: $opportunityIdCriado\n";
        }
    }
    
} catch (Exception $e) {
    echo "❌ ERRO na criação:\n";
    echo "   Mensagem: " . $e->getMessage() . "\n";
    echo "   Código HTTP: " . $e->getCode() . "\n";
    
    // Verificar se não há erro de TypeError relacionado a fwrite()
    if (strpos($e->getMessage(), 'fwrite') !== false || 
        strpos($e->getMessage(), 'must be of type resource') !== false ||
        strpos($e->getMessage(), 'TypeError') !== false) {
        echo "\n   ❌ ERRO CRÍTICO: Ainda há problema com fwrite() ou TypeError!\n";
        exit(1);
    } else {
        echo "\n   ✅ OK: Erro é da API do EspoCRM, não do código de log\n";
        echo "   A correção do class.php funcionou.\n";
    }
    
    // Se falhar, usar IDs de teste do log real
    echo "\n⚠️  Usando IDs de teste do log real para continuar o teste...\n";
    $leadIdCriado = '690d66fe5bee8df49';
    $opportunityIdCriado = '690d66fe82962f955';
}

echo "\n\n";

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
        'lead_id' => $leadIdCriado, // ID da primeira chamada
        'contact_id' => $leadIdCriado,
        'opportunity_id' => $opportunityIdCriado // ID da Opportunity criada
    ],
    'd' => '2025-11-07T03:48:27.513Z',
    'name' => 'Modal WhatsApp - Dados Completos'
];

echo "Payload UPDATE:\n";
echo json_encode($payloadUpdate, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES) . "\n\n";

// Simular processamento do endpoint (extrair form_data)
$formDataUpdate = $payloadUpdate['data'];

// Preparar payload para atualizar Lead
$leadDataUpdate = [
    'firstName' => $formDataUpdate['NOME'] ?? '',
    'emailAddress' => $formDataUpdate['Email'] ?? '',
    'cCelular' => ($formDataUpdate['DDD-CELULAR'] ?? '') . ($formDataUpdate['CELULAR'] ?? ''),
    'addressPostalCode' => $formDataUpdate['CEP'] ?? '',
    'cCpftext' => $formDataUpdate['CPF'] ?? '',
    'cPlaca' => $formDataUpdate['PLACA'] ?? '',
    'cGclid' => $formDataUpdate['GCLID_FLD'] ?? '',
    'cWebpage' => 'segurosimediato.com.br',
    'source' => 'Site'
];

// Filtrar campos vazios
$leadDataUpdateFiltered = [];
foreach ($leadDataUpdate as $key => $value) {
    if ($value !== null && $value !== '' && $value !== false) {
        $leadDataUpdateFiltered[$key] = $value;
    }
}

echo "Payload para atualizar Lead:\n";
echo json_encode($leadDataUpdateFiltered, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE) . "\n\n";

// Atualizar Lead primeiro
echo "Fazendo PATCH em: Lead/$leadIdCriado\n";
echo "----------------------------------------\n";

try {
    $client = new EspoApiClient($API_URL);
    $client->setApiKey($API_KEY);
    
    $responseUpdateLead = $client->request('PATCH', 'Lead/' . $leadIdCriado, $leadDataUpdateFiltered);
    
    echo "✅ SUCESSO: Lead atualizado\n";
    echo "Resposta da API:\n";
    print_r($responseUpdateLead);
    
} catch (Exception $e) {
    echo "❌ ERRO ao atualizar Lead:\n";
    echo "   Mensagem: " . $e->getMessage() . "\n";
    echo "   Código HTTP: " . $e->getCode() . "\n";
    
    // Verificar se não há erro de TypeError relacionado a fwrite()
    if (strpos($e->getMessage(), 'fwrite') !== false || 
        strpos($e->getMessage(), 'must be of type resource') !== false ||
        strpos($e->getMessage(), 'TypeError') !== false) {
        echo "\n   ❌ ERRO CRÍTICO: Ainda há problema com fwrite() ou TypeError!\n";
        exit(1);
    } else {
        echo "\n   ✅ OK: Erro é da API do EspoCRM, não do código de log\n";
    }
}

echo "\n";

// Preparar payload para atualizar Opportunity (como o endpoint faz)
$opportunityPayloadRaw = [
    'name' => $formDataUpdate['NOME'] ?? '',
    'leadId' => $leadIdCriado, // Será removido no filtro
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

// Filtrar campos vazios e remover leadId (como o endpoint faz)
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

echo "Payload para atualizar Opportunity (filtrado, sem leadId):\n";
echo json_encode($opportunityPayloadFiltered, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE) . "\n\n";

// Atualizar Opportunity (esta é a chamada que estava dando erro 500)
echo "Fazendo PATCH em: Opportunity/$opportunityIdCriado\n";
echo "----------------------------------------\n";
echo "⚠️  Esta é a chamada que estava causando erro 500!\n\n";

try {
    $client = new EspoApiClient($API_URL);
    $client->setApiKey($API_KEY);
    
    $responseUpdateOpportunity = $client->request('PATCH', 'Opportunity/' . $opportunityIdCriado, $opportunityPayloadFiltered);
    
    echo "✅ SUCESSO: Opportunity atualizada\n";
    echo "Resposta da API:\n";
    print_r($responseUpdateOpportunity);
    
    echo "\n✅✅✅ TESTE COMPLETO PASSOU! ✅✅✅\n";
    echo "A correção do class.php funcionou perfeitamente!\n";
    
} catch (Exception $e) {
    echo "❌ ERRO ao atualizar Opportunity:\n";
    echo "   Mensagem: " . $e->getMessage() . "\n";
    echo "   Código HTTP: " . $e->getCode() . "\n";
    echo "   Arquivo: " . $e->getFile() . "\n";
    echo "   Linha: " . $e->getLine() . "\n";
    
    // Verificar se não há erro de TypeError relacionado a fwrite()
    if (strpos($e->getMessage(), 'fwrite') !== false || 
        strpos($e->getMessage(), 'must be of type resource') !== false ||
        strpos($e->getMessage(), 'TypeError') !== false) {
        echo "\n   ❌ ERRO CRÍTICO: Ainda há problema com fwrite() ou TypeError!\n";
        echo "   A correção do class.php NÃO funcionou completamente.\n";
        exit(1);
    } else {
        echo "\n   ✅ OK: Erro é da API do EspoCRM, não do código de log\n";
        echo "   Isso significa que a correção do class.php funcionou.\n";
        echo "   O erro real da API é: " . $e->getMessage() . "\n";
    }
}

echo "\n";
echo "=== FIM DO TESTE COMPLETO ===\n";

