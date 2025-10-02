# PLANO DE DESENVOLVIMENTO - SIMULAÇÃO WEBFLOW

**Data:** 01/10/2025  
**Desenvolvedor:** Planejamento do Projeto de Simulação  
**Status:** ✅ PLANO DEFINIDO  

---

## 📋 OBJETIVO DO PROJETO

Criar uma simulação completa do funcionamento do website Webflow com integração RPA V4, incluindo:

1. **HTML de simulação** com formulário preenchido com dados do `parametros.json`
2. **JavaScript funcional** pronto para injeção no Webflow
3. **Modal de progresso** integrado com API RPA V4
4. **Testes completos** de funcionalidade

### Finalidade
- **Simular** o comportamento real do website Webflow
- **Testar** a integração completa com RPA V4
- **Validar** o modal de progresso e funcionalidades
- **Preparar** código para implementação no Webflow

---

## 🏗️ ARQUITETURA DA SIMULAÇÃO

### Componentes

```
┌─────────────────────────────────────────────────────────────┐
│                HTML DE SIMULAÇÃO                           │
│  simulacao_webflow.html                                    │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              FORMULÁRIO PREENCHIDO                  │    │
│  │  • CPF: 97137189768                                │    │
│  │  • Nome: ALEX KAMINSKI                             │    │
│  │  • Placa: EYQ4J41                                  │    │
│  │  • CEP: 03317-000                                  │    │
│  │  • Email: alex.kaminski@imediatoseguros.com.br     │    │
│  │  • Telefone: 11953288466                           │    │
│  │                                                     │    │
│  │              [BOTÃO: Calcular]                      │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                                │
                                │ JavaScript
                                ▼
┌─────────────────────────────────────────────────────────────┐
│              JAVASCRIPT WEBFLOW                            │
│  webflow_integration.js                                     │
│                                                             │
│  • Classe WebflowRPAClient                                 │
│  • Coleta de dados do formulário                           │
│  • Validação de campos                                     │
│  • Chamada para API RPA V4                                 │
│  • Modal de progresso                                      │
│  • Monitoramento em tempo real                             │
└─────────────────────────────────────────────────────────────┘
                                │
                                │ HTTP/HTTPS
                                ▼
┌─────────────────────────────────────────────────────────────┐
│                HETZNER CLOUD                               │
│  IP: 37.27.92.160                                           │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                API REST V4                          │    │
│  │  POST /api/rpa/start                                │    │
│  │  GET /api/rpa/progress/{session_id}                 │    │
│  └─────────────────────────────────────────────────────┘    │
│                                │                            │
│                                ▼                            │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                RPA PYTHON                           │    │
│  │  executar_rpa_imediato_playwright.py               │    │
│  │  • 15 telas de automação                           │    │
│  │  • Progress tracker JSON                            │    │
│  │  • Estimativas iniciais (Tela 4)                   │    │
│  │  • Cálculo final (Tela 15)                         │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 ESTRUTURA DE ARQUIVOS

### 1. **simulacao_webflow.html**
- HTML de simulação com formulário preenchido
- Estilos CSS inline para simular o Webflow
- Botão "Calcular" para disparar o RPA
- Referências claras aos campos do formulário

### 2. **webflow_integration.js**
- JavaScript completo para injeção no Webflow
- Classe `WebflowRPAClient` com todas as funcionalidades
- Comentários detalhados sobre campos do formulário
- Instruções para adaptação no Webflow

### 3. **PLANO_DESENVOLVIMENTO_SIMULACAO.md**
- Este arquivo de planejamento
- Especificações técnicas
- Instruções de implementação

---

## 🎯 ESPECIFICAÇÕES TÉCNICAS

### HTML de Simulação

#### Campos do Formulário
```html
<!-- Campos baseados no parametros.json -->
<input type="text" id="cpf" name="cpf" value="97137189768" required>
<input type="text" id="nome" name="nome" value="ALEX KAMINSKI" required>
<input type="text" id="placa" name="placa" value="EYQ4J41" required>
<input type="text" id="cep" name="cep" value="03317-000" required>
<input type="email" id="email" name="email" value="alex.kaminski@imediatoseguros.com.br">
<input type="tel" id="telefone" name="telefone" value="11953288466">
```

#### Botão de Ação
```html
<button type="button" id="botao-cotacao" class="botao-cotacao">
    Calcular
</button>
```

#### Estilos CSS
- Simular aparência do Webflow
- Responsividade básica
- Cores alinhadas com o design

### JavaScript para Webflow

#### Classe Principal
```javascript
class WebflowRPAClient {
    constructor() {
        this.apiBaseUrl = 'https://37.27.92.160/api/rpa';
        // Configurações específicas para Webflow
    }
    
    // Métodos principais
    async init() { /* Inicialização */ }
    collectFormData() { /* Coletar dados */ }
    validateFormData() { /* Validar dados */ }
    async startRPA() { /* Iniciar RPA */ }
    openProgressModal() { /* Abrir modal */ }
    startProgressMonitoring() { /* Monitorar progresso */ }
}
```

#### Comentários para Webflow
```javascript
// WEBFLOW INTEGRATION NOTES:
// 1. Substituir os seletores abaixo pelos IDs/classes reais do formulário Webflow
// 2. Adaptar a coleta de dados conforme a estrutura do formulário
// 3. Configurar o botão de envio conforme o Webflow
// 4. Testar em diferentes dispositivos
```

---

## 🔄 FLUXO DE EXECUÇÃO

### 1. **Carregamento da Página**
```javascript
// DOM ready → Inicializar WebflowRPAClient
document.addEventListener('DOMContentLoaded', () => {
    const rpaClient = new WebflowRPAClient();
    rpaClient.init();
});
```

### 2. **Clique no Botão "Calcular"**
```javascript
// Usuário clica → Coletar dados → Validar → Iniciar RPA
document.getElementById('botao-cotacao').addEventListener('click', async () => {
    const dados = rpaClient.collectFormData();
    rpaClient.validateFormData(dados);
    await rpaClient.startRPA(dados);
});
```

### 3. **Processamento RPA**
```javascript
// API call → Modal abre → Polling inicia → Progresso atualiza
const response = await fetch('https://37.27.92.160/api/rpa/start', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(dados)
});
```

### 4. **Monitoramento**
```javascript
// Polling a cada 2 segundos → Atualizar modal → Exibir resultados
setInterval(async () => {
    const progressData = await fetch(`/api/rpa/progress/${sessionId}`);
    rpaClient.updateProgress(progressData);
}, 2000);
```

### 5. **Conclusão**
```javascript
// RPA concluído → Resultados exibidos → Botão habilitado
rpaClient.completeProcessing(progressData);
```

---

## 📊 DADOS DE TESTE

### Baseados no `parametros.json`
```json
{
    "cpf": "97137189768",
    "nome": "ALEX KAMINSKI",
    "placa": "EYQ4J41",
    "cep": "03317-000",
    "email": "alex.kaminski@imediatoseguros.com.br",
    "telefone": "11953288466"
}
```

### Validações
- **CPF**: 11 dígitos válidos
- **Placa**: Formato brasileiro (3 letras + 4 números)
- **CEP**: 8 dígitos válidos
- **Email**: Formato válido
- **Telefone**: Formato brasileiro

---

## 🎨 DESIGN DA SIMULAÇÃO

### Estilos CSS
```css
/* Simular aparência do Webflow */
.formulario-cotacao {
    max-width: 600px;
    margin: 0 auto;
    padding: 20px;
    background: #f8f9fa;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.campo-formulario {
    margin-bottom: 15px;
}

.campo-formulario label {
    display: block;
    margin-bottom: 5px;
    font-weight: 600;
    color: #2c3e50;
}

.campo-formulario input {
    width: 100%;
    padding: 12px;
    border: 2px solid #e0e0e0;
    border-radius: 5px;
    font-size: 16px;
    transition: border-color 0.3s ease;
}

.campo-formulario input:focus {
    outline: none;
    border-color: #3498db;
}

.botao-cotacao {
    width: 100%;
    padding: 15px;
    background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
    color: white;
    border: none;
    border-radius: 5px;
    font-size: 18px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
}

.botao-cotacao:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(52, 152, 219, 0.3);
}

.botao-cotacao:disabled {
    background: #bdc3c7;
    cursor: not-allowed;
    transform: none;
    box-shadow: none;
}
```

### Responsividade
```css
@media (max-width: 768px) {
    .formulario-cotacao {
        margin: 10px;
        padding: 15px;
    }
    
    .campo-formulario input {
        font-size: 16px; /* Evitar zoom no iOS */
    }
}
```

---

## 🔧 IMPLEMENTAÇÃO NO WEBFLOW

### Passo 1: Preparar Código
1. **Copiar** o conteúdo do `webflow_integration.js`
2. **Adaptar** os seletores para o formulário real
3. **Configurar** o botão de envio
4. **Testar** em ambiente de desenvolvimento

### Passo 2: Injeção no Webflow
1. **Acessar** Webflow Editor
2. **Settings** → **Custom Code**
3. **Footer Code** → **Inserir JavaScript**
4. **Publicar** o website

### Passo 3: Testes
1. **Formulário** preenchido corretamente
2. **Botão** dispara o RPA
3. **Modal** abre e atualiza
4. **Resultados** são exibidos

---

## 📋 CHECKLIST DE DESENVOLVIMENTO

### HTML de Simulação
- [ ] Formulário com campos preenchidos
- [ ] Estilos CSS inline
- [ ] Botão "Calcular" funcional
- [ ] Responsividade básica
- [ ] Referências aos campos do Webflow

### JavaScript Webflow
- [ ] Classe `WebflowRPAClient` completa
- [ ] Comentários para adaptação
- [ ] Coleta de dados do formulário
- [ ] Validação de campos
- [ ] Integração com API RPA V4
- [ ] Modal de progresso
- [ ] Monitoramento em tempo real
- [ ] Tratamento de erros

### Testes
- [ ] Simulação local funcionando
- [ ] Integração com API testada
- [ ] Modal de progresso validado
- [ ] Responsividade verificada
- [ ] Tratamento de erros testado

### Documentação
- [ ] Instruções de implementação
- [ ] Comentários no código
- [ ] Exemplos de uso
- [ ] Troubleshooting

---

## 🚀 CRONOGRAMA

### Fase 1: Desenvolvimento (2 horas)
1. **HTML de simulação** (30 min)
2. **JavaScript Webflow** (60 min)
3. **Testes básicos** (30 min)

### Fase 2: Validação (1 hora)
1. **Testes de integração** (30 min)
2. **Ajustes finais** (30 min)

### Fase 3: Documentação (30 min)
1. **Comentários no código** (15 min)
2. **Instruções de uso** (15 min)

---

## 🎯 ENTREGÁVEIS

### 1. **simulacao_webflow.html**
- HTML funcional com formulário preenchido
- Estilos CSS inline
- Botão "Calcular" para teste
- Referências claras aos campos do Webflow

### 2. **webflow_integration.js**
- JavaScript completo para Webflow
- Classe `WebflowRPAClient` com todas as funcionalidades
- Comentários detalhados para adaptação
- Instruções de implementação

### 3. **PLANO_DESENVOLVIMENTO_SIMULACAO.md**
- Este arquivo de planejamento
- Especificações técnicas completas
- Instruções de implementação
- Checklist de desenvolvimento

---

## 📞 PRÓXIMOS PASSOS

### Após Desenvolvimento
1. **Revisão** pelo engenheiro de software
2. **Testes** de integração
3. **Ajustes** conforme feedback
4. **Implementação** no Webflow
5. **Testes** em produção

### Validação Final
1. **Simulação** funcionando 100%
2. **Código** pronto para Webflow
3. **Documentação** completa
4. **Testes** aprovados

---

**Plano de desenvolvimento definido e pronto para execução.**
