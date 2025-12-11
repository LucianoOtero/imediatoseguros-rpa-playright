/**
 * INJEÇÃO COMPLETA WEBFLOW - IMEDIATO SEGUROS V6.12.0
 * Arquivo único para injeção no Webflow
 * 
 * Contém:
 * - CSS completo (inline)
 * - HTML do modal (dinâmico)
 * - JavaScript completo
 * - Integração RPA
 * - SpinnerTimer integrado com ciclo de vida do RPA
 * 
 * USO: Copiar todo este código para o Custom Code do Webflow
 */

(function() {
    'use strict';
    
    // ========================================
    // 1. CSS COMPLETO (INLINE)
    // ========================================
    
    const cssStyles = `
        /* IDENTIDADE VISUAL IMEDIATO SEGUROS V6.2.2 */
        
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
            
            /* Font sizes */
            --font-size-xs: 0.75rem;
            --font-size-sm: 0.875rem;
            --font-size-base: 1rem;
            --font-size-lg: 1.125rem;
            --font-size-xl: 1.25rem;
            --font-size-2xl: 1.5rem;
            --font-size-3xl: 1.875rem;
            --font-size-4xl: 2.25rem;
        }
        
        /* MODAL DE PROGRESSO V6.2.2 - IMEDIATO SEGUROS */
        
        /* Aplicar fonte Titillium Web em todos os elementos do modal */
        #rpaModal * {
            font-family: 'Titillium Web', sans-serif !important;
            font-size: var(--font-size-base) !important;
        }
        
        /* Tamanhos específicos para elementos do modal */
        #rpaModal h1 {
            font-size: var(--font-size-2xl);
            font-weight: 600;
        }
        
        #rpaModal h3 {
            font-size: var(--font-size-lg) !important;
            font-weight: 600 !important;
        }
        
        #rpaModal .progress-text {
            font-size: var(--font-size-xl) !important;
            font-weight: 700 !important;
        }
        
        #rpaModal .current-phase {
            font-size: var(--font-size-lg) !important;
            font-weight: 500 !important;
        }
        
        #rpaModal .sub-phase {
            font-size: var(--font-size-sm) !important;
            font-weight: 400 !important;
        }
        
        #rpaModal .stage-info {
            font-size: var(--font-size-sm) !important;
            font-weight: 500 !important;
        }
        
        #rpaModal .value {
            font-size: var(--font-size-2xl) !important;
            font-weight: 700 !important;
        }
        
        #rpaModal .card-subtitle {
            font-size: var(--font-size-sm) !important;
            font-weight: 400 !important;
        }
        
        #rpaModal .card-features li {
            font-size: var(--font-size-sm) !important;
            font-weight: 400 !important;
        }
        
        #rpaModal .contact-message {
            font-size: var(--font-size-lg) !important;
            font-weight: 500 !important;
        }
        
        #rpaModal .action-buttons a {
            font-size: var(--font-size-base) !important;
            font-weight: 600 !important;
        }
        
        /* Modal principal */
        #rpaModal {
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            width: 100vw !important;
            height: 100vh !important;
            background: rgba(0, 0, 0, 0.8) !important;
            z-index: 999999 !important;
            opacity: 0 !important;
            visibility: hidden !important;
            transition: all 0.3s ease !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            padding: 2rem !important;
            box-sizing: border-box !important;
        }
        
        #rpaModal.show {
            opacity: 1 !important;
            visibility: visible !important;
        }
        
        /* Container do modal */
        #rpaModal .modal-container {
            background: var(--imediato-white) !important;
            border-radius: 20px !important;
            box-shadow: 0 20px 60px var(--imediato-shadow) !important;
            width: 100% !important;
            max-width: 900px !important;
            max-height: 80vh !important;
            overflow-y: auto !important;
            position: relative !important;
            margin: 0 auto !important;
        }
        
        /* Barra de progresso fixa no topo */
        #rpaModal .modal-progress-bar {
            background: var(--imediato-white) !important;
            position: sticky !important;
            top: 0 !important;
            z-index: 10001 !important;
            border-radius: 20px 20px 0 0 !important;
            padding: 0 !important;
            margin: 0 !important;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1) !important;
        }
        
        /* Restaurar estilos específicos após reset */
        #rpaModal .modal-progress-bar {
            background: var(--imediato-white);
            position: sticky;
            top: 0;
            z-index: 10001;
        }
        
        /* Progress bar visual */
        #rpaModal .progress-bar {
            height: 6px !important;
            background: linear-gradient(90deg, var(--imediato-dark-blue), var(--imediato-light-blue)) !important;
            border-radius: 3px !important;
            transition: width 0.5s ease !important;
            margin: 0 !important;
        }
        
        /* Header do progresso */
        #rpaModal .progress-header {
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 1.2rem 2rem;
            background: linear-gradient(135deg, var(--imediato-dark-blue), var(--imediato-light-blue));
            color: var(--imediato-white);
            border-radius: 20px 20px 0 0;
            text-align: center;
        }
        
        #rpaModal .progress-header h1 {
            color: var(--imediato-white) !important;
            font-size: 1.8rem;
            font-weight: 600;
            margin: 0 0 1rem 0;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0.5rem;
        }
        
        #rpaModal .progress-header .progress-text {
            color: var(--imediato-white) !important;
            font-size: 1.2rem;
            font-weight: 700;
            margin: 0;
        }
        
        #rpaModal .progress-info {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 1.5rem;
            margin-top: 1rem;
            flex-wrap: wrap;
        }
        
        #rpaModal .progress-info .info-item {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 0.9rem;
            opacity: 0.9;
        }
        
        #rpaModal .progress-info .info-item i {
            font-size: 1rem;
        }
        
        /* Conteúdo principal */
        #rpaModal .modal-content {
            padding: 2rem;
            background: var(--imediato-white);
            border-radius: 0 0 20px 20px;
        }
        
        /* Cards de informações */
        #rpaModal .info-cards {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
        }
        
        #rpaModal .info-card {
            background: var(--imediato-gray);
            border-radius: 15px;
            padding: 1.5rem;
            border: 1px solid var(--imediato-border);
            transition: all 0.3s ease;
        }
        
        #rpaModal .info-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px var(--imediato-shadow-hover);
        }
        
        .card-header {
            display: flex;
            align-items: center;
            gap: 1rem;
            margin-bottom: 1.5rem;
        }
        
        .card-icon {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            background: linear-gradient(135deg, var(--imediato-dark-blue), var(--imediato-light-blue));
            color: var(--imediato-white) !important;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem !important;
            font-weight: 600;
        }
        
        .card-title {
            color: var(--imediato-text) !important;
            font-size: 1.1rem !important;
            font-weight: 600;
            margin: 0;
        }
        
        .card-subtitle {
            color: var(--imediato-text-light) !important;
            font-size: 0.9rem !important;
            margin: 0.5rem 0 0 0;
        }
        
        .card-content {
            margin-top: 1rem;
        }
        
        .card-features {
            list-style: none;
            padding: 0;
            margin: 0;
        }
        
        .card-features li {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            margin-bottom: 0.5rem;
            color: var(--imediato-text) !important;
            font-size: 0.9rem !important;
        }
        
        .card-features li i {
            color: var(--imediato-light-blue);
            font-size: 0.8rem;
        }
        
        /* Timeline de progresso */
        #rpaModal .progress-timeline {
            background: var(--imediato-gray);
            border-radius: 15px;
            padding: 1.5rem;
            margin-bottom: 2rem;
            border: 1px solid var(--imediato-border);
        }
        
        #rpaModal .timeline-header {
            display: flex;
            align-items: center;
            gap: 1rem;
            margin-bottom: 1.5rem;
        }
        
        #rpaModal .timeline-title {
            color: var(--imediato-text) !important;
            font-size: 1.1rem !important;
            font-weight: 600;
            margin: 0;
        }
        
        #rpaModal .timeline-list {
            list-style: none;
            padding: 0;
            margin: 0;
        }
        
        #rpaModal .timeline-item {
            display: flex;
            align-items: flex-start;
            gap: 1rem;
            margin-bottom: 1rem;
            padding: 1rem;
            background: var(--imediato-white);
            border-radius: 10px;
            border-left: 4px solid var(--imediato-light-blue);
        }
        
        #rpaModal .timeline-item.completed {
            border-left-color: #28a745;
            background: #f8fff9;
        }
        
        #rpaModal .timeline-item.error {
            border-left-color: #dc3545;
            background: #fff8f8;
        }
        
        #rpaModal .timeline-item.current {
            border-left-color: var(--imediato-dark-blue);
            background: #f0f8ff;
            animation: pulse 2s infinite;
        }
        
        #rpaModal .timeline-icon {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1rem;
            font-weight: 600;
            flex-shrink: 0;
        }
        
        #rpaModal .timeline-item.completed .timeline-icon {
            background: #28a745;
            color: white;
        }
        
        #rpaModal .timeline-item.error .timeline-icon {
            background: #dc3545;
            color: white;
        }
        
        #rpaModal .timeline-item.current .timeline-icon {
            background: var(--imediato-dark-blue);
            color: white;
        }
        
        #rpaModal .timeline-item.pending .timeline-icon {
            background: var(--imediato-border);
            color: var(--imediato-text-light);
        }
        
        #rpaModal .timeline-content {
            flex: 1;
        }
        
        #rpaModal .timeline-phase {
            color: var(--imediato-text) !important;
            font-size: 1rem !important;
            font-weight: 600;
            margin: 0 0 0.5rem 0;
        }
        
        #rpaModal .timeline-description {
            color: var(--imediato-text-light) !important;
            font-size: 0.9rem !important;
            margin: 0;
        }
        
        #rpaModal .timeline-time {
            color: var(--imediato-text-light) !important;
            font-size: 0.8rem !important;
            margin-top: 0.5rem;
        }
        
        /* Botão de fechar */
        #rpaModal .close-button {
            position: absolute !important;
            top: 1rem !important;
            right: 1rem !important;
            width: 40px !important;
            height: 40px !important;
            border: none !important;
            background: rgba(255, 255, 255, 0.2) !important;
            border-radius: 50% !important;
            color: var(--imediato-white) !important;
            font-size: 16px !important;
            cursor: pointer !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            z-index: 10002 !important;
            transition: all 0.3s ease !important;
        }
        
        #rpaModal .close-button:hover {
            background: rgba(255, 255, 255, 0.3) !important;
            transform: scale(1.1) !important;
        }
        
        /* Resultados finais */
        #rpaModal .results-container {
            background: var(--imediato-gray);
            border-radius: 15px;
            padding: 1.5rem;
            margin-bottom: 2rem;
            border: 1px solid var(--imediato-border);
        }
        
        #rpaModal .results-header {
            display: flex;
            align-items: center;
            gap: 1rem;
            margin-bottom: 1.5rem;
        }
        
        #rpaModal .results-title {
            color: var(--imediato-text) !important;
            font-size: 1.1rem !important;
            font-weight: 600;
            margin: 0;
        }
        
        #rpaModal .results-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
        }
        
        #rpaModal .result-item {
            background: var(--imediato-white);
            border-radius: 10px;
            padding: 1rem;
            text-align: center;
            border: 1px solid var(--imediato-border);
        }
        
        #rpaModal .result-label {
            color: var(--imediato-text-light) !important;
            font-size: 0.8rem !important;
            font-weight: 500;
            margin-bottom: 0.5rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        #rpaModal .result-value {
            color: var(--imediato-text) !important;
            font-size: 1.5rem !important;
            font-weight: 700;
            margin: 0;
        }
        
        /* Mensagem de contato */
        #rpaModal .contact-message {
            background: linear-gradient(135deg, #e8f5e8, #f0f8f0);
            border: 1px solid #c3e6c3;
            border-radius: 15px;
            padding: 1.5rem;
            margin-bottom: 2rem;
            text-align: center;
            color: var(--imediato-text) !important;
            font-size: 1rem !important;
            font-weight: 500;
        }
        
        #rpaModal .contact-message i {
            color: #28a745;
            margin-right: 0.5rem;
        }
        
        /* Botões de ação */
        #rpaModal .action-buttons {
            display: flex;
            gap: 1rem;
            justify-content: center;
            margin-top: 2rem;
        }
        
        #rpaModal .action-button {
            background: linear-gradient(135deg, var(--imediato-dark-blue), var(--imediato-light-blue));
            color: var(--imediato-white) !important;
            border: none;
            border-radius: 10px;
            padding: 1rem 2rem;
            font-size: 1rem !important;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        #rpaModal .action-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px var(--imediato-shadow-hover);
        }
        
        /* Animações */
        @keyframes pulse {
            0%, 100% {
                opacity: 1;
            }
            50% {
                opacity: 0.7;
            }
        }
        
        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        @keyframes slideIn {
            from {
                transform: translateX(-100%);
            }
            to {
                transform: translateX(0);
            }
        }
        
        /* Responsividade */
        @media (max-width: 768px) {
            #rpaModal {
                padding: 1rem !important;
            }
            
            #rpaModal .modal-container {
                max-width: 100% !important;
                max-height: 90vh !important;
            }
            
            #rpaModal .modal-content {
                padding: 1rem;
            }
            
            #rpaModal .info-cards {
                grid-template-columns: 1fr;
            }
            
            #rpaModal .progress-info {
                flex-direction: column;
                gap: 0.5rem;
            }
            
            #rpaModal .action-buttons {
                flex-direction: column;
            }
        }
        
        /* SPINNER TIMER CONTAINER */
        .spinner-timer-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 2rem;
            background: var(--imediato-gray);
            border-radius: 15px;
            margin: 1rem 0;
            border-top: 2px solid var(--imediato-border);
        }
        
        .spinner-container {
            position: relative;
            width: 120px;
            height: 120px;
            margin-bottom: 1rem;
        }
        
        /* SpinKit Modelo 8 - Circle */
        .sk-circle {
            width: 120px;
            height: 120px;
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
            background-color: var(--imediato-dark-blue);
            border-radius: 100%;
            animation: sk-circle-bounce-delay 1.2s infinite ease-in-out both;
        }
        
        .sk-circle .sk-child:nth-child(1) { transform: rotate(30deg); }
        .sk-circle .sk-child:nth-child(2) { transform: rotate(60deg); }
        .sk-circle .sk-child:nth-child(3) { transform: rotate(90deg); }
        .sk-circle .sk-child:nth-child(4) { transform: rotate(120deg); }
        .sk-circle .sk-child:nth-child(5) { transform: rotate(150deg); }
        .sk-circle .sk-child:nth-child(6) { transform: rotate(180deg); }
        .sk-circle .sk-child:nth-child(7) { transform: rotate(210deg); }
        .sk-circle .sk-child:nth-child(8) { transform: rotate(240deg); }
        .sk-circle .sk-child:nth-child(9) { transform: rotate(270deg); }
        .sk-circle .sk-child:nth-child(10) { transform: rotate(300deg); }
        .sk-circle .sk-child:nth-child(11) { transform: rotate(330deg); }
        .sk-circle .sk-child:nth-child(12) { transform: rotate(360deg); }
        
        .sk-circle .sk-child:nth-child(1):before { animation-delay: -1.1s; }
        .sk-circle .sk-child:nth-child(2):before { animation-delay: -1s; }
        .sk-circle .sk-child:nth-child(3):before { animation-delay: -0.9s; }
        .sk-circle .sk-child:nth-child(4):before { animation-delay: -0.8s; }
        .sk-circle .sk-child:nth-child(5):before { animation-delay: -0.7s; }
        .sk-circle .sk-child:nth-child(6):before { animation-delay: -0.6s; }
        .sk-circle .sk-child:nth-child(7):before { animation-delay: -0.5s; }
        .sk-circle .sk-child:nth-child(8):before { animation-delay: -0.4s; }
        .sk-circle .sk-child:nth-child(9):before { animation-delay: -0.3s; }
        .sk-circle .sk-child:nth-child(10):before { animation-delay: -0.2s; }
        .sk-circle .sk-child:nth-child(11):before { animation-delay: -0.1s; }
        .sk-circle .sk-child:nth-child(12):before { animation-delay: 0s; }
        
        @keyframes sk-circle-bounce-delay {
            0%, 80%, 100% {
                transform: scale(0);
            }
            40% {
                transform: scale(1);
            }
        }
        
        .spinner-center {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 80px;
            height: 80px;
            background: linear-gradient(45deg, var(--imediato-dark-blue), var(--imediato-light-blue));
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 14px;
            font-weight: 700;
            color: var(--imediato-white);
            text-align: center;
            box-shadow: 0 4px 15px rgba(0, 51, 102, 0.3);
            font-family: 'Courier New', monospace;
        }
        
        .timer-message {
            text-align: center;
            padding: 12px 20px;
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            border-radius: 10px;
            color: #856404;
            font-size: 0.9rem;
            font-weight: 500;
            margin: 1rem 0;
            text-align: center;
            font-weight: 500;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0.5rem;
        }
    `;
    
    // ========================================
    // 2. CLASSE SPINNER TIMER
    // ========================================
    
    class SpinnerTimer {
        constructor() {
            this.initialDuration = 180; // 3 minutos em segundos
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
            
            console.log('🔄 Inicializando SpinnerTimer...');
            console.log('📍 spinnerCenter encontrado:', !!this.elements.spinnerCenter);
            console.log('📍 timerMessage encontrado:', !!this.elements.timerMessage);
            
            if (!this.elements.spinnerCenter) {
                console.warn('⚠️ Elementos do spinner timer não encontrados');
                return;
            }
            
            console.log('✅ Iniciando timer...');
            this.start();
        }
        
        start() {
            this.isRunning = true;
            this.totalDuration = this.initialDuration;
            this.remainingSeconds = this.initialDuration;
            
            console.log('⏰ Timer iniciado:', this.remainingSeconds, 'segundos');
            
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
                console.log('🔄 Timer atualizado:', timerText);
            } else {
                console.warn('⚠️ spinnerCenter não encontrado para atualizar');
            }
        }
        
        stop() {
            this.isRunning = false;
            clearInterval(this.interval);
        }
        
        reset() {
            this.stop();
            this.isExtended = false;
            this.totalDuration = this.initialDuration;
            this.remainingSeconds = this.initialDuration;
            
            if (this.elements.timerMessage) {
                this.elements.timerMessage.style.display = 'none';
            }
            
            this.updateDisplay();
        }
    }
    
    // ========================================
    // 3. CLASSE PROGRESS MODAL RPA
    // ========================================
    
    class ProgressModalRPA {
        constructor(sessionId) {
            this.apiBaseUrl = 'https://rpaimediatoseguros.com.br';
            this.sessionId = sessionId;
            this.progressInterval = null;
            this.isProcessing = true;
            this.spinnerTimer = null; // Será inicializado quando necessário
            this.spinnerTimerInitialized = false; // Controle de inicialização
            
            // Controle de atualizações
            this.initialEstimateUpdated = false;
            
            // Mensagens das 16 fases do RPA
            this.phaseMessages = {
                1: { title: "Iniciando Processo", description: "Conectando ao sistema..." },
                2: { title: "Acessando Portal", description: "Carregando página inicial..." },
                3: { title: "Preenchendo Dados", description: "Inserindo informações do veículo..." },
                4: { title: "Validando Informações", description: "Verificando dados inseridos..." },
                5: { title: "Processando Cotação", description: "Calculando valores..." },
                6: { title: "Aguardando Resultados", description: "Processando solicitação..." },
                7: { title: "Analisando Propostas", description: "Comparando opções..." },
                8: { title: "Gerando Relatório", description: "Preparando resultados..." },
                9: { title: "Finalizando Processo", description: "Concluindo operação..." },
                10: { title: "Verificando Dados", description: "Validando informações finais..." },
                11: { title: "Processando Pagamento", description: "Calculando valores finais..." },
                12: { title: "Gerando Contrato", description: "Preparando documentação..." },
                13: { title: "Enviando Proposta", description: "Finalizando cotação..." },
                14: { title: "Confirmando Dados", description: "Verificando informações..." },
                15: { title: "Processando Final", description: "Concluindo operação..." },
                16: { title: "Concluído", description: "Processo finalizado com sucesso!" }
            };
            
            this.lastProgressData = null;
            this.pollCount = 0;
            this.maxPolls = 300; // 10 minutos (300 * 2 segundos)
            
            console.log('🚀 ProgressModalRPA inicializado com sessionId:', this.sessionId);
        }
        
        setSessionId(sessionId) {
            this.sessionId = sessionId;
            console.log('🔄 SessionId atualizado:', this.sessionId);
            
            // Inicializar spinner timer apenas se não foi inicializado
            if (!this.spinnerTimerInitialized) {
                setTimeout(() => {
                    this.initSpinnerTimer();
                    this.spinnerTimerInitialized = true;
                }, 1000);
            }
        }
        
        initSpinnerTimer() {
            if (!this.spinnerTimer) {
                this.spinnerTimer = new SpinnerTimer();
                this.spinnerTimer.init();
                console.log('✅ SpinnerTimer inicializado');
            }
        }
        
        stopSpinnerTimer() {
            if (this.spinnerTimer) {
                this.spinnerTimer.finish(); // Para o timer completamente
                this.spinnerTimer = null;
                console.log('⏹️ SpinnerTimer parado');
            }
            
            // Esconder o spinner completamente
            const spinnerContainer = document.getElementById('spinnerTimerContainer');
            if (spinnerContainer) {
                spinnerContainer.style.display = 'none';
                console.log('✅ Spinner timer escondido');
            }
        }
        
        startProgressPolling() {
            if (!this.sessionId) {
                console.error('❌ SessionId não definido para polling');
                return;
            }
            
            console.log('🔄 Iniciando polling de progresso...');
            this.pollCount = 0;
            
            this.progressInterval = setInterval(() => {
                this.pollCount++;
                console.log(`🔄 Polling ${this.pollCount}/${this.maxPolls}`);
                
                if (this.pollCount > this.maxPolls) {
                    console.error('❌ Timeout: Processamento demorou mais de 10 minutos');
                    this.stopProgressPolling();
                    this.stopSpinnerTimer(); // ← NOVA LINHA: Parar spinner em timeout
                    this.showErrorAlert('O processamento está demorando mais que o esperado (10 minutos). Tente novamente ou entre em contato conosco.');
                    return;
                }
                
                this.updateProgress();
            }, 2000);
        }
        
        stopProgressPolling() {
            if (this.progressInterval) {
                clearInterval(this.progressInterval);
                this.progressInterval = null;
                console.log('⏹️ Polling interrompido');
            }
        }
        
        async updateProgress() {
            try {
                const response = await fetch(`${this.apiBaseUrl}/progress/${this.sessionId}`);
                const progressData = await response.json();
                
                console.log('📊 Dados de progresso recebidos:', progressData);
                this.lastProgressData = progressData;
                
                // Verificar se há erro
                if (progressData.erro) {
                    const mensagem = progressData.mensagem || 'Erro desconhecido';
                    const errorCode = progressData.codigo_erro || null;
                    console.error('❌ Erro detectado no progresso:', mensagem);
                    this.handleRPAError(mensagem, errorCode);
                    return;
                }
                
                // Verificar status
                const currentStatus = progressData.status;
                if (currentStatus === 'error' || currentStatus === 'failed') {
                    const mensagem = progressData.mensagem || `Status: ${currentStatus}`;
                    console.error('❌ Status de erro detectado:', mensagem);
                    this.handleRPAError(mensagem, errorCode);
                    return;
                }
                
                // Lógica corrigida: usar fase 16 quando status for 'success'
                let currentPhase = progressData.fase_atual || progressData.etapa_atual || 1;
                
                // Se status é 'success', forçar fase 16 (finalização completa)
                if (currentStatus === 'success') {
                    currentPhase = 16;
                }
                
                // Atualizar interface
                this.updateProgressBar(currentPhase);
                this.updateTimeline(progressData);
                
                // Atualizar estimativa inicial apenas uma vez
                if (!this.initialEstimateUpdated && progressData.estimativa_inicial) {
                    this.updateInitialEstimate(progressData);
                }
                
                // Verificar se há resultados finais
                if (progressData.resultados_finais || progressData.resultados) {
                    this.updateResults(progressData);
                    this.updateSuccessHeader();
                    
                    if (currentStatus === 'success') {
                        console.log('🎉 RPA concluído com sucesso!');
                        this.stopProgressPolling();
                        this.isProcessing = false;
                        this.stopSpinnerTimer(); // ← NOVA LINHA: Parar spinner em sucesso
                    }
                }
            } catch (error) {
                console.error('❌ Erro ao buscar progresso:', error);
                this.handleRPAError('Erro de conexão com o servidor', 500);
            }
        }
        
        updateProgressBar(phase) {
            const progressBar = document.querySelector('#rpaModal .progress-bar');
            if (progressBar) {
                const percentage = (phase / 16) * 100;
                progressBar.style.width = `${percentage}%`;
                console.log(`📊 Barra de progresso atualizada: ${percentage}%`);
            }
        }
        
        updateTimeline(progressData) {
            const timelineList = document.querySelector('#rpaModal .timeline-list');
            if (!timelineList) return;
            
            const currentPhase = progressData.fase_atual || progressData.etapa_atual || 1;
            const timeline = progressData.timeline || [];
            
            // Limpar timeline existente
            timelineList.innerHTML = '';
            
            // Adicionar itens da timeline
            timeline.forEach((entry, index) => {
                const timelineItem = document.createElement('li');
                timelineItem.className = 'timeline-item';
                
                // Determinar status do item
                if (entry.erro) {
                    timelineItem.classList.add('error');
                } else if (entry.fase === currentPhase) {
                    timelineItem.classList.add('current');
                } else if (entry.fase < currentPhase) {
                    timelineItem.classList.add('completed');
                } else {
                    timelineItem.classList.add('pending');
                }
                
                // Ícone baseado no status
                let icon = '⏳';
                if (entry.erro) {
                    icon = '❌';
                } else if (entry.fase === currentPhase) {
                    icon = '🔄';
                } else if (entry.fase < currentPhase) {
                    icon = '✅';
                }
                
                timelineItem.innerHTML = `
                    <div class="timeline-icon">${icon}</div>
                    <div class="timeline-content">
                        <div class="timeline-phase">${entry.fase || index + 1}. ${entry.titulo || 'Processando...'}</div>
                        <div class="timeline-description">${entry.descricao || 'Aguarde...'}</div>
                        ${entry.timestamp ? `<div class="timeline-time">${new Date(entry.timestamp).toLocaleTimeString()}</div>` : ''}
                    </div>
                `;
                
                timelineList.appendChild(timelineItem);
            });
        }
        
        updateInitialEstimate(progressData) {
            const estimateCard = document.querySelector('#rpaModal .info-card[data-type="estimate"]');
            if (estimateCard && progressData.estimativa_inicial) {
                const estimateValue = estimateCard.querySelector('.value');
                if (estimateValue) {
                    estimateValue.textContent = progressData.estimativa_inicial;
                    this.initialEstimateUpdated = true;
                    console.log('💰 Estimativa inicial atualizada:', progressData.estimativa_inicial);
                }
            }
            
            // Adicionar animação de pulso na estimativa
            const estimateCard = document.querySelector('#rpaModal .info-card[data-type="estimate"]');
            if (estimateCard) {
                estimateCard.style.animation = 'pulse 2s infinite';
            }
        }
        
        updateResults(data) {
            console.log('📊 Atualizando resultados finais:', data);
            console.log('📊 Estrutura completa dos dados:', JSON.stringify(data, null, 2));
            
            // Buscar resultados em múltiplas estruturas possíveis
            let resultados = null;
            
            if (data.resultados_finais) {
                resultados = data.resultados_finais;
            } else if (data.resultados) {
                resultados = data.resultados;
            } else if (data.dados_finais) {
                resultados = data.dados_finais;
            }
            
            if (!resultados) {
                console.warn('⚠️ Nenhum resultado encontrado nos dados');
                return;
            }
            
            console.log('📊 Resultados encontrados:', resultados);
            
            // Mapear campos de resultado para elementos do DOM
            const fieldMappings = {
                'valor_total': 'result-total',
                'valor_premio': 'result-premium',
                'valor_iof': 'result-iof',
                'valor_comissao': 'result-commission',
                'valor_desconto': 'result-discount',
                'valor_parcela': 'result-installment',
                'quantidade_parcelas': 'result-installments',
                'data_vencimento': 'result-due-date',
                'seguradora': 'result-insurer',
                'produto': 'result-product',
                'cobertura': 'result-coverage',
                'franquia': 'result-deductible',
                'valor_franquia': 'result-deductible-value',
                'assistencia': 'result-assistance',
                'protecao': 'result-protection',
                'bonus': 'result-bonus',
                'classe_bonus': 'result-bonus-class',
                'sinistro': 'result-claim',
                'valor_sinistro': 'result-claim-value',
                'data_sinistro': 'result-claim-date',
                'status': 'result-status',
                'observacoes': 'result-notes',
                'data_cotacao': 'result-quote-date',
                'validade_cotacao': 'result-quote-validity',
                'numero_cotacao': 'result-quote-number',
                'corretor': 'result-broker',
                'telefone_corretor': 'result-broker-phone',
                'email_corretor': 'result-broker-email',
                'endereco_corretor': 'result-broker-address',
                'cnpj_corretor': 'result-broker-cnpj',
                'creci_corretor': 'result-broker-creci',
                'nome_segurado': 'result-insured-name',
                'cpf_segurado': 'result-insured-cpf',
                'rg_segurado': 'result-insured-rg',
                'data_nascimento_segurado': 'result-insured-birth',
                'sexo_segurado': 'result-insured-gender',
                'estado_civil_segurado': 'result-insured-marital',
                'profissao_segurado': 'result-insured-profession',
                'renda_segurado': 'result-insured-income',
                'endereco_segurado': 'result-insured-address',
                'cep_segurado': 'result-insured-zip',
                'cidade_segurado': 'result-insured-city',
                'estado_segurado': 'result-insured-state',
                'telefone_segurado': 'result-insured-phone',
                'celular_segurado': 'result-insured-mobile',
                'email_segurado': 'result-insured-email',
                'nome_condutor': 'result-driver-name',
                'cpf_condutor': 'result-driver-cpf',
                'rg_condutor': 'result-driver-rg',
                'data_nascimento_condutor': 'result-driver-birth',
                'sexo_condutor': 'result-driver-gender',
                'estado_civil_condutor': 'result-driver-marital',
                'profissao_condutor': 'result-driver-profession',
                'renda_condutor': 'result-driver-income',
                'endereco_condutor': 'result-driver-address',
                'cep_condutor': 'result-driver-zip',
                'cidade_condutor': 'result-driver-city',
                'estado_condutor': 'result-driver-state',
                'telefone_condutor': 'result-driver-phone',
                'celular_condutor': 'result-driver-mobile',
                'email_condutor': 'result-driver-email',
                'nome_veiculo': 'result-vehicle-name',
                'marca_veiculo': 'result-vehicle-brand',
                'modelo_veiculo': 'result-vehicle-model',
                'ano_veiculo': 'result-vehicle-year',
                'placa_veiculo': 'result-vehicle-plate',
                'chassi_veiculo': 'result-vehicle-chassis',
                'renavam_veiculo': 'result-vehicle-renavam',
                'cor_veiculo': 'result-vehicle-color',
                'combustivel_veiculo': 'result-vehicle-fuel',
                'categoria_veiculo': 'result-vehicle-category',
                'tipo_veiculo': 'result-vehicle-type',
                'uso_veiculo': 'result-vehicle-usage',
                'garagem_veiculo': 'result-vehicle-garage',
                'alarme_veiculo': 'result-vehicle-alarm',
                'rastreador_veiculo': 'result-vehicle-tracker',
                'blindagem_veiculo': 'result-vehicle-armor',
                'valor_veiculo': 'result-vehicle-value',
                'valor_fipe_veiculo': 'result-vehicle-fipe',
                'km_veiculo': 'result-vehicle-mileage',
                'data_aquisicao_veiculo': 'result-vehicle-acquisition',
                'proprietario_veiculo': 'result-vehicle-owner',
                'financiamento_veiculo': 'result-vehicle-financing',
                'banco_financiamento': 'result-financing-bank',
                'valor_financiamento': 'result-financing-value',
                'parcelas_financiamento': 'result-financing-installments',
                'valor_parcela_financiamento': 'result-financing-installment-value',
                'data_vencimento_financiamento': 'result-financing-due-date',
                'saldo_devedor_financiamento': 'result-financing-balance',
                'cobertura_veiculo': 'result-vehicle-coverage',
                'franquia_veiculo': 'result-vehicle-deductible',
                'valor_franquia_veiculo': 'result-vehicle-deductible-value',
                'assistencia_veiculo': 'result-vehicle-assistance',
                'protecao_veiculo': 'result-vehicle-protection',
                'bonus_veiculo': 'result-vehicle-bonus',
                'classe_bonus_veiculo': 'result-vehicle-bonus-class',
                'sinistro_veiculo': 'result-vehicle-claim',
                'valor_sinistro_veiculo': 'result-vehicle-claim-value',
                'data_sinistro_veiculo': 'result-vehicle-claim-date',
                'status_veiculo': 'result-vehicle-status',
                'observacoes_veiculo': 'result-vehicle-notes',
                'data_cotacao_veiculo': 'result-vehicle-quote-date',
                'validade_cotacao_veiculo': 'result-vehicle-quote-validity',
                'numero_cotacao_veiculo': 'result-vehicle-quote-number',
                'corretor_veiculo': 'result-vehicle-broker',
                'telefone_corretor_veiculo': 'result-vehicle-broker-phone',
                'email_corretor_veiculo': 'result-vehicle-broker-email',
                'endereco_corretor_veiculo': 'result-vehicle-broker-address',
                'cnpj_corretor_veiculo': 'result-vehicle-broker-cnpj',
                'creci_corretor_veiculo': 'result-vehicle-broker-creci'
            };
            
            // Atualizar campos de resultado
            Object.entries(fieldMappings).forEach(([dataField, elementId]) => {
                if (resultados[dataField] !== undefined) {
                    this.updateResultField(elementId, resultados[dataField]);
                }
            });
            
            // Mostrar container de resultados
            const resultsContainer = document.querySelector('#rpaModal .results-container');
            if (resultsContainer) {
                resultsContainer.style.display = 'block';
                console.log('📊 Container de resultados exibido');
            }
        }
        
        updateResultField(elementId, value) {
            const element = document.getElementById(elementId);
            if (element) {
                // Formatar valor se for numérico
                if (typeof value === 'number') {
                    if (elementId.includes('valor') || elementId.includes('premio') || elementId.includes('total')) {
                        value = `R$ ${value.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
                    } else if (elementId.includes('parcela') || elementId.includes('installment')) {
                        value = value.toString();
                    }
                }
                
                element.innerHTML = value;
                console.log(`✅ Campo ${elementId} atualizado:`, value);
            }
        }
        
        updateSuccessHeader() {
            const progressHeader = document.querySelector('#rpaModal .progress-header');
            if (progressHeader) {
                const contactMessage = document.createElement('p');
                contactMessage.className = 'contact-message';
                contactMessage.innerHTML = '<i class="fas fa-phone"></i> Um especialista da Imediato Seguros entrará em contato em instantes para passar os detalhes!';
                
                progressHeader.appendChild(contactMessage);
                console.log('📞 Mensagem de contato adicionada ao header');
            }
        }
        
        showErrorAlert(message) {
            if (typeof Swal !== 'undefined') {
                Swal.fire({
                    title: 'Erro no Processamento',
                    text: message,
                    icon: 'error',
                    confirmButtonText: 'OK',
                    confirmButtonColor: '#dc3545'
                });
            } else {
                alert(message);
            }
        }
        
        /**
         * Tratamento de erros do RPA
         * Mapeia códigos de erro para mensagens específicas
         */
        handleRPAError(mensagem, errorCode = null) {
            console.error('🚨 Tratando erro do RPA:', { mensagem, errorCode });
            
            // Parar o polling
            this.stopProgressPolling();
            this.isProcessing = false;
            this.stopSpinnerTimer(); // ← NOVA LINHA: Parar spinner em erro
            
            // Remover modal de progresso
            const modal = document.getElementById('rpaModal');
            if (modal) {
                modal.remove();
            }
            
            // Verificar se há erro na timeline (buscar nos dados de progresso mais recentes)
            const timeline = this.lastProgressData?.timeline;
            const timelineWithError = timeline?.find(entry => entry.erro !== null);
            
            if (timelineWithError) {
                // Mostrar SweetAlert específico para cotação manual para QUALQUER erro
                if (typeof Swal !== 'undefined') {
                    Swal.fire({
                        title: 'Cotação Manual Necessária',
                        text: 'Não foi possível efetuar o cálculo nesse momento. Um especialista da Imediato Seguros fará o cálculo manualmente e entrará em contato para envia-lo à você em seguida.',
                        icon: 'info',
                        confirmButtonText: 'Entendi',
                        confirmButtonColor: '#007bff',
                        showCancelButton: false,
                        allowOutsideClick: false,
                        allowEscapeKey: false
                    });
                } else {
                    alert('Não foi possível efetuar o cálculo nesse momento. Um especialista da Imediato Seguros fará o cálculo manualmente e entrará em contato para envia-lo à você em seguida.');
                }
            } else {
                // Erro genérico
                this.showErrorAlert(mensagem);
            }
        }
    }
    
    // ========================================
    // 4. CLASSE MAIN PAGE
    // ========================================
    
    class MainPage {
        constructor() {
            this.modal = null;
            this.currentSessionId = null;
            
            console.log('🚀 MainPage inicializada');
        }
        
        createModal() {
            const modalHTML = `
                <div id="rpaModal" class="modal">
                    <div class="modal-container">
                        <div class="modal-progress-bar">
                            <div class="progress-bar" style="width: 0%"></div>
                        </div>
                        
                        <div class="progress-header">
                            <h1>
                                <i class="fas fa-cog fa-spin"></i>
                                Processando sua Cotação
                            </h1>
                            <p class="progress-text">Aguarde enquanto processamos suas informações...</p>
                            
                            <div class="progress-info">
                                <div class="info-item">
                                    <i class="fas fa-clock"></i>
                                    <span>Tempo estimado: 3-5 minutos</span>
                                </div>
                                <div class="info-item">
                                    <i class="fas fa-shield-alt"></i>
                                    <span>Processo seguro</span>
                                </div>
                                <div class="info-item">
                                    <i class="fas fa-user-tie"></i>
                                    <span>Especialista disponível</span>
                                </div>
                            </div>
                        </div>
                        
                        <div class="modal-content">
                            <div class="info-cards">
                                <div class="info-card" data-type="estimate">
                                    <div class="card-header">
                                        <div class="card-icon">💰</div>
                                        <div>
                                            <h3 class="card-title">Estimativa Inicial</h3>
                                            <p class="card-subtitle">Valor aproximado</p>
                                        </div>
                                    </div>
                                    <div class="card-content">
                                        <div class="value">R$ 0,00</div>
                                    </div>
                                </div>
                                
                                <div class="info-card" data-type="process">
                                    <div class="card-header">
                                        <div class="card-icon">⚙️</div>
                                        <div>
                                            <h3 class="card-title">Processo Automatizado</h3>
                                            <p class="card-subtitle">RPA em execução</p>
                                        </div>
                                    </div>
                                    <div class="card-content">
                                        <ul class="card-features">
                                            <li><i class="fas fa-check"></i> Preenchimento automático</li>
                                            <li><i class="fas fa-check"></i> Validação de dados</li>
                                            <li><i class="fas fa-check"></i> Cálculo de valores</li>
                                            <li><i class="fas fa-check"></i> Geração de proposta</li>
                                        </ul>
                                    </div>
                                </div>
                                
                                <div class="info-card" data-type="support">
                                    <div class="card-header">
                                        <div class="card-icon">👨‍💼</div>
                                        <div>
                                            <h3 class="card-title">Suporte Especializado</h3>
                                            <p class="card-subtitle">Sempre disponível</p>
                                        </div>
                                    </div>
                                    <div class="card-content">
                                        <ul class="card-features">
                                            <li><i class="fas fa-check"></i> Especialista em seguros</li>
                                            <li><i class="fas fa-check"></i> Atendimento personalizado</li>
                                            <li><i class="fas fa-check"></i> Suporte técnico</li>
                                            <li><i class="fas fa-check"></i> Acompanhamento completo</li>
                                        </ul>
                                    </div>
                                </div>
                            </div>
                            
                            <div class="progress-timeline">
                                <div class="timeline-header">
                                    <div class="card-icon">📋</div>
                                    <h3 class="timeline-title">Progresso do Processo</h3>
                                </div>
                                <ul class="timeline-list">
                                    <!-- Timeline será preenchida dinamicamente -->
                                </ul>
                            </div>
                            
                            <div class="results-container" style="display: none;">
                                <div class="results-header">
                                    <div class="card-icon">📊</div>
                                    <h3 class="results-title">Resultados da Cotação</h3>
                                </div>
                                <div class="results-grid">
                                    <div class="result-item">
                                        <div class="result-label">Valor Total</div>
                                        <div class="result-value" id="result-total">R$ 0,00</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">Prêmio</div>
                                        <div class="result-value" id="result-premium">R$ 0,00</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">IOF</div>
                                        <div class="result-value" id="result-iof">R$ 0,00</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">Comissão</div>
                                        <div class="result-value" id="result-commission">R$ 0,00</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">Desconto</div>
                                        <div class="result-value" id="result-discount">R$ 0,00</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">Valor da Parcela</div>
                                        <div class="result-value" id="result-installment">R$ 0,00</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">Quantidade de Parcelas</div>
                                        <div class="result-value" id="result-installments">0</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">Data de Vencimento</div>
                                        <div class="result-value" id="result-due-date">-</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">Seguradora</div>
                                        <div class="result-value" id="result-insurer">-</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">Produto</div>
                                        <div class="result-value" id="result-product">-</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">Cobertura</div>
                                        <div class="result-value" id="result-coverage">-</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">Franquia</div>
                                        <div class="result-value" id="result-deductible">-</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">Valor da Franquia</div>
                                        <div class="result-value" id="result-deductible-value">R$ 0,00</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">Assistência</div>
                                        <div class="result-value" id="result-assistance">-</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">Proteção</div>
                                        <div class="result-value" id="result-protection">-</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">Bônus</div>
                                        <div class="result-value" id="result-bonus">-</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">Classe de Bônus</div>
                                        <div class="result-value" id="result-bonus-class">-</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">Sinistro</div>
                                        <div class="result-value" id="result-claim">-</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">Valor do Sinistro</div>
                                        <div class="result-value" id="result-claim-value">R$ 0,00</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">Data do Sinistro</div>
                                        <div class="result-value" id="result-claim-date">-</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">Status</div>
                                        <div class="result-value" id="result-status">-</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">Observações</div>
                                        <div class="result-value" id="result-notes">-</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">Data da Cotação</div>
                                        <div class="result-value" id="result-quote-date">-</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">Validade da Cotação</div>
                                        <div class="result-value" id="result-quote-validity">-</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">Número da Cotação</div>
                                        <div class="result-value" id="result-quote-number">-</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">Corretor</div>
                                        <div class="result-value" id="result-broker">-</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">Telefone do Corretor</div>
                                        <div class="result-value" id="result-broker-phone">-</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">Email do Corretor</div>
                                        <div class="result-value" id="result-broker-email">-</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">Endereço do Corretor</div>
                                        <div class="result-value" id="result-broker-address">-</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">CNPJ do Corretor</div>
                                        <div class="result-value" id="result-broker-cnpj">-</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">CRECI do Corretor</div>
                                        <div class="result-value" id="result-broker-creci">-</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">Nome do Segurado</div>
                                        <div class="result-value" id="result-insured-name">-</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">CPF do Segurado</div>
                                        <div class="result-value" id="result-insured-cpf">-</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">RG do Segurado</div>
                                        <div class="result-value" id="result-insured-rg">-</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">Data de Nascimento do Segurado</div>
                                        <div class="result-value" id="result-insured-birth">-</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">Sexo do Segurado</div>
                                        <div class="result-value" id="result-insured-gender">-</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">Estado Civil do Segurado</div>
                                        <div class="result-value" id="result-insured-marital">-</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">Profissão do Segurado</div>
                                        <div class="result-value" id="result-insured-profession">-</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">Renda do Segurado</div>
                                        <div class="result-value" id="result-insured-income">R$ 0,00</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">Endereço do Segurado</div>
                                        <div class="result-value" id="result-insured-address">-</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">CEP do Segurado</div>
                                        <div class="result-value" id="result-insured-zip">-</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">Cidade do Segurado</div>
                                        <div class="result-value" id="result-insured-city">-</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">Estado do Segurado</div>
                                        <div class="result-value" id="result-insured-state">-</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">Telefone do Segurado</div>
                                        <div class="result-value" id="result-insured-phone">-</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">Celular do Segurado</div>
                                        <div class="result-value" id="result-insured-mobile">-</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">Email do Segurado</div>
                                        <div class="result-value" id="result-insured-email">-</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">Nome do Condutor</div>
                                        <div class="result-value" id="result-driver-name">-</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">CPF do Condutor</div>
                                        <div class="result-value" id="result-driver-cpf">-</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">RG do Condutor</div>
                                        <div class="result-value" id="result-driver-rg">-</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">Data de Nascimento do Condutor</div>
                                        <div class="result-value" id="result-driver-birth">-</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">Sexo do Condutor</div>
                                        <div class="result-value" id="result-driver-gender">-</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">Estado Civil do Condutor</div>
                                        <div class="result-value" id="result-driver-marital">-</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">Profissão do Condutor</div>
                                        <div class="result-value" id="result-driver-profession">-</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">Renda do Condutor</div>
                                        <div class="result-value" id="result-driver-income">R$ 0,00</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">Endereço do Condutor</div>
                                        <div class="result-value" id="result-driver-address">-</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">CEP do Condutor</div>
                                        <div class="result-value" id="result-driver-zip">-</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">Cidade do Condutor</div>
                                        <div class="result-value" id="result-driver-city">-</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">Estado do Condutor</div>
                                        <div class="result-value" id="result-driver-state">-</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">Telefone do Condutor</div>
                                        <div class="result-value" id="result-driver-phone">-</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">Celular do Condutor</div>
                                        <div class="result-value" id="result-driver-mobile">-</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">Email do Condutor</div>
                                        <div class="result-value" id="result-driver-email">-</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">Nome do Veículo</div>
                                        <div class="result-value" id="result-vehicle-name">-</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">Marca do Veículo</div>
                                        <div class="result-value" id="result-vehicle-brand">-</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">Modelo do Veículo</div>
                                        <div class="result-value" id="result-vehicle-model">-</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">Ano do Veículo</div>
                                        <div class="result-value" id="result-vehicle-year">-</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">Placa do Veículo</div>
                                        <div class="result-value" id="result-vehicle-plate">-</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">Chassi do Veículo</div>
                                        <div class="result-value" id="result-vehicle-chassis">-</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">RENAVAM do Veículo</div>
                                        <div class="result-value" id="result-vehicle-renavam">-</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">Cor do Veículo</div>
                                        <div class="result-value" id="result-vehicle-color">-</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">Combustível do Veículo</div>
                                        <div class="result-value" id="result-vehicle-fuel">-</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">Categoria do Veículo</div>
                                        <div class="result-value" id="result-vehicle-category">-</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">Tipo do Veículo</div>
                                        <div class="result-value" id="result-vehicle-type">-</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">Uso do Veículo</div>
                                        <div class="result-value" id="result-vehicle-usage">-</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">Garagem do Veículo</div>
                                        <div class="result-value" id="result-vehicle-garage">-</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">Alarme do Veículo</div>
                                        <div class="result-value" id="result-vehicle-alarm">-</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">Rastreador do Veículo</div>
                                        <div class="result-value" id="result-vehicle-tracker">-</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">Blindagem do Veículo</div>
                                        <div class="result-value" id="result-vehicle-armor">-</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">Valor do Veículo</div>
                                        <div class="result-value" id="result-vehicle-value">R$ 0,00</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">Valor FIPE do Veículo</div>
                                        <div class="result-value" id="result-vehicle-fipe">R$ 0,00</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">KM do Veículo</div>
                                        <div class="result-value" id="result-vehicle-mileage">-</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">Data de Aquisição do Veículo</div>
                                        <div class="result-value" id="result-vehicle-acquisition">-</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">Proprietário do Veículo</div>
                                        <div class="result-value" id="result-vehicle-owner">-</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">Financiamento do Veículo</div>
                                        <div class="result-value" id="result-vehicle-financing">-</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">Banco do Financiamento</div>
                                        <div class="result-value" id="result-financing-bank">-</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">Valor do Financiamento</div>
                                        <div class="result-value" id="result-financing-value">R$ 0,00</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">Parcelas do Financiamento</div>
                                        <div class="result-value" id="result-financing-installments">0</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">Valor da Parcela do Financiamento</div>
                                        <div class="result-value" id="result-financing-installment-value">R$ 0,00</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">Data de Vencimento do Financiamento</div>
                                        <div class="result-value" id="result-financing-due-date">-</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">Saldo Devedor do Financiamento</div>
                                        <div class="result-value" id="result-financing-balance">R$ 0,00</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">Cobertura do Veículo</div>
                                        <div class="result-value" id="result-vehicle-coverage">-</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">Franquia do Veículo</div>
                                        <div class="result-value" id="result-vehicle-deductible">-</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">Valor da Franquia do Veículo</div>
                                        <div class="result-value" id="result-vehicle-deductible-value">R$ 0,00</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">Assistência do Veículo</div>
                                        <div class="result-value" id="result-vehicle-assistance">-</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">Proteção do Veículo</div>
                                        <div class="result-value" id="result-vehicle-protection">-</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">Bônus do Veículo</div>
                                        <div class="result-value" id="result-vehicle-bonus">-</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">Classe de Bônus do Veículo</div>
                                        <div class="result-value" id="result-vehicle-bonus-class">-</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">Sinistro do Veículo</div>
                                        <div class="result-value" id="result-vehicle-claim">-</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">Valor do Sinistro do Veículo</div>
                                        <div class="result-value" id="result-vehicle-claim-value">R$ 0,00</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">Data do Sinistro do Veículo</div>
                                        <div class="result-value" id="result-vehicle-claim-date">-</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">Status do Veículo</div>
                                        <div class="result-value" id="result-vehicle-status">-</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">Observações do Veículo</div>
                                        <div class="result-value" id="result-vehicle-notes">-</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">Data da Cotação do Veículo</div>
                                        <div class="result-value" id="result-vehicle-quote-date">-</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">Validade da Cotação do Veículo</div>
                                        <div class="result-value" id="result-vehicle-quote-validity">-</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">Número da Cotação do Veículo</div>
                                        <div class="result-value" id="result-vehicle-quote-number">-</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">Corretor do Veículo</div>
                                        <div class="result-value" id="result-vehicle-broker">-</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">Telefone do Corretor do Veículo</div>
                                        <div class="result-value" id="result-vehicle-broker-phone">-</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">Email do Corretor do Veículo</div>
                                        <div class="result-value" id="result-vehicle-broker-email">-</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">Endereço do Corretor do Veículo</div>
                                        <div class="result-value" id="result-vehicle-broker-address">-</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">CNPJ do Corretor do Veículo</div>
                                        <div class="result-value" id="result-vehicle-broker-cnpj">-</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">CRECI do Corretor do Veículo</div>
                                        <div class="result-value" id="result-vehicle-broker-creci">-</div>
                                    </div>
                                </div>
                            </div>
                            
                            <!-- Spinner com Timer Regressivo -->
                            <div class="spinner-timer-container" id="spinnerTimerContainer" style="display: none;">
                                <div class="spinner-container">
                                    <div class="sk-circle" id="skCircle">
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
                                    <div class="spinner-center" id="spinnerCenter">03:00</div>
                                </div>
                                <div class="timer-message" id="timerMessage" style="display: none;">
                                    ⏰ Está demorando mais que o normal. Aguardando mais 2 minutos...
                                </div>
                            </div>
                            
                            <div class="action-buttons">
                                <a href="#" class="action-button" id="closeModalBtn">
                                    <i class="fas fa-times"></i>
                                    Fechar
                                </a>
                            </div>
                        </div>
                    </div>
                </div>
            `;
            
            // Injetar modal no DOM
            document.body.insertAdjacentHTML('beforeend', modalHTML);
            
            // Mostrar spinner timer após 2 segundos
            setTimeout(() => {
                const spinnerContainer = document.getElementById('spinnerTimerContainer');
                if (spinnerContainer) {
                    spinnerContainer.style.display = 'flex';
                    console.log('✅ Spinner timer container exibido');
                } else {
                    console.warn('⚠️ Spinner container não encontrado');
                }
            }, 2000);
            
            // Configurar botão de fechar
            const closeBtn = document.getElementById('closeModalBtn');
            if (closeBtn) {
                closeBtn.addEventListener('click', (e) => {
                    e.preventDefault();
                    this.closeModal();
                });
            }
            
            // Configurar botão de fechar do header
            const closeHeaderBtn = document.querySelector('#rpaModal .close-button');
            if (closeHeaderBtn) {
                closeHeaderBtn.addEventListener('click', () => {
                    this.closeModal();
                });
            }
            
            console.log('✅ Modal criado e configurado');
        }
        
        showModal(sessionId) {
            this.currentSessionId = sessionId;
            
            if (!this.modal) {
                this.createModal();
            }
            
            const modal = document.getElementById('rpaModal');
            if (modal) {
                modal.classList.add('show');
                console.log('✅ Modal exibido');
            }
        }
        
        closeModal() {
            const modal = document.getElementById('rpaModal');
            if (modal) {
                modal.classList.remove('show');
                setTimeout(() => {
                    modal.remove();
                    this.modal = null;
                    console.log('✅ Modal fechado e removido');
                }, 300);
            }
        }
        
        updateSessionId(sessionId) {
            this.currentSessionId = sessionId;
            console.log('🔄 SessionId atualizado:', sessionId);
        }
    }
    
    // ========================================
    // 5. INICIALIZAÇÃO
    // ========================================
    
    // Expor classes globalmente
    window.SpinnerTimer = SpinnerTimer;
    window.ProgressModalRPA = ProgressModalRPA;
    window.MainPage = MainPage;
    
    // Injetar CSS
    const styleSheet = document.createElement('style');
    styleSheet.textContent = cssStyles;
    document.head.appendChild(styleSheet);
    
    // Inicializar página principal
    const mainPage = new MainPage();
    window.mainPage = mainPage;
    
    console.log('🚀 Webflow Injection Complete V6.12.0 carregado com sucesso!');
    console.log('📋 Classes disponíveis:', {
        SpinnerTimer: typeof SpinnerTimer,
        ProgressModalRPA: typeof ProgressModalRPA,
        MainPage: typeof MainPage
    });
    
})();


