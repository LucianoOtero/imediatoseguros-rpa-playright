/**
 * INTEGRAÇÃO RPA V6.2.0 - IMEDIATO SEGUROS
 * JavaScript para integração completa com RPA
 * 
 * Funcionalidades:
 * - Integração com API RPA V4
 * - Polling de progresso
 * - Tratamento de erros
 * - Comunicação entre componentes
 */

class RPAIntegration {
    constructor() {
        this.apiBaseUrl = 'http://rpaimediatoseguros.com.br';
        this.sessionId = null;
        this.isProcessing = false;
        
        console.log('🔧 RPA Integration inicializado');
    }
    
    /**
     * Iniciar RPA com dados completos
     */
    async startRPA(completeData) {
        try {
            this.isProcessing = true;
            
            console.log('🚀 Iniciando RPA...');
            
            // Chamar API para iniciar RPA
            const response = await this.callRPAAPI(completeData);
            
            if (response.success) {
                this.sessionId = response.session_id;
                console.log('✅ RPA iniciado com sucesso. Session ID:', this.sessionId);
                
                return {
                    success: true,
                    sessionId: this.sessionId
                };
            } else {
                throw new Error(response.message || 'Erro ao iniciar RPA');
            }
            
        } catch (error) {
            console.error('❌ Erro ao iniciar RPA:', error);
            this.isProcessing = false;
            
            return {
                success: false,
                error: error.message
            };
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
     * Verificar progresso do RPA
     */
    async checkProgress(sessionId) {
        const url = `${this.apiBaseUrl}/api/rpa/progress/${sessionId}`;
        
        try {
            const response = await fetch(url);
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            
            const progressData = await response.json();
            console.log('📊 Progresso recebido:', progressData);
            
            return {
                success: true,
                data: progressData
            };
            
        } catch (error) {
            console.error('❌ Erro ao verificar progresso:', error);
            return {
                success: false,
                error: error.message
            };
        }
    }
    
    /**
     * Gerar ID de sessão único
     */
    generateSessionId() {
        return 'rpa_v4_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }
    
    /**
     * Verificar saúde da API
     */
    async checkAPIHealth() {
        const url = `${this.apiBaseUrl}/api/rpa/health`;
        
        try {
            const response = await fetch(url);
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            
            const healthData = await response.json();
            console.log('🏥 API Health:', healthData);
            
            return {
                success: true,
                data: healthData
            };
            
        } catch (error) {
            console.error('❌ Erro ao verificar saúde da API:', error);
            return {
                success: false,
                error: error.message
            };
        }
    }
    
    /**
     * Processar dados de progresso
     */
    processProgressData(data) {
        const { status, progress, current_phase, mensagem } = data;
        
        // Extrair dados do progresso
        const progressData = progress || {};
        const currentStatus = progressData.status || status;
        const currentMessage = progressData.mensagem || mensagem;
        const currentPhase = progressData.etapa_atual || current_phase;
        const percentual = progressData.percentual || 0;
        
        return {
            status: currentStatus,
            message: currentMessage,
            phase: currentPhase,
            percentage: percentual,
            progressData: progressData
        };
    }
    
    /**
     * Extrair dados de resultados
     */
    extractResultsData(progressData) {
        const estimativas = progressData?.estimativas?.dados;
        const resultadosFinais = progressData?.resultados_finais?.dados?.dados_finais;
        
        let initialEstimate = null;
        let recommendedValue = null;
        let alternativeValue = null;
        
        // Estimativa inicial (primeira cobertura)
        if (estimativas?.coberturas_detalhadas?.[0]) {
            const primeiraCobertura = estimativas.coberturas_detalhadas[0];
            initialEstimate = primeiraCobertura.valores?.de || primeiraCobertura.valores?.ate;
        }
        
        // Cálculo recomendado
        if (resultadosFinais?.plano_recomendado?.valor) {
            recommendedValue = resultadosFinais.plano_recomendado.valor;
        }
        
        // Cálculo alternativo
        if (resultadosFinais?.plano_alternativo?.valor) {
            alternativeValue = resultadosFinais.plano_alternativo.valor;
        }
        
        return {
            initialEstimate,
            recommendedValue,
            alternativeValue,
            estimativas,
            resultadosFinais
        };
    }
    
    /**
     * Verificar se RPA foi concluído
     */
    isRPACompleted(processedData) {
        const { status, message } = processedData;
        
        // Verificar se concluído
        if (status === 'success' || status === 'completed') {
            return true;
        }
        
        // Verificar se falhou
        if (status === 'failed' || status === 'error' || status === 'erro') {
            return true;
        }
        
        // Verificar se houve falha na mensagem
        if (message && message.includes('falhou')) {
            return true;
        }
        
        return false;
    }
    
    /**
     * Verificar se RPA teve sucesso
     */
    isRPASuccessful(processedData) {
        const { status, message } = processedData;
        
        // Verificar se concluído com sucesso
        if (status === 'success' || status === 'completed') {
            return true;
        }
        
        // Verificar se houve falha
        if (status === 'failed' || status === 'error' || status === 'erro') {
            return false;
        }
        
        // Verificar se houve falha na mensagem
        if (message && message.includes('falhou')) {
            return false;
        }
        
        return false;
    }
    
    /**
     * Formatar valor monetário
     */
    formatCurrency(value) {
        if (!value) return '-';
        
        // Se já está formatado (contém R$), retornar como está
        if (typeof value === 'string' && value.includes('R$')) {
            return value;
        }
        
        const numValue = parseFloat(value);
        if (isNaN(numValue)) return '-';
        
        return numValue.toLocaleString('pt-BR', {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        });
    }
    
    /**
     * Limpar recursos
     */
    cleanup() {
        this.sessionId = null;
        this.isProcessing = false;
        
        console.log('🧹 Recursos limpos');
    }
}

// Exportar classe para uso global
window.RPAIntegration = RPAIntegration;



