<?php
require_once('class.php');

echo "Iniciando teste RPA...\n";

try {
    $client = new EspoApiClient('https://travelangels.com.br');
    $client->setApiKey('7a6c08d438ee131971f561fd836b5e15');
    echo "Cliente EspoCRM criado\n";
    
    $response = $client->request('POST', 'Lead', [
        'firstName' => 'TESTE RPA',
        'emailAddress' => 'teste.rpa.' . time() . '@imediatoseguros.com.br',
        'cCelular' => '11999999999',
        'addressPostalCode' => '03317-000',
        'cCpftext' => '99999999999',
        'cMarca' => 'TOYOTA',
        'cPlaca' => 'TEST1234',
        'cAnoMod' => '2025',
        'cGclid' => '',
        'cWebpage' => 'Teste RPA Servidor',
    ]);
    
    echo "SUCESSO! Lead criado com ID: " . ($response['id'] ?? 'N/A') . "\n";
    echo "Email: teste.rpa." . time() . "@imediatoseguros.com.br\n";
    
} catch (Exception $e) {
    echo "ERRO: " . $e->getMessage() . "\n";
    echo "Arquivo: " . $e->getFile() . "\n";
    echo "Linha: " . $e->getLine() . "\n";
}
?>




