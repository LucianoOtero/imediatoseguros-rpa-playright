#!/usr/bin/env python3
"""
Configurações do ambiente
"""

# Configurações do Chrome
CHROME_OPTIONS = {
    "no_sandbox": True,
    "disable_dev_shm_usage": True,
    "disable_blink_features": "AutomationControlled",
    "disable_extensions": True,
    "disable_plugins": True,
    "disable_images": True,
    "disable_javascript": False,  # Manter JavaScript para funcionalidade
    "disable_css": False,  # Manter CSS para visualização
    "window_size": "1920,1080"
}

# Timeouts
TIMEOUTS = {
    "pagina": 30,
    "elemento": 20,
    "clicavel": 8,
    "estabilizacao": 5
}

# URLs
URLS = {
    "base": "https://cotacaoseguroonline.com.br/",
    "cotacao": "https://cotacaoseguroonline.com.br/cotacao"
}

# Diretórios
DIRETORIOS = {
    "screenshots": "screenshots",
    "logs": "logs",
    "estados": "estados"
}

# Configurações de retry
RETRY_CONFIG = {
    "max_tentativas": 3,
    "delay_entre_tentativas": 2
}
