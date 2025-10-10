#!/bin/bash
# Script para configurar o servidor com as otimizações conservadoras

echo "🔧 Configurando servidor para otimizações conservadoras..."

# 1. Criar diretório de logs
echo "📁 Criando diretório de logs..."
mkdir -p logs
chmod 755 logs

# 2. Configurar logrotate básico
echo "📋 Configurando logrotate básico..."
sudo tee /etc/logrotate.d/rpa-basic << EOF
$(pwd)/logs/rpa_basic.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
    create 644 www-data www-data
}
EOF

# 3. Configurar crontab básico
echo "⏰ Configurando crontab básico..."
(crontab -l 2>/dev/null; echo "0 */6 * * * $(pwd)/monitor_basic.sh") | crontab -

# 4. Tornar script executável
echo "🔐 Tornando script executável..."
chmod +x monitor_basic.sh

# 5. Testar configuração
echo "🧪 Testando configuração..."
if [ -f "logs/rpa_basic.log" ]; then
    echo "✅ Log file existe"
else
    echo "📝 Criando log file inicial..."
    touch logs/rpa_basic.log
    chmod 644 logs/rpa_basic.log
fi

echo "✅ Configuração do servidor concluída!"
echo ""
echo "📊 Para testar:"
echo "1. Acesse: http://seu-servidor/dashboard_basic.html"
echo "2. Verifique status: http://seu-servidor/status.php"
echo "3. Execute monitoramento: ./monitor_basic.sh"






















