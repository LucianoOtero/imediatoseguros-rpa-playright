/**
 * Modal RPA Imediato Seguros V6.1.0
 * JavaScript para integração completa com RPA V4
 * 
 * Funcionalidades:
 * - Formulário simplificado (8 campos essenciais)
 * - Integração com API RPA V4 
 * - Barra de progresso com identidade visual
 * - Polling do progresso das 15 telas
 * - Captura de estimativa inicial e cálculo final
 * - Dados hardcoded do parametros.json
 */

class ModalRPAImediatoV6 {
    constructor() {
        this.apiBaseUrl = 'http://rpaimediatoseguros.com.br';
        this.sessionId = null;
        this.progressInterval = null;
        this.isProcessing = false;
        
        // Fases do RPA (15 telas)
        this.rpaPhases = [
            'Tela 1: Acesso ao Site',
            'Tela 2: Início do Questionário',
            'Tela 3: Dados Pessoais',
            'Tela 4: Dados do Veículo',
            'Tela 5: Endereço',
            'Tela 6: Condutor Principal',
            'Tela 7: Condutor Adicional',
            'Tela 8: Configurações de Estacionamento',
            'Tela 9: Configurações Adicionais',
            'Tela 10: Verificação de Dados',
            'Tela 11: Cálculo de Prêmio',
            'Tela 12: Apresentação de Cotações',
            'Tela 13: Seleção de Seguro',
            'Tela 14: Confirmação Final',
            'Tela 15: Geração do Resultado'
        ];
        
        // Dados fixos do parametros.json
        this.fixedData = {
            // Configuração
            configuracao: {
                log: true,
                display: true,
                log_rotacao_dias: 90,
                log_nivel: "INFO",
                tempo_estabilizacao: 0.5,
                tempo_carregamento: 0.5,
                tempo_estabilizacao_tela5: 2,
                tempo_carregamento_tela5: 5,
                tempo_estabilizacao_tela15: 3,
                tempo_carregamento_tela15: 5,
                inserir_log: true,
                visualizar_mensagens: true,
                eliminar_tentativas_inuteis: true,
                modo_silencioso: false
            },
            
            // Autenticação
            autenticacao: {
                email_login: "aleximediatoseguros@gmail.com",
                senha_login: "Lrotero1$",
                manter_login_atual: true
            },
            
            // URL
            url: "https://www.app.tosegurado.com.br/imediatosolucoes",
            
            // Dados do Veículo (fixos)
            modelo: "COROLLA XEI 1.8/1.8 FLEX 16V MEC",
            ano: "2009",
            zero_km: false,
            combustivel: "Flex",
            veiculo_segurado: "Não",
            tipo_veiculo: "carro",
            
            // Dados de Endereço (fixos)
            endereco_completo: "Rua Serra de Botucatu, 410 APTO 11 - São Paulo, SP",
            uso_veiculo: "Pessoal",
            endereco: "Rua Serra de Botucatu, Tatuapé - São Paulo/SP",
            
            // Dados Pessoais (fixos)
            email: "alex.kaminski@imediatoseguros.com.br",
            celular: "11953288466",
            
            // Dados do Condutor (fixos)
            condutor_principal: true,
            nome_condutor: "SANDRA LOUREIRO",
            cpf_condutor: "25151787829",
            data_nascimento_condutor: "28/08/1975",
            sexo_condutor: "Feminino",
            estado_civil_condutor: "Casado ou Uniao Estavel",
            
            // Configurações de Estacionamento (fixas)
            local_de_trabalho: false,
            estacionamento_proprio_local_de_trabalho: false,
            local_de_estudo: false,
            estacionamento_proprio_local_de_estudo: false,
            garagem_residencia: true,
            portao_eletronico: "Eletronico",
            
            // Configurações Adicionais (fixas)
            kit_gas: false,
            blindado: false,
            financiado: false,
            reside_18_26: "Não",
            continuar_com_corretor_anterior: true
        };
        
        this.init();
    }
    
    /**
     * Inicializar a aplicação
     */
    init() {
        console.log('🚀 Inicializando Modal RPA Imediato V6.1.0...');
        
        // Aguardar DOM estar pronto
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.setupEventListeners());
        } else {
            this.setupEventListeners();
        }
        
        // Configurar validação em tempo real
        this.setupRealTimeValidation();
        
        console.log('✅ Modal RPA Imediato V6.1.0 inicializado');
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
     * Configurar validação em tempo real
     */
    setupRealTimeValidation() {
        console.log('🔍 Configurando validação em tempo real...');
        
        setTimeout(() => {
            this.setupFieldValidation();
        }, 500);
        
        console.log('✅ Validação em tempo real configurada');
    }
    
    /**
     * Set up field validation for real-time validation
     */
    setupFieldValidation() {
        // CPF validation
        const cpfField = document.getElementById('cpf');
        if (cpfField) {
            cpfField.addEventListener('input', () => this.validateCPFRealTime(cpfField));
        }
        
        // CEP validation
        const cepField = document.getElementById('cep');
        if (cepField) {
            cepField.addEventListener('input', () => this.validateCEPRealTime(cepField));
        }
        
        // Placa validation
        const placaField = document.getElementById('placa');
        if (placaField) {
            placaField.addEventListener('input', () => this.validatePlacaRealTime(placaField));
        }
        
        // Data nascimento validation
        const dataNascimentoField = document.getElementById('data_nascimento');
        if (dataNascimentoField) {
            dataNascimentoField.addEventListener('input', () => this.validateDataNascimentoRealTime(dataNascimentoField));
        }
        
        console.log('✅ Validação em tempo real configurada para todos os campos');
    }
    
    /**
     * Validar CPF em tempo real
     */
    validateCPFRealTime(field) {
        const value = field.value.replace(/\D/g, '');
        const isValid = value.length === 11 && this.isValidCPF(value);
        
        field.classList.remove('success', 'error');
        field.classList.add(isValid ? 'success' : 'error');
        
        return isValid;
    }
    
    /**
     * Validar CEP em tempo real
     */
    validateCEPRealTime(field) {
        const value = field.value.replace(/\D/g, '');
        const isValid = value.length === 8;
        
        field.classList.remove('success', 'error');
        field.classList.add(isValid ? 'success' : 'error');
        
        return isValid;
    }
    
    /**
     * Validar Placa em tempo real
     */
    validatePlacaRealTime(field) {
        const value = field.value.toUpperCase();
        const isValid = value.length === 7;
        
        field.classList.remove('success', 'error');
        field.classList.add(isValid ? 'success' : 'error');
        
        return isValid;
    }
    
    /**
     * Validar Data de Nascimento em tempo real
     */
    validateDataNascimentoRealTime(field) {
        const value = field.value;
        const isValid = /^\d{2}\/\d{2}\/\d{4}$/.test(value);
        
        field.classList.remove('success', 'error');
        field.classList.add(isValid ? 'success' : 'error');
        
        return isValid;
    }
    
    /**
     * Verificar se CPF é válido
     */
    isValidCPF(cpf) {
        if (cpf.length !== 11) return false;
        if (/^(\d)\1{10}$/.test(cpf)) return false;
        
        let sum = 0;
        for (let i = 0; i < 9; i++) {
            sum += parseInt(cpf.charAt(i)) * (10 - i);
        }
        let remainder = (sum * 10) % 11;
        if (remainder === 10 || remainder === 11) remainder = 0;
        if (remainder !== parseInt(cpf.charAt(9))) return false;
        
        sum = 0;
        for (let i = 0; i < 10; i++) {
            sum += parseInt(cpf.charAt(i)) * (11 - i);
        }
        remainder = (sum * 10) % 11;
        if (remainder === 10 || remainder === 11) remainder = 0;
        if (remainder !== parseInt(cpf.charAt(10))) return false;
        
        return true;
    }
    
    /**
     * Handle form submission
     */
    async handleFormSubmit(event) {
        event.preventDefault();
        
        console.log('📝 Formulário submetido');
        
        if (this.isProcessing) {
            console.log('⏳ RPA já está em execução');
            return;
        }
        
        // Validar formulário
        if (!this.validateForm()) {
            console.log('❌ Formulário inválido');
            this.showError('Por favor, preencha todos os campos corretamente.');
            return;
        }
        
        // Coletar dados do formulário
        const formData = this.collectFormData();
        console.log('📊 Dados coletados:', formData);
        
        // Mesclar com dados fixos
        const completeData = this.mergeWithFixedData(formData);
        console.log('🔗 Dados completos:', completeData);
        
        // Iniciar RPA
        await this.startRPA(completeData);
    }
    
    /**
     * Validar formulário completo
     */
    validateForm() {
        const requiredFields = ['cpf', 'nome', 'data_nascimento', 'sexo', 'estado_civil', 'placa', 'marca', 'cep'];
        
        for (const fieldId of requiredFields) {
            const field = document.getElementById(fieldId);
            if (!field || !field.value.trim()) {
                field.classList.add('error');
                return false;
            }
            
            // Validações específicas
            if (fieldId === 'cpf' && !this.validateCPFRealTime(field)) return false;
            if (fieldId === 'cep' && !this.validateCEPRealTime(field)) return false;
            if (fieldId === 'placa' && !this.validatePlacaRealTime(field)) return false;
            if (fieldId === 'data_nascimento' && !this.validateDataNascimentoRealTime(field)) return false;
        }
        
        return true;
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
     * Iniciar processo RPA
     */
    async startRPA(data) {
        try {
            this.isProcessing = true;
            this.updateButtonState(true);
            
            console.log('🚀 Iniciando RPA...');
            
            // Mostrar barra de progresso
            this.showProgressBar();
            
            // Chamar API para iniciar RPA
            const response = await this.callRPAAPI(data);
            
            if (response.success) {
                this.sessionId = response.session_id;
                console.log('✅ RPA iniciado com sucesso. Session ID:', this.sessionId);
                
                // Iniciar polling do progresso
                this.startProgressPolling();
            } else {
                throw new Error(response.message || 'Erro ao iniciar RPA');
            }
            
        } catch (error) {
            console.error('❌ Erro ao iniciar RPA:', error);
            this.handleRPAError(error.message);
        }
    }
    
    /**
     * Chamar API do RPA
     */
    async callRPAAPI(data) {
        const url = `${this.apiBaseUrl}/api/rpa/start`;
        
        console.log('🌐 Chamando API:', url);
        
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                session: this.generateSessionId(),
                dados: data
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        return await response.json();
    }
    
    /**
     * Gerar ID de sessão único
     */
    generateSessionId() {
        return 'rpa_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }
    
    /**
     * Mostrar barra de progresso
     */
    showProgressBar() {
        const progressContainer = document.getElementById('rpaProgressContainer');
        if (progressContainer) {
            progressContainer.style.display = 'block';
            progressContainer.classList.add('animate-slideInUp');
        }
    }
    
    /**
     * Esconder barra de progresso
     */
    hideProgressBar() {
        const progressContainer = document.getElementById('rpaProgressContainer');
        if (progressContainer) {
            progressContainer.style.display = 'none';
        }
    }
    
    /**
     * Iniciar polling do progresso
     */
    startProgressPolling() {
        console.log('🔄 Iniciando polling do progresso...');
        
        this.progressInterval = setInterval(async () => {
            try {
                await this.checkProgress();
            } catch (error) {
                console.error('❌ Erro no polling:', error);
                this.handleRPAError('Erro ao verificar progresso');
            }
        }, 2000); // Polling a cada 2 segundos
    }
    
    /**
     * Parar polling do progresso
     */
    stopProgressPolling() {
        if (this.progressInterval) {
            clearInterval(this.progressInterval);
            this.progressInterval = null;
            console.log('⏹️ Polling do progresso parado');
        }
    }
    
    /**
     * Verificar progresso do RPA
     */
    async checkProgress() {
        if (!this.sessionId) {
            console.log('❌ Session ID não encontrado');
            return;
        }
        
        const url = `${this.apiBaseUrl}/api/rpa/progress/${this.sessionId}`;
        
        try {
            const response = await fetch(url);
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            
            const progressData = await response.json();
            console.log('📊 Progresso recebido:', progressData);
            
            this.updateProgress(progressData);
            
        } catch (error) {
            console.error('❌ Erro ao verificar progresso:', error);
            throw error;
        }
    }
    
    /**
     * Atualizar progresso na interface
     */
    updateProgress(data) {
        const { status, progress, current_phase, mensagem } = data;
        
        // Extrair dados do progresso
        const progressData = progress || {};
        const currentStatus = progressData.status || status;
        const currentMessage = progressData.mensagem || mensagem;
        const currentPhase = progressData.etapa_atual || current_phase;
        const percentual = progressData.percentual || 0;
        
        // Atualizar porcentagem
        const progressFill = document.getElementById('rpaProgressFill');
        const progressGlow = document.getElementById('rpaProgressGlow');
        const progressText = document.getElementById('rpaProgressText');
        
        if (progressFill && progressGlow) {
            const percentage = Math.min(100, Math.max(0, percentual || 0));
            progressFill.style.width = `${percentage}%`;
            progressGlow.style.width = `${percentage}%`;
        }
        
        if (progressText) {
            progressText.textContent = `${Math.round(percentual || 0)}%`;
        }
        
        // Atualizar fase atual
        const currentPhaseElement = document.getElementById('rpaCurrentPhase');
        const phaseIndicator = document.getElementById('rpaPhaseIndicator');
        
        if (currentPhaseElement) {
            const phaseText = currentMessage || `Tela ${currentPhase}` || 'Processando...';
            currentPhaseElement.textContent = phaseText;
        }
        
        if (phaseIndicator) {
            const phaseText = currentMessage || `Tela ${currentPhase}` || 'Processando...';
            phaseIndicator.innerHTML = `<i class="fas fa-play"></i><span>${phaseText}</span>`;
        }
        
        // Verificar se houve falha
        if (currentMessage && currentMessage.includes('falhou')) {
            console.log('❌ RPA falhou:', currentMessage);
            this.handleProcessingError(currentMessage);
            return;
        }
        
        // Verificar se concluído
        if (currentStatus === 'success' || currentStatus === 'completed') {
            console.log('✅ RPA concluído com sucesso');
            this.handleRPASuccess(data);
            return;
        }
        
        // Verificar se falhou
        if (currentStatus === 'failed' || currentStatus === 'error' || currentStatus === 'erro') {
            console.log('❌ RPA falhou:', currentMessage);
            this.handleProcessingError(currentMessage || 'Erro desconhecido');
            return;
        }
    }
    
    /**
     * Handle RPA success
     */
    handleRPASuccess(data) {
        this.stopProgressPolling();
        this.hideProgressBar();
        this.updateButtonState(false);
        this.isProcessing = false;
        
        // Mostrar resultados
        this.showResults(data);
        
        console.log('🎉 RPA executado com sucesso!');
    }
    
    /**
     * Handle RPA error
     */
    handleRPAError(message) {
        this.stopProgressPolling();
        this.hideProgressBar();
        this.updateButtonState(false);
        this.isProcessing = false;
        
        this.showError(message);
        
        console.log('❌ RPA falhou:', message);
    }
    
    /**
     * Handle processing error
     */
    handleProcessingError(message) {
        this.stopProgressPolling();
        this.hideProgressBar();
        this.updateButtonState(false);
        this.isProcessing = false;
        
        this.showError(message);
        
        console.log('❌ Processamento falhou:', message);
    }
    
    /**
     * Mostrar resultados
     */
    showResults(data) {
        const resultsSection = document.getElementById('rpaResultsSection');
        if (!resultsSection) {
            console.log('❌ Seção de resultados não encontrada');
            return;
        }
        
        // Mostrar seção de resultados
        resultsSection.style.display = 'block';
        resultsSection.classList.add('animate-fadeIn');
        
        // Atualizar valores
        this.updateResults(data);
        
        console.log('💰 Resultados exibidos');
    }
    
    /**
     * Atualizar valores nos cards de resultados
     */
    updateResults(data) {
        const { progress } = data;
        
        // Extrair dados das estimativas
        const estimativas = progress?.estimativas?.dados;
        const resultadosFinais = progress?.resultados_finais?.dados?.dados_finais;
        
        // Estimativa inicial (primeira cobertura)
        const initialEstimateElement = document.getElementById('rpaInitialEstimate');
        if (initialEstimateElement && estimativas?.coberturas_detalhadas?.[0]) {
            const primeiraCobertura = estimativas.coberturas_detalhadas[0];
            const valorInicial = primeiraCobertura.valores?.de || primeiraCobertura.valores?.ate;
            if (valorInicial) {
                initialEstimateElement.textContent = valorInicial;
                initialEstimateElement.classList.add('animate-pulse');
            }
        }
        
        // Cálculo recomendado
        const recommendedElement = document.getElementById('rpaRecommendedValue');
        if (recommendedElement && resultadosFinais?.plano_recomendado?.valor) {
            recommendedElement.textContent = resultadosFinais.plano_recomendado.valor;
            recommendedElement.classList.add('animate-pulse');
        }
        
        // Cálculo alternativo
        const alternativeElement = document.getElementById('rpaAlternativeValue');
        if (alternativeElement && resultadosFinais?.plano_alternativo?.valor) {
            alternativeElement.textContent = resultadosFinais.plano_alternativo.valor;
            alternativeElement.classList.add('animate-pulse');
        }
    }
    
    /**
     * Formatar valor monetário
     */
    formatCurrency(value) {
        if (!value) return '-';
        
        const numValue = parseFloat(value);
        if (isNaN(numValue)) return '-';
        
        return numValue.toLocaleString('pt-BR', {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        });
    }
    
    /**
     * Atualizar estado do botão
     */
    updateButtonState(loading) {
        const btnCalculate = document.getElementById('btnCalculate');
        const btnLoading = btnCalculate?.querySelector('.btn-loading');
        const btnText = btnCalculate?.querySelector('span');
        
        if (btnCalculate) {
            btnCalculate.disabled = loading;
        }
        
        if (btnLoading) {
            btnLoading.style.display = loading ? 'flex' : 'none';
        }
        
        if (btnText) {
            btnText.textContent = loading ? 'Processando...' : 'Calcular Seguro';
        }
    }
    
    /**
     * Mostrar erro
     */
    showError(message) {
        // Implementar exibição de erro elegante
        alert(`Erro: ${message}`);
        console.error('❌ Erro:', message);
    }
}

// Inicializar quando DOM estiver pronto
document.addEventListener('DOMContentLoaded', () => {
    new ModalRPAImediatoV6();
});
