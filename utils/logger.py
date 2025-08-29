#!/usr/bin/env python3
"""
Sistema de logs para o projeto
"""

import logging
import os
from datetime import datetime

def configurar_logger(nome="cotacao_seguro"):
    """Configura o sistema de logs"""
    
    # Criar diretório de logs se não existir
    if not os.path.exists("logs"):
        os.makedirs("logs")
    
    # Nome do arquivo de log
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_arquivo = f"logs/{nome}_{timestamp}.log"
    
    # Configurar logger
    logger = logging.getLogger(nome)
    logger.setLevel(logging.INFO)
    
    # Handler para arquivo
    file_handler = logging.FileHandler(nome_arquivo, encoding="utf-8")
    file_handler.setLevel(logging.INFO)
    
    # Handler para console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # Formato
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Adicionar handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

def log_tela(logger, numero_tela, etapa, mensagem):
    """Log específico para telas"""
    logger.info(f"TELA {numero_tela} - {etapa}: {mensagem}")

def log_erro(logger, numero_tela, etapa, erro):
    """Log de erro para telas"""
    logger.error(f"TELA {numero_tela} - {etapa} - ERRO: {erro}")

def log_sucesso(logger, numero_tela, etapa):
    """Log de sucesso para telas"""
    logger.info(f"TELA {numero_tela} - {etapa}: ✅ SUCESSO")
