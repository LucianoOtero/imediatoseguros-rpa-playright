<?php
require_once('class.php');

$logs = fopen("logs_travelangels_v3.txt", "a");
$timestamp = date('Y-m-d H:i:s');
fwrite($logs, "=== INÍCIO PROCESSAMENTO V3 - $timestamp ===" . PHP_EOL);

try {
    // 1. Verificar se recebeu dados
    $json = file_get_contents('php://input');
    fwrite($logs, "1. JSON recebido: " . $json . PHP_EOL);
    
    if (empty($json)) {
        fwrite($logs, "ERRO: Nenhum JSON recebido" . PHP_EOL);
        fclose($logs);
        http_response_code(400);
        echo json_encode(['error' => 'No JSON data received']);
        exit;
    }
    
    // 2. Decodificar JSON
    $data = json_decode($json, true);
    fwrite($logs, "2. JSON decodificado: " . print_r($data, true) . PHP_EOL);
    
    if ($data === null) {
        fwrite($logs, "ERRO: JSON inválido - " . json_last_error_msg() . PHP_EOL);
        fclose($logs);
        http_response_code(400);
        echo json_encode(['error' => 'Invalid JSON: ' . json_last_error_msg()]);
        exit;
    }
    
    // 3. Verificar estrutura dos dados
    fwrite($logs, "3. Verificando estrutura dos dados..." . PHP_EOL);
    if (!isset($data['data'])) {
        fwrite($logs, "ERRO: Campo 'data' não encontrado" . PHP_EOL);
        fclose($logs);
        http_response_code(400);
        echo json_encode(['error' => 'Missing data field']);
        exit;
    }
    
    // 4. Extrair dados com verificações
    $name = isset($data['data']['NOME']) ? $data['data']['NOME'] : '';
    $dddCel = isset($data['data']['DDD-CELULAR']) ? $data['data']['DDD-CELULAR'] : '';
    $cel = isset($data['data']['CELULAR']) ? $data['data']['CELULAR'] : '';
    $email = isset($data['data']['Email']) ? $data['data']['Email'] : '';
    $cep = isset($data['data']['CEP']) ? $data['data']['CEP'] : '';
    $cpf = isset($data['data']['CPF']) ? $data['data']['CPF'] : '';
    $marca = isset($data['data']['MARCA']) ? $data['data']['MARCA'] : '';
    $placa = isset($data['data']['PLACA']) ? $data['data']['PLACA'] : '';
    $ano = isset($data['data']['ANO']) ? $data['data']['ANO'] : '';
    $gclid = isset($data['data']['GCLID_FLD']) ? $data['data']['GCLID_FLD'] : '';
    $date = isset($data['d']) ? $data['d'] : '';
    $webpage = isset($data['name']) ? $data['name'] : '';
    
    fwrite($logs, "4. Dados extraídos:" . PHP_EOL);
    fwrite($logs, "   Nome: $name" . PHP_EOL);
    fwrite($logs, "   Email: $email" . PHP_EOL);
    fwrite($logs, "   DDD Celular: $dddCel" . PHP_EOL);
    fwrite($logs, "   Celular: $cel" . PHP_EOL);
    fwrite($logs, "   CEP: $cep" . PHP_EOL);
    fwrite($logs, "   CPF: $cpf" . PHP_EOL);
    fwrite($logs, "   Marca: $marca" . PHP_EOL);
    fwrite($logs, "   Placa: $placa" . PHP_EOL);
    fwrite($logs, "   Ano: $ano" . PHP_EOL);
    fwrite($logs, "   GCLID: $gclid" . PHP_EOL);
    fwrite($logs, "   Data: $date" . PHP_EOL);
    fwrite($logs, "   Webpage: $webpage" . PHP_EOL);
    
    // 5. Processar telefone
    fwrite($logs, "5. Processando telefone..." . PHP_EOL);
    fwrite($logs, "   DDD antes: $dddCel" . PHP_EOL);
    
    if(strlen($dddCel) == 3) {
        $dddCel = substr($dddCel, 1);
        fwrite($logs, "   DDD após ajuste: $dddCel" . PHP_EOL);
    }
    
    $cel = $dddCel . $cel;
    fwrite($logs, "   Telefone final: $cel" . PHP_EOL);
    
    // 6. Criar cliente EspoCRM
    fwrite($logs, "6. Criando cliente EspoCRM..." . PHP_EOL);
    $client = new EspoApiClient('https://travelangels.com.br');
    $client->setApiKey('7a6c08d438ee131971f561fd836b5e15');
    fwrite($logs, "   Cliente criado com sucesso" . PHP_EOL);
    
    // 7. Preparar dados para API
    $apiData = [
        'firstName' => $name,
        'emailAddress' => $email,
        'cCelular' => $cel,
        'addressPostalCode' => $cep,
        'cCpftext' => $cpf,
        'cMarca' => $marca,
        'cPlaca' => $placa,
        'cAnoMod' => $ano,
        'cGclid' => $gclid,
        'cWebpage' => $webpage,
    ];
    
    fwrite($logs, "7. Dados para API: " . json_encode($apiData) . PHP_EOL);
    
    // 8. NOVA LÓGICA: Tentar criar lead primeiro
    fwrite($logs, "8. Tentando criar lead novo..." . PHP_EOL);
    
    try {
        $response = $client->request('POST', 'Lead', $apiData);
        fwrite($logs, "9. Lead criado com sucesso! ID: " . ($response['id'] ?? 'N/A') . PHP_EOL);
        fwrite($logs, "   Workflow do EspoCRM criará oportunidade automaticamente" . PHP_EOL);
        
        $finalResponse = [
            'success' => true,
            'message' => 'Lead criado com sucesso',
            'action' => 'created',
            'lead_id' => $response['id'] ?? null,
            'workflow_opportunity' => true
        ];
        
    } catch (Exception $e) {
        fwrite($logs, "9. Erro ao criar lead: " . $e->getMessage() . PHP_EOL);
        
        // Verificar se é erro de duplicata ou se retornou dados do lead existente
        $errorMessage = $e->getMessage();
        $isDuplicate = strpos($errorMessage, '409') !== false || 
                      strpos($errorMessage, 'duplicate') !== false || 
                      strpos($errorMessage, 'Conflict') !== false ||
                      (strpos($errorMessage, '"id":') !== false && strpos($errorMessage, '"emailAddress":') !== false);
        
        if ($isDuplicate) {
            fwrite($logs, "10. Detectado erro de duplicata - extraindo dados do lead existente..." . PHP_EOL);
            
            // Tentar extrair dados do lead existente da mensagem de erro
            $existingLeadData = null;
            if (strpos($errorMessage, '"id":') !== false) {
                // A mensagem contém dados do lead existente
                $jsonStart = strpos($errorMessage, '[');
                $jsonEnd = strrpos($errorMessage, ']') + 1;
                if ($jsonStart !== false && $jsonEnd !== false) {
                    $jsonData = substr($errorMessage, $jsonStart, $jsonEnd - $jsonStart);
                    $existingLeads = json_decode($jsonData, true);
                    if (!empty($existingLeads) && isset($existingLeads[0])) {
                        $existingLeadData = $existingLeads[0];
                    }
                }
            }
            
            if ($existingLeadData) {
                $leadId = $existingLeadData['id'];
                
                fwrite($logs, "11. Lead existente encontrado - ID: $leadId" . PHP_EOL);
                fwrite($logs, "    Nome atual: " . ($existingLeadData['firstName'] ?? 'N/A') . PHP_EOL);
                
                // Atualizar lead existente
                fwrite($logs, "12. Atualizando lead existente..." . PHP_EOL);
                $updatedLead = $client->request('PUT', 'Lead/' . $leadId, $apiData);
                fwrite($logs, "    Lead atualizado com sucesso" . PHP_EOL);
                
                // Criar nova oportunidade manualmente com TODOS os campos mapeados
                fwrite($logs, "13. Criando nova oportunidade..." . PHP_EOL);
                $opportunityData = [
                    'name' => $name . ' - ' . date('Y-m-d H:i:s'),
                    'leadId' => $leadId,
                    'amount' => 0,
                    'cCelular' => $cel,
                    'cEmail' => $email,
                    'cEmailAdress' => $email,
                    'leadSource' => 'MandeumZAP',
                    'cCEP' => $cep,
                    'cCpftext' => $cpf,
                    'cPlaca' => $placa,
                    'cWebpage' => $webpage,
                    'cMarca' => $marca,
                    'cAnoMod' => $ano,
                    'cGclid' => $gclid,
                    'cDistribuir' => true,
                    'cSeguradora' => 'Aliro'
                ];
                
                fwrite($logs, "    Dados da oportunidade: " . json_encode($opportunityData) . PHP_EOL);
                
                $opportunity = $client->request('POST', 'Opportunity', $opportunityData);
                fwrite($logs, "    Oportunidade criada com ID: " . ($opportunity['id'] ?? 'N/A') . PHP_EOL);
                
                $finalResponse = [
                    'success' => true,
                    'message' => 'Lead atualizado e oportunidade criada',
                    'action' => 'updated',
                    'lead_id' => $leadId,
                    'opportunity_id' => $opportunity['id'] ?? null,
                    'manual_opportunity' => true
                ];
                
            } else {
                fwrite($logs, "11. Lead existente não encontrado - buscando por email..." . PHP_EOL);
                
                // Fallback: buscar lead existente por email
                $existingLeads = $client->request('GET', 'Lead', [
                    'where' => [
                        ['emailAddress', '=', $email]
                    ],
                    'maxSize' => 1
                ]);
                
                if (!empty($existingLeads['list'])) {
                    $existingLead = $existingLeads['list'][0];
                    $leadId = $existingLead['id'];
                    
                    fwrite($logs, "    Lead encontrado via busca - ID: $leadId" . PHP_EOL);
                    
                    // Atualizar lead existente
                    fwrite($logs, "12. Atualizando lead existente..." . PHP_EOL);
                    $updatedLead = $client->request('PUT', 'Lead/' . $leadId, $apiData);
                    fwrite($logs, "    Lead atualizado com sucesso" . PHP_EOL);
                    
                    // Criar nova oportunidade manualmente com TODOS os campos mapeados
                    fwrite($logs, "13. Criando nova oportunidade..." . PHP_EOL);
                    $opportunityData = [
                        'name' => $name . ' - ' . date('Y-m-d H:i:s'),
                        'leadId' => $leadId,
                        'amount' => 0,
                        'cCelular' => $cel,
                        'cEmail' => $email,
                        'cEmailAdress' => $email,
                        'leadSource' => 'MandeumZAP',
                        'cCEP' => $cep,
                        'cCpftext' => $cpf,
                        'cPlaca' => $placa,
                        'cWebpage' => $webpage,
                        'cMarca' => $marca,
                        'cAnoMod' => $ano,
                        'cGclid' => $gclid,
                        'cDistribuir' => true,
                        'cSeguradora' => 'Aliro'
                    ];
                    
                    fwrite($logs, "    Dados da oportunidade: " . json_encode($opportunityData) . PHP_EOL);
                    
                    $opportunity = $client->request('POST', 'Opportunity', $opportunityData);
                    fwrite($logs, "    Oportunidade criada com ID: " . ($opportunity['id'] ?? 'N/A') . PHP_EOL);
                    
                    $finalResponse = [
                        'success' => true,
                        'message' => 'Lead atualizado e oportunidade criada',
                        'action' => 'updated',
                        'lead_id' => $leadId,
                        'opportunity_id' => $opportunity['id'] ?? null,
                        'manual_opportunity' => true
                    ];
                } else {
                    fwrite($logs, "    Lead não encontrado - erro inesperado" . PHP_EOL);
                    throw new Exception("Erro de duplicata mas lead não encontrado: " . $e->getMessage());
                }
            }
            
        } else {
            // Erro não relacionado a duplicata
            fwrite($logs, "10. Erro não relacionado a duplicata - relançando exceção" . PHP_EOL);
            throw $e;
        }
    }
    
    fwrite($logs, "14. Resposta final: " . json_encode($finalResponse) . PHP_EOL);
    fwrite($logs, "=== PROCESSAMENTO CONCLUÍDO COM SUCESSO ===" . PHP_EOL . PHP_EOL);
    fclose($logs);
    
    http_response_code(200);
    echo json_encode($finalResponse);
    
} catch (Exception $e) {
    fwrite($logs, "ERRO: " . $e->getMessage() . PHP_EOL);
    fwrite($logs, "Arquivo: " . $e->getFile() . PHP_EOL);
    fwrite($logs, "Linha: " . $e->getLine() . PHP_EOL);
    fwrite($logs, "Trace: " . $e->getTraceAsString() . PHP_EOL);
    fwrite($logs, "=== PROCESSAMENTO FALHOU ===" . PHP_EOL . PHP_EOL);
    fclose($logs);
    
    http_response_code(500);
    echo json_encode([
        'success' => false,
        'error' => $e->getMessage(),
        'file' => $e->getFile(),
        'line' => $e->getLine()
    ]);
}
?>