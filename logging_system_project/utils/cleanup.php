#!/usr/bin/env php
<?php
/**
 * utils/cleanup.php - Script de Limpeza Automática
 * Sistema de Logging PHP - RPA Imediato Seguros
 * 
 * Este script pode ser executado via cron job para limpeza automática
 * de logs antigos e manutenção do banco de dados.
 */

// Verificar se está sendo executado via CLI
if (php_sapi_name() !== 'cli') {
    die('Este script deve ser executado via linha de comando');
}

// Incluir dependências
require_once __DIR__ . '/../config/database.php';
require_once __DIR__ . '/../config/security.php';
require_once __DIR__ . '/../utils/helpers.php';

// Configurações
$config = [
    'retention_days' => 30,
    'dry_run' => false,
    'verbose' => false
];

// Processar argumentos da linha de comando
$options = getopt('d:rvh', ['days:', 'dry-run', 'verbose', 'help']);

if (isset($options['h']) || isset($options['help'])) {
    showHelp();
    exit(0);
}

if (isset($options['d']) || isset($options['days'])) {
    $config['retention_days'] = intval($options['d'] ?? $options['days']);
}

if (isset($options['r']) || isset($options['dry-run'])) {
    $config['dry_run'] = true;
}

if (isset($options['v']) || isset($options['verbose'])) {
    $config['verbose'] = true;
}

// Executar limpeza
echo "🧹 Iniciando limpeza do sistema de logging...\n";
echo "📅 Retenção: {$config['retention_days']} dias\n";
echo "🔍 Modo: " . ($config['dry_run'] ? 'DRY RUN (simulação)' : 'EXECUÇÃO REAL') . "\n";
echo str_repeat('=', 60) . "\n";

try {
    $results = performCleanup($config);
    displayResults($results);
    
    if (!$config['dry_run']) {
        echo "✅ Limpeza concluída com sucesso!\n";
    } else {
        echo "ℹ️ Simulação concluída. Use sem --dry-run para executar.\n";
    }
    
} catch (Exception $e) {
    echo "❌ Erro durante a limpeza: " . $e->getMessage() . "\n";
    exit(1);
}

/**
 * Executa a limpeza
 */
function performCleanup($config) {
    $results = [
        'logs_deleted' => 0,
        'sessions_deleted' => 0,
        'metrics_updated' => 0,
        'errors' => []
    ];
    
    try {
        $pdo = getDatabaseConnection();
        
        // 1. Limpar logs antigos
        $results['logs_deleted'] = cleanupOldLogs($pdo, $config);
        
        // 2. Limpar sessões antigas
        $results['sessions_deleted'] = cleanupOldSessions($pdo, $config);
        
        // 3. Atualizar métricas
        $results['metrics_updated'] = updateMetrics($pdo, $config);
        
        // 4. Otimizar tabelas
        optimizeTables($pdo, $config);
        
        // 5. Limpar arquivos temporários
        cleanupTempFiles($config);
        
    } catch (Exception $e) {
        $results['errors'][] = $e->getMessage();
    }
    
    return $results;
}

/**
 * Limpa logs antigos
 */
function cleanupOldLogs($pdo, $config) {
    $retentionDate = date('Y-m-d H:i:s', strtotime("-{$config['retention_days']} days"));
    
    if ($config['verbose']) {
        echo "🗑️ Limpando logs anteriores a: $retentionDate\n";
    }
    
    if ($config['dry_run']) {
        // Contar logs que seriam deletados
        $stmt = $pdo->prepare("SELECT COUNT(*) as count FROM debug_logs WHERE created_at < ?");
        $stmt->execute([$retentionDate]);
        $count = $stmt->fetch()['count'];
        
        if ($config['verbose']) {
            echo "   📊 Logs que seriam deletados: $count\n";
        }
        
        return $count;
    } else {
        // Deletar logs antigos
        $stmt = $pdo->prepare("DELETE FROM debug_logs WHERE created_at < ?");
        $stmt->execute([$retentionDate]);
        $deleted = $stmt->rowCount();
        
        if ($config['verbose']) {
            echo "   ✅ Logs deletados: $deleted\n";
        }
        
        return $deleted;
    }
}

/**
 * Limpa sessões antigas
 */
function cleanupOldSessions($pdo, $config) {
    $retentionDate = date('Y-m-d H:i:s', strtotime("-{$config['retention_days']} days"));
    
    if ($config['verbose']) {
        echo "🗑️ Limpando sessões anteriores a: $retentionDate\n";
    }
    
    if ($config['dry_run']) {
        // Contar sessões que seriam deletadas
        $stmt = $pdo->prepare("SELECT COUNT(*) as count FROM sessions WHERE created_at < ?");
        $stmt->execute([$retentionDate]);
        $count = $stmt->fetch()['count'];
        
        if ($config['verbose']) {
            echo "   📊 Sessões que seriam deletadas: $count\n";
        }
        
        return $count;
    } else {
        // Deletar sessões antigas
        $stmt = $pdo->prepare("DELETE FROM sessions WHERE created_at < ?");
        $stmt->execute([$retentionDate]);
        $deleted = $stmt->rowCount();
        
        if ($config['verbose']) {
            echo "   ✅ Sessões deletadas: $deleted\n";
        }
        
        return $deleted;
    }
}

/**
 * Atualiza métricas
 */
function updateMetrics($pdo, $config) {
    if ($config['verbose']) {
        echo "📊 Atualizando métricas...\n";
    }
    
    try {
        // Atualizar métricas dos últimos 7 dias
        for ($i = 0; $i < 7; $i++) {
            $date = date('Y-m-d', strtotime("-$i days"));
            
            if ($config['dry_run']) {
                if ($config['verbose']) {
                    echo "   📅 Métricas para $date (simulação)\n";
                }
                continue;
            }
            
            // Executar procedure de atualização de métricas
            $stmt = $pdo->prepare("CALL UpdateDailyMetrics(?)");
            $stmt->execute([$date]);
            
            if ($config['verbose']) {
                echo "   ✅ Métricas atualizadas para $date\n";
            }
        }
        
        return 7;
        
    } catch (Exception $e) {
        if ($config['verbose']) {
            echo "   ⚠️ Erro ao atualizar métricas: " . $e->getMessage() . "\n";
        }
        return 0;
    }
}

/**
 * Otimiza tabelas
 */
function optimizeTables($pdo, $config) {
    if ($config['verbose']) {
        echo "🔧 Otimizando tabelas...\n";
    }
    
    $tables = ['debug_logs', 'sessions', 'log_metrics', 'config'];
    
    foreach ($tables as $table) {
        if ($config['dry_run']) {
            if ($config['verbose']) {
                echo "   📊 Tabela $table seria otimizada\n";
            }
            continue;
        }
        
        try {
            $stmt = $pdo->prepare("OPTIMIZE TABLE $table");
            $stmt->execute();
            
            if ($config['verbose']) {
                echo "   ✅ Tabela $table otimizada\n";
            }
        } catch (Exception $e) {
            if ($config['verbose']) {
                echo "   ⚠️ Erro ao otimizar $table: " . $e->getMessage() . "\n";
            }
        }
    }
}

/**
 * Limpa arquivos temporários
 */
function cleanupTempFiles($config) {
    if ($config['verbose']) {
        echo "🗂️ Limpando arquivos temporários...\n";
    }
    
    $tempDir = sys_get_temp_dir();
    $pattern = $tempDir . '/rate_limit_*';
    $files = glob($pattern);
    
    $deleted = 0;
    foreach ($files as $file) {
        if ($config['dry_run']) {
            if ($config['verbose']) {
                echo "   📄 Arquivo que seria deletado: " . basename($file) . "\n";
            }
            $deleted++;
        } else {
            if (filemtime($file) < time() - 3600) { // Mais de 1 hora
                unlink($file);
                $deleted++;
                
                if ($config['verbose']) {
                    echo "   ✅ Arquivo deletado: " . basename($file) . "\n";
                }
            }
        }
    }
    
    if ($config['verbose']) {
        echo "   📊 Arquivos temporários processados: $deleted\n";
    }
}

/**
 * Exibe resultados
 */
function displayResults($results) {
    echo str_repeat('=', 60) . "\n";
    echo "📊 RESUMO DA LIMPEZA\n";
    echo str_repeat('=', 60) . "\n";
    echo "🗑️ Logs deletados: " . $results['logs_deleted'] . "\n";
    echo "🗑️ Sessões deletadas: " . $results['sessions_deleted'] . "\n";
    echo "📊 Métricas atualizadas: " . $results['metrics_updated'] . "\n";
    
    if (!empty($results['errors'])) {
        echo "\n❌ ERROS ENCONTRADOS:\n";
        foreach ($results['errors'] as $error) {
            echo "   - $error\n";
        }
    }
}

/**
 * Exibe ajuda
 */
function showHelp() {
    echo "🧹 Script de Limpeza - Sistema de Logging RPA\n";
    echo str_repeat('=', 50) . "\n";
    echo "Uso: php cleanup.php [opções]\n\n";
    echo "Opções:\n";
    echo "  -d, --days=N        Dias de retenção (padrão: 30)\n";
    echo "  -r, --dry-run       Modo simulação (não executa)\n";
    echo "  -v, --verbose       Modo verboso\n";
    echo "  -h, --help          Exibir esta ajuda\n\n";
    echo "Exemplos:\n";
    echo "  php cleanup.php                    # Limpeza padrão (30 dias)\n";
    echo "  php cleanup.php -d 7               # Manter apenas 7 dias\n";
    echo "  php cleanup.php -r -v              # Simulação verbosa\n";
    echo "  php cleanup.php --days=14 --dry-run # Simulação com 14 dias\n\n";
    echo "Cron Job (executar diariamente às 2h):\n";
    echo "  0 2 * * * /usr/bin/php /path/to/cleanup.php\n";
}
?>
