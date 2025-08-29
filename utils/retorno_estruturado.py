#!/usr/bin/env python3
"""
Módulo de Retorno Estruturado para RPA Tô Segurado
===================================================

Este módulo implementa funções para criar retornos estruturados
padronizados para frontend/API, incluindo códigos de erro e sucesso.

VERSÃO: 2.4.0
DATA: 29/08/2025
"""

import json
import time
from datetime import datetime
import os

def criar_retorno_estruturado(status, codigo_erro=None, dados_extras=None, logs_recentes=None):
    """
    Cria um retorno estruturado para o frontend com códigos de sucesso/erro padronizados

    Args:
        status: 'sucesso' ou 'erro'
        codigo_erro: Código de erro da tabela (1000-9999)
        dados_extras: Dicionário com dados adicionais
        logs_recentes: Lista de logs recentes para incluir no retorno

    Returns:
        Dicionário estruturado com retorno completo
    """

    # Códigos de sucesso e mensagens
    CODIGOS_SUCESSO = {
        9001: "Tela executada com sucesso",
        9002: "RPA executado com sucesso",
        9003: "Elemento encontrado e processado",
        9004: "Ação realizada com sucesso"
    }

    # Códigos de erro e mensagens compreensivas
    CODIGOS_ERRO = {
        # Erros de configuração (1000-1999)
        1001: "Erro ao carregar arquivo de configuração - Verifique se o arquivo parametros.json existe e está válido",
        1002: "Configuração inválida ou incompleta - Verifique a estrutura do arquivo de configuração",
        1003: "Erro no ChromeDriver - Verifique se o ChromeDriver está instalado e acessível",
        1004: "Erro ao inicializar navegador - Verifique as configurações do Chrome e permissões",

        # Erros de navegação (2000-2999)
        2001: "Timeout na navegação - A página demorou muito para carregar, verifique a conexão",
        2002: "Elemento não encontrado na página - A estrutura da página pode ter mudado",
        2003: "Elemento não está clicável - O elemento existe mas não pode ser interagido",
        2004: "Página não carregou completamente - Aguarde mais tempo ou verifique a conexão",
        2005: "Erro no redirecionamento - Problema na navegação entre páginas",

        # Erros de automação (3000-3999)
        3001: "Falha ao clicar no elemento - Elemento pode estar sobreposto ou não visível",
        3002: "Falha ao inserir dados no campo - Campo pode estar desabilitado ou inválido",
        3003: "Timeout aguardando elemento - Elemento não apareceu no tempo esperado",
        3004: "Elemento obsoleto (stale) - A página foi recarregada, tente novamente",
        3005: "Erro na execução de JavaScript - Problema na interação com a página",

        # Erros de sistema (4000-4999)
        4001: "Erro de conexão de rede - Verifique sua conexão com a internet",
        4002: "Erro de memória insuficiente - Feche outros programas e tente novamente",
        4003: "Erro de disco/arquivo - Verifique o espaço em disco e permissões",
        4004: "Erro de permissão - Execute como administrador se necessário",

        # Erros de validação (5000-5999)
        5001: "Dados inválidos fornecidos - Verifique os dados de entrada",
        5002: "Formato de dados incorreto - Verifique o formato dos dados",
        5003: "Validação falhou - Dados não passaram na validação"
    }

    # Estrutura base do retorno
    retorno = {
        "status": status,
        "timestamp": datetime.now().isoformat(),
        "versao": "2.4.0",
        "sistema": "RPA Tô Segurado"
    }

    if status == "sucesso":
        # Retorno de sucesso
        if codigo_erro and codigo_erro in CODIGOS_SUCESSO:
            retorno.update({
                "codigo": codigo_erro,
                "mensagem": CODIGOS_SUCESSO[codigo_erro],
                "tipo": "sucesso"
            })
        else:
            retorno.update({
                "codigo": 9002,
                "mensagem": "RPA executado com sucesso",
                "tipo": "sucesso"
            })

        # Adicionar dados extras se fornecidos
        if dados_extras:
            retorno["dados"] = dados_extras

        # Adicionar logs recentes se solicitado
        if logs_recentes:
            retorno["logs"] = logs_recentes

    else:
        # Retorno de erro
        if codigo_erro and codigo_erro in CODIGOS_ERRO:
            retorno.update({
                "codigo": codigo_erro,
                "mensagem": CODIGOS_ERRO[codigo_erro],
                "tipo": "erro"
            })
        else:
            retorno.update({
                "codigo": 4001,
                "mensagem": "Erro desconhecido durante a execução",
                "tipo": "erro"
            })

        # Adicionar dados extras se fornecidos
        if dados_extras:
            retorno["dados"] = dados_extras

    return retorno

def obter_logs_recentes(max_linhas=10):
    """
    Obtém os logs mais recentes do arquivo de log

    Args:
        max_linhas: Número máximo de linhas de log a retornar

    Returns:
        Lista de logs recentes ou None se não disponível
    """
    try:
        # Tentar obter logs do sistema de logging se disponível
        try:
            from utils.logger_rpa import rpa_logger
            log_file = rpa_logger.get_log_file_path()
            if log_file and os.path.exists(log_file):
                with open(log_file, 'r', encoding='utf-8') as f:
                    linhas = f.readlines()
                    # Retornar as últimas linhas
                    return [linha.strip() for linha in linhas[-max_linhas:]] if len(linhas) > max_linhas else [linha.strip() for linha in linhas]
        except ImportError:
            pass

        # Fallback: procurar por arquivos de log comuns
        arquivos_log = [
            "rpa.log",
            "logs/rpa.log",
            "temp/rpa.log"
        ]
        
        for arquivo in arquivos_log:
            if os.path.exists(arquivo):
                try:
                    with open(arquivo, 'r', encoding='utf-8') as f:
                        linhas = f.readlines()
                        return [linha.strip() for linha in linhas[-max_linhas:]] if len(linhas) > max_linhas else [linha.strip() for linha in linhas]
                except:
                    continue

        return None

    except Exception:
        return None

def main():
    """Função principal para teste do módulo"""
    print("🧪 **TESTE DO MÓDULO DE RETORNO ESTRUTURADO**")
    print("=" * 60)
    
    # Teste 1: Retorno de sucesso
    print("\n🟢 **TESTE 1: RETORNO DE SUCESSO**")
    print("-" * 40)
    
    dados_extras = {
        "telas_executadas": 8,
        "tempo_execucao": "85.2s",
        "placa_processada": "ABC1234",
        "url_final": "https://www.app.tosegurado.com.br/cotacao/resultado"
    }
    
    retorno_sucesso = criar_retorno_estruturado(
        status="sucesso",
        codigo_erro=9002,
        dados_extras=dados_extras
    )
    
    print("📤 JSON de retorno para o frontend:")
    print(json.dumps(retorno_sucesso, indent=2, ensure_ascii=False))
    
    # Teste 2: Retorno de erro
    print("\n🔴 **TESTE 2: RETORNO DE ERRO**")
    print("-" * 40)
    
    dados_extras_erro = {
        "tela_falhou": 6,
        "elemento_nao_encontrado": "//button[contains(., 'Continuar')]",
        "tentativas_realizadas": 3,
        "ultimo_url": "https://www.app.tosegurado.com.br/cotacao/tela5"
    }
    
    retorno_erro = criar_retorno_estruturado(
        status="erro",
        codigo_erro=2002,
        dados_extras=dados_extras_erro
    )
    
    print("📤 JSON de retorno para o frontend:")
    print(json.dumps(retorno_erro, indent=2, ensure_ascii=False))
    
    # Teste 3: Obter logs recentes
    print("\n📝 **TESTE 3: LOGS RECENTES**")
    print("-" * 40)
    
    logs = obter_logs_recentes(5)
    if logs:
        print(f"✅ Logs encontrados: {len(logs)} linhas")
        for i, log in enumerate(logs, 1):
            print(f"   {i}: {log[:100]}...")
    else:
        print("⚠️ Nenhum log encontrado")
    
    print(f"\n⏰ Teste concluído em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
