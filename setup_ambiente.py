#!/usr/bin/env python3
"""
🖥️ SCRIPT DE INSTALAÇÃO AUTOMATIZADA - IMEDIATO SEGUROS RPA
================================================================

Este script automatiza a instalação de todos os componentes necessários
para o ambiente de desenvolvimento do RPA Imediato Seguros.

USO:
    python setup_ambiente.py

FUNCIONALIDADES:
- Verifica versão do Python
- Instala dependências Python
- Instala navegadores Playwright
- Configura ambiente virtual
- Testa instalação

AUTOR: Luciano Otero
DATA: 04/09/2025
VERSÃO: 1.0.0
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def exibir_mensagem(mensagem: str, tipo: str = "INFO"):
    """Exibe mensagem formatada"""
    cores = {
        "INFO": "\033[94m",    # Azul
        "SUCCESS": "\033[92m", # Verde
        "WARNING": "\033[93m", # Amarelo
        "ERROR": "\033[91m",    # Vermelho
        "RESET": "\033[0m"     # Reset
    }
    
    timestamp = subprocess.run(['date', '+%H:%M:%S'], 
                             capture_output=True, text=True).stdout.strip()
    print(f"{cores.get(tipo, '')}[{timestamp}] {mensagem}{cores['RESET']}")

def executar_comando(comando: str, descricao: str = "") -> bool:
    """Executa comando e retorna sucesso"""
    try:
        if descricao:
            exibir_mensagem(f"Executando: {descricao}")
        
        resultado = subprocess.run(comando, shell=True, check=True, 
                                 capture_output=True, text=True)
        
        if resultado.stdout:
            print(resultado.stdout)
        
        exibir_mensagem(f"✅ {descricao} - SUCESSO", "SUCCESS")
        return True
        
    except subprocess.CalledProcessError as e:
        exibir_mensagem(f"❌ {descricao} - ERRO: {e}", "ERROR")
        if e.stderr:
            print(f"Erro detalhado: {e.stderr}")
        return False

def verificar_python():
    """Verifica se Python está instalado"""
    exibir_mensagem("🔍 Verificando versão do Python...")
    
    try:
        versao = subprocess.run([sys.executable, '--version'], 
                              capture_output=True, text=True).stdout.strip()
        exibir_mensagem(f"✅ Python encontrado: {versao}", "SUCCESS")
        return True
    except Exception as e:
        exibir_mensagem(f"❌ Python não encontrado: {e}", "ERROR")
        return False

def verificar_pip():
    """Verifica se pip está disponível"""
    exibir_mensagem("🔍 Verificando pip...")
    
    try:
        versao = subprocess.run([sys.executable, '-m', 'pip', '--version'], 
                              capture_output=True, text=True).stdout.strip()
        exibir_mensagem(f"✅ Pip encontrado: {versao}", "SUCCESS")
        return True
    except Exception as e:
        exibir_mensagem(f"❌ Pip não encontrado: {e}", "ERROR")
        return False

def criar_ambiente_virtual():
    """Cria ambiente virtual Python"""
    exibir_mensagem("🔧 Criando ambiente virtual...")
    
    if os.path.exists("venv"):
        exibir_mensagem("⚠️ Ambiente virtual já existe", "WARNING")
        return True
    
    return executar_comando(f"{sys.executable} -m venv venv", 
                          "Criação do ambiente virtual")

def ativar_ambiente_virtual():
    """Ativa ambiente virtual"""
    exibir_mensagem("🔧 Ativando ambiente virtual...")
    
    if platform.system() == "Windows":
        script_ativacao = "venv\\Scripts\\activate"
    else:
        script_ativacao = "source venv/bin/activate"
    
    exibir_mensagem("ℹ️ Para ativar o ambiente virtual, execute:", "INFO")
    print(f"    {script_ativacao}")
    
    return True

def instalar_dependencias():
    """Instala dependências Python"""
    exibir_mensagem("📦 Instalando dependências Python...")
    
    # Atualizar pip primeiro
    executar_comando(f"{sys.executable} -m pip install --upgrade pip", 
                    "Atualização do pip")
    
    # Instalar dependências do requirements.txt
    if os.path.exists("requirements.txt"):
        return executar_comando(f"{sys.executable} -m pip install -r requirements.txt", 
                              "Instalação das dependências")
    else:
        exibir_mensagem("❌ Arquivo requirements.txt não encontrado", "ERROR")
        return False

def instalar_playwright():
    """Instala Playwright e navegadores"""
    exibir_mensagem("🌐 Instalando Playwright...")
    
    # Instalar Playwright
    if not executar_comando(f"{sys.executable} -m pip install playwright==1.55.0", 
                          "Instalação do Playwright"):
        return False
    
    # Instalar navegadores
    exibir_mensagem("🌐 Instalando navegadores Playwright...")
    return executar_comando(f"{sys.executable} -m playwright install", 
                          "Instalação dos navegadores")

def verificar_playwright():
    """Verifica instalação do Playwright"""
    exibir_mensagem("🔍 Verificando instalação do Playwright...")
    
    try:
        versao = subprocess.run([sys.executable, '-m', 'playwright', '--version'], 
                              capture_output=True, text=True).stdout.strip()
        exibir_mensagem(f"✅ Playwright encontrado: {versao}", "SUCCESS")
        return True
    except Exception as e:
        exibir_mensagem(f"❌ Playwright não encontrado: {e}", "ERROR")
        return False

def listar_navegadores():
    """Lista navegadores instalados"""
    exibir_mensagem("🔍 Listando navegadores instalados...")
    
    try:
        resultado = subprocess.run([sys.executable, '-m', 'playwright', 'install', '--list'], 
                                 capture_output=True, text=True)
        print(resultado.stdout)
        return True
    except Exception as e:
        exibir_mensagem(f"❌ Erro ao listar navegadores: {e}", "ERROR")
        return False

def testar_instalacao():
    """Testa instalação básica"""
    exibir_mensagem("🧪 Testando instalação...")
    
    testes = [
        ("Python", f"{sys.executable} --version"),
        ("Pip", f"{sys.executable} -m pip --version"),
        ("Playwright", f"{sys.executable} -m playwright --version"),
    ]
    
    sucessos = 0
    for nome, comando in testes:
        try:
            resultado = subprocess.run(comando, shell=True, capture_output=True, text=True)
            if resultado.returncode == 0:
                exibir_mensagem(f"✅ {nome}: OK", "SUCCESS")
                sucessos += 1
            else:
                exibir_mensagem(f"❌ {nome}: FALHOU", "ERROR")
        except Exception as e:
            exibir_mensagem(f"❌ {nome}: ERRO - {e}", "ERROR")
    
    return sucessos == len(testes)

def criar_arquivo_env():
    """Cria arquivo .env básico"""
    exibir_mensagem("🔧 Criando arquivo .env...")
    
    conteudo_env = """# 🐍 ARQUIVO DE CONFIGURAÇÃO DO AMBIENTE
# Data de Criação: 04/09/2025

# Configurações Python
PYTHONPATH=.

# Configurações Playwright
PLAYWRIGHT_BROWSERS_PATH=C:\\Users\\%USERNAME%\\AppData\\Local\\ms-playwright

# Configurações do RPA
RPA_LOG_LEVEL=INFO
RPA_TIMEOUT=30
RPA_RETRY_ATTEMPTS=3

# Configurações de Autenticação (preencher conforme necessário)
# EMAIL_LOGIN=seu_email@exemplo.com
# SENHA_LOGIN=sua_senha
"""
    
    try:
        with open(".env", "w", encoding="utf-8") as f:
            f.write(conteudo_env)
        exibir_mensagem("✅ Arquivo .env criado com sucesso", "SUCCESS")
        return True
    except Exception as e:
        exibir_mensagem(f"❌ Erro ao criar .env: {e}", "ERROR")
        return False

def exibir_instrucoes_finais():
    """Exibe instruções finais"""
    exibir_mensagem("🎉 INSTALAÇÃO CONCLUÍDA!", "SUCCESS")
    print("\n" + "="*60)
    print("📋 PRÓXIMOS PASSOS:")
    print("="*60)
    
    instrucoes = [
        "1. Ative o ambiente virtual:",
        "   Windows: venv\\Scripts\\activate",
        "   Linux/Mac: source venv/bin/activate",
        "",
        "2. Configure o arquivo parametros.json com seus dados",
        "",
        "3. Teste o RPA:",
        "   python executar_rpa_imediato_playwright.py --help",
        "",
        "4. Execute o RPA:",
        "   python executar_rpa_imediato_playwright.py",
        "",
        "📚 Documentação completa: AMBIENTE_DE_DESENVOLVIMENTO_COMPLETO.md",
        "",
        "🔧 Suporte: lrotero@gmail.com"
    ]
    
    for instrucao in instrucoes:
        print(instrucao)

def main():
    """Função principal"""
    print("🖥️ SCRIPT DE INSTALAÇÃO AUTOMATIZADA - IMEDIATO SEGUROS RPA")
    print("="*70)
    print(f"📅 Data: {subprocess.run(['date'], capture_output=True, text=True).stdout.strip()}")
    print(f"💻 Sistema: {platform.system()} {platform.release()}")
    print(f"🐍 Python: {sys.version}")
    print("="*70)
    
    # Verificações iniciais
    if not verificar_python():
        exibir_mensagem("❌ Python não encontrado. Instale Python 3.13.7+ primeiro.", "ERROR")
        return False
    
    if not verificar_pip():
        exibir_mensagem("❌ Pip não encontrado. Instale pip primeiro.", "ERROR")
        return False
    
    # Instalação
    sucesso = True
    
    sucesso &= criar_ambiente_virtual()
    sucesso &= ativar_ambiente_virtual()
    sucesso &= instalar_dependencias()
    sucesso &= instalar_playwright()
    sucesso &= verificar_playwright()
    sucesso &= listar_navegadores()
    sucesso &= criar_arquivo_env()
    sucesso &= testar_instalacao()
    
    if sucesso:
        exibir_instrucoes_finais()
        exibir_mensagem("✅ INSTALAÇÃO CONCLUÍDA COM SUCESSO!", "SUCCESS")
        return True
    else:
        exibir_mensagem("❌ INSTALAÇÃO FALHOU. Verifique os erros acima.", "ERROR")
        return False

if __name__ == "__main__":
    try:
        sucesso = main()
        sys.exit(0 if sucesso else 1)
    except KeyboardInterrupt:
        exibir_mensagem("⚠️ Instalação interrompida pelo usuário", "WARNING")
        sys.exit(1)
    except Exception as e:
        exibir_mensagem(f"❌ Erro inesperado: {e}", "ERROR")
        sys.exit(1)

























