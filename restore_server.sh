#!/bin/bash
# restore_server.sh
# Script para restaurar backup completo em novo servidor

BACKUP_DIR="$(dirname "$0")"
LOG_FILE="/var/log/server_restore.log"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Iniciando restauração do servidor" | tee -a "$LOG_FILE"

# Verificar se está rodando como root
if [ "$EUID" -ne 0 ]; then
    echo "Este script deve ser executado como root"
    exit 1
fi

# 1. Instalar dependências
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Instalando dependências..." | tee -a "$LOG_FILE"
apt update
apt install -y nginx php8.3-fpm php8.3-mysql php8.3-curl mysql-server

# 2. Restaurar arquivos web
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Restaurando arquivos web..." | tee -a "$LOG_FILE"
tar -xzf "$BACKUP_DIR/web_files.tar.gz" -C /var/www/html/

# 3. Restaurar configurações do sistema
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Restaurando configurações do sistema..." | tee -a "$LOG_FILE"
cp -r "$BACKUP_DIR/config/nginx" /etc/
cp -r "$BACKUP_DIR/config/php" /etc/
cp -r "$BACKUP_DIR/config/mysql" /etc/

# 4. Restaurar banco de dados
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Restaurando banco de dados..." | tee -a "$LOG_FILE"
mysql -u root -p < "$BACKUP_DIR/database_backup.sql"

# 5. Restaurar usuários e grupos
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Restaurando usuários e grupos..." | tee -a "$LOG_FILE"
cp "$BACKUP_DIR/config/passwd" /etc/
cp "$BACKUP_DIR/config/group" /etc/
cp "$BACKUP_DIR/config/shadow" /etc/

# 6. Restaurar chaves SSH
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Restaurando chaves SSH..." | tee -a "$LOG_FILE"
cp -r "$BACKUP_DIR/config/.ssh" /root/

# 7. Restaurar cron jobs
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Restaurando cron jobs..." | tee -a "$LOG_FILE"
crontab "$BACKUP_DIR/config/crontab_root.txt"

# 8. Configurar permissões
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Configurando permissões..." | tee -a "$LOG_FILE"
chown -R www-data:www-data /var/www/html
chmod -R 755 /var/www/html
chmod 644 /var/www/html/*.php

# 9. Reiniciar serviços
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Reiniciando serviços..." | tee -a "$LOG_FILE"
systemctl restart nginx
systemctl restart php8.3-fpm
systemctl restart mysql

# 10. Verificar status dos serviços
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Verificando status dos serviços..." | tee -a "$LOG_FILE"
systemctl status nginx --no-pager
systemctl status php8.3-fpm --no-pager
systemctl status mysql --no-pager

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Restauração concluída!" | tee -a "$LOG_FILE"

































