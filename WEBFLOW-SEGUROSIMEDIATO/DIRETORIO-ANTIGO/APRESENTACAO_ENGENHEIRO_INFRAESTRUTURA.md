# 📋 APRESENTAÇÃO TÉCNICA PARA ENGENHEIRO DE SOFTWARE - INFRAESTRUTURA

## 🎯 PROBLEMA APRESENTADO

**Título**: Cache do Navegador/CDN Executando Versão Antiga de JavaScript  
**Severidade**: 🔴 CRÍTICA - Impede funcionamento do sistema em desenvolvimento  
**Data**: 2025-10-29

---

## 📊 RESUMO EXECUTIVO

Sistema JavaScript carregado dinamicamente via `<script src>` está sendo executado em versão antiga pelo navegador, mesmo após atualização no servidor e uso de versionamento (`?v=16`). 

**Impacto**: Sistema não consegue se comunicar com backend devido a URL incorreta sendo chamada.

---

## 🔍 FATO 1: CÓDIGO NO SERVIDOR ESTÁ CORRETO

**Arquivo**: `/var/www/html/dev/webhooks/MODAL_WHATSAPP_DEFINITIVO.js`  
**MD5 Hash**: `c60433b6c911360913e15e5b62c3f5b8`  
**Verificação**: Hash local idêntico ao do servidor ✅

**Código relevante (linha 145)**:
```javascript
dev: 'https://bpsegurosimediato.com.br/dev/webhooks/add_travelangels_dev.php',
```

✅ **Confirmação**: Servidor tem código correto.

---

## 🔍 FATO 2: NAVEGADOR EXECUTA VERSÃO ANTIGA

**Console do navegador mostra**:
```javascript
🌍 [MODAL] Ambiente: DEV | Endpoint travelangels: https://bpsegurosimediato.com.br/dev/webhooks/add_travelangels.php
```

**URL chamada**: `add_travelangels.php` (sem `_dev`)  
**URL esperada**: `add_travelangels_dev.php` (com `_dev`)

❌ **Confirmação**: Navegador está executando código antigo que retorna URL sem `_dev`.

---

## 🔍 FATO 3: VERSIONAMENTO PRESENTE MAS INEFICAZ

**Código de carregamento**:
```javascript
script.src = 'https://dev.bpsegurosimediato.com.br/webhooks/MODAL_WHATSAPP_DEFINITIVO.js?v=16';
```

**Problema**: Parâmetro `?v=16` não está forçando recarregamento do arquivo.

---

## 🏗️ ARQUITETURA ATUAL

```
┌─────────────────────────────────────────────────────────┐
│ CLOUDFLARE CDN                                          │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ Cache Rule: Bypass para /webhooks/*.js             │ │
│ │ Status: ✅ Configurada                              │ │
│ └─────────────────────────────────────────────────────┘ │
└──────────────┬──────────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────────┐
│ SERVIDOR ORIGIN (bpsegurosimediato.com.br)             │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ /dev/webhooks/MODAL_WHATSAPP_DEFINITIVO.js        │ │
│ │ MD5: c60433b6c911360913e15e5b62c3f5b8             │ │
│ │ Conteúdo: ✅ CORRETO                                │ │
│ └─────────────────────────────────────────────────────┘ │
└──────────────┬──────────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────────┐
│ NAVEGADOR (Chrome/Edge)                                 │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ Executando: Versão ANTIGA (sem _dev) ❌            │ │
│ │ Cache: Browser Cache / Service Worker?             │ │
│ └─────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

---

## ❓ QUESTIONAMENTOS TÉCNICOS PARA INFRAESTRUTURA

### **1. Gestão de Cache - Cloudflare**

**Pergunta**: A regra de bypass configurada está realmente funcionando?

**Contexto**:
- Regra configurada: `*://dev.bpsegurosimediato.com.br/webhooks/*.js` → Bypass cache
- Status: ✅ Ativa no painel Cloudflare

**Verificação necessária**:
- Como confirmar que Cloudflare está respeitando a regra?
- Há logs no Cloudflare Analytics que mostram cache hits/misses?
- Devo adicionar headers HTTP (`Cache-Control: no-cache`) como redundância?

---

### **2. Headers HTTP do Arquivo JavaScript**

**Pergunta**: Quais headers HTTP o servidor está enviando para o arquivo `.js`?

**Verificação necessária**:
```bash
curl -I https://dev.bpsegurosimediato.com.br/webhooks/MODAL_WHATSAPP_DEFINITIVO.js?v=16
```

**Headers críticos a verificar**:
- `Cache-Control`: Deve ser `no-cache, no-store, must-revalidate`?
- `ETag`: Como está sendo gerado? Pode estar causando cache?
- `Last-Modified`: Data está atualizada?
- `CF-Cache-Status`: Cloudflare está cacheando?

---

### **3. Versionamento de Assets - Melhor Prática**

**Pergunta**: Qual estratégia de versionamento é mais eficaz?

**Opções**:
1. **Timestamp**: `?v=1696000000000` (muda sempre)
2. **Version Number**: `?v=16` (manual, precisa incrementar)
3. **Content Hash**: `?v=c60433b6c911360913e15e5b62c3f5b8` (baseado em MD5)

**Recomendação técnica esperada**:
- Qual oferece melhor balance entre cache busting e performance?
- Devemos usar ambos (hash no filename + query param)?

---

### **4. Service Workers no Webflow**

**Pergunta**: O Webflow pode ter Service Worker cacheando assets externos?

**Verificação necessária**:
- Como detectar se há Service Worker ativo?
- Service Workers podem cachear assets de outros domínios (`dev.bpsegurosimediato.com.br`)?
- Como limpar programaticamente?

---

### **5. Estratégia de Deploy para Assets Estáticos**

**Pergunta**: Devo renomear o arquivo ao invés de usar query param?

**Opções**:
- `MODAL_WHATSAPP_DEFINITIVO.js` → `MODAL_WHATSAPP_DEFINITIVO.v17.js`
- Vantagem: Força download novo sempre
- Desvantagem: Precisa atualizar referência no código

**Recomendação técnica esperada**: Qual abordagem é mais robusta em ambientes com múltiplas camadas de cache?

---

### **6. Monitoramento de Versão em Runtime**

**Pergunta**: Devo implementar check de versão no próprio JavaScript?

**Proposta**:
```javascript
// No início do MODAL_WHATSAPP_DEFINITIVO.js
const EXPECTED_VERSION = '17';
const CURRENT_VERSION = '16'; // Hardcoded no arquivo

if (CURRENT_VERSION !== EXPECTED_VERSION) {
    console.error('❌ [VERSION MISMATCH] Arquivo desatualizado!');
    // Forçar reload?
}
```

**Recomendação técnica esperada**: Esta é uma boa prática ou há overhead desnecessário?

---

### **7. Configuração de Cache no Servidor Web**

**Pergunta**: Apache/Nginx pode estar enviando headers de cache incorretos?

**⚠️ DESCOBERTA CRÍTICA - Headers HTTP da Resposta**:

```http
HTTP/2 200
cache-control: public, max-age=2592000, immutable
expires: Fri, 28 Nov 2025 19:50:33 GMT
cf-cache-status: MISS
```

**ANÁLISE**:
- ❌ **`Cache-Control: immutable`** é o problema principal!
- Navegadores modernos (Chrome, Edge) **IGNORAM query params** (`?v=16`) quando o header `immutable` está presente
- `max-age=2592000` = 30 dias de cache
- A regra Cloudflare de bypass pode não estar funcionando porque o header `immutable` tem precedência

**Solução necessária**: Remover `immutable` ou configurar header diferente para arquivos em `/dev/webhooks/*.js`

**Verificação necessária**:
- Onde está sendo setado o header `immutable`? (Servidor web, Cloudflare Transform Rules, ou origin?)
- Devo adicionar regra específica para `/dev/webhooks/*.js` removendo `immutable`?
- Como configurar `Cache-Control: no-cache` apenas para desenvolvimento?

---

## 📁 INFORMAÇÕES TÉCNICAS COMPLETAS

### **Ambiente**

**Servidor**: `root@46.62.174.150`  
**Stack**: PHP, Apache/Nginx (a confirmar), Cloudflare CDN  
**Frontend**: Webflow (static site)  
**Backend**: PHP endpoints em subdiretório `/dev/webhooks/`

### **Arquivos Relevantes**

| Arquivo | Localização | MD5 Hash | Status |
|---------|-------------|----------|--------|
| `MODAL_WHATSAPP_DEFINITIVO.js` | Servidor: `/var/www/html/dev/webhooks/` | `c60433b6c911360913e15e5b62c3f5b8` | ✅ Correto |
| `MODAL_WHATSAPP_DEFINITIVO.js` | Local: `./MODAL_WHATSAPP_DEFINITIVO.js` | `c60433b6c911360913e5b62c3f5b8` | ✅ Idêntico |
| `Footer Code Site Definitivo.js` | Webflow Custom Code | N/A | Carrega modal |

### **Endpoints**

| Endpoint | URL Correta | URL Sendo Chamada | Status |
|----------|-------------|-------------------|--------|
| TravelAngels DEV | `/dev/webhooks/add_travelangels_dev.php` | `/dev/webhooks/add_travelangels.php` ❌ | Erro CORS + 500 |
| OctaDesk DEV | `/dev/webhooks/add_webflow_octa_dev.php` | `/dev/webhooks/add_webflow_octa.php` ❌ | Funciona (tem CORS?) |

---

## 🎯 CONCLUSÃO E SOLICITAÇÃO

**Diagnóstico**: Cache do navegador ou CDN está servindo versão antiga do JavaScript, mesmo com:
- ✅ Código correto no servidor
- ✅ Versionamento presente (`?v=16`)
- ✅ Regra Cloudflare configurada

**Solicitação ao Engenheiro de Infraestrutura**:

1. **Validar configuração de cache em todas as camadas** (Cloudflare, servidor web, browser)
2. **Recomendar estratégia robusta de versionamento** que funcione com múltiplas camadas de cache
3. **Implementar headers HTTP apropriados** para desenvolvimento (no-cache)
4. **Criar processo de deploy** que garanta invalidação de cache
5. **Configurar monitoramento** para detectar quando navegador usa versão desatualizada

---

**Documento criado em**: 2025-10-29  
**Contato para esclarecimentos**: Consultar logs em `02-DEVELOPMENT/DIAGNOSTICO_PROBLEMA_ENDPOINT_WRONG.md`

