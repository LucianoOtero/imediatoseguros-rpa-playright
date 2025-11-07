# 🔍 DIAGNÓSTICO TÉCNICO: Problema de Cache e Endpoint Incorreto

**Data**: 2025-10-29  
**Severidade**: 🔴 CRÍTICA  
**Status**: Problema ativo impedindo funcionamento do modal WhatsApp

---

## 📋 SUMÁRIO EXECUTIVO

O sistema está tentando chamar o endpoint `add_travelangels.php` (sem sufixo `_dev`) em ambiente de desenvolvimento, causando:
1. ❌ **Erro CORS**: Endpoint não possui headers CORS configurados
2. ❌ **Erro 500**: Endpoint pode não existir ou estar quebrado
3. ❌ **Falha na integração**: Lead não é criado no EspoCRM

**Causa raiz identificada**: Cache do navegador executando versão antiga do JavaScript, mesmo com versionamento (`?v=16`).

---

## 🚨 PROBLEMA IDENTIFICADO

### **Sintoma no Console do Navegador**

```
Access to fetch at 'https://bpsegurosimediato.com.br/dev/webhooks/add_travelangels.php' 
from origin 'https://segurosimediato-8119bf26e77bf4ff336a58e.webflow.io' 
has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present.
```

```
POST https://bpsegurosimediato.com.br/dev/webhooks/add_travelangels.php 
net::ERR_FAILED 500 (Internal Server Error)
```

### **Endpoint Incorreto Sendo Chamado**
- ❌ **Chamado**: `https://bpsegurosimediato.com.br/dev/webhooks/add_travelangels.php`
- ✅ **Esperado**: `https://bpsegurosimediato.com.br/dev/webhooks/add_travelangels_dev.php`

**Evidência**: Console mostra claramente a URL sem o sufixo `_dev`.

---

## 📊 EVIDÊNCIAS COLETADAS

### **1. Código Fonte no Servidor (Versão Correta)**

**Arquivo**: `/var/www/html/dev/webhooks/MODAL_WHATSAPP_DEFINITIVO.js`  
**Última modificação**: 2025-10-29 16:21  
**Tamanho**: 76KB

**Linha 145 do arquivo no servidor**:
```javascript
dev: 'https://bpsegurosimediato.com.br/dev/webhooks/add_travelangels_dev.php',
```

✅ **Código no servidor está CORRETO**.

---

### **2. Código Fonte Local (Versão Correta)**

**Arquivo**: `MODAL_WHATSAPP_DEFINITIVO.js` (local)  
**Linha 145**:
```javascript
dev: 'https://bpsegurosimediato.com.br/dev/webhooks/add_travelangels_dev.php',
```

✅ **Código local está CORRETO**.

---

### **3. Log do Console do Navegador (Versão Incorreta em Execução)**

**Evidência do console**:
```
🌍 [MODAL] Ambiente: DEV | Endpoint travelangels: https://bpsegurosimediato.com.br/dev/webhooks/add_travelangels.php
```

**Arquivo executado**: `MODAL_WHATSAPP_DEFINITIVO.js?v=16`

❌ **Navegador está executando versão ANTIGA** (sem `_dev` no endpoint).

---

### **4. Logs do Servidor**

**Arquivo**: `/var/www/html/dev/logs/travelangels_dev.txt`  
**Última entrada**: `2025-10-29 18:37:47`

**Log mostra**:
```json
{
    "event": "json_decode_error",
    "raw_input": "{\"data\": \"{\"DDD-CELULAR\":\"11\"\",\"CELULAR\":\"976687668\"...}"
}
```

**Análise**: 
- Endpoint `add_travelangels_dev.php` NÃO recebeu novas chamadas
- Última chamada foi há ~1 hora
- Problema de JSON malformado (enviando `data` como string) em chamadas anteriores

---

## 🔬 ANÁLISE TÉCNICA DETALHADA

### **1. Sistema de Versionamento**

**Arquivo**: `02-DEVELOPMENT/custom-codes/Footer Code Site Definitivo.js`  
**Linha 249**:
```javascript
script.src = 'https://dev.bpsegurosimediato.com.br/webhooks/MODAL_WHATSAPP_DEFINITIVO.js?v=16';
```

**Problema identificado**:
- ✅ Versionamento está presente (`?v=16`)
- ❌ **Cache do navegador pode estar ignorando o parâmetro `?v=16`**
- ❌ Cloudflare pode estar servindo versão em cache

---

### **2. Função de Detecção de Endpoint**

**Arquivo**: `MODAL_WHATSAPP_DEFINITIVO.js`  
**Linhas 140-160**:
```javascript
function getEndpointUrl(endpoint) {
    const isDev = isDevelopmentEnvironment();
    
    const endpoints = {
      travelangels: {
        dev: 'https://bpsegurosimediato.com.br/dev/webhooks/add_travelangels_dev.php',
        prod: 'https://bpsegurosimediato.com.br/add_travelangels.php'
      },
      octadesk: {
        dev: 'https://bpsegurosimediato.com.br/dev/webhooks/add_webflow_octa_dev.php',
        prod: 'https://bpsegurosimediato.com.br/add_webflow_octa.php'
      }
    };
    
    const env = isDev ? 'dev' : 'prod';
    const url = endpoints[endpoint][env];
    
    console.log(`🌍 [MODAL] Ambiente: ${env.toUpperCase()} | Endpoint ${endpoint}: ${url}`);
    
    return url;
}
```

**Análise**:
- ✅ Código está correto no servidor
- ✅ Retorna `add_travelangels_dev.php` quando `isDev = true`
- ❌ **Navegador está executando versão ANTIGA desta função** que retorna `add_travelangels.php`

---

### **3. Ambiente de Desenvolvimento Detectado**

**Console mostra**:
```
🌍 [MODAL] Ambiente detectado: DESENVOLVIMENTO
🌍 [MODAL] Ambiente: DEV | Endpoint travelangels: https://bpsegurosimediato.com.br/dev/webhooks/add_travelangels.php
```

**Análise**:
- ✅ Ambiente é detectado como DEV corretamente
- ❌ **MAS a URL retornada ainda é a antiga** (sem `_dev`)
- **Conclusão**: A função `getEndpointUrl()` sendo executada é de uma versão ANTIGA do arquivo

---

### **4. Configuração Webflow**

**Endpoints configurados no Webflow** (confirmado pelo usuário):
- `https://bpsegurosimediato.com.br/dev/webhooks/add_travelangels_dev.php`
- `https://bpsegurosimediato.com.br/dev/webhooks/add_webflow_octa_dev.php`

✅ **Webflow está configurado corretamente**.

---

## 🔍 CAUSAS RAIZ POSSÍVEIS

### **1. Cache do Navegador (Mais Provável) ⚠️**

**Evidências**:
- Código no servidor está correto
- Código local está correto
- Mas navegador executa versão antiga

**Mecanismos de cache possíveis**:
- **Browser Cache**: Navegador cacheou `MODAL_WHATSAPP_DEFINITIVO.js` mesmo com `?v=16`
- **Service Worker**: PWA/Service Worker pode estar servindo versão em cache
- **Cloudflare Cache**: CDN pode estar servindo versão antiga
  - **Evidência**: Cloudflare Cache Rule configurada anteriormente para bypass

---

### **2. Múltiplas Versões do Arquivo**

**Possibilidade**:
- Arquivo carregado de localização diferente
- Cache intermediary (proxy corporativo)
- Outro script sobrescrevendo a função `getEndpointUrl()`

**Verificação necessária**:
```bash
# Verificar se há múltiplas versões do arquivo no servidor
find /var/www/html -name "MODAL_WHATSAPP_DEFINITIVO.js" -type f
```

---

### **3. Problema de Upload/Deployment**

**Possibilidade**:
- Arquivo não foi atualizado corretamente no servidor
- Permissões incorretas impedindo sobrescrita
- Upload parcial (arquivo corrompido)

**Verificação realizada**: ✅ Arquivo no servidor tem código correto (linha 145 confere).

---

## 📁 REFERÊNCIAS AOS ARQUIVOS

### **Arquivos Fonte Relevantes**

1. **`MODAL_WHATSAPP_DEFINITIVO.js`**
   - **Local**: `./MODAL_WHATSAPP_DEFINITIVO.js`
   - **Servidor**: `/var/www/html/dev/webhooks/MODAL_WHATSAPP_DEFINITIVO.js`
   - **URL de carga**: `https://dev.bpsegurosimediato.com.br/webhooks/MODAL_WHATSAPP_DEFINITIVO.js?v=16`
   - **Linha crítica**: 145 (definição do endpoint dev)

2. **`Footer Code Site Definitivo.js`**
   - **Local**: `02-DEVELOPMENT/custom-codes/Footer Code Site Definitivo.js`
   - **Linha crítica**: 249 (carregamento do modal com `?v=16`)

3. **Endpoints PHP**
   - **Correto**: `/var/www/html/dev/webhooks/add_travelangels_dev.php`
   - **Incorreto (sendo chamado)**: `/var/www/html/dev/webhooks/add_travelangels.php` (pode não existir)

---

## 🎯 SOLUÇÕES PROPOSTAS

### **Solução 1: Forçar Bypass de Cache no Carregamento** ⭐ RECOMENDADA

**Implementação**:
```javascript
// Footer Code Site Definitivo.js - Linha 249
script.src = 'https://dev.bpsegurosimediato.com.br/webhooks/MODAL_WHATSAPP_DEFINITIVO.js?v=' + Date.now();
```

**Vantagens**:
- Força carregamento sempre da versão mais recente
- Não requer limpeza manual de cache
- Implementação simples

---

### **Solução 2: Incrementar Versão e Configurar Cache-Control**

**Implementação**:
1. Alterar `?v=16` para `?v=17` (ou usar timestamp)
2. Adicionar headers HTTP no servidor:
   ```
   Cache-Control: no-cache, no-store, must-revalidate
   Pragma: no-cache
   Expires: 0
   ```

---

### **Solução 3: Verificar e Limpar Cache do Cloudflare**

**Ações necessárias**:
1. Verificar regra de cache do Cloudflare para `/webhooks/*.js`
2. Fazer "Purge Everything" ou purge específico do arquivo
3. Confirmar que a regra está ativa

---

### **Solução 4: Verificar Service Workers**

**Verificação necessária**:
```javascript
// No console do navegador
navigator.serviceWorker.getRegistrations().then(registrations => {
  registrations.forEach(reg => reg.unregister());
});
```

---

## 🏗️ ANÁLISE DE INFRAESTRUTURA

### **Configuração Atual**

**Stack**:
- **Frontend**: Webflow (static site)
- **JavaScript**: Carregado via `<script src>` externo
- **Backend**: PHP endpoints em `bpsegurosimediato.com.br`
- **CDN**: Cloudflare (identificado pela presença de headers `Cf-Ray`)

**Camadas de Cache Identificadas**:
1. ✅ **Cloudflare Cache** - Configurado (regra de bypass para `/webhooks/*.js`)
2. ⚠️ **Browser Cache** - Provável culpado
3. ⚠️ **Service Worker** - A verificar

---

### **Fluxo de Carregamento Atual**

```
1. Navegador → Webflow (HTML)
2. HTML carrega → Footer Code Site Definitivo.js (via Webflow Custom Code)
3. Footer Code → Carrega MODAL_WHATSAPP_DEFINITIVO.js?v=16
4. MODAL → Executa getEndpointUrl() → Retorna URL incorreta ❌
```

**Onde o cache pode interferir**:
- Passo 3: Browser cacheia `MODAL_WHATSAPP_DEFINITIVO.js` mesmo com `?v=16`
- Passo 3: Cloudflare serve versão em cache (apesar da regra)
- Passo 4: Service Worker intercepta e serve versão antiga

---

## 📝 CHECKLIST DE VERIFICAÇÃO

Para confirmar diagnóstico:

- [ ] Verificar se há Service Worker ativo
- [ ] Confirmar que arquivo no servidor tem checksum correto
- [ ] Testar em modo anônimo do navegador
- [ ] Verificar headers HTTP do arquivo JavaScript servido
- [ ] Confirmar que Cloudflare está aplicando regra de bypass
- [ ] Verificar se há múltiplas versões do arquivo
- [ ] Testar com timestamp no lugar de `?v=16`

---

## 🚀 RECOMENDAÇÃO PRINCIPAL

**Implementar Solução 1 imediatamente**: Usar `Date.now()` ou timestamp para garantir que cada carregamento busque versão nova.

**Após implementação, validar**:
1. Console mostra endpoint correto (`add_travelangels_dev.php`)
2. Requisição não é bloqueada por CORS
3. Lead é criado com sucesso no EspoCRM
4. Logs do servidor mostram entrada nova

---

---

## 👨‍💻 APRESENTAÇÃO PARA ENGENHEIRO DE SOFTWARE (INFRAESTRUTURA)

### **Contexto do Problema**

Sistema de modal WhatsApp integrado com Webflow que precisa chamar endpoints diferentes em desenvolvimento vs. produção. O código JavaScript está correto tanto no servidor quanto localmente, mas o navegador executa uma versão antiga que chama o endpoint errado.

### **Sintomas em Produção/Desenvolvimento**

**Ambiente de Desenvolvimento** (atual):
- Navegador tenta chamar: `add_travelangels.php` (sem `_dev`)
- Deveria chamar: `add_travelangels_dev.php`
- Resultado: Erro CORS + 500

**Ambiente de Produção** (hipotético):
- Funcionaria corretamente, pois `add_travelangels.php` existe em produção

### **Questionamentos Técnicos para o Engenheiro**

1. **Gestão de Cache em CDN (Cloudflare)**:
   - A regra de bypass configurada (`*://dev.bpsegurosimediato.com.br/webhooks/*.js`) está realmente funcionando?
   - Há alguma outra camada de cache (origin cache, edge cache) que precisa ser configurada?
   - Devo usar headers HTTP específicos (`Cache-Control`, `Vary`) ao invés de apenas regras no Cloudflare?

2. **Versionamento de Assets JavaScript**:
   - Parâmetro `?v=16` é suficiente para invalidar cache?
   - Devo usar hash do conteúdo (e.g., `?v=a1b2c3d4`) ao invés de version number?
   - Qual a melhor prática: timestamp vs. version number vs. content hash?

3. **Service Workers e PWA**:
   - Webflow pode ter Service Worker ativo que cacheia assets?
   - Como detectar e limpar isso programaticamente?
   - Devo adicionar lógica no código para verificar/limpar Service Workers?

4. **Estratégia de Deploy**:
   - Devo renomear o arquivo ao invés de versionar? (`MODAL_WHATSAPP_DEFINITIVO_v17.js`)
   - Devo usar subdomínio diferente para assets (`assets-dev.bpsegurosimediato.com.br`)?
   - Há alguma estratégia de blue-green deployment para assets estáticos?

5. **Monitoramento e Diagnóstico**:
   - Como adicionar telemetria para detectar quando navegador está usando versão antiga?
   - Devo implementar check de versão na inicialização do modal?
   - Há ferramentas de CDN analytics que mostram hit rate de cache vs. miss?

6. **CORS e Headers de Desenvolvimento**:
   - O endpoint `add_travelangels.php` (sem `_dev`) deveria ter CORS configurado também?
   - Ou é mais seguro deixar ele sem CORS e garantir que sempre use o `_dev` correto?
   - Há alguma configuração no servidor web (Apache/Nginx) que pode bloquear requisições baseado em origem?

### **Informações Técnicas Adicionais**

**Servidor**: `root@46.62.174.150`  
**Stack**: PHP 7.x/8.x, Apache/Nginx (a confirmar), Cloudflare CDN  
**Estrutura de diretórios**:
```
/var/www/html/
├── dev/
│   ├── webhooks/
│   │   ├── add_travelangels_dev.php ✅ (existe, funcional)
│   │   ├── add_webflow_octa_dev.php ✅ (existe, funcional)
│   │   └── MODAL_WHATSAPP_DEFINITIVO.js ✅ (existe, código correto)
│   └── logs/
│       ├── travelangels_dev.txt
│       └── webhook_octadesk_dev.txt
└── [produção]
    └── webhooks/
        ├── add_travelangels.php
        └── add_webflow_octa.php
```

**Headers HTTP do arquivo JavaScript** (verificar necessário):
```bash
curl -I https://dev.bpsegurosimediato.com.br/webhooks/MODAL_WHATSAPP_DEFINITIVO.js?v=16
```

**Verificação de Service Worker** (executar no console):
```javascript
navigator.serviceWorker.getRegistrations().then(regs => console.log(regs.length))
```

### **Verificação de Integridade do Arquivo**

**MD5 Hash**:
- **Servidor**: `c60433b6c911360913e15e5b62c3f5b8`
- **Local**: `c60433b6c911360913e15e5b62c3f5b8`
- **Resultado**: ✅ **HASHES IDÊNTICOS** - Arquivo no servidor está correto

**Conclusão**: Problema NÃO é de upload/deployment. É definitivamente **cache** (navegador ou Cloudflare).

### **🔴 CAUSA RAIZ IDENTIFICADA: Header HTTP `Cache-Control: immutable`**

**Headers HTTP da resposta** (verificado via `curl -I`):
```http
HTTP/2 200
cache-control: public, max-age=2592000, immutable
expires: Fri, 28 Nov 2025 19:50:33 GMT
cf-cache-status: MISS
```

**PROBLEMA CRÍTICO**:
- ❌ **Header `Cache-Control: immutable`** faz navegadores modernos IGNORAREM query params
- Navegadores que veem `immutable` assumem que o arquivo NUNCA muda, então não verificam novamente mesmo com `?v=16`
- Isso explica por que o versionamento não está funcionando!

**SOLUÇÃO**:
- Remover `immutable` do header para arquivos em `/dev/webhooks/*.js`
- Ou configurar `Cache-Control: no-cache` especificamente para desenvolvimento

---

**Criado em**: 2025-10-29  
**Última atualização**: 2025-10-29  
**Próxima ação**: Apresentar a engenheiro de infraestrutura para análise técnica aprofundada

