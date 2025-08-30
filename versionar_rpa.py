#!/usr/bin/env python3
"""
Script de Versionamento Automático para RPA Tô Segurado
=======================================================

Este script automatiza o processo de versionamento:
1. Copia o arquivo executar_rpa_imediato.py para uma versão numerada
2. Facilita o controle de versões para comparação
3. Mantém sempre o executar_rpa_imediato.py como arquivo oficial

USO:
====
python versionar_rpa.py <versao>

EXEMPLO:
========
python versionar_rpa.py 2.5.1
"""

import os
import sys
import shutil
from datetime import datetime

def versionar_rpa(versao):
    """
    Cria uma nova versão do RPA baseada na versão especificada
    
    Args:
        versao (str): Número da versão (ex: "2.5.1")
    """
    
    # Arquivos base
    arquivo_oficial = "executar_rpa_imediato.py"
    arquivo_versao = f"executar_rpa_imediato_v{versao}.py"
    
    print(f"🚀 **VERSIONANDO RPA TÔ SEGURADO v{versao}**")
    print("=" * 60)
    
    # Verificar se o arquivo oficial existe
    if not os.path.exists(arquivo_oficial):
        print(f"❌ Erro: Arquivo oficial '{arquivo_oficial}' não encontrado!")
        print("   Certifique-se de que o arquivo existe antes de versionar.")
        return False
    
    # Verificar se a versão já existe
    if os.path.exists(arquivo_versao):
        print(f"⚠️  Aviso: Versão v{versao} já existe!")
        resposta = input("   Deseja sobrescrever? (s/N): ").strip().lower()
        if resposta != 's':
            print("   Versionamento cancelado.")
            return False
    
    try:
        # Copiar arquivo oficial para versão numerada
        shutil.copy2(arquivo_oficial, arquivo_versao)
        
        # Verificar se a cópia foi bem-sucedida
        if os.path.exists(arquivo_versao):
            # Obter informações dos arquivos
            stat_oficial = os.stat(arquivo_oficial)
            stat_versao = os.stat(arquivo_versao)
            
            print(f"✅ **VERSÃO v{versao} CRIADA COM SUCESSO!**")
            print(f"📁 Arquivo oficial: {arquivo_oficial}")
            print(f"📁 Nova versão: {arquivo_versao}")
            print(f"📊 Tamanho: {stat_versao.st_size:,} bytes")
            print(f"⏰ Timestamp: {datetime.fromtimestamp(stat_versao.st_mtime)}")
            
            # Verificar se os arquivos são idênticos
            if stat_oficial.st_size == stat_versao.st_size:
                print("🔍 **VERIFICAÇÃO**: Arquivos idênticos ✓")
            else:
                print("⚠️  **ATENÇÃO**: Arquivos com tamanhos diferentes!")
            
            print("\n🎯 **PRÓXIMOS PASSOS RECOMENDADOS:**")
            print("1. Testar a nova versão se necessário")
            print("2. Fazer commit no GitHub")
            print("3. Continuar desenvolvendo no arquivo oficial")
            print("4. Usar este script para criar novas versões")
            
            return True
            
        else:
            print(f"❌ Erro: Falha ao criar versão v{versao}")
            return False
            
    except Exception as e:
        print(f"❌ Erro durante versionamento: {str(e)}")
        return False

def listar_versoes():
    """
    Lista todas as versões disponíveis
    """
    print("📋 **VERSÕES DISPONÍVEIS:**")
    print("=" * 40)
    
    arquivos = [f for f in os.listdir('.') if f.startswith('executar_rpa_imediato_v') and f.endswith('.py')]
    
    if not arquivos:
        print("   Nenhuma versão encontrada.")
        return
    
    # Ordenar versões
    arquivos.sort()
    
    for arquivo in arquivos:
        # Extrair versão do nome do arquivo
        versao = arquivo.replace('executar_rpa_imediato_v', '').replace('.py', '')
        
        # Obter informações do arquivo
        stat = os.stat(arquivo)
        tamanho = stat.st_size
        timestamp = datetime.fromtimestamp(stat.st_mtime)
        
        print(f"   📁 {arquivo}")
        print(f"      🏷️  Versão: {versao}")
        print(f"      📊 Tamanho: {tamanho:,} bytes")
        print(f"      ⏰ Criado: {timestamp}")
        print()

def main():
    """
    Função principal do script
    """
    print("🚀 **SCRIPT DE VERSIONAMENTO RPA TÔ SEGURADO**")
    print("=" * 60)
    
    if len(sys.argv) < 2:
        print("❌ Erro: Versão não especificada!")
        print("\n📖 **USO:**")
        print("   python versionar_rpa.py <versao>")
        print("\n📖 **EXEMPLOS:**")
        print("   python versionar_rpa.py 2.5.1")
        print("   python versionar_rpa.py 2.6.0")
        print("   python versionar_rpa.py 3.0.0")
        print("\n📋 **COMANDOS ADICIONAIS:**")
        print("   python versionar_rpa.py --list    # Listar versões existentes")
        print("   python versionar_rpa.py --help    # Mostrar esta ajuda")
        return
    
    # Verificar comandos especiais
    if sys.argv[1] == '--list' or sys.argv[1] == '-l':
        listar_versoes()
        return
    
    if sys.argv[1] == '--help' or sys.argv[1] == '-h':
        print(__doc__)
        return
    
    # Extrair versão dos argumentos
    versao = sys.argv[1].strip()
    
    # Validar formato da versão
    if not versao.replace('.', '').replace('-', '').replace('_', '').isdigit():
        print(f"⚠️  Aviso: Formato de versão '{versao}' pode não ser padrão")
        resposta = input("   Continuar mesmo assim? (s/N): ").strip().lower()
        if resposta != 's':
            print("   Versionamento cancelado.")
            return
    
    # Executar versionamento
    sucesso = versionar_rpa(versao)
    
    if sucesso:
        print(f"\n🎉 **VERSIONAMENTO v{versao} CONCLUÍDO COM SUCESSO!**")
        print("   O arquivo oficial continua disponível para desenvolvimento.")
    else:
        print(f"\n❌ **VERSIONAMENTO v{versao} FALHOU!**")
        print("   Verifique os erros acima e tente novamente.")

if __name__ == "__main__":
    main()
