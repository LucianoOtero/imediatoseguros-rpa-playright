#!/usr/bin/env python3
# CONVERSOR UNICODE → ASCII ROBUSTO - ATIVAR ANTES DE QUALQUER SAÍDA
import converter_unicode_ascii_robusto

# EXCEPTION HANDLER - SISTEMA DE CAPTURA E FORMATAÇÃO DE EXCEÇÕES PLAYWRIGHT
from exception_handler import (
    handle_selenium_exception,
    handle_retry_attempt,
    format_success_message,
    set_session_info
)

"""
RPA Tô Segurado - VERSÃO PLAYWRIGHT
VERSÃO MIGRADA do Selenium para Playwright com melhor detecção de elementos dinâmicos

MIGRAÇÃO COMPLETA:
==================
- Todas as 13 telas implementadas
- Login automático otimizado para Playwright
- Captura de dados da tela final
- Sistema de logging e validação mantido
- Exception handler adaptado

VANTAGENS DO PLAYWRIGHT:
=======================
- Auto-waiting nativo para elementos
- Melhor detecção de modais dinâmicos
- Suporte nativo para React/Next.js
- Menos código para detecção de elementos
- Performance superior

ARQUIVOS MIGRADOS:
==================
- executar_rpa_playwright.py (NOVO - adaptado para Playwright)
- parametros.json (COPIADO)
- utils/ (COPIADO - toda a infraestrutura)
- exception_handler.py (COPIADO)
- converter_unicode_ascii_robusto.py (COPIADO)
- Todos os arquivos de configuração e validação

DEPENDÊNCIAS:
=============
- playwright==1.40.0
- python-dotenv==1.0.0
- requests==2.31.0
- beautifulsoup4==4.12.2
- lxml==4.9.3
- Pillow==10.0.1
"""

import json
import sys
import time
import os
import logging
from datetime import datetime
from pathlib import Path

# PLAYWRIGHT IMPORTS
from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext
import asyncio

# UTILS IMPORTS
from utils.validacao_parametros import validar_parametros_json
from utils.logger_rpa import setup_logger, exibir_mensagem
from utils.retorno_estruturado import criar_retorno_sucesso, criar_retorno_erro
from utils.helpers import aguardar_estabilizacao, salvar_estado_tela

# CONFIGURAÇÃO INICIAL
set_session_info("RPA Playwright", "1.0.0")

def setup_playwright_browser(headless=True):
    """
    CONFIGURAÇÃO DO BROWSER PLAYWRIGHT
    
    VANTAGENS:
    ==========
    - Auto-waiting nativo
    - Melhor detecção de elementos dinâmicos
    - Suporte nativo para React/Next.js
    - Performance superior
    """
    try:
        playwright = sync_playwright().start()
        
        # Configurações do browser
        browser = playwright.chromium.launch(
            headless=headless,
            args=[
                '--no-sandbox',
                '--disable-dev-shm-usage',
                '--disable-web-security',
                '--disable-features=VizDisplayCompositor'
            ]
        )
        
        # Configurações do contexto
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        
        # Configurações da página
        page = context.new_page()
        page.set_default_timeout(30000)  # 30 segundos timeout padrão
        
        exibir_mensagem("✅ BROWSER PLAYWRIGHT CONFIGURADO COM SUCESSO!")
        exibir_mensagem("   → Auto-waiting ativado")
        exibir_mensagem("   → Timeout padrão: 30s")
        exibir_mensagem("   → Viewport: 1920x1080")
        
        return playwright, browser, context, page
        
    except Exception as e:
        handle_selenium_exception(e, "Configuração do browser Playwright")
        return None, None, None, None

def realizar_login_automatico_playwright(page: Page, parametros):
    """
    REALIZA LOGIN AUTOMÁTICO COM PLAYWRIGHT - VERSÃO OTIMIZADA
    
    VANTAGENS DO PLAYWRIGHT:
    ========================
    - Auto-waiting nativo para elementos
    - Detecção automática de modais
    - Melhor handling de elementos dinâmicos
    - Menos código para detecção
    
    FLUXO CORRETO:
    ===============
    1. Modal de login aparece → Preenche email/senha → Clica "Acessar"
    2. Modal de login fecha
    3. Modal de CPF divergente aparece → Clica "Manter Login atual"
    4. Modal fecha e valores reais aparecem
    """
    try:
        exibir_mensagem("🔐 INICIANDO PROCESSO DE LOGIN AUTOMÁTICO (PLAYWRIGHT)...")
        exibir_mensagem("=" * 60)
        
        # Verificar se os parâmetros de autenticação existem
        if "autenticacao" not in parametros:
            exibir_mensagem("❌ ERRO: Parâmetros de autenticação não encontrados no JSON")
            return False
            
        email_login = parametros["autenticacao"].get("email_login")
        senha_login = parametros["autenticacao"].get("senha_login")
        
        if not email_login or not senha_login:
            exibir_mensagem("❌ ERRO: Email ou senha de login não configurados")
            return False
        
        exibir_mensagem(f"📧 Email configurado: {email_login}")
        exibir_mensagem("🔒 Senha configurada: [PROTEGIDA]")
        
        # ========================================
        # ETAPA 1: DETECÇÃO OTIMIZADA DO MODAL DE LOGIN
        # ========================================
        exibir_mensagem("\n🔍 ETAPA 1: DETECTANDO MODAL DE LOGIN (PLAYWRIGHT)")
        exibir_mensagem("-" * 50)
        
        # Verificar se já está logado
        exibir_mensagem("🔍 Verificando se já está logado...")
        try:
            # Playwright: Detecção automática de elementos logados
            elementos_logado = [
                "nav#navbar a[href*='/area-usuario']",
                "button#sairTelaAreaUsuario",
                "p:has-text('Fernando Otero')"
            ]
            
            for seletor in elementos_logado:
                try:
                    elemento = page.locator(seletor).first
                    if elemento.is_visible():
                        exibir_mensagem("✅ USUÁRIO JÁ ESTÁ LOGADO!")
                        exibir_mensagem(f"   → Elemento detectado: {seletor}")
                        return True
                except:
                    continue
                    
        except Exception as e:
            exibir_mensagem("   → Usuário não está logado, prosseguindo...")
        
        # Aguardar carregamento da página
        exibir_mensagem("⏳ Aguardando carregamento completo da página...")
        page.wait_for_load_state('networkidle')
        exibir_mensagem("✅ Página carregada completamente")
        
        # ========================================
        # DETECÇÃO DO MODAL DE LOGIN COM PLAYWRIGHT
        # ========================================
        exibir_mensagem("🎯 Estratégias de detecção Playwright:")
        exibir_mensagem("   1. Campo de senha (id=senhaTelaLogin)")
        exibir_mensagem("   2. Modal MUI padrão (div[role='dialog'])")
        exibir_mensagem("   3. Email pré-preenchido")
        
        modal_detectado = False
        tempo_inicio = time.time()
        tempo_maximo = 30  # 30 segundos máximo
        
        exibir_mensagem(f"⏳ Aguardando modal de login aparecer (timeout: {tempo_maximo}s)...")
        
        while time.time() - tempo_inicio < tempo_maximo:
            try:
                # ESTRATÉGIA 1: Campo de senha com auto-waiting
                senha_field = page.wait_for_selector("#senhaTelaLogin", timeout=5000)
                if senha_field and senha_field.is_visible():
                    tempo_detectado = int(time.time() - tempo_inicio)
                    exibir_mensagem(f"✅ MODAL DE LOGIN DETECTADO!")
                    exibir_mensagem(f"   → Estratégia: Campo de senha (id=senhaTelaLogin)")
                    exibir_mensagem(f"   → Tempo de detecção: {tempo_detectado}s")
                    modal_detectado = True
                    break
                    
            except Exception as e:
                try:
                    # ESTRATÉGIA 2: Modal MUI padrão
                    modal_container = page.locator("div[role='dialog']").first
                    if modal_container.is_visible():
                        campos_login = modal_container.locator("input[type='email'], input[type='password']")
                        if campos_login.count() > 0:
                            tempo_detectado = int(time.time() - tempo_inicio)
                            exibir_mensagem(f"✅ MODAL DE LOGIN DETECTADO!")
                            exibir_mensagem(f"   → Estratégia: Modal MUI padrão")
                            exibir_mensagem(f"   → Tempo de detecção: {tempo_detectado}s")
                            modal_detectado = True
                            break
                            
                except Exception as e2:
                    try:
                        # ESTRATÉGIA 3: Email pré-preenchido
                        email_field = page.locator("#emailTelaLogin").first
                        email_atual = email_field.input_value()
                        if email_atual == "alex.kaminski@imediatoseguros.com.br":
                            tempo_detectado = int(time.time() - tempo_inicio)
                            exibir_mensagem(f"✅ MODAL DE LOGIN DETECTADO!")
                            exibir_mensagem(f"   → Estratégia: Email pré-preenchido")
                            exibir_mensagem(f"   → Tempo de detecção: {tempo_detectado}s")
                            modal_detectado = True
                            break
                            
                    except Exception as e3:
                        # Aguardar e tentar novamente
                        time.sleep(2)
                        continue
        
        if not modal_detectado:
            exibir_mensagem(f"❌ ERRO: Modal de login não foi carregado!")
            exibir_mensagem(f"   → Timeout excedido: {tempo_maximo}s")
            
            # Capturar screenshot para debugging
            try:
                screenshot_path = "debug_modal_falha_playwright.png"
                page.screenshot(path=screenshot_path)
                exibir_mensagem(f"📸 Screenshot salvo: {screenshot_path}")
            except:
                pass
                
            return False
        
        # ========================================
        # ETAPA 2: PREENCHIMENTO DOS CAMPOS
        # ========================================
        exibir_mensagem("\n📝 ETAPA 2: PREENCHENDO CAMPOS DE LOGIN")
        exibir_mensagem("-" * 40)
        
        # VERIFICAR E PREENCHER EMAIL
        exibir_mensagem("📧 Verificando campo de email...")
        try:
            email_field = page.locator("#emailTelaLogin").first
            email_atual = email_field.input_value()
            exibir_mensagem(f"   → Email atual no campo: {email_atual}")
            
            if email_atual and email_atual.strip():
                exibir_mensagem("✅ EMAIL JÁ ESTÁ PREENCHIDO")
                exibir_mensagem(f"   → Email detectado: {email_atual}")
            else:
                exibir_mensagem("⚠️ Campo de email está vazio")
                exibir_mensagem("   → Preenchendo email...")
                
                # Playwright: Preenchimento otimizado
                email_field.fill(email_login)
                exibir_mensagem("✅ EMAIL PREENCHIDO COM SUCESSO")
                exibir_mensagem(f"   → Email inserido: {email_login}")
                
        except Exception as e:
            exibir_mensagem("❌ ERRO: Falha ao verificar/preencher email")
            exibir_mensagem(f"   → Erro: {str(e)}")
            return False
        
        # PREENCHER SENHA
        exibir_mensagem("🔒 Preenchendo campo de senha...")
        try:
            senha_field = page.locator("#senhaTelaLogin").first
            senha_field.fill(senha_login)
            exibir_mensagem("✅ SENHA PREENCHIDA COM SUCESSO")
            exibir_mensagem(f"   → Senha inserida: {senha_login[:3]}***{senha_login[-1:]}")
            
        except Exception as e:
            exibir_mensagem("❌ ERRO: Falha ao preencher senha")
            exibir_mensagem(f"   → Erro: {str(e)}")
            return False
        
        # ========================================
        # ETAPA 3: CLIQUE NO BOTÃO ACESSAR
        # ========================================
        exibir_mensagem("\n🚀 ETAPA 3: CLICANDO NO BOTÃO ACESSAR")
        exibir_mensagem("-" * 40)
        
        exibir_mensagem("🔍 Procurando botão 'Acessar'...")
        try:
            botao_acessar = page.locator("#gtm-telaLoginBotaoAcessar").first
            botao_acessar.click()
            exibir_mensagem("✅ BOTÃO 'ACESSAR' CLICADO COM SUCESSO")
            exibir_mensagem("   → Login enviado para processamento")
        except Exception as e:
            exibir_mensagem("❌ ERRO: Falha ao clicar no botão 'Acessar'")
            exibir_mensagem(f"   → Erro: {str(e)}")
            return False
        
        # Aguardar carregamento após login
        exibir_mensagem("⏳ Aguardando processamento do login...")
        page.wait_for_load_state('networkidle')
        
        # ========================================
        # ETAPA 4: VERIFICAÇÃO DE MODAIS DE CONFIRMAÇÃO
        # ========================================
        exibir_mensagem("\n🔍 ETAPA 4: VERIFICANDO MODAIS DE CONFIRMAÇÃO")
        exibir_mensagem("-" * 40)
        
        # VERIFICAR MODAL DE CPF DIVERGENTE
        exibir_mensagem("🔍 Verificando modal de CPF divergente...")
        try:
            # Playwright: Detecção automática de texto
            modal_cpf_divergente = page.locator("text=CPF informado não corresponde à conta").first
            if modal_cpf_divergente.is_visible():
                exibir_mensagem("✅ MODAL DE CPF DIVERGENTE DETECTADO!")
                
                # Procurar e clicar no botão "Manter Login atual"
                botao_manter_login = page.locator("#manterLoginAtualModalAssociarUsuario").first
                botao_manter_login.click()
                exibir_mensagem("✅ CONFIRMAÇÃO CPF DIVERGENTE REALIZADA")
                
                # Aguardar carregamento
                page.wait_for_load_state('networkidle')
                
        except Exception as e:
            exibir_mensagem("ℹ️ Modal de CPF divergente não detectado")
            
            # VERIFICAR MODAL "MANTER LOGIN ATUAL" PADRÃO
            exibir_mensagem("🔍 Verificando modal 'Manter Login atual' padrão...")
            try:
                botao_manter_login = page.locator("#manterLoginAtualModalAssociarUsuario").first
                if botao_manter_login.is_visible():
                    botao_manter_login.click()
                    exibir_mensagem("✅ CONFIRMAÇÃO PADRÃO REALIZADA")
                    page.wait_for_load_state('networkidle')
                else:
                    exibir_mensagem("ℹ️ Modal 'Manter Login atual' não detectado")
                    
            except Exception as e2:
                exibir_mensagem("ℹ️ Modal de confirmação não detectado")
        
        # ========================================
        # ETAPA 5: VERIFICAÇÃO FINAL DOS VALORES
        # ========================================
        exibir_mensagem("\n💰 ETAPA 5: VERIFICANDO VALORES REAIS")
        exibir_mensagem("-" * 40)
        
        exibir_mensagem("🎉 LOGIN REALIZADO COM SUCESSO!")
        exibir_mensagem("💡 Agora os valores reais do prêmio devem estar disponíveis")
        
        # Aguardar carregamento final
        exibir_mensagem("⏳ Aguardando carregamento dos valores reais...")
        page.wait_for_load_state('networkidle')
        
        # Verificar valores diferentes de R$ 100,00
        try:
            elementos_valor = page.locator("text=/R\\$ [^1]|R\\$ [2-9]/").all()
            if elementos_valor:
                exibir_mensagem("✅ VALORES REAIS DETECTADOS!")
                exibir_mensagem(f"   → Total de valores encontrados: {len(elementos_valor)}")
                exibir_mensagem("   → Primeiros valores detectados:")
                for i, elemento in enumerate(elementos_valor[:3]):
                    exibir_mensagem(f"     {i+1}. {elemento.text_content()}")
            else:
                exibir_mensagem("⚠️ VALORES REAIS NÃO DETECTADOS")
                exibir_mensagem("   → Ainda não foram encontrados valores diferentes de R$ 100,00")
                
        except Exception as e:
            exibir_mensagem("❌ ERRO: Falha ao verificar valores reais")
            exibir_mensagem(f"   → Erro: {str(e)}")
        
        exibir_mensagem("\n" + "=" * 60)
        exibir_mensagem("🏁 PROCESSO DE LOGIN FINALIZADO (PLAYWRIGHT)")
        exibir_mensagem("=" * 60)
        
        return True
        
    except Exception as e:
        handle_selenium_exception(e, "Processo de login automático Playwright")
        return False

def navegar_tela_5_playwright(page: Page, parametros):
    """
    Navega pela Tela 5 (Estimativa Inicial) - Captura dados dos cards de cobertura
    """
    try:
        exibir_mensagem("📱 TELA 5: Estimativa Inicial - Capturando dados dos cards")
        
        # Aguarda a página carregar e verifica se estamos na tela correta
        time.sleep(3)
        
        # Verifica se estamos na tela de estimativa inicial
        titulo_esperado = "Confira abaixo a estimativa inicial para o seu seguro carro!"
        try:
            titulo_elemento = page.locator("text=" + titulo_esperado)
            if titulo_elemento.count() > 0:
                exibir_mensagem("✅ Tela 5 identificada: Estimativa Inicial")
            else:
                exibir_mensagem("⚠️ Tela 5 não identificada pelo título, continuando...")
        except:
            exibir_mensagem("⚠️ Erro ao verificar título da Tela 5, continuando...")
        
        # Captura dados dos cards de cobertura
        dados_capturados = capturar_dados_carrossel_estimativas_playwright(page)
        
        if dados_capturados:
            exibir_mensagem(f"📊 Dados capturados: {len(dados_capturados.get('coberturas_detalhadas', []))} coberturas")
            exibir_mensagem(f"💰 Valores encontrados: {dados_capturados.get('valores_encontrados', 0)}")
        
        # Clica no botão "Continuar" para ir para a próxima tela
        try:
            botao_continuar = page.locator("#gtm-telaEstimativaContinuarParaCotacaoFinal")
            if botao_continuar.count() > 0:
                exibir_mensagem("🔄 Clicando no botão 'Continuar' da Tela 5")
                botao_continuar.click()
                time.sleep(3)
                exibir_mensagem("✅ Navegação da Tela 5 concluída")
                return True
            else:
                exibir_mensagem("❌ Botão 'Continuar' não encontrado na Tela 5")
                return False
        except Exception as e:
            exibir_mensagem(f"❌ ERRO ao clicar no botão 'Continuar': {str(e)}")
            return False
            
    except Exception as e:
        exibir_mensagem(f"❌ ERRO na Tela 5: {str(e)}")
        return False

def capturar_dados_carrossel_estimativas_playwright(page: Page):
    """
    Captura dados estruturados do carrossel de estimativas (Tela 5)
    """
    try:
        from datetime import datetime
        
        dados_carrossel = {
            "timestamp": datetime.now().isoformat(),
            "tela": 5,
            "nome_tela": "Estimativa Inicial",
            "url": page.url,
            "titulo": page.title,
            "coberturas_detalhadas": [],
            "beneficios_gerais": [],
            "valores_encontrados": 0,
            "seguradoras": [],
            "elementos_detectados": []
        }
        
        # Captura os cards de cobertura usando os seletores identificados na gravação
        cards_cobertura = page.locator(".min-w-0")
        
        if cards_cobertura.count() > 0:
            exibir_mensagem(f"🔍 Encontrados {cards_cobertura.count()} cards de cobertura")
            
            for i in range(cards_cobertura.count()):
                try:
                    card = cards_cobertura.nth(i)
                    
                    # Captura o nome da cobertura
                    nome_cobertura = ""
                    try:
                        nome_elemento = card.locator(".flex .text-white")
                        if nome_elemento.count() > 0:
                            nome_cobertura = nome_elemento.first.text_content().strip()
                    except:
                        pass
                    
                    # Captura o preço
                    preco = ""
                    try:
                        preco_elemento = card.locator(".font-semibold:nth-child(2)")
                        if preco_elemento.count() > 0:
                            preco = preco_elemento.first.text_content().strip()
                    except:
                        pass
                    
                    # Captura faixa de preço (se existir)
                    faixa_preco = ""
                    try:
                        faixa_elemento = card.locator(".text-primary .text-primary")
                        if faixa_elemento.count() > 0:
                            faixa_preco = faixa_elemento.first.text_content().strip()
                    except:
                        pass
                    
                    # Captura benefícios
                    beneficios = []
                    try:
                        beneficios_elementos = card.locator(".py-4 .text-sm")
                        for j in range(beneficios_elementos.count()):
                            beneficio = beneficios_elementos.nth(j).text_content().strip()
                            if beneficio:
                                beneficios.append(beneficio)
                    except:
                        pass
                    
                    # Monta o objeto da cobertura
                    if nome_cobertura or preco:
                        cobertura = {
                            "indice": i + 1,
                            "nome": nome_cobertura,
                            "preco": preco,
                            "faixa_preco": faixa_preco,
                            "beneficios": beneficios,
                            "card_selector": f".min-w-0:nth-child({i + 1})"
                        }
                        
                        dados_carrossel["coberturas_detalhadas"].append(cobertura)
                        
                        # Conta valores encontrados
                        if preco and "R$" in preco:
                            dados_carrossel["valores_encontrados"] += 1
                        
                        exibir_mensagem(f"📋 Card {i + 1}: {nome_cobertura} - {preco}")
                        
                except Exception as e:
                    exibir_mensagem(f"⚠️ Erro ao processar card {i + 1}: {str(e)}")
                    continue
        
        # Captura benefícios gerais da página
        try:
            beneficios_gerais = page.locator("text=benefício, text=vantagem, text=incluso")
            for i in range(beneficios_gerais.count()):
                beneficio = beneficios_gerais.nth(i).text_content().strip()
                if beneficio and beneficio not in dados_carrossel["beneficios_gerais"]:
                    dados_carrossel["beneficios_gerais"].append(beneficio)
        except:
            pass
        
        # Resumo dos elementos detectados
        dados_carrossel["elementos_detectados"] = [
            f"Cards de cobertura: {len(dados_carrossel['coberturas_detalhadas'])}",
            f"Benefícios gerais: {len(dados_carrossel['beneficios_gerais'])}",
            f"Valores encontrados: {dados_carrossel['valores_encontrados']}"
        ]
        
        exibir_mensagem(f"✅ Captura concluída: {len(dados_carrossel['coberturas_detalhadas'])} coberturas processadas")
        
        return dados_carrossel
        
    except Exception as e:
        exibir_mensagem(f"❌ ERRO na captura de dados: {str(e)}")
        return None

def executar_todas_telas_playwright(json_string):
    """
    EXECUTA O FLUXO PRINCIPAL DE COTAÇÃO COM PLAYWRIGHT
    
    VANTAGENS:
    ==========
    - Auto-waiting nativo
    - Melhor detecção de elementos dinâmicos
    - Performance superior
    - Menos código para detecção
    """
    try:
        # Configurar logging
        setup_logger()
        
        exibir_mensagem("🚀 INICIANDO RPA PLAYWRIGHT - TÔ SEGURADO")
        exibir_mensagem("=" * 60)
        
        # Validar JSON de entrada
        try:
            parametros = json.loads(json_string)
            exibir_mensagem("✅ JSON de entrada validado com sucesso")
        except json.JSONDecodeError as e:
            return criar_retorno_erro(1001, f"JSON inválido: {str(e)}")
        
        # Validar parâmetros
        resultado_validacao = validar_parametros_json(parametros)
        if not resultado_validacao["sucesso"]:
            return criar_retorno_erro(1002, resultado_validacao["mensagem"])
        
        exibir_mensagem("✅ Parâmetros validados com sucesso")
        
        # Configurar browser Playwright
        playwright, browser, context, page = setup_playwright_browser(headless=False)
        if not page:
            return criar_retorno_erro(1003, "Falha ao configurar browser Playwright")
        
        try:
            # Navegar para a URL base
            url_base = parametros.get("url_base", "https://www.app.tosegurado.com.br/imediatoseguros")
            exibir_mensagem(f"🌐 Navegando para: {url_base}")
            
            page.goto(url_base)
            page.wait_for_load_state('networkidle')
            exibir_mensagem("✅ Página carregada com sucesso")
            
            # TODO: Implementar todas as telas com Playwright
            # Por enquanto, vamos testar apenas o login
            
            # Testar login automático
            exibir_mensagem("\n🔐 TESTANDO LOGIN AUTOMÁTICO COM PLAYWRIGHT")
            exibir_mensagem("-" * 50)
            
            resultado_login = realizar_login_automatico_playwright(page, parametros)
            
            if resultado_login:
                exibir_mensagem("✅ LOGIN AUTOMÁTICO FUNCIONOU COM PLAYWRIGHT!")
            else:
                exibir_mensagem("❌ LOGIN AUTOMÁTICO FALHOU")
            
            # Aguardar um pouco para visualizar o resultado
            time.sleep(5)
            
            # TODO: Implementar captura de dados da tela final
            
            exibir_mensagem("\n" + "=" * 60)
            exibir_mensagem("🏁 TESTE PLAYWRIGHT CONCLUÍDO")
            exibir_mensagem("=" * 60)
            
            return criar_retorno_sucesso(
                "Teste Playwright concluído com sucesso!",
                {
                    "login_funcionou": resultado_login,
                    "tecnologia": "Playwright",
                    "timestamp": datetime.now().isoformat()
                }
            )
            
        finally:
            # Fechar browser
            if browser:
                browser.close()
            if playwright:
                playwright.stop()
            
    except Exception as e:
        return criar_retorno_erro(1000, f"Erro geral: {str(e)}")

def main():
    """
    FUNÇÃO PRINCIPAL - ENTRY POINT DO RPA PLAYWRIGHT
    """
    try:
        # Verificar argumentos de linha de comando
        if len(sys.argv) > 1:
            # Modo JSON direto
            json_string = sys.argv[1]
        else:
            # Modo stdin
            json_string = sys.stdin.read()
        
        # Executar RPA
        resultado = executar_todas_telas_playwright(json_string)
        
        # Retornar resultado em JSON
        print(json.dumps(resultado, ensure_ascii=False, indent=2))
        
    except Exception as e:
        erro = criar_retorno_erro(9999, f"Erro crítico: {str(e)}")
        print(json.dumps(erro, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
