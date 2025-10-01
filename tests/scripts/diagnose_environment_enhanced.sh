#!/bin/bash
# diagnose_environment_enhanced.sh

echo "=== Diagnóstico Aprimorado do Ambiente RPA V4 ==="

# 1. Verificar permissões do diretório de scripts
echo "1. Verificando permissões do diretório de scripts..."
ls -la /opt/imediatoseguros-rpa/scripts/

# 2. Verificar proprietário e grupo
echo "2. Verificando proprietário do diretório..."
stat /opt/imediatoseguros-rpa/scripts/

# 3. Verificar usuário do PHP-FPM
echo "3. Verificando usuário do PHP-FPM..."
ps aux | grep php-fpm | head -5

# 4. Verificar se www-data pode escrever
echo "4. Testando escrita como www-data..."
sudo -u www-data touch /opt/imediatoseguros-rpa/scripts/test_write_$(date +%s).txt
if [ $? -eq 0 ]; then
    echo "✅ Escrita bem-sucedida"
    sudo -u www-data rm /opt/imediatoseguros-rpa/scripts/test_write_*.txt
else
    echo "❌ Falha na escrita - PERMISSÕES INCORRETAS"
fi

# 5. Verificar espaço em disco
echo "5. Verificando espaço em disco..."
df -h /opt/imediatoseguros-rpa/

# 6. Verificar logs recentes
echo "6. Verificando logs recentes..."
tail -20 /opt/imediatoseguros-rpa-v4/logs/rpa/app.log

# 7. Verificar dependências
echo "7. Verificando dependências..."
which jq || echo "❌ jq não instalado"
which curl || echo "❌ curl não instalado"
which dos2unix || echo "❌ dos2unix não instalado"

# 8. Verificar conectividade
echo "8. Verificando conectividade..."
curl -s --connect-timeout 5 http://37.27.92.160/api/rpa/health > /dev/null
if [ $? -eq 0 ]; then
    echo "✅ API acessível"
else
    echo "❌ API não acessível"
fi

echo "=== Diagnóstico aprimorado concluído ==="
