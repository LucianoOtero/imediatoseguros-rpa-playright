#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tela 4 - Confirmação de Veículo Segurado
Módulo isolado para navegação da Tela 4
"""

import time
from typing import Dict, Any
from playwright.sync_api import Page


def exibir_mensagem(mensagem: str):
    """Exibe mensagem formatada"""
    from datetime import datetime
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {mensagem}")


def esperar_carregamento_pagina(page: Page, timeout: int = 30):
    """Espera o carregamento completo da página"""
    try:
        page.wait_for_load_state("networkidle", timeout=timeout * 1000)
        time.sleep(2)
    except Exception as e:
        exibir_mensagem(f"⚠️ Timeout no carregamento da página: {e}")


def navegar_tela_4_playwright(page: Page, veiculo_segurado: Dict[str, Any]) -> bool:
    """
    Navega pela Tela 4 - Confirmação de Veículo Segurado
    """
    try:
        exibir_mensagem("🎯 NAVEGANDO PARA TELA 4 - CONFIRMAÇÃO DE VEÍCULO SEGURADO")
        
        # Aguardar carregamento inicial
        esperar_carregamento_pagina(page)
        
        # Confirmar que o veículo está segurado
        # Esta tela geralmente é apenas de confirmação/leitura
        # Pode ter botões como "Sim, está segurado" ou "Continuar"
        
        # Botão de confirmação (pode variar o nome)
        try:
            confirmar_button = page.get_by_role("button", name="Sim, está segurado")
            confirmar_button.click()
            exibir_mensagem("✅ Confirmação de veículo segurado clicada")
        except:
            # Tentar botão alternativo
            try:
                continuar_button = page.get_by_role("button", name="Continuar")
                continuar_button.click()
                exibir_mensagem("✅ Botão Continuar clicado")
            except:
                # Se não encontrar botão específico, aguardar e continuar
                exibir_mensagem("⚠️ Botão de confirmação não encontrado, aguardando...")
                time.sleep(5)
        
        # Aguardar navegação
        time.sleep(3)
        
        exibir_mensagem("✅ TELA 4 CONCLUÍDA!")
        return True
        
    except Exception as e:
        exibir_mensagem(f"❌ ERRO NA TELA 4: {e}")
        return False
















