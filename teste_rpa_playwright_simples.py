#!/usr/bin/env python3
"""
TESTE SIMPLES DO RPA PLAYWRIGHT
Script para testar o RPA Playwright de forma direta
"""

import json
import sys
from executar_rpa_playwright import executar_todas_telas_playwright

def main():
    """Função principal"""
    print("🚀 TESTE SIMPLES DO RPA PLAYWRIGHT")
    print("=" * 50)
    
    try:
        # Carregar parâmetros
        with open('parametros.json', 'r', encoding='utf-8') as f:
            parametros = json.load(f)
        
        print("✅ Parâmetros carregados com sucesso")
        print(f"📧 Email: {parametros['autenticacao']['email_login']}")
        print(f"🚗 Placa: {parametros['placa']}")
        print(f"👤 Nome: {parametros['nome']}")
        
        # Executar RPA
        print("\n🔄 INICIANDO RPA PLAYWRIGHT...")
        print("=" * 50)
        
        resultado = executar_todas_telas_playwright(json.dumps(parametros))
        
        # Exibir resultado
        print("\n📊 RESULTADO:")
        print("=" * 30)
        
        if resultado.get('status') == 'sucesso':
            print("✅ RPA EXECUTADO COM SUCESSO!")
            print(f"📈 Tecnologia: {resultado['data']['tecnologia']}")
            print(f"📱 Telas navegadas: {resultado['data']['telas_navegadas']}")
            print(f"🔐 Login: {'Sim' if resultado['data']['login_sucesso'] else 'Não'}")
            print(f"💰 Dados capturados: {len(resultado['data']['dados_capturados'])} itens")
        else:
            print("❌ RPA FALHOU!")
            print(f"🔍 Erro: {resultado['mensagem']}")
            print(f"📝 Código: {resultado['codigo']}")
        
        return 0
        
    except Exception as e:
        print(f"❌ ERRO CRÍTICO: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())

