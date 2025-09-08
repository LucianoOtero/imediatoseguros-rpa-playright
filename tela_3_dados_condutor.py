#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tela 3 - Dados do Condutor
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


def navegar_tela_3_playwright(page: Page, condutor: Dict[str, Any]) -> bool:
    """
    Navega pela Tela 3 - Dados do Condutor
    """
    try:
        exibir_mensagem("🎯 NAVEGANDO PARA TELA 3 - DADOS DO CONDUTOR")
        
        # Aguardar carregamento inicial
        esperar_carregamento_pagina(page)
        
        # Nome do condutor
        if 'nome' in condutor:
            nome_input = page.get_by_role("textbox", name="Nome do condutor")
            nome_input.fill(condutor['nome'])
            exibir_mensagem("✅ Nome do condutor preenchido")
        
        # CPF do condutor
        if 'cpf' in condutor:
            cpf_input = page.get_by_role("textbox", name="CPF do condutor")
            cpf_input.fill(condutor['cpf'])
            exibir_mensagem("✅ CPF do condutor preenchido")
        
        # Data de nascimento do condutor
        if 'data_nascimento' in condutor:
            data_input = page.get_by_role("textbox", name="Data de nascimento")
            data_input.fill(condutor['data_nascimento'])
            exibir_mensagem("✅ Data de nascimento preenchida")
        
        # Tempo de habilitação
        if 'tempo_habilitacao' in condutor:
            tempo_input = page.get_by_role("textbox", name="Tempo de habilitação")
            tempo_input.fill(str(condutor['tempo_habilitacao']))
            exibir_mensagem("✅ Tempo de habilitação preenchido")
        
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





