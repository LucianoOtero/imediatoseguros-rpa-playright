# 🔒 PROJETO SEGURANÇA - PROTEÇÃO DO DIRETÓRIO JS

## 🎯 **OBJETIVO**
Implementar medidas de segurança para proteger o diretório `/js/` contra acessos não autorizados, permitindo apenas IPs reconhecidos (Webflow, IPs autorizados).

---

## 🚨 **PROBLEMA IDENTIFICADO**
- **Diretório JS público**: `/opt/imediatoseguros-rpa/js/` acessível via web
- **Arquivo sensível**: `webflow-injection-complete.js` contém lógica de negócio
- **Risco**: Acesso não autorizado pode comprometer segurança e performance
- **Abuso**: Possível uso indevido do JavaScript por terceiros

---

## 🛡️ **SOLUÇÕES DE SEGURANÇA**

### **1️⃣ WHITELIST DE IPs (NGINX)**

#### **📋 IMPLEMENTAÇÃO:**
```nginx
# /etc/nginx/sites-available/imediatoseguros-rpa
location /js/ {
    # IPs autorizados
    allow 104.21.0.0/16;    # Webflow CDN
    allow 172.67.0.0/16;    # Webflow CDN
    allow 192.168.1.0/24;   # Rede local
    allow SEU_IP_PUBLICO;   # Seu IP específico
    
    # Bloquear todos os outros
    deny all;
    
    # Headers de segurança
    add_header X-Content-Type-Options nosniff;
    add_header X-Frame-Options DENY;
    add_header X-XSS-Protection "1; mode=block";
}
```

### **2️⃣ VALIDAÇÃO DE ORIGEM**

#### **📋 IMPLEMENTAÇÃO:**
```nginx
location /js/ {
    # Validar Referer do Webflow
    if ($http_referer !~* "^https://.*\.webflow\.io") {
        return 403;
    }
    
    # Validar User-Agent
    if ($http_user_agent !~* "webflow|chrome|firefox|safari") {
        return 403;
    }
}
```

### **3️⃣ RATE LIMITING**

#### **📋 IMPLEMENTAÇÃO:**
```nginx
# Limite de requisições por IP
limit_req_zone $binary_remote_addr zone=js_limit:10m rate=10r/m;

location /js/ {
    limit_req zone=js_limit burst=5 nodelay;
}
```

### **4️⃣ LOGS DE SEGURANÇA**

#### **📋 IMPLEMENTAÇÃO:**
```nginx
location /js/ {
    # Log de acessos
    access_log /var/log/nginx/js_access.log;
    error_log /var/log/nginx/js_error.log;
    
    # Log de tentativas bloqueadas
    if ($http_referer !~* "webflow") {
        access_log /var/log/nginx/js_blocked.log;
    }
}
```

### **5️⃣ TOKEN DE AUTENTICAÇÃO**

#### **📋 IMPLEMENTAÇÃO:**
```nginx
location /js/ {
    # Validar token na URL
    if ($arg_token != "TOKEN_SECRETO_2025") {
        return 403;
    }
}
```

---

## 🚀 **IMPLEMENTAÇÃO PASSO A PASSO**

### **PASSO 1: BACKUP DA CONFIGURAÇÃO**
```bash
# Backup da configuração atual
sudo cp /etc/nginx/sites-available/imediatoseguros-rpa /etc/nginx/sites-available/imediatoseguros-rpa.backup
```

### **PASSO 2: CRIAR CONFIGURAÇÃO DE SEGURANÇA**
```bash
# Criar arquivo de configuração
sudo nano /etc/nginx/sites-available/imediatoseguros-rpa-security
```

### **PASSO 3: APLICAR CONFIGURAÇÃO**
```bash
# Testar configuração
sudo nginx -t

# Recarregar nginx
sudo systemctl reload nginx
```

### **PASSO 4: MONITORAR LOGS**
```bash
# Monitorar acessos
tail -f /var/log/nginx/js_access.log

# Monitorar bloqueios
tail -f /var/log/nginx/js_blocked.log
```

---

## 📊 **MONITORAMENTO E ALERTAS**

### **📋 SCRIPTS DE MONITORAMENTO:**

#### **1️⃣ ALERTA DE ACESSO SUSPEITO:**
```bash
#!/bin/bash
# /opt/imediatoseguros-rpa/scripts/security_monitor.sh

# Verificar tentativas bloqueadas
BLOCKED_COUNT=$(grep -c "403" /var/log/nginx/js_blocked.log)

if [ $BLOCKED_COUNT -gt 10 ]; then
    echo "ALERTA: $BLOCKED_COUNT tentativas bloqueadas no diretório JS" | mail -s "Alerta Segurança" admin@imediatoseguros.com.br
fi
```

#### **2️⃣ RELATÓRIO DIÁRIO:**
```bash
#!/bin/bash
# Relatório diário de segurança
echo "=== RELATÓRIO SEGURANÇA JS - $(date) ===" >> /var/log/security_report.log
echo "Acessos autorizados: $(grep -c "200" /var/log/nginx/js_access.log)" >> /var/log/security_report.log
echo "Tentativas bloqueadas: $(grep -c "403" /var/log/nginx/js_blocked.log)" >> /var/log/security_report.log
```

---

## 🔧 **CONFIGURAÇÃO WEBFLOW**

### **📋 ATUALIZAR INJEÇÃO:**
```html
<!-- Webflow Custom Code -->
<script>
// Validar origem antes de carregar
if (window.location.hostname.includes('webflow.io') || 
    document.referrer.includes('webflow.io')) {
    
    // Carregar JavaScript com token
    const script = document.createElement('script');
    script.src = 'https://rpaimediatoseguros.com.br/js/webflow-injection-complete.js?token=TOKEN_SECRETO_2025';
    script.defer = true;
    document.head.appendChild(script);
}
</script>
```

---

## ✅ **CHECKLIST DE IMPLEMENTAÇÃO**

### **🔒 SEGURANÇA BÁSICA:**
- [ ] Whitelist de IPs configurada
- [ ] Validação de Referer implementada
- [ ] Rate limiting ativo
- [ ] Logs de segurança configurados
- [ ] Backup da configuração atual

### **🛡️ SEGURANÇA AVANÇADA:**
- [ ] Token de autenticação implementado
- [ ] Monitoramento automático ativo
- [ ] Alertas por email configurados
- [ ] Relatórios diários automatizados
- [ ] Testes de penetração realizados

### **📊 MONITORAMENTO:**
- [ ] Dashboard de segurança
- [ ] Métricas de acesso
- [ ] Alertas em tempo real
- [ ] Relatórios de compliance
- [ ] Auditoria de logs

---

## 🎯 **RESULTADOS ESPERADOS**

### **✅ BENEFÍCIOS:**
1. **Proteção total** contra acessos não autorizados
2. **Performance otimizada** (menos requisições desnecessárias)
3. **Compliance** com boas práticas de segurança
4. **Monitoramento** proativo de ameaças
5. **Controle granular** de acesso

### **📊 MÉTRICAS DE SUCESSO:**
- **0 acessos** não autorizados por dia
- **< 1%** de requisições bloqueadas
- **100%** de uptime do serviço
- **< 100ms** tempo de resposta
- **0 incidentes** de segurança

---

## 🚨 **PLANO DE CONTINGÊNCIA**

### **📋 EM CASO DE PROBLEMAS:**
1. **Restaurar backup** da configuração
2. **Desabilitar** proteções temporariamente
3. **Investigar** logs de erro
4. **Aplicar correções** específicas
5. **Reativar** proteções gradualmente

### **📞 CONTATOS DE EMERGÊNCIA:**
- **Admin**: admin@imediatoseguros.com.br
- **DevOps**: devops@imediatoseguros.com.br
- **Suporte**: suporte@imediatoseguros.com.br

---

## 📝 **NOTAS IMPORTANTES**

### **⚠️ CONSIDERAÇÕES:**
- **IPs do Webflow** podem mudar (monitorar)
- **CDN** pode usar IPs diferentes
- **Testes** devem ser feitos em ambiente de staging
- **Backup** sempre antes de alterações
- **Documentação** deve ser atualizada

### **🔍 VALIDAÇÃO:**
- **Testar** acesso autorizado
- **Verificar** bloqueio de IPs não autorizados
- **Monitorar** logs por 24h
- **Validar** performance
- **Confirmar** funcionamento do Webflow

---

**🎯 PROJETO DE SEGURANÇA CRÍTICO PARA PROTEÇÃO DO DIRETÓRIO JS** 🔒

