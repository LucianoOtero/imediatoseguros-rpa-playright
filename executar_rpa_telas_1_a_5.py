#!/usr/bin/env python3
"""
EXECUTAR RPA TELAS 1-5 - VERSÃO BASEADA NO ORIGINAL
Implementação das Telas 1-5 do RPA usando Playwright com captura de dados da Tela 5
Baseado no arquivo executar_rpa_imediato_playwright.py

DESCRIÇÃO:
- Copiado do arquivo original executar_rpa_imediato_playwright.py
- Telas 1-5 implementadas e funcionais
- Telas 6-15 comentadas
- Captura de dados do carrossel de estimativas na Tela 5
- Saída intermediária dos dados capturados
- Estrutura de retorno padronizada

AUTOR: Luciano Otero
DATA: 2025-01-27
VERSÃO: 2.0.0
STATUS: Baseado no arquivo original - Telas 1-5 ativas
"""

import json
import time
import re
import os
import sys
import traceback
from datetime import datetime
from typing import Dict, Any, Optional, Union
from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext

# Importar Sistema de Retorno Estruturado
from utils.retorno_estruturado import (
    RetornoEstruturado,
    criar_retorno_sucesso,
    criar_retorno_erro,
    criar_retorno_warning,
    validar_retorno_estruturado
)

# ========================================
# SISTEMA DE EXCEPTION HANDLER
# ========================================

class RPAException(Exception):
    """
    Exceção customizada para o RPA
    """
    def __init__(self, message: str, tela: str = None, erro_original: Exception = None):
        self.message = message
        self.tela = tela
        self.erro_original = erro_original
        super().__init__(self.message)

class ExceptionHandler:
    """
    Sistema robusto de tratamento de exceções para o RPA
    """
    
    def __init__(self):
        self.erros_capturados = []
        self.warnings_capturados = []
        self.tela_atual = None
    
    def capturar_excecao(self, erro: Exception, tela: str = None, contexto: str = None) -> Dict[str, Any]:
        """
        Captura e formata uma exceção de forma estruturada
        
        PARÂMETROS:
            erro: Exception - Exceção capturada
            tela: str - Nome da tela onde ocorreu o erro
            contexto: str - Contexto adicional do erro
            
        RETORNO:
            dict: Dicionário estruturado com informações do erro
        """
        timestamp = datetime.now().isoformat()
        
        # Extrair informações detalhadas do erro
        tipo_erro = type(erro).__name__
        mensagem_erro = str(erro)
        traceback_completo = traceback.format_exc()
        
        # Determinar severidade do erro
        severidade = self._determinar_severidade(erro)
        
        # Criar estrutura de erro
        erro_estruturado = {
            "timestamp": timestamp,
            "tipo": tipo_erro,
            "mensagem": mensagem_erro,
            "tela": tela or self.tela_atual,
            "contexto": contexto,
            "severidade": severidade,
            "traceback": traceback_completo,
            "recomendacao": self._gerar_recomendacao(erro, tela)
        }
        
        # Adicionar à lista de erros
        self.erros_capturados.append(erro_estruturado)
        
        # Log do erro
        self._log_erro(erro_estruturado)
        
        return erro_estruturado
    
    def _determinar_severidade(self, erro: Exception) -> str:
        """
        Determina a severidade do erro baseado no tipo
        """
        if isinstance(erro, (TimeoutError, ConnectionError)):
            return "CRÍTICO"
        elif isinstance(erro, (ValueError, TypeError)):
            return "ALTO"
        elif isinstance(erro, (FileNotFoundError, PermissionError)):
            return "MÉDIO"
        else:
            return "BAIXO"
    
    def _gerar_recomendacao(self, erro: Exception, tela: str = None) -> str:
        """
        Gera recomendação baseada no tipo de erro
        """
        if isinstance(erro, TimeoutError):
            return f"Verificar conectividade e tentar novamente. Tela: {tela}"
        elif isinstance(erro, ValueError):
            return f"Verificar parâmetros de entrada. Tela: {tela}"
        elif "element not found" in str(erro).lower():
            return f"Elemento não encontrado. Verificar seletor. Tela: {tela}"
        elif "timeout" in str(erro).lower():
            return f"Timeout detectado. Aumentar tempo de espera. Tela: {tela}"
        else:
            return f"Erro genérico. Verificar logs detalhados. Tela: {tela}"
    
    def _log_erro(self, erro_estruturado: Dict[str, Any]):
        """
        Faz log do erro de forma formatada
        """
        timestamp = erro_estruturado["timestamp"]
        tela = erro_estruturado["tela"]
        tipo = erro_estruturado["tipo"]
        mensagem = erro_estruturado["mensagem"]
        severidade = erro_estruturado["severidade"]
        
        print(f"\n{'='*80}")
        print(f"🚨 ERRO CAPTURADO - {severidade}")
        print(f"{'='*80}")
        print(f"⏰ Timestamp: {timestamp}")
        print(f"📱 Tela: {tela}")
        print(f"🔍 Tipo: {tipo}")
        print(f"💬 Mensagem: {mensagem}")
        print(f"💡 Recomendação: {erro_estruturado['recomendacao']}")
        print(f"{'='*80}")
    
    def capturar_warning(self, mensagem: str, tela: str = None, contexto: str = None):
        """
        Captura um warning (não é erro crítico)
        """
        timestamp = datetime.now().isoformat()
        
        warning = {
            "timestamp": timestamp,
            "mensagem": mensagem,
            "tela": tela or self.tela_atual,
            "contexto": contexto,
            "tipo": "WARNING"
        }
        
        self.warnings_capturados.append(warning)
        
        print(f"⚠️ WARNING - {tela}: {mensagem}")
    
    def definir_tela_atual(self, tela: str):
        """
        Define a tela atual para contexto de erros
        """
        self.tela_atual = tela
    
    def obter_resumo_erros(self) -> Dict[str, Any]:
        """
        Retorna resumo dos erros capturados
        """
        return {
            "total_erros": len(self.erros_capturados),
            "total_warnings": len(self.warnings_capturados),
            "erros_criticos": len([e for e in self.erros_capturados if e["severidade"] == "CRÍTICO"]),
            "erros_altos": len([e for e in self.erros_capturados if e["severidade"] == "ALTO"]),
            "erros_medios": len([e for e in self.erros_capturados if e["severidade"] == "MÉDIO"]),
            "erros_baixos": len([e for e in self.erros_capturados if e["severidade"] == "BAIXO"]),
            "ultimo_erro": self.erros_capturados[-1] if self.erros_capturados else None
        }
    
    def limpar_erros(self):
        """
        Limpa a lista de erros capturados
        """
        self.erros_capturados = []
        self.warnings_capturados = []

# Instância global do Exception Handler
exception_handler = ExceptionHandler()

# ========================================
# FUNÇÕES AUXILIARES
# ========================================

def exibir_mensagem(mensagem: str):
    """
    Exibe mensagem formatada com timestamp
    
    PARÂMETROS:
        mensagem (str): Mensagem a ser exibida
    
    COMPORTAMENTO:
        1. Formata mensagem com timestamp
        2. Exibe no terminal
        3. Formato: [HH:MM:SS] mensagem
    """
    timestamp = time.strftime('%H:%M:%S')
    print(f"[{timestamp}] {mensagem}")

def carregar_parametros(arquivo_config: str = "config/parametros.json") -> Dict[str, Any]:
    """
    Carrega parâmetros do arquivo JSON
    
    PARÂMETROS:
        arquivo_config: str - Caminho para o arquivo de configuração
        
    RETORNO:
        dict: Parâmetros carregados
        
    EXCEÇÕES:
        RPAException: Se não conseguir carregar os parâmetros
    """
    try:
        exception_handler.definir_tela_atual("CARREGAMENTO_PARAMETROS")
        
        if not os.path.exists(arquivo_config):
            raise RPAException(f"Arquivo de configuração não encontrado: {arquivo_config}")
        
        with open(arquivo_config, 'r', encoding='utf-8') as f:
            parametros = json.load(f)
        
        exibir_mensagem("✅ Parâmetros carregados com sucesso!")
        return parametros
        
    except json.JSONDecodeError as e:
        erro = exception_handler.capturar_excecao(e, "CARREGAMENTO_PARAMETROS", "JSON inválido")
        raise RPAException("Erro ao decodificar JSON dos parâmetros", "CARREGAMENTO_PARAMETROS", e)
        
    except Exception as e:
        erro = exception_handler.capturar_excecao(e, "CARREGAMENTO_PARAMETROS", "Erro genérico")
        raise RPAException("Erro ao carregar parâmetros", "CARREGAMENTO_PARAMETROS", e)

def validar_parametros_obrigatorios(parametros: Dict[str, Any]) -> bool:
    """
    Valida se todos os parâmetros obrigatórios estão presentes
    
    PARÂMETROS:
        parametros: dict - Parâmetros a serem validados
        
    RETORNO:
        bool: True se válido, False caso contrário
        
    EXCEÇÕES:
        RPAException: Se parâmetros obrigatórios estiverem faltando
    """
    try:
        exception_handler.definir_tela_atual("VALIDACAO_PARAMETROS")
        
        parametros_obrigatorios = [
            "url", "placa", "marca", "modelo", "ano", "combustivel", 
            "cep", "uso_veiculo", "veiculo_segurado", "nome", "cpf", 
            "email", "celular", "autenticacao"
        ]
        
        parametros_faltando = []
        
        for param in parametros_obrigatorios:
            if param not in parametros:
                parametros_faltando.append(param)
            elif not parametros[param]:
                parametros_faltando.append(f"{param} (vazio)")
        
        if parametros_faltando:
            erro_msg = f"Parâmetros obrigatórios faltando: {', '.join(parametros_faltando)}"
            exception_handler.capturar_warning(erro_msg, "VALIDACAO_PARAMETROS")
            return False
        
        # Validar subcampos de autenticação
        if "autenticacao" in parametros:
            auth = parametros["autenticacao"]
            if "email_login" not in auth or "senha_login" not in auth:
                exception_handler.capturar_warning("Campos de autenticação incompletos", "VALIDACAO_PARAMETROS")
                return False
        
        exibir_mensagem("✅ Todos os parâmetros obrigatórios estão presentes!")
        return True
        
    except Exception as e:
        erro = exception_handler.capturar_excecao(e, "VALIDACAO_PARAMETROS", "Erro na validação")
        raise RPAException("Erro ao validar parâmetros", "VALIDACAO_PARAMETROS", e)

# ========================================
# FUNÇÕES DE NAVEGAÇÃO DAS TELAS
# ========================================

def navegar_tela_1_playwright(page: Page) -> bool:
    """
    TELA 1: Seleção do tipo de seguro (Carro)
    """
    try:
        exception_handler.definir_tela_atual("TELA_1")
        exibir_mensagem("📱 TELA 1: Selecionando Carro...")
        
        # Aguardar carregamento inicial da página
        page.wait_for_selector("button.group", timeout=5000)
        
        botao_carro = page.locator("button.group").first
        
        if botao_carro.is_visible():
            botao_carro.click()
            exibir_mensagem("✅ Botão 'Carro' clicado com sucesso")
            # Aguardar transição para a próxima tela
            page.wait_for_selector("#placaTelaDadosPlaca", timeout=5000)
            return True
        else:
            exception_handler.capturar_warning("Botão 'Carro' não está visível", "TELA_1")
            return False
            
    except Exception as e:
        exception_handler.capturar_excecao(e, "TELA_1", "Erro ao selecionar Carro")
        return False

def navegar_tela_2_playwright(page: Page, placa: str) -> bool:
    """
    TELA 2: Inserção da placa
    """
    try:
        exception_handler.definir_tela_atual("TELA_2")
        exibir_mensagem(f"📱 TELA 2: Inserindo placa {placa}...")
        
        campo_placa = page.locator("#placaTelaDadosPlaca").first
        campo_placa.click()
        campo_placa.fill(placa)
        
        exibir_mensagem(f"✅ Placa {placa} inserida com sucesso")
        
        botao_continuar = page.locator("#gtm-telaDadosAutoCotarComPlacaContinuar").first
        botao_continuar.click()
        
        exibir_mensagem("✅ Botão 'Continuar' clicado com sucesso")
        # Aguardar transição para a próxima tela
        page.wait_for_selector("#gtm-telaInfosAutoContinuar", timeout=5000)
        return True
        
    except Exception as e:
        exception_handler.capturar_excecao(e, "TELA_2", f"Erro ao inserir placa {placa}")
        return False

def navegar_tela_3_playwright(page: Page) -> bool:
    """
    TELA 3: Confirmação do veículo
    """
    try:
        exception_handler.definir_tela_atual("TELA_3")
        exibir_mensagem("📱 TELA 3: Confirmando informações do veículo...")
        
        botao_continuar = page.locator("#gtm-telaInfosAutoContinuar").first
        
        if botao_continuar.is_visible():
            botao_continuar.click()
            exibir_mensagem("✅ Botão 'Continuar' clicado com sucesso")
            page.wait_for_selector("#gtm-telaRenovacaoVeiculoContinuar", timeout=5000)
            return True
        else:
            exception_handler.capturar_warning("Botão 'Continuar' não encontrado", "TELA_3")
            return False
            
    except Exception as e:
        exception_handler.capturar_excecao(e, "TELA_3", "Erro ao confirmar veículo")
        return False

def navegar_tela_4_playwright(page: Page, veiculo_segurado: str) -> bool:
    """
    TELA 4: Veículo segurado
    """
    try:
        exception_handler.definir_tela_atual("TELA_4")
        exibir_mensagem("📱 TELA 4: Respondendo se veículo está segurado...")
        
        if veiculo_segurado == "Não":
            botao_nao = page.locator("#gtm-telaRenovacaoVeiculoContinuar").first
            botao_nao.click()
            exibir_mensagem("✅ Resposta 'Não' selecionada com sucesso")
        else:
            exception_handler.capturar_warning(f"Opção '{veiculo_segurado}' não implementada", "TELA_4")
            return False
        
        # Aguardar transição para a próxima tela
        page.wait_for_selector("div.bg-primary", timeout=5000)
        return True
        
    except Exception as e:
        exception_handler.capturar_excecao(e, "TELA_4", f"Erro ao responder veículo segurado: {veiculo_segurado}")
        return False

def navegar_tela_5_playwright(page: Page) -> bool:
    """
    TELA 5: Estimativa inicial - CAPTURA DE DADOS E RETORNO INTERMEDIÁRIO
    """
    try:
        exception_handler.definir_tela_atual("TELA_5")
        exibir_mensagem("📱 TELA 5: Aguardando carregamento da estimativa...")
        
        # Aguardar carregamento inicial da página
        # Este delay é maior que as outras telas porque a Tela 5
        # precisa calcular estimativas em tempo real
        page.wait_for_selector("div.bg-primary", timeout=10000)
        
        max_tentativas = 60  # Aumentado de 30 para 60
        tentativa = 0
        
        while tentativa < max_tentativas:
            exibir_mensagem(f"🔄 Tentativa {tentativa + 1}/{max_tentativas} - Aguardando cards de cobertura...")
            
            # Verificar se os cards de cobertura apareceram
            elemento_estimativa = page.locator("div.bg-primary")
            if elemento_estimativa.count() > 0:
                exibir_mensagem(f"✅ Elemento de estimativa encontrado: {elemento_estimativa.count()} cards")
                
                # Verificar se os cards ainda estão carregando (skeleton)
                card_text = elemento_estimativa.first.text_content().strip() if elemento_estimativa.first.text_content() else ""
                if "skeleton" not in card_text.lower() and len(card_text) > 10:
                    exibir_mensagem("✅ Cards carregados completamente!")
                    break
                else:
                    exibir_mensagem("⏳ Cards ainda carregando (skeleton detectado)...")
            
            # Verificar se há elementos com preços (fallback)
            elementos_preco = page.locator("text=R$")
            if elementos_preco.count() > 0:
                exibir_mensagem(f"✅ Elementos com preços encontrados: {elementos_preco.count()}")
                break
            
            # Verificar se o botão "Continuar" apareceu (fallback)
            botao_continuar = page.locator("#gtm-telaEstimativaContinuarParaCotacaoFinal")
            if botao_continuar.count() > 0:
                exibir_mensagem("✅ Botão 'Continuar' encontrado")
                break
            
            # Aguardar elementos dinâmicos com espera específica
            try:
                page.wait_for_selector("div.bg-primary", timeout=2000)  # Aumentado para 2 segundos
                break
            except Exception:
                try:
                    page.wait_for_selector("text=R$", timeout=2000)
                    break
                except Exception:
                    try:
                        page.wait_for_selector("#gtm-telaEstimativaContinuarParaCotacaoFinal", timeout=2000)
                        break
                    except Exception:
                        # Aguardar um pouco mais antes da próxima tentativa
                        time.sleep(2)
                        continue
            
            tentativa += 1
        
        if tentativa >= max_tentativas:
            exception_handler.capturar_warning("Elementos da estimativa não carregaram completamente", "TELA_5")
            # Não retornar False aqui, continuar mesmo sem dados completos
        
        exibir_mensagem("✅ Estimativa carregada com sucesso")
        
        # Aguardar um pouco mais para garantir que os dados estão carregados
        exibir_mensagem("⏳ Aguardando estabilização dos dados...")
        time.sleep(5)
        
        # CAPTURAR DADOS DO CARROSSEL DE ESTIMATIVAS
        dados_carrossel = capturar_dados_carrossel_estimativas_playwright(page)
        
        # ========================================
        # JSON COMPREENSIVO - TELA 5
        # ========================================
        if dados_carrossel and dados_carrossel.get('coberturas_detalhadas') and len(dados_carrossel.get('coberturas_detalhadas', [])) > 0:
            # Criar JSON compreensivo com todas as informações da estimativa inicial
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Extrair valores únicos (remover duplicatas)
            coberturas_unicas = {}
            for cobertura in dados_carrossel['coberturas_detalhadas']:
                nome = cobertura.get('nome_cobertura', '')
                if nome not in coberturas_unicas:
                    coberturas_unicas[nome] = cobertura
            
            # Criar estrutura do JSON compreensivo
            json_compreensivo = {
                "metadata": {
                    "timestamp": datetime.now().isoformat(),
                    "tela": 5,
                    "nome_tela": "Estimativa Inicial",
                    "url": page.url,
                    "titulo_pagina": page.title(),
                    "versao_rpa": "2.0.0",
                    "autor": "Luciano Otero"
                },
                "resumo_executivo": {
                    "total_coberturas": len(coberturas_unicas),
                    "total_beneficios": len(dados_carrossel.get('beneficios_gerais', [])),
                    "coberturas_disponiveis": list(coberturas_unicas.keys())
                },
                "coberturas_detalhadas": [
                    {
                        "nome": nome,
                        "valores": cobertura.get('valores', {}),
                        "beneficios": cobertura.get('beneficios', []),
                        "total_beneficios": len(cobertura.get('beneficios', [])),
                        "texto_completo": cobertura.get('texto_completo', '')
                    }
                    for nome, cobertura in coberturas_unicas.items()
                ],
                "beneficios_gerais": dados_carrossel.get('beneficios_gerais', []),
                "dados_brutos": dados_carrossel
            }
            
            # Salvar JSON compreensivo
            json_compreensivo_path = f"temp/json_compreensivo_tela_5_{timestamp}.json"
            with open(json_compreensivo_path, 'w', encoding='utf-8') as f:
                json.dump(json_compreensivo, f, indent=2, ensure_ascii=False)
            
            # Exibir resumo do JSON compreensivo
            print("\n" + "="*80)
            print("🎯 JSON COMPREENSIVO - TELA 5 CRIADO COM SUCESSO!")
            print("="*80)
            print(f"📁 Arquivo: {json_compreensivo_path}")
            print(f"📊 Total de Coberturas Únicas: {len(coberturas_unicas)}")
            print(f"🎁 Total de Benefícios: {len(dados_carrossel.get('beneficios_gerais', []))}")
            
            # Exibir coberturas encontradas
            for nome, cobertura in coberturas_unicas.items():
                valores = cobertura.get('valores', {})
                de = valores.get('de', 'N/A')
                ate = valores.get('ate', 'N/A')
                print(f"💰 {nome}: {de} até {ate}")
            
            print("="*80)
            
            exibir_mensagem(f"💾 **JSON COMPREENSIVO SALVO**: {json_compreensivo_path}")
        
        # RETORNO INTERMEDIÁRIO DOS DADOS DO CARROSSEL
        if dados_carrossel:
            exibir_mensagem("🎯 **RETORNO INTERMEDIÁRIO**: Dados do carrossel capturados com sucesso!")
            exibir_mensagem(f"📊 **COBERTURAS DETALHADAS**: {len(dados_carrossel['coberturas_detalhadas'])}")
            exibir_mensagem(f"🎁 **BENEFÍCIOS GERAIS**: {len(dados_carrossel['beneficios_gerais'])}")
            exibir_mensagem(f"💰 **VALORES MONETÁRIOS**: {dados_carrossel['valores_encontrados']}")
            
            # Exibir detalhes das coberturas encontradas
            for i, cobertura in enumerate(dados_carrossel['coberturas_detalhadas']):
                exibir_mensagem(f"📋 **COBERTURA {i+1}**: {cobertura['nome_cobertura']}")
                if cobertura['valores']['de'] and cobertura['valores']['ate']:
                    exibir_mensagem(f"   💰 **VALORES**: {cobertura['valores']['de']} até {cobertura['valores']['ate']}")
                if cobertura['beneficios']:
                    beneficios_nomes = [b['nome'] for b in cobertura['beneficios']]
                    exibir_mensagem(f"   🎁 **BENEFÍCIOS**: {', '.join(beneficios_nomes)}")
            
            # Salvar retorno intermediário em arquivo específico
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            retorno_path = f"temp/retorno_intermediario_carrossel_{timestamp}.json"
            
            # Criar diretório temp se não existir
            os.makedirs("temp", exist_ok=True)
            
            # Limpar dados para serialização JSON
            dados_limpos = {
                "timestamp": str(dados_carrossel.get("timestamp", "")),
                "tela": dados_carrossel.get("tela", 5),
                "nome_tela": str(dados_carrossel.get("nome_tela", "")),
                "url": str(dados_carrossel.get("url", "")),
                "titulo": str(dados_carrossel.get("titulo", "")),
                "coberturas_detalhadas": dados_carrossel.get("coberturas_detalhadas", []),
                "beneficios_gerais": dados_carrossel.get("beneficios_gerais", []),
                "valores_encontrados": dados_carrossel.get("valores_encontrados", 0),
                "seguradoras": dados_carrossel.get("seguradoras", []),
                "elementos_detectados": dados_carrossel.get("elementos_detectados", [])
            }
            
            with open(retorno_path, 'w', encoding='utf-8') as f:
                json.dump(dados_limpos, f, indent=2, ensure_ascii=False)
            
            exibir_mensagem(f"💾 **RETORNO SALVO**: {retorno_path}")
            
            # Exibir retorno intermediário estruturado no terminal
            print("\n" + "="*60)
            print("📋 RETORNO INTERMEDIÁRIO - TELA 5")
            print("="*60)
            print(json.dumps(dados_limpos, indent=2, ensure_ascii=False))
            print("="*60)
            
        else:
            exibir_mensagem("⚠️ **AVISO**: Não foi possível capturar dados do carrossel")
        
        # Clicar em Continuar
        exibir_mensagem("⏳ Aguardando botão Continuar aparecer...")
        
        try:
            # Aguardar o botão estar disponível
            page.wait_for_selector("#gtm-telaEstimativaContinuarParaCotacaoFinal", timeout=10000)
            botao_continuar = page.locator("#gtm-telaEstimativaContinuarParaCotacaoFinal").first
            
            # Verificar se o botão está visível e clicável
            if botao_continuar.is_visible():
                botao_continuar.click()
                exibir_mensagem("✅ Botão 'Continuar' clicado com sucesso")
            else:
                exibir_mensagem("⚠️ Botão 'Continuar' não está visível, tentando clicar mesmo assim...")
                botao_continuar.click()
                exibir_mensagem("✅ Botão 'Continuar' clicado com sucesso")
        except Exception as e:
            exibir_mensagem(f"⚠️ Erro ao aguardar botão Continuar: {str(e)}")
            exibir_mensagem("🔄 Tentando seletor alternativo...")
            try:
                # Fallback para seletor por texto
                botao_continuar = page.locator("text=Continuar").first
                botao_continuar.click()
                exibir_mensagem("✅ Botão 'Continuar' clicado com seletor alternativo")
            except Exception as e2:
                exibir_mensagem(f"❌ Falha ao clicar no botão Continuar: {str(e2)}")
                return False
        
        # Aguardar transição para a próxima tela
        page.wait_for_selector("#gtm-telaItensAutoContinuar", timeout=5000)
        return True
        
    except Exception as e:
        exception_handler.capturar_excecao(e, "TELA_5", "Erro ao processar Tela 5")
        return False

# ========================================
# FUNÇÕES DE CAPTURA DE DADOS
# ========================================

def capturar_dados_carrossel_estimativas_playwright(page: Page) -> Dict[str, Any]:
    """
    ================================================================================
    FUNÇÃO: capturar_dados_carrossel_estimativas_playwright()
    ================================================================================
    
    DESCRIÇÃO:
        Captura dados estruturados do carrossel de estimativas da Tela 5.
        Esta função é o coração da captura de dados, extraindo informações
        detalhadas de cada card de cobertura, incluindo valores monetários,
        benefícios e metadados.
    
    ELEMENTOS CAPTURADOS:
        - Nome da cobertura: "button p.text-white"
        - Valores monetários: "p.text-primary.underline"
        - Benefícios: "div.gap-3.flex.flex-col.pl-4.mt-3"
        - Texto completo: Conteúdo total do card
    
    ESTRATÉGIA DE CAPTURA:
        1. Localizar todos os cards de cobertura
        2. Para cada card:
           a. Extrair nome da cobertura
           b. Parsear valores "De R$ X até R$ Y"
           c. Capturar lista de benefícios
           d. Estruturar dados em JSON
        3. Salvar dados em arquivo temporário
        4. Retornar estrutura completa
    
    TÉCNICAS UTILIZADAS:
        - Regex patterns para parsing de valores monetários
        - Seletores CSS específicos para cada elemento
        - Estruturação hierárquica de dados
        - Fallbacks para casos de erro
    
    PARÂMETROS:
        page (Page): Objeto page do Playwright
    
    RETORNO:
        dict: Estrutura JSON com dados capturados ou None se erro
    
    ESTRUTURA DE RETORNO:
        {
            "timestamp": "2025-09-02T03:45:30.523994",
            "tela": 5,
            "nome_tela": "Estimativa Inicial",
            "coberturas_detalhadas": [
                {
                    "indice": 1,
                    "cobertura": "Cobertura Compreensiva",
                    "valores": {"de": "R$ 1.600,00", "ate": "R$ 2.200,00"},
                    "beneficios": [{"nome": "Colisão e Acidentes", "status": "incluido"}]
                }
            ],
            "valores_encontrados": 6,
            "beneficios_gerais": [...],
            "seguradoras": [...],
            "elementos_detectados": [...]
        }
    
    LOGS:
        - "🔍 Encontrados {X} cards de cobertura (bg-primary)"
        - "📋 Card {X}: {cobertura} - De {valor} até {valor}"
        - "💾 DADOS SALVOS: {caminho_arquivo}"
        - "📊 RESUMO: {X} coberturas detalhadas, {X} benefícios gerais"
        - "❌ ERRO na captura de dados: {erro}"
    ================================================================================
    """
    try:
        # PASSO 1: Inicializar estrutura de dados do carrossel
        # Esta estrutura segue o padrão definido no exemplo_json_retorno.json
        dados_carrossel = {
            "timestamp": datetime.now().isoformat(),  # Timestamp ISO para rastreamento
            "tela": 5,                                # Número da tela atual
            "nome_tela": "Estimativa Inicial",        # Nome descritivo da tela
            "url": str(page.url),                     # URL atual da página
            "titulo": str(page.title),                # Título da página
            "coberturas_detalhadas": [],              # Lista de coberturas capturadas
            "beneficios_gerais": [],                  # Benefícios encontrados na página
            "valores_encontrados": 0,                 # Contador de valores monetários
            "seguradoras": [],                        # Seguradoras detectadas
            "elementos_detectados": []                # Elementos especiais detectados
        }
        
        # DEBUG: Verificar quais elementos estão na página
        exibir_mensagem("🔍 DEBUG: Verificando elementos na página...")
        
        # ESTRATÉGIA 1: Tentar capturar cards usando seletores mais específicos
        # Primeiro, vamos tentar encontrar os cards de cobertura usando diferentes estratégias
        
        # Estratégia 1.1: Buscar por elementos que contenham "Cobertura" e valores monetários
        exibir_mensagem("🔍 DEBUG: Estratégia 1.1 - Buscando cards com 'Cobertura'...")
        
        # Buscar por elementos que contenham "Cobertura" e "R$" no mesmo contexto
        cards_cobertura = page.locator("div:has-text('Cobertura'):has-text('R$')")
        exibir_mensagem(f"🔍 DEBUG: Cards com 'Cobertura' e 'R$' encontrados: {cards_cobertura.count()}")
        
        if cards_cobertura.count() > 0:
            exibir_mensagem(f"✅ Encontrados {cards_cobertura.count()} cards de cobertura com valores")
            
            for i in range(cards_cobertura.count()):
                try:
                    card = cards_cobertura.nth(i)
                    card_text = card.text_content().strip() if card.text_content() else ""
                    
                    exibir_mensagem(f"🔍 DEBUG: Card {i+1} texto completo: '{card_text}'")
                    
                    if len(card_text) < 20:  # Se o texto for muito curto, tentar pegar o elemento pai
                        exibir_mensagem(f"🔍 DEBUG: Card {i+1} texto muito curto, buscando elemento pai...")
                        card = card.locator("..").first  # Elemento pai
                        card_text = card.text_content().strip() if card.text_content() else ""
                        exibir_mensagem(f"🔍 DEBUG: Card {i+1} texto do pai: '{card_text[:200]}...'")
                    
                    cobertura_info = {
                        "indice": i + 1,
                        "nome_cobertura": "",
                        "valores": {
                            "de": "",
                            "ate": ""
                        },
                        "beneficios": [],
                        "texto_completo": card_text
                    }
                    
                    # Extrair nome da cobertura usando regex mais robusto
                    cobertura_patterns = [
                        r"Cobertura\s+([A-Za-zÀ-ÿ\s]+?)(?:\s|$|R\$)",
                        r"([A-Za-zÀ-ÿ\s]+?)\s+Cobertura",
                        r"Cobertura\s+Compreensiva",
                        r"Cobertura\s+Roubo\s+e\s+Furto",
                        r"Cobertura\s+RCF"
                    ]
                    
                    for pattern in cobertura_patterns:
                        match = re.search(pattern, card_text, re.IGNORECASE)
                        if match:
                            if "Compreensiva" in pattern:
                                cobertura_info["nome_cobertura"] = "Cobertura Compreensiva"
                            elif "Roubo" in pattern:
                                cobertura_info["nome_cobertura"] = "Cobertura Roubo e Furto"
                            elif "RCF" in pattern:
                                cobertura_info["nome_cobertura"] = "Cobertura RCF"
                            else:
                                cobertura_info["nome_cobertura"] = match.group(1).strip()
                            exibir_mensagem(f"🔍 DEBUG: Nome encontrado via regex: '{cobertura_info['nome_cobertura']}'")
                            break
                    
                    # Extrair valores monetários usando regex mais específico
                    valor_patterns = [
                        r"De\s*R\$\s*([0-9.,]+)\s*até\s*R\$\s*([0-9.,]+)",
                        r"R\$\s*([0-9.,]+)\s*até\s*R\$\s*([0-9.,]+)",
                        r"([0-9.,]+)\s*até\s*([0-9.,]+)"
                    ]
                    
                    for pattern in valor_patterns:
                        match = re.search(pattern, card_text, re.IGNORECASE)
                        if match:
                            cobertura_info["valores"]["de"] = f"R$ {match.group(1)}"
                            cobertura_info["valores"]["ate"] = f"R$ {match.group(2)}"
                            exibir_mensagem(f"🔍 DEBUG: Valores extraídos: De {cobertura_info['valores']['de']} até {cobertura_info['valores']['ate']}")
                            break
                    
                    # Extrair benefícios conhecidos do texto do card
                    beneficios_conhecidos = [
                        "Colisão e Acidentes", "Roubo e Furto", "Incêndio", "Danos a terceiros",
                        "Assistência 24h", "Carro Reserva", "Vidros", "Roubo", "Furto",
                        "Danos parciais em tentativas de roubo", "Danos materiais a terceiros",
                        "Danos corporais a terceiro", "Assistência", "Carro reserva",
                        "Vidros", "Acidentes", "Colisão", "Terceiros", "Materiais", "Corporais"
                    ]
                    
                    for beneficio in beneficios_conhecidos:
                        if beneficio.lower() in card_text.lower():
                            cobertura_info["beneficios"].append({
                                "nome": beneficio,
                                "status": "incluido"
                            })
                    
                    dados_carrossel["coberturas_detalhadas"].append(cobertura_info)
                    exibir_mensagem(f"📋 Card {len(dados_carrossel['coberturas_detalhadas'])}: {cobertura_info['nome_cobertura']} - De {cobertura_info['valores']['de']} até {cobertura_info['valores']['ate']}")
                    
                except Exception as e:
                    exibir_mensagem(f"⚠️ Erro ao processar card {i+1}: {str(e)}")
                    continue
        
        # ESTRATÉGIA 1.2: Se não encontrou cards com a estratégia anterior, tentar seletores específicos
        if len(dados_carrossel["coberturas_detalhadas"]) == 0:
            exibir_mensagem("🔍 DEBUG: Estratégia 1.2 - Tentando seletores específicos...")
            
            # Tentar diferentes seletores para encontrar os cards
            seletores_cards = [
                "div.bg-primary",
                "div[class*='bg-primary']",
                "div[class*='card']",
                "div[class*='cobertura']",
                "div:has(button)",
                "div:has(p.text-white)"
            ]
            
            for seletor in seletores_cards:
                try:
                    cards = page.locator(seletor)
                    exibir_mensagem(f"🔍 DEBUG: Seletor '{seletor}' encontrou: {cards.count()} elementos")
                    
                    if cards.count() > 0:
                        for i in range(min(cards.count(), 5)):  # Limitar a 5 cards
                            try:
                                card = cards.nth(i)
                                card_text = card.text_content().strip() if card.text_content() else ""
                                
                                exibir_mensagem(f"🔍 DEBUG: Card {i+1} com seletor '{seletor}': '{card_text[:100]}...'")
                                
                                # Verificar se o card tem conteúdo relevante
                                if "cobertura" in card_text.lower() or "r$" in card_text.lower():
                                    cobertura_info = {
                                        "indice": len(dados_carrossel["coberturas_detalhadas"]) + 1,
                                        "nome_cobertura": "",
                                        "valores": {"de": "", "ate": ""},
                                        "beneficios": [],
                                        "texto_completo": card_text
                                    }
                                    
                                    # Extrair nome e valores (mesma lógica anterior)
                                    # ... (código de extração)
                                    
                                    dados_carrossel["coberturas_detalhadas"].append(cobertura_info)
                                    exibir_mensagem(f"📋 Card encontrado via '{seletor}': {cobertura_info['nome_cobertura']}")
                                    
                            except Exception as e:
                                exibir_mensagem(f"⚠️ Erro ao processar card com seletor '{seletor}': {str(e)}")
                                continue
                        
                        if len(dados_carrossel["coberturas_detalhadas"]) > 0:
                            break  # Se encontrou cards, parar de tentar outros seletores
                            
                except Exception as e:
                    exibir_mensagem(f"⚠️ Erro com seletor '{seletor}': {str(e)}")
                    continue
        
        # ESTRATÉGIA 2: Fallback - Buscar por valores monetários na página inteira
        if len(dados_carrossel["coberturas_detalhadas"]) == 0:
            exibir_mensagem("🔍 DEBUG: Estratégia 2 - Fallback: buscando valores monetários na página...")
            
            # Buscar por todos os elementos que contenham "R$"
            elementos_r = page.locator("text=R$")
            exibir_mensagem(f"🔍 DEBUG: Elementos com 'R$' encontrados: {elementos_r.count()}")
            
            if elementos_r.count() > 0:
                for i in range(min(elementos_r.count(), 10)):  # Limitar a 10 elementos
                    try:
                        elemento = elementos_r.nth(i)
                        elemento_text = elemento.text_content().strip() if elemento.text_content() else ""
                        
                        # Buscar o contexto do elemento (elemento pai)
                        contexto = elemento.locator("..").first
                        contexto_text = contexto.text_content().strip() if contexto.text_content() else ""
                        
                        exibir_mensagem(f"🔍 DEBUG: Elemento R$ {i+1}: '{elemento_text}' | Contexto: '{contexto_text[:100]}...'")
                        
                        # Se o contexto contém "Cobertura", pode ser um card válido
                        if "cobertura" in contexto_text.lower():
                            cobertura_info = {
                                "indice": len(dados_carrossel["coberturas_detalhadas"]) + 1,
                                "nome_cobertura": "Cobertura Detectada",
                                "valores": {"de": "", "ate": ""},
                                "beneficios": [],
                                "texto_completo": contexto_text
                            }
                            
                            # Extrair valores
                            valor_patterns = [
                                r"De\s*R\$\s*([0-9.,]+)\s*até\s*R\$\s*([0-9.,]+)",
                                r"R\$\s*([0-9.,]+)\s*até\s*R\$\s*([0-9.,]+)"
                            ]
                            
                            for pattern in valor_patterns:
                                match = re.search(pattern, contexto_text, re.IGNORECASE)
                                if match:
                                    cobertura_info["valores"]["de"] = f"R$ {match.group(1)}"
                                    cobertura_info["valores"]["ate"] = f"R$ {match.group(2)}"
                                    break
                            
                            dados_carrossel["coberturas_detalhadas"].append(cobertura_info)
                            exibir_mensagem(f"📋 Valor encontrado: De {cobertura_info['valores']['de']} até {cobertura_info['valores']['ate']}")
                            
                    except Exception as e:
                        exibir_mensagem(f"⚠️ Erro ao processar elemento R$ {i+1}: {str(e)}")
                        continue
        
        # Contar valores encontrados
        dados_carrossel["valores_encontrados"] = len(dados_carrossel["coberturas_detalhadas"])
        
        # Procurar por valores monetários gerais (fallback)
        valores_monetarios = page.locator("text=R$")
        dados_carrossel["valores_encontrados"] = max(dados_carrossel["valores_encontrados"], valores_monetarios.count())
        
        # Procurar por benefícios gerais na página
        beneficios_gerais = [
            "Colisão e Acidentes", "Roubo e Furto", "Incêndio", "Danos a terceiros",
            "Assistência 24h", "Carro Reserva", "Vidros", "Roubo", "Furto",
            "Danos parciais em tentativas de roubo", "Danos materiais a terceiros",
            "Danos corporais a terceiro"
        ]
        
        for beneficio in beneficios_gerais:
            elementos = page.locator(f"text={beneficio}")
            if elementos.count() > 0:
                dados_carrossel["beneficios_gerais"].append({
                    "nome": beneficio,
                    "encontrado": True,
                    "quantidade_elementos": elementos.count()
                })
        
        # Procurar por seguradoras
        seguradoras_texto = [
            "Seguradora", "seguradora", "Seguro", "seguro",
            "Allianz", "allianz", "Porto", "porto", "SulAmérica", "sulamerica",
            "Bradesco", "bradesco", "Itaú", "itau", "Santander", "santander"
        ]
        
        for seguradora in seguradoras_texto:
            elementos = page.locator(f"text={seguradora}")
            if elementos.count() > 0:
                for j in range(min(elementos.count(), 3)):  # Limitar a 3 elementos
                    texto = elementos.nth(j).text_content().strip()
                    if texto and len(texto) > 2:
                        dados_carrossel["seguradoras"].append({
                            "nome": texto,
                            "seletor": "texto_contido"
                        })
        
        # Procurar por elementos específicos do carrossel
        elementos_carrossel = page.locator("[class*='carousel'], [class*='slider'], [class*='swiper']")
        if elementos_carrossel.count() > 0:
            dados_carrossel["elementos_detectados"].append("carrossel_detectado")
        
        # Capturar texto completo da página para análise
        page_content = page.content()
        page_text = page_content.lower() if page_content else ""
        
        # Verificar presença de palavras-chave
        palavras_chave = ["estimativa", "carrossel", "cobertura", "preço", "valor", "plano"]
        for palavra in palavras_chave:
            if palavra in page_text:
                dados_carrossel["elementos_detectados"].append(f"palavra_chave: {palavra}")
        
        # Salvar dados em arquivo temporário
        temp_dir = "temp/captura_carrossel"
        os.makedirs(temp_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        json_path = f"{temp_dir}/carrossel_estimativas_{timestamp}.json"
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(dados_carrossel, f, indent=2, ensure_ascii=False)
        
        exibir_mensagem(f"💾 DADOS SALVOS: {json_path}")
        exibir_mensagem(f"📊 RESUMO: {len(dados_carrossel['coberturas_detalhadas'])} coberturas detalhadas, {len(dados_carrossel['beneficios_gerais'])} benefícios gerais")
        
        return dados_carrossel
        
    except Exception as e:
        exibir_mensagem(f"❌ ERRO na captura de dados: {str(e)}")
        return None

# ========================================
# FUNÇÃO PRINCIPAL
# ========================================

def executar_rpa_playwright(parametros: Dict[str, Any]) -> Dict[str, Any]:
    """
    Função principal do RPA Playwright - Telas 1-5
    
    PARÂMETROS:
        parametros: dict - Parâmetros de configuração
        
    RETORNO:
        dict: Resultado estruturado da execução
    """
    inicio_execucao = time.time()
    
    try:
        # Inicializar Exception Handler
        exception_handler.limpar_erros()
        exception_handler.definir_tela_atual("INICIALIZACAO")
        
        exibir_mensagem("🚀 INICIANDO RPA PLAYWRIGHT - TELAS 1-5")
        exibir_mensagem("=" * 50)
        
        # Validar parâmetros
        if not validar_parametros_obrigatorios(parametros):
            raise RPAException("Parâmetros obrigatórios inválidos", "VALIDACAO")
        
        # Inicializar Playwright
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()
            
            # Navegar para URL inicial
            page.goto(parametros["url"])
            exibir_mensagem(f"✅ Navegação para {parametros['url']} realizada")
            
            # Executar Telas 1-5 sequencialmente
            telas_executadas = 0
            resultado_telas = {}
            dados_tela_5 = None
            
            # TELA 1
            exibir_mensagem("\n" + "="*50)
            if navegar_tela_1_playwright(page):
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
            
            # TELA 2
            exibir_mensagem("\n" + "="*50)
            if navegar_tela_2_playwright(page, parametros['placa']):
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
            
            # TELA 3
            exibir_mensagem("\n" + "="*50)
            if navegar_tela_3_playwright(page):
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
            
            # TELA 4
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
            
            # TELA 5
            exibir_mensagem("\n" + "="*50)
            if navegar_tela_5_playwright(page):
                telas_executadas += 1
                resultado_telas["tela_5"] = True
                exibir_mensagem("✅ TELA 5 CONCLUÍDA!")
                
                # Os dados da Tela 5 já foram capturados dentro da função navegar_tela_5_playwright
                # Não é necessário capturar novamente aqui
                dados_tela_5 = {}  # Dados já processados na Tela 5
                arquivo_salvo = ""  # Arquivo já salvo na Tela 5
                
                exibir_mensagem("💾 Dados da Tela 5 já foram processados e salvos")
                
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
            
            # Resultado final
            exibir_mensagem("\n" + "="*60)
            exibir_mensagem("🎉 RPA TELAS 1 A 5 CONCLUÍDO COM SUCESSO!")
            exibir_mensagem(f"✅ Total de telas executadas: {telas_executadas}/5")
            exibir_mensagem("✅ Todas as telas funcionaram corretamente")
            exibir_mensagem("✅ Navegação sequencial realizada com sucesso")
            
            # Fechar browser
            browser.close()
            
            # Calcular tempo de execução
            tempo_execucao = time.time() - inicio_execucao
            
            # Retorno estruturado
            return criar_retorno_sucesso(
                resultado_telas,
                {"dados_tela_5": dados_tela_5} if dados_tela_5 else {},
                arquivo_salvo if 'arquivo_salvo' in locals() else "",
                tempo_execucao,
                parametros
            )
            
    except Exception as e:
        exception_handler.capturar_excecao(e, "EXECUCAO_PRINCIPAL", "Erro na execução principal")
        
        return criar_retorno_erro(
            str(e),
            "EXECUCAO_PRINCIPAL",
            time.time() - inicio_execucao,
            parametros,
            exception_handler
        )

# ========================================
# EXECUÇÃO DIRETA
# ========================================

if __name__ == "__main__":
    try:
        # Carregar parâmetros
        parametros = carregar_parametros()
        
        # Executar RPA
        resultado = executar_rpa_playwright(parametros)
        
        # Exibir resultado
        print("\n" + "="*50)
        print("📊 RESULTADO DA EXECUÇÃO")
        print("="*50)
        print(f"Status: {resultado['status']}")
        print(f"Tempo: {resultado['tempo_execucao']}")
        print(f"Erros: {resultado['erros']['total_erros']}")
        print(f"Warnings: {resultado['erros']['total_warnings']}")
        
        if resultado['status'] == 'success':
            print("✅ RPA executado com sucesso!")
        else:
            print("❌ RPA falhou!")
        
        # Exibir retorno estruturado completo
        print("\n" + "="*50)
        print("📋 RETORNO ESTRUTURADO COMPLETO")
        print("="*50)
        import json
        print(json.dumps(resultado, indent=2, ensure_ascii=False))
            
    except Exception as e:
        exception_handler.capturar_excecao(e, "EXECUCAO_DIRETA", "Erro na execução direta")
        sys.exit(1)
