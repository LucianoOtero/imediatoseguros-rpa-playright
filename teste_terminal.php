<?php
/**
 * TESTE SIMPLES NO TERMINAL
 * Testa se o RPA está funcionando e captura output
 */

echo "TESTE SIMPLES NO TERMINAL\n";
echo "=========================\n\n";

echo "1. Testando comando Python simples...\n";
$output = [];
$return_var = 0;
exec("python -c \"print(
Hello
from
Python)\"", $output, $return_var);
echo "Output: " . implode("\n", $output) . "\n";
echo "Codigo: $return_var\n\n";

echo "2. Testando RPA com parametros.json...\n";
$output2 = [];
$return_var2 = 0;
exec("python executar_rpa_imediato_playwright.py --config parametros.json", $output2, $return_var2);
echo "Output capturado:\n";
foreach ($output2 as $line) {
    echo $line . "\n";
}
echo "Codigo: $return_var2\n\n";

echo "3. Verificando se ha JSON no output...\n";
$full_output = implode("\n", $output2);
$json_start = strpos($full_output, "{");
if ($json_start !== false) {
    echo "JSON encontrado na posicao: $json_start\n";
    $json_content = substr($full_output, $json_start);
    $resultado = json_decode($json_content, true);
    if ($resultado) {
        echo "JSON valido!\n";
        echo "Status: " . ($resultado["status"] ?? "N/A") . "\n";
        if (isset($resultado["progresso"])) {
            echo "ProgressTracker encontrado!\n";
            echo "Etapa: " . ($resultado["progresso"]["etapa_atual"] ?? "N/A") . "\n";
        }
    } else {
        echo "JSON invalido\n";
    }
} else {
    echo "JSON nao encontrado\n";
}

echo "\nTESTE CONCLUIDO!\n";
?>
