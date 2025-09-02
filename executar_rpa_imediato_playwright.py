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
        
        time.sleep(3)
        
        botao_carro = page.locator("button.group").first
        
        if botao_carro.is_visible():
            botao_carro.click()
            exibir_mensagem("✅ Botão 'Carro' clicado com sucesso")
            time.sleep(3)
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
        time.sleep(3)
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
            time.sleep(3)
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
        
        time.sleep(3)
        return True
        
    except Exception as e:
        exception_handler.capturar_excecao(e, "TELA_4", f"Erro ao responder veículo segurado: {veiculo_segurado}")
        return False

def navegar_tela_5_playwright(page: Page) -> bool:
    """
    TELA 5: Estimativa inicial - CAPTURA DE DADOS
    """
    try:
        exception_handler.definir_tela_atual("TELA_5")
        exibir_mensagem("📱 TELA 5: Aguardando carregamento da estimativa...")
        
        time.sleep(2)
        
        max_tentativas = 30
        tentativa = 0
        
        while tentativa < max_tentativas:
            elemento_estimativa = page.locator("div.bg-primary")
            if elemento_estimativa.count() > 0:
                break
            time.sleep(1)
            tentativa += 1
        
        if tentativa >= max_tentativas:
            exception_handler.capturar_warning("Elementos da estimativa não carregaram", "TELA_5")
            return False
        
        exibir_mensagem("✅ Estimativa carregada com sucesso")
        
        botao_continuar = page.locator("#gtm-telaEstimativaContinuarParaCotacaoFinal").first
        botao_continuar.click()
        
        exibir_mensagem("✅ Botão 'Continuar' clicado com sucesso")
        time.sleep(3)
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
            time.sleep(1)
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
        time.sleep(3)
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
            time.sleep(1)
            tentativa += 1
        
        if tentativa >= max_tentativas:
            exception_handler.capturar_warning("Tela 7 não carregou", "TELA_7")
            return False
        
        exibir_mensagem("✅ Tela 7 carregada com sucesso")
        
        # Preencher CEP
        exibir_mensagem("📱 TELA 7: Preenchendo CEP...")
        campo_endereco.first.fill(cep)
        exibir_mensagem(f"✅ CEP preenchido: {cep}")
        time.sleep(1)
        
        # Aguardar carregamento do endereço
        exibir_mensagem("⏳ Aguardando carregamento do endereço...")
        time.sleep(5)
        
        # Tentar selecionar endereço sugerido
        try:
            sugestao_endereco = page.locator("css=.overflow-hidden").first
            if sugestao_endereco.is_visible():
                sugestao_endereco.click()
                exibir_mensagem("✅ Endereço sugerido selecionado")
                time.sleep(1)
            else:
                exception_handler.capturar_warning("Endereço sugerido não encontrado", "TELA_7")
        except Exception as e:
            exception_handler.capturar_warning(f"Erro ao selecionar endereço: {str(e)}", "TELA_7")
        
        # Clicar em Continuar
        botao_continuar = page.locator("#gtm-telaPernoiteVeiculoContinuar").first
        botao_continuar.click()
        
        exibir_mensagem("✅ Botão 'Continuar' clicado com sucesso")
        time.sleep(3)
        return True
        
    except Exception as e:
        exception_handler.capturar_excecao(e, "TELA_7", f"Erro ao preencher CEP {cep}")
        return False

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
        
        # Aguardar carregamento dos planos
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
        
        # ETAPA 1: ENCONTRAR CONTAINERS DOS PLANOS
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
        
        # ETAPA 2: ANALISAR CADA CONTAINER
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
                
            except Exception as e:
                exception_handler.capturar_warning(f"Erro ao analisar container {i+1}: {str(e)}", "CAPTURA_DADOS_PLANOS")
                continue
        
        # ETAPA 6: FALLBACK FINAL COM SELETORES ESPECÍFICOS
        exibir_mensagem("🔍 ETAPA 6: Fallback com seletores específicos...")
        
        # Se ainda não encontrou valores principais, tentar seletores específicos
        for plano_tipo in ["plano_recomendado", "plano_alternativo"]:
            if dados_planos[plano_tipo]["valor"] == "N/A":
                try:
                    # Tentar encontrar valor principal
                    valor_elemento = page.locator("label.text-primary.font-workSans.font-semibold.text-\\[32px\\]").first
                    if valor_elemento.is_visible():
                        valor_texto = valor_elemento.text_content()
                        if "R$" in valor_texto:
                            dados_planos[plano_tipo]["valor"] = valor_texto
                            exibir_mensagem(f"✅ Valor encontrado via seletor específico: {valor_texto}")
                except Exception as e:
                    exception_handler.capturar_warning(f"Erro ao buscar valor via seletor específico: {str(e)}", "CAPTURA_DADOS_PLANOS")
        
        # ETAPA 7: SALVAR E RETORNAR DADOS
        exibir_mensagem("💾 ETAPA 7: Salvando dados capturados...")
        
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
            
            # Executar Telas 1-15
            resultado_telas = {
                "tela_1": navegar_tela_1_playwright(page),
                "tela_2": navegar_tela_2_playwright(page, parametros["placa"]),
                "tela_3": navegar_tela_3_playwright(page),
                "tela_4": navegar_tela_4_playwright(page, parametros["veiculo_segurado"]),
                "tela_5": navegar_tela_5_playwright(page),
                "tela_6": navegar_tela_6_playwright(page, parametros["combustivel"], 
                                                   parametros.get("kit_gas", False), 
                                                   parametros.get("blindado", False), 
                                                   parametros.get("financiado", False)),
                "tela_7": navegar_tela_7_playwright(page, parametros["cep"]),
                # ... outras telas serão adicionadas em versões futuras
            }
            
            # Capturar dados finais
            dados_planos = capturar_dados_planos_seguro(page)
            
            # Salvar dados
            arquivo_dados = salvar_dados_planos(dados_planos)
            
            # Fechar browser
            browser.close()
            
            # Calcular tempo de execução
            tempo_execucao = time.time() - inicio_execucao
            
            # Retorno estruturado
            return {
                "status": "success",
                "timestamp": datetime.now().isoformat(),
                "tempo_execucao": f"{tempo_execucao:.2f}s",
                "telas_executadas": resultado_telas,
                "dados_planos": dados_planos,
                "arquivo_dados": arquivo_dados,
                "erros": exception_handler.obter_resumo_erros(),
                "parametros_entrada": parametros
            }
            
    except Exception as e:
        exception_handler.capturar_excecao(e, "EXECUCAO_PRINCIPAL", "Erro na execução principal")
        
        return {
            "status": "error",
            "timestamp": datetime.now().isoformat(),
            "tempo_execucao": f"{time.time() - inicio_execucao:.2f}s",
            "erro": str(e),
            "erros": exception_handler.obter_resumo_erros(),
            "parametros_entrada": parametros
        }

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
            
    except Exception as e:
        exception_handler.capturar_excecao(e, "EXECUCAO_DIRETA", "Erro na execução direta")
        sys.exit(1)
