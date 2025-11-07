# 🚀 PROJETO: APRIMORAMENTO DA CHAMADA DO WHATSAPP - VERSÃO 3 (DEBUG)
## Modal WhatsApp - Integração Completa com Logs de Debug Detalhados
### 🔍 Versão com Logging Completo para Testes e Diagnóstico

---

## 📋 INFORMAÇÃO DO PROJETO

**Nome**: Aprimoramento da chamada do WhatsApp pelo nosso novo modal WhatsApp criado - V3 (Debug)  
**Versão**: 3.0 - Debug & Observability  
**Objetivo**: Adicionar logs detalhados e compreensivos para facilitar testes e diagnóstico  
**Status**: 📝 **PROJETO** (Não executado)  
**Estratégia**: 🔍 **FASE 3** - Implementar após V2 (V2 já implementada)

---

## 🆕 MUDANÇAS PRINCIPAIS (V3 vs V2)

### **Fluxo V2 (Implementado)**:
1. ✅ Usuário valida celular → Processamento PARALELO (EspoCRM + Octadesk + GTM)
2. ✅ Usuário clica botão → Atualiza EspoCRM (se houver dados novos)

### **Fluxo V3 (Adiciona Logging)**:
1. ✅ **LOGS ANTES DAS CHAMADAS**: Mostrar JSON completo que será enviado
2. ✅ **LOGS DE GTM**: Mostrar dados que serão enviados ao dataLayer
3. ✅ **LOGS DE RESPOSTAS**: Detalhar respostas recebidas
4. ✅ **LOGS DE ESTADO**: Mostrar estado do localStorage e variáveis
5. ✅ **LOGS DE ERROS**: Detalhar erros com contexto completo

---

## 🎯 OBJETIVOS DO PROJETO V3

### 1️⃣ **Logs Compreensíveis e Detalhados**
   - **Quando**: Antes de TODAS as chamadas aos endpoints
   - **Conteúdo**: 
     - ✅ JSON completo que será enviado
     - ✅ URL do endpoint
     - ✅ Método HTTP
     - ✅ Headers
     - ✅ Ambiente detectado (DEV/PROD)

### 2️⃣ **Logs Específicos para GTM**
   - **Quando**: Antes de `dataLayer.push()`
   - **Conteúdo**:
     - ✅ Objeto completo que será enviado
     - ✅ Todas as variáveis GTM utilizadas
     - ✅ Valores finais (com fallbacks aplicados)

### 3️⃣ **Logs de Estado e Contexto**
   - **Quando**: Em momentos-chave do fluxo
   - **Conteúdo**:
     - ✅ Estado do localStorage
     - ✅ Flags de controle (initialRegistrationAttempted)
     - ✅ Dados coletados do formulário
     - ✅ IDs recuperados/gerados

---

## 🔧 ESPECIFICAÇÃO TÉCNICA V3

### **FUNÇÃO 1: Logger Centralizado com Níveis**

#### **Implementação**:

```javascript
/**
 * Sistema de logging detalhado para debug
 * @param {string} category - Categoria do log ('ESPOCRM', 'OCTADESK', 'GTM', 'STATE', 'ERROR')
 * @param {string} action - Ação sendo executada
 * @param {Object} data - Dados detalhados
 * @param {string} level - Nível do log ('info', 'warn', 'error', 'debug')
 */
function debugLog(category, action, data = {}, level = 'info') {
  const timestamp = new Date().toISOString();
  const environment = isDevelopmentEnvironment() ? '🔧 DEV' : '🚀 PROD';
  
  // Emoji por categoria
  const categoryEmojis = {
    'ESPOCRM': '📊',
    'OCTADESK': '📱',
    'GTM': '📈',
    'STATE': '💾',
    'ERROR': '❌',
    'PARALLEL': '⚡',
    'VALIDATION': '✅'
  };
  
  const emoji = categoryEmojis[category] || '📝';
  
  // Formatar dados para exibição
  const formattedData = {
    timestamp,
    environment,
    category,
    action,
    ...data
  };
  
  // Log formatado no console
  const logMessage = `${emoji} [${category}] ${action}`;
  const logData = {
    ...formattedData,
    data_stringified: JSON.stringify(data, null, 2)
  };
  
  // Escolher método de log baseado no nível
  switch(level) {
    case 'error':
      console.error(logMessage, logData);
      break;
    case 'warn':
      console.warn(logMessage, logData);
      break;
    case 'debug':
      console.debug(logMessage, logData);
      break;
    default:
      console.log(logMessage, logData);
  }
  
  // Se disponível, enviar para sistema de logging
  try {
    if (typeof window.logDebug === 'function') {
      window.logDebug(level.toUpperCase(), `[MODAL V3] ${category} - ${action}`, formattedData);
    }
  } catch (e) {
    // Falha silenciosa
  }
}
```

---

### **FUNÇÃO 2: Log Antes de Chamada EspoCRM**

#### **Implementação em `registrarPrimeiroContatoEspoCRM()`**:

```javascript
async function registrarPrimeiroContatoEspoCRM(ddd, celular, gclid) {
  // ✅ V3: LOG DETALHADO ANTES DA CHAMADA
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
    name: 'Modal WhatsApp - Primeiro Contato (V2)'
  };
  
  const endpointUrl = getEndpointUrl('travelangels');
  
  // ✅ V3: LOG COMPLETO ANTES DA CHAMADA
  debugLog('ESPOCRM', 'INITIAL_REQUEST_PREPARATION', {
    endpoint_url: endpointUrl,
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'User-Agent': 'Modal-WhatsApp-v2.0'
    },
    payload: webhook_data,
    payload_json: JSON.stringify(webhook_data, null, 2),
    input_data: {
      ddd: ddd,
      celular: '***' + onlyDigits(celular).slice(-4), // Não expor completo
      gclid: gclid || '(vazio)',
      gclid_length: (gclid || '').length
    },
    rate_limiting: {
      phone_key: `${ddd}${onlyDigits(celular)}`,
      can_make_call: rateLimiter.canMakeCall(`${ddd}${onlyDigits(celular)}`)
    }
  }, 'info');
  
  // Verificar rate limiting
  const phoneKey = `${ddd}${onlyDigits(celular)}`;
  if (!rateLimiter.canMakeCall(phoneKey)) {
    debugLog('ESPOCRM', 'RATE_LIMIT_EXCEEDED', {
      phone_key: phoneKey,
      message: 'Muitas tentativas recentes, aguarde...'
    }, 'warn');
    return { success: false, error: 'rate_limit' };
  }
  
  debugLog('ESPOCRM', 'INITIAL_REQUEST_STARTING', {
    endpoint_url: endpointUrl,
    attempt: 1,
    max_retries: 2
  }, 'info');
  
  try {
    const result = await fetchWithRetry(endpointUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'User-Agent': 'Modal-WhatsApp-v2.0'
      },
      body: JSON.stringify(webhook_data)
    }, 2, 1000);
    
    // ✅ V3: LOG DA RESPOSTA
    debugLog('ESPOCRM', 'INITIAL_RESPONSE_RECEIVED', {
      success: result.success,
      attempt: result.attempt + 1,
      http_status: result.response?.status || 'N/A',
      has_response_data: !!result.response,
      error: result.error || null
    }, result.success ? 'info' : 'warn');
    
    if (result.success && result.response) {
      try {
        const responseData = await result.response.json();
        
        // ✅ V3: LOG DA RESPOSTA PARSEADA
        debugLog('ESPOCRM', 'INITIAL_RESPONSE_PARSED', {
          response_data: responseData,
          response_json: JSON.stringify(responseData, null, 2),
          lead_id: responseData.contact_id || responseData.lead_id || null,
          success: responseData.success || result.response.ok
        }, 'info');
        
        if (responseData.success || result.response.ok) {
          const leadId = responseData.contact_id || responseData.lead_id || null;
          
          if (leadId) {
            saveLeadState({ id: leadId, ddd, celular, gclid });
            
            // ✅ V3: LOG DO ESTADO SALVO
            debugLog('STATE', 'LEAD_STATE_SAVED', {
              lead_id: leadId,
              ddd: ddd,
              celular: '***' + onlyDigits(celular).slice(-4),
              gclid: gclid || '(vazio)',
              localStorage_key: 'whatsapp_modal_lead_state'
            }, 'info');
          }
          
          return { success: true, id: leadId, attempt: result.attempt + 1 };
        }
      } catch (parseError) {
        debugLog('ESPOCRM', 'INITIAL_RESPONSE_PARSE_ERROR', {
          error: parseError.message,
          response_ok: result.response.ok,
          response_status: result.response.status
        }, 'warn');
        return { success: result.response.ok, attempt: result.attempt + 1 };
      }
    }
    
    return { success: false, error: result.error, attempt: result.attempt + 1 };
    
  } catch (error) {
    debugLog('ERROR', 'ESPOCRM_INITIAL_EXCEPTION', {
      error_message: error.message,
      error_stack: error.stack,
      error_name: error.name
    }, 'error');
    return { success: false, error: error.message };
  }
}
```

---

### **FUNÇÃO 3: Log Antes de Chamada Octadesk**

#### **Implementação em `enviarMensagemInicialOctadesk()`**:

```javascript
async function enviarMensagemInicialOctadesk(ddd, celular, gclid) {
  const webhook_data = {
    data: {
      'DDD-CELULAR': ddd,
      'CELULAR': onlyDigits(celular),
      'GCLID_FLD': gclid || '',
      'NOME': '',
      'CPF': '',
      'Email': '',
      'produto': 'seguro-auto',
      'landing_url': window.location.href,
      'utm_source': getUtmParam('utm_source'),
      'utm_campaign': getUtmParam('utm_campaign')
    },
    d: new Date().toISOString(),
    name: 'Modal WhatsApp - Mensagem Inicial (V2)'
  };
  
  const endpointUrl = getEndpointUrl('octadesk');
  
  // ✅ V3: LOG COMPLETO ANTES DA CHAMADA OCTADESK
  debugLog('OCTADESK', 'INITIAL_REQUEST_PREPARATION', {
    endpoint_url: endpointUrl,
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'User-Agent': 'Modal-WhatsApp-v2.0'
    },
    payload: webhook_data,
    payload_json: JSON.stringify(webhook_data, null, 2),
    input_data: {
      ddd: ddd,
      celular: '***' + onlyDigits(celular).slice(-4),
      gclid: gclid || '(vazio)'
    }
  }, 'info');
  
  debugLog('OCTADESK', 'INITIAL_REQUEST_STARTING', {
    endpoint_url: endpointUrl,
    attempt: 1,
    max_retries: 2
  }, 'info');
  
  try {
    const result = await fetchWithRetry(endpointUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'User-Agent': 'Modal-WhatsApp-v2.0'
      },
      body: JSON.stringify(webhook_data)
    }, 2, 1000);
    
    // ✅ V3: LOG DA RESPOSTA OCTADESK
    debugLog('OCTADESK', 'INITIAL_RESPONSE_RECEIVED', {
      success: result.success,
      attempt: result.attempt + 1,
      http_status: result.response?.status || 'N/A',
      has_response_data: !!result.response,
      error: result.error || null
    }, result.success ? 'info' : 'warn');
    
    if (result.success && result.response) {
      try {
        const responseData = await result.response.json();
        
        // ✅ V3: LOG DA RESPOSTA PARSEADA OCTADESK
        debugLog('OCTADESK', 'INITIAL_RESPONSE_PARSED', {
          response_data: responseData,
          response_json: JSON.stringify(responseData, null, 2),
          success: result.response.ok
        }, 'info');
        
        return { success: true, result: responseData, attempt: result.attempt + 1 };
      } catch (parseError) {
        debugLog('OCTADESK', 'INITIAL_RESPONSE_PARSE_ERROR', {
          error: parseError.message,
          response_ok: result.response.ok
        }, 'warn');
        return { success: result.response.ok, attempt: result.attempt + 1 };
      }
    }
    
    return { success: false, error: result.error, attempt: result.attempt + 1 };
    
  } catch (error) {
    debugLog('ERROR', 'OCTADESK_INITIAL_EXCEPTION', {
      error_message: error.message,
      error_stack: error.stack
    }, 'error');
    return { success: false, error: error.message };
  }
}
```

---

### **FUNÇÃO 4: Log Detalhado para GTM**

#### **Implementação em `registrarConversaoInicialGTM()`**:

```javascript
function registrarConversaoInicialGTM(ddd, celular, gclid) {
  // ✅ V3: LOG ANTES DE CONSTRUIR DADOS GTM
  debugLog('GTM', 'DATA_PREPARATION_START', {
    ddd: ddd,
    celular: '***' + onlyDigits(celular).slice(-4),
    gclid: gclid || '(vazio)',
    dataLayer_available: typeof window.dataLayer !== 'undefined',
    gtm_variables: {
      GTM_EVENT_NAME_INITIAL: window.GTM_EVENT_NAME_INITIAL || '(não definido)',
      GTM_FORM_TYPE: window.GTM_FORM_TYPE || '(não definido)',
      GTM_CONTACT_STAGE: window.GTM_CONTACT_STAGE || '(não definido)',
      GTM_UTM_SOURCE: window.GTM_UTM_SOURCE || '(null - será preenchido)',
      GTM_UTM_CAMPAIGN: window.GTM_UTM_CAMPAIGN || '(null - será preenchido)',
      GTM_PAGE_URL: window.GTM_PAGE_URL || '(null - será preenchido)',
      GTM_PAGE_TITLE: window.GTM_PAGE_TITLE || '(null - será preenchido)'
    },
    utm_params_from_url: {
      utm_source: getUtmParam('utm_source') || '(vazio)',
      utm_campaign: getUtmParam('utm_campaign') || '(vazio)',
      utm_medium: getUtmParam('utm_medium') || '(vazio)',
      utm_term: getUtmParam('utm_term') || '(vazio)',
      utm_content: getUtmParam('utm_content') || '(vazio)'
    }
  }, 'info');
  
  if (typeof window.dataLayer === 'undefined') {
    debugLog('GTM', 'DATALAYER_UNAVAILABLE', {
      message: 'dataLayer não disponível para registro de conversão inicial',
      window_dataLayer: typeof window.dataLayer
    }, 'warn');
    return { success: false, error: 'dataLayer_unavailable' };
  }
  
  // Construir dados do evento GTM
  const gtmEventData = {
    'event': window.GTM_EVENT_NAME_INITIAL || 'whatsapp_modal_initial_contact',
    'form_type': window.GTM_FORM_TYPE || 'whatsapp_modal',
    'contact_stage': window.GTM_CONTACT_STAGE || 'initial',
    'phone_ddd': ddd || '',
    'phone_number': '***',
    'has_phone': !!celular,
    'gclid': gclid || '',
    'utm_source': window.GTM_UTM_SOURCE || getUtmParam('utm_source') || '',
    'utm_campaign': window.GTM_UTM_CAMPAIGN || getUtmParam('utm_campaign') || '',
    'utm_medium': window.GTM_UTM_MEDIUM || getUtmParam('utm_medium') || '',
    'utm_term': window.GTM_UTM_TERM || getUtmParam('utm_term') || '',
    'utm_content': window.GTM_UTM_CONTENT || getUtmParam('utm_content') || '',
    'page_url': window.GTM_PAGE_URL || window.location.href || '',
    'page_title': window.GTM_PAGE_TITLE || document.title || '',
    'user_agent': window.GTM_USER_AGENT || navigator.userAgent || '',
    'timestamp': new Date().toISOString(),
    'environment': isDevelopmentEnvironment() ? 'dev' : 'prod'
  };
  
  // ✅ V3: LOG DO OBJETO COMPLETO QUE SERÁ ENVIADO AO GTM
  debugLog('GTM', 'EVENT_DATA_READY', {
    event_data: gtmEventData,
    event_data_json: JSON.stringify(gtmEventData, null, 2),
    event_name: gtmEventData.event,
    dataLayer_length_before: window.dataLayer.length
  }, 'info');
  
  // ✅ V3: LOG ANTES DO PUSH
  debugLog('GTM', 'PUSHING_TO_DATALAYER', {
    event_name: gtmEventData.event,
    dataLayer_length_before: window.dataLayer.length
  }, 'info');
  
  window.dataLayer.push(gtmEventData);
  
  // ✅ V3: LOG APÓS O PUSH
  debugLog('GTM', 'PUSHED_TO_DATALAYER', {
    event_name: gtmEventData.event,
    dataLayer_length_after: window.dataLayer.length,
    dataLayer_item: window.dataLayer[window.dataLayer.length - 1]
  }, 'info');
  
  return { success: true, eventData: gtmEventData };
}
```

---

### **FUNÇÃO 5: Log do Processamento Paralelo**

#### **Implementação no evento blur do celular**:

```javascript
// NO EVENTO BLUR DO CELULAR (após validação bem-sucedida)

if (celularDigits === 9 && dddDigits === 2 && !initialRegistrationAttempted) {
  initialRegistrationAttempted = true;
  const ddd = $(MODAL_CONFIG.fieldIds.ddd).val();
  const celular = $(this).val();
  const gclid = getGCLID();
  
  // ✅ V3: LOG DO INÍCIO DO PROCESSAMENTO PARALELO
  debugLog('PARALLEL', 'INITIAL_PROCESSING_START', {
    ddd: ddd,
    celular: '***' + onlyDigits(celular).slice(-4),
    gclid: gclid || '(vazio)',
    initialRegistrationAttempted: true,
    processes: ['EspoCRM', 'Octadesk', 'GTM'],
    strategy: 'Promise.all (paralelo)'
  }, 'info');
  
  // ✅ V3: LOG DO ESTADO ANTES DO PROCESSAMENTO
  const previousState = getLeadState();
  debugLog('STATE', 'STATE_BEFORE_PROCESSING', {
    localStorage_available: typeof(Storage) !== 'undefined',
    has_previous_state: !!previousState,
    previous_state: previousState || null,
    modal_session_id: generateSessionId()
  }, 'debug');
  
  console.log('📞 [MODAL] Processando registro inicial (paralelo): EspoCRM + Octadesk + GTM...');
  
  // PROCESSAR EM PARALELO: EspoCRM + Octadesk + GTM
  Promise.all([
    registrarPrimeiroContatoEspoCRM(ddd, celular, gclid),
    enviarMensagemInicialOctadesk(ddd, celular, gclid),
    Promise.resolve(registrarConversaoInicialGTM(ddd, celular, gclid))
  ])
  .then(([espocrmResult, octadeskResult, gtmResult]) => {
    // ✅ V3: LOG DOS RESULTADOS PARALELOS
    debugLog('PARALLEL', 'INITIAL_PROCESSING_COMPLETE', {
      espocrm: {
        success: espocrmResult.success,
        lead_id: espocrmResult.id || null,
        attempt: espocrmResult.attempt || null,
        error: espocrmResult.error || null
      },
      octadesk: {
        success: octadeskResult.success,
        attempt: octadeskResult.attempt || null,
        error: octadeskResult.error || null
      },
      gtm: {
        success: gtmResult.success,
        event_name: gtmResult.eventData?.event || null,
        error: gtmResult.error || null
      },
      overall_success: {
        espocrm: espocrmResult.success,
        octadesk: octadeskResult.success,
        gtm: gtmResult.success
      }
    }, 'info');
    
    // Logs individuais detalhados
    if (espocrmResult.success) {
      console.log('✅ [MODAL] Lead criado no EspoCRM:', espocrmResult.id || 'sem ID');
      if (espocrmResult.id) {
        saveLeadState({ id: espocrmResult.id, ddd, celular, gclid });
      }
    } else {
      console.warn('⚠️ [MODAL] Erro ao criar lead (não bloqueante):', espocrmResult.error);
    }
    
    if (octadeskResult.success) {
      console.log('✅ [MODAL] Mensagem inicial enviada via Octadesk');
    } else {
      console.warn('⚠️ [MODAL] Erro ao enviar mensagem (não bloqueante):', octadeskResult.error);
    }
    
    if (gtmResult.success) {
      console.log('✅ [MODAL] Conversão inicial registrada no GTM');
    } else {
      console.warn('⚠️ [MODAL] Erro ao registrar conversão (não bloqueante):', gtmResult.error);
    }
  })
  .catch(error => {
    // ✅ V3: LOG DE ERRO NO PROCESSAMENTO PARALELO
    debugLog('ERROR', 'PARALLEL_PROCESSING_EXCEPTION', {
      error_message: error.message,
      error_stack: error.stack,
      error_name: error.name
    }, 'error');
    
    console.warn('⚠️ [MODAL] Erros no processamento inicial (não bloqueante):', error);
  });
}
```

---

### **FUNÇÃO 6: Log da Atualização do Lead**

#### **Implementação em `atualizarLeadEspoCRM()`**:

```javascript
async function atualizarLeadEspoCRM(dados, espocrmId = null) {
  // Tentar recuperar estado anterior se não tiver ID
  if (!espocrmId) {
    const previousState = getLeadState();
    if (previousState && previousState.lead_id) {
      espocrmId = previousState.lead_id;
      
      // ✅ V3: LOG DA RECUPERAÇÃO DO ESTADO
      debugLog('STATE', 'LEAD_ID_RECOVERED', {
        lead_id: espocrmId,
        source: 'localStorage',
        previous_state: previousState
      }, 'info');
    }
  }
  
  const webhook_data = {
    data: {
      'NOME': sanitizeData({ NOME: dados.NOME }).NOME || '',
      'DDD-CELULAR': dados.DDD || '',
      'CELULAR': onlyDigits(dados.CELULAR) || '',
      'Email': sanitizeData({ Email: dados.EMAIL }).Email || '',
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
      'ENDERECO': sanitizeData({ ENDERECO: dados.ENDERECO }).ENDERECO || '',
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
  
  const endpointUrl = getEndpointUrl('travelangels');
  
  // ✅ V3: LOG COMPLETO ANTES DA ATUALIZAÇÃO
  debugLog('ESPOCRM', 'UPDATE_REQUEST_PREPARATION', {
    endpoint_url: endpointUrl,
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'User-Agent': 'Modal-WhatsApp-v2.0'
    },
    payload: webhook_data,
    payload_json: JSON.stringify(webhook_data, null, 2),
    lead_id: espocrmId || '(não fornecido)',
    has_lead_id: !!espocrmId,
    input_data_summary: {
      has_nome: !!dados.NOME,
      has_cpf: !!dados.CPF,
      has_cep: !!dados.CEP,
      has_placa: !!dados.PLACA,
      has_email: !!dados.EMAIL,
      ddd: dados.DDD || '',
      celular: dados.CELULAR ? '***' + onlyDigits(dados.CELULAR).slice(-4) : ''
    }
  }, 'info');
  
  try {
    const result = await fetchWithRetry(endpointUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'User-Agent': 'Modal-WhatsApp-v2.0'
      },
      body: JSON.stringify(webhook_data)
    }, 2, 1000);
    
    // ✅ V3: LOG DA RESPOSTA DE ATUALIZAÇÃO
    debugLog('ESPOCRM', 'UPDATE_RESPONSE_RECEIVED', {
      success: result.success,
      attempt: result.attempt + 1,
      http_status: result.response?.status || 'N/A',
      has_response_data: !!result.response,
      error: result.error || null
    }, result.success ? 'info' : 'warn');
    
    if (result.success && result.response) {
      try {
        const responseData = await result.response.json();
        
        // ✅ V3: LOG DA RESPOSTA PARSEADA DE ATUALIZAÇÃO
        debugLog('ESPOCRM', 'UPDATE_RESPONSE_PARSED', {
          response_data: responseData,
          response_json: JSON.stringify(responseData, null, 2),
          success: result.response.ok
        }, 'info');
        
        return { success: true, result: responseData, attempt: result.attempt + 1 };
      } catch (parseError) {
        debugLog('ESPOCRM', 'UPDATE_RESPONSE_PARSE_ERROR', {
          error: parseError.message
        }, 'warn');
        return { success: result.response.ok, attempt: result.attempt + 1 };
      }
    }
    
    return { success: false, error: result.error, attempt: result.attempt + 1 };
    
  } catch (error) {
    debugLog('ERROR', 'ESPOCRM_UPDATE_EXCEPTION', {
      error_message: error.message,
      error_stack: error.stack
    }, 'error');
    return { success: false, error: error.message };
  }
}
```

---

### **FUNÇÃO 7: Log do Submit**

#### **Implementação no evento submit**:

```javascript
$form.on('submit', async function(e) {
  e.preventDefault();
  
  // Validar DDD + Celular
  const ddd = $(MODAL_CONFIG.fieldIds.ddd).val();
  const celular = $(MODAL_CONFIG.fieldIds.celular).val();
  
  // ✅ V3: LOG DO INÍCIO DO SUBMIT
  debugLog('VALIDATION', 'SUBMIT_START', {
    ddd: ddd,
    celular: '***' + onlyDigits(celular).slice(-4),
    ddd_valid: onlyDigits(ddd).length === 2,
    celular_valid: onlyDigits(celular).length === 9
  }, 'info');
  
  if (!ddd || onlyDigits(ddd).length !== 2) {
    debugLog('VALIDATION', 'SUBMIT_VALIDATION_FAILED', {
      field: 'DDD',
      reason: 'DDD deve ter 2 dígitos'
    }, 'warn');
    alert('Por favor, preencha o DDD corretamente.');
    return;
  }
  
  if (!celular || onlyDigits(celular).length !== 9) {
    debugLog('VALIDATION', 'SUBMIT_VALIDATION_FAILED', {
      field: 'CELULAR',
      reason: 'Celular deve ter 9 dígitos'
    }, 'warn');
    alert('Por favor, preencha o celular corretamente.');
    return;
  }
  
  // Coletar todos os dados
  const dados = coletarTodosDados();
  dados.DDD = ddd;
  dados.GCLID = getGCLID();
  
  // ✅ V3: LOG DOS DADOS COLETADOS
  debugLog('STATE', 'SUBMIT_DATA_COLLECTED', {
    dados_summary: {
      has_ddd: !!dados.DDD,
      has_celular: !!dados.CELULAR,
      has_cpf: !!dados.CPF,
      has_nome: !!dados.NOME,
      has_placa: !!dados.PLACA,
      has_cep: !!dados.CEP,
      has_email: !!dados.EMAIL,
      has_gclid: !!dados.GCLID
    },
    dados_complete: dados,
    dados_json: JSON.stringify(dados, null, 2)
  }, 'info');
  
  // Verificar se há dados novos para atualizar
  const hasNewData = !!(dados.CPF || dados.NOME || dados.CEP || dados.PLACA);
  
  // ✅ V3: LOG DA DECISÃO DE ATUALIZAÇÃO
  debugLog('STATE', 'UPDATE_DECISION', {
    has_new_data: hasNewData,
    new_data_fields: {
      cpf: !!dados.CPF,
      nome: !!dados.NOME,
      cep: !!dados.CEP,
      placa: !!dados.PLACA
    },
    will_update: hasNewData
  }, 'info');
  
  if (hasNewData) {
    const previousState = getLeadState();
    const espocrmId = previousState?.lead_id || null;
    
    debugLog('ESPOCRM', 'UPDATE_WILL_BE_CALLED', {
      has_lead_id: !!espocrmId,
      lead_id: espocrmId || '(não encontrado)'
    }, 'info');
    
    // Atualizar lead (não bloqueante)
    atualizarLeadEspoCRM(dados, espocrmId)
      .then(result => {
        debugLog('ESPOCRM', 'UPDATE_COMPLETE', {
          success: result.success,
          error: result.error || null
        }, result.success ? 'info' : 'warn');
      })
      .catch(error => {
        debugLog('ERROR', 'UPDATE_EXCEPTION', {
          error_message: error.message
        }, 'error');
      });
  } else {
    debugLog('STATE', 'UPDATE_SKIPPED', {
      reason: 'Nenhum dado novo para atualizar'
    }, 'info');
  }
  
  // Sempre abrir WhatsApp
  debugLog('STATE', 'WHATSAPP_OPENING', {
    whatsapp_phone: MODAL_CONFIG.whatsapp.phone,
    message_built: buildWhatsAppMessage(dados)
  }, 'info');
  
  $modal.fadeOut(300, function() {
    openWhatsApp(dados);
  });
});
```

---

## 📊 EXEMPLO DE SAÍDA DOS LOGS

### **Console Output Esperado**:

```
📊 [ESPOCRM] INITIAL_REQUEST_PREPARATION {
  timestamp: "2025-10-29T10:45:00.000Z",
  environment: "🔧 DEV",
  category: "ESPOCRM",
  action: "INITIAL_REQUEST_PREPARATION",
  endpoint_url: "https://bpsegurosimediato.com.br/dev/webhooks/add_travelangels.php",
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "User-Agent": "Modal-WhatsApp-v2.0"
  },
  payload: {
    data: {
      "DDD-CELULAR": "11",
      "CELULAR": "999999999",
      "GCLID_FLD": "CjwKCAjw...",
      ...
    },
    d: "2025-10-29T10:45:00.000Z",
    name: "Modal WhatsApp - Primeiro Contato (V2)"
  },
  payload_json: "{ ... JSON completo formatado ... }",
  input_data: {
    ddd: "11",
    celular: "***9999",
    gclid: "CjwKCAjw...",
    gclid_length: 56
  },
  rate_limiting: {
    phone_key: "11999999999",
    can_make_call: true
  },
  data_stringified: "{ ... }"
}

📱 [OCTADESK] INITIAL_REQUEST_PREPARATION {
  ... (similar structure)
}

📈 [GTM] DATA_PREPARATION_START {
  ... (similar structure with GTM variables)
}

📈 [GTM] EVENT_DATA_READY {
  event_data: {
    event: "whatsapp_modal_initial_contact",
    form_type: "whatsapp_modal",
    contact_stage: "initial",
    ...
  },
  event_data_json: "{ ... JSON completo formatado ... }",
  ...
}

⚡ [PARALLEL] INITIAL_PROCESSING_COMPLETE {
  espocrm: { success: true, lead_id: "abc123", ... },
  octadesk: { success: true, ... },
  gtm: { success: true, event_name: "whatsapp_modal_initial_contact" },
  ...
}
```

---

## 📝 CHECKLIST DE IMPLEMENTAÇÃO V3

### **FASE 1: Adicionar Função de Debug Centralizada**

- [ ] 1. Criar função `debugLog()` com níveis e categorias
- [ ] 2. Testar função de logging localmente
- [ ] 3. Integrar com sistema de logging existente (se disponível)

### **FASE 2: Adicionar Logs nas Funções de Integração**

- [ ] 1. Adicionar logs em `registrarPrimeiroContatoEspoCRM()`
  - [ ] Log antes da chamada (com JSON completo)
  - [ ] Log após resposta recebida
  - [ ] Log após parse da resposta
- [ ] 2. Adicionar logs em `enviarMensagemInicialOctadesk()`
  - [ ] Log antes da chamada (com JSON completo)
  - [ ] Log após resposta recebida
  - [ ] Log após parse da resposta
- [ ] 3. Adicionar logs em `registrarConversaoInicialGTM()`
  - [ ] Log antes de construir dados
  - [ ] Log com objeto completo antes do push
  - [ ] Log após push ao dataLayer
- [ ] 4. Adicionar logs em `atualizarLeadEspoCRM()`
  - [ ] Log antes da atualização (com JSON completo)
  - [ ] Log após resposta

### **FASE 3: Adicionar Logs de Estado e Fluxo**

- [ ] 1. Log do início do processamento paralelo
- [ ] 2. Log do estado do localStorage
- [ ] 3. Log dos resultados do processamento paralelo
- [ ] 4. Log do início do submit
- [ ] 5. Log dos dados coletados
- [ ] 6. Log da decisão de atualização

### **FASE 4: Testes**

- [ ] 1. Testar em ambiente de desenvolvimento
- [ ] 2. Verificar logs no console do navegador
- [ ] 3. Verificar se todos os logs aparecem corretamente
- [ ] 4. Testar cenários de erro (desconectar internet, etc.)
- [ ] 5. Verificar logs em diferentes navegadores

---

## 🔧 CONFIGURAÇÃO OPCIONAL DE LOGGING

### **Ativar/Desativar Logs por Categoria**

```javascript
// Configuração de logging (opcional)
window.DEBUG_LOG_CONFIG = {
  ESPOCRM: true,      // Logs do EspoCRM
  OCTADESK: true,     // Logs do Octadesk
  GTM: true,          // Logs do GTM
  STATE: true,        // Logs de estado
  PARALLEL: true,     // Logs de processamento paralelo
  VALIDATION: true,   // Logs de validação
  ERROR: true         // Logs de erro
};

// Modificar função debugLog para respeitar configuração
function debugLog(category, action, data = {}, level = 'info') {
  // Verificar se categoria está habilitada
  if (window.DEBUG_LOG_CONFIG && !window.DEBUG_LOG_CONFIG[category]) {
    return; // Não logar esta categoria
  }
  
  // ... resto da implementação
}
```

---

## 🎯 BENEFÍCIOS DOS LOGS V3

1. **Debug Facilitado**: Logs detalhados facilitam identificação de problemas
2. **Rastreabilidade**: Todos os dados enviados/recebidos são logados
3. **Testes Simplificados**: JSONs completos permitem testar endpoints manualmente
4. **Monitoramento**: Logs estruturados podem ser coletados por ferramentas de monitoring
5. **Documentação**: Logs servem como documentação do fluxo em tempo real

---

## ✅ CONCLUSÃO

Este projeto (V3) adiciona capacidade completa de debug e observabilidade ao modal WhatsApp, permitindo:

1. 🔍 **Inspeção completa** de todas as chamadas aos endpoints
2. 📊 **Visualização detalhada** dos dados enviados ao GTM
3. 💾 **Rastreamento de estado** em todos os momentos
4. ❌ **Diagnóstico preciso** de erros com contexto completo

**Status**: 📝 **PRONTO PARA IMPLEMENTAÇÃO** (após testes da V2)

---

**Data de Criação**: 2025-10-29  
**Versão Base**: V2.0  
**Status**: 📝 **PROJETO** (Não executado)










