<?php
require_once('class.php');

try {
    $client = new EspoApiClient('https://travelangels.com.br');
    $client->setApiKey('7a6c08d438ee131971f561fd836b5e15');
    
    echo "Verificando campos da entidade Opportunity...\n";
    
    // Tentar obter metadata da entidade Opportunity
    $metadata = $client->request('GET', 'Opportunity/metadata');
    
    echo "Metadata da Opportunity:\n";
    echo json_encode($metadata, JSON_PRETTY_PRINT);
    
} catch (Exception $e) {
    echo "Erro: " . $e->getMessage() . "\n";
    
    // Tentar criar uma oportunidade simples para ver quais campos são aceitos
    echo "\nTentando criar oportunidade simples para ver campos aceitos...\n";
    
    try {
        $simpleOpportunity = $client->request('POST', 'Opportunity', [
            'name' => 'Teste Campos',
            'amount' => 0
        ]);
        
        echo "Oportunidade criada com sucesso:\n";
        echo json_encode($simpleOpportunity, JSON_PRETTY_PRINT);
        
    } catch (Exception $e2) {
        echo "Erro ao criar oportunidade: " . $e2->getMessage() . "\n";
    }
}
?>




