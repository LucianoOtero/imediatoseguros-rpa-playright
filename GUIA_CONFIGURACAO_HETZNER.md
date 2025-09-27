# GUIA DE CONFIGURAÇÃO SERVIDOR HETZNER
# Domínio: rpaimediatoseguros.com.br
# IP: 37.27.92.160

## 1️⃣ CONFIGURAÇÃO DNS (FAÇA PRIMEIRO)
Configure estes registros DNS no seu provedor de domínio:

```
A    rpaimediatoseguros.com.br        -> 37.27.92.160
A    www.rpaimediatoseguros.com.br    -> 37.27.92.160
A    api.rpaimediatoseguros.com.br    -> 37.27.92.160
```

## 2️⃣ CONECTAR NO SERVIDOR
```bash
ssh root@37.27.92.160
```

## 3️⃣ EXECUTAR CONFIGURAÇÃO BÁSICA
```bash
# Fazer upload do arquivo setup_hetzner_server.sh
chmod +x setup_hetzner_server.sh
./setup_hetzner_server.sh
```

## 4️⃣ CONFIGURAR SSL COM LET'S ENCRYPT
```bash
# Aguardar propagação DNS (pode levar até 24h)
# Testar se o domínio resolve:
nslookup rpaimediatoseguros.com.br

# Gerar certificado SSL
certbot --nginx -d rpaimediatoseguros.com.br -d www.rpaimediatoseguros.com.br
```

## 5️⃣ FAZER DEPLOY DOS ARQUIVOS
```bash
# Fazer upload dos arquivos de configuração:
# - nginx_rpaimediatoseguros.conf
# - websocket_server.js
# - package.json
# - rpa-websocket.service
# - deploy_rpa.sh

chmod +x deploy_rpa.sh
./deploy_rpa.sh
```

## 6️⃣ FAZER UPLOAD DO RPA
```bash
# Upload dos arquivos do RPA para:
/var/www/rpaimediatoseguros.com.br/api/

# Arquivos necessários:
# - executar_rpa_imediato_playwright.py
# - parametros.json
# - utils/ (diretório completo)
# - requirements.txt
```

## 7️⃣ INSTALAR DEPENDÊNCIAS PYTHON
```bash
cd /var/www/rpaimediatoseguros.com.br/api/
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install playwright redis
playwright install chromium
```

## 8️⃣ CONFIGURAR REDIS PROGRESS TRACKER
```bash
# Criar arquivo utils/progress_redis.py
# Atualizar executar_rpa_imediato_playwright.py para usar Redis
```

## 9️⃣ TESTAR SISTEMA
```bash
# Testar HTTP
curl -I http://rpaimediatoseguros.com.br

# Testar HTTPS
curl -I https://rpaimediatoseguros.com.br

# Testar WebSocket
curl -I http://rpaimediatoseguros.com.br:8080

# Testar Redis
redis-cli ping
```

## 🔟 MONITORAMENTO
```bash
# Logs em tempo real
tail -f /var/www/rpaimediatoseguros.com.br/logs/access.log
journalctl -u rpa-websocket -f

# Status dos serviços
systemctl status nginx rpa-websocket redis-server

# Reiniciar serviços se necessário
systemctl restart nginx
systemctl restart rpa-websocket
systemctl restart redis-server
```

## 🚨 COMANDOS DE EMERGÊNCIA
```bash
# Parar todos os serviços
systemctl stop nginx rpa-websocket redis-server

# Iniciar todos os serviços
systemctl start nginx rpa-websocket redis-server

# Verificar portas em uso
netstat -tlnp | grep -E ':(80|443|8080|6379)'

# Verificar logs de erro
journalctl -u nginx -f
journalctl -u rpa-websocket -f
```

## 📊 ESTRUTURA FINAL
```
/var/www/rpaimediatoseguros.com.br/
├── api/                    # Backend RPA
│   ├── executar_rpa_imediato_playwright.py
│   ├── parametros.json
│   ├── utils/
│   └── venv/
├── websocket/              # WebSocket Server
│   ├── server.js
│   ├── package.json
│   └── node_modules/
└── logs/                   # Logs do sistema
    ├── access.log
    └── error.log
```







