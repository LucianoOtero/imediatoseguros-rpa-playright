<?php
/**
 * Script de Limpeza Automatica de Logs
 * Sistema de Logging RPA - Imediato Seguros
 * Baseado na documentacao completa do projeto
 */

// Configuracoes
$config = require_once __DIR__ . '/../config/app.php';
$retentionDays = $config['logging']['retention_days'] ?? 30;
$dryRun = in_array('--dry-run', $argv);
$verbose = in_array('--verbose', $argv);

// Funcao para log
function logMessage($message, $level = 'INFO') {
    global $verbose;
    if ($verbose) {
        echo '[' . date('Y-m-d H:i:s') . '] [' . $level . '] ' . $message . PHP_EOL;
    }
}

// Funcao para obter dias personalizados
function getCustomDays($argv) {
    foreach ($argv as $arg) {
        if (strpos($arg, '--days=') === 0) {
            return (int) substr($arg, 7);
        }
    }
    return null;
}

// Verificar argumentos personalizados
$customDays = getCustomDays($argv);
if ($customDays !== null) {
    $retentionDays = $customDays;
    logMessage("Usando retencao personalizada: {$retentionDays} dias");
}

logMessage("Iniciando limpeza de logs (retencao: {$retentionDays} dias)");
logMessage("Modo dry-run: " . ($dryRun ? 'SIM' : 'NAO'));

try {
    // Conectar ao banco
    $dsn = sprintf(
        'mysql:host=%s;port=%d;dbname=%s;charset=%s',
        $config['database']['host'],
        $config['database']['port'],
        $config['database']['database'],
        $config['database']['charset']
    );
    
    $pdo = new PDO(
        $dsn,
        $config['database']['username'],
        $config['database']['password'],
        $config['database']['options']
    );
    
    logMessage('Conectado ao banco de dados');
    
    // Calcular data de corte
    $cutoffDate = date('Y-m-d H:i:s', strtotime("-{$retentionDays} days"));
    logMessage("Removendo logs anteriores a: {$cutoffDate}");
    
    // Contar registros que serao removidos
    $countStmt = $pdo->prepare('SELECT COUNT(*) FROM debug_logs WHERE timestamp < ?');
    $countStmt->execute([$cutoffDate]);
    $countToDelete = $countStmt->fetchColumn();
    
    logMessage("Registros a serem removidos: {$countToDelete}");
    
    if ($countToDelete > 0) {
        if ($dryRun) {
            logMessage('DRY RUN: Registros seriam removidos, mas nao foram deletados');
        } else {
            // Executar remocao
            $deleteStmt = $pdo->prepare('DELETE FROM debug_logs WHERE timestamp < ?');
            $result = $deleteStmt->execute([$cutoffDate]);
            
            if ($result) {
                $deletedCount = $deleteStmt->rowCount();
                logMessage("Removidos {$deletedCount} registros com sucesso");
                
                // Atualizar estatisticas
                $updateStmt = $pdo->prepare('UPDATE log_stats SET stat_value = ?, updated_at = NOW() WHERE stat_name = ?');
                $updateStmt->execute([$deletedCount, 'last_cleanup']);
                
                logMessage('Estatisticas atualizadas');
            } else {
                logMessage('Erro ao remover registros', 'ERROR');
            }
        }
    } else {
        logMessage('Nenhum registro antigo encontrado para remocao');
    }
    
    // Limpeza de arquivos de fallback
    $fallbackFile = $config['logging']['fallback_file'];
    if (file_exists($fallbackFile)) {
        $fileAge = time() - filemtime($fallbackFile);
        $fileAgeDays = $fileAge / (24 * 3600);
        
        if ($fileAgeDays > $retentionDays) {
            if ($dryRun) {
                logMessage("DRY RUN: Arquivo de fallback seria removido: {$fallbackFile}");
            } else {
                if (unlink($fallbackFile)) {
                    logMessage("Arquivo de fallback removido: {$fallbackFile}");
                } else {
                    logMessage("Erro ao remover arquivo de fallback", 'ERROR');
                }
            }
        }
    }
    
    // Estatisticas finais
    $totalStmt = $pdo->query('SELECT COUNT(*) FROM debug_logs');
    $totalLogs = $totalStmt->fetchColumn();
    
    $sessionsStmt = $pdo->query('SELECT COUNT(DISTINCT session_id) FROM debug_logs');
    $totalSessions = $sessionsStmt->fetchColumn();
    
    logMessage("Estatisticas finais:");
    logMessage("  - Total de logs: {$totalLogs}");
    logMessage("  - Total de sessoes: {$totalSessions}");
    logMessage("  - Retencao: {$retentionDays} dias");
    
    logMessage('Limpeza concluida com sucesso');
    
} catch (Exception $e) {
    logMessage('Erro durante limpeza: ' . $e->getMessage(), 'ERROR');
    exit(1);
}


































