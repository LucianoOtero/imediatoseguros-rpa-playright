#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EXEMPLO DE USO - LIMPADOR DE COMENTÁRIOS JAVASCRIPT
==================================================

Script de exemplo para demonstrar o uso do limpador de comentários.
"""

from limpar_comentarios_js import LimpadorComentariosJS
import os

def exemplo_uso():
    """Demonstra como usar o limpador de comentários."""
    
    print("🧹 EXEMPLO DE USO - LIMPADOR DE COMENTÁRIOS")
    print("=" * 50)
    
    # Arquivo de exemplo para limpeza
    arquivo_entrada = "webflow_injection_definitivo.js"
    
    # Verificar se arquivo existe
    if not os.path.exists(arquivo_entrada):
        print(f"❌ Arquivo não encontrado: {arquivo_entrada}")
        print("💡 Certifique-se de que o arquivo está no diretório atual")
        return
    
    # Criar instância do limpador
    limpador = LimpadorComentariosJS()
    
    # Processar arquivo
    print(f"🔄 Processando arquivo: {arquivo_entrada}")
    sucesso = limpador.processar_completo(arquivo_entrada)
    
    if sucesso:
        print("\n✅ Arquivo processado com sucesso!")
        print("📁 Arquivos gerados:")
        print(f"   - Backup: {limpador.arquivo_backup.name}")
        print(f"   - Limpo: webflow_injection_definitivo_limpo.js")
    else:
        print("\n❌ Falha no processamento!")

def limpar_multiplos_arquivos():
    """Exemplo para limpar múltiplos arquivos."""
    
    print("\n🔄 LIMPEZA DE MÚLTIPLOS ARQUIVOS")
    print("=" * 50)
    
    # Lista de arquivos para limpar
    arquivos = [
        "webflow_injection_definitivo.js",
        "Footer Code Site Definitivo.js"
    ]
    
    for arquivo in arquivos:
        if os.path.exists(arquivo):
            print(f"\n🔄 Processando: {arquivo}")
            limpador = LimpadorComentariosJS()
            sucesso = limpador.processar_completo(arquivo)
            
            if sucesso:
                print(f"✅ {arquivo} processado!")
            else:
                print(f"❌ Falha ao processar {arquivo}")
        else:
            print(f"⚠️ Arquivo não encontrado: {arquivo}")

if __name__ == "__main__":
    # Executar exemplo principal
    exemplo_uso()
    
    # Executar exemplo de múltiplos arquivos
    limpar_multiplos_arquivos()

