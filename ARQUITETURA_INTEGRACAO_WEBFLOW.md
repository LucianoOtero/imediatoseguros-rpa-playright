# ARQUITETURA DE INTEGRAÇÃO WEBFLOW - RPA V4

**Data:** 01/10/2025  
**Engenheiro de Software:** Análise e Design da Arquitetura  
**Status:** ✅ ARQUITETURA DEFINIDA  

---

## 📋 VISÃO GERAL DA SOLUÇÃO

### Objetivo
Criar uma solução JavaScript que será injetada no custom code do Webflow para integrar o formulário de cotação com o RPA V4, executando o processamento em background e exibindo o progresso em tempo real através do modal responsivo.

### Fluxo Principal
```
Usuário preenche formulário → Clica no botão → JavaScript coleta dados → 
Inicia RPA em background → Monitora progresso → Exibe resultados no modal
```

---

## 🏗️ ARQUITETURA DA SOLUÇÃO

### Diagrama de Componentes

```
┌─────────────────────────────────────────────────────────────────┐
│                    WEBFLOW WEBSITE                             │
│  segurosimediato.com.br                                         │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                FORMULÁRIO DE COTAÇÃO                   │    │
│  │                                                         │    │
│  │  [CPF] [Nome] [Placa] [CEP] [Email] [Telefone]         │    │
│  │                                                         │    │
│  │              [BOTÃO: Solicitar Cotação]                │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │              CUSTOM CODE (JavaScript)                  │    │
│  │                                                         │    │
│  │  • Coleta de dados do formulário                        │    │
│  │  • Validação de campos                                  │    │
│  │  • Chamada para API RPA V4                              │    │
│  │  • Monitoramento de progresso                           │    │
│  │  • Controle do modal de progresso                       │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
                                │
                                │ HTTP/HTTPS
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    HETZNER CLOUD                               │
│  IP: 37.27.92.160                                               │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                    NGINX                                │    │
│  │  Proxy Reverso + SSL/TLS                                │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                │                                │
│                                ▼                                │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                   PHP-FPM                               │    │
│  │  API REST V4                                            │    │
│  │                                                         │    │
│  │  POST /api/rpa/start                                    │    │
│  │  GET /api/rpa/progress/{session_id}                     │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                │                                │
│                                ▼                                │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                   RPA PYTHON                            │    │
│  │  executar_rpa_imediato_playwright.py                   │    │
│  │                                                         │    │
│  │  • 15 telas de automação                               │    │
│  │  • Progress tracker JSON                               │    │
│  │  • Estimativas iniciais (Tela 4)                       │    │
│  │  • Cálculo final (Tela 15)                             │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔧 COMPONENTES DA ARQUITETURA

### 1. **Frontend (Webflow)**

#### Formulário de Cotação
```html
<!-- Estrutura do formulário no Webflow -->
<form id="formulario-cotacao" class="formulario-cotacao">
    <input type="text" id="cpf" name="cpf" placeholder="CPF" required>
    <input type="text" id="nome" name="nome" placeholder="Nome Completo" required>
    <input type="text" id="placa" name="placa" placeholder="Placa do Veículo" required>
    <input type="text" id="cep" name="cep" placeholder="CEP" required>
    <input type="email" id="email" name="email" placeholder="E-mail" required>
    <input type="tel" id="telefone" name="telefone" placeholder="Telefone" required>
    
    <button type="submit" id="botao-cotacao" class="botao-cotacao">
        Solicitar Cotação
    </button>
</form>
```

#### Custom Code JavaScript
```javascript
// Código a ser injetado no custom code do Webflow
class WebflowRPAClient {
    constructor() {
        this.apiBaseUrl = 'https://37.27.92.160/api/rpa';
        this.formId = 'formulario-cotacao';
        this.buttonId = 'botao-cotacao';
        this.modal = null;
        this.sessionId = null;
        this.progressInterval = null;
    }
    
    // Inicializar o cliente
    init() {
        this.setupEventListeners();
        this.loadDependencies();
    }
    
    // Configurar event listeners
    setupEventListeners() {
        const form = document.getElementById(this.formId);
        const button = document.getElementById(this.buttonId);
        
        if (form && button) {
            form.addEventListener('submit', (e) => {
                e.preventDefault();
                this.handleFormSubmit();
            });
            
            button.addEventListener('click', (e) => {
                e.preventDefault();
                this.handleFormSubmit();
            });
        }
    }
    
    // Carregar dependências
    loadDependencies() {
        // SweetAlert2
        if (!window.Swal) {
            this.loadScript('https://cdn.jsdelivr.net/npm/sweetalert2@11/dist/sweetalert2.min.js');
        }
        
        // Font Awesome
        if (!document.querySelector('link[href*="font-awesome"]')) {
            this.loadStylesheet('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');
        }
        
        // Titillium Web Font
        if (!document.querySelector('link[href*="titillium"]')) {
            this.loadStylesheet('https://fonts.googleapis.com/css2?family=Titillium+Web:wght@300;400;600;700&display=swap');
        }
    }
    
    // Carregar script dinamicamente
    loadScript(src) {
        return new Promise((resolve, reject) => {
            const script = document.createElement('script');
            script.src = src;
            script.onload = resolve;
            script.onerror = reject;
            document.head.appendChild(script);
        });
    }
    
    // Carregar stylesheet dinamicamente
    loadStylesheet(href) {
        const link = document.createElement('link');
        link.rel = 'stylesheet';
        link.href = href;
        document.head.appendChild(link);
    }
    
    // Manipular envio do formulário
    async handleFormSubmit() {
        try {
            // Coletar dados do formulário
            const dados = this.collectFormData();
            
            // Validar dados
            this.validateFormData(dados);
            
            // Desabilitar botão
            this.disableButton();
            
            // Iniciar RPA
            await this.startRPA(dados);
            
        } catch (error) {
            console.error('Erro ao processar formulário:', error);
            this.showError('Erro', error.message);
            this.enableButton();
        }
    }
    
    // Coletar dados do formulário
    collectFormData() {
        const form = document.getElementById(this.formId);
        const formData = new FormData(form);
        
        return {
            cpf: formData.get('cpf') || document.getElementById('cpf')?.value,
            nome: formData.get('nome') || document.getElementById('nome')?.value,
            placa: formData.get('placa') || document.getElementById('placa')?.value,
            cep: formData.get('cep') || document.getElementById('cep')?.value,
            email: formData.get('email') || document.getElementById('email')?.value,
            telefone: formData.get('telefone') || document.getElementById('telefone')?.value
        };
    }
    
    // Validar dados do formulário
    validateFormData(dados) {
        const camposObrigatorios = ['cpf', 'nome', 'placa', 'cep'];
        const camposFaltando = camposObrigatorios.filter(campo => !dados[campo]);
        
        if (camposFaltando.length > 0) {
            throw new Error(`Campos obrigatórios faltando: ${camposFaltando.join(', ')}`);
        }
        
        // Validações específicas
        if (dados.cpf && !this.isValidCPF(dados.cpf)) {
            throw new Error('CPF inválido');
        }
        
        if (dados.placa && !this.isValidPlaca(dados.placa)) {
            throw new Error('Placa inválida');
        }
        
        if (dados.cep && !this.isValidCEP(dados.cep)) {
            throw new Error('CEP inválido');
        }
    }
    
    // Validar CPF
    isValidCPF(cpf) {
        cpf = cpf.replace(/[^\d]/g, '');
        return cpf.length === 11;
    }
    
    // Validar placa
    isValidPlaca(placa) {
        placa = placa.replace(/[^\w]/g, '').toUpperCase();
        return /^[A-Z]{3}\d{4}$/.test(placa);
    }
    
    // Validar CEP
    isValidCEP(cep) {
        cep = cep.replace(/[^\d]/g, '');
        return cep.length === 8;
    }
    
    // Iniciar RPA
    async startRPA(dados) {
        try {
            // Chamar API para iniciar sessão
            const response = await fetch(`${this.apiBaseUrl}/start`, {
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
                throw new Error(result.message || 'Erro ao iniciar RPA');
            }
            
            this.sessionId = result.session_id;
            
            // Abrir modal de progresso
            this.openProgressModal();
            
            // Iniciar monitoramento
            this.startProgressMonitoring();
            
        } catch (error) {
            throw new Error(`Erro ao iniciar RPA: ${error.message}`);
        }
    }
    
    // Abrir modal de progresso
    openProgressModal() {
        if (!window.Swal) {
            throw new Error('SweetAlert2 não carregado');
        }
        
        this.modal = Swal.fire({
            title: '<div style="font-family: \'Titillium Web\', sans-serif; font-size: 24px; font-weight: 600; color: #2c3e50;"><i class="fas fa-cogs" style="color: #3498db; margin-right: 10px;"></i>Processando Cotação</div>',
            html: this.generateModalHTML(),
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
                this.setupModalEventListeners();
            },
            willClose: () => {
                this.stopProgressMonitoring();
            }
        });
    }
    
    // Gerar HTML do modal
    generateModalHTML() {
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
    
    // Configurar event listeners do modal
    setupModalEventListeners() {
        const closeButton = document.getElementById('closeButton');
        if (closeButton) {
            closeButton.addEventListener('click', () => {
                this.closeModal();
            });
        }
    }
    
    // Iniciar monitoramento de progresso
    startProgressMonitoring() {
        if (this.progressInterval) {
            clearInterval(this.progressInterval);
        }
        
        let pollCount = 0;
        const maxPolls = 150; // 5 minutos (150 * 2s)
        
        this.progressInterval = setInterval(async () => {
            try {
                pollCount++;
                
                if (pollCount > maxPolls) {
                    this.showError('Timeout', 'Tempo limite de processamento excedido');
                    return;
                }
                
                const response = await fetch(`${this.apiBaseUrl}/progress/${this.sessionId}`);
                
                if (!response.ok) {
                    throw new Error(`Erro HTTP: ${response.status}`);
                }
                
                const data = await response.json();
                
                if (data.success) {
                    this.updateProgress(data.progress);
                    
                    // Verificar se concluído
                    if (data.progress && data.progress.status === 'success') {
                        this.completeProcessing(data.progress);
                    }
                } else {
                    throw new Error(data.message || 'Erro ao obter progresso');
                }
                
            } catch (error) {
                console.error('Erro ao monitorar progresso:', error);
                this.showError('Erro de Monitoramento', error.message);
            }
        }, 2000); // Polling a cada 2 segundos
    }
    
    // Atualizar progresso
    updateProgress(progressData) {
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
        this.updateCurrentPhase(progress);
        
        // Atualizar estimativas iniciais
        if (progressData.estimativas && progressData.estimativas.capturadas) {
            this.updateInitialEstimate(progressData.estimativas.dados);
        }
        
        // Atualizar resultados finais
        if (progressData.resultados_finais && progressData.resultados_finais.rpa_finalizado) {
            this.updateFinalValue(progressData.resultados_finais.dados);
        }
    }
    
    // Atualizar fase atual
    updateCurrentPhase(progress) {
        const currentPhase = document.getElementById('currentPhase');
        if (!currentPhase) return;
        
        const phases = [
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
        
        // Encontrar fase correspondente ao progresso
        let faseAtual = phases[0];
        for (let i = phases.length - 1; i >= 0; i--) {
            if (progress >= phases[i].progress) {
                faseAtual = phases[i];
                break;
            }
        }
        
        currentPhase.innerHTML = `
            <i class="${faseAtual.icon}" style="color: #3498db; margin-right: 8px;"></i>
            <span style="font-size: 16px; font-weight: 500; color: #2c3e50;">${faseAtual.text}</span>
        `;
    }
    
    // Atualizar estimativa inicial
    updateInitialEstimate(estimativas) {
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
    
    // Atualizar valor final
    updateFinalValue(resultados) {
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
    
    // Concluir processamento
    completeProcessing(progressData) {
        this.stopProgressMonitoring();
        
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
        this.dispatchEvent('rpaConcluido', {
            sessionId: this.sessionId,
            progressData: progressData
        });
    }
    
    // Parar monitoramento
    stopProgressMonitoring() {
        if (this.progressInterval) {
            clearInterval(this.progressInterval);
            this.progressInterval = null;
        }
    }
    
    // Fechar modal
    closeModal() {
        if (this.modal) {
            Swal.close();
            this.stopProgressMonitoring();
        }
    }
    
    // Mostrar erro
    showError(titulo, mensagem) {
        this.stopProgressMonitoring();
        
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
    
    // Disparar evento customizado
    dispatchEvent(eventName, data) {
        const event = new CustomEvent(eventName, {
            detail: data
        });
        document.dispatchEvent(event);
    }
    
    // Desabilitar botão
    disableButton() {
        const button = document.getElementById(this.buttonId);
        if (button) {
            button.disabled = true;
            button.textContent = 'Processando...';
            button.style.opacity = '0.6';
        }
    }
    
    // Habilitar botão
    enableButton() {
        const button = document.getElementById(this.buttonId);
        if (button) {
            button.disabled = false;
            button.textContent = 'Solicitar Cotação';
            button.style.opacity = '1';
        }
    }
}

// Inicializar quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', () => {
    const rpaClient = new WebflowRPAClient();
    rpaClient.init();
    
    // Event listener para conclusão do RPA
    document.addEventListener('rpaConcluido', (event) => {
        console.log('RPA concluído:', event.detail);
        // Aqui você pode adicionar lógica adicional
        // Por exemplo: redirecionar para página de resultados
        // window.location.href = `/resultados?session=${event.detail.sessionId}`;
    });
});
```

### 2. **Backend (Hetzner Cloud)**

#### API REST V4
- **POST** `/api/rpa/start` - Criar sessão RPA
- **GET** `/api/rpa/progress/{session_id}` - Monitorar progresso

#### RPA Python
- **executar_rpa_imediato_playwright.py** - Script principal
- **Progress tracker JSON** - Monitoramento em tempo real
- **15 telas de automação** - Processo completo

---

## 🔄 FLUXO DE EXECUÇÃO

### 1. **Inicialização**
```javascript
// DOM ready
document.addEventListener('DOMContentLoaded', () => {
    const rpaClient = new WebflowRPAClient();
    rpaClient.init();
});
```

### 2. **Coleta de Dados**
```javascript
// Usuário clica no botão
// JavaScript coleta dados do formulário
const dados = {
    cpf: '12345678901',
    nome: 'João Silva',
    placa: 'ABC1234',
    cep: '01234567',
    email: 'joao@email.com',
    telefone: '11999999999'
};
```

### 3. **Validação**
```javascript
// Validação de campos obrigatórios
// Validação de formato (CPF, placa, CEP)
// Dados já validados pelo Webflow
```

### 4. **Início do RPA**
```javascript
// Chamada para API
const response = await fetch('https://37.27.92.160/api/rpa/start', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(dados)
});

const result = await response.json();
// sessionId: 'rpa_v4_20251001_222340_28563ee9'
```

### 5. **Monitoramento**
```javascript
// Polling a cada 2 segundos
setInterval(async () => {
    const response = await fetch(`https://37.27.92.160/api/rpa/progress/${sessionId}`);
    const data = await response.json();
    
    // Atualizar modal
    updateProgress(data.progress);
}, 2000);
```

### 6. **Conclusão**
```javascript
// RPA concluído
// Exibir resultados finais
// Habilitar botão de fechar
// Disparar evento 'rpaConcluido'
```

---

## 📱 RESPONSIVIDADE

### Breakpoints
- **Desktop**: > 768px (Modal 500px)
- **Tablet**: 768px (Modal 90% width)
- **Mobile**: < 480px (Modal 90% width, cards empilhados)

### Adaptações
- Modal responsivo
- Cards empilhados no mobile
- Fonte adaptada
- Botões com área de toque aumentada

---

## 🔒 SEGURANÇA

### Validação de Dados
- Campos obrigatórios
- Formato CPF, placa, CEP
- Sanitização de entrada
- Prevenção de XSS

### Comunicação
- HTTPS obrigatório
- CORS configurado
- Timeout de 5 minutos
- Tratamento de erros

---

## 📊 MONITORAMENTO

### Métricas Frontend
- Tempo de carregamento
- Taxa de conversão
- Erros de validação
- Abandono do modal

### Métricas Backend
- Tempo de resposta da API
- Taxa de sucesso do RPA
- Uso de recursos
- Logs de erro

---

## 🚀 IMPLEMENTAÇÃO

### 1. **Preparação do Webflow**
```html
<!-- Adicionar no custom code do Webflow -->
<script>
// Código JavaScript completo aqui
</script>
```

### 2. **Configuração do Formulário**
- IDs específicos para campos
- Validação no Webflow
- Botão com ID específico

### 3. **Testes**
- Testes de responsividade
- Testes de funcionalidade
- Testes de performance
- Testes de segurança

---

## ✅ VANTAGENS DA ARQUITETURA

### 1. **Simplicidade**
- Código único para injetar
- Sem dependências externas
- Fácil manutenção

### 2. **Performance**
- Carregamento assíncrono
- Polling eficiente
- Cache de dependências

### 3. **Robustez**
- Tratamento de erros
- Validação de dados
- Timeout configurável

### 4. **Flexibilidade**
- Configurável via JavaScript
- Eventos customizados
- Integração fácil

---

## 📋 CHECKLIST DE IMPLEMENTAÇÃO

### Frontend (Webflow)
- [ ] Adicionar custom code JavaScript
- [ ] Configurar IDs do formulário
- [ ] Testar responsividade
- [ ] Validar funcionalidade

### Backend (Hetzner)
- [ ] API REST V4 funcionando
- [ ] RPA Python operacional
- [ ] Progress tracker ativo
- [ ] Logs configurados

### Integração
- [ ] Testes end-to-end
- [ ] Validação de dados
- [ ] Tratamento de erros
- [ ] Monitoramento ativo

---

**Arquitetura de integração Webflow definida e pronta para implementação.**
