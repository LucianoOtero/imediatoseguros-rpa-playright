# 🚀 PROJETO: MIGRAÇÃO PARA PRODUÇÃO - CORREÇÕES iOS MODAL E ERRO EMAIL

**Data de Criação:** 06/11/2025  
**Versão:** 1.0  
**Status:** 📋 Planejado - Aguardando Execução  
**Projetos Origem:** 
- PROJETO_CORRECAO_MODAL_IOS_NOVA_ABA.md (v1.7.0)
- PROJETO_CORRECAO_ERRO_EMAIL_SUBMISSAO_COMPLETA.md (v1.8.0)

---

## 📋 SUMÁRIO EXECUTIVO

Este projeto detalha o processo completo de migração para produção das correções implementadas nos dois projetos mais recentes:

1. **Correção Modal iOS** (v1.7.0): Correção do problema do modal abrindo como nova aba em dispositivos iOS
2. **Correção Erro Email** (v1.8.0): Correção da mensagem "❌ ERRO NO ENVIO: Erro desconhecido" no envio de email

**⚠️ CONTEXTO CRÍTICO:**
- Os arquivos JavaScript estão atualmente hospedados no mesmo diretório de DEV (`/var/www/html/dev/webhooks/`)
- Os endpoints PHP precisam ter sufixo `_prod` para produção
- Todas as modificações devem seguir as diretivas: **SEMPRE DEV PRIMEIRO, DEPOIS PROD**

---

## 📁 ARQUIVOS MODIFICADOS NOS PROJETOS

### **PROJETO 1: CORREÇÃO MODAL iOS (v1.7.0)**

#### **Arquivos Modificados:**

1. **`FooterCodeSiteDefinitivoCompleto_dev.js`**
   - **Localização DEV:** `WEBFLOW-SEGUROSIMEDIATO/02-DEVELOPMENT/FooterCodeSiteDefinitivoCompleto_dev.js`
   - **Localização Servidor DEV:** `/var/www/html/dev/webhooks/FooterCodeSiteDefinitivoCompleto_dev.js`
   - **Modificações:**
     - ✅ Função `isIOS()` melhorada (inclui iPad iOS 13+)
     - ✅ Flag de controle `modalOpening` para prevenir dupla execução
     - ✅ Função unificada `openWhatsAppModal()`
     - ✅ Verificação de suporte a `passive` listeners
     - ✅ Handler `touchstart` para iOS (com `passive: false`)
     - ✅ Handler `click` melhorado com prevenção de dupla execução
   - **Versão:** V25

2. **`MODAL_WHATSAPP_DEFINITIVO_dev.js`**
   - **Localização DEV:** `WEBFLOW-SEGUROSIMEDIATO/02-DEVELOPMENT/MODAL_WHATSAPP_DEFINITIVO_dev.js`
   - **Localização Servidor DEV:** `/var/www/html/dev/webhooks/MODAL_WHATSAPP_DEFINITIVO_dev.js`
   - **Modificações:**
     - ✅ Handler duplicado removido/comentado (linha ~2253)
     - ✅ Documentação atualizada
   - **Versão:** V25

### **PROJETO 2: CORREÇÃO ERRO EMAIL (v1.8.0)**

#### **Arquivos Modificados:**

1. **`MODAL_WHATSAPP_DEFINITIVO_dev.js`**
   - **Localização DEV:** `WEBFLOW-SEGUROSIMEDIATO/02-DEVELOPMENT/MODAL_WHATSAPP_DEFINITIVO_dev.js`
   - **Localização Servidor DEV:** `/var/www/html/dev/webhooks/MODAL_WHATSAPP_DEFINITIVO_dev.js`
   - **Modificações:**
     - ✅ Lógica de detecção de erro corrigida em `sendAdminEmailNotification()`
     - ✅ Suporte para estrutura real do endpoint (`status: 'success'` string)
     - ✅ Verificação de `responseData.data.leadIdFlyingDonkeys`
     - ✅ Verificação de `responseData.data.opportunityIdFlyingDonkeys`
     - ✅ Compatibilidade com estruturas antigas mantida
   - **Versão:** V26

2. **`send_email_notification_endpoint_dev.php`**
   - **Localização DEV:** `WEBFLOW-SEGUROSIMEDIATO/02-DEVELOPMENT/send_email_notification_endpoint_dev.php`
   - **Localização Servidor DEV:** `/var/www/html/dev/webhooks/send_email_notification_endpoint_dev.php`
   - **Status:** Arquivo existe e está sendo usado

---

## 🎯 OBJETIVOS DA MIGRAÇÃO

1. ✅ Migrar arquivos JavaScript corrigidos para produção
2. ✅ Garantir que endpoints PHP tenham sufixo `_prod` em produção
3. ✅ Atualizar URLs nos arquivos JavaScript para apontar para endpoints `_prod`
4. ✅ Manter ambiente DEV funcionando durante migração
5. ✅ Validar funcionamento completo em produção

---

## 📊 ESTADO ATUAL

### **Servidor Atual (Legado)**
- **IP:** 46.62.174.150
- **DEV:** `/var/www/html/dev/webhooks/`
- **PROD:** `/var/www/html/webhooks/` (bloqueado pelo Nginx)
- **Situação:** Arquivos PROD sendo servidos de DEV temporariamente

### **Arquivos em DEV (Windows)**
- ✅ `FooterCodeSiteDefinitivoCompleto_dev.js` (com correções iOS)
- ✅ `MODAL_WHATSAPP_DEFINITIVO_dev.js` (com correções iOS + Email)
- ✅ `send_email_notification_endpoint_dev.php`

### **Arquivos em PROD (Windows)**
- ⚠️ `FooterCodeSiteDefinitivoCompleto_prod.js` (precisa receber correções)
- ⚠️ `MODAL_WHATSAPP_DEFINITIVO_prod.js` (precisa receber correções)
- ✅ `send_email_notification_endpoint_prod.php` (já existe)

---

## 🔧 FASES DO PROJETO

### **FASE 1: PREPARAÇÃO E VERIFICAÇÃO**

**Objetivo:** Garantir que temos tudo necessário antes de iniciar

#### **1.1 Verificar Arquivos DEV no Servidor**

```bash
# Conectar no servidor DEV
ssh root@46.62.174.150

# Verificar arquivos DEV existentes
ls -lh /var/www/html/dev/webhooks/FooterCodeSiteDefinitivoCompleto_dev.js
ls -lh /var/www/html/dev/webhooks/MODAL_WHATSAPP_DEFINITIVO_dev.js
ls -lh /var/www/html/dev/webhooks/send_email_notification_endpoint_dev.php

# Verificar versões nos arquivos
grep -i "VERSÃO\|VERSION\|V25\|V26" /var/www/html/dev/webhooks/FooterCodeSiteDefinitivoCompleto_dev.js | head -5
grep -i "VERSÃO\|VERSION\|V25\|V26" /var/www/html/dev/webhooks/MODAL_WHATSAPP_DEFINITIVO_dev.js | head -5
```

#### **1.2 Verificar Arquivos PROD no Servidor**

```bash
# Verificar se diretório PROD existe e está acessível
ls -lh /var/www/html/webhooks/ 2>&1

# Verificar arquivos PROD existentes (se acessíveis)
ls -lh /var/www/html/webhooks/FooterCodeSiteDefinitivoCompleto_prod.js 2>&1
ls -lh /var/www/html/webhooks/MODAL_WHATSAPP_DEFINITIVO_prod.js 2>&1
ls -lh /var/www/html/webhooks/send_email_notification_endpoint_prod.php 2>&1
```

#### **1.3 Criar Backups de Produção**

```bash
# No servidor
ssh root@46.62.174.150

# Criar diretório de backup com timestamp
BACKUP_DIR="/root/backup_migracao_producao_$(date +%Y%m%d_%H%M%S)"
mkdir -p $BACKUP_DIR

# Backup arquivos PROD (se existirem)
if [ -f "/var/www/html/webhooks/FooterCodeSiteDefinitivoCompleto_prod.js" ]; then
  cp /var/www/html/webhooks/FooterCodeSiteDefinitivoCompleto_prod.js $BACKUP_DIR/
fi

if [ -f "/var/www/html/webhooks/MODAL_WHATSAPP_DEFINITIVO_prod.js" ]; then
  cp /var/www/html/webhooks/MODAL_WHATSAPP_DEFINITIVO_prod.js $BACKUP_DIR/
fi

if [ -f "/var/www/html/webhooks/send_email_notification_endpoint_prod.php" ]; then
  cp /var/www/html/webhooks/send_email_notification_endpoint_prod.php $BACKUP_DIR/
fi

# Backup arquivos DEV (como referência)
cp /var/www/html/dev/webhooks/FooterCodeSiteDefinitivoCompleto_dev.js $BACKUP_DIR/FooterCodeSiteDefinitivoCompleto_dev.js.backup
cp /var/www/html/dev/webhooks/MODAL_WHATSAPP_DEFINITIVO_dev.js $BACKUP_DIR/MODAL_WHATSAPP_DEFINITIVO_dev.js.backup
cp /var/www/html/dev/webhooks/send_email_notification_endpoint_dev.php $BACKUP_DIR/send_email_notification_endpoint_dev.php.backup

# Verificar backups criados
ls -lh $BACKUP_DIR/
```

---

### **FASE 2: BACKUP E PREPARAR ARQUIVOS PROD LOCAIS**

**Objetivo:** Criar backups dos arquivos PROD atuais e depois criar versões PROD dos arquivos JavaScript com URLs corretas

#### **2.1 Criar Backups dos Arquivos PROD Atuais (Windows)**

**⚠️ CRÍTICO:** Sempre fazer backup ANTES de qualquer modificação!

```powershell
# No Windows
cd "C:\Users\Luciano\OneDrive - Imediato Soluções em Seguros\Imediato\imediatoseguros-rpa-playwright"

# Criar diretório de backup com timestamp
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$backupDir = "WEBFLOW-SEGUROSIMEDIATO\04-BACKUPS\MIGRACAO_PRODUCAO_$timestamp"
New-Item -ItemType Directory -Path $backupDir -Force | Out-Null

# Backup arquivos JavaScript PROD (se existirem)
if (Test-Path "WEBFLOW-SEGUROSIMEDIATO\03-PRODUCTION\FooterCodeSiteDefinitivoCompleto_prod.js") {
    Copy-Item "WEBFLOW-SEGUROSIMEDIATO\03-PRODUCTION\FooterCodeSiteDefinitivoCompleto_prod.js" `
              "$backupDir\FooterCodeSiteDefinitivoCompleto_prod.js.backup" -Force
    Write-Host "✅ Backup FooterCode PROD criado" -ForegroundColor Green
}

if (Test-Path "WEBFLOW-SEGUROSIMEDIATO\03-PRODUCTION\MODAL_WHATSAPP_DEFINITIVO_prod.js") {
    Copy-Item "WEBFLOW-SEGUROSIMEDIATO\03-PRODUCTION\MODAL_WHATSAPP_DEFINITIVO_prod.js" `
              "$backupDir\MODAL_WHATSAPP_DEFINITIVO_prod.js.backup" -Force
    Write-Host "✅ Backup Modal PROD criado" -ForegroundColor Green
}

# Backup arquivos PHP PROD (se existirem)
if (Test-Path "WEBFLOW-SEGUROSIMEDIATO\03-PRODUCTION\send_email_notification_endpoint_prod.php") {
    Copy-Item "WEBFLOW-SEGUROSIMEDIATO\03-PRODUCTION\send_email_notification_endpoint_prod.php" `
              "$backupDir\send_email_notification_endpoint_prod.php.backup" -Force
    Write-Host "✅ Backup Email Endpoint PROD criado" -ForegroundColor Green
}

if (Test-Path "WEBFLOW-SEGUROSIMEDIATO\03-PRODUCTION\add_flyingdonkeys_prod.php") {
    Copy-Item "WEBFLOW-SEGUROSIMEDIATO\03-PRODUCTION\add_flyingdonkeys_prod.php" `
              "$backupDir\add_flyingdonkeys_prod.php.backup" -Force
    Write-Host "✅ Backup FlyingDonkeys PROD criado" -ForegroundColor Green
}

if (Test-Path "WEBFLOW-SEGUROSIMEDIATO\03-PRODUCTION\add_webflow_octa_prod.php") {
    Copy-Item "WEBFLOW-SEGUROSIMEDIATO\03-PRODUCTION\add_webflow_octa_prod.php" `
              "$backupDir\add_webflow_octa_prod.php.backup" -Force
    Write-Host "✅ Backup Octadesk PROD criado" -ForegroundColor Green
}

# Verificar backups criados
Write-Host "`n📋 Backups criados em: $backupDir" -ForegroundColor Cyan
Get-ChildItem $backupDir | Format-Table Name, Length, LastWriteTime -AutoSize
```

#### **2.2 Copiar Arquivos DEV para PROD (Windows)**

```powershell
# No Windows
cd "C:\Users\Luciano\OneDrive - Imediato Soluções em Seguros\Imediato\imediatoseguros-rpa-playwright"

# Copiar FooterCode DEV para PROD
Copy-Item "WEBFLOW-SEGUROSIMEDIATO\02-DEVELOPMENT\FooterCodeSiteDefinitivoCompleto_dev.js" `
          "WEBFLOW-SEGUROSIMEDIATO\03-PRODUCTION\FooterCodeSiteDefinitivoCompleto_prod.js" -Force

# Copiar Modal DEV para PROD
Copy-Item "WEBFLOW-SEGUROSIMEDIATO\02-DEVELOPMENT\MODAL_WHATSAPP_DEFINITIVO_dev.js" `
          "WEBFLOW-SEGUROSIMEDIATO\03-PRODUCTION\MODAL_WHATSAPP_DEFINITIVO_prod.js" -Force
```

#### **2.2 Atualizar URLs no FooterCode PROD**

**Arquivo:** `WEBFLOW-SEGUROSIMEDIATO/03-PRODUCTION/FooterCodeSiteDefinitivoCompleto_prod.js`

**Modificações Necessárias:**

1. **Atualizar cabeçalho (linha ~1-60):**
   ```javascript
   /**
    * PROJETO: UNIFICAÇÃO DE ARQUIVOS FOOTER CODE + CORREÇÕES iOS MODAL
    * INÍCIO: 30/10/2025 19:55
    * ÚLTIMA ALTERAÇÃO: 06/11/2025 [HH:MM]
    * 
    * VERSÃO: 1.6.0 - Correções iOS Modal + Sistema de Controle de Logs
    * 
    * ALTERAÇÕES VERSÃO 1.6.0:
    * - ✅ Correção modal abrindo como nova aba em iOS (V25)
    * - ✅ Implementada detecção iOS melhorada (inclui iPad iOS 13+)
    * - ✅ Adicionada flag de controle para prevenir dupla execução
    * - ✅ Implementado handler touchstart para iOS
    * - ✅ Melhorado handler click com prevenção de dupla execução
    * 
    * Localização: https://bpsegurosimediato.com.br/webhooks/FooterCodeSiteDefinitivoCompleto_prod.js
    * 
    * ⚠️ AMBIENTE: PRODUÇÃO
    * - SafetyMails Ticket: 9bab7f0c2711c5accfb83588c859dc1103844a94
    * - SafetyMails API Key: 20a7a1c297e39180bd80428ac13c363e882a531f
    */
   ```

2. **Atualizar URL do Modal (linha ~1261):**
   ```javascript
   // ANTES (DEV):
   script.src = 'https://dev.bpsegurosimediato.com.br/webhooks/MODAL_WHATSAPP_DEFINITIVO_dev.js?v=24&force=' + Math.random();
   
   // DEPOIS (PROD):
   script.src = 'https://bpsegurosimediato.com.br/webhooks/MODAL_WHATSAPP_DEFINITIVO_prod.js?v=26&force=' + Math.random();
   ```

3. **Atualizar log (linha ~1259):**
   ```javascript
   // ANTES:
   window.logInfo('MODAL', '🔄 Carregando modal de dev.bpsegurosimediato.com.br...');
   
   // DEPOIS:
   window.logInfo('MODAL', '🔄 Carregando modal de bpsegurosimediato.com.br...');
   ```

#### **2.3 Atualizar URLs no Modal PROD**

**Arquivo:** `WEBFLOW-SEGUROSIMEDIATO/03-PRODUCTION/MODAL_WHATSAPP_DEFINITIVO_prod.js`

**Modificações Necessárias:**

1. **Atualizar cabeçalho (linha ~1-30):**
   ```javascript
   /**
    * PROJETO: CORREÇÃO MODAL ABRINDO COMO NOVA ABA NO iOS + CORREÇÃO DETECÇÃO DE ERRO EMAIL
    * INÍCIO: 05/11/2025 01:00
    * ÚLTIMA ALTERAÇÃO: 06/11/2025 [HH:MM]
    * 
    * VERSÃO: V26 - Correção Detecção de Erro Email (Submissão Completa) + Correção iOS Modal
    * 
    * ALTERAÇÕES NESTA VERSÃO (V26):
    * - Corrigida lógica de detecção de erro em sendAdminEmailNotification
    * - Suporte para estrutura real do endpoint (status: 'success' string)
    * - Verificação de responseData.data.leadIdFlyingDonkeys
    * - Verificação de responseData.data.opportunityIdFlyingDonkeys
    * - Mantida compatibilidade com estruturas antigas
    * 
    * ALTERAÇÕES VERSÃO ANTERIOR (V25):
    * - Removido handler duplicado de abertura do modal
    * - Lógica centralizada no FooterCodeSiteDefinitivoCompleto_prod.js
    * 
    * ⚠️ AMBIENTE: PRODUÇÃO
    */
   ```

2. **Atualizar URL do endpoint de email (linha ~708-710):**
   ```javascript
   // ANTES (DEV):
   const emailEndpoint = isDev 
     ? 'https://dev.bpsegurosimediato.com.br/webhooks/send_email_notification_endpoint_dev.php'
     : 'https://bpsegurosimediato.com.br/webhooks/send_email_notification_endpoint.php';
   
   // DEPOIS (PROD):
   const emailEndpoint = isDev 
     ? 'https://dev.bpsegurosimediato.com.br/webhooks/send_email_notification_endpoint_dev.php'
     : 'https://bpsegurosimediato.com.br/webhooks/send_email_notification_endpoint_prod.php';
   ```

3. **Atualizar URLs dos endpoints EspoCRM e Octadesk (linha ~149-157):**
   ```javascript
   // ANTES (DEV - usando _v2.php):
   const endpoints = {
     travelangels: {
       dev: 'https://bpsegurosimediato.com.br/dev/webhooks/add_travelangels_dev.php',
       prod: 'https://bpsegurosimediato.com.br/webhooks/add_flyingdonkeys_v2.php' // ✅ V2: Endpoint paralelo
     },
     octadesk: {
       dev: 'https://bpsegurosimediato.com.br/dev/webhooks/add_webflow_octa_dev.php',
       prod: 'https://bpsegurosimediato.com.br/webhooks/add_webflow_octa_v2.php' // ✅ V2: Endpoint paralelo
     }
   };
   
   // DEPOIS (PROD - usando _prod.php):
   const endpoints = {
     travelangels: {
       dev: 'https://bpsegurosimediato.com.br/dev/webhooks/add_travelangels_dev.php',
       prod: 'https://bpsegurosimediato.com.br/webhooks/add_flyingdonkeys_prod.php' // ✅ PROD: Endpoint com sufixo _prod
     },
     octadesk: {
       dev: 'https://bpsegurosimediato.com.br/dev/webhooks/add_webflow_octa_dev.php',
       prod: 'https://bpsegurosimediato.com.br/webhooks/add_webflow_octa_prod.php' // ✅ PROD: Endpoint com sufixo _prod
     }
   };
   ```

3. **Atualizar lógica de detecção de erro (linha ~655-659):**
   ```javascript
   // Verificar se a lógica V26 está presente:
   const isError = errorInfo !== null || 
     (responseData && (
       // Verificar status como string (estrutura atual do endpoint)
       responseData.status === 'error' ||
       // Verificar success como boolean (compatibilidade)
       responseData.success === false ||
       // Se não é sucesso explícito E não tem IDs de sucesso, considerar erro
       (responseData.status !== 'success' && 
        responseData.success !== true &&
        !responseData.data?.leadIdFlyingDonkeys &&
        !responseData.data?.opportunityIdFlyingDonkeys &&
        !responseData.contact_id &&
        !responseData.lead_id &&
        !responseData.id)
     ));
   ```

#### **2.4 Verificar e Preparar Arquivos PHP PROD**

**Arquivos PHP a Verificar/Copiar:**

1. **`send_email_notification_endpoint_prod.php`**
   - ✅ Arquivo já existe em `03-PRODUCTION/`
   - ✅ Nome correto com sufixo `_prod`
   - ⚠️ Verificar se conteúdo está atualizado

2. **`add_flyingdonkeys_prod.php`**
   - ✅ Arquivo já existe em `03-PRODUCTION/`
   - ⚠️ **CRÍTICO:** Verificar se está atualizado comparado com `add_flyingdonkeys_v2.php`
   - Se não estiver atualizado, copiar `add_flyingdonkeys_v2.php` → `add_flyingdonkeys_prod.php`

3. **`add_webflow_octa_prod.php`**
   - ✅ Arquivo já existe em `03-PRODUCTION/`
   - ⚠️ **CRÍTICO:** Verificar se está atualizado comparado com `add_webflow_octa_v2.php`
   - Se não estiver atualizado, copiar `add_webflow_octa_v2.php` → `add_webflow_octa_prod.php`

**⚠️ IMPORTANTE:** Os arquivos `_v2.php` são os que estão sendo usados atualmente em produção. Precisamos garantir que os `_prod.php` estejam sincronizados com eles antes de atualizar as referências no JavaScript.

---

### **FASE 3: COPIAR ARQUIVOS PARA SERVIDOR PROD**

**Objetivo:** Criar backups no servidor e fazer upload dos arquivos PROD

#### **3.1 Criar Backups no Servidor (ANTES DE QUALQUER CÓPIA)**

**⚠️ CRÍTICO:** Sempre fazer backup no servidor ANTES de copiar novos arquivos!

```bash
# Conectar no servidor
ssh root@46.62.174.150

# Criar diretório de backup com timestamp
BACKUP_DIR="/root/backup_migracao_producao_$(date +%Y%m%d_%H%M%S)"
mkdir -p $BACKUP_DIR

# Backup arquivos JavaScript PROD (se existirem)
if [ -f "/var/www/html/webhooks/FooterCodeSiteDefinitivoCompleto_prod.js" ]; then
  cp /var/www/html/webhooks/FooterCodeSiteDefinitivoCompleto_prod.js $BACKUP_DIR/FooterCodeSiteDefinitivoCompleto_prod.js.backup
  echo "✅ Backup FooterCode PROD criado"
fi

if [ -f "/var/www/html/webhooks/MODAL_WHATSAPP_DEFINITIVO_prod.js" ]; then
  cp /var/www/html/webhooks/MODAL_WHATSAPP_DEFINITIVO_prod.js $BACKUP_DIR/MODAL_WHATSAPP_DEFINITIVO_prod.js.backup
  echo "✅ Backup Modal PROD criado"
fi

# Backup arquivos PHP PROD (se existirem)
if [ -f "/var/www/html/webhooks/send_email_notification_endpoint_prod.php" ]; then
  cp /var/www/html/webhooks/send_email_notification_endpoint_prod.php $BACKUP_DIR/send_email_notification_endpoint_prod.php.backup
  echo "✅ Backup Email Endpoint PROD criado"
fi

if [ -f "/var/www/html/webhooks/add_flyingdonkeys_prod.php" ]; then
  cp /var/www/html/webhooks/add_flyingdonkeys_prod.php $BACKUP_DIR/add_flyingdonkeys_prod.php.backup
  echo "✅ Backup FlyingDonkeys PROD criado"
fi

if [ -f "/var/www/html/webhooks/add_webflow_octa_prod.php" ]; then
  cp /var/www/html/webhooks/add_webflow_octa_prod.php $BACKUP_DIR/add_webflow_octa_prod.php.backup
  echo "✅ Backup Octadesk PROD criado"
fi

# Backup também dos arquivos _v2.php (caso precisemos reverter)
if [ -f "/var/www/html/webhooks/add_flyingdonkeys_v2.php" ]; then
  cp /var/www/html/webhooks/add_flyingdonkeys_v2.php $BACKUP_DIR/add_flyingdonkeys_v2.php.backup
  echo "✅ Backup FlyingDonkeys V2 criado"
fi

if [ -f "/var/www/html/webhooks/add_webflow_octa_v2.php" ]; then
  cp /var/www/html/webhooks/add_webflow_octa_v2.php $BACKUP_DIR/add_webflow_octa_v2.php.backup
  echo "✅ Backup Octadesk V2 criado"
fi

# Verificar backups criados
echo ""
echo "📋 Backups criados em: $BACKUP_DIR"
ls -lh $BACKUP_DIR/
```

#### **3.2 Verificar Estrutura no Servidor**

```bash
# Conectar no servidor
ssh root@46.62.174.150

# Verificar se diretório PROD existe
ls -ld /var/www/html/webhooks/ 2>&1

# Se não existir ou não estiver acessível, criar/verificar
mkdir -p /var/www/html/webhooks/
chmod 755 /var/www/html/webhooks/
```

#### **3.3 Copiar Arquivos JavaScript PROD**

```powershell
# No Windows
cd "C:\Users\Luciano\OneDrive - Imediato Soluções em Seguros\Imediato\imediatoseguros-rpa-playwright"

# Copiar FooterCode PROD para servidor
scp "WEBFLOW-SEGUROSIMEDIATO\03-PRODUCTION\FooterCodeSiteDefinitivoCompleto_prod.js" `
    root@46.62.174.150:/var/www/html/webhooks/

# Copiar Modal PROD para servidor
scp "WEBFLOW-SEGUROSIMEDIATO\03-PRODUCTION\MODAL_WHATSAPP_DEFINITIVO_prod.js" `
    root@46.62.174.150:/var/www/html/webhooks/
```

#### **3.4 Copiar Arquivos PHP PROD**

```powershell
# Copiar endpoint de email PROD para servidor
scp "WEBFLOW-SEGUROSIMEDIATO\03-PRODUCTION\send_email_notification_endpoint_prod.php" `
    root@46.62.174.150:/var/www/html/webhooks/

# Copiar endpoint EspoCRM PROD para servidor
scp "WEBFLOW-SEGUROSIMEDIATO\03-PRODUCTION\add_flyingdonkeys_prod.php" `
    root@46.62.174.150:/var/www/html/webhooks/

# Copiar endpoint Octadesk PROD para servidor
scp "WEBFLOW-SEGUROSIMEDIATO\03-PRODUCTION\add_webflow_octa_prod.php" `
    root@46.62.174.150:/var/www/html/webhooks/
```

#### **3.5 Configurar Permissões**

```bash
# No servidor
ssh root@46.62.174.150

# Configurar permissões dos arquivos PROD
chmod 644 /var/www/html/webhooks/FooterCodeSiteDefinitivoCompleto_prod.js
chmod 644 /var/www/html/webhooks/MODAL_WHATSAPP_DEFINITIVO_prod.js
chmod 644 /var/www/html/webhooks/send_email_notification_endpoint_prod.php
chmod 644 /var/www/html/webhooks/add_flyingdonkeys_prod.php
chmod 644 /var/www/html/webhooks/add_webflow_octa_prod.php

# Verificar propriedade
chown www-data:www-data /var/www/html/webhooks/*.js
chown www-data:www-data /var/www/html/webhooks/*.php

# Verificar arquivos copiados
ls -lh /var/www/html/webhooks/FooterCodeSiteDefinitivoCompleto_prod.js
ls -lh /var/www/html/webhooks/MODAL_WHATSAPP_DEFINITIVO_prod.js
ls -lh /var/www/html/webhooks/send_email_notification_endpoint_prod.php
ls -lh /var/www/html/webhooks/add_flyingdonkeys_prod.php
ls -lh /var/www/html/webhooks/add_webflow_octa_prod.php
```

---

### **FASE 4: VERIFICAR E CORRIGIR NGINX**

**Objetivo:** Garantir que Nginx permite acesso ao diretório PROD

#### **4.1 Verificar Configuração Nginx**

```bash
# No servidor
ssh root@46.62.174.150

# Verificar configuração Nginx para produção
cat /etc/nginx/sites-available/default | grep -A 20 "webhooks\|location /webhooks"

# Ou verificar configuração específica
cat /etc/nginx/sites-available/bpsegurosimediato.com.br 2>/dev/null | grep -A 20 "webhooks\|location"
```

#### **4.2 Corrigir Configuração Nginx (se necessário)**

**Se Nginx estiver bloqueando `/var/www/html/webhooks/`:**

```bash
# Editar configuração Nginx
nano /etc/nginx/sites-available/default
# ou
nano /etc/nginx/sites-available/bpsegurosimediato.com.br

# Adicionar/verificar configuração:
# location /webhooks/ {
#     alias /var/www/html/webhooks/;
#     index index.php index.html;
#     try_files $uri $uri/ =404;
#     
#     location ~ \.php$ {
#         fastcgi_pass unix:/var/run/php/php8.1-fpm.sock;
#         fastcgi_index index.php;
#         fastcgi_param SCRIPT_FILENAME $request_filename;
#         include fastcgi_params;
#     }
# }

# Testar configuração
nginx -t

# Se OK, recarregar Nginx
systemctl reload nginx
```

---

### **FASE 5: ATUALIZAR URLS NO WEBFLOW**

**Objetivo:** Atualizar Footer Code no Webflow para apontar para arquivo PROD

#### **5.1 Atualizar Footer Code PROD no Webflow**

**Ações:**
1. Acessar Webflow Dashboard PROD
2. Navegar para: Project Settings → Custom Code → Footer Code
3. Atualizar URL de:
   ```
   https://dev.bpsegurosimediato.com.br/webhooks/FooterCodeSiteDefinitivoCompleto_prod.js?v=1.3
   ```
   Para:
   ```
   https://bpsegurosimediato.com.br/webhooks/FooterCodeSiteDefinitivoCompleto_prod.js?v=1.6
   ```
4. Publicar alterações

#### **5.2 Verificar URLs nos Arquivos**

- ✅ FooterCode PROD deve carregar Modal de: `bpsegurosimediato.com.br/webhooks/MODAL_WHATSAPP_DEFINITIVO_prod.js`
- ✅ Modal PROD deve usar endpoint: `bpsegurosimediato.com.br/webhooks/send_email_notification_endpoint_prod.php`

---

### **FASE 6: TESTES E VALIDAÇÃO**

**Objetivo:** Garantir que tudo está funcionando corretamente em produção

#### **6.1 Testes de Acesso aos Arquivos**

```bash
# Testar acesso HTTP aos arquivos PROD
curl -I http://bpsegurosimediato.com.br/webhooks/FooterCodeSiteDefinitivoCompleto_prod.js
curl -I http://bpsegurosimediato.com.br/webhooks/MODAL_WHATSAPP_DEFINITIVO_prod.js
curl -I http://bpsegurosimediato.com.br/webhooks/send_email_notification_endpoint_prod.php

# Testar acesso HTTPS (se SSL configurado)
curl -I https://bpsegurosimediato.com.br/webhooks/FooterCodeSiteDefinitivoCompleto_prod.js
curl -I https://bpsegurosimediato.com.br/webhooks/MODAL_WHATSAPP_DEFINITIVO_prod.js
```

#### **6.2 Testes Funcionais**

**Teste 1: Modal em iOS**
- [ ] Acessar `www.segurosimediato.com.br` em dispositivo iOS
- [ ] Clicar em elemento `#whatsapplink`
- [ ] Verificar que modal abre na mesma página (não como nova aba)
- [ ] Verificar console (sem erros)

**Teste 2: Modal em Android/Desktop**
- [ ] Acessar `www.segurosimediato.com.br` em dispositivo Android/Desktop
- [ ] Clicar em elemento `#whatsapplink`
- [ ] Verificar que modal abre normalmente
- [ ] Verificar que não abre duas vezes (flag funcionando)

**Teste 3: Envio de Email**
- [ ] Preencher formulário completo no modal
- [ ] Submeter formulário
- [ ] Verificar que email é enviado corretamente
- [ ] Verificar que não aparece "❌ ERRO NO ENVIO: Erro desconhecido" quando submissão é completa
- [ ] Verificar logs no servidor

#### **6.3 Verificar Logs**

```bash
# No servidor
ssh root@46.62.174.150

# Verificar logs Nginx
tail -f /var/log/nginx/access.log | grep webhooks
tail -f /var/log/nginx/error.log | grep webhooks

# Verificar logs PHP (se existirem)
tail -f /var/log/php8.1-fpm.log | grep send_email_notification_endpoint_prod
```

---

### **FASE 7: VALIDAÇÃO FINAL**

**Objetivo:** Confirmar que migração foi bem-sucedida

#### **7.1 Checklist Final**

- [ ] Arquivos JavaScript PROD copiados para servidor
- [ ] Arquivo PHP PROD copiado para servidor
- [ ] Permissões configuradas corretamente
- [ ] Nginx configurado para permitir acesso ao diretório PROD
- [ ] URLs atualizadas no Webflow
- [ ] URLs verificadas nos arquivos JavaScript
- [ ] Testes funcionais realizados (iOS, Android, Desktop)
- [ ] Teste de envio de email realizado
- [ ] Logs verificados (sem erros críticos)
- [ ] Ambiente DEV ainda funcionando

#### **7.2 Documentação**

- [ ] Atualizar arquitetura com novas URLs PROD
- [ ] Documentar configuração final
- [ ] Registrar data/hora da migração
- [ ] Criar nota sobre correções aplicadas

---

## 🔄 PLANO DE ROLLBACK

### **Cenário 1: Problemas com Arquivos JavaScript**

**Sintomas:**
- Arquivos não carregam
- Erros 404 ou 500
- Modal não funciona

**Ação:**
1. Reverter URL no Webflow para DEV:
   ```
   https://dev.bpsegurosimediato.com.br/webhooks/FooterCodeSiteDefinitivoCompleto_prod.js?v=1.3
   ```
2. Verificar arquivos no servidor
3. Restaurar backups se necessário

### **Cenário 2: Problemas com Endpoint PHP**

**Sintomas:**
- Email não é enviado
- Erro 404 no endpoint
- Erro 500 no endpoint

**Ação:**
1. Verificar arquivo PHP no servidor
2. Verificar permissões
3. Verificar logs PHP
4. Restaurar backup se necessário

### **Cenário 3: Problemas com Nginx**

**Sintomas:**
- Arquivos não acessíveis
- Erro 403 Forbidden
- Erro 404 Not Found

**Ação:**
1. Verificar configuração Nginx
2. Verificar permissões de diretório
3. Testar configuração: `nginx -t`
4. Recarregar Nginx: `systemctl reload nginx`
5. Se não resolver, reverter URL no Webflow para DEV

### **Rollback Completo**

**Se necessário reverter tudo:**

1. **Reverter URL no Webflow:**
   ```
   https://dev.bpsegurosimediato.com.br/webhooks/FooterCodeSiteDefinitivoCompleto_prod.js?v=1.3
   ```

2. **Restaurar Backups (se necessário):**
   ```bash
   # No servidor
   ssh root@46.62.174.150
   
   # Identificar backup mais recente
   ls -lt /root/backup_migracao_producao_* | head -1
   
   # Restaurar arquivos (substituir TIMESTAMP pelo correto)
   BACKUP_DIR="/root/backup_migracao_producao_TIMESTAMP"
   cp $BACKUP_DIR/FooterCodeSiteDefinitivoCompleto_prod.js /var/www/html/webhooks/ 2>/dev/null
   cp $BACKUP_DIR/MODAL_WHATSAPP_DEFINITIVO_prod.js /var/www/html/webhooks/ 2>/dev/null
   cp $BACKUP_DIR/send_email_notification_endpoint_prod.php /var/www/html/webhooks/ 2>/dev/null
   ```

3. **Documentar Problemas:**
   - Listar todos os problemas encontrados
   - Documentar tentativas de correção
   - Criar plano de correção para próxima tentativa

---

## 📋 CHECKLIST COMPLETO

### **Preparação**
- [ ] Arquivos DEV verificados no servidor
- [ ] Arquivos PROD verificados no servidor (se existirem)
- [ ] **Backups criados no Windows ANTES de copiar DEV → PROD**
- [ ] **Backups criados no servidor ANTES de copiar arquivos**
- [ ] Backups verificados e acessíveis (Windows e servidor)

### **Preparação Arquivos Locais**
- [ ] Arquivos DEV copiados para diretório PROD (Windows)
- [ ] URLs atualizadas no FooterCode PROD
- [ ] URLs atualizadas no Modal PROD (email, EspoCRM, Octadesk)
- [ ] Lógica de detecção de erro verificada no Modal PROD
- [ ] Arquivos PHP PROD verificados (`send_email_notification_endpoint_prod.php`, `add_flyingdonkeys_prod.php`, `add_webflow_octa_prod.php`)
- [ ] Arquivos PHP `_v2.php` comparados com `_prod.php` (garantir sincronização)

### **Upload para Servidor**
- [ ] FooterCode PROD copiado para servidor
- [ ] Modal PROD copiado para servidor
- [ ] Endpoint email PHP PROD copiado para servidor (`send_email_notification_endpoint_prod.php`)
- [ ] Endpoint EspoCRM PHP PROD copiado para servidor (`add_flyingdonkeys_prod.php`)
- [ ] Endpoint Octadesk PHP PROD copiado para servidor (`add_webflow_octa_prod.php`)
- [ ] Permissões configuradas corretamente
- [ ] Propriedade configurada corretamente

### **Configuração Nginx**
- [ ] Configuração Nginx verificada
- [ ] Acesso ao diretório PROD permitido
- [ ] Nginx testado (`nginx -t`)
- [ ] Nginx recarregado (se necessário)

### **Atualização Webflow**
- [ ] Footer Code PROD atualizado no Webflow
- [ ] URL verificada (aponta para PROD)
- [ ] Alterações publicadas

### **Testes**
- [ ] Arquivos acessíveis via HTTP/HTTPS
- [ ] Teste funcional iOS realizado
- [ ] Teste funcional Android realizado
- [ ] Teste funcional Desktop realizado
- [ ] Teste de envio de email realizado
- [ ] Logs verificados (sem erros críticos)

### **Validação Final**
- [ ] Site PROD funcionando completamente
- [ ] Modal funcionando em todos os dispositivos
- [ ] Email sendo enviado corretamente
- [ ] Sem mensagens de erro falsas
- [ ] Ambiente DEV ainda funcionando
- [ ] Documentação atualizada

---

## ⚠️ RISCOS E MITIGAÇÕES

### **Risco 1: Nginx bloqueando acesso PROD**
- **Mitigação:** Verificar e corrigir configuração Nginx antes de copiar arquivos
- **Plano B:** Manter arquivos em DEV temporariamente até Nginx ser corrigido

### **Risco 2: URLs incorretas nos arquivos**
- **Mitigação:** Verificar todas as URLs antes de copiar
- **Plano B:** Corrigir URLs diretamente no servidor se necessário

### **Risco 3: Endpoint PHP não encontrado**
- **Mitigação:** Verificar que arquivo `_prod.php` existe antes de atualizar URLs
- **Plano B:** Criar arquivo `_prod.php` se não existir

### **Risco 4: Permissões incorretas**
- **Mitigação:** Configurar permissões após cópia
- **Plano B:** Verificar e corrigir permissões manualmente

### **Risco 5: Ambiente DEV afetado**
- **Mitigação:** Não modificar arquivos DEV durante migração
- **Plano B:** Restaurar arquivos DEV de backup se necessário

---

## 📊 CRONOGRAMA ESTIMADO

| **Fase** | **Tempo Estimado** | **Dependências** |
|----------|-------------------|------------------|
| Fase 1: Preparação | 15 minutos | - |
| Fase 2: Preparar Arquivos Locais | 20 minutos | Fase 1 |
| Fase 3: Copiar para Servidor | 10 minutos | Fase 2 |
| Fase 4: Verificar Nginx | 15 minutos | Fase 3 |
| Fase 5: Atualizar Webflow | 10 minutos | Fase 4 |
| Fase 6: Testes | 30 minutos | Fase 5 |
| Fase 7: Validação Final | 15 minutos | Fase 6 |
| **TOTAL** | **~2 horas** | - |

---

## 📝 NOTAS IMPORTANTES

1. **⚠️ NUNCA modificar arquivos DEV durante migração para PROD**
2. **⚠️ SEMPRE criar backups antes de qualquer alteração**
3. **⚠️ VERIFICAR URLs nos arquivos antes de copiar**
4. **⚠️ TESTAR extensivamente antes de atualizar Webflow**
5. **⚠️ MANTER ambiente DEV funcionando durante migração**
6. **⚠️ TER plano de rollback pronto antes de iniciar**

---

## 🔗 ARQUIVOS RELACIONADOS

- `WEBFLOW-SEGUROSIMEDIATO/05-DOCUMENTATION/PROJETO_CORRECAO_MODAL_IOS_NOVA_ABA.md`
- `WEBFLOW-SEGUROSIMEDIATO/05-DOCUMENTATION/PROJETO_CORRECAO_ERRO_EMAIL_SUBMISSAO_COMPLETA.md`
- `WEBFLOW-SEGUROSIMEDIATO/05-DOCUMENTATION/ARQUITETURA_FOOTER_CODES_WEBFLOW_DEV_PROD.md`
- `DIRETIVAS_PROJETOS.md`

---

**Status:** 📋 Planejado - Aguardando Execução  
**Próxima Ação:** Executar Fase 1 (Preparação e Verificação)  
**Última Atualização:** 06/11/2025

