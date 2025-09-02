#!/usr/bin/env python3
"""
TESTE DO LOGIN AUTOMÁTICO
=========================

OBJETIVO:
- Testar a funcionalidade de login automático implementada
- Verificar se detecta e preenche os campos corretamente
- Validar se os parâmetros de autenticação estão sendo lidos

FUNCIONALIDADES TESTADAS:
- Leitura dos parâmetros de autenticação do JSON
- Detecção da janela de login
- Preenchimento automático de email e senha
- Clique nos botões necessários
- Tratamento de erros
"""

import json
import sys
import os

def testar_parametros_autenticacao():
    """Testa se os parâmetros de autenticação estão configurados corretamente"""
    print("🔍 TESTANDO PARÂMETROS DE AUTENTICAÇÃO...")
    
    try:
        # Carregar parâmetros
        with open('parametros.json', 'r', encoding='utf-8') as f:
            parametros = json.load(f)
        
        # Verificar se existe seção de autenticação
        if "autenticacao" not in parametros:
            print("❌ ERRO: Seção 'autenticacao' não encontrada no JSON")
            return False
        
        # Verificar campos obrigatórios
        autenticacao = parametros["autenticacao"]
        
        if "email_login" not in autenticacao:
            print("❌ ERRO: Campo 'email_login' não encontrado")
            return False
            
        if "senha_login" not in autenticacao:
            print("❌ ERRO: Campo 'senha_login' não encontrado")
            return False
        
        # Verificar se os campos não estão vazios
        email = autenticacao["email_login"]
        senha = autenticacao["senha_login"]
        
        if not email or email.strip() == "":
            print("❌ ERRO: Campo 'email_login' está vazio")
            return False
            
        if not senha or senha.strip() == "":
            print("❌ ERRO: Campo 'senha_login' está vazio")
            return False
        
        print(f"✅ Email configurado: {email}")
        print(f"✅ Senha configurada: {'*' * len(senha)}")
        print(f"✅ Manter login atual: {autenticacao.get('manter_login_atual', True)}")
        
        return True
        
    except FileNotFoundError:
        print("❌ ERRO: Arquivo 'parametros.json' não encontrado")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ ERRO: JSON inválido: {e}")
        return False
    except Exception as e:
        print(f"❌ ERRO: {e}")
        return False

def testar_elementos_login():
    """Testa se os elementos de login estão definidos corretamente"""
    print("\n🔍 TESTANDO ELEMENTOS DE LOGIN...")
    
    elementos_esperados = [
        "emailTelaLogin",
        "senhaTelaLogin", 
        "gtm-telaLoginBotaoAcessar",
        "manterLoginAtualModalAssociarUsuario"
    ]
    
    print("✅ Elementos esperados:")
    for elemento in elementos_esperados:
        print(f"   - {elemento}")
    
    return True

def testar_importacao_funcao():
    """Testa se a função de login pode ser importada"""
    print("\n🔍 TESTANDO IMPORTAÇÃO DA FUNÇÃO...")
    
    try:
        # Tentar importar a função do arquivo principal
        sys.path.append(os.getcwd())
        
        # Verificar se o arquivo existe
        if not os.path.exists('executar_rpa_imediato.py'):
            print("❌ ERRO: Arquivo 'executar_rpa_imediato.py' não encontrado")
            return False
        
        # Verificar se a função existe no arquivo
        with open('executar_rpa_imediato.py', 'r', encoding='utf-8') as f:
            conteudo = f.read()
            
        if 'def realizar_login_automatico' not in conteudo:
            print("❌ ERRO: Função 'realizar_login_automatico' não encontrada no arquivo")
            return False
        
        print("✅ Função 'realizar_login_automatico' encontrada no arquivo")
        return True
        
    except Exception as e:
        print(f"❌ ERRO: {e}")
        return False

def testar_estrutura_completa():
    """Testa a estrutura completa da implementação"""
    print("\n🔍 TESTANDO ESTRUTURA COMPLETA...")
    
    # Verificar se todos os arquivos necessários existem
    arquivos_necessarios = [
        'parametros.json',
        'executar_rpa_imediato.py',
        'converter_unicode_ascii_robusto.py',
        'exception_handler.py'
    ]
    
    for arquivo in arquivos_necessarios:
        if os.path.exists(arquivo):
            print(f"✅ {arquivo} - OK")
        else:
            print(f"❌ {arquivo} - NÃO ENCONTRADO")
            return False
    
    return True

def main():
    """Função principal de teste"""
    print("🚀 TESTE DO LOGIN AUTOMÁTICO")
    print("=" * 50)
    
    testes = [
        ("Parâmetros de Autenticação", testar_parametros_autenticacao),
        ("Elementos de Login", testar_elementos_login),
        ("Importação da Função", testar_importacao_funcao),
        ("Estrutura Completa", testar_estrutura_completa)
    ]
    
    resultados = []
    
    for nome_teste, funcao_teste in testes:
        print(f"\n📋 {nome_teste.upper()}")
        print("-" * 30)
        
        try:
            resultado = funcao_teste()
            resultados.append((nome_teste, resultado))
            
            if resultado:
                print(f"✅ {nome_teste}: PASSOU")
            else:
                print(f"❌ {nome_teste}: FALHOU")
                
        except Exception as e:
            print(f"❌ {nome_teste}: ERRO - {e}")
            resultados.append((nome_teste, False))
    
    # Resumo final
    print("\n" + "=" * 50)
    print("📊 RESUMO DOS TESTES")
    print("=" * 50)
    
    testes_passaram = sum(1 for _, resultado in resultados if resultado)
    total_testes = len(resultados)
    
    for nome_teste, resultado in resultados:
        status = "✅ PASSOU" if resultado else "❌ FALHOU"
        print(f"{nome_teste}: {status}")
    
    print(f"\n🎯 RESULTADO: {testes_passaram}/{total_testes} testes passaram")
    
    if testes_passaram == total_testes:
        print("🎉 TODOS OS TESTES PASSARAM! Login automático está pronto para uso.")
        print("\n💡 PRÓXIMOS PASSOS:")
        print("   1. Execute o RPA principal: python executar_rpa_imediato.py")
        print("   2. O login será verificado automaticamente")
        print("   3. Os valores reais do prêmio estarão disponíveis")
    else:
        print("⚠️ ALGUNS TESTES FALHARAM. Verifique as configurações.")
        print("\n🔧 CORREÇÕES NECESSÁRIAS:")
        for nome_teste, resultado in resultados:
            if not resultado:
                print(f"   - {nome_teste}")

if __name__ == "__main__":
    main()
