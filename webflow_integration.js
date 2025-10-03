/**
 * WEBFLOW INTEGRATION - JAVASCRIPT PARA INJEÇÃO NO WEBFLOW
 * 
 * Este arquivo contém o código JavaScript completo para integração
 * do formulário Webflow com o RPA V4
 * 
 * INSTRUÇÕES PARA IMPLEMENTAÇÃO NO WEBFLOW:
 * 1. Copie todo o conteúdo deste arquivo
 * 2. Cole no Custom Code > Footer Code do Webflow
 * 3. Configure os IDs dos campos conforme seu formulário
 * 4. Teste a funcionalidade
 * 
 * CAMPOS DO FORMULÁRIO WEBFLOW (substitua pelos IDs reais):
 * - CPF: id="cpf" ou name="cpf"
 * - Nome: id="nome" ou name="nome"  
 * - Placa: id="placa" ou name="placa"
 * - CEP: id="cep" ou name="cep"
 * - Email: id="email" ou name="email"
 * - Telefone: id="telefone" ou name="telefone"
 * 
 * BOTÃO DO WEBFLOW (substitua pelo ID/class real):
 * - Botão: id="botao-cotacao" ou class="botao-cotacao"
 * 
 * Versão: 1.0
 * Data: 01/10/2025
 * Compatível com: segurosimediato.com.br
 */

class WebflowRPAClient {
    constructor() {
        this.apiBaseUrl = 'https://rpaimediatoseguros.com.br/api/rpa';
        this.modal = null;
        this.sessionId = null;
        this.progressInterval = null;
        this.isProcessing = false;
        
        // Configurações
        this.config = {
            pollInterval: 2000, // 2 segundos
            maxPollTime: 300000, // 5 minutos
            colors: {
                primary: '#2c3e50',
                secondary: '#3498db',
                success: '#27ae60',
                warning: '#f39c12',
                danger: '#e74c3c'
            }
        };
        
        // Fases do RPA (15 telas)
        this.phases = [
            { text: 'Iniciando processamento...', icon: 'fas fa-play-circle', progress: 0 },
            { text: 'Selecionando tipo de seguro...', icon: 'fas fa-car', progress: 6.7 },
            { text: 'Inserindo dados da placa...', icon: 'fas fa-key', progress: 13.3 },
            { text: 'Validando dados do veículo...', icon: 'fas fa-car-side', progress: 20 },
            { text: 'Processando dados do proprietário...', icon: 'fas fa-user', progress: 26.7 },
            { text: 'Calculando estimativas iniciais...', icon: 'fas fa-calculator', progress: 33.3 },
            { text: 'Selecionando coberturas...', icon: 'fas fa-shield-alt', progress: 40 },
            { text: 'Processando dados do condutor...', icon: 'fas fa-id-card', progress: 46.7 },
            { text: 'Validando informações pessoais...', icon: 'fas fa-user-check', progress: 53.3 },
            { text: 'Verificando dados do veículo...', icon: 'fas fa-car-crash', progress: 60 },
            { text: 'Finalizando dados do veículo...', icon: 'fas fa-tools', progress: 66.7 },
            { text: 'Confirmando informações...', icon: 'fas fa-check-double', progress: 73.3 },
            { text: 'Selecionando plano ideal...', icon: 'fas fa-star', progress: 80 },
            { text: 'Processando dados de pagamento...', icon: 'fas fa-credit-card', progress: 86.7 },
            { text: 'Capturando dados finais...', icon: 'fas fa-coins', progress: 93.3 },
            { text: 'Concluído com sucesso!', icon: 'fas fa-check-circle', progress: 100 }
        ];
    }

    /**
     * Inicializar o cliente RPA
     */
    async init() {
        try {
            console.log('🚀 Inicializando Webflow RPA Client...');
            
            // Aguardar dependências
            await this.loadDependencies();
            
            // Configurar event listeners
            this.setupEventListeners();
            
            // Aguardar DOM estar pronto
            if (document.readyState === 'loading') {
                document.addEventListener('DOMContentLoaded', () => {
                    this.setupFormIntegration();
                    this.setupRealTimeValidation();
                });
            } else {
                this.setupFormIntegration();
                this.setupRealTimeValidation();
            }
            
            console.log('✅ Webflow RPA Client inicializado com sucesso');
            
        } catch (error) {
            console.error('❌ Erro ao inicializar Webflow RPA Client:', error);
        }
    }
    
    /**
     * Carregar dependências necessárias
     */
    async loadDependencies() {
        const dependencies = [
            {
                name: 'SweetAlert2',
                check: () => window.Swal,
                load: () => this.loadScript('https://cdn.jsdelivr.net/npm/sweetalert2@11/dist/sweetalert2.min.js')
            },
            {
                name: 'SweetAlert2 CSS',
                check: () => document.querySelector('link[href*="sweetalert2"]'),
                load: () => this.loadStylesheet('https://cdn.jsdelivr.net/npm/sweetalert2@11/dist/sweetalert2.min.css')
            },
            {
                name: 'Font Awesome',
                check: () => document.querySelector('link[href*="font-awesome"]'),
                load: () => this.loadStylesheet('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css')
            },
            {
                name: 'Titillium Web Font',
                check: () => document.querySelector('link[href*="titillium"]'),
                load: () => this.loadStylesheet('https://fonts.googleapis.com/css2?family=Titillium+Web:wght@300;400;600;700&display=swap')
            }
        ];
        
        // Carregar dependências em paralelo para melhor performance
        const loadPromises = dependencies.map(async (dep) => {
            if (!dep.check()) {
                console.log(`📦 Carregando ${dep.name}...`);
                await dep.load();
                console.log(`✅ ${dep.name} carregado`);
            } else {
                console.log(`✅ ${dep.name} já carregado`);
            }
        });
        
        await Promise.all(loadPromises);
    }
    
    /**
     * Carregar script dinamicamente com cache
     */
    loadScript(src) {
        return new Promise((resolve, reject) => {
            // Verificar se já existe
            const existingScript = document.querySelector(`script[src="${src}"]`);
            if (existingScript) {
                resolve();
                return;
            }
            
            const script = document.createElement('script');
            script.src = src;
            script.async = true; // Carregar assíncrono para melhor performance
            script.onload = resolve;
            script.onerror = reject;
            document.head.appendChild(script);
        });
    }
    
    /**
     * Carregar stylesheet dinamicamente com cache
     */
    loadStylesheet(href) {
        return new Promise((resolve) => {
            // Verificar se já existe
            const existingLink = document.querySelector(`link[href="${href}"]`);
            if (existingLink) {
                resolve();
                return;
            }
            
            const link = document.createElement('link');
            link.rel = 'stylesheet';
            link.href = href;
            link.onload = resolve;
            document.head.appendChild(link);
        });
    }
    
    /**
     * Configurar event listeners globais
     */
    setupEventListeners() {
        // Event listener para conclusão do RPA
        document.addEventListener('rpaConcluido', (event) => {
            console.log('🎉 RPA concluído:', event.detail);
            this.handleRPASuccess(event.detail);
        });
        
        // Event listener para erros do RPA
        document.addEventListener('rpaErro', (event) => {
            console.error('❌ Erro no RPA:', event.detail);
            this.handleRPAError(event.detail);
        });
    }
    
    /**
     * Configurar integração com formulário
     * 
     * WEBFLOW INTEGRATION NOTES:
     * Este método tenta encontrar automaticamente o formulário e botão.
     * Se não encontrar, você pode configurar manualmente os seletores.
     */
    setupFormIntegration() {
        // Tentar encontrar formulário por diferentes seletores
        const formSelectors = [
            '#formulario-cotacao',           // ID específico
            '.formulario-cotacao',           // Classe específica
            'form[data-name="Formulário de Cotação"]', // Webflow data-name
            'form[data-name="Cotação"]',     // Webflow data-name alternativo
            'form'                           // Qualquer formulário
        ];
        
        let form = null;
        for (const selector of formSelectors) {
            form = document.querySelector(selector);
            if (form) {
                console.log(`📝 Formulário encontrado: ${selector}`);
                break;
            }
        }
        
        if (!form) {
            console.warn('⚠️ Formulário não encontrado. Aguardando...');
            // Tentar novamente após 1 segundo
            setTimeout(() => this.setupFormIntegration(), 1000);
            return;
        }
        
        // Configurar event listener do formulário
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleFormSubmit();
        });
        
        // Tentar encontrar botão por diferentes seletores
        const buttonSelectors = [
            '#botao-cotacao',                // ID específico
            '.botao-cotacao',                // Classe específica
            'button[type="submit"]',         // Botão submit
            'input[type="submit"]',          // Input submit
            'button:contains("Solicitar")',  // Texto "Solicitar"
            'button:contains("Cotação")',    // Texto "Cotação"
            'button:contains("Calcular")'    // Texto "Calcular"
        ];
        
        let button = null;
        for (const selector of buttonSelectors) {
            button = document.querySelector(selector);
            if (button) {
                console.log(`🔘 Botão encontrado: ${selector}`);
                break;
            }
        }
        
        if (button) {
            button.addEventListener('click', (e) => {
                e.preventDefault();
                this.handleFormSubmit();
            });
        }
        
        console.log('✅ Integração com formulário configurada');
    }

    /**
     * Configurar validação em tempo real
     */
    setupRealTimeValidation() {
        console.log('🔍 Configurando validação em tempo real...');
        
        // Aguardar um pouco para garantir que os campos existam
        setTimeout(() => {
            this.setupFieldValidation();
        }, 500);
        
        console.log('✅ Validação em tempo real configurada');
    }

    /**
     * Configurar validação de campos
     */
    setupFieldValidation() {
        const fields = this.getFormFields();
        
        fields.forEach(field => {
            if (field) {
                // Validação em tempo real para CPF
                if (field.name === 'cpf' || field.id === 'cpf' || field.classList.contains('cpf')) {
                    field.addEventListener('input', (e) => {
                        this.validateCPFRealTime(e.target);
                    });
                    field.addEventListener('blur', (e) => {
                        this.validateCPFRealTime(e.target);
                    });
                }
                
                // Validação em tempo real para placa
                if (field.name === 'placa' || field.id === 'placa' || field.classList.contains('placa')) {
                    field.addEventListener('input', (e) => {
                        this.validatePlacaRealTime(e.target);
                    });
                    field.addEventListener('blur', (e) => {
                        this.validatePlacaRealTime(e.target);
                    });
                }
                
                // Validação em tempo real para CEP
                if (field.name === 'cep' || field.id === 'cep' || field.classList.contains('cep')) {
                    field.addEventListener('input', (e) => {
                        this.validateCEPRealTime(e.target);
                    });
                    field.addEventListener('blur', (e) => {
                        this.validateCEPRealTime(e.target);
                    });
                }
                
                // Validação em tempo real para email
                if (field.type === 'email' || field.name === 'email' || field.id === 'email') {
                    field.addEventListener('input', (e) => {
                        this.validateEmailRealTime(e.target);
                    });
                    field.addEventListener('blur', (e) => {
                        this.validateEmailRealTime(e.target);
                    });
                }
            }
        });
    }

    /**
     * Validar CPF em tempo real
     */
    validateCPFRealTime(field) {
        const value = field.value.replace(/[^\d]/g, '');
        const isValid = this.isValidCPF(value);
        
        this.updateFieldValidation(field, isValid, 'CPF inválido');
    }

    /**
     * Validar placa em tempo real
     */
    validatePlacaRealTime(field) {
        const value = field.value.toUpperCase();
        const isValid = this.isValidPlaca(value);
        
        this.updateFieldValidation(field, isValid, 'Placa inválida');
    }

    /**
     * Validar CEP em tempo real
     */
    validateCEPRealTime(field) {
        const value = field.value.replace(/[^\d]/g, '');
        const isValid = this.isValidCEP(value);
        
        this.updateFieldValidation(field, isValid, 'CEP inválido');
    }

    /**
     * Validar email em tempo real
     */
    validateEmailRealTime(field) {
        const value = field.value.trim();
        const isValid = value === '' || this.isValidEmail(value);
        
        this.updateFieldValidation(field, isValid, 'Email inválido');
    }

    /**
     * Atualizar validação visual do campo
     */
    updateFieldValidation(field, isValid, errorMessage) {
        // Remover classes anteriores
        field.classList.remove('valid', 'invalid');
        
        // Remover mensagem de erro anterior
        const existingError = field.parentNode.querySelector('.field-error');
        if (existingError) {
            existingError.remove();
        }
        
        if (field.value.trim() !== '') {
            if (isValid) {
                field.classList.add('valid');
            } else {
                field.classList.add('invalid');
                
                // Adicionar mensagem de erro
                const errorDiv = document.createElement('div');
                errorDiv.className = 'field-error';
                errorDiv.textContent = errorMessage;
                errorDiv.style.cssText = `
                    color: #e74c3c;
                    font-size: 12px;
                    margin-top: 4px;
                    display: block;
                `;
                
                field.parentNode.appendChild(errorDiv);
            }
        }
    }
    
    /**
     * Manipular envio do formulário
     */
    async handleFormSubmit() {
        if (this.isProcessing) {
            console.log('⏳ Processamento já em andamento...');
            return;
        }
        
        try {
            console.log('🚀 Iniciando processamento do formulário...');
            this.isProcessing = true;
            
            // Coletar dados do formulário
            const dados = this.collectFormData();
            console.log('📋 Dados coletados:', dados);
            
            // Validar dados
            this.validateFormData(dados);
            console.log('✅ Dados validados');
            
            // Desabilitar botão
            this.disableButton();
            
            // Iniciar RPA
            await this.startRPA(dados);
            
        } catch (error) {
            console.error('❌ Erro ao processar formulário:', error);
            this.showError('Erro', error.message);
            this.enableButton();
            this.isProcessing = false;
        }
    }

    /**
     * Coletar dados do formulário
     * 
     * WEBFLOW INTEGRATION NOTES:
     * Este método tenta coletar dados de diferentes formas.
     * Adapte conforme a estrutura do seu formulário Webflow.
     */
    collectFormData() {
        const form = document.querySelector('form') || document;
        
        // Mapear campos possíveis
        const fieldMappings = {
            cpf: ['cpf', 'CPF', 'documento', 'document'],
            nome: ['nome', 'Nome', 'name', 'fullname', 'nome_completo'],
            placa: ['placa', 'Placa', 'plate', 'placa_veiculo'],
            cep: ['cep', 'CEP', 'zipcode', 'postal_code'],
            email: ['email', 'Email', 'e-mail', 'mail'],
            telefone: ['telefone', 'Telefone', 'phone', 'celular', 'mobile']
        };
        
        const dados = {};
        
        // Coletar dados usando mapeamento
        for (const [key, selectors] of Object.entries(fieldMappings)) {
            for (const selector of selectors) {
                const element = form.querySelector(`[name="${selector}"], [id="${selector}"], [data-name="${selector}"]`);
                if (element && element.value) {
                    dados[key] = element.value.trim();
                    break;
                }
            }
        }
        
        // Fallback: tentar coletar todos os inputs
        if (Object.keys(dados).length === 0) {
            const inputs = form.querySelectorAll('input, select, textarea');
            inputs.forEach((input, index) => {
                if (input.value && input.name) {
                    const name = input.name.toLowerCase();
                    if (name.includes('cpf')) dados.cpf = input.value;
                    else if (name.includes('nome')) dados.nome = input.value;
                    else if (name.includes('placa')) dados.placa = input.value;
                    else if (name.includes('cep')) dados.cep = input.value;
                    else if (name.includes('email')) dados.email = input.value;
                    else if (name.includes('telefone') || name.includes('celular')) dados.telefone = input.value;
                }
            });
        }
        
        return dados;
    }
    
    /**
     * Validar dados do formulário
     */
    validateFormData(dados) {
        const camposObrigatorios = ['cpf', 'nome', 'placa', 'cep'];
        const camposFaltando = camposObrigatorios.filter(campo => !dados[campo]);
        
        if (camposFaltando.length > 0) {
            throw new Error(`Campos obrigatórios faltando: ${camposFaltando.join(', ')}`);
        }
        
        // Validações específicas
        if (dados.cpf && !this.isValidCPF(dados.cpf)) {
            throw new Error('CPF inválido');
        }
        
        if (dados.placa && !this.isValidPlaca(dados.placa)) {
            throw new Error('Placa inválida');
        }
        
        if (dados.cep && !this.isValidCEP(dados.cep)) {
            throw new Error('CEP inválido');
        }
        
        if (dados.email && !this.isValidEmail(dados.email)) {
            throw new Error('E-mail inválido');
        }
    }
    
    /**
     * Validar CPF (básico - validação completa no frontend)
     */
    isValidCPF(cpf) {
        cpf = cpf.replace(/[^\d]/g, '');
        return cpf.length === 11;
    }
    
    /**
     * Validar placa
     */
    isValidPlaca(placa) {
        placa = placa.replace(/[^\w]/g, '').toUpperCase();
        return /^[A-Z]{3}\d{4}$/.test(placa);
    }
    
    /**
     * Validar CEP
     */
    isValidCEP(cep) {
        cep = cep.replace(/[^\d]/g, '');
        return cep.length === 8;
    }
    
    /**
     * Validar email
     */
    isValidEmail(email) {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    }
    
    /**
     * Fetch com retry e backoff exponencial
     */
    async fetchWithRetry(url, options, maxRetries = 3) {
        for (let i = 0; i < maxRetries; i++) {
            try {
                console.log(`🔄 Tentativa ${i + 1}/${maxRetries} para ${url}`);
                const response = await fetch(url, options);
                
                if (response.ok) {
                    console.log(`✅ Sucesso na tentativa ${i + 1}`);
                    return response;
                }
                
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            } catch (error) {
                console.warn(`⚠️ Tentativa ${i + 1} falhou:`, error.message);
                
                if (i === maxRetries - 1) {
                    throw new Error(`Falha após ${maxRetries} tentativas: ${error.message}`);
                }
                
                // Backoff exponencial: 1s, 2s, 4s, 8s...
                const delay = Math.pow(2, i) * 1000;
                console.log(`⏳ Aguardando ${delay}ms antes da próxima tentativa...`);
                await new Promise(resolve => setTimeout(resolve, delay));
            }
        }
    }

    /**
     * Iniciar RPA
     */
    async startRPA(dados) {
        try {
            console.log('🚀 Iniciando RPA...');
            
            // Chamar API para iniciar sessão com retry
            const response = await this.fetchWithRetry(`${this.apiBaseUrl}/start`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(dados)
            });
            
            const result = await response.json();
            console.log('📡 Resposta da API:', result);
            
            if (!result.success) {
                throw new Error(result.message || 'Erro ao iniciar RPA');
            }
            
            this.sessionId = result.session_id;
            console.log('🆔 Session ID:', this.sessionId);
            
            // Abrir modal de progresso
            this.openProgressModal();
            
            // Iniciar monitoramento
            this.startProgressMonitoring();
            
        } catch (error) {
            throw new Error(`Erro ao iniciar RPA: ${error.message}`);
        }
    }
    
    /**
     * Abrir modal de progresso
     */
    openProgressModal() {
        if (!window.Swal) {
            throw new Error('SweetAlert2 não carregado');
        }
        
        console.log('📱 Abrindo modal de progresso...');
        
        this.modal = Swal.fire({
            title: '<div style="font-family: \'Titillium Web\', sans-serif; font-size: 24px; font-weight: 600; color: #2c3e50;"><i class="fas fa-cogs" style="color: #3498db; margin-right: 10px;"></i>Processando Cotação</div>',
            html: this.generateModalHTML(),
            width: '500px',
            showConfirmButton: false,
            allowOutsideClick: false,
            allowEscapeKey: false,
            customClass: {
                popup: 'rpa-modal-popup',
                title: 'rpa-modal-title',
                htmlContainer: 'rpa-modal-content'
            },
            didOpen: () => {
                this.setupModalEventListeners();
            },
            willClose: () => {
                this.stopProgressMonitoring();
                this.isProcessing = false;
            }
        });
    }

    /**
     * Gerar HTML do modal
     */
    generateModalHTML() {
        return `
            <div style="font-family: 'Titillium Web', sans-serif;">
                <!-- Barra de Progresso -->
                <div style="margin-bottom: 25px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; font-size: 14px; color: #555;">
                        <span>Progresso da Execução</span>
                        <span id="progressPercentage" style="font-weight: 600; color: #2c3e50;">0%</span>
                    </div>
                    <div style="position: relative; background: #f0f0f0; border-radius: 25px; height: 12px; overflow: hidden; box-shadow: inset 0 2px 4px rgba(0,0,0,0.1);">
                        <div id="progressBar" style="height: 100%; background: linear-gradient(90deg, #3498db 0%, #2ecc71 100%); border-radius: 25px; transition: width 0.5s ease; position: relative; overflow: hidden; width: 0%;">
                            <div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: linear-gradient(90deg, transparent 0%, rgba(255,255,255,0.3) 50%, transparent 100%); animation: shimmer 2s infinite;"></div>
                        </div>
                    </div>
                </div>
                
                <!-- Fase Atual -->
                <div id="currentPhase" style="text-align: center; margin-bottom: 25px; padding: 15px; background: #f8f9fa; border-radius: 10px; border-left: 4px solid #3498db;">
                    <i class="fas fa-play-circle" style="color: #3498db; margin-right: 8px;"></i>
                    <span style="font-size: 16px; font-weight: 500; color: #2c3e50;">Iniciando processamento...</span>
                </div>
                
                <!-- Cards de Dados -->
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-bottom: 25px;">
                    <div id="estimativaCard" style="background: #f8f9fa; border-radius: 12px; padding: 20px; text-align: center; border: 2px solid transparent; transition: all 0.3s ease;">
                        <div style="font-size: 12px; font-weight: 600; color: #7f8c8d; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px;">Estimativa Inicial</div>
                        <div id="estimativaValue" style="font-size: 18px; font-weight: 700; color: #bdc3c7; font-style: italic; min-height: 24px; display: flex; align-items: center; justify-content: center;">Aguardando...</div>
                    </div>
                    <div id="valorFinalCard" style="background: #f8f9fa; border-radius: 12px; padding: 20px; text-align: center; border: 2px solid transparent; transition: all 0.3s ease;">
                        <div style="font-size: 12px; font-weight: 600; color: #7f8c8d; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px;">Valor Final Obtido</div>
                        <div id="valorFinalValue" style="font-size: 18px; font-weight: 700; color: #bdc3c7; font-style: italic; min-height: 24px; display: flex; align-items: center; justify-content: center;">Aguardando...</div>
                    </div>
                </div>
                
                <!-- Botão de Fechar -->
                <button id="closeButton" style="width: 100%; padding: 15px; background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%); color: white; border: none; border-radius: 10px; font-size: 16px; font-weight: 600; cursor: pointer; transition: all 0.3s ease; font-family: 'Titillium Web', sans-serif;" disabled>
                    <i class="fas fa-times"></i> Fechar
                </button>
            </div>
            
            <style>
                @keyframes shimmer {
                    0% { transform: translateX(-100%); }
                    100% { transform: translateX(100%); }
                }
                
                .rpa-modal-popup {
                    border-radius: 20px !important;
                    box-shadow: 0 20px 40px rgba(0,0,0,0.1) !important;
                }
                
                .rpa-modal-title {
                    margin-bottom: 20px !important;
                }
                
                .rpa-modal-content {
                    padding: 0 !important;
                }
                
                @media (max-width: 768px) {
                    .rpa-modal-popup {
                        width: 90% !important;
                        margin: 10px !important;
                    }
                    
                    .rpa-modal-content div[style*="grid-template-columns: 1fr 1fr"] {
                        grid-template-columns: 1fr !important;
                    }
                }
            </style>
        `;
    }
    
    /**
     * Configurar event listeners do modal
     */
    setupModalEventListeners() {
        const closeButton = document.getElementById('closeButton');
        if (closeButton) {
            closeButton.addEventListener('click', () => {
                this.closeModal();
            });
        }
    }
    
    /**
     * Iniciar monitoramento de progresso
     */
    startProgressMonitoring() {
        if (this.progressInterval) {
            clearInterval(this.progressInterval);
        }
        
        console.log('📊 Iniciando monitoramento de progresso...');
        
        let pollCount = 0;
        const maxPolls = this.config.maxPollTime / this.config.pollInterval;
        
        this.progressInterval = setInterval(async () => {
            try {
                pollCount++;
                
                if (pollCount > maxPolls) {
                    this.showError('Timeout', 'Tempo limite de processamento excedido');
                    return;
                }
                
                // Usar fetchWithRetry para monitoramento
                const response = await this.fetchWithRetry(`${this.apiBaseUrl}/progress/${this.sessionId}`, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                    }
                }, 2); // Menos tentativas para polling
                
                const data = await response.json();
                console.log('📈 Progresso atualizado:', data);
                
                if (data.success) {
                    this.updateProgress(data.progress);
                    
                    // Verificar se concluído
                    if (data.progress && data.progress.status === 'success') {
                        this.completeProcessing(data.progress);
                    }
                } else {
                    throw new Error(data.message || 'Erro ao obter progresso');
                }
                
            } catch (error) {
                console.error('❌ Erro ao monitorar progresso:', error);
                this.showError('Erro de Monitoramento', error.message);
            }
        }, this.config.pollInterval);
    }
    
    /**
     * Atualizar progresso
     */
    updateProgress(progressData) {
        if (!progressData) return;
        
        // Atualizar barra de progresso
        const progress = progressData.percentual || 0;
        const progressBar = document.getElementById('progressBar');
        const progressPercentage = document.getElementById('progressPercentage');
        
        if (progressBar && progressPercentage) {
            progressBar.style.width = progress + '%';
            progressPercentage.textContent = Math.round(progress) + '%';
        }
        
        // Atualizar fase atual
        this.updateCurrentPhase(progress);
        
        // Atualizar estimativas iniciais
        if (progressData.estimativas && progressData.estimativas.capturadas) {
            this.updateInitialEstimate(progressData.estimativas.dados);
        }
        
        // Atualizar resultados finais
        if (progressData.resultados_finais && progressData.resultados_finais.rpa_finalizado) {
            this.updateFinalValue(progressData.resultados_finais.dados);
        }
    }
    
    /**
     * Atualizar fase atual
     */
    updateCurrentPhase(progress) {
        const currentPhase = document.getElementById('currentPhase');
        if (!currentPhase) return;
        
        // Encontrar fase correspondente ao progresso
        let faseAtual = this.phases[0];
        for (let i = this.phases.length - 1; i >= 0; i--) {
            if (progress >= this.phases[i].progress) {
                faseAtual = this.phases[i];
                break;
            }
        }
        
        currentPhase.innerHTML = `
            <i class="${faseAtual.icon}" style="color: #3498db; margin-right: 8px;"></i>
            <span style="font-size: 16px; font-weight: 500; color: #2c3e50;">${faseAtual.text}</span>
        `;
    }
    
    /**
     * Atualizar estimativa inicial
     */
    updateInitialEstimate(estimativas) {
        const estimativaValue = document.getElementById('estimativaValue');
        const estimativaCard = document.getElementById('estimativaCard');
        
        if (estimativaValue && estimativaCard) {
            const valor = estimativas.plano_recomendado || 'N/A';
            estimativaValue.textContent = valor;
            estimativaValue.style.color = '#2c3e50';
            estimativaValue.style.fontStyle = 'normal';
            
            estimativaCard.style.borderColor = '#3498db';
            estimativaCard.style.background = '#fff';
            estimativaCard.style.boxShadow = '0 5px 15px rgba(52, 152, 219, 0.1)';
            
            console.log('💰 Estimativa inicial atualizada:', valor);
        }
    }
    
    /**
     * Atualizar valor final
     */
    updateFinalValue(resultados) {
        const valorFinalValue = document.getElementById('valorFinalValue');
        const valorFinalCard = document.getElementById('valorFinalCard');
        
        if (valorFinalValue && valorFinalCard) {
            const valor = resultados.valor_final || 'N/A';
            valorFinalValue.textContent = valor;
            valorFinalValue.style.color = '#2c3e50';
            valorFinalValue.style.fontStyle = 'normal';
            
            valorFinalCard.style.borderColor = '#3498db';
            valorFinalCard.style.background = '#fff';
            valorFinalCard.style.boxShadow = '0 5px 15px rgba(52, 152, 219, 0.1)';
            
            console.log('🎯 Valor final atualizado:', valor);
        }
    }
    
    /**
     * Concluir processamento
     */
    completeProcessing(progressData) {
        console.log('🎉 Processamento concluído!');
        
        this.stopProgressMonitoring();
        
        const closeButton = document.getElementById('closeButton');
        const currentPhase = document.getElementById('currentPhase');
        const progressBar = document.getElementById('progressBar');
        
        if (closeButton) {
            closeButton.disabled = false;
            closeButton.innerHTML = '<i class="fas fa-check"></i> Concluído - Fechar';
            closeButton.style.background = 'linear-gradient(135deg, #27ae60 0%, #2ecc71 100%)';
        }
        
        if (currentPhase) {
            currentPhase.style.color = '#27ae60';
            currentPhase.style.borderLeftColor = '#27ae60';
        }
        
        if (progressBar) {
            progressBar.style.background = 'linear-gradient(90deg, #27ae60 0%, #2ecc71 100%)';
        }
        
        // Disparar evento de conclusão
        this.dispatchEvent('rpaConcluido', {
            sessionId: this.sessionId,
            progressData: progressData
        });
        
        this.isProcessing = false;
    }
    
    /**
     * Parar monitoramento
     */
    stopProgressMonitoring() {
        if (this.progressInterval) {
            clearInterval(this.progressInterval);
            this.progressInterval = null;
            console.log('⏹️ Monitoramento parado');
        }
    }
    
    /**
     * Fechar modal
     */
    closeModal() {
        if (this.modal) {
            Swal.close();
            this.stopProgressMonitoring();
            this.isProcessing = false;
            console.log('❌ Modal fechado');
        }
    }
    
    /**
     * Mostrar erro
     */
    showError(titulo, mensagem, detalhes = null) {
        this.stopProgressMonitoring();
        
        // Preparar mensagem detalhada
        let mensagemCompleta = mensagem;
        if (detalhes) {
            mensagemCompleta += `\n\nDetalhes: ${detalhes}`;
        }
        
        Swal.fire({
            icon: 'error',
            title: titulo,
            text: mensagemCompleta,
            confirmButtonText: 'Fechar',
            showCancelButton: true,
            cancelButtonText: 'Tentar Novamente',
            cancelButtonColor: '#3498db',
            customClass: {
                popup: 'rpa-modal-popup',
                title: 'rpa-modal-title'
            }
        }).then((result) => {
            if (result.dismiss === Swal.DismissReason.cancel) {
                // Tentar novamente
                this.retryLastOperation();
            } else {
                this.isProcessing = false;
            }
        });
    }

    /**
     * Tentar novamente a última operação
     */
    retryLastOperation() {
        console.log('🔄 Tentando novamente a última operação...');
        
        if (this.sessionId) {
            // Se temos uma sessão, continuar monitoramento
            this.startProgressMonitoring();
        } else {
            // Se não temos sessão, tentar iniciar novamente
            this.handleFormSubmit();
        }
    }
    
    /**
     * Disparar evento customizado
     */
    dispatchEvent(eventName, data) {
        const event = new CustomEvent(eventName, {
            detail: data
        });
        document.dispatchEvent(event);
    }
    
    /**
     * Desabilitar botão
     */
    disableButton() {
        const button = document.querySelector('button[type="submit"], input[type="submit"], .botao-cotacao, #botao-cotacao');
        if (button) {
            button.disabled = true;
            button.textContent = 'Processando...';
            button.style.opacity = '0.6';
            button.style.cursor = 'not-allowed';
            console.log('🔒 Botão desabilitado');
        }
    }
    
    /**
     * Habilitar botão
     */
    enableButton() {
        const button = document.querySelector('button[type="submit"], input[type="submit"], .botao-cotacao, #botao-cotacao');
        if (button) {
            button.disabled = false;
            button.textContent = 'Solicitar Cotação';
            button.style.opacity = '1';
            button.style.cursor = 'pointer';
            console.log('🔓 Botão habilitado');
        }
    }
    
    /**
     * Manipular sucesso do RPA
     */
    handleRPASuccess(data) {
        console.log('🎉 RPA concluído com sucesso:', data);
        
        // Aqui você pode adicionar lógica adicional
        // Por exemplo: redirecionar para página de resultados
        // window.location.href = `/resultados?session=${data.sessionId}`;
        
        // Ou exibir mensagem de sucesso
        // this.showSuccess('Cotação concluída!', 'Sua cotação foi processada com sucesso.');
    }
    
    /**
     * Manipular erro do RPA
     */
    handleRPAError(data) {
        console.error('❌ Erro no RPA:', data);
        
        // Aqui você pode adicionar lógica adicional
        // Por exemplo: enviar erro para analytics
        // gtag('event', 'rpa_error', { error_message: data.message });
    }
    
    /**
     * Mostrar sucesso
     */
    showSuccess(titulo, mensagem) {
        Swal.fire({
            icon: 'success',
            title: titulo,
            text: mensagem,
            confirmButtonText: 'OK',
            customClass: {
                popup: 'rpa-modal-popup',
                title: 'rpa-modal-title'
            }
        });
    }
}

// Inicializar quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', () => {
    console.log('🚀 Inicializando Webflow RPA Integration...');
    
    const rpaClient = new WebflowRPAClient();
    rpaClient.init();
    
    // Tornar disponível globalmente para debug
    window.rpaClient = rpaClient;
    
    console.log('✅ Webflow RPA Integration carregado');
});

// Fallback para casos onde o DOM já está pronto
if (document.readyState === 'loading') {
    // DOM ainda carregando, aguardar
} else {
    // DOM já pronto, inicializar imediatamente
    console.log('🚀 Inicializando Webflow RPA Integration (DOM já pronto)...');
    
    const rpaClient = new WebflowRPAClient();
    rpaClient.init();
    
    // Tornar disponível globalmente para debug
    window.rpaClient = rpaClient;
    
    console.log('✅ Webflow RPA Integration carregado');
}
