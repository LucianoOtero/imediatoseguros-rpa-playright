/**
 * Modal de Progresso RPA - Imediato Seguros V6.3.0
 * Versão simplificada sem estimativas iniciais
 */

class ProgressModalRPA {
    constructor(sessionId = null) {
        this.sessionId = sessionId;
        this.isProcessing = false;
        this.pollingInterval = null;
        this.pollingIntervalMs = 2000; // 2 segundos
        
        // Mensagens das fases (16 fases)
        this.phaseMessages = {
            1: "🚀 Iniciando sistema RPA...",
            2: "📋 Coletando dados do formulário...",
            3: "🔍 Validando informações...",
            4: "🌐 Conectando com seguradoras...",
            5: "📊 Processando dados...",
            6: "⚙️ Calculando coberturas...",
            7: "📈 Analisando riscos...",
            8: "💼 Consultando tabelas...",
            9: "🔢 Aplicando fórmulas...",
            10: "📋 Gerando propostas...",
            11: "🎯 Otimizando valores...",
            12: "📊 Comparando opções...",
            13: "✅ Validando resultados...",
            14: "📋 Finalizando cálculos...",
            15: "⚙️ Finalizando processamento...",
            16: "🎉 Cálculo finalizado"
        };
        
        // Submensagens das fases
        this.phaseSubMessages = {
            1: "Preparando ambiente de cálculo",
            2: "Verificando dados obrigatórios",
            3: "Confirmando informações",
            4: "Estabelecendo conexões",
            5: "Processando informações",
            6: "Calculando valores",
            7: "Avaliando perfil de risco",
            8: "Consultando bases de dados",
            9: "Aplicando cálculos",
            10: "Gerando propostas",
            11: "Otimizando custos",
            12: "Comparando alternativas",
            13: "Validando resultados",
            14: "Preparando finalização",
            15: "",
            16: ""
        };
        
        console.log('🚀 ProgressModalRPA V6.3.0 inicializado');
        console.log('📋 Modal simplificado - apenas resultados finais');
    }
    
    /**
     * Definir Session ID
     */
    setSessionId(sessionId) {
        this.sessionId = sessionId;
        console.log('🆔 Session ID definido:', sessionId);
    }
    
    /**
     * Iniciar polling de progresso
     */
    startProgressPolling() {
        if (!this.sessionId) {
            console.error('❌ Session ID não encontrado');
            return;
        }
        
        console.log('🔄 Iniciando polling de progresso...');
        this.isProcessing = true;
        
        // Primeira verificação imediata
        this.checkProgress();
        
        // Polling contínuo
        this.pollingInterval = setInterval(() => {
            this.checkProgress();
        }, this.pollingIntervalMs);
    }
    
    /**
     * Parar polling de progresso
     */
    stopProgressPolling() {
        if (this.pollingInterval) {
            clearInterval(this.pollingInterval);
            this.pollingInterval = null;
        }
        this.isProcessing = false;
        console.log('⏹️ Polling de progresso parado');
    }
    
    /**
     * Verificar progresso do RPA
     */
    async checkProgress() {
        if (!this.sessionId) {
            console.error('❌ Session ID não encontrado');
            return;
        }
        
        try {
            const response = await fetch(`https://rpaimediatoseguros.com.br/api/rpa/progress/${this.sessionId}`);
            const data = await response.json();
            
            if (data.success) {
                this.updateProgress(data);
            } else {
                console.error('❌ Erro na API:', data.message);
                this.handleProgressError(data.message || 'Erro desconhecido');
            }
        } catch (error) {
            console.error('❌ Erro ao verificar progresso:', error);
            this.handleProgressError('Erro de conexão');
        }
    }
    
    /**
     * Atualizar progresso na interface
     */
    updateProgress(data) {
        const { progress } = data;
        const progressData = progress?.progress || progress;
        
        if (!progressData) {
            console.error('❌ Dados de progresso não encontrados');
            return;
        }
        
        const currentStatus = progressData.current_status || progressData.status;
        const currentPhase = progressData.current_etapa || progressData.etapa || 0;
        const currentMessage = progressData.current_mensagem || progressData.mensagem || '';
        
        // Calcular percentual
        let percentual = progressData.percentual || (currentPhase / 16) * 100;
        percentual = Math.min(100, Math.max(0, percentual));
        
        if (percentual > 100) {
            console.warn(`⚠️ Percentual excedeu 100%: ${percentual}%`);
            percentual = 100;
        }
        
        // Se concluído, garantir 100%
        if (currentStatus === 'success' || currentStatus === 'completed') {
            percentual = 100;
        }
        
        console.log(`📊 Fase ${currentPhase}: ${currentMessage} (${percentual.toFixed(1)}%)`);
        
        // Atualizar elementos da interface
        this.updateProgressBar(percentual, currentPhase);
        this.updatePhaseInfo(currentPhase, currentMessage);
        
        // Verificar se concluído
        if (currentStatus === 'success' || currentStatus === 'completed') {
            console.log('✅ RPA concluído com sucesso');
            this.handleRPASuccess(data);
            return;
        }
        
        // Verificar se falhou
        if (currentStatus === 'failed' || currentStatus === 'error' || currentStatus === 'erro') {
            console.log('❌ RPA falhou:', currentMessage);
            this.handleProgressError(currentMessage || 'Erro desconhecido');
            return;
        }
    }
    
    /**
     * Handle RPA success
     */
    handleRPASuccess(data) {
        this.stopProgressPolling();
        this.isProcessing = false;
        
        // Atualizar header para sucesso
        this.updateSuccessHeader();
        
        // Atualizar resultados
        this.updateResults(data);
        
        console.log('🎉 RPA concluído com sucesso!');
    }
    
    /**
     * Handle progress error
     */
    handleProgressError(message) {
        this.stopProgressPolling();
        this.isProcessing = false;
        this.updateErrorHeader(message);
        console.error('❌ Erro no RPA:', message);
    }
    
    /**
     * Atualizar barra de progresso
     */
    updateProgressBar(percentual, currentPhase) {
        const progressFill = document.getElementById('progressFill');
        const progressGlow = document.getElementById('progressGlow');
        const progressText = document.getElementById('progressText');
        
        if (progressFill) {
            progressFill.style.width = `${percentual}%`;
        }
        
        if (progressGlow) {
            progressGlow.style.width = `${percentual}%`;
        }
        
        if (progressText) {
            progressText.textContent = `${Math.round(percentual)}%`;
        }
    }
    
    /**
     * Atualizar informações da fase
     */
    updatePhaseInfo(currentPhase, currentMessage) {
        const currentPhaseElement = document.getElementById('currentPhase');
        const stageInfoElement = document.getElementById('stageInfo');
        const subPhaseElement = document.getElementById('subPhase');
        
        if (currentPhaseElement) {
            const message = this.getPhaseMessage(currentPhase);
            currentPhaseElement.textContent = message;
        }
        
        if (stageInfoElement) {
            stageInfoElement.textContent = `Fase ${currentPhase} de 16`;
        }
        
        if (subPhaseElement) {
            const subMessage = this.getPhaseSubMessage(currentPhase);
            subPhaseElement.textContent = subMessage;
        }
    }
    
    /**
     * Obter mensagem da fase
     */
    getPhaseMessage(phaseNumber) {
        return this.phaseMessages[phaseNumber] || `Fase ${phaseNumber}`;
    }
    
    /**
     * Obter submensagem da fase
     */
    getPhaseSubMessage(phaseNumber) {
        return this.phaseSubMessages[phaseNumber] || '';
    }
    
    /**
     * Atualizar header para sucesso
     */
    updateSuccessHeader() {
        const resultsHeader = document.querySelector('.results-header');
        if (resultsHeader) {
            resultsHeader.innerHTML = `
                <h2><i class="fas fa-check-circle"></i> Seu seguro foi calculado com sucesso!</h2>
                <p class="contact-message"><i class="fas fa-phone"></i> Um especialista da Imediato Seguros entrará em contato em instantes para passar os detalhes!</p>
            `;
            resultsHeader.style.background = 'linear-gradient(135deg, #28a745, #20c997)';
        }
    }
    
    /**
     * Atualizar header para erro
     */
    updateErrorHeader(message) {
        const resultsHeader = document.querySelector('.results-header');
        if (resultsHeader) {
            resultsHeader.innerHTML = `
                <h2><i class="fas fa-exclamation-triangle"></i> Erro no Cálculo</h2>
                <p>${message}</p>
            `;
            resultsHeader.style.background = 'linear-gradient(135deg, #dc3545, #fd7e14)';
        }
    }
    
    /**
     * Atualizar resultados finais
     */
    updateResults(data) {
        const { progress } = data;
        const progressData = progress?.progress || progress;
        
        if (!progressData) {
            console.error('❌ Dados de progresso não encontrados para resultados');
            return;
        }
        
        // Extrair dados dos resultados finais
        const resultadosFinais = progressData.resultados_finais?.dados?.dados_finais;
        
        if (!resultadosFinais) {
            console.error('❌ Resultados finais não encontrados');
            return;
        }
        
        console.log('📊 Resultados finais encontrados:', resultadosFinais);
        
        // Atualizar plano recomendado
        const planoRecomendado = resultadosFinais.plano_recomendado;
        if (planoRecomendado) {
            const recommendedValueElement = document.getElementById('recommendedValue');
            if (recommendedValueElement) {
                const valorFormatado = this.formatCurrency(planoRecomendado.valor_total);
                recommendedValueElement.textContent = valorFormatado;
                console.log('✅ Plano recomendado atualizado:', valorFormatado);
            }
        }
        
        // Atualizar plano alternativo
        const planoAlternativo = resultadosFinais.plano_alternativo;
        if (planoAlternativo) {
            const alternativeValueElement = document.getElementById('alternativeValue');
            if (alternativeValueElement) {
                const valorFormatado = this.formatCurrency(planoAlternativo.valor_total);
                alternativeValueElement.textContent = valorFormatado;
                console.log('✅ Plano alternativo atualizado:', valorFormatado);
            }
        }
        
        console.log('🎉 Resultados finais atualizados com sucesso!');
    }
    
    /**
     * Formatar valor como moeda brasileira
     */
    formatCurrency(value) {
        if (!value) return 'R$ 0,00';
        
        // Converter para string se necessário
        let valueStr = String(value);
        
        // Remover caracteres não numéricos exceto vírgula e ponto
        valueStr = valueStr.replace(/[^\d,.-]/g, '');
        
        // Converter vírgula para ponto para parsing
        valueStr = valueStr.replace(',', '.');
        
        // Converter para número
        let numericValue = parseFloat(valueStr);
        
        if (isNaN(numericValue)) {
            console.warn('⚠️ Valor não numérico:', value);
            return 'R$ 0,00';
        }
        
        // Detectar e corrigir valores divididos por 1000
        if (numericValue >= 0.1 && numericValue <= 100) {
            console.log(`🔧 Valor pequeno detectado (${numericValue}), multiplicando por 1000`);
            numericValue = numericValue * 1000;
        }
        
        // Formatar como moeda brasileira
        const formatted = numericValue.toLocaleString('pt-BR', {
            style: 'currency',
            currency: 'BRL'
        });
        
        console.log(`💰 Valor formatado: ${value} → ${formatted}`);
        return formatted;
    }
}

// Exportar para uso global
window.ProgressModalRPA = ProgressModalRPA;
