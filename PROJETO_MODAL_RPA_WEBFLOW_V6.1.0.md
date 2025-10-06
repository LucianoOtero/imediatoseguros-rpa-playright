# PROJETO MODAL RPA WEBFLOW V6.1.0

**Data**: 03 de Outubro de 2025  
**Versão**: 6.1.0  
**Cliente**: Imediato Soluções em Seguros  
**Desenvolvedor**: Web Designer  
**Prazo**: 5 horas de desenvolvimento  
**Prioridade**: MÁXIMA  

---

## 🎯 **OBJETIVO DO PROJETO**

Desenvolver uma interface moderna e responsiva para substituir o SweetAlert2 atual, com foco na integração perfeita com Webflow e exibição em tempo real das estimativas iniciais e cálculos finais durante a execução do RPA.

---

## 📋 **REQUISITOS FUNCIONAIS**

### **✅ FUNCIONALIDADES OBRIGATÓRIAS**
1. **Barra de Progresso Fixa**: Topo da página, 0-100%, fase atual centralizada
2. **Layout Responsivo**: 
   - Desktop: 1/3 (estimativa) + 2/3 (2 cálculos finais)
   - Mobile: 3 divs verticais (estimativa + 2 cálculos)
3. **Integração Webflow**: Via Embed Custom Code
4. **Tempo Real**: Atualizações a cada 2 segundos
5. **Animações Elegantes**: Transições suaves e profissionais
6. **Compatibilidade**: Funcionar com API V6.0.0 existente

### **🔧 FUNCIONALIDADES DESEJÁVEIS**
1. **Temas**: Suporte a tema claro/escuro
2. **Acessibilidade**: Suporte a leitores de tela
3. **Cache Local**: Armazenar dados temporariamente
4. **Métricas**: Coleta de dados de performance

---

## 🏗️ **ARQUITETURA TÉCNICA**

### **📁 ESTRUTURA DE ARQUIVOS**
```
webflow-rpa-modal-v6.1.0/
├── index.html                 # Página de demonstração
├── css/
│   ├── rpa-progress.css       # Estilos da barra de progresso
│   ├── rpa-results.css        # Estilos dos resultados
│   ├── rpa-animations.css     # Animações e transições
│   └── rpa-responsive.css     # Estilos responsivos
├── js/
│   ├── rpa-progress-tracker.js    # Monitoramento de progresso
│   ├── rpa-api-handler.js         # Integração com API
│   ├── rpa-webflow-integration.js # Integração Webflow
│   └── rpa-responsive-handler.js  # Gerenciamento responsivo
├── assets/
│   └── icons/                 # Ícones SVG personalizados
└── webflow-integration/
    ├── embed-code.html        # Código para Embed Webflow
    └── components/            # Componentes Webflow
```

### **🎨 TECNOLOGIAS RECOMENDADAS**
- **HTML5**: Estrutura semântica
- **CSS3**: Grid/Flexbox + Custom Properties
- **JavaScript ES6**: Classes e async/await
- **Font Awesome**: Ícones (v6.4.0)
- **Animate.css**: Animações elegantes (v4.1.1)

---

## 🎨 **ESPECIFICAÇÕES DE DESIGN**

### **🎯 PALETA DE CORES**
```css
:root {
    --primary-color: #2E7D32;      /* Verde principal */
    --secondary-color: #4CAF50;     /* Verde secundário */
    --accent-color: #FF9800;        /* Laranja destaque */
    --success-color: #4CAF50;        /* Verde sucesso */
    --warning-color: #FF9800;       /* Laranja aviso */
    --error-color: #F44336;         /* Vermelho erro */
    --text-color: #333333;          /* Texto principal */
    --text-light: #666666;          /* Texto secundário */
    --bg-color: #f8f9fa;            /* Fundo principal */
    --card-bg: #ffffff;             /* Fundo cards */
    --border-color: #e0e0e0;        /* Bordas */
    --shadow-light: 0 2px 4px rgba(0,0,0,0.1);
    --shadow-medium: 0 4px 8px rgba(0,0,0,0.15);
    --shadow-heavy: 0 8px 16px rgba(0,0,0,0.2);
}
```

### **📱 BREAKPOINTS RESPONSIVOS**
```css
/* Mobile First */
@media (max-width: 767px) { /* Mobile */ }
@media (min-width: 768px) { /* Tablet */ }
@media (min-width: 1024px) { /* Desktop */ }
@media (min-width: 1440px) { /* Large Desktop */ }
```

### **🎭 ANIMAÇÕES PRINCIPAIS**
- **Progress Bar**: Transição suave 0.5s ease-in-out
- **Cards**: Slide-in + hover effects (translateY -5px)
- **Values**: Pulse animation on update (0.3s)
- **Responsive**: Smooth transitions (0.3s ease-in-out)

---

## 📋 **REFERÊNCIA AO HTML ATUAL**

### **🎯 FORMULÁRIO SIMPLIFICADO**

**IMPORTANTE**: O web designer deve criar um formulário simplificado com apenas os campos essenciais:
- ✅ **8 campos apenas**: CPF, Nome, Placa, Marca, CEP, Data Nascimento, Estado Civil, Sexo
- ✅ **Botão "Calcular Seguro"** (id: `btnCalculate`)
- ✅ **Dados fixos**: Todos os demais campos serão hardcoded no JavaScript
- ✅ **Valores do parametros.json**: Usados como referência para dados fixos

#### **📋 CAMPOS DO FORMULÁRIO SIMPLIFICADO**
```html
<form id="rpa-form" class="rpa-form">
    <!-- Dados Pessoais -->
    <div class="form-group">
        <label for="cpf">CPF *</label>
        <input type="text" id="cpf" name="cpf" required maxlength="11" placeholder="00000000000">
    </div>
    
    <div class="form-group">
        <label for="nome">Nome Completo *</label>
        <input type="text" id="nome" name="nome" required placeholder="Seu nome completo">
    </div>
    
    <div class="form-group">
        <label for="data_nascimento">Data de Nascimento *</label>
        <input type="text" id="data_nascimento" name="data_nascimento" required placeholder="DD/MM/AAAA">
    </div>
    
    <div class="form-group">
        <label for="sexo">Sexo *</label>
        <select id="sexo" name="sexo" required>
            <option value="Masculino">Masculino</option>
            <option value="Feminino">Feminino</option>
        </select>
    </div>
    
    <div class="form-group">
        <label for="estado_civil">Estado Civil *</label>
        <select id="estado_civil" name="estado_civil" required>
            <option value="Casado ou Uniao Estavel">Casado ou União Estável</option>
            <option value="Solteiro">Solteiro</option>
            <option value="Divorciado">Divorciado</option>
            <option value="Viuvo">Viúvo</option>
        </select>
    </div>
    
    <!-- Dados do Veículo -->
    <div class="form-group">
        <label for="placa">Placa do Veículo *</label>
        <input type="text" id="placa" name="placa" required maxlength="7" placeholder="ABC1234" style="text-transform: uppercase">
    </div>
    
    <div class="form-group">
        <label for="marca">Marca *</label>
        <input type="text" id="marca" name="marca" required placeholder="Ex: TOYOTA">
    </div>
    
    <!-- Dados de Endereço -->
    <div class="form-group">
        <label for="cep">CEP *</label>
        <input type="text" id="cep" name="cep" required maxlength="9" placeholder="00000-000">
    </div>
    
    <!-- Botão de Ação -->
    <div class="form-actions">
        <button type="submit" class="btn-calculate" id="btnCalculate">
            <i class="fas fa-calculator"></i>
            Calcular Seguro
        </button>
    </div>
</form>
```

#### **📋 DADOS FIXOS NO JAVASCRIPT**
Todos os demais campos serão hardcoded no JavaScript com valores do `parametros.json`:
```javascript
// Dados fixos do parametros.json
const FIXED_DATA = {
    // Configuração
    configuracao: {
        log: true,
        display: true,
        log_rotacao_dias: 90,
        log_nivel: "INFO",
        tempo_estabilizacao: 0.5,
        tempo_carregamento: 0.5,
        tempo_estabilizacao_tela5: 2,
        tempo_carregamento_tela5: 5,
        tempo_estabilizacao_tela15: 3,
        tempo_carregamento_tela15: 5,
        inserir_log: true,
        visualizar_mensagens: true,
        eliminar_tentativas_inuteis: true,
        modo_silencioso: false
    },
    
    // Autenticação
    autenticacao: {
        email_login: "aleximediatoseguros@gmail.com",
        senha_login: "Lrotero1$",
        manter_login_atual: true
    },
    
    // URL
    url: "https://www.app.tosegurado.com.br/imediatosolucoes",
    
    // Dados do Veículo (fixos)
    modelo: "COROLLA XEI 1.8/1.8 FLEX 16V MEC",
    ano: "2009",
    zero_km: false,
    combustivel: "Flex",
    veiculo_segurado: "Não",
    tipo_veiculo: "carro",
    
    // Dados de Endereço (fixos)
    endereco_completo: "Rua Serra de Botucatu, 410 APTO 11 - São Paulo, SP",
    uso_veiculo: "Pessoal",
    endereco: "Rua Serra de Botucatu, Tatuapé - São Paulo/SP",
    
    // Dados Pessoais (fixos)
    email: "alex.kaminski@imediatoseguros.com.br",
    celular: "11953288466",
    
    // Dados do Condutor (fixos)
    condutor_principal: true,
    nome_condutor: "SANDRA LOUREIRO",
    cpf_condutor: "25151787829",
    data_nascimento_condutor: "28/08/1975",
    sexo_condutor: "Feminino",
    estado_civil_condutor: "Casado ou Uniao Estavel",
    
    // Configurações de Estacionamento (fixas)
    local_de_trabalho: false,
    estacionamento_proprio_local_de_trabalho: false,
    local_de_estudo: false,
    estacionamento_proprio_local_de_estudo: false,
    garagem_residencia: true,
    portao_eletronico: "Eletronico",
    
    // Configurações Adicionais (fixas)
    kit_gas: false,
    blindado: false,
    financiado: false,
    reside_18_26: "Não",
    continuar_com_corretor_anterior: true
};
```

### **🎯 SIMULAÇÃO DA PÁGINA WEBFLOW**

O formulário simplificado deve ser usado como **simulação da página Webflow** que será desenvolvida posteriormente. O web designer deve:

1. **Criar formulário simplificado** com apenas 8 campos essenciais
2. **Manter o botão** "Calcular Seguro" com id `btnCalculate`
3. **Hardcodar dados fixos** no JavaScript usando valores do `parametros.json`
4. **Usar como referência** para desenvolvimento da página Webflow

---

## 📋 **ESTRUTURA HTML BASE**

### **🎯 HTML PRINCIPAL**
```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RPA Progress Tracker V6.1.0</title>
    
    <!-- CSS -->
    <link rel="stylesheet" href="css/rpa-progress.css">
    <link rel="stylesheet" href="css/rpa-results.css">
    <link rel="stylesheet" href="css/rpa-animations.css">
    <link rel="stylesheet" href="css/rpa-responsive.css">
    
    <!-- External Libraries -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css">
</head>
<body>
    <!-- Barra de Progresso Fixa no Topo -->
    <div class="rpa-progress-container fixed-top">
        <div class="rpa-progress-bar">
            <div class="rpa-progress-fill" id="rpaProgressFill"></div>
            <div class="rpa-progress-text" id="rpaProgressText">0%</div>
            <div class="rpa-current-phase" id="rpaCurrentPhase">Iniciando RPA...</div>
        </div>
    </div>

    <!-- Container Principal -->
    <div class="rpa-main-container">
        <!-- Seção de Resultados -->
        <div class="rpa-results-section" id="rpaResultsSection" style="display: none;">
            <!-- Estimativa Inicial -->
            <div class="rpa-estimate-card" id="rpaEstimateCard">
                <div class="rpa-card-header">
                    <i class="fas fa-chart-line"></i>
                    <h3>Estimativa Inicial</h3>
                </div>
                <div class="rpa-card-content">
                    <div class="rpa-value" id="rpaInitialEstimate">-</div>
                    <div class="rpa-subtitle">Tela 5 - Primeira Cotação</div>
                </div>
            </div>

            <!-- Cálculos Finais -->
            <div class="rpa-calculations-container" id="rpaCalculationsContainer">
                <!-- Cálculo Recomendado -->
                <div class="rpa-calculation-card recommended" id="rpaRecommendedCard">
                    <div class="rpa-card-header">
                        <i class="fas fa-star"></i>
                        <h3>Recomendado</h3>
                        <span class="rpa-badge">Melhor Custo-Benefício</span>
                    </div>
                    <div class="rpa-card-content">
                        <div class="rpa-value" id="rpaRecommendedValue">-</div>
                        <div class="rpa-subtitle">Tela 15 - Cálculo Final</div>
                    </div>
                </div>

                <!-- Cálculo Alternativo -->
                <div class="rpa-calculation-card alternative" id="rpaAlternativeCard">
                    <div class="rpa-card-header">
                        <i class="fas fa-exchange-alt"></i>
                        <h3>Alternativo</h3>
                        <span class="rpa-badge">Opção Adicional</span>
                    </div>
                    <div class="rpa-card-content">
                        <div class="rpa-value" id="rpaAlternativeValue">-</div>
                        <div class="rpa-subtitle">Tela 15 - Cálculo Final</div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Seção de Fases (Opcional - Collapsible) -->
        <div class="rpa-phases-section" id="rpaPhasesSection">
            <button class="rpa-toggle-phases" id="rpaTogglePhases">
                <i class="fas fa-chevron-down"></i>
                Ver Detalhes das Fases
            </button>
            <div class="rpa-phases-list" id="rpaPhasesList">
                <!-- 15 fases serão geradas dinamicamente -->
            </div>
        </div>
    </div>

    <!-- Scripts -->
    <script src="js/rpa-progress-tracker.js"></script>
    <script src="js/rpa-api-handler.js"></script>
    <script src="js/rpa-webflow-integration.js"></script>
    <script src="js/rpa-responsive-handler.js"></script>
</body>
</html>
```

---

## 🎨 **ESPECIFICAÇÕES CSS**

### **📊 LAYOUT DESKTOP (1/3 + 2/3)**
```css
.rpa-results-section {
    display: grid;
    grid-template-columns: 1fr 2fr;
    gap: 2rem;
    padding: 2rem;
    max-width: 1200px;
    margin: 0 auto;
}

.rpa-estimate-card {
    grid-column: 1;
    background: var(--card-bg);
    border-radius: 12px;
    padding: 1.5rem;
    box-shadow: var(--shadow-light);
    transition: all 0.3s ease;
}

.rpa-calculations-container {
    grid-column: 2;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
}

.rpa-calculation-card {
    background: var(--card-bg);
    border-radius: 12px;
    padding: 1.5rem;
    box-shadow: var(--shadow-light);
    transition: all 0.3s ease;
}

.rpa-calculation-card:hover {
    transform: translateY(-5px);
    box-shadow: var(--shadow-medium);
}
```

### **📱 LAYOUT MOBILE (3 DIVS VERTICAIS)**
```css
@media (max-width: 767px) {
    .rpa-results-section {
        grid-template-columns: 1fr;
        gap: 1rem;
        padding: 1rem;
    }
    
    .rpa-calculations-container {
        grid-template-columns: 1fr;
    }
    
    .rpa-estimate-card,
    .rpa-calculation-card {
        padding: 1rem;
    }
}
```

### **🎭 ANIMAÇÕES CSS**
```css
/* Progress Bar Animation */
.rpa-progress-fill {
    transition: width 0.5s ease-in-out;
    background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
    border-radius: 2px;
}

/* Card Animations */
.rpa-estimate-card,
.rpa-calculation-card {
    animation: slideInUp 0.6s ease-out;
}

@keyframes slideInUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* Value Updates */
.rpa-value {
    animation: pulse 0.3s ease-in-out;
}

@keyframes pulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.05); }
    100% { transform: scale(1); }
}
```

---

## ⚡ **ESPECIFICAÇÕES JAVASCRIPT**

### **📊 PROGRESS TRACKER**
```javascript
class RPAProgressTracker {
    constructor() {
        this.progressFill = document.getElementById('rpaProgressFill');
        this.progressText = document.getElementById('rpaProgressText');
        this.currentPhase = document.getElementById('rpaCurrentPhase');
        this.sessionId = null;
        this.progressInterval = null;
    }

    startTracking(sessionId) {
        this.sessionId = sessionId;
        this.progressInterval = setInterval(() => {
            this.checkProgress();
        }, 2000);
    }

    async checkProgress() {
        try {
            const response = await fetch(`/api/rpa/progress/${this.sessionId}`);
            const data = await response.json();
            
            if (data.success) {
                this.updateProgress(data.progress);
            }
        } catch (error) {
            console.error('Erro ao verificar progresso:', error);
        }
    }

    updateProgress(progressData) {
        const { percentual, etapa_atual, mensagem } = progressData;
        
        // Animate progress bar
        this.progressFill.style.width = `${percentual}%`;
        this.progressText.textContent = `${Math.round(percentual)}%`;
        this.currentPhase.textContent = `Fase ${etapa_atual}: ${mensagem}`;
        
        // Add animation class
        this.progressFill.classList.add('animate__animated', 'animate__pulse');
        
        // Check if completed
        if (progressData.status === 'success' || progressData.status === 'concluido') {
            this.completeTracking(progressData);
        }
    }

    completeTracking(progressData) {
        this.stopTracking();
        
        // Update to 100%
        this.progressFill.style.width = '100%';
        this.progressText.textContent = '100%';
        this.currentPhase.textContent = 'Processamento Concluído';
        
        // Show results
        this.showResults(progressData);
    }

    stopTracking() {
        if (this.progressInterval) {
            clearInterval(this.progressInterval);
            this.progressInterval = null;
        }
    }

    showResults(progressData) {
        const resultsSection = document.getElementById('rpaResultsSection');
        resultsSection.style.display = 'block';
        resultsSection.classList.add('animate__animated', 'animate__fadeInUp');
        
        // Update values
        const initialEstimate = progressData.estimativas?.dados?.valor_estimativa;
        const finalCalculation = progressData.resultados_finais?.dados?.valor_final;
        
        if (initialEstimate) {
            document.getElementById('rpaInitialEstimate').textContent = `R$ ${initialEstimate}`;
        }
        
        if (finalCalculation) {
            document.getElementById('rpaRecommendedValue').textContent = `R$ ${finalCalculation}`;
            document.getElementById('rpaAlternativeValue').textContent = `R$ ${finalCalculation * 1.1}`; // Exemplo
        }
    }
}
```

### **🌐 WEBFLOW INTEGRATION**
```javascript
class WebflowRPAIntegration {
    constructor() {
        this.init();
    }

    init() {
        // Aguardar Webflow carregar
        if (window.Webflow) {
            this.injectRPAComponents();
        } else {
            window.addEventListener('load', () => {
                this.injectRPAComponents();
            });
        }
    }

    injectRPAComponents() {
        // Injetar CSS
        this.injectCSS();
        
        // Injetar HTML
        this.injectHTML();
        
        // Inicializar componentes
        this.initializeComponents();
    }

    injectCSS() {
        const css = `
            .rpa-progress-container {
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                z-index: 9999;
                background: white;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            
            .rpa-progress-bar {
                height: 4px;
                background: #e0e0e0;
                position: relative;
                overflow: hidden;
            }
            
            .rpa-progress-fill {
                height: 100%;
                background: linear-gradient(90deg, #4CAF50, #8BC34A);
                width: 0%;
                transition: width 0.5s ease-in-out;
            }
            
            .rpa-results-grid {
                display: grid;
                grid-template-columns: 1fr 2fr;
                gap: 2rem;
                padding: 2rem;
                max-width: 1200px;
                margin: 0 auto;
            }
            
            @media (max-width: 767px) {
                .rpa-results-grid {
                    grid-template-columns: 1fr;
                }
            }
        `;
        
        const style = document.createElement('style');
        style.textContent = css;
        document.head.appendChild(style);
    }

    injectHTML() {
        const container = document.getElementById('rpa-progress-container');
        if (!container) return;

        container.innerHTML = `
            <div class="rpa-progress-container">
                <div class="rpa-progress-bar">
                    <div class="rpa-progress-fill" id="rpaProgressFill"></div>
                </div>
                <div class="rpa-progress-info">
                    <span id="rpaProgressText">0%</span>
                    <span id="rpaCurrentPhase">Iniciando RPA...</span>
                </div>
            </div>
            
            <div class="rpa-results-section" id="rpaResultsSection" style="display: none;">
                <div class="rpa-results-grid">
                    <div class="rpa-estimate-card">
                        <h3>Estimativa Inicial</h3>
                        <div class="rpa-value" id="rpaInitialEstimate">-</div>
                    </div>
                    
                    <div class="rpa-calculations-container">
                        <div class="rpa-calculation-card recommended">
                            <h3>Recomendado</h3>
                            <div class="rpa-value" id="rpaRecommendedValue">-</div>
                        </div>
                        
                        <div class="rpa-calculation-card alternative">
                            <h3>Alternativo</h3>
                            <div class="rpa-value" id="rpaAlternativeValue">-</div>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    initializeComponents() {
        // Inicializar progress tracker
        this.progressTracker = new RPAProgressTracker();
        
        // Inicializar API handler
        this.apiHandler = new RPAApiHandler();
        
        // Configurar event listeners
        this.setupEventListeners();
    }

    setupEventListeners() {
        // Interceptar cliques em botões de cálculo
        document.addEventListener('click', (e) => {
            if (e.target.matches('[data-rpa-trigger]') || e.target.id === 'btnCalculate') {
                e.preventDefault();
                this.startRPAProcess(e.target);
            }
        });
    }

    async startRPAProcess(triggerElement) {
        try {
            // Coletar dados do formulário Webflow
            const formData = this.collectWebflowFormData(triggerElement);
            
            // Iniciar RPA
            const sessionId = await this.apiHandler.startRPA(formData);
            
            // Mostrar progresso
            this.progressTracker.startTracking(sessionId);
            
        } catch (error) {
            console.error('Erro ao iniciar RPA:', error);
            this.showError(error.message);
        }
    }

    collectWebflowFormData(triggerElement) {
        // Coletar dados do formulário Webflow
        const form = triggerElement.closest('form');
        const formData = new FormData(form);
        const data = {};
        
        for (let [key, value] of formData.entries()) {
            data[key] = value;
        }
        
        return data;
    }
}

// Inicializar quando DOM estiver pronto
document.addEventListener('DOMContentLoaded', () => {
    new WebflowRPAIntegration();
});
```

---

## 📄 **JAVASCRIPT PARA INJEÇÃO NO WEBFLOW**

### **🎯 ARQUIVO SEPARADO: webflow-rpa-injection.js**

**IMPORTANTE**: O web designer deve criar um arquivo separado `webflow-rpa-injection.js` com referências explícitas a cada campo do formulário para facilitar a renomeação posterior.

```javascript
/**
 * WEBFLOW RPA INJECTION SCRIPT V6.1.0
 * 
 * Este arquivo contém referências explícitas a todos os campos do formulário
 * para facilitar a renomeação posterior no Webflow.
 * 
 * FORMULÁRIO SIMPLIFICADO (8 campos apenas):
 * - Dados Pessoais: cpf, nome, data_nascimento, sexo, estado_civil
 * - Dados do Veículo: placa, marca
 * - Dados de Endereço: cep
 * - Botão de Ação: btnCalculate
 * 
 * DADOS FIXOS (hardcoded no JavaScript):
 * - Todos os demais campos do parametros.json são fixos
 * - Configuração, autenticação, URL, modelo, ano, combustivel, etc.
 * - Dados do condutor, estacionamento, configurações adicionais
 */

class WebflowRPAInjection {
    constructor() {
        // Mapeamento de campos do formulário simplificado
        this.fieldMapping = {
            // Campos do formulário (8 campos apenas)
            cpf: 'cpf',
            nome: 'nome',
            data_nascimento: 'data_nascimento',
            sexo: 'sexo',
            estado_civil: 'estado_civil',
            placa: 'placa',
            marca: 'marca',
            cep: 'cep',
            
            // Botão de Ação
            btnCalculate: 'btnCalculate'
        };
        
        // Dados fixos do parametros.json
        this.fixedData = {
            // Configuração
            configuracao: {
                log: true,
                display: true,
                log_rotacao_dias: 90,
                log_nivel: "INFO",
                tempo_estabilizacao: 0.5,
                tempo_carregamento: 0.5,
                tempo_estabilizacao_tela5: 2,
                tempo_carregamento_tela5: 5,
                tempo_estabilizacao_tela15: 3,
                tempo_carregamento_tela15: 5,
                inserir_log: true,
                visualizar_mensagens: true,
                eliminar_tentativas_inuteis: true,
                modo_silencioso: false
            },
            
            // Autenticação
            autenticacao: {
                email_login: "aleximediatoseguros@gmail.com",
                senha_login: "Lrotero1$",
                manter_login_atual: true
            },
            
            // URL
            url: "https://www.app.tosegurado.com.br/imediatosolucoes",
            
            // Dados do Veículo (fixos)
            modelo: "COROLLA XEI 1.8/1.8 FLEX 16V MEC",
            ano: "2009",
            zero_km: false,
            combustivel: "Flex",
            veiculo_segurado: "Não",
            tipo_veiculo: "carro",
            
            // Dados de Endereço (fixos)
            endereco_completo: "Rua Serra de Botucatu, 410 APTO 11 - São Paulo, SP",
            uso_veiculo: "Pessoal",
            endereco: "Rua Serra de Botucatu, Tatuapé - São Paulo/SP",
            
            // Dados Pessoais (fixos)
            email: "alex.kaminski@imediatoseguros.com.br",
            celular: "11953288466",
            
            // Dados do Condutor (fixos)
            condutor_principal: true,
            nome_condutor: "SANDRA LOUREIRO",
            cpf_condutor: "25151787829",
            data_nascimento_condutor: "28/08/1975",
            sexo_condutor: "Feminino",
            estado_civil_condutor: "Casado ou Uniao Estavel",
            
            // Configurações de Estacionamento (fixas)
            local_de_trabalho: false,
            estacionamento_proprio_local_de_trabalho: false,
            local_de_estudo: false,
            estacionamento_proprio_local_de_estudo: false,
            garagem_residencia: true,
            portao_eletronico: "Eletronico",
            
            // Configurações Adicionais (fixas)
            kit_gas: false,
            blindado: false,
            financiado: false,
            reside_18_26: "Não",
            continuar_com_corretor_anterior: true
        };
        
        this.init();
    }

    init() {
        // Aguardar Webflow carregar
        if (window.Webflow) {
            this.injectRPAComponents();
        } else {
            window.addEventListener('load', () => {
                this.injectRPAComponents();
            });
        }
    }

    injectRPAComponents() {
        // Injetar CSS
        this.injectCSS();
        
        // Injetar HTML
        this.injectHTML();
        
        // Inicializar componentes
        this.initializeComponents();
    }

    injectCSS() {
        const css = `
            .rpa-progress-container {
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                z-index: 9999;
                background: white;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            
            .rpa-progress-bar {
                height: 4px;
                background: #e0e0e0;
                position: relative;
                overflow: hidden;
            }
            
            .rpa-progress-fill {
                height: 100%;
                background: linear-gradient(90deg, #4CAF50, #8BC34A);
                width: 0%;
                transition: width 0.5s ease-in-out;
            }
            
            .rpa-progress-info {
                padding: 1rem;
                text-align: center;
                background: white;
                border-bottom: 1px solid #e0e0e0;
            }
            
            .rpa-progress-text {
                font-weight: bold;
                color: #2E7D32;
                margin-right: 1rem;
            }
            
            .rpa-current-phase {
                color: #666;
                font-size: 0.9rem;
            }
            
            .rpa-results-section {
                margin-top: 80px;
                padding: 2rem;
                background: #f8f9fa;
                min-height: 100vh;
            }
            
            .rpa-results-grid {
                display: grid;
                grid-template-columns: 1fr 2fr;
                gap: 2rem;
                max-width: 1200px;
                margin: 0 auto;
            }
            
            .rpa-estimate-card,
            .rpa-calculation-card {
                background: white;
                border-radius: 12px;
                padding: 1.5rem;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                transition: all 0.3s ease;
            }
            
            .rpa-estimate-card:hover,
            .rpa-calculation-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 8px 16px rgba(0,0,0,0.15);
            }
            
            .rpa-calculations-container {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 1rem;
            }
            
            .rpa-card-header {
                display: flex;
                align-items: center;
                margin-bottom: 1rem;
            }
            
            .rpa-card-header i {
                margin-right: 0.5rem;
                color: #4CAF50;
            }
            
            .rpa-card-header h3 {
                margin: 0;
                color: #333;
            }
            
            .rpa-badge {
                background: #FF9800;
                color: white;
                padding: 0.25rem 0.5rem;
                border-radius: 4px;
                font-size: 0.8rem;
                margin-left: auto;
            }
            
            .rpa-value {
                font-size: 2rem;
                font-weight: bold;
                color: #2E7D32;
                margin-bottom: 0.5rem;
            }
            
            .rpa-subtitle {
                color: #666;
                font-size: 0.9rem;
            }
            
            @media (max-width: 767px) {
                .rpa-results-grid {
                    grid-template-columns: 1fr;
                }
                
                .rpa-calculations-container {
                    grid-template-columns: 1fr;
                }
                
                .rpa-estimate-card,
                .rpa-calculation-card {
                    padding: 1rem;
                }
                
                .rpa-value {
                    font-size: 1.5rem;
                }
            }
        `;
        
        const style = document.createElement('style');
        style.textContent = css;
        document.head.appendChild(style);
    }

    injectHTML() {
        const container = document.getElementById('rpa-progress-container');
        if (!container) return;

        container.innerHTML = `
            <div class="rpa-progress-container">
                <div class="rpa-progress-bar">
                    <div class="rpa-progress-fill" id="rpaProgressFill"></div>
                </div>
                <div class="rpa-progress-info">
                    <span class="rpa-progress-text" id="rpaProgressText">0%</span>
                    <span class="rpa-current-phase" id="rpaCurrentPhase">Iniciando RPA...</span>
                </div>
            </div>
            
            <div class="rpa-results-section" id="rpaResultsSection" style="display: none;">
                <div class="rpa-results-grid">
                    <div class="rpa-estimate-card">
                        <div class="rpa-card-header">
                            <i class="fas fa-chart-line"></i>
                            <h3>Estimativa Inicial</h3>
                        </div>
                        <div class="rpa-card-content">
                            <div class="rpa-value" id="rpaInitialEstimate">-</div>
                            <div class="rpa-subtitle">Tela 5 - Primeira Cotação</div>
                        </div>
                    </div>
                    
                    <div class="rpa-calculations-container">
                        <div class="rpa-calculation-card recommended">
                            <div class="rpa-card-header">
                                <i class="fas fa-star"></i>
                                <h3>Recomendado</h3>
                                <span class="rpa-badge">Melhor Custo-Benefício</span>
                            </div>
                            <div class="rpa-card-content">
                                <div class="rpa-value" id="rpaRecommendedValue">-</div>
                                <div class="rpa-subtitle">Tela 15 - Cálculo Final</div>
                            </div>
                        </div>
                        
                        <div class="rpa-calculation-card alternative">
                            <div class="rpa-card-header">
                                <i class="fas fa-exchange-alt"></i>
                                <h3>Alternativo</h3>
                                <span class="rpa-badge">Opção Adicional</span>
                            </div>
                            <div class="rpa-card-content">
                                <div class="rpa-value" id="rpaAlternativeValue">-</div>
                                <div class="rpa-subtitle">Tela 15 - Cálculo Final</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    initializeComponents() {
        // Inicializar progress tracker
        this.progressTracker = new RPAProgressTracker();
        
        // Inicializar API handler
        this.apiHandler = new RPAApiHandler();
        
        // Configurar event listeners
        this.setupEventListeners();
    }

    setupEventListeners() {
        // Interceptar cliques em botões de cálculo
        document.addEventListener('click', (e) => {
            // Suporte para botão atual (btnCalculate) e futuro (data-rpa-trigger)
            if (e.target.id === this.fieldMapping.btnCalculate || e.target.matches('[data-rpa-trigger]')) {
                e.preventDefault();
                this.startRPAProcess(e.target);
            }
        });
    }

    async startRPAProcess(triggerElement) {
        try {
            // Coletar dados do formulário Webflow
            const formData = this.collectWebflowFormData(triggerElement);
            
            // Iniciar RPA
            const sessionId = await this.apiHandler.startRPA(formData);
            
            // Mostrar progresso
            this.progressTracker.startTracking(sessionId);
            
        } catch (error) {
            console.error('Erro ao iniciar RPA:', error);
            this.showError(error.message);
        }
    }

    collectWebflowFormData(triggerElement) {
        // Coletar dados do formulário Webflow (apenas 8 campos)
        const form = triggerElement.closest('form');
        const formData = new FormData(form);
        const data = {};
        
        // Mapear apenas os campos do formulário simplificado
        for (let [key, value] of formData.entries()) {
            if (this.fieldMapping[key]) {
                data[key] = value;
            }
        }
        
        // Mesclar com dados fixos do parametros.json
        const completeData = { ...this.fixedData, ...data };
        
        // Converter tipos de dados conforme necessário
        this.convertDataTypes(completeData);
        
        return completeData;
    }

    convertDataTypes(data) {
        // Converter strings booleanas para boolean
        const booleanFields = [
            'condutor_principal',
            'garagem_residencia',
            'local_de_trabalho',
            'estacionamento_proprio_local_de_trabalho',
            'local_de_estudo',
            'estacionamento_proprio_local_de_estudo',
            'zero_km',
            'kit_gas',
            'blindado',
            'financiado',
            'continuar_com_corretor_anterior'
        ];
        
        booleanFields.forEach(field => {
            if (data[field] !== undefined) {
                data[field] = data[field] === 'true';
            }
        });
    }

    showError(message) {
        // Mostrar erro de forma elegante
        const progressInfo = document.querySelector('.rpa-progress-info');
        if (progressInfo) {
            progressInfo.innerHTML = `
                <span style="color: #F44336;">
                    <i class="fas fa-exclamation-triangle"></i>
                    Erro: ${message}
                </span>
            `;
        }
    }
}

// Inicializar quando DOM estiver pronto
document.addEventListener('DOMContentLoaded', () => {
    new WebflowRPAInjection();
});
```

### **📋 INSTRUÇÕES PARA O WEB DESIGNER**

**IMPORTANTE**: O web designer deve:

1. **Criar arquivo separado** `webflow-rpa-injection.js` com o código acima
2. **Manter referências explícitas** a todos os campos do formulário
3. **Usar o mapeamento** `this.fieldMapping` para facilitar renomeação
4. **Documentar cada campo** com comentários explicativos
5. **Testar com formulário atual** antes de entregar

### **🔧 COMO RENOMEAR CAMPOS NO WEBFLOW**

Para renomear campos no Webflow, basta alterar o mapeamento dos 8 campos do formulário:

```javascript
// Exemplo de renomeação dos 8 campos do formulário
this.fieldMapping = {
    cpf: 'customer_cpf',              // Renomeado de 'cpf' para 'customer_cpf'
    nome: 'customer_name',           // Renomeado de 'nome' para 'customer_name'
    data_nascimento: 'birth_date',    // Renomeado de 'data_nascimento' para 'birth_date'
    sexo: 'gender',                   // Renomeado de 'sexo' para 'gender'
    estado_civil: 'marital_status',   // Renomeado de 'estado_civil' para 'marital_status'
    placa: 'vehicle_plate',           // Renomeado de 'placa' para 'vehicle_plate'
    marca: 'vehicle_brand',           // Renomeado de 'marca' para 'vehicle_brand'
    cep: 'zip_code',                  // Renomeado de 'cep' para 'zip_code'
    btnCalculate: 'calculate_button'  // Renomeado de 'btnCalculate' para 'calculate_button'
};
```

**IMPORTANTE**: Os dados fixos (`this.fixedData`) não precisam ser renomeados, pois são hardcoded no JavaScript.

---

## 🔧 **INTEGRAÇÃO COM WEBFLOW**

### **📝 MÉTODO RECOMENDADO: EMBED CUSTOM CODE**

#### **1. Código para Embed Webflow**
```html
<!-- Webflow Embed Custom Code -->
<div id="rpa-progress-container"></div>

<!-- CSS -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/seu-repo/rpa-progress.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/seu-repo/rpa-animations.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/seu-repo/rpa-responsive.css">

<!-- JavaScript -->
<script src="https://cdn.jsdelivr.net/gh/seu-repo/rpa-progress-tracker.js"></script>
<script src="https://cdn.jsdelivr.net/gh/seu-repo/rpa-api-handler.js"></script>
<script src="https://cdn.jsdelivr.net/gh/seu-repo/rpa-webflow-integration.js"></script>
```

#### **2. Configuração no Webflow**
- Adicionar Embed na página principal
- Configurar para carregar após o body
- Adicionar `data-rpa-trigger` nos botões de cálculo
- Configurar classes CSS personalizadas

#### **3. Componentes Webflow**
```html
<!-- Progress Bar Component -->
<div class="rpa-progress-component">
    <div class="progress-bar-wrapper">
        <div class="progress-bar">
            <div class="progress-fill" data-rpa-progress="0"></div>
        </div>
        <div class="progress-text" data-rpa-text="0%"></div>
        <div class="current-phase" data-rpa-phase="Iniciando..."></div>
    </div>
</div>

<!-- Results Grid Component -->
<div class="rpa-results-component">
    <div class="results-grid">
        <div class="estimate-card" data-rpa-estimate>
            <h3>Estimativa Inicial</h3>
            <div class="value">-</div>
        </div>
        
        <div class="calculations-grid">
            <div class="calculation-card recommended" data-rpa-recommended>
                <h3>Recomendado</h3>
                <div class="value">-</div>
            </div>
            
            <div class="calculation-card alternative" data-rpa-alternative>
                <h3>Alternativo</h3>
                <div class="value">-</div>
            </div>
        </div>
    </div>
</div>
```

---

## 📅 **CRONOGRAMA DE DESENVOLVIMENTO**

### **⏱️ TIMELINE (5 horas total)**

| **Fase** | **Duração** | **Atividade** | **Entregáveis** |
|----------|-------------|---------------|-----------------|
| **Fase 1** | 2h | Desenvolvimento HTML/CSS/JS | Estrutura completa |
| **Fase 2** | 1h | Criação componentes Webflow | Componentes reutilizáveis |
| **Fase 3** | 1h | Integração Embed Custom Code | Código de integração |
| **Fase 4** | 1h | Testes e ajustes | Sistema funcional |
| **Total** | **5h** | **Sistema completo** | **Pronto para produção** |

### **📋 CHECKLIST DE ENTREGAS**

#### **✅ Fase 1 - Desenvolvimento Base**
- [ ] Estrutura HTML completa
- [ ] CSS responsivo (desktop + mobile)
- [ ] Animações e transições
- [ ] JavaScript funcional
- [ ] Integração com API V6.0.0

#### **✅ Fase 2 - Componentes Webflow**
- [ ] Progress Bar Component
- [ ] Results Grid Component
- [ ] CSS Classes personalizadas
- [ ] Documentação de uso

#### **✅ Fase 3 - Integração**
- [ ] Embed Custom Code
- [ ] JavaScript de integração
- [ ] Event listeners
- [ ] Coleta de dados Webflow

#### **✅ Fase 4 - Testes**
- [ ] Testes em diferentes dispositivos
- [ ] Validação de responsividade
- [ ] Testes de performance
- [ ] Documentação final

---

## 🎯 **CRITÉRIOS DE SUCESSO**

### **✅ FUNCIONALIDADES OBRIGATÓRIAS**
1. **Barra de Progresso**: Funcionando 0-100% com fase atual
2. **Layout Responsivo**: Desktop 1/3+2/3, Mobile 3 divs verticais
3. **Integração Webflow**: Via Embed Custom Code
4. **Tempo Real**: Atualizações a cada 2 segundos
5. **Animações**: Transições suaves e elegantes
6. **API**: Compatibilidade com V6.0.0

### **📊 MÉTRICAS DE QUALIDADE**
- **Performance**: Carregamento < 2 segundos
- **Responsividade**: Funcionar em todos os dispositivos
- **Acessibilidade**: Suporte básico a leitores de tela
- **Compatibilidade**: Funcionar em todos os browsers modernos
- **Manutenibilidade**: Código limpo e documentado

---

## 📚 **RECURSOS E REFERÊNCIAS**

### **🔗 LINKS ÚTEIS**
- [Webflow Embed Custom Code](https://university.webflow.com/lesson/embed-custom-code)
- [CSS Grid Layout](https://css-tricks.com/snippets/css/complete-guide-grid/)
- [Animate.css Documentation](https://animate.style/)
- [Font Awesome Icons](https://fontawesome.com/icons)
- [API V6.0.0 Documentation](ARQUITETURA_SOLUCAO_RPA_V6.md)

### **📖 DOCUMENTAÇÃO TÉCNICA**
- [Arquitetura Solução RPA V6.0.0](ARQUITETURA_SOLUCAO_RPA_V6.md)
- [Plano Desenvolvimento Modal V6.1.0](PLANO_DESENVOLVIMENTO_MODAL_V6.1.0.md)
- [Correções SessionService V6.0.0](CORRECOES_SESSIONSERVICE_V6.md)

---

## 🎉 **CONCLUSÃO**

### **✅ PROJETO COMPLETO E DETALHADO**
O projeto Modal RPA Webflow V6.1.0 está completamente especificado e pronto para desenvolvimento.

### **🎯 OBJETIVOS CLAROS**
- **Funcionalidade**: Interface moderna e responsiva
- **Integração**: Perfeita compatibilidade com Webflow
- **Performance**: Carregamento rápido e animações suaves
- **Prazo**: 5 horas de desenvolvimento

### **📋 PRÓXIMOS PASSOS**
1. **Iniciar desenvolvimento** seguindo o cronograma
2. **Implementar integração** com Webflow
3. **Realizar testes** em diferentes dispositivos
4. **Entregar sistema** pronto para produção

**Projeto Modal RPA Webflow V6.1.0 pronto para desenvolvimento!** 🚀

---

**Desenvolvido por**: Equipe de Desenvolvimento  
**Data**: 03 de Outubro de 2025  
**Versão**: 6.1.0  
**Status**: ✅ **PROJETO COMPLETO E PRONTO PARA DESENVOLVIMENTO**
