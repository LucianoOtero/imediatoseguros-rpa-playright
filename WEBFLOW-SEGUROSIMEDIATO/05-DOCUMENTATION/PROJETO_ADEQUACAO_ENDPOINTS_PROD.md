# PROJETO: ADEQUAÇÃO DE ENDPOINTS E REFERÊNCIAS PARA PRODUÇÃO

**DATA DE CRIAÇÃO:** 06/11/2025  
**ÚLTIMA ATUALIZAÇÃO:** 06/11/2025  
**STATUS:** 🔴 PENDENTE

---

## 📋 OBJETIVO

Adequar os arquivos `FooterCodeSiteDefinitivoCompleto_prod.js` e `MODAL_WHATSAPP_DEFINITIVO_prod.js` no diretório `03-PRODUCTION` para usar endpoints e referências `_prod` ao invés de `_dev`, garantindo que os arquivos de produção estejam corretamente configurados.

---

## 🎯 ESCOPO

### Arquivos a Modificar:
1. `WEBFLOW-SEGUROSIMEDIATO/03-PRODUCTION/FooterCodeSiteDefinitivoCompleto_prod.js`
2. `WEBFLOW-SEGUROSIMEDIATO/03-PRODUCTION/MODAL_WHATSAPP_DEFINITIVO_prod.js`

---

## 📝 LISTA DETALHADA DE ALTERAÇÕES

### **1. FooterCodeSiteDefinitivoCompleto_prod.js**

#### **1.1 Cabeçalho do Arquivo**

| Linha | Tipo | Atual | Novo | Observação |
|-------|------|-------|------|------------|
| 26 | Comentário | `MODAL_WHATSAPP_DEFINITIVO_dev.js` | `MODAL_WHATSAPP_DEFINITIVO_prod.js` | Referência em comentário |
| 69 | Comentário | `https://dev.bpsegurosimediato.com.br/webhooks/FooterCodeSiteDefinitivoCompleto_dev.js` | `https://dev.bpsegurosimediato.com.br/webhooks/FooterCodeSiteDefinitivoCompleto_prod.js` | Localização do arquivo (mesmo diretório, apenas sufixo muda) |
| 71 | Comentário | `⚠️ AMBIENTE: DESENVOLVIMENTO` | `⚠️ AMBIENTE: PRODUÇÃO` | Ambiente |
| 72 | Comentário | `SafetyMails Ticket: fc5e18c10c4aa883b2c31a305f1c09fea3834138` | `SafetyMails Ticket: 9bab7f0c2711c5accfb83588c859dc1103844a94` | Ticket de produção |
| 98 | Comentário | `⚠️ AMBIENTE: DESENVOLVIMENTO` | `⚠️ AMBIENTE: PRODUÇÃO` | Ambiente |

#### **1.2 Constantes Globais**

| Linha | Tipo | Atual | Novo | Observação |
|-------|------|-------|------|------------|
| 101 | Código | `window.SAFETY_TICKET = 'fc5e18c10c4aa883b2c31a305f1c09fea3834138'` | `window.SAFETY_TICKET = '9bab7f0c2711c5accfb83588c859dc1103844a94'` | Ticket de produção |

#### **1.3 Função loadWhatsAppModal()**

| Linha | Tipo | Atual | Novo | Observação |
|-------|------|-------|------|------------|
| 1293 | Log | `'🔄 Carregando modal de dev.bpsegurosimediato.com.br...'` | `'🔄 Carregando modal de dev.bpsegurosimediato.com.br...'` | Mensagem de log (manter domínio, apenas mudar sufixo) |
| 1295 | URL | `'https://dev.bpsegurosimediato.com.br/webhooks/MODAL_WHATSAPP_DEFINITIVO_dev.js?v=24&force='` | `'https://dev.bpsegurosimediato.com.br/webhooks/MODAL_WHATSAPP_DEFINITIVO_prod.js?v=24&force='` | URL do modal (mesmo diretório, apenas sufixo muda) |

---

### **2. MODAL_WHATSAPP_DEFINITIVO_prod.js**

#### **2.1 Cabeçalho do Arquivo**

| Linha | Tipo | Atual | Novo | Observação |
|-------|------|-------|------|------------|
| 18 | Comentário | `FooterCodeSiteDefinitivoCompleto_dev.js` | `FooterCodeSiteDefinitivoCompleto_prod.js` | Referência em comentário |
| 23 | Comentário | `FooterCodeSiteDefinitivoCompleto_dev.js` | `FooterCodeSiteDefinitivoCompleto_prod.js` | Referência em comentário |
| 24 | Comentário | `add_travelangels_dev.php` | `add_flyingdonkeys_prod.php` | Referência em comentário |
| 2300 | Comentário | `FooterCodeSiteDefinitivoCompleto_dev.js` | `FooterCodeSiteDefinitivoCompleto_prod.js` | Referência em comentário |

#### **2.2 Função getEndpointUrl() - Hardcode para webflow.io**

| Linha | Tipo | Atual | Novo | Observação |
|-------|------|-------|------|------------|
| 171 | URL | `'https://bpsegurosimediato.com.br/dev/webhooks/add_travelangels_dev.php'` | `'https://bpsegurosimediato.com.br/webhooks/add_flyingdonkeys_prod.php'` | Endpoint TravelAngels |
| 172 | URL | `'https://bpsegurosimediato.com.br/dev/webhooks/add_webflow_octa_dev.php'` | `'https://bpsegurosimediato.com.br/webhooks/add_webflow_octa_prod.php'` | Endpoint Octadesk |

#### **2.3 Função getEndpointUrl() - Endpoints DEV**

| Linha | Tipo | Atual | Novo | Observação |
|-------|------|-------|------|------------|
| 184 | URL | `dev: 'https://bpsegurosimediato.com.br/dev/webhooks/add_travelangels_dev.php'` | `dev: 'https://dev.bpsegurosimediato.com.br/webhooks/add_flyingdonkeys_dev.php'` | Endpoint DEV TravelAngels |
| 188 | URL | `dev: 'https://bpsegurosimediato.com.br/dev/webhooks/add_webflow_octa_dev.php'` | `dev: 'https://dev.bpsegurosimediato.com.br/webhooks/add_webflow_octa_dev.php'` | Endpoint DEV Octadesk |

**NOTA:** Os endpoints DEV devem continuar apontando para `dev.bpsegurosimediato.com.br`, mas o endpoint TravelAngels DEV deve usar `add_flyingdonkeys_dev.php` ao invés de `add_travelangels_dev.php` (se existir).

#### **2.4 Função sendAdminEmailNotification()**

| Linha | Tipo | Atual | Novo | Observação |
|-------|------|-------|------|------------|
| 756 | URL | `'https://dev.bpsegurosimediato.com.br/webhooks/send_email_notification_endpoint_dev.php'` | `'https://dev.bpsegurosimediato.com.br/webhooks/send_email_notification_endpoint_dev.php'` | **MANTER** (DEV continua DEV) |
| 757 | URL | `'https://bpsegurosimediato.com.br/webhooks/send_email_notification_endpoint_prod.php'` | `'https://bpsegurosimediato.com.br/webhooks/send_email_notification_endpoint_prod.php'` | **VERIFICAR** (já está correto?) |

**NOTA:** A linha 757 já deve estar correta, mas vamos verificar durante a implementação.

---

## 🔧 FASES DE IMPLEMENTAÇÃO

### **FASE 1: BACKUP DOS ARQUIVOS PROD**

**Objetivo:** Criar backups dos arquivos PROD antes de qualquer modificação.

**Ações:**
1. Criar diretório de backup com timestamp: `WEBFLOW-SEGUROSIMEDIATO/04-BACKUPS/ADEQUACAO_ENDPOINTS_PROD_YYYYMMDD_HHMMSS/`
2. Copiar `FooterCodeSiteDefinitivoCompleto_prod.js` para backup
3. Copiar `MODAL_WHATSAPP_DEFINITIVO_prod.js` para backup
4. Verificar integridade dos backups

---

### **FASE 2: MODIFICAÇÕES NO FooterCodeSiteDefinitivoCompleto_prod.js**

**Objetivo:** Atualizar todas as referências DEV para PROD no FooterCode.

**Ações:**
1. Atualizar cabeçalho (linhas 26, 69, 71-72, 98)
2. Atualizar constante `SAFETY_TICKET` (linha 101)
3. Atualizar função `loadWhatsAppModal()` (linhas 1293, 1295)
4. Verificar se não há outras referências DEV no arquivo

---

### **FASE 3: MODIFICAÇÕES NO MODAL_WHATSAPP_DEFINITIVO_prod.js**

**Objetivo:** Atualizar todas as referências DEV para PROD no Modal.

**Ações:**
1. Atualizar cabeçalho (linhas 18, 23, 24, 2300)
2. Atualizar função `getEndpointUrl()` - hardcode webflow.io (linhas 171-172)
3. Atualizar função `getEndpointUrl()` - endpoints DEV (linhas 184, 188)
4. Verificar função `sendAdminEmailNotification()` (linhas 756-757)
5. Verificar se não há outras referências DEV no arquivo

---

### **FASE 4: VALIDAÇÃO E TESTES**

**Objetivo:** Garantir que todas as alterações foram aplicadas corretamente.

**Ações:**
1. Buscar por todas as ocorrências de `_dev.js` nos arquivos modificados (deve ser `_prod.js`)
2. Verificar se URLs de arquivos `.js` continuam em `dev.bpsegurosimediato.com.br` (mesmo diretório)
3. Verificar se endpoints PHP PROD apontam para `bpsegurosimediato.com.br` (sem `dev.`)
4. Verificar se endpoints PHP DEV apontam para `dev.bpsegurosimediato.com.br`
5. Verificar se todas as referências de arquivos `.js` usam sufixo `_prod`
6. Verificar se o `SAFETY_TICKET` está correto para produção

---

## ✅ CHECKLIST DE VALIDAÇÃO

- [ ] Backup criado com sucesso
- [ ] FooterCodeSiteDefinitivoCompleto_prod.js:
  - [ ] Cabeçalho atualizado
  - [ ] SAFETY_TICKET atualizado para produção
  - [ ] URL do modal atualizada para `_prod.js`
  - [ ] Logs atualizados
- [ ] MODAL_WHATSAPP_DEFINITIVO_prod.js:
  - [ ] Cabeçalho atualizado
  - [ ] Endpoints hardcoded atualizados
  - [ ] Endpoints DEV mantidos corretos
  - [ ] Endpoint de email verificado
- [ ] Nenhuma referência `_dev` restante nos arquivos `.js` PROD
- [ ] URLs de arquivos `.js` continuam em `dev.bpsegurosimediato.com.br` (mesmo diretório)
- [ ] Endpoints PHP PROD apontam para `bpsegurosimediato.com.br` (sem `dev.`)

---

## 📊 RESUMO DE ALTERAÇÕES

### **Total de Alterações:**

**FooterCodeSiteDefinitivoCompleto_prod.js:**
- **Cabeçalho:** 5 alterações
- **Constantes:** 1 alteração
- **Funções:** 2 alterações
- **TOTAL:** 8 alterações

**MODAL_WHATSAPP_DEFINITIVO_prod.js:**
- **Cabeçalho:** 4 alterações
- **Funções:** 4 alterações
- **TOTAL:** 8 alterações

**TOTAL GERAL:** 16 alterações

---

## ⚠️ OBSERVAÇÕES IMPORTANTES

1. **Arquivos JavaScript (.js):**
   - ✅ **IMPORTANTE:** Os arquivos `.js` de PROD e DEV estão no **MESMO diretório** no servidor (`/var/www/html/dev/webhooks/`)
   - ✅ A diferença é apenas no **SUFIXO** do nome do arquivo (`_prod` vs `_dev`)
   - ✅ URLs de arquivos `.js` continuam apontando para `dev.bpsegurosimediato.com.br/webhooks/`
   - ✅ Exemplo: `https://dev.bpsegurosimediato.com.br/webhooks/MODAL_WHATSAPP_DEFINITIVO_prod.js`

2. **Endpoints PHP:**
   - ✅ **DEV:** Apontam para `dev.bpsegurosimediato.com.br/webhooks/` com sufixo `_dev`
   - ✅ **PROD:** Apontam para `bpsegurosimediato.com.br/webhooks/` (sem `dev.`) com sufixo `_prod`
   - ✅ Exemplo DEV: `https://dev.bpsegurosimediato.com.br/webhooks/add_flyingdonkeys_dev.php`
   - ✅ Exemplo PROD: `https://bpsegurosimediato.com.br/webhooks/add_flyingdonkeys_prod.php`

3. **SafetyMails Ticket:** O ticket de produção é `9bab7f0c2711c5accfb83588c859dc1103844a94`.

4. **Validação:** Após as alterações, buscar por `_dev` nos arquivos `.js` PROD para garantir que não restaram referências incorretas. Os endpoints PHP DEV podem continuar sendo referenciados quando o ambiente for DEV.

---

## 🚀 PRÓXIMOS PASSOS

1. Executar FASE 1 (Backup)
2. Executar FASE 2 (Modificações FooterCode)
3. Executar FASE 3 (Modificações Modal)
4. Executar FASE 4 (Validação)
5. Documentar resultados

---

**CRIADO EM:** 06/11/2025  
**AUTOR:** Sistema de Gerenciamento de Projetos

