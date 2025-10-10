<?php
// arquivo: teste_ph3a_performance.php
// Projeto: Teste de Performance da API PH3A
// Data: 2025-10-09
// Descrição: Testa 54 CPFs na API PH3A e mede tempos de execução

// Configurações
$ph3a_url = 'https://mdmidia.com.br/cpf-validate.php';
$timeout_total = 60;        // 60 segundos total
$timeout_conexao = 15;       // 15 segundos conexão
$log_file = 'ph3a_performance_test_' . date('Y-m-d_H-i-s') . '.log';

// Lista de CPFs para teste
$cpfs = [
    '675.624.188-53',
    '035.607.930-92',
    '123.399.619-39',
    '012.830.634-33',
    '355.335.208-64',
    '054.726.178-04',
    '097.623.737-74',
    '204.959.228-03',
    '317.241.418-30',
    '132.792.869-80',
    '636.211.691-72',
    '043.219.508-48',
    '022.084.441-08',
    '187.491.238-66',
    '319.764.208-22',
    '279.479.658-54',
    '439.340.038-00',
    '568.730.429-00',
    '144.552.437-63',
    '13149082862',
    '482.010.228-15',
    '907.793.120-15',
    '344.174.888-35',
    '505.350.198-07',
    '164.690.418-41',
    '247.553.848-18',
    '220.680.348-83',
    '012.350.883-59',
    '082.353.059-09',
    '343.066.358-05',
    '259.103.768-02',
    '430.808.008-85',
    '481.167.248-86',
    '146.082.908-51',
    '779.284.589-34',
    '054.616.917-14',
    '291.286.838-62',
    '075.391.706-89',
    '038.943.749-26',
    '187.711.108-28',
    '806.560.058-15',
    '130.673.849-03',
    '104.552.738-63',
    '416.080.498-50',
    '087.451.678-18',
    '195.701.177-70',
    '486.152.007-00',
    '761.344.900-91',
    '087.654.389-55',
    '137-917-547-00',
    '530.196.158-60',
    '131.061.338-99',
    '089.687.924-02',
    '136.277.187-20'
];

// Função para chamar API PH3A
function callPH3AApi($cpf, $url, $timeout_total, $timeout_conexao) {
    $start_time = microtime(true);
    
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode(['cpf' => $cpf]));
    curl_setopt($ch, CURLOPT_HTTPHEADER, [
        'Content-Type: application/json',
        'User-Agent: PH3A-Performance-Test-v1.0'
    ]);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_TIMEOUT, $timeout_total);
    curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, $timeout_conexao);
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
    
    $response = curl_exec($ch);
    $http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    $error = curl_error($ch);
    $connect_time = curl_getinfo($ch, CURLINFO_CONNECT_TIME);
    $total_time = curl_getinfo($ch, CURLINFO_TOTAL_TIME);
    curl_close($ch);
    
    $execution_time = microtime(true) - $start_time;
    
    return [
        'success' => $http_code >= 200 && $http_code < 300,
        'http_code' => $http_code,
        'response' => $response,
        'error' => $error,
        'connect_time' => $connect_time,
        'total_time' => $total_time,
        'execution_time' => $execution_time
    ];
}

// Função para log
function writeLog($message, $log_file) {
    $timestamp = date('Y-m-d H:i:s');
    $log_entry = "[$timestamp] $message\n";
    file_put_contents($log_file, $log_entry, FILE_APPEND | LOCK_EX);
    echo $log_entry;
}

// Iniciar teste
echo "🚀 INICIANDO TESTE DE PERFORMANCE DA API PH3A\n";
echo "===============================================\n";
echo "URL: $ph3a_url\n";
echo "Timeout Total: {$timeout_total}s\n";
echo "Timeout Conexão: {$timeout_conexao}s\n";
echo "Total de CPFs: " . count($cpfs) . "\n";
echo "Arquivo de Log: $log_file\n";
echo "===============================================\n\n";

writeLog("INICIANDO TESTE DE PERFORMANCE DA API PH3A", $log_file);
writeLog("URL: $ph3a_url", $log_file);
writeLog("Timeout Total: {$timeout_total}s", $log_file);
writeLog("Timeout Conexão: {$timeout_conexao}s", $log_file);
writeLog("Total de CPFs: " . count($cpfs), $log_file);
writeLog("===============================================", $log_file);

// Estatísticas
$stats = [
    'total_tests' => 0,
    'successful' => 0,
    'failed' => 0,
    'timeouts' => 0,
    'total_time' => 0,
    'min_time' => PHP_FLOAT_MAX,
    'max_time' => 0,
    'times' => []
];

// Executar testes
foreach ($cpfs as $index => $cpf) {
    $test_number = $index + 1;
    echo "📋 Teste $test_number/54: CPF $cpf\n";
    
    $result = callPH3AApi($cpf, $ph3a_url, $timeout_total, $timeout_conexao);
    
    // Atualizar estatísticas
    $stats['total_tests']++;
    $stats['total_time'] += $result['execution_time'];
    $stats['times'][] = $result['execution_time'];
    
    if ($result['execution_time'] < $stats['min_time']) {
        $stats['min_time'] = $result['execution_time'];
    }
    
    if ($result['execution_time'] > $stats['max_time']) {
        $stats['max_time'] = $result['execution_time'];
    }
    
    if ($result['success']) {
        $stats['successful']++;
        
        // Tentar decodificar resposta JSON
        $json_response = json_decode($result['response'], true);
        
        if ($json_response) {
            $codigo = $json_response['codigo'] ?? 'N/A';
            $mensagem = $json_response['mensagem'] ?? 'N/A';
            $dados = $json_response['data'] ?? [];
            
            echo "✅ Sucesso: " . round($result['execution_time'], 3) . "s (HTTP {$result['http_code']})\n";
            echo "   Código: $codigo\n";
            echo "   Mensagem: $mensagem\n";
            
            if (!empty($dados)) {
                $sexo = $dados['sexo'] ?? 'N/A';
                $estado_civil = $dados['estado_civil'] ?? 'N/A';
                $data_nascimento = $dados['data_nascimento'] ?? 'N/A';
                
                echo "   Dados: Sexo=$sexo, Estado Civil=$estado_civil, Data Nascimento=$data_nascimento\n";
            }
            
            writeLog("TESTE $test_number: CPF $cpf - SUCESSO - Tempo: " . round($result['execution_time'], 3) . "s - HTTP: {$result['http_code']} - Código: $codigo - Mensagem: $mensagem", $log_file);
            
            if (!empty($dados)) {
                writeLog("TESTE $test_number: Dados retornados - Sexo: {$dados['sexo']} - Estado Civil: {$dados['estado_civil']} - Data Nascimento: {$dados['data_nascimento']}", $log_file);
            }
        } else {
            echo "✅ Sucesso: " . round($result['execution_time'], 3) . "s (HTTP {$result['http_code']}) - Resposta não é JSON válido\n";
            writeLog("TESTE $test_number: CPF $cpf - SUCESSO - Tempo: " . round($result['execution_time'], 3) . "s - HTTP: {$result['http_code']} - Resposta não é JSON válido", $log_file);
        }
    } else {
        $stats['failed']++;
        
        if (strpos($result['error'], 'timeout') !== false) {
            $stats['timeouts']++;
            echo "⏰ Timeout: " . round($result['execution_time'], 3) . "s - {$result['error']}\n";
            writeLog("TESTE $test_number: CPF $cpf - TIMEOUT - Tempo: " . round($result['execution_time'], 3) . "s - Erro: {$result['error']}", $log_file);
        } else {
            echo "❌ Falha: " . round($result['execution_time'], 3) . "s - HTTP {$result['http_code']} - {$result['error']}\n";
            writeLog("TESTE $test_number: CPF $cpf - FALHA - Tempo: " . round($result['execution_time'], 3) . "s - HTTP: {$result['http_code']} - Erro: {$result['error']}", $log_file);
        }
    }
    
    echo "\n";
    
    // Pequena pausa entre testes para não sobrecarregar o servidor
    usleep(100000); // 0.1 segundo
}

// Calcular estatísticas finais
$stats['avg_time'] = $stats['total_time'] / $stats['total_tests'];
$stats['success_rate'] = ($stats['successful'] / $stats['total_tests']) * 100;

// Ordenar tempos para calcular mediana
sort($stats['times']);
$median_index = floor(count($stats['times']) / 2);
$stats['median_time'] = $stats['times'][$median_index];

// Exibir estatísticas finais
echo "📊 ESTATÍSTICAS FINAIS\n";
echo "======================\n";
echo "Total de Testes: {$stats['total_tests']}\n";
echo "Sucessos: {$stats['successful']} (" . round($stats['success_rate'], 1) . "%)\n";
echo "Falhas: {$stats['failed']}\n";
echo "Timeouts: {$stats['timeouts']}\n";
echo "Tempo Total: " . round($stats['total_time'], 3) . "s\n";
echo "Tempo Médio: " . round($stats['avg_time'], 3) . "s\n";
echo "Tempo Mínimo: " . round($stats['min_time'], 3) . "s\n";
echo "Tempo Máximo: " . round($stats['max_time'], 3) . "s\n";
echo "Tempo Mediano: " . round($stats['median_time'], 3) . "s\n";
echo "======================\n";

// Log das estatísticas finais
writeLog("ESTATÍSTICAS FINAIS", $log_file);
writeLog("Total de Testes: {$stats['total_tests']}", $log_file);
writeLog("Sucessos: {$stats['successful']} (" . round($stats['success_rate'], 1) . "%)", $log_file);
writeLog("Falhas: {$stats['failed']}", $log_file);
writeLog("Timeouts: {$stats['timeouts']}", $log_file);
writeLog("Tempo Total: " . round($stats['total_time'], 3) . "s", $log_file);
writeLog("Tempo Médio: " . round($stats['avg_time'], 3) . "s", $log_file);
writeLog("Tempo Mínimo: " . round($stats['min_time'], 3) . "s", $log_file);
writeLog("Tempo Máximo: " . round($stats['max_time'], 3) . "s", $log_file);
writeLog("Tempo Mediano: " . round($stats['median_time'], 3) . "s", $log_file);
writeLog("===============================================", $log_file);

// Análise de performance
echo "\n🔍 ANÁLISE DE PERFORMANCE\n";
echo "==========================\n";

if ($stats['avg_time'] < 5) {
    echo "✅ Performance EXCELENTE: Tempo médio < 5s\n";
} elseif ($stats['avg_time'] < 10) {
    echo "✅ Performance BOA: Tempo médio < 10s\n";
} elseif ($stats['avg_time'] < 20) {
    echo "⚠️ Performance REGULAR: Tempo médio < 20s\n";
} else {
    echo "❌ Performance RUIM: Tempo médio > 20s\n";
}

if ($stats['success_rate'] >= 95) {
    echo "✅ Taxa de Sucesso EXCELENTE: " . round($stats['success_rate'], 1) . "%\n";
} elseif ($stats['success_rate'] >= 90) {
    echo "✅ Taxa de Sucesso BOA: " . round($stats['success_rate'], 1) . "%\n";
} elseif ($stats['success_rate'] >= 80) {
    echo "⚠️ Taxa de Sucesso REGULAR: " . round($stats['success_rate'], 1) . "%\n";
} else {
    echo "❌ Taxa de Sucesso RUIM: " . round($stats['success_rate'], 1) . "%\n";
}

if ($stats['timeouts'] == 0) {
    echo "✅ Nenhum timeout detectado\n";
} else {
    echo "⚠️ {$stats['timeouts']} timeouts detectados\n";
}

echo "==========================\n";

writeLog("ANÁLISE DE PERFORMANCE", $log_file);
if ($stats['avg_time'] < 5) {
    writeLog("Performance EXCELENTE: Tempo médio < 5s", $log_file);
} elseif ($stats['avg_time'] < 10) {
    writeLog("Performance BOA: Tempo médio < 10s", $log_file);
} elseif ($stats['avg_time'] < 20) {
    writeLog("Performance REGULAR: Tempo médio < 20s", $log_file);
} else {
    writeLog("Performance RUIM: Tempo médio > 20s", $log_file);
}

if ($stats['success_rate'] >= 95) {
    writeLog("Taxa de Sucesso EXCELENTE: " . round($stats['success_rate'], 1) . "%", $log_file);
} elseif ($stats['success_rate'] >= 90) {
    writeLog("Taxa de Sucesso BOA: " . round($stats['success_rate'], 1) . "%", $log_file);
} elseif ($stats['success_rate'] >= 80) {
    writeLog("Taxa de Sucesso REGULAR: " . round($stats['success_rate'], 1) . "%", $log_file);
} else {
    writeLog("Taxa de Sucesso RUIM: " . round($stats['success_rate'], 1) . "%", $log_file);
}

if ($stats['timeouts'] == 0) {
    writeLog("Nenhum timeout detectado", $log_file);
} else {
    writeLog("{$stats['timeouts']} timeouts detectados", $log_file);
}

writeLog("TESTE CONCLUÍDO", $log_file);

echo "\n✅ Teste concluído! Log salvo em: $log_file\n";
?>
