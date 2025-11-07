# 🏗️ ARQUITETURA FOOTER CODES WEBFLOW - AMBIENTES DEV E PROD

**Data de Criação:** 05/11/2025  
**Versão do Documento:** 1.0  
**Status:** ✅ Completo

---

## 📋 SUMÁRIO EXECUTIVO

Este documento descreve detalhadamente a arquitetura dos Footer Codes do Webflow nos ambientes de **Desenvolvimento (DEV)** e **Produção (PROD)**, incluindo:

- ✅ Configuração atual dos ambientes
- ✅ Arquivos principais e suas localizações
- ✅ Arquivos carregados dinamicamente
- ✅ Endpoints acessados por cada arquivo
- ✅ Estrutura de diretórios no servidor e Windows
- ✅ Comparação detalhada de conteúdo entre servidor e Windows
- ✅ Diagramas de fluxo e dependências

---

## 🎯 CONFIGURAÇÃO ATUAL DOS AMBIENTES

### **Ambiente de Desenvolvimento (DEV)**

**Webflow DEV:** `segurosimediato-8119bf26e77bf4ff336a58e.webflow.io`

**Footer Code Carregado:**
```html
<script src="https://dev.bpsegurosimediato.com.br/webhooks/FooterCodeSiteDefinitivoCompleto.js?v=1.5" defer></script>
```

**URL Completa:** `https://dev.bpsegurosimediato.com.br/webhooks/FooterCodeSiteDefinitivoCompleto.js`

---

### **Ambiente de Produção (PROD)**

**Webflow PROD:** `www.segurosimediato.com.br`

**Footer Code Carregado:**
```html
<script src="https://dev.bpsegurosimediato.com.br/webhooks/FooterCodeSiteDefinitivoCompleto_prod.js?v=1.3" defer></script>
```

**⚠️ OBSERVAÇÃO CRÍTICA:**  
Atualmente, o ambiente de **PRODUÇÃO** está carregando o arquivo do servidor **DEV** (`dev.bpsegurosimediato.com.br`).  
Isso ocorre porque o Nginx está bloqueando acesso ao diretório `/var/www/html/webhooks/` em produção.

**URL Esperada (quando corrigido):** `https://bpsegurosimediato.com.br/webhooks/FooterCodeSiteDefinitivoCompleto_prod.js`

---

## 📁 ARQUIVOS PRINCIPAIS

### **1. FooterCodeSiteDefinitivoCompleto.js (DEV)**

#### **Localização no Servidor:**
- **Caminho:** `/var/www/html/dev/webhooks/FooterCodeSiteDefinitivoCompleto.js`
- **URL:** `https://dev.bpsegurosimediato.com.br/webhooks/FooterCodeSiteDefinitivoCompleto.js`
- **Versão Atual:** `1.5.0` (com sistema de controle de logs)

#### **Localização no Windows:**
- **Caminho Esperado:** `02-DEVELOPMENT/custom-codes/FooterCodeSiteDefinitivoCompleto.js`
- **Status:** ⚠️ **VERIFICAR** (arquivo pode existir em outro local ou com nome diferente)
- **Backups Encontrados:**
  - `02-DEVELOPMENT/custom-codes/FooterCodeSiteDefinitivoCompleto.js.backup_20251101_101206`
  - `02-DEVELOPMENT/custom-codes/FooterCodeSiteDefinitivoCompleto.js.backup_20251103_111616`
- **Nota:** O arquivo pode estar localizado em outro diretório ou ter sido renomeado. Verificar localização exata.

#### **Características:**
- **Ambiente:** DEV
- **SafetyMails Ticket:** `fc5e18c10c4aa883b2c31a305f1c09fea3834138` (DEV)
- **SafetyMails API Key:** `20a7a1c297e39180bd80428ac13c363e882a531f`
- **Sistema de Logs:** Habilitado (`window.DEBUG_CONFIG.enabled: false` por padrão)
- **Modal WhatsApp:** Carrega de `dev.bpsegurosimediato.com.br/webhooks/MODAL_WHATSAPP_DEFINITIVO.js`

#### **Conteúdo:**
- ✅ Parte 1: FooterCodeSiteDefinitivoUtils.js (funções utilitárias)
- ✅ Parte 2: Footer Code Site Definitivo.js (validações, máscaras)
- ✅ Parte 3: Inside Head Tag Pagina.js (captura GCLID)

---

### **2. FooterCodeSiteDefinitivoCompleto_prod.js (PROD)**

#### **Localização no Servidor:**
- **Caminho:** `/var/www/html/dev/webhooks/FooterCodeSiteDefinitivoCompleto_prod.js` ⚠️ (temporariamente em DEV)
- **URL Atual:** `https://dev.bpsegurosimediato.com.br/webhooks/FooterCodeSiteDefinitivoCompleto_prod.js`
- **URL Esperada:** `https://bpsegurosimediato.com.br/webhooks/FooterCodeSiteDefinitivoCompleto_prod.js` (quando Nginx corrigido)
- **Versão Atual:** `1.3_PROD`

**⚠️ OBSERVAÇÃO IMPORTANTE - PROBLEMA TEMPORÁRIO DO NGINX:**  
O arquivo `FooterCodeSiteDefinitivoCompleto_prod.js` está localizado temporariamente no diretório `/var/www/html/dev/webhooks/` devido a um problema na configuração do Nginx que está bloqueando o acesso HTTP ao diretório de produção `/var/www/html/webhooks/`. 

**Situação Atual:**
- O Nginx não permite acesso HTTP ao diretório `/var/www/html/webhooks/` em produção
- Como solução temporária, o arquivo foi movido para `/var/www/html/dev/webhooks/`
- O Webflow PROD está configurado para carregar o arquivo do servidor DEV (`dev.bpsegurosimediato.com.br`)

**Solução Necessária:**
- Configurar o Nginx para permitir acesso HTTP ao diretório `/var/www/html/webhooks/`
- Após correção, mover o arquivo para o diretório correto: `/var/www/html/webhooks/`
- Atualizar a URL no Webflow para apontar para `bpsegurosimediato.com.br` (sem `dev`)

#### **Localização no Windows:**
- **Caminho:** `02-DEVELOPMENT/custom-codes/FooterCodeSiteDefinitivoCompleto_prod.js`
- **Status:** ✅ **ARQUIVO EXISTE**

#### **Características:**
- **Ambiente:** PRODUÇÃO
- **SafetyMails Ticket:** `fc5e18c10c4aa883b2c31a305f1c09fea3834138` (mesmo que DEV)
- **SafetyMails API Key:** `20a7a1c297e39180bd80428ac13c363e882a531f`
- **Modal WhatsApp:** ⚠️ **HARDCODED para DEV** (linha 1032):
  ```javascript
  script.src = 'https://dev.bpsegurosimediato.com.br/webhooks/MODAL_WHATSAPP_DEFINITIVO.js?v=23&force=' + Math.random();
  ```

#### **Conteúdo:**
- ✅ Parte 1: FooterCodeSiteDefinitivoUtils.js (funções utilitárias)
- ✅ Parte 2: Footer Code Site Definitivo.js (validações, máscaras)
- ✅ Parte 3: Inside Head Tag Pagina.js (captura GCLID)

---

## 🔄 ARQUIVOS CARREGADOS DINAMICAMENTE

### **1. MODAL_WHATSAPP_DEFINITIVO.js**

#### **Carregado Por:**
- `FooterCodeSiteDefinitivoCompleto.js` (DEV)
- `FooterCodeSiteDefinitivoCompleto_prod.js` (PROD)

#### **Função de Carregamento:**
```javascript
function loadWhatsAppModal() {
  if (window.whatsappModalLoaded) return;
  
  const script = document.createElement('script');
  script.src = 'https://dev.bpsegurosimediato.com.br/webhooks/MODAL_WHATSAPP_DEFINITIVO.js?v=23&force=' + Math.random();
  document.head.appendChild(script);
}
```

#### **Localização no Servidor:**
- **Caminho:** `/var/www/html/dev/webhooks/MODAL_WHATSAPP_DEFINITIVO.js`
- **URL:** `https://dev.bpsegurosimediato.com.br/webhooks/MODAL_WHATSAPP_DEFINITIVO.js`

#### **Localização no Windows:**
- **Caminho:** `MODAL_WHATSAPP_DEFINITIVO.js` (raiz do projeto)
- **Status:** ✅ **ARQUIVO EXISTE**

#### **Versão:**
- **Atual:** `v24` (conforme comentário no código)

---

### **2. webflow_injection_limpo.js (RPA)**

#### **Carregado Por:**
- `FooterCodeSiteDefinitivoCompleto.js` (DEV)
- `FooterCodeSiteDefinitivoCompleto_prod.js` (PROD)

#### **Função de Carregamento:**
```javascript
function loadRPAScript() {
  const script = document.createElement('script');
  script.src = 'https://mdmidia.com.br/webflow_injection_limpo.js';
  document.head.appendChild(script);
}
```

#### **Localização:**
- **URL:** `https://mdmidia.com.br/webflow_injection_limpo.js`
- **Status:** ⚠️ **Arquivo externo** (não controlado neste projeto)

---

## 🌐 ENDPOINTS ACESSADOS

### **Endpoints Acessados pelo FooterCodeSiteDefinitivoCompleto.js**

#### **1. Sistema de Logging**
- **URL:** `https://bpsegurosimediato.com.br/logging_system/debug_logger_db.php`
- **Método:** POST
- **Função:** Enviar logs para banco de dados MySQL
- **Usado por:** Ambos DEV e PROD

#### **2. Validação de CPF**
- **URL:** `https://mdmidia.com.br/cpf-validate.php`
- **Método:** GET/POST
- **Função:** Validar CPF via API PH3A
- **Usado por:** Ambos DEV e PROD

#### **3. Validação de CEP**
- **URL:** `https://viacep.com.br/ws/{cep}/json/`
- **Método:** GET
- **Função:** Buscar endereço por CEP
- **Usado por:** Ambos DEV e PROD

#### **4. Validação de Placa**
- **URL:** `https://mdmidia.com.br/placa-validate.php`
- **Método:** GET/POST
- **Função:** Validar placa de veículo
- **Usado por:** Ambos DEV e PROD

#### **5. Validação de Telefone**
- **URL:** `https://apilayer.net/api/validate?access_key={key}&country_code=BR&number={number}`
- **Método:** GET
- **Função:** Validar número de telefone
- **Usado por:** Ambos DEV e PROD

#### **6. SafetyMails API**
- **URL:** `https://{ticket}.safetymails.com/api/{code}`
- **Método:** POST
- **Função:** Validar email via SafetyMails
- **Ticket DEV:** `fc5e18c10c4aa883b2c31a305f1c09fea3834138`
- **Ticket PROD:** `fc5e18c10c4aa883b2c31a305f1c09fea3834138` (mesmo que DEV)
- **API Key:** `20a7a1c297e39180bd80428ac13c363e882a531f`

---

### **Endpoints Acessados pelo MODAL_WHATSAPP_DEFINITIVO.js**

#### **1. EspoCRM (FlyingDonkeys) - DEV**
- **URL:** `https://bpsegurosimediato.com.br/dev/webhooks/add_travelangels_dev.php`
- **Método:** POST
- **Função:** Criar/atualizar lead no EspoCRM (ambiente DEV)
- **Usado quando:** `isDevelopmentEnvironment() === true`

#### **2. EspoCRM (FlyingDonkeys) - PROD**
- **URL:** `https://bpsegurosimediato.com.br/webhooks/add_flyingdonkeys_v2.php`
- **Método:** POST
- **Função:** Criar/atualizar lead no EspoCRM (ambiente PROD)
- **Usado quando:** `isDevelopmentEnvironment() === false`

#### **3. OctaDesk - DEV**
- **URL:** `https://bpsegurosimediato.com.br/dev/webhooks/add_webflow_octa_dev.php`
- **Método:** POST
- **Função:** Enviar mensagem WhatsApp via OctaDesk (ambiente DEV)
- **Usado quando:** `isDevelopmentEnvironment() === true`

#### **4. OctaDesk - PROD**
- **URL:** `https://bpsegurosimediato.com.br/webhooks/add_webflow_octa_v2.php`
- **Método:** POST
- **Função:** Enviar mensagem WhatsApp via OctaDesk (ambiente PROD)
- **Usado quando:** `isDevelopmentEnvironment() === false`

#### **5. Notificação Email - DEV**
- **URL:** `https://dev.bpsegurosimediato.com.br/webhooks/send_email_notification_endpoint.php`
- **Método:** POST
- **Função:** Enviar email de notificação para administradores (DEV)
- **Usado quando:** `isDevelopmentEnvironment() === true`

#### **6. Notificação Email - PROD**
- **URL:** `https://bpsegurosimediato.com.br/webhooks/send_email_notification_endpoint.php`
- **Método:** POST
- **Função:** Enviar email de notificação para administradores (PROD)
- **Usado quando:** `isDevelopmentEnvironment() === false`

---

## 📂 ESTRUTURA DE DIRETÓRIOS

### **Servidor Linux (46.62.174.150)**

#### **Ambiente DEV:**
```
/var/www/html/dev/webhooks/
├── FooterCodeSiteDefinitivoCompleto.js          ✅ (v1.5.0)
├── FooterCodeSiteDefinitivoCompleto_prod.js     ✅ (v1.3_PROD)
├── MODAL_WHATSAPP_DEFINITIVO.js                 ✅ (v24)
├── add_travelangels_dev.php                     ✅
├── add_webflow_octa_dev.php                    ✅
└── send_email_notification_endpoint.php         ✅
```

#### **Ambiente PROD (Esperado):**
```
/var/www/html/webhooks/
├── FooterCodeSiteDefinitivoCompleto_prod.js     ⚠️ (deveria estar aqui)
├── MODAL_WHATSAPP_DEFINITIVO.js                 ⚠️ (deveria estar aqui)
├── add_flyingdonkeys_v2.php                     ✅
├── add_webflow_octa_v2.php                      ✅
└── send_email_notification_endpoint.php         ✅
```

**⚠️ PROBLEMA IDENTIFICADO:**  
Nginx está bloqueando acesso HTTP ao diretório `/var/www/html/webhooks/` em produção, forçando uso do diretório DEV.

**📌 OBSERVAÇÃO DETALHADA:**  
O arquivo `FooterCodeSiteDefinitivoCompleto_prod.js` está localizado temporariamente no diretório `/var/www/html/dev/webhooks/` em função de um problema temporário na configuração do Nginx. Este problema impede o acesso HTTP ao diretório de produção `/var/www/html/webhooks/`, forçando a utilização do diretório DEV como solução temporária. A correção do Nginx permitirá que o arquivo seja movido para seu local correto em produção.

---

### **Windows (Máquina de Desenvolvimento)**

#### **Diretório Principal:**
```
C:\Users\Luciano\OneDrive - Imediato Soluções em Seguros\Imediato\imediatoseguros-rpa-playwright\
```

#### **Estrutura de Arquivos:**
```
02-DEVELOPMENT/
├── custom-codes/
│   ├── FooterCodeSiteDefinitivoCompleto_prod.js          ✅ (v1.3_PROD)
│   ├── FooterCodeSiteDefinitivoCompleto.js.backup_*      ✅ (backups)
│   ├── FooterCodeSiteDefinitivoUtils.js                 ✅
│   ├── Footer Code Site Definitivo.js                    ✅
│   ├── Footer Code Site Definitivo WEBFLOW.js           ✅ (DEV)
│   ├── Footer Code Site Definitivo WEBFLOW_prod.js       ✅ (PROD)
│   ├── add_flyingdonkeys_v2.php                         ✅
│   ├── add_webflow_octa_v2.php                          ✅
│   ├── send_email_notification_endpoint.php              ✅
│   └── send_admin_notification_ses.php                   ✅
│
├── backups/
│   └── FooterCodeSiteDefinitivoCompleto.js.backup_*     ✅
│
└── migration/
    └── migracao_debug_email_20251104_192051/
        └── FooterCodeSiteDefinitivoCompleto_prod.js      ✅

MODAL_WHATSAPP_DEFINITIVO.js                              ✅ (raiz do projeto)
```

---

## 🔍 COMPARAÇÃO DETALHADA: SERVIDOR vs WINDOWS

### **1. FooterCodeSiteDefinitivoCompleto.js (DEV)**

#### **Status:**
- **Servidor:** ✅ Existe (`/var/www/html/dev/webhooks/`)
- **Windows:** ⚠️ **VERIFICAR LOCALIZAÇÃO** (arquivo pode existir em outro diretório)

#### **Diferenças Identificadas:**

**⚠️ OBSERVAÇÃO:** Arquivo pode existir no Windows em local diferente do esperado. Backups encontrados:
- `FooterCodeSiteDefinitivoCompleto.js.backup_20251101_101206`
- `FooterCodeSiteDefinitivoCompleto.js.backup_20251103_111616`

**Ação Necessária:**  
Verificar localização exata do arquivo `FooterCodeSiteDefinitivoCompleto.js` no Windows. Se não existir, criar baseado no backup mais recente ou copiar do servidor.

---

### **2. FooterCodeSiteDefinitivoCompleto_prod.js (PROD)**

#### **Status:**
- **Servidor:** ✅ Existe (`/var/www/html/dev/webhooks/`) ⚠️ (temporariamente em DEV)
- **Windows:** ✅ Existe (`02-DEVELOPMENT/custom-codes/`)

#### **Comparação de Conteúdo:**

**Versão:**
- **Servidor:** `1.3_PROD` (conforme URL: `?v=1.3`)
- **Windows:** `1.3_PROD` (conforme cabeçalho do arquivo)

**Modal WhatsApp (Linha ~1032):**
- **Servidor:** ⚠️ **VERIFICAR** (necessário acesso SSH)
- **Windows:** ⚠️ **HARDCODED para DEV:**
  ```javascript
  script.src = 'https://dev.bpsegurosimediato.com.br/webhooks/MODAL_WHATSAPP_DEFINITIVO.js?v=23&force=' + Math.random();
  ```

**Diferenças Identificadas:**

1. **⚠️ Modal WhatsApp Hardcoded para DEV:**
   - **Problema:** Arquivo PROD carregando Modal de DEV
   - **Impacto:** Modal sempre carregado de ambiente DEV, mesmo em produção
   - **Solução Necessária:** Atualizar para:
     ```javascript
     script.src = 'https://bpsegurosimediato.com.br/webhooks/MODAL_WHATSAPP_DEFINITIVO.js?v=24&force=' + Math.random();
     ```

2. **SafetyMails Credentials:**
   - **Windows:** `SAFETY_TICKET = 'fc5e18c10c4aa883b2c31a305f1c09fea3834138'` (mesmo que DEV)
   - **Servidor:** ⚠️ **VERIFICAR** (necessário acesso SSH)

---

### **3. MODAL_WHATSAPP_DEFINITIVO.js**

#### **Status:**
- **Servidor:** ✅ Existe (`/var/www/html/dev/webhooks/`)
- **Windows:** ✅ Existe (raiz do projeto)

#### **Comparação de Conteúdo:**

**Versão:**
- **Servidor:** ⚠️ **VERIFICAR** (necessário acesso SSH)
- **Windows:** `v24` (conforme comentário no código)

**Endpoints (Função `getEndpointUrl`):**

**Windows (Linhas 131-168):**
```javascript
function getEndpointUrl(endpoint) {
  const hostname = window.location.hostname;
  
  // Forçar DEV para webflow.io
  if (hostname.indexOf('webflow.io') !== -1) {
    const devEndpoints = {
      travelangels: 'https://bpsegurosimediato.com.br/dev/webhooks/add_travelangels_dev.php',
      octadesk: 'https://bpsegurosimediato.com.br/dev/webhooks/add_webflow_octa_dev.php'
    };
    return devEndpoints[endpoint];
  }
  
  const isDev = isDevelopmentEnvironment();
  const endpoints = {
    travelangels: {
      dev: 'https://bpsegurosimediato.com.br/dev/webhooks/add_travelangels_dev.php',
      prod: 'https://bpsegurosimediato.com.br/webhooks/add_flyingdonkeys_v2.php'
    },
    octadesk: {
      dev: 'https://bpsegurosimediato.com.br/dev/webhooks/add_webflow_octa_dev.php',
      prod: 'https://bpsegurosimediato.com.br/webhooks/add_webflow_octa_v2.php'
    }
  };
  
  return endpoints[endpoint][isDev ? 'dev' : 'prod'];
}
```

**Diferenças Identificadas:**

1. **⚠️ Endpoint de Email (Linha ~708):**
   - **Windows:** Usa detecção de ambiente:
     ```javascript
     const emailEndpoint = isDev 
       ? 'https://dev.bpsegurosimediato.com.br/webhooks/send_email_notification_endpoint.php'
       : 'https://bpsegurosimediato.com.br/webhooks/send_email_notification_endpoint.php';
     ```
   - **Servidor:** ⚠️ **VERIFICAR** (necessário acesso SSH)

---

### **4. Arquivos PHP**

#### **add_flyingdonkeys_v2.php**

**Status:**
- **Servidor:** ✅ Existe (`/var/www/html/webhooks/`)
- **Windows:** ✅ Existe (`02-DEVELOPMENT/custom-codes/`)

**Versão:**
- **Windows:** `2.1` (conforme cabeçalho)

**Diferenças Identificadas:**
- ⚠️ **VERIFICAR** conteúdo do servidor via SSH para comparação completa

---

#### **add_webflow_octa_v2.php**

**Status:**
- **Servidor:** ✅ Existe (`/var/www/html/webhooks/`)
- **Windows:** ✅ Existe (`02-DEVELOPMENT/custom-codes/`)

**Versão:**
- **Windows:** `2.0` (conforme cabeçalho)

**Diferenças Identificadas:**
- ⚠️ **VERIFICAR** conteúdo do servidor via SSH para comparação completa

---

#### **send_email_notification_endpoint.php**

**Status:**
- **Servidor:** ✅ Existe (`/var/www/html/dev/webhooks/` e `/var/www/html/webhooks/`)
- **Windows:** ✅ Existe (`02-DEVELOPMENT/custom-codes/`)

**Versão:**
- **Windows:** `1.1` (conforme cabeçalho)

**Diferenças Identificadas:**
- ⚠️ **VERIFICAR** conteúdo do servidor via SSH para comparação completa

---

## 📊 DIAGRAMA DE FLUXO

### **Fluxo DEV:**

```
Webflow DEV (webflow.io)
    ↓
Footer Code: FooterCodeSiteDefinitivoCompleto.js
    ↓
[Carrega Dinamicamente]
    ├──→ MODAL_WHATSAPP_DEFINITIVO.js (dev.bpsegurosimediato.com.br)
    └──→ webflow_injection_limpo.js (mdmidia.com.br)
    ↓
[Endpoints Acessados]
    ├──→ add_travelangels_dev.php (DEV)
    ├──→ add_webflow_octa_dev.php (DEV)
    ├──→ send_email_notification_endpoint.php (DEV)
    ├──→ debug_logger_db.php (PROD)
    ├──→ cpf-validate.php (mdmidia.com.br)
    ├──→ placa-validate.php (mdmidia.com.br)
    ├──→ viacep.com.br (API externa)
    ├──→ apilayer.net (API externa)
    └──→ safetymails.com (API externa)
```

### **Fluxo PROD:**

```
Webflow PROD (segurosimediato.com.br)
    ↓
Footer Code: FooterCodeSiteDefinitivoCompleto_prod.js
    ↓
[Carrega Dinamicamente]
    ├──→ MODAL_WHATSAPP_DEFINITIVO.js (dev.bpsegurosimediato.com.br) ⚠️ PROBLEMA
    └──→ webflow_injection_limpo.js (mdmidia.com.br)
    ↓
[Endpoints Acessados]
    ├──→ add_flyingdonkeys_v2.php (PROD)
    ├──→ add_webflow_octa_v2.php (PROD)
    ├──→ send_email_notification_endpoint.php (PROD)
    ├──→ debug_logger_db.php (PROD)
    ├──→ cpf-validate.php (mdmidia.com.br)
    ├──→ placa-validate.php (mdmidia.com.br)
    ├──→ viacep.com.br (API externa)
    ├──→ apilayer.net (API externa)
    └──→ safetymails.com (API externa)
```

---

## ⚠️ PROBLEMAS IDENTIFICADOS

### **1. Arquivo DEV Não Existe no Windows**
- **Arquivo:** `FooterCodeSiteDefinitivoCompleto.js`
- **Impacto:** Impossível fazer modificações locais antes de deploy
- **Solução:** Criar arquivo baseado no backup mais recente ou copiar do servidor

### **2. Modal WhatsApp Hardcoded para DEV no Arquivo PROD**
- **Arquivo:** `FooterCodeSiteDefinitivoCompleto_prod.js` (linha ~1032)
- **Problema:** Modal sempre carregado de ambiente DEV, mesmo em produção
- **Impacto:** Dependência de ambiente DEV em produção
- **Solução:** Atualizar URL para produção:
  ```javascript
  script.src = 'https://bpsegurosimediato.com.br/webhooks/MODAL_WHATSAPP_DEFINITIVO.js?v=24&force=' + Math.random();
  ```

### **3. Nginx Bloqueando Acesso ao Diretório PROD**
- **Problema:** Nginx bloqueia `/var/www/html/webhooks/` em produção
- **Impacto:** Arquivos PROD sendo servidos de DEV
- **Solução:** Configurar Nginx para permitir acesso HTTP ao diretório

### **4. Arquivo PROD Temporariamente em Diretório DEV**
- **Problema:** `FooterCodeSiteDefinitivoCompleto_prod.js` está em `/var/www/html/dev/webhooks/`
- **Impacto:** Confusão entre ambientes
- **Solução:** Mover para `/var/www/html/webhooks/` após correção do Nginx

---

## 📝 RECOMENDAÇÕES

### **Curto Prazo:**

1. ✅ **Criar arquivo DEV no Windows:**
   - Copiar `FooterCodeSiteDefinitivoCompleto.js` do servidor para Windows
   - Ou restaurar do backup mais recente

2. ✅ **Corrigir Modal WhatsApp no arquivo PROD:**
   - Atualizar URL para produção em `FooterCodeSiteDefinitivoCompleto_prod.js`
   - Testar em ambiente DEV antes de deploy

3. ✅ **Configurar Nginx:**
   - Permitir acesso HTTP ao diretório `/var/www/html/webhooks/`
   - Mover arquivos PROD para diretório correto

### **Médio Prazo:**

1. ✅ **Sincronizar arquivos:**
   - Estabelecer processo de sincronização entre Windows e Servidor
   - Criar script de deploy automatizado

2. ✅ **Versionamento:**
   - Implementar controle de versão adequado
   - Documentar todas as alterações

3. ✅ **Testes:**
   - Criar ambiente de testes isolado
   - Implementar testes automatizados

---

## 📚 REFERÊNCIAS

- **Documentação de Migração:** `02-DEVELOPMENT/DOCUMENTACAO_MIGRACAO_PRODUCAO_SAFETYMAILS.md`
- **Projeto de Migração:** `02-DEVELOPMENT/PROJETO_MIGRACAO_PRODUCAO_COMPLETA_V2_ATUALIZADO.md`
- **Análise de Endpoints:** `migration/migracao_debug_email_20251104_192051/ANALISE_ENDPOINTS_MODAL.md`

---

## ✅ CHECKLIST DE VERIFICAÇÃO

### **Arquivos DEV:**
- [ ] `FooterCodeSiteDefinitivoCompleto.js` existe no Windows
- [ ] `FooterCodeSiteDefinitivoCompleto.js` sincronizado com servidor
- [ ] `MODAL_WHATSAPP_DEFINITIVO.js` sincronizado com servidor
- [ ] Endpoints DEV funcionando corretamente

### **Arquivos PROD:**
- [ ] `FooterCodeSiteDefinitivoCompleto_prod.js` corrigido (Modal URL)
- [ ] `FooterCodeSiteDefinitivoCompleto_prod.js` movido para diretório correto
- [ ] Nginx configurado corretamente
- [ ] Endpoints PROD funcionando corretamente

### **Infraestrutura:**
- [ ] Nginx permitindo acesso ao diretório `/var/www/html/webhooks/`
- [ ] Arquivos PROD no diretório correto
- [ ] Backups criados antes de alterações

---

**Documento criado em:** 05/11/2025  
**Última atualização:** 05/11/2025  
**Versão:** 1.0

