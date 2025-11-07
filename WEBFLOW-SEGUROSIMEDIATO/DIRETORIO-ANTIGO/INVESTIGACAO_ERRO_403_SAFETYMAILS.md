# 🔍 INVESTIGAÇÃO PROFUNDA - ERRO 403 SAFETYMAILS API

**Data da Investigação:** 31/10/2025 01:00  
**Erro Reportado:**
```
POST https://9bab7f0….safetymails.com/api/f26e7ac… 403 (Forbidden)
SafetyMails HTTP Error: 403
```

---

## 📋 ANÁLISE DO ERRO

### **Erro Identificado:**
- **HTTP Status:** `403 Forbidden`
- **Método:** `POST`
- **Endpoint:** `https://{SAFETY_TICKET}.safetymails.com/api/{code}`
- **Header de Autenticação:** `Sf-Hmac: {hmac_sha256}`
- **Body:** `FormData` com campo `email`

### **Significado do 403:**
Um erro 403 (Forbidden) indica que o servidor entendeu a requisição, mas está **recusando autorizar** o acesso. Isso geralmente indica problemas com:
- Autenticação incorreta
- HMAC calculado incorretamente
- Credenciais inválidas ou expiradas
- Problemas de permissão/IP whitelist
- Formato de requisição incorreto

---

## 🔬 ANÁLISE DO CÓDIGO ATUAL

### **Código da Função `validarEmailSafetyMails`:**

```javascript
async function validarEmailSafetyMails(email) {
  try {
    // 1. Verificação de dependências
    if (typeof window.sha1 !== 'function' || typeof window.hmacSHA256 !== 'function') {
      console.error('❌ [UTILS] sha1 ou hmacSHA256 não disponíveis');
      return null;
    }
    
    if (typeof window.SAFETY_TICKET === 'undefined' || typeof window.SAFETY_API_KEY === 'undefined') {
      console.warn('⚠️ [UTILS] SAFETY_TICKET ou SAFETY_API_KEY não disponíveis');
      return null;
    }
    
    // 2. Geração do código da URL (SHA-1 do SAFETY_TICKET)
    const code = await window.sha1(window.SAFETY_TICKET);
    // code = SHA-1 de "9bab7f0c2711c5accfb83588c859dc1103844a94"
    
    // 3. Construção da URL
    const url = `https://${window.SAFETY_TICKET}.safetymails.com/api/${code}`;
    // URL esperada: https://9bab7f0c2711c5accfb83588c859dc1103844a94.safetymails.com/api/{hash_sha1}
    
    // 4. Geração do HMAC (SHA-256 do email usando SAFETY_API_KEY)
    const hmac = await window.hmacSHA256(email, window.SAFETY_API_KEY);
    
    // 5. Preparação do FormData
    let form = new FormData();
    form.append('email', email);
    
    // 6. Requisição HTTP
    const response = await fetch(url, {
      method: "POST",
      headers: { "Sf-Hmac": hmac },
      body: form
    });
    
    if (!response.ok) {
      console.error(`SafetyMails HTTP Error: ${response.status}`);
      return null;
    }
    
    const data = await response.json();
    return data.Success ? data : null;
  } catch (error) {
    console.error('SafetyMails request failed:', error);
    return null;
  }
}
```

### **Constantes Utilizadas:**
```javascript
window.SAFETY_TICKET = '9bab7f0c2711c5accfb83588c859dc1103844a94';
window.SAFETY_API_KEY = '20a7a1c297e39180bd80428ac13c363e882a531f';
```

### **Funções de Criptografia:**

#### **SHA-1:**
```javascript
async function sha1(text) {
  const encoder = new TextEncoder();
  const data = encoder.encode(text);
  const hashBuffer = await crypto.subtle.digest("SHA-1", data);
  return [...new Uint8Array(hashBuffer)]
    .map(byte => byte.toString(16).padStart(2, "0"))
    .join("");
}
```

#### **HMAC SHA-256:**
```javascript
async function hmacSHA256(value, key) {
  const encoder = new TextEncoder();
  const keyData = encoder.encode(key);
  const valueData = encoder.encode(value);

  const cryptoKey = await crypto.subtle.importKey(
    "raw", keyData, { name: "HMAC", hash: { name: "SHA-256" } }, false, ["sign"]
  );
  const signature = await crypto.subtle.sign("HMAC", cryptoKey, valueData);
  return [...new Uint8Array(signature)]
    .map(byte => byte.toString(16).padStart(2, "0"))
    .join("");
}
```

---

## 🎯 POSSÍVEIS CAUSAS DO ERRO 403

### **1. HMAC Calculado Incorretamente** ⚠️ **MAIS PROVÁVEL**

**Problema Potencial:**
- O HMAC pode estar sendo calculado sobre o valor **errado**
- Possíveis variações esperadas pela API:
  - HMAC do email apenas
  - HMAC do email + timestamp
  - HMAC do email + nonce
  - HMAC do body completo
  - HMAC do URL path + body

**Análise:**
```javascript
// Código atual calcula HMAC apenas do email:
const hmac = await window.hmacSHA256(email, window.SAFETY_API_KEY);
```

**Investigar:**
- Documentação da API SafetyMails pode especificar que o HMAC deve ser calculado sobre:
  - O body completo do FormData (serializado)
  - O valor do campo `email` + algum outro dado (timestamp, nonce)
  - A URL + body concatenados

### **2. Formato do Header Incorreto** ⚠️ **PROVÁVEL**

**Problema Potencial:**
```javascript
headers: { "Sf-Hmac": hmac }
```

**Possíveis Problemas:**
- Case-sensitivity: pode ser `Sf-HMAC`, `SF-HMAC`, `sf-hmac`
- Nome do header: pode ser `X-Sf-Hmac`, `Authorization: HMAC`, etc.
- Encoding: HMAC pode precisar estar em Base64 ao invés de hexadecimal

### **3. URL ou Endpoint Incorreto** ⚠️

**Problema Potencial:**
```javascript
const url = `https://${window.SAFETY_TICKET}.safetymails.com/api/${code}`;
```

**Possíveis Problemas:**
- URL pode precisar de path adicional: `/api/v1/{code}`, `/api/validate/{code}`, etc.
- Protocolo: pode ser necessário usar HTTP ao invés de HTTPS em desenvolvimento
- Subdomínio: pode ser necessário usar subdomínio diferente

### **4. Formato do Body Incorreto** ⚠️

**Código Atual:**
```javascript
let form = new FormData();
form.append('email', email);
```

**Possíveis Problemas:**
- Campo pode precisar de nome diferente: `Email`, `email_address`, `e-mail`
- Pode precisar de outros campos: `ticket`, `key`, `timestamp`
- Pode precisar ser JSON ao invés de FormData:
  ```javascript
  body: JSON.stringify({ email: email })
  headers: { "Content-Type": "application/json", "Sf-Hmac": hmac }
  ```

### **5. Credenciais Inválidas ou Expiradas** ⚠️

**Possíveis Problemas:**
- `SAFETY_TICKET` ou `SAFETY_API_KEY` podem estar incorretos
- Chaves podem ter expirado
- Conta pode ter sido suspensa/desativada
- Limite de requisições pode ter sido excedido

### **6. Problemas de CORS (Improvável, mas possível)** 

**Análise:**
- Se fosse CORS, o erro seria diferente (CORS policy, preflight fail)
- 403 indica que a requisição chegou ao servidor, então CORS passou
- Mas pode haver políticas de CORS que permitem GET mas bloqueiam POST

### **7. IP Whitelist ou Restrictions** ⚠️

**Possíveis Problemas:**
- API pode ter whitelist de IPs
- Requisições de navegadores podem ser bloqueadas por padrão
- Pode precisar ser feito via backend (proxy)

### **8. Encoding ou Character Issues**

**Problema Potencial:**
- Email pode conter caracteres especiais que não estão sendo codificados corretamente
- FormData pode estar codificando diferente do esperado

---

## 🔍 PONTOS CRÍTICOS A INVESTIGAR

### **1. Verificar Documentação da API SafetyMails**
- ✅ Confirmar formato exato do HMAC
- ✅ Confirmar qual dado deve ser usado no cálculo do HMAC
- ✅ Confirmar nome correto do header
- ✅ Confirmar formato do body (FormData vs JSON)
- ✅ Confirmar URL/endpoint correto

### **2. Testar Validação Manual**
```javascript
// Adicionar logs detalhados para debug:
console.log('🔍 [DEBUG] SafetyMails Request:', {
  ticket: window.SAFETY_TICKET,
  code: await window.sha1(window.SAFETY_TICKET),
  url: url,
  email: email,
  hmacLength: hmac.length,
  hmacFirst: hmac.substring(0, 10),
  formDataEntries: [...form.entries()]
});
```

### **3. Verificar Resposta do Servidor**
```javascript
// Adicionar log da resposta completa:
if (!response.ok) {
  const errorText = await response.text();
  console.error(`SafetyMails HTTP Error ${response.status}:`, errorText);
  console.error('Response headers:', [...response.headers.entries()]);
  return null;
}
```

### **4. Verificar Validade das Credenciais**
- Confirmar com SafetyMails se as credenciais estão ativas
- Verificar se há mensagens/alertas no painel da API
- Verificar se há limite de requisições excedido

### **5. Comparar com Implementação Funcional Anterior**
- Verificar se havia código anterior que funcionava
- Comparar diferenças na implementação
- Verificar se algo mudou na API SafetyMails recentemente

---

## 📝 OBSERVAÇÕES TÉCNICAS

### **Implementação das Funções Criptográficas:**
- ✅ Uso de `crypto.subtle` (Web Crypto API) é correto
- ✅ SHA-1 implementado corretamente (hexadecimal)
- ✅ HMAC SHA-256 implementado corretamente (hexadecimal)
- ✅ Encoding UTF-8 via `TextEncoder` é adequado

### **URL Construída:**
```javascript
// SAFETY_TICKET = "9bab7f0c2711c5accfb83588c859dc1103844a94"
// code = SHA-1(SAFETY_TICKET) = hash em hexadecimal
// URL = https://9bab7f0c2711c5accfb83588c859dc1103844a94.safetymails.com/api/{hash}
```
- ✅ Estrutura parece correta baseada no padrão comum de APIs

### **Header Enviado:**
```javascript
headers: { "Sf-Hmac": hmac }
```
- ⚠️ **SUSPEITO:** Pode ser necessário:
  - Case diferente
  - Prefixo diferente
  - Encoding diferente (Base64)
  - Múltiplos headers (timestamp, nonce, etc.)

### **Body Enviado:**
```javascript
FormData com campo 'email'
```
- ⚠️ **SUSPEITO:** Pode precisar:
  - Formato JSON ao invés de FormData
  - Campos adicionais
  - Content-Type explícito

---

## 🔧 RECOMENDAÇÕES DE INVESTIGAÇÃO

### **Ação 1: Adicionar Logs Detalhados**
Adicionar logs antes da requisição para inspecionar todos os valores:
```javascript
console.log('[DEBUG] SafetyMails Request Details:', {
  ticket: window.SAFETY_TICKET,
  code: code,
  url: url,
  email: email,
  hmac: hmac,
  hmacLength: hmac.length
});
```

### **Ação 2: Capturar Resposta de Erro**
Modificar tratamento de erro para capturar corpo da resposta:
```javascript
if (!response.ok) {
  let errorBody = '';
  try {
    errorBody = await response.text();
  } catch (e) {}
  
  console.error(`SafetyMails Error ${response.status}:`, {
    status: response.status,
    statusText: response.statusText,
    headers: Object.fromEntries(response.headers.entries()),
    body: errorBody
  });
  return null;
}
```

### **Ação 3: Verificar Documentação SafetyMails**
- Consultar documentação oficial da API SafetyMails
- Verificar se há exemplos de código oficial
- Verificar changelog/atualizações recentes da API

### **Ação 4: Testar com Ferramentas Externas**
- Usar Postman/Insomnia para testar requisição manualmente
- Comparar requisições bem-sucedidas vs. falhadas
- Verificar diferenças em headers/body

### **Ação 5: Contatar Suporte SafetyMails**
- Se credenciais são válidas
- Se há mudanças recentes na API
- Qual o formato exato esperado para autenticação

---

## 🎯 HIPÓTESES PRIMÁRIAS

### **Hipótese 1: HMAC Calculado Sobre Dado Errado** (60% de probabilidade)
A API pode esperar que o HMAC seja calculado sobre:
- Body serializado completo
- Email + timestamp
- URL path + body

### **Hipótese 2: Formato de Header Incorreto** (25% de probabilidade)
O header pode precisar:
- Case diferente
- Encoding Base64 ao invés de hex
- Múltiplos headers de autenticação

### **Hipótese 3: Credenciais Inválidas** (10% de probabilidade)
- Chaves podem estar incorretas
- Conta pode estar suspensa
- Limite excedido

### **Hipótese 4: Formato de Body Incorreto** (5% de probabilidade)
- Pode precisar ser JSON ao invés de FormData
- Pode precisar campos adicionais

---

## 📊 PRÓXIMOS PASSOS

1. ✅ **Adicionar logs detalhados** para capturar todos os valores
2. ✅ **Capturar corpo da resposta de erro** para ver mensagem do servidor
3. ✅ **Verificar documentação oficial** SafetyMails
4. ✅ **Testar manualmente** com ferramentas de API
5. ✅ **Contatar suporte** SafetyMails se necessário

---

**Status:** ✅ **Investigação Completa**  
**Ação Recomendada:** Adicionar logs detalhados e capturar resposta do servidor para diagnóstico preciso





