#!/usr/bin/env python3
"""
Teste de debug para o campo veiculo_segurado
"""

import json
import sys

def testar_veiculo_segurado():
    """Testa especificamente o campo veiculo_segurado"""
    
    print("🔍 **DEBUG DO CAMPO VEICULO_SEGURADO**")
    print("="*50)
    
    # Ler o arquivo parametros.json
    try:
        with open('parametros.json', 'r', encoding='utf-8') as f:
            conteudo = f.read()
            print(f"📄 Conteúdo do arquivo (primeiros 200 chars):")
            print(f"'{conteudo[:200]}'")
            print()
            
            parametros = json.loads(conteudo)
            valor = parametros.get('veiculo_segurado')
            
            print(f"📋 Valor lido: '{valor}'")
            print(f"📋 Tipo: {type(valor)}")
            print(f"📋 Comprimento: {len(valor)}")
            print(f"📋 Bytes: {valor.encode('utf-8')}")
            print(f"📋 ASCII: {repr(valor)}")
            
            # Valores válidos
            veiculo_segurado_validos = ["Sim", "Não"]
            print(f"\n📋 Valores válidos: {veiculo_segurado_validos}")
            
            # Testar cada valor válido
            for i, valido in enumerate(veiculo_segurado_validos):
                print(f"📋 Valor válido {i+1}: '{valido}' (tipo: {type(valido)}, len: {len(valido)}, bytes: {valido.encode('utf-8')})")
                print(f"   Comparação direta: {valor == valido}")
                print(f"   Comparação case-insensitive: {valor.lower() == valido.lower()}")
            
            # Verificar se está na lista
            esta_na_lista = valor in veiculo_segurado_validos
            print(f"\n📋 Está na lista de valores válidos? {esta_na_lista}")
            
            if not esta_na_lista:
                print("❌ **PROBLEMA IDENTIFICADO**")
                print(f"   Valor recebido: '{valor}'")
                print(f"   Valores aceitos: {veiculo_segurado_validos}")
                
                # Tentar normalizar
                valor_normalizado = valor.replace('ã', 'a').replace('Ã', 'A')
                print(f"   Valor normalizado: '{valor_normalizado}'")
                
                if valor_normalizado in ["Sim", "Nao"]:
                    print("   ✅ Problema de codificação identificado!")
                    return valor_normalizado
                    
    except Exception as e:
        print(f"❌ Erro ao ler arquivo: {str(e)}")
        return None
    
    return valor

if __name__ == "__main__":
    resultado = testar_veiculo_segurado()
    print(f"\n🎯 Resultado final: {resultado}")
