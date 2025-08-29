#!/usr/bin/env python3
"""
Teste da Função de Retorno Estruturado para Frontend
====================================================

Este script demonstra como implementar e usar a função de retorno estruturado
que pode ser chamada por um frontend JavaScript ou qualquer outra aplicação.

VERSÃO: 2.3.0 - COM SISTEMA DE RETORNO ESTRUTURADO
DATA: 29/08/2025
"""

import json
import time
from datetime import datetime
import sys
import os

# Sistema de logging integrado
try:
    from utils.logger_rpa import rpa_logger, log_info, log_error, log_success, log_exception
    LOGGING_AVAILABLE = True
except ImportError:
    LOGGING_AVAILABLE = False
    print("⚠️ Sistema de logging não disponível. Usando print padrão.")

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
        "versao": "2.3.0",
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
        if not LOGGING_AVAILABLE:
            return None
            
        log_file = rpa_logger.get_log_file_path()
        if not log_file or not os.path.exists(log_file):
            return None
            
        with open(log_file, 'r', encoding='utf-8') as f:
            linhas = f.readlines()
            # Retornar as últimas linhas
            return [linha.strip() for linha in linhas[-max_linhas:]] if len(linhas) > max_linhas else [linha.strip() for linha in linhas]
            
    except Exception:
        return None

def simular_rpa_sucesso():
    """
    Simula uma execução bem-sucedida do RPA
    """
    print("🚀 Simulando execução bem-sucedida do RPA...")
    
    # Simular algum processamento
    time.sleep(1)
    
    # Dados extras de exemplo
    dados_extras = {
        "telas_executadas": 8,
        "tempo_execucao": "85.2s",
        "placa_processada": "KVA-1791",
        "url_final": "https://www.app.tosegurado.com.br/cotacao/resultado"
    }
    
    # Obter logs recentes
    logs_recentes = obter_logs_recentes(5)
    
    # Criar retorno estruturado de sucesso
    retorno = criar_retorno_estruturado(
        status="sucesso",
        codigo_erro=9002,
        dados_extras=dados_extras,
        logs_recentes=logs_recentes
    )
    
    return retorno

def simular_rpa_erro():
    """
    Simula uma execução com erro do RPA
    """
    print("❌ Simulando execução com erro do RPA...")
    
    # Simular algum processamento
    time.sleep(0.5)
    
    # Dados extras de exemplo para erro
    dados_extras = {
        "tela_falhou": 6,
        "elemento_nao_encontrado": "//button[contains(., 'Continuar')]",
        "tentativas_realizadas": 3,
        "ultimo_url": "https://www.app.tosegurado.com.br/cotacao/tela5"
    }
    
    # Criar retorno estruturado de erro
    retorno = criar_retorno_estruturado(
        status="erro",
        codigo_erro=2002,
        dados_extras=dados_extras
    )
    
    return retorno

def main():
    """
    Função principal - Testa os retornos estruturados
    """
    print("🧪 **TESTE DA FUNÇÃO DE RETORNO ESTRUTURADO**")
    print("=" * 60)
    print("📋 Este script demonstra como o RPA retorna dados para o frontend")
    print("=" * 60)
    
    # Teste 1: Retorno de sucesso
    print("\n🟢 **TESTE 1: RETORNO DE SUCESSO**")
    print("-" * 40)
    retorno_sucesso = simular_rpa_sucesso()
    
    print("📤 JSON de retorno para o frontend:")
    print(json.dumps(retorno_sucesso, indent=2, ensure_ascii=False))
    
    # Teste 2: Retorno de erro
    print("\n🔴 **TESTE 2: RETORNO DE ERRO**")
    print("-" * 40)
    retorno_erro = simular_rpa_erro()
    
    print("📤 JSON de retorno para o frontend:")
    print(json.dumps(retorno_erro, indent=2, ensure_ascii=False))
    
    # Teste 3: Como usar no frontend JavaScript
    print("\n💻 **EXEMPLO DE USO NO FRONTEND JAVASCRIPT**")
    print("-" * 50)
    
    exemplo_js = """
// Frontend JavaScript - Exemplo de uso
async function executarRPA() {
    try {
        const resultado = await fetch('/api/executar-rpa', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'}
        });
        
        const retorno = await resultado.json();
        
        if (retorno.status === 'sucesso') {
            console.log('✅ RPA executado com sucesso!');
            console.log('Código:', retorno.codigo);
            console.log('Mensagem:', retorno.mensagem);
            console.log('Dados:', retorno.dados);
            
            // Processar dados de sucesso
            if (retorno.dados) {
                document.getElementById('resultado').innerHTML = 
                    `RPA concluído em ${retorno.dados.tempo_execucao}`;
            }
            
        } else {
            console.error('❌ Erro no RPA:', retorno.mensagem);
            console.error('Código do erro:', retorno.codigo);
            
            // Mostrar mensagem de erro amigável para o usuário
            alert(retorno.mensagem);
        }
        
    } catch (error) {
        console.error('Erro na comunicação:', error);
    }
}
"""
    
    print(exemplo_js)
    
    print("\n✅ **RESUMO DOS BENEFÍCIOS**")
    print("-" * 30)
    print("🔹 Códigos de erro padronizados e compreensivos")
    print("🔹 Mensagens de erro amigáveis para o usuário")
    print("🔹 Estrutura JSON consistente")
    print("🔹 Informações extras contextuais")
    print("🔹 Logs recentes para debugging")
    print("🔹 Timestamp para auditoria")
    print("🔹 Versionamento do sistema")
    
    print(f"\n⏰ Teste concluído em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
