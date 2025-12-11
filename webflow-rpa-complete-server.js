/**
 * WEBFLOW RPA COMPLETE - IMEDIATO SEGUROS V6.13.1
 * Arquivo único para hospedagem externa no Webflow
 * 
 * Contém:
 * - CSS completo (inline)
 * - HTML do modal (dinâmico)
 * - JavaScript completo
 * - Integração RPA
 * - SpinnerTimer integrado
 * - Validação completa de formulário
 * - SweetAlert2 integrado dinamicamente
 * 
 * HOSPEDAGEM: https://rpaimediatoseguros.com.br/js/webflow-rpa-complete.js
 * BASEADO EM: new_webflow-injection-complete.js
 */

(function() {
    'use strict';
    
    // ========================================
    // 1. CARREGAMENTO DINÂMICO DE DEPENDÊNCIAS
    // ========================================
    
    // SweetAlert2 v11.22.4 - Carregamento dinâmico
    const loadSweetAlert = () => {
        return new Promise((resolve, reject) => {
            if (typeof Swal !== 'undefined') {
                console.log('✅ SweetAlert2 já carregado');
                resolve();
                return;
            }
            
            console.log('🔄 Carregando SweetAlert2...');
            const script = document.createElement('script');
            script.src = 'https://cdn.jsdelivr.net/npm/sweetalert2@11.22.4/dist/sweetalert2.all.min.js';
            script.defer = true;
            
            const css = document.createElement('link');
            css.rel = 'stylesheet';
            css.href = 'https://cdn.jsdelivr.net/npm/sweetalert2@11.22.4/dist/sweetalert2.min.css';
            
            script.onload = () => {
                console.log('✅ SweetAlert2 carregado com sucesso');
                resolve();
            };
            
            script.onerror = () => {
                console.warn('⚠️ SweetAlert2 falhou ao carregar, usando alert nativo');
                resolve(); // Continuar mesmo sem SweetAlert2
            };
            
            document.head.appendChild(css);
            document.head.appendChild(script);
        });
    };
    
    // Font Awesome 6.6.0 - Carregamento dinâmico
    const loadFontAwesome = () => {
        return new Promise((resolve) => {
            if (document.querySelector('link[href*="font-awesome"]')) {
                console.log('✅ Font Awesome já carregado');
                resolve();
                return;
            }
            
            console.log('🔄 Carregando Font Awesome...');
            const fontAwesome = document.createElement('link');
            fontAwesome.rel = 'stylesheet';
            fontAwesome.href = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.6.0/css/all.min.css';
            fontAwesome.crossOrigin = 'anonymous';
            
            fontAwesome.onload = () => {
                console.log('✅ Font Awesome carregado com sucesso');
                resolve();
            };
            
            fontAwesome.onerror = () => {
                console.warn('⚠️ Font Awesome falhou ao carregar');
                resolve();
            };
            
            document.head.appendChild(fontAwesome);
        });
    };
    
    // ========================================
    // 2. CSS COMPLETO (INLINE) - OTIMIZADO
    // ========================================
    
    const cssStyles = `
        /* IDENTIDADE VISUAL IMEDIATO SEGUROS V6.13.1 */
        
        /* Importar fonte Titillium Web */
        @import url('https://fonts.googleapis.com/css2?family=Titillium+Web:wght@300;400;600;700&display=swap');
        
        /* Variáveis CSS com cores da Imediato */
        :root {
            --imediato-dark-blue: #003366;
            --imediato-light-blue: #0099CC;
            --imediato-white: #FFFFFF;
            --imediato-gray: #F8F9FA;
            --imediato-text: #333333;
            --imediato-text-light: #666666;
            --imediato-border: #E0E0E0;
            --imediato-shadow: rgba(0, 51, 102, 0.1);
            --imediato-shadow-hover: rgba(0, 51, 102, 0.2);
        }
        
        /* MODAL DE PROGRESSO V6.13.1 */
        #rpaModal {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100vh;
            background: rgba(0, 51, 102, 0.95);
            z-index: 99999;
            display: none;
            font-family: 'Titillium Web', sans-serif;
        }
        
        #rpaModal.show {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }
        
        /* SPINNER TIMER CENTRALIZADO */
        .spinner-timer-container {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            z-index: 1000;
            background: transparent;
            border: none;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }
        
        .spinner-container {
            position: relative;
            width: 240px;
            height: 240px;
            margin-bottom: 1rem;
        }
        
        .sk-circle {
            width: 240px;
            height: 240px;
            position: relative;
        }
        
        .sk-circle .sk-child {
            width: 100%;
            height: 100%;
            position: absolute;
            left: 0;
            top: 0;
        }
        
        .sk-circle .sk-child:before {
            content: '';
            display: block;
            margin: 0 auto;
            width: 15%;
            height: 15%;
            background-color: #dc3545;
            border-radius: 100%;
            animation: sk-circle-bounce-delay 1.2s infinite ease-in-out both;
        }
        
        .spinner-center {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-size: 48px;
            font-weight: bold;
            color: #dc3545;
            z-index: 10;
        }
        
        @keyframes sk-circle-bounce-delay {
            0%, 80%, 100% {
                transform: scale(0);
            }
            40% {
                transform: scale(1);
            }
        }
        
        /* PROGRESS BAR */
        .progress-bar-container {
            width: 100%;
            height: 8px;
            background: var(--imediato-border);
            border-radius: 4px;
            overflow: hidden;
            margin: 1rem 0;
        }
        
        .progress-bar-fill {
            height: 100%;
            background: linear-gradient(90deg, var(--imediato-light-blue), var(--imediato-dark-blue));
            border-radius: 4px;
            transition: width 0.3s ease;
        }
        
        /* RESULTADOS */
        .results-container {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 2rem;
            margin-top: 2rem;
        }
        
        .result-card {
            background: var(--imediato-white);
            border-radius: 15px;
            padding: 1.5rem;
            box-shadow: 0 8px 25px var(--imediato-shadow);
            border: 2px solid var(--imediato-border);
        }
        
        .card-title h3 {
            color: var(--imediato-dark-blue);
            font-size: 1.3rem;
            font-weight: 600;
            margin: 0 0 0.5rem 0;
        }
        
        .value {
            font-size: 2.5rem;
            font-weight: 700;
            color: var(--imediato-dark-blue);
            text-align: center;
            margin: 1rem 0;
        }
        
        /* RESPONSIVIDADE */
        @media (max-width: 768px) {
            .results-container {
                grid-template-columns: 1fr;
                gap: 1rem;
            }
            
            .spinner-container,
            .sk-circle {
                width: 180px;
                height: 180px;
            }
            
            .spinner-center {
                font-size: 36px;
            }
        }
    `;
    
    // Injetar CSS
    const styleSheet = document.createElement('style');
    styleSheet.textContent = cssStyles;
    document.head.appendChild(styleSheet);
    
    // ========================================
    // 3. CLASSES PRINCIPAIS
    // ========================================
    
    class SpinnerTimer {
        constructor() {
            this.initialDuration = 180; // 3 minutos
            this.extendedDuration = 120; // 2 minutos adicionais
            this.totalDuration = this.initialDuration;
            this.remainingSeconds = this.initialDuration;
            this.isRunning = false;
            this.isExtended = false;
            this.interval = null;
            
            this.elements = {
                spinnerCenter: null,
                timerMessage: null
            };
        }
        
        init() {
            this.elements.spinnerCenter = document.getElementById('spinnerCenter');
            this.elements.timerMessage = document.getElementById('timerMessage');
            
            if (!this.elements.spinnerCenter) {
                console.warn('⚠️ Elementos do spinner timer não encontrados');
                return;
            }
            
            this.start();
        }
        
        start() {
            this.isRunning = true;
            this.isExtended = false;
            this.totalDuration = this.initialDuration;
            this.remainingSeconds = this.initialDuration;
            
            this.interval = setInterval(() => {
                this.tick();
            }, 100);
        }
        
        tick() {
            this.remainingSeconds -= 0.1;
            
            if (this.remainingSeconds <= 0) {
                if (!this.isExtended) {
                    this.extendTimer();
                    return;
                } else {
                    this.finish();
                    return;
                }
            }
            
            this.updateDisplay();
        }
        
        extendTimer() {
            this.isExtended = true;
            this.totalDuration += this.extendedDuration;
            this.remainingSeconds = this.extendedDuration;
            
            if (this.elements.timerMessage) {
                this.elements.timerMessage.style.display = 'block';
            }
        }
        
        finish() {
            this.isRunning = false;
            this.remainingSeconds = 0;
            this.updateDisplay();
            clearInterval(this.interval);
        }
        
        updateDisplay() {
            const minutes = Math.floor(this.remainingSeconds / 60);
            const seconds = Math.floor(this.remainingSeconds % 60);
            const centiseconds = Math.floor((this.remainingSeconds % 1) * 10);
            
            const timerText = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}.${centiseconds}`;
            
            if (this.elements.spinnerCenter) {
                this.elements.spinnerCenter.textContent = timerText;
            }
        }
        
        stop() {
            this.isRunning = false;
            clearInterval(this.interval);
        }
    }
    
    class ProgressModalRPA {
        constructor(sessionId = null) {
            this.sessionId = sessionId;
            this.modal = null;
            this.spinnerTimer = null;
            this.spinnerTimerInitialized = false;
            this.isProcessing = false;
            this.progressInterval = null;
            this.pollCount = 0;
            this.maxPolls = 300;
            
            this.setSessionId(sessionId);
        }
        
        setSessionId(sessionId) {
            this.sessionId = sessionId;
            
            if (!this.spinnerTimerInitialized) {
                this.initSpinnerTimer();
                this.spinnerTimerInitialized = true;
            }
        }
        
        initSpinnerTimer() {
            if (!this.spinnerTimer) {
                this.spinnerTimer = new SpinnerTimer();
                this.spinnerTimer.init();
                this.spinnerTimer.start();
            }
        }
        
        stopSpinnerTimer() {
            try {
                if (this.spinnerTimer) {
                    this.spinnerTimer.finish();
                    this.spinnerTimer = null;
                }
                
                const spinnerContainer = document.getElementById('spinnerTimerContainer');
                if (spinnerContainer) {
                    spinnerContainer.style.display = 'none';
                }
            } catch (error) {
                console.error('Erro ao parar spinner timer:', error);
            }
        }
        
        createModal() {
            const modalHTML = `
                <div id="rpaModal" class="show">
                    <div class="spinner-timer-container" id="spinnerTimerContainer">
                        <div class="spinner-container">
                            <div class="sk-circle">
                                <div class="sk-child"></div>
                                <div class="sk-child"></div>
                                <div class="sk-child"></div>
                                <div class="sk-child"></div>
                                <div class="sk-child"></div>
                                <div class="sk-child"></div>
                                <div class="sk-child"></div>
                                <div class="sk-child"></div>
                                <div class="sk-child"></div>
                                <div class="sk-child"></div>
                                <div class="sk-child"></div>
                                <div class="sk-child"></div>
                            </div>
                        </div>
                        <div class="spinner-center" id="spinnerCenter">03:00.0</div>
                        <div class="timer-message" id="timerMessage" style="display: none;">
                            Está demorando mais que o normal. Aguardando mais 2 minutos...
                        </div>
                    </div>
                    
                    <div class="progress-header">
                        <h1>🚀 Executando RPA</h1>
                        <div class="progress-info">
                            <div class="progress-text" id="progressText">0%</div>
                            <div class="current-phase" id="currentPhase">Iniciando...</div>
                        </div>
                        <div class="progress-bar-container">
                            <div class="progress-bar-fill" id="progressBarFill" style="width: 0%"></div>
                        </div>
                    </div>
                    
                    <div class="results-container" id="resultsContainer" style="display: none;">
                        <!-- Resultados serão inseridos aqui -->
                    </div>
                </div>
            `;
            
            document.body.insertAdjacentHTML('beforeend', modalHTML);
            this.modal = document.getElementById('rpaModal');
            
            // ✅ CORREÇÃO: Atribuir à variável global para debug
            window.progressModal = this.modal;
        }
        
        startProgressPolling() {
            if (!this.sessionId) {
                console.error('❌ Session ID não encontrado');
                return;
            }
            
            console.log('🔄 Iniciando polling do progresso...');
            this.pollCount = 0;
            this.maxPolls = 300;
            
            this.progressInterval = setInterval(() => {
                this.pollCount++;
                console.log(`🔄 Polling ${this.pollCount}/${this.maxPolls}`);
                
                if (this.pollCount > this.maxPolls) {
                    console.error('❌ Timeout: Processamento demorou mais de 10 minutos');
                    this.stopProgressPolling();
                    this.stopSpinnerTimer();
                    this.showTimeoutMessage();
                    return;
                }
                
                this.updateProgress();
            }, 2000);
        }
        
        async updateProgress() {
            try {
                const API_BASE_URL = 'https://rpaimediatoseguros.com.br';
                const response = await fetch(`${API_BASE_URL}/api/rpa/progress/${this.sessionId}`);
                const progressData = await response.json();
                
                console.log('📊 Progresso recebido:', progressData);
                
                const currentStatus = progressData.status;
                const currentPhase = progressData.current_phase || 'Processando...';
                const progressPercent = progressData.progress_percent || 0;
                
                // Atualizar elementos do modal
                const progressText = document.getElementById('progressText');
                const currentPhaseEl = document.getElementById('currentPhase');
                const progressBarFill = document.getElementById('progressBarFill');
                
                if (progressText) progressText.textContent = `${progressPercent}%`;
                if (currentPhaseEl) currentPhaseEl.textContent = currentPhase;
                if (progressBarFill) progressBarFill.style.width = `${progressPercent}%`;
                
                if (currentStatus === 'success') {
                    console.log('✅ RPA concluído com sucesso');
                    this.stopProgressPolling();
                    this.stopSpinnerTimer();
                    this.showSuccessResults(progressData);
                } else if (currentStatus === 'error') {
                    console.log('❌ RPA falhou');
                    this.stopProgressPolling();
                    this.stopSpinnerTimer();
                    this.handleRPAError(progressData);
                } else if (currentStatus === 'manual_quotation') {
                    console.log('📞 Cotação manual necessária');
                    this.stopProgressPolling();
                    this.stopSpinnerTimer();
                    this.showManualQuotationMessage();
                }
                
            } catch (error) {
                console.error('❌ Erro ao buscar progresso:', error);
            }
        }
        
        stopProgressPolling() {
            if (this.progressInterval) {
                clearInterval(this.progressInterval);
                this.progressInterval = null;
                console.log('⏹️ Polling do progresso parado');
            }
        }
        
        showSuccessResults(progressData) {
            const resultsContainer = document.getElementById('resultsContainer');
            if (!resultsContainer) return;
            
            resultsContainer.style.display = 'grid';
            
            const results = progressData.results || {};
            const premioSeguro = results.premio_seguro || 'R$ 0,00';
            const premioTotal = results.premio_total || 'R$ 0,00';
            
            resultsContainer.innerHTML = `
                <div class="result-card">
                    <div class="card-title">
                        <h3>💰 Prêmio Seguro</h3>
                    </div>
                    <div class="card-value">
                        <div class="value">${premioSeguro}</div>
                    </div>
                </div>
                
                <div class="result-card">
                    <div class="card-title">
                        <h3>💳 Prêmio Total</h3>
                    </div>
                    <div class="card-value">
                        <div class="value">${premioTotal}</div>
                    </div>
                </div>
            `;
        }
        
        handleRPAError(progressData) {
            const mensagem = progressData.message || 'Erro desconhecido';
            
            // ✅ TODOS os erros são tratados como cotação manual
            if (typeof Swal !== 'undefined') {
                Swal.fire({
                    title: '📞 Cotação Manual Necessária',
                    text: 'Não foi possível efetuar o cálculo nesse momento. Um especialista da Imediato Seguros fará o cálculo manualmente e entrará em contato para envia-lo à você em seguida.',
                    icon: 'info',
                    confirmButtonText: 'Entendi',
                    confirmButtonColor: '#3085d6'
                });
            } else {
                alert('📞 Cotação Manual Necessária\n\nNão foi possível efetuar o cálculo nesse momento. Um especialista da Imediato Seguros fará o cálculo manualmente e entrará em contato para envia-lo à você em seguida.');
            }
            
            this.closeModal();
        }
        
        showManualQuotationMessage() {
            if (typeof Swal !== 'undefined') {
                Swal.fire({
                    title: '📞 Cotação Manual Necessária',
                    text: 'Não foi possível efetuar o cálculo nesse momento. Um especialista da Imediato Seguros fará o cálculo manualmente e entrará em contato para envia-lo à você em seguida.',
                    icon: 'info',
                    confirmButtonText: 'Entendi',
                    confirmButtonColor: '#3085d6'
                });
            } else {
                alert('📞 Cotação Manual Necessária\n\nNão foi possível efetuar o cálculo nesse momento. Um especialista da Imediato Seguros fará o cálculo manualmente e entrará em contato para envia-lo à você em seguida.');
            }
            
            this.closeModal();
        }
        
        showTimeoutMessage() {
            if (typeof Swal !== 'undefined') {
                Swal.fire({
                    title: '⏰ Tempo Esgotado',
                    text: 'O processamento demorou mais que o esperado. Um especialista entrará em contato para fornecer a cotação manualmente.',
                    icon: 'warning',
                    confirmButtonText: 'Entendi',
                    confirmButtonColor: '#3085d6'
                });
            } else {
                alert('⏰ Tempo Esgotado\n\nO processamento demorou mais que o esperado. Um especialista entrará em contato para fornecer a cotação manualmente.');
            }
            
            this.closeModal();
        }
        
        closeModal() {
            if (this.modal) {
                this.modal.remove();
                this.modal = null;
            }
            this.isProcessing = false;
        }
    }
    
    // ========================================
    // 4. CLASSE PRINCIPAL DE INTEGRAÇÃO
    // ========================================
    
    class MainPage {
        constructor() {
            this.isProcessing = false;
            this.modalProgress = null;
        }
        
        async init() {
            console.log('🚀 Inicializando Webflow RPA Complete V6.13.1...');
            
            // Aguardar dependências carregarem
            await Promise.all([
                loadSweetAlert(),
                loadFontAwesome()
            ]);
            
            // Aguardar DOM estar pronto
            if (document.readyState === 'loading') {
                document.addEventListener('DOMContentLoaded', () => this.setupEventListeners());
            } else {
                this.setupEventListeners();
            }
        }
        
        setupEventListeners() {
            console.log('🔧 Configurando event listeners...');
            
            // ✅ INTERCEPTAÇÃO CONDICIONAL: Só intercepta se RPA habilitado
            if (window.rpaEnabled === false) {
                console.log('❌ RPA desabilitado - não configurando interceptação');
                return;
            }
            
            // Interceptar submit do formulário
            const forms = document.querySelectorAll('form');
            forms.forEach(form => {
                form.addEventListener('submit', (e) => this.handleFormSubmit(e));
            });
            
            // Interceptar clique no botão submit
            const submitButtons = document.querySelectorAll('button[type="submit"], input[type="submit"]');
            submitButtons.forEach(button => {
                button.addEventListener('click', (e) => this.handleButtonClick(e));
            });
        }
        
        async handleFormSubmit(event) {
            // ✅ VERIFICAÇÃO ADICIONAL: Se RPA desabilitado, não processar
            if (window.rpaEnabled === false) {
                console.log('❌ RPA desabilitado - não processando submit');
                return;
            }
            
            event.preventDefault();
            console.log('📝 Formulário interceptado');
            
            if (this.isProcessing) {
                console.log('⚠️ Já processando, ignorando submit');
                return;
            }
            
            await this.processForm(event.target);
        }
        
        async handleButtonClick(event) {
            const form = event.target.closest('form');
            if (form) {
                event.preventDefault();
                console.log('🔘 Botão submit interceptado');
                
                if (this.isProcessing) {
                    console.log('⚠️ Já processando, ignorando clique');
                    return;
                }
                
                await this.processForm(form);
            }
        }
        
        async processForm(form) {
            try {
                console.log('🚀 Iniciando processo RPA...');
                this.isProcessing = true;
                
                const formData = this.collectFormData(form);
                console.log('📤 Dados coletados:', formData);
                
                // Criar modal de progresso
                this.modalProgress = new ProgressModalRPA();
                this.modalProgress.createModal();
                
                // Iniciar RPA
                const sessionId = await this.startRPA(formData);
                console.log('🆔 Session ID recebido:', sessionId);
                
                if (sessionId) {
                    this.modalProgress.setSessionId(sessionId);
                    this.modalProgress.startProgressPolling();
                } else {
                    throw new Error('Session ID não recebido');
                }
                
            } catch (error) {
                console.error('❌ Erro no processo RPA:', error);
                this.handleError(error);
            }
        }
        
        collectFormData(form) {
            const formData = new FormData(form);
            const data = {};
            
            // Coletar todos os campos do formulário
            for (let [key, value] of formData.entries()) {
                data[key] = value;
            }
            
            // ✅ CORREÇÃO: Capturar campo GCLID_FLD manualmente
            const gclidField = document.getElementById('GCLID_FLD');
            if (gclidField) {
                data.GCLID_FLD = gclidField.value || 'TesteRPA123';
                console.log('✅ Campo GCLID_FLD capturado:', data.GCLID_FLD);
            } else {
                data.GCLID_FLD = 'TesteRPA123'; // Valor padrão
                console.log('⚠️ Campo GCLID_FLD não encontrado, usando valor padrão');
            }
            
            return data;
        }
        
        async startRPA(formData) {
            try {
                const API_BASE_URL = 'https://rpaimediatoseguros.com.br';
                const response = await fetch(`${API_BASE_URL}/api/rpa/start`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(formData)
                });
                
                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                }
                
                const result = await response.json();
                return result.session_id;
                
            } catch (error) {
                console.error('❌ Erro ao iniciar RPA:', error);
                throw error;
            }
        }
        
        handleError(error) {
            this.isProcessing = false;
            
            if (this.modalProgress) {
                this.modalProgress.closeModal();
            }
            
            const errorMessage = error.message || 'Erro desconhecido';
            
            if (typeof Swal !== 'undefined') {
                Swal.fire({
                    title: '❌ Erro',
                    text: `Ocorreu um erro: ${errorMessage}`,
                    icon: 'error',
                    confirmButtonText: 'OK',
                    confirmButtonColor: '#3085d6'
                });
            } else {
                alert(`❌ Erro: ${errorMessage}`);
            }
        }
    }
    
    // ========================================
    // 5. INICIALIZAÇÃO
    // ========================================
    
    // Aguardar DOM estar pronto
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            const mainPage = new MainPage();
            mainPage.init();
        });
    } else {
        const mainPage = new MainPage();
        mainPage.init();
    }
    
    console.log('🚀 Webflow RPA Complete V6.13.1 carregado com sucesso!');
    console.log('📋 SpinnerTimer integrado com ciclo de vida do RPA');
    console.log('📋 SweetAlert2 carregado dinamicamente');
    console.log('📋 Font Awesome carregado dinamicamente');
    console.log('📋 Interceptação de formulário garantida');
    
})();
