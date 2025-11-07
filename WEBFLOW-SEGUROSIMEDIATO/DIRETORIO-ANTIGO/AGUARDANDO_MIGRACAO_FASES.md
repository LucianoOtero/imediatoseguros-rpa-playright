# ⏳ AGUARDANDO MIGRAÇÃO EM FASES

**Data:** 02/11/2025 10:15  
**Status:** Arquivos prontos, aguardando migração gradual pelo usuário

## ✅ Arquivos Prontos para Migração

### **Servidor de Produção**
- ✅ `/var/www/html/webhooks/add_flyingdonkeys_v2.php`
- ✅ `/var/www/html/webhooks/add_webflow_octa_v2.php`
- ✅ `/var/www/html/webhooks/FooterCodeSiteDefinitivoCompleto_prod.js`
- ✅ Credenciais SafetyMails atualizadas (mesmas do DEV)

### **Arquivos Locais**
- ✅ `02-DEVELOPMENT/custom-codes/Footer Code Site Definitivo WEBFLOW_prod.js`
- ✅ `MODAL_WHATSAPP_DEFINITIVO.js` (endpoints _v2 já configurados)

## 🔄 Estratégia de Migração (Usuário)

### **FASE 1: Apenas Endpoints (PRIMEIRA FASE)**
Usuário vai:
1. Atualizar Footer Code no Webflow para usar `FooterCodeSiteDefinitivoCompleto_prod.js`
2. Monitorar logs dos novos endpoints _v2

**Endpoints que serão ativados:**
- `https://bpsegurosimediato.com.br/webhooks/add_flyingdonkeys_v2.php`
- `https://bpsegurosimediato.com.br/webhooks/add_webflow_octa_v2.php`

## 📊 Logs para Monitoramento

### **FlyingDonkeys**
```bash
tail -f /var/www/html/logs/flyingdonkeys_prod.txt
```

### **OctaDesk**
```bash
tail -f /var/www/html/logs/webhook_octadesk_prod.txt
```

## 🔍 Checklist de Validação

Quando o usuário avisar para acompanhar os logs, verificar:

### **add_flyingdonkeys_v2.php**
- [ ] Requisições chegando no endpoint
- [ ] Validação de signature funcionando
- [ ] Criação de leads no FlyingDonkeys
- [ ] Criação de oportunidades
- [ ] Logs sem erros críticos

### **add_webflow_octa_v2.php**
- [ ] Requisições chegando no endpoint
- [ ] Validação de signature funcionando
- [ ] Template WhatsApp sendo enviado (`site_cotacao`)
- [ ] Conversas sendo criadas no OctaDesk
- [ ] Logs sem erros críticos

### **FooterCodeSiteDefinitivoCompleto_prod.js**
- [ ] Arquivo carregando corretamente
- [ ] Sem erros de CORS
- [ ] Chamadas aos endpoints _v2 funcionando
- [ ] GCLID sendo capturado e enviado

## ⚠️ Pontos de Atenção

1. **Validação de Signature Webflow**
   - Em produção, signature é obrigatória
   - Se houver erros 401, verificar secrets do Webflow

2. **Template OctaDesk**
   - Template code: `site_cotacao`
   - Language: `pt_BR`
   - Se template não existir, OctaDesk retornará erro

3. **Credenciais**
   - SafetyMails: ✅ Configuradas (mesmas do DEV)
   - FlyingDonkeys: ✅ Configuradas (obtidas de produção)
   - OctaDesk: ✅ Configuradas (obtidas de produção)

## 📝 Comandos Úteis para Acompanhamento

```bash
# Ver últimos logs FlyingDonkeys
tail -n 50 /var/www/html/logs/flyingdonkeys_prod.txt

# Ver últimos logs OctaDesk
tail -n 50 /var/www/html/logs/webhook_octadesk_prod.txt

# Verificar se arquivos existem
ls -lah /var/www/html/webhooks/*_v2.php
ls -lah /var/www/html/webhooks/*_prod.js

# Testar sintaxe PHP
php -l /var/www/html/webhooks/add_flyingdonkeys_v2.php
php -l /var/www/html/webhooks/add_webflow_octa_v2.php
```

---

**Aguardando aviso do usuário para iniciar monitoramento dos logs.**



