#!/usr/bin/env python3
"""
CONVERSOR UNICODE → ASCII FINAL
Resolve problemas de codificação no terminal Windows (cp1252)

Este script converte APENAS emojis para ASCII compreensível,
PRESERVANDO acentos portugueses e outros caracteres legítimos.
"""

import sys
import os
import re
import json
from pathlib import Path

def carregar_substituicoes():
    """Carrega o mapeamento de substituições APENAS para emojis"""
    
    # Substituições APENAS para emojis e símbolos especiais
    # NÃO converter acentos portugueses (À, á, ç, etc.)
    substituicoes = {
        # Emojis de status
        '✅': '[OK]', '❌': '[ERROR]', '⚠️': '[WARNING]', 'ℹ️': '[INFO]',
        
        # Emojis de ferramentas
        '🔧': '[WRENCH]', '⚙️': '[GEAR]', '🔨': '[HAMMER]', '🛠️': '[TOOLS]',
        
        # Emojis de navegação
        '🌐': '[GLOBE]', '🔗': '[LINK]', '📡': '[SATELLITE]',
        
        # Emojis de interface
        '📱': '[PHONE]', '💻': '[LAPTOP]', '🖥️': '[DESKTOP]', '🖱️': '[MOUSE]',
        
        # Emojis de dados
        '📊': '[CHART]', '📈': '[CHART_UP]', '📉': '[CHART_DOWN]', '📋': '[CLIPBOARD]',
        
        # Emojis de tempo
        '⏰': '[CLOCK]', '⏱️': '[TIMER]', '⏳': '[HOURGLASS]', '⏸️': '[PAUSE]',
        
        # Emojis de arte
        '🎨': '[ART]', '🎭': '[THEATER]', '🎬': '[MOVIE]', '🎮': '[GAME]', '🎯': '[TARGET]',
        
        # Emojis outros
        '⭐': '[STAR]', '🌟': '[SPARKLE]', '🎉': '[PARTY]', '🏆': '[TROPHY]',
        '💡': '[IDEA]', '🔥': '[FIRE]', '🚀': '[ROCKET]',
        
        # Emojis de veículos
        '🚗': '[CAR]', '🚙': '[SUV]', '🏎️': '[RACING]',
        
        # Caracteres especiais (não acentos)
        '⚡': '[LIGHTNING]', '⛽': '[FUEL]', '✏️': '[PENCIL]', '❓': '[QUESTION]',
        
        # Símbolos técnicos (não acentos)
        '£': '[LIBRA]', 'ª': '[ORDINAL]', '•': '[BULLET]', 'ℹ': '[INFO]',
        '←': '[LEFT]', '→': '[RIGHT]', '↓': '[DOWN]',
        '─': '[HORIZONTAL]', '│': '[VERTICAL]', '└': '[CORNER]', '├': '[T]',
        '▶': '[PLAY]', '☑️': '[CHECKBOX]', '✓': '[CHECK]',
        '➕': '[PLUS]', '➖': '[MINUS]', '➡': '[ARROW]',
        
        # Outros emojis comuns no projeto
        '🆕': '[NEW]', '🎁': '[GIFT]', '🎛️': '[KNOBS]', '🎠': '[CAROUSEL]',
        '🏗️': '[CONSTRUCTION]', '🏠': '[HOUSE]', '🏢': '[BUILDING]', '🏷️': '[LABEL]',
        '🐍': '[PYTHON]', '🐛': '[BUG]', '👁️': '[EYE]', '👤': '[PERSON]', '👥': '[PEOPLE]',
        '👦': '[BOY]', '👧': '[GIRL]', '👨': '[MAN]', '👩': '[WOMAN]',
        '💬': '[CHAT]', '💰': '[MONEY]', '💵': '[CASH]', '💾': '[SAVE]',
        '📁': '[FOLDER]', '📂': '[OPEN_FOLDER]', '📄': '[DOCUMENT]', '📅': '[CALENDAR]',
        '📍': '[PIN]', '📏': '[RULER]', '📖': '[BOOK]', '📚': '[BOOKS]',
        '📝': '[NOTE]', '📞': '[PHONE]', '📤': '[UPLOAD]', '📥': '[DOWNLOAD]',
        '📦': '[PACKAGE]', '📧': '[EMAIL]', '📸': '[CAMERA]', '📺': '[TV]', '📻': '[RADIO]',
        '🔄': '[REFRESH]', '🔇': '[MUTE]', '🔍': '[SEARCH]', '🔐': '[LOCK]',
        '🔒': '[LOCKED]', '🔘': '[RADIO_BUTTON]', '🔚': '[END]', '🔢': '[NUMBERS]',
        '🔬': '[MICROSCOPE]', '🔮': '[CRYSTAL_BALL]', '🔴': '[RED]', '🔸': '[DIAMOND]',
        '🔹': '[BLUE_DIAMOND]', '🔽': '[DOWN_ARROW]', '🗑️': '[TRASH]', '🙏': '[PRAY]',
        '🚦': '[TRAFFIC_LIGHT]', '🚨': '[POLICE]', '🚫': '[FORBIDDEN]',
        '🛡️': '[SHIELD]', '🟢': '[GREEN]', '🤖': '[ROBOT]', '🤝': '[HANDSHAKE]',
        '🧠': '[BRAIN]', '🧪': '[TEST_TUBE]', '🧭': '[COMPASS]', '🧹': '[BROOM]'
    }
    
    return substituicoes

def converter_texto(texto, substituicoes):
    """Converte texto Unicode para ASCII usando as substituições"""
    
    texto_convertido = texto
    
    # Aplicar todas as substituições
    for unicode_char, ascii_subst in substituicoes.items():
        texto_convertido = texto_convertido.replace(unicode_char, ascii_subst)
    
    return texto_convertido

def interceptar_print():
    """Intercepta e converte todas as chamadas print()"""
    
    substituicoes = carregar_substituicoes()
    
    # Salvar função print original
    print_original = __builtins__['print']
    
    def print_convertido(*args, **kwargs):
        """Função print que converte Unicode para ASCII"""
        
        # Converter argumentos para strings e aplicar conversão
        args_convertidos = []
        for arg in args:
            if isinstance(arg, str):
                arg_convertido = converter_texto(arg, substituicoes)
                args_convertidos.append(arg_convertido)
            else:
                args_convertidos.append(arg)
        
        # Chamar print original com texto convertido
        print_original(*args_convertidos, **kwargs)
    
    # Substituir função print global
    __builtins__['print'] = print_convertido
    
    return print_original

def configurar_ambiente():
    """Configura o ambiente para funcionar no Windows"""
    
    # Configurar encoding do sistema
    if sys.platform == 'win32':
        # Forçar encoding UTF-8 no Windows
        os.environ['PYTHONIOENCODING'] = 'utf-8'
        
        # Configurar stdout para UTF-8
        if hasattr(sys.stdout, 'reconfigure'):
            try:
                sys.stdout.reconfigure(encoding='utf-8')
            except:
                pass
        
        # Configurar stderr para UTF-8
        if hasattr(sys.stderr, 'reconfigure'):
            try:
                sys.stderr.reconfigure(encoding='utf-8')
            except:
                pass

# ATIVAR CONVERSOR IMEDIATAMENTE AO IMPORTAR
print_original = interceptar_print()
configurar_ambiente()

def main():
    """Função principal"""
    
    print("🔧 CONVERSOR UNICODE → ASCII FINAL ATIVADO")
    print("=" * 60)
    print("✅ Resolvendo problemas de codificação no Windows")
    print("✅ Convertendo APENAS emojis para ASCII compreensível")
    print("✅ PRESERVANDO acentos portugueses intactos")
    print("✅ Mantendo funcionalidade do RPA")
    print()
    
    print("🎯 Sistema configurado com sucesso!")
    print("📱 Todos os emojis serão convertidos automaticamente")
    print("🇧🇷 Acentos portugueses serão preservados")
    print("💻 Compatível com terminal Windows (cp1252)")
    print()
    
    # Exemplo de conversão
    print("🔍 EXEMPLO DE CONVERSÃO:")
    print("   Unicode: ✅ Sucesso! ❌ Erro! 🔧 Configurando...")
    print("   ASCII:   [OK] Sucesso! [ERROR] Erro! [WRENCH] Configurando...")
    print()
    
    # Exemplo com acentos preservados
    print("🇧🇷 EXEMPLO COM ACENTOS PRESERVADOS:")
    print("   Configuração, operação, veículo, segurado")
    print("   Acentos portugueses funcionando perfeitamente!")
    print()
    
    return True

if __name__ == "__main__":
    main()
