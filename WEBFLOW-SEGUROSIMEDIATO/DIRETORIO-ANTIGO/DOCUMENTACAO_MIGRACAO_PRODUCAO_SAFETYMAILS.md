# 📋 DOCUMENTAÇÃO DE MIGRAÇÃO PARA PRODUÇÃO - ENDPOINTS E KEYS

**Data de Criação:** 31/10/2025 01:30  
**Ambiente Atual:** DEV  
**Objetivo:** Guia completo para migração de todas as credenciais, endpoints e configurações de DEV para PRODUÇÃO

---

## 🎯 VISÃO GERAL

Este documento lista **todos os endpoints, chaves e configurações** que devem ser ajustados ao migrar do ambiente de desenvolvimento para produção no SafetyMails.

---

## 🔑 CREDENCIAIS SAFETYMAILS

### **AMBIENTE DEV (Atual - segurosimediato dev)**

| Campo | Valor | Observação |
|-------|-------|------------|
| **Nome da Origem** | `segurosimediato dev` | Identificação no painel SafetyMails |
| **Domínio/IP** | `segurosimediato-8119bf26e77bf4ff336a58e.webflow.io` | Webflow DEV |
| **Ticket Origem** | `fc5e18c10c4aa883b2c31a305f1c09fea3834138` | Usado na URL da API |
| **Api Key** | `20a7a1c297e39180bd80428ac13c363e882a531f` | Usado no cálculo HMAC |

### **AMBIENTE PRODUÇÃO (A ser configurado)**

| Campo | Valor | Observação |
|-------|-------|------------|
| **Nome da Origem** | `[A DEFINIR]` | Ex: "segurosimediato prod" |
| **Domínio/IP** | `[DOMÍNIO DE PRODUÇÃO]` | Ex: `bpsegurosimediato.com.br` ou domínio Webflow de produção |
| **Ticket Origem** | `[A OBTER DO SAFETYMAILS]` | Nova origem será criada no painel |
| **Api Key** | `[A OBTER DO SAFETYMAILS]` | Pode ser a mesma ou diferente |

---

## 📝 ARQUIVOS QUE PRECISAM SER ATUALIZADOS

### **1. Inside Head Tag Pagina.js (Head Code do Webflow):**

**⚠️ IMPORTANTE:** Este arquivo precisa ser atualizado **diretamente no Webflow**, na seção **Head Code** (Inside `<head>` tag).

**Arquivo Local:** `02-DEVELOPMENT/custom-codes/Inside Head Tag Pagina.js`

**Onde Atualizar:**
- Webflow Dashboard → Settings → Custom Code → **Head Code** (Inside `<head>` tag)
- Substituir o código atual pelo conteúdo do arquivo `Inside Head Tag Pagina.js`
- **OU** se o arquivo for servido externamente, atualizar referência para:
  - `https://dev.bpsegurosimediato.com.br/webhooks/InsideHeadTagPagina.js` (DEV)
  - `https://bpsegurosimediato.com.br/webhooks/InsideHeadTagPagina.js` (PRODUÇÃO - ajustar se necessário)

**Última Versão:**
- **Versão 1.1** - Correção na definição dos campos gclid (31/10/2025 13:06)
- Correção: Verificação defensiva antes de acessar `.value` de elementos

**Checklist:**
- [ ] Fazer backup do código atual no Webflow Head Code
- [ ] Atualizar Head Code com versão mais recente do arquivo
- [ ] Verificar se arquivo será servido externamente ou colado diretamente
- [ ] Testar funcionalidade GCLID após atualização

---

### **2. Arquivo Principal (Produção):**

**Arquivo:** `02-DEVELOPMENT/custom-codes/FooterCodeSiteDefinitivoCompleto.js`

**Linha:** 679-680

**Código Atual (DEV):**
```javascript
window.SAFETY_TICKET = 'fc5e18c10c4aa883b2c31a305f1c09fea3834138'; // DEV: segurosimediato dev
window.SAFETY_API_KEY = '20a7a1c297e39180bd80428ac13c363e882a531f'; // Mesmo para DEV e PROD
```

**Código para PRODUÇÃO:**
```javascript
// ⚠️ AMBIENTE: PRODUÇÃO
window.SAFETY_TICKET = '[TICKET_ORIGEM_PRODUCAO]'; // PROD: [nome da origem]
window.SAFETY_API_KEY = '[API_KEY_PRODUCAO]'; // PROD
```

---

## 🔄 PROCESSO DE MIGRAÇÃO - PASSO A PASSO

### **FASE 1: Criar Nova Origem no SafetyMails (Produção)**

1. Acessar painel SafetyMails: https://www.safetymails.com
2. Ir em **"Origens da API"** ou **"API Origins"**
3. Clicar em **"Criar Nova Origem"**
4. Preencher:
   - **Nome da Origem:** `segurosimediato prod` (ou similar)
   - **Domínio ou IP:** 
     - Domínio de produção (ex: `bpsegurosimediato.com.br`)
     - OU domínio Webflow de produção (ex: `[site].webflow.io`)
   - **Descrição:** Ambiente de produção
5. Salvar e obter as novas credenciais:
   - ✅ **Ticket Origem** (novo)
   - ✅ **Api Key** (pode ser a mesma ou nova)

### **FASE 2: Documentar Credenciais de Produção**

**⚠️ IMPORTANTE:** Preencher esta tabela com as credenciais reais de produção:

| Item | Valor | Fonte |
|------|-------|-------|
| Ticket Origem PROD | `________________` | Painel SafetyMails |
| Api Key PROD | `________________` | Painel SafetyMails |
| Domínio PROD | `________________` | Configuração Webflow |
| Data de Migração | `________________` | Data do deploy |

### **FASE 3: Atualizar Código**

#### **3.1. Atualizar FooterCodeSiteDefinitivoCompleto.js**

**Localização:** Linhas 679-680

**Substituir:**
```javascript
window.SAFETY_TICKET = 'fc5e18c10c4aa883b2c31a305f1c09fea3834138'; // DEV
window.SAFETY_API_KEY = '20a7a1c297e39180bd80428ac13c363e882a531f';
```

**Por:**
```javascript
window.SAFETY_TICKET = '[TICKET_ORIGEM_PRODUCAO]'; // PROD
window.SAFETY_API_KEY = '[API_KEY_PRODUCAO]'; // PROD
```

**Exemplo (após preencher):**
```javascript
window.SAFETY_TICKET = '9bab7f0c2711c5accfb83588c859dc1103844a94'; // PROD: segurosimediato prod
window.SAFETY_API_KEY = '20a7a1c297e39180bd80428ac13c363e882a531f'; // PROD
```

#### **3.2. Verificar Comentários no Código**

Atualizar comentários indicando ambiente PRODUÇÃO:
```javascript
// ⚠️ AMBIENTE: PRODUÇÃO
// OU
// PROD: segurosimediato prod
```

### **FASE 4: Testar em Ambiente de Staging**

1. Fazer deploy em ambiente de staging/teste
2. Testar validação de email:
   - Digitar email válido → deve passar
   - Digitar email inválido → deve mostrar aviso
3. Verificar console do navegador:
   - ✅ Não deve haver erro 403
   - ✅ Requisições devem retornar 200 OK
4. Testar em diferentes navegadores (Chrome, Firefox, Safari)

### **FASE 5: Deploy em Produção**

1. Fazer backup do arquivo atual em produção
2. Fazer deploy do arquivo atualizado
3. Monitorar logs/console nas primeiras 24h
4. Verificar métricas no painel SafetyMails

---

## 🌐 ENDPOINTS E URLs

### **Endpoint da API SafetyMails**

**Formato:**
```
https://{SAFETY_TICKET}.safetymails.com/api/{SHA1(SAFETY_TICKET)}
```

### **DEV (Atual):**

**Ticket:** `fc5e18c10c4aa883b2c31a305f1c09fea3834138`

**SHA-1 do Ticket:** `[será calculado automaticamente pelo código]`

**URL completa:** `https://fc5e18c10c4aa883b2c31a305f1c09fea3834138.safetymails.com/api/{hash}`

### **PRODUÇÃO (A ser configurado):**

**Ticket:** `[A PREENCHER]`

**SHA-1 do Ticket:** `[calculado automaticamente]`

**URL completa:** `https://[TICKET_PRODUCAO].safetymails.com/api/{hash}`

---

## 🔐 AUTENTICAÇÃO HMAC

### **Como Funciona:**

1. **Cálculo do HMAC:**
   ```javascript
   const hmac = await window.hmacSHA256(email, window.SAFETY_API_KEY);
   ```

2. **Header enviado:**
   ```javascript
   headers: { "Sf-Hmac": hmac }
   ```

### **Valores:**

| Ambiente | API Key | Uso |
|----------|---------|-----|
| **DEV** | `20a7a1c297e39180bd80428ac13c363e882a531f` | Cálculo do HMAC |
| **PROD** | `[A PREENCHER]` | Cálculo do HMAC |

---

## ✅ CHECKLIST DE MIGRAÇÃO

### **Pré-Migração:**
- [ ] Criar nova origem no painel SafetyMails (PRODUÇÃO)
- [ ] Documentar Ticket Origem de produção
- [ ] Documentar Api Key de produção
- [ ] Documentar domínio de produção
- [ ] Verificar se domínio está autorizado no SafetyMails

### **Atualização do Código:**
- [ ] **Inside Head Tag Pagina.js:** Atualizar Head Code do Webflow com versão mais recente
- [ ] Fazer backup do arquivo atual
- [ ] Atualizar `SAFETY_TICKET` no `FooterCodeSiteDefinitivoCompleto.js`
- [ ] Atualizar `SAFETY_API_KEY` (se diferente)
- [ ] Atualizar comentários indicando ambiente PRODUÇÃO
- [ ] Verificar se não há outras referências às credenciais DEV

### **Testes:**
- [ ] Testar em staging/teste
- [ ] Verificar console do navegador (sem erros 403)
- [ ] Testar validação de email válido
- [ ] Testar validação de email inválido
- [ ] Testar em múltiplos navegadores
- [ ] Verificar métricas no painel SafetyMails

### **Deploy:**
- [ ] Fazer backup do arquivo em produção
- [ ] Deploy do arquivo atualizado
- [ ] Monitorar logs nas primeiras 24h
- [ ] Verificar consumo de créditos no SafetyMails
- [ ] Documentar data/hora da migração

---

## 📊 MAPEAMENTO DE CONFIGURAÇÕES

### **Configurações DEV (Atual):**

```javascript
// Ambiente: DESENVOLVIMENTO
// Data: 31/10/2025
window.SAFETY_TICKET = 'fc5e18c10c4aa883b2c31a305f1c09fea3834138';
window.SAFETY_API_KEY = '20a7a1c297e39180bd80428ac13c363e882a531f';

// Domínio autorizado: segurosimediato-8119bf26e77bf4ff336a58e.webflow.io
// Nome da origem: segurosimediato dev
```

### **Configurações PRODUÇÃO (Template):**

```javascript
// Ambiente: PRODUÇÃO
// Data de migração: [A PREENCHER]
window.SAFETY_TICKET = '[TICKET_PRODUCAO]';
window.SAFETY_API_KEY = '[API_KEY_PRODUCAO]';

// Domínio autorizado: [DOMINIO_PRODUCAO]
// Nome da origem: [NOME_ORIGEM_PRODUCAO]
```

---

## 🔍 VALIDAÇÃO PÓS-MIGRAÇÃO

### **Como Verificar se Está Funcionando:**

1. **Console do Navegador:**
   - Abrir DevTools (F12)
   - Ir na aba Network
   - Digitar email no campo de validação
   - Verificar requisição para `*.safetymails.com`
   - ✅ Status deve ser `200 OK`
   - ❌ Não deve ser `403 Forbidden`

2. **Painel SafetyMails:**
   - Verificar logs de uso
   - Verificar consumo de créditos
   - Verificar origem que está sendo usada

3. **Teste Funcional:**
   - Email válido: deve validar sem erro
   - Email inválido: deve mostrar aviso (se configurado)
   - Sem erros no console

---

## 📞 SUPORTE E CONTATOS

### **SafetyMails:**
- **Site:** https://www.safetymails.com
- **Documentação:** https://docs.safetymails.com
- **Suporte:** Através do painel SafetyMails

### **Informações da Conta:**
- **Email da conta:** [A DOCUMENTAR]
- **Usuário:** [A DOCUMENTAR]
- **Plano:** [A DOCUMENTAR]

---

## ⚠️ IMPORTANTE

1. **Nunca commitar credenciais de produção no GitHub** (se houver repositório público)
2. **Sempre fazer backup** antes de atualizar arquivos em produção
3. **Testar em staging** antes de produção
4. **Monitorar logs** após deploy
5. **Documentar data/hora** da migração

---

## 🔗 TODOS OS ENDPOINTS E KEYS DO SISTEMA

### **1. SafetyMails (Validação de Email)**

**DEV:**
- Ticket: `fc5e18c10c4aa883b2c31a305f1c09fea3834138`
- API Key: `20a7a1c297e39180bd80428ac13c363e882a531f`
- Endpoint: `https://fc5e18c10c4aa883b2c31a305f1c09fea3834138.safetymails.com/api/{hash}`

**PRODUÇÃO:**
- Ticket: `[A PREENCHER]`
- API Key: `[A PREENCHER]`
- Endpoint: `https://[TICKET_PRODUCAO].safetymails.com/api/{hash}`

---

### **2. Apilayer (Validação de Telefone)**

**DEV e PRODUÇÃO (Mesmo):**
- API Key: `dce92fa84152098a3b5b7b8db24debbc`
- Endpoint: `https://apilayer.net/api/validate?access_key={KEY}&country_code=BR&number={NUM}`

**Observação:** Parece ser a mesma key para ambos os ambientes. Verificar se é necessário criar key separada para produção.

---

### **3. APIs Internas (mdmidia.com.br)**

**Validação de CPF:**
- Endpoint DEV/PROD: `https://mdmidia.com.br/cpf-validate.php`
- Método: POST
- Body: JSON `{ "cpf": "xxx" }`

**Validação de Placa:**
- Endpoint DEV/PROD: `https://mdmidia.com.br/placa-validate.php`
- Método: POST
- Body: JSON `{ "placa": "xxx" }`

**Observação:** Verificar se estes endpoints funcionam igual em DEV e PROD, ou se há endpoints separados.

---

### **4. ViaCEP (Consulta de Endereço)**

**DEV e PRODUÇÃO (Público):**
- Endpoint: `https://viacep.com.br/ws/{cep}/json/`
- Método: GET
- Público, não requer autenticação

---

### **5. RPA (Sistema de Automação)**

**Script RPA:**
- Endpoint DEV: `https://mdmidia.com.br/webflow_injection_limpo.js`
- Endpoint PRODUÇÃO: `[VERIFICAR SE É DIFERENTE]`

**Observação:** Verificar se há script separado para produção ou se usa o mesmo.

---

### **6. Modal WhatsApp**

**DEV:**
- Endpoint: `https://dev.bpsegurosimediato.com.br/webhooks/MODAL_WHATSAPP_DEFINITIVO.js?v=23`

**PRODUÇÃO:**
- Endpoint: `https://bpsegurosimediato.com.br/webhooks/MODAL_WHATSAPP_DEFINITIVO.js?v=23`
- OU: `[VERIFICAR ENDPOINT DE PRODUÇÃO]`

---

### **7. Sistema de Logging (Debug Logger)**

**DEV e PRODUÇÃO:**
- Endpoint: `https://bpsegurosimediato.com.br/logging_system/debug_logger_db.php`
- Método: POST
- Body: JSON com logs

**Observação:** Parece ser o mesmo endpoint para ambos os ambientes.

---

### **8. Arquivo Principal (Footer Code Unificado)**

**DEV:**
- URL: `https://dev.bpsegurosimediato.com.br/webhooks/FooterCodeSiteDefinitivoCompleto.js?v=1`

**PRODUÇÃO:**
- URL: `https://bpsegurosimediato.com.br/webhooks/FooterCodeSiteDefinitivoCompleto.js?v=1`
- OU: `[VERIFICAR URL DE PRODUÇÃO]`

**Observação:** Verificar se o arquivo será servido do mesmo servidor ou se há servidor separado para produção.

---

## 📝 CHECKLIST COMPLETO DE ENDPOINTS

### **SafetyMails:**
- [ ] Criar origem de produção no SafetyMails
- [ ] Obter Ticket Origem de produção
- [ ] Obter API Key de produção (ou confirmar se é a mesma)
- [ ] Autorizar domínio de produção
- [ ] Atualizar `SAFETY_TICKET` no código
- [ ] Atualizar `SAFETY_API_KEY` no código (se diferente)

### **Apilayer:**
- [ ] Verificar se API Key é a mesma para DEV e PROD
- [ ] Se não, criar nova key para produção
- [ ] Atualizar `APILAYER_KEY` no código (se necessário)

### **APIs Internas (mdmidia.com.br):**
- [ ] Verificar se endpoints de CPF funcionam em produção
- [ ] Verificar se endpoints de Placa funcionam em produção
- [ ] Se houver endpoints diferentes para produção, atualizar URLs

### **RPA:**
- [ ] Verificar URL do script RPA em produção
- [ ] Atualizar URL no código se for diferente

### **Modal WhatsApp:**
- [ ] Verificar URL do modal em produção
- [ ] Atualizar URL no código se for diferente

### **Webflow Head Code (Inside Head Tag Pagina.js):**
- [ ] ⚠️ **ATENÇÃO:** Atualizar Head Code do Webflow com versão mais recente
- [ ] Fazer backup do código atual no Webflow
- [ ] Atualizar com arquivo `Inside Head Tag Pagina.js` versão 1.1
- [ ] Verificar se arquivo será servido externamente ou colado diretamente
- [ ] Testar funcionalidade GCLID após atualização

### **Arquivo Principal:**
- [ ] Verificar URL do arquivo unificado em produção
- [ ] Atualizar referência no Webflow se necessário
- [ ] Testar acesso à URL de produção

---

## 📝 NOTAS ADICIONAIS

### **URLs Relevantes:**

- **Painel SafetyMails:** https://www.safetymails.com
- **Documentação API:** https://docs.safetymails.com
- **Arquivo Principal:** `02-DEVELOPMENT/custom-codes/FooterCodeSiteDefinitivoCompleto.js`
- **Servidor:** `https://dev.bpsegurosimediato.com.br/webhooks/FooterCodeSiteDefinitivoCompleto.js`

### **Versão do Arquivo:**

- **Versão atual:** 1.0
- **Última atualização DEV:** 31/10/2025
- **Próxima atualização PROD:** [A DEFINIR]

---

**Status:** ✅ **Documentação Completa**  
**Próxima Ação:** Preencher credenciais de produção quando disponíveis e executar migração

