#!/bin/bash
# rollback_enhanced.sh

echo "=== Rollback Aprimorado ==="

# 1. Parar serviços
echo "1. Parando serviços..."
systemctl stop php8.3-fpm
systemctl stop nginx

# 2. Restaurar permissões originais
echo "2. Restaurando permissões originais..."
if [ -f "/opt/imediatoseguros-rpa/backup_*/permissions_backup.txt" ]; then
    chown -R root:root /opt/imediatoseguros-rpa/scripts/
    chmod 755 /opt/imediatoseguros-rpa/scripts/
    echo "✅ Permissões restauradas"
else
    echo "⚠️ Backup de permissões não encontrado"
fi

# 3. Restaurar código original
echo "3. Restaurando código original..."
if [ -f "/opt/imediatoseguros-rpa-v4/src/Services/SessionService.php.backup.*" ]; then
    BACKUP_FILE=$(ls -t /opt/imediatoseguros-rpa-v4/src/Services/SessionService.php.backup.* | head -1)
    cp "$BACKUP_FILE" /opt/imediatoseguros-rpa-v4/src/Services/SessionService.php
    echo "✅ Código restaurado"
else
    echo "⚠️ Backup de código não encontrado"
fi

# 4. Reiniciar serviços
echo "4. Reiniciando serviços..."
systemctl start php8.3-fpm
systemctl start nginx

# 5. Verificar status
echo "5. Verificando status..."
systemctl status php8.3-fpm --no-pager -l
systemctl status nginx --no-pager -l

# 6. Teste de validação
echo "6. Teste de validação..."
curl -s http://37.27.92.160/api/rpa/health | jq -r '.health.status'

echo "=== Rollback aprimorado concluído ==="
