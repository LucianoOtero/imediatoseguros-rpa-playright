#!/bin/bash

# Script de Deploy para RPA Imediato Seguros
# Executar no servidor Hetzner após configuração básica

echo "🚀 Iniciando deploy do RPA Imediato Seguros..."

# Verificar se está rodando como root
if [ "$EUID" -ne 0 ]; then
    echo "❌ Execute como root: sudo ./deploy_rpa.sh"
    exit 1
fi

# Parar serviços se estiverem rodando
echo "🛑 Parando serviços..."
systemctl stop rpa-websocket 2>/dev/null || true
systemctl stop nginx 2>/dev/null || true

# Configurar Nginx
echo "🌐 Configurando Nginx..."
cp nginx_rpaimediatoseguros.conf /etc/nginx/sites-available/rpaimediatoseguros.com.br
ln -sf /etc/nginx/sites-available/rpaimediatoseguros.com.br /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# Testar configuração Nginx
nginx -t
if [ $? -ne 0 ]; then
    echo "❌ Erro na configuração do Nginx!"
    exit 1
fi

# Configurar WebSocket Server
echo "🔌 Configurando WebSocket Server..."
cd /var/www/rpaimediatoseguros.com.br/websocket
cp websocket_server.js server.js
cp package.json .

# Instalar dependências Node.js
npm install --production

# Configurar systemd service
echo "⚙️ Configurando systemd service..."
cp rpa-websocket.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable rpa-websocket

# Configurar permissões
echo "🔐 Configurando permissões..."
chown -R www-data:www-data /var/www/rpaimediatoseguros.com.br
chmod -R 755 /var/www/rpaimediatoseguros.com.br

# Criar diretório de logs
mkdir -p /var/www/rpaimediatoseguros.com.br/logs
chown www-data:www-data /var/www/rpaimediatoseguros.com.br/logs

# Configurar logrotate
echo "📝 Configurando logrotate..."
cat > /etc/logrotate.d/rpaimediatoseguros << EOF
/var/www/rpaimediatoseguros.com.br/logs/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 644 www-data www-data
    postrotate
        systemctl reload nginx
    endscript
}
EOF

# Iniciar serviços
echo "🚀 Iniciando serviços..."
systemctl start nginx
systemctl start rpa-websocket

# Verificar status
echo "🔍 Verificando status dos serviços..."
systemctl status nginx --no-pager -l
systemctl status rpa-websocket --no-pager -l
systemctl status redis-server --no-pager -l

# Testar conectividade
echo "🧪 Testando conectividade..."
curl -I http://localhost 2>/dev/null | head -1
redis-cli ping 2>/dev/null || echo "❌ Redis não respondeu"

echo ""
echo "✅ Deploy concluído!"
echo ""
echo "📋 PRÓXIMOS PASSOS:"
echo "1. Configure os registros DNS do domínio rpaimediatoseguros.com.br"
echo "2. Execute: certbot --nginx -d rpaimediatoseguros.com.br -d www.rpaimediatoseguros.com.br"
echo "3. Faça upload dos arquivos do RPA para /var/www/rpaimediatoseguros.com.br/api/"
echo ""
echo "🔍 URLs de teste:"
echo "- HTTP: http://37.27.92.160"
echo "- WebSocket: ws://37.27.92.160:8080"
echo "- Redis: redis-cli ping"
echo ""
echo "📊 Monitoramento:"
echo "- Logs Nginx: tail -f /var/www/rpaimediatoseguros.com.br/logs/access.log"
echo "- Logs WebSocket: journalctl -u rpa-websocket -f"
echo "- Status serviços: systemctl status nginx rpa-websocket redis-server"







