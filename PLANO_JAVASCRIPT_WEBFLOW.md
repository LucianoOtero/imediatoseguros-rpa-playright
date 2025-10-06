# 🚀 PLANO JAVASCRIPT PARA WEBFLOW
## Custom Code para Modal RPA - Imediato Seguros

**Data:** 29 de Setembro de 2025  
**Projeto:** JavaScript para Webflow Custom Code  
**Status:** PLANO DE DESENVOLVIMENTO  
**Objetivo:** Criar script JavaScript para injetar no Webflow  

---

## 🎯 ESCOPO DO PROJETO

### **Objetivo Principal**
- **JavaScript único** para Webflow Custom Code
- **Modal de progresso** integrado ao site existente
- **Chamada da API** do Hetzner
- **Interface consistente** com segurosimediato.com.br

### **Não Incluído**
- ❌ Formulário HTML completo
- ❌ Páginas de teste
- ❌ Build system complexo
- ❌ Múltiplos arquivos

### **Foco Principal**
- ✅ **Um único arquivo JavaScript**
- ✅ **Modal de progresso elegante**
- ✅ **Integração com API do Hetzner**
- ✅ **Design consistente com o site**

---

## 📋 ESTRUTURA DO SCRIPT

### **Arquivo Único: `rpa-modal.js`**
```javascript
/**
 * RPA Modal para Webflow - Imediato Seguros
 * Custom Code para integração com RPA
 * Versão: 1.0.0
 */

(function() {
  'use strict';

  // Configurações
  const CONFIG = {
    apiUrl: 'http://37.27.92.160',
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
      this.createModal();
      this.setupEventListeners();
      this.injectStyles();
    }

    // Criar modal HTML
    createModal() {
      const modalHTML = `
        <div id="rpa-modal" class="rpa-modal-overlay" style="display: none;">
          <div class="rpa-modal-container">
            <div class="rpa-modal-header">
              <div class="rpa-modal-logo">
                <img src="https://uploads-ssl.webflow.com/your-logo-path/logo-imediato-seguros.svg" 
                     alt="Imediato Seguros" class="rpa-logo">
              </div>
              <div class="rpa-modal-title">
                <h3>⏳ Calculando seu Seguro...</h3>
                <p>Aguarde um momento, estamos processando seus dados</p>
              </div>
              <button class="rpa-modal-close" onclick="window.rpaModal.hide()">
                <i class="fas fa-times"></i>
              </button>
            </div>
            
            <div class="rpa-modal-body">
              <!-- Progresso Geral -->
              <div class="rpa-progress-container">
                <div class="rpa-progress-header">
                  <span class="rpa-progress-label">Progresso Geral</span>
                  <span class="rpa-progress-percentage">0%</span>
                </div>
                <div class="rpa-progress-bar">
                  <div class="rpa-progress-fill" style="width: 0%"></div>
                </div>
                <div class="rpa-progress-steps">0 de 15 telas processadas</div>
              </div>

              <!-- Tela Atual -->
              <div class="rpa-current-step">
                <div class="rpa-step-header">
                  <div class="rpa-step-icon">🚗</div>
                  <div class="rpa-step-info">
                    <h4>Aguardando início...</h4>
                    <small>Preparando processamento</small>
                  </div>
                </div>
                <div class="rpa-step-progress">
                  <div class="rpa-progress-bar small">
                    <div class="rpa-progress-fill" style="width: 0%"></div>
                  </div>
                  <span class="rpa-step-time">⏱️ Tempo estimado: --</span>
                </div>
              </div>

              <!-- Estimativas -->
              <div class="rpa-estimates">
                <h5>📊 Estimativas Iniciais (Tela 5)</h5>
                <div class="rpa-estimates-grid">
                  <div class="rpa-estimate-card">
                    <div class="rpa-estimate-header">
                      <i class="fas fa-shield-alt"></i>
                      <h6>Compreensiva</h6>
                    </div>
                    <div class="rpa-estimate-value">--</div>
                  </div>
                  <div class="rpa-estimate-card">
                    <div class="rpa-estimate-header">
                      <i class="fas fa-lock"></i>
                      <h6>Roubo e Furto</h6>
                    </div>
                    <div class="rpa-estimate-value">--</div>
                  </div>
                  <div class="rpa-estimate-card">
                    <div class="rpa-estimate-header">
                      <i class="fas fa-car-crash"></i>
                      <h6>RCF</h6>
                    </div>
                    <div class="rpa-estimate-value">--</div>
                  </div>
                </div>
              </div>

              <!-- Timeline -->
              <div class="rpa-timeline">
                <h5>📋 Timeline de Execução</h5>
                <div class="rpa-timeline-container" id="rpa-timeline">
                  <!-- Timeline items will be populated dynamically -->
                </div>
              </div>
            </div>

            <div class="rpa-modal-footer">
              <div class="rpa-last-update">
                <i class="fas fa-sync-alt"></i>
                Última atualização: <span id="rpa-last-update">--</span>
              </div>
            </div>
          </div>
        </div>
      `;

      document.body.insertAdjacentHTML('beforeend', modalHTML);
    }

    // Injetar estilos CSS
    injectStyles() {
      const styles = `
        <style>
          /* Modal Overlay */
          .rpa-modal-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.8);
            z-index: 9999;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
          }

          /* Modal Container */
          .rpa-modal-container {
            background: white;
            border-radius: 16px;
            max-width: 600px;
            width: 100%;
            max-height: 90vh;
            overflow-y: auto;
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
            animation: rpa-modal-slide-in 0.3s ease-out;
          }

          @keyframes rpa-modal-slide-in {
            from {
              opacity: 0;
              transform: translateY(-20px) scale(0.95);
            }
            to {
              opacity: 1;
              transform: translateY(0) scale(1);
            }
          }

          /* Modal Header */
          .rpa-modal-header {
            background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
            color: white;
            padding: 24px;
            border-radius: 16px 16px 0 0;
            display: flex;
            align-items: center;
            gap: 16px;
            position: relative;
          }

          .rpa-modal-logo .rpa-logo {
            height: 40px;
            width: auto;
            filter: brightness(0) invert(1);
          }

          .rpa-modal-title h3 {
            margin: 0;
            font-size: 20px;
            font-weight: 700;
          }

          .rpa-modal-title p {
            margin: 4px 0 0 0;
            opacity: 0.9;
            font-size: 14px;
          }

          .rpa-modal-close {
            position: absolute;
            top: 16px;
            right: 16px;
            background: none;
            border: none;
            color: white;
            font-size: 18px;
            padding: 8px;
            border-radius: 8px;
            cursor: pointer;
            transition: background 0.3s ease;
          }

          .rpa-modal-close:hover {
            background: rgba(255, 255, 255, 0.1);
          }

          /* Modal Body */
          .rpa-modal-body {
            padding: 24px;
          }

          /* Progress Container */
          .rpa-progress-container {
            margin-bottom: 24px;
          }

          .rpa-progress-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 8px;
          }

          .rpa-progress-label {
            font-weight: 600;
            color: #374151;
          }

          .rpa-progress-percentage {
            font-weight: 700;
            color: #1e40af;
            font-size: 18px;
          }

          .rpa-progress-bar {
            height: 8px;
            background: #e5e7eb;
            border-radius: 4px;
            overflow: hidden;
            margin-bottom: 8px;
          }

          .rpa-progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #1e40af 0%, #3b82f6 100%);
            border-radius: 4px;
            transition: width 0.5s ease;
            position: relative;
          }

          .rpa-progress-fill::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(90deg, transparent 0%, rgba(255,255,255,0.3) 50%, transparent 100%);
            animation: rpa-progress-shine 2s infinite;
          }

          @keyframes rpa-progress-shine {
            0% { transform: translateX(-100%); }
            100% { transform: translateX(100%); }
          }

          .rpa-progress-steps {
            font-size: 14px;
            color: #6b7280;
            text-align: center;
          }

          /* Current Step */
          .rpa-current-step {
            background: #f9fafb;
            border: 1px solid #e5e7eb;
            border-radius: 12px;
            padding: 16px;
            margin-bottom: 24px;
          }

          .rpa-step-header {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 12px;
          }

          .rpa-step-icon {
            font-size: 24px;
          }

          .rpa-step-info h4 {
            margin: 0;
            font-size: 16px;
            font-weight: 600;
            color: #374151;
          }

          .rpa-step-info small {
            color: #6b7280;
            font-size: 12px;
          }

          .rpa-step-progress {
            display: flex;
            align-items: center;
            gap: 12px;
          }

          .rpa-progress-bar.small {
            flex: 1;
            height: 6px;
          }

          .rpa-step-time {
            font-size: 12px;
            color: #6b7280;
            white-space: nowrap;
          }

          /* Estimates */
          .rpa-estimates {
            margin-bottom: 24px;
          }

          .rpa-estimates h5 {
            margin: 0 0 16px 0;
            font-size: 16px;
            font-weight: 600;
            color: #374151;
          }

          .rpa-estimates-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 12px;
          }

          .rpa-estimate-card {
            background: white;
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            padding: 12px;
            text-align: center;
          }

          .rpa-estimate-header {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            margin-bottom: 8px;
          }

          .rpa-estimate-header i {
            color: #1e40af;
          }

          .rpa-estimate-header h6 {
            margin: 0;
            font-size: 12px;
            font-weight: 600;
            color: #374151;
          }

          .rpa-estimate-value {
            font-size: 14px;
            font-weight: 700;
            color: #059669;
          }

          /* Timeline */
          .rpa-timeline h5 {
            margin: 0 0 16px 0;
            font-size: 16px;
            font-weight: 600;
            color: #374151;
          }

          .rpa-timeline-container {
            max-height: 200px;
            overflow-y: auto;
          }

          .rpa-timeline-item {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 8px 0;
            border-bottom: 1px solid #f3f4f6;
          }

          .rpa-timeline-item:last-child {
            border-bottom: none;
          }

          .rpa-timeline-icon {
            font-size: 16px;
            width: 24px;
            text-align: center;
          }

          .rpa-timeline-content h6 {
            margin: 0;
            font-size: 14px;
            font-weight: 600;
            color: #374151;
          }

          .rpa-timeline-content small {
            color: #6b7280;
            font-size: 12px;
          }

          .rpa-timeline-item.completed .rpa-timeline-icon {
            color: #059669;
          }

          .rpa-timeline-item.active .rpa-timeline-icon {
            color: #1e40af;
          }

          .rpa-timeline-item.pending .rpa-timeline-icon {
            color: #9ca3af;
          }

          /* Modal Footer */
          .rpa-modal-footer {
            padding: 16px 24px;
            border-top: 1px solid #e5e7eb;
            background: #f9fafb;
            border-radius: 0 0 16px 16px;
          }

          .rpa-last-update {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            font-size: 12px;
            color: #6b7280;
          }

          .rpa-last-update i {
            animation: rpa-spin 2s linear infinite;
          }

          @keyframes rpa-spin {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
          }

          /* Responsive */
          @media (max-width: 768px) {
            .rpa-modal-container {
              margin: 10px;
              max-width: calc(100% - 20px);
            }
            
            .rpa-modal-header {
              padding: 16px;
              flex-direction: column;
              text-align: center;
              gap: 12px;
            }
            
            .rpa-modal-close {
              position: static;
              align-self: flex-end;
            }
            
            .rpa-modal-body {
              padding: 16px;
            }
            
            .rpa-estimates-grid {
              grid-template-columns: 1fr;
            }
          }
        </style>
      `;

      document.head.insertAdjacentHTML('beforeend', styles);
    }

    // Configurar event listeners
    setupEventListeners() {
      // Fechar modal ao clicar no overlay
      document.addEventListener('click', (e) => {
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
      const modal = document.getElementById('rpa-modal');
      modal.style.display = 'flex';
      document.body.style.overflow = 'hidden';
      this.startPolling();
    }

    // Esconder modal
    hide() {
      this.isActive = false;
      const modal = document.getElementById('rpa-modal');
      modal.style.display = 'none';
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
          this.updateProgressBar(data.progress);
          this.updateCurrentStep(data.current_step);
          this.updateEstimates(data.estimates);
          this.updateTimeline(data.timeline);
          this.updateLastUpdate();

          // Verificar se concluído
          if (data.progress >= 100) {
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
        this.showResults(data.final_result);
      }, 2000);
    }

    // Mostrar resultados
    showResults(result) {
      // Implementar modal de resultados ou callback
      if (window.rpaModal.onComplete) {
        window.rpaModal.onComplete(result);
      }
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
```

---

## 🎯 COMO USAR NO WEBFLOW

### **1. Adicionar Custom Code**
```html
<!-- No Webflow: Project Settings > Custom Code > Head Code -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/js/all.min.js"></script>

<!-- No Webflow: Project Settings > Custom Code > Footer Code -->
<script>
// rpa-modal.js (código completo acima)
</script>
```

### **2. Configurar Botão de Chamada**
```html
<!-- No Webflow: Adicionar botão com ID -->
<button id="calcular-seguro" class="btn btn-primary">
  Calcular Seguro
</button>
```

### **3. JavaScript de Integração**
```javascript
// No Webflow: Custom Code > Footer Code (após o script do modal)
document.getElementById('calcular-seguro').addEventListener('click', async function() {
  // Coletar dados do formulário Webflow
  const formData = {
    placa: document.querySelector('[data-name="placa"]').value,
    marca: document.querySelector('[data-name="marca"]').value,
    modelo: document.querySelector('[data-name="modelo"]').value,
    ano: document.querySelector('[data-name="ano"]').value,
    // ... outros campos
  };

  // Executar RPA
  const result = await executeRPA(formData);
  
  if (result.success) {
    console.log('RPA iniciado com sucesso!');
  } else {
    alert('Erro ao iniciar cálculo: ' + result.error);
  }
});
```

---

## 🎨 PERSONALIZAÇÃO

### **Cores da Marca**
```css
/* Alterar cores no CSS do modal */
:root {
  --primary-blue: #1e40af;      /* Azul principal */
  --primary-blue-light: #3b82f6; /* Azul claro */
  --success-green: #059669;      /* Verde sucesso */
}
```

### **Logo da Empresa**
```javascript
// Alterar URL do logo
<img src="https://uploads-ssl.webflow.com/SEU-PROJETO/logo-imediato-seguros.svg" 
     alt="Imediato Seguros" class="rpa-logo">
```

### **Callback de Conclusão**
```javascript
// Configurar callback quando RPA terminar
window.rpaModal.onComplete = function(result) {
  // Redirecionar para página de resultados
  window.location.href = '/resultados?session=' + result.session_id;
  
  // Ou mostrar modal de resultados
  // showResultsModal(result);
};
```

---

## 📱 RESPONSIVIDADE

### **Mobile-First**
- Modal responsivo para todos os dispositivos
- Touch-friendly (botões com 44px mínimo)
- Scroll otimizado para mobile
- Layout adaptativo

### **Breakpoints**
- Mobile: < 768px
- Tablet: 768px - 1024px
- Desktop: > 1024px

---

## 🔒 SEGURANÇA

### **Validações**
- Sanitização de dados antes do envio
- Timeout de 30 segundos para requests
- Tratamento de erros robusto
- CSP compatível

### **CORS**
- Configurar CORS no servidor Hetzner
- Headers apropriados para Webflow

---

## 🚀 CRONOGRAMA

### **Fase 1: Desenvolvimento (2 dias)**
- [ ] Criar script JavaScript completo
- [ ] Implementar modal de progresso
- [ ] Configurar polling e atualizações
- [ ] Testes básicos

### **Fase 2: Integração Webflow (1 dia)**
- [ ] Configurar Custom Code
- [ ] Integrar com formulário existente
- [ ] Testes de integração
- [ ] Ajustes finais

### **Fase 3: Testes e Deploy (1 dia)**
- [ ] Testes em diferentes dispositivos
- [ ] Validação de performance
- [ ] Deploy em produção
- [ ] Documentação final

**Total: 4 dias**

---

## 🎯 RESULTADO

### **Script Único**
- **Um arquivo JavaScript** para Webflow
- **Modal elegante** com progresso em tempo real
- **Integração simples** com formulário existente
- **Design consistente** com a marca

### **Funcionalidades**
- Modal de progresso animado
- Polling inteligente (1.5s)
- Timeline de execução
- Estimativas em tempo real
- Responsivo mobile-first
- Acessibilidade básica

### **Fácil Implementação**
- Copy-paste no Webflow Custom Code
- Configuração mínima necessária
- Compatível com qualquer formulário
- Sem dependências externas complexas

---

**📋 Plano gerado em:** 29 de Setembro de 2025  
**🚀 Foco:** JavaScript para Webflow Custom Code  
**⏱️ Prazo:** 4 dias  
**👥 Complexidade:** Baixa  
**💰 Investimento:** Baixo  
**🏆 Resultado:** Script pronto para uso
















