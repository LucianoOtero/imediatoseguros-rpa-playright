# 🎨 PROJETO MODAL SEPARADO RPA IMEDIATO SEGUROS V6.2.0

## 📋 **VISÃO GERAL DO PROJETO**

### **🎯 OBJETIVO**
Criar um sistema de modal separado que abre após clicar "Efetuar Cálculo", contendo:
- Barra de progresso fixa no topo
- 3 divs de resultados conforme especificação
- Identidade visual completa da Imediato Seguros

### **📅 VERSÃO**
- **Versão**: 6.2.0
- **Data**: Janeiro 2025
- **Status**: Planejamento

---

## 🏗️ **ARQUITETURA DO NOVO SISTEMA**

### **📱 COMPONENTE 1: PÁGINA PRINCIPAL (FORMULÁRIO)**
```html
<!-- Página principal com formulário -->
<div class="main-page">
    <div class="form-container">
        <!-- Formulário simplificado (8 campos) -->
        <!-- Botão "Efetuar Cálculo" -->
    </div>
</div>
```

### **🎭 COMPONENTE 2: MODAL DE PROGRESSO**
```html
<!-- Modal que abre após clicar "Efetuar Cálculo" -->
<div class="rpa-modal" id="rpaModal">
    <!-- Barra de Progresso Fixa no Topo -->
    <div class="modal-progress-bar">
        <div class="progress-header">
            <div class="progress-info">
                <span class="progress-text">0%</span>
                <span class="current-phase">Iniciando RPA...</span>
            </div>
        </div>
        <div class="progress-bar">
            <div class="progress-fill"></div>
        </div>
    </div>
    
    <!-- Container Principal -->
    <div class="modal-content">
        <!-- 3 Divs de Resultados -->
        <div class="results-container">
            <!-- Div 1: Estimativa Inicial -->
            <div class="result-card estimate">
                <h3>Estimativa Inicial</h3>
                <div class="value">R$ 2.400,00</div>
            </div>
            
            <!-- Div 2: Cálculo Recomendado -->
            <div class="result-card recommended">
                <h3>Recomendado</h3>
                <div class="value">R$ 3.962,68</div>
            </div>
            
            <!-- Div 3: Cálculo Alternativo -->
            <div class="result-card alternative">
                <h3>Alternativo</h3>
                <div class="value">R$ 4.202,52</div>
            </div>
        </div>
    </div>
</div>
```

---

## 🎨 **ESPECIFICAÇÕES DE DESIGN**

### **🌈 PALETA DE CORES**
```css
:root {
    --imediato-dark-blue: #003366;
    --imediato-light-blue: #0099CC;
    --imediato-white: #FFFFFF;
    --imediato-gray: #F8F9FA;
    --imediato-text: #333333;
    --imediato-text-light: #666666;
    --imediato-border: #E0E0E0;
    --imediato-shadow: rgba(0, 51, 102, 0.1);
    --imediato-shadow-hover: rgba(0, 51, 102, 0.2);
}
```

### **📝 TIPOGRAFIA**
- **Fonte Principal**: `Titillium Web` (Google Fonts)
- **Pesos**: 300, 400, 600, 700

### **🖼️ LOGOTIPO**
- **Fonte**: `https://www.segurosimediato.com.br/assets/logo.png`
- **Posicionamento**: Header do modal
- **Tamanho**: Max-width 180px

---

## 🎭 **COMPORTAMENTO DO MODAL**

### **🔄 FLUXO DE EXECUÇÃO**
1. **Usuário preenche formulário** → Página principal
2. **Clica "Efetuar Cálculo"** → Modal abre instantaneamente
3. **Barra de progresso** → Atualiza em tempo real
4. **3 divs de resultados** → Aparecem conforme dados chegam
5. **Modal permanece aberto** → Até usuário fechar

### **📊 ESTRUTURA DOS 3 DIVS**
```css
.results-container {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr; /* Desktop: 3 colunas */
    gap: 2rem;
    padding: 2rem;
}

/* Mobile: 3 linhas verticais */
@media (max-width: 768px) {
    .results-container {
        grid-template-columns: 1fr;
    }
}
```

### **🎨 DESIGN DOS CARDS**
- **Estimativa Inicial**: Borda azul claro, ícone gráfico
- **Recomendado**: Borda azul escuro, ícone estrela, badge "Recomendado"
- **Alternativo**: Borda cinza, ícone troca, badge "Alternativo"

---

## 🔧 **IMPLEMENTAÇÃO TÉCNICA**

### **📁 ESTRUTURA DE ARQUIVOS**
```
modal-rpa-separado-v6.2.0/
├── index.html                 # Página principal (formulário)
├── modal-progress.html        # Modal de progresso
├── css/
│   ├── main-page.css         # Estilos da página principal
│   ├── modal-progress.css    # Estilos do modal
│   └── imediato-brand.css    # Cores e tipografia
├── js/
│   ├── main-page.js          # Lógica da página principal
│   ├── modal-progress.js     # Lógica do modal
│   └── rpa-integration.js    # Integração com RPA
└── assets/
    └── logo.png              # Logotipo local (backup)
```

### **🎯 INTEGRAÇÃO RPA**
```javascript
// Página principal
class MainPageRPA {
    async handleFormSubmit() {
        // Validar formulário
        // Coletar dados
        // Abrir modal
        this.openProgressModal();
        // Iniciar RPA
        this.startRPA();
    }
    
    openProgressModal() {
        // Criar modal dinamicamente
        // Injetar HTML do modal
        // Mostrar modal
    }
}

// Modal de progresso
class ProgressModalRPA {
    constructor() {
        this.setupProgressBar();
        this.setupResultsCards();
    }
    
    updateProgress(data) {
        // Atualizar barra de progresso
        // Atualizar 3 divs de resultados
    }
}
```

---

## 📱 **RESPONSIVIDADE**

### **🖥️ DESKTOP (1200px+)**
- **Modal**: Centralizado, largura fixa
- **3 Divs**: Grid 3 colunas
- **Barra de Progresso**: Largura total do modal

### **💻 TABLET (768px-1199px)**
- **Modal**: Largura adaptada
- **3 Divs**: Grid 2 colunas (estimativa + 2 cálculos)
- **Barra de Progresso**: Mantida

### **📱 MOBILE (até 767px)**
- **Modal**: Largura total da tela
- **3 Divs**: Grid 1 coluna (vertical)
- **Barra de Progresso**: Compacta

---

## 🎭 **ANIMAÇÕES E TRANSIÇÕES**

### **✨ ANIMAÇÕES DO MODAL**
```css
/* Abertura do modal */
@keyframes modalSlideIn {
    from {
        opacity: 0;
        transform: scale(0.9) translateY(-50px);
    }
    to {
        opacity: 1;
        transform: scale(1) translateY(0);
    }
}

/* Barra de progresso */
@keyframes progressShimmer {
    0% { background-position: -200% 0; }
    100% { background-position: 200% 0; }
}

/* Cards de resultados */
@keyframes cardSlideIn {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}
```

### **🎯 CLASSES DE ANIMAÇÃO**
- `.modal-slide-in`: Entrada do modal
- `.progress-shimmer`: Brilho na barra de progresso
- `.card-slide-in`: Entrada dos cards
- `.fade-in`: Aparição suave dos valores

---

## 🔧 **FUNCIONALIDADES ESPECÍFICAS**

### **📊 BARRA DE PROGRESSO**
- **Posição**: Fixa no topo do modal
- **Informações**: Porcentagem + fase atual
- **Animação**: Shimmer effect
- **Cores**: Gradiente azul Imediato

### **💰 3 DIVS DE RESULTADOS**
- **Div 1**: Estimativa Inicial (Tela 5)
- **Div 2**: Cálculo Recomendado (Tela 15)
- **Div 3**: Cálculo Alternativo (Tela 15)
- **Atualização**: Em tempo real conforme dados chegam

### **🎨 IDENTIDADE VISUAL**
- **Logotipo**: Header do modal
- **Cores**: Paleta oficial Imediato
- **Tipografia**: Titillium Web
- **Gradientes**: Azul escuro → Azul claro

---

## 🚀 **CRONOGRAMA DE IMPLEMENTAÇÃO**

### **📅 FASE 1: ESTRUTURA BASE (1 dia)**
- [ ] Criar página principal com formulário
- [ ] Criar modal de progresso
- [ ] Configurar CSS base
- [ ] Implementar JavaScript base

### **📅 FASE 2: MODAL E PROGRESSO (1 dia)**
- [ ] Implementar abertura do modal
- [ ] Criar barra de progresso
- [ ] Configurar 3 divs de resultados
- [ ] Aplicar identidade visual

### **📅 FASE 3: INTEGRAÇÃO RPA (1 dia)**
- [ ] Integrar com API RPA
- [ ] Implementar polling de progresso
- [ ] Atualizar resultados em tempo real
- [ ] Tratamento de erros

### **📅 FASE 4: ANIMAÇÕES E RESPONSIVIDADE (1 dia)**
- [ ] Implementar animações
- [ ] Configurar responsividade
- [ ] Testes em diferentes dispositivos
- [ ] Ajustes finais

---

## ✅ **CHECKLIST DE QUALIDADE**

### **🎨 DESIGN**
- [ ] Modal separado da página principal
- [ ] Barra de progresso fixa no topo
- [ ] 3 divs conforme especificação
- [ ] Identidade visual Imediato aplicada
- [ ] Logotipo integrado

### **🎭 FUNCIONALIDADE**
- [ ] Modal abre após "Efetuar Cálculo"
- [ ] Barra de progresso atualiza em tempo real
- [ ] 3 divs mostram valores corretos
- [ ] Integração com RPA funcionando
- [ ] Tratamento de erros

### **📱 RESPONSIVIDADE**
- [ ] Desktop: Modal centralizado, 3 colunas
- [ ] Tablet: Modal adaptado, 2 colunas
- [ ] Mobile: Modal full-width, 1 coluna
- [ ] Touch-friendly em mobile

---

## 🎯 **DIFERENÇAS DO PROJETO ANTERIOR**

### **❌ V6.1.0 (Anterior)**
- Formulário + Progresso + Resultados na mesma página
- Elementos aparecem/desaparecem dinamicamente
- Barra de progresso fixa no topo da página

### **✅ V6.2.0 (Novo)**
- **Página principal**: Apenas formulário
- **Modal separado**: Abre após clicar "Efetuar Cálculo"
- **Barra de progresso**: Fixa no topo do modal
- **3 divs**: Sempre visíveis no modal
- **Experiência**: Mais limpa e focada

---

## 📚 **RECURSOS E REFERÊNCIAS**

### **🎨 DESIGN SYSTEM**
- **Cores**: Paleta oficial Imediato Seguros
- **Tipografia**: Titillium Web (Google Fonts)
- **Ícones**: Font Awesome 6
- **Logotipo**: https://www.segurosimediato.com.br/assets/logo.png

### **🔗 TECNOLOGIAS**
- **HTML5**: Estrutura semântica
- **CSS3**: Grid, Flexbox, Animações
- **JavaScript ES6+**: Classes, Async/Await
- **API RPA**: Integração com backend

---

## 🎯 **PRÓXIMOS PASSOS**

1. **Aprovação do Conceito**: Confirmar arquitetura do modal separado
2. **Implementação**: Desenvolver componentes
3. **Testes**: Validar funcionalidade
4. **Deploy**: Implementar em produção

---

**📝 Documento criado em: Janeiro 2025**  
**👨‍💻 Versão: 6.2.0**  
**🎨 Status: Planejamento Completo**



