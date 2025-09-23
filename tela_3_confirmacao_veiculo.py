#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tela 3 - Confirmação do Veículo
Módulo isolado para navegação da Tela 3
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


def navegar_tela_3_playwright(page: Page, veiculo_segurado: Dict[str, Any]) -> bool:
    """
    Navega pela Tela 3 - Confirmação do Veículo
    """
    try:
        exibir_mensagem("🎯 NAVEGANDO PARA TELA 3 - CONFIRMAÇÃO DO VEÍCULO")
        
        # Aguardar carregamento inicial
        esperar_carregamento_pagina(page)
        
        # Confirmar dados do veículo (marca, modelo, ano, cor)
        if 'marca' in veiculo_segurado:
            marca_select = page.get_by_role("combobox", name="Marca")
            marca_select.select_option(label=veiculo_segurado['marca'])
            exibir_mensagem("✅ Marca selecionada")
        
        if 'modelo' in veiculo_segurado:
            modelo_select = page.get_by_role("combobox", name="Modelo")
            modelo_select.select_option(label=veiculo_segurado['modelo'])
            exibir_mensagem("✅ Modelo selecionado")
        
        if 'ano' in veiculo_segurado:
            ano_select = page.get_by_role("combobox", name="Ano")
            ano_select.select_option(label=str(veiculo_segurado['ano']))
            exibir_mensagem("✅ Ano selecionado")
        
        if 'cor' in veiculo_segurado:
            cor_select = page.get_by_role("combobox", name="Cor")
            cor_select.select_option(label=veiculo_segurado['cor'])
            exibir_mensagem("✅ Cor selecionada")
        
        # Botão Continuar
        continuar_button = page.get_by_role("button", name="Continuar")
        continuar_button.click()
        exibir_mensagem("✅ Botão Continuar clicado")
        
        # Aguardar navegação
        time.sleep(3)
        
        exibir_mensagem("✅ TELA 3 CONCLUÍDA!")
        return True
        
    except Exception as e:
        exibir_mensagem(f"❌ ERRO NA TELA 3: {e}")
        return False











