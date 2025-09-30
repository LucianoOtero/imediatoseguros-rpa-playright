class RPADashboard {
    constructor() {
        this.baseUrl = window.location.origin;
        this.sessions = [];
        this.selectedSessionId = null;
        this.updateInterval = 5000; // 5 segundos
        this.autoRefreshEnabled = true;
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadInitialData();
        this.startAutoRefresh();
    }

    setupEventListeners() {
        // Auto refresh toggle
        document.getElementById('autoRefresh').addEventListener('change', (e) => {
            this.autoRefreshEnabled = e.target.checked;
            if (this.autoRefreshEnabled) {
                this.startAutoRefresh();
            } else {
                this.stopAutoRefresh();
            }
        });

        // Modal events
        const newSessionModal = document.getElementById('newSessionModal');
        newSessionModal.addEventListener('hidden.bs.modal', () => {
            document.getElementById('newSessionForm').reset();
        });
    }

    async loadInitialData() {
        await Promise.all([
            this.loadSessions(),
            this.loadMetrics(),
            this.checkHealth()
        ]);
    }

    async loadSessions() {
        try {
            const response = await fetch(`${this.baseUrl}/api/rpa/sessions`);
            const data = await response.json();

            if (data.success) {
                this.sessions = data.sessions;
                this.renderSessions();
            } else {
                this.showError('Erro ao carregar sessões: ' + data.error);
            }
        } catch (error) {
            console.error('Erro ao carregar sessões:', error);
            this.showError('Erro de conexão ao carregar sessões');
        }
    }

    async loadMetrics() {
        try {
            const response = await fetch(`${this.baseUrl}/api/rpa/metrics`);
            const data = await response.json();

            if (data.success) {
                this.renderMetrics(data.metrics);
            }
        } catch (error) {
            console.error('Erro ao carregar métricas:', error);
        }
    }

    async checkHealth() {
        try {
            const response = await fetch(`${this.baseUrl}/api/rpa/health`);
            const data = await response.json();

            if (data.success) {
                this.renderHealthStatus(data.health);
            }
        } catch (error) {
            console.error('Erro ao verificar saúde:', error);
            this.renderHealthStatus({ status: 'unhealthy' });
        }
    }

    renderSessions() {
        const container = document.getElementById('sessions-list');
        
        if (this.sessions.length === 0) {
            container.innerHTML = '<div class="text-muted text-center">Nenhuma sessão encontrada</div>';
            return;
        }

        const html = this.sessions.map(session => {
            const statusClass = this.getStatusClass(session.status);
            const statusIcon = this.getStatusIcon(session.status);
            const progress = session.progress || 0;
            const createdAt = new Date(session.created_at).toLocaleString('pt-BR');

            return `
                <div class="session-item ${statusClass}" onclick="dashboard.selectSession('${session.session_id}')">
                    <div class="d-flex justify-content-between align-items-start">
                        <div>
                            <strong>${session.session_id}</strong>
                            <span class="badge bg-${this.getStatusColor(session.status)} status-badge ms-2">
                                ${statusIcon} ${session.status}
                            </span>
                        </div>
                        <small class="text-muted">${createdAt}</small>
                    </div>
                    <div class="progress-container">
                        <div class="progress" style="height: 6px;">
                            <div class="progress-bar bg-${this.getStatusColor(session.status)}" 
                                 style="width: ${progress}%"></div>
                        </div>
                        <small class="text-muted">${progress}% concluído</small>
                    </div>
                    ${session.current_step ? `<small class="text-muted">Etapa: ${session.current_step}</small>` : ''}
                </div>
            `;
        }).join('');

        container.innerHTML = html;
    }

    renderMetrics(metrics) {
        document.getElementById('total-sessions').textContent = metrics.sessions?.total || 0;
        
        const activeSessions = metrics.sessions?.by_status?.running || 0;
        document.getElementById('active-sessions').textContent = activeSessions;
        
        const successRate = metrics.performance?.success_rate || 0;
        document.getElementById('success-rate').textContent = successRate + '%';
        
        document.getElementById('last-update').textContent = new Date().toLocaleTimeString('pt-BR');
    }

    renderHealthStatus(health) {
        const indicator = document.getElementById('health-indicator');
        const status = document.getElementById('health-status');
        
        indicator.className = `health-indicator ${health.status}`;
        
        const statusText = {
            'healthy': 'Sistema Saudável',
            'degraded': 'Sistema Degradado',
            'unhealthy': 'Sistema Instável'
        };
        
        status.textContent = statusText[health.status] || 'Status Desconhecido';
    }

    selectSession(sessionId) {
        this.selectedSessionId = sessionId;
        this.loadSessionLogs(sessionId);
        
        // Highlight selected session
        document.querySelectorAll('.session-item').forEach(item => {
            item.classList.remove('border-primary');
        });
        
        event.currentTarget.classList.add('border-primary');
    }

    async loadSessionLogs(sessionId) {
        try {
            const response = await fetch(`${this.baseUrl}/api/rpa/logs/${sessionId}?limit=20`);
            const data = await response.json();

            if (data.success) {
                this.renderLogs(data.logs);
            }
        } catch (error) {
            console.error('Erro ao carregar logs:', error);
        }
    }

    renderLogs(logs) {
        const container = document.getElementById('realtime-logs');
        
        if (logs.length === 0) {
            container.innerHTML = '<div class="text-muted">Nenhum log disponível</div>';
            return;
        }

        const html = logs.map(log => {
            const level = log.level?.toLowerCase() || 'info';
            const timestamp = log.timestamp || new Date().toLocaleTimeString('pt-BR');
            const message = log.message || log;
            
            return `
                <div class="log-entry ${level}">
                    <small class="text-muted">[${timestamp}]</small>
                    <strong>[${level.toUpperCase()}]</strong>
                    ${message}
                </div>
            `;
        }).join('');

        container.innerHTML = html;
        container.scrollTop = container.scrollHeight;
    }

    async startNewSession() {
        const modal = new bootstrap.Modal(document.getElementById('newSessionModal'));
        modal.show();
    }

    async submitNewSession() {
        const form = document.getElementById('newSessionForm');
        const formData = new FormData(form);
        
        const data = {
            cpf: formData.get('cpf'),
            nome: formData.get('nome'),
            email: formData.get('email'),
            telefone: formData.get('telefone')
        };

        try {
            const response = await fetch(`${this.baseUrl}/api/rpa/start`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (result.success) {
                this.showSuccess('Sessão iniciada com sucesso!');
                bootstrap.Modal.getInstance(document.getElementById('newSessionModal')).hide();
                this.loadSessions();
            } else {
                this.showError('Erro ao iniciar sessão: ' + result.error);
            }
        } catch (error) {
            console.error('Erro ao iniciar sessão:', error);
            this.showError('Erro de conexão ao iniciar sessão');
        }
    }

    async showHealthCheck() {
        const modal = new bootstrap.Modal(document.getElementById('healthModal'));
        modal.show();
        
        try {
            const response = await fetch(`${this.baseUrl}/api/rpa/health`);
            const data = await response.json();

            if (data.success) {
                this.renderHealthDetails(data.health);
            }
        } catch (error) {
            console.error('Erro ao verificar saúde:', error);
        }
    }

    renderHealthDetails(health) {
        const container = document.getElementById('health-details');
        
        const html = `
            <div class="row">
                <div class="col-md-12">
                    <h6>Status Geral: <span class="badge bg-${this.getHealthColor(health.status)}">${health.status}</span></h6>
                </div>
            </div>
            <div class="row mt-3">
                ${Object.entries(health.checks || {}).map(([name, check]) => `
                    <div class="col-md-6 mb-2">
                        <div class="card">
                            <div class="card-body p-2">
                                <h6 class="card-title">${name}</h6>
                                <span class="badge bg-${this.getHealthColor(check.status)}">${check.status}</span>
                                ${check.path ? `<br><small class="text-muted">${check.path}</small>` : ''}
                                ${check.count !== undefined ? `<br><small>Count: ${check.count}</small>` : ''}
                                ${check.used_percent !== undefined ? `<br><small>Uso: ${check.used_percent}%</small>` : ''}
                            </div>
                        </div>
                    </div>
                `).join('')}
            </div>
        `;
        
        container.innerHTML = html;
    }

    refreshData() {
        this.loadInitialData();
        if (this.selectedSessionId) {
            this.loadSessionLogs(this.selectedSessionId);
        }
    }

    startAutoRefresh() {
        if (this.autoRefreshInterval) {
            clearInterval(this.autoRefreshInterval);
        }
        
        this.autoRefreshInterval = setInterval(() => {
            if (this.autoRefreshEnabled) {
                this.refreshData();
            }
        }, this.updateInterval);
    }

    stopAutoRefresh() {
        if (this.autoRefreshInterval) {
            clearInterval(this.autoRefreshInterval);
            this.autoRefreshInterval = null;
        }
    }

    getStatusClass(status) {
        const classes = {
            'running': 'running',
            'completed': 'completed',
            'failed': 'failed',
            'stopped': 'stopped',
            'pending': 'pending'
        };
        return classes[status] || '';
    }

    getStatusColor(status) {
        const colors = {
            'running': 'success',
            'completed': 'primary',
            'failed': 'danger',
            'stopped': 'secondary',
            'pending': 'warning'
        };
        return colors[status] || 'secondary';
    }

    getStatusIcon(status) {
        const icons = {
            'running': '▶️',
            'completed': '✅',
            'failed': '❌',
            'stopped': '⏹️',
            'pending': '⏳'
        };
        return icons[status] || '❓';
    }

    getHealthColor(status) {
        const colors = {
            'healthy': 'success',
            'degraded': 'warning',
            'unhealthy': 'danger',
            'ok': 'success',
            'warning': 'warning',
            'error': 'danger'
        };
        return colors[status] || 'secondary';
    }

    showSuccess(message) {
        this.showAlert(message, 'success');
    }

    showError(message) {
        this.showAlert(message, 'danger');
    }

    showAlert(message, type) {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        alertDiv.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(alertDiv);
        
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.parentNode.removeChild(alertDiv);
            }
        }, 5000);
    }
}

// Inicializar dashboard
const dashboard = new RPADashboard();

// Funções globais para os botões
function startNewSession() {
    dashboard.startNewSession();
}

function refreshData() {
    dashboard.refreshData();
}

function showHealthCheck() {
    dashboard.showHealthCheck();
}
