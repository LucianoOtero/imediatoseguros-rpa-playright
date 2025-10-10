#!/bin/bash

# Script de configuração do servidor Hetzner para RPA Imediato Seguros
# Domínio: rpaimediatoseguros.com.br
# IP: 37.27.92.160

echo "🚀 Iniciando configuração do servidor Hetzner..."

# Atualizar sistema
echo "📦 Atualizando sistema..."
sudo apt update && sudo apt upgrade -y

# Instalar dependências básicas
echo "🔧 Instalando dependências..."
sudo apt install -y curl wget git unzip software-properties-common

# Instalar Nginx
echo "🌐 Instalando Nginx..."
sudo apt install -y nginx
sudo systemctl enable nginx
sudo systemctl start nginx

# Instalar PHP 8.3
echo "🐘 Instalando PHP 8.3..."
sudo apt install -y php8.3 php8.3-fpm php8.3-cli php8.3-curl php8.3-gd php8.3-mysql php8.3-xml php8.3-zip php8.3-mbstring php8.3-redis

# Instalar Redis
echo "🔴 Instalando Redis..."
sudo apt install -y redis-server
sudo systemctl enable redis-server
sudo systemctl start redis-server

# Instalar Node.js 18
echo "📦 Instalando Node.js 18..."
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Instalar Python 3.11 e pip
echo "🐍 Instalando Python 3.11..."
sudo apt install -y python3.11 python3.11-pip python3.11-venv

# Instalar Certbot para Let's Encrypt
echo "🔒 Instalando Certbot..."
sudo apt install -y certbot python3-certbot-nginx

# Configurar firewall
echo "🔥 Configurando firewall..."
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw allow 80
sudo ufw allow 443
sudo ufw --force enable

# Criar diretórios do projeto
echo "📁 Criando estrutura de diretórios..."
sudo mkdir -p /var/www/rpaimediatoseguros.com.br
sudo mkdir -p /var/www/rpaimediatoseguros.com.br/api
sudo mkdir -p /var/www/rpaimediatoseguros.com.br/websocket
sudo mkdir -p /var/www/rpaimediatoseguros.com.br/logs

# Configurar permissões
sudo chown -R www-data:www-data /var/www/rpaimediatoseguros.com.br
sudo chmod -R 755 /var/www/rpaimediatoseguros.com.br

echo "✅ Configuração básica concluída!"
echo ""
echo "📋 PRÓXIMOS PASSOS:"
echo "1. Configure os registros DNS do domínio"
echo "2. Execute: sudo certbot --nginx -d rpaimediatoseguros.com.br -d www.rpaimediatoseguros.com.br"
echo "3. Configure o Nginx com os arquivos de configuração"
echo ""
echo "🔍 Verificar status dos serviços:"
echo "sudo systemctl status nginx"
echo "sudo systemctl status redis-server"
echo "sudo systemctl status php8.3-fpm"






























