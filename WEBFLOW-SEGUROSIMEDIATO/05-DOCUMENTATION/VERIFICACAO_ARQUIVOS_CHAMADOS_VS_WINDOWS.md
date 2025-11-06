# 🔍 VERIFICAÇÃO DE ARQUIVOS CHAMADOS vs EXISTÊNCIA NO WINDOWS

**Data:** 06/11/2025  
**Análise:** Comparação entre arquivos chamados pelos arquivos DEV e sua existência nos diretórios Windows

---

## 📋 ARQUIVOS CHAMADOS POR FooterCodeSiteDefinitivoCompleto_dev.js

### **1. Arquivos .PHP**

#### **1.1 debug_logger_db.php**
- **URL Chamada:** `https://bpsegurosimediato.com.br/logging_system/debug_logger_db.php`
- **Diretório Servidor:** `/var/www/html/logging_system/`
- **Existência no Windows:** ❌ **NÃO EXISTE**
- **Observação:** Arquivo não está presente nos diretórios Windows (02-DEVELOPMENT ou 03-PRODUCTION)

#### **1.2 cpf-validate.php**
- **URL Chamada:** `https://mdmidia.com.br/cpf-validate.php`
- **Diretório Servidor:** Servidor externo (mdmidia.com.br)
- **Existência no Windows:** ❌ **NÃO EXISTE** (arquivo externo)
- **Observação:** Arquivo externo, não controlado por este projeto

#### **1.3 placa-validate.php**
- **URL Chamada:** `https://mdmidia.com.br/placa-validate.php`
- **Diretório Servidor:** Servidor externo (mdmidia.com.br)
- **Existência no Windows:** ❌ **NÃO EXISTE** (arquivo externo)
- **Observação:** Arquivo externo, não controlado por este projeto

---

### **2. Arquivos .JS**

#### **2.1 MODAL_WHATSAPP_DEFINITIVO_dev.js**
- **URL Chamada:** `https://dev.bpsegurosimediato.com.br/webhooks/MODAL_WHATSAPP_DEFINITIVO_dev.js`
- **Diretório Servidor:** `/var/www/html/dev/webhooks/MODAL_WHATSAPP_DEFINITIVO.js` (sem sufixo)
- **Existência no Windows:** ✅ **EXISTE**
- **Localização Windows:** `WEBFLOW-SEGUROSIMEDIATO/02-DEVELOPMENT/MODAL_WHATSAPP_DEFINITIVO_dev.js`
- **Status:** ✅ Arquivo existe e foi modificado no projeto iOS

#### **2.2 webflow_injection_limpo.js**
- **URL Chamada:** `https://mdmidia.com.br/webflow_injection_limpo.js`
- **Diretório Servidor:** Servidor externo (mdmidia.com.br)
- **Existência no Windows:** ❌ **NÃO EXISTE** (arquivo externo)
- **Observação:** Arquivo externo, não controlado por este projeto

---

## 📋 ARQUIVOS CHAMADOS POR MODAL_WHATSAPP_DEFINITIVO_dev.js

### **1. Arquivos .PHP**

#### **1.1 add_travelangels_dev.php (DEV)**
- **URL Chamada:** `https://bpsegurosimediato.com.br/dev/webhooks/add_travelangels_dev.php`
- **Diretório Servidor:** `/var/www/html/dev/webhooks/`
- **Existência no Windows:** ✅ **EXISTE**
- **Localização Windows:** `WEBFLOW-SEGUROSIMEDIATO/02-DEVELOPMENT/add_travelangels_dev.php`
- **Status:** ✅ Arquivo existe no diretório correto

#### **1.2 add_flyingdonkeys_v2.php (PROD)**
- **URL Chamada:** `https://bpsegurosimediato.com.br/webhooks/add_flyingdonkeys_v2.php`
- **Diretório Servidor:** `/var/www/html/webhooks/`
- **Existência no Windows:** ✅ **EXISTE** (com nome diferente)
- **Localização Windows:** `WEBFLOW-SEGUROSIMEDIATO/03-PRODUCTION/add_flyingdonkeys_prod.php`
- **Status:** ⚠️ **NOME DIFERENTE** - No Windows: `add_flyingdonkeys_prod.php`, no servidor: `add_flyingdonkeys_v2.php`

#### **1.3 add_webflow_octa_dev.php (DEV)**
- **URL Chamada:** `https://bpsegurosimediato.com.br/dev/webhooks/add_webflow_octa_dev.php`
- **Diretório Servidor:** `/var/www/html/dev/webhooks/`
- **Existência no Windows:** ✅ **EXISTE**
- **Localização Windows:** `WEBFLOW-SEGUROSIMEDIATO/02-DEVELOPMENT/add_webflow_octa_dev.php`
- **Status:** ✅ Arquivo existe no diretório correto

#### **1.4 add_webflow_octa_v2.php (PROD)**
- **URL Chamada:** `https://bpsegurosimediato.com.br/webhooks/add_webflow_octa_v2.php`
- **Diretório Servidor:** `/var/www/html/webhooks/`
- **Existência no Windows:** ✅ **EXISTE** (com nome diferente)
- **Localização Windows:** `WEBFLOW-SEGUROSIMEDIATO/03-PRODUCTION/add_webflow_octa_prod.php`
- **Status:** ⚠️ **NOME DIFERENTE** - No Windows: `add_webflow_octa_prod.php`, no servidor: `add_webflow_octa_v2.php`

#### **1.5 send_email_notification_endpoint_dev.php (DEV)**
- **URL Chamada:** `https://dev.bpsegurosimediato.com.br/webhooks/send_email_notification_endpoint_dev.php`
- **Diretório Servidor:** `/var/www/html/dev/webhooks/`
- **Existência no Windows:** ✅ **EXISTE** (com nome diferente)
- **Localização Windows:** `WEBFLOW-SEGUROSIMEDIATO/02-DEVELOPMENT/send_email_notification_endpoint.php`
- **Status:** ⚠️ **NOME DIFERENTE** - No Windows: `send_email_notification_endpoint.php` (sem `_dev`), no código: `send_email_notification_endpoint_dev.php`

#### **1.6 send_email_notification_endpoint_prod.php (PROD)**
- **URL Chamada:** `https://bpsegurosimediato.com.br/webhooks/send_email_notification_endpoint_prod.php`
- **Diretório Servidor:** `/var/www/html/webhooks/`
- **Existência no Windows:** ✅ **EXISTE**
- **Localização Windows:** `WEBFLOW-SEGUROSIMEDIATO/03-PRODUCTION/send_email_notification_endpoint_prod.php`
- **Status:** ✅ Arquivo existe no diretório correto

---

## 📊 RESUMO COMPARATIVO

### **Arquivos que EXISTEM no Windows:**

| Arquivo Chamado | Windows DEV | Windows PROD | Status |
|----------------|-------------|--------------|--------|
| **MODAL_WHATSAPP_DEFINITIVO_dev.js** | ✅ `02-DEVELOPMENT/MODAL_WHATSAPP_DEFINITIVO_dev.js` | - | ✅ OK |
| **add_travelangels_dev.php** | ✅ `02-DEVELOPMENT/add_travelangels_dev.php` | - | ✅ OK |
| **add_webflow_octa_dev.php** | ✅ `02-DEVELOPMENT/add_webflow_octa_dev.php` | - | ✅ OK |
| **add_flyingdonkeys_v2.php** | - | ✅ `03-PRODUCTION/add_flyingdonkeys_prod.php` | ⚠️ Nome diferente |
| **add_webflow_octa_v2.php** | - | ✅ `03-PRODUCTION/add_webflow_octa_prod.php` | ⚠️ Nome diferente |
| **send_email_notification_endpoint_dev.php** | ✅ `02-DEVELOPMENT/send_email_notification_endpoint.php` | - | ⚠️ Nome diferente |
| **send_email_notification_endpoint_prod.php** | - | ✅ `03-PRODUCTION/send_email_notification_endpoint_prod.php` | ✅ OK |

### **Arquivos que NÃO EXISTEM no Windows:**

| Arquivo Chamado | Motivo |
|----------------|--------|
| **debug_logger_db.php** | Arquivo não está presente nos diretórios Windows |
| **cpf-validate.php** | Arquivo externo (mdmidia.com.br) |
| **placa-validate.php** | Arquivo externo (mdmidia.com.br) |
| **webflow_injection_limpo.js** | Arquivo externo (mdmidia.com.br) |

---

## ⚠️ PROBLEMAS IDENTIFICADOS

### **1. Nomes Diferentes entre Código e Windows**

#### **1.1 send_email_notification_endpoint_dev.php**
- **Código chama:** `send_email_notification_endpoint_dev.php`
- **Windows tem:** `send_email_notification_endpoint.php` (sem `_dev`)
- **Impacto:** ⚠️ **CRÍTICO** - O código está chamando um arquivo que não existe no servidor com esse nome
- **Solução Necessária:** 
  - Opção 1: Renomear arquivo no Windows para `send_email_notification_endpoint_dev.php`
  - Opção 2: Atualizar código para chamar `send_email_notification_endpoint.php`

#### **1.2 add_flyingdonkeys_v2.php**
- **Código chama:** `add_flyingdonkeys_v2.php`
- **Windows tem:** `add_flyingdonkeys_prod.php`
- **Impacto:** ⚠️ **MÉDIO** - No servidor o arquivo pode ter nome `_v2`, mas no Windows está como `_prod`
- **Observação:** Isso é esperado devido à convenção de nomenclatura, mas pode causar confusão

#### **1.3 add_webflow_octa_v2.php**
- **Código chama:** `add_webflow_octa_v2.php`
- **Windows tem:** `add_webflow_octa_prod.php`
- **Impacto:** ⚠️ **MÉDIO** - No servidor o arquivo pode ter nome `_v2`, mas no Windows está como `_prod`
- **Observação:** Isso é esperado devido à convenção de nomenclatura, mas pode causar confusão

---

### **2. Arquivos Faltantes**

#### **2.1 debug_logger_db.php**
- **Status:** ❌ **NÃO EXISTE** no Windows
- **Impacto:** ⚠️ **BAIXO** - Arquivo está no servidor, não é necessário no Windows para desenvolvimento local
- **Observação:** Arquivo pode ser necessário apenas no servidor

---

## ✅ ARQUIVOS CORRETOS

### **Arquivos que estão corretos:**

1. ✅ `MODAL_WHATSAPP_DEFINITIVO_dev.js` - Existe em `02-DEVELOPMENT/`
2. ✅ `add_travelangels_dev.php` - Existe em `02-DEVELOPMENT/`
3. ✅ `add_webflow_octa_dev.php` - Existe em `02-DEVELOPMENT/`
4. ✅ `send_email_notification_endpoint_prod.php` - Existe em `03-PRODUCTION/`

---

## 🔧 AÇÕES RECOMENDADAS

### **CRÍTICO:**

1. **Corrigir nome do arquivo de email DEV:**
   - **Opção A:** Renomear `02-DEVELOPMENT/send_email_notification_endpoint.php` para `send_email_notification_endpoint_dev.php`
   - **Opção B:** Atualizar código `MODAL_WHATSAPP_DEFINITIVO_dev.js` linha ~731 para chamar `send_email_notification_endpoint.php` (sem `_dev`)

### **MÉDIO:**

2. **Verificar nomes dos arquivos no servidor:**
   - Confirmar se no servidor os arquivos PROD têm sufixo `_v2` ou `_prod`
   - Atualizar código se necessário para corresponder ao nome real no servidor

### **BAIXO:**

3. **Considerar adicionar debug_logger_db.php:**
   - Se necessário para desenvolvimento local, copiar do servidor para Windows

---

## 📊 ESTATÍSTICAS

- **Total de arquivos chamados:** 11
- **Arquivos que existem no Windows:** 7 (63.6%)
- **Arquivos externos (não controlados):** 3 (27.3%)
- **Arquivos faltantes:** 1 (9.1%)
- **Arquivos com nome diferente:** 3 (27.3%)

---

## 📝 OBSERVAÇÕES FINAIS

1. **Arquivos Externos:** 3 arquivos são externos (mdmidia.com.br) e não precisam estar no Windows
2. **Convenção de Nomenclatura:** Há diferença entre nomes no código e nomes no Windows devido à convenção `_dev` e `_prod`
3. **Arquivo Crítico:** `send_email_notification_endpoint_dev.php` precisa ser corrigido (nome diferente)
4. **Arquivos Modificados:** Os dois arquivos JavaScript principais (`FooterCodeSiteDefinitivoCompleto_dev.js` e `MODAL_WHATSAPP_DEFINITIVO_dev.js`) foram modificados no projeto iOS e existem no Windows

---

**Status:** ✅ Análise Completa  
**Última Atualização:** 06/11/2025 10:25

