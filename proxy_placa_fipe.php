<?php
header("Content-Type: application/json");
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Methods: GET, POST, OPTIONS");
header("Access-Control-Allow-Headers: Content-Type");

if ($_SERVER["REQUEST_METHOD"] === "OPTIONS") {
    http_response_code(200);
    exit;
}

$placa = $_GET["placa"] ?? "";
$token = "1696FBDDD9736D542D6958B1770B683EBBA1EFCCC4D0963A2A8A6FA9EFC29214";

if (empty($placa)) {
    http_response_code(400);
    echo json_encode(["error" => "Placa é obrigatória"]);
    exit;
}

// NOVO FORMATO: /placa/ABC1234/token/TOKEN (conforme sugerido pelo suporte)
$url = "https://api.placafipe.com.br/getplaca/placa/" . urlencode($placa) . "/token/" . urlencode($token);

// Usar cURL em vez de file_get_contents
$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $url);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_TIMEOUT, 30);
curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
curl_setopt($ch, CURLOPT_HTTPHEADER, [
    "Content-Type: application/json"
]);

$response = curl_exec($ch);
$httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
$error = curl_error($ch);
curl_close($ch);

if ($response === false || !empty($error)) {
    http_response_code(500);
    echo json_encode(["error" => "Erro ao consultar API: " . $error]);
    exit;
}

if ($httpCode !== 200) {
    http_response_code($httpCode);
    echo json_encode(["error" => "API retornou código: " . $httpCode]);
    exit;
}

echo $response;
?>
