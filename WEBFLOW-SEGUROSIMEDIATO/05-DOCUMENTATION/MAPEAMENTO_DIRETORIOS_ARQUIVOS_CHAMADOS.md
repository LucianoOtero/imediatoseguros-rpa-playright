# 📍 MAPEAMENTO DETALHADO: DIRETÓRIOS DOS ARQUIVOS CHAMADOS E INJETADOS

**Data:** 06/11/2025  
**Análise:** Mapeamento completo de URLs para diretórios do servidor

---

## 🎯 RESUMO EXECUTIVO

Este documento mapeia **exatamente** cada arquivo .php ou .js chamado/injetado pelos arquivos JavaScript, identificando:
- URL completa usada no código
- Diretório exato no servidor onde o arquivo está localizado
- Domínio/servidor onde está hospedado
- Ambiente (DEV/PROD)

---

## 📁 ARQUIVOS CHAMADOS POR FooterCodeSiteDefinitivoCompleto_dev.js

### **1. Sistema de Logging**

**URL no Código:**
```
https://bpsegurosimediato.com.br/logging_system/debug_logger_db.php
```

**Diretório no Servidor:**
```
/var/www/html/logging_system/debug_logger_db.php
```

**Domínio:** `bpsegurosimediato.com.br`  
**Ambiente:** PRODUÇÃO (mesmo para DEV e PROD)  
**Linha no Código:** ~1129

---

### **2. Validação de CPF (Proxy Externo)**

**URL no Código:**
```
https://mdmidia.com.br/cpf-validate.php
```

**Diretório no Servidor:**
```
[Servidor externo: mdmidia.com.br]
/var/www/html/cpf-validate.php (presumido)
```

**Domínio:** `mdmidia.com.br` (servidor externo)  
**Ambiente:** EXTERNO  
**Linha no Código:** ~639

---

### **3. Validação de Placa (Proxy Externo)**

**URL no Código:**
```
https://mdmidia.com.br/placa-validate.php
```

**Diretório no Servidor:**
```
[Servidor externo: mdmidia.com.br]
/var/www/html/placa-validate.php (presumido)
```

**Domínio:** `mdmidia.com.br` (servidor externo)  
**Ambiente:** EXTERNO  
**Linha no Código:** ~698

---

### **4. Script RPA (Injeção Dinâmica)**

**URL no Código:**
```
https://mdmidia.com.br/webflow_injection_limpo.js
```

**Diretório no Servidor:**
```
[Servidor externo: mdmidia.com.br]
/var/www/html/webflow_injection_limpo.js (presumido)
```

**Domínio:** `mdmidia.com.br` (servidor externo)  
**Ambiente:** EXTERNO  
**Linha no Código:** ~1232  
**Tipo:** Injeção dinâmica via `<script>` tag

---

### **5. Modal WhatsApp (Injeção Dinâmica)**

**URL no Código:**
```
https://dev.bpsegurosimediato.com.br/webhooks/MODAL_WHATSAPP_DEFINITIVO_dev.js?v=24&force=[RANDOM]
```

**Diretório no Servidor:**
```
/var/www/html/dev/webhooks/MODAL_WHATSAPP_DEFINITIVO.js
```

**Domínio:** `dev.bpsegurosimediato.com.br`  
**Ambiente:** DESENVOLVIMENTO  
**Linha no Código:** ~1295  
**Tipo:** Injeção dinâmica via `<script>` tag  
**⚠️ NOTA:** No servidor, o arquivo não tem sufixo `_dev`, apenas está no diretório `/dev/webhooks/`

---

## 📁 ARQUIVOS CHAMADOS POR MODAL_WHATSAPP_DEFINITIVO_dev.js

### **1. EspoCRM - FlyingDonkeys (DEV)**

**URL no Código:**
```
https://bpsegurosimediato.com.br/dev/webhooks/add_travelangels_dev.php
```

**Diretório no Servidor:**
```
/var/www/html/dev/webhooks/add_travelangels_dev.php
```

**Domínio:** `bpsegurosimediato.com.br`  
**Ambiente:** DESENVOLVIMENTO  
**Linha no Código:** ~160, ~173  
**Função:** `getEndpointUrl('travelangels')` quando `isDev === true`  
**Quando é chamado:**
- Quando `isDevelopmentEnvironment() === true`
- OU quando hostname contém `webflow.io`

---

### **2. EspoCRM - FlyingDonkeys (PROD)**

**URL no Código:**
```
https://bpsegurosimediato.com.br/webhooks/add_flyingdonkeys_v2.php
```

**Diretório no Servidor:**
```
/var/www/html/webhooks/add_flyingdonkeys_v2.php
```

**Domínio:** `bpsegurosimediato.com.br`  
**Ambiente:** PRODUÇÃO  
**Linha no Código:** ~174  
**Função:** `getEndpointUrl('travelangels')` quando `isDev === false`  
**Quando é chamado:** Quando `isDevelopmentEnvironment() === false`

---

### **3. OctaDesk - WhatsApp (DEV)**

**URL no Código:**
```
https://bpsegurosimediato.com.br/dev/webhooks/add_webflow_octa_dev.php
```

**Diretório no Servidor:**
```
/var/www/html/dev/webhooks/add_webflow_octa_dev.php
```

**Domínio:** `bpsegurosimediato.com.br`  
**Ambiente:** DESENVOLVIMENTO  
**Linha no Código:** ~161, ~177  
**Função:** `getEndpointUrl('octadesk')` quando `isDev === true`  
**Quando é chamado:**
- Quando `isDevelopmentEnvironment() === true`
- OU quando hostname contém `webflow.io`

---

### **4. OctaDesk - WhatsApp (PROD)**

**URL no Código:**
```
https://bpsegurosimediato.com.br/webhooks/add_webflow_octa_v2.php
```

**Diretório no Servidor:**
```
/var/www/html/webhooks/add_webflow_octa_v2.php
```

**Domínio:** `bpsegurosimediato.com.br`  
**Ambiente:** PRODUÇÃO  
**Linha no Código:** ~178  
**Função:** `getEndpointUrl('octadesk')` quando `isDev === false`  
**Quando é chamado:** Quando `isDevelopmentEnvironment() === false`

---

### **5. Notificação Email (DEV)**

**URL no Código:**
```
https://dev.bpsegurosimediato.com.br/webhooks/send_email_notification_endpoint_dev.php
```

**Diretório no Servidor:**
```
/var/www/html/dev/webhooks/send_email_notification_endpoint_dev.php
```

**Domínio:** `dev.bpsegurosimediato.com.br`  
**Ambiente:** DESENVOLVIMENTO  
**Linha no Código:** ~731  
**Função:** `sendAdminEmailNotification()` quando `isDev === true`  
**Quando é chamado:** Quando `isDevelopmentEnvironment() === true`

---

### **6. Notificação Email (PROD)**

**URL no Código:**
```
https://bpsegurosimediato.com.br/webhooks/send_email_notification_endpoint_prod.php
```

**Diretório no Servidor:**
```
/var/www/html/webhooks/send_email_notification_endpoint_prod.php
```

**Domínio:** `bpsegurosimediato.com.br`  
**Ambiente:** PRODUÇÃO  
**Linha no Código:** ~732  
**Função:** `sendAdminEmailNotification()` quando `isDev === false`  
**Quando é chamado:** Quando `isDevelopmentEnvironment() === false`

---

## 📊 MAPEAMENTO POR DIRETÓRIO DO SERVIDOR

### **Servidor: bpsegurosimediato.com.br (46.62.174.150)**

#### **Diretório: `/var/www/html/logging_system/`**
```
/var/www/html/logging_system/
└── debug_logger_db.php                    ← Chamado por FooterCode (DEV e PROD)
```

#### **Diretório: `/var/www/html/dev/webhooks/`**
```
/var/www/html/dev/webhooks/
├── MODAL_WHATSAPP_DEFINITIVO.js          ← Injetado por FooterCode (DEV)
├── add_travelangels_dev.php               ← Chamado por Modal (DEV)
├── add_webflow_octa_dev.php              ← Chamado por Modal (DEV)
└── send_email_notification_endpoint_dev.php ← Chamado por Modal (DEV)
```

#### **Diretório: `/var/www/html/webhooks/`**
```
/var/www/html/webhooks/
├── add_flyingdonkeys_v2.php               ← Chamado por Modal (PROD)
├── add_webflow_octa_v2.php               ← Chamado por Modal (PROD)
└── send_email_notification_endpoint_prod.php ← Chamado por Modal (PROD)
```

---

### **Servidor: mdmidia.com.br (Servidor Externo)**

#### **Diretório: `/var/www/html/` (presumido)**
```
/var/www/html/
├── cpf-validate.php                       ← Chamado por FooterCode (validação CPF)
├── placa-validate.php                     ← Chamado por FooterCode (validação Placa)
└── webflow_injection_limpo.js            ← Injetado por FooterCode (RPA)
```

---

## 🔄 MAPEAMENTO POR AMBIENTE

### **AMBIENTE DEV**

**Arquivos Chamados:**
1. `/var/www/html/logging_system/debug_logger_db.php` (bpsegurosimediato.com.br)
2. `/var/www/html/dev/webhooks/add_travelangels_dev.php` (bpsegurosimediato.com.br)
3. `/var/www/html/dev/webhooks/add_webflow_octa_dev.php` (bpsegurosimediato.com.br)
4. `/var/www/html/dev/webhooks/send_email_notification_endpoint_dev.php` (dev.bpsegurosimediato.com.br)
5. `mdmidia.com.br/cpf-validate.php` (servidor externo)
6. `mdmidia.com.br/placa-validate.php` (servidor externo)

**Arquivos Injetados:**
1. `/var/www/html/dev/webhooks/MODAL_WHATSAPP_DEFINITIVO.js` (dev.bpsegurosimediato.com.br)
2. `mdmidia.com.br/webflow_injection_limpo.js` (servidor externo)

---

### **AMBIENTE PROD**

**Arquivos Chamados:**
1. `/var/www/html/logging_system/debug_logger_db.php` (bpsegurosimediato.com.br)
2. `/var/www/html/webhooks/add_flyingdonkeys_v2.php` (bpsegurosimediato.com.br)
3. `/var/www/html/webhooks/add_webflow_octa_v2.php` (bpsegurosimediato.com.br)
4. `/var/www/html/webhooks/send_email_notification_endpoint_prod.php` (bpsegurosimediato.com.br)
5. `mdmidia.com.br/cpf-validate.php` (servidor externo)
6. `mdmidia.com.br/placa-validate.php` (servidor externo)

**Arquivos Injetados:**
1. `/var/www/html/webhooks/MODAL_WHATSAPP_DEFINITIVO.js` (bpsegurosimediato.com.br) ⚠️ **VERIFICAR**
2. `mdmidia.com.br/webflow_injection_limpo.js` (servidor externo)

---

## 📋 TABELA RESUMO

| Arquivo | URL no Código | Diretório Servidor | Domínio | Ambiente | Tipo |
|---------|--------------|-------------------|---------|----------|------|
| **debug_logger_db.php** | `bpsegurosimediato.com.br/logging_system/...` | `/var/www/html/logging_system/` | bpsegurosimediato.com.br | PROD | Chamado |
| **cpf-validate.php** | `mdmidia.com.br/cpf-validate.php` | `/var/www/html/` (externo) | mdmidia.com.br | EXTERNO | Chamado |
| **placa-validate.php** | `mdmidia.com.br/placa-validate.php` | `/var/www/html/` (externo) | mdmidia.com.br | EXTERNO | Chamado |
| **webflow_injection_limpo.js** | `mdmidia.com.br/webflow_injection_limpo.js` | `/var/www/html/` (externo) | mdmidia.com.br | EXTERNO | Injetado |
| **MODAL_WHATSAPP_DEFINITIVO.js (DEV)** | `dev.bpsegurosimediato.com.br/webhooks/...` | `/var/www/html/dev/webhooks/` | dev.bpsegurosimediato.com.br | DEV | Injetado |
| **add_travelangels_dev.php** | `bpsegurosimediato.com.br/dev/webhooks/...` | `/var/www/html/dev/webhooks/` | bpsegurosimediato.com.br | DEV | Chamado |
| **add_webflow_octa_dev.php** | `bpsegurosimediato.com.br/dev/webhooks/...` | `/var/www/html/dev/webhooks/` | bpsegurosimediato.com.br | DEV | Chamado |
| **send_email_notification_endpoint_dev.php** | `dev.bpsegurosimediato.com.br/webhooks/...` | `/var/www/html/dev/webhooks/` | dev.bpsegurosimediato.com.br | DEV | Chamado |
| **add_flyingdonkeys_v2.php** | `bpsegurosimediato.com.br/webhooks/...` | `/var/www/html/webhooks/` | bpsegurosimediato.com.br | PROD | Chamado |
| **add_webflow_octa_v2.php** | `bpsegurosimediato.com.br/webhooks/...` | `/var/www/html/webhooks/` | bpsegurosimediato.com.br | PROD | Chamado |
| **send_email_notification_endpoint_prod.php** | `bpsegurosimediato.com.br/webhooks/...` | `/var/www/html/webhooks/` | bpsegurosimediato.com.br | PROD | Chamado |

---

## ⚠️ OBSERVAÇÕES IMPORTANTES

### **1. Convenção de Nomenclatura no Servidor:**

**DEV:**
- Arquivos PHP: mantêm sufixo `_dev` no nome (ex: `add_travelangels_dev.php`)
- Arquivos JS: **NÃO** têm sufixo, diferenciados pelo diretório `/dev/webhooks/`

**PROD:**
- Arquivos PHP: podem ter sufixo `_v2` ou `_prod` (ex: `add_flyingdonkeys_v2.php`)
- Arquivos JS: **NÃO** têm sufixo, diferenciados pelo diretório `/webhooks/`

### **2. Diferença entre Domínios:**

- `bpsegurosimediato.com.br` → Servidor principal (ambos DEV e PROD)
- `dev.bpsegurosimediato.com.br` → Subdomínio DEV (apenas DEV)
- `mdmidia.com.br` → Servidor externo (validações e RPA)

### **3. Diretórios Especiais:**

- `/var/www/html/logging_system/` → Sistema de logging (compartilhado entre DEV e PROD)
- `/var/www/html/dev/webhooks/` → Webhooks de desenvolvimento
- `/var/www/html/webhooks/` → Webhooks de produção

### **4. Arquivos Externos:**

- `mdmidia.com.br` → Servidor externo, não controlado por este projeto
- Arquivos neste servidor são proxies/APIs externas

---

## 🔍 VERIFICAÇÕES NECESSÁRIAS

### **1. Modal WhatsApp em PROD:**
- ⚠️ **VERIFICAR:** O arquivo `MODAL_WHATSAPP_DEFINITIVO.js` existe em `/var/www/html/webhooks/`?
- ⚠️ **VERIFICAR:** O FooterCode PROD está carregando do diretório correto?

### **2. Endpoint de Email em PROD:**
- ⚠️ **VERIFICAR:** O arquivo `send_email_notification_endpoint_prod.php` existe em `/var/www/html/webhooks/`?
- ⚠️ **VERIFICAR:** Nome correto no servidor (pode ser `send_email_notification_endpoint.php` sem sufixo)

### **3. Nginx Configuration:**
- ⚠️ **VERIFICAR:** Nginx permite acesso HTTP a `/var/www/html/webhooks/`?
- ⚠️ **VERIFICAR:** Nginx permite acesso HTTP a `/var/www/html/dev/webhooks/`?

---

**Status:** ✅ Mapeamento Completo  
**Última Atualização:** 06/11/2025 10:20

