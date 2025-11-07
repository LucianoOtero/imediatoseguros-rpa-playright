# 🏗️ PROPOSTA DE ESTRUTURA DE DIRETÓRIOS - FOOTER CODES WEBFLOW

**Data de Criação:** 05/11/2025  
**Versão:** 1.1  
**Status:** Proposta Atualizada

---

## 📋 OBJETIVOS DA ESTRUTURA

1. ✅ **Separação Clara DEV/PROD:** Identificação imediata do ambiente
2. ✅ **Organização por Tipo:** JavaScript, PHP, Configurações separados
3. ✅ **Nomenclatura Consistente:** Nomes originais mantidos, identificação por diretórios
4. ✅ **Versionamento Claro:** Versões identificáveis nos nomes (quando aplicável)
5. ✅ **Backups Organizados:** Histórico acessível e datado
6. ✅ **Escalabilidade:** Estrutura que cresce sem confusão

---

## 🏷️ IDENTIFICAÇÃO DO PROJETO

### **Projeto Webflow/Website (segurosimediato.com.br):**

- **Diretório Raiz:** `01-WEBFLOW-WEBSITE/`
- **Identificação:** Todos os arquivos dentro deste diretório são do projeto Webflow/Website
- **Nomes dos arquivos:** Mantidos originais (sem prefixos ou modificações)
- **Objetivo:** Organizar arquivos que suportam o website segurosimediato.com.br no Webflow

**Exemplos de Localização:**
- `01-WEBFLOW-WEBSITE/02-DEVELOPMENT/javascript/footer-code/DEV/FooterCodeSiteDefinitivoCompleto.js`
- `01-WEBFLOW-WEBSITE/02-DEVELOPMENT/javascript/modal/PROD/MODAL_WHATSAPP_DEFINITIVO.js`
- `01-WEBFLOW-WEBSITE/02-DEVELOPMENT/php/endpoints/PROD/add_flyingdonkeys_v2.php`

**⚠️ NOTA:** Arquivos relacionados ao projeto RPA permanecem na estrutura atual e serão organizados posteriormente.

---

## 📁 ESTRUTURA PROPOSTA

```
imediatoseguros-rpa-playwright/
│
├── 01-WEBFLOW-WEBSITE/                        🌐 PROJETO WEBFLOW/WEBSITE
│   │
│   ├── 02-DEVELOPMENT/
│   │   │
│   │   ├── javascript/
│   │   │   │
│   │   │   ├── footer-code/
│   │   │   │   ├── DEV/
│   │   │   │   │   ├── FooterCodeSiteDefinitivoCompleto.js      ✅ Arquivo unificado DEV (nome original)
│   │   │   │   │   ├── FooterCodeSiteDefinitivoCompleto.js.backup_YYYYMMDD_HHMMSS
│   │   │   │   │   └── FooterCodeSiteDefinitivoCompleto_latest.js 🔗 Link simbólico
│   │   │   │   │
│   │   │   │   ├── PROD/
│   │   │   │   │   ├── FooterCodeSiteDefinitivoCompleto_prod.js ✅ Arquivo unificado PROD (nome original)
│   │   │   │   │   ├── FooterCodeSiteDefinitivoCompleto_prod.js.backup_YYYYMMDD_HHMMSS
│   │   │   │   │   └── FooterCodeSiteDefinitivoCompleto_prod_latest.js 🔗 Link simbólico
│   │   │   │   │
│   │   │   │   └── LEGACY/
│   │   │   │       ├── Footer Code Site Definitivo.js           📦 Versão antiga (nome original)
│   │   │   │       ├── FooterCodeSiteDefinitivoUtils.js         📦 Utils separado (nome original)
│   │   │   │       └── README_LEGACY.md                         📝 Documentação
│   │   │   │
│   │   │   ├── modal/
│   │   │   │   ├── DEV/
│   │   │   │   │   ├── MODAL_WHATSAPP_DEFINITIVO.js             ✅ Modal DEV (nome original)
│   │   │   │   │   ├── MODAL_WHATSAPP_DEFINITIVO.js.backup_YYYYMMDD_HHMMSS
│   │   │   │   │   └── MODAL_WHATSAPP_DEFINITIVO_latest.js     🔗 Link simbólico
│   │   │   │   │
│   │   │   │   ├── PROD/
│   │   │   │   │   ├── MODAL_WHATSAPP_DEFINITIVO.js             ✅ Modal PROD (nome original)
│   │   │   │   │   ├── MODAL_WHATSAPP_DEFINITIVO.js.backup_YYYYMMDD_HHMMSS
│   │   │   │   │   └── MODAL_WHATSAPP_DEFINITIVO_latest.js     🔗 Link simbólico
│   │   │   │   │
│   │   │   │   └── LEGACY/
│   │   │   │       └── MODAL_WHATSAPP_DEFINITIVO.js             📦 Versão antiga (nome original)
│   │   │   │
│   │   │   └── utils/
│   │   │       ├── FooterCodeSiteDefinitivoUtils.js             🛠️ Utilitários (nome original)
│   │   │       └── FooterCodeSiteDefinitivoUtils.js.backup_YYYYMMDD_HHMMSS
│   │   │
│   │   ├── php/
│   │   │   │
│   │   │   ├── endpoints/
│   │   │   │   ├── DEV/
│   │   │   │   │   ├── add_travelangels_dev.php                ✅ EspoCRM DEV (nome original)
│   │   │   │   │   ├── add_webflow_octa_dev.php                ✅ OctaDesk DEV (nome original)
│   │   │   │   │   └── send_email_notification_endpoint.php    ✅ Email DEV (nome original)
│   │   │   │   │
│   │   │   │   └── PROD/
│   │   │   │       ├── add_flyingdonkeys_v2.php                ✅ EspoCRM PROD (nome original)
│   │   │   │       ├── add_webflow_octa_v2.php                 ✅ OctaDesk PROD (nome original)
│   │   │   │       └── send_email_notification_endpoint.php    ✅ Email PROD (nome original)
│   │   │   │
│   │   │   └── config/
│   │   │       ├── aws_ses_config.php                          ⚙️ Configuração AWS (nome original)
│   │   │       ├── aws_ses_config.example.php                  📋 Template (nome original)
│   │   │       ├── send_admin_notification_ses.php             📋 Notificação SES (nome original)
│   │   │       └── README_CONFIG.md                             📝 Documentação
│   │   │
│   │   └── webflow-codes/
│   │       │
│   │       ├── DEV/
│   │       │   ├── Footer Code Site Definitivo WEBFLOW.js      📋 Código Webflow DEV (nome original)
│   │       │   └── Footer Code Site Definitivo WEBFLOW_latest.js 🔗 Link simbólico
│   │       │
│   │       └── PROD/
│   │           ├── Footer Code Site Definitivo WEBFLOW_prod.js 📋 Código Webflow PROD (nome original)
│   │           └── Footer Code Site Definitivo WEBFLOW_prod_latest.js 🔗 Link simbólico
│   │
│   ├── 03-PRODUCTION/
│   │   │
│   │   ├── javascript/
│   │   │   ├── FooterCodeSiteDefinitivoCompleto_prod.js         ✅ Versão em produção (nome original)
│   │   │   ├── MODAL_WHATSAPP_DEFINITIVO.js                     ✅ Versão em produção (nome original)
│   │   │   └── README_PRODUCTION.md                              📝 Status de produção
│   │   │
│   │   └── php/
│   │       ├── add_flyingdonkeys_v2.php                         ✅ Versão em produção (nome original)
│   │       ├── add_webflow_octa_v2.php                          ✅ Versão em produção (nome original)
│   │       └── send_email_notification_endpoint.php             ✅ Versão em produção (nome original)
│   │
│   └── 04-BACKUPS/
│       │
│       ├── YYYY-MM-DD/
│       │   ├── DEV/
│       │   │   ├── FooterCodeSiteDefinitivoCompleto.js
│       │   │   └── MODAL_WHATSAPP_DEFINITIVO.js
│       │   │
│       │   └── PROD/
│       │       ├── FooterCodeSiteDefinitivoCompleto_prod.js
│       │       └── MODAL_WHATSAPP_DEFINITIVO.js
│       │
│       └── README_BACKUPS.md                                     📝 Política de backups
│
└── 05-DOCUMENTATION/
    ├── ARQUITETURA_FOOTER_CODES_WEBFLOW_DEV_PROD.md             📚 Arquitetura Webflow
    ├── DEPLOYMENT_GUIDE_WEBFLOW.md                              📚 Guia de deploy Webflow
    ├── ROLLBACK_GUIDE_WEBFLOW.md                                📚 Guia de rollback Webflow
    └── NAMING_CONVENTIONS.md                                     📚 Convenções de nomenclatura
```

---

## 🏷️ CONVENÇÕES DE NOMENCLATURA

### **Convenções de Nomenclatura:**

#### **1. Nomes dos Arquivos:**
- ✅ **MANTIDOS ORIGINAIS** (sem prefixos ou modificações)
- ✅ Identificação do projeto feita apenas pela localização no diretório

#### **2. Estrutura de Diretórios:**
- `01-WEBFLOW-WEBSITE/` = Todos os arquivos dentro são do projeto Webflow/Website (segurosimediato.com.br)

#### **3. Subdiretórios por Ambiente:**
- `DEV/` = Desenvolvimento
- `PROD/` = Produção
- `LEGACY/` = Versão antiga/legado

#### **4. Links Simbólicos (opcional):**
- `[arquivo]_latest.js` = Link simbólico para versão mais recente
- Exemplo: `FooterCodeSiteDefinitivoCompleto_latest.js`

#### **5. Backups:**
- `.backup_YYYYMMDD_HHMMSS` = Backup com timestamp
- Exemplo: `FooterCodeSiteDefinitivoCompleto.js.backup_20251105_143022`

### **Exemplos de Localização:**

#### **Arquivos Webflow/Website (nomes originais mantidos):**
- `01-WEBFLOW-WEBSITE/02-DEVELOPMENT/javascript/footer-code/DEV/FooterCodeSiteDefinitivoCompleto.js`
- `01-WEBFLOW-WEBSITE/02-DEVELOPMENT/javascript/footer-code/PROD/FooterCodeSiteDefinitivoCompleto_prod.js`
- `01-WEBFLOW-WEBSITE/02-DEVELOPMENT/javascript/modal/PROD/MODAL_WHATSAPP_DEFINITIVO.js`
- `01-WEBFLOW-WEBSITE/02-DEVELOPMENT/php/endpoints/PROD/add_flyingdonkeys_v2.php`


---

## 📊 MAPEAMENTO DE ARQUIVOS ATUAIS → NOVA ESTRUTURA

### **JavaScript (Projeto Webflow/Website):**

| **Arquivo Atual** | **Nova Localização** | **Nome Mantido** |
|-------------------|---------------------|------------------|
| `FooterCodeSiteDefinitivoCompleto.js` (servidor DEV) | `01-WEBFLOW-WEBSITE/02-DEVELOPMENT/javascript/footer-code/DEV/` | `FooterCodeSiteDefinitivoCompleto.js` ✅ |
| `FooterCodeSiteDefinitivoCompleto_prod.js` | `01-WEBFLOW-WEBSITE/02-DEVELOPMENT/javascript/footer-code/PROD/` | `FooterCodeSiteDefinitivoCompleto_prod.js` ✅ |
| `Footer Code Site Definitivo.js` | `01-WEBFLOW-WEBSITE/02-DEVELOPMENT/javascript/footer-code/LEGACY/` | `Footer Code Site Definitivo.js` ✅ |
| `FooterCodeSiteDefinitivoUtils.js` | `01-WEBFLOW-WEBSITE/02-DEVELOPMENT/javascript/utils/` | `FooterCodeSiteDefinitivoUtils.js` ✅ |
| `MODAL_WHATSAPP_DEFINITIVO.js` | `01-WEBFLOW-WEBSITE/02-DEVELOPMENT/javascript/modal/PROD/` | `MODAL_WHATSAPP_DEFINITIVO.js` ✅ |
| `Footer Code Site Definitivo WEBFLOW.js` | `01-WEBFLOW-WEBSITE/02-DEVELOPMENT/javascript/webflow-codes/DEV/` | `Footer Code Site Definitivo WEBFLOW.js` ✅ |
| `Footer Code Site Definitivo WEBFLOW_prod.js` | `01-WEBFLOW-WEBSITE/02-DEVELOPMENT/javascript/webflow-codes/PROD/` | `Footer Code Site Definitivo WEBFLOW_prod.js` ✅ |

### **PHP (Projeto Webflow/Website):**

| **Arquivo Atual** | **Nova Localização** | **Nome Mantido** |
|-------------------|---------------------|------------------|
| `add_travelangels_dev.php` | `01-WEBFLOW-WEBSITE/02-DEVELOPMENT/php/endpoints/DEV/` | `add_travelangels_dev.php` ✅ |
| `add_flyingdonkeys_v2.php` | `01-WEBFLOW-WEBSITE/02-DEVELOPMENT/php/endpoints/PROD/` | `add_flyingdonkeys_v2.php` ✅ |
| `add_webflow_octa_dev.php` | `01-WEBFLOW-WEBSITE/02-DEVELOPMENT/php/endpoints/DEV/` | `add_webflow_octa_dev.php` ✅ |
| `add_webflow_octa_v2.php` | `01-WEBFLOW-WEBSITE/02-DEVELOPMENT/php/endpoints/PROD/` | `add_webflow_octa_v2.php` ✅ |
| `send_email_notification_endpoint.php` | `01-WEBFLOW-WEBSITE/02-DEVELOPMENT/php/endpoints/PROD/` | `send_email_notification_endpoint.php` ✅ |
| `send_admin_notification_ses.php` | `01-WEBFLOW-WEBSITE/02-DEVELOPMENT/php/config/` | `send_admin_notification_ses.php` ✅ |
| `aws_ses_config.php` | `01-WEBFLOW-WEBSITE/02-DEVELOPMENT/php/config/` | `aws_ses_config.php` ✅ |

---

## 🎯 BENEFÍCIOS DA ESTRUTURA

### **1. Identificação Imediata:**
- ✅ Nome do arquivo indica ambiente (DEV/PROD)
- ✅ Versão visível no nome
- ✅ Tipo de arquivo identificável pelo radical

### **2. Organização Lógica:**
- ✅ Separação por tipo (JavaScript, PHP, Config)
- ✅ Separação por ambiente (DEV, PROD, LEGACY)
- ✅ Backups organizados por data

### **3. Manutenção Simplificada:**
- ✅ Fácil localizar arquivos
- ✅ Versões claramente identificadas
- ✅ Histórico acessível

### **4. Deploy Controlado:**
- ✅ Arquivos PROD isolados
- ✅ Testes em DEV sem risco
- ✅ Rollback facilitado

---

## 📋 EXEMPLOS DE USO

### **Exemplo 1: Criar Nova Versão DEV**

```bash
# 1. Desenvolver nova versão
cp FooterCode_DEV_v1.5.0.js FooterCode_DEV_v1.6.0.js

# 2. Fazer backup da versão anterior
cp FooterCode_DEV_v1.5.0.js 04-BACKUPS/$(date +%Y-%m-%d)/DEV/FooterCode_DEV_v1.5.0.js

# 3. Atualizar link simbólico
ln -sf FooterCode_DEV_v1.6.0.js FooterCode_DEV_latest.js
```

### **Exemplo 2: Deploy para Produção**

```bash
# 1. Copiar versão testada de DEV para PROD
cp 02-DEVELOPMENT/javascript/footer-code/DEV/FooterCode_DEV_v1.6.0.js \
   02-DEVELOPMENT/javascript/footer-code/PROD/FooterCode_PROD_v1.4.0.js

# 2. Fazer backup da versão PROD atual
cp 03-PRODUCTION/javascript/FooterCode_PROD_v1.3.0.js \
   04-BACKUPS/$(date +%Y-%m-%d)/PROD/FooterCode_PROD_v1.3.0.js

# 3. Copiar para produção
scp FooterCode_PROD_v1.4.0.js root@server:/var/www/html/webhooks/
```

### **Exemplo 3: Rollback**

```bash
# 1. Localizar backup
ls 04-BACKUPS/2025-11-04/PROD/

# 2. Restaurar versão anterior
cp 04-BACKUPS/2025-11-04/PROD/FooterCode_PROD_v1.3.0.js \
   03-PRODUCTION/javascript/FooterCode_PROD_v1.3.0.js

# 3. Deploy para servidor
scp FooterCode_PROD_v1.3.0.js root@server:/var/www/html/webhooks/
```

---

## 🔄 FLUXO DE TRABALHO

### **Desenvolvimento:**
```
1. Desenvolver em: 02-DEVELOPMENT/javascript/footer-code/DEV/
2. Testar localmente
3. Criar backup antes de alterações
4. Atualizar versão no nome do arquivo
5. Atualizar link _latest.js
```

### **Deploy DEV:**
```
1. Copiar para servidor DEV
2. Testar em ambiente DEV
3. Validar funcionalidades
4. Documentar alterações
```

### **Deploy PROD:**
```
1. Copiar versão testada para PROD/
2. Criar backup da versão atual em produção
3. Copiar para servidor PROD
4. Monitorar por 24-48h
5. Documentar deploy
```

---

## ✅ CHECKLIST DE MIGRAÇÃO

### **Fase 1: Criar Estrutura**
- [ ] Criar diretórios principais
- [ ] Criar subdiretórios DEV/PROD/LEGACY
- [ ] Criar diretório de backups

### **Fase 2: Migrar Arquivos**
- [ ] Mover arquivos JavaScript para nova estrutura
- [ ] Renomear arquivos conforme convenções
- [ ] Mover arquivos PHP para nova estrutura
- [ ] Organizar backups existentes

### **Fase 3: Atualizar Documentação**
- [ ] Atualizar referências em documentos
- [ ] Criar guia de nomenclatura
- [ ] Atualizar scripts de deploy

### **Fase 4: Validar**
- [ ] Verificar todos os arquivos migrados
- [ ] Testar links simbólicos
- [ ] Validar estrutura de backups
- [ ] Documentar processo de migração

---

## 📝 NOTAS IMPORTANTES

1. **Links Simbólicos:** Usar `_latest.js` para facilitar referências
2. **Versionamento:** Sempre atualizar versão no nome ao fazer alterações
3. **Backups:** Criar backup antes de qualquer alteração significativa
4. **Documentação:** Manter README atualizado em cada diretório
5. **Consistência:** Seguir convenções rigorosamente para evitar confusão

---

**Documento criado em:** 05/11/2025  
**Versão:** 1.0  
**Status:** Proposta para Aprovação

