#!/bin/bash
# Configurações centralizadas para testes

# URLs e endpoints
export API_URL="https://rpaimediatoseguros.com.br"
export HEALTH_ENDPOINT="/api/rpa/health"
export START_ENDPOINT="/api/rpa/start"
export PROGRESS_ENDPOINT="/api/rpa/progress"

# Timeouts e intervalos
export TIMEOUT=900  # 15 minutos
export POLL_INTERVAL=2
export CONNECTION_TIMEOUT=30

# Dados de teste (aceitável para testes iniciais)
export TEST_DATA='{"cpf":"97137189768","nome":"ALEX KAMINSKI","placa":"EYQ4J41","cep":"03317000","email":"alex.kaminski@imediatoseguros.com.br","celular":"11953288466","ano":"2009"}'

# Diretórios
export RPA_DATA_DIR="/opt/imediatoseguros-rpa/rpa_data"
export SESSIONS_DIR="/opt/imediatoseguros-rpa/sessions"
export SCRIPTS_DIR="/opt/imediatoseguros-rpa/scripts"

# Cores para output
export RED='\033[0;31m'
export GREEN='\033[0;32m'
export YELLOW='\033[1;33m'
export BLUE='\033[0;34m'
export NC='\033[0m' # No Color

# Funções utilitárias
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Função para verificar se comando existe
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Função para validar JSON
validate_json() {
    local json_string="$1"
    if command_exists jq; then
        echo "$json_string" | jq . >/dev/null 2>&1
    else
        echo "$json_string" | python3 -m json.tool >/dev/null 2>&1
    fi
}
