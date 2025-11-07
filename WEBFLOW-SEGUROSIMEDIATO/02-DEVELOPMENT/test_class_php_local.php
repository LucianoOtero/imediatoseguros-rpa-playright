<?php
/**
 * TESTE LOCAL - class.php
 * 
 * Script para testar a correção do class.php localmente
 * Simula as requisições que causam erro 500
 */

// Incluir o class.php local
require_once __DIR__ . '/class.php';

// Configurações de teste (usar credenciais de DEV ou mock)
$API_URL = 'https://dev.bpsegurosimediato.com.br/api/v1'; // ou URL de teste
$USERNAME = 'test_user'; // Substituir por credenciais reais de DEV
$PASSWORD = 'test_password'; // Substituir por credenciais reais de DEV

echo "=== TESTE LOCAL - class.php ===\n\n";

// TESTE 1: Simular erro da API (código HTTP diferente de 200)
echo "TESTE 1: Simular erro da API (código HTTP 400)\n";
echo "----------------------------------------\n";

try {
    $client = new EspoApiClient($API_URL, $USERNAME, $PASSWORD);
    
    // Tentar fazer uma requisição que vai falhar (endpoint inválido ou credenciais erradas)
    // Isso vai causar um erro HTTP diferente de 200
    $response = $client->request('GET', 'InvalidEndpoint/InvalidId', []);
    
    echo "❌ ERRO: Não deveria chegar aqui\n";
} catch (Exception $e) {
    echo "✅ SUCESSO: Exception capturada corretamente\n";
    echo "   Mensagem: " . $e->getMessage() . "\n";
    echo "   Código: " . $e->getCode() . "\n";
    echo "   Arquivo: " . $e->getFile() . "\n";
    echo "   Linha: " . $e->getLine() . "\n";
}

echo "\n";

// TESTE 2: Verificar se logs.txt pode ser escrito (simular problema de permissão)
echo "TESTE 2: Verificar escrita em logs.txt\n";
echo "----------------------------------------\n";

$logs = @fopen("logs.txt", "a");
if ($logs !== false) {
    echo "✅ SUCESSO: Arquivo logs.txt pode ser aberto\n";
    fwrite($logs, "Teste de escrita - " . date('Y-m-d H:i:s') . PHP_EOL);
    fclose($logs);
} else {
    echo "⚠️  AVISO: Não foi possível abrir logs.txt (esperado em ambiente local)\n";
    echo "   Isso não é um erro - a correção previne o TypeError fatal\n";
}

echo "\n";

// TESTE 3: Simular o cenário completo (como no add_flyingdonkeys_prod.php)
echo "TESTE 3: Simular cenário completo (PATCH Opportunity)\n";
echo "----------------------------------------\n";

// Payload de teste baseado no console log do usuário
$testPayload = [
    'name' => 'Teste Opportunity',
    'cCelular' => '11976687668',
    'cEmail' => 'teste@teste.com.br',
    'cCpftext' => '96799329075',
    'cCEP' => '01310-100',
    'cPlaca' => 'ABC1234',
    'cMarca' => 'Honda',
    'cAnoMod' => '2020',
    'cGclid' => 'teste-producao-202511070047',
    'cWebpage' => 'https://www.segurosimediato.com.br/',
    'leadSource' => 'webflow',
    'stage' => 'Novo Sem Contato',
    'amount' => 0,
    'probability' => 10
];

echo "Payload de teste:\n";
print_r($testPayload);

echo "\nTentando fazer PATCH em Opportunity (vai falhar sem credenciais válidas)...\n";

try {
    $client = new EspoApiClient($API_URL, $USERNAME, $PASSWORD);
    
    // Tentar atualizar uma Opportunity (vai falhar, mas não deve causar TypeError fatal)
    $response = $client->request('PATCH', 'Opportunity/690d66fe82962f955', $testPayload);
    
    echo "❌ ERRO: Não deveria chegar aqui\n";
} catch (Exception $e) {
    echo "✅ SUCESSO: Exception capturada sem TypeError fatal\n";
    echo "   Mensagem: " . $e->getMessage() . "\n";
    echo "   Código HTTP: " . $e->getCode() . "\n";
    
    // Verificar se não há erro de TypeError
    if (strpos($e->getMessage(), 'fwrite') !== false || 
        strpos($e->getMessage(), 'must be of type resource') !== false) {
        echo "   ❌ ERRO: Ainda há problema com fwrite()!\n";
    } else {
        echo "   ✅ OK: Erro é da API, não do código de log\n";
    }
}

echo "\n=== FIM DOS TESTES ===\n";

