# 🚀 CONFIGURAÇÃO NECESSÁRIA NO HETZNER/UBUNTU

## 📋 RESUMO DOS PROBLEMAS IDENTIFICADOS

### ❌ **PROBLEMA 1: REDIS NÃO ESTÁ RODANDO**
- **Erro**: `Error 10061 connecting to localhost:6379`
- **Causa**: Redis não está instalado ou não está rodando no servidor
- **Impacto**: Sistema de cache e comunicação em tempo real não funciona

### ❌ **PROBLEMA 2: WEBSOCKET NÃO DISPONÍVEL**
- **Erro**: `WebSocket não disponível - módulo websockets não instalado`
- **Causa**: Módulo Python `websockets` não está instalado
- **Impacto**: Comunicação em tempo real não funciona

### ❌ **PROBLEMA 3: DEPENDÊNCIAS FALTANDO**
- **Causa**: Módulos Python necessários não estão instalados
- **Impacto**: Sistema não funciona completamente

---

## 🔧 **AÇÕES NECESSÁRIAS NO HETZNER**

### **1. INSTALAR E CONFIGURAR REDIS**

```bash
# Conectar no servidor Hetzner
ssh seu_usuario@seu_ip_hetzner

# Atualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Redis
sudo apt install redis-server -y

# Configurar Redis
sudo nano /etc/redis/redis.conf

# Alterar as seguintes linhas:
# bind 127.0.0.1 ::1
# para:
# bind 0.0.0.0

# Definir senha (opcional mas recomendado)
# requirepass sua_senha_redis

# Reiniciar Redis
sudo systemctl restart redis-server
sudo systemctl enable redis-server

# Verificar se está rodando
redis-cli ping
# Deve retornar: PONG
```

### **2. INSTALAR DEPENDÊNCIAS PYTHON**

```bash
# Instalar módulos Python necessários
pip3 install redis websockets asyncio psutil

# Verificar instalação
python3 -c "import redis; print('Redis OK')"
python3 -c "import websockets; print('WebSockets OK')"
```

### **3. CONFIGURAR FIREWALL**

```bash
# Abrir portas necessárias
sudo ufw allow 6379/tcp  # Redis
sudo ufw allow 8765/tcp  # WebSocket
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS

# Verificar status
sudo ufw status
```

### **4. VERIFICAR CONFIGURAÇÃO NGINX**

```bash
# Verificar se Nginx está rodando
sudo systemctl status nginx

# Se não estiver, instalar
sudo apt install nginx -y
sudo systemctl start nginx
sudo systemctl enable nginx

# Verificar configuração
sudo nginx -t
```

### **5. EXECUTAR SCRIPT DE VERIFICAÇÃO**

```bash
# Fazer upload do script de verificação
# (usar scp, rsync ou git clone)

# Executar verificação
chmod +x verify_environment_hetzner.sh
./verify_environment_hetzner.sh
```

---

## 📊 **VERIFICAÇÕES PÓS-INSTALAÇÃO**

### **Teste 1: Redis**
```bash
redis-cli ping
# Deve retornar: PONG

redis-cli set test "hello"
redis-cli get test
# Deve retornar: "hello"
```

### **Teste 2: Python Modules**
```bash
python3 -c "
import redis
import websockets
import asyncio
import psutil
print('✅ Todos os módulos Python OK')
"
```

### **Teste 3: Conectividade**
```bash
# Testar conexão Redis
telnet localhost 6379

# Testar porta WebSocket
netstat -tuln | grep 8765
```

---

## 🚀 **DEPLOY NO HETZNER**

### **Opção 1: Deploy Automático**
```bash
# Executar script de deploy
chmod +x deploy_v3.6.0.sh
./deploy_v3.6.0.sh
```

### **Opção 2: Deploy Manual**
```bash
# 1. Fazer backup
cp -r /caminho/atual /backup/$(date +%Y%m%d)

# 2. Atualizar código
git pull origin master

# 3. Instalar dependências
pip3 install -r requirements.txt

# 4. Iniciar serviços
./start_services.sh

# 5. Verificar status
./monitor_services.sh
```

---

## 🔍 **MONITORAMENTO**

### **Comandos Úteis**
```bash
# Status dos serviços
sudo systemctl status redis-server
sudo systemctl status nginx

# Logs
sudo journalctl -u redis-server -f
sudo tail -f /var/log/nginx/error.log

# Uso de recursos
htop
df -h
free -h
```

### **Verificação Contínua**
```bash
# Executar verificação periódica
crontab -e

# Adicionar linha para verificação a cada hora
0 * * * * /caminho/para/verify_environment_hetzner.sh
```

---

## 🆘 **SOLUÇÃO DE PROBLEMAS**

### **Redis não conecta**
```bash
# Verificar se está rodando
sudo systemctl status redis-server

# Reiniciar se necessário
sudo systemctl restart redis-server

# Verificar logs
sudo journalctl -u redis-server
```

### **Porta 8765 não abre**
```bash
# Verificar se processo está rodando
ps aux | grep websocket

# Verificar firewall
sudo ufw status
sudo ufw allow 8765
```

### **Módulos Python não encontrados**
```bash
# Reinstalar módulos
pip3 install --upgrade redis websockets asyncio psutil

# Verificar Python path
python3 -c "import sys; print(sys.path)"
```

---

## ✅ **CHECKLIST FINAL**

- [ ] Redis instalado e rodando
- [ ] Módulos Python instalados
- [ ] Firewall configurado
- [ ] Nginx configurado
- [ ] Script de verificação executado
- [ ] Testes de conectividade passando
- [ ] Serviços iniciados
- [ ] Monitoramento configurado

---

## 📞 **PRÓXIMOS PASSOS**

1. **Execute as configurações acima no Hetzner**
2. **Rode o script de verificação**
3. **Teste a conectividade**
4. **Inicie os serviços**
5. **Monitore o sistema**

**Status atual**: ❌ **NÃO PRONTO** - Requer configuração no Hetzner
**Após configuração**: ✅ **PRONTO** - Sistema funcionará completamente
