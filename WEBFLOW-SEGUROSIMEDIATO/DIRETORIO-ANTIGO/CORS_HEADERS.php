
// ==================== CONFIGURAÇÃO CORS ====================
// Permitir requisições do Webflow staging e dev.bpsegurosimediato.com.br
$allowed_origins = array(
    'https://segurosimediato-8119bf26e77bf4ff336a58e.webflow.io',
    'https://dev.bpsegurosimediato.com.br',
    'http://localhost',
    'http://localhost:8080'
);

$origin = isset($_SERVER['HTTP_ORIGIN']) ? $_SERVER['HTTP_ORIGIN'] : '';
if (in_array($origin, $allowed_origins)) {
    header('Access-Control-Allow-Origin: ' . $origin);
}

header('Access-Control-Allow-Methods: POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type, X-Requested-With, Authorization');
header('Access-Control-Allow-Credentials: true');
header('Access-Control-Max-Age: 86400'); // 24 horas

// Responder a requisições OPTIONS (preflight)
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit(0);
}
// ==================== FIM CONFIGURAÇÃO CORS ====================











