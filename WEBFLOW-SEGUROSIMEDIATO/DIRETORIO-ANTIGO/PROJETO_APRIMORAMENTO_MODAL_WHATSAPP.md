# 🚀 PROJETO: APRIMORAMENTO DA CHAMADA DO WHATSAPP
## Modal WhatsApp - Integração Completa com EspoCRM, Octadesk e Google Ads

---

## 📋 INFORMAÇÃO DO PROJETO

**Nome**: Aprimoramento da chamada do WhatsApp pelo nosso novo modal WhatsApp criado  
**Objetivo**: Utilizar o modal WhatsApp de forma eficiente para captura de leads, registro em CRM e tracking de conversões  
**Status**: 📝 **PROJETO** (Não executado)  
**Estratégia**: 🔄 Implementar primeiro em **DESENVOLVIMENTO**, testar, e depois migrar para **PRODUÇÃO**

---

## 🌍 AMBIENTES: DESENVOLVIMENTO vs PRODUÇÃO

### **📋 URLs dos Endpoints por Ambiente**

| Endpoint | Ambiente | URL |
|----------|----------|-----|
| **EspoCRM** | 🧪 **DEV** | `https://bpsegurosimediato.com.br/dev/webhooks/add_travelangels.php` |
| **EspoCRM** | 🚀 **PROD** | `https://bpsegurosimediato.com.br/add_travelangels.php` |
| **Octadesk** | 🧪 **DEV** | `https://bpsegurosimediato.com.br/dev/webhooks/add_webflow_octa.php` |
| **Octadesk** | 🚀 **PROD** | `https://bpsegurosimediato.com.br/add_webflow_octa.php` |
| **Modal WhatsApp** | 🧪 **DEV** | `https://dev.bpsegurosimediato.com.br/webhooks/MODAL_WHATSAPP_DEFINITIVO.js` |
| **Modal WhatsApp** | 🚀 **PROD** | *(a definir)* |

### **🔧 Função de Detecção de Ambiente**

**SERÁ IMPLEMENTADA NO CÓDIGO**:

```javascript
/**
 * Detectar se estamos em ambiente de desenvolvimento
 */
function isDevelopmentEnvironment() {
  // Opção 1: Verificar hostname
  if (window.location.hostname.includes('dev.') || 
      window.location.hostname.includes('localhost') ||
      window.location.hostname.includes('127.0.0.1')) {
    return true;
  }
  
  // Opção 2: Verificar URL
  if (window.location.href.includes('/dev/')) {
    return true;
  }
  
  // Opção 3: Parâmetro GET
  const urlParams = new URLSearchParams(window.location.search);
  if (urlParams.get('env') === 'dev' || urlParams.get('dev') === '1') {
    return true;
  }
  
  // Opção 4: Variável global configurada
  if (typeof window.ENVIRONMENT !== 'undefined' && window.ENVIRONMENT === 'development') {
    return true;
  }
  
  return false;
}

/**
 * Obter URL do endpoint baseado no ambiente
 * @param {string} endpoint - 'travelangels' ou 'octadesk'
 * @returns {string} URL do endpoint
 */
function getEndpointUrl(endpoint) {
  const isDev = isDevelopmentEnvironment();
  
  const endpoints = {
    travelangels: {
      dev: 'https://bpsegurosimediato.com.br/dev/webhooks/add_travelangels.php',
      prod: 'https://bpsegurosimediato.com.br/add_travelangels.php'
    },
    octadesk: {
      dev: 'https://bpsegurosimediato.com.br/dev/webhooks/add_webflow_octa.php',
      prod: 'https://bpsegurosimediato.com.br/add_webflow_octa.php'
    }
  };
  
  const env = isDev ? 'dev' : 'prod';
  const url = endpoints[endpoint][env];
  
  console.log(`🌍 [MODAL] Ambiente: ${env.toUpperCase()} | Endpoint ${endpoint}: ${url}`);
  
  return url;
}
```

### **📝 Estratégia de Implementação em 2 Fases**

#### **FASE 1: DESENVOLVIMENTO** 🧪

1. **Implementar usando URLs de desenvolvimento**
   - Todas as funções usarão `getEndpointUrl()` para detectar ambiente automaticamente
   - Testes serão feitos em ambiente de desenvolvimento
   - Logs podem ser verificados em `/var/www/html/dev/logs/`

2. **Testes a realizar**
   - ✅ Testar registro inicial no EspoCRM (DEV)
   - ✅ Testar atualização no EspoCRM (DEV)
   - ✅ Testar chamada ao Octadesk (DEV)
   - ✅ Testar conversão no Google Ads (modo preview do GTM)
   - ✅ Validar tratamento de erros
   - ✅ Verificar logs de desenvolvimento

3. **Health Check**
   - URL: `https://bpsegurosimediato.com.br/dev/webhooks/health.php`
   - Verificar se endpoints estão funcionando antes de começar

#### **FASE 2: MIGRAÇÃO PARA PRODUÇÃO** 🚀

1. **Após testes bem-sucedidos**
   - A função `isDevelopmentEnvironment()` automaticamente detectará produção
   - URLs serão alteradas automaticamente sem necessidade de mudança no código
   - Ou alternativamente, forçar produção removendo detecção de dev

2. **Deploy gradual**
   - Monitorar logs de produção
   - Verificar conversões no Google Ads
   - Validar leads no EspoCRM
   - Confirmar mensagens enviadas pelo Octadesk

### **⚠️ IMPORTANTE: Modificar Funções para Usar Detecção de Ambiente**

**TODAS as funções devem usar `getEndpointUrl()`**:

```javascript
// ANTES (hardcoded - produção)
const response = await fetch('https://bpsegurosimediato.com.br/add_travelangels.php', {...});

// DEPOIS (automático - dev ou prod)
const response = await fetch(getEndpointUrl('travelangels'), {...});
```

---

## 🎯 OBJETIVOS DO PROJETO

### 1️⃣ **Registro Inicial no EspoCRM (Após Validação do Celular)**
   - Enviar registro para o EspoCRM assim que o usuário preencher e validar o celular
   - Dados mínimos: Telefone celular + GCLID
   - Momento: Após validação do campo celular (blur)

### 2️⃣ **Atualização do Registro no EspoCRM (No Click do Botão)**
   - Atualizar o registro criado anteriormente com os demais dados fornecidos
   - Dados adicionais: CPF, Nome, CEP, Placa, Endereço (se preenchidos)
   - Momento: No click do botão "IR PARA O WHATSAPP"

### 3️⃣ **Chamada ao Octadesk (No Click do Botão)**
   - Enviar mensagem para o usuário via Octadesk
   - Momento: No mesmo momento do envio do registro para o EspoCRM (click do botão)

### 4️⃣ **Registro de Conversão no Google Ads (No Click do Botão)**
   - Registrar conversão no Google Ads através do GTM
   - Momento: No mesmo momento do envio do registro para o EspoCRM (click do botão)

---

## 📊 ANÁLISE DO ESTADO ATUAL

### **Modal WhatsApp Atual**
- **Arquivo**: `MODAL_WHATSAPP_DEFINITIVO.js`
- **Localização**: `https://dev.bpsegurosimediato.com.br/webhooks/MODAL_WHATSAPP_DEFINITIVO.js`
- **Status**: Funcional, mas sem integrações com backend

### **Funcionalidades Existentes**
- ✅ Validação de DDD e Celular (com API)
- ✅ Expansão automática de campos opcionais
- ✅ Validações individuais (CPF, CEP, Placa)
- ✅ Máscaras aplicadas
- ✅ Abre WhatsApp após submit

### **Funcionalidades Faltantes**
- ❌ Registro no EspoCRM após validação do celular
- ❌ Atualização no EspoCRM no click do botão
- ❌ Chamada ao Octadesk
- ❌ Registro de conversão no Google Ads

---

## 🔧 ESPECIFICAÇÃO TÉCNICA

### **FASE 1: Registro Inicial no EspoCRM (Após Validação do Celular)**

#### **Momento**: Evento `blur` do campo CELULAR, após validação bem-sucedida

#### **Fluxo**:
1. Usuário preenche DDD e Celular
2. Validação do celular via API (se disponível)
3. Se validação OK → **Chamar endpoint `add_travelangels`**
4. Dados enviados:
   ```javascript
   {
     data: {
       'DDD-CELULAR': ddd,          // Ex: '11'
       'CELULAR': celular,           // Ex: '99999-9999' (apenas dígitos)
       'GCLID_FLD': gclid,           // Capturado dos cookies
       'NOME': '',                    // Vazio inicialmente
       'CPF': '',                     // Vazio inicialmente
       'CEP': '',                     // Vazio inicialmente
       'PLACA': '',                   // Vazio inicialmente
       'Email': '',                   // Vazio inicialmente
       'produto': 'seguro-auto',
       'landing_url': window.location.href,
       'utm_source': getUtmParam('utm_source'),
       'utm_campaign': getUtmParam('utm_campaign')
     },
     d: new Date().toISOString(),
     name: 'Modal WhatsApp - Primeiro Contato'
   }
   ```
5. Armazenar `lead_id` ou `contact_id` retornado pelo EspoCRM para atualização posterior
6. **Não bloquear** o fluxo se a chamada falhar

#### **Função a ser criada**:
```javascript
async function registrarPrimeiroContatoEspoCRM(ddd, celular, gclid) {
  const webhook_data = {
    data: {
      'DDD-CELULAR': ddd,
      'CELULAR': onlyDigits(celular),
      'GCLID_FLD': gclid || '',
      'NOME': '',
      'CPF': '',
      'CEP': '',
      'PLACA': '',
      'Email': '',
      'produto': 'seguro-auto',
      'landing_url': window.location.href,
      'utm_source': getUtmParam('utm_source'),
      'utm_campaign': getUtmParam('utm_campaign')
    },
    d: new Date().toISOString(),
    name: 'Modal WhatsApp - Primeiro Contato'
  };

  try {
    // ✅ Usar getEndpointUrl() para detectar ambiente automaticamente
    const endpointUrl = getEndpointUrl('travelangels');
    
    const response = await fetch(endpointUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'User-Agent': 'Modal-WhatsApp-v1.0'
      },
      body: JSON.stringify(webhook_data)
    });

    const result = await response.json();
    
    if (result.success || response.ok) {
      console.log('✅ [MODAL] Lead criado no EspoCRM:', result);
      // Armazenar ID para atualização posterior (se disponível)
      if (result.contact_id || result.lead_id) {
        window.modalEspoCRMId = result.contact_id || result.lead_id;
      }
      return { success: true, id: result.contact_id || result.lead_id };
    } else {
      console.warn('⚠️ [MODAL] Erro ao criar lead no EspoCRM:', result);
      return { success: false, error: result };
    }
  } catch (error) {
    console.error('❌ [MODAL] Erro na requisição ao EspoCRM:', error);
    return { success: false, error: error.message };
  }
}
```

#### **Integração no código existente**:
```javascript
// No evento blur do CELULAR (após validação bem-sucedida)
$(MODAL_CONFIG.fieldIds.celular).on('blur', debounce(function() {
  // ... código de validação existente ...
  
  if (celularDigits === 9 && dddDigits === 2) {
    showLoading('Validando celular…');
    validarTelefoneAsync($(MODAL_CONFIG.fieldIds.ddd), $(this)).then(res => {
      hideLoading();
      if (res.ok) {
        showFieldSuccess($(this));
        
        // ✅ NOVO: Registrar primeiro contato no EspoCRM
        const ddd = $(MODAL_CONFIG.fieldIds.ddd).val();
        const celular = $(this).val();
        const gclid = getGCLID();
        
        registrarPrimeiroContatoEspoCRM(ddd, celular, gclid)
          .then(result => {
            if (result.success) {
              console.log('✅ [MODAL] Primeiro contato registrado:', result.id);
            }
          })
          .catch(error => {
            console.warn('⚠️ [MODAL] Erro ao registrar primeiro contato (não bloqueante)');
          });
      } else {
        showFieldWarning($(this), 'Celular inválido');
      }
    });
  }
}, 500));
```

---

### **FASE 2: Atualização no EspoCRM + Chamada Octadesk + Conversão Google Ads**

#### **Momento**: Evento `submit` do formulário (click do botão "IR PARA O WHATSAPP")

#### **Fluxo**:
1. Validar DDD e Celular (obrigatórios)
2. Coletar todos os dados preenchidos
3. **Chamar endpoint `add_travelangels`** com dados completos (atualização)
4. **Chamar endpoint `add_webflow_octa`** para enviar mensagem WhatsApp
5. **Registrar conversão no Google Ads** via `dataLayer.push()`
6. Abrir WhatsApp
7. Fechar modal

#### **Função a ser criada - Atualização EspoCRM**:
```javascript
async function atualizarLeadEspoCRM(dados, espocrmId = null) {
  const webhook_data = {
    data: {
      'NOME': dados.NOME || '',
      'DDD-CELULAR': dados.DDD || '',
      'CELULAR': onlyDigits(dados.CELULAR) || '',
      'Email': dados.EMAIL || '',
      'CEP': dados.CEP || '',
      'CPF': dados.CPF || '',
      'PLACA': dados.PLACA || '',
      'MARCA': dados.MARCA || '',
      'VEICULO': dados.MARCA || '',
      'ANO': dados.ANO || '',
      'GCLID_FLD': dados.GCLID || '',
      'SEXO': dados.SEXO || '',
      'DATA-DE-NASCIMENTO': dados.DATA_NASCIMENTO || '',
      'ESTADO-CIVIL': dados.ESTADO_CIVIL || '',
      'ENDERECO': dados.ENDERECO || '',
      'produto': 'seguro-auto',
      'landing_url': window.location.href,
      'utm_source': getUtmParam('utm_source'),
      'utm_campaign': getUtmParam('utm_campaign')
    },
    d: new Date().toISOString(),
    name: 'Modal WhatsApp - Dados Completos'
  };

  // Se tiver ID do lead criado anteriormente, incluir no payload
  if (espocrmId) {
    webhook_data.data.lead_id = espocrmId;
    webhook_data.data.contact_id = espocrmId;
  }

  try {
    // ✅ Usar getEndpointUrl() para detectar ambiente automaticamente
    const endpointUrl = getEndpointUrl('travelangels');
    
    const response = await fetch(endpointUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'User-Agent': 'Modal-WhatsApp-v1.0'
      },
      body: JSON.stringify(webhook_data)
    });

    const result = await response.json();
    return { success: response.ok, result };
  } catch (error) {
    console.error('❌ [MODAL] Erro ao atualizar lead no EspoCRM:', error);
    return { success: false, error: error.message };
  }
}
```

#### **Função a ser criada - Chamada Octadesk**:
```javascript
async function enviarMensagemOctadesk(dados) {
  const webhook_data = {
    data: {
      'NOME': dados.NOME || '',
      'DDD-CELULAR': dados.DDD || '',
      'CELULAR': onlyDigits(dados.CELULAR) || '',
      'Email': dados.EMAIL || '',
      'CEP': dados.CEP || '',
      'CPF': dados.CPF || '',
      'PLACA': dados.PLACA || '',
      'MARCA': dados.MARCA || '',
      'VEICULO': dados.MARCA || '',
      'ANO': dados.ANO || '',
      'GCLID_FLD': dados.GCLID || '',
      'SEXO': dados.SEXO || '',
      'DATA-DE-NASCIMENTO': dados.DATA_NASCIMENTO || '',
      'ESTADO-CIVIL': dados.ESTADO_CIVIL || '',
      'ENDERECO': dados.ENDERECO || '',
      'produto': 'seguro-auto',
      'landing_url': window.location.href,
      'utm_source': getUtmParam('utm_source'),
      'utm_campaign': getUtmParam('utm_campaign')
    },
    d: new Date().toISOString(),
    name: 'Modal WhatsApp - Mensagem Octadesk'
  };

  try {
    // ✅ Usar getEndpointUrl() para detectar ambiente automaticamente
    const endpointUrl = getEndpointUrl('octadesk');
    
    const response = await fetch(endpointUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'User-Agent': 'Modal-WhatsApp-v1.0'
      },
      body: JSON.stringify(webhook_data)
    });

    const result = await response.json();
    return { success: response.ok, result };
  } catch (error) {
    console.error('❌ [MODAL] Erro ao enviar mensagem via Octadesk:', error);
    return { success: false, error: error.message };
  }
}
```

#### **Função a ser criada - Conversão Google Ads**:
```javascript
function registrarConversaoGoogleAds(dados) {
  if (typeof window.dataLayer === 'undefined') {
    console.warn('⚠️ [MODAL] dataLayer não disponível para registro de conversão');
    return;
  }

  window.dataLayer.push({
    'event': 'whatsapp_modal_submit',
    'form_type': 'whatsapp_modal',
    'validation_status': 'valid',
    'phone': dados.CELULAR,
    'has_cpf': !!dados.CPF,
    'has_placa': !!dados.PLACA,
    'has_cep': !!dados.CEP,
    'has_nome': !!dados.NOME,
    'gclid': dados.GCLID || ''
  });

  console.log('✅ [MODAL] Conversão registrada no Google Ads');
}
```

#### **Integração no código existente - Submit**:
```javascript
$form.on('submit', async function(e) {
  e.preventDefault();
  e.stopPropagation();
  
  console.log('🎯 [MODAL] Submit do formulário');
  
  // Validar DDD + Celular (obrigatórios)
  const ddd = $(MODAL_CONFIG.fieldIds.ddd).val();
  const celular = $(MODAL_CONFIG.fieldIds.celular).val();
  
  if (!ddd || onlyDigits(ddd).length !== 2) {
    alert('Por favor, preencha o DDD corretamente.');
    $(MODAL_CONFIG.fieldIds.ddd).focus();
    return;
  }
  
  if (!celular || onlyDigits(celular).length !== 9) {
    alert('Por favor, preencha o celular corretamente.');
    $(MODAL_CONFIG.fieldIds.celular).focus();
    return;
  }
  
  // Coletar todos os dados
  const dados = coletarTodosDados();
  dados.DDD = ddd;
  dados.GCLID = getGCLID();
  
  console.log('📋 [MODAL] Dados coletados:', dados);
  
  // Mostrar loading
  showLoading('Processando seus dados...');
  
  try {
    // 1. Atualizar lead no EspoCRM
    const espocrmId = window.modalEspoCRMId || null;
    const espocrmResult = await atualizarLeadEspoCRM(dados, espocrmId);
    
    if (espocrmResult.success) {
      console.log('✅ [MODAL] Lead atualizado no EspoCRM');
    } else {
      console.warn('⚠️ [MODAL] Erro ao atualizar lead (não bloqueante)');
    }
    
    // 2. Enviar mensagem via Octadesk
    const octadeskResult = await enviarMensagemOctadesk(dados);
    
    if (octadeskResult.success) {
      console.log('✅ [MODAL] Mensagem enviada via Octadesk');
    } else {
      console.warn('⚠️ [MODAL] Erro ao enviar mensagem (não bloqueante)');
    }
    
    // 3. Registrar conversão no Google Ads
    registrarConversaoGoogleAds(dados);
    
    // 4. Esconder loading
    hideLoading();
    
    // 5. Fechar modal e abrir WhatsApp
    console.log('✅ [MODAL] Processo concluído, abrindo WhatsApp');
    $modal.fadeOut(300, function() {
      openWhatsApp(dados);
    });
    
  } catch (error) {
    hideLoading();
    console.error('❌ [MODAL] Erro no processo:', error);
    
    // Mesmo com erro, permitir abrir WhatsApp (não bloquear usuário)
    alert('Seus dados foram processados. Abrindo WhatsApp...');
    $modal.fadeOut(300, function() {
      openWhatsApp(dados);
    });
  }
});
```

---

## 🛠️ FUNÇÕES AUXILIARES NECESSÁRIAS

### **Função para obter parâmetros UTM**:
```javascript
function getUtmParam(param) {
  const urlParams = new URLSearchParams(window.location.search);
  return urlParams.get(param) || '';
}
```

### **Função para exibir loading**:
```javascript
function showLoading(message) {
  // Usar função existente do Footer Code ou criar nova
  if (typeof window.showLoading === 'function') {
    window.showLoading(message);
  } else {
    // Implementação básica
    const overlay = document.getElementById('si-loading-overlay');
    const text = document.getElementById('si-loading-text');
    if (overlay) overlay.style.display = 'flex';
    if (text && message) text.textContent = message;
  }
}

function hideLoading() {
  if (typeof window.hideLoading === 'function') {
    window.hideLoading();
  } else {
    const overlay = document.getElementById('si-loading-overlay');
    if (overlay) overlay.style.display = 'none';
  }
}
```

---

## 📁 ARQUIVOS A SEREM MODIFICADOS

1. **`MODAL_WHATSAPP_DEFINITIVO.js`**
   - Adicionar função `registrarPrimeiroContatoEspoCRM()`
   - Adicionar função `atualizarLeadEspoCRM()`
   - Adicionar função `enviarMensagemOctadesk()`
   - Adicionar função `registrarConversaoGoogleAds()`
   - Adicionar função `getUtmParam()`
   - Modificar evento `blur` do campo CELULAR
   - Modificar evento `submit` do formulário

---

## 🔄 FLUXO COMPLETO PROPOSTO

```
┌─────────────────────────────────────────────────────────────┐
│ USUÁRIO CLICA NO LINK WHATSAPP                               │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│ MODAL WHATSAPP ABRE                                          │
│ - DIV 1: DDD + CELULAR (sempre visível)                     │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│ USUÁRIO PREENCHE DDD + CELULAR                              │
│ - Validação local (DDD = 2 dígitos, CELULAR = 9 dígitos)   │
│ - Validação via API (se disponível)                         │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│ ✅ VALIDAÇÃO OK                                               │
│ 📞 CHAMAR add_travelangels.php (EspoCRM)                     │
│    - Dados: DDD, CELULAR, GCLID                             │
│    - Armazenar ID retornado                                  │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│ DIV 2: CAMPOS OPCIONAIS EXPANDIDOS                          │
│ - CPF                                                         │
│ - Nome                                                        │
│ - CEP                                                         │
│ - Placa                                                       │
│ - Endereço (se CEP preenchido)                               │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│ USUÁRIO CLICA EM "IR PARA O WHATSAPP"                       │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│ 1️⃣ ATUALIZAR LEAD NO ESPOCRM                                 │
│    - Endpoint: add_travelangels.php                          │
│    - Dados completos (DDD, CELULAR, CPF, NOME, CEP, PLACA) │
│    - Incluir ID do lead criado anteriormente (se houver)    │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│ 2️⃣ ENVIAR MENSAGEM OCTADESK                                   │
│    - Endpoint: add_webflow_octa.php                          │
│    - Dados completos                                         │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│ 3️⃣ REGISTRAR CONVERSÃO GOOGLE ADS                             │
│    - dataLayer.push({ event: 'whatsapp_modal_submit' })     │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│ 4️⃣ FECHAR MODAL E ABRIR WHATSAPP                             │
│    - window.open(whatsappUrl, '_blank')                     │
└─────────────────────────────────────────────────────────────┘
```

---

## ⚠️ CONSIDERAÇÕES IMPORTANTES

### **Tratamento de Erros**
- **Não bloquear o usuário** se alguma chamada falhar
- Sempre permitir abrir o WhatsApp mesmo em caso de erro
- Registrar erros no console para debug
- Considerar implementar retry para chamadas críticas

### **Performance**
- Chamadas devem ser assíncronas (async/await)
- Considerar executar chamadas em paralelo (Promise.all) quando possível
- Timeout de 30s para cada endpoint (seguir padrão existente)

### **Compatibilidade**
- Verificar se `dataLayer` está disponível antes de registrar conversão
- Verificar se funções de loading existem antes de usar
- Manter compatibilidade com código existente

### **Segurança**
- Validar todos os dados antes de enviar
- Não expor informações sensíveis no console
- Usar HTTPS para todas as requisições

---

## 🧪 TESTES A SEREM REALIZADOS

### **Cenário 1: Usuário preenche apenas DDD + Celular**
- ✅ Validar registro inicial no EspoCRM
- ✅ Validar expansão da DIV 2
- ✅ Validar click no botão (sem campos opcionais)

### **Cenário 2: Usuário preenche todos os campos**
- ✅ Validar registro inicial no EspoCRM
- ✅ Validar atualização no EspoCRM com todos os dados
- ✅ Validar chamada ao Octadesk
- ✅ Validar conversão no Google Ads

### **Cenário 3: Falha na chamada do EspoCRM**
- ✅ Validar que o fluxo continua (não bloqueia)
- ✅ Validar abertura do WhatsApp mesmo com erro

### **Cenário 4: GCLID presente**
- ✅ Validar captura do GCLID dos cookies
- ✅ Validar envio do GCLID nos webhooks

---

## 💾 BACKUP E VERSIONAMENTO

### **⚠️ CRÍTICO: Criar Backups Antes de Qualquer Implementação**

**NUNCA iniciar modificações sem criar backups completos dos arquivos originais!**

### **📋 Checklist de Backup**

#### **1. Backup Local dos Arquivos Fonte**

Antes de qualquer modificação, criar backups locais:

```bash
# Criar diretório de backup com timestamp
mkdir -p backups/pre-implementacao-modal-whatsapp-$(date +%Y%m%d_%H%M%S)
cd backups/pre-implementacao-modal-whatsapp-$(date +%Y%m%d_%H%M%S)

# Copiar arquivo do modal (se existir localmente)
cp ../../MODAL_WHATSAPP_DEFINITIVO.js ./MODAL_WHATSAPP_DEFINITIVO_BACKUP.js

# Copiar footer code
cp ../../02-DEVELOPMENT/custom-codes/"Footer Code Site Definitivo.js" ./Footer_Code_BACKUP.js
```

#### **2. Backup no Servidor (via SSH/FTP)**

**Via SSH:**
```bash
# Conectar ao servidor
ssh usuario@bpsegurosimediato.com.br

# Criar diretório de backup no servidor
mkdir -p /var/www/html/backups/pre-implementacao-modal-$(date +%Y%m%d_%H%M%S)
cd /var/www/html/backups/pre-implementacao-modal-$(date +%Y%m%d_%H%M%S)

# Backup do modal em produção (se existir)
cp /var/www/html/webhooks/MODAL_WHATSAPP_DEFINITIVO.js ./MODAL_WHATSAPP_DEFINITIVO_PROD_BACKUP.js 2>/dev/null || echo "Arquivo não encontrado em produção"

# Backup do modal em desenvolvimento
cp /var/www/html/dev/webhooks/MODAL_WHATSAPP_DEFINITIVO.js ./MODAL_WHATSAPP_DEFINITIVO_DEV_BACKUP.js 2>/dev/null || echo "Arquivo não encontrado em dev"

# Backup dos endpoints de desenvolvimento
cp /var/www/html/dev/webhooks/add_travelangels.php ./add_travelangels_DEV_BACKUP.php 2>/dev/null || echo "Arquivo não encontrado"
cp /var/www/html/dev/webhooks/add_webflow_octa.php ./add_webflow_octa_DEV_BACKUP.php 2>/dev/null || echo "Arquivo não encontrado"

# Listar arquivos de backup criados
ls -lah
```

**Via FTP/SFTP:**
1. Conectar ao servidor via cliente FTP (FileZilla, WinSCP, etc.)
2. Navegar até `/var/www/html/dev/webhooks/`
3. Baixar arquivos:
   - `MODAL_WHATSAPP_DEFINITIVO.js`
   - `add_travelangels.php` (se for modificar)
   - `add_webflow_octa.php` (se for modificar)
4. Salvar em diretório local com timestamp: `backups/pre-implementacao-[data-hora]/`

#### **3. Backup via Git (Recomendado)**

Se o projeto usa controle de versão:

```bash
# Verificar status do Git
git status

# Criar branch de backup antes das mudanças
git checkout -b backup/pre-implementacao-modal-whatsapp-$(date +%Y%m%d)

# Fazer commit do estado atual
git add .
git commit -m "BACKUP: Estado antes da implementação do aprimoramento do modal WhatsApp"

# Criar tag de backup
git tag -a backup-pre-modal-whatsapp-$(date +%Y%m%d) -m "Backup antes de implementação modal WhatsApp"

# Voltar para branch principal
git checkout main  # ou master, conforme seu repositório

# Criar branch de desenvolvimento
git checkout -b feature/modal-whatsapp-integration
```

#### **4. Backup do Webflow (Custom Code)**

Se modificações forem feitas no Custom Code do Webflow:

1. **Acessar Webflow Designer**
2. **Ir em**: Settings → Custom Code
3. **Localizar**: Footer Code
4. **Copiar todo o conteúdo** e salvar em:
   ```
   backups/pre-implementacao-[data-hora]/Webflow_Custom_Code_Footer_BACKUP.js
   ```
5. **Screenshot** da configuração também é recomendado

#### **5. Estrutura de Backup Recomendada**

```
backups/
└── pre-implementacao-modal-whatsapp-20250123_143000/
    ├── MODAL_WHATSAPP_DEFINITIVO_BACKUP.js
    ├── Footer_Code_BACKUP.js
    ├── dev/
    │   └── webhooks/
    │       ├── MODAL_WHATSAPP_DEFINITIVO_DEV_BACKUP.js
    │       ├── add_travelangels_DEV_BACKUP.php
    │       └── add_webflow_octa_DEV_BACKUP.php
    ├── README_BACKUP.md        # Notas sobre o que foi feito
    └── webflow_custom_code_backup.txt
```

### **📝 Template de README_BACKUP.md**

Criar arquivo `README_BACKUP.md` no diretório de backup:

```markdown
# 📦 BACKUP: Pré-Implementação Modal WhatsApp
**Data**: 2025-01-23 14:30:00  
**Versão Anterior**: MODAL_WHATSAPP_DEFINITIVO.js v15  
**Motivo**: Implementação de integração com EspoCRM, Octadesk e Google Ads

## 📋 Arquivos Incluídos neste Backup

- ✅ MODAL_WHATSAPP_DEFINITIVO.js (original)
- ✅ Footer Code Site Definitivo.js (original)
- ✅ Endpoints de desenvolvimento (se modificados)

## 🔄 Como Restaurar

### Restaurar Modal WhatsApp:
```bash
cp MODAL_WHATSAPP_DEFINITIVO_BACKUP.js /caminho/original/MODAL_WHATSAPP_DEFINITIVO.js
```

### Restaurar via Git:
```bash
git checkout backup-pre-modal-whatsapp-20250123
```

## ⚠️ AVISOS

- Este backup foi criado ANTES da implementação
- Não modificar este diretório
- Manter por pelo menos 30 dias após implementação bem-sucedida
```

### **✅ Checklist Pré-Implementação**

Antes de começar QUALQUER modificação:

- [ ] **Backup local criado** (diretório com timestamp)
- [ ] **Backup no servidor criado** (arquivos copiados)
- [ ] **Git commit/tag de backup** (se usar Git)
- [ ] **Webflow Custom Code copiado** (se aplicável)
- [ ] **README_BACKUP.md criado** com informações relevantes
- [ ] **Screenshots de configurações** (se aplicável)
- [ ] **Lista de arquivos modificados** documentada

### **🔄 Procedimento de Rollback**

Se algo der errado durante implementação:

#### **Rollback Rápido (via Git)**:
```bash
# Descartar todas as mudanças e voltar ao estado do backup
git reset --hard backup-pre-modal-whatsapp-20250123

# OU voltar para a tag
git checkout backup-pre-modal-whatsapp-20250123
```

#### **Rollback Manual (servidor)**:
```bash
# Conectar ao servidor
ssh usuario@bpsegurosimediato.com.br

# Restaurar arquivos de backup
cp /var/www/html/backups/pre-implementacao-modal-*/MODAL_WHATSAPP_DEFINITIVO_DEV_BACKUP.js \
   /var/www/html/dev/webhooks/MODAL_WHATSAPP_DEFINITIVO.js

# Verificar permissões
chmod 644 /var/www/html/dev/webhooks/MODAL_WHATSAPP_DEFINITIVO.js
chown www-data:www-data /var/www/html/dev/webhooks/MODAL_WHATSAPP_DEFINITIVO.js
```

#### **Rollback Webflow**:
1. Acessar Webflow Designer
2. Settings → Custom Code
3. Colar conteúdo do arquivo `Webflow_Custom_Code_Footer_BACKUP.js`
4. Salvar e publicar

---

## 📝 CHECKLIST DE IMPLEMENTAÇÃO

### **💾 FASE 0: Backup e Preparação**
- [ ] Criar backup local de todos os arquivos
- [ ] Criar backup no servidor (via SSH/FTP)
- [ ] Criar branch/tag de backup no Git
- [ ] Documentar estado atual em README_BACKUP.md
- [ ] Verificar acesso ao servidor e permissões
- [ ] Testar rollback (confirmar que backup funciona)

### **🔧 Funções Base (Detecção de Ambiente)**
- [ ] Criar função `isDevelopmentEnvironment()`
- [ ] Criar função `getEndpointUrl(endpoint)`

### **📞 Funções de Integração**
- [ ] Criar função `registrarPrimeiroContatoEspoCRM()` (usar `getEndpointUrl()`)
- [ ] Criar função `atualizarLeadEspoCRM()` (usar `getEndpointUrl()`)
- [ ] Criar função `enviarMensagemOctadesk()` (usar `getEndpointUrl()`)
- [ ] Criar função `registrarConversaoGoogleAds()`
- [ ] Criar função `getUtmParam()`

### **⚙️ Modificações no Modal**
- [ ] Modificar evento `blur` do campo CELULAR
- [ ] Modificar evento `submit` do formulário

### **🧪 Testes em Desenvolvimento**
- [ ] Testar detecção de ambiente (verificar logs console)
- [ ] Testar registro inicial no EspoCRM (DEV)
- [ ] Testar atualização no EspoCRM (DEV)
- [ ] Testar chamada ao Octadesk (DEV)
- [ ] Testar conversão no Google Ads (modo preview GTM)
- [ ] Validar tratamento de erros
- [ ] Verificar logs em `/var/www/html/dev/logs/`
- [ ] Testar com diferentes cenários (com/sem campos opcionais)

### **🚀 Migração para Produção**
- [ ] Validar que detecção de ambiente funciona em produção
- [ ] Testar em produção (staging se disponível)
- [ ] Monitorar logs de produção
- [ ] Validar conversões no Google Ads
- [ ] Confirmar leads no EspoCRM
- [ ] Verificar mensagens Octadesk

### **📚 Documentação**
- [ ] Documentar alterações no código
- [ ] Atualizar este documento com resultados dos testes
- [ ] Criar guia de troubleshooting
- [ ] Documentar procedimento de rollback executado (se necessário)

### **🔄 Pós-Implementação**
- [ ] Validar que backups estão seguros e acessíveis
- [ ] Testar procedimento de rollback (simulação)
- [ ] Manter backups por pelo menos 30 dias
- [ ] Documentar data de criação dos backups

---

## 📚 REFERÊNCIAS

- **Especificação de Endpoints**: `02-DEVELOPMENT/ESPECIFICACAO_REGISTRO_CONVERSOES_E_ENDPOINTS.md`
- **Modal WhatsApp Atual**: `MODAL_WHATSAPP_DEFINITIVO.js`
- **Footer Code**: `02-DEVELOPMENT/custom-codes/Footer Code Site Definitivo.js`

---

**Data de Criação**: 2025-01-23  
**Versão**: 1.0  
**Status**: 📝 PROJETO (Não executado)

