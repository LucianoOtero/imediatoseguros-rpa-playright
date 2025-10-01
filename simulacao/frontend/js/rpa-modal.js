/**
 * RPA Modal para Simulação - Imediato Seguros
 * Versão: 1.0.0
 */

(function() {
  'use strict';

  // Configurações
  const CONFIG = {
    apiUrl: 'http://37.27.92.160', // Backend Hetzner
    pollingInterval: 1500, // 1.5 segundos
    timeout: 30000, // 30 segundos
    sessionPrefix: 'seguro_webflow_'
  };

  // Classe principal do modal
  class RPAModal {
    constructor() {
      this.modal = null;
      this.isActive = false;
      this.sessionId = null;
      this.pollingInterval = null;
      this.init();
    }

    init() {
      this.modal = document.getElementById('rpa-modal');
      this.setupEventListeners();
    }

    // Configurar event listeners
    setupEventListeners() {
      // Fechar modal ao clicar no overlay
      this.modal.addEventListener('click', (e) => {
        if (e.target.classList.contains('rpa-modal-overlay')) {
          this.hide();
        }
      });

      // Fechar modal com ESC
      document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && this.isActive) {
          this.hide();
        }
      });
    }

    // Mostrar modal
    show(sessionId) {
      this.sessionId = sessionId;
      this.isActive = true;
      this.modal.style.display = 'flex';
      document.body.style.overflow = 'hidden';
      this.startPolling();
    }

    // Esconder modal
    hide() {
      this.isActive = false;
      this.modal.style.display = 'none';
      document.body.style.overflow = '';
      this.stopPolling();
    }

    // Iniciar polling
    startPolling() {
      if (this.pollingInterval) {
        clearInterval(this.pollingInterval);
      }

      this.pollingInterval = setInterval(() => {
        this.updateProgress();
      }, CONFIG.pollingInterval);
    }

    // Parar polling
    stopPolling() {
      if (this.pollingInterval) {
        clearInterval(this.pollingInterval);
        this.pollingInterval = null;
      }
    }

    // Atualizar progresso
    async updateProgress() {
      try {
        const response = await fetch(`${CONFIG.apiUrl}/get_progress.php?session=${this.sessionId}`);
        const data = await response.json();

        if (data.success) {
          // Adaptar formato do Hetzner para o modal
          const progress = data.data?.percentual || 0;
          const currentStep = data.data?.etapa_atual || 0;
          const totalSteps = data.data?.total_etapas || 15;
          
          this.updateProgressBar(progress);
          this.updateCurrentStep({
            icon: '🚗',
            title: `Tela ${currentStep} de ${totalSteps}`,
            description: data.data?.mensagem || 'Processando...',
            progress: progress,
            estimated_time: '--'
          });
          
          // Atualizar estimativas se disponíveis
          if (data.data?.dados_extra?.estimativas_tela_5) {
            this.updateEstimatesFromHetzner(data.data.dados_extra.estimativas_tela_5);
          }
          
          this.updateLastUpdate();

          // Verificar se concluído
          if (progress >= 100) {
            this.handleCompletion(data);
          }
        }
      } catch (error) {
        console.error('Erro ao atualizar progresso:', error);
      }
    }

    // Atualizar barra de progresso
    updateProgressBar(progress) {
      const progressFill = document.querySelector('.rpa-progress-fill');
      const progressPercentage = document.querySelector('.rpa-progress-percentage');
      const progressSteps = document.querySelector('.rpa-progress-steps');

      if (progressFill) {
        progressFill.style.width = `${progress}%`;
      }
      if (progressPercentage) {
        progressPercentage.textContent = `${progress}%`;
      }
      if (progressSteps) {
        const currentStep = Math.floor((progress / 100) * 15);
        progressSteps.textContent = `${currentStep} de 15 telas processadas`;
      }
    }

    // Atualizar etapa atual
    updateCurrentStep(stepData) {
      const stepIcon = document.querySelector('.rpa-step-icon');
      const stepTitle = document.querySelector('.rpa-step-info h4');
      const stepDescription = document.querySelector('.rpa-step-info small');
      const stepProgress = document.querySelector('.rpa-step-progress .rpa-progress-fill');
      const stepTime = document.querySelector('.rpa-step-time');

      if (stepIcon) stepIcon.textContent = stepData.icon || '🚗';
      if (stepTitle) stepTitle.textContent = stepData.title || 'Processando...';
      if (stepDescription) stepDescription.textContent = stepData.description || 'Aguarde...';
      if (stepProgress) stepProgress.style.width = `${stepData.progress || 0}%`;
      if (stepTime) stepTime.textContent = `⏱️ Tempo estimado: ${stepData.estimated_time || '--'}`;
    }

    // Atualizar estimativas
    updateEstimates(estimates) {
      if (!estimates) return;

      const estimateCards = document.querySelectorAll('.rpa-estimate-card');
      const estimateTypes = ['compreensiva', 'roubo_furto', 'rcf'];

      estimateTypes.forEach((type, index) => {
        const card = estimateCards[index];
        if (card && estimates[type]) {
          const valueElement = card.querySelector('.rpa-estimate-value');
          if (valueElement) {
            valueElement.textContent = estimates[type];
          }
        }
      });
    }

    // Atualizar estimativas do formato Hetzner
    updateEstimatesFromHetzner(estimativasData) {
      if (!estimativasData?.coberturas_detalhadas) return;

      const estimateCards = document.querySelectorAll('.rpa-estimate-card');
      
      // Mapear coberturas do Hetzner para os cards
      const coberturas = estimativasData.coberturas_detalhadas;
      
      coberturas.forEach((cobertura, index) => {
        if (index < estimateCards.length) {
          const card = estimateCards[index];
          const valueElement = card.querySelector('.rpa-estimate-value');
          
          if (valueElement && cobertura.valores) {
            const valor = `${cobertura.valores.de} - ${cobertura.valores.ate}`;
            valueElement.textContent = valor;
          }
        }
      });
    }

    // Atualizar timeline
    updateTimeline(timeline) {
      if (!timeline) return;

      const timelineContainer = document.getElementById('rpa-timeline');
      if (!timelineContainer) return;

      timelineContainer.innerHTML = timeline.map(step => `
        <div class="rpa-timeline-item ${step.status}">
          <div class="rpa-timeline-icon">${step.icon}</div>
          <div class="rpa-timeline-content">
            <h6>${step.title}</h6>
            <small>${step.description}</small>
          </div>
        </div>
      `).join('');
    }

    // Atualizar última atualização
    updateLastUpdate() {
      const lastUpdateElement = document.getElementById('rpa-last-update');
      if (lastUpdateElement) {
        lastUpdateElement.textContent = new Date().toLocaleTimeString();
      }
    }

    // Tratar conclusão
    handleCompletion(data) {
      this.stopPolling();
      
      // Mostrar resultado final
      setTimeout(() => {
        this.hide();
        this.showResults(data);
      }, 2000);
    }

    // Mostrar resultados
    showResults(result) {
      console.log('Resultado completo:', result);
      
      let message = 'RPA concluído com sucesso!\n\n';
      
      // Verificar diferentes estruturas de dados
      let coberturas = null;
      
      // Estrutura 1: dados_extra.estimativas_tela_5.coberturas_detalhadas
      if (result.data?.dados_extra?.estimativas_tela_5?.coberturas_detalhadas) {
        coberturas = result.data.dados_extra.estimativas_tela_5.coberturas_detalhadas;
        console.log('Estimativas encontradas (estrutura 1):', coberturas);
      }
      // Estrutura 2: dados_extra como array
      else if (Array.isArray(result.data?.dados_extra) && result.data.dados_extra.length > 0) {
        const estimativas = result.data.dados_extra[0]?.estimativas_tela_5;
        if (estimativas?.coberturas_detalhadas) {
          coberturas = estimativas.coberturas_detalhadas;
          console.log('Estimativas encontradas (estrutura 2):', coberturas);
        }
      }
      // Estrutura 3: dados_extra direto
      else if (result.data?.dados_extra?.coberturas_detalhadas) {
        coberturas = result.data.dados_extra.coberturas_detalhadas;
        console.log('Estimativas encontradas (estrutura 3):', coberturas);
      }
      
      if (coberturas && coberturas.length > 0) {
        message += 'Estimativas encontradas:\n\n';
        
        coberturas.forEach((cobertura, index) => {
          const nome = cobertura.nome_cobertura || cobertura.nome || cobertura.cobertura || `Cobertura ${index + 1}`;
          message += `${index + 1}. ${nome}\n`;
          
          if (cobertura.valores) {
            const de = cobertura.valores.de || 'N/A';
            const ate = cobertura.valores.ate || 'N/A';
            message += `   Valor: ${de} - ${ate}\n`;
          }
          
          if (cobertura.beneficios && cobertura.beneficios.length > 0) {
            message += `   Benefícios: ${cobertura.beneficios.length} incluídos\n`;
          }
          
          message += '\n';
        });
      } else {
        message += 'Nenhuma estimativa encontrada nos dados.\n';
        message += 'Estrutura dos dados:\n';
        message += JSON.stringify(result.data, null, 2);
      }
      
      alert(message);
    }
  }

  // Função para executar RPA
  async function executeRPA(formData) {
    try {
      const sessionId = CONFIG.sessionPrefix + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
      
      const response = await fetch(`${CONFIG.apiUrl}/executar_rpa.php`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          session: sessionId,
          dados: formData
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      
      if (data.success) {
        // Mostrar modal de progresso
        window.rpaModal.show(sessionId);
        return { success: true, sessionId };
      } else {
        throw new Error(data.message || 'Erro ao executar RPA');
      }
    } catch (error) {
      console.error('Erro ao executar RPA:', error);
      return { success: false, error: error.message };
    }
  }

  // Inicializar quando DOM estiver pronto
  function init() {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', () => {
        window.rpaModal = new RPAModal();
        window.executeRPA = executeRPA;
      });
    } else {
      window.rpaModal = new RPAModal();
      window.executeRPA = executeRPA;
    }
  }

  // Inicializar
  init();

})();
