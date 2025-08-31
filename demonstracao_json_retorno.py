#!/usr/bin/env python3
"""
Script de Demonstração - Documentação do JSON de Retorno
Demonstra como processar e utilizar o JSON de retorno do RPA Tô Segurado
"""

import json
import sys
from datetime import datetime

def carregar_exemplo_json():
    """Carrega um exemplo de JSON de retorno para demonstração"""
    return {
        "status": "sucesso",
        "timestamp": "2025-08-31T17:45:00.199712",
        "versao": "2.11.0",
        "sistema": "RPA Tô Segurado",
        "codigo": 9002,
        "mensagem": "RPA executado com sucesso",
        "dados": {
            "telas_executadas": 8,
            "tempo_execucao": "85.2s",
            "placa_processada": "FPG-8D63",
            "url_final": "https://www.app.tosegurado.com.br/cotacao/carro",
            "capturas_intermediarias": {
                "carrossel": {
                    "timestamp": "2025-08-31T17:44:30.123456",
                    "tela": "carrossel",
                    "nome_tela": "Estimativas de Cobertura",
                    "url": "https://www.app.tosegurado.com.br/cotacao/carro",
                    "titulo": "Faça agora sua cotação de Seguro Auto",
                    "estimativas": [
                        {
                            "cobertura": "Cobertura Compreensiva",
                            "valores": {
                                "de": "R$ 1.200,00",
                                "ate": "R$ 1.700,00"
                            },
                            "beneficios": [
                                {
                                    "nome": "Colisão e Acidentes",
                                    "status": "incluido"
                                },
                                {
                                    "nome": "Roubo e Furto",
                                    "status": "incluido"
                                }
                            ]
                        }
                    ]
                },
                "tela_final": {
                    "timestamp": "2025-08-31T17:45:00.199712",
                    "tela": "final",
                    "nome_tela": "Resultado Final",
                    "url": "https://www.app.tosegurado.com.br/cotacao/carro",
                    "titulo": "Faça agora sua cotação de Seguro Auto",
                    "titulo_pagina": "Parabéns, chegamos ao resultado final",
                    "planos": [
                        {
                            "titulo": "Plano Recomendado",
                            "franquia": {
                                "valor": "R$ 2.500,00",
                                "tipo": "Reduzida"
                            },
                            "valor_mercado": "100% da tabela FIPE",
                            "assistencia": True,
                            "vidros": True,
                            "carro_reserva": True,
                            "danos_materiais": "R$ 50.000,00",
                            "danos_corporais": "R$ 50.000,00",
                            "danos_morais": "R$ 10.000,00",
                            "morte_invalidez": "R$ 5.000,00",
                            "precos": {
                                "anual": "R$ 100,00",
                                "parcelado": {
                                    "valor": "R$ 218,17",
                                    "parcelas": "1x sem juros"
                                }
                            },
                            "score_qualidade": 100,
                            "texto_completo": "Texto completo do plano...",
                            "categoria": "premium"
                        }
                    ],
                    "modal_login": {
                        "detectado": True,
                        "titulo": "Modal de envio de cotação por email",
                        "campos": ["email"]
                    },
                    "elementos_detectados": [
                        "palavra_chave: Parabéns",
                        "palavra_chave: resultado final"
                    ],
                    "resumo": {
                        "total_planos": 2,
                        "plano_recomendado": "Plano Recomendado",
                        "valores_encontrados": 22,
                        "qualidade_captura": "boa"
                    }
                }
            }
        },
        "logs": [
            "2025-08-31 17:44:07 | INFO | RPA executado com sucesso",
            "2025-08-31 17:44:09 | INFO | Chrome fechado"
        ]
    }

def processar_retorno_rpa(json_retorno):
    """Processa o JSON de retorno do RPA e exibe informações detalhadas"""
    print("=" * 80)
    print("📋 PROCESSAMENTO DO JSON DE RETORNO - RPA TÔ SEGURADO")
    print("=" * 80)
    
    # Verificar estrutura básica
    if not isinstance(json_retorno, dict):
        print("❌ ERRO: JSON de retorno inválido")
        return False
    
    # Verificar campos obrigatórios
    campos_obrigatorios = ['status', 'timestamp', 'codigo', 'mensagem', 'dados']
    for campo in campos_obrigatorios:
        if campo not in json_retorno:
            print(f"❌ ERRO: Campo obrigatório ausente: {campo}")
            return False
    
    # Processar conforme status
    if json_retorno['status'] == 'sucesso':
        return processar_sucesso(json_retorno)
    else:
        return processar_erro(json_retorno)

def processar_sucesso(json_retorno):
    """Processa retorno de sucesso"""
    print("✅ RPA EXECUTADO COM SUCESSO!")
    print(f"📅 Timestamp: {json_retorno['timestamp']}")
    print(f"🔢 Código: {json_retorno['codigo']}")
    print(f"💬 Mensagem: {json_retorno['mensagem']}")
    print(f"📦 Versão: {json_retorno['versao']}")
    
    dados = json_retorno['dados']
    print(f"\n📊 DADOS DA EXECUÇÃO:")
    print(f"   • Telas executadas: {dados['telas_executadas']}")
    print(f"   • Tempo de execução: {dados['tempo_execucao']}")
    print(f"   • Placa processada: {dados['placa_processada']}")
    print(f"   • URL final: {dados['url_final']}")
    
    # Processar capturas intermediárias
    if 'capturas_intermediarias' in dados:
        capturas = dados['capturas_intermediarias']
        
        # Carrossel
        if 'carrossel' in capturas:
            processar_carrossel(capturas['carrossel'])
        
        # Tela final
        if 'tela_final' in capturas:
            processar_tela_final(capturas['tela_final'])
    
    # Processar logs
    if 'logs' in json_retorno:
        processar_logs(json_retorno['logs'])
    
    return True

def processar_carrossel(carrossel):
    """Processa dados do carrossel"""
    print(f"\n🎠 CARROSSEL - {carrossel['nome_tela']}:")
    print(f"   • Timestamp: {carrossel['timestamp']}")
    print(f"   • URL: {carrossel['url']}")
    print(f"   • Estimativas encontradas: {len(carrossel['estimativas'])}")
    
    for i, estimativa in enumerate(carrossel['estimativas'], 1):
        print(f"\n   📋 Estimativa {i}:")
        print(f"      • Cobertura: {estimativa['cobertura']}")
        print(f"      • Valores: {estimativa['valores']['de']} até {estimativa['valores']['ate']}")
        print(f"      • Benefícios: {len(estimativa['beneficios'])} encontrados")
        
        for beneficio in estimativa['beneficios']:
            status_icon = "✅" if beneficio['status'] == 'incluido' else "❌"
            print(f"        {status_icon} {beneficio['nome']}")

def processar_tela_final(tela_final):
    """Processa dados da tela final"""
    print(f"\n🎯 TELA FINAL - {tela_final['nome_tela']}:")
    print(f"   • Timestamp: {tela_final['timestamp']}")
    print(f"   • URL: {tela_final['url']}")
    print(f"   • Título da página: {tela_final['titulo_pagina']}")
    print(f"   • Planos encontrados: {len(tela_final['planos'])}")
    
    # Processar planos
    for i, plano in enumerate(tela_final['planos'], 1):
        print(f"\n   📋 Plano {i}: {plano['titulo']}")
        print(f"      • Categoria: {plano['categoria']}")
        print(f"      • Score de qualidade: {plano['score_qualidade']}/100")
        print(f"      • Preço anual: {plano['precos']['anual']}")
        print(f"      • Parcelado: {plano['precos']['parcelado']['valor']} em {plano['precos']['parcelado']['parcelas']}")
        print(f"      • Franquia: {plano['franquia']['valor']} ({plano['franquia']['tipo']})")
        print(f"      • Valor de mercado: {plano['valor_mercado']}")
        
        # Coberturas
        print(f"      • Coberturas:")
        print(f"        ✅ Assistência: {'Sim' if plano['assistencia'] else 'Não'}")
        print(f"        ✅ Vidros: {'Sim' if plano['vidros'] else 'Não'}")
        print(f"        ✅ Carro reserva: {'Sim' if plano['carro_reserva'] else 'Não'}")
        print(f"        💰 Danos materiais: {plano['danos_materiais']}")
        print(f"        💰 Danos corporais: {plano['danos_corporais']}")
        print(f"        💰 Danos morais: {plano['danos_morais']}")
        print(f"        💰 Morte/invalidez: {plano['morte_invalidez']}")
    
    # Processar modal de login
    if 'modal_login' in tela_final:
        modal = tela_final['modal_login']
        print(f"\n   🔐 Modal de Login:")
        print(f"      • Detectado: {'Sim' if modal['detectado'] else 'Não'}")
        print(f"      • Título: {modal['titulo']}")
        print(f"      • Campos: {', '.join(modal['campos'])}")
    
    # Processar resumo
    if 'resumo' in tela_final:
        resumo = tela_final['resumo']
        print(f"\n   📊 Resumo:")
        print(f"      • Total de planos: {resumo['total_planos']}")
        print(f"      • Plano recomendado: {resumo['plano_recomendado']}")
        print(f"      • Valores encontrados: {resumo['valores_encontrados']}")
        print(f"      • Qualidade da captura: {resumo['qualidade_captura']}")

def processar_logs(logs):
    """Processa logs da execução"""
    print(f"\n📝 LOGS DA EXECUÇÃO ({len(logs)} entradas):")
    for log in logs[-5:]:  # Mostrar apenas os últimos 5 logs
        print(f"   • {log}")

def processar_erro(json_retorno):
    """Processa retorno de erro"""
    print("❌ ERRO NO RPA!")
    print(f"📅 Timestamp: {json_retorno['timestamp']}")
    print(f"🔢 Código: {json_retorno['codigo']}")
    print(f"💬 Mensagem: {json_retorno['mensagem']}")
    
    # Sugerir soluções baseadas no código de erro
    sugestoes = {
        2002: "Verifique se o site não mudou sua estrutura",
        3001: "Tente executar novamente",
        4001: "Verifique sua conexão com a internet",
        5001: "Verifique os dados de entrada fornecidos"
    }
    
    if json_retorno['codigo'] in sugestoes:
        print(f"💡 Sugestão: {sugestoes[json_retorno['codigo']]}")
    
    # Mostrar dados do erro se disponíveis
    if 'dados' in json_retorno:
        dados = json_retorno['dados']
        print(f"\n📊 DETALHES DO ERRO:")
        for chave, valor in dados.items():
            print(f"   • {chave}: {valor}")
    
    return False

def demonstrar_validacao(json_retorno):
    """Demonstra como validar o JSON de retorno"""
    print("\n" + "=" * 80)
    print("🔍 VALIDAÇÃO DO JSON DE RETORNO")
    print("=" * 80)
    
    # Validar estrutura básica
    print("✅ Estrutura básica válida")
    
    # Validar campos obrigatórios
    campos_obrigatorios = ['status', 'timestamp', 'codigo', 'mensagem', 'dados']
    for campo in campos_obrigatorios:
        if campo in json_retorno:
            print(f"✅ Campo obrigatório '{campo}' presente")
        else:
            print(f"❌ Campo obrigatório '{campo}' ausente")
    
    # Validar tipos de dados
    if isinstance(json_retorno['status'], str):
        print("✅ Campo 'status' é string")
    else:
        print("❌ Campo 'status' não é string")
    
    if isinstance(json_retorno['codigo'], int):
        print("✅ Campo 'codigo' é integer")
    else:
        print("❌ Campo 'codigo' não é integer")
    
    # Validar dados específicos
    if json_retorno['status'] == 'sucesso':
        dados = json_retorno['dados']
        if 'capturas_intermediarias' in dados:
            capturas = dados['capturas_intermediarias']
            if 'tela_final' in capturas:
                tela_final = capturas['tela_final']
                if 'planos' in tela_final and isinstance(tela_final['planos'], list):
                    print(f"✅ {len(tela_final['planos'])} planos encontrados")
                else:
                    print("❌ Campo 'planos' inválido ou ausente")

def main():
    """Função principal"""
    print("🚀 DEMONSTRAÇÃO - DOCUMENTAÇÃO DO JSON DE RETORNO")
    print("RPA Tô Segurado - Versão 2.11.0")
    print(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    
    # Carregar exemplo
    json_exemplo = carregar_exemplo_json()
    
    # Processar retorno
    sucesso = processar_retorno_rpa(json_exemplo)
    
    # Demonstrar validação
    demonstrar_validacao(json_exemplo)
    
    # Salvar exemplo em arquivo
    with open('exemplo_json_retorno.json', 'w', encoding='utf-8') as f:
        json.dump(json_exemplo, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Exemplo salvo em: exemplo_json_retorno.json")
    print("📚 Consulte DOCUMENTACAO_JSON_RETORNO.md para mais detalhes")
    
    return 0 if sucesso else 1

if __name__ == "__main__":
    sys.exit(main())
