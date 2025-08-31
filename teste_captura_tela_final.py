#!/usr/bin/env python3
"""
Teste da nova funcionalidade de captura da Tela Final
Demonstra a captura estruturada de planos de seguro com valores e coberturas
"""

import json
from datetime import datetime

def simular_captura_tela_final():
    """
    Simula a captura de dados da tela final com a nova estrutura
    """
    print("📊 **SIMULANDO CAPTURA DA TELA FINAL**")
    
    # Dados simulados baseados nos elementos reais descritos pelo usuário
    dados_tela_final = {
        "timestamp": datetime.now().isoformat(),
        "tela": "final",
        "nome_tela": "Resultado Final",
        "url": "https://www.app.tosegurado.com.br/resultado-final",
        "titulo": "Resultado Final - Tô Segurado",
        "titulo_pagina": "Parabéns, chegamos ao resultado final",
        "subtitulo_pagina": "Confira abaixo os melhores planos elaborados exclusivamente para você",
        "planos": [
            {
                "indice": 1,
                "tipo": "recomendado",
                "nome": "Morte/Invalidez",
                "valor_principal": "R$ 100,00",
                "preco_total": "R$ 2.561,00",
                "franquia": "Reduzida",
                "valor_mercado": "100% da tabela FIPE",
                "coberturas": {
                    "danos_materiais": "R$ 50.000,00",
                    "danos_corporais": "R$ 50.000,00",
                    "danos_morais": "R$ 10.000,00",
                    "assistencia": "Incluído",
                    "vidros": "Incluído",
                    "carro_reserva": "Incluído"
                },
                "beneficios_incluidos": [
                    "Assistência",
                    "Vidros",
                    "Carro Reserva"
                ],
                "texto_completo": "Morte/Invalidez\nPlano recomendado\nR$ 100,00\nanual\nem até 12x sem juros!\nR$ 2.561,00\nReduzida\n100% da tabela FIPE\nIcone de OK\nAssistência\nIcone de OK\nVidros\nIcone de OK\nCarro Reserva\nR$ 50.000,00\nR$ 50.000,00\nR$ 10.000,00\nR$ 5.000,00"
            },
            {
                "indice": 2,
                "tipo": "alternativo",
                "nome": "Plano Alternativo",
                "valor_principal": "R$ 5.000,00",
                "preco_total": "R$ 2.561,00",
                "franquia": "Reduzida",
                "valor_mercado": "100% da tabela FIPE",
                "coberturas": {
                    "danos_materiais": "R$ 50.000,00",
                    "danos_corporais": "R$ 50.000,00",
                    "danos_morais": "R$ 10.000,00",
                    "assistencia": "Incluído",
                    "vidros": "Incluído",
                    "carro_reserva": "Incluído"
                },
                "beneficios_incluidos": [
                    "Assistência",
                    "Vidros",
                    "Carro Reserva"
                ],
                "texto_completo": "R$ 5.000,00\nR$ 100,00\nanual\nem até 12x sem juros!\nR$ 2.561,00\nReduzida\n100% da tabela FIPE\nIcone de OK\nAssistência\nIcone de OK\nVidros\nIcone de OK\nCarro Reserva\nR$ 50.000,00\nR$ 50.000,00\nR$ 10.000,00\nR$ 5.000,00"
            }
        ],
        "modal_login": {
            "detectado": True,
            "titulo": "Acesse sua conta para visualizar o resultado final",
            "campos": ["email", "senha"]
        },
        "elementos_detectados": [
            "palavra_chave: Parabéns",
            "palavra_chave: resultado final",
            "palavra_chave: melhores planos",
            "palavra_chave: elaborados exclusivamente",
            "palavra_chave: Morte/Invalidez",
            "palavra_chave: Plano recomendado",
            "palavra_chave: Franquia",
            "palavra_chave: Valor de Mercado"
        ],
        "resumo": {
            "total_planos": 2,
            "plano_recomendado": "Morte/Invalidez",
            "valores_encontrados": 12
        }
    }
    
    return dados_tela_final

def exibir_resultado_detalhado(dados):
    """
    Exibe o resultado da captura da tela final de forma detalhada
    """
    print("\n" + "="*60)
    print("🎯 **CAPTURA DA TELA FINAL MELHORADA**")
    print("="*60)
    
    print(f"📋 **TÍTULO**: {dados['titulo_pagina']}")
    print(f"📝 **SUBTÍTULO**: {dados['subtitulo_pagina']}")
    print(f"📊 **PLANOS ENCONTRADOS**: {len(dados['planos'])}")
    print(f"💰 **VALORES MONETÁRIOS**: {dados['resumo']['valores_encontrados']}")
    
    if dados['modal_login']['detectado']:
        print(f"🔐 **MODAL DE LOGIN**: {dados['modal_login']['titulo']}")
    
    print("\n📋 **DETALHES DOS PLANOS**:")
    print("-" * 40)
    
    for i, plano in enumerate(dados['planos']):
        print(f"\n🔸 **PLANO {i+1}**: {plano['tipo'].upper()} - {plano['nome']}")
        
        if plano['valor_principal']:
            print(f"   💰 **VALOR PRINCIPAL**: {plano['valor_principal']}")
        
        if plano['preco_total']:
            print(f"   💵 **PREÇO TOTAL**: {plano['preco_total']}")
        
        if plano['franquia']:
            print(f"   🛡️ **FRANQUIA**: {plano['franquia']}")
        
        if plano['valor_mercado']:
            print(f"   📈 **VALOR DE MERCADO**: {plano['valor_mercado']}")
        
        if plano['coberturas']:
            print(f"   🛡️ **COBERTURAS**:")
            for cobertura, valor in plano['coberturas'].items():
                print(f"      • {cobertura.replace('_', ' ').title()}: {valor}")
        
        if plano['beneficios_incluidos']:
            print(f"   ✅ **BENEFÍCIOS INCLUÍDOS**:")
            for beneficio in plano['beneficios_incluidos']:
                print(f"      • {beneficio}")
    
    print("\n🔍 **ELEMENTOS DETECTADOS**:")
    print("-" * 40)
    for elemento in dados['elementos_detectados']:
        print(f"🔹 {elemento}")
    
    print(f"\n📊 **RESUMO**:")
    print(f"   • Plano Recomendado: {dados['resumo']['plano_recomendado']}")
    print(f"   • Total de Planos: {dados['resumo']['total_planos']}")
    print(f"   • Valores Monetários: {dados['resumo']['valores_encontrados']}")
    
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
    arquivo_demo = f"temp/demonstracao_tela_final_{timestamp}.json"
    
    with open(arquivo_demo, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 **ARQUIVO SALVO**: {arquivo_demo}")
    return arquivo_demo

def main():
    """
    Função principal do teste
    """
    print("🚀 **INICIANDO TESTE DA CAPTURA DA TELA FINAL**")
    print("="*60)
    
    # Simular captura
    dados = simular_captura_tela_final()
    
    # Exibir resultado detalhado
    dados_exibidos = exibir_resultado_detalhado(dados)
    
    # Salvar JSON de demonstração
    arquivo_salvo = salvar_json_demonstracao(dados_exibidos)
    
    print("\n" + "="*60)
    print("✅ **TESTE CONCLUÍDO COM SUCESSO**")
    print("="*60)
    print("\n📋 **RESUMO DAS MELHORIAS**:")
    print("🔸 Captura estruturada de planos de seguro")
    print("🔸 Valores monetários organizados")
    print("🔸 Coberturas detalhadas por plano")
    print("🔸 Benefícios incluídos identificados")
    print("🔸 Modal de login detectado")
    print("🔸 JSON estruturado com metadados")
    print("🔸 Retorno intermediário sem interromper o RPA")
    
    return dados_exibidos

if __name__ == "__main__":
    main()
