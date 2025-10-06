#!/bin/bash
# Wrapper para execução padronizada do RPA
set -e

# Configurar ambiente
cd /opt/imediatoseguros-rpa
export PATH="/opt/imediatoseguros-rpa/venv/bin:$PATH"
export PYTHONPATH="/opt/imediatoseguros-rpa:$PYTHONPATH"

# Log de execução
echo "$(date): Starting RPA with args: $@" >> /opt/imediatoseguros-rpa/logs/wrapper.log

# Executar Python
exec /opt/imediatoseguros-rpa/venv/bin/python "$@"
















