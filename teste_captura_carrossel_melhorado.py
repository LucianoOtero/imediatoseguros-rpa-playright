#!/usr/bin/env python3
"""
Teste da nova funcionalidade de captura de dados do carrossel
Demonstra a captura estruturada de valores "de" e "até" e benefícios organizados
"""

import json
from datetime import datetime

def simular_captura_carrossel_melhorado():
    """
    Simula a captura de dados do carrossel com a nova estrutura
    """
    print("📊 **SIMULANDO CAPTURA MELHORADA DO CARROSSEL**")
    
    # Dados simulados baseados nos elementos reais descritos pelo usuário
    dados_carrossel = {
        "timestamp": datetime.now().isoformat(),
        "tela": 5,
        "nome_tela": "Estimativa Inicial",
        "url": "https://www.app.tosegurado.com.br/imediatoseguros/estimativa",
        "titulo": "Estimativa de Seguro - Tô Segurado",
        "coberturas_detalhadas": [
            {
                "indice": 1,
                "nome_cobertura": "Compreensiva",
                "valores": {
                    "de": "R$ 1.200,00",
                    "ate": "R$ 1.700,00"
                },
                "beneficios": [
                    "Colisão e Acidentes",
                    "Roubo e Furto", 
                    "Incêndio",
                    "Danos a terceiros",
                    "Assistência 24h",
                    "Carro Reserva",
                    "Vidros"
                ],
                "texto_completo": "Cobertura Compreensiva\nDe R$ 1.200,00 até R$ 1.700,00\ncom possibilidade de parcelamento sem juros\nPrincipais Benefícios\nColisão e Acidentes\nRoubo e Furto\nIncêndio\nDanos a terceiros\nAssistência 24h\nCarro Reserva\nVidros"
            },
            {
                "indice": 2,
                "nome_cobertura": "Roubo e Furto",
                "valores": {
                    "de": "R$ 1.200,00",
                    "ate": "R$ 1.500,00"
                },
                "beneficios": [
                    "Roubo",
                    "Furto",
                    "Danos parciais em tentativas de roubo"
                ],
                "texto_completo": "Cobertura Roubo e Furto\nDe R$ 1.200,00 até R$ 1.500,00\ncom possibilidade de parcelamento sem juros\nPrincipais Benefícios\nRoubo\nFurto\nDanos parciais em tentativas de roubo"
            },
            {
                "indice": 3,
                "nome_cobertura": "RCF",
                "valores": {
                    "de": "R$ 900,00",
                    "ate": "R$ 1.400,00"
                },
                "beneficios": [
                    "Danos materiais a terceiros",
                    "Danos corporais a terceiro"
                ],
                "texto_completo": "Cobertura RCF\nDe R$ 900,00 até R$ 1.400,00\ncom possibilidade de parcelamento sem juros\nPrincipais Benefícios\nDanos materiais a terceiros\nDanos corporais a terceiro"
            }
        ],
        "beneficios_gerais": [
            {
                "nome": "Colisão e Acidentes",
                "encontrado": True,
                "quantidade_elementos": 1
            },
            {
                "nome": "Roubo e Furto",
                "encontrado": True,
                "quantidade_elementos": 2
            },
            {
                "nome": "Incêndio",
                "encontrado": True,
                "quantidade_elementos": 1
            },
            {
                "nome": "Danos a terceiros",
                "encontrado": True,
                "quantidade_elementos": 1
            },
            {
                "nome": "Assistência 24h",
                "encontrado": True,
                "quantidade_elementos": 1
            },
            {
                "nome": "Carro Reserva",
                "encontrado": True,
                "quantidade_elementos": 1
            },
            {
                "nome": "Vidros",
                "encontrado": True,
                "quantidade_elementos": 1
            },
            {
                "nome": "Danos parciais em tentativas de roubo",
                "encontrado": True,
                "quantidade_elementos": 1
            },
            {
                "nome": "Danos materiais a terceiros",
                "encontrado": True,
                "quantidade_elementos": 1
            },
            {
                "nome": "Danos corporais a terceiro",
                "encontrado": True,
                "quantidade_elementos": 1
            }
        ],
        "valores_encontrados": 6,
        "seguradoras": [],
        "elementos_detectados": [
            "carrossel_detectado",
            "cards_cobertura: 3",
            "palavra_chave: estimativa",
            "palavra_chave: cobertura",
            "palavra_chave: valor"
        ]
    }
    
    return dados_carrossel

def exibir_resultado_detalhado(dados):
    """
    Exibe o resultado da captura de forma detalhada
    """
    print("\n" + "="*60)
    print("🎯 **RETORNO INTERMEDIÁRIO MELHORADO**")
    print("="*60)
    
    print(f"📊 **COBERTURAS DETALHADAS**: {len(dados['coberturas_detalhadas'])}")
    print(f"🎁 **BENEFÍCIOS GERAIS**: {len(dados['beneficios_gerais'])}")
    print(f"💰 **VALORES MONETÁRIOS**: {dados['valores_encontrados']}")
    
    print("\n📋 **DETALHES DAS COBERTURAS**:")
    print("-" * 40)
    
    for i, cobertura in enumerate(dados['coberturas_detalhadas']):
        print(f"\n🔸 **COBERTURA {i+1}**: {cobertura['nome_cobertura']}")
        
        if cobertura['valores']['de'] and cobertura['valores']['ate']:
            print(f"   💰 **VALORES**: {cobertura['valores']['de']} até {cobertura['valores']['ate']}")
        
        if cobertura['beneficios']:
            print(f"   🎁 **BENEFÍCIOS**:")
            for beneficio in cobertura['beneficios']:
                print(f"      ✅ {beneficio}")
    
    print("\n🎁 **BENEFÍCIOS GERAIS ENCONTRADOS**:")
    print("-" * 40)
    for beneficio in dados['beneficios_gerais']:
        if beneficio['encontrado']:
            print(f"✅ {beneficio['nome']} ({beneficio['quantidade_elementos']} elementos)")
    
    print("\n🔍 **ELEMENTOS DETECTADOS**:")
    print("-" * 40)
    for elemento in dados['elementos_detectados']:
        print(f"🔹 {elemento}")
    
    return dados

def salvar_json_demonstracao(dados):
    """
    Salva o JSON de demonstração
    """
    # Criar diretório temp se não existir
    import os
    os.makedirs("temp", exist_ok=True)
    
    # Salvar arquivo de demonstração
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    arquivo_demo = f"temp/demonstracao_carrossel_melhorado_{timestamp}.json"
    
    with open(arquivo_demo, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 **ARQUIVO SALVO**: {arquivo_demo}")
    return arquivo_demo

def main():
    """
    Função principal do teste
    """
    print("🚀 **INICIANDO TESTE DA CAPTURA MELHORADA**")
    print("="*60)
    
    # Simular captura
    dados = simular_captura_carrossel_melhorado()
    
    # Exibir resultado detalhado
    dados_exibidos = exibir_resultado_detalhado(dados)
    
    # Salvar JSON de demonstração
    arquivo_salvo = salvar_json_demonstracao(dados_exibidos)
    
    print("\n" + "="*60)
    print("✅ **TESTE CONCLUÍDO COM SUCESSO**")
    print("="*60)
    print("\n📋 **RESUMO DAS MELHORIAS**:")
    print("🔸 Captura estruturada de valores 'de' e 'até'")
    print("🔸 Benefícios organizados por cobertura")
    print("🔸 Lista geral de benefícios encontrados")
    print("🔸 JSON estruturado com subitens")
    print("🔸 Retorno intermediário sem interromper o RPA")
    
    return dados_exibidos

if __name__ == "__main__":
    main()
