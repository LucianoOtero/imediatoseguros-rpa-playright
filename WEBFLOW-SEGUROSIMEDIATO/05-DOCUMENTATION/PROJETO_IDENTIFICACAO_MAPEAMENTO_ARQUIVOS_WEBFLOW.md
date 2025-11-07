# 📋 PROJETO: IDENTIFICAÇÃO E MAPEAMENTO DE ARQUIVOS WEBFLOW-WEBSITE

**Data de Criação:** 05/11/2025  
**Status:** Planejado  
**Versão:** 1.0

---

## 🎯 OBJETIVO

Identificar todos os arquivos relacionados ao projeto **Webflow/Website (segurosimediato.com.br)** no diretório atual e mapear cada arquivo para sua localização na nova estrutura proposta (`01-WEBFLOW-WEBSITE/`).

---

## 📊 INVENTÁRIO DE ARQUIVOS WEBFLOW-WEBSITE

### **1. JAVASCRIPT - FOOTER CODES**

#### **1.1 Arquivos Principais (DEV/PROD)**

| **Arquivo Atual** | **Tipo** | **Nova Localização** | **Observações** |
|-------------------|----------|---------------------|-----------------|
| `02-DEVELOPMENT/custom-codes/FooterCodeSiteDefinitivoCompleto_prod.js` | PROD | `01-WEBFLOW-WEBSITE/02-DEVELOPMENT/javascript/footer-code/PROD/FooterCodeSiteDefinitivoCompleto_prod.js` | Arquivo unificado PROD |
| `migration/migracao_debug_email_20251104_192051/FooterCodeSiteDefinitivoCompleto_prod.js` | PROD (backup) | `01-WEBFLOW-WEBSITE/04-BACKUPS/2025-11-04/PROD/FooterCodeSiteDefinitivoCompleto_prod.js` | Backup de migração |
| `02-DEVELOPMENT/custom-codes/Footer Code Site Definitivo.js` | LEGACY | `01-WEBFLOW-WEBSITE/02-DEVELOPMENT/javascript/footer-code/LEGACY/Footer Code Site Definitivo.js` | Versão antiga não unificada |
| `02-DEVELOPMENT/custom-codes/FooterCodeSiteDefinitivoUtils.js` | UTILS | `01-WEBFLOW-WEBSITE/02-DEVELOPMENT/javascript/utils/FooterCodeSiteDefinitivoUtils.js` | Funções utilitárias |

#### **1.2 Arquivos Webflow (Códigos para Webflow Dashboard)**

| **Arquivo Atual** | **Tipo** | **Nova Localização** | **Observações** |
|-------------------|----------|---------------------|-----------------|
| `02-DEVELOPMENT/custom-codes/Footer Code Site Definitivo WEBFLOW.js` | DEV | `01-WEBFLOW-WEBSITE/02-DEVELOPMENT/javascript/webflow-codes/DEV/Footer Code Site Definitivo WEBFLOW.js` | Código para Webflow DEV |
| `02-DEVELOPMENT/custom-codes/Footer Code Site Definitivo WEBFLOW_prod.js` | PROD | `01-WEBFLOW-WEBSITE/02-DEVELOPMENT/javascript/webflow-codes/PROD/Footer Code Site Definitivo WEBFLOW_prod.js` | Código para Webflow PROD |

#### **1.3 Arquivos Legados/Outros**

| **Arquivo Atual** | **Tipo** | **Nova Localização** | **Observações** |
|-------------------|----------|---------------------|-----------------|
| `02-DEVELOPMENT/custom-codes/Head code Site.js` | LEGACY | `01-WEBFLOW-WEBSITE/02-DEVELOPMENT/javascript/footer-code/LEGACY/Head code Site.js` | Arquivo legado |
| `02-DEVELOPMENT/custom-codes/Inside Head Tag Pagina.js` | LEGACY | `01-WEBFLOW-WEBSITE/02-DEVELOPMENT/javascript/footer-code/LEGACY/Inside Head Tag Pagina.js` | Arquivo legado |
| `Footer Code Site FINAL.js` | LEGACY | `01-WEBFLOW-WEBSITE/02-DEVELOPMENT/javascript/footer-code/LEGACY/Footer Code Site FINAL.js` | Arquivo legado na raiz |
| `Footer Code Site Definitivo backup tarefa 2.3.js` | LEGACY | `01-WEBFLOW-WEBSITE/02-DEVELOPMENT/javascript/footer-code/LEGACY/Footer Code Site Definitivo backup tarefa 2.3.js` | Arquivo legado na raiz |
| `Footer Code Site FINAL backup tarefa 2.3.js` | LEGACY | `01-WEBFLOW-WEBSITE/02-DEVELOPMENT/javascript/footer-code/LEGACY/Footer Code Site FINAL backup tarefa 2.3.js` | Arquivo legado na raiz |

---

### **2. JAVASCRIPT - MODAL WHATSAPP**

#### **2.1 Arquivos Principais**

| **Arquivo Atual** | **Tipo** | **Nova Localização** | **Observações** |
|-------------------|----------|---------------------|-----------------|
| `MODAL_WHATSAPP_DEFINITIVO.js` | PROD | `01-WEBFLOW-WEBSITE/02-DEVELOPMENT/javascript/modal/PROD/MODAL_WHATSAPP_DEFINITIVO.js` | Modal principal PROD |
| `migration/migracao_debug_email_20251104_192051/MODAL_WHATSAPP_DEFINITIVO.js` | PROD (backup) | `01-WEBFLOW-WEBSITE/04-BACKUPS/2025-11-04/PROD/MODAL_WHATSAPP_DEFINITIVO.js` | Backup de migração |

#### **2.2 Arquivos Legados/Versões Antigas**

| **Arquivo Atual** | **Tipo** | **Nova Localização** | **Observações** |
|-------------------|----------|---------------------|-----------------|
| `MODAL_WHATSAPP_DEFINITIVO.backup_20251030_120500.js` | LEGACY | `01-WEBFLOW-WEBSITE/02-DEVELOPMENT/javascript/modal/LEGACY/MODAL_WHATSAPP_DEFINITIVO.backup_20251030_120500.js` | Backup antigo |
| `MODAL_WHATSAPP_PROGRESSIVO_V2_FINAL.js` | LEGACY | `01-WEBFLOW-WEBSITE/02-DEVELOPMENT/javascript/modal/LEGACY/MODAL_WHATSAPP_PROGRESSIVO_V2_FINAL.js` | Versão antiga |
| `MODAL_WHATSAPP_PROGRESSIVO_HIBRIDO_V1.2.js` | LEGACY | `01-WEBFLOW-WEBSITE/02-DEVELOPMENT/javascript/modal/LEGACY/MODAL_WHATSAPP_PROGRESSIVO_HIBRIDO_V1.2.js` | Versão antiga |
| `MODAL_WHATSAPP_V2_APRIMORADO.js` | LEGACY | `01-WEBFLOW-WEBSITE/02-DEVELOPMENT/javascript/modal/LEGACY/MODAL_WHATSAPP_V2_APRIMORADO.js` | Versão antiga |

---

### **3. PHP - ENDPOINTS**

#### **3.1 Endpoints PROD**

| **Arquivo Atual** | **Tipo** | **Nova Localização** | **Observações** |
|-------------------|----------|---------------------|-----------------|
| `02-DEVELOPMENT/custom-codes/add_flyingdonkeys_v2.php` | PROD | `01-WEBFLOW-WEBSITE/02-DEVELOPMENT/php/endpoints/PROD/add_flyingdonkeys_v2.php` | Endpoint EspoCRM PROD |
| `02-DEVELOPMENT/custom-codes/add_flyingdonkeys_v2_GIT_VERSION.php` | PROD | `01-WEBFLOW-WEBSITE/02-DEVELOPMENT/php/endpoints/PROD/add_flyingdonkeys_v2_GIT_VERSION.php` | Versão com Git |
| `02-DEVELOPMENT/custom-codes/add_webflow_octa_v2.php` | PROD | `01-WEBFLOW-WEBSITE/02-DEVELOPMENT/php/endpoints/PROD/add_webflow_octa_v2.php` | Endpoint OctaDesk PROD |

#### **3.2 Endpoints DEV**

| **Arquivo Atual** | **Tipo** | **Nova Localização** | **Observações** |
|-------------------|----------|---------------------|-----------------|
| `02-DEVELOPMENT/patch_add_travelangels_dev.php` | DEV | `01-WEBFLOW-WEBSITE/02-DEVELOPMENT/php/endpoints/DEV/patch_add_travelangels_dev.php` | Patch DEV |
| `add_travelangels_v2.php` | DEV (raiz) | `01-WEBFLOW-WEBSITE/02-DEVELOPMENT/php/endpoints/DEV/add_travelangels_dev.php` | ⚠️ Renomear para padrão DEV |
| `add_travelangels_v3.php` | DEV (raiz) | `01-WEBFLOW-WEBSITE/02-DEVELOPMENT/php/endpoints/DEV/add_travelangels_v3.php` | Versão v3 DEV |

#### **3.3 Endpoints de Email**

| **Arquivo Atual** | **Tipo** | **Nova Localização** | **Observações** |
|-------------------|----------|---------------------|-----------------|
| `02-DEVELOPMENT/custom-codes/send_email_notification_endpoint.php` | PROD | `01-WEBFLOW-WEBSITE/02-DEVELOPMENT/php/endpoints/PROD/send_email_notification_endpoint.php` | Endpoint email PROD |
| `migration/migracao_debug_email_20251104_192051/send_email_notification_endpoint.php` | PROD (backup) | `01-WEBFLOW-WEBSITE/04-BACKUPS/2025-11-04/PROD/send_email_notification_endpoint.php` | Backup de migração |

---

### **4. PHP - CONFIGURAÇÕES**

| **Arquivo Atual** | **Tipo** | **Nova Localização** | **Observações** |
|-------------------|----------|---------------------|-----------------|
| `02-DEVELOPMENT/custom-codes/aws_ses_config.php` | CONFIG | `01-WEBFLOW-WEBSITE/02-DEVELOPMENT/php/config/aws_ses_config.php` | Configuração AWS SES |
| `02-DEVELOPMENT/custom-codes/aws_ses_config.example.php` | CONFIG | `01-WEBFLOW-WEBSITE/02-DEVELOPMENT/php/config/aws_ses_config.example.php` | Template de configuração |
| `02-DEVELOPMENT/custom-codes/send_admin_notification_ses.php` | CONFIG | `01-WEBFLOW-WEBSITE/02-DEVELOPMENT/php/config/send_admin_notification_ses.php` | Função de notificação SES |
| `migration/migracao_debug_email_20251104_192051/aws_ses_config.php` | CONFIG (backup) | `01-WEBFLOW-WEBSITE/04-BACKUPS/2025-11-04/PROD/aws_ses_config.php` | Backup de migração |
| `migration/migracao_debug_email_20251104_192051/send_admin_notification_ses.php` | CONFIG (backup) | `01-WEBFLOW-WEBSITE/04-BACKUPS/2025-11-04/PROD/send_admin_notification_ses.php` | Backup de migração |

---

### **5. BACKUPS**

#### **5.1 Backups em `02-DEVELOPMENT/backups/`**

| **Arquivo Atual** | **Nova Localização** | **Observações** |
|-------------------|---------------------|-----------------|
| `02-DEVELOPMENT/backups/FooterCodeSiteDefinitivoCompleto.js.backup_PROD_20251102_094203.js` | `01-WEBFLOW-WEBSITE/04-BACKUPS/2025-11-02/PROD/FooterCodeSiteDefinitivoCompleto.js.backup_PROD_20251102_094203.js` | Backup PROD |
| `02-DEVELOPMENT/backups/Footer Code Site Definitivo WEBFLOW.js.backup_PROD_20251102_094203.js` | `01-WEBFLOW-WEBSITE/04-BACKUPS/2025-11-02/PROD/Footer Code Site Definitivo WEBFLOW.js.backup_PROD_20251102_094203.js` | Backup Webflow |

#### **5.2 Backups em `02-DEVELOPMENT/custom-codes/`**

| **Arquivo Atual** | **Nova Localização** | **Observações** |
|-------------------|---------------------|-----------------|
| `02-DEVELOPMENT/custom-codes/Footer Code Site Definitivo.backup_20251028.js` | `01-WEBFLOW-WEBSITE/04-BACKUPS/2025-10-28/DEV/Footer Code Site Definitivo.backup_20251028.js` | Backup DEV |
| `02-DEVELOPMENT/custom-codes/Footer Code Site Definitivo.backup_20251029_123729.js` | `01-WEBFLOW-WEBSITE/04-BACKUPS/2025-10-29/DEV/Footer Code Site Definitivo.backup_20251029_123729.js` | Backup DEV |
| `02-DEVELOPMENT/custom-codes/Footer Code Site Definitivo.backup_20251030_163729.js` | `01-WEBFLOW-WEBSITE/04-BACKUPS/2025-10-30/DEV/Footer Code Site Definitivo.backup_20251030_163729.js` | Backup DEV |
| `02-DEVELOPMENT/custom-codes/Footer Code Site Definitivo.backup_20251030_175118.js` | `01-WEBFLOW-WEBSITE/04-BACKUPS/2025-10-30/DEV/Footer Code Site Definitivo.backup_20251030_175118.js` | Backup DEV |
| `02-DEVELOPMENT/custom-codes/Footer Code Site Definitivo.backup_20251030_181500.js` | `01-WEBFLOW-WEBSITE/04-BACKUPS/2025-10-30/DEV/Footer Code Site Definitivo.backup_20251030_181500.js` | Backup DEV |
| `02-DEVELOPMENT/custom-codes/Footer Code Site Definitivo.backup_antes_restauracao_20251030_174631.js` | `01-WEBFLOW-WEBSITE/04-BACKUPS/2025-10-30/DEV/Footer Code Site Definitivo.backup_antes_restauracao_20251030_174631.js` | Backup DEV |
| `02-DEVELOPMENT/custom-codes/Footer Code Site Definitivo.backup_antes_restauracao_final_20251030_174830.js` | `01-WEBFLOW-WEBSITE/04-BACKUPS/2025-10-30/DEV/Footer Code Site Definitivo.backup_antes_restauracao_final_20251030_174830.js` | Backup DEV |
| `02-DEVELOPMENT/custom-codes/Footer Code Site Definitivo.backup_pre_refatoracao_20251029_133138.js` | `01-WEBFLOW-WEBSITE/04-BACKUPS/2025-10-29/DEV/Footer Code Site Definitivo.backup_pre_refatoracao_20251029_133138.js` | Backup DEV |
| `02-DEVELOPMENT/custom-codes/Footer Code Site Definitivo.js.backup_20251030_183310` | `01-WEBFLOW-WEBSITE/04-BACKUPS/2025-10-30/DEV/Footer Code Site Definitivo.js.backup_20251030_183310` | Backup DEV |
| `02-DEVELOPMENT/custom-codes/Footer Code Site Definitivo.js.backup_20251030_183328` | `01-WEBFLOW-WEBSITE/04-BACKUPS/2025-10-30/DEV/Footer Code Site Definitivo.js.backup_20251030_183328` | Backup DEV |
| `02-DEVELOPMENT/custom-codes/FooterCodeSiteDefinitivoCompleto.js.backup_20251101_101206` | `01-WEBFLOW-WEBSITE/04-BACKUPS/2025-11-01/DEV/FooterCodeSiteDefinitivoCompleto.js.backup_20251101_101206` | Backup DEV |
| `02-DEVELOPMENT/custom-codes/FooterCodeSiteDefinitivoCompleto.js.backup_20251103_111616` | `01-WEBFLOW-WEBSITE/04-BACKUPS/2025-11-03/DEV/FooterCodeSiteDefinitivoCompleto.js.backup_20251103_111616` | Backup DEV |
| `02-DEVELOPMENT/custom-codes/FooterCodeSiteDefinitivoUtils.backup_20251030_163733.js` | `01-WEBFLOW-WEBSITE/04-BACKUPS/2025-10-30/DEV/FooterCodeSiteDefinitivoUtils.backup_20251030_163733.js` | Backup DEV |
| `02-DEVELOPMENT/custom-codes/FooterCodeSiteDefinitivoUtils.js.backup_20251030_183310` | `01-WEBFLOW-WEBSITE/04-BACKUPS/2025-10-30/DEV/FooterCodeSiteDefinitivoUtils.js.backup_20251030_183310` | Backup DEV |
| `02-DEVELOPMENT/custom-codes/FooterCodeSiteDefinitivoUtils.js.backup_20251030_183328` | `01-WEBFLOW-WEBSITE/04-BACKUPS/2025-10-30/DEV/FooterCodeSiteDefinitivoUtils.js.backup_20251030_183328` | Backup DEV |
| `02-DEVELOPMENT/custom-codes/Inside Head Tag Pagina.js.backup_antes_correcao_gclid_20251031_130658` | `01-WEBFLOW-WEBSITE/04-BACKUPS/2025-10-31/DEV/Inside Head Tag Pagina.js.backup_antes_correcao_gclid_20251031_130658` | Backup DEV |
| `02-DEVELOPMENT/custom-codes/add_flyingdonkeys_v2.php.backup_20251102_142054` | `01-WEBFLOW-WEBSITE/04-BACKUPS/2025-11-02/PROD/add_flyingdonkeys_v2.php.backup_20251102_142054` | Backup PROD |
| `02-DEVELOPMENT/custom-codes/add_flyingdonkeys_v2.php.backup_20251103_180000` | `01-WEBFLOW-WEBSITE/04-BACKUPS/2025-11-03/PROD/add_flyingdonkeys_v2.php.backup_20251103_180000` | Backup PROD |
| `02-DEVELOPMENT/custom-codes/add_webflow_octa_v2.php.backup_20251102_142054` | `01-WEBFLOW-WEBSITE/04-BACKUPS/2025-11-02/PROD/add_webflow_octa_v2.php.backup_20251102_142054` | Backup PROD |

---

### **6. DOCUMENTAÇÃO RELACIONADA**

| **Arquivo Atual** | **Nova Localização** | **Observações** |
|-------------------|---------------------|-----------------|
| `02-DEVELOPMENT/ARQUITETURA_FOOTER_CODES_WEBFLOW_DEV_PROD.md` | `01-WEBFLOW-WEBSITE/05-DOCUMENTATION/ARQUITETURA_FOOTER_CODES_WEBFLOW_DEV_PROD.md` | Arquitetura Webflow |
| `02-DEVELOPMENT/PROPOSTA_ESTRUTURA_DIRETORIOS_FOOTER_CODES.md` | `01-WEBFLOW-WEBSITE/05-DOCUMENTATION/PROPOSTA_ESTRUTURA_DIRETORIOS_FOOTER_CODES.md` | Proposta de estrutura |
| `02-DEVELOPMENT/PROJETO_CORRECAO_MODAL_IOS_NOVA_ABA.md` | `01-WEBFLOW-WEBSITE/05-DOCUMENTATION/PROJETO_CORRECAO_MODAL_IOS_NOVA_ABA.md` | Projeto correção iOS |
| `02-DEVELOPMENT/PESQUISA_SOLUCOES_VALIDADAS_FONTES_REFERENCIA.md` | `01-WEBFLOW-WEBSITE/05-DOCUMENTATION/PESQUISA_SOLUCOES_VALIDADAS_FONTES_REFERENCIA.md` | Pesquisa soluções |
| `02-DEVELOPMENT/PLANO_ROLLBACK_MIGRACAO_DEBUG_LOGS_EMAIL.md` | `01-WEBFLOW-WEBSITE/05-DOCUMENTATION/PLANO_ROLLBACK_MIGRACAO_DEBUG_LOGS_EMAIL.md` | Plano de rollback |
| `02-DEVELOPMENT/PLANEJAMENTO_COPIA_ARQUIVOS_PRODUCAO_POS_NGINX.md` | `01-WEBFLOW-WEBSITE/05-DOCUMENTATION/PLANEJAMENTO_COPIA_ARQUIVOS_PRODUCAO_POS_NGINX.md` | Planejamento Nginx |
| `migration/migracao_debug_email_20251104_192051/ALTERACOES_NECESSARIAS.txt` | `01-WEBFLOW-WEBSITE/05-DOCUMENTATION/migration/ALTERACOES_NECESSARIAS.txt` | Alterações migração |
| `migration/migracao_debug_email_20251104_192051/ANALISE_ENDPOINTS_MODAL.md` | `01-WEBFLOW-WEBSITE/05-DOCUMENTATION/migration/ANALISE_ENDPOINTS_MODAL.md` | Análise endpoints |

---

## 📋 RESUMO ESTATÍSTICO

### **Por Tipo de Arquivo:**

- **JavaScript Footer Codes:** 8 arquivos principais + 17 backups
- **JavaScript Modal:** 2 arquivos principais + 4 legados
- **JavaScript Webflow Codes:** 2 arquivos
- **JavaScript Utils:** 1 arquivo + 3 backups
- **PHP Endpoints:** 7 arquivos principais + 3 backups
- **PHP Config:** 3 arquivos principais + 2 backups
- **Documentação:** 8 arquivos

### **Por Ambiente:**

- **DEV:** ~15 arquivos principais
- **PROD:** ~8 arquivos principais
- **LEGACY:** ~10 arquivos
- **BACKUPS:** ~30 arquivos
- **DOCUMENTAÇÃO:** 8 arquivos

**TOTAL IDENTIFICADO:** ~71 arquivos relacionados ao projeto Webflow/Website

---

## 🔄 PLANO DE MIGRAÇÃO

### **FASE 1: Criação da Estrutura**
1. Criar diretório raiz `01-WEBFLOW-WEBSITE/`
2. Criar subdiretórios conforme estrutura proposta
3. Criar diretórios de backup por data (`YYYY-MM-DD/`)

### **FASE 2: Migração de Arquivos Principais**
1. Migrar arquivos JavaScript (Footer Codes, Modal, Utils)
2. Migrar arquivos PHP (Endpoints, Config)
3. Migrar arquivos Webflow Codes

### **FASE 3: Organização de Backups**
1. Organizar backups por data
2. Separar backups DEV/PROD
3. Manter estrutura de nomes originais

### **FASE 4: Migração de Documentação**
1. Migrar documentação técnica
2. Migrar projetos relacionados
3. Organizar por categoria

### **FASE 5: Validação**
1. Verificar todos os arquivos migrados
2. Validar estrutura de diretórios
3. Confirmar que nenhum arquivo foi perdido

---

## ⚠️ OBSERVAÇÕES IMPORTANTES

1. **Nomes Originais Mantidos:** Todos os arquivos manterão seus nomes originais
2. **Backups Preservados:** Todos os backups serão organizados por data
3. **Estrutura Hierárquica:** Organização clara por tipo e ambiente
4. **Documentação Preservada:** Toda documentação relacionada será migrada
5. **Arquivos Legados:** Arquivos legados serão organizados em `LEGACY/`

---

## ✅ CHECKLIST DE MIGRAÇÃO

### **Pré-Migração:**
- [ ] Criar backup completo do diretório atual
- [ ] Validar estrutura proposta
- [ ] Confirmar mapeamento de todos os arquivos

### **Migração:**
- [ ] Criar estrutura de diretórios
- [ ] Migrar arquivos JavaScript
- [ ] Migrar arquivos PHP
- [ ] Organizar backups
- [ ] Migrar documentação

### **Pós-Migração:**
- [ ] Validar estrutura criada
- [ ] Verificar integridade dos arquivos
- [ ] Atualizar referências em documentação
- [ ] Documentar processo de migração

---

**Documento criado em:** 05/11/2025  
**Versão:** 1.0  
**Status:** Planejado - Aguardando Aprovação

