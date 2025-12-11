<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>📊 Log Viewer - Sistema de Logging RPA</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            background: rgba(255, 255, 255, 0.95);
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            text-align: center;
        }
        
        .header h1 {
            color: #667eea;
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .header .subtitle {
            color: #666;
            font-size: 1.1em;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .stat-card {
            background: rgba(255, 255, 255, 0.95);
            padding: 25px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }
        
        .stat-card:hover {
            transform: translateY(-5px);
        }
        
        .stat-value {
            font-size: 2.5em;
            font-weight: bold;
            margin-bottom: 10px;
        }
        
        .stat-label {
            color: #666;
            font-size: 0.9em;
        }
        
        .controls {
            background: rgba(255, 255, 255, 0.95);
            padding: 25px;
            border-radius: 15px;
            margin-bottom: 30px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        
        .controls h3 {
            color: #667eea;
            margin-bottom: 20px;
        }
        
        .filter-row {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }
        
        .filter-group {
            display: flex;
            flex-direction: column;
        }
        
        .filter-group label {
            font-weight: bold;
            margin-bottom: 5px;
            color: #555;
        }
        
        .filter-group input,
        .filter-group select {
            padding: 10px;
            border: 2px solid #e9ecef;
            border-radius: 8px;
            font-size: 14px;
            transition: border-color 0.3s ease;
        }
        
        .filter-group input:focus,
        .filter-group select:focus {
            outline: none;
            border-color: #667eea;
        }
        
        .btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 12px 25px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
            font-weight: bold;
            transition: transform 0.3s ease;
        }
        
        .btn:hover {
            transform: translateY(-2px);
        }
        
        .btn-secondary {
            background: #6c757d;
        }
        
        .logs-container {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        
        .logs-header {
            display: flex;
            justify-content: between;
            align-items: center;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 2px solid #e9ecef;
        }
        
        .logs-header h3 {
            color: #667eea;
        }
        
        .log-entry {
            background: #f8f9fa;
            border-left: 4px solid #e9ecef;
            padding: 15px;
            margin-bottom: 15px;
            border-radius: 8px;
            transition: all 0.3s ease;
        }
        
        .log-entry:hover {
            background: #e9ecef;
            transform: translateX(5px);
        }
        
        .log-entry.debug {
            border-left-color: #6c757d;
        }
        
        .log-entry.info {
            border-left-color: #17a2b8;
        }
        
        .log-entry.warning {
            border-left-color: #ffc107;
        }
        
        .log-entry.error {
            border-left-color: #dc3545;
        }
        
        .log-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }
        
        .log-level {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.8em;
            font-weight: bold;
            text-transform: uppercase;
        }
        
        .log-level.debug {
            background: #6c757d;
            color: white;
        }
        
        .log-level.info {
            background: #17a2b8;
            color: white;
        }
        
        .log-level.warning {
            background: #ffc107;
            color: #333;
        }
        
        .log-level.error {
            background: #dc3545;
            color: white;
        }
        
        .log-timestamp {
            color: #666;
            font-size: 0.9em;
        }
        
        .log-message {
            font-weight: bold;
            margin-bottom: 8px;
            color: #333;
        }
        
        .log-details {
            font-size: 0.9em;
            color: #666;
        }
        
        .log-data {
            background: #fff;
            border: 1px solid #e9ecef;
            border-radius: 5px;
            padding: 10px;
            margin-top: 10px;
            font-family: 'Courier New', monospace;
            font-size: 0.8em;
            max-height: 200px;
            overflow-y: auto;
        }
        
        .pagination {
            display: flex;
            justify-content: center;
            align-items: center;
            margin-top: 30px;
            gap: 10px;
        }
        
        .pagination button {
            padding: 8px 15px;
            border: 1px solid #e9ecef;
            background: white;
            border-radius: 5px;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .pagination button:hover {
            background: #667eea;
            color: white;
        }
        
        .pagination button.active {
            background: #667eea;
            color: white;
        }
        
        .pagination button:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }
        
        .loading {
            text-align: center;
            padding: 50px;
            color: #666;
        }
        
        .error {
            background: #f8d7da;
            color: #721c24;
            padding: 15px;
            border-radius: 8px;
            margin: 20px 0;
        }
        
        .success {
            background: #d4edda;
            color: #155724;
            padding: 15px;
            border-radius: 8px;
            margin: 20px 0;
        }
        
        .export-buttons {
            display: flex;
            gap: 10px;
            margin-top: 20px;
        }
        
        @media (max-width: 768px) {
            .container {
                padding: 10px;
            }
            
            .header h1 {
                font-size: 2em;
            }
            
            .filter-row {
                grid-template-columns: 1fr;
            }
            
            .logs-header {
                flex-direction: column;
                gap: 15px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Log Viewer</h1>
            <div class="subtitle">Sistema de Logging RPA - Imediato Seguros</div>
        </div>
        
        <div class="stats-grid" id="statsGrid">
            <div class="stat-card">
                <div class="stat-value" id="totalLogs">-</div>
                <div class="stat-label">Total de Logs</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" id="uniqueSessions">-</div>
                <div class="stat-label">Sessões Únicas</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" id="logs24h">-</div>
                <div class="stat-label">Logs (24h)</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" id="errorCount">-</div>
                <div class="stat-label">Erros</div>
            </div>
        </div>
        
        <div class="controls">
            <h3>🔍 Filtros e Controles</h3>
            
            <div class="filter-row">
                <div class="filter-group">
                    <label for="levelFilter">Nível:</label>
                    <select id="levelFilter">
                        <option value="">Todos</option>
                        <option value="DEBUG">DEBUG</option>
                        <option value="INFO">INFO</option>
                        <option value="WARNING">WARNING</option>
                        <option value="ERROR">ERROR</option>
                    </select>
                </div>
                
                <div class="filter-group">
                    <label for="sessionFilter">Sessão:</label>
                    <input type="text" id="sessionFilter" placeholder="ID da sessão">
                </div>
                
                <div class="filter-group">
                    <label for="urlFilter">URL:</label>
                    <input type="text" id="urlFilter" placeholder="Filtrar por URL">
                </div>
                
                <div class="filter-group">
                    <label for="dateFrom">Data Início:</label>
                    <input type="datetime-local" id="dateFrom">
                </div>
                
                <div class="filter-group">
                    <label for="dateTo">Data Fim:</label>
                    <input type="datetime-local" id="dateTo">
                </div>
                
                <div class="filter-group">
                    <label for="searchMessage">Buscar:</label>
                    <input type="text" id="searchMessage" placeholder="Buscar na mensagem">
                </div>
            </div>
            
            <div style="display: flex; gap: 10px; align-items: center;">
                <button class="btn" onclick="loadLogs()">🔍 Filtrar</button>
                <button class="btn btn-secondary" onclick="clearFilters()">🗑️ Limpar</button>
                <button class="btn btn-secondary" onclick="refreshStats()">📊 Atualizar Stats</button>
                <button class="btn btn-secondary" onclick="exportLogs()">📥 Exportar</button>
            </div>
        </div>
        
        <div class="logs-container">
            <div class="logs-header">
                <h3>📋 Logs</h3>
                <div>
                    <span id="logsCount">0</span> logs encontrados
                </div>
            </div>
            
            <div id="logsList">
                <div class="loading">Carregando logs...</div>
            </div>
            
            <div class="pagination" id="pagination">
                <!-- Paginação será gerada dinamicamente -->
            </div>
        </div>
    </div>

    <script>
        let currentPage = 1;
        let totalPages = 1;
        let logsPerPage = 20;
        
        // Carregar dados iniciais
        document.addEventListener('DOMContentLoaded', function() {
            loadStats();
            loadLogs();
            
            // Configurar data padrão (últimas 24 horas)
            const now = new Date();
            const yesterday = new Date(now.getTime() - 24 * 60 * 60 * 1000);
            
            document.getElementById('dateTo').value = now.toISOString().slice(0, 16);
            document.getElementById('dateFrom').value = yesterday.toISOString().slice(0, 16);
        });
        
        // Carregar estatísticas
        async function loadStats() {
            try {
                const response = await fetch('api/analytics.php?action=stats');
                const data = await response.json();
                
                if (data.success) {
                    document.getElementById('totalLogs').textContent = data.stats.total_logs || 0;
                    document.getElementById('uniqueSessions').textContent = data.stats.unique_sessions || 0;
                    document.getElementById('logs24h').textContent = data.stats.logs_24h || 0;
                    document.getElementById('errorCount').textContent = data.stats.error_count || 0;
                }
            } catch (error) {
                console.error('Erro ao carregar estatísticas:', error);
            }
        }
        
        // Carregar logs
        async function loadLogs(page = 1) {
            const filters = getFilters();
            filters.page = page;
            filters.limit = logsPerPage;
            
            try {
                document.getElementById('logsList').innerHTML = '<div class="loading">Carregando logs...</div>';
                
                const response = await fetch('api/analytics.php?' + new URLSearchParams({
                    action: 'logs',
                    ...filters
                }));
                
                const data = await response.json();
                
                if (data.success) {
                    displayLogs(data.logs);
                    updatePagination(data.pagination);
                    document.getElementById('logsCount').textContent = data.pagination.total;
                } else {
                    document.getElementById('logsList').innerHTML = '<div class="error">Erro ao carregar logs: ' + data.message + '</div>';
                }
            } catch (error) {
                document.getElementById('logsList').innerHTML = '<div class="error">Erro de conexão: ' + error.message + '</div>';
            }
        }
        
        // Obter filtros
        function getFilters() {
            return {
                level: document.getElementById('levelFilter').value,
                session_id: document.getElementById('sessionFilter').value,
                url: document.getElementById('urlFilter').value,
                date_from: document.getElementById('dateFrom').value,
                date_to: document.getElementById('dateTo').value,
                search: document.getElementById('searchMessage').value
            };
        }
        
        // Exibir logs
        function displayLogs(logs) {
            const container = document.getElementById('logsList');
            
            if (logs.length === 0) {
                container.innerHTML = '<div class="loading">Nenhum log encontrado com os filtros aplicados.</div>';
                return;
            }
            
            let html = '';
            
            logs.forEach(log => {
                const levelClass = log.level.toLowerCase();
                const timestamp = new Date(log.timestamp).toLocaleString('pt-BR');
                
                html += `
                    <div class="log-entry ${levelClass}">
                        <div class="log-header">
                            <span class="log-level ${levelClass}">${log.level}</span>
                            <span class="log-timestamp">${timestamp}</span>
                        </div>
                        <div class="log-message">${escapeHtml(log.message)}</div>
                        <div class="log-details">
                            <strong>Sessão:</strong> ${log.session_id}<br>
                            <strong>URL:</strong> ${escapeHtml(log.url || 'N/A')}<br>
                            <strong>IP:</strong> ${log.ip_address}<br>
                            ${log.data ? '<strong>Dados:</strong><br>' : ''}
                        </div>
                        ${log.data ? `<div class="log-data">${escapeHtml(JSON.stringify(JSON.parse(log.data), null, 2))}</div>` : ''}
                    </div>
                `;
            });
            
            container.innerHTML = html;
        }
        
        // Atualizar paginação
        function updatePagination(pagination) {
            const container = document.getElementById('pagination');
            currentPage = pagination.current_page;
            totalPages = pagination.total_pages;
            
            let html = '';
            
            // Botão anterior
            html += `<button ${!pagination.has_prev ? 'disabled' : ''} onclick="loadLogs(${currentPage - 1})">« Anterior</button>`;
            
            // Páginas
            const startPage = Math.max(1, currentPage - 2);
            const endPage = Math.min(totalPages, currentPage + 2);
            
            if (startPage > 1) {
                html += `<button onclick="loadLogs(1)">1</button>`;
                if (startPage > 2) {
                    html += `<span>...</span>`;
                }
            }
            
            for (let i = startPage; i <= endPage; i++) {
                html += `<button class="${i === currentPage ? 'active' : ''}" onclick="loadLogs(${i})">${i}</button>`;
            }
            
            if (endPage < totalPages) {
                if (endPage < totalPages - 1) {
                    html += `<span>...</span>`;
                }
                html += `<button onclick="loadLogs(${totalPages})">${totalPages}</button>`;
            }
            
            // Botão próximo
            html += `<button ${!pagination.has_next ? 'disabled' : ''} onclick="loadLogs(${currentPage + 1})">Próximo »</button>`;
            
            container.innerHTML = html;
        }
        
        // Limpar filtros
        function clearFilters() {
            document.getElementById('levelFilter').value = '';
            document.getElementById('sessionFilter').value = '';
            document.getElementById('urlFilter').value = '';
            document.getElementById('searchMessage').value = '';
            
            // Resetar datas para últimas 24 horas
            const now = new Date();
            const yesterday = new Date(now.getTime() - 24 * 60 * 60 * 1000);
            
            document.getElementById('dateTo').value = now.toISOString().slice(0, 16);
            document.getElementById('dateFrom').value = yesterday.toISOString().slice(0, 16);
            
            loadLogs();
        }
        
        // Atualizar estatísticas
        function refreshStats() {
            loadStats();
        }
        
        // Exportar logs
        async function exportLogs() {
            const filters = getFilters();
            
            try {
                const response = await fetch('api/analytics.php?' + new URLSearchParams({
                    action: 'export',
                    format: 'csv',
                    ...filters
                }));
                
                if (response.ok) {
                    const blob = await response.blob();
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = `logs_${new Date().toISOString().slice(0, 10)}.csv`;
                    document.body.appendChild(a);
                    a.click();
                    document.body.removeChild(a);
                    window.URL.revokeObjectURL(url);
                } else {
                    alert('Erro ao exportar logs');
                }
            } catch (error) {
                alert('Erro ao exportar logs: ' + error.message);
            }
        }
        
        // Escapar HTML
        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }
        
        // Auto-refresh a cada 30 segundos
        setInterval(() => {
            loadStats();
        }, 30000);
    </script>
</body>
</html>




































