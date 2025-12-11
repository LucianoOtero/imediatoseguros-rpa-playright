# ARQUITETURA DE INTEGRAÇÃO WEBFLOW - RPA V6.12.1

**Data:** 18/10/2025  
**Engenheiro de Software:** Análise e Design da Arquitetura  
**Status:** ✅ ARQUITETURA IMPLEMENTADA E FUNCIONANDO  

---

## 📋 VISÃO GERAL DA SOLUÇÃO

### Objetivo
Sistema JavaScript hospedado no servidor `rpaimediatoseguros.com.br` que é injetado no Webflow via Custom Code, integrando o formulário de cotação com o RPA V6.12.1, executando processamento em background com SpinnerTimer regressivo e exibindo progresso em tempo real através de modal responsivo.

### Fluxo Principal
```
Usuário preenche formulário → Clica no botão → JavaScript intercepta → 
Coleta dados + GCLID_FLD → Inicia RPA → SpinnerTimer regressivo → 
Monitora progresso → Exibe resultados → Webhooks executam
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
│  │  [GCLID_FLD] (invisível)                               │    │
│  │                                                         │    │
│  │              [BOTÃO: Solicitar Cotação]                │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │              CUSTOM CODE (JavaScript)                  │    │
│  │                                                         │    │
│  │  <script src="https://rpaimediatoseguros.com.br/js/     │    │
│  │           webflow-injection-complete.js" defer>         │    │
│  │                                                         │    │
│  │  • Intercepta envio do formulário                      │    │
│  │  • Coleta dados + GCLID_FLD                            │    │
│  │  • SpinnerTimer regressivo (3min + 2min)              │    │
│  │  • Modal com progresso em tempo real                   │    │
│  │  • Tratamento unificado de erros                       │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
                                │
                                │ HTTP/HTTPS
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    SERVIDOR RPA                                │
│  rpaimediatoseguros.com.br (37.27.92.160)                      │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                    NGINX                                │    │
│  │  Proxy Reverso + SSL/TLS + Proteção /js/               │    │
│  │                                                         │    │
│  │  /js/webflow-injection-complete.js (118KB)             │    │
│  │  • Whitelist de IPs (Webflow, IPs autorizados)         │    │
│  │  • Rate limiting (10 req/min)                           │    │
│  │  • Validação de Referer                                │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                │                                │
│                                ▼                                │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                   PHP-FPM                               │    │
│  │  API REST V6.12.1                                       │    │
│  │                                                         │    │
│  │  POST /api/rpa/start                                    │    │
│  │  GET /api/rpa/progress/{session_id}                     │    │
│  │  • Redis Progress Tracker                              │    │
│  │  • Substituições: "Tela" → "Processo"                  │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                │                                │
│                                ▼                                │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                   RPA PYTHON                            │    │
│  │  executar_rpa_imediato_playwright.py                   │    │
│  │                                                         │    │
│  │  • 15 telas de automação                               │    │
│  │  • Progress tracker Redis/JSON                         │    │
│  │  • Estimativas iniciais (Tela 4)                       │    │
│  │  • Cálculo final (Tela 15)                             │    │
│  │  • Detecção de cotação manual                          │    │
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
    <input type="hidden" id="GCLID_FLD" name="GCLID_FLD" value="">
    
    <button type="submit" id="botao-cotacao" class="botao-cotacao">
        Solicitar Cotação
    </button>
</form>
```

#### Custom Code JavaScript (Injeção Externa)
```html
<!-- Webflow Custom Code - Before </body> tag -->
<script src="https://rpaimediatoseguros.com.br/js/webflow-injection-complete.js" defer></script>
```

#### Funcionalidades do JavaScript V6.12.1

##### **🎯 Características Principais:**
- **Interceptação**: Captura envio do formulário antes do redirect
- **Coleta de Dados**: Inclui campo `GCLID_FLD` automaticamente
- **SpinnerTimer**: Timer regressivo de 3 minutos + extensão de 2 minutos
- **Modal Responsivo**: Progresso em tempo real com SpinKit Model 8
- **Tratamento de Erros**: Mensagem unificada "Cotação Manual Necessária"
- **Webhooks**: 4 webhooks implementados (comentados para testes)

##### **🔧 Classes Principais:**
```javascript
// Classe principal do cliente RPA
class ProgressModalRPA {
    constructor(sessionId) {
        this.sessionId = sessionId;
        this.spinnerTimer = null;
        this.modalProgress = null;
    }
    
    // Inicializar SpinnerTimer
    initSpinnerTimer() {
        this.spinnerTimer = new SpinnerTimer();
        this.spinnerTimer.init();
        this.spinnerTimer.start();
    }
    
    // Parar SpinnerTimer
    stopSpinnerTimer() {
        if (this.spinnerTimer) {
            this.spinnerTimer.finish();
        }
    }
}

// Classe do timer regressivo
class SpinnerTimer {
    constructor() {
        this.duration = 180; // 3 minutos
        this.extensionDuration = 120; // 2 minutos
        this.currentTime = this.duration;
        this.isExtended = false;
    }
    
    // Inicializar timer
    init() {
        this.createSpinnerHTML();
        this.updateDisplay();
    }
    
    // Iniciar contagem regressiva
    start() {
        this.interval = setInterval(() => {
            this.tick();
        }, 100);
    }
    
    // Tick do timer
    tick() {
        this.currentTime -= 0.1;
        this.updateDisplay();
        
        if (this.currentTime <= 0) {
            if (!this.isExtended) {
                this.extendTimer();
            } else {
                this.finish();
            }
        }
    }
}
```

##### **📊 Coleta de Dados Aprimorada:**
```javascript
// Coleta automática incluindo GCLID_FLD
collectFormData() {
    const formData = new FormData(form);
    const data = {};
    
    // Coletar campos do formulário
    for (let [key, value] of formData.entries()) {
        data[key] = value;
    }
    
    // ✅ CORREÇÃO: Capturar campo GCLID_FLD manualmente
    const gclidField = document.getElementById('GCLID_FLD');
    if (gclidField) {
        data.GCLID_FLD = gclidField.value || 'TesteRPA123';
    } else {
        data.GCLID_FLD = 'TesteRPA123'; // Valor padrão
    }
    
    return data;
}
```

##### **🔄 Webhooks Implementados:**
```javascript
// 4 webhooks implementados (comentados para testes)
async executeWebflowWebhooks(form, formData) {
    // Webhook 1: Send form data to Webflow
    await this.sendToWebflow(formData);
    
    // Webhook 2: webhook.site
    await this.sendToWebhookSite(formData);
    
    // Webhook 3: mdmidia.com.br/add_tra
    await this.sendToMdmidiaTra(formData);
    
    // Webhook 4: mdmidia.com.br/add_we
    await this.sendToMdmidiaWe(formData);
}
```

### 2. **Backend (Servidor RPA)**

#### Diretório JS Protegido
- **Localização**: `/opt/imediatoseguros-rpa/js/`
- **Arquivo**: `webflow-injection-complete.js` (118KB)
- **URL**: `https://rpaimediatoseguros.com.br/js/webflow-injection-complete.js`
- **Proteção**: Whitelist de IPs, Rate limiting, Validação de Referer

#### API REST V6.12.1
- **POST** `/api/rpa/start` - Criar sessão RPA
- **GET** `/api/rpa/progress/{session_id}` - Monitorar progresso
- **Redis Progress Tracker** - Monitoramento em tempo real
- **Substituições**: "Tela" → "Processo", "concluída" → "finalizou"

#### RPA Python
- **executar_rpa_imediato_playwright.py** - Script principal
- **Progress tracker Redis/JSON** - Monitoramento em tempo real
- **15 telas de automação** - Processo completo
- **Detecção de cotação manual** - Tratamento de erros

---

## 🔄 FLUXO DE EXECUÇÃO

### 1. **Inicialização**
```javascript
// DOM ready
document.addEventListener('DOMContentLoaded', () => {
    const rpaClient = new ProgressModalRPA();
    rpaClient.init();
});
```

### 2. **Coleta de Dados**
```javascript
// Usuário clica no botão
// JavaScript intercepta e coleta dados
const dados = {
    cpf: '12345678901',
    nome: 'João Silva',
    placa: 'ABC1234',
    cep: '01234567',
    email: 'joao@email.com',
    telefone: '11999999999',
    GCLID_FLD: 'TesteRPA123' // ✅ Capturado automaticamente
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
const response = await fetch('https://rpaimediatoseguros.com.br/api/rpa/start', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(dados)
});

const result = await response.json();
// sessionId: 'rpa_v6_20251018_143000_abc123def'
```

### 5. **SpinnerTimer Regressivo**
```javascript
// Timer de 3 minutos com extensão de 2 minutos
// SpinKit Model 8 (Circle) com 12 pontos pulsando
// Posicionamento centralizado no modal
// Cores vermelhas para contraste
```

### 6. **Monitoramento**
```javascript
// Polling a cada 2 segundos
setInterval(async () => {
    const response = await fetch(`https://rpaimediatoseguros.com.br/api/rpa/progress/${sessionId}`);
    const data = await response.json();
    
    // Atualizar modal
    updateProgress(data.progress);
}, 2000);
```

### 7. **Conclusão**
```javascript
// RPA concluído
// Exibir resultados finais
// Habilitar botão de fechar
// Disparar evento 'rpaConcluido'
// Webhooks executam automaticamente
```

---

## 📱 RESPONSIVIDADE

### Breakpoints
- **Desktop**: > 768px (Modal 500px)
- **Tablet**: 768px (Modal 90% width)
- **Mobile**: < 480px (Modal 90% width, cards empilhados)

### Adaptações
- Modal responsivo
- SpinnerTimer centralizado
- Cards empilhados no mobile
- Fonte adaptada
- Botões com área de toque aumentada

---

## 🔒 SEGURANÇA

### Proteção do Diretório JS
- **Whitelist de IPs**: Webflow CDN, IPs autorizados
- **Rate Limiting**: 10 requisições por minuto por IP
- **Validação de Referer**: Apenas domínios `.webflow.io`
- **Token de Autenticação**: Parâmetro opcional na URL
- **Logs de Segurança**: Monitoramento de acessos

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
- Tempo de carregamento do JavaScript
- Taxa de conversão
- Erros de validação
- Abandono do modal
- Performance do SpinnerTimer

### Métricas Backend
- Tempo de resposta da API
- Taxa de sucesso do RPA
- Uso de recursos
- Logs de erro
- Acessos ao diretório JS

---

## 🚀 IMPLEMENTAÇÃO

### 1. **Preparação do Webflow**
```html
<!-- Adicionar no custom code do Webflow -->
<script src="https://rpaimediatoseguros.com.br/js/webflow-injection-complete.js" defer></script>
```

### 2. **Configuração do Formulário**
- IDs específicos para campos
- Campo `GCLID_FLD` invisível
- Validação no Webflow
- Botão com ID específico
- **Desabilitar redirect** para página de sucesso

### 3. **Configuração do Servidor**
- Diretório `/js/` criado
- Arquivo JavaScript hospedado
- Proteções de segurança ativas
- Logs de monitoramento

### 4. **Testes**
- Testes de responsividade
- Testes de funcionalidade
- Testes de performance
- Testes de segurança
- Testes de interceptação

---

## ✅ VANTAGENS DA ARQUITETURA

### 1. **Simplicidade**
- Arquivo único hospedado externamente
- Sem dependências externas complexas
- Fácil manutenção e atualização
- Versionamento centralizado

### 2. **Performance**
- Carregamento assíncrono com `defer`
- Polling eficiente
- Cache de dependências
- SpinnerTimer otimizado

### 3. **Robustez**
- Tratamento de erros unificado
- Validação de dados
- Timeout configurável
- Fallbacks implementados

### 4. **Flexibilidade**
- Configurável via JavaScript
- Eventos customizados
- Integração fácil
- Webhooks modulares

### 5. **Segurança**
- Proteção do diretório JS
- Validação de origem
- Rate limiting
- Logs de segurança

---

## 📋 CHECKLIST DE IMPLEMENTAÇÃO

### Frontend (Webflow)
- [x] Adicionar custom code JavaScript externo
- [x] Configurar IDs do formulário
- [x] Adicionar campo `GCLID_FLD`
- [x] Desabilitar redirect para página de sucesso
- [x] Testar responsividade
- [x] Validar funcionalidade

### Backend (Servidor RPA)
- [x] Criar diretório `/js/`
- [x] Hospedar arquivo JavaScript
- [x] Configurar proteções de segurança
- [x] API REST V6.12.1 funcionando
- [x] RPA Python operacional
- [x] Progress tracker Redis ativo
- [x] Logs configurados

### Integração
- [x] Testes end-to-end
- [x] Validação de dados
- [x] Tratamento de erros
- [x] Monitoramento ativo
- [x] SpinnerTimer funcionando
- [x] Webhooks implementados

---

## 🔍 OBSERVAÇÕES IMPORTANTES

### **🎯 Funcionalidades Implementadas:**
1. **Interceptação de Formulário**: JavaScript captura envio antes do redirect
2. **Coleta de GCLID_FLD**: Campo invisível capturado automaticamente
3. **SpinnerTimer Regressivo**: Timer de 3min + extensão de 2min
4. **Modal Centralizado**: SpinnerTimer posicionado no centro do modal
5. **Tratamento Unificado**: Todos os erros mostram "Cotação Manual Necessária"
6. **Webhooks Modulares**: 4 webhooks implementados e comentados
7. **Proteção de Segurança**: Diretório JS protegido com whitelist

### **⚠️ Considerações:**
- **Redirect Desabilitado**: Necessário para interceptação funcionar
- **Webhooks Nativos**: Webflow executa webhooks automaticamente
- **JavaScript Externo**: Hospedado no servidor RPA para controle
- **Segurança Crítica**: Implementar proteções do diretório JS
- **Monitoramento**: Logs de acesso e performance essenciais

### **🔧 Manutenção:**
- **Atualizações**: Fazer via servidor RPA (controle centralizado)
- **Versionamento**: Git tags para controle de versões
- **Backup**: Manter backup do arquivo JavaScript
- **Testes**: Validar após cada atualização
- **Monitoramento**: Acompanhar logs de segurança

---

**Arquitetura de integração Webflow V6.12.1 implementada e funcionando com SpinnerTimer regressivo e proteções de segurança.** ✅

