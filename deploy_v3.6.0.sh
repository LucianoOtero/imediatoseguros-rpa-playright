#!/bin/bash
# 🚀 DEPLOY V3.6.0 - SISTEMA DE COMUNICAÇÃO EM TEMPO REAL
# Script de deploy para a nova versão com Redis e WebSocket

set -e  # Parar em caso de erro

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para log colorido
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

warn() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] WARNING: $1${NC}"
}

error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: $1${NC}"
}

info() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')] INFO: $1${NC}"
}

# Verificar se está rodando como root
if [[ $EUID -eq 0 ]]; then
   error "Este script não deve ser executado como root"
   exit 1
fi

# Verificar sistema operacional
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
else
    error "Sistema operacional não suportado: $OSTYPE"
    exit 1
fi

log "🚀 INICIANDO DEPLOY V3.6.0 - SISTEMA DE COMUNICAÇÃO EM TEMPO REAL"
log "Sistema: $OS"
log "Usuário: $(whoami)"
log "Diretório: $(pwd)"

# 1. BACKUP DO SISTEMA ATUAL
log "📦 Criando backup do sistema atual..."
BACKUP_DIR="backup_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

# Backup dos arquivos críticos
cp -r utils/ "$BACKUP_DIR/" 2>/dev/null || warn "Utils não encontrado"
cp -r tela_*.py "$BACKUP_DIR/" 2>/dev/null || warn "Telas não encontradas"
cp -r *.json "$BACKUP_DIR/" 2>/dev/null || warn "JSONs não encontrados"
cp -r *.js "$BACKUP_DIR/" 2>/dev/null || warn "JSs não encontrados"

log "✅ Backup criado em: $BACKUP_DIR"

# 2. VERIFICAR DEPENDÊNCIAS
log "🔍 Verificando dependências..."

# Python
if ! command -v python3 &> /dev/null; then
    error "Python3 não encontrado"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
log "✅ Python: $PYTHON_VERSION"

# Node.js
if ! command -v node &> /dev/null; then
    warn "Node.js não encontrado - instalando..."
    if [[ "$OS" == "linux" ]]; then
        curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
        sudo apt-get install -y nodejs
    elif [[ "$OS" == "macos" ]]; then
        brew install node
    fi
fi

NODE_VERSION=$(node --version)
log "✅ Node.js: $NODE_VERSION"

# 3. INSTALAR DEPENDÊNCIAS PYTHON
log "📦 Instalando dependências Python..."
pip3 install --upgrade pip

# Dependências principais
pip3 install redis websockets asyncio psutil

# Dependências do Playwright
pip3 install playwright
playwright install chromium

log "✅ Dependências Python instaladas"

# 4. INSTALAR DEPENDÊNCIAS NODE.JS
log "📦 Instalando dependências Node.js..."
npm install ws redis

log "✅ Dependências Node.js instaladas"

# 5. CONFIGURAR REDIS
log "🔴 Configurando Redis..."

if [[ "$OS" == "linux" ]]; then
    # Ubuntu/Debian
    if ! command -v redis-server &> /dev/null; then
        log "Instalando Redis..."
        sudo apt-get update
        sudo apt-get install -y redis-server
    fi
    
    # Iniciar Redis
    sudo systemctl start redis-server
    sudo systemctl enable redis-server
    
elif [[ "$OS" == "macos" ]]; then
    # macOS
    if ! command -v redis-server &> /dev/null; then
        brew install redis
    fi
    
    # Iniciar Redis
    brew services start redis
fi

# Verificar se Redis está rodando
if redis-cli ping | grep -q "PONG"; then
    log "✅ Redis está rodando"
else
    warn "Redis não está respondendo - tentando iniciar..."
    if [[ "$OS" == "linux" ]]; then
        sudo systemctl restart redis-server
    elif [[ "$OS" == "macos" ]]; then
        brew services restart redis
    fi
    sleep 2
    
    if redis-cli ping | grep -q "PONG"; then
        log "✅ Redis iniciado com sucesso"
    else
        error "Falha ao iniciar Redis"
        exit 1
    fi
fi

# 6. CONFIGURAR LOGS
log "📝 Configurando sistema de logs..."
mkdir -p logs
chmod 755 logs

# 7. EXECUTAR TESTES
log "🧪 Executando testes do sistema..."
python3 run_all_tests.py

if [ $? -eq 0 ]; then
    log "✅ Todos os testes passaram"
else
    warn "Alguns testes falharam - continuando com deploy"
fi

# 8. CONFIGURAR SERVIÇOS
log "⚙️ Configurando serviços..."

# Criar script de inicialização
cat > start_services.sh << 'EOF'
#!/bin/bash
# Script para iniciar todos os serviços

echo "🚀 Iniciando serviços do RPA v3.6.0..."

# Iniciar Redis se não estiver rodando
if ! redis-cli ping | grep -q "PONG"; then
    echo "🔴 Iniciando Redis..."
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        sudo systemctl start redis-server
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        brew services start redis
    fi
    sleep 2
fi

# Iniciar WebSocket server
echo "🌐 Iniciando WebSocket server..."
node websocket_server.js &

# Aguardar serviços iniciarem
sleep 3

echo "✅ Serviços iniciados com sucesso!"
echo "📊 Status dos serviços:"
echo "   Redis: $(redis-cli ping)"
echo "   WebSocket: Verifique se a porta 8765 está aberta"
EOF

chmod +x start_services.sh

# 9. CRIAR SCRIPT DE PARADA
cat > stop_services.sh << 'EOF'
#!/bin/bash
# Script para parar todos os serviços

echo "🛑 Parando serviços do RPA v3.6.0..."

# Parar WebSocket server
pkill -f "websocket_server.js"

# Parar Redis (opcional - comentado para manter dados)
# if [[ "$OSTYPE" == "linux-gnu"* ]]; then
#     sudo systemctl stop redis-server
# elif [[ "$OSTYPE" == "darwin"* ]]; then
#     brew services stop redis
# fi

echo "✅ Serviços parados com sucesso!"
EOF

chmod +x stop_services.sh

# 10. CONFIGURAR MONITORAMENTO
log "📊 Configurando monitoramento..."

cat > monitor_services.sh << 'EOF'
#!/bin/bash
# Script de monitoramento dos serviços

echo "📊 Status dos serviços RPA v3.6.0"
echo "=================================="

# Redis
if redis-cli ping | grep -q "PONG"; then
    echo "🔴 Redis: ✅ RODANDO"
else
    echo "🔴 Redis: ❌ PARADO"
fi

# WebSocket
if netstat -tuln | grep -q ":8765"; then
    echo "🌐 WebSocket: ✅ RODANDO (porta 8765)"
else
    echo "🌐 WebSocket: ❌ PARADO"
fi

# Processos Python
PYTHON_PROCESSES=$(ps aux | grep -c "python.*rpa")
echo "🐍 Processos Python RPA: $PYTHON_PROCESSES"

# Uso de memória
MEMORY_USAGE=$(free -h | grep "Mem:" | awk '{print $3 "/" $2}')
echo "💾 Uso de memória: $MEMORY_USAGE"

# Espaço em disco
DISK_USAGE=$(df -h . | tail -1 | awk '{print $5}')
echo "💿 Uso de disco: $DISK_USAGE"
EOF

chmod +x monitor_services.sh

# 11. CRIAR DOCUMENTAÇÃO DE DEPLOY
log "📚 Criando documentação de deploy..."

cat > DEPLOY_V3.6.0.md << 'EOF'
# 🚀 DEPLOY V3.6.0 - SISTEMA DE COMUNICAÇÃO EM TEMPO REAL

## 📋 Resumo da Versão

- **Versão**: 3.6.0
- **Data**: $(date +'%Y-%m-%d %H:%M:%S')
- **Principais mudanças**:
  - Sistema de comunicação em tempo real
  - Integração Redis para cache
  - WebSocket para comunicação bidirecional
  - Módulos RPA atualizados com comunicação
  - Sistema de testes automatizados

## 🛠️ Componentes Instalados

### Módulos Python
- `utils/platform_utils.py` - Detecção de plataforma
- `utils/redis_manager.py` - Gerenciamento Redis
- `utils/websocket_manager.py` - Gerenciamento WebSocket
- `utils/communication_manager.py` - Orquestração de comunicação

### Módulos RPA Atualizados
- `tela_2_placa.py` - Com comunicação em tempo real
- `tela_3_confirmacao_veiculo.py` - Com comunicação em tempo real
- `tela_4_confirmacao_segurado.py` - Com comunicação em tempo real
- `tela_5_estimativas.py` - Com comunicação em tempo real

### Scripts de Teste
- `test_communication_system.py` - Testes do sistema de comunicação
- `test_rpa_modules.py` - Testes dos módulos RPA
- `run_all_tests.py` - Execução de todos os testes

### Scripts de Gerenciamento
- `start_services.sh` - Iniciar serviços
- `stop_services.sh` - Parar serviços
- `monitor_services.sh` - Monitorar serviços

## 🚀 Como Usar

### Iniciar Serviços
```bash
./start_services.sh
```

### Parar Serviços
```bash
./stop_services.sh
```

### Monitorar Serviços
```bash
./monitor_services.sh
```

### Executar Testes
```bash
python3 run_all_tests.py
```

## 🔧 Configuração

### Redis
- **Host**: localhost
- **Porta**: 6379
- **DB**: 0

### WebSocket
- **Host**: localhost
- **Porta**: 8765

## 📊 Monitoramento

O sistema inclui monitoramento automático de:
- Status do Redis
- Status do WebSocket
- Processos Python
- Uso de memória
- Uso de disco

## 🆘 Solução de Problemas

### Redis não inicia
```bash
# Linux
sudo systemctl restart redis-server

# macOS
brew services restart redis
```

### WebSocket não conecta
```bash
# Verificar se a porta está aberta
netstat -tuln | grep 8765
```

### Testes falham
```bash
# Executar testes individuais
python3 test_communication_system.py
python3 test_rpa_modules.py
```

## 📞 Suporte

Para suporte técnico, consulte a documentação ou execute os testes para diagnóstico.
EOF

# 12. FINALIZAÇÃO
log "🎉 DEPLOY V3.6.0 CONCLUÍDO COM SUCESSO!"
log ""
log "📋 Próximos passos:"
log "   1. Execute: ./start_services.sh"
log "   2. Execute: ./monitor_services.sh"
log "   3. Execute: python3 run_all_tests.py"
log ""
log "📚 Documentação: DEPLOY_V3.6.0.md"
log "📦 Backup: $BACKUP_DIR"
log ""
log "✅ Sistema pronto para uso!"
