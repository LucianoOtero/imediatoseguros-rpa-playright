<?php
// Verificação simples dos logs do Footer Code
$config = require_once '/var/www/html/logging_system/config/app.php';

try {
    $pdo = new PDO(
        sprintf('mysql:host=%s;port=%d;dbname=%s;charset=%s',
            $config['database']['host'],
            $config['database']['port'],
            $config['database']['database'],
            $config['database']['charset']),
        $config['database']['username'],
        $config['database']['password']
    );
    
    // Contar logs do Footer Code
    $stmt = $pdo->prepare("SELECT COUNT(*) as total FROM debug_logs WHERE message LIKE ?");
    $stmt->execute(['%RPA habilitado via PHP Log%']);
    $total = $stmt->fetchColumn();
    
    echo "Total de logs do Footer Code: " . $total . "\n";
    
    // Mostrar os últimos 3 logs
    $stmt = $pdo->prepare("SELECT log_id, session_id, timestamp, level, url FROM debug_logs WHERE message LIKE ? ORDER BY timestamp DESC LIMIT 3");
    $stmt->execute(['%RPA habilitado via PHP Log%']);
    $logs = $stmt->fetchAll(PDO::FETCH_ASSOC);
    
    echo "\nUltimos logs do Footer Code:\n";
    foreach ($logs as $i => $log) {
        echo ($i+1) . ". [" . $log['level'] . "] " . $log['timestamp'] . " | " . $log['session_id'] . " | " . $log['url'] . "\n";
    }
    
    if ($total > 0) {
        echo "\n✅ CONFIRMADO: Banco de dados foi sensibilizado com logs do Footer Code!\n";
    } else {
        echo "\n❌ ERRO: Nenhum log do Footer Code encontrado no banco.\n";
    }
    
} catch (Exception $e) {
    echo "Erro: " . $e->getMessage() . "\n";
}


































