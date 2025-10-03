<?php
header('Content-Type: application/json');

// Log de debug
error_log("=== API RPA DEBUG (COM WRAPPER) ===");
error_log("Timestamp: " . date('Y-m-d H:i:s'));

// Capturar input bruto
$raw_input = file_get_contents('php://input');
error_log("Raw input length: " . strlen($raw_input));
error_log("Raw input: " . $raw_input);

// Validar se há dados
if (empty($raw_input)) {
    error_log("ERROR: No input data");
    http_response_code(400);
    echo json_encode([
        'success' => false, 
        'error' => 'No input data',
        'timestamp' => date('Y-m-d H:i:s')
    ]);
    exit;
}

// Decodificar JSON
$dados = json_decode($raw_input, true);
$json_error = json_last_error();

// Verificar se JSON é válido
if ($json_error !== JSON_ERROR_NONE) {
    error_log("ERROR: JSON decode failed - " . json_last_error_msg());
    http_response_code(400);
    echo json_encode([
        'success' => false, 
        'error' => 'Invalid JSON: ' . json_last_error_msg(),
        'json_error_code' => $json_error,
        'raw_input' => $raw_input,
        'timestamp' => date('Y-m-d H:i:s')
    ]);
    exit;
}

error_log("JSON decoded successfully: " . print_r($dados, true));

// Validar estrutura obrigatória
if (!isset($dados['session'])) {
    error_log("ERROR: Session key missing");
    http_response_code(400);
    echo json_encode([
        'success' => false, 
        'error' => 'Session key missing',
        'received_keys' => array_keys($dados),
        'timestamp' => date('Y-m-d H:i:s')
    ]);
    exit;
}

if (empty($dados['session'])) {
    error_log("ERROR: Session ID empty");
    http_response_code(400);
    echo json_encode([
        'success' => false, 
        'error' => 'Session ID cannot be empty',
        'timestamp' => date('Y-m-d H:i:s')
    ]);
    exit;
}

$session_id = $dados['session'];
error_log("Session ID validated: " . $session_id);

// Salvar dados do formulário
$dados_formulario = $dados['dados'] ?? [];
$parametros_file = "temp/parametros_{$session_id}.json";
$saved = file_put_contents($parametros_file, json_encode($dados_formulario));

if ($saved === false) {
    error_log("ERROR: Failed to save parameters file");
    http_response_code(500);
    echo json_encode([
        'success' => false, 
        'error' => 'Failed to save parameters',
        'timestamp' => date('Y-m-d H:i:s')
    ]);
    exit;
}

error_log("Parameters saved to: " . $parametros_file);

// Executar RPA usando wrapper
$command = "/opt/imediatoseguros-rpa/executar_rpa_wrapper.sh teste_api_simples.py --session $session_id --modo-silencioso";
error_log("Executing command with wrapper: " . $command);

$pid = shell_exec("nohup bash -c '$command' > /dev/null 2>&1 & echo $!");
$pid = trim($pid);

error_log("RPA started with PID: " . $pid);

// Resposta de sucesso
$response = [
    'success' => true,
    'session_id' => $session_id,
    'pid' => $pid,
    'timestamp' => date('Y-m-d H:i:s'),
    'parameters_saved' => true,
    'wrapper_used' => true
];

error_log("API response: " . json_encode($response));
echo json_encode($response);
?>














