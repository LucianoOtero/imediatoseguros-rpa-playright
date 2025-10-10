// RPA Integration v6.9.0 - Webflow Integration (Simplificado)
// Arquivo: rpa-integration-v6.9.0.js
// Data: 2025-10-09
// Descrição: JavaScript simplificado para integração RPA (GCLID já capturado automaticamente)

const RPAIntegration = {
    // Configurações
    config: {
        apiBaseUrl: 'https://rpaimediatoseguros.com.br',
        webhookUrls: {
            rpaStart: 'https://rpaimediatoseguros.com.br/api/rpa/start',
            rpaProgress: 'https://rpaimediatoseguros.com.br/api/rpa/progress'
        },
        pollingInterval: 2000, // 2 segundos
        maxPolls: 90, // 3 minutos (180 segundos)
        timeoutMessage: 'O cálculo está demorando mais que o esperado. Tente novamente em alguns minutos.'
    },
    
    // Coletar dados do formulário (GCLID já preenchido automaticamente)
    collectFormData() {
        const form = document.getElementById('cotacaoForm');
        if (!form) {
            throw new Error('Formulário de cotação não encontrado');
        }
        
        const formData = new FormData(form);
        const data = {};
        
        // Coletar todos os campos do formulário (incluindo GCLID_FLD já preenchido)
        for (let [key, value] of formData.entries()) {
            data[key] = value;
        }
        
        // Validar campos obrigatórios
        const requiredFields = ['cpf', 'nome', 'placa', 'cep', 'email', 'telefone'];
        const missingFields = requiredFields.filter(field => !data[field]);
        
        if (missingFields.length > 0) {
            throw new Error(`Campos obrigatórios não preenchidos: ${missingFields.join(', ')}`);
        }
        
        return data;
    },
    
    // Iniciar RPA
    async startRPA(formData) {
        try {
            const response = await fetch(this.config.webhookUrls.rpaStart, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });
            
            const data = await response.json();
            if (!data.success) {
                throw new Error(data.message || 'Erro ao iniciar RPA');
            }
            
            return data.session_id;
        } catch (error) {
            console.error('Erro ao iniciar RPA:', error);
            throw error;
        }
    },
    
    // Monitorar progresso
    async getProgress(sessionId) {
        try {
            const response = await fetch(`${this.config.webhookUrls.rpaProgress}/${sessionId}`);
            const data = await response.json();
            
            if (!data.success) {
                throw new Error(data.message || 'Erro ao obter progresso');
            }
            
            return data.progress;
        } catch (error) {
            console.error('Erro ao obter progresso:', error);
            throw error;
        }
    },
    
    // Função principal de execução
    async execute() {
        try {
            // 1. Coletar dados do formulário (GCLID já incluído)
            const formData = this.collectFormData();
            console.log('Dados coletados:', formData);
            
            // 2. Abrir modal de progresso
            this.openProgressModal();
            
            // 3. Iniciar RPA
            const sessionId = await this.startRPA(formData);
            console.log('Sessão RPA criada:', sessionId);
            
            // 4. Monitorar progresso
            let pollCount = 0;
            const progressInterval = setInterval(async () => {
                try {
                    pollCount++;
                    const progress = await this.getProgress(sessionId);
                    
                    // Atualizar interface
                    this.updateProgressUI(progress);
                    
                    // Verificar conclusão
                    if (progress.status === 'success') {
                        clearInterval(progressInterval);
                        this.showResults(progress.resultados_finais);
                        return;
                    }
                    
                    // Verificar timeout
                    if (pollCount >= this.config.maxPolls) {
                        clearInterval(progressInterval);
                        this.showTimeout();
                    }
                    
                } catch (error) {
                    clearInterval(progressInterval);
                    this.showError('Erro no monitoramento: ' + error.message);
                }
            }, this.config.pollingInterval);
            
        } catch (error) {
            console.error('Erro na execução:', error);
            this.showError('Erro ao iniciar cálculo: ' + error.message);
        }
    },
    
    // Métodos de interface (implementar conforme necessário)
    openProgressModal() {
        console.log('Abrindo modal de progresso...');
        // Implementar modal de progresso
    },
    
    updateProgressUI(progress) {
        console.log('Atualizando progresso:', progress);
        // Implementar atualização da interface
    },
    
    showResults(results) {
        console.log('Exibindo resultados:', results);
        // Implementar exibição de resultados
    },
    
    showError(message) {
        console.error('Erro:', message);
        alert('Erro: ' + message);
    },
    
    showTimeout() {
        console.warn('Timeout atingido');
        alert(this.config.timeoutMessage);
    }
};

// Event listener para o formulário
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('cotacaoForm');
    if (form) {
        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            await RPAIntegration.execute();
        });
    }
});

// Teste para verificar se GCLID está sendo capturado automaticamente
function testarGCLIDExistente() {
    console.log('🔍 Testando captura automática de GCLID...');
    
    // Verificar campo GCLID_FLD (preenchido automaticamente)
    var gclidField = document.getElementById('GCLID_FLD');
    if (gclidField) {
        console.log('✅ Campo GCLID_FLD encontrado:', gclidField.value);
        
        // Verificar se está preenchido automaticamente
        if (gclidField.value) {
            console.log('✅ GCLID capturado automaticamente:', gclidField.value);
        } else {
            console.log('⚠️ Campo GCLID_FLD vazio - aguardando captura...');
        }
    } else {
        console.error('❌ Campo GCLID_FLD não encontrado!');
    }
    
    // Verificar cookie do GCLID
    var gclidCookie = (document.cookie.match(/(^|;)\s*gclid=([^;]+)/) || [])[2];
    if (gclidCookie) {
        console.log('✅ GCLID salvo em cookie:', decodeURIComponent(gclidCookie));
    } else {
        console.log('⚠️ GCLID não encontrado em cookie');
    }
    
    // Verificar localStorage
    var gclidLocalStorage = window.localStorage.getItem('GCLID_FLD');
    if (gclidLocalStorage) {
        console.log('✅ GCLID salvo no localStorage:', gclidLocalStorage);
    } else {
        console.log('⚠️ GCLID não encontrado no localStorage');
    }
}

// Executar teste quando página carregar
document.addEventListener('DOMContentLoaded', function() {
    setTimeout(testarGCLIDExistente, 1000); // Aguardar 1 segundo
});


