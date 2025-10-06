# 🎨 PLANO DE DESIGN MODAL IMEDIATO SEGUROS V6.1.0

## 📋 **VISÃO GERAL DO PROJETO**

### **🎯 OBJETIVO**
Implementar identidade visual completa da Imediato Seguros no modal RPA, incluindo logotipo, cores oficiais e tipografia Titillium Web.

### **📅 VERSÃO**
- **Versão**: 6.1.0
- **Data**: Janeiro 2025
- **Status**: Planejamento Completo

---

## 🎨 **IDENTIDADE VISUAL OFICIAL**

### **🌈 PALETA DE CORES**
```css
:root {
    --imediato-dark-blue: #003366;    /* Azul Escuro Principal */
    --imediato-light-blue: #0099CC;   /* Azul Claro Secundário */
    --imediato-white: #FFFFFF;        /* Branco Neutro */
    --imediato-gray: #F8F9FA;         /* Cinza Claro */
    --imediato-text: #333333;         /* Texto Principal */
    --imediato-text-light: #666666;   /* Texto Secundário */
    --imediato-border: #E0E0E0;       /* Bordas */
    --imediato-shadow: rgba(0, 51, 102, 0.1);      /* Sombra Suave */
    --imediato-shadow-hover: rgba(0, 51, 102, 0.2); /* Sombra Hover */
}
```

### **📝 TIPOGRAFIA**
- **Fonte Principal**: `Titillium Web` (Google Fonts)
- **Pesos**: 300, 400, 600, 700
- **Importação**: `@import url('https://fonts.googleapis.com/css2?family=Titillium+Web:wght@300;400;600;700&display=swap');`

### **🖼️ LOGOTIPO**
- **Fonte**: `https://www.segurosimediato.com.br/assets/logo.png`
- **Posicionamento**: Header centralizado
- **Tamanho**: Max-width 180px (desktop), 150px (mobile)
- **Efeito**: Hover com scale(1.05) e drop-shadow

---

## 🏗️ **ARQUITETURA DOS COMPONENTES**

### **📱 COMPONENTE 1: FORMULÁRIO PRINCIPAL**

#### **🎯 ESTRUTURA HTML**
```html
<div class="rpa-form-container">
    <!-- Header com Logotipo -->
    <div class="form-header">
        <div class="logo-container">
            <img src="https://www.segurosimediato.com.br/assets/logo.png" 
                 alt="Imediato Seguros" 
                 class="company-logo">
        </div>
        <h2><i class="fas fa-car"></i> Calculadora de Seguro</h2>
        <p>Preencha os dados essenciais para calcular seu seguro</p>
    </div>
    
    <form id="rpa-form" class="rpa-form">
        <!-- 8 campos essenciais -->
        <!-- Dados Pessoais: cpf, nome, data_nascimento, sexo, estado_civil -->
        <!-- Dados do Veículo: placa, marca -->
        <!-- Dados de Endereço: cep -->
        <!-- Botão de Ação -->
    </form>
</div>
```

#### **🎨 CARACTERÍSTICAS VISUAIS**
- **Header**: Gradiente azul escuro → azul claro
- **Formulário**: Fundo branco com seções em cinza claro
- **Bordas**: Azul claro nas seções (border-left)
- **Botão**: Gradiente azul com efeito shimmer
- **Hover**: Transform translateY(-2px) nas seções

### **📊 COMPONENTE 2: BARRA DE PROGRESSO**

#### **🎯 ESTRUTURA HTML**
```html
<div class="rpa-progress-container" id="rpaProgressContainer">
    <div class="progress-header">
        <div class="progress-info">
            <span class="progress-text" id="rpaProgressText">0%</span>
            <span class="current-phase" id="rpaCurrentPhase">Iniciando RPA...</span>
        </div>
        <div class="progress-stages">
            <span class="stage-info" id="rpaStageInfo">Fase 0 de 15</span>
        </div>
    </div>
    
    <div class="progress-bar-wrapper">
        <div class="progress-bar">
            <div class="progress-fill" id="rpaProgressFill"></div>
            <div class="progress-glow" id="rpaProgressGlow"></div>
        </div>
    </div>
    
    <div class="progress-details">
        <div class="phase-indicator" id="rpaPhaseIndicator">
            <i class="fas fa-play"></i>
            <span>Preparando execução...</span>
        </div>
    </div>
</div>
```

#### **🎨 CARACTERÍSTICAS VISUAIS**
- **Header**: Gradiente azul com texto branco
- **Barra**: Fundo cinza claro com fill gradiente azul
- **Animação**: Shimmer effect no progress-fill
- **Posição**: Fixed no topo da página
- **Z-index**: 9999 para sobreposição

### **💰 COMPONENTE 3: SEÇÃO DE RESULTADOS**

#### **🎯 ESTRUTURA HTML**
```html
<div class="rpa-results-section" id="rpaResultsSection">
    <div class="results-header">
        <h2><i class="fas fa-check-circle"></i> Cálculo Concluído</h2>
        <p>Seu seguro foi calculado com sucesso!</p>
    </div>
    
    <div class="results-grid">
        <!-- Estimativa Inicial -->
        <div class="estimate-card" id="rpaEstimateCard">
            <!-- Card com valor da Tela 5 -->
        </div>
        
        <!-- Cálculos Finais -->
        <div class="calculations-container">
            <!-- Cálculo Recomendado -->
            <div class="calculation-card recommended" id="rpaRecommendedCard">
                <!-- Card com melhor custo-benefício -->
            </div>
            
            <!-- Cálculo Alternativo -->
            <div class="calculation-card alternative" id="rpaAlternativeCard">
                <!-- Card com opção adicional -->
            </div>
        </div>
    </div>
    
    <!-- Ações -->
    <div class="results-actions">
        <button class="btn-secondary" id="rpaNewCalculation">Nova Cotação</button>
        <button class="btn-primary" id="rpaContactUs">Falar com Corretor</button>
    </div>
</div>
```

#### **🎨 CARACTERÍSTICAS VISUAIS**
- **Header**: Gradiente azul com ícone de sucesso
- **Cards**: Fundo branco com bordas coloridas
- **Recomendado**: Borda azul claro
- **Alternativo**: Borda azul escuro
- **Valores**: Tipografia grande com sombra
- **Hover**: Transform translateY(-10px)

---

## 🎭 **SISTEMA DE ANIMAÇÕES**

### **✨ ANIMAÇÕES PRINCIPAIS**
```css
/* Entrada */
@keyframes slideInUp {
    from { opacity: 0; transform: translateY(40px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

@keyframes scaleIn {
    from { opacity: 0; transform: scale(0.9); }
    to { opacity: 1; transform: scale(1); }
}

/* Interação */
@keyframes pulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.05); }
    100% { transform: scale(1); }
}

@keyframes bounce {
    0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
    40% { transform: translateY(-10px); }
    60% { transform: translateY(-5px); }
}

/* Progresso */
@keyframes shimmer {
    0% { background-position: -200% 0; }
    100% { background-position: 200% 0; }
}
```

### **🎯 CLASSES DE ANIMAÇÃO**
- `.animate-slideInUp`: Entrada de baixo para cima
- `.animate-fadeIn`: Fade in suave
- `.animate-scaleIn`: Entrada com escala
- `.animate-pulse`: Pulsação para valores
- `.animate-bounce`: Bounce para sucesso
- `.animate-shimmer`: Brilho no progresso

---

## 📱 **RESPONSIVIDADE**

### **🖥️ DESKTOP (1200px+)**
- **Grid**: 2 colunas para resultados
- **Formulário**: 2 colunas para campos
- **Logotipo**: 180px
- **Padding**: 2rem

### **💻 TABLET (768px - 1199px)**
- **Grid**: 1 coluna para resultados
- **Formulário**: 2 colunas mantidas
- **Logotipo**: 150px
- **Padding**: 1.5rem

### **📱 MOBILE (até 767px)**
- **Grid**: 1 coluna para tudo
- **Formulário**: 1 coluna
- **Logotipo**: 150px
- **Padding**: 1rem
- **Botões**: Largura total

---

## 🔧 **IMPLEMENTAÇÃO TÉCNICA**

### **📁 ESTRUTURA DE ARQUIVOS**
```
webflow-rpa-v6.1.0/
├── index.html                 # Página principal
├── css/
│   ├── imediato-brand.css    # Cores e tipografia
│   ├── components.css        # Componentes específicos
│   └── animations.css        # Animações
├── js/
│   ├── rpa-webflow.js        # Lógica principal
│   └── form-validation.js    # Validação
└── assets/
    └── logo.png              # Logotipo local (backup)
```

### **🎯 INTEGRAÇÃO WEBFLOW**

#### **📝 CÓDIGO DE INJEÇÃO**
```javascript
// Injeção automática no Webflow
class ImediatoRPAIntegration {
    constructor() {
        this.brandColors = {
            darkBlue: '#003366',
            lightBlue: '#0099CC',
            white: '#FFFFFF'
        };
        this.init();
    }
    
    init() {
        this.loadFonts();
        this.injectStyles();
        this.setupComponents();
    }
    
    loadFonts() {
        const link = document.createElement('link');
        link.href = 'https://fonts.googleapis.com/css2?family=Titillium+Web:wght@300;400;600;700&display=swap';
        link.rel = 'stylesheet';
        document.head.appendChild(link);
    }
    
    injectStyles() {
        // Injetar CSS com cores da marca
    }
    
    setupComponents() {
        // Configurar componentes RPA
    }
}
```

### **🔗 REFERÊNCIAS DE CAMPOS**
```javascript
// Mapeamento explícito para Webflow
const fieldMapping = {
    // Campos do formulário (8 campos)
    cpf: 'cpf',
    nome: 'nome',
    data_nascimento: 'data_nascimento',
    sexo: 'sexo',
    estado_civil: 'estado_civil',
    placa: 'placa',
    marca: 'marca',
    cep: 'cep',
    
    // Botão de ação
    btnCalculate: 'btnCalculate',
    
    // Elementos de progresso
    progressContainer: 'rpaProgressContainer',
    progressText: 'rpaProgressText',
    currentPhase: 'rpaCurrentPhase',
    
    // Elementos de resultados
    resultsSection: 'rpaResultsSection',
    initialEstimate: 'rpaInitialEstimate',
    recommendedValue: 'rpaRecommendedValue',
    alternativeValue: 'rpaAlternativeValue'
};
```

---

## 🎨 **ESPECIFICAÇÕES DE DESIGN**

### **🎯 HIERARQUIA VISUAL**
1. **Logotipo**: Elemento principal no header
2. **Títulos**: Titillium Web 600, cor azul escuro
3. **Subtítulos**: Titillium Web 400, cor azul claro
4. **Texto**: Titillium Web 400, cor cinza escuro
5. **Valores**: Titillium Web 700, cor azul escuro

### **📏 ESPAÇAMENTOS**
- **Padding Principal**: 2rem (desktop), 1rem (mobile)
- **Gap Grid**: 2rem (desktop), 1rem (mobile)
- **Margin Seções**: 2rem entre seções
- **Border Radius**: 15-20px para elementos principais

### **🎭 EFEITOS VISUAIS**
- **Sombras**: rgba(0, 51, 102, 0.1) para profundidade
- **Gradientes**: Azul escuro → Azul claro
- **Transições**: 0.3s cubic-bezier(0.4, 0, 0.2, 1)
- **Hover**: Transform translateY(-3px)

---

## 🚀 **CRONOGRAMA DE IMPLEMENTAÇÃO**

### **📅 FASE 1: PREPARAÇÃO (1 dia)**
- [ ] Análise do logotipo atual
- [ ] Extração das cores exatas
- [ ] Configuração da tipografia Titillium Web
- [ ] Criação da paleta de cores CSS

### **📅 FASE 2: COMPONENTES (2 dias)**
- [ ] Implementação do formulário com logotipo
- [ ] Criação da barra de progresso
- [ ] Desenvolvimento da seção de resultados
- [ ] Aplicação das cores da marca

### **📅 FASE 3: ANIMAÇÕES (1 dia)**
- [ ] Implementação das animações de entrada
- [ ] Criação dos efeitos hover
- [ ] Desenvolvimento das transições
- [ ] Teste de performance

### **📅 FASE 4: RESPONSIVIDADE (1 dia)**
- [ ] Adaptação para tablet
- [ ] Otimização para mobile
- [ ] Teste em diferentes dispositivos
- [ ] Ajustes finais

### **📅 FASE 5: INTEGRAÇÃO (1 dia)**
- [ ] Preparação para Webflow
- [ ] Criação do código de injeção
- [ ] Documentação de campos
- [ ] Testes de integração

---

## ✅ **CHECKLIST DE QUALIDADE**

### **🎨 DESIGN**
- [ ] Logotipo integrado e visível
- [ ] Cores oficiais aplicadas corretamente
- [ ] Tipografia Titillium Web funcionando
- [ ] Gradientes aplicados nos elementos corretos
- [ ] Sombras com tons de azul

### **🎭 ANIMAÇÕES**
- [ ] Entrada suave dos componentes
- [ ] Hover effects funcionando
- [ ] Transições fluidas
- [ ] Performance otimizada
- [ ] Sem travamentos

### **📱 RESPONSIVIDADE**
- [ ] Desktop (1200px+): Layout completo
- [ ] Tablet (768px-1199px): Adaptado
- [ ] Mobile (até 767px): Otimizado
- [ ] Touch-friendly em mobile
- [ ] Textos legíveis em todas as telas

### **🔧 FUNCIONALIDADE**
- [ ] Formulário validando corretamente
- [ ] Barra de progresso animando
- [ ] Resultados exibindo valores
- [ ] Botões funcionais
- [ ] Integração com API RPA

---

## 📚 **RECURSOS E REFERÊNCIAS**

### **🎨 DESIGN SYSTEM**
- **Cores**: Paleta oficial Imediato Seguros
- **Tipografia**: Titillium Web (Google Fonts)
- **Ícones**: Font Awesome 6
- **Logotipo**: https://www.segurosimediato.com.br/assets/logo.png

### **📖 DOCUMENTAÇÃO**
- **Arquitetura**: ARQUITETURA_SOLUCAO_RPA_V6.md
- **Projeto Webflow**: PROJETO_MODAL_RPA_WEBFLOW_V6.1.0.md
- **Implementação**: Este documento

### **🔗 LINKS ÚTEIS**
- **Google Fonts**: https://fonts.google.com/specimen/Titillium+Web
- **Font Awesome**: https://fontawesome.com/
- **Webflow**: https://webflow.com/

---

## 🎯 **PRÓXIMOS PASSOS**

1. **Aprovação do Design**: Revisar e aprovar o plano visual
2. **Implementação**: Desenvolver os componentes
3. **Testes**: Validar em diferentes dispositivos
4. **Integração**: Preparar para Webflow
5. **Deploy**: Implementar na produção

---

**📝 Documento criado em: Janeiro 2025**  
**👨‍💻 Versão: 6.1.0**  
**🎨 Status: Planejamento Completo**



