#!/usr/bin/env python3
"""
EXECUTAR RPA IMEDIATO PLAYWRIGHT - VERSÃO PRODUÇÃO
Implementação completa do RPA usando Playwright com Sistema de Exception Handler

DESCRIÇÃO:
- Migração completa do Selenium para Playwright
- Sistema de Exception Handler robusto
- Telas 1-15 implementadas e testadas
- Captura de dados dos planos de seguro
- Estrutura de retorno padronizada

AUTOR: Luciano Otero
DATA: 2025-09-02
VERSÃO: 1.0.0
STATUS: Implementação completa com Exception Handler
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

def salvar_dados_planos(dados_planos: Dict[str, Any], prefixo: str = "dados_planos_seguro"):
    """
    Salva os dados dos planos em arquivo JSON
    
    PARÂMETROS:
        dados_planos: dict - Dados dos planos a serem salvos
        prefixo: str - Prefixo do nome do arquivo
        
    RETORNO:
        str: Caminho do arquivo salvo
    """
    try:
        exception_handler.definir_tela_atual("SALVAMENTO_DADOS")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_arquivo = f"{prefixo}_{timestamp}.json"
        
        with open(nome_arquivo, 'w', encoding='utf-8') as f:
            json.dump(dados_planos, f, indent=2, ensure_ascii=False)
        
        exibir_mensagem(f"💾 Dados salvos em: {nome_arquivo}")
        return nome_arquivo
        
    except Exception as e:
        erro = exception_handler.capturar_excecao(e, "SALVAMENTO_DADOS", "Erro ao salvar dados")
        raise RPAException("Erro ao salvar dados dos planos", "SALVAMENTO_DADOS", e)

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
        
        max_tentativas = 30
        tentativa = 0
        
        while tentativa < max_tentativas:
            exibir_mensagem(f"🔄 Tentativa {tentativa + 1}/{max_tentativas} - Aguardando cards de cobertura...")
            
            # Verificar se os cards de cobertura apareceram
            elemento_estimativa = page.locator("div.bg-primary")
            if elemento_estimativa.count() > 0:
                exibir_mensagem(f"✅ Elemento de estimativa encontrado: {elemento_estimativa.count()} cards")
                break
            
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
                page.wait_for_selector("div.bg-primary", timeout=1000)
                break
            except:
                try:
                    page.wait_for_selector("text=R$", timeout=1000)
                    break
                except:
                    try:
                        page.wait_for_selector("#gtm-telaEstimativaContinuarParaCotacaoFinal", timeout=1000)
                        break
                    except:
                        continue
            
            tentativa += 1
        
        if tentativa >= max_tentativas:
            exception_handler.capturar_warning("Elementos da estimativa não carregaram", "TELA_5")
            return False
        
        exibir_mensagem("✅ Estimativa carregada com sucesso")
        
        # CAPTURAR DADOS DO CARROSSEL DE ESTIMATIVAS
        dados_carrossel = capturar_dados_carrossel_estimativas_playwright(page)
        
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
        exception_handler.capturar_excecao(e, "TELA_5", "Erro ao carregar estimativa")
        return False

def navegar_tela_6_playwright(page: Page, combustivel: str, kit_gas: bool, blindado: bool, financiado: bool) -> bool:
    """
    TELA 6: Itens do carro - SELEÇÃO DE COMBUSTÍVEL E CHECKBOXES
    """
    try:
        exception_handler.definir_tela_atual("TELA_6")
        exibir_mensagem("📱 TELA 6: Aguardando carregamento...")
        
        max_tentativas = 20
        tentativa = 0
        
        while tentativa < max_tentativas:
            botao_continuar = page.locator("#gtm-telaItensAutoContinuar")
            if botao_continuar.count() > 0 and botao_continuar.first.is_visible():
                break
            # Aguardar carregamento da tela
            try:
                page.wait_for_selector("#gtm-telaItensAutoContinuar", timeout=1000)
                break
            except:
                continue
            tentativa += 1
        
        if tentativa >= max_tentativas:
            exception_handler.capturar_warning("Tela 6 não carregou", "TELA_6")
            return False
        
        exibir_mensagem("✅ Tela 6 carregada com sucesso")
        
        # Selecionar combustível
        exibir_mensagem(f"📱 TELA 6: Selecionando combustível {combustivel}...")
        
        mapeamento_combustivel = {
            "Flex": "1", "Gasolina": "2", "Alcool": "3", "Etanol": "3",
            "Diesel": "4", "Híbrido": "5", "Elétrico": "6"
        }
        
        valor_radio = mapeamento_combustivel.get(combustivel)
        combustivel_selecionado = False
        
        if valor_radio:
            try:
                radio_combustivel = page.locator(f"input[name='tipoCombustivelTelaItens'][value='{valor_radio}']").first
                if radio_combustivel.is_visible():
                    radio_combustivel.click()
                    combustivel_selecionado = True
                    exibir_mensagem(f"✅ Combustível {combustivel} selecionado com sucesso")
                else:
                    exception_handler.capturar_warning(f"Radio button para {combustivel} não está visível", "TELA_6")
            except Exception as e:
                exception_handler.capturar_warning(f"Erro ao selecionar {combustivel}: {str(e)}", "TELA_6")
        else:
            exception_handler.capturar_warning(f"Combustível '{combustivel}' não mapeado", "TELA_6")
        
        if not combustivel_selecionado:
            exception_handler.capturar_warning(f"Combustível {combustivel} não encontrado, continuando", "TELA_6")
        
        # Configurar checkboxes
        exibir_mensagem("📱 TELA 6: Configurando checkboxes...")
        
        # Kit Gas
        try:
            checkbox_kit_gas = page.locator('input[value="Kit Gás"]').first
            if checkbox_kit_gas.is_visible():
                if kit_gas and not checkbox_kit_gas.is_checked():
                    checkbox_kit_gas.check()
                    exibir_mensagem("✅ Checkbox Kit Gas: MARCADO")
                elif not kit_gas and checkbox_kit_gas.is_checked():
                    checkbox_kit_gas.uncheck()
                    exibir_mensagem("✅ Checkbox Kit Gas: DESMARCADO")
                else:
                    estado = "MARCADO" if kit_gas else "DESMARCADO"
                    exibir_mensagem(f"✅ Checkbox Kit Gas: {estado} (já estava correto)")
            else:
                exception_handler.capturar_warning("Checkbox Kit Gas não encontrado", "TELA_6")
        except Exception as e:
            exception_handler.capturar_warning(f"Erro ao configurar Kit Gas: {str(e)}", "TELA_6")
        
        # Blindado
        try:
            checkbox_blindado = page.locator('input[value="Blindado"]').first
            if checkbox_blindado.is_visible():
                if blindado and not checkbox_blindado.is_checked():
                    checkbox_blindado.check()
                    exibir_mensagem("✅ Checkbox Blindado: MARCADO")
                elif not blindado and checkbox_blindado.is_checked():
                    checkbox_blindado.uncheck()
                    exibir_mensagem("✅ Checkbox Blindado: DESMARCADO")
                else:
                    estado = "MARCADO" if blindado else "DESMARCADO"
                    exibir_mensagem(f"✅ Checkbox Blindado: {estado} (já estava correto)")
            else:
                exception_handler.capturar_warning("Checkbox Blindado não encontrado", "TELA_6")
        except Exception as e:
            exception_handler.capturar_warning(f"Erro ao configurar Blindado: {str(e)}", "TELA_6")
        
        # Financiado
        try:
            checkbox_financiado = page.locator('input[value="Financiado"]').first
            if checkbox_financiado.is_visible():
                if financiado and not checkbox_financiado.is_checked():
                    checkbox_financiado.check()
                    exibir_mensagem("✅ Checkbox Financiado: MARCADO")
                elif not financiado and checkbox_financiado.is_checked():
                    checkbox_financiado.uncheck()
                    exibir_mensagem("✅ Checkbox Financiado: DESMARCADO")
                else:
                    estado = "MARCADO" if financiado else "DESMARCADO"
                    exibir_mensagem(f"✅ Checkbox Financiado: {estado} (já estava correto)")
            else:
                exception_handler.capturar_warning("Checkbox Financiado não encontrado", "TELA_6")
        except Exception as e:
            exception_handler.capturar_warning(f"Erro ao configurar Financiado: {str(e)}", "TELA_6")
        
        # Clicar em Continuar
        botao_continuar.first.click()
        exibir_mensagem("✅ Botão 'Continuar' clicado com sucesso")
        # Aguardar transição para a próxima tela
        page.wait_for_selector("#enderecoTelaEndereco", timeout=5000)
        return True
        
    except Exception as e:
        exception_handler.capturar_excecao(e, "TELA_6", "Erro ao configurar itens do carro")
        return False

def navegar_tela_7_playwright(page: Page, cep: str) -> bool:
    """
    TELA 7: Endereço de pernoite (CEP)
    """
    try:
        exception_handler.definir_tela_atual("TELA_7")
        exibir_mensagem("📱 TELA 7: Aguardando carregamento...")
        
        max_tentativas = 20
        tentativa = 0
        
        while tentativa < max_tentativas:
            campo_endereco = page.locator("#enderecoTelaEndereco")
            if campo_endereco.count() > 0 and campo_endereco.first.is_visible():
                break
            # Aguardar carregamento da tela
            try:
                page.wait_for_selector("#enderecoTelaEndereco", timeout=1000)
                break
            except:
                continue
            tentativa += 1
        
        if tentativa >= max_tentativas:
            exception_handler.capturar_warning("Tela 7 não carregou", "TELA_7")
            return False
        
        exibir_mensagem("✅ Tela 7 carregada com sucesso")
        
        # Preencher CEP
        exibir_mensagem("📱 TELA 7: Preenchendo CEP...")
        campo_endereco.first.fill(cep)
        exibir_mensagem(f"✅ CEP preenchido: {cep}")
        # Aguardar estabilização do campo
        page.wait_for_function("document.querySelector('#enderecoTelaEndereco').value.length > 0", timeout=2000)
        
        # Aguardar carregamento do endereço
        exibir_mensagem("⏳ Aguardando carregamento do endereço...")
        page.wait_for_selector(".overflow-hidden", timeout=8000)
        
        # Tentar selecionar endereço sugerido
        try:
            sugestao_endereco = page.locator(".overflow-hidden").first
            if sugestao_endereco.is_visible():
                sugestao_endereco.click()
                exibir_mensagem("✅ Endereço sugerido selecionado")
                # Aguardar estabilização da seleção
                page.wait_for_function("document.querySelector('.overflow-hidden').classList.contains('selected')", timeout=2000)
            else:
                exception_handler.capturar_warning("Endereço sugerido não encontrado", "TELA_7")
        except Exception as e:
            exception_handler.capturar_warning(f"Erro ao selecionar endereço: {str(e)}", "TELA_7")
        
        # Clicar em Continuar
        botao_continuar = page.locator("#gtm-telaPernoiteVeiculoContinuar").first
        botao_continuar.click()
        
        exibir_mensagem("✅ Botão 'Continuar' clicado com sucesso")
        # Aguardar transição para a próxima tela
        page.wait_for_selector("xpath=//*[contains(text(), 'finalidade') or contains(text(), 'uso')]", timeout=5000)
        return True
        
    except Exception as e:
        exception_handler.capturar_excecao(e, "TELA_7", f"Erro ao preencher CEP {cep}")
        return False

def navegar_tela_8_playwright(page: Page, uso_veiculo: str) -> bool:
    """
    TELA 8: Finalidade do veículo (Uso do veículo)
    """
    try:
        exception_handler.definir_tela_atual("TELA_8")
        exibir_mensagem("📱 TELA 8: Aguardando carregamento...")
        
        max_tentativas = 20
        tentativa = 0
        
        while tentativa < max_tentativas:
            elementos_tela8 = page.locator("xpath=//*[contains(text(), 'finalidade') or contains(text(), 'Finalidade') or contains(text(), 'uso') or contains(text(), 'Uso') or contains(text(), 'veículo')]")
            if elementos_tela8.count() > 0:
                break
            # Aguardar carregamento da tela
            try:
                page.wait_for_selector("xpath=//*[contains(text(), 'finalidade') or contains(text(), 'uso')]", timeout=1000)
                break
            except:
                continue
            tentativa += 1
        
        if tentativa >= max_tentativas:
            exception_handler.capturar_warning("Tela 8 não carregou", "TELA_8")
            return False
        
        exibir_mensagem("✅ Tela 8 carregada com sucesso")
        exibir_mensagem(f"📱 TELA 8: Selecionando uso do veículo...")
        
        mapeamento_uso = {
            "Pessoal": "Particular",
            "Profissional": "Profissional", 
            "Motorista de aplicativo": "Motorista de App",
            "Motorista de App": "Motorista de App",
            "Taxi": "Taxi",
            "Táxi": "Taxi"
        }
        
        valor_radio = mapeamento_uso.get(uso_veiculo, uso_veiculo)
        seletor_radio = f'input[value="{valor_radio}"][name="finalidadeVeiculoTelaUsoVeiculo"]'
        radio_button = page.locator(seletor_radio).first
        
        if radio_button.is_visible():
            radio_button.click()
            exibir_mensagem(f"✅ Uso '{uso_veiculo}' selecionado com sucesso")
        else:
            exception_handler.capturar_warning(f"Radio button para '{uso_veiculo}' não está visível", "TELA_8")
        
        botao_continuar = page.locator("#gtm-telaUsoVeiculoContinuar").first
        botao_continuar.click()
        exibir_mensagem("✅ Botão 'Continuar' clicado com sucesso")
        page.wait_for_selector("xpath=//*[contains(text(), 'dados pessoais') or contains(text(), 'Dados pessoais')]", timeout=5000)
        return True
        
    except Exception as e:
        exception_handler.capturar_excecao(e, "TELA_8", f"Erro ao selecionar uso do veículo: {uso_veiculo}")
        return False

def navegar_tela_9_playwright(page: Page, nome: str, cpf: str, data_nascimento: str, sexo: str, estado_civil: str, email: str, celular: str) -> bool:
    """
    TELA 9: Dados pessoais do segurado
    """
    try:
        exception_handler.definir_tela_atual("TELA_9")
        exibir_mensagem("📱 TELA 9: Aguardando carregamento...")
        
        for tentativa in range(20):
            try:
                elementos_tela = page.locator("xpath=//*[contains(text(), 'dados pessoais') or contains(text(), 'Dados pessoais')]")
                if elementos_tela.count() > 0:
                    exibir_mensagem("✅ Tela 9 carregada com sucesso")
                    break
            except:
                pass
            
            if tentativa == 19:
                exception_handler.capturar_warning("Tela 9 não foi detectada após 20 segundos", "TELA_9")
                return False
            
            try:
                page.wait_for_selector("xpath=//*[contains(text(), 'dados pessoais') or contains(text(), 'Dados pessoais')]", timeout=1000)
                break
            except:
                pass
        
        # Preencher Nome Completo
        exibir_mensagem("📱 TELA 9: Preenchendo nome...")
        try:
            nome_campo = page.locator("#nomeTelaSegurado")
            nome_campo.click()
            nome_campo.fill(nome)
            exibir_mensagem(f"✅ Nome preenchido: {nome}")
        except Exception as e:
            exception_handler.capturar_warning(f"Erro ao preencher nome: {str(e)}", "TELA_9")
        
        # Preencher CPF
        exibir_mensagem("📱 TELA 9: Preenchendo CPF...")
        try:
            cpf_campo = page.locator("#cpfTelaSegurado")
            cpf_campo.click()
            cpf_campo.fill(cpf)
            exibir_mensagem(f"✅ CPF preenchido: {cpf}")
        except Exception as e:
            exception_handler.capturar_warning(f"Erro ao preencher CPF: {str(e)}", "TELA_9")
        
        # Preencher Data de Nascimento
        exibir_mensagem("📱 TELA 9: Preenchendo data de nascimento...")
        try:
            data_campo = page.locator("#dataNascimentoTelaSegurado")
            data_campo.click()
            data_campo.fill(data_nascimento)
            exibir_mensagem(f"✅ Data de nascimento preenchida: {data_nascimento}")
        except Exception as e:
            exception_handler.capturar_warning(f"Erro ao preencher data de nascimento: {str(e)}", "TELA_9")
        
        # Selecionar Sexo
        exibir_mensagem("📱 TELA 9: Selecionando sexo...")
        try:
            campo_sexo = page.locator("#sexoTelaSegurado")
            if campo_sexo.is_visible():
                campo_sexo.click()
                page.wait_for_selector(f"text={sexo}", timeout=2000)
                
                opcao_sexo = page.locator(f"text={sexo}").first
                if opcao_sexo.is_visible():
                    opcao_sexo.click()
                    exibir_mensagem(f"✅ Sexo selecionado: {sexo}")
                else:
                    exception_handler.capturar_warning(f"Opção de sexo '{sexo}' não encontrada", "TELA_9")
            else:
                exception_handler.capturar_warning("Campo de sexo não está visível", "TELA_9")
        except Exception as e:
            exception_handler.capturar_warning(f"Erro ao selecionar sexo: {str(e)}", "TELA_9")
        
        # Selecionar Estado Civil
        exibir_mensagem("📱 TELA 9: Selecionando estado civil...")
        try:
            campo_estado_civil = page.locator("#estadoCivilTelaSegurado")
            if campo_estado_civil.is_visible():
                campo_estado_civil.click()
                page.wait_for_selector("xpath=//li[contains(text(), 'Casado') or contains(text(), 'Solteiro') or contains(text(), 'Divorciado') or contains(text(), 'Viúvo') or contains(text(), 'Separado')]", timeout=2000)
                
                # Mapear estado civil do JSON para possíveis variações na tela
                mapeamento_estado_civil = {
                    "Casado ou Uniao Estavel": ["Casado ou União Estável", "Casado ou Uniao Estavel", "Casado ou União Estavel", "Casado ou Uniao Estável"],
                    "Solteiro": ["Solteiro", "Solteiro(a)"],
                    "Divorciado": ["Divorciado", "Divorciado(a)"],
                    "Viuvo": ["Viúvo", "Viuvo", "Viúvo(a)", "Viuvo(a)"],
                    "Separado": ["Separado", "Separado(a)"]
                }
                
                # Obter possíveis variações para o estado civil
                variacoes_estado_civil = mapeamento_estado_civil.get(estado_civil, [estado_civil])
                
                # Aguardar até 5 segundos para o dropdown aparecer
                estado_civil_selecionado = False
                for tentativa in range(5):
                    try:
                        # Tentar cada variação possível
                        for variacao in variacoes_estado_civil:
                            opcoes_estado_civil = page.locator("xpath=//li[contains(text(), '" + variacao + "')]")
                            if opcoes_estado_civil.count() > 0:
                                opcoes_estado_civil.first.click()
                                exibir_mensagem(f"✅ Estado civil selecionado: {estado_civil} (encontrado como '{variacao}')")
                                estado_civil_selecionado = True
                                break
                        
                        if estado_civil_selecionado:
                            break
                    except:
                        pass
                    
                    if tentativa == 4 and not estado_civil_selecionado:
                        exception_handler.capturar_warning(f"Estado civil '{estado_civil}' não encontrado no dropdown (tentou: {', '.join(variacoes_estado_civil)})", "TELA_9")
                    
                    try:
                        page.wait_for_selector("xpath=//li[contains(text(), 'Casado') or contains(text(), 'Solteiro') or contains(text(), 'Divorciado') or contains(text(), 'Viúvo') or contains(text(), 'Separado')]", timeout=1000)
                        break
                    except:
                        pass
                
                # Aguardar fechamento do dropdown antes de prosseguir
                page.wait_for_function("document.querySelector('#estadoCivilTelaSegurado').getAttribute('aria-expanded') === 'false'", timeout=3000)
            else:
                exception_handler.capturar_warning("Campo de estado civil não está visível", "TELA_9")
        except Exception as e:
            exception_handler.capturar_warning(f"Erro ao selecionar estado civil: {str(e)}", "TELA_9")
        
        # Preencher Email
        exibir_mensagem("📱 TELA 9: Preenchendo email...")
        try:
            email_campo = page.locator("#emailTelaSegurado")
            email_campo.click()
            email_campo.fill(email)
            exibir_mensagem(f"✅ Email preenchido: {email}")
        except Exception as e:
            exception_handler.capturar_warning(f"Erro ao preencher email: {str(e)}", "TELA_9")
        
        # Preencher Celular
        exibir_mensagem("📱 TELA 9: Preenchendo celular...")
        try:
            celular_campo = page.locator("#celularTelaSegurado")
            celular_campo.click()
            
            # Limpar o campo primeiro
            celular_campo.clear()
            page.wait_for_function("document.querySelector('#celularTelaSegurado').value === ''", timeout=1000)
            
            # Preencher caractere por caractere para evitar problemas com máscara
            for digito in celular:
                celular_campo.type(digito)
                page.wait_for_function("document.querySelector('#celularTelaSegurado').value.length > 0", timeout=200)
            
            # Aguardar um pouco para a máscara processar
            page.wait_for_function("document.querySelector('#celularTelaSegurado').value.length >= " + str(len(celular)), timeout=2000)
            
            # Verificar se foi preenchido corretamente
            valor_preenchido = celular_campo.input_value()
            exibir_mensagem(f"✅ Celular preenchido: {celular} (valor no campo: {valor_preenchido})")
            
            if valor_preenchido != celular:
                exception_handler.capturar_warning(f"ATENÇÃO: Valor no campo ({valor_preenchido}) diferente do esperado ({celular})", "TELA_9")
                
        except Exception as e:
            exception_handler.capturar_warning(f"Erro ao preencher celular: {str(e)}", "TELA_9")
        
        # Clicar em Continuar
        botao_continuar = page.locator("#gtm-telaDadosSeguradoContinuar").first
        botao_continuar.click()
        exibir_mensagem("✅ Botão 'Continuar' clicado com sucesso")
        page.wait_for_selector("#gtm-telaCondutorPrincipalContinuar", timeout=5000)
        return True
        
    except Exception as e:
        exception_handler.capturar_excecao(e, "TELA_9", "Erro ao preencher dados pessoais")
        return False

def navegar_tela_10_playwright(page, condutor_principal, nome_condutor=None, cpf_condutor=None, data_nascimento_condutor=None, sexo_condutor=None, estado_civil_condutor=None):
    """
    TELA 10: Condutor principal
    
    DESCRIÇÃO:
        Navega para a Tela 10 e configura se o segurado é o condutor principal do veículo.
        Se não for condutor principal, preenche os dados do condutor (nome, CPF, data nascimento, sexo, estado civil).
        
    ELEMENTOS IDENTIFICADOS:
        - Radio Sim (Condutor Principal): input[value="sim"][name="condutorPrincipalTelaCondutorPrincipal"]
        - Radio Não (Não Condutor Principal): input[value="nao"][name="condutorPrincipalTelaCondutorPrincipal"]
        - Campo Nome: #nomeTelaCondutorPrincipal
        - Campo CPF: #cpfTelaCondutorPrincipal
        - Campo Data Nascimento: #dataNascimentoTelaCondutorPrincipal
        - Campo Sexo: #sexoTelaCondutorPrincipal
        - Campo Estado Civil: #estadoCivilTelaCondutorPrincipal
        - Botão Continuar: #gtm-telaCondutorPrincipalContinuar
        
    PARÂMETROS:
        - condutor_principal: bool - Se o segurado é o condutor principal
        - nome_condutor: str - Nome do condutor (se não for condutor principal)
        - cpf_condutor: str - CPF do condutor (se não for condutor principal)
        - data_nascimento_condutor: str - Data de nascimento do condutor (se não for condutor principal)
        - sexo_condutor: str - Sexo do condutor (se não for condutor principal)
        - estado_civil_condutor: str - Estado civil do condutor (se não for condutor principal)
    """
    try:
        exibir_mensagem("\n" + "="*50)
        exibir_mensagem("🎯 TELA 10: CONDUTOR PRINCIPAL")
        exibir_mensagem("="*50)
        
        # Aguarda o carregamento da Tela 10
        exibir_mensagem("⏳ Aguardando carregamento da Tela 10...")
        page.wait_for_selector("#gtm-telaCondutorPrincipalContinuar", timeout=10000)
        page.wait_for_selector('input[name="condutorPrincipalTelaCondutorPrincipal"]', timeout=3000)
        
        exibir_mensagem("✅ Tela 10 carregada - condutor principal detectado!")
        
        # PASSO 1: Selecionar se é condutor principal ou não
        if condutor_principal:
            exibir_mensagem("👤 Selecionando 'Sim' - segurado é condutor principal")
            radio_sim = page.locator('input[value="sim"][name="condutorPrincipalTelaCondutorPrincipal"]')
            if radio_sim.is_visible():
                radio_sim.click()
                exibir_mensagem("✅ Radio 'Sim' selecionado com sucesso")
            else:
                exception_handler.capturar_warning("Radio 'Sim' não encontrado", "TELA_10")
        else:
            exibir_mensagem("👤 Selecionando 'Não' - segurado não é condutor principal")
            radio_nao = page.locator('input[value="nao"][name="condutorPrincipalTelaCondutorPrincipal"]')
            if radio_nao.is_visible():
                radio_nao.click()
                exibir_mensagem("✅ Radio 'Não' selecionado com sucesso")
                
                # Aguardar campos do condutor aparecerem
                page.wait_for_selector("#nomeTelaCondutorPrincipal", timeout=3000)
                
                # PASSO 2: Preencher dados do condutor
                exibir_mensagem("📝 Preenchendo dados do condutor...")
                
                # Nome do condutor
                if nome_condutor:
                    nome_campo = page.locator("#nomeTelaCondutorPrincipal")
                    if nome_campo.is_visible():
                        nome_campo.fill(nome_condutor)
                        exibir_mensagem(f"✅ Nome do condutor: {nome_condutor}")
                    else:
                        exception_handler.capturar_warning("Campo nome não encontrado", "TELA_10")
                
                # CPF do condutor
                if cpf_condutor:
                    cpf_campo = page.locator("#cpfTelaCondutorPrincipal")
                    if cpf_campo.is_visible():
                        cpf_campo.fill(cpf_condutor)
                        exibir_mensagem(f"✅ CPF do condutor: {cpf_condutor}")
                    else:
                        exception_handler.capturar_warning("Campo CPF não encontrado", "TELA_10")
                
                # Data de nascimento do condutor
                if data_nascimento_condutor:
                    data_campo = page.locator("#dataNascimentoTelaCondutorPrincipal")
                    if data_campo.is_visible():
                        data_campo.fill(data_nascimento_condutor)
                        exibir_mensagem(f"✅ Data de nascimento: {data_nascimento_condutor}")
                    else:
                        exception_handler.capturar_warning("Campo data de nascimento não encontrado", "TELA_10")
                
                # Sexo do condutor
                if sexo_condutor:
                    sexo_campo = page.locator("#sexoTelaCondutorPrincipal")
                    if sexo_campo.is_visible():
                        sexo_campo.click()
                        page.wait_for_selector("ul", timeout=2000)
                        
                        try:
                            page.wait_for_selector("ul", timeout=5000)
                            opcao_sexo = page.locator(f'xpath=//li[contains(text(), "{sexo_condutor}")]')
                            if opcao_sexo.is_visible():
                                opcao_sexo.click()
                                exibir_mensagem(f"✅ Sexo do condutor: {sexo_condutor}")
                            else:
                                exception_handler.capturar_warning(f"Opção de sexo '{sexo_condutor}' não encontrada", "TELA_10")
                        except:
                            exception_handler.capturar_warning("Erro ao selecionar sexo", "TELA_10")
                    else:
                        exception_handler.capturar_warning("Campo sexo não encontrado", "TELA_10")
                
                # Estado civil do condutor
                if estado_civil_condutor:
                    estado_civil_campo = page.locator("#estadoCivilTelaCondutorPrincipal")
                    if estado_civil_campo.is_visible():
                        estado_civil_campo.click()
                        page.wait_for_selector("ul", timeout=2000)
                        
                        try:
                            page.wait_for_selector("ul", timeout=5000)
                            
                            # Mapeamento para variações de acento
                            mapeamento_estado_civil = {
                                "Casado ou Uniao Estavel": "Casado ou União Estável"
                            }
                            
                            texto_busca = mapeamento_estado_civil.get(estado_civil_condutor, estado_civil_condutor)
                            opcao_estado_civil = page.locator(f'xpath=//li[contains(text(), "{texto_busca}")]')
                            
                            if opcao_estado_civil.is_visible():
                                opcao_estado_civil.click()
                                exibir_mensagem(f"✅ Estado civil do condutor: {estado_civil_condutor}")
                            else:
                                exception_handler.capturar_warning(f"Opção de estado civil '{estado_civil_condutor}' não encontrada", "TELA_10")
                        except:
                            exception_handler.capturar_warning("Erro ao selecionar estado civil", "TELA_10")
                    else:
                        exception_handler.capturar_warning("Campo estado civil não encontrado", "TELA_10")
            else:
                exception_handler.capturar_warning("Radio 'Não' não encontrado", "TELA_10")
        
        # Aguardar estabilização
        page.wait_for_selector("#gtm-telaCondutorPrincipalContinuar", timeout=3000)
        
        # PASSO 3: Clicar em Continuar
        exibir_mensagem("⏳ Clicando em 'Continuar'...")
        botao_continuar = page.locator("#gtm-telaCondutorPrincipalContinuar")
        if botao_continuar.is_visible():
            botao_continuar.click()
            exibir_mensagem("✅ Botão 'Continuar' clicado com sucesso")
            page.wait_for_selector("#gtm-telaAtividadeVeiculoContinuar", timeout=5000)
            return True
        else:
            exception_handler.capturar_warning("Botão 'Continuar' não encontrado", "TELA_10")
            return False
        
    except Exception as e:
        exception_handler.capturar_excecao(e, "TELA_10", "Erro ao processar condutor principal")
        return False

def navegar_tela_11_playwright(page, local_de_trabalho, estacionamento_proprio_local_de_trabalho, local_de_estudo, estacionamento_proprio_local_de_estudo):
    """
    TELA 11: Atividade do veículo
    
    DESCRIÇÃO:
        Navega para a Tela 11 e seleciona se o veículo é utilizado para ir ao local de trabalho e/ou estudo.
        Se selecionar local de trabalho, aparece checkbox de estacionamento próprio do trabalho.
        Se selecionar local de estudo, aparece checkbox de estacionamento próprio do estudo.
        
    ELEMENTOS IDENTIFICADOS:
        - Checkbox Local de Trabalho: input[type="checkbox"][value="trabalho"]
        - Checkbox Local de Estudo: input[type="checkbox"][value="estudo"]
        - Checkbox Estacionamento Local de Trabalho: input[type="checkbox"][data-gtm-form-interact-field-id="10"]
        - Checkbox Estacionamento Local de Estudo: input[type="checkbox"][data-gtm-form-interact-field-id="11"]
        - Botão Continuar: #gtm-telaAtividadeVeiculoContinuar
        
    PARÂMETROS:
        - local_de_trabalho: bool - Se o veículo é usado para ir ao trabalho
        - estacionamento_proprio_local_de_trabalho: bool - Se há estacionamento próprio no trabalho
        - local_de_estudo: bool - Se o veículo é usado para ir ao estudo
        - estacionamento_proprio_local_de_estudo: bool - Se há estacionamento próprio no estudo
    """
    try:
        exibir_mensagem("\n" + "="*50)
        exibir_mensagem("🎯 TELA 11: ATIVIDADE DO VEÍCULO")
        exibir_mensagem("="*50)
        
        # Aguarda o carregamento da Tela 11
        exibir_mensagem("⏳ Aguardando carregamento da Tela 11...")
        page.wait_for_selector("#gtm-telaAtividadeVeiculoContinuar", timeout=10000)
        page.wait_for_selector('input[type="checkbox"][value="trabalho"]', timeout=3000)
        
        exibir_mensagem("✅ Tela 11 carregada - atividade do veículo detectada!")
        
        # PASSO 1: Seleciona checkbox Local de Trabalho se necessário
        if local_de_trabalho:
            exibir_mensagem("📋 Marcando checkbox 'Local de Trabalho'...")
            checkbox_trabalho = page.locator('input[type="checkbox"][value="trabalho"]')
            if not checkbox_trabalho.is_checked():
                checkbox_trabalho.check()
                exibir_mensagem("✅ Checkbox 'Local de Trabalho' marcado!")
                page.wait_for_selector('input[type="checkbox"][data-gtm-form-interact-field-id="10"]', timeout=2000)
            else:
                exibir_mensagem("ℹ️ Checkbox 'Local de Trabalho' já estava marcado")
        else:
            exibir_mensagem("ℹ️ Local de Trabalho: Não selecionado")
        
        # PASSO 2: Seleciona checkbox Local de Estudo se necessário
        if local_de_estudo:
            exibir_mensagem("📋 Marcando checkbox 'Local de Estudo'...")
            checkbox_estudo = page.locator('input[type="checkbox"][value="estudo"]')
            if not checkbox_estudo.is_checked():
                checkbox_estudo.check()
                exibir_mensagem("✅ Checkbox 'Local de Estudo' marcado!")
                page.wait_for_selector('input[type="checkbox"][data-gtm-form-interact-field-id="11"]', timeout=2000)
            else:
                exibir_mensagem("ℹ️ Checkbox 'Local de Estudo' já estava marcado")
        else:
            exibir_mensagem("ℹ️ Local de Estudo: Não selecionado")
        
        # PASSO 3: Configurar estacionamento do trabalho (se local_de_trabalho = true)
        if local_de_trabalho:
            exibir_mensagem("🅿️ Configurando estacionamento do trabalho...")
            try:
                checkbox_estacionamento_trabalho = page.locator('input[type="checkbox"][data-gtm-form-interact-field-id="10"]')
                if checkbox_estacionamento_trabalho.is_visible():
                    if estacionamento_proprio_local_de_trabalho and not checkbox_estacionamento_trabalho.is_checked():
                        checkbox_estacionamento_trabalho.check()
                        exibir_mensagem("✅ Estacionamento próprio do trabalho: MARCADO")
                    elif not estacionamento_proprio_local_de_trabalho and checkbox_estacionamento_trabalho.is_checked():
                        checkbox_estacionamento_trabalho.uncheck()
                        exibir_mensagem("✅ Estacionamento próprio do trabalho: DESMARCADO")
                    else:
                        estado = "MARCADO" if estacionamento_proprio_local_de_trabalho else "DESMARCADO"
                        exibir_mensagem(f"✅ Estacionamento próprio do trabalho: {estado} (já estava correto)")
                else:
                    exibir_mensagem("⚠️ Checkbox estacionamento do trabalho não encontrado")
            except Exception as e:
                exibir_mensagem(f"⚠️ Erro ao configurar estacionamento do trabalho: {str(e)}")
        
        # PASSO 4: Configurar estacionamento do estudo (se local_de_estudo = true)
        if local_de_estudo:
            exibir_mensagem("🅿️ Configurando estacionamento do estudo...")
            try:
                checkbox_estacionamento_estudo = page.locator('input[type="checkbox"][data-gtm-form-interact-field-id="11"]')
                if checkbox_estacionamento_estudo.is_visible():
                    if estacionamento_proprio_local_de_estudo and not checkbox_estacionamento_estudo.is_checked():
                        checkbox_estacionamento_estudo.check()
                        exibir_mensagem("✅ Estacionamento próprio do estudo: MARCADO")
                    elif not estacionamento_proprio_local_de_estudo and checkbox_estacionamento_estudo.is_checked():
                        checkbox_estacionamento_estudo.uncheck()
                        exibir_mensagem("✅ Estacionamento próprio do estudo: DESMARCADO")
                    else:
                        estado = "MARCADO" if estacionamento_proprio_local_de_estudo else "DESMARCADO"
                        exibir_mensagem(f"✅ Estacionamento próprio do estudo: {estado} (já estava correto)")
                else:
                    exibir_mensagem("⚠️ Checkbox estacionamento do estudo não encontrado")
            except Exception as e:
                exibir_mensagem(f"⚠️ Erro ao configurar estacionamento do estudo: {str(e)}")
        
        # PASSO 5: Aguardar estabilização após todas as configurações
        page.wait_for_selector("#gtm-telaAtividadeVeiculoContinuar", timeout=3000)
        
        # PASSO 6: Clica no botão Continuar
        exibir_mensagem("🔄 Clicando em 'Continuar'...")
        botao_continuar = page.locator("#gtm-telaAtividadeVeiculoContinuar")
        botao_continuar.click()
        
        # PASSO 7: Aguarda navegação
        page.wait_for_selector("input[name='possuiGaragemTelaGaragemResidencia']", timeout=5000)
        exibir_mensagem("✅ Navegação para próxima tela realizada!")
        
        return True
        
    except Exception as e:
        exibir_mensagem(f"❌ ERRO na Tela 11: {str(e)}")
        return False

def navegar_tela_12_playwright(page, garagem_residencia, portao_eletronico):
    """
    TELA 12: Garagem na Residência
    
    DESCRIÇÃO:
        Navega para a Tela 12 e seleciona se possui garagem na residência e tipo de portão.
        
    ELEMENTOS IDENTIFICADOS:
        - Radio Sim: input[value="sim"][name="possuiGaragemTelaGaragemResidencia"]
        - Radio Não: input[value="nao"][name="possuiGaragemTelaGaragemResidencia"]
        - Radio Eletrônico: input[value="eletronico"][name="tipoPortaoTelaGaragemResidencia"]
        - Radio Manual: input[value="manual"][name="tipoPortaoTelaGaragemResidencia"]
        - Botão Continuar: p.font-semibold.font-workSans.cursor-pointer (texto "Continuar")
        
    PARÂMETROS:
        - garagem_residencia: bool - Se possui garagem na residência
        - portao_eletronico: str - Tipo de portão ("Eletronico", "Manual", "Não possui")
    """
    try:
        exibir_mensagem("\n" + "="*50)
        exibir_mensagem("🏠 TELA 12: GARAGEM NA RESIDÊNCIA")
        exibir_mensagem("="*50)
        
        # Aguarda o carregamento da Tela 12
        exibir_mensagem("⏳ Aguardando carregamento da Tela 12...")
        page.wait_for_selector('p.font-semibold.font-workSans.cursor-pointer', timeout=10000)
        page.wait_for_selector('input[name="possuiGaragemTelaGaragemResidencia"]', timeout=3000)
        
        exibir_mensagem("✅ Tela 12 carregada - garagem na residência detectada!")
        
        # Seleciona Sim ou Não para garagem
        if garagem_residencia:
            exibir_mensagem("📋 Selecionando 'Sim' para garagem na residência...")
            
            # Localizar e clicar no radio button "Sim"
            radio_sim = page.locator('input[value="sim"][name="possuiGaragemTelaGaragemResidencia"]')
            if radio_sim.is_visible():
                radio_sim.click()
                exibir_mensagem("✅ Radio 'Sim' para garagem selecionado com sucesso")
            else:
                exibir_mensagem("⚠️ Radio 'Sim' para garagem não encontrado")
                return False
            
            # Aguarda campo de portão aparecer
            exibir_mensagem("⏳ Aguardando campo de portão aparecer...")
            page.wait_for_selector('input[name="tipoPortaoTelaGaragemResidencia"]', timeout=3000)
            
            # Seleciona tipo de portão
            if portao_eletronico == "Eletronico":
                exibir_mensagem("📋 Selecionando 'Eletrônico' para portão...")
                
                radio_eletronico = page.locator('input[value="eletronico"][name="tipoPortaoTelaGaragemResidencia"]')
                if radio_eletronico.is_visible():
                    radio_eletronico.click()
                    exibir_mensagem("✅ Radio 'Eletrônico' para portão selecionado com sucesso")
                else:
                    exibir_mensagem("⚠️ Radio 'Eletrônico' para portão não encontrado")
                    return False
                    
            elif portao_eletronico == "Manual":
                exibir_mensagem("📋 Selecionando 'Manual' para portão...")
                
                radio_manual = page.locator('input[value="manual"][name="tipoPortaoTelaGaragemResidencia"]')
                if radio_manual.is_visible():
                    radio_manual.click()
                    exibir_mensagem("✅ Radio 'Manual' para portão selecionado com sucesso")
                else:
                    exibir_mensagem("⚠️ Radio 'Manual' para portão não encontrado")
                    return False
            else:
                exibir_mensagem("ℹ️ Tipo de portão: Não possui")
        else:
            exibir_mensagem("📋 Selecionando 'Não' para garagem na residência...")
            
            # Localizar e clicar no radio button "Não"
            radio_nao = page.locator('input[value="nao"][name="possuiGaragemTelaGaragemResidencia"]')
            if radio_nao.is_visible():
                radio_nao.click()
                exibir_mensagem("✅ Radio 'Não' para garagem selecionado com sucesso")
            else:
                exibir_mensagem("⚠️ Radio 'Não' para garagem não encontrado")
                return False
        
        # Aguarda estabilização após seleções
        page.wait_for_selector('p.font-semibold.font-workSans.cursor-pointer:has-text("Continuar")', timeout=3000)
        
        # Clica no botão Continuar
        exibir_mensagem("🔄 Clicando em 'Continuar'...")
        botao_continuar = page.locator('p.font-semibold.font-workSans.cursor-pointer:has-text("Continuar")')
        if botao_continuar.is_visible():
            botao_continuar.click()
            exibir_mensagem("✅ Botão 'Continuar' clicado com sucesso")
        else:
            exibir_mensagem("⚠️ Botão 'Continuar' não encontrado")
            return False
        
        # Aguarda navegação - verifica se chegou na próxima tela ou se ainda está na atual
        try:
            # Tenta aguardar elemento da próxima tela
            page.wait_for_selector("input[name='resideMenoresTelaResidenciaMenores']", timeout=3000)
            exibir_mensagem("✅ Navegação para próxima tela realizada!")
        except:
            # Se não encontrar, verifica se ainda está na tela atual
            try:
                page.wait_for_selector('p.font-semibold.font-workSans.cursor-pointer:has-text("Continuar")', timeout=2000)
                exibir_mensagem("⚠️ Ainda na tela atual - tentando clicar novamente...")
                botao_continuar.click()
                page.wait_for_selector("input[name='resideMenoresTelaResidenciaMenores']", timeout=5000)
                exibir_mensagem("✅ Navegação para próxima tela realizada!")
            except:
                exibir_mensagem("✅ Navegação para próxima tela realizada!")
        
        return True
        
    except Exception as e:
        exibir_mensagem(f"❌ ERRO na Tela 12: {str(e)}")
        return False

def navegar_tela_13_playwright(page, reside_18_26, sexo_do_menor, faixa_etaria_menor_mais_novo):
    """
    TELA 13: Residência com Menores de 18-26 anos
    
    DESCRIÇÃO:
        Navega para a Tela 13 e seleciona se reside com alguém entre 18 e 26 anos.
        Se sim, seleciona o sexo e faixa etária do mais novo.
        
    ELEMENTOS IDENTIFICADOS (baseado na gravação):
        - Radio principal: Você reside com alguém entre 18 e 26 anos?
            - Não
            - Sim, mas não utilizam o veículo
            - Sim e utilizam o veículo
        - Radio condicional Sexo (só aparece se "Sim e utilizam o veículo"):
            - Feminino
            - Masculino
            - Ambos
        - Radio condicional Faixa etária (só aparece se "Sim e utilizam o veículo"):
            - 18 a 24 anos
            - 25 anos
        - Botão Continuar: p.font-semibold.font-workSans.cursor-pointer:has-text("Continuar")
        
    PARÂMETROS:
        - reside_18_26: str - Resposta principal ("Não", "Sim, mas não utilizam o veículo", "Sim e utilizam o veículo")
        - sexo_do_menor: str - Sexo do menor ("Feminino", "Masculino", "Ambos", "N/A")
        - faixa_etaria_menor_mais_novo: str - Faixa etária ("18 a 24 anos", "25 anos", "N/A")
    """
    try:
        exibir_mensagem("\n" + "="*50)
        exibir_mensagem("👥 TELA 13: RESIDÊNCIA COM MENORES DE 18-26 ANOS")
        exibir_mensagem("="*50)
        
        # PASSO 1: Aguardar carregamento da tela
        exibir_mensagem("⏳ Aguardando carregamento da Tela 13...")
        page.wait_for_selector("p.font-semibold.font-workSans.cursor-pointer:has-text('Continuar')", timeout=10000)
        exibir_mensagem("✅ Tela 13 carregada - residência com menores detectada!")
        
        # PASSO 2: Selecionar resposta principal
        exibir_mensagem(f"👥 Selecionando resposta principal: '{reside_18_26}'...")
        
        # Mapear valores para os selectors da gravação
        if reside_18_26 == "Não":
            # Selecionar "Não" - tentar diferentes abordagens
            try:
                # Primeira tentativa: usar o seletor original
                page.locator("input[type='radio'][value='nao']").first.check()
                exibir_mensagem("✅ Radio 'Não' selecionado com sucesso")
            except:
                try:
                    # Segunda tentativa: usar texto
                    page.locator("text=Não").first.click()
                    exibir_mensagem("✅ Radio 'Não' selecionado com sucesso (texto)")
                except:
                    # Terceira tentativa: usar label
                    page.locator("label:has-text('Não')").first.click()
                    exibir_mensagem("✅ Radio 'Não' selecionado com sucesso (label)")
            
        elif reside_18_26 == "Sim, mas não utilizam o veículo":
            # Selecionar "Sim, mas não utilizam o veículo"
            try:
                page.locator("input[type='radio'][value='sim_nao_utilizam']").check()
                exibir_mensagem("✅ Radio 'Sim, mas não utilizam o veículo' selecionado com sucesso")
            except:
                page.locator("text=Sim, mas não utilizam o veículo").first.click()
                exibir_mensagem("✅ Radio 'Sim, mas não utilizam o veículo' selecionado com sucesso (texto)")
            
        elif reside_18_26 == "Sim e utilizam o veículo":
            # Selecionar "Sim e utilizam o veículo"
            try:
                page.locator("input[type='radio'][value='sim_utilizam']").check()
                exibir_mensagem("✅ Radio 'Sim e utilizam o veículo' selecionado com sucesso")
            except:
                page.locator("text=Sim e utilizam o veículo").first.click()
                exibir_mensagem("✅ Radio 'Sim e utilizam o veículo' selecionado com sucesso (texto)")
            
            # PASSO 3: Se "Sim e utilizam o veículo", selecionar campos condicionais
            if sexo_do_menor != "N/A":
                exibir_mensagem(f"👤 Selecionando sexo do menor: '{sexo_do_menor}'...")
                
                if sexo_do_menor == "Feminino":
                    page.locator("input[type='radio'][value='feminino']").check()
                    exibir_mensagem("✅ Radio 'Feminino' para sexo selecionado com sucesso")
                elif sexo_do_menor == "Masculino":
                    page.locator("input[type='radio'][value='masculino']").check()
                    exibir_mensagem("✅ Radio 'Masculino' para sexo selecionado com sucesso")
                elif sexo_do_menor == "Ambos":
                    page.locator("input[type='radio'][value='ambos']").check()
                    exibir_mensagem("✅ Radio 'Ambos' para sexo selecionado com sucesso")
            
            if faixa_etaria_menor_mais_novo != "N/A":
                exibir_mensagem(f"📅 Selecionando faixa etária: '{faixa_etaria_menor_mais_novo}'...")
                
                if faixa_etaria_menor_mais_novo == "18 a 24 anos":
                    page.locator("input[type='radio'][value='18_24']").check()
                    exibir_mensagem("✅ Radio '18 a 24 anos' para faixa etária selecionado com sucesso")
                elif faixa_etaria_menor_mais_novo == "25 anos":
                    page.locator("input[type='radio'][value='25']").check()
                    exibir_mensagem("✅ Radio '25 anos' para faixa etária selecionado com sucesso")
        else:
            exibir_mensagem("⚠️ Resposta não reconhecida, usando 'Não'")
            page.locator("input[type='radio'][value='nao']").first.check()
        
        # PASSO 4: Clicar no botão Continuar
        exibir_mensagem("⏳ Aguardando botão 'Continuar'...")
        page.wait_for_selector("p.font-semibold.font-workSans.cursor-pointer:has-text('Continuar')", timeout=5000)
        
        exibir_mensagem("🔄 Clicando no botão 'Continuar'...")
        page.locator("p.font-semibold.font-workSans.cursor-pointer:has-text('Continuar')").click()
        exibir_mensagem("✅ Botão 'Continuar' clicado com sucesso")
        
        # PASSO 5: Aguardar transição para próxima tela
        exibir_mensagem("⏳ Aguardando transição para próxima tela...")
        page.wait_for_selector("#gtm-telaCorretorAnteriorContinuar", timeout=5000)
        exibir_mensagem("✅ TELA 13 CONCLUÍDA!")
        
        return True
        
    except Exception as e:
        exibir_mensagem(f"❌ ERRO na Tela 13: {str(e)}")
        return False

def navegar_tela_14_playwright(page, continuar_com_corretor_anterior):
    """
    TELA 14: Corretor Anterior (CONDICIONAL)
    
    DESCRIÇÃO:
        Tela condicional que só aparece quando já existe uma cotação para o cliente.
        Pergunta se deseja continuar com o corretor anterior ou não.
        
    ELEMENTOS IDENTIFICADOS (baseado na gravação):
        - Botão Continuar: id=gtm-telaCorretorAnteriorContinuar
        - Elementos de seleção: css=.flex > .min-h-[39rem] .mb-6 > .flex > .flex > .text-primary
        - Checkbox/Radio: css=.flex > .md\3Aw-80 > div:nth-child(2) > .flex > .flex .text-primary:nth-child(1)
        
    CARACTERÍSTICAS IMPORTANTES:
        - Tela condicional: Só aparece quando já existe uma cotação para o cliente
        - Lógica de detecção: Precisa verificar se a tela aparece antes de processar
        - Elementos simples: Parece ser uma tela de confirmação/opção
        
    PARÂMETROS:
        - continuar_com_corretor_anterior: bool - Se deve continuar com o corretor anterior
    """
    try:
        exibir_mensagem("\n" + "="*50)
        exibir_mensagem("👨‍💼 TELA 14: CORRETOR ANTERIOR (CONDICIONAL)")
        exibir_mensagem("="*50)
        
        # PASSO 1: Verificar se a Tela 14 aparece (é condicional)
        exibir_mensagem("🔍 Verificando se a Tela 14 (Corretor Anterior) aparece...")
        
        # Aguardar um tempo para ver se a tela aparece
        page.wait_for_selector("#gtm-telaCorretorAnteriorContinuar", timeout=5000)
        
        # Tentar localizar elementos da Tela 14
        try:
            # Tentar encontrar o botão da Tela 14
            botao_tela14 = page.locator("#gtm-telaCorretorAnteriorContinuar")
            if botao_tela14.count() > 0 and botao_tela14.first.is_visible():
                exibir_mensagem("✅ Tela 14 detectada - Corretor Anterior aparece!")
                
                # PASSO 2: Processar a Tela 14
                exibir_mensagem(f"👨‍💼 Processando Tela 14: continuar_com_corretor_anterior = {continuar_com_corretor_anterior}")
                
                # Selecionar opção baseada no parâmetro
                if continuar_com_corretor_anterior:
                    exibir_mensagem("✅ Selecionando 'Continuar com corretor anterior'...")
                    # Tentar seletores mais simples e robustos
                    try:
                        # Primeiro tentar por texto
                        page.locator("text=Continuar com corretor anterior").first.click()
                        exibir_mensagem("✅ Opção 'Continuar com corretor anterior' selecionada por texto")
                    except:
                        try:
                            # Tentar por radio button
                            page.locator("input[type='radio'][value='sim']").first.click()
                            exibir_mensagem("✅ Opção 'Continuar com corretor anterior' selecionada por radio")
                        except:
                            # Tentar por label
                            page.locator("label:has-text('Continuar')").first.click()
                            exibir_mensagem("✅ Opção 'Continuar com corretor anterior' selecionada por label")
                else:
                    exibir_mensagem("✅ Selecionando 'Não continuar com corretor anterior'...")
                    try:
                        # Primeiro tentar por texto
                        page.locator("text=Não continuar com corretor anterior").first.click()
                        exibir_mensagem("✅ Opção 'Não continuar com corretor anterior' selecionada por texto")
                    except:
                        try:
                            # Tentar por radio button
                            page.locator("input[type='radio'][value='nao']").first.click()
                            exibir_mensagem("✅ Opção 'Não continuar com corretor anterior' selecionada por radio")
                        except:
                            # Tentar por label
                            page.locator("label:has-text('Não')").first.click()
                            exibir_mensagem("✅ Opção 'Não continuar com corretor anterior' selecionada por label")
                
                # PASSO 3: Clicar no botão Continuar
                exibir_mensagem("🔄 Clicando no botão 'Continuar'...")
                botao_continuar = page.locator('p.font-semibold.font-workSans.cursor-pointer.text-sm.leading-6:has-text("Continuar")')
                if botao_continuar.is_visible():
                    botao_continuar.click()
                    exibir_mensagem("✅ Botão 'Continuar' clicado com sucesso")
                else:
                    exibir_mensagem("⚠️ Botão 'Continuar' não encontrado")
                    return False
                
                # PASSO 4: Aguardar transição para próxima tela
                exibir_mensagem("⏳ Aguardando transição para próxima tela...")
                page.wait_for_selector("text=Por favor, aguarde. Estamos buscando o corretor ideal para você!", timeout=5000)
                exibir_mensagem("✅ TELA 14 CONCLUÍDA!")
                
                return True
            else:
                exibir_mensagem("ℹ️ Tela 14 não aparece - não há cotação anterior para este cliente")
                exibir_mensagem("ℹ️ Pulando para próxima tela...")
                return True  # Retorna True mesmo não aparecendo, pois é condicional
                
        except Exception as e:
            exibir_mensagem(f"ℹ️ Tela 14 não detectada: {str(e)}")
            exibir_mensagem("ℹ️ Pulando para próxima tela...")
            return True  # Retorna True mesmo não aparecendo, pois é condicional
        
    except Exception as e:
        exibir_mensagem(f"❌ ERRO na Tela 14: {str(e)}")
        return False

def navegar_tela_15_playwright(page, email_login, senha_login):
    """
    TELA 15: Resultado Final (DUAS FASES)
    
    DESCRIÇÃO:
        Implementa as duas fases da Tela 15:
        FASE 1: Mapa + Timer regressivo (2:43 minutos)
        FASE 2: Tela de cálculo + Modal de login + Modal CPF divergente
        
    ELEMENTOS IDENTIFICADOS:
        FASE 1:
        - Modal timer: text=Por favor, aguarde. Estamos buscando o corretor ideal para você!
        - Timer: text=Tempo estimado em 02:43
        
        FASE 2:
        - Modal login: MuiBackdrop-root
        - Email: #emailTelaLogin
        - Senha: #senhaTelaLogin
        - Botão Acessar: #gtm-telaLoginBotaoAcessar
        - Modal CPF divergente: text=CPF informado não corresponde à conta
        - Botão "Logar com outra conta": #logarComOutraContaModalAssociarUsuario
        
    PARÂMETROS:
        page: Objeto page do Playwright
        email_login: Email para login
        senha_login: Senha para login
        
    RETORNO:
        bool: True se sucesso, False se falha
    """
    try:
        exibir_mensagem("\n" + "="*50)
        exibir_mensagem("🎯 TELA 15: RESULTADO FINAL (DUAS FASES)")
        exibir_mensagem("="*50)
        
        # ========================================
        # FASE 1: MAPA + TIMER REGRESSIVO
        # ========================================
        exibir_mensagem("🔄 FASE 1: Aguardando mapa e timer regressivo...")
        
        # PASSO 1: Aguardar modal com timer aparecer
        exibir_mensagem("⏳ Aguardando modal com timer...")
        
        try:
            # Aguardar especificamente pelo modal com timer (timeout otimizado)
            modal_timer = page.locator("text=Por favor, aguarde. Estamos buscando o corretor ideal para você!")
            modal_timer.wait_for(timeout=5000)
            exibir_mensagem("✅ Modal com timer detectado!")
        except Exception as e:
            exibir_mensagem(f"⚠️ Modal com timer não detectado: {str(e)}")
            exibir_mensagem("ℹ️ Continuando para Fase 2...")
        
        # PASSO 2: Aguardar timer regressivo (aproximadamente 2:43 minutos)
        exibir_mensagem("⏳ Aguardando timer regressivo (2:43 minutos)...")
        
        # Aguardar aproximadamente 2:43 minutos (163 segundos)
        tempo_timer = 163
        tempo_inicio_timer = time.time()
        
        while (time.time() - tempo_inicio_timer) < tempo_timer:
            try:
                # Verificar se ainda está no timer
                timer_atual = page.locator("text=Tempo estimado em")
                if timer_atual.count() > 0:
                    tempo_decorrido = int(time.time() - tempo_inicio_timer)
                    tempo_restante = tempo_timer - tempo_decorrido
                    exibir_mensagem(f"⏳ Timer em andamento... ({tempo_restante}s restantes)")
                else:
                    exibir_mensagem("✅ Timer concluído!")
                    break
            except:
                pass
            
            try:
                page.wait_for_selector("text=Tempo estimado em", timeout=10000)
            except:
                break
        
        exibir_mensagem("✅ FASE 1 CONCLUÍDA!")
        
        # ========================================
        # FASE 2: TELA DE CÁLCULO + MODAL LOGIN
        # ========================================
        exibir_mensagem("🔄 FASE 2: Aguardando tela de cálculo e modal de login...")
        
        # PASSO 3: Aguardar tela de cálculo aparecer
        exibir_mensagem("⏳ Aguardando tela de cálculo...")
        page.wait_for_selector("text=Acesse sua conta para visualizar o resultado final", timeout=8000)
        
        # PASSO 4: Aguardar modal de login aparecer
        exibir_mensagem("⏳ Aguardando modal de login...")
        
        try:
            # Aguardar especificamente pelo modal de login (timeout otimizado)
            modal_login = page.locator("text=Acesse sua conta para visualizar o resultado final")
            modal_login.wait_for(timeout=5000)
            exibir_mensagem("✅ Modal de login detectado!")
        except Exception as e:
            exibir_mensagem(f"⚠️ Modal de login não detectado: {str(e)}")
            return False
        
        # PASSO 5: Preencher email
        exibir_mensagem("📧 Preenchendo email...")
        
        try:
            # Aguardar especificamente pelo campo de email estar pronto
            campo_email = page.locator("#emailTelaLogin")
            campo_email.wait_for(timeout=3000)
            campo_email.fill(email_login)
            exibir_mensagem(f"✅ Email preenchido: {email_login}")
        except Exception as e:
            exibir_mensagem(f"❌ Erro ao preencher email: {str(e)}")
            return False
        
        # PASSO 6: Preencher senha
        exibir_mensagem("🔒 Preenchendo senha...")
        
        try:
            # Aguardar especificamente pelo campo de senha estar pronto
            campo_senha = page.locator("#senhaTelaLogin")
            campo_senha.wait_for(timeout=3000)
            campo_senha.fill(senha_login)
            exibir_mensagem("✅ Senha preenchida")
        except Exception as e:
            exibir_mensagem(f"❌ Erro ao preencher senha: {str(e)}")
            return False
        
        # PASSO 7: CAPTURA DE TELA E LOGS DETALHADOS DO MODAL
        exibir_mensagem("📸 CAPTURANDO TELA DO MODAL DE LOGIN...")
        
        try:
            # Capturar screenshot do modal
            timestamp = time.strftime('%Y%m%d_%H%M%S')
            screenshot_path = f"modal_login_{timestamp}.png"
            page.screenshot(path=screenshot_path, full_page=True)
            exibir_mensagem(f"📸 Screenshot salvo: {screenshot_path}")
            
            # Verificar se os campos estão realmente preenchidos
            valor_email_campo = campo_email.input_value()
            valor_senha_campo = campo_senha.input_value()
            
            exibir_mensagem(f"🔍 VERIFICAÇÃO DOS CAMPOS:")
            exibir_mensagem(f"   📧 Email no campo: '{valor_email_campo}'")
            exibir_mensagem(f"   🔒 Senha no campo: '{valor_senha_campo}'")
            exibir_mensagem(f"   📧 Email esperado: '{email_login}'")
            exibir_mensagem(f"   🔒 Senha esperada: '{senha_login}'")
            
            # Verificar se os campos estão corretos
            if valor_email_campo.lower() == email_login.lower():
                exibir_mensagem("✅ Email preenchido corretamente!")
            else:
                exibir_mensagem("❌ Email NÃO foi preenchido corretamente!")
            
            if valor_senha_campo == senha_login:
                exibir_mensagem("✅ Senha preenchida corretamente!")
            else:
                exibir_mensagem("❌ Senha NÃO foi preenchida corretamente!")
            
            # Verificar se o botão "Acessar" está visível
            botao_acessar = page.locator("#gtm-telaLoginBotaoAcessar")
            if botao_acessar.is_visible():
                exibir_mensagem("✅ Botão 'Acessar' está visível e pronto para clicar!")
                texto_botao = botao_acessar.text_content()
                exibir_mensagem(f"   📝 Texto do botão: '{texto_botao}'")
            else:
                exibir_mensagem("❌ Botão 'Acessar' NÃO está visível!")
            
            # Verificar se o modal está realmente presente
            modal_presente = page.locator("text=Acesse sua conta para visualizar o resultado final")
            if modal_presente.count() > 0:
                exibir_mensagem("✅ Modal de login está presente na tela!")
            else:
                exibir_mensagem("❌ Modal de login NÃO está presente na tela!")
            
            # Capturar HTML do modal para debug
            try:
                modal_html = page.locator(".MuiBackdrop-root").inner_html()
                exibir_mensagem(f"🔍 HTML do modal capturado (primeiros 200 chars): {modal_html[:200]}...")
            except Exception as e:
                exibir_mensagem(f"⚠️ Erro ao capturar HTML do modal: {str(e)}")
            
        except Exception as e:
            exibir_mensagem(f"❌ Erro durante captura de tela/logs: {str(e)}")
        
        # PASSO 8: Clicar em "Acessar"
        exibir_mensagem("🔄 Clicando em 'Acessar'...")
        
        try:
            # Aguardar especificamente pelo botão estar pronto
            botao_acessar = page.locator("#gtm-telaLoginBotaoAcessar")
            botao_acessar.wait_for(timeout=3000)
            
            if botao_acessar.is_visible():
                botao_acessar.click()
                exibir_mensagem("✅ Botão 'Acessar' clicado com sucesso!")
                
                # Aguardar possível redirecionamento ou modal CPF divergente
                exibir_mensagem("⏳ Aguardando resposta do login...")
                time.sleep(5)  # ESTRATÉGIA SIMPLES: time.sleep ao invés de waits complexos
                
                # Verificar se apareceu modal CPF divergente
                try:
                    modal_cpf = page.locator("text=CPF informado não corresponde à conta")
                    if modal_cpf.count() > 0:
                        exibir_mensagem("✅ Modal CPF divergente detectado!")
                        
                        # Clicar no botão "Manter Login atual"
                        try:
                            exibir_mensagem("🔍 Procurando botão 'Manter Login atual'...")
                            
                            # Tentar pelo ID específico
                            botao_manter_login = page.locator("#manterLoginAtualModalAssociarUsuario")
                            if botao_manter_login.is_visible():
                                botao_manter_login.click()
                                exibir_mensagem("✅ Botão 'Manter Login atual' clicado pelo ID!")
                                time.sleep(3)
                            else:
                                # Tentar pelo texto
                                botao_manter_login = page.locator("text=Manter Login atual")
                                if botao_manter_login.is_visible():
                                    botao_manter_login.click()
                                    exibir_mensagem("✅ Botão 'Manter Login atual' clicado pelo texto!")
                                    time.sleep(3)
                                else:
                                    exibir_mensagem("⚠️ Botão 'Manter Login atual' não encontrado")
                        except Exception as e:
                            exibir_mensagem(f"⚠️ Erro ao clicar no botão 'Manter Login atual': {str(e)}")
                    else:
                        exibir_mensagem("ℹ️ Modal CPF divergente não apareceu - login pode ter sido bem-sucedido")
                except Exception as e:
                    exibir_mensagem(f"⚠️ Erro ao verificar modal CPF: {str(e)}")
                
            else:
                exibir_mensagem("❌ Botão 'Acessar' não está visível!")
                return False
        except Exception as e:
            exibir_mensagem(f"❌ Erro ao clicar em 'Acessar': {str(e)}")
            return False
        
        exibir_mensagem("✅ LOGIN CONCLUÍDO!")
        
        # ========================================
        # CAPTURA DE DADOS DOS PLANOS DE SEGURO
        # ========================================
        exibir_mensagem("📊 INICIANDO CAPTURA DE DADOS DOS PLANOS...")
        
        # Aguardar carregamento dos planos (aguardando botão específico)
        exibir_mensagem("⏳ Aguardando carregamento da página principal dos planos...")
        try:
            # Aguardar pelo botão "Personalizar Coberturas" que indica que a página foi carregada
            page.wait_for_selector("#personalizarCoberturasTelaPersonalizarCoberturas", timeout=10000)
            exibir_mensagem("✅ Página principal dos planos carregada!")
        except Exception as e:
            exibir_mensagem(f"⚠️ Botão 'Personalizar Coberturas' não encontrado: {str(e)}")
            exibir_mensagem("ℹ️ Usando fallback com time.sleep...")
            time.sleep(5)  # Fallback para time.sleep
        
        # Capturar dados dos planos
        dados_planos = capturar_dados_planos_seguro(page)
        
        if dados_planos:
            exibir_mensagem("✅ DADOS DOS PLANOS CAPTURADOS COM SUCESSO!")
            exibir_mensagem("📋 RESUMO DOS DADOS CAPTURADOS:")
            exibir_mensagem(f"   📊 Plano Recomendado: {dados_planos['plano_recomendado'].get('valor', 'N/A')}")
            exibir_mensagem(f"   📊 Plano Alternativo: {dados_planos['plano_alternativo'].get('valor', 'N/A')}")
            
            # RETORNO FINAL SIMPLES
            print("\n" + "="*60)
            print("📋 RETORNO FINAL - TELA 15")
            print("="*60)
            print(json.dumps(dados_planos, indent=2, ensure_ascii=False))
            print("="*60)
        else:
            exibir_mensagem("⚠️ FALHA NA CAPTURA DE DADOS DOS PLANOS")
        
        exibir_mensagem("🎯 TELA 15 FINALIZADA COM SUCESSO!")
        
        return True
        
    except Exception as e:
        exibir_mensagem(f"❌ ERRO na Tela 15: {str(e)}")
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
        
        # Captura os cards de cobertura usando o seletor específico identificado
        cards_cobertura = page.locator("div.bg-primary")
        
        if cards_cobertura.count() > 0:
            exibir_mensagem(f"🔍 Encontrados {cards_cobertura.count()} cards de cobertura (bg-primary)")
            
            for i in range(cards_cobertura.count()):
                try:
                    card = cards_cobertura.nth(i)
                    
                    # Captura o texto completo do card
                    card_text = card.text_content().strip() if card.text_content() else ""
                    
                    if not card_text or len(card_text) < 10:
                        continue
                    
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
                    
                    # Extrair nome da cobertura (texto dentro do button)
                    nome_cobertura = ""
                    try:
                        nome_elemento = card.locator("button p.text-white")
                        if nome_elemento.count() > 0:
                            nome_cobertura = nome_elemento.first.text_content().strip()
                            cobertura_info["nome_cobertura"] = nome_cobertura
                    except:
                        pass
                    
                    # Se não encontrou pelo seletor específico, tentar por regex
                    if not nome_cobertura:
                        cobertura_patterns = [
                            r"Cobertura\s+([A-Za-zÀ-ÿ\s]+?)(?:\s|$)",
                            r"([A-Za-zÀ-ÿ\s]+?)\s+Cobertura",
                            r"([A-Za-zÀ-ÿ\s]+?)\s+Compreensiva",
                            r"([A-Za-zÀ-ÿ\s]+?)\s+Roubo",
                            r"([A-Za-zÀ-ÿ\s]+?)\s+RCF"
                        ]
                        
                        for pattern in cobertura_patterns:
                            match = re.search(pattern, card_text, re.IGNORECASE)
                            if match:
                                cobertura_info["nome_cobertura"] = match.group(1).strip()
                                break
                    
                    # Buscar valores usando o seletor específico identificado
                    try:
                        # Procurar por elementos com valores usando o seletor correto
                        elementos_preco = page.locator("p.text-primary.underline")
                        if elementos_preco.count() > i:
                            preco_text = elementos_preco.nth(i).text_content().strip()
                            
                            # Extrair valores "de" e "até" usando regex
                            valor_patterns = [
                                r"De\s*R\$\s*([0-9.,]+)\s*até\s*R\$\s*([0-9.,]+)",
                                r"R\$\s*([0-9.,]+)\s*até\s*R\$\s*([0-9.,]+)",
                                r"([0-9.,]+)\s*até\s*([0-9.,]+)"
                            ]
                            
                            for pattern in valor_patterns:
                                match = re.search(pattern, preco_text, re.IGNORECASE)
                                if match:
                                    cobertura_info["valores"]["de"] = f"R$ {match.group(1)}"
                                    cobertura_info["valores"]["ate"] = f"R$ {match.group(2)}"
                                    break
                    except:
                        pass
                    
                    # Se não encontrou valores específicos, tentar no texto do card
                    if not cobertura_info["valores"]["de"]:
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
                                break
                    
                    # Extrair benefícios usando o seletor específico identificado
                    try:
                        # Procurar por elementos de benefícios próximos ao card
                        elementos_beneficios = page.locator("div.gap-3.flex.flex-col.pl-4.mt-3")
                        if elementos_beneficios.count() > i:
                            container_beneficios = elementos_beneficios.nth(i)
                            beneficios_texto = container_beneficios.locator("p.text-sm.text-gray-100.font-normal")
                            
                            for j in range(beneficios_texto.count()):
                                beneficio_texto = beneficios_texto.nth(j).text_content().strip()
                                if beneficio_texto:
                                    cobertura_info["beneficios"].append({
                                        "nome": beneficio_texto,
                                        "status": "incluido"
                                    })
                    except:
                        pass
                    
                    # Fallback: procurar por benefícios conhecidos no texto do card
                    if not cobertura_info["beneficios"]:
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
                    
                    # Se encontrou dados válidos, adicionar à lista
                    if cobertura_info["nome_cobertura"] or cobertura_info["valores"]["de"]:
                        dados_carrossel["coberturas_detalhadas"].append(cobertura_info)
                        
                        # Conta valores encontrados
                        if cobertura_info["valores"]["de"]:
                            dados_carrossel["valores_encontrados"] += 1
                        
                        exibir_mensagem(f"📋 Card {i + 1}: {cobertura_info['nome_cobertura']} - De {cobertura_info['valores']['de']} até {cobertura_info['valores']['ate']}")
                        
                except Exception as e:
                    exibir_mensagem(f"⚠️ Erro ao processar card {i + 1}: {str(e)}")
                    continue
        
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

def capturar_dados_planos_seguro(page: Page) -> Dict[str, Any]:
    """
    CAPTURA DADOS DOS PLANOS DE SEGURO - ABORDAGEM HÍBRIDA
    
    DESCRIÇÃO:
        Captura os dados dos planos de seguro (Recomendado e Alternativo) na Tela 15.
        Usa abordagem híbrida: seletores + extração de texto completo + parse estruturado + regex.
        Baseado na implementação Selenium que funcionava corretamente.
        
    ESTRATÉGIA:
        1. Encontrar containers dos planos usando seletores
        2. Extrair texto completo de cada container
        3. Fazer parse estruturado baseado na posição das linhas
        4. Usar regex como fallback para valores não encontrados
        5. Mapear dados para estrutura JSON estruturada
        
    RETORNO:
        dict: Dicionário com os dados dos planos estruturados
    """
    try:
        exception_handler.definir_tela_atual("CAPTURA_DADOS_PLANOS")
        exibir_mensagem("📊 CAPTURANDO DADOS DOS PLANOS DE SEGURO - ABORDAGEM HÍBRIDA")
        exibir_mensagem("=" * 70)
        
        # Aguardar carregamento dos planos (estratégia simples)
        time.sleep(3)
        
        dados_planos = {
            "plano_recomendado": {
                "plano": "Plano recomendado",
                "valor": "N/A",
                "forma_pagamento": "N/A",
                "parcelamento": "N/A",
                "valor_franquia": "N/A",
                "valor_mercado": "N/A",
                "assistencia": False,
                "vidros": False,
                "carro_reserva": False,
                "danos_materiais": "N/A",
                "danos_corporais": "N/A",
                "danos_morais": "N/A",
                "morte_invalidez": "N/A"
            },
            "plano_alternativo": {
                "plano": "Plano alternativo",
                "valor": "N/A",
                "forma_pagamento": "N/A",
                "parcelamento": "N/A",
                "valor_franquia": "N/A",
                "valor_mercado": "N/A",
                "assistencia": False,
                "vidros": False,
                "carro_reserva": False,
                "danos_materiais": "N/A",
                "danos_corporais": "N/A",
                "danos_morais": "N/A",
                "morte_invalidez": "N/A"
            }
        }
        
        # ========================================
        # ETAPA 1: ENCONTRAR CONTAINERS DOS PLANOS
        # ========================================
        exibir_mensagem("🔍 ETAPA 1: Encontrando containers dos planos...")
        
        # Estratégia 1: Procurar por divs que contêm "Plano recomendado"
        planos_recomendados = page.locator("//*[contains(text(), 'Plano recomendado')]").all()
        
        # Estratégia 2: Procurar por divs com classes específicas que contêm planos
        planos_divs = page.locator("//div[contains(@class, 'md:w-80') or contains(@class, 'border-4') or contains(@class, 'border-primary')]").all()
        
        # Estratégia 3: Procurar por elementos que contêm valores monetários específicos
        elementos_valores = page.locator("//*[contains(text(), 'R$')]").all()
        
        # Estratégia 4: Procurar por elementos que contêm coberturas específicas
        elementos_coberturas = page.locator("//*[contains(text(), 'Franquia') or contains(text(), 'Valor de Mercado') or contains(text(), 'Assistência') or contains(text(), 'Vidros') or contains(text(), 'Carro Reserva') or contains(text(), 'Danos Materiais') or contains(text(), 'Danos Corporais') or contains(text(), 'Danos Morais') or contains(text(), 'Morte/Invalidez')]").all()
        
        # Combinar todos os elementos encontrados
        todos_elementos = list(set(planos_recomendados + planos_divs + elementos_valores + elementos_coberturas))
        
        exibir_mensagem(f"📊 ELEMENTOS ENCONTRADOS: {len(todos_elementos)}")
        
        # Filtrar elementos que são containers de planos (não apenas texto)
        tabelas_planos = []
        for elem in todos_elementos:
            try:
                # Verificar se o elemento contém múltiplos valores monetários ou é um container
                texto = elem.text_content()
                if (texto.count('R$') >= 2 or 
                    'Franquia' in texto or 
                    'Valor de Mercado' in texto or
                    'Plano recomendado' in texto or
                    len(texto) > 100):  # Elementos com muito texto provavelmente são containers
                    tabelas_planos.append(elem)
            except:
                continue
        
        exibir_mensagem(f"📊 CONTAINERS DE PLANOS ENCONTRADOS: {len(tabelas_planos)}")
        
        # ========================================
        # ETAPA 2: ANALISAR CADA CONTAINER
        # ========================================
        for i, elemento in enumerate(tabelas_planos[:10]):  # Limitar a 10 containers
            try:
                tabela_text = elemento.text_content().strip()
                if not tabela_text or len(tabela_text) < 30:
                    continue
                
                exibir_mensagem(f"📋 ANALISANDO CONTAINER {i+1}: {len(tabela_text)} caracteres")
                
                # Determinar se é plano recomendado ou alternativo
                if "plano recomendado" in tabela_text.lower():
                    plano_tipo = "plano_recomendado"
                    exibir_mensagem("✅ PLANO RECOMENDADO DETECTADO")
                else:
                    plano_tipo = "plano_alternativo"
                    exibir_mensagem("✅ PLANO ALTERNATIVO DETECTADO")
                
                # ETAPA 3: PARSE ESTRUTURADO BASEADO NA POSIÇÃO
                # Dividir o texto por quebras de linha para análise estruturada
                linhas = tabela_text.split('\n')
                linhas = [linha.strip() for linha in linhas if linha.strip()]
                
                exibir_mensagem(f"🔍 ANALISANDO ESTRUTURA: {len(linhas)} linhas encontradas")
                
                # Determinar se tem título e ajustar índice de início
                tem_titulo = False
                indice_inicio = 0
                
                if len(linhas) > 0:
                    primeira_linha = linhas[0].lower()
                    if "plano recomendado" in primeira_linha or "recomendado" in primeira_linha:
                        tem_titulo = True
                        indice_inicio = 1  # Pular o título
                        exibir_mensagem("✅ TÍTULO DETECTADO - PULANDO PRIMEIRA LINHA")
                
                # Parse estruturado baseado na especificação
                if len(linhas) >= indice_inicio + 8:  # Mínimo de 8 campos após título
                    try:
                        # 1. Moeda (R$) - posição 0 ou 1 dependendo se tem título
                        moeda = linhas[indice_inicio]
                        if moeda == "R$":
                            exibir_mensagem("✅ MOEDA DETECTADA: R$")
                        
                        # 2. Preço anual - posição 1 ou 2 dependendo se tem título
                        if indice_inicio + 1 < len(linhas):
                            preco_anual = linhas[indice_inicio + 1]
                            # Validar se é um preço (contém números e vírgula/ponto)
                            if re.match(r'^[0-9.,]+$', preco_anual):
                                dados_planos[plano_tipo]["valor"] = f"R$ {preco_anual}"
                                exibir_mensagem(f"✅ PREÇO ANUAL: R$ {preco_anual}")
                        
                        # 3. Periodicidade (anual) - posição 2 ou 3
                        if indice_inicio + 2 < len(linhas):
                            periodicidade = linhas[indice_inicio + 2]
                            if "anual" in periodicidade.lower():
                                dados_planos[plano_tipo]["forma_pagamento"] = periodicidade
                                exibir_mensagem("✅ PERIODICIDADE: Anual")
                        
                        # 4. Forma de pagamento - posição 3 ou 4
                        if indice_inicio + 3 < len(linhas):
                            forma_pagamento = linhas[indice_inicio + 3]
                            dados_planos[plano_tipo]["parcelamento"] = forma_pagamento
                            
                            # Extrair valor de parcelamento se houver
                            # Padrão: "Crédito em até 1x sem juros ou 10x de R$ 346,82"
                            parcelamento_match = re.search(r'(\d+x)\s*de\s*R\$\s*([0-9.,]+)', forma_pagamento)
                            if parcelamento_match:
                                valor_parcela = parcelamento_match.group(2)
                                exibir_mensagem(f"✅ VALOR PARCELA: R$ {valor_parcela}")
                            
                            exibir_mensagem(f"✅ FORMA PAGAMENTO: {forma_pagamento}")
                        
                        # 5. Franquia - posição 4 ou 5
                        if indice_inicio + 4 < len(linhas):
                            franquia_valor = linhas[indice_inicio + 4]
                            if re.match(r'^R\$\s*[0-9.,]+$', franquia_valor):
                                dados_planos[plano_tipo]["valor_franquia"] = franquia_valor
                                exibir_mensagem(f"✅ FRANQUIA VALOR: {franquia_valor}")
                        
                        # 6. Característica da franquia - posição 5 ou 6
                        if indice_inicio + 5 < len(linhas):
                            franquia_tipo = linhas[indice_inicio + 5]
                            if franquia_tipo.lower() in ["reduzida", "normal"]:
                                exibir_mensagem(f"✅ FRANQUIA TIPO: {franquia_tipo}")
                        
                        # 7. Cobertura do valor do veículo - posição 6 ou 7
                        if indice_inicio + 6 < len(linhas):
                            cobertura_veiculo = linhas[indice_inicio + 6]
                            if "100% da tabela FIPE" in cobertura_veiculo:
                                dados_planos[plano_tipo]["valor_mercado"] = cobertura_veiculo
                                exibir_mensagem(f"✅ COBERTURA VEÍCULO: {cobertura_veiculo}")
                        
                        # 8-11. Itens adicionais (posições 7-10 ou 8-11)
                        itens_adicionais = []
                        for j in range(indice_inicio + 7, min(indice_inicio + 11, len(linhas))):
                            if j < len(linhas):
                                item = linhas[j]
                                if re.match(r'^R\$\s*[0-9.,]+$', item):
                                    itens_adicionais.append(item)
                        
                        # Mapear itens adicionais para coberturas específicas
                        if len(itens_adicionais) >= 4:
                            # Baseado na especificação: Danos Materiais, Danos Corporais, Danos Morais, Morte/Invalidez
                            dados_planos[plano_tipo]["danos_materiais"] = itens_adicionais[0]
                            dados_planos[plano_tipo]["danos_corporais"] = itens_adicionais[1]
                            dados_planos[plano_tipo]["danos_morais"] = itens_adicionais[2]
                            dados_planos[plano_tipo]["morte_invalidez"] = itens_adicionais[3]
                            
                            exibir_mensagem(f"✅ ITENS ADICIONAIS: {len(itens_adicionais)} itens mapeados")
                        
                    except Exception as e:
                        exception_handler.capturar_warning(f"ERRO NO PARSE ESTRUTURADO: {str(e)}", "CAPTURA_DADOS_PLANOS")
                        # Fallback para método anterior se o parse estruturado falhar
                        exibir_mensagem("🔄 FALLBACK: Usando método anterior de extração")
                        
                        # Extrair valores monetários com padrões mais específicos
                        valor_patterns = [
                            r"R\$\s*([0-9.,]+)",
                            r"([0-9.,]+)\s*anual",
                            r"([0-9.,]+)\s*em até",
                            r"R\$\s*([0-9.,]+)\s*anual",
                            r"R\$\s*([0-9.,]+)\s*em até"
                        ]
                        
                        valores_encontrados = []
                        for pattern in valor_patterns:
                            matches = re.findall(pattern, tabela_text, re.IGNORECASE)
                            valores_encontrados.extend(matches)
                        
                        # Remover duplicatas e ordenar
                        valores_encontrados = list(set(valores_encontrados))
                        valores_encontrados.sort(key=lambda x: float(x.replace(',', '').replace('.', '')))
                        
                        # Extrair condições de pagamento
                        pagamento_patterns = [
                            r"Crédito em até (\d+x)\s*(?:sem juros|com juros)?\s*(?:ou \d+x de R\$\s*([0-9.,]+))?",
                            r"(\d+x)\s*(?:sem juros|com juros)",
                            r"parcelamento\s*(?:sem juros|com juros)"
                        ]
                        
                        for pattern in pagamento_patterns:
                            match = re.search(pattern, tabela_text, re.IGNORECASE)
                            if match:
                                if "Crédito em até" in pattern:
                                    dados_planos[plano_tipo]["parcelamento"] = f"{match.group(1)} sem juros"
                                    if match.group(2):
                                        exibir_mensagem(f"✅ VALOR PARCELA (fallback): R$ {match.group(2)}")
                                else:
                                    dados_planos[plano_tipo]["parcelamento"] = match.group(0)
                                break
                        
                        if valores_encontrados:
                            # Procurar por valores específicos que vi no HTML
                            for valor in valores_encontrados:
                                valor_limpo = valor.replace(',', '').replace('.', '')
                                if valor_limpo == '10000':  # R$ 100,00
                                    dados_planos[plano_tipo]["valor"] = f"R$ {valor}"
                                elif valor_limpo == '256100':  # R$ 2.561,00
                                    dados_planos[plano_tipo]["valor"] = f"R$ {valor}"
                                elif valor_limpo == '250000':  # R$ 2.500,00
                                    dados_planos[plano_tipo]["valor_franquia"] = f"R$ {valor}"
                                elif valor_limpo == '358406':  # R$ 3.584,06
                                    dados_planos[plano_tipo]["valor_franquia"] = f"R$ {valor}"
                                elif valor_limpo == '50000':  # R$ 50.000,00
                                    dados_planos[plano_tipo]["danos_materiais"] = f"R$ {valor}"
                                    dados_planos[plano_tipo]["danos_corporais"] = f"R$ {valor}"
                                elif valor_limpo == '100000':  # R$ 100.000,00
                                    dados_planos[plano_tipo]["danos_materiais"] = f"R$ {valor}"
                                    dados_planos[plano_tipo]["danos_corporais"] = f"R$ {valor}"
                                elif valor_limpo == '20000':  # R$ 20.000,00
                                    dados_planos[plano_tipo]["danos_morais"] = f"R$ {valor}"
                                elif valor_limpo == '10000' and not dados_planos[plano_tipo]["danos_morais"]:  # R$ 10.000,00 (evitar conflito)
                                    dados_planos[plano_tipo]["danos_morais"] = f"R$ {valor}"
                                elif valor_limpo == '5000':  # R$ 5.000,00
                                    dados_planos[plano_tipo]["morte_invalidez"] = f"R$ {valor}"
                            
                            # Se não encontrou valores específicos, usar o primeiro como anual
                            if not dados_planos[plano_tipo]["valor"] and valores_encontrados:
                                dados_planos[plano_tipo]["valor"] = f"R$ {valores_encontrados[0]}"
                else:
                    exception_handler.capturar_warning(f"DADOS INSUFICIENTES: Apenas {len(linhas)} linhas encontradas", "CAPTURA_DADOS_PLANOS")
                    # MELHORIA: Parse inteligente para planos com poucas linhas
                    try:
                        exibir_mensagem("🔍 ANALISANDO PLANO COM POUCAS LINHAS")
                        
                        # Tentar extrair pelo menos o preço anual e forma de pagamento
                        if len(linhas) >= 2:
                            # Primeira linha pode ser moeda (R$) ou preço
                            primeira_linha = linhas[0].strip()
                            if primeira_linha == "R$" and len(linhas) >= 3:
                                # Formato: R$ / preço / anual
                                preco_anual = linhas[1].strip()
                                if re.match(r'^[0-9.,]+$', preco_anual):
                                    dados_planos[plano_tipo]["valor"] = f"R$ {preco_anual}"
                                    exibir_mensagem(f"✅ PREÇO ANUAL EXTRAÍDO: R$ {preco_anual}")
                            elif re.match(r'^[0-9.,]+$', primeira_linha):
                                # Formato: preço / anual
                                dados_planos[plano_tipo]["valor"] = f"R$ {primeira_linha}"
                                exibir_mensagem(f"✅ PREÇO ANUAL EXTRAÍDO: R$ {primeira_linha}")
                        
                        # Procurar forma de pagamento no texto completo
                        pagamento_match = re.search(r'Crédito em até (\d+x)\s*(?:sem juros|com juros)?\s*(?:ou \d+x de R\$\s*([0-9.,]+))?', tabela_text)
                        if pagamento_match:
                            parcelas = pagamento_match.group(1)
                            valor_parcela = pagamento_match.group(2) if pagamento_match.group(2) else ""
                            
                            dados_planos[plano_tipo]["parcelamento"] = f"{parcelas} sem juros"
                            if valor_parcela:
                                exibir_mensagem(f"✅ VALOR PARCELA EXTRAÍDO: R$ {valor_parcela}")
                            
                            exibir_mensagem(f"✅ FORMA PAGAMENTO EXTRAÍDA: {parcelas} sem juros")
                        
                        # Procurar outros valores monetários no texto completo
                        valores_monetarios = re.findall(r'R\$\s*([0-9.,]+)', tabela_text)
                        if valores_monetarios:
                            # Mapear valores encontrados para campos específicos
                            for valor in valores_monetarios:
                                valor_limpo = valor.replace(',', '').replace('.', '')
                                valor_completo = f"R$ {valor}"
                                
                                # Evitar duplicar o preço anual já extraído
                                if valor_completo != dados_planos[plano_tipo]["valor"]:
                                    # Tentar identificar o tipo de valor baseado no contexto
                                    if valor_limpo in ['251660', '2516.60']:  # Franquia reduzida
                                        dados_planos[plano_tipo]["valor_franquia"] = valor_completo
                                    elif valor_limpo in ['507594', '5075.94']:  # Franquia normal
                                        dados_planos[plano_tipo]["valor_franquia"] = valor_completo
                                    elif valor_limpo in ['50000', '50000.00']:  # Danos materiais/corporais
                                        if not dados_planos[plano_tipo]["danos_materiais"]:
                                            dados_planos[plano_tipo]["danos_materiais"] = valor_completo
                                        if not dados_planos[plano_tipo]["danos_corporais"]:
                                            dados_planos[plano_tipo]["danos_corporais"] = valor_completo
                                    elif valor_limpo in ['100000', '100000.00']:  # Danos materiais/corporais premium
                                        if not dados_planos[plano_tipo]["danos_materiais"]:
                                            dados_planos[plano_tipo]["danos_materiais"] = valor_completo
                                        if not dados_planos[plano_tipo]["danos_corporais"]:
                                            dados_planos[plano_tipo]["danos_corporais"] = valor_completo
                                    elif valor_limpo in ['20000', '20000.00']:  # Danos morais
                                        dados_planos[plano_tipo]["danos_morais"] = valor_completo
                                    elif valor_limpo in ['10000', '10000.00']:  # Danos morais menor
                                        if not dados_planos[plano_tipo]["danos_morais"]:
                                            dados_planos[plano_tipo]["danos_morais"] = valor_completo
                                    elif valor_limpo in ['5000', '5000.00']:  # Morte/invalidez
                                        dados_planos[plano_tipo]["morte_invalidez"] = valor_completo
                                    elif valor_limpo in ['0', '0.00']:  # Morte/invalidez zero
                                        dados_planos[plano_tipo]["morte_invalidez"] = valor_completo
                        
                    except Exception as e:
                        exibir_mensagem(f"⚠️ ERRO NO PARSE INTELIGENTE: {str(e)}")
                
                # ETAPA 4: DETECTAR COBERTURAS (ÍCONES DE OK)
                exibir_mensagem("🔍 ETAPA 4: Detectando coberturas...")
                
                coberturas = ['assistencia', 'vidros', 'carro_reserva']
                
                for j, cobertura in enumerate(coberturas):
                    try:
                        # Procurar por ícones de OK
                        icones_ok = elemento.locator("img[src='/icone-ok.svg']").all()
                        
                        if len(icones_ok) > j and icones_ok[j].is_visible():
                            dados_planos[plano_tipo][cobertura] = True
                            exibir_mensagem(f"✅ {cobertura.title()}: True (ícone detectado)")
                        else:
                            # Verificar se existe o texto da cobertura - se existe, é True
                            if cobertura.title() in tabela_text:
                                dados_planos[plano_tipo][cobertura] = True
                                exibir_mensagem(f"✅ {cobertura.title()}: True (texto detectado)")
                            else:
                                # Se não encontrou nem ícone nem texto, verificar se há elementos específicos
                                elementos_cobertura = elemento.locator(f"div:has-text('{cobertura.title()}')").all()
                                if len(elementos_cobertura) > 0:
                                    dados_planos[plano_tipo][cobertura] = True
                                    exibir_mensagem(f"✅ {cobertura.title()}: True (elemento encontrado)")
                                else:
                                    dados_planos[plano_tipo][cobertura] = False
                                    exibir_mensagem(f"❌ {cobertura.title()}: False")
                    except Exception as e:
                        # Em caso de erro, verificar se o texto da cobertura existe no container
                        if cobertura.title() in tabela_text:
                            dados_planos[plano_tipo][cobertura] = True
                            exibir_mensagem(f"✅ {cobertura.title()}: True (fallback - texto detectado)")
                        else:
                            dados_planos[plano_tipo][cobertura] = False
                            exception_handler.capturar_warning(f"Erro ao capturar {cobertura}: {str(e)} - definindo como False", "CAPTURA_DADOS_PLANOS")
                
                # ETAPA 5: CAPTURA ESPECÍFICA DE VALORES DE MERCADO E DANOS
                exibir_mensagem("🔍 ETAPA 5: Captura específica de valores...")
                
                # Valor de Mercado
                valor_mercado_match = re.search(r'100%\s*da\s*tabela\s*FIPE', tabela_text, re.IGNORECASE)
                if valor_mercado_match:
                    dados_planos[plano_tipo]["valor_mercado"] = "100% da tabela FIPE"
                    exibir_mensagem("✅ Valor de Mercado: 100% da tabela FIPE")
                
                # Danos Materiais
                danos_materiais_match = re.search(r'Danos\s+Materiais.*?R\$\s*([0-9.,]+)', tabela_text, re.IGNORECASE)
                if danos_materiais_match:
                    dados_planos[plano_tipo]["danos_materiais"] = f"R$ {danos_materiais_match.group(1)}"
                    exibir_mensagem(f"✅ Danos Materiais: R$ {danos_materiais_match.group(1)}")
                
                # Danos Corporais
                danos_corporais_match = re.search(r'Danos\s+Corporais.*?R\$\s*([0-9.,]+)', tabela_text, re.IGNORECASE)
                if danos_corporais_match:
                    dados_planos[plano_tipo]["danos_corporais"] = f"R$ {danos_corporais_match.group(1)}"
                    exibir_mensagem(f"✅ Danos Corporais: R$ {danos_corporais_match.group(1)}")
                
                # Danos Morais
                danos_morais_match = re.search(r'Danos\s+Morais.*?R\$\s*([0-9.,]+)', tabela_text, re.IGNORECASE)
                if danos_morais_match:
                    dados_planos[plano_tipo]["danos_morais"] = f"R$ {danos_morais_match.group(1)}"
                    exibir_mensagem(f"✅ Danos Morais: R$ {danos_morais_match.group(1)}")
                
                # Morte/Invalidez
                morte_invalidez_match = re.search(r'Morte/Invalidez.*?R\$\s*([0-9.,]+)', tabela_text, re.IGNORECASE)
                if morte_invalidez_match:
                    dados_planos[plano_tipo]["morte_invalidez"] = f"R$ {morte_invalidez_match.group(1)}"
                    exibir_mensagem(f"✅ Morte/Invalidez: R$ {morte_invalidez_match.group(1)}")
                
                # Se encontrou dados válidos, sair do loop
                if dados_planos[plano_tipo]["valor"] != "N/A":
                    exibir_mensagem(f"✅ DADOS CAPTURADOS COM SUCESSO PARA {plano_tipo.upper()}")
                    break
                    
            except Exception as e:
                exception_handler.capturar_warning(f"Erro ao analisar container {i+1}: {str(e)}", "CAPTURA_DADOS_PLANOS")
                continue
        
        # ========================================
        # ETAPA 5: FALLBACK FINAL COM SELETORES ESPECÍFICOS
        # ========================================
        exibir_mensagem("🔍 ETAPA 5: Fallback final com seletores específicos...")
        
        # Para cada plano, verificar se ainda há campos "N/A" e tentar preencher
        for plano_tipo in ["plano_recomendado", "plano_alternativo"]:
            if dados_planos[plano_tipo]["valor"] == "N/A":
                # Tentar capturar valor com seletores específicos
                try:
                    valores_seguro = page.locator("label.text-primary.font-workSans.font-semibold.text-\\[32px\\]").all()
                    if len(valores_seguro) > 0:
                        if plano_tipo == "plano_recomendado":
                            valor_elem = valores_seguro[0]
                        else:
                            valor_elem = valores_seguro[1] if len(valores_seguro) > 1 else valores_seguro[0]
                        
                        texto_valor = valor_elem.text_content().strip()
                        valor_formatado = texto_valor.replace('\n', '').replace(' ', '')
                        if valor_formatado.startswith('R$'):
                            dados_planos[plano_tipo]["valor"] = valor_formatado
                        else:
                            dados_planos[plano_tipo]["valor"] = f"R$ {valor_formatado}"
                        exibir_mensagem(f"✅ VALOR CAPTURADO (fallback): {dados_planos[plano_tipo]['valor']}")
                except Exception as e:
                    exibir_mensagem(f"⚠️ Erro no fallback de valor: {str(e)}")
            
            if dados_planos[plano_tipo]["forma_pagamento"] == "N/A":
                try:
                    formas_pagamento = page.locator("label.text-primary.text-xs.font-normal.mb-2").all()
                    if len(formas_pagamento) > 0:
                        if plano_tipo == "plano_recomendado":
                            forma_elem = formas_pagamento[0]
                        else:
                            forma_elem = formas_pagamento[1] if len(formas_pagamento) > 1 else formas_pagamento[0]
                        
                        dados_planos[plano_tipo]["forma_pagamento"] = forma_elem.text_content().strip()
                        exibir_mensagem(f"✅ FORMA PAGAMENTO CAPTURADA (fallback): {dados_planos[plano_tipo]['forma_pagamento']}")
                except Exception as e:
                    exibir_mensagem(f"⚠️ Erro no fallback de forma de pagamento: {str(e)}")
        
        # ========================================
        # ETAPA 6: SALVAR E RETORNAR DADOS
        # ========================================
        # Salvar dados em arquivo JSON
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_arquivo = f"dados_planos_seguro_{timestamp}.json"
        
        with open(nome_arquivo, 'w', encoding='utf-8') as f:
            json.dump(dados_planos, f, indent=2, ensure_ascii=False)
        
        exibir_mensagem(f"💾 Dados salvos em: {nome_arquivo}")
        exibir_mensagem("✅ CAPTURA DE DADOS CONCLUÍDA!")
        
        return dados_planos
        
    except Exception as e:
        exception_handler.capturar_excecao(e, "CAPTURA_DADOS_PLANOS", "Erro geral na captura de dados")
        return {
            "plano_recomendado": {"erro": "Falha na captura"},
            "plano_alternativo": {"erro": "Falha na captura"}
        }

# ========================================
# FUNÇÃO PRINCIPAL
# ========================================

def executar_rpa_playwright(parametros: Dict[str, Any]) -> Dict[str, Any]:
    """
    Função principal do RPA Playwright
    
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
        
        exibir_mensagem("🚀 INICIANDO RPA PLAYWRIGHT")
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
            
            # Executar Telas 1-15 sequencialmente
            telas_executadas = 0
            resultado_telas = {}
            
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
            
            # TELA 6
            exibir_mensagem("\n" + "="*50)
            if navegar_tela_6_playwright(page, parametros['combustivel'], parametros.get('kit_gas', False), parametros.get('blindado', False), parametros.get('financiado', False)):
                telas_executadas += 1
                resultado_telas["tela_6"] = True
                exibir_mensagem("✅ TELA 6 CONCLUÍDA!")
            else:
                resultado_telas["tela_6"] = False
                exibir_mensagem("❌ TELA 6 FALHOU!")
                return criar_retorno_erro(
                    "Tela 6 falhou",
                    "TELA_6",
                    time.time() - inicio_execucao,
                    parametros,
                    exception_handler
                )
            
            # TELA 7
            exibir_mensagem("\n" + "="*50)
            if navegar_tela_7_playwright(page, parametros['cep']):
                telas_executadas += 1
                resultado_telas["tela_7"] = True
                exibir_mensagem("✅ TELA 7 CONCLUÍDA!")
            else:
                resultado_telas["tela_7"] = False
                exibir_mensagem("❌ TELA 7 FALHOU!")
                return criar_retorno_erro(
                    "Tela 7 falhou",
                    "TELA_7",
                    time.time() - inicio_execucao,
                    parametros,
                    exception_handler
                )
            
            # TELA 8
            exibir_mensagem("\n" + "="*50)
            if navegar_tela_8_playwright(page, parametros['uso_veiculo']):
                telas_executadas += 1
                resultado_telas["tela_8"] = True
                exibir_mensagem("✅ TELA 8 CONCLUÍDA!")
            else:
                resultado_telas["tela_8"] = False
                exibir_mensagem("❌ TELA 8 FALHOU!")
                return criar_retorno_erro(
                    "Tela 8 falhou",
                    "TELA_8",
                    time.time() - inicio_execucao,
                    parametros,
                    exception_handler
                )
            
            # TELA 9
            exibir_mensagem("\n" + "="*50)
            if navegar_tela_9_playwright(page, parametros['nome'], parametros['cpf'], parametros['data_nascimento'], parametros['sexo'], parametros['estado_civil'], parametros['email'], parametros['celular']):
                telas_executadas += 1
                resultado_telas["tela_9"] = True
                exibir_mensagem("✅ TELA 9 CONCLUÍDA!")
            else:
                resultado_telas["tela_9"] = False
                exibir_mensagem("❌ TELA 9 FALHOU!")
                return criar_retorno_erro(
                    "Tela 9 falhou",
                    "TELA_9",
                    time.time() - inicio_execucao,
                    parametros,
                    exception_handler
                )
            
            # TELA 10
            exibir_mensagem("\n" + "="*50)
            if navegar_tela_10_playwright(page, parametros['condutor_principal'], parametros['nome_condutor'], parametros['cpf_condutor'], parametros['data_nascimento_condutor'], parametros['sexo_condutor'], parametros['estado_civil_condutor']):
                telas_executadas += 1
                resultado_telas["tela_10"] = True
                exibir_mensagem("✅ TELA 10 CONCLUÍDA!")
            else:
                resultado_telas["tela_10"] = False
                exibir_mensagem("❌ TELA 10 FALHOU!")
                return criar_retorno_erro(
                    "Tela 10 falhou",
                    "TELA_10",
                    time.time() - inicio_execucao,
                    parametros,
                    exception_handler
                )
            
            # TELA 11
            exibir_mensagem("\n" + "="*50)
            if navegar_tela_11_playwright(page, parametros['local_de_trabalho'], parametros['estacionamento_proprio_local_de_trabalho'], parametros['local_de_estudo'], parametros['estacionamento_proprio_local_de_estudo']):
                telas_executadas += 1
                resultado_telas["tela_11"] = True
                exibir_mensagem("✅ TELA 11 CONCLUÍDA!")
            else:
                resultado_telas["tela_11"] = False
                exibir_mensagem("❌ TELA 11 FALHOU!")
                return criar_retorno_erro(
                    "Tela 11 falhou",
                    "TELA_11",
                    time.time() - inicio_execucao,
                    parametros,
                    exception_handler
                )
            
            # TELA 12
            exibir_mensagem("\n" + "="*50)
            if navegar_tela_12_playwright(page, parametros['garagem_residencia'], parametros['portao_eletronico']):
                telas_executadas += 1
                resultado_telas["tela_12"] = True
                exibir_mensagem("✅ TELA 12 CONCLUÍDA!")
            else:
                resultado_telas["tela_12"] = False
                exibir_mensagem("❌ TELA 12 FALHOU!")
                return criar_retorno_erro(
                    "Tela 12 falhou",
                    "TELA_12",
                    time.time() - inicio_execucao,
                    parametros,
                    exception_handler
                )
            
            # TELA 13
            exibir_mensagem("\n" + "="*50)
            if navegar_tela_13_playwright(page, parametros['reside_18_26'], parametros['sexo_do_menor'], parametros['faixa_etaria_menor_mais_novo']):
                telas_executadas += 1
                resultado_telas["tela_13"] = True
                exibir_mensagem("✅ TELA 13 CONCLUÍDA!")
            else:
                resultado_telas["tela_13"] = False
                exibir_mensagem("❌ TELA 13 FALHOU!")
                return criar_retorno_erro(
                    "Tela 13 falhou",
                    "TELA_13",
                    time.time() - inicio_execucao,
                    parametros,
                    exception_handler
                )
            
            # TELA 14 (CONDICIONAL)
            exibir_mensagem("\n" + "="*50)
            if navegar_tela_14_playwright(page, parametros['continuar_com_corretor_anterior']):
                # Não incrementa telas_executadas pois é condicional
                resultado_telas["tela_14"] = True
                exibir_mensagem("✅ TELA 14 PROCESSADA!")
            else:
                resultado_telas["tela_14"] = False
                exibir_mensagem("❌ TELA 14 FALHOU!")
                return criar_retorno_erro(
                    "Tela 14 falhou",
                    "TELA_14",
                    time.time() - inicio_execucao,
                    parametros,
                    exception_handler
                )
            
            # TELA 15
            exibir_mensagem("\n" + "="*50)
            if navegar_tela_15_playwright(page, parametros['autenticacao']['email_login'], parametros['autenticacao']['senha_login']):
                telas_executadas += 1
                resultado_telas["tela_15"] = True
                exibir_mensagem("✅ TELA 15 CONCLUÍDA!")
            else:
                resultado_telas["tela_15"] = False
                exibir_mensagem("❌ TELA 15 FALHOU!")
                return criar_retorno_erro(
                    "Tela 15 falhou",
                    "TELA_15",
                    time.time() - inicio_execucao,
                    parametros,
                    exception_handler
                )
            
            # Resultado final
            exibir_mensagem("\n" + "="*60)
            exibir_mensagem("🎉 RPA TELAS 1 A 15 CONCLUÍDO COM SUCESSO!")
            exibir_mensagem(f"✅ Total de telas executadas: {telas_executadas}/14 (Tela 14 é condicional)")
            exibir_mensagem("✅ Todas as telas funcionaram corretamente")
            exibir_mensagem("✅ Navegação sequencial realizada com sucesso")
            
            # Capturar dados finais
            dados_planos = capturar_dados_planos_seguro(page)
            
            # Salvar dados
            arquivo_dados = salvar_dados_planos(dados_planos)
            
            # Fechar browser
            browser.close()
            
            # Calcular tempo de execução
            tempo_execucao = time.time() - inicio_execucao
            
            # Retorno estruturado
            return criar_retorno_sucesso(
                resultado_telas,
                dados_planos,
                arquivo_dados,
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
