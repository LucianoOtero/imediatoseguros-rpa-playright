<?php

require_once __DIR__ . '/../vendor/autoload.php';

use RPA\Controllers\RPAController;
use RPA\Services\ConfigService;
use RPA\Services\LoggerService;
use RPA\Services\ValidationService;
use RPA\Services\RateLimitService;
use RPA\Services\SessionService;
use RPA\Services\MonitorService;
use RPA\Repositories\SessionRepository;

// Configuração de CORS
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type, Authorization');

// Responder a requisições OPTIONS
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit;
}

// Configurar content type
header('Content-Type: application/json; charset=utf-8');

try {
    // Inicializar serviços
    $config = new ConfigService();
    $logger = new LoggerService($config->get('logging', []));
    
    // Configurar validação
    $validationRules = $config->get('validation', []);
    $validationService = new ValidationService($validationRules);
    
    // Configurar rate limiting
    $rateLimitConfig = array_merge(
        $config->get('redis', []),
        $config->get('rate_limit', [])
    );
    $rateLimitService = new RateLimitService($rateLimitConfig);
    
    // Configurar repositório e serviços
    $rpaConfig = $config->get('rpa', []);
    $repository = new SessionRepository(
        $rpaConfig['sessions_path'] ?? '/opt/imediatoseguros-rpa/sessions',
        $rpaConfig['data_path'] ?? '/opt/imediatoseguros-rpa/rpa_data'
    );
    
    $sessionService = new SessionService(
        $repository,
        $logger,
        $rpaConfig['scripts_path'] ?? '/opt/imediatoseguros-rpa/scripts'
    );
    
    $monitorService = new MonitorService($repository, $logger);
    
    // Inicializar controller
    $controller = new RPAController(
        $sessionService,
        $monitorService,
        $config,
        $validationService,
        $rateLimitService,
        $logger
    );
    
    // Processar requisição
    $method = $_SERVER['REQUEST_METHOD'];
    $path = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
    $path = rtrim($path, '/');
    
    // Roteamento
    switch ($method) {
        case 'POST':
            if ($path === '/api/rpa/start' || $path === '/start') {
                $input = json_decode(file_get_contents('php://input'), true);
                $response = $controller->startRPA($input ?: []);
            } elseif ($path === '/api/rpa/cleanup' || $path === '/cleanup') {
                $response = $controller->cleanup();
            } else {
                $response = ['success' => false, 'error' => 'Endpoint não encontrado'];
            }
            break;
            
        case 'GET':
            if ($path === '/api/rpa/health' || $path === '/health') {
                $response = $controller->healthCheck();
            } elseif ($path === '/api/rpa/metrics' || $path === '/metrics') {
                $response = $controller->getMetrics();
            } elseif ($path === '/api/rpa/sessions' || $path === '/sessions') {
                $response = $controller->listSessions();
            } elseif (preg_match('/^\/api\/rpa\/status\/(.+)$/', $path, $matches) || 
                     preg_match('/^\/status\/(.+)$/', $path, $matches)) {
                $response = $controller->getStatus($matches[1]);
            } elseif (preg_match('/^\/api\/rpa\/monitor\/(.+)$/', $path, $matches) || 
                     preg_match('/^\/monitor\/(.+)$/', $path, $matches)) {
                $response = $controller->monitorSession($matches[1]);
            } elseif (preg_match('/^\/api\/rpa\/logs\/(.+)$/', $path, $matches) || 
                     preg_match('/^\/logs\/(.+)$/', $path, $matches)) {
                $limit = $_GET['limit'] ?? 100;
                $response = $controller->getLogs($matches[1], (int)$limit);
            } else {
                $response = ['success' => false, 'error' => 'Endpoint não encontrado'];
            }
            break;
            
        case 'DELETE':
            if (preg_match('/^\/api\/rpa\/stop\/(.+)$/', $path, $matches) || 
                preg_match('/^\/stop\/(.+)$/', $path, $matches)) {
                $response = $controller->stopSession($matches[1]);
            } else {
                $response = ['success' => false, 'error' => 'Endpoint não encontrado'];
            }
            break;
            
        default:
            $response = ['success' => false, 'error' => 'Método não permitido'];
            break;
    }
    
    // Retornar resposta
    echo json_encode($response, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
    
} catch (Exception $e) {
    // Log do erro
    error_log("RPA V4 Error: " . $e->getMessage());
    
    // Resposta de erro
    http_response_code(500);
    echo json_encode([
        'success' => false,
        'error' => 'Erro interno do servidor',
        'message' => $e->getMessage(),
        'timestamp' => date('Y-m-d H:i:s')
    ], JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
}
