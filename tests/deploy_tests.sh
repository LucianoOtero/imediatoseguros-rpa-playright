#!/bin/bash
# Script para fazer deploy dos testes no servidor Hetzner

# Configurações
SERVER="root@37.27.92.160"
REMOTE_DIR="/opt/imediatoseguros-rpa/tests"
LOCAL_DIR="tests"

echo "=== Deploy dos Testes para o Servidor Hetzner ==="

# Verificar se estamos no diretório correto
if [ ! -d "$LOCAL_DIR" ]; then
    echo "Erro: Diretório $LOCAL_DIR não encontrado"
    echo "Execute este script a partir da raiz do projeto"
    exit 1
fi

# Criar diretório remoto
echo "Criando diretório remoto..."
ssh "$SERVER" "mkdir -p $REMOTE_DIR"

# Fazer upload dos arquivos
echo "Fazendo upload dos arquivos..."
scp -r "$LOCAL_DIR"/* "$SERVER:$REMOTE_DIR/"

# Tornar scripts executáveis
echo "Tornando scripts executáveis..."
ssh "$SERVER" "chmod +x $REMOTE_DIR/scripts/*.sh $REMOTE_DIR/config/*.sh"

# Verificar se o deploy foi bem-sucedido
echo "Verificando deploy..."
ssh "$SERVER" "ls -la $REMOTE_DIR/"

echo "=== Deploy concluído com sucesso ==="
echo "Para executar os testes, conecte-se ao servidor:"
echo "ssh $SERVER"
echo "cd $REMOTE_DIR/scripts"
echo "./test_prepare.sh"
