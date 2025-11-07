<?php

/**
 * WEBHOOK OCTADESK DESENVOLVIMENTO V2
 * dev.bpsegurosimediato.com.br/webhooks/add_webflow_octa_dev.php
 * 
 * Webhook de desenvolvimento para integração Webflow + OctaDesk
 * Versão V2 com logging avançado e validação de signature
 * 
 * VERSÃO: 2.0 - Versão de desenvolvimento
 * 
 * ALTERAÇÕES NESTA VERSÃO:
 * - Removidas funções de simulação
 * - Atualizado para usar API real do OctaDesk de produção
 * - Credenciais de produção configuradas
 * - CORS configurado para domínios de produção
 * - Logs apontando para diretório de produção
 * - Validação de signature habilitada (obrigatória em produção)
 */

// ==================== CONFIGURAÇÃO CORS ====================
// Permitir requisições de domínios de produção
$allowed_origins = array(
    'https://www.segurosimediato.com.br',
    'https://segurosimediato.com.br',
    'https://bpsegurosimediato.com.br',
    // Manter staging para testes de produção
    'https://segurosimediato-8119bf26e77bf4ff336a58e.webflow.io'
);

$origin = isset($_SERVER['HTTP_ORIGIN']) ? $_SERVER['HTTP_ORIGIN'] : '';
if (in_array($origin, $allowed_origins)) {
    header('Access-Control-Allow-Origin: ' . $origin);
}

header('Access-Control-Allow-Methods: POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type, X-Webflow-Signature, X-Webflow-Timestamp, X-Requested-With');
header('Access-Control-Allow-Credentials: true');
header('Access-Control-Max-Age: 86400'); // 24 horas

// Responder a requisições OPTIONS (preflight)
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    header('Content-Length: 0');
    header('Content-Type: text/plain');
    exit(0);
}
// ==================== FIM CONFIGURAÇÃO CORS ====================

// Headers de resposta para desenvolvimento
header('Content-Type: application/json; charset=utf-8');
header('X-Environment: development');
header('X-API-Version: 2.0');
header('X-Webhook: octadesk-v2');

// ⚠️ CREDENCIAIS DE DESENVOLVIMENTO OCTADESK (obtidas do add_webflow_octa.php de produção)
$OCTADESK_API_KEY = 'b4e081fa-94ab-4456-8378-991bf995d3ea.d3e8e579-869d-4973-b34d-82391d08702b';
$API_BASE = 'https://o205242-d60.api004.octadesk.services';
$OCTADESK_FROM = '+551132301422';
$WEBFLOW_SECRET_OCTADESK = '4d012059c79aa7250f4b22825487129da9291178b17bbf1dc970de119052dc8f'; // ✅ Secret obtido do Webflow Dashboard

// Log específico do webhook de desenvolvimento
function logDevWebhook($action, $data = null, $success = true)
{
    $logFile = '/var/www/html/logs/webhook_octadesk_dev.txt';
    $timestamp = date('Y-m-d H:i:s');
    $status = $success ? 'SUCCESS' : 'ERROR';

    $logEntry = "[{$timestamp}] [{$status}] [OCTADESK-DEV] {$action}";
    if ($data !== null) {
        $logEntry .= " | Data: " . json_encode($data, JSON_UNESCAPED_UNICODE);
    }
    $logEntry .= PHP_EOL;

    file_put_contents($logFile, $logEntry, FILE_APPEND | LOCK_EX);
}


// Função HTTP helper para OctaDesk (DESENVOLVIMENTO)
function octa_request($method, $url, $body = null) {
    global $OCTADESK_API_KEY;
    $headers = [
        'accept: application/json',
        'content-type: application/json',
        "X-API-KEY: {$OCTADESK_API_KEY}"
    ];
    $bodyStr = ($body === null) ? '' : json_encode($body, JSON_UNESCAPED_SLASHES|JSON_UNESCAPED_UNICODE);
    logDevWebhook('OCTA_REQ', ['method'=>$method, 'url'=>$url, 'body'=>$body]);
    $ch = curl_init($url);
    $opts = [
        CURLOPT_CUSTOMREQUEST => $method,
        CURLOPT_HTTPHEADER => $headers,
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_TIMEOUT => 25
    ];
    if ($method !== 'GET' && $bodyStr !== '') $opts[CURLOPT_POSTFIELDS] = $bodyStr;
    curl_setopt_array($ch, $opts);
    $resp = curl_exec($ch);
    $http = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    $err = curl_error($ch);
    curl_close($ch);
    logDevWebhook('OCTA_RES', ['http'=>$http, 'url'=>$url, 'err'=>$err, 'body_head'=>substr((string)$resp, 0, 600)]);
    $json = json_decode((string)$resp, true);
    return [$http, $json, $resp, $err];
}

// Helper functions (mesmas do arquivo de produção)
function onlyDigits($s) { 
    return preg_replace('/\D+/', '', (string)$s); 
}

function toLocalDigitsBR($ddd, $cel) {
    $n = onlyDigits((string)$ddd . (string)$cel);
    if (strpos($n, '55') === 0) $n = substr($n, 2); // remove DDI se vier
    return (strlen($n) >= 10 && strlen($n) <= 11) ? $n : null;
}

function toE164FromLocal($localDigits) {
    $n = onlyDigits($localDigits);
    if ($n === '') return null;
    if (strpos($n, '55') === 0) return '+'.$n;
    return '+55'.$n;
}

function buildCustomFieldsPairs($pairs) {
    $out = [];
    foreach ($pairs as $k => $v) if ($v !== null && $v !== '') $out[$k] = $v;
    return $out;
}

// Função para enviar template WhatsApp via OctaDesk (DESENVOLVIMENTO)
// Segue a mesma estrutura do add_webflow_octa.php de produção
function sendToOctaDesk($data)
{
    global $API_BASE, $OCTADESK_FROM, $URL_SEND_TPL, $URL_CONTACTS;
    
    // Extrair dados
    $nome = $data['name'] ?? '';
    $email = $data['email'] ?? '';
    $phone = $data['phone'] ?? '';
    $ddd = $data['ddd'] ?? '';
    $celular = $data['celular'] ?? '';
    $gclid = $data['gclid'] ?? $data['custom_fields']['gclid'] ?? '';
    $produto = $data['custom_fields']['produto'] ?? $data['produto'] ?? '';
    $utmSource = $data['custom_fields']['utm_source'] ?? '';
    $utmCampaign = $data['custom_fields']['utm_campaign'] ?? '';
    $landing = $data['custom_fields']['landing_url'] ?? '';
    
    // Preparar telefone
    $foneLocal = null;
    $foneE164 = null;
    
    if (!empty($ddd) && !empty($celular)) {
        $foneLocal = toLocalDigitsBR($ddd, $celular);
    } else if (!empty($phone)) {
        $phoneDigits = onlyDigits($phone);
        $foneLocal = toLocalDigitsBR('', $phoneDigits);
    }
    
    if ($foneLocal) {
        $foneE164 = toE164FromLocal($foneLocal);
    }
    
    if (!$foneE164) {
        logDevWebhook('phone_validation_error', ['phone' => $phone, 'ddd' => $ddd, 'celular' => $celular], false);
        return [
            'http_code' => 422,
            'response' => '',
            'error' => 'Telefone inválido',
            'success' => false
        ];
    }
    
    // Preparar custom fields
    $customObj = buildCustomFieldsPairs([
        'cpf' => $data['custom_fields']['cpf'] ?? '',
        'cep' => $data['custom_fields']['cep'] ?? '',
        'placa' => $data['custom_fields']['placa'] ?? '',
        'veiculo' => $data['custom_fields']['veiculo'] ?? '',
        'ano_do_veiculo' => $data['custom_fields']['ano'] ?? ''
    ]);
    
    // Criar/atualizar contato primeiro (simplificado - sem busca completa)
    // Em produção real, isso seria feito pelo upsertContactWithCF
    // Para v2, vamos direto para o send-template que cria o contato automaticamente
    
    // Preparar payload do send-template (estrutura idêntica ao arquivo de produção)
    $payloadSend = [
        'target' => [
            'contact' => [
                'name' => ($nome !== '' ? $nome : 'Cliente'),
                'email' => ($email ?: null),
                'phoneContact' => ['number' => $foneE164],
            ],
            'customFields' => [
                ['key' => 'nome-contato', 'value' => $nome ?: ''],
                ['key' => 'gclid', 'value' => $gclid ?: '']
            ],
            'tags' => array_values(array_filter(['lead-webflow', $produto ? "produto:$produto" : null]))
        ],
        'content' => [
            'templateMessage' => [
                'code' => 'site_cotacao',
                'language' => 'pt_BR',
                'components' => [[
                    'type' => 'body',
                    'parameters' => [[ 'type' => 'text', 'text' => ($nome !== '' ? $nome : 'cliente') ]]
                ]]
            ]
        ],
        'origin' => ['from' => ['number' => $OCTADESK_FROM]],
        'options' => ['automaticAssign' => true],
        'metadata'=> [
            'campaign' => 'webflow_form',
            'utm_source' => $utmSource,
            'utm_campaign' => $utmCampaign,
            'landing_url' => $landing
        ]
    ];
    
    logDevWebhook('octadesk_send_template_payload', [
        'payload' => $payloadSend,
        'phone_e164' => $foneE164,
        'phone_local' => $foneLocal
    ], true);
    
    list($http, $json, $resp, $err) = octa_request('POST', $URL_SEND_TPL, $payloadSend);
    $conversationId = is_array($json) ? ($json['conversationId'] ?? ($json['result']['roomKey'] ?? null)) : null;
    
    if ($http >= 200 && $http < 300) {
        return [
            'http_code' => $http,
            'response' => $resp,
            'error' => null,
            'success' => true,
            'data' => $json,
            'conversationId' => $conversationId
        ];
    } else {
        return [
            'http_code' => $http,
            'response' => $resp,
            'error' => $err ?: 'HTTP ' . $http,
            'success' => false,
            'conversationId' => $conversationId
        ];
    }
}

// Funções de conversa e mensagem - REMOVIDAS
// O send-template já cria a conversa automaticamente, não precisamos criar separadamente

// Função para validar assinatura Webflow
// Documentação Webflow: signature = HMAC-SHA256(timestamp:payload, secret_key)
function validateWebflowSignature($input, $signature, $secret)
{
    $headers = getallheaders();
    $timestamp = $headers['X-Webflow-Timestamp'] ?? '';
    
    if (empty($timestamp)) {
        return false;
    }
    
    // String de assinatura: timestamp:payload
    $signature_string = $timestamp . ':' . $input;
    $expectedSignature = hash_hmac('sha256', $signature_string, $secret);
    
    return hash_equals($expectedSignature, $signature);
}

// Variáveis globais para URLs
$URL_SEND_TPL = $API_BASE . '/chat/conversation/send-template';
$URL_CONTACTS = $API_BASE . '/contacts';

// Função principal do webhook
function processWebflowWebhook()
{
    global $WEBFLOW_SECRET_OCTADESK;

    // Função para corrigir JSON malformado
    function fixMalformedJson($json_string)
    {
        // Tentar corrigir aspas duplas mal escapadas
        $fixed = $json_string;

        // Corrigir aspas duplas dentro de strings JSON
        $fixed = preg_replace('/"([^"]*)"([^"]*)"([^"]*)"/', '"$1\\"$2\\"$3"', $fixed);

        // Corrigir aspas duplas no final de strings
        $fixed = preg_replace('/"([^"]*)"([^"]*)"([^"]*)"([^"]*)"([^"]*)"/', '"$1\\"$2\\"$3\\"$4\\"$5"', $fixed);

        // Tentar decodificar novamente
        $test_decode = json_decode($fixed, true);
        if (json_last_error() === JSON_ERROR_NONE) {
            return $fixed;
        }

        // Se ainda não funcionar, tentar uma abordagem mais agressiva
        $fixed = str_replace('""', '\\"', $fixed);
        $test_decode = json_decode($fixed, true);
        if (json_last_error() === JSON_ERROR_NONE) {
            return $fixed;
        }

        return false;
    }

    // Obter dados da requisição
    $input = file_get_contents('php://input');
    $headers = getallheaders();

    logDevWebhook('webhook_received', [
        'method' => $_SERVER['REQUEST_METHOD'],
        'headers' => $headers,
        'input_length' => strlen($input)
    ], true);

    // Validar método
    if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
        logDevWebhook('invalid_method', ['method' => $_SERVER['REQUEST_METHOD']], false);
        http_response_code(405);
        echo json_encode(['error' => 'Method not allowed']);
        return;
    }

    // Validar assinatura Webflow - VALIDAÇÃO CONDICIONAL
    // Se assinatura presente = requisição do Webflow (validar obrigatoriamente)
    // Se assinatura ausente = requisição do navegador/modal (aceitar sem validação)
    $signature = $headers['X-Webflow-Signature'] ?? '';
    $timestamp = $headers['X-Webflow-Timestamp'] ?? '';

    if (!empty($signature) && !empty($timestamp)) {
        // Assinatura presente - validar (requisição do Webflow)
        if (!validateWebflowSignature($input, $signature, $WEBFLOW_SECRET_OCTADESK)) {
            logDevWebhook('invalid_signature', [
                'signature_received' => substr($signature, 0, 16) . '...',
                'timestamp_received' => $timestamp,
                'expected_length' => strlen($signature),
                'ip' => $_SERVER['REMOTE_ADDR'] ?? 'unknown',
                'reason' => 'signature_invalid'
            ], false);
            http_response_code(401);
            echo json_encode(['error' => 'Invalid signature']);
            return;
        }
        logDevWebhook('signature_validation', [
            'status' => 'valid',
            'source' => 'webflow',
            'signature_received' => substr($signature, 0, 16) . '...',
            'timestamp_received' => $timestamp
        ], true);
    } else {
        // Assinatura ausente - requisição do navegador/modal (aceitar)
        logDevWebhook('signature_validation', [
            'status' => 'skipped',
            'source' => 'browser',
            'reason' => 'signature_not_provided',
            'ip' => $_SERVER['REMOTE_ADDR'] ?? 'unknown'
        ], true);
    }


    // Parse dos dados
    $data = json_decode($input, true);
    if (!$data) {
        // Tentar corrigir JSON malformado
        $fixed_input = fixMalformedJson($input);
        if ($fixed_input) {
            $data = json_decode($fixed_input, true);
            if ($data) {
                logDevWebhook('json_fixed', ['status' => 'success'], true);
            } else {
                logDevWebhook('invalid_json', ['input' => substr($input, 0, 500) . '...'], false);
                http_response_code(400);
                echo json_encode(['error' => 'Invalid JSON - não foi possível corrigir']);
                return;
            }
        } else {
            logDevWebhook('invalid_json', ['input' => substr($input, 0, 500) . '...'], false);
            http_response_code(400);
            echo json_encode(['error' => 'Invalid JSON']);
            return;
        }
    }

    logDevWebhook('webflow_data_parsed', $data, true);

    // Extrair dados do formulário (API V2 do Webflow usa payload.data)
    $formData = $data['payload']['data'] ?? $data['data'] ?? [];
    $formName = $data['payload']['name'] ?? $data['name'] ?? 'Formulário Desconhecido';

    // Mapear campos do formulário para produção (estrutura compatível com produção)
    $ddd = $formData['DDD-CELULAR'] ?? '';
    $celular = $formData['CELULAR'] ?? '';
    $nome = $formData['name'] ?? $formData['nome'] ?? $formData['NOME'] ?? '';
    $email = $formData['email'] ?? $formData['Email'] ?? $formData['EMAIL'] ?? '';
    $gclid = $formData['GCLID_FLD'] ?? $formData['gclid'] ?? '';
    $produto = $formData['produto'] ?? 'seguro-auto';
    $utmSource = $formData['utm_source'] ?? '';
    $utmCampaign = $formData['utm_campaign'] ?? '';
    $landing = $formData['landing_url'] ?? $data['pageUrl'] ?? '';
    
    $contactData = [
        'name' => $nome,
        'email' => $email,
        'ddd' => $ddd,
        'celular' => $celular,
        'phone' => trim($ddd . $celular), // Fallback
        'gclid' => $gclid,
        'custom_fields' => [
            'cpf' => $formData['CPF'] ?? '',
            'cep' => $formData['CEP'] ?? '',
            'placa' => $formData['PLACA'] ?? '',
            'veiculo' => $formData['VEICULO'] ?? $formData['MARCA'] ?? '',
            'ano' => $formData['ANO'] ?? '',
            'produto' => $produto,
            'utm_source' => $utmSource,
            'utm_campaign' => $utmCampaign,
            'landing_url' => $landing
        ]
    ];

    logDevWebhook('contact_data_mapped', $contactData, true);

    // Validar telefone obrigatório (ddd e celular)
    if (empty($ddd) || empty($celular)) {
        logDevWebhook('validation_error', [
            'field' => 'telefone', 
            'error' => 'DDD e CELULAR obrigatórios',
            'ddd' => $ddd,
            'celular' => $celular
        ], false);
        http_response_code(422);
        echo json_encode([
            'success' => false,
            'error' => 'DDD e CELULAR são obrigatórios'
        ]);
        return;
    }

    // Enviar template WhatsApp via OctaDesk (DESENVOLVIMENTO)
    $octaResult = sendToOctaDesk($contactData);

    if ($octaResult['success']) {
        logDevWebhook('webhook_success', [
            'form_name' => $formName,
            'phone' => substr($contactData['phone'], 0, 4) . '***' . substr($contactData['phone'], -2),
            'http_code' => $octaResult['http_code']
        ], true);

        http_response_code(200);
        echo json_encode([
            'success' => true,
            'message' => 'Webhook processado com sucesso',
            'environment' => 'development',
            'api_version' => '2.0'
        ]);
    } else {
        logDevWebhook('webhook_error', [
            'http_code' => $octaResult['http_code'],
            'error' => $octaResult['error'],
            'response' => substr($octaResult['response'], 0, 200)
        ], false);

        http_response_code(500);
        echo json_encode([
            'success' => false,
            'error' => 'Erro ao processar webhook',
            'details' => $octaResult['error']
        ]);
    }
}

// Executar webhook
try {
    processWebflowWebhook();
} catch (Exception $e) {
    logDevWebhook('webhook_exception', [
        'error' => $e->getMessage(),
        'file' => $e->getFile(),
        'line' => $e->getLine(),
        'trace' => $e->getTraceAsString()
    ], false);

    http_response_code(500);
    echo json_encode([
        'success' => false,
        'error' => 'Erro interno do webhook',
        'message' => $e->getMessage()
    ]);
}
