#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tela 3 - Confirmação do Veículo
Módulo isolado para navegação da Tela 3 com comunicação em tempo real
"""

import time
import logging
from typing import Dict, Any, Optional
from playwright.sync_api import Page
from datetime import datetime

# Importar módulos de comunicação
try:
    from utils.communication_manager import communication_manager
    from utils.redis_manager import redis_manager
    from utils.websocket_manager import websocket_manager
    COMMUNICATION_AVAILABLE = True
except ImportError:
    COMMUNICATION_AVAILABLE = False
    communication_manager = None
    redis_manager = None
    websocket_manager = None

# Configurar logging
logger = logging.getLogger(__name__)


def exibir_mensagem(mensagem: str, session_id: Optional[str] = None):
    """Exibe mensagem formatada e envia via comunicação"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    formatted_message = f"[{timestamp}] {mensagem}"
    
    # Exibir no console
    print(formatted_message)
    
    # Enviar via comunicação se disponível
    if COMMUNICATION_AVAILABLE and session_id:
        try:
            websocket_manager.send_status_update(
                session_id, 
                "info", 
                mensagem
            )
        except Exception as e:
            logger.warning(f"Falha ao enviar mensagem via comunicação: {e}")


def esperar_carregamento_pagina(page: Page, timeout: int = 30):
    """Espera o carregamento completo da página"""
    try:
        page.wait_for_load_state("networkidle", timeout=timeout * 1000)
        time.sleep(2)
    except Exception as e:
        exibir_mensagem(f"⚠️ Timeout no carregamento da página: {e}")


def navegar_tela_3_playwright(page: Page, veiculo_segurado: Dict[str, Any], session_id: Optional[str] = None) -> bool:
    """
    Navega pela Tela 3 - Confirmação do Veículo com comunicação em tempo real
    """
    try:
        exibir_mensagem("🎯 NAVEGANDO PARA TELA 3 - CONFIRMAÇÃO DO VEÍCULO", session_id)
        
        # Atualizar progresso
        if COMMUNICATION_AVAILABLE and session_id:
            communication_manager.update_progress(session_id, {
                "tela_atual": "Tela 3 - Confirmação do Veículo",
                "status": "iniciando",
                "progresso": 10,
                "timestamp": datetime.now().isoformat()
            })
        
        # Aguardar carregamento inicial
        esperar_carregamento_pagina(page)
        
        # Confirmar dados do veículo (marca, modelo, ano, cor)
        if 'marca' in veiculo_segurado:
            marca_select = page.get_by_role("combobox", name="Marca")
            marca_select.select_option(label=veiculo_segurado['marca'])
            exibir_mensagem("✅ Marca selecionada", session_id)
            
            # Atualizar progresso
            if COMMUNICATION_AVAILABLE and session_id:
                communication_manager.update_progress(session_id, {
                    "tela_atual": "Tela 3 - Confirmação do Veículo",
                    "status": "marca_selecionada",
                    "progresso": 30,
                    "marca": veiculo_segurado['marca'],
                    "timestamp": datetime.now().isoformat()
                })
        
        if 'modelo' in veiculo_segurado:
            modelo_select = page.get_by_role("combobox", name="Modelo")
            modelo_select.select_option(label=veiculo_segurado['modelo'])
            exibir_mensagem("✅ Modelo selecionado", session_id)
            
            # Atualizar progresso
            if COMMUNICATION_AVAILABLE and session_id:
                communication_manager.update_progress(session_id, {
                    "tela_atual": "Tela 3 - Confirmação do Veículo",
                    "status": "modelo_selecionado",
                    "progresso": 50,
                    "modelo": veiculo_segurado['modelo'],
                    "timestamp": datetime.now().isoformat()
                })
        
        if 'ano' in veiculo_segurado:
            ano_select = page.get_by_role("combobox", name="Ano")
            ano_select.select_option(label=str(veiculo_segurado['ano']))
            exibir_mensagem("✅ Ano selecionado", session_id)
            
            # Atualizar progresso
            if COMMUNICATION_AVAILABLE and session_id:
                communication_manager.update_progress(session_id, {
                    "tela_atual": "Tela 3 - Confirmação do Veículo",
                    "status": "ano_selecionado",
                    "progresso": 70,
                    "ano": veiculo_segurado['ano'],
                    "timestamp": datetime.now().isoformat()
                })
        
        if 'cor' in veiculo_segurado:
            cor_select = page.get_by_role("combobox", name="Cor")
            cor_select.select_option(label=veiculo_segurado['cor'])
            exibir_mensagem("✅ Cor selecionada", session_id)
            
            # Atualizar progresso
            if COMMUNICATION_AVAILABLE and session_id:
                communication_manager.update_progress(session_id, {
                    "tela_atual": "Tela 3 - Confirmação do Veículo",
                    "status": "cor_selecionada",
                    "progresso": 80,
                    "cor": veiculo_segurado['cor'],
                    "timestamp": datetime.now().isoformat()
                })
        
        # Botão Continuar
        continuar_button = page.get_by_role("button", name="Continuar")
        continuar_button.click()
        exibir_mensagem("✅ Botão Continuar clicado", session_id)
        
        # Atualizar progresso
        if COMMUNICATION_AVAILABLE and session_id:
            communication_manager.update_progress(session_id, {
                "tela_atual": "Tela 3 - Confirmação do Veículo",
                "status": "navegando",
                "progresso": 90,
                "timestamp": datetime.now().isoformat()
            })
        
        # Aguardar navegação
        time.sleep(3)
        
        # Atualizar progresso final
        if COMMUNICATION_AVAILABLE and session_id:
            communication_manager.update_progress(session_id, {
                "tela_atual": "Tela 3 - Confirmação do Veículo",
                "status": "concluida",
                "progresso": 100,
                "timestamp": datetime.now().isoformat()
            })
        
        exibir_mensagem("✅ TELA 3 CONCLUÍDA!", session_id)
        return True
        
    except Exception as e:
        error_msg = f"❌ ERRO NA TELA 3: {e}"
        exibir_mensagem(error_msg, session_id)
        
        # Enviar erro via comunicação
        if COMMUNICATION_AVAILABLE and session_id:
            communication_manager.send_error(session_id, error_msg, {
                "tela": "Tela 3 - Confirmação do Veículo",
                "erro": str(e),
                "timestamp": datetime.now().isoformat()
            })
        
        return False

















