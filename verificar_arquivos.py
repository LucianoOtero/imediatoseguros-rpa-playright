#!/usr/bin/env python3
"""
Script para verificar se todos os arquivos necessários estão presentes
"""

import os
import sys
from pathlib import Path

def verificar_arquivos():
    """Verifica se todos os arquivos necessários estão presentes"""
    
    print("�� VERIFICANDO ARQUIVOS DO PROJETO...")
    print("=" * 60)
    
    # Lista de arquivos obrigatórios
    arquivos_obrigatorios = {
        # Arquivos principais
        "main.py": "Arquivo principal (Tela 1)",
        "executar_todas_telas.py": "Executor de todas as telas",
        "testar_telas_individual.py": "Testador individual de telas",
        "parametros.json": "Parâmetros de teste",
        
        # Diretório utils
        "utils/helpers.py": "Funções auxiliares",
        "utils/logger.py": "Sistema de logs",
        "utils/validacao.py": "Validação de parâmetros",
        "utils/relatorio.py": "Sistema de relatórios",
        
        # Diretório telas
        "telas/tela2_placa.py": "Tela 2 - Inserção de placa",
        "telas/tela3_confirmacao.py": "Tela 3 - Confirmação do veículo",
        "telas/tela4_segurado.py": "Tela 4 - Veículo já segurado",
        "telas/tela5_estimativa.py": "Tela 5 - Estimativa inicial",
        "telas/tela6_combustivel.py": "Tela 6 - Tipo de combustível",
        "telas/tela7_endereco.py": "Tela 7 - Endereço de pernoite",
        "telas/tela8_finalidade.py": "Tela 8 - Finalidade do veículo",
        "telas/tela9_dados.py": "Tela 9 - Dados pessoais",
        "telas/tela10_contato.py": "Tela 10 - Contato",
        "telas/tela11_coberturas.py": "Tela 11 - Coberturas adicionais",
        "telas/tela12_finalizacao.py": "Tela 12 - Finalização",
        
        # Arquivos de configuração
        "config.py": "Configurações do ambiente",
        "requirements.txt": "Dependências Python",
        
        # Arquivos .bat para Windows
        "install.bat": "Instalador de dependências",
        "run.bat": "Execução rápida",
        "test.bat": "Teste individual",
        "clean.bat": "Limpeza de arquivos"
    }
    
    # Lista de diretórios obrigatórios
    diretorios_obrigatorios = [
        "utils",
        "telas",
        "relatorios",
        "logs"
    ]
    
    # Verificar arquivos
    arquivos_faltando = []
    arquivos_presentes = []
    
    print("�� VERIFICANDO ARQUIVOS:")
    print("-" * 40)
    
    for arquivo, descricao in arquivos_obrigatorios.items():
        if os.path.exists(arquivo):
            tamanho = os.path.getsize(arquivo)
            status = "✅"
            arquivos_presentes.append(arquivo)
            print(f"{status} {arquivo:<30} ({descricao:<25}) - {tamanho:,} bytes")
        else:
            status = "❌"
            arquivos_faltando.append(arquivo)
            print(f"{status} {arquivo:<30} ({descricao:<25}) - FALTANDO")
    
    print("\n�� VERIFICANDO DIRETÓRIOS:")
    print("-" * 40)
    
    diretorios_faltando = []
    for diretorio in diretorios_obrigatorios:
        if os.path.exists(diretorio) and os.path.isdir(diretorio):
            arquivos_no_dir = len([f for f in os.listdir(diretorio) if os.path.isfile(os.path.join(diretorio, f))])
            print(f"✅ {diretorio:<20} - {arquivos_no_dir} arquivos")
        else:
            print(f"❌ {diretorio:<20} - FALTANDO")
            diretorios_faltando.append(diretorio)
    
    # Verificar ambiente virtual
    print("\n🐍 VERIFICANDO AMBIENTE PYTHON:")
    print("-" * 40)
    
    if os.path.exists("venv"):
        print("✅ Ambiente virtual 'venv' encontrado")
        if os.path.exists("venv/Scripts/activate.bat"):
            print("✅ Script de ativação encontrado")
        else:
            print("❌ Script de ativação não encontrado")
    else:
        print("❌ Ambiente virtual 'venv' não encontrado")
    
    # Verificar dependências Python
    print("\n�� VERIFICANDO DEPENDÊNCIAS PYTHON:")
    print("-" * 40)
    
    try:
        import selenium
        print(f"✅ Selenium {selenium.__version__}")
    except ImportError:
        print("❌ Selenium não instalado")
    
    try:
        import webdriver_manager
        print(f"✅ WebDriver Manager {webdriver_manager.__version__}")
    except ImportError:
        print("❌ WebDriver Manager não instalado")
    
    # Resumo
    print("\n" + "=" * 60)
    print("�� RESUMO DA VERIFICAÇÃO:")
    print("=" * 60)
    
    total_arquivos = len(arquivos_obrigatorios)
    arquivos_ok = len(arquivos_presentes)
    arquivos_faltando_count = len(arquivos_faltando)
    
    print(f"�� Total de arquivos: {total_arquivos}")
    print(f"✅ Arquivos presentes: {arquivos_ok}")
    print(f"❌ Arquivos faltando: {arquivos_faltando_count}")
    print(f"📂 Diretórios faltando: {len(diretorios_faltando)}")
    
    if arquivos_faltando_count == 0 and len(diretorios_faltando) == 0:
        print("\n🎉 TODOS OS ARQUIVOS ESTÃO PRESENTES!")
        print("✅ O projeto está pronto para execução!")
    else:
        print(f"\n⚠️  ARQUIVOS FALTANDO ({arquivos_faltando_count}):")
        for arquivo in arquivos_faltando:
            print(f"   ❌ {arquivo}")
        
        print(f"\n⚠️  DIRETÓRIOS FALTANDO ({len(diretorios_faltando)}):")
        for diretorio in diretorios_faltando:
            print(f"   ❌ {diretorio}")
    
    print("\n" + "=" * 60)
    
    return arquivos_faltando_count == 0 and len(diretorios_faltando) == 0

if __name__ == "__main__":
    verificar_arquivos()
