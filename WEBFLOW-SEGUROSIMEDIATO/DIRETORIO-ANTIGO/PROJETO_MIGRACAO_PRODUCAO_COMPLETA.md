# 📋 PROJETO: MIGRAÇÃO COMPLETA PARA PRODUÇÃO

**Data de Criação:** 01/11/2025 14:00  
**Status:** 🟡 **PLANEJADO - AGUARDANDO REVISÃO**  
**Complexidade:** Alta  
**Impacto:** Crítico  
**Tempo Estimado:** ~6-8 horas

---

## 🎯 OBJETIVO

Migrar todo o sistema de desenvolvimento para produção, criando versões de produção de todos os arquivos JavaScript e PHP, atualizando endpoints, credenciais e configurações, garantindo que a produção utilize exclusivamente os serviços corretos (FlyingDonkeys ao invés de TravelAngels, endpoints de produção, etc.).

---

## 📋 ESCOPO DO PROJETO

Este projeto envolve:
- Criação de versões _prod de arquivos JavaScript
- Criação de versões v2 de webhooks PHP apontando para produção
- Atualização de todas as referências de endpoints de dev para prod
- Migração de credenciais (FlyingDonkeys, Octadesk, SafetyMails)
- Deploy dos arquivos para servidor de produção
- Atualização do Webflow para usar versões de produção

---

## 🔍 ANÁLISE PRÉVIA

### **Arquivos Atuais (DEV):**

| Arquivo | Localização | Versão |
|---------|-------------|--------|
| `FooterCodeSiteDefinitivoCompleto.js` | DEV | v1.3 |
| `Footer Code Site Definitivo WEBFLOW.js` | DEV | v1.2 |
| `add_travelangels_dev.php` | DEV | - |
| `add_webflow_octa_dev.php` | DEV | - |

### **Arquivos de Produção (Referência):**

| Arquivo | Localização | Uso |
|---------|-------------|-----|
| `add_travelangels.php` | `/var/www/html/add_travelangels.php` | Produção atual (FlyingDonkeys) |
| `add_webflow_octa.php` | `/var/www/html/add_webflow_octa.php` | Produção atual (Octadesk) |

### **Endpoints Atuais e Novos:**

| Serviço | DEV | PRODUÇÃO (Atual) | PRODUÇÃO (Novo _v2) |
|---------|-----|------------------|---------------------|
| **EspoCRM (FlyingDonkeys)** | `add_travelangels_dev.php` → `travelangels.com.br` ❌ | `add_travelangels.php` → `flyingdonkeys.com.br` ✅ | `add_flyingdonkeys_v2.php` → `flyingdonkeys.com.br` ✅ |
| **Octadesk** | `add_webflow_octa_dev.php` → Simulador | `add_webflow_octa.php` → Octadesk Real ✅ | `add_webflow_octa_v2.php` → Octadesk Real ✅ |
| **JavaScript** | `dev.bpsegurosimediato.com.br` | `bpsegurosimediato.com.br` | `bpsegurosimediato.com.br` (com sufixo `_prod.js`) |

**Nota:** Endpoints antigos permanecerão funcionando. Novos endpoints _v2 serão criados em paralelo.

---

## 📝 TAREFAS DETALHADAS

### **FASE 1: PREPARAÇÃO E BACKUPS**

#### **Tarefa 1.1: Criar Backups de Todos os Arquivos que Serão Modificados**

**Arquivos a Fazer Backup:**

1. `02-DEVELOPMENT/custom-codes/FooterCodeSiteDefinitivoCompleto.js`
2. `02-DEVELOPMENT/custom-codes/Footer Code Site Definitivo WEBFLOW.js`
3. `02-DEVELOPMENT/custom-codes/add_travelangels_dev.php` (se existir localmente)
4. `02-DEVELOPMENT/custom-codes/add_webflow_octa_dev.php` (se existir localmente)

**Arquivos de Produção (Não serão alterados, mas fazer backup para referência):**

1. **Footer Code do Webflow** (backup manual - copiar conteúdo)
2. **MODAL_WHATSAPP_DEFINITIVO.js** (se existir em produção, fazer backup antes de atualizar)

**⚠️ NOTA:** Arquivos PHP de produção (`add_travelangels.php`, `add_webflow_octa.php`) **NÃO serão alterados** - permanecerão intactos. Não é necessário fazer backup deles, pois não serão tocados.

**Ações:**
- Criar backup com timestamp: `arquivo.backup_PROD_YYYYMMDD_HHMMSS`
- Documentar localização dos backups na seção de backups deste documento

**Checklist:**
- [ ] Backup de `FooterCodeSiteDefinitivoCompleto.js`
- [ ] Backup de `Footer Code Site Definitivo WEBFLOW.js`
- [ ] Verificar se há arquivos PHP locais para backup
- [ ] Documentar localização dos backups

---

### **FASE 2: CRIAÇÃO DE ARQUIVOS DE PRODUÇÃO**

#### **Tarefa 2.1: Criar `FooterCodeSiteDefinitivoCompleto_prod.js`**

**Objetivo:** Criar versão de produção do arquivo JavaScript principal

**Arquivo Base:** `02-DEVELOPMENT/custom-codes/FooterCodeSiteDefinitivoCompleto.js`

**Alterações Necessárias:**

1. **Atualizar Header do Arquivo:**
   ```javascript
   /**
    * PROJETO: UNIFICAÇÃO DE ARQUIVOS FOOTER CODE
    * INÍCIO: 30/10/2025 19:55
    * ÚLTIMA ALTERAÇÃO: [DATA_CRIAÇÃO_PROD]
    * 
    * VERSÃO: 1.3_PROD - Versão de Produção
    * 
    * ALTERAÇÕES NESTA VERSÃO (PRODUÇÃO):
    * - Versão de produção baseada na versão 1.3
    * - Endpoints atualizados para produção
    * - Credenciais de produção configuradas
    * - URLs apontando para bpsegurosimediato.com.br (sem dev)
    * 
    * Localização: https://bpsegurosimediato.com.br/webhooks/FooterCodeSiteDefinitivoCompleto_prod.js
    * 
    * ⚠️ AMBIENTE: PRODUÇÃO
    * - SafetyMails Ticket: [OBTER DO PAINEL]
    * - SafetyMails API Key: [OBTER DO PAINEL]
    * - Ver documentação: DOCUMENTACAO_MIGRACAO_PRODUCAO_SAFETYMAILS.md
    */
   ```

2. **Atualizar URL de Localização (Linha ~30):**
   ```javascript
   // ANTES:
   * Localização: https://dev.bpsegurosimediato.com.br/webhooks/FooterCodeSiteDefinitivoCompleto.js
   
   // DEPOIS:
   * Localização: https://bpsegurosimediato.com.br/webhooks/FooterCodeSiteDefinitivoCompleto_prod.js
   ```

3. **Atualizar Credenciais SafetyMails (Linhas ~33-34):**
   ```javascript
   // ANTES (DEV):
   window.SAFETY_TICKET = 'fc5e18c10c4aa883b2c31a305f1c09fea3834138';
   window.SAFETY_API_KEY = '20a7a1c297e39180bd80428ac13c363e882a531f';
   
   // DEPOIS (PROD):
   window.SAFETY_TICKET = '[OBTER DO PAINEL SAFETYMAILS]';
   window.SAFETY_API_KEY = '[OBTER DO PAINEL SAFETYMAILS]';
   ```

4. **Atualizar URL do Modal WhatsApp (Linha ~1019):**
   ```javascript
   // ANTES:
   script.src = 'https://dev.bpsegurosimediato.com.br/webhooks/MODAL_WHATSAPP_DEFINITIVO.js?v=23&force=' + Math.random();
   
   // DEPOIS:
   script.src = 'https://bpsegurosimediato.com.br/webhooks/MODAL_WHATSAPP_DEFINITIVO.js?v=23&force=' + Math.random();
   ```

5. **Verificar e Atualizar Chamadas de Webhooks (se houver no código):**
   - Procurar por referências a `add_travelangels_dev.php`
   - Procurar por referências a `add_webflow_octa_dev.php`
   - Substituir por `add_flyingdonkeys_v2.php` e `add_webflow_octa_v2.php`
   - **NOTA:** Verificar se o FooterCodeSiteDefinitivoCompleto.js faz chamadas diretas aos webhooks ou se isso é feito pelo MODAL_WHATSAPP_DEFINITIVO.js

**Localização do Novo Arquivo:**
- Local: `02-DEVELOPMENT/custom-codes/FooterCodeSiteDefinitivoCompleto_prod.js`

**Checklist:**
- [ ] Copiar arquivo base
- [ ] Atualizar header
- [ ] Atualizar URL de localização
- [ ] Atualizar credenciais SafetyMails
- [ ] Atualizar URL do modal WhatsApp
- [ ] Verificar e atualizar chamadas de webhooks (se houver)
- [ ] Revisar todas as URLs para remover referências a `dev.bpsegurosimediato.com.br`

---

#### **Tarefa 2.2: Criar `Footer Code Site Definitivo WEBFLOW_prod.js`**

**Objetivo:** Criar versão de produção do código do Footer Code do Webflow

**Arquivo Base:** `02-DEVELOPMENT/custom-codes/Footer Code Site Definitivo WEBFLOW.js`

**Alterações Necessárias:**

1. **Atualizar URL do Script Unificado (Linha ~38):**
   ```html
   <!-- ANTES (DEV): -->
   <script src="https://dev.bpsegurosimediato.com.br/webhooks/FooterCodeSiteDefinitivoCompleto.js?v=1.2" defer></script>
   
   <!-- DEPOIS (PROD): -->
   <script src="https://bpsegurosimediato.com.br/webhooks/FooterCodeSiteDefinitivoCompleto_prod.js?v=1.3" defer></script>
   ```

**Localização do Novo Arquivo:**
- Local: `02-DEVELOPMENT/custom-codes/Footer Code Site Definitivo WEBFLOW_prod.js`

**Checklist:**
- [ ] Copiar arquivo base
- [ ] Atualizar URL do script unificado
- [ ] Atualizar versão na query string (v=1.3)

---

#### **Tarefa 2.3: Criar `add_flyingdonkeys_v2.php`**

**Objetivo:** Criar versão de produção do webhook EspoCRM apontando para FlyingDonkeys

**Arquivo Base:** `add_travelangels_dev.php` (no servidor: `/var/www/html/dev/webhooks/add_travelangels_dev.php`)

**Alterações Necessárias:**

1. **Atualizar Header do Arquivo:**
   ```php
   /**
    * WEBHOOK FLYINGDONKEYS - PRODUÇÃO V2
    * bpsegurosimediato.com.br/webhooks/add_flyingdonkeys_v2.php
    * 
    * Versão de produção com API V2, logging avançado e validação de signature
    * Baseado no add_travelangels_dev.php mas apontando para produção FlyingDonkeys
    * 
    * VERSÃO: 2.0 - Migração de TravelAngels para FlyingDonkeys
    * 
    * ALTERAÇÕES NESTA VERSÃO:
    * - Removidas todas as chamadas ao endpoint travelangels.com.br
    * - Atualizado para usar endpoints de produção do FlyingDonkeys
    * - Credenciais de produção do FlyingDonkeys configuradas
    * - CORS configurado para domínios de produção
    * - Logs apontando para diretório de produção
    */
   ```

2. **Obter Credenciais de Produção do FlyingDonkeys:**
   - Acessar arquivo de produção: `/var/www/html/add_travelangels.php`
   - Localizar:
     - URL da API: `https://flyingdonkeys.com.br` (ou similar)
     - API Key de produção
     - API User Email de produção
   - Documentar credenciais no arquivo (sem commitar no GitHub)

3. **Eliminar Chamadas a TravelAngels:**
   - Buscar por `travelangels.com.br` no arquivo
   - Remover ou comentar todas as referências
   - Verificar se há configurações específicas de TravelAngels

4. **Atualizar Configurações de CORS:**
   ```php
   // ANTES (DEV):
   $allowed_origins = array(
       'https://segurosimediato-8119bf26e77bf4ff336a58e.webflow.io',
       'https://dev.bpsegurosimediato.com.br',
       // ...
   );
   
   // DEPOIS (PROD):
   $allowed_origins = array(
       'https://www.segurosimediato.com.br',
       'https://segurosimediato.com.br',
       'https://bpsegurosimediato.com.br',
       // ... outros domínios de produção
   );
   ```

5. **Atualizar Configurações do CRM:**
   ```php
   // Substituir:
   $DEV_ESPOCRM_CREDENTIALS
   $DEV_CRM_CONFIG
   
   // Por configurações de produção (obter do add_travelangels.php em produção)
   ```

6. **Atualizar Caminhos de Log:**
   ```php
   // ANTES (DEV):
   $DEBUG_LOG_FILE = '/var/www/html/dev/logs/travelangels_dev.txt';
   
   // DEPOIS (PROD):
   $DEBUG_LOG_FILE = '/var/www/html/logs/travelangels_prod.txt';
   ```

7. **Atualizar Headers de Resposta:**
   ```php
   // ANTES (DEV):
   header('X-Environment: development');
   header('X-API-Version: 2.0-dev');
   
   // DEPOIS (PROD):
   header('X-Environment: production');
   header('X-API-Version: 2.0');
   ```

**Localização do Novo Arquivo:**
- Local: `02-DEVELOPMENT/custom-codes/add_flyingdonkeys_v2.php`

**Checklist:**
- [ ] Copiar arquivo base do servidor
- [ ] Atualizar header
- [ ] Obter credenciais de produção do arquivo add_travelangels.php
- [ ] Remover todas as chamadas a travelangels.com.br
- [ ] Atualizar configurações de CORS
- [ ] Atualizar configurações do CRM
- [ ] Atualizar caminhos de log
- [ ] Atualizar headers de resposta
- [ ] Verificar includes/requires (class.php, configs, etc.)

---

#### **Tarefa 2.4: Criar `add_webflow_octa_v2.php`**

**Objetivo:** Criar versão de produção do webhook Octadesk

**Arquivo Base:** `add_webflow_octa_dev.php` (no servidor: `/var/www/html/dev/webhooks/add_webflow_octa_dev.php`)

**Alterações Necessárias:**

1. **Obter Configurações de Produção:**
   - Acessar arquivo de produção: `/var/www/html/add_webflow_octa.php`
   - Localizar:
     - Endpoint do Octadesk
     - Credenciais (API Key, Token, etc.)
     - Configurações de webhook

2. **Atualizar Header do Arquivo:**
   ```php
   /**
    * WEBHOOK OCTADESK - PRODUÇÃO V2
    * bpsegurosimediato.com.br/webhooks/add_webflow_octa_v2.php
    * 
    * Versão de produção do webhook Octadesk
    * Baseado no add_webflow_octa_dev.php mas apontando para Octadesk real
    * 
    * VERSÃO: 2.0 - Migração para produção
    * 
    * ALTERAÇÕES NESTA VERSÃO:
    * - Endpoint atualizado para Octadesk de produção
    * - Credenciais de produção configuradas
    * - CORS configurado para domínios de produção
    * - Logs apontando para diretório de produção
    */
   ```

3. **Atualizar Configurações de CORS:**
   - Mesmo processo da Tarefa 2.3

4. **Atualizar Endpoint do Octadesk:**
   - Substituir simulador por endpoint real de produção
   - Obter do arquivo `add_webflow_octa.php` em produção

5. **Atualizar Caminhos de Log:**
   ```php
   // ANTES (DEV):
   $DEBUG_LOG_FILE = '/var/www/html/dev/logs/octadesk_dev.txt';
   
   // DEPOIS (PROD):
   $DEBUG_LOG_FILE = '/var/www/html/logs/octadesk_prod.txt';
   ```

**Localização do Novo Arquivo:**
- Local: `02-DEVELOPMENT/custom-codes/add_webflow_octa_v2.php`

**Checklist:**
- [ ] Copiar arquivo base do servidor
- [ ] Obter configurações de produção do add_webflow_octa.php
- [ ] Atualizar header
- [ ] Atualizar endpoint do Octadesk
- [ ] Atualizar configurações de CORS
- [ ] Atualizar caminhos de log
- [ ] Atualizar headers de resposta

---

### **FASE 3: ATUALIZAÇÃO DE REFERÊNCIAS NO JAVASCRIPT**

#### **Tarefa 3.1: Atualizar Chamadas de Webhooks no `FooterCodeSiteDefinitivoCompleto_prod.js`**

**Investigação Necessária:**
- Verificar se `FooterCodeSiteDefinitivoCompleto.js` faz chamadas diretas aos webhooks
- Ou se as chamadas são feitas pelo `MODAL_WHATSAPP_DEFINITIVO.js`

**Se houver chamadas no FooterCodeSiteDefinitivoCompleto.js:**

1. **Buscar por Referências:**
   ```javascript
   // Procurar por:
   - 'add_travelangels_dev.php'
   - 'add_webflow_octa_dev.php'
   - 'bpsegurosimediato.com.br/dev/webhooks'
   ```

2. **Substituir por:**
   ```javascript
   // Substituir por:
   - 'add_flyingdonkeys_v2.php'
   - 'add_webflow_octa_v2.php'
   - 'bpsegurosimediato.com.br/webhooks'
   ```

**Se as chamadas forem no MODAL_WHATSAPP_DEFINITIVO.js:**

- **Ação:** Criar nota para atualizar o MODAL_WHATSAPP_DEFINITIVO.js em produção também
- Verificar se há versão _prod do modal ou se será necessário criar

**Checklist:**
- [ ] Verificar onde são feitas as chamadas aos webhooks
- [ ] Atualizar referências no FooterCodeSiteDefinitivoCompleto_prod.js (se aplicável)
- [ ] Documentar necessidade de atualizar MODAL_WHATSAPP_DEFINITIVO.js (se aplicável)

---

### **FASE 4: DEPLOY PARA SERVIDOR**

#### **Tarefa 4.1: Copiar `add_flyingdonkeys_v2.php` para Produção (PARALELO)**

**Ação:**
```bash
scp "02-DEVELOPMENT/custom-codes/add_flyingdonkeys_v2.php" root@46.62.174.150:/var/www/html/webhooks/add_flyingdonkeys_v2.php
```

**⚠️ IMPORTANTE:** Este arquivo será criado **PARALELO** ao `add_travelangels.php` existente. O arquivo antigo **NÃO será alterado** e continuará funcionando normalmente.

**Verificação:**
```bash
ssh root@46.62.174.150 "ls -lh /var/www/html/webhooks/add_flyingdonkeys_v2.php"
curl -I https://bpsegurosimediato.com.br/webhooks/add_flyingdonkeys_v2.php
```

**Validação Paralela:**
```bash
# Verificar que ambos os arquivos existem:
ssh root@46.62.174.150 "ls -lh /var/www/html/webhooks/add_*travelangels*.php"
# Deve mostrar:
# - add_travelangels.php (antigo - intacto)
# - add_flyingdonkeys_v2.php (novo - paralelo)
```

**Checklist:**
- [ ] Arquivo copiado para servidor (novo, não sobrescreve nada)
- [ ] Arquivo antigo `add_travelangels.php` ainda existe e não foi alterado
- [ ] Permissões corretas (644 ou 755)
- [ ] Arquivo acessível via HTTP (Status 200)
- [ ] Verificar se diretório `/var/www/html/webhooks` existe

---

#### **Tarefa 4.2: Copiar `add_webflow_octa_v2.php` para Produção (PARALELO)**

**Ação:**
```bash
scp "02-DEVELOPMENT/custom-codes/add_webflow_octa_v2.php" root@46.62.174.150:/var/www/html/webhooks/add_webflow_octa_v2.php
```

**⚠️ IMPORTANTE:** Este arquivo será criado **PARALELO** ao `add_webflow_octa.php` existente. O arquivo antigo **NÃO será alterado** e continuará funcionando normalmente.

**Verificação:**
```bash
ssh root@46.62.174.150 "ls -lh /var/www/html/webhooks/add_webflow_octa_v2.php"
curl -I https://bpsegurosimediato.com.br/webhooks/add_webflow_octa_v2.php
```

**Validação Paralela:**
```bash
# Verificar que ambos os arquivos existem:
ssh root@46.62.174.150 "ls -lh /var/www/html/webhooks/add_*octa*.php"
# Deve mostrar:
# - add_webflow_octa.php (antigo - intacto)
# - add_webflow_octa_v2.php (novo - paralelo)
```

**Checklist:**
- [ ] Arquivo copiado para servidor (novo, não sobrescreve nada)
- [ ] Arquivo antigo `add_webflow_octa.php` ainda existe e não foi alterado
- [ ] Permissões corretas
- [ ] Arquivo acessível via HTTP

---

#### **Tarefa 4.3: Copiar `FooterCodeSiteDefinitivoCompleto_prod.js` para Produção**

**Ação:**
```bash
scp "02-DEVELOPMENT/custom-codes/FooterCodeSiteDefinitivoCompleto_prod.js" root@46.62.174.150:/var/www/html/webhooks/FooterCodeSiteDefinitivoCompleto_prod.js
```

**⚠️ IMPORTANTE:** Este arquivo será criado com sufixo `_prod.js`. Se houver uma versão antiga de produção (`FooterCodeSiteDefinitivoCompleto.js` sem sufixo), ela **NÃO será sobrescrita** - ambos existirão em paralelo.

**Verificação:**
```bash
ssh root@46.62.174.150 "ls -lh /var/www/html/webhooks/FooterCodeSiteDefinitivoCompleto*.js"
curl -I https://bpsegurosimediato.com.br/webhooks/FooterCodeSiteDefinitivoCompleto_prod.js
```

**Validação:**
```bash
# Verificar que arquivo foi criado (não sobrescreveu nada):
ssh root@46.62.174.150 "ls -lh /var/www/html/webhooks/*FooterCode*.js"
```

**Checklist:**
- [ ] Arquivo copiado para servidor com sufixo `_prod.js`
- [ ] Arquivos antigos (se existirem) não foram alterados
- [ ] Permissões corretas
- [ ] Arquivo acessível via HTTP
- [ ] Verificar se Content-Type é `application/javascript`

---

### **FASE 5: ATUALIZAÇÃO NO WEBFLOW**

#### **Tarefa 5.1: Atualizar Footer Code no Webflow**

**Objetivo:** Substituir o conteúdo do Footer Code no Webflow pela versão de produção

**Arquivo:** `Footer Code Site Definitivo WEBFLOW_prod.js`

**Passos:**

1. Acessar Webflow Dashboard
2. Ir em Settings → Custom Code
3. Localizar seção **Footer Code** (ou **Footer** → Custom Code)
4. Fazer backup do conteúdo atual (copiar e colar em arquivo local)
5. Substituir todo o conteúdo pelo conteúdo do arquivo `Footer Code Site Definitivo WEBFLOW_prod.js`
6. Salvar alterações
7. Publicar o site

**Checklist:**
- [ ] Backup do Footer Code atual do Webflow criado
- [ ] Conteúdo substituído pelo Footer Code Site Definitivo WEBFLOW_prod.js
- [ ] Alterações salvas
- [ ] Site publicado

---

### **FASE 6: VALIDAÇÃO E TESTES**

#### **Tarefa 6.1: Validação de Endpoints**

**Testes:**

1. **Testar acesso aos arquivos JavaScript:**
   ```bash
   curl -I https://bpsegurosimediato.com.br/webhooks/FooterCodeSiteDefinitivoCompleto_prod.js
   curl -I https://bpsegurosimediato.com.br/webhooks/MODAL_WHATSAPP_DEFINITIVO.js
   ```

2. **Testar endpoints PHP (sem dados reais):**
   ```bash
   curl -X OPTIONS https://bpsegurosimediato.com.br/webhooks/add_flyingdonkeys_v2.php
   curl -X OPTIONS https://bpsegurosimediato.com.br/webhooks/add_webflow_octa_v2.php
   ```

3. **Verificar CORS headers:**
   ```bash
   curl -H "Origin: https://www.segurosimediato.com.br" \
        -H "Access-Control-Request-Method: POST" \
        -X OPTIONS \
        https://bpsegurosimediato.com.br/webhooks/add_flyingdonkeys_v2.php -v
   ```

**Checklist:**
- [ ] JavaScript acessível (Status 200)
- [ ] Endpoints PHP respondendo (Status 200 para OPTIONS)
- [ ] Headers CORS presentes
- [ ] Content-Type correto para JavaScript

---

#### **Tarefa 6.2: Testes Funcionais**

**Testes no Site de Produção:**

1. **Teste de Carregamento:**
   - Acessar site de produção
   - Abrir DevTools (F12)
   - Verificar se `FooterCodeSiteDefinitivoCompleto_prod.js` carrega sem erros
   - Verificar console para erros

2. **Teste de Formulário:**
   - Preencher formulário com dados válidos
   - Enviar formulário
   - Verificar logs do webhook no servidor
   - Verificar se lead foi criado no FlyingDonkeys
   - Verificar se mensagem foi enviada no Octadesk

3. **Teste de GCLID:**
   - Acessar com `?gclid=teste-prod-YYYYMMDD`
   - Verificar se GCLID é capturado
   - Verificar se campo GCLID_FLD é preenchido
   - Verificar se GCLID chega no webhook

4. **Teste de Validações:**
   - Testar validação de CPF inválido
   - Testar validação de email inválido
   - Testar validação de telefone inválido
   - Testar validação de CEP inválido
   - Testar validação de placa inválida

**Checklist:**
- [ ] JavaScript carrega sem erros
- [ ] Formulário envia corretamente
- [ ] Webhook recebe dados corretos
- [ ] Lead criado no FlyingDonkeys
- [ ] Mensagem enviada no Octadesk
- [ ] GCLID funcionando
- [ ] Validações funcionando

---

## 🔍 VERIFICAÇÃO CRÍTICA: ITENS ADICIONAIS

### **1. MODAL_WHATSAPP_DEFINITIVO.js** ⚠️ **CRÍTICO - TAREFA OBRIGATÓRIA**

**Situação:**
- ✅ O `FooterCodeSiteDefinitivoCompleto_prod.js` carrega o modal de: `https://bpsegurosimediato.com.br/webhooks/MODAL_WHATSAPP_DEFINITIVO.js`
- ✅ O `MODAL_WHATSAPP_DEFINITIVO.js` contém **lógica crítica** de chamadas aos webhooks através da função `getEndpointUrl()`
- ✅ **Confirmado:** Modal faz 4 chamadas aos webhooks (2x EspoCRM, 2x Octadesk)
- ⚠️ **Problema:** Modal em produção aponta para endpoints antigos (`add_travelangels.php`, `add_webflow_octa.php`)
- ⚠️ **Solução:** Atualizar URLs de produção no modal para usar `add_flyingdonkeys_v2.php` e `add_webflow_octa_v2.php`

**Estratégia:**
- **NÃO criar versão separada** (evita duplicação)
- **Atualizar modal existente** para usar endpoints _v2 em produção
- **Manter detecção de ambiente** (já funciona corretamente)
- **Rollback simples:** Reverter modal para usar endpoints antigos (3 minutos)

**Ação (Tarefa 2.5 - CRÍTICA):**
- [ ] Baixar modal atual de produção para análise local
- [ ] Fazer backup do modal atual
- [ ] Atualizar função `getEndpointUrl()` para usar endpoints _v2 em produção
- [ ] Verificar se há outras referências hardcoded
- [ ] Deploy do modal atualizado
- [ ] Teste isolado do modal (verificar console - deve mostrar URLs com _v2)

**Ver detalhes completos em:** `RESPOSTA_DESENVOLVEDOR_REVISAO_MIGRACAO_V2.md` (Tarefa 2.5)

---

### **2. SafetyMails - Credenciais de Produção**

**Ação Necessária:**
- [ ] Acessar painel SafetyMails
- [ ] Criar nova origem de produção
- [ ] Obter Ticket Origem de produção
- [ ] Obter API Key de produção
- [ ] Autorizar domínio de produção
- [ ] Atualizar credenciais no `FooterCodeSiteDefinitivoCompleto_prod.js`

**Documentação:**
- Ver: `02-DEVELOPMENT/DOCUMENTACAO_MIGRACAO_PRODUCAO_SAFETYMAILS.md`

---

### **3. Apilayer - Validação de Telefone**

**Verificação:**
- [ ] Confirmar se API Key é a mesma para DEV e PROD
- [ ] Se não, obter key de produção
- [ ] Atualizar no `FooterCodeSiteDefinitivoCompleto_prod.js` (se necessário)

---

### **4. RPA Script**

**Verificação:**
- [ ] Verificar se script RPA é o mesmo para DEV e PROD
- [ ] Verificar URL do script RPA em produção
- [ ] Atualizar se necessário no `FooterCodeSiteDefinitivoCompleto_prod.js`

---

### **5. Sistema de Logging**

**Verificação:**
- [ ] Verificar se endpoint de logging é o mesmo para DEV e PROD
- [ ] Verificar se há configurações específicas de produção
- [ ] Atualizar se necessário

---

### **6. Head Code do Webflow**

**Verificação:**
- [ ] Verificar se há código no Head Code do Webflow que precisa ser atualizado
- [ ] Verificar se há referências a `Inside Head Tag Pagina.js` (já integrado no arquivo unificado)
- [ ] Se houver código no Head Code, verificar se precisa ser removido/atualizado

---

## 📊 MATRIZ DE DEPENDÊNCIAS

| Tarefa | Depende de | Bloqueia |
|--------|------------|----------|
| Tarefa 2.1 | Tarefa 1.1 | Tarefa 3.1, 4.3, 5.1 |
| Tarefa 2.2 | Tarefa 2.1 | Tarefa 5.1 |
| Tarefa 2.3 | Tarefa 1.1, Obter credenciais | Tarefa 4.1, 3.1 |
| Tarefa 2.4 | Tarefa 1.1, Obter credenciais | Tarefa 4.2, 3.1 |
| Tarefa 3.1 | Tarefa 2.1, 2.3, 2.4 | Tarefa 6.2 |
| Tarefa 4.1 | Tarefa 2.3 | Tarefa 6.1 |
| Tarefa 4.2 | Tarefa 2.4 | Tarefa 6.1 |
| Tarefa 4.3 | Tarefa 2.1 | Tarefa 6.1 |
| Tarefa 5.1 | Tarefa 2.2, 4.3 | Tarefa 6.2 |
| Tarefa 6.1 | Tarefa 4.1, 4.2, 4.3 | Tarefa 6.2 |
| Tarefa 6.2 | Todas as anteriores | Conclusão |

---

## ⚠️ RISCOS E MITIGAÇÕES

### **Risco 1: Quebra de Funcionalidades Existentes**
- **Mitigação:** ✅ **Endpoints paralelos** - arquivos antigos não serão alterados
- **Mitigação:** ✅ **Rollback instantâneo** - apenas reverter referências no frontend (3-5 min)
- **Mitigação:** Testes extensivos antes de fazer deploy em produção
- **Mitigação:** Deploy gradual (ativar frontend apenas após validar endpoints _v2)

### **Risco 2: Credenciais Incorretas**
- **Mitigação:** Obter credenciais diretamente dos arquivos de produção
- **Mitigação:** Validar credenciais antes de fazer deploy
- **Mitigação:** Testar endpoints com credenciais antes de usar

### **Risco 3: Problemas de CORS**
- **Mitigação:** Verificar configurações de CORS nos novos arquivos
- **Mitigação:** Testar requisições cross-origin antes de deploy
- **Mitigação:** Manter configurações de CORS baseadas nos arquivos de produção existentes

### **Risco 4: Endpoints Não Funcionais**
- **Mitigação:** ✅ **Endpoints antigos permanecem funcionando** - sempre disponíveis como fallback
- **Mitigação:** Validar novos endpoints _v2 antes de atualizar referências no frontend
- **Mitigação:** Testar todos os endpoints após deploy
- **Mitigação:** **Rollback = apenas atualizar modal para usar endpoints antigos** (3 minutos)

---

## 📋 CHECKLIST FINAL DE VALIDAÇÃO

### **Pré-Deploy:**
- [ ] Todos os backups criados
- [ ] Todos os arquivos de produção criados
- [ ] Credenciais de produção obtidas e documentadas
- [ ] Endpoints validados
- [ ] CORS configurado corretamente
- [ ] URLs atualizadas (sem referências a dev)
- [ ] Chamadas a travelangels.com.br removidas

### **Deploy:**
- [ ] Arquivos PHP copiados para servidor
- [ ] Arquivo JavaScript copiado para servidor
- [ ] Permissões corretas
- [ ] Arquivos acessíveis via HTTP
- [ ] Webflow atualizado

### **Pós-Deploy:**
- [ ] Testes funcionais completos
- [ ] Validação de endpoints
- [ ] Verificação de logs
- [ ] Monitoramento nas primeiras 24h
- [ ] Documentação atualizada

---

## 📝 NOTAS IMPORTANTES

1. **Nunca commitar credenciais de produção no GitHub**
2. **✅ Endpoints paralelos:** Arquivos antigos **NÃO serão alterados** - sempre disponíveis como backup
3. **✅ Rollback simplificado:** Apenas reverter referências no frontend (3-5 minutos)
4. **Testar novos endpoints _v2 isoladamente antes de ativar no frontend**
5. **Monitorar logs após deploy**
6. **Documentar data/hora do deploy**
7. **Endpoints antigos podem permanecer indefinidamente como rede de segurança**

---

## 🔗 ARQUIVOS DE REFERÊNCIA

- `02-DEVELOPMENT/DOCUMENTACAO_MIGRACAO_PRODUCAO_SAFETYMAILS.md` - Migração SafetyMails
- `02-DEVELOPMENT/VERIFICACAO_ENDPOINTS_SERVIDOR.md` - Endpoints no servidor
- `02-DEVELOPMENT/ESPECIFICACAO_REGISTRO_CONVERSOES_E_ENDPOINTS.md` - Especificação de endpoints
- `PROJETOS_imediatoseguros-rpa-playwright.md` - Controle de projetos
- `DIRETIVAS_PROJETOS.md` - Diretivas de gerenciamento

---

## 📅 CRONOGRAMA SUGERIDO

**Fase 1 (Preparação):** ~30 minutos  
**Fase 2 (Criação de Arquivos):** ~3-4 horas  
**Fase 3 (Atualização de Referências):** ~1 hora  
**Fase 4 (Deploy):** ~30 minutos  
**Fase 5 (Webflow):** ~15 minutos  
**Fase 6 (Validação):** ~2-3 horas  

**Total Estimado:** ~6-8 horas

---

**Status:** 🟡 **PLANEJADO - AGUARDANDO REVISÃO E APROVAÇÃO**  
**Próxima Ação:** Revisar plano, obter credenciais de produção, iniciar execução

---

## 🔍 REVISÃO TÉCNICA

**Revisor:** Engenheiro de Produção - Especialista em Migrações  
**Data da Revisão:** 01/11/2025 14:30  
**Documento Completo:** `REVISAO_TECNICA_MIGRACAO_PRODUCAO.md`

### **Resumo Executivo:**

**Status da Revisão:** ⚠️ **REQUER ALTERAÇÕES ANTES DE APROVAÇÃO**

**Pontuação Geral:** 7/10

**Principais Lacunas Identificadas:**

1. **🔴 CRÍTICO:** Dependência do `MODAL_WHATSAPP_DEFINITIVO.js` não resolvida (pode quebrar todo o fluxo)
2. **🔴 CRÍTICO:** Ausência de procedimento de rollback detalhado
3. **🟡 IMPORTANTE:** Falta validação de credenciais antes do deploy
4. **🟡 IMPORTANTE:** Backup de arquivos de produção não documentado
5. **🟡 IMPORTANTE:** Estratégia de deploy gradual não definida

**Recomendações Prioritárias:**
- Resolver dependência do MODAL antes de qualquer deploy
- Criar seção completa de ROLLBACK PROCEDURES
- Adicionar validação de credenciais como tarefa obrigatória
- Implementar backup de produção antes de alterações
- Definir estratégia de deploy gradual

**Ver revisão completa em:** `02-DEVELOPMENT/REVISAO_TECNICA_MIGRACAO_PRODUCAO.md`

