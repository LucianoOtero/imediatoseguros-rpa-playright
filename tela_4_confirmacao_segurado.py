#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tela 4 - Confirmação de Veículo Segurado
Módulo isolado para navegação da Tela 4 com comunicação em tempo real
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


def navegar_tela_4_playwright(page: Page, veiculo_segurado: Dict[str, Any], session_id: Optional[str] = None) -> bool:
    """
    Navega pela Tela 4 - Confirmação de Veículo Segurado com comunicação em tempo real
    """
    try:
        exibir_mensagem("🎯 NAVEGANDO PARA TELA 4 - CONFIRMAÇÃO DE VEÍCULO SEGURADO", session_id)
        
        # Atualizar progresso
        if COMMUNICATION_AVAILABLE and session_id:
            communication_manager.update_progress(session_id, {
                "tela_atual": "Tela 4 - Confirmação de Veículo Segurado",
                "status": "iniciando",
                "progresso": 10,
                "timestamp": datetime.now().isoformat()
            })
        
        # Aguardar carregamento inicial
        esperar_carregamento_pagina(page)
        
        # Confirmar que o veículo está segurado
        # Esta tela geralmente é apenas de confirmação/leitura
        # Pode ter botões como "Sim, está segurado" ou "Continuar"
        
        # Botão de confirmação (pode variar o nome)
        try:
            confirmar_button = page.get_by_role("button", name="Sim, está segurado")
            confirmar_button.click()
            exibir_mensagem("✅ Confirmação de veículo segurado clicada", session_id)
            
            # Atualizar progresso
            if COMMUNICATION_AVAILABLE and session_id:
                communication_manager.update_progress(session_id, {
                    "tela_atual": "Tela 4 - Confirmação de Veículo Segurado",
                    "status": "confirmacao_clicada",
                    "progresso": 50,
                    "timestamp": datetime.now().isoformat()
                })
        except:
            # Tentar botão alternativo
            try:
                continuar_button = page.get_by_role("button", name="Continuar")
                continuar_button.click()
                exibir_mensagem("✅ Botão Continuar clicado", session_id)
                
                # Atualizar progresso
                if COMMUNICATION_AVAILABLE and session_id:
                    communication_manager.update_progress(session_id, {
                        "tela_atual": "Tela 4 - Confirmação de Veículo Segurado",
                        "status": "continuar_clicado",
                        "progresso": 50,
                        "timestamp": datetime.now().isoformat()
                    })
            except:
                # Se não encontrar botão específico, aguardar e continuar
                exibir_mensagem("⚠️ Botão de confirmação não encontrado, aguardando...", session_id)
                time.sleep(5)
        
        # Atualizar progresso
        if COMMUNICATION_AVAILABLE and session_id:
            communication_manager.update_progress(session_id, {
                "tela_atual": "Tela 4 - Confirmação de Veículo Segurado",
                "status": "navegando",
                "progresso": 80,
                "timestamp": datetime.now().isoformat()
            })
        
        # Aguardar navegação
        time.sleep(3)
        
        # Atualizar progresso final
        if COMMUNICATION_AVAILABLE and session_id:
            communication_manager.update_progress(session_id, {
                "tela_atual": "Tela 4 - Confirmação de Veículo Segurado",
                "status": "concluida",
                "progresso": 100,
                "timestamp": datetime.now().isoformat()
            })
        
        exibir_mensagem("✅ TELA 4 CONCLUÍDA!", session_id)
        return True
        
    except Exception as e:
        error_msg = f"❌ ERRO NA TELA 4: {e}"
        exibir_mensagem(error_msg, session_id)
        
        # Enviar erro via comunicação
        if COMMUNICATION_AVAILABLE and session_id:
            communication_manager.send_error(session_id, error_msg, {
                "tela": "Tela 4 - Confirmação de Veículo Segurado",
                "erro": str(e),
                "timestamp": datetime.now().isoformat()
            })
        
        return False

















