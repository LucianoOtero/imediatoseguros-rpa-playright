#!/bin/bash
# sync_servers.sh
# Script para sincronização incremental entre servidores

SOURCE_SERVER="root@bpsegurosimediato.com.br"
TARGET_SERVER="root@test.bpsegurosimediato.com.br"
LOG_FILE="/var/log/server_sync.log"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Iniciando sincronização entre servidores" | tee -a "$LOG_FILE"

# 1. Sincronizar arquivos web
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Sincronizando arquivos web..." | tee -a "$LOG_FILE"
rsync -avz --delete \
    --exclude="*.log" \
    --exclude="*.tmp" \
    --exclude="logs/" \
    "$SOURCE_SERVER:/var/www/html/" \
    "$TARGET_SERVER:/var/www/html/"

# 2. Sincronizar configurações do sistema
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Sincronizando configurações do sistema..." | tee -a "$LOG_FILE"
rsync -avz --delete \
    "$SOURCE_SERVER:/etc/nginx/" \
    "$TARGET_SERVER:/etc/nginx/"

rsync -avz --delete \
    "$SOURCE_SERVER:/etc/php/" \
    "$TARGET_SERVER:/etc/php/"

# 3. Sincronizar banco de dados
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Sincronizando banco de dados..." | tee -a "$LOG_FILE"
ssh "$SOURCE_SERVER" "mysqldump -u root -p --all-databases" | \
ssh "$TARGET_SERVER" "mysql -u root -p"

# 4. Sincronizar logs (opcional)
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Sincronizando logs..." | tee -a "$LOG_FILE"
rsync -avz \
    "$SOURCE_SERVER:/var/www/html/logs/" \
    "$TARGET_SERVER:/var/www/html/logs/"

# 5. Reiniciar serviços no servidor de destino
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Reiniciando serviços no servidor de destino..." | tee -a "$LOG_FILE"
ssh "$TARGET_SERVER" "systemctl restart nginx"
ssh "$TARGET_SERVER" "systemctl restart php8.3-fpm"
ssh "$TARGET_SERVER" "systemctl restart mysql"

# 6. Verificar status dos serviços
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Verificando status dos serviços..." | tee -a "$LOG_FILE"
ssh "$TARGET_SERVER" "systemctl status nginx --no-pager"
ssh "$TARGET_SERVER" "systemctl status php8.3-fpm --no-pager"
ssh "$TARGET_SERVER" "systemctl status mysql --no-pager"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Sincronização concluída!" | tee -a "$LOG_FILE"

































