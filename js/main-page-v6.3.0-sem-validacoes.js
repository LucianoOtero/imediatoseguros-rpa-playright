/**
 * Página Principal - Imediato Seguros V6.3.0
 * Versão simplificada sem validações desnecessárias
 */

class MainPage {
    constructor() {
        this.sessionId = null;
        this.modalProgress = null;
        
        // Dados fixos (hardcoded)
        this.fixedData = {
            // Dados pessoais fixos
            telefone: "11999999999",
            email: "cliente@exemplo.com",
            profissao: "Empresário",
            renda_mensal: "10000",
            
            // Dados do veículo fixos
            modelo: "Civic",
            ano: "2020",
            cor: "Prata",
            combustivel: "Flex",
            zero_km: "false",
            uso: "Particular",
            garagem: "true",
            
            // Dados do seguro fixos
            tipo_seguro: "Comprehensive",
            franquia: "500",
            cobertura_adicional: "true",
            assistencia_24h: "true",
            
            // Dados adicionais fixos
            cnh_categoria: "B",
            tempo_habilitacao: "5",
            sinistros_ultimos_5_anos: "0",
            condutores_adicionais: "1"
        };
        
        this.init();
    }
    
    /**
     * Inicializar página
     */
    init() {
        console.log('🚀 Inicializando Página Principal V6.3.0...');
        
        // Aguardar DOM estar pronto
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.setupEventListeners());
        } else {
            this.setupEventListeners();
        }
        
        console.log('✅ Página Principal inicializada');
        console.log('📋 Modal simplificado - apenas resultados finais');
        console.log('🚫 Validações removidas - formulário livre');
    }
    
    /**
     * Configurar event listeners
     */
    setupEventListeners() {
        const form = document.getElementById('rpa-form');
        const btnCalculate = document.getElementById('btnCalculate');
        
        if (!form || !btnCalculate) {
            console.error('❌ Elementos do formulário não encontrados');
            return;
        }
        
        form.addEventListener('submit', (e) => this.handleFormSubmit(e));
        
        console.log('📝 Event listeners configurados');
    }
    
    /**
     * Handle form submission
     */
    async handleFormSubmit(event) {
        event.preventDefault();
        
        console.log('📝 Formulário submetido');
        
        // Coletar dados do formulário (sem validações)
        const formData = this.collectFormData();
        console.log('📊 Dados do formulário:', formData);
        
        // Mesclar com dados fixos
        const completeData = this.mergeWithFixedData(formData);
        console.log('🔗 Dados completos:', completeData);
        
        // Abrir modal de progresso
        this.openProgressModal();
        
        // Iniciar RPA
        await this.startRPA(completeData);
    }
    
    /**
     * Coletar dados do formulário
     */
    collectFormData() {
        const form = document.getElementById('rpa-form');
        const formData = new FormData(form);
        const data = {};
        
        for (let [key, value] of formData.entries()) {
            data[key] = value;
        }
        
        return data;
    }
    
    /**
     * Mesclar dados do formulário com dados fixos
     */
    mergeWithFixedData(formData) {
        return { ...this.fixedData, ...formData };
    }
    
    /**
     * Abrir modal de progresso
     */
    openProgressModal() {
        console.log('🎭 Abrindo modal de progresso...');
        
        // Verificar se já existe um modal
        const existingModal = document.getElementById('rpaModal');
        if (existingModal) {
            existingModal.remove();
            console.log('🗑️ Modal anterior removido');
        }
        
        // Criar modal com reset completo
        const modalHTML = `
            <div id="rpaModal" class="show" style="
                all: unset !important;
                position: fixed !important;
                top: 0 !important;
                left: 0 !important;
                width: 100vw !important;
                height: 100vh !important;
                background: rgba(0, 0, 0, 0.8) !important;
                z-index: 999999 !important;
                display: flex !important;
                flex-direction: column !important;
                margin: 0 !important;
                padding: 0 !important;
                border: none !important;
                box-shadow: none !important;
                overflow: hidden !important;
                box-sizing: border-box !important;
                isolation: isolate !important;
            ">
                <div class="modal-progress-bar">
                    <div class="progress-header">
                        <div class="logo-container">
                            <img src="https://www.segurosimediato.com.br/wp-content/uploads/2023/01/logo-imediato-seguros.png" alt="Imediato Seguros" class="modal-logo" onerror="this.style.display='none'; this.nextElementSibling.style.display='block';">
                            <div class="logo-fallback" style="display: none; color: white; font-size: 1.5rem; font-weight: bold;">IMEDIATO SEGUROS</div>
                        </div>
                        <div class="progress-info">
                            <span class="progress-text" id="progressText">0%</span>
                            <span class="current-phase" id="currentPhase">Iniciando RPA...</span>
                            <span class="sub-phase" id="subPhase"></span>
                        </div>
                        <div class="progress-stages">
                            <span class="stage-info" id="stageInfo">Fase 0 de 16</span>
                        </div>
                    </div>
                    <div class="progress-bar-wrapper">
                        <div class="progress-bar">
                            <div class="progress-fill" id="progressFill"></div>
                            <div class="progress-glow" id="progressGlow"></div>
                        </div>
                    </div>
                </div>
                
                <div class="modal-content">
                    <div class="results-section" id="resultsSection">
                        <div class="results-header">
                            <h2><i class="fas fa-chart-line"></i> Cálculo em Andamento</h2>
                            <p>Acompanhe o progresso do seu seguro em tempo real</p>
                        </div>
                        
                        <!-- 2 Divs de Resultados -->
                        <div class="results-container">
                            <!-- Div 1: Cálculo Recomendado -->
                            <div class="result-card recommended" id="recommendedCard">
                                <div class="card-header">
                                    <div class="card-icon">
                                        <i class="fas fa-star"></i>
                                    </div>
                                    <div class="card-title">
                                        <h3>Recomendado</h3>
                                        <span class="card-subtitle">Melhor Custo-Benefício</span>
                                    </div>
                                </div>
                                <div class="card-content">
                                    <div class="value-display">
                                        <span class="value" id="recommendedValue">-</span>
                                    </div>
                                </div>
                            </div>
                            
                            <!-- Div 2: Cálculo Alternativo -->
                            <div class="result-card alternative" id="alternativeCard">
                                <div class="card-header">
                                    <div class="card-icon">
                                        <i class="fas fa-exchange-alt"></i>
                                    </div>
                                    <div class="card-title">
                                        <h3>Alternativo</h3>
                                        <span class="card-subtitle">Opção Adicional</span>
                                    </div>
                                </div>
                                <div class="card-content">
                                    <div class="value-display">
                                        <span class="value" id="alternativeValue">-</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                        
                        <!-- Ações -->
                        <div class="results-actions">
                            <button class="btn-secondary" id="btnNewCalculation">
                                <i class="fas fa-redo"></i>
                                Nova Cotação
                            </button>
                            <button class="btn-primary" id="btnContactUs">
                                <i class="fas fa-phone"></i>
                                Falar com Corretor
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        // Injetar modal no DOM
        document.body.insertAdjacentHTML('beforeend', modalHTML);
        
        // Aguardar um pouco para garantir que os estilos sejam aplicados
        setTimeout(() => {
            const modal = document.getElementById('rpaModal');
            if (modal) {
                const computedStyle = window.getComputedStyle(modal);
                console.log('🎭 Modal injetado:', {
                    position: computedStyle.position,
                    zIndex: computedStyle.zIndex,
                    display: computedStyle.display
                });
                
                // Verificar se está funcionando como overlay
                if (computedStyle.position === 'fixed' && computedStyle.zIndex === '999999') {
                    console.log('✅ Modal configurado como overlay fixo');
                } else {
                    console.warn('⚠️ Modal pode não estar funcionando como overlay');
                }
            }
        }, 100);
        
        console.log('🎭 Modal de progresso aberto');
    }
    
    /**
     * Iniciar RPA
     */
    async startRPA(data) {
        try {
            console.log('🚀 Iniciando RPA...');
            
            // Chamar API do RPA (URL corrigida para Hetzner)
            const response = await fetch('https://rpaimediatoseguros.com.br/api/rpa/start', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });
            
            const result = await response.json();
            
            if (result.success && result.session_id) {
                this.sessionId = result.session_id;
                console.log('✅ RPA iniciado com sucesso. Session ID:', this.sessionId);
                
                // Inicializar modal de progresso
                this.initializeProgressModal();
                
            } else {
                console.error('❌ Erro ao iniciar RPA:', result.message);
                this.showFormError(result.message || 'Erro ao iniciar cálculo');
            }
            
        } catch (error) {
            console.error('❌ Erro na requisição:', error);
            this.showFormError('Erro de conexão. Tente novamente.');
        }
    }
    
    /**
     * Inicializar modal de progresso
     */
    initializeProgressModal() {
        console.log('🔄 Inicializando modal de progresso...');
        
        // Aguardar um pouco para garantir que o modal esteja no DOM
        setTimeout(() => {
            if (window.ProgressModalRPA) {
                this.modalProgress = new window.ProgressModalRPA(this.sessionId);
                this.modalProgress.startProgressPolling();
                console.log('✅ Modal de progresso inicializado');
            } else {
                console.error('❌ ProgressModalRPA não encontrado');
            }
        }, 200);
    }
    
    /**
     * Mostrar erro no formulário
     */
    showFormError(message) {
        // Remover modal se existir
        const modal = document.getElementById('rpaModal');
        if (modal) {
            modal.remove();
        }
        
        // Mostrar erro
        alert(message);
    }
}

// Inicializar quando DOM estiver pronto
document.addEventListener('DOMContentLoaded', () => {
    window.mainPage = new MainPage();
});
