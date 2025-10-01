#!/bin/bash
# fix_permissions_enhanced.sh

echo "=== Correção Aprimorada de Permissões ==="

# 1. Verificar impacto antes da correção
echo "1. Verificando impacto antes da correção..."
lsof /opt/imediatoseguros-rpa/scripts/ 2>/dev/null || echo "Nenhum processo usando o diretório"

# 2. Parar serviços para evitar conflitos
echo "2. Parando serviços..."
systemctl stop php8.3-fpm
systemctl stop nginx

# 3. Corrigir proprietário do diretório de scripts
echo "3. Corrigindo proprietário..."
chown -R www-data:www-data /opt/imediatoseguros-rpa/scripts/

# 4. Corrigir permissões do diretório
echo "4. Corrigindo permissões..."
chmod 755 /opt/imediatoseguros-rpa/scripts/

# 5. Verificar integridade dos arquivos existentes
echo "5. Verificando integridade dos arquivos existentes..."
find /opt/imediatoseguros-rpa/scripts/ -type f -exec ls -la {} \;

# 6. Verificar se www-data pode escrever
echo "6. Testando escrita após correção..."
sudo -u www-data touch /opt/imediatoseguros-rpa/scripts/test_write_$(date +%s).txt
if [ $? -eq 0 ]; then
    echo "✅ Escrita bem-sucedida após correção"
    sudo -u www-data rm /opt/imediatoseguros-rpa/scripts/test_write_*.txt
else
    echo "❌ Falha na escrita - CORREÇÃO INSUFICIENTE"
    exit 1
fi

# 7. Reiniciar serviços
echo "7. Reiniciando serviços..."
systemctl start php8.3-fpm
systemctl start nginx

# 8. Verificar status dos serviços
echo "8. Verificando status dos serviços..."
systemctl status php8.3-fpm --no-pager -l
systemctl status nginx --no-pager -l

echo "=== Correção aprimorada de permissões concluída ==="
