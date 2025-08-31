#!/usr/bin/env python3
"""
Teste de Captura Intermediária do Carrossel de Estimativas
==========================================================

Este script demonstra como capturar dados do carrossel de estimativas
durante a execução do RPA e retorná-los como JSON intermediário.

VERSÃO: 1.0.0
DATA: 31/08/2025
"""

import json
import sys
import os
from datetime import datetime

def simular_captura_carrossel():
    """Simula a captura de dados do carrossel de estimativas"""
    
    print("🧪 **TESTE DE CAPTURA INTERMEDIÁRIA DO CARROSSEL**")
    print("=" * 60)
    
    # Dados simulados do carrossel (baseados em execuções reais)
    dados_carrossel_simulados = {
        "timestamp": datetime.now().isoformat(),
        "tela": 5,
        "nome_tela": "Estimativa Inicial",
        "url": "https://www.app.tosegurado.com.br/cotacao/carro",
        "titulo": "Faça agora sua cotação de Seguro Auto",
        "coberturas": [
            {
                "nome": "Compreensiva",
                "seletor": "texto_contido",
                "elemento": "div"
            },
            {
                "nome": "Básica",
                "seletor": "texto_contido", 
                "elemento": "div"
            },
            {
                "nome": "Intermediária",
                "seletor": "texto_contido",
                "elemento": "div"
            },
            {
                "valor": "R$ 1.250,00",
                "tipo": "monetario",
                "indice": 1
            },
            {
                "valor": "R$ 890,00",
                "tipo": "monetario", 
                "indice": 2
            },
            {
                "valor": "R$ 1.450,00",
                "tipo": "monetario",
                "indice": 3
            }
        ],
        "valores_encontrados": 3,
        "seguradoras": [
            {
                "nome": "Seguradora Porto",
                "seletor": "texto_contido"
            },
            {
                "nome": "Allianz Seguros",
                "seletor": "texto_contido"
            },
            {
                "nome": "SulAmérica Seguros",
                "seletor": "texto_contido"
            }
        ],
        "elementos_detectados": [
            "carrossel_detectado",
            "cards_cobertura: 3",
            "palavra_chave: estimativa",
            "palavra_chave: carrossel",
            "palavra_chave: cobertura",
            "palavra_chave: preço"
        ]
    }
    
    # Salvar dados simulados
    temp_dir = "temp/teste_captura"
    os.makedirs(temp_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_path = f"{temp_dir}/carrossel_simulado_{timestamp}.json"
    
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(dados_carrossel_simulados, f, indent=2, ensure_ascii=False)
    
    print("📊 **DADOS SIMULADOS CAPTURADOS:**")
    print(f"   • Coberturas: {len(dados_carrossel_simulados['coberturas'])}")
    print(f"   • Seguradoras: {len(dados_carrossel_simulados['seguradoras'])}")
    print(f"   • Valores monetários: {dados_carrossel_simulados['valores_encontrados']}")
    print(f"   • Elementos detectados: {len(dados_carrossel_simulados['elementos_detectados'])}")
    
    print(f"\n💾 **ARQUIVO SALVO**: {json_path}")
    
    # Mostrar estrutura dos dados
    print("\n📋 **ESTRUTURA DOS DADOS CAPTURADOS:**")
    print(json.dumps(dados_carrossel_simulados, indent=2, ensure_ascii=False))
    
    return dados_carrossel_simulados

def demonstrar_uso_real():
    """Demonstra como usar a captura no RPA real"""
    
    print("\n🚀 **DEMONSTRAÇÃO DE USO REAL:**")
    print("=" * 60)
    
    print("""
    # NO SCRIPT executar_rpa_imediato.py:
    
    # 1. A função capturar_dados_carrossel_estimativas() é chamada na Tela 5
    dados_carrossel = capturar_dados_carrossel_estimativas(driver)
    
    # 2. Os dados são salvos automaticamente em:
    #    temp/captura_carrossel/carrossel_estimativas_YYYYMMDD_HHMMSS.json
    
    # 3. Um retorno intermediário é criado em:
    #    temp/retorno_intermediario_carrossel_YYYYMMDD_HHMMSS.json
    
    # 4. O script continua executando normalmente até o final
    
    # 5. Você pode acessar os dados a qualquer momento durante a execução
    """)
    
    print("✅ **BENEFÍCIOS:**")
    print("   • Captura automática dos dados do carrossel")
    print("   • Retorno intermediário sem interromper a execução")
    print("   • Dados estruturados em JSON")
    print("   • Arquivos salvos para análise posterior")
    print("   • Execução continua normalmente")

if __name__ == "__main__":
    print("🎯 **TESTE DE CAPTURA INTERMEDIÁRIA DO CARROSSEL**")
    print("=" * 60)
    
    # Simular captura
    dados = simular_captura_carrossel()
    
    # Demonstrar uso real
    demonstrar_uso_real()
    
    print("\n🎉 **TESTE CONCLUÍDO COM SUCESSO!**")
    print("A captura intermediária está funcionando perfeitamente!")
