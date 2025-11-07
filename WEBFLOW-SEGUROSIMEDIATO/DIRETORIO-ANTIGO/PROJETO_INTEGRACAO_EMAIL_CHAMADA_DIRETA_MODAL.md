# PROJETO: INTEGRAÇÃO DE EMAIL NOTIFICAÇÃO ADMINISTRADORES VIA CHAMADA DIRETA NO MODAL

**Data de Criação:** 03/11/2025 20:00  
**Última Modificação:** 03/11/2025 21:00  
**Status:** Planejamento (NÃO EXECUTAR)  
**Workspace:** imediatoseguros-rpa-playwright

**⚠️ IMPORTANTE:** Este projeto implementa chamadas diretas ao endpoint de email, sem usar interceptadores. Abordagem simples e explícita.

**🔄 MODIFICAÇÃO:** Projeto atualizado para enviar email também em caso de ERRO no endpoint `add_flyingdonkeys_v2.php`, permitindo que administradores sejam notificados mesmo quando ocorrem problemas.

---

## 📋 OBJETIVO

Integrar o envio de email para administradores via Amazon SES através de **chamadas diretas** no `MODAL_WHATSAPP_DEFINITIVO.js`, após **SUCESSO OU ERRO** nas respostas do `add_flyingdonkeys_v2.php`. O sistema deve identificar claramente os três cenários distintos:

1. **MOMENTO 1 (INITIAL - SUCESSO):** Após digitação do telefone no modal (apenas DDD + Celular) - resposta de sucesso de `registrarPrimeiroContatoEspoCRM()`
2. **MOMENTO 2 (UPDATE - SUCESSO):** Após submissão completa do formulário no modal (todos os dados) - resposta de sucesso de `atualizarLeadEspoCRM()`
3. **MOMENTO 3 (ERRO):** Após qualquer erro no endpoint `add_flyingdonkeys_v2.php` (INITIAL ou UPDATE) - indicar erro no email

**Abordagem:** Chamadas diretas ao endpoint `send_email_notification_endpoint.php` após **qualquer resposta** (sucesso ou erro), sem uso de interceptadores ou monkey-patching.

**CRÍTICO:** NÃO alterar `add_flyingdonkeys_v2.php` - ele é usado diretamente pelo Webflow.

---

## 🎯 PROBLEMA ATUAL

Atualmente, o sistema de notificação por email para administradores (`send_admin_notification_ses.php`) foi criado e testado, mas **não está integrado** ao fluxo do modal WhatsApp. Os emails não são enviados automaticamente quando:

1. Um cliente digita o telefone corretamente no modal (sucesso)
2. Um cliente submete o formulário completo no modal (sucesso)
3. **NOVO:** Um erro ocorre ao chamar o endpoint `add_flyingdonkeys_v2.php` (erro)

**Solução Anterior (REJEITADA):** Tentativa de usar interceptor com monkey-patch do `fetch` global foi rejeitada por ser excessivamente sofisticada e poder afetar outras chamadas.

**Nova Abordagem:** Chamadas diretas e explícitas no modal após **qualquer resposta** (sucesso ou erro) do EspoCRM, permitindo que administradores sejam notificados mesmo quando ocorrem erros.

---

## 📁 ARQUIVOS ENVOLVIDOS

### Backups Criados:
- ✅ `MODAL_WHATSAPP_DEFINITIVO.js.backup_EMAIL_DIRETO_YYYYMMDD_HHMMSS` - Backup criado antes da implementação
- ✅ `send_email_notification_endpoint.php.backup_EMAIL_DIRETO_YYYYMMDD_HHMMSS` - Backup criado antes da implementação
- ✅ `send_admin_notification_ses.php.backup_EMAIL_DIRETO_YYYYMMDD_HHMMSS` - Backup criado antes da implementação

**Nota:** `FooterCodeSiteDefinitivoCompleto.js` NÃO será modificado, apenas carrega o modal dinamicamente.

### Arquivos a Modificar:
1. **`MODAL_WHATSAPP_DEFINITIVO.js`** ⚠️ **ARQUIVO SEPARADO**
   - **IMPORTANTE:** Este arquivo NÃO está incluído dentro do `FooterCodeSiteDefinitivoCompleto.js`
   - É um arquivo **separado** que é carregado **dinamicamente** pelo `FooterCodeSiteDefinitivoCompleto.js` via `<script src="...">` (linha ~1261)
   - Localização no servidor: `/var/www/html/webhooks/MODAL_WHATSAPP_DEFINITIVO.js`
   - Modificações necessárias:
     - Adicionar função `sendAdminEmailNotification()` para enviar emails após sucesso OU erro
     - Adicionar função `identifyModalMoment()` para identificar INITIAL vs UPDATE vs ERRO
     - Integrar chamada de email após sucesso de `registrarPrimeiroContatoEspoCRM()` (linha ~725)
     - Integrar chamada de email após ERRO de `registrarPrimeiroContatoEspoCRM()` (linha ~729, ~737, ~746)
     - Integrar chamada de email após sucesso de `atualizarLeadEspoCRM()` (linha ~882)
     - Integrar chamada de email após ERRO de `atualizarLeadEspoCRM()` (linha ~888, ~897, ~905)
   - **Backup:** `MODAL_WHATSAPP_DEFINITIVO.js.backup_EMAIL_DIRETO_20251103_200000`

2. **`02-DEVELOPMENT/custom-codes/send_email_notification_endpoint.php`**
   - Modificar para aceitar parâmetro `erro` opcional
   - Modificar para incluir informações de erro no email quando presente
   - **Backup:** `send_email_notification_endpoint.php.backup_EMAIL_DIRETO_YYYYMMDD_HHMMSS`

3. **`02-DEVELOPMENT/custom-codes/send_admin_notification_ses.php`**
   - Modificar para incluir informações de erro no corpo do email quando presente
   - Modificar para usar cor vermelha no banner quando houver erro
   - **Backup:** `send_admin_notification_ses.php.backup_EMAIL_DIRETO_YYYYMMDD_HHMMSS`

### Arquivos de Referência (NÃO MODIFICAR):
- `02-DEVELOPMENT/custom-codes/add_flyingdonkeys_v2.php` - **NÃO ALTERAR** (usado pelo Webflow)
- `02-DEVELOPMENT/custom-codes/FooterCodeSiteDefinitivoCompleto.js` - **NÃO ALTERAR** (apenas carrega o modal dinamicamente, não contém o código do modal)
- `02-DEVELOPMENT/custom-codes/send_email_notification_endpoint.php` - Endpoint já criado (será modificado para suportar erros)
- `02-DEVELOPMENT/custom-codes/send_admin_notification_ses.php` - Função de envio já criada (será modificada para incluir erros)
- `02-DEVELOPMENT/custom-codes/aws_ses_config.php` - Configuração AWS SES já criada

### Destino no Servidor:
- `/var/www/html/webhooks/MODAL_WHATSAPP_DEFINITIVO.js` (DEV e PROD) - Arquivo separado carregado dinamicamente
- `/var/www/html/webhooks/send_email_notification_endpoint.php` (DEV e PROD) - Será modificado
- `/var/www/html/webhooks/send_admin_notification_ses.php` (DEV e PROD) - Será modificado

**Nota:** O `FooterCodeSiteDefinitivoCompleto.js` carrega o modal via:
```javascript
script.src = 'https://dev.bpsegurosimediato.com.br/webhooks/MODAL_WHATSAPP_DEFINITIVO.js?v=23&force=' + Math.random();
```

---

## 🔍 ANÁLISE DOS DOIS MOMENTOS

### **MOMENTO 1: INITIAL (Primeiro Contato - Apenas Telefone)**

**Quando ocorre:**
- Após o cliente digitar DDD + Celular no modal WhatsApp
- Função JavaScript: `criarLeadEspoCRM()` no `MODAL_WHATSAPP_DEFINITIVO.js` (linha ~600)
- Chamada fetch para `add_flyingdonkeys_v2.php` via `getEndpointUrl('travelangels')`

**Dados enviados (payload do modal):**
```javascript
{
  data: {
    'DDD-CELULAR': '11',
    'CELULAR': '999999999',
    'GCLID_FLD': '...',
    'NOME': '11-999999999-NOVO CLIENTE WHATSAPP',
    'CPF': '',
    'CEP': '',
    'PLACA': '',
    'Email': '11999999999@imediatoseguros.com.br'
  },
  name: 'Modal WhatsApp - Primeiro Contato (V2)',
  d: '2025-11-03T...'
}
```

**Resposta esperada (do add_flyingdonkeys_v2.php):**
```javascript
{
  success: true,
  contact_id: '69039ffd9055284be',
  opportunity_id: '690608ef4f11a0462',
  // ... outros campos
}
```

**Localização no código:**
- Função `registrarPrimeiroContatoEspoCRM()` - linha ~566
- Payload `webhook_data` criado na linha ~587
- Retorno de sucesso: linha ~725: `return { success: true, id: leadId, opportunity_id: opportunityId, attempt: result.attempt + 1 };`
- **Chamada de email:** Adicionar ANTES da linha 725 (return), após linha 724 (logEvent), usando `webhook_data` e `responseData` disponíveis no escopo

**Identificador:**
- Campo `name` contém: `'Modal WhatsApp - Primeiro Contato (V2)'`
- Campo `NOME` contém padrão: `'{DDD}-{CELULAR}-NOVO CLIENTE WHATSAPP'`
- Campos `CPF`, `CEP`, `PLACA` estão vazios ou ausentes

**Emoji identificador (SUCESSO):** 📞 (telefone azul)
**Cor no log (SUCESSO):** 🔵 (azul)
**Cor no email (SUCESSO):** `#2196F3` (azul)

**Emoji identificador (ERRO):** ❌ (erro vermelho)
**Cor no log (ERRO):** 🔴 (vermelho)
**Cor no email (ERRO):** `#F44336` (vermelho)

---

### **MOMENTO 2: UPDATE (Submissão Completa - Todos os Dados)**

**Quando ocorre:**
- Após o cliente clicar no botão de submissão do modal
- Todos os campos estão preenchidos (CPF, CEP, PLACA, etc.)
- Função JavaScript: `atualizarLeadEspoCRM()` no `MODAL_WHATSAPP_DEFINITIVO.js` (linha ~763)
- Chamada fetch para `add_flyingdonkeys_v2.php` via `getEndpointUrl('travelangels')`

**Dados enviados (payload do modal):**
```javascript
{
  data: {
    'DDD-CELULAR': '11',
    'CELULAR': '999999999',
    'GCLID_FLD': '...',
    'NOME': 'Nome Completo do Cliente',
    'CPF': '123.456.789-00',
    'CEP': '01234-567',
    'PLACA': 'ABC1234',
    'Email': 'cliente@email.com',
    'lead_id': '69039ffd9055284be',  // ID do lead criado anteriormente
    // ... outros campos
  },
  name: 'Modal WhatsApp - Dados Completos',
  d: '2025-11-03T...'
}
```

**Resposta esperada (do add_flyingdonkeys_v2.php):**
```javascript
{
  success: true,
  // ... outros campos (geralmente não retorna novo lead_id, apenas confirma atualização)
}
```

**Localização no código:**
- Função `atualizarLeadEspoCRM()` - linha ~763
- Payload `webhook_data` criado na linha ~779
- Retorno de sucesso: linha ~882: `return { success: true, result: responseData, attempt: result.attempt + 1 };`
- **Chamada de email:** Adicionar ANTES da linha 882 (return), após linha 881 (logEvent), usando `webhook_data` e `responseData` disponíveis no escopo

**Identificador:**
- Campo `name` contém: `'Modal WhatsApp - Dados Completos'` ou `'Modal WhatsApp - Mensagem Octadesk'`
- Campo `NOME` contém nome real do cliente (não o padrão)
- Campos `CPF`, `CEP`, `PLACA` estão preenchidos
- Campo `lead_id` ou `contact_id` presente no payload

**Emoji identificador (SUCESSO):** ✅ (check verde)
**Cor no log (SUCESSO):** 🟢 (verde)
**Cor no email (SUCESSO):** `#4CAF50` (verde)

**Emoji identificador (ERRO):** ❌ (erro vermelho)
**Cor no log (ERRO):** 🔴 (vermelho)
**Cor no email (ERRO):** `#F44336` (vermelho)

---

## 🔧 FASE 1: IMPLEMENTAÇÃO DAS ALTERAÇÕES

### **1.1. Adicionar Funções Helper no MODAL_WHATSAPP_DEFINITIVO.js**

**Localização:** Após as funções auxiliares existentes, antes da função `criarLeadEspoCRM()`

#### **1.1.1. Função para Identificar Momento do Modal**

```javascript
/**
 * Identifica em qual momento o modal está sendo processado
 * Baseado no payload enviado pelo modal ao add_flyingdonkeys_v2.php
 * 
 * @param {Object} payload - Payload enviado pelo modal ao add_flyingdonkeys_v2.php
 * @param {boolean} isError - Se true, indica que houve erro na chamada
 * @returns {Object} Objeto com informações do momento
 */
function identifyModalMoment(payload, isError = false) {
  try {
    const name = payload.name || '';
    const nome = (payload.data && payload.data.NOME) || '';
    const cpf = (payload.data && payload.data.CPF) || '';
    const cep = (payload.data && payload.data.CEP) || '';
    const placa = (payload.data && payload.data.PLACA) || '';
    
    // Verificar pelo campo 'name'
    const isInitialByName = name.includes('Primeiro Contato') || name.includes('Mensagem Inicial');
    
    // Verificar pelo padrão do nome (INITIAL tem padrão especial)
    const isInitialPattern = /^\d{2}-\d{9}-NOVO CLIENTE WHATSAPP$/.test(nome);
    
    // Verificar se campos obrigatórios estão vazios (INITIAL tem apenas telefone)
    const camposVazios = !cpf && !cep && !placa;
    
    // Determinar tipo base (INITIAL ou UPDATE)
    const isInitial = isInitialByName || isInitialPattern || camposVazios;
    
    // Se houver erro, usar identificadores de erro
    if (isError) {
      return {
        moment: isInitial ? 'initial_error' : 'update_error',
        emoji: '❌',
        color: '🔴',
        color_name: 'VERMELHO',
        description: isInitial 
          ? 'ERRO - Primeiro Contato - Apenas Telefone' 
          : 'ERRO - Submissão Completa - Todos os Dados',
        banner_color: '#F44336'
      };
    }
    
    // Lógica de identificação (SUCESSO)
    if (isInitial) {
      // MOMENTO 1: INITIAL (SUCESSO)
      return {
        moment: 'initial',
        emoji: '📞',
        color: '🔵',
        color_name: 'AZUL',
        description: 'Primeiro Contato - Apenas Telefone',
        banner_color: '#2196F3'
      };
    } else {
      // MOMENTO 2: UPDATE (SUCESSO)
      return {
        moment: 'update',
        emoji: '✅',
        color: '🟢',
        color_name: 'VERDE',
        description: 'Submissão Completa - Todos os Dados',
        banner_color: '#4CAF50'
      };
    }
  } catch (error) {
    console.error('❌ [EMAIL] Erro ao identificar momento:', error);
    // Default: assumir UPDATE com erro (mais seguro)
    return {
      moment: 'update_error',
      emoji: '❌',
      color: '🔴',
      color_name: 'VERMELHO',
      description: 'ERRO - Submissão Completa - Todos os Dados',
      banner_color: '#F44336'
    };
  }
}
```

#### **1.1.2. Função para Enviar Email aos Administradores**

```javascript
/**
 * Envia notificação por email aos administradores
 * Chamada após sucesso OU erro nas respostas do add_flyingdonkeys_v2.php
 * 
 * @param {Object} modalPayload - Payload original enviado pelo modal
 * @param {Object} responseData - Resposta do add_flyingdonkeys_v2.php (pode ser sucesso ou erro)
 * @param {Object} errorInfo - Informações do erro (se houver): { message, status, code }
 * @returns {Promise<Object>} Resultado do envio de email
 */
async function sendAdminEmailNotification(modalPayload, responseData, errorInfo = null) {
  try {
    // Identificar se houve erro
    const isError = errorInfo !== null || (responseData && !responseData.success && !responseData.contact_id);
    
    // Identificar momento (com flag de erro)
    const modalMoment = identifyModalMoment(modalPayload, isError);
    
    // Extrair dados do payload do modal
    const data = modalPayload.data || {};
    const ddd = data['DDD-CELULAR'] || '';
    const celular = data['CELULAR'] || '';
    const nome = data['NOME'] || 'Não informado';
    const cpf = data['CPF'] || 'Não informado';
    const cep = data['CEP'] || 'Não informado';
    const placa = data['PLACA'] || 'Não informado';
    const email = data['Email'] || 'Não informado';
    const gclid = data['GCLID_FLD'] || 'Não informado';
    
    // Validar dados mínimos
    if (!ddd || !celular) {
      console.warn('📧 [EMAIL] Dados insuficientes para enviar email - DDD ou celular ausente');
      return {
        success: false,
        error: 'DDD e celular são obrigatórios'
      };
    }
    
    // Preparar dados para endpoint de email
    const emailPayload = {
      ddd: ddd,
      celular: celular,
      cpf: cpf,
      nome: nome,
      email: email,
      cep: cep,
      placa: placa,
      gclid: gclid,
      momento: modalMoment.moment,
      momento_descricao: modalMoment.description,
      momento_emoji: modalMoment.emoji,
      // Informações de erro (se houver)
      erro: errorInfo ? {
        message: errorInfo.message || 'Erro desconhecido',
        status: errorInfo.status || null,
        code: errorInfo.code || null,
        response_data: errorInfo.responseData || null
      } : null
    };
    
    // Determinar URL do endpoint (dev ou prod)
    const isDev = isDevelopmentEnvironment();
    const emailEndpoint = isDev 
      ? 'https://dev.bpsegurosimediato.com.br/webhooks/send_email_notification_endpoint.php'
      : 'https://bpsegurosimediato.com.br/webhooks/send_email_notification_endpoint.php';
    
    // Log antes do envio
    console.log(`${modalMoment.emoji} [EMAIL-${modalMoment.color_name}] Enviando notificação ${modalMoment.description}`);
    
    // Fazer chamada para endpoint de email
    const response = await fetch(emailEndpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'User-Agent': 'Modal-WhatsApp-EmailNotification-v1.0'
      },
      body: JSON.stringify(emailPayload)
    });
    
    // Verificar se a resposta é JSON válido antes de fazer parse
    let result;
    const contentType = response.headers.get('content-type');
    const responseText = await response.text();
    
    if (contentType && contentType.includes('application/json')) {
      try {
        result = responseText ? JSON.parse(responseText) : { success: false, error: 'Resposta vazia' };
      } catch (parseError) {
        console.error('❌ [EMAIL-ERRO] Erro ao parsear resposta JSON:', parseError);
        console.error('❌ [EMAIL-ERRO] Resposta recebida:', responseText.substring(0, 500));
        return {
          success: false,
          error: 'Erro ao processar resposta do servidor: ' + parseError.message
        };
      }
    } else {
      console.error(`❌ [EMAIL-ERRO] Resposta não é JSON. Status: ${response.status}, Tipo: ${contentType}, Texto: ${responseText.substring(0, 200)}`);
      return {
        success: false,
        error: `Resposta inválida do servidor (Status: ${response.status})`
      };
    }
    
    // Log do resultado
    if (result.success) {
      console.log(`${modalMoment.emoji} [EMAIL-${modalMoment.color_name}] Notificação ${modalMoment.description} enviada com SUCESSO`);
    } else {
      console.error(`❌ [EMAIL-ERRO] Falha ao enviar notificação ${modalMoment.description}:`, result.error || 'Erro desconhecido');
    }
    
    return result;
    
  } catch (error) {
    console.error('❌ [EMAIL-EXCEPTION] Erro ao enviar notificação:', error);
    return {
      success: false,
      error: error.message
    };
  }
}
```

---

### **1.2. Integrar Chamada de Email após Sucesso OU Erro do EspoCRM**

#### **1.2.0. Nota sobre Integração em Casos de Erro**

As chamadas de email devem ser feitas em **TODOS** os pontos de retorno (sucesso e erro) para garantir que administradores sejam notificados mesmo quando ocorrem problemas no endpoint `add_flyingdonkeys_v2.php`.

#### **1.2.1. Após Sucesso de `registrarPrimeiroContatoEspoCRM()` (INITIAL)**

**Localização:** Linha ~725, dentro do bloco `if (responseData.success || result.response.ok)`, ANTES do `return`

**Código a adicionar:**

```javascript
// Localização: Após linha 724 (logEvent), antes da linha 725 (return)
// 📧 ENVIAR EMAIL PARA ADMINISTRADORES APÓS SUCESSO (INITIAL)
// Enviar email de forma assíncrona (não bloquear o retorno)
sendAdminEmailNotification(webhook_data, responseData)
  .catch(error => {
    console.error('❌ [EMAIL] Erro ao enviar email (não bloqueante):', error);
  });

return { success: true, id: leadId, opportunity_id: opportunityId, attempt: result.attempt + 1 };
```

#### **1.2.1.1. Após ERRO de `registrarPrimeiroContatoEspoCRM()` (INITIAL - ERRO)**

**Localização 1:** Linha ~729, dentro do bloco `else` (quando `responseData.success === false`)

**Código a adicionar:**

```javascript
// Localização: Após linha 728 (logEvent), antes da linha 729 (return)
// 📧 ENVIAR EMAIL PARA ADMINISTRADORES APÓS ERRO (INITIAL)
// Enviar email de forma assíncrona (não bloquear o retorno)
sendAdminEmailNotification(webhook_data, responseData, {
  message: responseData.error || responseData.message || 'Erro ao criar lead no EspoCRM',
  status: null,
  code: null,
  responseData: responseData
})
  .catch(error => {
    console.error('❌ [EMAIL] Erro ao enviar email de notificação (não bloqueante):', error);
  });

return { success: false, error: responseData, attempt: result.attempt + 1 };
```

**Localização 2:** Linha ~737, dentro do bloco `catch (parseError)`

**Código a adicionar:**

```javascript
// Localização: Após linha 736 (debugLog), antes da linha 737 (return)
// 📧 ENVIAR EMAIL PARA ADMINISTRADORES APÓS ERRO DE PARSE (INITIAL)
sendAdminEmailNotification(webhook_data, null, {
  message: parseError.message || 'Erro ao parsear resposta do EspoCRM',
  status: result.response?.status || null,
  code: null,
  responseData: null
})
  .catch(error => {
    console.error('❌ [EMAIL] Erro ao enviar email de notificação (não bloqueante):', error);
  });

return { success: result.response.ok, attempt: result.attempt + 1 };
```

**Localização 3:** Linha ~746, dentro do bloco `else` (quando `result.error` existe)

**Código a adicionar:**

```javascript
// Localização: Após linha 745 (debugLog), antes da linha 746 (return)
// 📧 ENVIAR EMAIL PARA ADMINISTRADORES APÓS ERRO DE REQUEST (INITIAL)
sendAdminEmailNotification(webhook_data, null, {
  message: errorMsg || 'Erro desconhecido na requisição',
  status: null,
  code: null,
  responseData: null
})
  .catch(error => {
    console.error('❌ [EMAIL] Erro ao enviar email de notificação (não bloqueante):', error);
  });

return { success: false, error: errorMsg, attempt: result.attempt + 1 };
```

**Observação:** 
- A variável `webhook_data` está disponível no escopo da função `registrarPrimeiroContatoEspoCRM()` (criada na linha ~587)
- A chamada é assíncrona e não bloqueia o retorno da função
- Em caso de erro, `responseData` pode ser `null` ou conter informações de erro

#### **1.2.2. Após Sucesso de `atualizarLeadEspoCRM()` (UPDATE)**

**Localização:** Linha ~882, dentro do bloco `try`, após `logEvent`, ANTES do `return`

**Código a adicionar:**

```javascript
// Localização: Após linha 881 (logEvent), antes da linha 882 (return)
// 📧 ENVIAR EMAIL PARA ADMINISTRADORES APÓS SUCESSO (UPDATE)
// Enviar email de forma assíncrona (não bloquear o retorno)
sendAdminEmailNotification(webhook_data, responseData)
  .catch(error => {
    console.error('❌ [EMAIL] Erro ao enviar email (não bloqueante):', error);
  });

return { success: true, result: responseData, attempt: result.attempt + 1 };
```

#### **1.2.2.1. Após ERRO de `atualizarLeadEspoCRM()` (UPDATE - ERRO)**

**Localização 1:** Linha ~888, dentro do bloco `catch (parseError)`

**Código a adicionar:**

```javascript
// Localização: Após linha 887 (logEvent), antes da linha 888 (return)
// 📧 ENVIAR EMAIL PARA ADMINISTRADORES APÓS ERRO DE PARSE (UPDATE)
sendAdminEmailNotification(webhook_data, null, {
  message: parseError.message || 'Erro ao parsear resposta do EspoCRM',
  status: result.response?.status || null,
  code: null,
  responseData: null
})
  .catch(error => {
    console.error('❌ [EMAIL] Erro ao enviar email de notificação (não bloqueante):', error);
  });

return { success: result.response.ok, attempt: result.attempt + 1 };
```

**Localização 2:** Linha ~897, dentro do bloco `else` (quando `result.error` existe)

**Código a adicionar:**

```javascript
// Localização: Após linha 896 (logEvent), antes da linha 897 (return)
// 📧 ENVIAR EMAIL PARA ADMINISTRADORES APÓS ERRO DE REQUEST (UPDATE)
sendAdminEmailNotification(webhook_data, null, {
  message: errorMsg || 'Erro desconhecido na requisição',
  status: null,
  code: null,
  responseData: null
})
  .catch(error => {
    console.error('❌ [EMAIL] Erro ao enviar email de notificação (não bloqueante):', error);
  });

return { success: false, error: errorMsg, attempt: result.attempt + 1 };
```

**Localização 3:** Linha ~905, dentro do bloco `catch (error)` final

**Código a adicionar:**

```javascript
// Localização: Após linha 904 (logEvent), antes da linha 905 (return)
// 📧 ENVIAR EMAIL PARA ADMINISTRADORES APÓS EXCEÇÃO (UPDATE)
sendAdminEmailNotification(webhook_data, null, {
  message: error.message || 'Exceção ao atualizar lead',
  status: null,
  code: null,
  responseData: null
})
  .catch(emailError => {
    console.error('❌ [EMAIL] Erro ao enviar email de notificação (não bloqueante):', emailError);
  });

return { success: false, error: error.message };
```

**Observação:** 
- A variável `webhook_data` está disponível no escopo da função `atualizarLeadEspoCRM()` (criada na linha ~779)
- A chamada é assíncrona e não bloqueia o retorno da função
- Em caso de erro, `responseData` pode ser `null` ou não estar disponível

---

### **1.3. Modificar Arquivos PHP para Suportar Erros**

#### **1.3.1. Modificar `send_email_notification_endpoint.php`**

**Localização:** Após linha ~60, na preparação do `$emailData`

**Código a modificar/adicionar:**

```php
// Preparar dados para função de envio
$emailData = [
    'ddd' => $ddd,
    'celular' => $celular,
    'cpf' => $data['cpf'] ?? 'Não informado',
    'nome' => $data['nome'] ?? 'Não informado',
    'email' => $data['email'] ?? 'Não informado',
    'cep' => $data['cep'] ?? 'Não informado',
    'placa' => $data['placa'] ?? 'Não informado',
    'gclid' => $data['gclid'] ?? 'Não informado',
    'momento' => $data['momento'] ?? 'unknown',
    'momento_descricao' => $data['momento_descricao'] ?? 'Notificação',
    'momento_emoji' => $data['momento_emoji'] ?? '📧',
    // NOVO: Informações de erro (se presente)
    'erro' => $data['erro'] ?? null
];
```

**Modificar log de resultado (linha ~95):**

```php
// Log de resultado
error_log(sprintf(
    "[EMAIL-ENDPOINT] Momento: %s | DDD: %s | Celular: %s | Sucesso: %s | Erro: %s",
    $emailData['momento'],
    $ddd,
    substr($celular, 0, 3) . '***',  // Mascarar para segurança
    $result['success'] ? 'SIM' : 'NÃO',
    ($emailData['erro'] !== null) ? 'SIM' : 'NÃO'  // NOVO
));
```

#### **1.3.2. Modificar `send_admin_notification_ses.php`**

**Localização:** Após linha ~50, na preparação dos dados para email

**Código a modificar/adicionar:**

```php
// Identificadores visuais do momento
$momento_emoji = $dados['momento_emoji'] ?? '📧';
$momento_descricao = $dados['momento_descricao'] ?? 'Notificação';
$momento = $dados['momento'] ?? 'unknown';

// NOVO: Verificar se há erro
$temErro = isset($dados['erro']) && $dados['erro'] !== null;

// NOVO: Cor do banner baseada em erro ou momento
if ($temErro) {
    $bannerColor = '#F44336'; // Vermelho para erro
} else {
    $bannerColor = ($momento === 'initial') ? '#2196F3' : '#4CAF50'; // Azul para INITIAL, Verde para UPDATE
}
```

**Modificar assunto do email (linha ~70):**

```php
// Assunto do email com identificador visual
$subject = sprintf(
    '%s %s - Modal WhatsApp - %s',
    $momento_emoji,
    $momento_descricao,
    $telefoneCompleto
);
```

**Modificar corpo HTML do email (após linha ~100, adicionar seção de erro):**

```php
// NOVO: Seção de erro (se houver)
$erroSection = '';
if ($temErro) {
    $erroMessage = $dados['erro']['message'] ?? 'Erro desconhecido';
    $erroStatus = $dados['erro']['status'] ?? null;
    $erroCode = $dados['erro']['code'] ?? null;
    
    $erroSection = '
    <div class="field" style="background-color: #ffebee; border-left-color: #F44336;">
        <span class="label" style="color: #F44336; font-weight: bold;">❌ ERRO NO ENVIO:</span>
        <span class="value" style="color: #F44336;">' . htmlspecialchars($erroMessage) . '</span>
    </div>';
    
    if ($erroStatus !== null) {
        $erroSection .= '
        <div class="field" style="background-color: #ffebee; border-left-color: #F44336;">
            <span class="label">Status HTTP:</span>
            <span class="value" style="color: #F44336;">' . htmlspecialchars($erroStatus) . '</span>
        </div>';
    }
    
    if ($erroCode !== null) {
        $erroSection .= '
        <div class="field" style="background-color: #ffebee; border-left-color: #F44336;">
            <span class="label">Código:</span>
            <span class="value" style="color: #F44336;">' . htmlspecialchars($erroCode) . '</span>
        </div>';
    }
}
```

**Inserir `$erroSection` no HTML (após o campo GCLID, antes do campo Data/Hora):**

```php
// ... campo GCLID ...
' . $erroSection . '  // NOVO: Inserir seção de erro aqui
// ... campo Data/Hora ...
```

**Modificar corpo texto simples (após linha ~200, adicionar seção de erro):**

```php
// Corpo do email (texto simples - fallback)
$textBody = "
Novo Contato - Modal WhatsApp
============================

Um cliente preencheu o telefone corretamente no modal WhatsApp.
" . ($temErro ? "\n⚠️ ERRO: O envio ao EspoCRM falhou!\n" : "") . "

Telefone: {$telefoneCompleto}
Nome: {$nome}
CPF: {$cpf}
Email: {$emailCliente}
CEP: {$cep}
Placa: {$placa}
GCLID: {$gclid}
" . ($temErro ? "ERRO: " . ($dados['erro']['message'] ?? 'Erro desconhecido') . "\n" : "") . "
Data/Hora: {$dataHora}

---
Esta é uma notificação automática do sistema BP Seguros Imediato.
Não responda este email.
";
```

---

## 📝 LOGS ESPERADOS

### **Momento 1 (INITIAL - SUCESSO) - Console:**
```
📞 [EMAIL-AZUL] Enviando notificação Primeiro Contato - Apenas Telefone
📞 [EMAIL-AZUL] Notificação Primeiro Contato - Apenas Telefone enviada com SUCESSO
```

### **Momento 1 (INITIAL - ERRO) - Console:**
```
❌ [EMAIL-VERMELHO] Enviando notificação ERRO - Primeiro Contato - Apenas Telefone
❌ [EMAIL-VERMELHO] Notificação ERRO - Primeiro Contato - Apenas Telefone enviada com SUCESSO
```

### **Momento 2 (UPDATE - SUCESSO) - Console:**
```
✅ [EMAIL-VERDE] Enviando notificação Submissão Completa - Todos os Dados
✅ [EMAIL-VERDE] Notificação Submissão Completa - Todos os Dados enviada com SUCESSO
```

### **Momento 2 (UPDATE - ERRO) - Console:**
```
❌ [EMAIL-VERMELHO] Enviando notificação ERRO - Submissão Completa - Todos os Dados
❌ [EMAIL-VERMELHO] Notificação ERRO - Submissão Completa - Todos os Dados enviada com SUCESSO
```

### **Logs PHP (send_email_notification_endpoint.php):**
```
[EMAIL-ENDPOINT] Momento: initial | DDD: 11 | Celular: 999*** | Sucesso: SIM | Erro: NÃO
[EMAIL-ENDPOINT] Momento: initial_error | DDD: 11 | Celular: 888*** | Sucesso: SIM | Erro: SIM
[EMAIL-ENDPOINT] Momento: update | DDD: 11 | Celular: 777*** | Sucesso: SIM | Erro: NÃO
[EMAIL-ENDPOINT] Momento: update_error | DDD: 11 | Celular: 666*** | Sucesso: SIM | Erro: SIM
```

---

## ✅ CHECKLIST DE IMPLEMENTAÇÃO

- [ ] 1. Criar backup de `MODAL_WHATSAPP_DEFINITIVO.js` (local) - **`MODAL_WHATSAPP_DEFINITIVO.js.backup_EMAIL_DIRETO_YYYYMMDD_HHMMSS`**
- [ ] 2. Criar backup de `send_email_notification_endpoint.php` (local)
- [ ] 3. Criar backup de `send_admin_notification_ses.php` (local)
- [ ] 4. Adicionar função `identifyModalMoment()` no modal (com suporte a erro)
- [ ] 5. Adicionar função `sendAdminEmailNotification()` no modal (com suporte a erro)
- [ ] 6. Integrar chamada de email após sucesso de `registrarPrimeiroContatoEspoCRM()` (INITIAL)
- [ ] 7. Integrar chamada de email após ERRO de `registrarPrimeiroContatoEspoCRM()` (INITIAL - 3 locais)
- [ ] 8. Integrar chamada de email após sucesso de `atualizarLeadEspoCRM()` (UPDATE)
- [ ] 9. Integrar chamada de email após ERRO de `atualizarLeadEspoCRM()` (UPDATE - 3 locais)
- [ ] 10. Modificar `send_email_notification_endpoint.php` para aceitar parâmetro `erro`
- [ ] 11. Modificar `send_admin_notification_ses.php` para incluir informações de erro no email
- [ ] 12. Atualizar cabeçalho dos arquivos modificados (se houver versão)
- [ ] 13. Testar em DEV:
    - [ ] Abrir modal, digitar telefone (INITIAL - SUCESSO)
    - [ ] Verificar console logs: `📞 [EMAIL-AZUL]`
    - [ ] Verificar email recebido (banner azul)
    - [ ] Simular erro no endpoint (INITIAL - ERRO)
    - [ ] Verificar console logs: `❌ [EMAIL-VERMELHO]`
    - [ ] Verificar email recebido com informações de erro (banner vermelho)
    - [ ] Preencher todos os dados, submeter (UPDATE - SUCESSO)
    - [ ] Verificar console logs: `✅ [EMAIL-VERDE]`
    - [ ] Verificar email recebido (banner verde)
    - [ ] Simular erro no endpoint (UPDATE - ERRO)
    - [ ] Verificar console logs: `❌ [EMAIL-VERMELHO]`
    - [ ] Verificar email recebido com informações de erro (banner vermelho)
- [ ] 14. Verificar logs PHP do endpoint
- [ ] 15. Copiar arquivos modificados para servidor DEV
- [ ] 16. Testar em produção após aprovação
- [ ] 17. Copiar arquivos modificados para servidor PROD
- [ ] 18. Atualizar `PROJETOS_imediatoseguros-rpa-playwright.md`
- [ ] 19. Criar nova versão no GitHub com tag

---

## 🔄 ROLLBACK

Em caso de problemas:

1. **JavaScript:**
   - Restaurar backup de `MODAL_WHATSAPP_DEFINITIVO.js`
   - Copiar para servidor (DEV/PROD conforme necessário)

2. **PHP:**
   - Não há alterações em arquivos PHP
   - Endpoint `send_email_notification_endpoint.php` permanece inalterado

---

## ⚠️ OBSERVAÇÕES IMPORTANTES

1. **Não bloquear fluxo principal:** Em caso de erro no envio de email, o processo principal (modal) deve continuar normalmente
2. **Chamadas assíncronas:** Usar `.catch()` para não bloquear o retorno das funções principais
3. **Logs diferenciados:** Cada momento deve ter logs claramente identificáveis
4. **Emails visuais:** Cada email deve ter identificação visual clara (cor e emoji) no assunto e corpo
5. **Administradores:** 3 emails configurados:
   - `lrotero@gmail.com`
   - `alex.kaminski@imediatoseguros.com.br`
   - `alexkaminski70@gmail.com`
6. **Simplicidade:** Abordagem direta e explícita, sem interceptadores ou monkey-patching
7. **Manutenibilidade:** Código fácil de entender e debugar

---

## 🔍 REVISÃO TÉCNICA

**Status:** ⏳ Aguardando revisão do Engenheiro de Software

**Comentários do Engenheiro:**
_[Aguardando comentários]_

---

## 📊 TESTES

### **Teste 1: Momento INITIAL**
1. Abrir modal WhatsApp
2. Digitar apenas DDD + Celular
3. Verificar console: `📞 [EMAIL-AZUL]`
4. Verificar email recebido com banner azul e emoji 📞
5. Verificar que campos CPF, CEP, PLACA aparecem como "Não informado"

### **Teste 2: Momento UPDATE**
1. Com lead já criado no passo anterior
2. Preencher todos os campos no modal
3. Clicar em enviar
4. Verificar console: `✅ [EMAIL-VERDE]`
5. Verificar email recebido com banner verde e emoji ✅
6. Verificar que todos os campos aparecem preenchidos

### **Teste 3: Erro no Endpoint add_flyingdonkeys (INITIAL)**
1. Simular erro no endpoint `add_flyingdonkeys_v2.php` (ex: desabilitar temporariamente)
2. Abrir modal, digitar telefone
3. Verificar console: `❌ [EMAIL-VERMELHO]` (não `📞 [EMAIL-AZUL]`)
4. Verificar email recebido com banner vermelho e seção de erro
5. Verificar que informações de erro aparecem no email (mensagem, status, etc.)
6. Verificar que modal continua funcionando normalmente (não bloqueia)

### **Teste 4: Erro no Endpoint add_flyingdonkeys (UPDATE)**
1. Com lead já criado
2. Simular erro no endpoint `add_flyingdonkeys_v2.php`
3. Preencher todos os dados no modal e submeter
4. Verificar console: `❌ [EMAIL-VERMELHO]` (não `✅ [EMAIL-VERDE]`)
5. Verificar email recebido com banner vermelho e seção de erro
6. Verificar que informações de erro aparecem no email
7. Verificar que modal continua funcionando normalmente

### **Teste 5: Erro no Envio de Email (Não Bloqueante)**
1. Simular erro no endpoint de email (ex: desabilitar AWS SES temporariamente)
2. Verificar que modal continua funcionando normalmente
3. Verificar logs de erro no console (não crítico)

---

## 📈 ESTATÍSTICAS

**Tempo Estimado:** ~2h30min (aumentado devido à adição de tratamento de erros)
**Complexidade:** Média (chamadas diretas simples, mas com múltiplos pontos de integração)
**Impacto:** Alto (automatiza notificações e alerta sobre erros, permitindo resposta rápida a problemas)
**Risco:** Baixo (não modifica endpoints críticos, implementação explícita e fácil de reverter)

---

## 🎯 VANTAGENS DESTA ABORDAGEM

1. **Simplicidade:** Chamadas diretas e explícitas, fácil de entender
2. **Sem efeitos colaterais:** Não afeta outras chamadas fetch na página
3. **Manutenibilidade:** Código claro e fácil de debugar
4. **Baixo risco:** Não usa interceptadores ou monkey-patching
5. **Reversível:** Fácil de remover se necessário
6. **Visibilidade completa:** Administradores são notificados tanto em sucesso quanto em erro
7. **Resposta rápida a problemas:** Erros são comunicados imediatamente via email
8. **Informações detalhadas:** Emails de erro incluem mensagem, status HTTP e código de erro quando disponíveis

---

**Próximos Passos:**
1. Aguardar aprovação do projeto
2. Verificar backups criados
3. Implementar alterações conforme checklist
4. Testar em ambiente de desenvolvimento
5. Deploy para produção após validação

