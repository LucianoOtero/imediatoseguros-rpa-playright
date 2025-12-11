<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sistema de Logging RPA - Imediato Seguros</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f5f5f5; }
        .container { max-width: 1400px; margin: 0 auto; padding: 20px; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 10px; margin-bottom: 30px; }
        .header h1 { font-size: 2.5em; margin-bottom: 10px; }
        .header p { font-size: 1.2em; opacity: 0.9; }
        .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 30px; }
        .stat-card { background: white; padding: 25px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; }
        .stat-number { font-size: 2.5em; font-weight: bold; color: #667eea; margin-bottom: 10px; }
        .stat-label { color: #666; font-size: 1.1em; }
        .filters { background: white; padding: 25px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin-bottom: 30px; }
        .filter-row { display: flex; gap: 15px; margin-bottom: 15px; flex-wrap: wrap; }
        .filter-group { flex: 1; min-width: 200px; }
        .filter-group label { display: block; margin-bottom: 5px; font-weight: bold; color: #333; }
        .filter-group input, .filter-group select { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px; }
        .btn { padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; }
        .btn-primary { background: #667eea; color: white; }
        .btn-secondary { background: #6c757d; color: white; }
        .btn:hover { opacity: 0.9; }
        .logs-container { background: white; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); overflow: hidden; }
        .logs-header { background: #f8f9fa; padding: 20px; border-bottom: 1px solid #dee2e6; }
        .logs-content { max-height: 600px; overflow-y: auto; }
        .log-entry { padding: 15px; border-bottom: 1px solid #eee; }
        .log-entry:last-child { border-bottom: none; }
        .log-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
        .log-level { padding: 4px 8px; border-radius: 4px; font-size: 0.8em; font-weight: bold; }
        .log-level.DEBUG { background: #e3f2fd; color: #1976d2; }
        .log-level.INFO { background: #e8f5e8; color: #2e7d32; }
        .log-level.WARNING { background: #fff3e0; color: #f57c00; }
        .log-level.ERROR { background: #ffebee; color: #d32f2f; }
        .log-timestamp { color: #666; font-size: 0.9em; }
        .log-session { color: #667eea; font-weight: bold; }
        .log-message { margin: 10px 0; font-size: 1.1em; }
        .log-data { background: #f8f9fa; padding: 10px; border-radius: 5px; margin-top: 10px; font-family: monospace; font-size: 0.9em; }
        .loading { text-align: center; padding: 50px; color: #666; }
        .error { background: #ffebee; color: #d32f2f; padding: 15px; border-radius: 5px; margin: 20px 0; }
        .success { background: #e8f5e8; color: #2e7d32; padding: 15px; border-radius: 5px; margin: 20px 0; }
        @media (max-width: 768px) {
            .filter-row { flex-direction: column; }
            .filter-group { min-width: 100%; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔍 Sistema de Logging RPA</h1>
            <p>Monitoramento em tempo real - Imediato Seguros</p>
        </div>

        <div class="stats-grid" id="statsGrid">
            <div class="stat-card">
                <div class="stat-number" id="totalLogs">-</div>
                <div class="stat-label">Total de Logs</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" id="totalSessions">-</div>
                <div class="stat-label">Sessões Únicas</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" id="todayLogs">-</div>
                <div class="stat-label">Logs Hoje</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" id="errorCount">-</div>
                <div class="stat-label">Erros</div>
            </div>
        </div>

        <div class="filters">
            <h3 style="margin-bottom: 20px;">🔍 Filtros</h3>
            <div class="filter-row">
                <div class="filter-group">
                    <label>Nível:</label>
                    <select id="levelFilter">
                        <option value="">Todos</option>
                        <option value="DEBUG">DEBUG</option>
                        <option value="INFO">INFO</option>
                        <option value="WARNING">WARNING</option>
                        <option value="ERROR">ERROR</option>
                    </select>
                </div>
                <div class="filter-group">
                    <label>Sessão:</label>
                    <input type="text" id="sessionFilter" placeholder="ID da sessão">
                </div>
                <div class="filter-group">
                    <label>URL:</label>
                    <input type="text" id="urlFilter" placeholder="URL do log">
                </div>
            </div>
            <div class="filter-row">
                <div class="filter-group">
                    <label>Data Início:</label>
                    <input type="datetime-local" id="dateFrom">
                </div>
                <div class="filter-group">
                    <label>Data Fim:</label>
                    <input type="datetime-local" id="dateTo">
                </div>
                <div class="filter-group">
                    <label>&nbsp;</label>
                    <div>
                        <button class="btn btn-primary" onclick="applyFilters()">Aplicar Filtros</button>
                        <button class="btn btn-secondary" onclick="clearFilters()">Limpar</button>
                    </div>
                </div>
            </div>
        </div>

        <div class="logs-container">
            <div class="logs-header">
                <h3>📋 Logs Recentes</h3>
                <div>
                    <button class="btn btn-primary" onclick="refreshLogs()">🔄 Atualizar</button>
                    <button class="btn btn-secondary" onclick="exportLogs()">📥 Exportar</button>
                </div>
            </div>
            <div class="logs-content" id="logsContent">
                <div class="loading">Carregando logs...</div>
            </div>
        </div>
    </div>

    <script>
        let currentFilters = {};
        let autoRefresh = true;

        // Carregar estatísticas
        async function loadStats() {
            try {
                const response = await fetch('api/analytics.php?action=stats');
                const data = await response.json();
                
                if (data.success) {
                    document.getElementById('totalLogs').textContent = data.stats.total_logs || 0;
                    document.getElementById('totalSessions').textContent = data.stats.total_sessions || 0;
                    document.getElementById('todayLogs').textContent = data.stats.today_logs || 0;
                    document.getElementById('errorCount').textContent = data.stats.error_count || 0;
                }
            } catch (error) {
                console.error('Erro ao carregar estatísticas:', error);
            }
        }

        // Carregar logs
        async function loadLogs() {
            try {
                const params = new URLSearchParams({
                    action: 'logs',
                    page: 1,
                    limit: 50,
                    ...currentFilters
                });

                const response = await fetch(`api/analytics.php?${params}`);
                const data = await response.json();

                if (data.success) {
                    displayLogs(data.logs);
                } else {
                    showError('Erro ao carregar logs: ' + data.error);
                }
            } catch (error) {
                showError('Erro de conexão: ' + error.message);
            }
        }

        // Exibir logs
        function displayLogs(logs) {
            const container = document.getElementById('logsContent');
            
            if (!logs || logs.length === 0) {
                container.innerHTML = '<div class="loading">Nenhum log encontrado</div>';
                return;
            }

            container.innerHTML = logs.map(log => `
                <div class="log-entry">
                    <div class="log-header">
                        <div>
                            <span class="log-level ${log.level}">${log.level}</span>
                            <span class="log-session">${log.session_id}</span>
                        </div>
                        <div class="log-timestamp">${log.timestamp}</div>
                    </div>
                    <div class="log-message">${log.message}</div>
                    ${log.data ? `<div class="log-data">${JSON.stringify(log.data, null, 2)}</div>` : ''}
                    <div style="font-size: 0.8em; color: #666; margin-top: 5px;">
                        URL: ${log.url} | IP: ${log.ip_address}
                    </div>
                </div>
            `).join('');
        }

        // Aplicar filtros
        function applyFilters() {
            currentFilters = {
                level: document.getElementById('levelFilter').value,
                session_id: document.getElementById('sessionFilter').value,
                url: document.getElementById('urlFilter').value,
                date_from: document.getElementById('dateFrom').value,
                date_to: document.getElementById('dateTo').value
            };

            // Remover filtros vazios
            Object.keys(currentFilters).forEach(key => {
                if (!currentFilters[key]) {
                    delete currentFilters[key];
                }
            });

            loadLogs();
        }

        // Limpar filtros
        function clearFilters() {
            document.getElementById('levelFilter').value = '';
            document.getElementById('sessionFilter').value = '';
            document.getElementById('urlFilter').value = '';
            document.getElementById('dateFrom').value = '';
            document.getElementById('dateTo').value = '';
            currentFilters = {};
            loadLogs();
        }

        // Atualizar logs
        function refreshLogs() {
            loadStats();
            loadLogs();
        }

        // Exportar logs
        function exportLogs() {
            const params = new URLSearchParams({
                action: 'export',
                format: 'json',
                ...currentFilters
            });
            
            window.open(`api/analytics.php?${params}`, '_blank');
        }

        // Mostrar erro
        function showError(message) {
            const container = document.getElementById('logsContent');
            container.innerHTML = `<div class="error">${message}</div>`;
        }

        // Auto-refresh
        setInterval(() => {
            if (autoRefresh) {
                loadStats();
            }
        }, 30000); // 30 segundos

        // Inicializar
        document.addEventListener('DOMContentLoaded', function() {
            loadStats();
            loadLogs();
        });
    </script>
</body>
</html>


































