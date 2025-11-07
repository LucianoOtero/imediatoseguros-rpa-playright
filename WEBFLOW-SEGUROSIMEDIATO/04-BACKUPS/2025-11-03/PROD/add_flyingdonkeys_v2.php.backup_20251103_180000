<?php

/**
 * WEBHOOK FLYINGDONKEYS - PRODUÇÃO V2
 * bpsegurosimediato.com.br/webhooks/add_flyingdonkeys_v2.php
 * 
 * Versão de produção com API V2, logging avançado e validação de signature
 * Baseado no add_travelangels_dev.php mas apontando para produção FlyingDonkeys
 * 
 * VERSÃO: 2.1 - Integração de Notificação Email Administradores
 * 
 * ALTERAÇÕES VERSÃO 2.1:
 * - ✅ Integração de notificação por email para administradores via Amazon SES
 * - ✅ Identificação automática do momento do modal (INITIAL vs UPDATE)
 * - ✅ Logs diferenciados com emojis e cores (📞🔵 para INITIAL, ✅🟢 para UPDATE)
 * - ✅ Envio de email após criação/atualização bem-sucedida do lead
 * - ✅ Tratamento de erros sem bloquear fluxo principal
 * 
 * ALTERAÇÕES VERSÃO 2.0:
 * - Removidas todas as chamadas ao endpoint travelangels.com.br
 * - Atualizado para usar endpoints de produção do FlyingDonkeys
 * - Credenciais de produção do FlyingDonkeys configuradas
 * - CORS configurado para domínios de produção
 * - Logs apontando para diretório de produção
 * - Removidas funções de simulação (produção sempre usa CRM real)
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

// Configurações específicas do webhook de produção
// ✅ SECRET DO WEBFLOW DE PRODUÇÃO (obtido do Webflow Dashboard)
$WEBFLOW_SECRET_TRAVELANGELS = 'ce051cb1d819faac5837f4e47a7fdd8cf2a8b248a2b3ecdb9ab358cfb9ed7990';
$DEBUG_LOG_FILE = '/var/www/html/logs/flyingdonkeys_prod.txt';
$LOG_PREFIX = '[PROD-FLYINGDONKEYS] ';

// Headers de resposta para produção
header('Content-Type: application/json; charset=utf-8');
header('X-Environment: production');
header('X-API-Version: 2.0');
header('X-Webhook: flyingdonkeys-v2');

// Variável global para armazenar request_id
$GLOBAL_REQUEST_ID = null;

// Função para log de produção
function logProdWebhook($event, $data, $success = true)
{
    global $DEBUG_LOG_FILE, $LOG_PREFIX, $GLOBAL_REQUEST_ID;

    // Gerar request_id apenas uma vez por requisição
    if ($GLOBAL_REQUEST_ID === null) {
        $GLOBAL_REQUEST_ID = uniqid('prod_fd_', true);
    }

    $log_data = [
        'timestamp' => date('Y-m-d H:i:s'),
        'environment' => 'production',
        'webhook' => 'flyingdonkeys-v2',
        'event' => $event,
        'success' => $success,
        'data' => $data,
        'request_id' => $GLOBAL_REQUEST_ID,
        'memory_usage' => memory_get_usage(true),
        'execution_time' => microtime(true) - $_SERVER['REQUEST_TIME_FLOAT']
    ];

    $log_entry = $LOG_PREFIX . json_encode($log_data, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT) . PHP_EOL;
    file_put_contents($DEBUG_LOG_FILE, $log_entry, FILE_APPEND | LOCK_EX);
}

// Alias para manter compatibilidade durante transição
function logDevWebhook($event, $data, $success = true) {
    return logProdWebhook($event, $data, $success);
}

// Função para validar signature do Webflow (API V2) - PRODUÇÃO
function validateWebflowSignatureProd($payload, $signature, $timestamp, $secret)
{
    // Em produção, signature é obrigatória
    if (empty($signature) || empty($timestamp)) {
        logProdWebhook('signature_validation', ['status' => 'missing', 'reason' => 'signature_or_timestamp_empty'], false);
        return false;
    }

    // Documentação Webflow: signature = HMAC-SHA256(timestamp:payload, secret_key)
    $signature_string = $timestamp . ':' . $payload;
    $expected_signature = hash_hmac('sha256', $signature_string, $secret);
    $is_valid = hash_equals($expected_signature, $signature);

    if (!$is_valid) {
        logProdWebhook('signature_validation', [
            'status' => 'failed',
            'expected' => substr($expected_signature, 0, 16) . '...',
            'received' => substr($signature, 0, 16) . '...',
            'payload_length' => strlen($payload)
        ], false);
    }

    return $is_valid;
}

// Alias para compatibilidade
function validateWebflowSignatureDev($payload, $signature, $timestamp, $secret) {
    return validateWebflowSignatureProd($payload, $signature, $timestamp, $secret);
}

// Função para enviar resposta de produção
function sendProdWebhookResponse($success, $message, $data = null)
{
    global $GLOBAL_REQUEST_ID;
    
    $response = [
        'status' => $success ? 'success' : 'error',
        'message' => $message,
        'environment' => 'production',
        'timestamp' => date('Y-m-d H:i:s'),
        'webhook' => 'flyingdonkeys-v2'
    ];

    if ($data !== null) {
        $response['data'] = $data;
    }
    
    if ($GLOBAL_REQUEST_ID !== null) {
        $response['request_id'] = $GLOBAL_REQUEST_ID;
    }

    http_response_code($success ? 200 : 400);
    echo json_encode($response, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT);
}

// Alias para compatibilidade
function sendDevWebhookResponse($success, $message, $data = null) {
    return sendProdWebhookResponse($success, $message, $data);
}

// Função para processar dados de teste - REMOVIDA EM PRODUÇÃO
// Em produção, todos os dados são processados normalmente
function processTestData($data)
{
    // Em produção, não há dados de teste
    return false;
}

// Função super robusta para corrigir JSON malformado do Webflow
function fixMalformedJson($json_string)
{
    // Log inicial
    logDevWebhook('json_fix_started', ['original_length' => strlen($json_string)], true);

    // CAMADA 1 - DECODIFICAR JSON PRINCIPAL
    $main_data = json_decode($json_string, true);
    if (json_last_error() === JSON_ERROR_NONE) {
        logDevWebhook('json_fix_layer1', ['status' => 'main_json_valid'], true);

        // Se tem payload, corrigir o payload interno
        if (isset($main_data['payload'])) {
            logDevWebhook('json_fix_layer1', ['status' => 'fixing_payload'], true);
            $fixed_payload = fixPayloadInternal($main_data['payload']);
            if ($fixed_payload) {
                $main_data['payload'] = $fixed_payload;
                logDevWebhook('json_fix_success', ['layer' => 1, 'method' => 'payload_correction'], true);
                return json_encode($main_data);
            }
        }

        logDevWebhook('json_fix_success', ['layer' => 1, 'method' => 'no_changes_needed'], true);
        return $json_string; // Já está correto
    }

    // CAMADA 2 - CORREÇÕES SIMPLES E SEGURAS
    logDevWebhook('json_fix_layer2', ['status' => 'simple_corrections'], true);

    // 2.1 Remover aspas duplas extras genéricas
    $fixed = preg_replace('/"([^"]*)"+([,}])/', '"$1"$2', $json_string);

    // 2.2 Corrigir escape de barras
    $fixed = str_replace('\\/', '/', $fixed);

    // 2.3 Corrigir URLs malformadas
    $fixed = preg_replace('/"https: "\\\\\/\\\\\//', '"https://', $fixed);
    $fixed = preg_replace('/"http: "\\\\\/\\\\\//', '"http://', $fixed);

    // 2.4 Testar se já está correto
    $test_decode = json_decode($fixed, true);
    if (json_last_error() === JSON_ERROR_NONE) {
        logDevWebhook('json_fix_success', ['layer' => 2, 'method' => 'simple_corrections'], true);
        return $fixed;
    }

    // CAMADA 3 - CORREÇÕES ESPECÍFICAS DO WEBFLOW
    logDevWebhook('json_fix_layer3', ['status' => 'webflow_specific'], true);

    $patterns = [
        '/"Home""/' => '"Home"',
        '/"NOME""/' => '"NOME"',
        '/"Email""/' => '"Email"',
        '/"DDD-CELULAR""/' => '"DDD-CELULAR"',
        '/"CELULAR""/' => '"CELULAR"',
        '/"CEP""/' => '"CEP"',
        '/"CPF""/' => '"CPF"',
        '/"PLACA""/' => '"PLACA"',
        '/"ANO""/' => '"ANO"',
        '/"MARCA""/' => '"MARCA"',
        '/"GCLID_FLD""/' => '"GCLID_FLD"',
        '/"SEQUENCIA_FLD""/' => '"SEQUENCIA_FLD"'
    ];

    foreach ($patterns as $pattern => $replacement) {
        $fixed = preg_replace($pattern, $replacement, $fixed);
    }

    // 3.2 Testar novamente
    $test_decode = json_decode($fixed, true);
    if (json_last_error() === JSON_ERROR_NONE) {
        logDevWebhook('json_fix_success', ['layer' => 3, 'method' => 'webflow_specific'], true);
        return $fixed;
    }

    // CAMADA 4 - RECONSTRUÇÃO INTELIGENTE
    logDevWebhook('json_fix_layer4', ['status' => 'intelligent_reconstruction'], true);

    // 4.1 Extrair dados com regex robustos
    $fields = [
        'NOME' => '/"NOME":"([^"]*)"+([,}])/',
        'Email' => '/"Email":"([^"]*)"+([,}])/',
        'DDD-CELULAR' => '/"DDD-CELULAR":"([^"]*)"+([,}])/',
        'CELULAR' => '/"CELULAR":"([^"]*)"+([,}])/',
        'CEP' => '/"CEP":"([^"]*)"+([,}])/',
        'CPF' => '/"CPF":"([^"]*)"+([,}])/',
        'PLACA' => '/"PLACA":"([^"]*)"+([,}])/',
        'ANO' => '/"ANO":"([^"]*)"+([,}])/',
        'MARCA' => '/"MARCA":"([^"]*)"+([,}])/',
        'GCLID_FLD' => '/"GCLID_FLD":"([^"]*)"+([,}])/',
        'SEQUENCIA_FLD' => '/"SEQUENCIA_FLD":"([^"]*)"+([,}])/'
    ];

    $extracted_data = [];
    foreach ($fields as $field => $pattern) {
        if (preg_match($pattern, $fixed, $matches)) {
            $extracted_data[$field] = $matches[1];
            logDevWebhook('json_fix_extracted', ['field' => $field, 'value' => $matches[1]], true);
        }
    }

    // 4.2 Se conseguiu extrair dados suficientes, reconstruir
    if (count($extracted_data) >= 2) {
        logDevWebhook('json_fix_reconstruction', ['extracted_count' => count($extracted_data)], true);
        $reconstructed = reconstructJson($extracted_data);
        logDevWebhook('json_fix_success', ['layer' => 4, 'method' => 'intelligent_reconstruction'], true);
        return $reconstructed;
    }

    // CAMADA 5 - FALLBACK COM DADOS MÍNIMOS
    logDevWebhook('json_fix_layer5', ['status' => 'minimal_fallback'], true);

    // 5.1 Tentar extrair pelo menos nome ou email
    $minimal_patterns = [
        '/"NOME":"([^"]+)"/',
        '/"Email":"([^"]+)"/',
        '/"email":"([^"]+)"/',
        '/"nome":"([^"]+)"/'
    ];

    $minimal_data = [];
    foreach ($minimal_patterns as $pattern) {
        if (preg_match($pattern, $fixed, $matches)) {
            $minimal_data[] = $matches[1];
            logDevWebhook('json_fix_minimal', ['value' => $matches[1]], true);
        }
    }

    // 5.2 Se conseguiu algo, criar JSON mínimo
    if (!empty($minimal_data)) {
        logDevWebhook('json_fix_minimal_json', ['data_count' => count($minimal_data)], true);
        $minimal_json = createMinimalJson($minimal_data);
        logDevWebhook('json_fix_success', ['layer' => 5, 'method' => 'minimal_fallback'], true);
        return $minimal_json;
    }

    // Se chegou até aqui, falhou completamente
    logDevWebhook('json_fix_failed', ['reason' => 'all_layers_failed'], false);
    return false;
}

// Função auxiliar para corrigir payload interno
function fixPayloadInternal($payload_string)
{
    logDevWebhook('payload_fix_started', ['payload_length' => strlen($payload_string)], true);

    // Tentar decodificar o payload
    $payload_data = json_decode($payload_string, true);
    if (json_last_error() === JSON_ERROR_NONE) {
        logDevWebhook('payload_fix_success', ['method' => 'no_changes_needed'], true);
        return $payload_string;
    }

    // Corrigir aspas duplas extras no payload
    $fixed_payload = preg_replace('/"([^"]*)"+([,}])/', '"$1"$2', $payload_string);

    // Tentar decodificar novamente
    $payload_data = json_decode($fixed_payload, true);
    if (json_last_error() === JSON_ERROR_NONE) {
        logDevWebhook('payload_fix_success', ['method' => 'simple_correction'], true);
        return $fixed_payload;
    }

    // Se tem data interno, corrigir também
    if (isset($payload_data['data'])) {
        $data_string = $payload_data['data'];
        $fixed_data = preg_replace('/"([^"]*)"+([,}])/', '"$1"$2', $data_string);
        $payload_data['data'] = $fixed_data;
        logDevWebhook('payload_fix_success', ['method' => 'data_correction'], true);
        return json_encode($payload_data);
    }

    logDevWebhook('payload_fix_failed', ['reason' => 'all_methods_failed'], false);
    return false;
}

// Função auxiliar para reconstruir JSON completo
function reconstructJson($data)
{
    return json_encode([
        'name' => 'Home',
        'siteId' => '68f77ea29d6b098f6bcad795',
        'data' => $data,
        'submittedAt' => date('c'),
        'id' => uniqid(),
        'formId' => '68f788bd5dc3f2ca4483eee0',
        'formElementId' => '97e5c20e-4fe9-8fcf-d941-485bbc20f783',
        'pageId' => '68f77ea29d6b098f6bcad76f',
        'publishedPath' => '/',
        'pageUrl' => 'https://segurosimediato-8119bf26e77bf4ff336a58e.webflow.io/',
        'schema' => []
    ]);
}

// Função auxiliar para criar JSON mínimo
function createMinimalJson($data)
{
    return json_encode([
        'name' => 'Home',
        'data' => [
            'NOME' => $data[0] ?? 'Nome não informado',
            'Email' => $data[1] ?? 'email@nao.informado.com'
        ]
    ]);
}

// Função para buscar lead por email (IDÊNTICA À PRODUÇÃO)
function findLeadByEmail($email, $client, $logs)
{
    try {
        $leads = $client->request('GET', 'Lead', [
            'where' => [
                'emailAddress' => $email
            ],
            'maxSize' => 1
        ]);

        if (isset($leads['list']) && count($leads['list']) > 0) {
            logDevWebhook("Lead encontrado por email: " . $leads['list'][0]['id'], [], true);
            return $leads['list'][0];
        }
        logDevWebhook("Nenhum lead encontrado para o email: " . $email, [], true);
        return null;
    } catch (Exception $e) {
        logDevWebhook("Erro ao buscar lead por email: " . $e->getMessage(), [], false);
        return null;
    }
}

// Função para simular resposta do CRM - REMOVIDA EM PRODUÇÃO
// Em produção, sempre usa CRM real - não há simulação

// Log de início da requisição
logDevWebhook('webhook_started', [
    'method' => $_SERVER['REQUEST_METHOD'],
    'headers' => getallheaders(),
    'content_type' => $_SERVER['CONTENT_TYPE'] ?? 'unknown'
], true);

// Verificar método HTTP
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    logDevWebhook('invalid_method', ['method' => $_SERVER['REQUEST_METHOD']], false);
    sendDevWebhookResponse(false, 'Método não permitido');
    exit;
}

// Obter dados da requisição
$raw_input = file_get_contents('php://input');
$data = json_decode($raw_input, true);

if (json_last_error() !== JSON_ERROR_NONE) {
    // Log ANTES da correção
    logDevWebhook('json_decode_error_before_fix', [
        'error' => json_last_error_msg(),
        'raw_input_length' => strlen($raw_input),
        'raw_input_preview' => substr($raw_input, 0, 300) . '...'
    ], false);

    // Tentar corrigir JSON malformado
    logDevWebhook('attempting_json_fix', [
        'original_error' => json_last_error_msg(),
        'raw_input_preview' => substr($raw_input, 0, 200) . '...'
    ], false);

    $fixed_input = fixMalformedJson($raw_input);

    // Log DEPOIS da correção
    logDevWebhook('json_fix_result', [
        'fix_function_returned' => $fixed_input ? 'success' : 'false',
        'fixed_input_length' => $fixed_input ? strlen($fixed_input) : 0,
        'fixed_input_preview' => $fixed_input ? substr($fixed_input, 0, 300) . '...' : 'NULL'
    ], $fixed_input ? true : false);

    if ($fixed_input) {
        $data = json_decode($fixed_input, true);

        // Log do resultado da decodificação após correção
        logDevWebhook('json_decode_after_fix', [
            'json_error' => json_last_error_msg(),
            'json_error_code' => json_last_error(),
            'decode_success' => json_last_error() === JSON_ERROR_NONE,
            'data_keys' => json_last_error() === JSON_ERROR_NONE ? array_keys($data) : [],
            'data_preview' => json_last_error() === JSON_ERROR_NONE ? json_encode(array_slice($data, 0, 3)) : 'DECODE_FAILED'
        ], json_last_error() === JSON_ERROR_NONE);

        if (json_last_error() === JSON_ERROR_NONE) {
            logDevWebhook('json_fix_complete_success', [
                'success' => true,
                'data_keys' => array_keys($data),
                'data_structure' => isset($data['payload']) ? 'has_payload' : 'no_payload'
            ], true);

            // CORREÇÃO: Se o JSON foi corrigido, processar os dados diretamente
            if (isset($data['payload'])) {
                $payload_data = json_decode($data['payload'], true);
                if ($payload_data && isset($payload_data['data'])) {
                    $form_data = $payload_data['data'];
                    logDevWebhook('api_v2_payload_fixed_and_decoded', [
                        'payload_data' => $payload_data,
                        'form_data' => $form_data
                    ], true);
                }
            }
        } else {
            logDevWebhook('json_fix_decode_failed', [
                'error' => json_last_error_msg(),
                'error_code' => json_last_error(),
                'fixed_input_preview' => substr($fixed_input, 0, 200) . '...'
            ], false);
            sendDevWebhookResponse(false, 'Erro ao decodificar JSON após correção');
            exit;
        }
    } else {
        logDevWebhook('json_fix_returned_false', [
            'fix_function_returned' => false,
            'raw_input_length' => strlen($raw_input)
        ], false);
        sendDevWebhookResponse(false, 'Erro ao decodificar JSON - função de correção retornou false');
        exit;
    }
}

logDevWebhook('data_received', $data, true);

// Validar signature do Webflow (API V2) - VALIDAÇÃO CONDICIONAL
// Se assinatura presente = requisição do Webflow (validar obrigatoriamente)
// Se assinatura ausente = requisição do navegador/modal (aceitar sem validação)
$signature = $_SERVER['HTTP_X_WEBFLOW_SIGNATURE'] ?? '';
$timestamp = $_SERVER['HTTP_X_WEBFLOW_TIMESTAMP'] ?? '';

if (!empty($signature) && !empty($timestamp)) {
    // Assinatura presente - validar (requisição do Webflow)
    if (!validateWebflowSignatureProd($raw_input, $signature, $timestamp, $WEBFLOW_SECRET_TRAVELANGELS)) {
        logProdWebhook('signature_validation_failed', [
            'signature_received' => substr($signature, 0, 16) . '...',
            'timestamp_received' => $timestamp,
            'ip' => $_SERVER['REMOTE_ADDR'] ?? 'unknown',
            'reason' => 'signature_invalid'
        ], false);
        sendProdWebhookResponse(false, 'Assinatura inválida');
        exit;
    }
    logProdWebhook('signature_validation', [
        'status' => 'valid',
        'source' => 'webflow',
        'signature_received' => substr($signature, 0, 16) . '...',
        'timestamp_received' => $timestamp
    ], true);
} else {
    // Assinatura ausente - requisição do navegador/modal (aceitar)
    logProdWebhook('signature_validation', [
        'status' => 'skipped',
        'source' => 'browser',
        'reason' => 'signature_not_provided',
        'ip' => $_SERVER['REMOTE_ADDR'] ?? 'unknown'
    ], true);
}

// Processar dados da API V2 do Webflow (ÚNICA VEZ)
$form_data = [];
if (isset($data['payload'])) {
    // API V2: payload é uma string JSON que precisa ser decodificada
    if (is_string($data['payload'])) {
        $payload_data = json_decode($data['payload'], true);
    } else {
        $payload_data = $data['payload']; // Já é um array
    }

    if ($payload_data && isset($payload_data['data'])) {
        // Decodificar o campo 'data' que também é uma string JSON
        if (is_string($payload_data['data'])) {
            $form_data = json_decode($payload_data['data'], true);
        } else {
            $form_data = $payload_data['data']; // Já é um array
        }

        if (is_array($form_data)) {
            logDevWebhook('api_v2_payload_decoded', ['payload_data' => $payload_data, 'form_data' => $form_data], true);
        } else {
            logDevWebhook('api_v2_data_decode_error', [
                'data_raw' => $payload_data['data'],
                'error' => json_last_error_msg()
            ], false);
            sendDevWebhookResponse(false, 'Erro ao decodificar campo data da API V2');
            exit;
        }
    } else {
        // Tentar corrigir o payload malformado
        $fixed_payload = fixMalformedJson($data['payload']);
        if ($fixed_payload) {
            $payload_data = json_decode($fixed_payload, true);
            if ($payload_data && isset($payload_data['data'])) {
                // Se payload_data['data'] já é um array (retornado pela função de correção), usar diretamente
                if (is_array($payload_data['data'])) {
                    $form_data = $payload_data['data'];
                    logDevWebhook('api_v2_payload_fixed_and_decoded', [
                        'payload_data' => $payload_data,
                        'form_data' => $form_data
                    ], true);
                } else {
                    // Decodificar o campo 'data' que é uma string JSON
                    $form_data = json_decode($payload_data['data'], true);
                    if (json_last_error() === JSON_ERROR_NONE) {
                        logDevWebhook('api_v2_payload_fixed_and_decoded', [
                            'payload_data' => $payload_data,
                            'form_data' => $form_data
                        ], true);
                    } else {
                        logDevWebhook('api_v2_fixed_data_decode_error', [
                            'data_raw' => $payload_data['data'],
                            'error' => json_last_error_msg()
                        ], false);
                        sendDevWebhookResponse(false, 'Erro ao decodificar campo data corrigido da API V2');
                        exit;
                    }
                }
            } else {
                logDevWebhook('api_v2_payload_fix_failed', [
                    'payload_raw' => $data['payload'],
                    'fixed_payload' => $fixed_payload,
                    'error' => json_last_error_msg()
                ], false);
                sendDevWebhookResponse(false, 'Erro ao decodificar payload da API V2 - correção falhou');
                exit;
            }
        } else {
            logDevWebhook('api_v2_payload_decode_error', [
                'payload_raw' => $data['payload'],
                'error' => json_last_error_msg()
            ], false);
            sendDevWebhookResponse(false, 'Erro ao decodificar payload da API V2');
            exit;
        }
    }
} else {
    // Fallback para estrutura direta (API V1 ou dados de teste)
    if (isset($data['data'])) {
        $form_data = $data['data'];  // ✅ CORRETO - pega apenas os dados do formulário
        logDevWebhook('api_v2_direct_data', ['form_data' => $form_data], true);
    } else {
        $form_data = $data;  // Para dados realmente diretos
        logDevWebhook('api_v1_or_direct_data', ['data' => $data], true);
    }
}

logDevWebhook('data_processing_complete', ['form_data' => $form_data], true);

// Verificar se são dados de teste
if (processTestData($form_data)) {
    logDevWebhook('test_data_processed', ['original_data' => $form_data, 'test_mode' => true, 'crm_bypass' => true], true);
    sendDevWebhookResponse(true, 'Dados de teste processados - não enviado para CRM', [
        'test_mode' => true,
        'request_id' => $GLOBAL_REQUEST_ID
    ]);
    exit;
}

// Incluir classe do CRM
// Em produção, o arquivo estará em /var/www/html/webhooks/
// E o class.php está em /var/www/html/class.php
require_once __DIR__ . '/../class.php';

// Carregar função de notificação de administradores
require_once __DIR__ . '/send_admin_notification_ses.php';

// ⚠️ CREDENCIAIS DE PRODUÇÃO FLYINGDONKEYS (obtidas do add_travelangels.php de produção)
$FLYINGDONKEYS_API_URL = 'https://flyingdonkeys.com.br';
$FLYINGDONKEYS_API_KEY = '82d5f667f3a65a9a43341a0705be2b0c';

try {
    // Em produção, sempre usar CRM real
    $client = new EspoApiClient($FLYINGDONKEYS_API_URL);
    $client->setApiKey($FLYINGDONKEYS_API_KEY);
    
    logProdWebhook('crm_connection', [
        'url' => $FLYINGDONKEYS_API_URL,
        'api_key_length' => strlen($FLYINGDONKEYS_API_KEY),
        'mode' => 'production'
    ], true);

    // Mapeamento adaptativo dos campos recebidos (IDÊNTICO À PRODUÇÃO)
    // Estrutura 1: campos diretos (formulário simples)
    // Estrutura 2: campos aninhados (Webflow API V2)
    $name = isset($form_data['nome']) ? $form_data['nome'] : (isset($form_data['NOME']) ? $form_data['NOME'] : '');
    $telefone = isset($form_data['telefone']) ? $form_data['telefone'] : (isset($form_data['DDD-CELULAR']) && isset($form_data['CELULAR']) ? $form_data['DDD-CELULAR'] . $form_data['CELULAR'] : '');
    $email = isset($form_data['email']) ? $form_data['email'] : (isset($form_data['Email']) ? $form_data['Email'] : '');
    $cep = isset($form_data['cep']) ? $form_data['cep'] : (isset($form_data['CEP']) ? $form_data['CEP'] : '');
    $cpf = isset($form_data['cpf']) ? $form_data['cpf'] : (isset($form_data['CPF']) ? $form_data['CPF'] : '');
    $marca = isset($form_data['marca']) ? $form_data['marca'] : (isset($form_data['MARCA']) ? $form_data['MARCA'] : '');
    $placa = isset($form_data['placa']) ? $form_data['placa'] : (isset($form_data['PLACA']) ? $form_data['PLACA'] : '');
    $ano = isset($form_data['ano']) ? $form_data['ano'] : (isset($form_data['ANO']) ? $form_data['ANO'] : '');
    $gclid = isset($form_data['gclid']) ? $form_data['gclid'] : (isset($form_data['GCLID_FLD']) ? $form_data['GCLID_FLD'] : '');
    $endereco = '';
    $cidade = '';
    $estado = '';
    $veiculo = '';
    $webpage = 'mdmidia.com.br'; // Ambiente de produção
    $source = 'Site';

    // Validação crítica dos campos obrigatórios
    if (empty($name)) {
        logDevWebhook('validation_error', [
            'field' => 'name',
            'value' => $name,
            'form_data' => $form_data,
            'error' => 'Campo name está vazio'
        ], false);
        sendDevWebhookResponse(false, 'Erro de validação: Campo nome é obrigatório', [
            'request_id' => $GLOBAL_REQUEST_ID,
            'validation_error' => 'name_required'
        ]);
        exit;
    }

    if (empty($email)) {
        logDevWebhook('validation_error', [
            'field' => 'email',
            'value' => $email,
            'form_data' => $form_data,
            'error' => 'Campo email está vazio'
        ], false);
        sendDevWebhookResponse(false, 'Erro de validação: Campo email é obrigatório', [
            'request_id' => $GLOBAL_REQUEST_ID,
            'validation_error' => 'email_required'
        ]);
        exit;
    }

    logDevWebhook('field_mapping', [
        'name' => $name,
        'telefone' => $telefone,
        'email' => $email,
        'cep' => $cep,
        'cpf' => $cpf,
        'marca' => $marca,
        'placa' => $placa,
        'ano' => $ano,
        'gclid' => $gclid,
        'webpage' => $webpage,
        'source' => $source
    ], true);

    /**
     * Identifica em qual momento o modal está sendo processado
     * 
     * @param array $form_data Dados do formulário recebido
     * @return array ['moment' => 'initial'|'update', 'emoji' => string, 'color' => string, 'color_name' => string, 'description' => string, 'icon' => string]
     */
    function identifyModalMoment($form_data) {
        // Verificar pelo campo 'name' do payload (se disponível)
        $name_field = isset($form_data['name']) ? $form_data['name'] : '';
        
        // Verificar pelo padrão do nome (INITIAL tem padrão especial)
        $nome_value = isset($form_data['nome']) ? $form_data['nome'] : (isset($form_data['NOME']) ? $form_data['NOME'] : '');
        $is_initial_pattern = preg_match('/^\d{2}-\d{9}-NOVO CLIENTE WHATSAPP$/', $nome_value);
        
        // Verificar se campos obrigatórios estão vazios (INITIAL tem apenas telefone)
        $cpf_vazio = empty($form_data['cpf']) && empty($form_data['CPF']);
        $cep_vazio = empty($form_data['cep']) && empty($form_data['CEP']);
        $placa_vazia = empty($form_data['placa']) && empty($form_data['PLACA']);
        
        // Lógica de identificação
        if (
            (strpos($name_field, 'Primeiro Contato') !== false) ||
            $is_initial_pattern ||
            ($cpf_vazio && $cep_vazio && $placa_vazia)
        ) {
            // MOMENTO 1: INITIAL
            return [
                'moment' => 'initial',
                'emoji' => '📞',
                'color' => '🔵',
                'color_name' => 'AZUL',
                'description' => 'Primeiro Contato - Apenas Telefone',
                'icon' => '📞'
            ];
        } else {
            // MOMENTO 2: UPDATE
            return [
                'moment' => 'update',
                'emoji' => '✅',
                'color' => '🟢',
                'color_name' => 'VERDE',
                'description' => 'Submissão Completa - Todos os Dados',
                'icon' => '✅'
            ];
        }
    }

    // Identificar momento do modal
    $modalMoment = identifyModalMoment($form_data);

    // Preparar dados para email (sempre incluir, mesmo se alguns campos estiverem vazios)
    $emailData = [
        'ddd' => isset($form_data['DDD-CELULAR']) ? $form_data['DDD-CELULAR'] : '',
        'celular' => isset($form_data['CELULAR']) ? $form_data['CELULAR'] : '',
        'cpf' => $cpf,
        'nome' => $name,
        'email' => $email,
        'cep' => $cep,
        'placa' => $placa,
        'gclid' => $gclid,
        'momento' => $modalMoment['moment'],
        'momento_descricao' => $modalMoment['description'],
        'momento_emoji' => $modalMoment['emoji']
    ];

    // Payload completo para FlyingDonkeys (IDÊNTICO À PRODUÇÃO)
    $lead_data = [
        'firstName' => $name,
        'emailAddress' => $email,
        'cCelular' => $telefone,
        'addressPostalCode' => $cep,
        'addressCity' => $cidade,
        'addressState' => $estado,
        'addressCountry' => 'Brasil',
        'addressStreet' => $endereco,
        'cCpftext' => $cpf,
        'cMarca' => $marca,
        'cPlaca' => $placa,
        'cAnoMod' => $ano,
        'cGclid' => $gclid,
        'cWebpage' => $webpage,
        'source' => $source,
    ];

    logDevWebhook('lead_data_prepared', $lead_data, true);

    // Log detalhado antes de enviar para EspoCRM
    logProdWebhook('espocrm_request_details', [
        'espocrm_url' => $FLYINGDONKEYS_API_URL,
        'api_key' => substr($FLYINGDONKEYS_API_KEY, 0, 8) . '...',
        'endpoint' => 'Lead',
        'method' => 'POST',
        'payload' => $lead_data,
        'field_mapping' => [
            'NOME' => $name,
            'Email' => $email,
            'DDD-CELULAR' => $form_data['DDD-CELULAR'] ?? '',
            'CELULAR' => $form_data['CELULAR'] ?? '',
            'telefone_completo' => $telefone,
            'CEP' => $cep,
            'CPF' => $cpf,
            'MARCA' => $marca,
            'PLACA' => $placa,
            'ANO' => $ano,
            'GCLID_FLD' => $gclid
        ]
    ], true);

    // ===== PROCESSAMENTO FLYINGDONKEYS (LÓGICA COMPLETA IDÊNTICA À PRODUÇÃO) =====
    logDevWebhook('processing_flyingdonkeys', ['status' => 'started'], true);

    $leadIdFlyingDonkeys = null;
    $opportunityIdFlyingDonkeys = null;

    // ✅ V4: Verificar se vem lead_id, contact_id ou opportunity_id no payload (indica atualização)
    $leadIdFromPayload = isset($form_data['lead_id']) ? $form_data['lead_id'] : (isset($form_data['contact_id']) ? $form_data['contact_id'] : null);
    $opportunityIdFromPayload = isset($form_data['opportunity_id']) ? $form_data['opportunity_id'] : null;
    
    // ✅ V4: Log dos IDs recebidos no payload
    logDevWebhook('payload_ids_analysis', [
        'has_lead_id' => !empty($leadIdFromPayload),
        'lead_id' => $leadIdFromPayload,
        'has_opportunity_id' => !empty($opportunityIdFromPayload),
        'opportunity_id' => $opportunityIdFromPayload,
        'mode' => empty($leadIdFromPayload) && empty($opportunityIdFromPayload) ? 'create' : 'update'
    ], true);
    
    if ($leadIdFromPayload) {
        // Se tem ID no payload, fazer UPDATE diretamente
        logDevWebhook('update_lead_requested', [
            'lead_id' => $leadIdFromPayload,
            'source' => isset($form_data['lead_id']) ? 'lead_id' : 'contact_id'
        ], true);

        try {
            // Atualizar lead existente
            $updateResponse = $client->request('PATCH', 'Lead/' . $leadIdFromPayload, $lead_data);
            logDevWebhook('lead_updated_via_payload', [
                'lead_id' => $leadIdFromPayload,
                'updated_data' => $lead_data
            ], true);
            $leadIdFlyingDonkeys = $leadIdFromPayload;

            // 📧 ENVIAR EMAIL PARA ADMINISTRADORES APÓS ATUALIZAÇÃO DO LEAD VIA PAYLOAD
            try {
                $emailResult = enviarNotificacaoAdministradores($emailData);
                
                // Log diferenciado por momento
                if ($modalMoment['moment'] === 'initial') {
                    logProdWebhook('email_notification_initial_sent', [
                        'moment' => $modalMoment['moment'],
                        'emoji' => $modalMoment['emoji'],
                        'color' => $modalMoment['color'],
                        'description' => $modalMoment['description'],
                        'lead_id' => $leadIdFlyingDonkeys,
                        'email_result' => $emailResult,
                        'recipients' => count(ADMIN_EMAILS)
                    ], $emailResult['success']);
                    
                    error_log(sprintf(
                        "%s [EMAIL-%s] %s Notificação INITIAL enviada - Lead: %s - Sucesso: %s",
                        $modalMoment['emoji'],
                        $modalMoment['color_name'],
                        $modalMoment['description'],
                        $leadIdFlyingDonkeys,
                        $emailResult['success'] ? 'SIM' : 'NÃO'
                    ));
                } else {
                    logProdWebhook('email_notification_update_sent', [
                        'moment' => $modalMoment['moment'],
                        'emoji' => $modalMoment['emoji'],
                        'color' => $modalMoment['color'],
                        'description' => $modalMoment['description'],
                        'lead_id' => $leadIdFlyingDonkeys,
                        'email_result' => $emailResult,
                        'recipients' => count(ADMIN_EMAILS)
                    ], $emailResult['success']);
                    
                    error_log(sprintf(
                        "%s [EMAIL-%s] %s Notificação UPDATE enviada - Lead: %s - Sucesso: %s",
                        $modalMoment['emoji'],
                        $modalMoment['color_name'],
                        $modalMoment['description'],
                        $leadIdFlyingDonkeys,
                        $emailResult['success'] ? 'SIM' : 'NÃO'
                    ));
                }
                
                if (!$emailResult['success']) {
                    logProdWebhook('email_notification_failed', [
                        'error' => $emailResult['error'] ?? 'Erro desconhecido',
                        'lead_id' => $leadIdFlyingDonkeys,
                        'moment' => $modalMoment['moment']
                    ], false);
                }
            } catch (Exception $emailException) {
                // Não bloquear o fluxo principal em caso de erro no email
                logProdWebhook('email_notification_exception', [
                    'error' => $emailException->getMessage(),
                    'lead_id' => $leadIdFlyingDonkeys,
                    'moment' => $modalMoment['moment']
                ], false);
                
                error_log(sprintf(
                    "⚠️ [EMAIL-ERRO] Falha ao enviar notificação - Lead: %s - Erro: %s",
                    $leadIdFlyingDonkeys,
                    $emailException->getMessage()
                ));
            }
        } catch (Exception $e) {
            $errorMessage = $e->getMessage();
            logDevWebhook('lead_update_failed', [
                'lead_id' => $leadIdFromPayload,
                'error' => $errorMessage
            ], false);
            // Se falhar a atualização, tentar criar novo (fallback)
            logDevWebhook('fallback_to_create', ['reason' => 'update_failed'], true);
            $leadIdFromPayload = null; // Resetar para tentar criar novo
        }
    }

    // Se não veio ID ou a atualização falhou, tentar criar novo lead
    if (!$leadIdFlyingDonkeys) {
        // Preparar chamada cURL completa para log
        $curlRequestLead = [
        'url' => $FLYINGDONKEYS_API_URL . '/api/v1/Lead',
        'method' => 'POST',
        'headers' => [
            'X-Api-Key' => $FLYINGDONKEYS_API_KEY,
            'Content-Type' => 'application/json'
        ],
        'payload' => $lead_data,
        'request_id' => $GLOBAL_REQUEST_ID
    ];

    // Log da chamada completa antes de executar
    logDevWebhook('curl_request_complete_lead', $curlRequestLead, true);

    // Tentar criar lead no FlyingDonkeys
    try {
        logProdWebhook('flyingdonkeys_lead_creation_started', [
            'email' => $email,
            'name' => $name,
            'payload_keys' => array_keys($lead_data)
        ], true);
        
        $responseFlyingDonkeys = $client->request('POST', 'Lead', $lead_data);
        
        logProdWebhook('flyingdonkeys_api_response', [
            'response_keys' => array_keys($responseFlyingDonkeys),
            'has_id' => isset($responseFlyingDonkeys['id']),
            'response_preview' => json_encode($responseFlyingDonkeys)
        ], true);
        
        $leadIdFlyingDonkeys = $responseFlyingDonkeys['id'] ?? null;
        
        if (!$leadIdFlyingDonkeys) {
            logProdWebhook('flyingdonkeys_lead_creation_missing_id', [
                'response' => json_encode($responseFlyingDonkeys)
            ], false);
            throw new Exception('Lead criado mas ID não retornado na resposta');
        }
        
        logDevWebhook('flyingdonkeys_lead_created', ['lead_id' => $leadIdFlyingDonkeys], true);

        // 📧 ENVIAR EMAIL PARA ADMINISTRADORES APÓS CRIAÇÃO DO LEAD
        try {
            $emailResult = enviarNotificacaoAdministradores($emailData);
            
            // Log diferenciado por momento
            if ($modalMoment['moment'] === 'initial') {
                logProdWebhook('email_notification_initial_sent', [
                    'moment' => $modalMoment['moment'],
                    'emoji' => $modalMoment['emoji'],
                    'color' => $modalMoment['color'],
                    'description' => $modalMoment['description'],
                    'lead_id' => $leadIdFlyingDonkeys,
                    'email_result' => $emailResult,
                    'recipients' => count(ADMIN_EMAILS)
                ], $emailResult['success']);
                
                error_log(sprintf(
                    "%s [EMAIL-%s] %s Notificação INITIAL enviada - Lead: %s - Sucesso: %s",
                    $modalMoment['emoji'],
                    $modalMoment['color_name'],
                    $modalMoment['description'],
                    $leadIdFlyingDonkeys,
                    $emailResult['success'] ? 'SIM' : 'NÃO'
                ));
            } else {
                logProdWebhook('email_notification_update_sent', [
                    'moment' => $modalMoment['moment'],
                    'emoji' => $modalMoment['emoji'],
                    'color' => $modalMoment['color'],
                    'description' => $modalMoment['description'],
                    'lead_id' => $leadIdFlyingDonkeys,
                    'email_result' => $emailResult,
                    'recipients' => count(ADMIN_EMAILS)
                ], $emailResult['success']);
                
                error_log(sprintf(
                    "%s [EMAIL-%s] %s Notificação UPDATE enviada - Lead: %s - Sucesso: %s",
                    $modalMoment['emoji'],
                    $modalMoment['color_name'],
                    $modalMoment['description'],
                    $leadIdFlyingDonkeys,
                    $emailResult['success'] ? 'SIM' : 'NÃO'
                ));
            }
            
            if (!$emailResult['success']) {
                logProdWebhook('email_notification_failed', [
                    'error' => $emailResult['error'] ?? 'Erro desconhecido',
                    'lead_id' => $leadIdFlyingDonkeys,
                    'moment' => $modalMoment['moment']
                ], false);
            }
        } catch (Exception $emailException) {
            // Não bloquear o fluxo principal em caso de erro no email
            logProdWebhook('email_notification_exception', [
                'error' => $emailException->getMessage(),
                'lead_id' => $leadIdFlyingDonkeys,
                'moment' => $modalMoment['moment']
            ], false);
            
            error_log(sprintf(
                "⚠️ [EMAIL-ERRO] Falha ao enviar notificação - Lead: %s - Erro: %s",
                $leadIdFlyingDonkeys,
                $emailException->getMessage()
            ));
        }
    } catch (Exception $e) {
        $errorMessage = $e->getMessage();
        logDevWebhook('flyingdonkeys_exception', ['error' => $errorMessage], false);

        // Se erro 409 (duplicata) ou se a resposta contém dados do lead (EspoCRM retorna lead existente como "erro")
        if (
            strpos($errorMessage, '409') !== false || strpos($errorMessage, 'duplicate') !== false ||
            (strpos($errorMessage, '"id":') !== false && strpos($errorMessage, '"name":') !== false)
        ) {

            logDevWebhook('duplicate_lead_detected', ['email' => $email], true);

            $existingLead = findLeadByEmail($email, $client, null);
            if ($existingLead) {
                logDevWebhook('existing_lead_found', ['lead_id' => $existingLead['id']], true);

                // Atualizar lead existente
                $updateResponse = $client->request('PATCH', 'Lead/' . $existingLead['id'], $lead_data);
                logDevWebhook('lead_updated', ['lead_id' => $existingLead['id']], true);
                $leadIdFlyingDonkeys = $existingLead['id'];

                // 📧 ENVIAR EMAIL PARA ADMINISTRADORES APÓS ATUALIZAÇÃO DO LEAD
                try {
                    $emailResult = enviarNotificacaoAdministradores($emailData);
                    
                    // Log diferenciado por momento
                    if ($modalMoment['moment'] === 'initial') {
                        logProdWebhook('email_notification_initial_sent', [
                            'moment' => $modalMoment['moment'],
                            'emoji' => $modalMoment['emoji'],
                            'color' => $modalMoment['color'],
                            'description' => $modalMoment['description'],
                            'lead_id' => $leadIdFlyingDonkeys,
                            'email_result' => $emailResult,
                            'recipients' => count(ADMIN_EMAILS)
                        ], $emailResult['success']);
                        
                        error_log(sprintf(
                            "%s [EMAIL-%s] %s Notificação INITIAL enviada - Lead: %s - Sucesso: %s",
                            $modalMoment['emoji'],
                            $modalMoment['color_name'],
                            $modalMoment['description'],
                            $leadIdFlyingDonkeys,
                            $emailResult['success'] ? 'SIM' : 'NÃO'
                        ));
                    } else {
                        logProdWebhook('email_notification_update_sent', [
                            'moment' => $modalMoment['moment'],
                            'emoji' => $modalMoment['emoji'],
                            'color' => $modalMoment['color'],
                            'description' => $modalMoment['description'],
                            'lead_id' => $leadIdFlyingDonkeys,
                            'email_result' => $emailResult,
                            'recipients' => count(ADMIN_EMAILS)
                        ], $emailResult['success']);
                        
                        error_log(sprintf(
                            "%s [EMAIL-%s] %s Notificação UPDATE enviada - Lead: %s - Sucesso: %s",
                            $modalMoment['emoji'],
                            $modalMoment['color_name'],
                            $modalMoment['description'],
                            $leadIdFlyingDonkeys,
                            $emailResult['success'] ? 'SIM' : 'NÃO'
                        ));
                    }
                    
                    if (!$emailResult['success']) {
                        logProdWebhook('email_notification_failed', [
                            'error' => $emailResult['error'] ?? 'Erro desconhecido',
                            'lead_id' => $leadIdFlyingDonkeys,
                            'moment' => $modalMoment['moment']
                        ], false);
                    }
                } catch (Exception $emailException) {
                    // Não bloquear o fluxo principal em caso de erro no email
                    logProdWebhook('email_notification_exception', [
                        'error' => $emailException->getMessage(),
                        'lead_id' => $leadIdFlyingDonkeys,
                        'moment' => $modalMoment['moment']
                    ], false);
                    
                    error_log(sprintf(
                        "⚠️ [EMAIL-ERRO] Falha ao enviar notificação - Lead: %s - Erro: %s",
                        $leadIdFlyingDonkeys,
                        $emailException->getMessage()
                    ));
                }
            } else {
                // Se não encontrou por email, mas a resposta contém dados do lead, usar esses dados
                if (strpos($errorMessage, '"id":') !== false && strpos($errorMessage, '"name":') !== false) {
                    $leadData = json_decode($errorMessage, true);
                    if (isset($leadData[0]['id'])) {
                        logDevWebhook('using_lead_from_response', ['lead_id' => $leadData[0]['id']], true);
                        $leadIdFlyingDonkeys = $leadData[0]['id'];
                    } else {
                        logDevWebhook('duplicate_lead_not_found', ['error' => 'Lead duplicado mas não encontrado por email'], false);
                        throw $e;
                    }
                } else {
                    logDevWebhook('duplicate_lead_not_found', ['error' => 'Lead duplicado mas não encontrado por email'], false);
                    throw $e;
                }
            }
        } else {
            logDevWebhook('real_error_creating_lead', ['error' => $errorMessage], false);
            throw $e;
        }
    }
    } // ✅ Fechar bloco if (!$leadIdFlyingDonkeys)

    // ✅ V4: PROCESSAMENTO DE OPORTUNIDADE (LÓGICA CONDICIONAL)
    // Regra 1: Se vem opportunity_id no payload → ATUALIZAR oportunidade existente
    // Regra 2: Se vem lead_id mas NÃO opportunity_id → NÃO criar nova oportunidade (apenas atualizar lead)
    // Regra 3: Se NÃO vem nenhum dos dois → Criar lead + oportunidade normalmente (backward compatibility)
    
    if ($opportunityIdFromPayload) {
        // ✅ V4: ATUALIZAR oportunidade existente
        logDevWebhook('update_opportunity_requested', [
            'opportunity_id' => $opportunityIdFromPayload,
            'lead_id' => $leadIdFlyingDonkeys
        ], true);

        try {
            $opportunityPayload = [
                'name' => $name,
                'leadId' => $leadIdFlyingDonkeys,
                'stage' => 'Novo Sem Contato',
                'amount' => 0,
                'probability' => 10,
                'cAnoFab' => $ano,
                'cAnoMod' => $ano,
                'cCEP' => $cep,
                'cCelular' => $telefone,
                'cCpftext' => $cpf,
                'cGclid' => $gclid,
                'cMarca' => $marca,
                'cPlaca' => $placa,
                'cWebpage' => $webpage,
                'cEmail' => $email,
                'cEmailAdress' => $email,
                'leadSource' => $source,
                'cSegpref' => isset($form_data['seguradora_preferencia']) ? $form_data['seguradora_preferencia'] : '',
                'cValorpret' => isset($form_data['valor_preferencia']) ? $form_data['valor_preferencia'] : '',
                'cModalidade' => isset($form_data['modalidade_seguro']) ? $form_data['modalidade_seguro'] : '',
                'cSegant' => isset($form_data['seguradora_apolice']) ? $form_data['seguradora_apolice'] : '',
                'cCiapol' => isset($form_data['ci']) ? $form_data['ci'] : '',
            ];

            // Atualizar oportunidade existente
            $updateOpportunityResponse = $client->request('PATCH', 'Opportunity/' . $opportunityIdFromPayload, $opportunityPayload);
            $opportunityIdFlyingDonkeys = $opportunityIdFromPayload;
            logDevWebhook('opportunity_updated_via_payload', [
                'opportunity_id' => $opportunityIdFlyingDonkeys,
                'updated_data' => $opportunityPayload
            ], true);
        } catch (Exception $e) {
            $errorMessage = $e->getMessage();
            logDevWebhook('opportunity_update_failed', [
                'opportunity_id' => $opportunityIdFromPayload,
                'error' => $errorMessage
            ], false);
            // Em caso de erro na atualização, não tentar criar nova (manter null)
        }
    } elseif (!$leadIdFromPayload && $leadIdFlyingDonkeys) {
        // ✅ V4: CRIAR oportunidade APENAS se não veio lead_id no payload (comportamento normal/criação inicial)
        // Se veio lead_id no payload, significa que é uma atualização e não devemos criar nova oportunidade
        try {
            $opportunityPayload = [
                'name' => $name,
                'leadId' => $leadIdFlyingDonkeys,
                'stage' => 'Novo Sem Contato',
                'amount' => 0,
                'probability' => 10,
                'cAnoFab' => $ano,
                'cAnoMod' => $ano,
                'cCEP' => $cep,
                'cCelular' => $telefone,
                'cCpftext' => $cpf,
                'cGclid' => $gclid,
                'cMarca' => $marca,
                'cPlaca' => $placa,
                'cWebpage' => $webpage,
                'cEmail' => $email,
                'cEmailAdress' => $email,
                'leadSource' => $source,
                'cSegpref' => isset($form_data['seguradora_preferencia']) ? $form_data['seguradora_preferencia'] : '',
                'cValorpret' => isset($form_data['valor_preferencia']) ? $form_data['valor_preferencia'] : '',
                'cModalidade' => isset($form_data['modalidade_seguro']) ? $form_data['modalidade_seguro'] : '',
                'cSegant' => isset($form_data['seguradora_apolice']) ? $form_data['seguradora_apolice'] : '',
                'cCiapol' => isset($form_data['ci']) ? $form_data['ci'] : '',
            ];

            // Validação crítica do payload da oportunidade
            if (empty($opportunityPayload['name'])) {
                logDevWebhook('opportunity_validation_error', [
                    'field' => 'name',
                    'value' => $opportunityPayload['name'],
                    'original_name' => $name,
                    'payload' => $opportunityPayload,
                    'error' => 'Campo name da oportunidade está vazio'
                ], false);
                throw new Exception('Campo name da oportunidade é obrigatório');
            }

            logProdWebhook('opportunity_data_prepared', $opportunityPayload, true);
            logProdWebhook('espocrm_opportunity_request_details', [
                'espocrm_url' => $FLYINGDONKEYS_API_URL,
                'api_key' => substr($FLYINGDONKEYS_API_KEY, 0, 8) . '...',
                'endpoint' => 'Opportunity',
                'method' => 'POST',
                'payload' => $opportunityPayload,
                'lead_id' => $leadIdFlyingDonkeys
            ], true);

            $responseOpportunity = $client->request('POST', 'Opportunity', $opportunityPayload);
            $opportunityIdFlyingDonkeys = $responseOpportunity['id'];
            logDevWebhook('opportunity_created', ['opportunity_id' => $opportunityIdFlyingDonkeys], true);
        } catch (Exception $e) {
            $errorMessage = $e->getMessage();
            logDevWebhook('opportunity_exception', ['error' => $errorMessage], false);

            // Se erro 409 (duplicata), criar nova oportunidade com duplicate = yes
            if (strpos($errorMessage, '409') !== false || strpos($errorMessage, 'duplicate') !== false) {
                logDevWebhook('duplicate_opportunity_detected', ['creating_with_duplicate_yes' => true], true);

                $opportunityPayload['duplicate'] = 'yes';
                $responseOpportunity = $client->request('POST', 'Opportunity', $opportunityPayload);
                $opportunityIdFlyingDonkeys = $responseOpportunity['id'];
                logDevWebhook('duplicate_opportunity_created', ['opportunity_id' => $opportunityIdFlyingDonkeys], true);
            } else {
                logDevWebhook('real_error_creating_opportunity', ['error' => $errorMessage], false);
            }
        }
    } else {
        // ✅ V4: Se veio lead_id mas não opportunity_id → NÃO criar nova oportunidade (apenas atualização de lead)
        logDevWebhook('opportunity_skip_creation', [
            'reason' => 'lead_update_mode',
            'lead_id' => $leadIdFlyingDonkeys,
            'opportunity_id_received' => $opportunityIdFromPayload
        ], true);
    }

    // ✅ Retornar opportunity_id na resposta se disponível
    sendProdWebhookResponse(true, 'Lead e Oportunidade processados com sucesso', [
        'leadIdFlyingDonkeys' => $leadIdFlyingDonkeys,
        'opportunityIdFlyingDonkeys' => $opportunityIdFlyingDonkeys,
        'environment' => 'production',
        'api_version' => '2.0',
        'webhook' => 'flyingdonkeys-v2',
        'request_id' => $GLOBAL_REQUEST_ID
    ]);
} catch (Exception $e) {
    logProdWebhook('crm_error', [
        'error' => $e->getMessage(),
        'file' => $e->getFile(),
        'line' => $e->getLine(),
        'trace' => $e->getTraceAsString()
    ], false);

    // Em produção, retornar erro real
    sendProdWebhookResponse(false, 'Erro no CRM: ' . $e->getMessage(), [
        'error_details' => [
            'file' => $e->getFile(),
            'line' => $e->getLine(),
            'message' => $e->getMessage()
        ],
        'request_id' => $GLOBAL_REQUEST_ID
    ]);
}

logProdWebhook('webhook_completed', [
    'execution_time' => microtime(true) - $_SERVER['REQUEST_TIME_FLOAT'],
    'memory_peak' => memory_get_peak_usage(true)
], true);
