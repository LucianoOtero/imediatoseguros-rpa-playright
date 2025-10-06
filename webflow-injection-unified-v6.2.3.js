/**
 * WEBFLOW INJECTION UNIFIED V6.3.0 - IMEDIATO SEGUROS
 * Código unificado para injeção no Webflow
 * 
 * Inclui:
 * - CSS completo (brand + main-page + modal-progress)
 * - JavaScript completo (main-page + modal-progress + rpa-integration)
 * - HTML do modal injetado
 * - Todas as funcionalidades consolidadas
 * - Correções críticas implementadas
 * - Sanitização de dados
 * - FontAwesome v7.1.0
 * - Tratamento robusto de erros
 */

(function() {
    'use strict';
    
    // ========================================
    // CSS COMPLETO INLINE
    // ========================================
    
    const cssStyles = `
        /* IDENTIDADE VISUAL IMEDIATO SEGUROS V6.3.0 */
        
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
        
        /* Reset e base */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Titillium Web', sans-serif;
        }
        
        /* MODAL PROGRESS CSS */
        #rpaModal {
            all: unset !important;
            isolation: isolate !important;
            position: fixed !important;
            top: 80px !important;
            left: 0 !important;
            width: 100vw !important;
            height: calc(100vh - 80px) !important;
            background: rgba(0, 0, 0, 0.9) !important;
            z-index: 999999 !important;
            display: flex !important;
            flex-direction: column !important;
            margin: 0 !important;
            padding: 0 !important;
            border: none !important;
            box-shadow: none !important;
            overflow: hidden !important;
            box-sizing: border-box !important;
        }
        
        #rpaModal * {
            box-sizing: border-box !important;
        }
        
        .progress-header {
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 1.2rem 2rem;
            background-color: #f2f5f8;
            background-image: url(https://cdn.prod.website-files.com/59eb807f9d16950001e202af/68ad0b4d507fa7c358ff42e2_header-grid-nodes-12-standard.svg);
            background-position: 0 0;
            background-size: auto;
            background-repeat: no-repeat;
            color: var(--imediato-dark-blue);
            text-align: center;
        }
        
        .progress-header .company-logo {
            max-width: 20rem;
            width: 20rem !important;
            height: 6rem !important;
            object-fit: contain !important;
            display: block !important;
            filter: none !important;
        }
        
        .progress-header h1 {
            color: var(--imediato-dark-blue);
            font-size: 2rem;
            margin: 1rem 0 0.5rem 0;
            font-weight: 600;
        }
        
        .progress-header h1 i {
            color: var(--imediato-dark-blue);
        }
        
        .progress-info {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 1rem;
            margin-bottom: 1rem;
        }
        
        .progress-text {
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--imediato-dark-blue);
        }
        
        .current-phase {
            font-size: 1rem;
            color: var(--imediato-dark-blue);
            font-weight: 500;
        }
        
        .sub-phase {
            font-size: 0.9rem;
            color: var(--imediato-text-light);
            font-style: italic;
            margin-top: 0.25rem;
        }
        
        .progress-stages {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 0.5rem;
        }
        
        .stage-info {
            font-size: 0.9rem;
            color: var(--imediato-text-light);
            background: rgba(0, 153, 204, 0.1);
            padding: 0.25rem 0.75rem;
            border-radius: 15px;
        }
        
        .progress-bar-wrapper {
            padding: 0 2rem 2rem;
        }
        
        .progress-bar {
            width: 100%;
            height: 8px;
            background: rgba(255, 255, 255, 0.2);
            border-radius: 4px;
            overflow: hidden;
            position: relative;
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, var(--imediato-light-blue), var(--imediato-dark-blue));
            border-radius: 4px;
            transition: width 0.5s ease;
            position: relative;
        }
        
        .progress-fill::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
            animation: progressShimmer 2s infinite;
        }
        
        @keyframes progressShimmer {
            0% { background-position: -200% 0; }
            100% { background-position: 200% 0; }
        }
        
        @keyframes progressShimmerFallback {
            0% { opacity: 0.3; }
            50% { opacity: 0.8; }
            100% { opacity: 0.3; }
        }
        
        /* Suporte para Safari e outros navegadores */
        @supports (background-position: -200%) {
            .progress-fill::after {
                background-size: 200% 100%;
                animation: progressShimmer 2s infinite;
            }
        }
        
        /* Fallback para navegadores sem suporte */
        @supports not (background-position: -200%) {
            .progress-fill::after {
                background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
                animation: progressShimmerFallback 2s infinite;
            }
        }
        
        .results-container {
            flex: 1;
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 2rem;
            padding: 2rem;
            overflow-y: auto;
        }
        
        .result-card {
            background: var(--imediato-white);
            border-radius: 20px;
            padding: 2rem;
            box-shadow: 0 8px 25px var(--imediato-shadow);
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
            transition: all 0.3s ease;
            border: 2px solid transparent;
        }
        
        .result-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 40px var(--imediato-shadow-hover);
        }
        
        .result-card.recommended {
            border-color: var(--imediato-light-blue);
        }
        
        .result-card.alternative {
            border-color: var(--imediato-border);
        }
        
        .card-header {
            display: flex;
            flex-direction: column;
            align-items: center;
            margin-bottom: 1.5rem;
            min-height: 60px;
            gap: 1rem;
        }
        
        .card-icon {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
            color: var(--imediato-dark-blue);
            background: var(--imediato-gray);
            flex-shrink: 0;
            min-width: 60px;
            min-height: 60px;
        }
        
        .result-card.recommended .card-icon {
            background: var(--imediato-gray);
            color: var(--imediato-dark-blue);
        }
        
        .result-card.alternative .card-icon {
            background: var(--imediato-gray);
            color: var(--imediato-dark-blue);
        }
        
        .card-title h3 {
            font-size: 1.2rem;
            font-weight: 600;
            color: var(--imediato-dark-blue);
            margin: 0;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            max-width: 100%;
        }
        
        .card-subtitle {
            font-size: 0.9rem;
            color: var(--imediato-text-light);
            margin-top: 0.25rem;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            max-width: 100%;
        }
        
        .card-value {
            margin-top: auto;
        }
        
        .value {
            font-size: 2rem;
            font-weight: 700;
            color: var(--imediato-dark-blue);
            margin: 0;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            max-width: 100%;
        }
        
        .results-header {
            text-align: center;
            padding: 2rem;
            background: linear-gradient(135deg, #28a745, #20c997);
            color: white;
            margin-bottom: 0;
        }
        
        .results-header h2 {
            font-size: 1.8rem;
            margin-bottom: 0.5rem;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0.5rem;
        }
        
        .contact-message {
            font-size: 1rem;
            margin-top: 1rem;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0.5rem;
            opacity: 0.9;
        }
        
        .modal-actions {
            display: flex;
            gap: 1rem;
            padding: 2rem;
            justify-content: center;
            background: var(--imediato-gray);
        }
        
        .btn-modal {
            padding: 1rem 2rem;
            border-radius: 10px;
            font-size: 1rem;
            font-weight: 600;
            font-family: 'Titillium Web', sans-serif;
            cursor: pointer;
            transition: all 0.3s ease;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            text-decoration: none;
            border: none;
        }
        
        .btn-modal.secondary {
            background: var(--imediato-white);
            color: var(--imediato-dark-blue);
            border: 2px solid var(--imediato-light-blue);
        }
        
        .btn-modal.primary {
            background: linear-gradient(135deg, var(--imediato-dark-blue), var(--imediato-light-blue));
            color: var(--imediato-white);
        }
        
        .btn-modal:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px var(--imediato-shadow-hover);
        }
        
        /* Responsividade */
        @media (max-width: 768px) {
            #rpaModal {
                top: 70px !important;
                height: calc(100vh - 70px) !important;
            }
            
            .progress-header {
                padding: 1rem;
            }
            
            .progress-header h1 {
                font-size: 1.5rem;
                margin: 0 0 0.5rem 0;
            }
            
            .progress-header .company-logo {
                max-width: 18rem;
                width: 18rem !important;
                height: 5rem !important;
                object-fit: contain !important;
                display: block !important;
                filter: none !important;
            }
            
            .progress-info {
                flex-direction: column;
                gap: 0.5rem;
            }
            
            .progress-text {
                font-size: 1.2rem;
            }
            
            .current-phase {
                font-size: 0.9rem;
            }
            
            .sub-phase {
                font-size: 0.85rem;
            }
            
            .modal-logo {
                max-width: 18rem;
                width: 18rem !important;
                height: 5rem !important;
                object-fit: contain !important;
                display: block !important;
                filter: none !important;
            }
            
            .progress-bar-wrapper {
                padding: 0 1rem 1rem;
            }
            
            .results-container {
                grid-template-columns: 1fr;
                gap: 1rem;
                padding: 1rem;
            }
            
            .result-card {
                padding: 1.5rem;
            }
            
            .card-icon {
                width: 50px;
                height: 50px;
                font-size: 1.2rem;
            }
            
            .card-title h3 {
                font-size: 1rem;
            }
            
            .value {
                font-size: 1.5rem;
            }
            
            .results-header h2 {
                font-size: 1.4rem;
            }
            
            .modal-actions {
                flex-direction: column;
                padding: 1rem;
            }
            
            .btn-modal {
                width: 100%;
                justify-content: center;
            }
        }
        
        @media (max-width: 480px) {
            .progress-header .company-logo {
                max-width: 16rem;
                width: 16rem !important;
                height: 4rem !important;
            }
            
            .modal-logo {
                max-width: 16rem;
                width: 16rem !important;
                height: 4rem !important;
            }
            
            .result-card {
                padding: 1rem;
            }
            
            .card-icon {
                width: 40px;
                height: 40px;
                font-size: 1rem;
            }
            
            .value {
                font-size: 1.3rem;
            }
        }
    `;
    
    // ========================================
    // FONTAWESOME V7.1.0 - CARREGAMENTO DINÂMICO
    // ========================================
    
    // Carregar FontAwesome v7.1.0 se não estiver presente
    if (!document.querySelector('link[href*="font-awesome"]')) {
        const fontAwesomeLink = document.createElement('link');
        fontAwesomeLink.rel = 'stylesheet';
        fontAwesomeLink.href = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/7.1.0/css/all.min.css';
        fontAwesomeLink.crossOrigin = 'anonymous';
        document.head.appendChild(fontAwesomeLink);
        console.log('✅ FontAwesome v7.1.0 carregado');
    } else {
        console.log('✅ FontAwesome já está carregado');
    }
    
    // ========================================
    // JAVASCRIPT COMPLETO
    // ========================================
    
    class MainPage {
        constructor() {
            this.sessionId = null;
            this.modalProgress = null;
            this.fixedData = {
                telefone: "11999999999",
                email: "cliente@exemplo.com",
                profissao: "Empresário",
                renda_mensal: "10000",
                modelo: "Civic",
                ano: "2020",
                cor: "Prata",
                combustivel: "Flex",
                zero_km: "false",
                uso: "Particular",
                garagem: "true",
                tipo_seguro: "Comprehensive",
                franquia: "500",
                cobertura_terceiros: "true",
                cobertura_vidros: "true",
                cobertura_carro_reserva: "true",
                cobertura_assistencia: "true"
            };
            
            this.apiUrls = [
                'https://rpaimediatoseguros.com.br/api/rpa',
                'http://rpaimediatoseguros.com.br/api/rpa',
                '/api/rpa'
            ];
            
            console.log('🚀 Inicializando Página Principal V6.2.3...');
            this.init();
        }
        
        init() {
            this.setupEventListeners();
            console.log('✅ Página Principal inicializada');
            console.log('📋 Modal simplificado - apenas resultados finais');
            console.log('🚫 Validações removidas - formulário livre');
            console.log('🔧 URLs de API configuradas:', this.apiUrls);
        }
        
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
        
        async handleFormSubmit(event) {
            event.preventDefault();
            console.log('📝 Formulário submetido');
            
            const btn = document.getElementById('submit_button_auto');
            const originalText = btn ? btn.textContent : 'CALCULE AGORA!';
            const originalDisabled = btn ? btn.disabled : false;
            
            // Atualizar estado do botão
            if (btn) {
                btn.textContent = 'Aguarde...';
                btn.disabled = true;
            }
            
            try {
                const form = event.target;
                const formData = this.collectFormData(form);
                
                console.log('📊 Dados do formulário:', formData);
                
                // Mesclar com dados fixos
                const completeData = { ...this.fixedData, ...formData };
                
                console.log('🔗 Dados completos:', completeData);
                
                // Abrir modal de progresso
                this.openProgressModal();
                
                // Iniciar RPA
                await this.startRPA(completeData);
                
            } catch (error) {
                console.error('❌ Erro no envio:', error);
                this.showError('Erro ao processar formulário. Tente novamente.');
                
            } finally {
                // Restaurar estado original do botão
                if (btn) {
                    btn.textContent = originalText;
                    btn.disabled = originalDisabled;
                }
            }
        }
        
        collectFormData(form) {
            const formData = new FormData(form);
            const data = {};
            
            // Coletar dados do formulário
            for (let [key, value] of formData.entries()) {
                data[key] = value;
            }
            
            // Aplicar conversões específicas
            this.applyFieldConversions(data);
            
            return data;
        }
        
        applyFieldConversions(data) {
            // Converter estado civil
            if (data['ESTADO-CIVIL']) {
                data.estado_civil = this.convertEstadoCivil(data['ESTADO-CIVIL']);
                console.log(`🔄 Estado civil convertido: "${data['ESTADO-CIVIL']}" → "${data.estado_civil}"`);
            }
            
            // Converter sexo
            if (data.SEXO) {
                data.sexo = this.convertSexo(data.SEXO);
                console.log(`🔄 Sexo convertido: "${data.SEXO}" → "${data.sexo}"`);
            }
            
            // Concatenar DDD + CELULAR com sanitização (PRIORIZAR FORMULÁRIO)
            if (data['DDD-CELULAR'] && data.CELULAR) {
                data.telefone = (data['DDD-CELULAR'] + data.CELULAR).replace(/\D/g, '');
                console.log(`🔄 Telefone concatenado e sanitizado: "${data['DDD-CELULAR']}" + "${data.CELULAR}" = "${data.telefone}"`);
            }
            
            // Mapear campos do Webflow para nomes do RPA (INCLUINDO ANO E EMAIL)
            const fieldMapping = {
                'CPF': 'cpf',
                'PLACA': 'placa',
                'MARCA': 'marca',
                'CEP': 'cep',
                'DATA-DE-NASCIMENTO': 'data_nascimento',
                'TIPO-DE-VEICULO': 'tipo_veiculo',
                'ANO': 'ano_veiculo',
                'EMAIL': 'email'
            };
            
            // Aplicar mapeamento de campos com sanitização
            Object.keys(fieldMapping).forEach(webflowField => {
                if (data[webflowField]) {
                    data[fieldMapping[webflowField]] = data[webflowField];
                }
            });
            
            // Sanitização específica de campos críticos
            if (data.cpf) {
                data.cpf = data.cpf.replace(/\D/g, '');
                console.log(`🔄 CPF sanitizado: "${data.cpf}"`);
            }
            
            if (data.cep) {
                data.cep = data.cep.replace(/\D/g, '');
                console.log(`🔄 CEP sanitizado: "${data.cep}"`);
            }
        }
        
        convertEstadoCivil(webflowValue) {
            if (!webflowValue) return '';
            
            const normalized = webflowValue.toLowerCase().trim();
            
            const mapping = {
                'solteiro': 'Solteiro',
                'casado': 'Casado ou Uniao Estavel',
                'casado ou uniao estavel': 'Casado ou Uniao Estavel',
                'married': 'Casado ou Uniao Estavel',
                'divorciado': 'Divorciado',
                'separado': 'Separado',
                'viuvo': 'Viuvo',
                'widowed': 'Viuvo'
            };
            
            return mapping[normalized] || webflowValue.charAt(0).toUpperCase() + webflowValue.slice(1);
        }
        
        convertSexo(webflowValue) {
            if (!webflowValue) return '';
            
            const normalized = webflowValue.toLowerCase().trim();
            
            const mapping = {
                'm': 'Masculino',
                'masculino': 'Masculino',
                'male': 'Masculino',
                'f': 'Feminino',
                'feminino': 'Feminino',
                'feminina': 'Feminino',
                'female': 'Feminino'
            };
            
            return mapping[normalized] || webflowValue.charAt(0).toUpperCase() + webflowValue.slice(1);
        }
        
        openProgressModal() {
            console.log('🎭 Abrindo modal de progresso...');
            
            // Remover modal existente se houver
            const existingModal = document.getElementById('rpaModal');
            if (existingModal) {
                existingModal.remove();
            }
            
            // Criar e injetar modal HTML
            const modalHTML = `
                <div id="rpaModal" style="all: unset !important; isolation: isolate !important; position: fixed !important; top: 80px !important; left: 0 !important; width: 100vw !important; height: calc(100vh - 80px) !important; background: rgba(0, 0, 0, 0.9) !important; z-index: 999999 !important; display: flex !important; flex-direction: column !important; margin: 0 !important; padding: 0 !important; border: none !important; box-shadow: none !important; overflow: hidden !important; box-sizing: border-box !important;">
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
                            <div class="progress-fill" id="progressFill" style="width: 0%"></div>
                        </div>
                    </div>
                    
                    <div class="results-container" id="resultsContainer" style="display: none;">
                        <!-- 2 Divs de Resultados -->
                        <div class="result-card recommended">
                            <div class="card-header">
                                <div class="card-icon">
                                    <i class="fas fa-star"></i>
                                </div>
                                <div class="card-title">
                                    <h3>Recomendado</h3>
                                    <div class="card-subtitle">Melhor Custo-Benefício</div>
                                </div>
                            </div>
                            <div class="card-value">
                                <div class="value" id="recommendedValue">-</div>
                            </div>
                        </div>
                        
                        <div class="result-card alternative">
                            <div class="card-header">
                                <div class="card-icon">
                                    <i class="fas fa-exchange-alt"></i>
                                </div>
                                <div class="card-title">
                                    <h3>Alternativo</h3>
                                    <div class="card-subtitle">Opção Adicional</div>
                                </div>
                            </div>
                            <div class="card-value">
                                <div class="value" id="alternativeValue">-</div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="modal-actions" id="modalActions" style="display: none;">
                        <button class="btn-modal secondary" onclick="location.reload()">
                            <i class="fas fa-redo"></i> Nova Cotação
                        </button>
                        <button class="btn-modal primary" onclick="window.open('tel:+5511999999999', '_self')">
                            <i class="fas fa-phone"></i> Falar com Corretor
                        </button>
                    </div>
                </div>
            `;
            
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
                    const logoElement = modal.querySelector('.company-logo');
                    console.log('🔍 DEBUG Logo encontrado:', !!logoElement);
                    if (logoElement) {
                        console.log('🔍 DEBUG Logo src:', logoElement.src);
                        console.log('🔍 DEBUG Logo dimensions:', {
                            width: logoElement.offsetWidth,
                            height: logoElement.offsetHeight,
                            display: window.getComputedStyle(logoElement).display
                        });
                    } else {
                        console.warn('⚠️ Logo não encontrado - verificando elementos disponíveis:');
                        const allImages = modal.querySelectorAll('img');
                        allImages.forEach((img, index) => {
                            console.log(`Imagem ${index}:`, img.className, img.src);
                        });
                    }
                }
            }, 100);
            
            console.log('🎭 Modal de progresso aberto');
        }
        
        async startRPA(completeData) {
            console.log('🚀 Iniciando RPA...');
            
            let lastWorkingUrl = null;
            
            for (let i = 0; i < this.apiUrls.length; i++) {
                const url = this.apiUrls[i];
                console.log(`🔍 Tentativa ${i + 1}/3: ${url}/start`);
                
                try {
                    const response = await fetch(`${url}/start`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            session: this.generateSessionId(),
                            dados: completeData
                        })
                    });
                    
                    if (response.ok) {
                        const result = await response.json();
                        console.log(`📡 Resposta recebida de ${url}/start:`, response.status);
                        console.log('✅ RPA iniciado com sucesso. Session ID:', result.session_id);
                        console.log('✅ URL funcionando:', url);
                        
                        this.sessionId = result.session_id;
                        lastWorkingUrl = url;
                        break;
                    } else {
                        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                    }
                    
                } catch (error) {
                    console.log(`❌ Erro na tentativa ${i + 1}:`, error.message);
                    
                    if (i === this.apiUrls.length - 1) {
                        console.error('❌ Todas as URLs falharam');
                        this.showError('Erro de conectividade. Tente novamente.');
                        return;
                    }
                }
            }
            
            if (this.sessionId) {
                console.log('🔄 Inicializando modal de progresso...');
                this.modalProgress = new ProgressModalRPA(this.sessionId, lastWorkingUrl);
                console.log('✅ Modal de progresso inicializado');
            } else {
                console.error('❌ Session ID não disponível para polling');
                this.showError('Erro de sessão. Tente novamente.');
                return;
            }
        }
        
        generateSessionId() {
            return 'rpa_v4_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
        }
        
        showError(message) {
            console.error('❌ Erro:', message);
            
            // Remover modal existente se houver
            const existingModal = document.getElementById('rpaModal');
            if (existingModal) {
                existingModal.remove();
            }
            
            // Mostrar erro no modal
            const errorModal = document.createElement('div');
            errorModal.id = 'errorModal';
            errorModal.style.cssText = `
                position: fixed;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                background: white;
                padding: 2rem;
                border-radius: 10px;
                box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
                z-index: 999999;
                text-align: center;
                max-width: 400px;
            `;
            
            errorModal.innerHTML = `
                <div style="color: #e74c3c; font-size: 2rem; margin-bottom: 1rem;">
                    <i class="fas fa-exclamation-triangle"></i>
                </div>
                <h3 style="color: #333; margin-bottom: 1rem;">Erro</h3>
                <p style="color: #666; margin-bottom: 1.5rem;">${message}</p>
                <button onclick="this.parentElement.remove(); location.reload();" 
                        style="background: #0099CC; color: white; border: none; padding: 0.75rem 1.5rem; border-radius: 5px; cursor: pointer;">
                    Tentar Novamente
                </button>
            `;
            
            document.body.appendChild(errorModal);
        }
    }
    
    class ProgressModalRPA {
        constructor(sessionId, baseUrl) {
            this.sessionId = sessionId;
            this.baseUrl = baseUrl;
            this.isPolling = false;
            this.pollingInterval = null;
            this.phaseMessages = {
                0: "🔄 Iniciando Multi-Cálculo...",
                1: "🔄 Iniciando sistema...",
                2: "🔐 Fazendo login no sistema",
                3: "🚗 Selecionando veículo",
                4: "📋 Validando dados do veículo",
                5: "🚗 Validando informações do veículo",
                6: "⚙️ Configurando coberturas",
                7: "👤 Inserindo dados pessoais",
                8: "🏠 Inserindo dados de endereço",
                9: "🚗 Inserindo dados do veículo",
                10: "👤 Selecionando condutor principal",
                11: "🏢 Inserindo atividade do veículo",
                12: "🏠 Inserindo dados de garagem",
                13: "👨‍👩‍👧‍👦 Inserindo dados de residentes",
                14: "📊 Processando cotação",
                15: "⚙️ Finalizando processamento...",
                16: "Cálculo finalizado"
            };
            
            this.phaseSubMessages = {
                0: "🚀 Preparando ambiente de cálculo",
                1: "📋 Preparando dados para cotação",
                2: "👤 Processando autenticação",
                3: "🔍 Localizando veículo no sistema",
                4: "✅ Verificando informações",
                5: "📋 Inserindo dados do veículo",
                6: "⚙️ Configurando proteções",
                7: "📝 Coletando dados pessoais",
                8: "📍 Validando endereço",
                9: "🚗 Confirmando dados do veículo",
                10: "👤 Definindo condutor",
                11: "🏢 Configurando uso",
                12: "🏠 Definindo segurança",
                13: "👨‍👩‍👧‍👦 Analisando residentes",
                14: "📊 Calculando prêmios",
                15: "",
                16: ""
            };
            
            this.phasePercentages = {
                0: 0, 1: 6, 2: 13, 3: 20, 4: 26, 5: 33, 6: 40, 7: 46, 8: 53,
                9: 60, 10: 66, 11: 73, 12: 80, 13: 86, 14: 93, 15: 97, 16: 100
            };
            
            console.log('🎭 Inicializando Modal de Progresso...');
            this.init();
        }
        
        init() {
            this.setupElements();
            this.setupEventListeners();
            this.setupAnimations();
            this.startProgressPolling();
            console.log('✅ Modal de Progresso inicializado');
        }
        
        setupElements() {
            console.log('🔍 DEBUG Configurando elementos do modal...');
            
            this.progressTextElement = document.getElementById('progressText');
            this.currentPhaseElement = document.getElementById('currentPhase');
            this.subPhaseElement = document.getElementById('subPhase');
            this.stageInfoElement = document.getElementById('stageInfo');
            this.progressFillElement = document.getElementById('progressFill');
            this.resultsContainerElement = document.getElementById('resultsContainer');
            this.modalActionsElement = document.getElementById('modalActions');
            
            console.log('🔍 DEBUG Elementos encontrados:');
            console.log('🔍 DEBUG progressText:', !!this.progressTextElement);
            console.log('🔍 DEBUG currentPhase:', !!this.currentPhaseElement);
            console.log('🔍 DEBUG subPhase:', !!this.subPhaseElement);
            console.log('🔍 DEBUG stageInfo:', !!this.stageInfoElement);
            console.log('🔍 DEBUG progressFill:', !!this.progressFillElement);
            console.log('🔍 DEBUG resultsContainer:', !!this.resultsContainerElement);
            console.log('🔍 DEBUG modalActions:', !!this.modalActionsElement);
            
            // Verificar se todos os elementos críticos foram encontrados
            const criticalElements = [
                'progressText', 'currentPhase', 'stageInfo', 'progressFill'
            ];
            
            const missingElements = criticalElements.filter(id => !document.getElementById(id));
            if (missingElements.length > 0) {
                console.error('❌ Elementos críticos não encontrados:', missingElements);
                console.log('🔍 DEBUG HTML do modal:', document.getElementById('rpaModal')?.innerHTML);
            } else {
                console.log('✅ Todos os elementos críticos encontrados');
            }
        }
        
        setupEventListeners() {
            // Event listeners específicos do modal
            console.log('📝 Event listeners do modal configurados');
        }
        
        setupAnimations() {
            // Configurar animações
            console.log('✨ Animações configuradas');
        }
        
        startProgressPolling() {
            if (this.isPolling) return;
            
            this.isPolling = true;
            console.log('🔄 Iniciando polling do progresso...');
            
            this.pollingInterval = setInterval(() => {
                this.checkProgress();
            }, 2000);
        }
        
        async checkProgress() {
            let retries = 3;
            while (retries > 0) {
                try {
                    // CORREÇÃO: Remover duplicação do path da API
                    const response = await fetch(`${this.baseUrl}/progress/${this.sessionId}`);
                    
                    if (!response.ok) {
                        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                    }
                    
                    const progressData = await response.json();
                    console.log('📊 Progresso recebido:', progressData);
                    
                    this.updateProgress(progressData);
                    return;
                    
                } catch (error) {
                    console.error(`❌ Erro ao verificar progresso (tentativa ${4-retries}):`, error);
                    retries--;
                    
                    if (retries === 0) {
                        this.showError('Erro de conectividade. Tente novamente.');
                        return;
                    }
                    
                    // Exponential backoff
                    await new Promise(resolve => setTimeout(resolve, 1000 * (4-retries)));
                }
            }
        }
        
        updateProgress(progressData) {
            console.log('🔍 DEBUG ProgressData completo:', progressData);
            
            const progress = progressData.progress || {};
            console.log('🔍 DEBUG Progress object:', progress);
            
            const currentPhase = progress.etapa_atual || 0;
            const currentStatus = progress.status || 'executando';
            const currentMessage = progress.mensagem || '';
            
            console.log('🔍 DEBUG Fase atual:', currentPhase);
            console.log('🔍 DEBUG Status:', currentStatus);
            console.log('🔍 DEBUG Mensagem:', currentMessage);
            
            // Usar percentual fixo baseado na fase
            const percentual = this.phasePercentages[currentPhase] || 0;
            console.log('🔍 DEBUG Percentual calculado:', percentual);
            
            // Atualizar elementos da interface
            console.log('🔍 DEBUG Elementos da interface:');
            console.log('🔍 DEBUG progressTextElement:', !!this.progressTextElement);
            console.log('🔍 DEBUG currentPhaseElement:', !!this.currentPhaseElement);
            console.log('🔍 DEBUG subPhaseElement:', !!this.subPhaseElement);
            console.log('🔍 DEBUG stageInfoElement:', !!this.stageInfoElement);
            console.log('🔍 DEBUG progressFillElement:', !!this.progressFillElement);
            
            if (this.progressTextElement) {
                this.progressTextElement.textContent = `${percentual}%`;
                console.log('✅ Progresso atualizado:', `${percentual}%`);
            } else {
                console.warn('⚠️ progressTextElement não encontrado');
            }
            
            if (this.currentPhaseElement) {
                const phaseMessage = this.getPhaseMessage(currentPhase);
                this.currentPhaseElement.textContent = phaseMessage;
                console.log('✅ Fase atualizada:', phaseMessage);
            } else {
                console.warn('⚠️ currentPhaseElement não encontrado');
            }
            
            if (this.subPhaseElement) {
                const subMessage = this.getPhaseSubMessage(currentPhase);
                this.subPhaseElement.textContent = subMessage;
                console.log('✅ Subfase atualizada:', subMessage);
            } else {
                console.warn('⚠️ subPhaseElement não encontrado');
            }
            
            if (this.stageInfoElement) {
                this.stageInfoElement.textContent = `Fase ${currentPhase} de 15`;
                console.log('✅ Stage info atualizado:', `Fase ${currentPhase} de 15`);
            } else {
                console.warn('⚠️ stageInfoElement não encontrado');
            }
            
            if (this.progressFillElement) {
                this.progressFillElement.style.width = `${percentual}%`;
                console.log('✅ Barra de progresso atualizada:', `${percentual}%`);
            } else {
                console.warn('⚠️ progressFillElement não encontrado');
            }
            
            // Verificar se RPA foi concluído
            if (currentStatus === 'success' || currentStatus === 'completed') {
                this.handleRPACompletion(progress);
            }
        }
        
        getPhaseMessage(phaseNumber) {
            return this.phaseMessages[phaseNumber] || `Fase ${phaseNumber}`;
        }
        
        getPhaseSubMessage(phaseNumber) {
            return this.phaseSubMessages[phaseNumber] || '';
        }
        
        handleRPACompletion(progress) {
            console.log('🎉 RPA concluído com sucesso!');
            
            // Parar polling
            if (this.pollingInterval) {
                clearInterval(this.pollingInterval);
                this.isPolling = false;
            }
            
            // Atualizar para 100%
            if (this.progressTextElement) {
                this.progressTextElement.textContent = '100%';
            }
            
            if (this.currentPhaseElement) {
                this.currentPhaseElement.textContent = '🎉 Cálculo Concluído';
            }
            
            if (this.subPhaseElement) {
                this.subPhaseElement.textContent = 'Seu seguro foi calculado com sucesso!';
            }
            
            if (this.stageInfoElement) {
                this.stageInfoElement.textContent = 'Fase 16 de 16';
            }
            
            if (this.progressFillElement) {
                this.progressFillElement.style.width = '100%';
            }
            
            // Mostrar resultados
            this.showResults(progress);
        }
        
        showResults(progress) {
            console.log('📊 Exibindo resultados...');
            
            // Mostrar container de resultados
            if (this.resultsContainerElement) {
                this.resultsContainerElement.style.display = 'grid';
            }
            
            // Atualizar valores
            this.updateResults(progress);
            
            // Mostrar ações do modal
            if (this.modalActionsElement) {
                this.modalActionsElement.style.display = 'flex';
            }
            
            // Adicionar mensagem de contato
            this.addContactMessage();
        }
        
        updateResults(progress) {
            const resultadosFinais = progress?.resultados_finais?.dados?.dados_finais;
            
            if (resultadosFinais) {
                // Cálculo recomendado
                if (resultadosFinais.plano_recomendado?.valor) {
                    const recommendedElement = document.getElementById('recommendedValue');
                    if (recommendedElement) {
                        recommendedElement.textContent = this.formatCurrency(resultadosFinais.plano_recomendado.valor);
                    }
                }
                
                // Cálculo alternativo
                if (resultadosFinais.plano_alternativo?.valor) {
                    const alternativeElement = document.getElementById('alternativeValue');
                    if (alternativeElement) {
                        alternativeElement.textContent = this.formatCurrency(resultadosFinais.plano_alternativo.valor);
                    }
                }
            }
        }
        
        formatCurrency(value) {
            if (!value) return '-';
            
            // Se já está formatado (contém R$), retornar como está
            if (typeof value === 'string' && value.includes('R$')) {
                return value;
            }
            
            const numValue = parseFloat(value);
            if (isNaN(numValue)) return '-';
            
            // Detectar valores que parecem divididos por 1000
            if (numValue >= 0.1 && numValue <= 100) {
                const correctedValue = numValue * 1000;
                console.log(`🔧 Valor corrigido: ${numValue} → ${correctedValue}`);
                return correctedValue.toLocaleString('pt-BR', {
                    style: 'currency',
                    currency: 'BRL'
                });
            }
            
            return numValue.toLocaleString('pt-BR', {
                style: 'currency',
                currency: 'BRL'
            });
        }
        
        addContactMessage() {
            // CORREÇÃO: Append no container pai, não no grid
            const resultsContainer = document.querySelector('.results-container');
            if (resultsContainer && !resultsContainer.parentNode.querySelector('.contact-message')) {
                const contactMessage = document.createElement('div');
                contactMessage.className = 'contact-message';
                contactMessage.style.cssText = `
                    text-align: center;
                    padding: 1rem 2rem;
                    background: linear-gradient(135deg, #28a745, #20c997);
                    color: white;
                    font-size: 1rem;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    gap: 0.5rem;
                `;
                contactMessage.innerHTML = '<i class="fas fa-phone"></i> Um especialista da Imediato Seguros entrará em contato em instantes para passar os detalhes!';
                
                // Append no container pai, antes do results-container
                resultsContainer.parentNode.insertBefore(contactMessage, resultsContainer);
                console.log('✅ Mensagem de contato adicionada');
            }
        }
    }
    
    // ========================================
    // INICIALIZAÇÃO
    // ========================================
    
    // Aguardar DOM estar pronto
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            new MainPage();
        });
    } else {
        new MainPage();
    }
    
})();
