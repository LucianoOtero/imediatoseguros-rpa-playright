#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Executor Principal - Telas 1 a 5
Arquivo principal que orquestra a execução das telas 1-5 de forma modular
"""

import json
import time
import os
from datetime import datetime
from typing import Dict, Any
from playwright.sync_api import sync_playwright, Page

# Importar módulos das telas
from tela_1_selecao_carro import navegar_tela_1_playwright
from tela_2_placa import navegar_tela_2_playwright
from tela_3_confirmacao_veiculo import navegar_tela_3_playwright
from tela_4_confirmacao_segurado import navegar_tela_4_playwright
from tela_5_estimativas import (
    navegar_tela_5_playwright,
    capturar_dados_carrossel_estimativas_playwright,
    salvar_dados_json
)

# Configurações
HEADLESS = False
TIMEOUT = 30000


class RPAException(Exception):
    """Exceção personalizada para erros do RPA"""
    pass


class ExceptionHandler:
    """Classe para tratamento de exceções"""
    
    def __init__(self):
        self.errors = []
    
    def add_error(self, error: str, context: str = ""):
        """Adiciona um erro à lista"""
        self.errors.append({
            "error": error,
            "context": context,
            "timestamp": datetime.now().isoformat()
        })
    
    def get_errors(self) -> list:
        """Retorna a lista de erros"""
        return self.errors


def exibir_mensagem(mensagem: str):
    """Exibe mensagem formatada"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {mensagem}")


def carregar_parametros() -> Dict[str, Any]:
    """Carrega parâmetros do arquivo JSON"""
    try:
        with open("config/parametros.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        raise RPAException(f"Erro ao carregar parâmetros: {e}")


def esperar_carregamento_pagina(page: Page, timeout: int = 30):
    """Espera o carregamento completo da página"""
    try:
        page.wait_for_load_state("networkidle", timeout=timeout * 1000)
        time.sleep(2)
    except Exception as e:
        exibir_mensagem(f"⚠️ Timeout no carregamento da página: {e}")


def criar_retorno_sucesso(resultado_telas: Dict[str, bool], dados_extras: Dict[str, Any], 
                         retorno_path: str, tempo_execucao: float, parametros: Dict[str, Any]) -> Dict[str, Any]:
    """Cria retorno de sucesso estruturado"""
    return {
        "sucesso": True,
        "resultado_telas": resultado_telas,
        "dados_extras": dados_extras,
        "retorno_path": retorno_path,
        "tempo_execucao": tempo_execucao,
        "parametros": parametros,
        "timestamp": datetime.now().isoformat()
    }


def criar_retorno_erro(mensagem: str, contexto: str, tempo_execucao: float, 
                      parametros: Dict[str, Any], exception_handler: ExceptionHandler) -> Dict[str, Any]:
    """Cria retorno de erro estruturado"""
    return {
        "sucesso": False,
        "erro": mensagem,
        "contexto": contexto,
        "tempo_execucao": tempo_execucao,
        "parametros": parametros,
        "erros_detalhados": exception_handler.get_errors(),
        "timestamp": datetime.now().isoformat()
    }


def executar_rpa_telas_1_a_5_modular():
    """Função principal para executar as Telas 1-5 de forma modular"""
    inicio_execucao = time.time()
    exception_handler = ExceptionHandler()
    
    try:
        exibir_mensagem("🚀 INICIANDO EXECUÇÃO MODULAR DAS TELAS 1-5")
        exibir_mensagem("=" * 80)
        
        # Carregar parâmetros
        parametros = carregar_parametros()
        exibir_mensagem("✅ Parâmetros carregados")
        
        # Inicializar variáveis de controle
        telas_executadas = 0
        resultado_telas = {}
        dados_tela_5 = None
        
        # Iniciar Playwright
        with sync_playwright() as p:
            # Configurar browser
            browser = p.chromium.launch(
                headless=HEADLESS,
                args=[
                    "--no-sandbox",
                    "--disable-dev-shm-usage",
                    "--disable-web-security",
                    "--disable-features=VizDisplayCompositor"
                ]
            )
            
            # Criar contexto
            context = browser.new_context(
                viewport={"width": 1920, "height": 1080},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
            
            # Criar página
            page = context.new_page()
            page.set_default_timeout(TIMEOUT)
            
            exibir_mensagem("✅ Browser configurado")
            
            # Navegar para a página inicial
            exibir_mensagem("🌐 Navegando para a página inicial...")
            page.goto("https://www.imediatoseguros.com.br/")
            esperar_carregamento_pagina(page)
            
            # TELA 1 - Seleção do Botão Carro
            exibir_mensagem("\n" + "="*50)
            if navegar_tela_1_playwright(page, parametros):
                telas_executadas += 1
                resultado_telas["tela_1"] = True
                exibir_mensagem("✅ TELA 1 CONCLUÍDA!")
            else:
                resultado_telas["tela_1"] = False
                exibir_mensagem("❌ TELA 1 FALHOU!")
                return criar_retorno_erro(
                    "Tela 1 falhou",
                    "TELA_1",
                    time.time() - inicio_execucao,
                    parametros,
                    exception_handler
                )
            
            # TELA 2 - Tela da Placa
            exibir_mensagem("\n" + "="*50)
            if navegar_tela_2_playwright(page, parametros['veiculo_segurado']):
                telas_executadas += 1
                resultado_telas["tela_2"] = True
                exibir_mensagem("✅ TELA 2 CONCLUÍDA!")
            else:
                resultado_telas["tela_2"] = False
                exibir_mensagem("❌ TELA 2 FALHOU!")
                return criar_retorno_erro(
                    "Tela 2 falhou",
                    "TELA_2",
                    time.time() - inicio_execucao,
                    parametros,
                    exception_handler
                )
            
            # TELA 3 - Confirmação do Veículo
            exibir_mensagem("\n" + "="*50)
            if navegar_tela_3_playwright(page, parametros['veiculo_segurado']):
                telas_executadas += 1
                resultado_telas["tela_3"] = True
                exibir_mensagem("✅ TELA 3 CONCLUÍDA!")
            else:
                resultado_telas["tela_3"] = False
                exibir_mensagem("❌ TELA 3 FALHOU!")
                return criar_retorno_erro(
                    "Tela 3 falhou",
                    "TELA_3",
                    time.time() - inicio_execucao,
                    parametros,
                    exception_handler
                )
            
            # TELA 4 - Confirmação de Veículo Segurado
            exibir_mensagem("\n" + "="*50)
            if navegar_tela_4_playwright(page, parametros['veiculo_segurado']):
                telas_executadas += 1
                resultado_telas["tela_4"] = True
                exibir_mensagem("✅ TELA 4 CONCLUÍDA!")
            else:
                resultado_telas["tela_4"] = False
                exibir_mensagem("❌ TELA 4 FALHOU!")
                return criar_retorno_erro(
                    "Tela 4 falhou",
                    "TELA_4",
                    time.time() - inicio_execucao,
                    parametros,
                    exception_handler
                )
            
            # TELA 5 - Carrossel de Estimativas
            exibir_mensagem("\n" + "="*50)
            sucesso_tela_5 = navegar_tela_5_playwright(page)
            
            if sucesso_tela_5:
                telas_executadas += 1
                resultado_telas["tela_5"] = True
                exibir_mensagem("✅ TELA 5 CONCLUÍDA!")
                
                # Capturar dados da Tela 5
                dados_tela_5 = capturar_dados_carrossel_estimativas_playwright(page)
                
                # Salvar dados em arquivo JSON
                arquivo_salvo = salvar_dados_json(dados_tela_5)
                
                # SAÍDA INTERMEDIÁRIA DOS DADOS DA TELA 5
                exibir_mensagem("\n" + "🎯 **SAÍDA INTERMEDIÁRIA - DADOS DA TELA 5**")
                exibir_mensagem("=" * 80)
                exibir_mensagem(f"📊 Total de coberturas: {len(dados_tela_5.get('coberturas_detalhadas', []))}")
                exibir_mensagem(f"💰 Valores encontrados: {dados_tela_5.get('valores_encontrados', 0)}")
                
                # Exibir detalhes das coberturas capturadas
                for i, cobertura in enumerate(dados_tela_5.get('coberturas_detalhadas', [])):
                    exibir_mensagem(f"📋 Cobertura {i+1}: {cobertura.get('nome_cobertura', 'N/A')}")
                    if cobertura.get('valores', {}).get('de'):
                        exibir_mensagem(f"   💰 Valores: {cobertura['valores']['de']} até {cobertura['valores']['ate']}")
                    if cobertura.get('beneficios'):
                        beneficios = [b['nome'] for b in cobertura['beneficios']]
                        exibir_mensagem(f"   🎁 Benefícios: {', '.join(beneficios)}")
                
                exibir_mensagem("=" * 80)
                exibir_mensagem("✅ **SAÍDA INTERMEDIÁRIA CONCLUÍDA**")
                
            else:
                resultado_telas["tela_5"] = False
                exibir_mensagem("❌ TELA 5 FALHOU!")
                return criar_retorno_erro(
                    "Tela 5 falhou",
                    "TELA_5",
                    time.time() - inicio_execucao,
                    parametros,
                    exception_handler
                )
            
            # Fechar browser
            browser.close()
            exibir_mensagem("✅ Browser fechado")
            
            # Calcular tempo de execução
            tempo_execucao = time.time() - inicio_execucao
            
            # Retorno estruturado com dados da Tela 5 como saída intermediária
            return criar_retorno_sucesso(
                resultado_telas,
                {"dados_tela_5": dados_tela_5} if dados_tela_5 else {},
                arquivo_salvo if 'arquivo_salvo' in locals() else "",
                tempo_execucao,
                parametros
            )
            
    except Exception as e:
        exibir_mensagem(f"❌ ERRO GERAL: {e}")
        exception_handler.add_error(str(e), "GERAL")
        return criar_retorno_erro(
            str(e),
            "GERAL",
            time.time() - inicio_execucao,
            parametros,
            exception_handler
        )


if __name__ == "__main__":
    resultado = executar_rpa_telas_1_a_5_modular()
    
    # Exibir resultado final
    exibir_mensagem("\n" + "=" * 80)
    exibir_mensagem("🏁 RESULTADO FINAL DA EXECUÇÃO")
    exibir_mensagem("=" * 80)
    exibir_mensagem(f"✅ Sucesso: {resultado['sucesso']}")
    exibir_mensagem(f"📊 Telas executadas: {sum(resultado['resultado_telas'].values())}/5")
    exibir_mensagem(f"⏱️ Tempo total: {resultado['tempo_execucao']:.2f}s")
    
    if resultado['sucesso'] and resultado['dados_extras'].get('dados_tela_5'):
        dados_tela_5 = resultado['dados_extras']['dados_tela_5']
        exibir_mensagem(f"📈 Coberturas capturadas: {dados_tela_5['valores_encontrados']}")
        exibir_mensagem(f"💾 Arquivo salvo: {resultado['retorno_path']}")
    
    exibir_mensagem("=" * 80)

















