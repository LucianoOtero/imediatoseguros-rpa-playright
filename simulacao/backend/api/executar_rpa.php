<?php
header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: http://localhost:3000');
header('Access-Control-Allow-Methods: POST, GET, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type, X-Requested-With');
header('Access-Control-Allow-Credentials: true');

// Tratar preflight OPTIONS
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit();
}

// Verificar método
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['success' => false, 'message' => 'Método não permitido']);
    exit();
}

// Obter dados JSON
$input = file_get_contents('php://input');
$data = json_decode($input, true);

if (!$data) {
    http_response_code(400);
    echo json_encode(['success' => false, 'message' => 'Dados JSON inválidos']);
    exit();
}

// Validar dados obrigatórios
$required_fields = ['session', 'dados'];
foreach ($required_fields as $field) {
    if (!isset($data[$field])) {
        http_response_code(400);
        echo json_encode(['success' => false, 'message' => "Campo obrigatório: $field"]);
        exit();
    }
}

$session_id = $data['session'];
$dados = $data['dados'];

// Criar arquivo de parâmetros temporário
$parametros_file = "temp/parametros_{$session_id}.json";
$parametros_dir = dirname($parametros_file);

if (!is_dir($parametros_dir)) {
    mkdir($parametros_dir, 0755, true);
}

// Mapear dados do formulário para parâmetros do RPA
$parametros = [
    'placa' => $dados['placa'] ?? 'EYQ4J41',
    'marca' => $dados['marca'] ?? 'TOYOTA',
    'modelo' => $dados['modelo'] ?? 'COROLLA',
    'ano' => intval($dados['ano'] ?? 2009),
    'combustivel' => 'flex',
    'zero_km' => false,
    'kit_gas' => false,
    'blindado' => false,
    'financiado' => false,
    'nome' => $dados['nome'] ?? 'João Silva',
    'cpf' => $dados['cpf'] ?? '123.456.789-00',
    'email' => $dados['email'] ?? 'joao@email.com',
    'celular' => $dados['celular'] ?? '(11) 99999-9999',
    'cep' => '01234-567',
    'endereco' => 'Rua das Flores, 123',
    'cidade' => 'São Paulo',
    'estado' => 'SP',
    'garagem_residencia' => true,
    'garagem_trabalho' => false,
    'garagem_outros' => false,
    'uso_veiculo' => 'particular'
];

// Salvar arquivo de parâmetros
file_put_contents($parametros_file, json_encode($parametros, JSON_PRETTY_PRINT));

// Executar RPA em background
$rpa_script = '../rpa/executar_rpa_imediato_playwright.py';
$command = "python \"$rpa_script\" --config \"$parametros_file\" --session \"$session_id\" --progress-tracker json --modo-silencioso > logs/rpa_{$session_id}.log 2>&1 &";

// Executar comando
$pid = shell_exec($command);
if ($pid === null) {
    $pid = '';
}

// Resposta de sucesso
echo json_encode([
    'success' => true,
    'session_id' => $session_id,
    'pid' => trim($pid),
    'message' => 'RPA iniciado com sucesso'
]);
?>
