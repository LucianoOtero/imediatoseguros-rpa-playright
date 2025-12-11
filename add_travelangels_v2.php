<?php
require_once('class.php');

$logs = fopen("logs_travelangels_v2.txt", "a");
$timestamp = date('Y-m-d H:i:s');
fwrite($logs, "=== INÍCIO PROCESSAMENTO - $timestamp ===" . PHP_EOL);

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
    
    // 8. Fazer requisição para EspoCRM
    fwrite($logs, "8. Fazendo requisição para EspoCRM..." . PHP_EOL);
    $response = $client->request('POST', 'Lead', $apiData);
    
    fwrite($logs, "9. Resposta do EspoCRM: " . json_encode($response) . PHP_EOL);
    fwrite($logs, "   Sucesso! Lead criado com ID: " . ($response['id'] ?? 'N/A') . PHP_EOL);
    
    // 9. Resposta de sucesso
    fwrite($logs, "10. Enviando resposta de sucesso" . PHP_EOL);
    fwrite($logs, "=== PROCESSAMENTO CONCLUÍDO COM SUCESSO ===" . PHP_EOL . PHP_EOL);
    fclose($logs);
    
    http_response_code(200);
    echo json_encode([
        'success' => true,
        'message' => 'Lead criado com sucesso',
        'lead_id' => $response['id'] ?? null
    ]);
    
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