<?php
/**
 * TESTE LOCAL - add_flyingdonkeys_prod.php
 * 
 * Script para testar o endpoint completo localmente
 * Simula as requisições do modal (CREATE e UPDATE)
 */

// Incluir dependências
require_once __DIR__ . '/class.php';
require_once __DIR__ . '/../03-PRODUCTION/add_flyingdonkeys_prod.php';

echo "=== TESTE LOCAL - Endpoint Completo ===\n\n";

// Payload da primeira chamada (CREATE) - baseado no console log
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

// Payload da segunda chamada (UPDATE) - baseado no código do modal
$payloadUpdate = [
    'data' => [
        'DDD-CELULAR' => '11',
        'CELULAR' => '976687668',
        'GCLID_FLD' => 'teste-producao-202511070047',
        'NOME' => 'Luciano R Otero',
        'CPF' => '967.993.290-75',
        'CEP' => '01310-100',
        'PLACA' => 'ABC1234',
        'Email' => 'lrotero0047@gmail.com',
        'produto' => 'seguro-auto',
        'landing_url' => 'https://www.segurosimediato.com.br/',
        'utm_source' => '',
        'utm_campaign' => '',
        'lead_id' => '690d66fe82962f955', // ID retornado na primeira chamada
        'contact_id' => '690d66fe82962f955',
        'opportunity_id' => '690d66fe82962f955' // ID da Opportunity criada na primeira chamada
    ],
    'd' => '2025-11-07T03:48:27.510Z',
    'name' => 'Modal WhatsApp - Dados Completos'
];

echo "TESTE 1: Simular primeira chamada (CREATE)\n";
echo "==========================================\n";
echo "Payload:\n";
echo json_encode($payloadCreate, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE) . "\n\n";

// Simular POST request
$_SERVER['REQUEST_METHOD'] = 'POST';
$_SERVER['HTTP_ORIGIN'] = 'https://www.segurosimediato.com.br';
$_SERVER['REQUEST_TIME_FLOAT'] = microtime(true);

// Capturar output
ob_start();
try {
    // Simular entrada JSON
    $_POST = [];
    $GLOBALS['input_json'] = json_encode($payloadCreate);
    
    echo "⚠️  NOTA: Este teste requer configuração completa do endpoint\n";
    echo "   (credenciais EspoCRM, configurações de produção, etc.)\n";
    echo "   Execute apenas se tiver ambiente de desenvolvimento configurado.\n\n";
    
} catch (Exception $e) {
    echo "❌ ERRO: " . $e->getMessage() . "\n";
    echo "   Arquivo: " . $e->getFile() . "\n";
    echo "   Linha: " . $e->getLine() . "\n";
}
$output = ob_get_clean();
echo $output;

echo "\n\n";

echo "TESTE 2: Simular segunda chamada (UPDATE)\n";
echo "==========================================\n";
echo "Payload:\n";
echo json_encode($payloadUpdate, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE) . "\n\n";

echo "⚠️  NOTA: Este teste requer configuração completa do endpoint\n";
echo "   Execute apenas se tiver ambiente de desenvolvimento configurado.\n\n";

echo "=== FIM DOS TESTES ===\n";
echo "\n";
echo "PRÓXIMOS PASSOS:\n";
echo "1. Configure as credenciais de desenvolvimento no add_flyingdonkeys_prod.php\n";
echo "2. Execute: php test_endpoint_local.php\n";
echo "3. Verifique se não há TypeError fatal relacionado a fwrite()\n";
echo "4. Verifique os logs em /var/www/html/logs/flyingdonkeys_prod.txt\n";

