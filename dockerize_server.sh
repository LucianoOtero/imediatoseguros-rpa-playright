#!/bin/bash
# dockerize_server.sh
# Script para containerizar aplicações do servidor

LOG_FILE="/var/log/dockerize_server.log"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Iniciando containerização do servidor" | tee -a "$LOG_FILE"

# 1. Criar Dockerfile para aplicação web
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Criando Dockerfile..." | tee -a "$LOG_FILE"
cat > Dockerfile << 'EOF'
FROM ubuntu:24.04

# Instalar dependências
RUN apt-get update && apt-get install -y \
    nginx \
    php8.3-fpm \
    php8.3-mysql \
    php8.3-curl \
    mysql-server \
    && rm -rf /var/lib/apt/lists/*

# Copiar arquivos da aplicação
COPY /var/www/html/ /var/www/html/
COPY /etc/nginx/ /etc/nginx/
COPY /etc/php/ /etc/php/

# Configurar permissões
RUN chown -R www-data:www-data /var/www/html
RUN chmod -R 755 /var/www/html

# Expor portas
EXPOSE 80 443 3306

# Script de inicialização
COPY start_services.sh /start_services.sh
RUN chmod +x /start_services.sh

CMD ["/start_services.sh"]
EOF

# 2. Criar script de inicialização
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Criando script de inicialização..." | tee -a "$LOG_FILE"
cat > start_services.sh << 'EOF'
#!/bin/bash

# Iniciar MySQL
service mysql start

# Iniciar PHP-FPM
service php8.3-fpm start

# Iniciar Nginx
service nginx start

# Manter container rodando
tail -f /var/log/nginx/access.log
EOF

# 3. Criar docker-compose.yml
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Criando docker-compose.yml..." | tee -a "$LOG_FILE"
cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  web:
    build: .
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./logs:/var/log
      - ./data:/var/lib/mysql
    environment:
      - MYSQL_ROOT_PASSWORD=root_password
    restart: unless-stopped

  mysql:
    image: mysql:8.0
    environment:
      - MYSQL_ROOT_PASSWORD=root_password
      - MYSQL_DATABASE=rpa_logs
    volumes:
      - mysql_data:/var/lib/mysql
    ports:
      - "3306:3306"
    restart: unless-stopped

volumes:
  mysql_data:
EOF

# 4. Criar script de exportação
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Criando script de exportação..." | tee -a "$LOG_FILE"
cat > export_container.sh << 'EOF'
#!/bin/bash
# export_container.sh
# Script para exportar container para novo servidor

echo "Exportando container..."

# Construir imagem
docker-compose build

# Exportar imagem
docker save web_app > web_app.tar

# Exportar volumes
docker run --rm -v web_app_mysql_data:/data -v $(pwd):/backup ubuntu tar czf /backup/mysql_data.tar.gz -C /data .

echo "Arquivos exportados:"
echo "- web_app.tar (imagem Docker)"
echo "- mysql_data.tar.gz (dados do MySQL)"
echo "- docker-compose.yml (configuração)"
EOF

chmod +x export_container.sh

# 5. Criar script de importação
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Criando script de importação..." | tee -a "$LOG_FILE"
cat > import_container.sh << 'EOF'
#!/bin/bash
# import_container.sh
# Script para importar container em novo servidor

echo "Importando container..."

# Instalar Docker
apt update
apt install -y docker.io docker-compose

# Importar imagem
docker load < web_app.tar

# Importar volumes
docker volume create web_app_mysql_data
docker run --rm -v web_app_mysql_data:/data -v $(pwd):/backup ubuntu tar xzf /backup/mysql_data.tar.gz -C /data

# Iniciar serviços
docker-compose up -d

echo "Container importado e iniciado!"
EOF

chmod +x import_container.sh

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Containerização concluída!" | tee -a "$LOG_FILE"
echo "Arquivos criados:"
echo "- Dockerfile"
echo "- docker-compose.yml"
echo "- start_services.sh"
echo "- export_container.sh"
echo "- import_container.sh"
echo ""
echo "Para exportar: ./export_container.sh"
echo "Para importar em novo servidor: ./import_container.sh"

































