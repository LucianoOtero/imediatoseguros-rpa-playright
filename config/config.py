import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Configurações do Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'imediatoseguros-rpa-2024')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # Configurações do Redis
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    
    # Configurações do Celery
    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
    CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
    
    # Configurações do Selenium
    SELENIUM_HEADLESS = os.getenv('SELENIUM_HEADLESS', 'True').lower() == 'true'
    SELENIUM_TIMEOUT = int(os.getenv('SELENIUM_TIMEOUT', '30'))
    
    # URLs dos sites
    TOSEGURADO_URL = "https://www.app.tosegurado.com.br/imediatosolucoes"
    IMEDIATO_WEBSITE = "https://www.segurosimediato.com.br"
    
    # Tipos de seguro suportados
    SUPPORTED_INSURANCE_TYPES = ['auto', 'moto']
    
    # Configurações de log
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = '/opt/imediatoseguros-rpa/logs/rpa.log'
