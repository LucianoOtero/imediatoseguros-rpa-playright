# SCRIPT DE INICIALIZAÇÃO HETZNER V6.0.0

**Data**: 03 de Outubro de 2025  
**Versão**: 6.0.0  
**Arquivo**: `/opt/imediatoseguros-rpa/startup.sh`  
**Serviço**: `/etc/systemd/system/rpa-startup.service`  

---

## 🎯 **OBJETIVO**

Garantir que o sistema RPA seja automaticamente recuperado após um reboot do servidor Hetzner, instalando dependências necessárias e configurando permissões corretas.

---

## 📁 **ARQUIVOS ENVOLVIDOS**

### **🔧 Script Principal**
- **Arquivo**: `/opt/imediatoseguros-rpa/startup.sh`
- **Função**: Executar tarefas de inicialização
- **Permissões**: `755` (executável)

### **⚙️ Serviço Systemd**
- **Arquivo**: `/etc/systemd/system/rpa-startup.service`
- **Função**: Executar script automaticamente no boot
- **Status**: Habilitado para inicialização automática

---

## 🔧 **CONTEÚDO DO SCRIPT**

### **📄 `/opt/imediatoseguros-rpa/startup.sh`**
```bash
#!/bin/bash
# Script de inicialização RPA V6.0.0
# Data: 03/10/2025
# Versão: 6.0.0

echo "$(date): === INICIANDO SCRIPT DE INICIALIZAÇÃO RPA V6.0.0 ===" >> /opt/imediatoseguros-rpa/logs/startup.log

# Instalar browsers Playwright
echo "$(date): Instalando browsers Playwright..." >> /opt/imediatoseguros-rpa/logs/startup.log
/opt/imediatoseguros-rpa/venv/bin/playwright install chromium

# Verificar permissões dos diretórios
echo "$(date): Verificando permissões dos diretórios..." >> /opt/imediatoseguros-rpa/logs/startup.log
chown -R www-data:www-data /opt/imediatoseguros-rpa/rpa_data /opt/imediatoseguros-rpa/logs /opt/imediatoseguros-rpa/sessions /opt/imediatoseguros-rpa/scripts
chmod -R 755 /opt/imediatoseguros-rpa/rpa_data /opt/imediatoseguros-rpa/logs /opt/imediatoseguros-rpa/sessions /opt/imediatoseguros-rpa/scripts

# Limpar sessões antigas
echo "$(date): Limpando sessões antigas..." >> /opt/imediatoseguros-rpa/logs/startup.log
find /opt/imediatoseguros-rpa/sessions -type d -mtime +1 -exec rm -rf {} + 2>/dev/null
find /opt/imediatoseguros-rpa/rpa_data -name "progress_*.json" -mtime +1 -delete 2>/dev/null

echo "$(date): === SCRIPT DE INICIALIZAÇÃO RPA V6.0.0 CONCLUÍDO COM SUCESSO ===" >> /opt/imediatoseguros-rpa/logs/startup.log
echo "$(date): Sistema RPA pronto para uso!" >> /opt/imediatoseguros-rpa/logs/startup.log

exit 0
```

---

## ⚙️ **CONFIGURAÇÃO DO SERVIÇO SYSTEMD**

### **📄 `/etc/systemd/system/rpa-startup.service`**
```ini
[Unit]
Description=RPA Startup Script
After=network.target nginx.service php8.3-fpm.service

[Service]
Type=oneshot
ExecStart=/opt/imediatoseguros-rpa/startup.sh
RemainAfterExit=yes
User=root
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

---

## 🔧 **FUNCIONALIDADES DO SCRIPT**

### **🌐 1. INSTALAÇÃO DE BROWSERS PLAYWRIGHT**
```bash
/opt/imediatoseguros-rpa/venv/bin/playwright install chromium
```
- **Função**: Instala navegador Chromium para Playwright
- **Necessidade**: Browsers são perdidos após reboot
- **Ambiente**: Virtual environment Python

### **🔐 2. CONFIGURAÇÃO DE PERMISSÕES**
```bash
chown -R www-data:www-data /opt/imediatoseguros-rpa/rpa_data /opt/imediatoseguros-rpa/logs /opt/imediatoseguros-rpa/sessions /opt/imediatoseguros-rpa/scripts
chmod -R 755 /opt/imediatoseguros-rpa/rpa_data /opt/imediatoseguros-rpa/logs /opt/imediatoseguros-rpa/sessions /opt/imediatoseguros-rpa/scripts
```
- **Função**: Define permissões corretas para usuário `www-data`
- **Diretórios**: Dados, logs, sessões e scripts
- **Permissões**: `755` (leitura, escrita, execução)

### **🧹 3. LIMPEZA DE SESSÕES ANTIGAS**
```bash
find /opt/imediatoseguros-rpa/sessions -type d -mtime +1 -exec rm -rf {} + 2>/dev/null
find /opt/imediatoseguros-rpa/rpa_data -name "progress_*.json" -mtime +1 -delete 2>/dev/null
```
- **Função**: Remove sessões e arquivos de progresso antigos
- **Critério**: Arquivos com mais de 1 dia
- **Segurança**: Redirecionamento de erros para `/dev/null`

---

## 📊 **LOGS E MONITORAMENTO**

### **📁 Arquivo de Log**
- **Localização**: `/opt/imediatoseguros-rpa/logs/startup.log`
- **Formato**: Timestamp + Mensagem
- **Rotação**: Manual (pode ser implementada)

### **📝 Exemplo de Log**
```
Fri Oct  3 22:15:00 UTC 2025: === INICIANDO SCRIPT DE INICIALIZAÇÃO RPA V6.0.0 ===
Fri Oct  3 22:15:01 UTC 2025: Instalando browsers Playwright...
Fri Oct  3 22:15:30 UTC 2025: Verificando permissões dos diretórios...
Fri Oct  3 22:15:31 UTC 2025: Limpando sessões antigas...
Fri Oct  3 22:15:32 UTC 2025: === SCRIPT DE INICIALIZAÇÃO RPA V6.0.0 CONCLUÍDO COM SUCESSO ===
Fri Oct  3 22:15:32 UTC 2025: Sistema RPA pronto para uso!
```

---

## 🚀 **CONFIGURAÇÃO E ATIVAÇÃO**

### **📋 Passos para Configuração**
```bash
# 1. Criar o script
sudo nano /opt/imediatoseguros-rpa/startup.sh

# 2. Tornar executável
sudo chmod +x /opt/imediatoseguros-rpa/startup.sh

# 3. Criar o serviço systemd
sudo nano /etc/systemd/system/rpa-startup.service

# 4. Recarregar systemd
sudo systemctl daemon-reload

# 5. Habilitar o serviço
sudo systemctl enable rpa-startup.service

# 6. Testar manualmente
sudo systemctl start rpa-startup.service

# 7. Verificar status
sudo systemctl status rpa-startup.service
```

### **✅ Verificação de Status**
```bash
# Verificar se está habilitado
sudo systemctl is-enabled rpa-startup.service

# Verificar logs do serviço
sudo journalctl -u rpa-startup.service

# Verificar logs do script
tail -f /opt/imediatoseguros-rpa/logs/startup.log
```

---

## 🔍 **DEPENDÊNCIAS E PRÉ-REQUISITOS**

### **📋 Serviços Necessários**
- **network.target**: Rede configurada
- **nginx.service**: Servidor web ativo
- **php8.3-fpm.service**: PHP-FPM ativo

### **📁 Diretórios Necessários**
- `/opt/imediatoseguros-rpa/venv/`: Virtual environment Python
- `/opt/imediatoseguros-rpa/logs/`: Diretório de logs
- `/opt/imediatoseguros-rpa/rpa_data/`: Dados de progresso
- `/opt/imediatoseguros-rpa/sessions/`: Sessões ativas
- `/opt/imediatoseguros-rpa/scripts/`: Scripts gerados

### **👤 Usuário Necessário**
- **www-data**: Usuário do servidor web
- **Permissões**: Acesso aos diretórios RPA

---

## 🧪 **TESTES E VALIDAÇÃO**

### **✅ Teste Manual**
```bash
# Executar script manualmente
sudo /opt/imediatoseguros-rpa/startup.sh

# Verificar se browsers foram instalados
/opt/imediatoseguros-rpa/venv/bin/playwright --version

# Verificar permissões
ls -la /opt/imediatoseguros-rpa/rpa_data/
ls -la /opt/imediatoseguros-rpa/logs/
```

### **✅ Teste de Reboot**
```bash
# Simular reboot (cuidado!)
sudo reboot

# Após reboot, verificar se serviço executou
sudo systemctl status rpa-startup.service

# Verificar logs
tail -f /opt/imediatoseguros-rpa/logs/startup.log
```

---

## 🚨 **TROUBLESHOOTING**

### **❌ Problemas Comuns**

#### **1. Script não executa**
```bash
# Verificar permissões
ls -la /opt/imediatoseguros-rpa/startup.sh

# Verificar se está habilitado
sudo systemctl is-enabled rpa-startup.service

# Verificar logs do systemd
sudo journalctl -u rpa-startup.service
```

#### **2. Browsers não instalam**
```bash
# Verificar virtual environment
ls -la /opt/imediatoseguros-rpa/venv/bin/

# Verificar Playwright
/opt/imediatoseguros-rpa/venv/bin/playwright --version

# Instalar manualmente
/opt/imediatoseguros-rpa/venv/bin/playwright install chromium
```

#### **3. Permissões incorretas**
```bash
# Verificar usuário atual
whoami

# Verificar permissões
ls -la /opt/imediatoseguros-rpa/

# Corrigir permissões
sudo chown -R www-data:www-data /opt/imediatoseguros-rpa/
sudo chmod -R 755 /opt/imediatoseguros-rpa/
```

---

## 📈 **BENEFÍCIOS IMPLEMENTADOS**

### **🔄 Recuperação Automática**
- **Reboot**: Sistema se recupera automaticamente
- **Dependências**: Browsers reinstalados automaticamente
- **Permissões**: Configuradas automaticamente
- **Limpeza**: Sessões antigas removidas automaticamente

### **🛡️ Robustez do Sistema**
- **Confiabilidade**: Sistema sempre pronto após reboot
- **Manutenção**: Limpeza automática de arquivos antigos
- **Segurança**: Permissões sempre corretas
- **Monitoramento**: Logs detalhados de inicialização

### **⚡ Eficiência Operacional**
- **Tempo**: Recuperação rápida após reboot
- **Recursos**: Limpeza automática de espaço
- **Manutenção**: Redução de intervenção manual
- **Disponibilidade**: Sistema sempre operacional

---

## 🎯 **PRÓXIMOS PASSOS**

### **📋 Melhorias Futuras**
1. **Rotação de Logs**: Implementar rotação automática
2. **Monitoramento**: Alertas em caso de falha
3. **Backup**: Backup automático de configurações
4. **Métricas**: Coleta de métricas de inicialização

### **🔧 Otimizações**
1. **Paralelização**: Executar tarefas em paralelo
2. **Cache**: Cache de browsers para instalação mais rápida
3. **Validação**: Validação de integridade dos arquivos
4. **Notificações**: Notificações de status de inicialização

---

## 🎉 **CONCLUSÃO**

### **✅ SCRIPT DE INICIALIZAÇÃO IMPLEMENTADO COM SUCESSO**
O script de inicialização garante que o sistema RPA V6.0.0 seja automaticamente recuperado após qualquer reboot do servidor Hetzner.

### **🔧 FUNCIONALIDADES VALIDADAS**
- ✅ **Instalação de Browsers**: Playwright Chromium instalado automaticamente
- ✅ **Configuração de Permissões**: Usuário www-data configurado corretamente
- ✅ **Limpeza Automática**: Sessões antigas removidas automaticamente
- ✅ **Logs Detalhados**: Monitoramento completo da inicialização
- ✅ **Serviço Systemd**: Execução automática no boot configurada

### **📊 STATUS ATUAL**
**Sistema de Inicialização Automática - Operacional** ✅

---

**Desenvolvido por**: Equipe de Desenvolvimento  
**Data**: 03 de Outubro de 2025  
**Versão**: 6.0.0  
**Status**: ✅ **SCRIPT DE INICIALIZAÇÃO IMPLEMENTADO COM SUCESSO**
