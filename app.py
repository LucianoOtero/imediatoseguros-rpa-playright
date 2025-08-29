#!/usr/bin/env python3
"""
Sistema RPA Imediato Seguros - Auto e Moto
Aplicação principal Flask para automação de cotações
"""

import os
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from celery import Celery
from config.config import Config

# Configurar logging
logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(Config.LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Inicializar Flask
app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

# Inicializar Celery
celery = Celery('imediatoseguros_rpa')
celery.config_from_object(Config)

# Importar tarefas APÓS inicializar o Celery
from tasks import process_auto_quote, process_moto_quote

@app.route('/health', methods=['GET'])
def health_check():
    """Verificação de saúde da aplicação"""
    return jsonify({
        'status': 'healthy',
        'service': 'Imediato Seguros RPA - Auto e Moto',
        'version': '1.0.0',
        'supported_types': Config.SUPPORTED_INSURANCE_TYPES
    })

@app.route('/api/auto/quote', methods=['POST'])
def create_auto_quote():
    """Endpoint para criar cotação de seguro auto"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Dados não fornecidos'}), 400
        
        # Validar dados obrigatórios para auto
        required_fields = ['placa', 'cpf', 'nome', 'email', 'telefone', 'marca', 'modelo', 'ano']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Campo obrigatório para auto: {field}'}), 400
        
        # Adicionar tipo de seguro
        data['tipo_seguro'] = 'auto'
        
        # Enviar para processamento assíncrono
        task = process_auto_quote.delay(data)
        
        return jsonify({
            'message': 'Cotação de seguro auto enviada para processamento',
            'tipo': 'auto',
            'task_id': task.id,
            'status': 'processing'
        }), 202
        
    except Exception as e:
        logger.error(f"Erro ao criar cotação auto: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@app.route('/api/moto/quote', methods=['POST'])
def create_moto_quote():
    """Endpoint para criar cotação de seguro moto"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Dados não fornecidos'}), 400
        
        # Validar dados obrigatórios para moto
        required_fields = ['placa', 'cpf', 'nome', 'email', 'telefone', 'marca', 'modelo', 'ano', 'cilindrada']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Campo obrigatório para moto: {field}'}), 400
        
        # Adicionar tipo de seguro
        data['tipo_seguro'] = 'moto'
        
        # Enviar para processamento assíncrono
        task = process_moto_quote.delay(data)
        
        return jsonify({
            'message': 'Cotação de seguro moto enviada para processamento',
            'tipo': 'moto',
            'task_id': task.id,
            'status': 'processing'
        }), 202
        
    except Exception as e:
        logger.error(f"Erro ao criar cotação moto: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@app.route('/api/quote/<task_id>', methods=['GET'])
def get_quote_status(task_id):
    """Verificar status da cotação"""
    try:
        task = celery.AsyncResult(task_id)
        
        if task.ready():
            if task.successful():
                result = task.result
                return jsonify({
                    'task_id': task_id,
                    'status': 'completed',
                    'result': result
                })
            else:
                return jsonify({
                    'task_id': task_id,
                    'status': 'failed',
                    'error': str(task.info)
                })
        else:
            return jsonify({
                'task_id': task_id,
                'status': 'processing',
                'progress': task.info.get('progress', 0) if task.info else 0
            })
            
    except Exception as e:
        logger.error(f"Erro ao verificar status: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@app.route('/api/supported-types', methods=['GET'])
def get_supported_types():
    """Retornar tipos de seguro suportados"""
    return jsonify({
        'supported_types': Config.SUPPORTED_INSURANCE_TYPES,
        'auto_fields': ['placa', 'cpf', 'nome', 'email', 'telefone', 'marca', 'modelo', 'ano'],
        'moto_fields': ['placa', 'cpf', 'nome', 'email', 'telefone', 'marca', 'modelo', 'ano', 'cilindrada']
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=Config.DEBUG)
