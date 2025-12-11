#!/bin/bash
# backup_server_complete.sh
# Script para fazer backup completo do servidor atual

BACKUP_DIR="/tmp/server_backup_$(date +%Y%m%d_%H%M%S)"
LOG_FILE="/var/log/server_backup.log"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Iniciando backup completo do servidor" | tee -a "$LOG_FILE"

# Criar diretório de backup
mkdir -p "$BACKUP_DIR"

# 1. Backup dos arquivos web
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Fazendo backup dos arquivos web..." | tee -a "$LOG_FILE"
tar -czf "$BACKUP_DIR/web_files.tar.gz" -C /var/www/html .

# 2. Backup das configurações do sistema
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Fazendo backup das configurações do sistema..." | tee -a "$LOG_FILE"
mkdir -p "$BACKUP_DIR/config"
cp -r /etc/nginx "$BACKUP_DIR/config/"
cp -r /etc/php "$BACKUP_DIR/config/"
cp -r /etc/mysql "$BACKUP_DIR/config/"

# 3. Backup do banco de dados
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Fazendo backup do banco de dados..." | tee -a "$LOG_FILE"
mysqldump -u root -p --all-databases > "$BACKUP_DIR/database_backup.sql"

# 4. Backup dos logs
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Fazendo backup dos logs..." | tee -a "$LOG_FILE"
tar -czf "$BACKUP_DIR/logs.tar.gz" -C /var/log .

# 5. Backup das configurações de usuários e grupos
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Fazendo backup de usuários e grupos..." | tee -a "$LOG_FILE"
cp /etc/passwd "$BACKUP_DIR/config/"
cp /etc/group "$BACKUP_DIR/config/"
cp /etc/shadow "$BACKUP_DIR/config/"

# 6. Backup das chaves SSH
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Fazendo backup das chaves SSH..." | tee -a "$LOG_FILE"
cp -r /root/.ssh "$BACKUP_DIR/config/"

# 7. Backup dos cron jobs
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Fazendo backup dos cron jobs..." | tee -a "$LOG_FILE"
crontab -l > "$BACKUP_DIR/config/crontab_root.txt"

# 8. Backup das variáveis de ambiente
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Fazendo backup das variáveis de ambiente..." | tee -a "$LOG_FILE"
env > "$BACKUP_DIR/config/environment.txt"

# 9. Backup das informações do sistema
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Fazendo backup das informações do sistema..." | tee -a "$LOG_FILE"
uname -a > "$BACKUP_DIR/config/system_info.txt"
lsb_release -a >> "$BACKUP_DIR/config/system_info.txt"
df -h >> "$BACKUP_DIR/config/system_info.txt"
free -h >> "$BACKUP_DIR/config/system_info.txt"

# 10. Criar arquivo de informações do backup
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Criando arquivo de informações do backup..." | tee -a "$LOG_FILE"
cat > "$BACKUP_DIR/backup_info.txt" << EOF
Backup realizado em: $(date)
Servidor origem: $(hostname)
IP origem: $(curl -s ifconfig.me)
Sistema: $(uname -a)
Tamanho total: $(du -sh "$BACKUP_DIR" | cut -f1)
Arquivos incluídos:
- Arquivos web (/var/www/html)
- Configurações do sistema (/etc/nginx, /etc/php, /etc/mysql)
- Banco de dados (todos os databases)
- Logs do sistema (/var/log)
- Usuários e grupos
- Chaves SSH
- Cron jobs
- Variáveis de ambiente
- Informações do sistema
EOF

# 11. Criar arquivo compactado final
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Criando arquivo compactado final..." | tee -a "$LOG_FILE"
cd "$(dirname "$BACKUP_DIR")"
tar -czf "server_backup_$(date +%Y%m%d_%H%M%S).tar.gz" "$(basename "$BACKUP_DIR")"

# 12. Informações finais
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Backup concluído!" | tee -a "$LOG_FILE"
echo "Arquivo de backup: $(dirname "$BACKUP_DIR")/server_backup_$(date +%Y%m%d_%H%M%S).tar.gz"
echo "Tamanho: $(du -sh "$(dirname "$BACKUP_DIR")/server_backup_$(date +%Y%m%d_%H%M%S).tar.gz" | cut -f1)"
echo "Para restaurar em novo servidor:"
echo "1. Transferir arquivo .tar.gz para novo servidor"
echo "2. Extrair: tar -xzf server_backup_*.tar.gz"
echo "3. Executar script de restauração"

































