<?php
/**
 * TESTE PHP DIRETO - RPA IMEDIATO SEGUROS
 * Script para testar execução direta via PHP
 */

header('Content-Type: application/json');

// Configurações
$rpa_dir = '/opt/imediatoseguros-rpa';
$log_file = '/tmp/debug_php_direto_' . date('Ymd_His') . '.log';

// Função para log
function log_debug($message, $data = null) {
    global $log_file;
    $timestamp = date('Y-m-d H:i:s');
    $log_entry = "[$timestamp] $message";
    if ($data) {
        $log_entry .= " - " . json_encode($data);
    }
    file_put_contents($log_file, $log_entry . "\n", FILE_APPEND);
    echo $log_entry . "\n";
}

log_debug("=== INICIANDO TESTE PHP DIRETO ===");

// 1. Verificar ambiente
log_debug("1. VERIFICANDO AMBIENTE");
log_debug("   Usuário: " . get_current_user());
log_debug("   Diretório atual: " . getcwd());
log_debug("   PHP Version: " . phpversion());
log_debug("   SAPI: " . php_sapi_name());

// 2. Verificar se diretório RPA existe
log_debug("2. VERIFICANDO DIRETÓRIO RPA");
if (is_dir($rpa_dir)) {
    log_debug("   Diretório RPA existe: $rpa_dir");
    chdir($rpa_dir);
    log_debug("   Mudou para: " . getcwd());
} else {
    log_debug("   ERRO: Diretório RPA não existe: $rpa_dir");
    exit(1);
}

// 3. Verificar arquivo de teste
log_debug("3. VERIFICANDO ARQUIVO DE TESTE");
$test_file = 'teste_api_simples.py';
if (file_exists($test_file)) {
    log_debug("   Arquivo $test_file existe");
    $perms = fileperms($test_file);
    log_debug("   Permissões: " . substr(sprintf('%o', $perms), -4));
} else {
    log_debug("   ERRO: Arquivo $test_file não encontrado");
    exit(1);
}

// 4. Verificar ambiente virtual
log_debug("4. VERIFICANDO AMBIENTE VIRTUAL");
$venv_activate = 'venv/bin/activate';
if (file_exists($venv_activate)) {
    log_debug("   Script de ativação existe: $venv_activate");
} else {
    log_debug("   ERRO: Script de ativação não encontrado: $venv_activate");
    exit(1);
}

// 5. Testar comando direto
log_debug("5. TESTANDO COMANDO DIRETO");
$session_id = 'teste_php_direto_' . time();
$command = "source venv/bin/activate && python $test_file --session $session_id --modo-silencioso";
log_debug("   Comando: $command");

$output = [];
$return_code = 0;
exec($command . ' 2>&1', $output, $return_code);

log_debug("   Código de saída: $return_code");
log_debug("   Output:", $output);

// 6. Verificar Redis
log_debug("6. VERIFICANDO REDIS");
sleep(2);

// Tentar conectar ao Redis via PHP
try {
    $redis = new Redis();
    $redis->connect('127.0.0.1', 6379);
    
    $keys = $redis->keys("*$session_id*");
    log_debug("   Chaves Redis encontradas:", $keys);
    
    if (!empty($keys)) {
        log_debug("   ✅ Dados salvos no Redis com sucesso");
        foreach ($keys as $key) {
            $value = $redis->get($key);
            log_debug("   Chave: $key");
            log_debug("   Valor: " . substr($value, 0, 200) . "...");
        }
    } else {
        log_debug("   ❌ Nenhum dado encontrado no Redis");
    }
    
    $redis->close();
} catch (Exception $e) {
    log_debug("   ERRO ao conectar Redis: " . $e->getMessage());
}

// 7. Testar com nohup
log_debug("7. TESTANDO COM NOHUP");
$session_id_nohup = 'teste_php_nohup_' . time();
$command_nohup = "nohup bash -c 'source venv/bin/activate && python $test_file --session $session_id_nohup --modo-silencioso' > /dev/null 2>&1 & echo \$!";
log_debug("   Comando nohup: $command_nohup");

$pid = shell_exec($command_nohup);
$pid = trim($pid);
log_debug("   PID retornado: $pid");

// Aguardar um pouco
sleep(3);

// Verificar se processo ainda está rodando
$ps_output = shell_exec("ps -p $pid 2>/dev/null");
if (strpos($ps_output, $pid) !== false) {
    log_debug("   Processo $pid ainda está rodando");
} else {
    log_debug("   Processo $pid já terminou");
}

// Verificar Redis após nohup
sleep(2);
try {
    $redis = new Redis();
    $redis->connect('127.0.0.1', 6379);
    
    $keys_nohup = $redis->keys("*$session_id_nohup*");
    log_debug("   Chaves Redis após nohup:", $keys_nohup);
    
    if (!empty($keys_nohup)) {
        log_debug("   ✅ Dados salvos no Redis com sucesso (nohup)");
    } else {
        log_debug("   ❌ Nenhum dado encontrado no Redis (nohup)");
    }
    
    $redis->close();
} catch (Exception $e) {
    log_debug("   ERRO ao conectar Redis (nohup): " . $e->getMessage());
}

// 8. Verificar logs do sistema
log_debug("8. VERIFICANDO LOGS DO SISTEMA");
$nginx_log = '/var/log/nginx/error.log';
if (file_exists($nginx_log)) {
    $nginx_tail = shell_exec("tail -5 $nginx_log 2>/dev/null");
    log_debug("   Últimas linhas do nginx error.log:", explode("\n", trim($nginx_tail)));
}

$php_log = '/var/log/php8.3-fpm.log';
if (file_exists($php_log)) {
    $php_tail = shell_exec("tail -5 $php_log 2>/dev/null");
    log_debug("   Últimas linhas do php-fpm.log:", explode("\n", trim($php_tail)));
}

// 9. Verificar variáveis de ambiente
log_debug("9. VERIFICANDO VARIÁVEIS DE AMBIENTE");
$env_vars = [
    'HOME' => getenv('HOME'),
    'USER' => getenv('USER'),
    'SHELL' => getenv('SHELL'),
    'PATH' => getenv('PATH'),
    'LANG' => getenv('LANG'),
    'DISPLAY' => getenv('DISPLAY')
];
log_debug("   Variáveis de ambiente:", $env_vars);

// 10. Testar comando mínimo
log_debug("10. TESTANDO COMANDO MÍNIMO");
$minimo_output = shell_exec('python -c "print(\"Teste mínimo funcionando\")" 2>&1');
log_debug("   Comando mínimo:", trim($minimo_output));

log_debug("=== TESTE PHP DIRETO FINALIZADO ===");

// Retornar resultado
$resultado = [
    'success' => true,
    'session_id' => $session_id,
    'log_file' => $log_file,
    'timestamp' => date('Y-m-d H:i:s')
];

echo json_encode($resultado, JSON_PRETTY_PRINT);
?>



























