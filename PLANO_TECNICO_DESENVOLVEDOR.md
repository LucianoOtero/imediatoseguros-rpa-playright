# 💻 PLANO TÉCNICO DE DESENVOLVIMENTO
## Formulário HTML RPA - Imediato Seguros

**Data:** 29 de Setembro de 2025  
**Desenvolvedor:** Análise Técnica Detalhada  
**Projeto:** Interface Web RPA Consistente  
**Status:** PLANO DE DESENVOLVIMENTO TÉCNICO  

---

## 🎯 ANÁLISE TÉCNICA DO PROJETO

### **Requisitos Funcionais**
- Formulário multi-step (4 etapas)
- Modal de progresso em tempo real
- Validação client-side e server-side
- Integração com API PHP do Hetzner
- Responsividade mobile-first
- Acessibilidade WCAG 2.1 AA

### **Requisitos Não-Funcionais**
- Performance: Core Web Vitals otimizados
- Segurança: Validação híbrida, CSP
- Compatibilidade: Chrome 90+, Firefox 88+, Safari 14+
- Acessibilidade: Screen readers, navegação por teclado

---

## 🏗️ ARQUITETURA TÉCNICA

### **Stack Tecnológico**
```javascript
// Frontend
- HTML5 (semântico)
- CSS3 (Grid, Flexbox, Custom Properties)
- JavaScript ES6+ (Vanilla)
- Bootstrap 5.3.2
- Font Awesome 6.4.0

// Build Tools
- Vite (desenvolvimento)
- PostCSS (autoprefixer, minify)
- ESLint + Prettier (qualidade)

// APIs
- Fetch API (HTTP requests)
- Intersection Observer (lazy loading)
- Web Workers (validações pesadas)
```

### **Estrutura de Arquivos**
```
src/
├── index.html
├── assets/
│   ├── css/
│   │   ├── main.css
│   │   ├── components/
│   │   │   ├── form.css
│   │   │   ├── modal.css
│   │   │   └── progress.css
│   │   └── responsive.css
│   ├── js/
│   │   ├── app.js
│   │   ├── modules/
│   │   │   ├── FormManager.js
│   │   │   ├── ModalProgress.js
│   │   │   ├── Validator.js
│   │   │   └── ApiClient.js
│   │   └── utils/
│   │       ├── helpers.js
│   │       └── constants.js
│   └── images/
│       └── logo-imediato-seguros.svg
├── dist/ (build output)
└── package.json
```

---

## 📋 IMPLEMENTAÇÃO DETALHADA

### **1. FormManager.js - Gerenciador do Formulário**
```javascript
class FormManager {
  constructor() {
    this.currentStep = 1;
    this.totalSteps = 4;
    this.formData = {};
    this.validator = new Validator();
    this.init();
  }

  init() {
    this.setupEventListeners();
    this.loadDraft();
    this.updateProgress();
  }

  setupEventListeners() {
    // Navegação entre etapas
    document.querySelectorAll('.step-nav').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const direction = e.target.dataset.direction;
        this.navigateStep(direction);
      });
    });

    // Validação em tempo real
    document.querySelectorAll('input, select, textarea').forEach(field => {
      field.addEventListener('blur', (e) => this.validateField(e.target));
      field.addEventListener('input', (e) => this.saveField(e.target));
    });
  }

  navigateStep(direction) {
    if (direction === 'next' && this.validateCurrentStep()) {
      this.currentStep++;
    } else if (direction === 'prev') {
      this.currentStep--;
    }
    
    this.updateProgress();
    this.showStep(this.currentStep);
  }

  validateCurrentStep() {
    const stepFields = document.querySelectorAll(`[data-step="${this.currentStep}"] input, select, textarea`);
    let isValid = true;

    stepFields.forEach(field => {
      const result = this.validator.validateField(field.name, field.value);
      if (!result.valid) {
        this.showFieldError(field, result.message);
        isValid = false;
      } else {
        this.clearFieldError(field);
      }
    });

    return isValid;
  }

  showStep(stepNumber) {
    // Esconder todas as etapas
    document.querySelectorAll('.form-step').forEach(step => {
      step.classList.remove('active');
    });

    // Mostrar etapa atual
    const currentStepElement = document.querySelector(`[data-step="${stepNumber}"]`);
    if (currentStepElement) {
      currentStepElement.classList.add('active');
    }

    // Atualizar indicador de progresso
    this.updateStepIndicator(stepNumber);
  }

  updateProgress() {
    const progress = (this.currentStep / this.totalSteps) * 100;
    const progressBar = document.querySelector('.progress-bar-fill');
    if (progressBar) {
      progressBar.style.width = `${progress}%`;
    }
  }

  saveField(field) {
    this.formData[field.name] = field.value;
    this.saveDraft();
  }

  saveDraft() {
    localStorage.setItem('seguro_form_draft', JSON.stringify(this.formData));
  }

  loadDraft() {
    const draft = localStorage.getItem('seguro_form_draft');
    if (draft) {
      this.formData = JSON.parse(draft);
      this.populateForm();
    }
  }

  populateForm() {
    Object.entries(this.formData).forEach(([name, value]) => {
      const field = document.querySelector(`[name="${name}"]`);
      if (field) {
        field.value = value;
      }
    });
  }

  getFormData() {
    return { ...this.formData };
  }

  clearDraft() {
    localStorage.removeItem('seguro_form_draft');
    this.formData = {};
  }
}
```

### **2. ModalProgress.js - Modal de Progresso**
```javascript
class ModalProgress {
  constructor() {
    this.modal = null;
    this.progressBar = null;
    this.currentStepElement = null;
    this.estimatesContainer = null;
    this.isActive = false;
    this.pollingInterval = null;
    this.sessionId = null;
    this.init();
  }

  init() {
    this.createModal();
    this.setupEventListeners();
  }

  createModal() {
    const modalHTML = `
      <div class="modal fade" id="progressModal" tabindex="-1">
        <div class="modal-dialog modal-lg">
          <div class="modal-content">
            <div class="modal-header">
              <div class="modal-logo">
                <img src="assets/images/logo-imediato-seguros.svg" alt="Imediato Seguros" class="logo-small">
              </div>
              <div class="modal-title">
                <h5><i class="fas fa-hourglass-half"></i> Calculando seu Seguro...</h5>
                <p class="modal-subtitle">Aguarde um momento, estamos processando seus dados</p>
              </div>
              <button type="button" class="btn-close" data-bs-dismiss="modal">
                <i class="fas fa-times"></i>
              </button>
            </div>
            <div class="modal-body">
              <div class="progress-container">
                <div class="progress-header">
                  <span class="progress-label">Progresso Geral</span>
                  <span class="progress-percentage">0%</span>
                </div>
                <div class="progress-bar">
                  <div class="progress-fill" style="width: 0%"></div>
                </div>
                <div class="progress-steps">0 de 15 telas processadas</div>
              </div>
              
              <div class="current-step-card">
                <div class="step-header">
                  <div class="step-icon">🚗</div>
                  <div class="step-info">
                    <h6>Aguardando início...</h6>
                    <small>Preparando processamento</small>
                  </div>
                </div>
                <div class="step-progress">
                  <div class="progress-bar small">
                    <div class="progress-fill" style="width: 0%"></div>
                  </div>
                  <span class="step-time">⏱️ Tempo estimado: --</span>
                </div>
              </div>

              <div class="estimates-container">
                <h6>📊 Estimativas Iniciais (Tela 5)</h6>
                <div class="estimates-grid">
                  <div class="estimate-card">
                    <div class="estimate-header">
                      <i class="fas fa-shield-alt"></i>
                      <h6>Compreensiva</h6>
                    </div>
                    <div class="estimate-value">--</div>
                  </div>
                  <div class="estimate-card">
                    <div class="estimate-header">
                      <i class="fas fa-lock"></i>
                      <h6>Roubo e Furto</h6>
                    </div>
                    <div class="estimate-value">--</div>
                  </div>
                  <div class="estimate-card">
                    <div class="estimate-header">
                      <i class="fas fa-car-crash"></i>
                      <h6>RCF</h6>
                    </div>
                    <div class="estimate-value">--</div>
                  </div>
                </div>
              </div>

              <div class="timeline-container">
                <h6>📋 Timeline de Execução</h6>
                <div class="timeline" id="executionTimeline">
                  <!-- Timeline items will be populated dynamically -->
                </div>
              </div>
            </div>
            <div class="modal-footer">
              <div class="last-update">
                <i class="fas fa-sync-alt"></i>
                Última atualização: <span id="lastUpdate">--</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    `;

    document.body.insertAdjacentHTML('beforeend', modalHTML);
    this.modal = new bootstrap.Modal(document.getElementById('progressModal'));
  }

  setupEventListeners() {
    // Fechar modal
    document.querySelector('#progressModal .btn-close').addEventListener('click', () => {
      this.stopPolling();
    });

    // Modal hidden event
    document.getElementById('progressModal').addEventListener('hidden.bs.modal', () => {
      this.stopPolling();
    });
  }

  show(sessionId) {
    this.sessionId = sessionId;
    this.isActive = true;
    this.modal.show();
    this.startPolling();
  }

  hide() {
    this.isActive = false;
    this.modal.hide();
    this.stopPolling();
  }

  startPolling() {
    if (this.pollingInterval) {
      clearInterval(this.pollingInterval);
    }

    this.pollingInterval = setInterval(() => {
      this.updateProgress();
    }, 1500); // Polling a cada 1.5 segundos
  }

  stopPolling() {
    if (this.pollingInterval) {
      clearInterval(this.pollingInterval);
      this.pollingInterval = null;
    }
  }

  async updateProgress() {
    try {
      const response = await fetch(`http://37.27.92.160/get_progress.php?session=${this.sessionId}`);
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

  updateProgressBar(progress) {
    const progressFill = document.querySelector('.progress-fill');
    const progressPercentage = document.querySelector('.progress-percentage');
    const progressSteps = document.querySelector('.progress-steps');

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

  updateCurrentStep(stepData) {
    const stepIcon = document.querySelector('.step-icon');
    const stepTitle = document.querySelector('.step-info h6');
    const stepDescription = document.querySelector('.step-info small');
    const stepProgress = document.querySelector('.step-progress .progress-fill');
    const stepTime = document.querySelector('.step-time');

    if (stepIcon) stepIcon.textContent = stepData.icon || '🚗';
    if (stepTitle) stepTitle.textContent = stepData.title || 'Processando...';
    if (stepDescription) stepDescription.textContent = stepData.description || 'Aguarde...';
    if (stepProgress) stepProgress.style.width = `${stepData.progress || 0}%`;
    if (stepTime) stepTime.textContent = `⏱️ Tempo estimado: ${stepData.estimated_time || '--'}`;
  }

  updateEstimates(estimates) {
    if (!estimates) return;

    const estimateCards = document.querySelectorAll('.estimate-card');
    const estimateTypes = ['compreensiva', 'roubo_furto', 'rcf'];

    estimateTypes.forEach((type, index) => {
      const card = estimateCards[index];
      if (card && estimates[type]) {
        const valueElement = card.querySelector('.estimate-value');
        if (valueElement) {
          valueElement.textContent = estimates[type];
        }
      }
    });
  }

  updateTimeline(timeline) {
    if (!timeline) return;

    const timelineContainer = document.getElementById('executionTimeline');
    if (!timelineContainer) return;

    timelineContainer.innerHTML = timeline.map(step => `
      <div class="timeline-item ${step.status}">
        <div class="timeline-icon">${step.icon}</div>
        <div class="timeline-content">
          <h6>${step.title}</h6>
          <small>${step.description}</small>
        </div>
      </div>
    `).join('');
  }

  updateLastUpdate() {
    const lastUpdateElement = document.getElementById('lastUpdate');
    if (lastUpdateElement) {
      lastUpdateElement.textContent = new Date().toLocaleTimeString();
    }
  }

  handleCompletion(data) {
    this.stopPolling();
    
    // Mostrar resultado final
    setTimeout(() => {
      this.hide();
      this.showResults(data.final_result);
    }, 2000);
  }

  showResults(result) {
    // Implementar modal de resultados
    console.log('Resultado final:', result);
  }
}
```

### **3. Validator.js - Validação de Dados**
```javascript
class Validator {
  constructor() {
    this.rules = {
      placa: {
        required: true,
        pattern: /^[A-Z]{3}[0-9]{4}$/,
        message: 'Placa deve ter formato ABC1234'
      },
      cpf: {
        required: true,
        validator: this.validateCPF,
        message: 'CPF inválido'
      },
      email: {
        required: true,
        pattern: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
        message: 'Email inválido'
      },
      celular: {
        required: true,
        pattern: /^\(\d{2}\)\s\d{4,5}-\d{4}$/,
        message: 'Celular deve ter formato (11) 99999-9999'
      },
      cep: {
        required: true,
        pattern: /^\d{5}-?\d{3}$/,
        message: 'CEP inválido'
      }
    };
  }

  validateField(fieldName, value) {
    const rule = this.rules[fieldName];
    if (!rule) return { valid: true };

    // Verificar se é obrigatório
    if (rule.required && !value) {
      return { valid: false, message: `${fieldName} é obrigatório` };
    }

    // Verificar padrão
    if (rule.pattern && !rule.pattern.test(value)) {
      return { valid: false, message: rule.message };
    }

    // Verificar validador customizado
    if (rule.validator && !rule.validator(value)) {
      return { valid: false, message: rule.message };
    }

    return { valid: true };
  }

  validateCPF(cpf) {
    cpf = cpf.replace(/[^\d]/g, '');
    if (cpf.length !== 11) return false;

    // Verificar se todos os dígitos são iguais
    if (/^(\d)\1{10}$/.test(cpf)) return false;

    // Validar primeiro dígito
    let sum = 0;
    for (let i = 0; i < 9; i++) {
      sum += parseInt(cpf.charAt(i)) * (10 - i);
    }
    let remainder = (sum * 10) % 11;
    if (remainder === 10 || remainder === 11) remainder = 0;
    if (remainder !== parseInt(cpf.charAt(9))) return false;

    // Validar segundo dígito
    sum = 0;
    for (let i = 0; i < 10; i++) {
      sum += parseInt(cpf.charAt(i)) * (11 - i);
    }
    remainder = (sum * 10) % 11;
    if (remainder === 10 || remainder === 11) remainder = 0;
    return remainder === parseInt(cpf.charAt(10));
  }

  validateCNPJ(cnpj) {
    cnpj = cnpj.replace(/[^\d]/g, '');
    if (cnpj.length !== 14) return false;

    // Verificar se todos os dígitos são iguais
    if (/^(\d)\1{13}$/.test(cnpj)) return false;

    // Validar primeiro dígito
    let sum = 0;
    let weight = 2;
    for (let i = 11; i >= 0; i--) {
      sum += parseInt(cnpj.charAt(i)) * weight;
      weight = weight === 9 ? 2 : weight + 1;
    }
    let remainder = sum % 11;
    const firstDigit = remainder < 2 ? 0 : 11 - remainder;
    if (firstDigit !== parseInt(cnpj.charAt(12))) return false;

    // Validar segundo dígito
    sum = 0;
    weight = 2;
    for (let i = 12; i >= 0; i--) {
      sum += parseInt(cnpj.charAt(i)) * weight;
      weight = weight === 9 ? 2 : weight + 1;
    }
    remainder = sum % 11;
    const secondDigit = remainder < 2 ? 0 : 11 - remainder;
    return secondDigit === parseInt(cnpj.charAt(13));
  }
}
```

### **4. ApiClient.js - Cliente da API**
```javascript
class ApiClient {
  constructor() {
    this.baseUrl = 'http://37.27.92.160';
    this.timeout = 30000; // 30 segundos
  }

  async executeRPA(formData) {
    try {
      const response = await fetch(`${this.baseUrl}/executar_rpa.php`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          session: this.generateSessionId(),
          dados: formData
        }),
        signal: AbortSignal.timeout(this.timeout)
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Erro ao executar RPA:', error);
      throw error;
    }
  }

  async getProgress(sessionId) {
    try {
      const response = await fetch(`${this.baseUrl}/get_progress.php?session=${sessionId}`, {
        signal: AbortSignal.timeout(10000) // 10 segundos para progresso
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Erro ao obter progresso:', error);
      throw error;
    }
  }

  generateSessionId() {
    return `seguro_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  sanitizeData(data) {
    const sanitized = {};
    for (const [key, value] of Object.entries(data)) {
      if (typeof value === 'string') {
        sanitized[key] = value.trim().replace(/[<>]/g, '');
      } else {
        sanitized[key] = value;
      }
    }
    return sanitized;
  }
}
```

---

## 🎨 IMPLEMENTAÇÃO CSS

### **main.css - Estilos Principais**
```css
:root {
  /* Cores da marca Imediato Seguros */
  --primary-blue: #1e40af;
  --primary-blue-light: #3b82f6;
  --primary-blue-dark: #1e3a8a;
  --success-green: #059669;
  --success-green-light: #10b981;
  --warning-orange: #d97706;
  --error-red: #dc2626;
  
  /* Cores neutras */
  --white: #ffffff;
  --gray-50: #f9fafb;
  --gray-100: #f3f4f6;
  --gray-200: #e5e7eb;
  --gray-300: #d1d5db;
  --gray-400: #9ca3af;
  --gray-500: #6b7280;
  --gray-600: #4b5563;
  --gray-700: #374151;
  --gray-800: #1f2937;
  --gray-900: #111827;
  
  /* Tipografia */
  --font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  --font-size-xs: 0.75rem;
  --font-size-sm: 0.875rem;
  --font-size-base: 1rem;
  --font-size-lg: 1.125rem;
  --font-size-xl: 1.25rem;
  --font-size-2xl: 1.5rem;
  --font-size-3xl: 1.875rem;
  
  /* Espaçamentos */
  --spacing-xs: 0.25rem;
  --spacing-sm: 0.5rem;
  --spacing-md: 1rem;
  --spacing-lg: 1.5rem;
  --spacing-xl: 2rem;
  --spacing-2xl: 3rem;
  
  /* Bordas */
  --border-radius-sm: 0.375rem;
  --border-radius-md: 0.5rem;
  --border-radius-lg: 0.75rem;
  --border-radius-xl: 1rem;
  
  /* Sombras */
  --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
  --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1);
  --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1);
  --shadow-xl: 0 20px 25px -5px rgb(0 0 0 / 0.1);
}

/* Reset e base */
* {
  box-sizing: border-box;
}

body {
  font-family: var(--font-family);
  font-size: var(--font-size-base);
  line-height: 1.6;
  color: var(--gray-800);
  background-color: var(--gray-50);
  margin: 0;
  padding: 0;
}

/* Container principal */
.main-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: var(--spacing-lg);
}

/* Header do formulário */
.form-header {
  background: linear-gradient(135deg, var(--primary-blue) 0%, var(--primary-blue-light) 100%);
  color: white;
  padding: var(--spacing-2xl);
  text-align: center;
  border-radius: var(--border-radius-lg) var(--border-radius-lg) 0 0;
  margin-bottom: 0;
}

.logo-container {
  margin-bottom: var(--spacing-lg);
}

.logo {
  height: 60px;
  width: auto;
  filter: brightness(0) invert(1);
}

.form-title {
  font-size: var(--font-size-2xl);
  font-weight: 700;
  margin-bottom: var(--spacing-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-sm);
}

.form-subtitle {
  font-size: var(--font-size-base);
  opacity: 0.9;
  margin: 0;
}

/* Indicador de progresso */
.progress-indicator {
  display: flex;
  justify-content: space-between;
  padding: var(--spacing-xl);
  background: var(--white);
  border-bottom: 1px solid var(--gray-200);
  margin-bottom: 0;
}

.step {
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  flex: 1;
}

.step-number {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: var(--gray-300);
  color: var(--gray-600);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  margin-bottom: var(--spacing-sm);
  transition: all 0.3s ease;
}

.step.active .step-number {
  background: var(--primary-blue);
  color: white;
  transform: scale(1.1);
}

.step.completed .step-number {
  background: var(--success-green);
  color: white;
}

.step-label {
  font-size: var(--font-size-sm);
  color: var(--gray-600);
  font-weight: 500;
  text-align: center;
}

/* Formulário */
.form-container {
  background: var(--white);
  border-radius: 0 0 var(--border-radius-lg) var(--border-radius-lg);
  padding: var(--spacing-2xl);
  box-shadow: var(--shadow-lg);
}

.form-step {
  display: none;
}

.form-step.active {
  display: block;
}

.form-step-title {
  font-size: var(--font-size-xl);
  font-weight: 600;
  color: var(--gray-800);
  margin-bottom: var(--spacing-lg);
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

/* Campos do formulário */
.form-group {
  margin-bottom: var(--spacing-lg);
}

.form-label {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  font-weight: 600;
  color: var(--gray-700);
  margin-bottom: var(--spacing-sm);
}

.form-input,
.form-select,
.form-textarea {
  width: 100%;
  padding: var(--spacing-md);
  border: 2px solid var(--gray-300);
  border-radius: var(--border-radius-md);
  font-size: var(--font-size-base);
  font-family: var(--font-family);
  transition: all 0.3s ease;
  background: var(--white);
}

.form-input:focus,
.form-select:focus,
.form-textarea:focus {
  outline: none;
  border-color: var(--primary-blue);
  box-shadow: 0 0 0 3px rgba(30, 64, 175, 0.1);
}

.form-input.is-valid {
  border-color: var(--success-green);
}

.form-input.is-invalid {
  border-color: var(--error-red);
}

.form-help {
  font-size: var(--font-size-sm);
  color: var(--gray-500);
  margin-top: var(--spacing-xs);
}

.invalid-feedback {
  font-size: var(--font-size-sm);
  color: var(--error-red);
  margin-top: var(--spacing-xs);
}

/* Checkboxes */
.checkbox-group {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: var(--spacing-md);
  margin-top: var(--spacing-md);
}

.checkbox-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-md);
  border: 2px solid var(--gray-200);
  border-radius: var(--border-radius-md);
  cursor: pointer;
  transition: all 0.3s ease;
}

.checkbox-item:hover {
  border-color: var(--primary-blue);
  background: var(--gray-50);
}

.checkbox-item input[type="checkbox"] {
  margin: 0;
}

.checkbox-label {
  font-weight: 500;
  color: var(--gray-700);
}

/* Botões */
.btn {
  padding: var(--spacing-md) var(--spacing-lg);
  border: none;
  border-radius: var(--border-radius-md);
  font-size: var(--font-size-base);
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  gap: var(--spacing-sm);
  text-decoration: none;
}

.btn-primary {
  background: var(--primary-blue);
  color: white;
}

.btn-primary:hover {
  background: var(--primary-blue-dark);
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.btn-secondary {
  background: var(--gray-200);
  color: var(--gray-700);
}

.btn-secondary:hover {
  background: var(--gray-300);
}

.btn-success {
  background: var(--success-green);
  color: white;
}

.btn-success:hover {
  background: var(--success-green-light);
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

/* Navegação do formulário */
.form-navigation {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: var(--spacing-2xl);
  padding-top: var(--spacing-lg);
  border-top: 1px solid var(--gray-200);
}

.step-nav {
  min-width: 120px;
}

/* Loading states */
.btn-loading {
  position: relative;
  color: transparent;
}

.btn-loading::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 20px;
  height: 20px;
  margin: -10px 0 0 -10px;
  border: 2px solid transparent;
  border-top: 2px solid currentColor;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Responsividade */
@media (max-width: 768px) {
  .main-container {
    padding: var(--spacing-md);
  }
  
  .form-header {
    padding: var(--spacing-lg);
  }
  
  .form-container {
    padding: var(--spacing-lg);
  }
  
  .progress-indicator {
    padding: var(--spacing-lg);
    flex-wrap: wrap;
    gap: var(--spacing-md);
  }
  
  .step {
    flex: 1;
    min-width: 80px;
  }
  
  .form-navigation {
    flex-direction: column;
    gap: var(--spacing-md);
  }
  
  .step-nav {
    width: 100%;
  }
  
  .checkbox-group {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 480px) {
  .form-title {
    font-size: var(--font-size-xl);
    flex-direction: column;
    gap: var(--spacing-xs);
  }
  
  .step-number {
    width: 32px;
    height: 32px;
    font-size: var(--font-size-sm);
  }
  
  .step-label {
    font-size: var(--font-size-xs);
  }
}
```

---

## 🚀 CRONOGRAMA TÉCNICO

### **Fase 1: Setup e Estrutura (2 dias)**
- [ ] Configurar ambiente de desenvolvimento
- [ ] Criar estrutura de arquivos
- [ ] Implementar design system CSS
- [ ] Configurar build tools (Vite)

### **Fase 2: Formulário Multi-Step (3 dias)**
- [ ] Implementar FormManager.js
- [ ] Criar validações em tempo real
- [ ] Implementar navegação entre etapas
- [ ] Adicionar auto-save e draft

### **Fase 3: Modal de Progresso (2 dias)**
- [ ] Implementar ModalProgress.js
- [ ] Criar polling inteligente
- [ ] Implementar timeline de execução
- [ ] Adicionar animações e transições

### **Fase 4: Integração e Testes (2 dias)**
- [ ] Integrar com API do Hetzner
- [ ] Implementar tratamento de erros
- [ ] Testes de funcionalidade
- [ ] Otimizações de performance

**Total: 9 dias**

---

## 🎯 RESULTADO TÉCNICO

### **Arquitetura Robusta**
- **Modular:** Código organizado em classes
- **Escalável:** Fácil manutenção e extensão
- **Performático:** Otimizado para Core Web Vitals
- **Acessível:** WCAG 2.1 AA compliant

### **Funcionalidades Implementadas**
- **Formulário inteligente** com validação híbrida
- **Modal de progresso** em tempo real
- **Auto-save** e recuperação de dados
- **Responsividade** mobile-first

### **Qualidade de Código**
- **ESLint + Prettier** para consistência
- **Testes unitários** para validações
- **Documentação** técnica completa
- **Performance monitoring** integrado

---

**📋 Plano técnico gerado em:** 29 de Setembro de 2025  
**💻 Desenvolvedor:** Análise Técnica Detalhada  
**⏱️ Prazo:** 9 dias  
**👥 Complexidade:** Média  
**💰 Investimento:** Médio  
**🏆 Resultado:** Código profissional e escalável














