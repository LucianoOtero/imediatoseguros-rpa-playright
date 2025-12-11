<?php

/**
 * SIMULADOR OCTADESK - DESENVOLVIMENTO
 * dev/octadesk-simulator/index.php
 * 
 * Simulador simples para testes de integração OctaDesk
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
        'message' => 'API Key inválida para o simulador'
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
                    'error' => 'Invalid JSON'
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
                    'name' => $data['name'] ?? 'Nome não informado',
                    'email' => $data['email'] ?? 'email@nao.informado.com',
                    'phone' => $data['phone'] ?? 'Telefone não informado',
                    'tags' => $data['tags'] ?? [],
                    'custom_fields' => $data['custom_fields'] ?? [],
                    'created_at' => date('Y-m-d H:i:s'),
                    'simulator' => true
                ]
            ]);
        } else {
            http_response_code(405);
            echo json_encode([
                'success' => false,
                'error' => 'Method not allowed'
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
                    'error' => 'Invalid JSON'
                ]);
                exit;
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
                    'contact_id' => $data['contact_id'] ?? 'unknown',
                    'subject' => $data['subject'] ?? 'Assunto não informado',
                    'status' => $data['status'] ?? 'open',
                    'created_at' => date('Y-m-d H:i:s'),
                    'simulator' => true
                ]
            ]);
        } else {
            http_response_code(405);
            echo json_encode([
                'success' => false,
                'error' => 'Method not allowed'
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
                    'error' => 'Invalid JSON'
                ]);
                exit;
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
                    'conversation_id' => $data['conversation_id'] ?? 'unknown',
                    'message' => $data['message'] ?? 'Mensagem não informada',
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
                'error' => 'Method not allowed'
            ]);
        }
        break;
        
    default:
        // Endpoint de status
        logSimulator('status_requested');
        echo json_encode([
            'success' => true,
            'message' => 'Simulador OctaDesk funcionando',
            'version' => '1.0.0-dev',
            'endpoints' => [
                'POST /api/v1/contacts' => 'Criar contato',
                'POST /api/v1/conversations' => 'Criar conversa',
                'POST /api/v1/messages' => 'Enviar mensagem'
            ],
            'timestamp' => date('Y-m-d H:i:s')
        ]);
        break;
}

logSimulator('response_sent', [
    'status_code' => http_response_code(),
    'endpoint' => $endpoint
]);








