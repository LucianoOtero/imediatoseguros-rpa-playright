/**
 * MODAL PROGRESSO RPA - INTEGRAÇÃO WEBFLOW
 * 
 * Este arquivo contém a implementação JavaScript para integração
 * do modal de progresso RPA com o website segurosimediato.com.br
 * 
 * Dependências:
 * - SweetAlert2 (https://sweetalert2.github.io/)
 * - Titillium Web Font (Google Fonts)
 * - Font Awesome (ícones)
 */

class RPAProgressModal {
    constructor() {
        this.sessionId = null;
        this.progressInterval = null;
        this.isModalOpen = false;
        this.currentProgress = 0;
        this.estimativaInicial = null;
        this.valorFinal = null;
        
        // Configurações do modal
        this.config = {
            apiBaseUrl: 'https://37.27.92.160/api/rpa',
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
     * Inicia uma nova sessão RPA e abre o modal de progresso
     * @param {Object} dados - Dados do formulário (cpf, nome, placa, cep, email, telefone)
     * @returns {Promise} - Promise que resolve com o sessionId
     */
    async iniciarSessao(dados) {
        try {
            // Validar dados obrigatórios
            this.validarDados(dados);
            
            // Criar sessão via API
            const response = await fetch(`${this.config.apiBaseUrl}/start`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(dados)
            });
            
            if (!response.ok) {
                throw new Error(`Erro HTTP: ${response.status}`);
            }
            
            const result = await response.json();
            
            if (!result.success) {
                throw new Error(result.message || 'Erro ao criar sessão');
            }
            
            this.sessionId = result.session_id;
            
            // Abrir modal de progresso
            this.abrirModal();
            
            // Iniciar monitoramento
            this.iniciarMonitoramento();
            
            return this.sessionId;
            
        } catch (error) {
            console.error('Erro ao iniciar sessão RPA:', error);
            this.mostrarErro('Erro ao iniciar processamento', error.message);
            throw error;
        }
    }

    /**
     * Valida os dados obrigatórios
     * @param {Object} dados - Dados a serem validados
     */
    validarDados(dados) {
        const camposObrigatorios = ['cpf', 'nome', 'placa', 'cep'];
        const camposFaltando = camposObrigatorios.filter(campo => !dados[campo]);
        
        if (camposFaltando.length > 0) {
            throw new Error(`Campos obrigatórios faltando: ${camposFaltando.join(', ')}`);
        }
    }

    /**
     * Abre o modal de progresso usando SweetAlert2
     */
    abrirModal() {
        if (this.isModalOpen) return;
        
        this.isModalOpen = true;
        
        Swal.fire({
            title: '<div style="font-family: \'Titillium Web\', sans-serif; font-size: 24px; font-weight: 600; color: #2c3e50;"><i class="fas fa-cogs" style="color: #3498db; margin-right: 10px;"></i>Processando Cotação</div>',
            html: this.gerarHTMLModal(),
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
                this.configurarEventListeners();
            },
            willClose: () => {
                this.isModalOpen = false;
                this.pararMonitoramento();
            }
        });
    }

    /**
     * Gera o HTML do modal
     * @returns {string} - HTML do modal
     */
    gerarHTMLModal() {
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
                }
            </style>
        `;
    }

    /**
     * Configura os event listeners do modal
     */
    configurarEventListeners() {
        const closeButton = document.getElementById('closeButton');
        if (closeButton) {
            closeButton.addEventListener('click', () => {
                this.fecharModal();
            });
        }
    }

    /**
     * Inicia o monitoramento do progresso via API
     */
    iniciarMonitoramento() {
        if (this.progressInterval) {
            clearInterval(this.progressInterval);
        }
        
        let pollCount = 0;
        const maxPolls = this.config.maxPollTime / this.config.pollInterval;
        
        this.progressInterval = setInterval(async () => {
            try {
                pollCount++;
                
                if (pollCount > maxPolls) {
                    this.mostrarErro('Timeout', 'Tempo limite de processamento excedido');
                    return;
                }
                
                const response = await fetch(`${this.config.apiBaseUrl}/progress/${this.sessionId}`);
                
                if (!response.ok) {
                    throw new Error(`Erro HTTP: ${response.status}`);
                }
                
                const data = await response.json();
                
                if (data.success) {
                    this.atualizarProgresso(data.progress);
                    
                    // Verificar se concluído
                    if (data.progress && data.progress.status === 'success') {
                        this.concluirProcessamento(data.progress);
                    }
                } else {
                    throw new Error(data.message || 'Erro ao obter progresso');
                }
                
            } catch (error) {
                console.error('Erro ao monitorar progresso:', error);
                this.mostrarErro('Erro de Monitoramento', error.message);
            }
        }, this.config.pollInterval);
    }

    /**
     * Atualiza o progresso do modal
     * @param {Object} progressData - Dados de progresso da API
     */
    atualizarProgresso(progressData) {
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
        this.atualizarFaseAtual(progress);
        
        // Atualizar estimativas iniciais
        if (progressData.estimativas && progressData.estimativas.capturadas) {
            this.atualizarEstimativaInicial(progressData.estimativas.dados);
        }
        
        // Atualizar resultados finais
        if (progressData.resultados_finais && progressData.resultados_finais.rpa_finalizado) {
            this.atualizarValorFinal(progressData.resultados_finais.dados);
        }
    }

    /**
     * Atualiza a fase atual baseada no progresso
     * @param {number} progress - Percentual de progresso (0-100)
     */
    atualizarFaseAtual(progress) {
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
     * Atualiza a estimativa inicial
     * @param {Object} estimativas - Dados das estimativas
     */
    atualizarEstimativaInicial(estimativas) {
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
        }
    }

    /**
     * Atualiza o valor final
     * @param {Object} resultados - Dados dos resultados finais
     */
    atualizarValorFinal(resultados) {
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
        }
    }

    /**
     * Conclui o processamento e habilita o botão de fechar
     * @param {Object} progressData - Dados finais de progresso
     */
    concluirProcessamento(progressData) {
        this.pararMonitoramento();
        
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
        this.dispararEvento('rpaConcluido', {
            sessionId: this.sessionId,
            progressData: progressData
        });
    }

    /**
     * Para o monitoramento do progresso
     */
    pararMonitoramento() {
        if (this.progressInterval) {
            clearInterval(this.progressInterval);
            this.progressInterval = null;
        }
    }

    /**
     * Fecha o modal
     */
    fecharModal() {
        if (this.isModalOpen) {
            Swal.close();
            this.pararMonitoramento();
        }
    }

    /**
     * Mostra erro no modal
     * @param {string} titulo - Título do erro
     * @param {string} mensagem - Mensagem do erro
     */
    mostrarErro(titulo, mensagem) {
        this.pararMonitoramento();
        
        Swal.fire({
            icon: 'error',
            title: titulo,
            text: mensagem,
            confirmButtonText: 'Fechar',
            customClass: {
                popup: 'rpa-modal-popup',
                title: 'rpa-modal-title'
            }
        });
    }

    /**
     * Dispara evento customizado
     * @param {string} eventName - Nome do evento
     * @param {Object} data - Dados do evento
     */
    dispararEvento(eventName, data) {
        const event = new CustomEvent(eventName, {
            detail: data
        });
        document.dispatchEvent(event);
    }
}

// Instância global do modal
window.rpaModal = new RPAProgressModal();

// Event listeners globais
document.addEventListener('rpaConcluido', (event) => {
    console.log('RPA concluído:', event.detail);
    // Aqui você pode adicionar lógica adicional quando o RPA for concluído
});

// Exemplo de uso:
/*
// Iniciar sessão RPA
const dados = {
    cpf: '12345678901',
    nome: 'João Silva',
    placa: 'ABC1234',
    cep: '01234567',
    email: 'joao@email.com',
    telefone: '11999999999'
};

window.rpaModal.iniciarSessao(dados)
    .then(sessionId => {
        console.log('Sessão iniciada:', sessionId);
    })
    .catch(error => {
        console.error('Erro:', error);
    });
*/
