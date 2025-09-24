/**
 * PROGRESS TRACKER PARA WEBFLOW
 * Conecta via Server-Sent Events para monitorar progresso do RPA
 */

class WebflowProgressTracker {
    
    constructor(options = {}) {
        this.sessionId = options.sessionId || this.generateSessionId();
        this.baseUrl = options.baseUrl || '';
        this.eventSource = null;
        this.isConnected = false;
        this.callbacks = {
            onProgress: options.onProgress || this.defaultProgressHandler,
            onComplete: options.onComplete || this.defaultCompleteHandler,
            onError: options.onError || this.defaultErrorHandler
        };
        
        // Elementos DOM (customize conforme sua estrutura Webflow)
        this.elements = {
            progressBar: document.getElementById('progress-bar'),
            statusText: document.getElementById('status-text'),
            sessionInfo: document.getElementById('session-info'),
            estimativasContainer: document.getElementById('estimativas-container'),
            resultadoContainer: document.getElementById('resultado-container')
        };
    }
    
    /**
     * Gerar ID único da sessão
     */
    generateSessionId() {
        return 'session_' + Math.random().toString(36).substr(2, 9);
    }
    
    /**
     * Iniciar monitoramento
     */
    start() {
        if (this.isConnected) {
            console.warn('Progress tracker já está conectado');
            return;
        }
        
        const url = `${this.baseUrl}/progress_sse.php?session_id=${this.sessionId}`;
        
        try {
            this.eventSource = new EventSource(url);
            this.isConnected = true;
            
            this.eventSource.onopen = () => {
                console.log('Conexão SSE estabelecida');
                this.updateStatus('Conectado ao servidor...');
            };
            
            this.eventSource.onmessage = (event) => {
                try {
                    const data = JSON.parse(event.data);
                    this.handleMessage(data);
                } catch (error) {
                    console.error('Erro ao processar mensagem:', error);
                    this.callbacks.onError(error);
                }
            };
            
            this.eventSource.onerror = (error) => {
                console.error('Erro na conexão SSE:', error);
                this.isConnected = false;
                this.callbacks.onError(error);
            };
            
        } catch (error) {
            console.error('Erro ao iniciar EventSource:', error);
            this.callbacks.onError(error);
        }
    }
    
    /**
     * Parar monitoramento
     */
    stop() {
        if (this.eventSource) {
            this.eventSource.close();
            this.eventSource = null;
            this.isConnected = false;
            console.log('Conexão SSE fechada');
        }
    }
    
    /**
     * Processar mensagem recebida
     */
    handleMessage(data) {
        console.log('Dados recebidos:', data);
        
        switch (data.status) {
            case 'starting':
                this.updateStatus('Iniciando cotação...');
                this.updateProgress(0);
                break;
                
            case 'started':
                this.updateStatus('Processando dados...');
                break;
                
            case 'completed':
                this.updateStatus('Cotação concluída!');
                this.updateProgress(100);
                this.showResultadoFinal(data.progresso);
                this.callbacks.onComplete(data);
                this.stop();
                break;
                
            case 'timeout':
                this.updateStatus('Timeout - Cotação cancelada');
                this.callbacks.onError(new Error('Timeout'));
                this.stop();
                break;
                
            case 'error':
                this.updateStatus('Erro na cotação');
                this.callbacks.onError(new Error(data.message));
                this.stop();
                break;
                
            default:
                // Dados de progresso normal
                if (data.etapa_atual !== undefined) {
                    this.handleProgressData(data);
                }
                break;
        }
    }
    
    /**
     * Processar dados de progresso
     */
    handleProgressData(data) {
        const percentual = Math.round(data.percentual || 0);
        const etapa = data.etapa_atual || 0;
        const status = data.status || 'Processando...';
        
        // Atualizar UI
        this.updateProgress(percentual);
        this.updateStatus(`${status} (${etapa}/15)`);
        
        // Mostrar estimativas na Etapa 5
        if (etapa === 5 && data.details && data.details.estimativas) {
            this.showEstimativas(data.details.estimativas);
        }
        
        // Callback personalizado
        this.callbacks.onProgress(data);
    }
    
    /**
     * Atualizar barra de progresso
     */
    updateProgress(percentual) {
        if (this.elements.progressBar) {
            this.elements.progressBar.style.width = percentual + '%';
            this.elements.progressBar.setAttribute('aria-valuenow', percentual);
        }
    }
    
    /**
     * Atualizar texto de status
     */
    updateStatus(text) {
        if (this.elements.statusText) {
            this.elements.statusText.textContent = text;
        }
        
        if (this.elements.sessionInfo) {
            this.elements.sessionInfo.textContent = `Sessão: ${this.sessionId}`;
        }
    }
    
    /**
     * Mostrar estimativas (Etapa 5)
     */
    showEstimativas(estimativas) {
        if (this.elements.estimativasContainer) {
            this.elements.estimativasContainer.innerHTML = `
                <div class="estimativas-box">
                    <h3>Estimativas Iniciais</h3>
                    <div class="estimativas-grid">
                        <div class="estimativa-item">
                            <span class="label">Valor Estimado:</span>
                            <span class="valor">${estimativas.valor_estimado || 'N/A'}</span>
                        </div>
                        <div class="estimativa-item">
                            <span class="label">Franquia:</span>
                            <span class="valor">${estimativas.franquia || 'N/A'}</span>
                        </div>
                    </div>
                </div>
            `;
            this.elements.estimativasContainer.style.display = 'block';
        }
    }
    
    /**
     * Mostrar resultado final
     */
    showResultadoFinal(progresso) {
        if (this.elements.resultadoContainer && progresso.details) {
            const planos = progresso.details.planos || {};
            
            this.elements.resultadoContainer.innerHTML = `
                <div class="resultado-final">
                    <h3>Cotação Concluída!</h3>
                    <div class="planos-grid">
                        <div class="plano-item recomendado">
                            <h4>Plano Recomendado</h4>
                            <div class="valor-principal">${planos.plano_recomendado?.valor || 'N/A'}</div>
                            <div class="franquia">Franquia: ${planos.plano_recomendado?.valor_franquia || 'N/A'}</div>
                        </div>
                        <div class="plano-item alternativo">
                            <h4>Plano Alternativo</h4>
                            <div class="valor-principal">${planos.plano_alternativo?.valor || 'N/A'}</div>
                            <div class="franquia">Franquia: ${planos.plano_alternativo?.valor_franquia || 'N/A'}</div>
                        </div>
                    </div>
                </div>
            `;
            this.elements.resultadoContainer.style.display = 'block';
        }
    }
    
    /**
     * Handlers padrão
     */
    defaultProgressHandler(data) {
        console.log('Progresso:', data);
    }
    
    defaultCompleteHandler(data) {
        console.log('Cotação concluída:', data);
    }
    
    defaultErrorHandler(error) {
        console.error('Erro:', error);
    }
}

/**
 * FUNÇÃO DE INICIALIZAÇÃO PARA WEBFLOW
 * Chame esta função quando o modal for aberto
 */
function iniciarCotacao(dadosFormulario) {
    // Criar instância do tracker
    const tracker = new WebflowProgressTracker({
        baseUrl: '', // URL base do seu servidor
        onProgress: (data) => {
            console.log('Progresso atualizado:', data);
        },
        onComplete: (data) => {
            console.log('Cotação concluída:', data);
            // Aqui você pode adicionar lógica adicional
        },
        onError: (error) => {
            console.error('Erro na cotação:', error);
            // Aqui você pode mostrar mensagem de erro
        }
    });
    
    // Iniciar monitoramento
    tracker.start();
    
    // Retornar instância para controle manual se necessário
    return tracker;
}

// Exemplo de uso no Webflow:
/*
// Quando o modal for aberto
const progressTracker = iniciarCotacao({
    cpf: '12345678901',
    cep: '01234567',
    placa: 'ABC1234'
});

// Para parar manualmente (opcional)
// progressTracker.stop();
*/
