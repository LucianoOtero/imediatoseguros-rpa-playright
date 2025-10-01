#!/bin/bash
# check_impact.sh

echo "=== Verificação de Impacto ==="

# Verificar processos usando o diretório
echo "1. Verificando processos usando o diretório..."
lsof /opt/imediatoseguros-rpa/scripts/ 2>/dev/null || echo "Nenhum processo usando o diretório"

# Verificar serviços dependentes
echo "2. Verificando serviços dependentes..."
systemctl list-dependencies php8.3-fpm | grep -E "(nginx|apache)" || echo "Nenhum serviço dependente crítico"

# Verificar uso de recursos
echo "3. Verificando uso de recursos..."
df -h /opt/imediatoseguros-rpa/
free -h

# Verificar conectividade
echo "4. Verificando conectividade..."
curl -s --connect-timeout 5 http://37.27.92.160/api/rpa/health > /dev/null
if [ $? -eq 0 ]; then
    echo "✅ API acessível"
else
    echo "❌ API não acessível"
fi

echo "=== Verificação de impacto concluída ==="
