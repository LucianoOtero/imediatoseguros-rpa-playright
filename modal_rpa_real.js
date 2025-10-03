/**
 * Modal RPA Real - Execução das 15 Telas
 * JavaScript para integração completa com RPA V4
 * 
 * Funcionalidades:
 * - Coleta de dados do formulário HTML
 * - Integração com API RPA V4 
 * - Modal de progresso em tempo real
 * - Polling do progresso das 15 telas
 * - Captura de estimativa inicial e cálculo final
 */

class ModalRPAReal {
    constructor() {
        this.apiBaseUrl = 'http://37.27.92.160/api/rpa';
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
        
        this.init();
    }
    
    /**
     * Inicializar a aplicação
     */
    init() {
        console.log('🚀 Inicializando Modal RPA Real...');
        
        // Aguardar DOM estar pronto
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.setupEventListeners());
        } else {
            this.setupEventListeners();
        }
        
        // Configurar validação em tempo real
        this.setupRealTimeValidation();
        
        console.log('✅ Modal RPA Real inicializado');
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
我来修改中文的注释为英文，并继续完成JavaScript代码：
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
        
        // License plate validation
        const placaField = document.getElementById('placa');
        if (placaField) {
            placaField.addEventListener('input', () => {
                placaField.value = placaField.value.toUpperCase();
                this.validatePlacaRealTime(placaField);
            });
        }
        
        // CEP validation
        const cepField = document.getElementById('cep');
        if (cepField) {
            cepField.addEventListener('input', () => this.validateCEPRealTime(cepField));
        }
        
        // Email validation
        const emailField = document.getElementById('email');
        if (emailField) {
            emailField.addEventListener('input', () => this.validateEmailRealTime(emailField));
        }
    }
    
    /**
     * Real-time CPF validation (basic - complete validation in frontend)
     */
    validateCPFRealTime(field) {
        const cpf = field.value.replace(/[^\d]/g, '');
        const isValid = cpf.length === 11;
        
        this.updateFieldValidation(field, isValid, 'CPF deve ter 11 dígitos');
        return isValid;
    }
    
    /**
     * Real-time license plate validation
     */
    validatePlacaRealTime(field) {
        const placa = field.value.replace(/[^\w]/g, '').toUpperCase();
        const isValid = placa.length === 7;
        
        this.updateFieldValidation(field, isValid, 'Placa deve ter 7 caracteres');
        return isValid;
    }
    
    /**
     * Real-time CEP validation
     */
    validateCEPRealTime(field) {
        const cep = field.value.replace(/[^\d]/g, '');
        const isValid = cep.length === 8;
        
        this.updateFieldValidation(field, isValid, 'CEP deve ter 8 dígitos');
        return isValid;
    }
    
    /**
     * Real-time email validation
     */
    validateEmailRealTime(field) {
        const email = field.value;
        const isValid = email === '' || /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
        
        this.updateFieldValidation(field, isValid, 'Email deve ser válido');
        return isValid;
    }
    
    /**
     * Update field validation visual state
     */
    updateFieldValidation(field, isValid, message) {
        field.classList.remove('field-valid', 'field-invalid');
        
        if (field.value !== '') {
            field.classList.add(isValid ? 'field-valid' : 'field-invalid');
        }
        
        // Remove existing error message
        const existingError = field.parentNode.querySelector('.field-error');
        if (existingError) {
            existingError.remove();
        }
        
        // Add new error message if invalid
        if (!isValid && field.value !== '') {
            const errorDiv = document.createElement('div');
            errorDiv.className = 'field-error';
            errorDiv.textContent = message;
            field.parentNode.appendChild(errorDiv);
        }
    }
    
    /**
     * Handle form submission
     */
    async handleFormSubmit(event) {
        event.preventDefault();
        
        if (this.isProcessing) {
            console.log('⚠️ Processamento já em andamento');
            return;
        }
        
        console.log('🚀 Iniciando processo RPA...');
        
        this.isProcessing = true;
        this.updateUI(true);
        
        try {
            console.log('🔍 DEBUG: Tentando coletar dados...');
            
            // Collect form data
            const formData = this.collectFormData();
            console.log('📋 DEBUG: Dados coletados:', formData);
            
            // Validate data
            console.log('🔍 DEBUG: Validando dados...');
            if (!this.validateFormData(formData)) {
                throw new Error('Dados do formulário inválidos');
            }
            console.log('✅ DEBUG: Validação OK');
            
            // Start RPA
            console.log('🔍 DEBUG: Iniciando RPA...');
            await this.startRPA(formData);
            console.log('✅ DEBUG: RPA iniciado');
            
        } catch (error) {
            console.error('❌ DEBUG: Erro no processo RPA:', error);
            console.error('❌ DEBUG: Stack trace:', error.stack);
            this.showError('Erro no Processamento', error.message);
            this.isProcessing = false;
            this.updateUI(false);
        }
    }
    
    /**
     * Collect form data
     */
    collectFormData() {
        const form = document.getElementById('rpa-form');
        const formData = new FormData(form);
        const data = {};
        
        // Convert FormData to object
        for (let [key, value] of formData.entries()) {
            data[key] = value;
        }
        
        // Convert strings types
        data.condutor_principal = data.condutor_principal === 'true';
        data.garagem_residencia = data.garagem_residencia === 'true';
        data.local_de_trabalho = data.local_de_trabalho === 'true';
        data.estacionamento_proprio_local_de_trabalho = data.estacionamento_proprio_local_de_trabalho === 'true';
        data.local_de_estudo = data.local_de_estudo === 'true';
        data.estacionamento_proprio_local_de_estudo = data.estacionamento_proprio_local_de_estudo === 'true';
        data.zero_km = data.zero_km === 'true';
        data.kit_gas = data.kit_gas === 'true';
        data.blindado = data.blindado === 'true';
        data.financiado = data.financiado === 'true';
        data.continuar_com_corretor_anterior = data.continuar_com_corretor_anterior === 'true';
        
        return data;
    }
    
    /**
     * Validate form data
     */
    validateFormData(data) {
        const requiredFields = ['cpf', 'nome', 'placa', 'cep'];
        
        for (let field of requiredFields) {
            if (!data[field] || data[field].trim() === '') {
                console.error(`❌ Campo obrigatório vazio: ${field}`);
                return false;
            }
        }
        
        // Validate CPF (basic)
        if (!this.isValidCPF(data.cpf)) {
            console.error('❌ CPF inválido');
            return false;
        }
        
        // Validate email if provided
        if (data.email && !this.isValidEmail(data.email)) {
            console.error('❌ Email inválido');
            return false;
        }
        
        return true;
    }
    
    /**
     * Validate CPF (basic - complete validation in frontend)
     */
    isValidCPF(cpf) {
        cpf = cpf.replace(/[^\d]/g, '');
        return cpf.length === 11;
    }
    
    /**
     * Validate email
     */
    isValidEmail(email) {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    }
    
    /**
     * Start RPA execution
     */
    async startRPA(formData) {
        console.log('🚀 DEBUG: Iniciando execução RPA...');
        console.log('🔍 DEBUG: API URL:', this.apiBaseUrl);
        console.log('🔍 DEBUG: Form Data:', formData);
        
        try {
            // Call API to start RPA
            console.log('🔍 DEBUG: Fazendo chamada para:', `${this.apiBaseUrl}/start`);
            const response = await this.fetchWithRetry(`${this.apiBaseUrl}/start`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                body: JSON.stringify(formData)
            });
            
            const result = await response.json();
            
            if (!result.success) {
                throw new Error(result.message || 'Erro ao iniciar RPA');
            }
            
            this.sessionId = result.session_id;
            console.log('🆔 Session ID:', this.sessionId);
            
            // Show progress modal
            this.showProgressModal();
            
            // Start progress monitoring
            this.startProgressMonitoring();
            
        } catch (error) {
            console.error('❌ Erro ao iniciar RPA:', error);
            
            // Detectar erro 502 Bad Gateway especificamente
            if (error.message && error.message.includes('502')) {
                throw new Error('Servidor indisponível (502 Bad Gateway). O PHP-FPM pode não estar funcionando no servidor.');
            } else if (error.message && error.message.includes('Failed to fetch')) {
                throw new Error('Erro de conectividade. Verifique a conexão com o servidor.');
            }
            
            throw error;
        }
    }
    
    /**
     * Show progress modal
     */
    showProgressModal() {
        console.log('🔍 DEBUG: Tentando mostrar modal de progresso...');
        
        if (typeof Swal === 'undefined') {
            console.error('❌ DEBUG: SweetAlert2 não está carregado!');
            throw new Error('SweetAlert2 não está carregado');
        }
        
        console.log('✅ DEBUG: SweetAlert2 disponível');
        
        const phasesHtml = this.rpaPhases.map((phase, index) => 
            `<div class="phase-item pending" id="phase-${index}">
                <i class="fas fa-clock"></i>
                <span>${phase}</span>
            </div>`
        ).join('');
        
        Swal.fire({
            title: 'Calculando Seguro...',
            html: `
                <div class="rpa-progress-modal">
                    <div class="modal-header">
                        <h3><i class="fas fa-calculator"></i> Execução RPA</h3>
                        <div class="progress-container">
                            <div class="progress-bar">
                                <div class="progress-fill" id="progressFill"></div>
                            </div>
                            <div class="progress-text" id="progressText">0%</div>
                        </div>
                    </div>
                    <div class="modal-body">
                        <div class="current-phase" id="currentPhase">
                            <i class="fas fa-play"></i>
                            <span>Iniciando RPA...</span>
                        </div>
                        <div class="phases-list">
                            ${phasesHtml}
                        </div>
                    </div>
                    <div class="modal-footer">
                        <div class="results-section" id="resultsSection" style="display: none;">
                            <div class="estimate-card">
                                <h4>Estimação Inicial</h4>
                                <div class="estimate-value" id="initialEstimate">-</div>
                            </div>
                            <div class="final-card">
                                <h4>Valor Final</h4>
                                <div class="final-value" id="finalCalculation">-</div>
                            </div>
                        </div>
                        <button class="close-btn" id="closeBtn" disabled>
                            <i class="fas fa-times"></i> Fechar
                        </button>
                    </div>
                </div>
            `,
            showConfirmButton: false,
            showCancelButton: false,
            allowOutsideClick: false,
            allowEscapeKey: false,
            customClass: {
                popup: 'rpa-popup',
                title: 'rpa-title'
            },
            didOpen: () => {
                // Store references for updates
                this.progressFill = document.getElementById('progressFill');
                this.progressText = document.getElementById('progressText');
                this.currentPhase = document.getElementById('currentPhase');
                this.resultsSection = document.getElementById('resultsSection');
                this.closeBtn = document.getElementById('closeBtn');
                this.initialEstimate = document.getElementById('initialEstimate');
                this.finalCalculation = document.getElementById('finalCalculation');
            }
        });
        
        console.log('📊 Modal de progresso exibido');
    }
    
    /**
     * Start progress monitoring
     */
    startProgressMonitoring() {
        console.log('🔄 Iniciando monitoramento de progresso...');
        
        this.progressInterval = setInterval(async () => {
            try {
                await this.checkProgress();
            } catch (error) {
                console.error('❌ Erro no monitoramento:', error);
                this.handleMonitoringError(error);
            }
        }, 2000); // Poll every 2 seconds
        
        console.log('✅ Monitoramento de progresso iniciado');
    }
    
    /**
     * Check RPA progress
     */
    async checkProgress() {
        if (!this.sessionId) {
            console.error('❌ Session ID não disponível');
            return;
        }
        
        console.log('📊 Verificando progresso da sessão:', this.sessionId);
        
        try {
            // Use fetchWithRetry for monitoring
            const response = await this.fetchWithRetry(`${this.apiBaseUrl}/progress/${this.sessionId}`, {
                method: 'GET',
                headers: {
                    'Accept': 'application/json'
                }
            });
            
            const progressData = await response.json();
            
            if (!progressData.success) {
                throw new Error(progressData.message || 'Erro ao obter progresso');
            }
            
            this.updateProgress(progressData.data);
            
        } catch (error) {
            console.error('❌ Erro ao verificar progresso:', error);
            throw error;
        }
    }
    
    /**
     * Update progress in modal
     */
    updateProgress(progressData) {
        console.log('📊 Atualizando progresso:', progressData);
        
        const {
            current_progress: currentProgress,
            current_stage: currentStage,
            status,
            current_phase: currentPhase,
            initial_estimate,
            final_calculation,
            phases_completed: phasesCompleted
        } = progressData;
        
        // Update progress bar
        if (currentProgress !== undefined && this.progressFill && this.progressText) {
            this.progressFill.style.width = `${currentProgress}%`;
            this.progressText.textContent = `${Math.round(currentProgress)}%`;
        }
        
        // Update current phase
        if (currentPhase && this.currentPhase) {
            const phaseIndex = this.rpaPhases.findIndex(phase => 
                phase.includes(currentPhase) || phase.includes(currentStage)
            );
            
            const currentPhaseElement = this.currentPhase.querySelector('span');
            if (currentPhaseElement) {
                currentPhaseElement.textContent = `${currentPhase}` || 'Processando...';
            }
        }
        
        // Update phases list
        this.updatePhasesList(phasesCompleted);
        
        // Update estimates
        this.updateEstimates(initial_estimate, final_calculation);
        
        // Check if completed
        if (status === 'completed') {
            this.completeProcessing(progressData);
        } else if (status === 'failed' || status === 'error') {
            this.handleProcessingError(progressData);
        }
    }
    
    /**
     * Update phases list visual state
     */
    updatePhasesList(phasesCompleted) {
        if (!phasesCompleted) return;
        
        this.rpaPhases.forEach((phase, index) => {
            const phaseElement = document.getElementById(`phase-${index}`);
            if (!phaseElement) return;
            
            if (index < phasesCompleted) {
                phaseElement.className = 'phase-item completed';
                phaseElement.querySelector('i').className = 'fas fa-check-circle';
            } else if (index === phasesCompleted) {
                phaseElement.className = 'phase-item active';
                phaseElement.querySelector('i').className = 'fas fa-spinner fa-spin';
            } else {
                phaseElement.className = 'phase-item pending';
                phaseElement.querySelector('i').className = 'fas fa-clock';
            }
        });
    }
    
    /**
     * Update estimates in modal
     */
    updateEstimates(initialEstimate, finalCalculation) {
        if (initialEstimate && this.initialEstimate) {
            this.initialEstimate.textContent = `R$ ${initialEstimate}`;
            this.showResultsSection();
        }
        
        if (finalCalculation && this.finalCalculation) {
            this.finalCalculation.textContent = `R$ ${finalCalculation}`;
            this.showResultsSection();
        }
    }
    
    /**
     * Show results section
     */
    showResultsSection() {
        if (this.resultsSection) {
            this.resultsSection.style.display = 'grid';
        }
    }
    
    /**
     * Complete processing
     */
    completeProcessing(progressData) {
        console.log('✅ Processamento concluído com sucesso');
        
        this.stopProgressMonitoring();
        
        // Update progress bar to 100%
        if (this.progressFill && this.progressText) {
            this.progressFill.style.width = '100%';
            this.progressText.textContent = '100%';
        }
        
        // Enable close button
        if (this.closeBtn) {
            this.closeBtn.disabled = false;
            this.closeBtn.innerHTML = '<i class="fas fa-check"></i> Concluído';
        }
        
        this.isProcessing = false;
        this.updateUI(false);
        
        // Fire completion event
        this.dispatchEvent('rpaConcluido', {
            sessionId: this.sessionId,
            progressData: progressData
        });
        
        console.log('🎉 Processo RPA finalizado com sucesso');
    }
    
    /**
     * Handle processing error
     */
    handleProcessingError(progressData) {
        console.error('❌ Erro no processamento RPA');
        
        this.stopProgressMonitoring();
        
        // Show error in modal
        const errorMessage = progressData.error || 'Erro durante execução do RPA';
        
        if (this.currentPhase) {
            const currentPhaseElement = this.currentPhase.querySelector('span');
            if (currentPhaseElement) {
                currentPhaseElement.innerHTML = `<i class="fas fa-exclamation-triangle"></i> ${errorMessage}`;
            }
        }
        
        // Enable close button
        if (this.closeBtn) {
            this.closeBtn.disabled = false;
            this.closeBtn.innerHTML = '<i class="fas fa-times"></i> Fechar';
        }
        
        this.isProcessing = false;
        this.updateUI(false);
        
        this.showError('Erro no Processamento', errorMessage);
    }
    
    /**
     * Handle monitoring error
     */
    handleMonitoringError(error) {
        console.error('❌ Erro no monitoramento:', error);
        
        // Try to continue for a bit longer
        setTimeout(() => {
            this.stopProgressMonitoring();
            
            if (this.closeBtn) {
                this.closeBtn.disabled = false;
                this.closeBtn.innerHTML = '<i class="fas fa-exclamation-triangle"></i> Erro na Conexão';
            }
            
            this.isProcessing = false;
            this.updateUI(false);
            
            this.showError('Erro de Conexão', 'Erro ao monitorar progresso. Tente novamente.');
        }, 10000); // Wait 10 seconds before giving up
    }
    
    /**
     * Stop progress monitoring
     */
    stopProgressMonitoring() {
        if (this.progressInterval) {
            clearInterval(this.progressInterval);
            this.progressInterval = null;
            console.log('🛑 Monitoramento de progresso interrompido');
        }
    }
    
    /**
     * Show error modal
     */
    showError(titulo, mensagem, detalhes = null) {
        // Stop progress monitoring
        this.stopProgressMonitoring();
        
        // Prepare detailed message
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
                // Try again
                this.retryLastOperation();
            } else {
                this.isProcessing = false;
                this.updateUI(false);
            }
        });
    }
    
    /**
     * Retry last operation
     */
    retryLastOperation() {
        console.log('🔄 Tentando novamente a última operação...');
        
        if (this.sessionId) {
            // If we have a session, continue monitoring
            this.startProgressMonitoring();
        } else {
            // Try to restart the form submission
            if (!this.isProcessing) {
                console.log('🔄 Reiniciando submissão do formulário...');
                document.getElementById('rpa-form').dispatchEvent(new Event('submit'));
            }
        }
    }
    
    /**
     * Update UI state
     */
    updateUI(loading) {
        const form = document.getElementById('rpa-form');
        const btnCalculate = document.getElementById('btnCalculate');
        const statusIndicator = document.getElementById('statusIndicator');
        
        if (loading) {
            form.classList.add('loading');
            btnCalculate.disabled = true;
            btnCalculate.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processando...';
            if (statusIndicator) statusIndicator.style.display = 'inline-flex';
        } else {
            form.classList.remove('loading');
            btnCalculate.disabled = false;
            btnCalculate.innerHTML = '<i class="fas fa-calculator"></i> Calcular Seguro';
            if (statusIndicator) statusIndicator.style.display = 'none';
        }
    }
    
    /**
     * Dispatch custom event
     */
    dispatchEvent(eventName, data) {
        const event = new CustomEvent(eventName, { detail: data });
        document.dispatchEvent(event);
        
        console.log(`📡 Evento disparado: ${eventName}`, data);
    }
    
    /**
     * Fetch with retry and exponential backoff
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
                
                throw new Error(`HTTP ${response.status}: ${response.statusText} - URL: ${url}`);
            } catch (error) {
                console.warn(`⚠️ Tentativa ${i + 1} falhou:`, error.message);
                
                if (i === maxRetries - 1) {
                    throw new Error(`Falha após ${maxRetries} tentativas: ${error.message}`);
                }
                
                // Exponential backoff: 1s, 2s, 4s, 8s...
                const delay = Math.pow(2, i) * 1000;
                console.log(`⏳ Aguardando ${delay}ms antes da próxima tentativa...`);
                await new Promise(resolve => setTimeout(resolve, delay));
            }
        }
    }
    
    /**
     * Clean up resources
     */
    destroy() {
        this.stopProgressMonitoring();
        
        // Remove event listeners
        document.removeEventListener('rpaConcluido', this.handleRPAConcluido);
        
        // Reset state
        this.sessionId = null;
        this.isProcessing = false;
        
        console.log('🧹 Modal RPA Real destruído');
    }
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', () => {
    window.modalRPALreal = new ModalRPAReal();
    console.log('🚀 Modal RPA Real carregado na página');
});

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ModalRPAReal;
}
