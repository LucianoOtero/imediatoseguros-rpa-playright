#!/bin/bash
# check_dependencies.sh

echo "=== Verificação de Dependências ==="

DEPENDENCIES=("jq" "curl" "dos2unix" "php" "systemctl")
MISSING_DEPS=()

for dep in "${DEPENDENCIES[@]}"; do
    if ! command -v "$dep" &> /dev/null; then
        MISSING_DEPS+=("$dep")
    fi
done

if [ ${#MISSING_DEPS[@]} -eq 0 ]; then
    echo "✅ Todas as dependências estão instaladas"
else
    echo "❌ Dependências faltando: ${MISSING_DEPS[*]}"
    echo "Instalando dependências faltantes..."
    
    for dep in "${MISSING_DEPS[@]}"; do
        case $dep in
            "jq")
                apt update && apt install -y jq
                ;;
            "dos2unix")
                apt update && apt install -y dos2unix
                ;;
            *)
                echo "⚠️ Dependência $dep não pode ser instalada automaticamente"
                ;;
        esac
    done
fi

echo "=== Verificação de dependências concluída ==="
