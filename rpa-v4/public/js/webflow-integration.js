/**
 * Webflow Integration - RPA V4 Modal
 * JavaScript para integração com segurosimediato.com.br
 * 
 * Funcionalidades:
 * - Modal de monitoramento em tempo real
 * - Polling automático do progresso
 * - Exibição de estimativas e resultados
 * - Tratamento de erros compreensível
 */

class RPAWebflowIntegration {
    constructor() {
        this.apiBaseUrl = 'http://37.27.92.160'; // Servidor Hetzner
        this.currentSessionId = null;
        this.pollingInterval = null;
        this.pollingIntervalMs = 2000; // 2 segundos
        this.maxPollingTime = 300000; // 5 minutos
        this.startTime = null;
        
        this.init();
    }

    init() {
        this.createModal();
        this.setupEventListeners();
        console.log('[RPA] Webflow integration initialized');
    }

    createModal() {
        // Verificar se modal já existe
        if (document.getElementById('rpa-modal')) {
            return;
        }

        const modalHTML = `
            <div id="rpa-modal" class="rpa-modal" style="display: none;">
                <div class="rpa-modal-overlay">
                    <div class="rpa-modal-content">
                        <div class="rpa-modal-header">
                            <h3>Cotando seu Seguro</h3>
                            <button class="rpa-modal-close" onclick="rpaIntegration.closeModal()">&times;</button>
                        </div>
                        <div class="rpa-modal-body">
                            <div class="rpa-progress-container">
                                <div class="rpa-progress-bar">
                                    <div class="rpa-progress-fill" id="rpa-progress-fill"></div>
                                </div>
                                <div class="rpa-progress-text" id="rpa-progress-text">Iniciando cotação...</div>
                                <div class="rpa-progress-percentage" id="rpa-progress-percentage">0%</div>
                            </div>
                            
                            <div class="rpa-status-container">
                                <div class="rpa-status-item">
                                    <span class="rpa-status-label">Status:</span>
                                    <span class="rpa-status-value" id="rpa-status-value">Aguardando</span>
                                </div>
                                <div class="rpa-status-item">
                                    <span class="rpa-status-label">Etapa:</span>
                                    <span class="rpa-status-value" id="rpa-etapa-value">0/15</span>
                                </div>
                            </div>

                            <div class="rpa-estimates-container" id="rpa-estimates-container" style="display: none;">
                                <h4>Estimativas Iniciais</h4>
                                <div class="rpa-estimates-content" id="rpa-estimates-content"></div>
                            </div>

                            <div class="rpa-results-container" id="rpa-results-container" style="display: none;">
                                <h4>Resultados Finais</h4>
                                <div class="rpa-results-content" id="rpa-results-content"></div>
                            </div>

                            <div class="rpa-error-container" id="rpa-error-container" style="display: none;">
                                <h4>Erro na Cotação</h4>
                                <div class="rpa-error-content" id="rpa-error-content"></div>
                            </div>

                            <div class="rpa-timeline-container" id="rpa-timeline-container" style="display: none;">
                                <h4>Histórico da Execução</h4>
                                <div class="rpa-timeline-content" id="rpa-timeline-content"></div>
                            </div>
                        </div>
                        <div class="rpa-modal-footer">
                            <button class="rpa-btn rpa-btn-secondary" onclick="rpaIntegration.closeModal()">Fechar</button>
                        </div>
                    </div>
                </div>
            </div>
        `;

        // Adicionar CSS
        const css = `
            <style>
                .rpa-modal {
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    z-index: 10000;
                }
                
                .rpa-modal-overlay {
                    position: absolute;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    background: rgba(0, 0, 0, 0.7);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                }
                
                .rpa-modal-content {
                    background: white;
                    border-radius: 8px;
                    width: 90%;
                    max-width: 600px;
                    max-height: 80vh;
                    overflow-y: auto;
                    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
                }
                
                .rpa-modal-header {
                    padding: 20px;
                    border-bottom: 1px solid #eee;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                }
                
                .rpa-modal-header h3 {
                    margin: 0;
                    color: #333;
                }
                
                .rpa-modal-close {
                    background: none;
                    border: none;
                    font-size: 24px;
                    cursor: pointer;
                    color: #999;
                }
                
                .rpa-modal-close:hover {
                    color: #333;
                }
                
                .rpa-modal-body {
                    padding: 20px;
                }
                
                .rpa-progress-container {
                    margin-bottom: 20px;
                }
                
                .rpa-progress-bar {
                    width: 100%;
                    height: 20px;
                    background: #f0f0f0;
                    border-radius: 10px;
                    overflow: hidden;
                    margin-bottom: 10px;
                }
                
                .rpa-progress-fill {
                    height: 100%;
                    background: linear-gradient(90deg, #4CAF50, #45a049);
                    width: 0%;
                    transition: width 0.3s ease;
                }
                
                .rpa-progress-text {
                    font-size: 14px;
                    color: #666;
                    margin-bottom: 5px;
                }
                
                .rpa-progress-percentage {
                    font-size: 12px;
                    color: #999;
                    text-align: right;
                }
                
                .rpa-status-container {
                    display: flex;
                    gap: 20px;
                    margin-bottom: 20px;
                }
                
                .rpa-status-item {
                    flex: 1;
                }
                
                .rpa-status-label {
                    font-weight: bold;
                    color: #333;
                }
                
                .rpa-status-value {
                    color: #666;
                    margin-left: 5px;
                }
                
                .rpa-estimates-container,
                .rpa-results-container,
                .rpa-error-container,
                .rpa-timeline-container {
                    margin-top: 20px;
                    padding: 15px;
                    border-radius: 5px;
                }
                
                .rpa-estimates-container {
                    background: #e3f2fd;
                    border: 1px solid #2196f3;
                }
                
                .rpa-results-container {
                    background: #e8f5e8;
                    border: 1px solid #4caf50;
                }
                
                .rpa-error-container {
                    background: #ffebee;
                    border: 1px solid #f44336;
                }
                
                .rpa-timeline-container {
                    background: #f5f5f5;
                    border: 1px solid #ccc;
                }
                
                .rpa-estimates-content,
                .rpa-results-content,
                .rpa-error-content,
                .rpa-timeline-content {
                    margin-top: 10px;
                }
                
                .rpa-modal-footer {
                    padding: 20px;
                    border-top: 1px solid #eee;
                    text-align: right;
                }
                
                .rpa-btn {
                    padding: 10px 20px;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                    font-size: 14px;
                }
                
                .rpa-btn-secondary {
                    background: #6c757d;
                    color: white;
                }
                
                .rpa-btn-secondary:hover {
                    background: #5a6268;
                }
                
                .rpa-timeline-item {
                    padding: 8px 0;
                    border-bottom: 1px solid #eee;
                    font-size: 12px;
                }
                
                .rpa-timeline-item:last-child {
                    border-bottom: none;
                }
                
                .rpa-timeline-time {
                    color: #999;
                    margin-right: 10px;
                }
                
                .rpa-timeline-message {
                    color: #333;
                }
            </style>
        `;

        document.head.insertAdjacentHTML('beforeend', css);
        document.body.insertAdjacentHTML('beforeend', modalHTML);
    }

    setupEventListeners() {
        // Fechar modal ao clicar no overlay
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('rpa-modal-overlay')) {
                this.closeModal();
            }
        });

        // Fechar modal com ESC
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.isModalOpen()) {
                this.closeModal();
            }
        });
    }

    startRPA(data) {
        console.log('[RPA] Starting RPA with data:', data);
        
        // Validar dados obrigatórios
        if (!this.validateData(data)) {
            this.showError('Dados inválidos. Verifique CPF, placa e CEP.');
            return;
        }

        this.showModal();
        this.resetProgress();

        // Fazer requisição para iniciar RPA
        fetch(`${this.apiBaseUrl}/api/rpa/start`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(result => {
            if (result.success) {
                this.currentSessionId = result.session_id;
                this.startTime = Date.now();
                this.startPolling();
                console.log('[RPA] RPA started successfully:', result.session_id);
            } else {
                this.showError(result.error || 'Erro ao iniciar cotação');
            }
        })
        .catch(error => {
            console.error('[RPA] Error starting RPA:', error);
            this.showError('Erro de conexão. Tente novamente.');
        });
    }

    validateData(data) {
        const required = ['cpf', 'nome', 'placa', 'cep'];
        for (const field of required) {
            if (!data[field] || data[field].trim() === '') {
                return false;
            }
        }

        // Validar CPF (11 dígitos)
        if (!/^\d{11}$/.test(data.cpf)) {
            return false;
        }

        // Validar placa (formato brasileiro)
        if (!/^[A-Z]{3}\d{4}$/.test(data.placa)) {
            return false;
        }

        // Validar CEP (8 dígitos)
        if (!/^\d{8}$/.test(data.cep)) {
            return false;
        }

        return true;
    }

    startPolling() {
        if (this.pollingInterval) {
            clearInterval(this.pollingInterval);
        }

        this.pollingInterval = setInterval(() => {
            this.checkProgress();
        }, this.pollingIntervalMs);

        // Timeout de segurança
        setTimeout(() => {
            if (this.pollingInterval) {
                this.showError('Tempo limite excedido. A cotação pode ter falhado.');
                this.stopPolling();
            }
        }, this.maxPollingTime);
    }

    stopPolling() {
        if (this.pollingInterval) {
            clearInterval(this.pollingInterval);
            this.pollingInterval = null;
        }
    }

    checkProgress() {
        if (!this.currentSessionId) {
            return;
        }

        fetch(`${this.apiBaseUrl}/api/rpa/progress/${this.currentSessionId}`)
        .then(response => response.json())
        .then(result => {
            if (result.success) {
                this.updateProgress(result.progress);
                
                // Parar polling se concluído
                if (result.progress.status === 'success' || result.progress.status === 'completed') {
                    this.stopPolling();
                }
            } else {
                console.error('[RPA] Error checking progress:', result.error);
            }
        })
        .catch(error => {
            console.error('[RPA] Error checking progress:', error);
        });
    }

    updateProgress(progress) {
        // Atualizar barra de progresso
        const progressFill = document.getElementById('rpa-progress-fill');
        const progressPercentage = document.getElementById('rpa-progress-percentage');
        const progressText = document.getElementById('rpa-progress-text');
        const statusValue = document.getElementById('rpa-status-value');
        const etapaValue = document.getElementById('rpa-etapa-value');

        if (progressFill) {
            progressFill.style.width = `${progress.percentual}%`;
        }

        if (progressPercentage) {
            progressPercentage.textContent = `${Math.round(progress.percentual)}%`;
        }

        if (progressText) {
            progressText.textContent = progress.mensagem || 'Processando...';
        }

        if (statusValue) {
            statusValue.textContent = this.getStatusText(progress.status);
        }

        if (etapaValue) {
            etapaValue.textContent = `${progress.etapa_atual}/${progress.total_etapas}`;
        }

        // Atualizar estimativas se disponíveis
        if (progress.estimativas && progress.estimativas.capturadas) {
            this.updateEstimates(progress.estimativas.dados);
        }

        // Atualizar resultados finais se disponíveis
        if (progress.resultados_finais && progress.resultados_finais.rpa_finalizado) {
            this.updateFinalResults(progress.resultados_finais.dados);
        }

        // Atualizar timeline se disponível
        if (progress.timeline && progress.timeline.length > 0) {
            this.updateTimeline(progress.timeline);
        }
    }

    updateEstimates(estimatesData) {
        const container = document.getElementById('rpa-estimates-container');
        const content = document.getElementById('rpa-estimates-content');

        if (container && content && estimatesData) {
            container.style.display = 'block';
            
            if (estimatesData.coberturas_detalhadas) {
                content.innerHTML = `
                    <div class="rpa-estimates-grid">
                        ${estimatesData.coberturas_detalhadas.map(cobertura => `
                            <div class="rpa-estimate-item">
                                <strong>${cobertura.nome_cobertura}</strong><br>
                                <small>De: ${cobertura.valores.de}</small><br>
                                <small>Até: ${cobertura.valores.ate}</small>
                            </div>
                        `).join('')}
                    </div>
                `;
            }
        }
    }

    updateFinalResults(resultsData) {
        const container = document.getElementById('rpa-results-container');
        const content = document.getElementById('rpa-results-content');

        if (container && content && resultsData) {
            container.style.display = 'block';
            content.innerHTML = `<pre>${JSON.stringify(resultsData, null, 2)}</pre>`;
        }
    }

    updateTimeline(timeline) {
        const container = document.getElementById('rpa-timeline-container');
        const content = document.getElementById('rpa-timeline-content');

        if (container && content && timeline.length > 0) {
            container.style.display = 'block';
            
            content.innerHTML = timeline.map(item => `
                <div class="rpa-timeline-item">
                    <span class="rpa-timeline-time">${this.formatTime(item.timestamp)}</span>
                    <span class="rpa-timeline-message">${item.mensagem}</span>
                </div>
            `).join('');
        }
    }

    showError(message) {
        const container = document.getElementById('rpa-error-container');
        const content = document.getElementById('rpa-error-content');

        if (container && content) {
            container.style.display = 'block';
            content.innerHTML = `<p>${message}</p>`;
        }

        this.stopPolling();
    }

    getStatusText(status) {
        const statusMap = {
            'waiting': 'Aguardando',
            'running': 'Executando',
            'completed': 'Concluído',
            'success': 'Sucesso',
            'failed': 'Falhou',
            'error': 'Erro'
        };

        return statusMap[status] || status;
    }

    formatTime(timestamp) {
        if (!timestamp) return '';
        
        try {
            const date = new Date(timestamp);
            return date.toLocaleTimeString('pt-BR');
        } catch (e) {
            return timestamp;
        }
    }

    showModal() {
        const modal = document.getElementById('rpa-modal');
        if (modal) {
            modal.style.display = 'block';
        }
    }

    closeModal() {
        const modal = document.getElementById('rpa-modal');
        if (modal) {
            modal.style.display = 'none';
        }
        
        this.stopPolling();
        this.currentSessionId = null;
    }

    isModalOpen() {
        const modal = document.getElementById('rpa-modal');
        return modal && modal.style.display !== 'none';
    }

    resetProgress() {
        const progressFill = document.getElementById('rpa-progress-fill');
        const progressPercentage = document.getElementById('rpa-progress-percentage');
        const progressText = document.getElementById('rpa-progress-text');
        const statusValue = document.getElementById('rpa-status-value');
        const etapaValue = document.getElementById('rpa-etapa-value');

        if (progressFill) progressFill.style.width = '0%';
        if (progressPercentage) progressPercentage.textContent = '0%';
        if (progressText) progressText.textContent = 'Iniciando cotação...';
        if (statusValue) statusValue.textContent = 'Aguardando';
        if (etapaValue) etapaValue.textContent = '0/15';

        // Esconder containers
        const containers = ['rpa-estimates-container', 'rpa-results-container', 'rpa-error-container', 'rpa-timeline-container'];
        containers.forEach(id => {
            const container = document.getElementById(id);
            if (container) {
                container.style.display = 'none';
            }
        });
    }
}

// Inicializar integração
const rpaIntegration = new RPAWebflowIntegration();

// Função global para iniciar RPA (chamada pelo Webflow)
window.startRPACotacao = function(data) {
    rpaIntegration.startRPA(data);
};

// Função global para fechar modal
window.closeRPAModal = function() {
    rpaIntegration.closeModal();
};

console.log('[RPA] Webflow integration ready');
