<?php
// TESTE SIMPLES DE CAPTURA DE OUTPUT
echo "🔍 TESTE SIMPLES DE CAPTURA\n";
echo "==========================\n\n";

echo "📋 Testando comando simples...\n";
$output = [];
$return_var = 0;
exec("echo 
Teste
de
output", $output, $return_var);

echo "📊 Output capturado:\n";
print_r($output);
echo "🔢 Código de retorno: $return_var\n\n";

echo "📋 Testando comando Python...\n";
$output2 = [];
$return_var2 = 0;
exec("python -c \"print(Hello
from
Python)\"", $output2, $return_var2);

echo "📊 Output Python capturado:\n";
print_r($output2);
echo "🔢 Código de retorno: $return_var2\n\n";

echo "📋 Testando RPA com visualizar_mensagens=true...\n";
$config = [
    "configuracao" => [
        "visualizar_mensagens" => true
    ],
    "tipo_veiculo" => "carro",
    "placa" => "EYQ4J41"
];
file_put_contents("teste_config.json", json_encode($config));

$output3 = [];
$return_var3 = 0;
exec("python executar_rpa_imediato_playwright.py --config teste_config.json", $output3, $return_var3);

echo "📊 Output RPA capturado:\n";
print_r($output3);
echo "🔢 Código de retorno: $return_var3\n\n";

// Limpar
if (file_exists("teste_config.json")) {
    unlink("teste_config.json");
}
?>
