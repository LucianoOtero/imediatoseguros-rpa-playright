#!/usr/bin/env python3
"""
Tarefas Celery para processamento de seguros Auto e Moto
Integrado com automação completa do ToSegurado
"""

import logging
import time
import os
from celery import Celery
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from config.config import Config

# Importar automação completa
from tosegurado_complete import execute_tosegurado_complete_quote

logger = logging.getLogger(__name__)

# Inicializar Celery
celery = Celery('imediatoseguros_rpa')
celery.config_from_object(Config)

@celery.task(bind=True)
def process_auto_quote(self, data):
    """
    Processar cotação de seguro auto usando RPA COMPLETO
    """
    try:
        logger.info(f"Iniciando cotação auto para: {data.get('nome', 'N/A')}")
        
        # Atualizar status
        self.update_state(
            state='PROGRESS',
            meta={'progress': 10, 'message': 'Iniciando cotação de seguro auto...'}
        )
        
        # Preparar dados para ToSegurado
        quote_data = {
            'placa': data['placa'],
            'cpf': data['cpf'],
            'nome': data['nome'],
            'email': data['email'],
            'telefone': data['telefone'],
            'marca': data.get('marca', 'NISSAN'),
            'modelo': data.get('modelo', 'MARCH'),
            'ano': data['ano'],
            'cep': data.get('cep', '03317-000'),
            'combustivel': 'Flex',
            'uso': 'Pessoal',
            'data_nascimento': '09/02/1965',
            'sexo': 'Masculino',
            'estado_civil': 'Casado ou União Estável'
        }
        
        self.update_state(
            state='PROGRESS',
            meta={'progress': 30, 'message': 'Executando automação no ToSegurado...'}
        )
        
        # Executar automação completa
        result = execute_tosegurado_complete_quote(quote_data)
        
        if result and result.get('success'):
            self.update_state(
                state='PROGRESS',
                meta={'progress': 90, 'message': 'Finalizando cotação...'}
            )
            
            # Processar resultado
            prices = result.get('prices', {})
            
            # Criar resultado final
            final_result = {
                'success': True,
                'message': 'Cotação de seguro auto processada com sucesso via ToSegurado',
                'tipo': 'auto',
                'quote_id': f'AUTO{int(time.time())}',
                'data': data,
                'precos_reais': prices,
                'fonte': 'ToSegurado',
                'timestamp': time.time()
            }
            
            logger.info(f"Cotação auto concluída: {final_result['quote_id']}")
            return final_result
            
        else:
            error_msg = result.get('error', 'Erro desconhecido na automação') if result else 'Falha na automação'
            raise Exception(f"Falha na automação do ToSegurado: {error_msg}")
            
    except Exception as e:
        error_msg = f"Erro no processamento da cotação auto: {str(e)}"
        logger.error(error_msg)
        raise Exception(error_msg)

@celery.task(bind=True)
def process_moto_quote(self, data):
    """
    Processar cotação de seguro moto usando RPA COMPLETO
    """
    try:
        logger.info(f"Iniciando cotação moto para: {data.get('nome', 'N/A')}")
        
        # Atualizar status
        self.update_state(
            state='PROGRESS',
            meta={'progress': 10, 'message': 'Iniciando cotação de seguro moto...'}
        )
        
        # Preparar dados para ToSegurado
        quote_data = {
            'placa': data['placa'],
            'cpf': data['cpf'],
            'nome': data['nome'],
            'email': data['email'],
            'telefone': data['telefone'],
            'marca': data.get('marca', 'HONDA'),
            'modelo': data.get('modelo', 'CG'),
            'ano': data['ano'],
            'cep': data.get('cep', '03317-000'),
            'combustivel': 'Flex',
            'uso': 'Pessoal',
            'data_nascimento': '09/02/1965',
            'sexo': 'Masculino',
            'estado_civil': 'Casado ou União Estável'
        }
        
        self.update_state(
            state='PROGRESS',
            meta={'progress': 30, 'message': 'Executando automação no ToSegurado...'}
        )
        
        # Executar automação completa
        result = execute_tosegurado_complete_quote(quote_data)
        
        if result and result.get('success'):
            self.update_state(
                state='PROGRESS',
                meta={'progress': 90, 'message': 'Finalizando cotação...'}
            )
            
            # Processar resultado
            prices = result.get('prices', {})
            
            # Criar resultado final
            final_result = {
                'success': True,
                'message': 'Cotação de seguro moto processada com sucesso via ToSegurado',
                'tipo': 'moto',
                'quote_id': f'MOTO{int(time.time())}',
                'result': data,
                'precos_reais': prices,
                'fonte': 'ToSegurado',
                'timestamp': time.time()
            }
            
            logger.info(f"Cotação moto concluída: {final_result['quote_id']}")
            return final_result
            
        else:
            error_msg = result.get('error', 'Erro desconhecido na automação') if result else 'Falha na automação'
            raise Exception(f"Falha na automação do ToSegurado: {error_msg}")
            
    except Exception as e:
        error_msg = f"Erro no processamento da cotação moto: {str(e)}"
        logger.error(error_msg)
        raise Exception(error_msg)

@celery.task
def health_check():
    """Verificação de saúde das tarefas"""
    return {'status': 'healthy', 'timestamp': time.time()}
