<?php
/**
 * Teste para chamar add_travelangels.php exatamente como o JavaScript/RPA faz
 * Usando dados do parametros.json
 */

// Dados do parametros.json convertidos para o formato do RPA
$webhook_data = [
    'data' => [
        'NOME' => 'ALEX KAMINSKI',
        'DDD-CELULAR' => '11',
        'CELULAR' => '953288466',
        'Email' => 'alex.kaminski@imediatoseguros.com.br',
        'CEP' => '03317-000',
        'CPF' => '97137189768',
        'MARCA' => 'TOYOTA',
        'PLACA' => 'EYQ4J41',
        'VEICULO' => 'TOYOTA',
        'ANO' => '2009',
        'GCLID_FLD' => '',
        'SEXO' => 'Masculino',
        'DATA-DE-NASCIMENTO' => '25/04/1970',
        'ESTADO-CIVIL' => 'Casado ou Uniao Estavel',
        'produto' => 'seguro-auto',
        'landing_url' => '',
        'utm_source' => '',
        'utm_campaign' => ''
    ],
    'd' => date('c'),
    'name' => 'Formulário de Cotação RPA'
];

// Teste de conectividade básica
function testConnectivity() {
    echo "🔍 TESTE DE CONECTIVIDADE\n";
    
    // Teste 1: Ping básico
    echo "1. Testando ping para travelangels.com.br...\n";
    $ping_result = shell_exec("ping -n 1 travelangels.com.br 2>&1");
    echo "Ping result: " . $ping_result . "\n";
    
    // Teste 2: Teste de porta HTTPS
    echo "2. Testando porta 443...\n";
    $socket = @fsockopen("travelangels.com.br", 443, $errno, $errstr, 10);
    if ($socket) {
        echo "✅ Porta 443: Aberta\n";
        fclose($socket);
    } else {
        echo "❌ Porta 443: Fechada ou bloqueada\n";
        echo "Erro: $errstr ($errno)\n";
    }
    
    // Teste 3: Teste SSL básico
    echo "3. Testando SSL...\n";
    $context = stream_context_create([
        "ssl" => [
            "verify_peer" => false,
            "verify_peer_name" => false,
        ]
    ]);
    
    $ssl_socket = @stream_socket_client("ssl://travelangels.com.br:443", $errno, $errstr, 10, STREAM_CLIENT_CONNECT, $context);
    if ($ssl_socket) {
        echo "✅ SSL: Conexão estabelecida\n";
        fclose($ssl_socket);
    } else {
        echo "❌ SSL: Falha na conexão\n";
        echo "Erro: $errstr ($errno)\n";
    }
    
    // Teste 4: Teste HTTP básico
    echo "4. Testando requisição HTTP básica...\n";
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, "https://travelangels.com.br");
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_TIMEOUT, 10);
    curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 5);
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
    curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, false);
    curl_setopt($ch, CURLOPT_NOBODY, true); // HEAD request only
    
    $result = curl_exec($ch);
    $http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    $error = curl_error($ch);
    curl_close($ch);
    
    if ($result !== false && $http_code > 0) {
        echo "✅ HTTP: Resposta recebida (HTTP $http_code)\n";
    } else {
        echo "❌ HTTP: Falha na requisição\n";
        echo "HTTP Code: $http_code\n";
        echo "CURL Error: $error\n";
    }
}

// Teste direto da API EspoCRM
function testEspoCRM() {
    echo "🔍 TESTE DIRETO DA API ESPOCRM\n";
    
    $client = new EspoApiClient('https://travelangels.com.br');
    $client->setApiKey('7a6c08d438ee131971f561fd836b5e15');
    
    try {
        $response = $client->request('POST', 'Lead', [
            'firstName' => 'TESTE RPA ' . date('Y-m-d H:i:s'),
            'emailAddress' => 'teste.rpa.' . time() . '@imediatoseguros.com.br',
            'cCelular' => '11999999999',
            'addressPostalCode' => '03317-000',
            'cCpftext' => '99999999999',
            'cMarca' => 'TOYOTA',
            'cPlaca' => 'TEST1234',
            'cAnoMod' => '2025',
            'cGclid' => '',
            'cWebpage' => 'Formulário de Cotação RPA',
        ]);
        
        echo "✅ EspoCRM: Sucesso\n";
        echo "Response: " . json_encode($response) . "\n";
        
    } catch (Exception $e) {
        echo "❌ EspoCRM: Erro\n";
        echo "Error: " . $e->getMessage() . "\n";
        echo "Code: " . $e->getCode() . "\n";
        echo "File: " . $e->getFile() . "\n";
        echo "Line: " . $e->getLine() . "\n";
        echo "Trace: " . $e->getTraceAsString() . "\n";
    }
}

// Classe EspoApiClient (copiada do servidor)
class EspoApiClient
{
    private $url;
    private $userName = null;
    private $password = null;
    protected $urlPath = '/api/v1/';
    private $lastCh;
    private $lastResponse;
    private $apiKey = null;
    private $secretKey = null;

    public function __construct($url = null, $userName = null, $password = null)
    {
        if (isset($url)) {
            $this->url = $url;
        }
        if (isset($userName)) {
            $this->userName = $userName;
        }
        if (isset($password)) {
            $this->password = $password;
        }
    }

    public function setUrl($url)
    {
        $this->url = $url;
    }

    public function setUserName($userName)
    {
        $this->userName = $userName;
    }

    public function setPassword($password)
    {
        $this->password = $password;
    }

    public function setApiKey($apiKey)
    {
        $this->apiKey = $apiKey;
    }

    public function setSecretKey($secretKey)
    {
        $this->secretKey = $secretKey;
    }

    public function request($method, $action, ?array $data = null)
    {
        $method = strtoupper($method);
        $this->checkParams();
        $this->lastResponse = null;
        $this->lastCh = null;
        $url = $this->normalizeUrl($action);

        $ch = curl_init($url);
        $headerList = [];

        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        if ($this->userName && $this->password) {
            curl_setopt($ch, CURLOPT_USERPWD, $this->userName.':'.$this->password);
            curl_setopt($ch, CURLOPT_HTTPAUTH, CURLAUTH_BASIC);
        } else if ($this->apiKey && $this->secretKey) {
            $string = $method . ' /' . $action;
            $authPart = base64_encode($this->apiKey . ':' . hash_hmac('sha256', $string, $this->secretKey, true));
            $authHeader = 'X-Hmac-Authorization: ' .  $authPart;
            $headerList[] = $authHeader;
        } else if ($this->apiKey) {
            $authHeader = 'X-Api-Key: ' .  $this->apiKey;
            $headerList[] = $authHeader;
        }

        curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
        curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, false);
        curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
        curl_setopt($ch, CURLOPT_HEADER, true);

        if ($method != 'GET') {
            curl_setopt($ch, CURLOPT_CUSTOMREQUEST, $method);
        }

        if (isset($data)) {
            if ($method == 'GET') {
                curl_setopt($ch, CURLOPT_URL, $url. '?' . http_build_query($data));
            } else {
                $payload = json_encode($data);
                curl_setopt($ch, CURLOPT_POSTFIELDS, $payload);
                $headerList[] = 'Content-Type: application/json';
                $headerList[] = 'Content-Length: ' . strlen($payload);
            }
        }

        if (!empty($headerList)) {
            curl_setopt($ch, CURLOPT_HTTPHEADER, $headerList);
        }

        $this->lastResponse = curl_exec($ch);
        $this->lastCh = $ch;

        // Debug: mostrar informações da requisição
        echo "🔍 DEBUG ESPOCRM:\n";
        echo "URL: " . $url . "\n";
        echo "Method: " . $method . "\n";
        echo "Headers: " . json_encode($headerList) . "\n";
        echo "Payload: " . (isset($data) ? json_encode($data) : 'null') . "\n";
        echo "Response Code: " . curl_getinfo($ch, CURLINFO_HTTP_CODE) . "\n";
        echo "Response: " . $this->lastResponse . "\n";
        echo "CURL Error: " . curl_error($ch) . "\n";

        $parsedResponse = $this->parseResponce($this->lastResponse);
        $responseCode = $this->getResponseHttpCode();
        $responseContentType = $this->getResponseContentType();

        if ($responseCode == 200) {
            curl_close($ch);
            if ($responseContentType === 'application/json') {
                return json_decode($parsedResponse['body'], true);
            }
            return $parsedResponse['body'];
        }

        $header = $this->normalizeHeader($parsedResponse['header']);
        $errorMessage = !empty($header['X-Status-Reason']) ? $header['X-Status-Reason'] : $parsedResponse['body'];

        curl_close($ch);
        throw new \Exception($errorMessage, $responseCode);
    }

    public function getResponseContentType()
    {
        return $this->getInfo(CURLINFO_CONTENT_TYPE);
    }

    public function getResponseTotalTime()
    {
        return $this->getInfo(CURLINFO_TOTAL_TIME);
    }

    public function getResponseHttpCode()
    {
        return $this->getInfo(CURLINFO_HTTP_CODE);
    }

    protected function normalizeUrl($action)
    {
        return $this->url . $this->urlPath . $action;
    }

    protected function checkParams()
    {
        $paramList = ['url'];
        foreach ($paramList as $name) {
            if (empty($this->$name)) {
                throw new \Exception('EspoClient: Parameter "'.$name.'" is not defined.');
            }
        }
        return true;
    }

    protected function getInfo($option)
    {
        if (isset($this->lastCh)) {
            return curl_getinfo($this->lastCh, $option);
        }
    }

    protected function parseResponce($response)
    {
        $headerSize = $this->getInfo(CURLINFO_HEADER_SIZE);
        return [
            'header' => trim( substr($response, 0, $headerSize) ),
            'body' => substr($response, $headerSize),
        ];
    }

    protected function normalizeHeader($header)
    {
        preg_match_all('/(.*): (.*)\r\n/', $header, $matches);
        $headerArray = array();
        foreach ($matches[1] as $index => $name) {
            if (isset($matches[2][$index])) {
                $headerArray[$name] = trim($matches[2][$index]);
            }
        }
        return $headerArray;
    }
}

// Função para chamar webhook (igual ao RPAController)
function callWebhook($url, $data) {
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
    curl_setopt($ch, CURLOPT_HTTPHEADER, [
        'Content-Type: application/json',
        'User-Agent: RPA-API-v6.9.1'
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

// Executar testes
echo "🧪 TESTE 1: Conectividade básica\n";
testConnectivity();

echo "\n" . str_repeat("=", 60) . "\n\n";

echo "🧪 TESTE 2: Chamada direta à API EspoCRM\n";
testEspoCRM();

echo "\n" . str_repeat("=", 60) . "\n\n";

echo "🧪 TESTE 3: Chamando add_teste_travelangels.php\n";
echo "📤 Dados enviados:\n";
echo json_encode($webhook_data, JSON_PRETTY_PRINT) . "\n\n";

// Chamar o endpoint de teste
$result = callWebhook('https://mdmidia.com.br/add_teste_travelangels.php', $webhook_data);

echo "📊 RESULTADO:\n";
echo "Status: " . ($result['success'] ? '✅ SUCESSO' : '❌ ERRO') . "\n";
echo "HTTP Code: " . $result['http_code'] . "\n";
echo "Response: " . $result['response'] . "\n";

if (!empty($result['error'])) {
    echo "Error: " . $result['error'] . "\n";
}

echo "\n🔍 Verifique o log detalhado em: https://mdmidia.com.br/logs_teste_travelangels.txt\n";
?>
