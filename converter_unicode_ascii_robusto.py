#!/usr/bin/env python3
"""
CONVERSOR UNICODE → ASCII ROBUSTO
Resolve problemas de codificação no terminal Windows (cp1252)

Este script converte TODAS as saídas Unicode para ASCII,
interceptando stdout, stderr e todas as funções de saída.
"""

import sys
import os
import re
import io
from pathlib import Path

def carregar_substituicoes():
    """Carrega o mapeamento de substituições APENAS para emojis"""
    
    # Substituições APENAS para emojis e símbolos especiais
    # NÃO converter acentos portugueses (À, á, ç, etc.)
    substituicoes = {
        # Emojis de status
        '✅': '[OK]', '❌': '[ERROR]', '⚠️': '[WARNING]', 'ℹ️': '[INFO]',
        
        # Emojis de ferramentas
        '🔧': '[CORRIGINDO]', '⚙️': '[GEAR]', '🔨': '[HAMMER]', '🛠️': '[TOOLS]',
        
        # Emojis de navegação
        '🌐': '[ACESSANDO]', '🔗': '[LINK]', '📡': '[SATELLITE]',
        
        # Emojis de interface
        '📱': '[PHONE]', '💻': '[LAPTOP]', '🖥️': '[DESKTOP]', '🖱️': '[MOUSE]',
        
        # Emojis de dados
        '📊': '[PROCESSANDO]', '📈': '[CHART_UP]', '📉': '[CHART_DOWN]', '📋': '[PROC-LISTA]',
        
        # Emojis de tempo
        '⏰': '[CLOCK]', '⏱️': '[TIMER]', '⏳': '[AGUARDE]', '⏸️': '[PAUSE]',
        
        # Emojis de arte
        '🎨': '[ESTILIZANDO]', '🎭': '[THEATER]', '🎬': '[MOVIE]', '🎮': '[GAME]', '🎯': '[PROGRESSO]',
        
        # Emojis outros
        '⭐': '[STAR]', '🌟': '[SPARKLE]', '🎉': '[PROGRESSO]', '🏆': '[TROPHY]',
        '💡': '[IDEA]', '🔥': '[FIRE]', '🚀': '[INICIANDO]',
        
        # Emojis de veículos
        '🚗': '[CAR]', '🚙': '[SUV]', '🏎️': '[RACING]',
        
        # Caracteres especiais (não acentos)
        '⚡': '[FAST]', '⛽': '[FUEL]', '✏️': '[PENCIL]', '❓': '[QUESTION]',
        
        # Símbolos técnicos (não acentos)
        '£': '[LIBRA]', 'ª': '[ORDINAL]', '•': '[BULLET]', 'ℹ': '[INFO]',
        '←': '[LEFT]', '→': '[RIGHT]', '↓': '[DOWN]',
        '─': '[HORIZONTAL]', '│': '[VERTICAL]', '└': '[CORNER]', '├': '[T]',
        '▶': '[PLAY]', '☑️': '[CHECKBOX]', '✓': '[CHECK]',
        '➕': '[PLUS]', '➖': '[MINUS]', '➡': '[ARROW]',
        
        # Outros emojis comuns no projeto
        '🆕': '[NEW]', '🎁': '[GIFT]', '🎛️': '[KNOBS]', '🎠': '[CAROUSEL]',
        '🏗️': '[CONSTRUCTION]', '🏠': '[HOUSE]', '🏢': '[HOME]', '🏷️': '[LABEL]',
        '🐍': '[PYTHON]', '🐛': '[BUG]', '👁️': '[EYE]', '👤': '[USER]', '👥': '[GROUP]',
        '👦': '[BOY]', '👧': '[GIRL]', '👨': '[MAN]', '👩': '[WOMAN]',
        '💬': '[CHAT]', '💰': '[MONEY]', '💵': '[CASH]', '💾': '[SAVE]',
        '📁': '[FOLDER]', '📂': '[OPEN_FOLDER]', '📄': '[DOCUMENTANDO]', '📅': '[CALENDAR]',
        '📍': '[PIN]', '📏': '[RULER]', '📖': '[BOOK]', '📚': '[BOOKS]',
        '📝': '[OBS]', '📞': '[CONECTANDO]', '📤': '[UPLOAD]', '📥': '[DOWNLOAD]',
        '📦': '[PACKAGE]', '📧': '[EMAIL]', '📸': '[CAPTURANDO]', '📺': '[TV]', '📻': '[RADIO]',
        '🔄': '[SINCRONIZANDO]', '🔇': '[MUTE]', '🔍': '[PROCURANDO]', '🔐': '[LOCK]',
        '🔒': '[LOCKED]', '🔘': '[RADIO_BUTTON]', '🔚': '[END]', '🔢': '[NUMBERS]',
        '🔬': '[MICROSCOPE]', '🔮': '[CRYSTAL_BALL]', '🔴': '[RED]', '🔸': '[DIAMOND]',
        '🔹': '[BLUE_DIAMOND]', '🔽': '[DOWN_ARROW]', '🗑️': '[DEL]', '🙏': '[PRAY]',
        '🚦': '[TRAFFIC_LIGHT]', '🚨': '[POLICE]', '🚫': '[FORBIDDEN]',
        '🛡️': '[SAFE]', '🟢': '[GREEN]', '🤖': '[ROBOT]', '🤝': '[HANDSHAKE]',
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

class UnicodeConverterStream:
    """Stream que converte Unicode para ASCII em tempo real"""
    
    def __init__(self, stream_original, substituicoes):
        self.stream_original = stream_original
        self.substituicoes = substituicoes
        self.buffer = ""
    
    def write(self, texto):
        """Intercepta e converte texto antes de escrever"""
        if texto:
            # Converter texto Unicode para ASCII
            texto_convertido = converter_texto(texto, self.substituicoes)
            
            # Escrever no stream original
            self.stream_original.write(texto_convertido)
    
    def flush(self):
        """Força flush do buffer"""
        if hasattr(self.stream_original, 'flush'):
            self.stream_original.flush()
    
    def __getattr__(self, attr):
        """Delega outros atributos para o stream original"""
        return getattr(self.stream_original, attr)

def interceptar_todas_saidas():
    """Intercepta TODAS as saídas: stdout, stderr e print"""
    
    substituicoes = carregar_substituicoes()
    
    # 1. Interceptar stdout
    stdout_original = sys.stdout
    sys.stdout = UnicodeConverterStream(stdout_original, substituicoes)
    
    # 2. Interceptar stderr
    stderr_original = sys.stderr
    sys.stderr = UnicodeConverterStream(stderr_original, substituicoes)
    
    # 3. Interceptar função print
    print_original = print
    
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
    globals()['print'] = print_convertido
    
    return stdout_original, stderr_original, print_original

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

# ATIVAR CONVERSOR ROBUSTO IMEDIATAMENTE AO IMPORTAR
stdout_original, stderr_original, print_original = interceptar_todas_saidas()
configurar_ambiente()

def main():
    """Função principal"""
    
    print("🔧 CONVERSOR UNICODE → ASCII ROBUSTO ATIVADO")
    print("=" * 70)
    print("✅ Resolvendo problemas de codificação no Windows")
    print("✅ Convertendo TODAS as saídas para ASCII compreensível")
    print("✅ Interceptando stdout, stderr e print")
    print("✅ PRESERVANDO acentos portugueses intactos")
    print("✅ Compatível com PHP shell_exec, exec, passthru")
    print()
    
    print("🎯 Sistema configurado com sucesso!")
    print("📱 Todos os emojis serão convertidos automaticamente")
    print("🇧🇷 Acentos portugueses serão preservados")
    print("💻 Compatível com terminal Windows (cp1252)")
    print("🔄 Todas as saídas interceptadas e convertidas")
    print()
    
    # Exemplo de conversão
    print("🔍 EXEMPLO DE CONVERSÃO:")
    print("   Unicode: ✅ Sucesso! ❌ Erro! 🔧 Configurando...")
    print("   ASCII:   [OK] Sucesso! [ERROR] Erro! [CORRIGINDO] Configurando...")
    print()
    
    # Exemplo com acentos preservados
    print("🇧🇷 EXEMPLO COM ACENTOS PRESERVADOS:")
    print("   Configuração, operação, veículo, segurado")
    print("   Acentos portugueses funcionando perfeitamente!")
    print()
    
    # Teste de saída direta para stdout
    sys.stdout.write("🔍 Teste direto para stdout: ✅ ❌ 🔧\n")
    sys.stderr.write("⚠️ Teste direto para stderr: ⚠️ ℹ️\n")
    
    return True

if __name__ == "__main__":
    main()
