<?php

/**
 * SIMULADOR OCTADESK MELHORADO - DESENVOLVIMENTO
 * dev/octadesk-simulator/index.php
 * 
 * Simulador que segue padrões REST e validações básicas
 * para garantir compatibilidade com API real do Octadesk
 */

// Configurações CORS
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type, X-Api-Key, Accept');
header('Content-Type: application/json; charset=utf-8');

// Responder a requisições OPTIONS
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit(0);
}

// Função para log
function logSimulator($action, $data = null) {
    $logFile = __DIR__ . '/../logs/octadesk_simulator.txt';
    $timestamp = date('Y-m-d H:i:s');
    $logEntry = "[{$timestamp}] [SIMULATOR] {$action}";
    if ($data !== null) {
        $logEntry .= " | Data: " . json_encode($data, JSON_UNESCAPED_UNICODE);
    }
    $logEntry .= PHP_EOL;
    file_put_contents($logFile, $logEntry, FILE_APPEND | LOCK_EX);
}

// Função para gerar ID simulado
function generateSimulatedId($prefix = 'sim') {
    return $prefix . '_' . uniqid() . '_' . substr(md5(microtime()), 0, 8);
}

// Função para validar campos obrigatórios
function validateRequiredFields($data, $requiredFields) {
    $missing = [];
    foreach ($requiredFields as $field) {
        if (!isset($data[$field]) || empty($data[$field])) {
            $missing[] = $field;
        }
    }
    return $missing;
}

// Função para validar valores enum
function validateEnumValue($value, $allowedValues) {
    return in_array($value, $allowedValues);
}

// Obter dados da requisição
$input = file_get_contents('php://input');
$headers = getallheaders();
$method = $_SERVER['REQUEST_METHOD'];
$path = $_SERVER['REQUEST_URI'];

logSimulator('request_received', [
    'method' => $method,
    'path' => $path,
    'headers' => $headers,
    'input_length' => strlen($input)
]);

// Verificar API Key
$apiKey = $headers['X-Api-Key'] ?? '';
if ($apiKey !== 'dev_octadesk_key_12345') {
    logSimulator('invalid_api_key', ['received' => $apiKey]);
    http_response_code(401);
    echo json_encode([
        'success' => false,
        'error' => 'Invalid API Key',
        'message' => 'API Key inválida para o simulador',
        'code' => 'INVALID_API_KEY'
    ]);
    exit;
}

// Roteamento baseado no path
$pathParts = explode('/', trim($path, '/'));
$endpoint = end($pathParts);

switch ($endpoint) {
    case 'contacts':
        if ($method === 'POST') {
            // Simular criação de contato
            $data = json_decode($input, true);
            
            if (!$data) {
                http_response_code(400);
                echo json_encode([
                    'success' => false,
                    'error' => 'Invalid JSON',
                    'code' => 'INVALID_JSON'
                ]);
                exit;
            }
            
            // Validar campos obrigatórios
            $requiredFields = ['name', 'email'];
            $missingFields = validateRequiredFields($data, $requiredFields);
            
            if (!empty($missingFields)) {
                http_response_code(400);
                echo json_encode([
                    'success' => false,
                    'error' => 'Missing required fields',
                    'message' => 'Campos obrigatórios: ' . implode(', ', $missingFields),
                    'code' => 'MISSING_REQUIRED_FIELDS',
                    'missing_fields' => $missingFields
                ]);
                exit;
            }
            
            // Validar formato de email
            if (!filter_var($data['email'], FILTER_VALIDATE_EMAIL)) {
                http_response_code(400);
                echo json_encode([
                    'success' => false,
                    'error' => 'Invalid email format',
                    'code' => 'INVALID_EMAIL_FORMAT'
                ]);
                exit;
            }
            
            $contactId = generateSimulatedId('contact');
            
            logSimulator('contact_created', [
                'contact_id' => $contactId,
                'data' => $data
            ]);
            
            http_response_code(201);
            echo json_encode([
                'success' => true,
                'message' => 'Contato criado com sucesso no simulador',
                'data' => [
                    'id' => $contactId,
                    'name' => $data['name'],
                    'email' => $data['email'],
                    'phone' => $data['phone'] ?? null,
                    'tags' => $data['tags'] ?? [],
                    'custom_fields' => $data['custom_fields'] ?? [],
                    'created_at' => date('Y-m-d H:i:s'),
                    'updated_at' => date('Y-m-d H:i:s'),
                    'simulator' => true
                ]
            ]);
        } else {
            http_response_code(405);
            echo json_encode([
                'success' => false,
                'error' => 'Method not allowed',
                'code' => 'METHOD_NOT_ALLOWED'
            ]);
        }
        break;
        
    case 'conversations':
        if ($method === 'POST') {
            // Simular criação de conversa
            $data = json_decode($input, true);
            
            if (!$data) {
                http_response_code(400);
                echo json_encode([
                    'success' => false,
                    'error' => 'Invalid JSON',
                    'code' => 'INVALID_JSON'
                ]);
                exit;
            }
            
            // Validar campos obrigatórios
            $requiredFields = ['contact_id', 'subject'];
            $missingFields = validateRequiredFields($data, $requiredFields);
            
            if (!empty($missingFields)) {
                http_response_code(400);
                echo json_encode([
                    'success' => false,
                    'error' => 'Missing required fields',
                    'message' => 'Campos obrigatórios: ' . implode(', ', $missingFields),
                    'code' => 'MISSING_REQUIRED_FIELDS',
                    'missing_fields' => $missingFields
                ]);
                exit;
            }
            
            // Validar status se fornecido
            if (isset($data['status'])) {
                $allowedStatuses = ['open', 'closed', 'pending', 'resolved'];
                if (!validateEnumValue($data['status'], $allowedStatuses)) {
                    http_response_code(400);
                    echo json_encode([
                        'success' => false,
                        'error' => 'Invalid status value',
                        'message' => 'Status deve ser um dos: ' . implode(', ', $allowedStatuses),
                        'code' => 'INVALID_STATUS_VALUE'
                    ]);
                    exit;
                }
            }
            
            $conversationId = generateSimulatedId('conv');
            
            logSimulator('conversation_created', [
                'conversation_id' => $conversationId,
                'data' => $data
            ]);
            
            http_response_code(201);
            echo json_encode([
                'success' => true,
                'message' => 'Conversa criada com sucesso no simulador',
                'data' => [
                    'id' => $conversationId,
                    'contact_id' => $data['contact_id'],
                    'subject' => $data['subject'],
                    'status' => $data['status'] ?? 'open',
                    'created_at' => date('Y-m-d H:i:s'),
                    'updated_at' => date('Y-m-d H:i:s'),
                    'simulator' => true
                ]
            ]);
        } else {
            http_response_code(405);
            echo json_encode([
                'success' => false,
                'error' => 'Method not allowed',
                'code' => 'METHOD_NOT_ALLOWED'
            ]);
        }
        break;
        
    case 'messages':
        if ($method === 'POST') {
            // Simular envio de mensagem
            $data = json_decode($input, true);
            
            if (!$data) {
                http_response_code(400);
                echo json_encode([
                    'success' => false,
                    'error' => 'Invalid JSON',
                    'code' => 'INVALID_JSON'
                ]);
                exit;
            }
            
            // Validar campos obrigatórios
            $requiredFields = ['conversation_id', 'message'];
            $missingFields = validateRequiredFields($data, $requiredFields);
            
            if (!empty($missingFields)) {
                http_response_code(400);
                echo json_encode([
                    'success' => false,
                    'error' => 'Missing required fields',
                    'message' => 'Campos obrigatórios: ' . implode(', ', $missingFields),
                    'code' => 'MISSING_REQUIRED_FIELDS',
                    'missing_fields' => $missingFields
                ]);
                exit;
            }
            
            // Validar tipo de mensagem se fornecido
            if (isset($data['type'])) {
                $allowedTypes = ['text', 'image', 'file', 'audio', 'video'];
                if (!validateEnumValue($data['type'], $allowedTypes)) {
                    http_response_code(400);
                    echo json_encode([
                        'success' => false,
                        'error' => 'Invalid message type',
                        'message' => 'Tipo deve ser um dos: ' . implode(', ', $allowedTypes),
                        'code' => 'INVALID_MESSAGE_TYPE'
                    ]);
                    exit;
                }
            }
            
            // Validar sender se fornecido
            if (isset($data['sender'])) {
                $allowedSenders = ['system', 'user', 'agent', 'bot'];
                if (!validateEnumValue($data['sender'], $allowedSenders)) {
                    http_response_code(400);
                    echo json_encode([
                        'success' => false,
                        'error' => 'Invalid sender value',
                        'message' => 'Sender deve ser um dos: ' . implode(', ', $allowedSenders),
                        'code' => 'INVALID_SENDER_VALUE'
                    ]);
                    exit;
                }
            }
            
            $messageId = generateSimulatedId('msg');
            
            logSimulator('message_sent', [
                'message_id' => $messageId,
                'data' => $data
            ]);
            
            http_response_code(201);
            echo json_encode([
                'success' => true,
                'message' => 'Mensagem enviada com sucesso no simulador',
                'data' => [
                    'id' => $messageId,
                    'conversation_id' => $data['conversation_id'],
                    'message' => $data['message'],
                    'type' => $data['type'] ?? 'text',
                    'sender' => $data['sender'] ?? 'system',
                    'sent_at' => date('Y-m-d H:i:s'),
                    'simulator' => true
                ]
            ]);
        } else {
            http_response_code(405);
            echo json_encode([
                'success' => false,
                'error' => 'Method not allowed',
                'code' => 'METHOD_NOT_ALLOWED'
            ]);
        }
        break;
        
    default:
        // Endpoint de status
        logSimulator('status_requested');
        echo json_encode([
            'success' => true,
            'message' => 'Simulador OctaDesk funcionando',
            'version' => '2.0.0-dev',
            'endpoints' => [
                'POST /api/v1/contacts' => 'Criar contato (campos obrigatórios: name, email)',
                'POST /api/v1/conversations' => 'Criar conversa (campos obrigatórios: contact_id, subject)',
                'POST /api/v1/messages' => 'Enviar mensagem (campos obrigatórios: conversation_id, message)'
            ],
            'validation' => [
                'email_format' => 'Validado com FILTER_VALIDATE_EMAIL',
                'status_values' => ['open', 'closed', 'pending', 'resolved'],
                'message_types' => ['text', 'image', 'file', 'audio', 'video'],
                'sender_values' => ['system', 'user', 'agent', 'bot']
            ],
            'timestamp' => date('Y-m-d H:i:s')
        ]);
        break;
}

logSimulator('response_sent', [
    'status_code' => http_response_code(),
    'endpoint' => $endpoint
]);








