#!/usr/bin/env python3
"""
Script para remover APENAS emojis, preservando acentos portugueses
"""

import re
import os
import glob

def limpar_apenas_emojis(texto):
    """
    Remove apenas emojis, preservando acentos portugueses
    """
    # Mapeamento de emojis comuns para texto
    emoji_map = {
        '🚀': '[INICIANDO]',
        '🎯': '[OBJETIVO]',
        '✅': '[OK]',
        '❌': '[ERRO]',
        '⚠️': '[AVISO]',
        '🔧': '[CONFIG]',
        '📋': '[INFO]',
        '🎉': '[SUCESSO]',
        '🚗': '[VEICULO]',
        '🛡': '[SEGURO]',
        '🏷': '[TAG]',
        '🏢': '[EMPRESA]',
        '👥': '[USUARIOS]',
        '🎁': '[PRESENTE]',
        '💬': '[MENSAGEM]',
        '📅': '[DATA]',
        '📖': '[DOCUMENTO]',
        'ℹ': '[INFO]',
        '🔟': '[10]',
        '🔒': '[BLOQUEADO]',
        '👶': '[CRIANCA]',
        '💰': '[DINHEIRO]',
        '→': '->',
        '🚨': '[ALERTA]',
        '📸': '[FOTO]',
        '⏰': '[TEMPO]',
        '💻': '[COMPUTADOR]',
        '🔍': '[BUSCAR]',
        '🔗': '[LINK]',
        '📝': '[NOTA]',
        '🏠': '[CASA]',
        '🛵': '[MOTO]',
        '📱': '[CELULAR]',
        '🅿': '[P]',
        '🚫': '[PROIBIDO]',
        '📧': '[EMAIL]',
        '←': '<-',
        '⏳': '[AGUARDANDO]',
        '🔄': '[ATUALIZANDO]',
        '💼': '[TRABALHO]',
        '💾': '[SALVAR]',
        '📈': '[GRAFICO]',
        '⚙': '[CONFIG]',
        '📁': '[PASTA]',
        '•': '*',
        '👤': '[USUARIO]',
        '📍': '[LOCALIZACAO]',
        '🎪': '[EVENTO]',
        '💡': '[IDEIA]',
        '📊': '[DADOS]',
        '👨': '[HOMEM]',
        '🧪': '[TESTE]',
        '1️⃣': '1',
        '2️⃣': '2',
        '3️⃣': '3',
        '4️⃣': '4',
        '5️⃣': '5',
        '6️⃣': '6',
        '7️⃣': '7',
        '8️⃣': '8',
        '9️⃣': '9',
        '0️⃣': '0',
        'c️⃣': 'c',
        'a️⃣': 'a',
        'b️⃣': 'b',
        'd️⃣': 'd',
        'e️⃣': 'e',
        'f️⃣': 'f',
        'g️⃣': 'g',
        'h️⃣': 'h',
        'i️⃣': 'i',
        'j️⃣': 'j',
        'k️⃣': 'k',
        'l️⃣': 'l',
        'm️⃣': 'm',
        'n️⃣': 'n',
        'o️⃣': 'o',
        'p️⃣': 'p',
        'q️⃣': 'q',
        'r️⃣': 'r',
        's️⃣': 's',
        't️⃣': 't',
        'u️⃣': 'u',
        'v️⃣': 'v',
        'w️⃣': 'w',
        'x️⃣': 'x',
        'y️⃣': 'y',
        'z️⃣': 'z'
    }
    
    # Aplicar mapeamento de emojis
    for emoji, replacement in emoji_map.items():
        texto = texto.replace(emoji, replacement)
    
    # Remover apenas emojis Unicode, preservando acentos portugueses
    # Padrão para emojis: caracteres Unicode que não são letras acentuadas
    texto = re.sub(r'[\U0001F600-\U0001F64F]', '', texto)  # Emoticons
    texto = re.sub(r'[\U0001F300-\U0001F5FF]', '', texto)  # Símbolos e pictogramas
    texto = re.sub(r'[\U0001F680-\U0001F6FF]', '', texto)  # Transporte
    texto = re.sub(r'[\U0001F1E0-\U0001F1FF]', '', texto)  # Bandeiras
    texto = re.sub(r'[\U00002600-\U000026FF]', '', texto)   # Símbolos diversos
    texto = re.sub(r'[\U00002700-\U000027BF]', '', texto)  # Dingbats
    texto = re.sub(r'[\U0001F900-\U0001F9FF]', '', texto)  # Símbolos suplementares
    texto = re.sub(r'[\U0001FA70-\U0001FAFF]', '', texto)  # Símbolos e pictogramas estendidos
    
    return texto

def processar_arquivo(arquivo):
    """
    Processa um arquivo Python preservando acentos
    """
    print(f"[CONFIG] Processando {arquivo}...")
    
    try:
        # Ler arquivo
        with open(arquivo, 'r', encoding='utf-8') as f:
            conteudo = f.read()
        
        # Contar emojis antes
        emojis_antes = len(re.findall(r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF\U00002600-\U000026FF\U00002700-\U000027BF\U0001F900-\U0001F9FF\U0001FA70-\U0001FAFF]', conteudo))
        
        if emojis_antes > 0:
            print(f"[INFO] Emojis encontrados: {emojis_antes}")
            
            # Limpar apenas emojis
            conteudo_limpo = limpar_apenas_emojis(conteudo)
            
            # Contar emojis depois
            emojis_depois = len(re.findall(r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF\U00002600-\U000026FF\U00002700-\U000027BF\U0001F900-\U0001F9FF\U0001FA70-\U0001FAFF]', conteudo_limpo))
            
            # Salvar arquivo
            with open(arquivo, 'w', encoding='utf-8') as f:
                f.write(conteudo_limpo)
            
            print(f"[OK] Removidos {emojis_antes - emojis_depois} emojis de {arquivo}")
        else:
            print(f"[OK] Nenhum emoji encontrado em {arquivo}")
            
    except Exception as e:
        print(f"[ERRO] Erro ao processar {arquivo}: {e}")

def processar_todos_arquivos():
    """
    Processa todos os arquivos Python preservando acentos
    """
    print("[INICIANDO] Removendo APENAS emojis, preservando acentos portugueses...")
    
    # Encontrar todos os arquivos Python
    arquivos_python = []
    
    # Arquivo principal
    if os.path.exists('executar_rpa_imediato_playwright.py'):
        arquivos_python.append('executar_rpa_imediato_playwright.py')
    
    # Arquivos na pasta utils
    for arquivo in glob.glob('utils/*.py'):
        arquivos_python.append(arquivo)
    
    # Processar cada arquivo
    for arquivo in arquivos_python:
        processar_arquivo(arquivo)
    
    print("[SUCESSO] Todos os arquivos processados preservando acentos!")

if __name__ == "__main__":
    processar_todos_arquivos()







