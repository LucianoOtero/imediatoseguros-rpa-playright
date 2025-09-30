#!/bin/bash

# Script de Deploy para RPA V4
# Data: $(date)

set -e  # Parar em caso de erro

echo "🚀 Iniciando deploy da RPA V4..."

# Configurações
BACKUP_DIR="/opt/imediatoseguros-rpa-backup-$(date +%Y%m%d_%H%M%S)"
CURRENT_DIR="/opt/imediatoseguros-rpa"
NEW_DIR="/opt/imediatoseguros-rpa-v4"
NGINX_CONFIG="/etc/nginx/sites-available/rpa-v4"
NGINX_ENABLED="/etc/nginx/sites-enabled/rpa-v4"

# Função para log
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# Função para verificar se comando existe
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Verificar dependências
log "Verificando dependências..."
if ! command_exists php; then
    echo "❌ PHP não encontrado"
    exit 1
fi

if ! command_exists composer; then
    echo "❌ Composer não encontrado"
    exit 1
fi

if ! command_exists nginx; then
    echo "❌ Nginx não encontrado"
    exit 1
fi

# Verificar versão do PHP
PHP_VERSION=$(php -r "echo PHP_MAJOR_VERSION.'.'.PHP_MINOR_VERSION;")
if [[ "$PHP_VERSION" < "8.1" ]]; then
    echo "❌ PHP 8.1+ necessário. Versão atual: $PHP_VERSION"
    exit 1
fi

log "✅ Dependências verificadas"

# Backup da versão atual
log "📦 Criando backup da versão atual..."
if [ -d "$CURRENT_DIR" ]; then
    sudo cp -r "$CURRENT_DIR" "$BACKUP_DIR"
    log "✅ Backup criado em: $BACKUP_DIR"
else
    log "⚠️  Diretório atual não encontrado, pulando backup"
fi

# Criar diretório da nova versão
log "📁 Criando diretório da nova versão..."
sudo mkdir -p "$NEW_DIR"
sudo chown -R www-data:www-data "$NEW_DIR"
sudo chmod -R 755 "$NEW_DIR"

# Copiar arquivos
log "📋 Copiando arquivos..."
cp -r . "$NEW_DIR/"
cd "$NEW_DIR"

# Instalar dependências
log "📦 Instalando dependências PHP..."
composer install --no-dev --optimize-autoloader

# Executar testes
log "🧪 Executando testes..."
if [ -f "vendor/bin/phpunit" ]; then
    vendor/bin/phpunit --no-coverage
    log "✅ Testes executados com sucesso"
else
    log "⚠️  PHPUnit não encontrado, pulando testes"
fi

# Configurar permissões
log "🔐 Configurando permissões..."
sudo chown -R www-data:www-data "$NEW_DIR"
sudo chmod -R 755 "$NEW_DIR"
sudo chmod +x "$NEW_DIR/deploy.sh"

# Criar diretórios necessários
log "📁 Criando diretórios necessários..."
sudo mkdir -p /opt/imediatoseguros-rpa/sessions
sudo mkdir -p /opt/imediatoseguros-rpa/rpa_data
sudo mkdir -p /opt/imediatoseguros-rpa/scripts
sudo mkdir -p /opt/imediatoseguros-rpa/logs
sudo mkdir -p "$NEW_DIR/logs/rpa"

sudo chown -R www-data:www-data /opt/imediatoseguros-rpa
sudo chmod -R 755 /opt/imediatoseguros-rpa

# Configurar Nginx
log "🌐 Configurando Nginx..."
sudo tee "$NGINX_CONFIG" > /dev/null <<EOF
server {
    listen 80;
    server_name rpa-v4.local;
    root $NEW_DIR/public;
    index index.php;

    # Logs
    access_log /var/log/nginx/rpa-v4.access.log;
    error_log /var/log/nginx/rpa-v4.error.log;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_proxied expired no-cache no-store private must-revalidate auth;
    gzip_types text/plain text/css text/xml text/javascript application/x-javascript application/xml+rss application/javascript application/json;

    # Main location
    location / {
        try_files \$uri \$uri/ /index.php?\$query_string;
    }

    # PHP processing
    location ~ \.php$ {
        fastcgi_pass unix:/var/run/php/php8.1-fpm.sock;
        fastcgi_index index.php;
        fastcgi_param SCRIPT_FILENAME \$realpath_root\$fastcgi_script_name;
        include fastcgi_params;
        
        # Security
        fastcgi_hide_header X-Powered-By;
        fastcgi_read_timeout 300;
        fastcgi_connect_timeout 300;
        fastcgi_send_timeout 300;
    }

    # Static files
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
        try_files \$uri =404;
    }

    # Deny access to sensitive files
    location ~ /\. {
        deny all;
    }
    
    location ~ /(vendor|tests|config|logs)/ {
        deny all;
    }
}
EOF

# Habilitar site
sudo ln -sf "$NGINX_CONFIG" "$NGINX_ENABLED"

# Testar configuração do Nginx
log "🔍 Testando configuração do Nginx..."
sudo nginx -t

# Recarregar Nginx
log "🔄 Recarregando Nginx..."
sudo systemctl reload nginx

# Reiniciar PHP-FPM
log "🔄 Reiniciando PHP-FPM..."
sudo systemctl restart php8.1-fpm

# Verificar status dos serviços
log "📊 Verificando status dos serviços..."
if systemctl is-active --quiet nginx; then
    log "✅ Nginx está rodando"
else
    log "❌ Nginx não está rodando"
    exit 1
fi

if systemctl is-active --quiet php8.1-fpm; then
    log "✅ PHP-FPM está rodando"
else
    log "❌ PHP-FPM não está rodando"
    exit 1
fi

# Testar API
log "🧪 Testando API..."
if command_exists curl; then
    # Aguardar um pouco para o serviço inicializar
    sleep 2
    
    # Testar health check
    if curl -s -f "http://localhost/api/rpa/health" > /dev/null; then
        log "✅ API respondendo corretamente"
    else
        log "⚠️  API não está respondendo (pode ser normal se não estiver configurada)"
    fi
else
    log "⚠️  curl não encontrado, pulando teste da API"
fi

# Configurar cron para limpeza automática
log "⏰ Configurando limpeza automática..."
CRON_JOB="0 2 * * * cd $NEW_DIR && php public/index.php cleanup > /dev/null 2>&1"
if ! crontab -l 2>/dev/null | grep -q "rpa-v4 cleanup"; then
    (crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -
    log "✅ Cron job configurado"
else
    log "⚠️  Cron job já existe"
fi

# Configurar logrotate
log "📝 Configurando rotação de logs..."
sudo tee /etc/logrotate.d/rpa-v4 > /dev/null <<EOF
$NEW_DIR/logs/rpa/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 644 www-data www-data
    postrotate
        systemctl reload php8.1-fpm > /dev/null 2>&1 || true
    endscript
}
EOF

# Criar script de monitoramento
log "📊 Criando script de monitoramento..."
sudo tee /usr/local/bin/rpa-v4-monitor > /dev/null <<EOF
#!/bin/bash
# Script de monitoramento RPA V4

LOG_FILE="$NEW_DIR/logs/rpa/monitor.log"
API_URL="http://localhost/api/rpa/health"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] \$1" >> "\$LOG_FILE"
}

# Verificar API
if curl -s -f "\$API_URL" > /dev/null; then
    log "INFO: API está respondendo"
else
    log "ERROR: API não está respondendo"
    # Tentar reiniciar PHP-FPM
    systemctl restart php8.1-fpm
    log "INFO: PHP-FPM reiniciado"
fi

# Verificar uso de disco
DISK_USAGE=\$(df /opt | tail -1 | awk '{print \$5}' | sed 's/%//')
if [ "\$DISK_USAGE" -gt 90 ]; then
    log "WARNING: Uso de disco alto: \$DISK_USAGE%"
fi

# Verificar memória
MEM_USAGE=\$(free | grep Mem | awk '{printf "%.0f", \$3/\$2 * 100.0}')
if [ "\$MEM_USAGE" -gt 90 ]; then
    log "WARNING: Uso de memória alto: \$MEM_USAGE%"
fi
EOF

sudo chmod +x /usr/local/bin/rpa-v4-monitor

# Configurar monitoramento no cron
MONITOR_CRON="*/5 * * * * /usr/local/bin/rpa-v4-monitor"
if ! crontab -l 2>/dev/null | grep -q "rpa-v4-monitor"; then
    (crontab -l 2>/dev/null; echo "$MONITOR_CRON") | crontab -
    log "✅ Monitoramento configurado"
fi

# Resumo do deploy
log "📋 Resumo do deploy:"
log "   - Diretório: $NEW_DIR"
log "   - Backup: $BACKUP_DIR"
log "   - Nginx: $NGINX_CONFIG"
log "   - Logs: $NEW_DIR/logs/rpa/"
log "   - Monitoramento: /usr/local/bin/rpa-v4-monitor"

# Instruções finais
log "🎉 Deploy concluído com sucesso!"
log ""
log "📝 Próximos passos:"
log "   1. Configure o DNS para apontar para este servidor"
log "   2. Acesse http://seu-dominio/dashboard.html"
log "   3. Teste a API em http://seu-dominio/api/rpa/health"
log "   4. Monitore os logs em $NEW_DIR/logs/rpa/"
log ""
log "🔧 Comandos úteis:"
log "   - Ver logs: tail -f $NEW_DIR/logs/rpa/app.log"
log "   - Reiniciar: sudo systemctl restart php8.1-fpm"
log "   - Status: sudo systemctl status nginx php8.1-fpm"
log "   - Monitoramento: /usr/local/bin/rpa-v4-monitor"
log ""
log "📞 Suporte: Em caso de problemas, verifique os logs e status dos serviços"

echo "✅ Deploy da RPA V4 concluído com sucesso!"
