/**
 * Página Principal - Imediato Seguros V6.3.0
 * Versão com correção de conectividade
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
        
        // URLs para tentar (em ordem de prioridade)
        this.apiUrls = [
            'https://rpaimediatoseguros.com.br/api/rpa',
            'http://rpaimediatoseguros.com.br/api/rpa',
            '/api/rpa'
        ];
        
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
        console.log('🔧 URLs de API configuradas:', this.apiUrls);
    }
    
    /**
     * Configurar event listeners
     */
    setupEventListeners() {
        console.log('🔍 DEBUG: Procurando elementos do formulário...');
        const form = document.getElementById('rpa-form');
        const btnCalculate = document.getElementById('submit_button_auto');
        
        console.log('🔍 DEBUG: Form encontrado:', form);
        console.log('🔍 DEBUG: Botão encontrado:', btnCalculate);
        console.log('🔍 DEBUG: IDs encontrados:', document.querySelectorAll('[id]').length);
        
        if (!form || !btnCalculate) {
            console.error('❌ Elementos do formulário não encontrados');
            console.error('Form encontrado:', !!form);
            console.error('Botão encontrado:', !!btnCalculate);
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
                top: 80px !important;
                left: 0 !important;
                width: 100vw !important;
                height: calc(100vh - 80px) !important;
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
                            <img src="https://cdn.prod.website-files.com/59eb807f9d16950001e202af/5f845624fe08f9f0d0573fee_logotipo-imediato-seguros.svg" alt="Imediato Seguros" class="company-logo">
                        </div>
                        <h1><i class="fas fa-car"></i> Calculadora de Seguro</h1>
                        <div class="progress-info">
                            <span class="progress-text" id="progressText">0%</span>
                            <span class="current-phase" id="currentPhase">Iniciando Multi-Cálculo...</span>
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
                
                // DEBUG: Verificar logo
                const logoElement = modal.querySelector('.modal-logo');
                console.log('🔍 DEBUG Logo encontrado:', !!logoElement);
                if (logoElement) {
                    console.log('🔍 DEBUG Logo src:', logoElement.src);
                    console.log('🔍 DEBUG Logo dimensions:', {
                        width: logoElement.offsetWidth,
                        height: logoElement.offsetHeight,
                        display: window.getComputedStyle(logoElement).display
                    });
                }
            }
        }, 100);
        
        console.log('🎭 Modal de progresso aberto');
    }
    
    /**
     * Iniciar RPA com tentativas múltiplas
     */
    async startRPA(data) {
        console.log('🚀 Iniciando RPA...');
        
        // Tentar cada URL até uma funcionar
        for (let i = 0; i < this.apiUrls.length; i++) {
            const baseUrl = this.apiUrls[i];
            const url = `${baseUrl}/start`;
            
            console.log(`🔍 Tentativa ${i + 1}/${this.apiUrls.length}: ${url}`);
            
            try {
                const response = await fetch(url, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data)
                });
                
                console.log(`📡 Resposta recebida de ${url}:`, response.status);
                
                if (response.ok) {
                    const result = await response.json();
                    
                    if (result.success && result.session_id) {
                        this.sessionId = result.session_id;
                        console.log('✅ RPA iniciado com sucesso. Session ID:', this.sessionId);
                        console.log('✅ URL funcionando:', url);
                        
                        // Inicializar modal de progresso
                        this.initializeProgressModal();
                        return; // Sucesso, sair do loop
                    } else {
                        console.warn('⚠️ Resposta não contém session_id:', result);
                    }
                } else {
                    console.warn(`⚠️ Resposta não OK: ${response.status} ${response.statusText}`);
                }
                
            } catch (error) {
                console.warn(`❌ Erro na tentativa ${i + 1}:`, error.message);
                
                // Se for a última tentativa, mostrar erro
                if (i === this.apiUrls.length - 1) {
                    console.error('❌ Todas as tentativas falharam');
                    this.showFormError(`Erro de conexão. Tentativas: ${this.apiUrls.join(', ')}`);
                }
            }
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
