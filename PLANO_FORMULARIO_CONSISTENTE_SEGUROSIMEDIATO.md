# 🎨 PLANO DE FORMULÁRIO CONSISTENTE
## Alinhado com segurosimediato.com.br

**Data:** 29 de Setembro de 2025  
**Projeto:** RPA Imediato Seguros - Interface Consistente  
**Status:** PLANO DE DESENVOLVIMENTO  
**Objetivo:** Criar formulário HTML alinhado com a identidade visual do site  

---

## 🔍 ANÁLISE DO SITE ATUAL

### **Identidade Visual Identificada**
- **Marca:** Imediato Soluções em Seguros
- **Domínio:** segurosimediato.com.br
- **Segmento:** Seguros automotivos
- **Público:** Clientes brasileiros

### **Elementos de Design Presumidos**
- **Cores:** Azul (confiança), Verde (sucesso), Branco (limpeza)
- **Tipografia:** Sans-serif moderna (Inter, Roboto, ou similar)
- **Estilo:** Profissional, confiável, moderno
- **Layout:** Limpo, organizado, focado na conversão

---

## 🎯 DESIGN SYSTEM CONSISTENTE

### **Paleta de Cores Alinhada**
```css
:root {
  /* Cores Primárias - Baseadas no setor de seguros */
  --primary-blue: #1e40af;      /* Azul confiança */
  --primary-blue-light: #3b82f6; /* Azul claro */
  --primary-blue-dark: #1e3a8a;  /* Azul escuro */
  
  /* Cores Secundárias */
  --success-green: #059669;      /* Verde sucesso */
  --success-green-light: #10b981; /* Verde claro */
  --warning-orange: #d97706;     /* Laranja aviso */
  --error-red: #dc2626;          /* Vermelho erro */
  
  /* Cores Neutras */
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
  
  /* Gradientes */
  --gradient-primary: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
  --gradient-success: linear-gradient(135deg, #059669 0%, #10b981 100%);
}
```

### **Tipografia Consistente**
```css
:root {
  /* Fontes */
  --font-primary: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  --font-display: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  
  /* Tamanhos */
  --text-xs: 0.75rem;    /* 12px */
  --text-sm: 0.875rem;   /* 14px */
  --text-base: 1rem;     /* 16px */
  --text-lg: 1.125rem;   /* 18px */
  --text-xl: 1.25rem;    /* 20px */
  --text-2xl: 1.5rem;    /* 24px */
  --text-3xl: 1.875rem;  /* 30px */
  --text-4xl: 2.25rem;   /* 36px */
  
  /* Pesos */
  --font-light: 300;
  --font-normal: 400;
  --font-medium: 500;
  --font-semibold: 600;
  --font-bold: 700;
}
```

---

## 📱 LAYOUT DO FORMULÁRIO

### **Estrutura Visual**
```
┌─────────────────────────────────────────────────────────┐
│  🏢 IMEDIATO SOLUÇÕES EM SEGUROS                       │
│  ┌─────────────────────────────────────────────────────┐ │
│  │  🚗 CALCULADORA DE SEGURO AUTO                     │ │
│  │  Obtenha sua cotação em poucos minutos             │ │
│  └─────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────┤
│  📋 ETAPA 1: DADOS DO VEÍCULO                         │
│  ┌─────────────────┐ ┌─────────────────┐ ┌───────────┐ │
│  │ 🚗 Tipo Veículo │ │ 🏷️ Placa        │ │ 🏭 Marca  │ │
│  │ [Carro ▼]       │ │ [EYQ4J41]       │ │ [TOYOTA]  │ │
│  └─────────────────┘ └─────────────────┘ └───────────┘ │
│  ┌─────────────────┐ ┌─────────────────┐ ┌───────────┐ │
│  │ 🚙 Modelo       │ │ 📅 Ano          │ │ ⛽ Combust.│ │
│  │ [COROLLA...]    │ │ [2009]          │ │ [Flex ▼]  │ │
│  └─────────────────┘ └─────────────────┘ └───────────┘ │
│  ┌─────────────────────────────────────────────────────┐ │
│  │ ☑ Zero KM  ☑ Kit Gás  ☑ Blindado  ☑ Financiado   │ │
│  └─────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────┤
│  [⬅️ Anterior]  [Próximo ➡️]  [💾 Salvar Rascunho]    │
└─────────────────────────────────────────────────────────┘
```

### **Componentes Visuais**

#### **1. Header com Logo**
```html
<header class="form-header">
  <div class="logo-container">
    <img src="assets/logo-imediato-seguros.svg" alt="Imediato Soluções em Seguros" class="logo">
  </div>
  <div class="header-content">
    <h1 class="form-title">
      <i class="fas fa-car"></i>
      Calculadora de Seguro Auto
    </h1>
    <p class="form-subtitle">Obtenha sua cotação em poucos minutos</p>
  </div>
</header>
```

#### **2. Progress Indicator**
```html
<div class="progress-indicator">
  <div class="step active" data-step="1">
    <div class="step-number">1</div>
    <div class="step-label">Veículo</div>
  </div>
  <div class="step" data-step="2">
    <div class="step-number">2</div>
    <div class="step-label">Segurado</div>
  </div>
  <div class="step" data-step="3">
    <div class="step-number">3</div>
    <div class="step-label">Uso</div>
  </div>
  <div class="step" data-step="4">
    <div class="step-number">4</div>
    <div class="step-label">Residência</div>
  </div>
</div>
```

#### **3. Form Fields Modernos**
```html
<div class="form-group">
  <label class="form-label">
    <i class="fas fa-car"></i>
    Tipo de Veículo
  </label>
  <div class="input-wrapper">
    <select class="form-select" name="tipo_veiculo">
      <option value="carro">🚗 Carro</option>
      <option value="moto">🏍️ Moto</option>
    </select>
  </div>
  <div class="form-help">Selecione o tipo de veículo a ser segurado</div>
</div>
```

---

## 🎭 MODAL DE PROGRESSO CONSISTENTE

### **Design do Modal**
```
┌─────────────────────────────────────────────────────────┐
│  ⏳ Calculando seu Seguro...                    [✕]     │
├─────────────────────────────────────────────────────────┤
│  🏢 IMEDIATO SOLUÇÕES EM SEGUROS                       │
│  🎯 Aguarde um momento, estamos processando seus dados │
│                                                         │
│  📊 PROGRESSO GERAL                                     │
│  ┌─────────────────────────────────────────────────────┐ │
│  │ ████████████████████░░░░ 80% (12/15 telas)        │ │
│  └─────────────────────────────────────────────────────┘ │
│                                                         │
│  📋 TELA ATUAL                                          │
│  ┌─────────────────────────────────────────────────────┐ │
│  │ 🏠 Tela 12: Garagem na Residência                 │ │
│  │ ████████████████████░░░░ 85%                      │ │
│  │ ⏱️ Tempo estimado: 17 segundos                     │ │
│  └─────────────────────────────────────────────────────┘ │
│                                                         │
│  📊 ESTIMATIVAS INICIAIS (Tela 5)                      │
│  ┌─────────────────────────────────────────────────────┐ │
│  │ 💰 Compreensiva: R$ 2.400,00 - R$ 2.900,00        │ │
│  │ 🔒 Roubo e Furto: R$ 1.300,00 - R$ 1.700,00       │ │
│  │ 🛡️ RCF: R$ 1.300,00 - R$ 1.700,00                 │ │
│  └─────────────────────────────────────────────────────┘ │
│                                                         │
│  🔄 Última atualização: 14:23:45                       │
└─────────────────────────────────────────────────────────┘
```

### **Componentes do Modal**

#### **1. Modal Header**
```html
<div class="modal-header">
  <div class="modal-logo">
    <img src="assets/logo-imediato-seguros.svg" alt="Imediato Seguros" class="logo-small">
  </div>
  <div class="modal-title">
    <h5>
      <i class="fas fa-hourglass-half"></i>
      Calculando seu Seguro...
    </h5>
    <p class="modal-subtitle">Aguarde um momento, estamos processando seus dados</p>
  </div>
  <button type="button" class="btn-close" data-bs-dismiss="modal">
    <i class="fas fa-times"></i>
  </button>
</div>
```

#### **2. Progress Bar Consistente**
```html
<div class="progress-container">
  <div class="progress-header">
    <span class="progress-label">Progresso Geral</span>
    <span class="progress-percentage">80%</span>
  </div>
  <div class="progress-bar">
    <div class="progress-fill" style="width: 80%">
      <div class="progress-glow"></div>
    </div>
  </div>
  <div class="progress-steps">12 de 15 telas processadas</div>
</div>
```

#### **3. Current Step Card**
```html
<div class="current-step-card">
  <div class="step-header">
    <div class="step-icon">🏠</div>
    <div class="step-info">
      <h6>Tela 12: Garagem na Residência</h6>
      <small>Processando informações de garagem</small>
    </div>
  </div>
  <div class="step-progress">
    <div class="progress-bar small">
      <div class="progress-fill" style="width: 85%"></div>
    </div>
    <span class="step-time">⏱️ Tempo estimado: 17 segundos</span>
  </div>
</div>
```

---

## 🎨 ESTILOS CSS CONSISTENTES

### **Form Header**
```css
.form-header {
  background: var(--gradient-primary);
  color: white;
  padding: 2rem;
  text-align: center;
  border-radius: var(--radius-lg) var(--radius-lg) 0 0;
}

.logo-container {
  margin-bottom: 1rem;
}

.logo {
  height: 60px;
  width: auto;
}

.form-title {
  font-size: var(--text-2xl);
  font-weight: var(--font-bold);
  margin-bottom: 0.5rem;
}

.form-subtitle {
  font-size: var(--text-base);
  opacity: 0.9;
  margin: 0;
}
```

### **Progress Indicator**
```css
.progress-indicator {
  display: flex;
  justify-content: space-between;
  padding: 2rem;
  background: var(--gray-50);
  border-bottom: 1px solid var(--gray-200);
}

.step {
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
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
  font-weight: var(--font-semibold);
  margin-bottom: 0.5rem;
}

.step.active .step-number {
  background: var(--primary-blue);
  color: white;
}

.step-label {
  font-size: var(--text-sm);
  color: var(--gray-600);
  font-weight: var(--font-medium);
}
```

### **Form Fields**
```css
.form-group {
  margin-bottom: 1.5rem;
}

.form-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: var(--font-semibold);
  color: var(--gray-700);
  margin-bottom: 0.5rem;
}

.form-select, .form-input {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 2px solid var(--gray-300);
  border-radius: var(--radius-md);
  font-size: var(--text-base);
  transition: all 0.3s ease;
}

.form-select:focus, .form-input:focus {
  outline: none;
  border-color: var(--primary-blue);
  box-shadow: 0 0 0 3px rgba(30, 64, 175, 0.1);
}

.form-help {
  font-size: var(--text-sm);
  color: var(--gray-500);
  margin-top: 0.25rem;
}
```

### **Modal Styles**
```css
.modal-content {
  border: none;
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-xl);
}

.modal-header {
  background: var(--gradient-primary);
  color: white;
  border-radius: var(--radius-xl) var(--radius-xl) 0 0;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
}

.modal-logo .logo-small {
  height: 40px;
  width: auto;
}

.modal-title h5 {
  margin: 0;
  font-size: var(--text-xl);
  font-weight: var(--font-bold);
}

.modal-subtitle {
  margin: 0;
  opacity: 0.9;
  font-size: var(--text-sm);
}

.btn-close {
  background: none;
  border: none;
  color: white;
  font-size: var(--text-lg);
  padding: 0.5rem;
  border-radius: var(--radius-md);
  transition: background 0.3s ease;
}

.btn-close:hover {
  background: rgba(255, 255, 255, 0.1);
}
```

---

## 📱 RESPONSIVIDADE

### **Mobile First**
```css
/* Mobile */
@media (max-width: 575.98px) {
  .form-header {
    padding: 1.5rem 1rem;
  }
  
  .progress-indicator {
    padding: 1rem;
    flex-wrap: wrap;
    gap: 1rem;
  }
  
  .step {
    flex: 1;
    min-width: 80px;
  }
  
  .modal-dialog {
    margin: 0.5rem;
    max-width: calc(100% - 1rem);
  }
}

/* Tablet */
@media (min-width: 576px) and (max-width: 767.98px) {
  .form-header {
    padding: 2rem 1.5rem;
  }
  
  .progress-indicator {
    padding: 1.5rem;
  }
  
  .modal-dialog {
    max-width: 500px;
  }
}

/* Desktop */
@media (min-width: 768px) {
  .form-header {
    padding: 2rem;
  }
  
  .progress-indicator {
    padding: 2rem;
  }
  
  .modal-dialog {
    max-width: 600px;
  }
}
```

---

## 🔒 SEGURANÇA E VALIDAÇÃO

### **Validação Consistente**
```javascript
class FormValidator {
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
      }
    };
  }

  validateField(fieldName, value) {
    const rule = this.rules[fieldName];
    if (!rule) return { valid: true };
    
    if (rule.required && !value) {
      return { valid: false, message: `${fieldName} é obrigatório` };
    }
    
    if (rule.pattern && !rule.pattern.test(value)) {
      return { valid: false, message: rule.message };
    }
    
    return { valid: true };
  }
}
```

---

## 🚀 IMPLEMENTAÇÃO

### **Estrutura de Arquivos**
```
/
├── index.html
├── css/
│   ├── style.css
│   ├── components.css
│   └── responsive.css
├── js/
│   ├── app.js
│   ├── form-validator.js
│   ├── modal-progress.js
│   └── api-client.js
├── assets/
│   ├── images/
│   │   └── logo-imediato-seguros.svg
│   └── icons/
└── fonts/
    └── inter/
```

### **Dependências**
```html
<!-- Bootstrap 5.3 -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>

<!-- Font Awesome 6 -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">

<!-- Google Fonts -->
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
```

---

## 📊 CRONOGRAMA

### **Fase 1: Design System (2 dias)**
- [ ] Criar paleta de cores consistente
- [ ] Configurar tipografia
- [ ] Implementar componentes base

### **Fase 2: Formulário (3 dias)**
- [ ] Criar formulário multi-step
- [ ] Implementar validações
- [ ] Adicionar responsividade

### **Fase 3: Modal (2 dias)**
- [ ] Criar modal de progresso
- [ ] Implementar animações
- [ ] Configurar polling

### **Fase 4: Integração (2 dias)**
- [ ] Integrar com API
- [ ] Testes de funcionalidade
- [ ] Ajustes finais

**Total: 9 dias**

---

## 🎯 RESULTADO ESPERADO

### **Interface Consistente**
- **Design alinhado** com a marca Imediato Seguros
- **Cores profissionais** do setor de seguros
- **Tipografia moderna** e legível
- **Layout responsivo** para todos os dispositivos

### **Experiência do Usuário**
- **Formulário intuitivo** em etapas
- **Modal elegante** com progresso em tempo real
- **Validações claras** e feedback visual
- **Integração perfeita** com o site existente

---

**📋 Plano gerado em:** 29 de Setembro de 2025  
**🎨 Foco:** Consistência com segurosimediato.com.br  
**⏱️ Prazo:** 9 dias  
**👥 Complexidade:** Média  
**💰 Investimento:** Baixo  
**🏆 Resultado:** Interface integrada e profissional














