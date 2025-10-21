#!/usr/bin/env python3
"""
🚀 SETUP TEST ENVIRONMENT - SISTEMA DE LOGGING PHP
Configura ambiente de teste local para Windows
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def main():
    """Função principal de configuração"""
    print("🚀 Configurando ambiente de teste...")
    
    # Verificar Python
    check_python_version()
    
    # Instalar dependências
    install_dependencies()
    
    # Criar diretórios necessários
    create_directories()
    
    # Verificar conectividade
    check_connectivity()
    
    print("✅ Ambiente configurado com sucesso!")
    print("\n📋 Próximos passos:")
    print("1. Execute: python test_runner.py --all")
    print("2. Verifique os resultados em: results/")
    print("3. Abra o relatório HTML no navegador")

def check_python_version():
    """Verifica versão do Python"""
    print("🐍 Verificando versão do Python...")
    
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ é necessário!")
        print(f"   Versão atual: {sys.version}")
        sys.exit(1)
    
    print(f"✅ Python {sys.version.split()[0]} detectado")

def install_dependencies():
    """Instala dependências Python"""
    print("📦 Instalando dependências...")
    
    requirements_file = Path(__file__).parent / 'requirements.txt'
    
    if not requirements_file.exists():
        print("❌ Arquivo requirements.txt não encontrado!")
        sys.exit(1)
    
    try:
        subprocess.run([
            sys.executable, '-m', 'pip', 'install', '-r', str(requirements_file)
        ], check=True, capture_output=True)
        print("✅ Dependências instaladas com sucesso")
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar dependências: {e}")
        print("   Tente executar manualmente: pip install -r requirements.txt")
        sys.exit(1)

def create_directories():
    """Cria diretórios necessários"""
    print("📁 Criando diretórios...")
    
    base_dir = Path(__file__).parent
    
    directories = [
        'config',
        'results',
        'logs',
        'data'
    ]
    
    for directory in directories:
        dir_path = base_dir / directory
        dir_path.mkdir(exist_ok=True)
        print(f"   ✅ {directory}/")
    
    # Criar arquivo .gitignore
    gitignore_content = """
# Resultados de teste
results/*.html
results/*.json
results/*.csv

# Logs
logs/*.log

# Configurações sensíveis
config/*.json

# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.venv/
pip-log.txt
pip-delete-this-directory.txt

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
"""
    
    gitignore_path = base_dir / '.gitignore'
    with open(gitignore_path, 'w', encoding='utf-8') as f:
        f.write(gitignore_content.strip())
    
    print("   ✅ .gitignore")

def check_connectivity():
    """Verifica conectividade básica"""
    print("🌐 Verificando conectividade...")
    
    try:
        import requests
        
        # Testar conectividade com bpsegurosimediato.com.br
        response = requests.get('http://bpsegurosimediato.com.br:8080', timeout=10)
        if response.status_code == 200:
            print("✅ Conectividade com bpsegurosimediato.com.br OK")
        else:
            print(f"⚠️ bpsegurosimediato.com.br retornou status {response.status_code}")
            
    except ImportError:
        print("⚠️ requests não instalado - conectividade não verificada")
    except Exception as e:
        print(f"⚠️ Erro de conectividade: {e}")

if __name__ == "__main__":
    main()


