#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tela 1 - Dados Pessoais
Módulo isolado para navegação da Tela 1
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


def navegar_tela_1_playwright(page: Page, parametros: Dict[str, Any]) -> bool:
    """
    Navega pela Tela 1 - Dados Pessoais
    """
    try:
        exibir_mensagem("🎯 NAVEGANDO PARA TELA 1 - DADOS PESSOAIS")
        
        # Aguardar carregamento inicial
        esperar_carregamento_pagina(page)
        
        # Preencher dados pessoais
        dados_pessoais = parametros.get('dados_pessoais', {})
        
        # Nome completo
        if 'nome_completo' in dados_pessoais:
            nome_input = page.get_by_role("textbox", name="Nome completo")
            nome_input.fill(dados_pessoais['nome_completo'])
            exibir_mensagem("✅ Nome preenchido")
        
        # CPF
        if 'cpf' in dados_pessoais:
            cpf_input = page.get_by_role("textbox", name="CPF")
            cpf_input.fill(dados_pessoais['cpf'])
            exibir_mensagem("✅ CPF preenchido")
        
        # Data de nascimento
        if 'data_nascimento' in dados_pessoais:
            data_input = page.get_by_role("textbox", name="Data de nascimento")
            data_input.fill(dados_pessoais['data_nascimento'])
            exibir_mensagem("✅ Data de nascimento preenchida")
        
        # Email
        if 'email' in dados_pessoais:
            email_input = page.get_by_role("textbox", name="E-mail")
            email_input.fill(dados_pessoais['email'])
            exibir_mensagem("✅ Email preenchido")
        
        # Telefone
        if 'telefone' in dados_pessoais:
            telefone_input = page.get_by_role("textbox", name="Telefone")
            telefone_input.fill(dados_pessoais['telefone'])
            exibir_mensagem("✅ Telefone preenchido")
        
        # CEP
        if 'cep' in dados_pessoais:
            cep_input = page.get_by_role("textbox", name="CEP")
            cep_input.fill(dados_pessoais['cep'])
            exibir_mensagem("✅ CEP preenchido")
        
        # Aguardar carregamento do endereço
        time.sleep(3)
        
        # Endereço
        if 'endereco' in dados_pessoais:
            endereco_input = page.get_by_role("textbox", name="Endereço")
            endereco_input.fill(dados_pessoais['endereco'])
            exibir_mensagem("✅ Endereço preenchido")
        
        # Número
        if 'numero' in dados_pessoais:
            numero_input = page.get_by_role("textbox", name="Número")
            numero_input.fill(dados_pessoais['numero'])
            exibir_mensagem("✅ Número preenchido")
        
        # Complemento
        if 'complemento' in dados_pessoais:
            complemento_input = page.get_by_role("textbox", name="Complemento")
            complemento_input.fill(dados_pessoais['complemento'])
            exibir_mensagem("✅ Complemento preenchido")
        
        # Bairro
        if 'bairro' in dados_pessoais:
            bairro_input = page.get_by_role("textbox", name="Bairro")
            bairro_input.fill(dados_pessoais['bairro'])
            exibir_mensagem("✅ Bairro preenchido")
        
        # Cidade
        if 'cidade' in dados_pessoais:
            cidade_input = page.get_by_role("textbox", name="Cidade")
            cidade_input.fill(dados_pessoais['cidade'])
            exibir_mensagem("✅ Cidade preenchida")
        
        # Estado
        if 'estado' in dados_pessoais:
            estado_select = page.get_by_role("combobox", name="Estado")
            estado_select.select_option(label=dados_pessoais['estado'])
            exibir_mensagem("✅ Estado selecionado")
        
        # Botão Continuar
        continuar_button = page.get_by_role("button", name="Continuar")
        continuar_button.click()
        exibir_mensagem("✅ Botão Continuar clicado")
        
        # Aguardar navegação
        time.sleep(3)
        
        exibir_mensagem("✅ TELA 1 CONCLUÍDA!")
        return True
        
    except Exception as e:
        exibir_mensagem(f"❌ ERRO NA TELA 1: {e}")
        return False





