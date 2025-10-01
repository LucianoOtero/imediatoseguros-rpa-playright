<?php
/**
 * MONITOR DE TEMPO REAL - RPA MODULAR
 * Monitora o progresso do RPA em tempo real via AJAX
 */

// Configurações
$session_id = $_GET['session'] ?? 'teste_php_' . date('Ymd_His');
$refresh_interval = 1500; // 1.5 segundos (otimização conservadora)
?>

<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Monitor RPA - Tempo Real</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #2196F3, #21CBF3);
            color: white;
            padding: 20px;
            text-align: center;
        }
        .content {
            padding: 20px;
        }
        .status-card {
            background: #f8f9fa;
            border-radius: 8px;
            padding: 20px;
            margin: 10px 0;
            border-left: 4px solid #2196F3;
        }
        .progress-bar {
            width: 100%;
            height: 20px;
            background: #e0e0e0;
            border-radius: 10px;
            overflow: hidden;
            margin: 10px 0;
        }
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #4CAF50, #8BC34A);
            transition: width 0.3s ease;
        }
        .log-container {
            background: #1e1e1e;
            color: #00ff00;
            padding: 15px;
            border-radius: 5px;
            font-family: 'Courier New', monospace;
            max-height: 300px;
            overflow-y: auto;
            margin: 10px 0;
        }
        .btn {
            background: #2196F3;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            margin: 5px;
        }
        .btn:hover {
            background: #1976D2;
        }
        .btn-danger {
            background: #f44336;
        }
        .btn-danger:hover {
            background: #d32f2f;
        }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }
        .stat-item {
            background: white;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            text-align: center;
        }
        .stat-value {
            font-size: 24px;
            font-weight: bold;
            color: #2196F3;
        }
        .stat-label {
            color: #666;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 Monitor RPA - Tempo Real</h1>
            <p>Session ID: <strong><?php echo htmlspecialchars($session_id); ?></strong></p>
        </div>
        
        <div class="content">
            <div class="stats">
                <div class="stat-item">
                    <div class="stat-value" id="etapa-atual">0</div>
                    <div class="stat-label">Etapa Atual</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value" id="total-etapas">5</div>
                    <div class="stat-label">Total de Etapas</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value" id="percentual">0%</div>
                    <div class="stat-label">Progresso</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value" id="tempo-decorrido">0s</div>
                    <div class="stat-label">Tempo Decorrido</div>
                </div>
            </div>
            
            <div class="status-card">
                <h3>📊 Progresso</h3>
                <div class="progress-bar">
                    <div class="progress-fill" id="progress-fill" style="width: 0%"></div>
                </div>
                <p id="status-text">Aguardando execução...</p>
            </div>
            
            <div class="status-card">
                <h3>📝 Log de Execução</h3>
                <div class="log-container" id="log-container">
                    <div>🔄 Iniciando monitoramento...</div>
                </div>
            </div>
            
            <div class="status-card">
                <h3>🎮 Controles</h3>
                <button class="btn" onclick="startRPA()">▶️ Iniciar RPA</button>
                <button class="btn btn-danger" onclick="stopMonitoring()">⏹️ Parar Monitoramento</button>
                <button class="btn" onclick="clearLog()">🗑️ Limpar Log</button>
            </div>
        </div>
    </div>

    <script>
        let monitoring = false;
        let rpaProcess = null;
        
        function startRPA() {
            if (monitoring) return;
            
            monitoring = true;
            addLog('🚀 Iniciando execução do RPA...');
            
            // Simular execução do RPA (em produção, usar exec() do PHP)
            fetch('executar_rpa.php', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    session: '<?php echo $session_id; ?>',
                    action: 'start'
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    addLog('✅ RPA iniciado com sucesso!');
                    startMonitoring();
                } else {
                    addLog('❌ Erro ao iniciar RPA: ' + data.error);
                    monitoring = false;
                }
            })
            .catch(error => {
                addLog('❌ Erro de comunicação: ' + error);
                monitoring = false;
            });
        }
        
        function startMonitoring() {
            if (!monitoring) return;
            
            // Mostrar indicador de carregamento
            showLoading();
            
            fetch('get_progress.php?session=<?php echo $session_id; ?>')
            .then(response => response.json())
            .then(data => {
                if (data.success && data.data) {
                    updateProgress(data.data);
                    addLog(`📊 Etapa ${data.data.etapa_atual}/${data.data.total_etapas}: ${data.data.status}`);
                } else {
                    addLog('⏳ Aguardando dados de progresso...');
                }
                
                // Atualizar timestamp
                updateTimestamp();
                
                if (monitoring) {
                    setTimeout(startMonitoring, <?php echo $refresh_interval; ?>);
                }
            })
            .catch(error => {
                addLog('❌ Erro ao obter progresso: ' + error);
                if (monitoring) {
                    setTimeout(startMonitoring, <?php echo $refresh_interval; ?>);
                }
            });
        }
        
        function updateProgress(data) {
            document.getElementById('etapa-atual').textContent = data.etapa_atual;
            document.getElementById('total-etapas').textContent = data.total_etapas;
            document.getElementById('percentual').textContent = Math.round(data.percentual) + '%';
            document.getElementById('tempo-decorrido').textContent = Math.round(data.tempo_decorrido) + 's';
            document.getElementById('progress-fill').style.width = data.percentual + '%';
            document.getElementById('status-text').textContent = data.status;
            
            if (data.etapa_atual >= data.total_etapas) {
                addLog('🎉 Execução concluída com sucesso!');
                monitoring = false;
            }
        }
        
        function addLog(message) {
            const logContainer = document.getElementById('log-container');
            const timestamp = new Date().toLocaleTimeString();
            logContainer.innerHTML += `<div>[${timestamp}] ${message}</div>`;
            logContainer.scrollTop = logContainer.scrollHeight;
        }
        
        // Função para mostrar indicador de carregamento
        function showLoading() {
            const status = document.getElementById('status-text');
            if (status) {
                status.innerHTML = '⏳ Processando...';
            }
        }
        
        // Função para atualizar timestamp
        function updateTimestamp() {
            const timestamp = new Date().toLocaleTimeString();
            const header = document.querySelector('.header p');
            if (header) {
                header.innerHTML = `Session ID: <strong><?php echo htmlspecialchars($session_id); ?></strong> | Última atualização: ${timestamp}`;
            }
        }
        
        function stopMonitoring() {
            monitoring = false;
            addLog('⏹️ Monitoramento parado pelo usuário');
        }
        
        function clearLog() {
            document.getElementById('log-container').innerHTML = '<div>🗑️ Log limpo</div>';
        }
        
        // Iniciar monitoramento automático
        document.addEventListener('DOMContentLoaded', function() {
            addLog('🔄 Sistema de monitoramento carregado');
            addLog('💡 Clique em "Iniciar RPA" para começar');
        });
    </script>
</body>
</html>
