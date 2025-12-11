<?php
// arquivo: /opt/imediatoseguros-rpa-v4/public/api/rpa/start.php
// Projeto: Integração Webhooks RPA V6.9.0
// Data: 2025-10-09
// Descrição: Endpoint modificado com PH3A, webhooks e RPA

header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

// Handle preflight requests
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit;
}

// Only allow POST requests
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['status' => 'error', 'message' => 'Method not allowed']);
    exit;
}

// Get JSON input
$input = file_get_contents('php://input');
$data = json_decode($input, true);

if (!$data) {
    http_response_code(400);
    echo json_encode(['status' => 'error', 'message' => 'Invalid JSON']);
    exit;
}

// Validate required fields
$required_fields = ['cpf', 'nome', 'placa', 'cep', 'email', 'telefone'];
foreach ($required_fields as $field) {
    if (empty($data[$field])) {
        http_response_code(400);
        echo json_encode(['status' => 'error', 'message' => "Campo obrigatório: $field"]);
        exit;
    }
}

// Generate session ID
$session_id = 'rpa_v6.9.0_' . date('Ymd_His') . '_' . substr(md5(uniqid()), 0, 8);

// ========================================
// ETAPA 1: CONSULTAR API PH3A (SE NECESSÁRIO)
// ========================================
$start_time = microtime(true);
echo "🔍 ETAPA 1: VERIFICANDO CAMPOS PH3A\n";
echo "====================================\n";

// Verificar se campos PH3A estão em branco
$campos_ph3a_vazios = [];
if (empty($data['sexo'])) $campos_ph3a_vazios[] = 'sexo';
if (empty($data['data_nascimento'])) $campos_ph3a_vazios[] = 'data_nascimento';
if (empty($data['estado_civil'])) $campos_ph3a_vazios[] = 'estado_civil';

$ph3a_data = [];
$ph3a_result = null;

if (!empty($campos_ph3a_vazios) && !empty($data['cpf'])) {
    echo "📞 Consultando API PH3A para campos: " . implode(', ', $campos_ph3a_vazios) . "\n";
    
    // Function to call PH3A API
    function callPH3AApi($cpf) {
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, 'https://mdmidia.com.br/cpf-validate.php');
        curl_setopt($ch, CURLOPT_POST, true);
        curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode(['cpf' => $cpf]));
        curl_setopt($ch, CURLOPT_HTTPHEADER, [
            'Content-Type: application/json',
            'User-Agent: RPA-API-v6.9.0'
        ]);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_TIMEOUT, 15);
        curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 5);
        curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
        
        $response = curl_exec($ch);
        $http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        $error = curl_error($ch);
        curl_close($ch);
        
        return [
            'success' => $http_code >= 200 && $http_code < 300,
            'http_code' => $http_code,
            'response' => $response,
            'error' => $error
        ];
    }
    
    $ph3a_result = callPH3AApi($data['cpf']);
    
    if ($ph3a_result['success']) {
        $ph3a_json = json_decode($ph3a_result['response'], true);
        
        if ($ph3a_json && $ph3a_json['codigo'] == 1 && isset($ph3a_json['data'])) {
            $ph3a_data = $ph3a_json['data'];
            
            // Mapear sexo
            if (empty($data['sexo']) && isset($ph3a_data['sexo'])) {
                $data['sexo'] = ($ph3a_data['sexo'] == 1) ? 'Masculino' : 'Feminino';
                echo "✅ SEXO preenchido: " . $data['sexo'] . "\n";
            }
            
            // Mapear estado civil
            if (empty($data['estado_civil']) && isset($ph3a_data['estado_civil'])) {
                $estado_civil_map = [0 => 'Solteiro', 1 => 'Casado', 2 => 'Divorciado', 3 => 'Viúvo'];
                $data['estado_civil'] = $estado_civil_map[$ph3a_data['estado_civil']] ?? '';
                if ($data['estado_civil']) {
                    echo "✅ ESTADO-CIVIL preenchido: " . $data['estado_civil'] . "\n";
                }
            }
            
            // Mapear data de nascimento (ISO para DD/MM/YYYY)
            if (empty($data['data_nascimento']) && isset($ph3a_data['data_nascimento'])) {
                try {
                    $date = new DateTime($ph3a_data['data_nascimento']);
                    $data['data_nascimento'] = $date->format('d/m/Y');
                    echo "✅ DATA-DE-NASCIMENTO preenchida: " . $data['data_nascimento'] . "\n";
                } catch (Exception $e) {
                    $data['data_nascimento'] = $ph3a_data['data_nascimento'];
                    echo "✅ DATA-DE-NASCIMENTO preenchida (formato original): " . $data['data_nascimento'] . "\n";
                }
            }
        } else {
            echo "⚠️ PH3A: CPF válido mas não encontrado na base\n";
        }
    } else {
        echo "❌ PH3A: Falha na consulta - " . $ph3a_result['error'] . "\n";
    }
} else {
    echo "✅ PH3A: Campos já preenchidos ou CPF vazio\n";
}

$ph3a_time = microtime(true) - $start_time;
echo "⏱️ Tempo PH3A: " . round($ph3a_time, 3) . "s\n";

// ========================================
// ETAPA 2: CHAMAR WEBHOOKS PRIMEIRO
// ========================================
$webhooks_start = microtime(true);
echo "\n🚀 ETAPA 2: CHAMANDO WEBHOOKS PRIMEIRO\n";
echo "========================================\n";

// Prepare webhook data for both webhooks
$webhook_data = [
    'data' => [
        'NOME' => $data['nome'],
        'DDD-CELULAR' => $data['ddd_celular'] ?? '11',
        'CELULAR' => $data['celular'] ?? substr($data['telefone'], 2),
        'Email' => $data['email'],
        'CEP' => $data['cep'],
        'CPF' => $data['cpf'],
        'MARCA' => $data['marca'] ?? '',
        'PLACA' => $data['placa'],
        'VEICULO' => $data['marca'] ?? '',
        'ANO' => $data['ano'] ?? '',
        'GCLID_FLD' => $data['gclid'] ?? '',
        'SEXO' => $data['sexo'] ?? '',
        'DATA-DE-NASCIMENTO' => $data['data_nascimento'] ?? '',
        'ESTADO-CIVIL' => $data['estado_civil'] ?? '',
        'produto' => $data['produto'] ?? 'seguro-auto',
        'landing_url' => $data['landing_url'] ?? '',
        'utm_source' => $data['utm_source'] ?? '',
        'utm_campaign' => $data['utm_campaign'] ?? ''
    ],
    'd' => date('c'),
    'name' => 'Formulário de Cotação RPA'
];

// Function to call webhook
function callWebhook($url, $data) {
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
    curl_setopt($ch, CURLOPT_HTTPHEADER, [
        'Content-Type: application/json',
        'User-Agent: RPA-API-v6.9.0'
    ]);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_TIMEOUT, 30);
    curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 10);
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
    
    $response = curl_exec($ch);
    $http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    $error = curl_error($ch);
    curl_close($ch);
    
    return [
        'success' => $http_code >= 200 && $http_code < 300,
        'http_code' => $http_code,
        'response' => $response,
        'error' => $error
    ];
}

// Call both webhooks FIRST
$webhook_results = [];
$webhook_success_count = 0;

echo "📞 Chamando add_travelangels.php (EspoCRM)...\n";
$travelangels_result = callWebhook('https://mdmidia.com.br/add_travelangels.php', $webhook_data);
$webhook_results['travelangels'] = $travelangels_result;

if ($travelangels_result['success']) {
    $webhook_success_count++;
    echo "✅ EspoCRM: Lead criado com sucesso\n";
} else {
    echo "❌ EspoCRM: Falha - " . $travelangels_result['error'] . "\n";
}

echo "📱 Chamando add_webflow_octa.php (Octadesk)...\n";
$octa_result = callWebhook('https://mdmidia.com.br/add_webflow_octa.php', $webhook_data);
$webhook_results['octadesk'] = $octa_result;

if ($octa_result['success']) {
    $webhook_success_count++;
    echo "✅ Octadesk: Mensagem WhatsApp enviada\n";
} else {
    echo "❌ Octadesk: Falha - " . $octa_result['error'] . "\n";
}

echo "📊 Resultado dos Webhooks: $webhook_success_count/2 sucessos\n";

$webhooks_time = microtime(true) - $webhooks_start;
echo "⏱️ Tempo Webhooks: " . round($webhooks_time, 3) . "s\n";

// ========================================
// ETAPA 3: INICIAR RPA APÓS WEBHOOKS
// ========================================
$rpa_start = microtime(true);
echo "\n🤖 ETAPA 3: INICIANDO RPA APÓS WEBHOOKS\n";
echo "========================================\n";

// Start RPA process
$rpa_command = "cd /opt/imediatoseguros-rpa && source venv/bin/activate && python executar_rpa_imediato_playwright.py '" . json_encode($data) . "' > /dev/null 2>&1 & echo $!";
$rpa_pid = shell_exec($rpa_command);
$rpa_pid = trim($rpa_pid);

if ($rpa_pid) {
    echo "✅ RPA iniciado com PID: $rpa_pid\n";
} else {
    echo "❌ Falha ao iniciar RPA\n";
}

$rpa_time = microtime(true) - $rpa_start;
echo "⏱️ Tempo RPA: " . round($rpa_time, 3) . "s\n";

$total_time = microtime(true) - $start_time;
echo "⏱️ Tempo Total: " . round($total_time, 3) . "s\n";

// Log webhook results (mask sensitive data)
$masked_cpf = substr($data['cpf'], -4);
$log_data = [
    'session_id' => $session_id,
    'timestamp' => date('c'),
    'performance' => [
        'ph3a_time' => round($ph3a_time, 3),
        'webhooks_time' => round($webhooks_time, 3),
        'rpa_time' => round($rpa_time, 3),
        'total_time' => round($total_time, 3)
    ],
    'ph3a_result' => $ph3a_result ?? null,
    'ph3a_data' => $ph3a_data ?? null,
    'campos_ph3a_vazios' => $campos_ph3a_vazios ?? [],
    'webhook_results' => $webhook_results,
    'webhook_success_count' => $webhook_success_count,
    'input_data' => [
        'cpf' => '***' . $masked_cpf,
        'nome' => $data['nome'],
        'placa' => $data['placa'],
        'cep' => $data['cep'],
        'email' => $data['email'],
        'gclid' => $data['gclid'] ?? ''
    ]
];

$log_file = "/opt/imediatoseguros-rpa/logs/webhook_calls_" . date('Y-m-d') . ".log";
if (!is_dir(dirname($log_file))) {
    mkdir(dirname($log_file), 0755, true);
}
file_put_contents($log_file, json_encode($log_data) . "\n", FILE_APPEND | LOCK_EX);

// Save session info
$session_info = [
    'session_id' => $session_id,
    'rpa_pid' => $rpa_pid,
    'status' => 'started',
    'started_at' => date('c'),
    'webhook_results' => $webhook_results,
    'webhook_success_count' => $webhook_success_count,
    'execution_order' => 'ph3a_then_webhooks_then_rpa'
];

$session_file = "/opt/imediatoseguros-rpa/sessions/$session_id/status.json";
if (!is_dir(dirname($session_file))) {
    mkdir(dirname($session_file), 0755, true);
}
file_put_contents($session_file, json_encode($session_info, JSON_PRETTY_PRINT));

// Return response
$response = [
    'success' => true,
    'session_id' => $session_id,
    'message' => 'PH3A consultado, webhooks executados e RPA iniciado com sucesso',
    'performance' => [
        'ph3a_time' => round($ph3a_time, 3),
        'webhooks_time' => round($webhooks_time, 3),
        'rpa_time' => round($rpa_time, 3),
        'total_time' => round($total_time, 3)
    ],
    'ph3a_consulted' => !empty($campos_ph3a_vazios) && !empty($data['cpf']),
    'ph3a_fields_filled' => array_diff(['sexo', 'data_nascimento', 'estado_civil'], $campos_ph3a_vazios ?? []),
    'webhook_results' => $webhook_results,
    'webhook_success_count' => $webhook_success_count,
    'rpa_pid' => $rpa_pid,
    'execution_order' => 'ph3a_then_webhooks_then_rpa',
    'timestamp' => date('c')
];

http_response_code(200);
echo json_encode($response, JSON_PRETTY_PRINT);
?>







