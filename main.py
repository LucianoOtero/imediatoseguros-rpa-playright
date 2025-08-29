#!/usr/bin/env python3
"""
RPA Tô Segurado - ARQUITETURA MODULAR
Arquivo principal que orquestra todas as telas
"""

import json
import sys
import time
from datetime import datetime
from utils.browser import configurar_chrome
from utils.helpers import carregar_parametros, validar_parametros
from telas.tela1_selecao import implementar_tela1
from telas.tela2_placa import implementar_tela2
from telas.tela3_confirmacao import implementar_tela3
from telas.tela4_segurado import implementar_tela4
from telas.tela5_estimativa import implementar_tela5
from telas.tela6_combustivel import implementar_tela6
from telas.tela7_endereco import implementar_tela7
from telas.tela8_finalidade import implementar_tela8
from telas.tela9_dados import implementar_tela9
from telas.tela10_contato import implementar_tela10
from telas.tela11_coberturas import implementar_tela11
from telas.tela12_finalizacao import implementar_tela12

def main():
    """Função principal que executa todas as telas"""
    print("🚀 **RPA TÔ SEGURADO - ARQUITETURA MODULAR**")
    print("=" * 80)
    print("�� OBJETIVO: Executar RPA com arquitetura modular")
    print("🔧 MÉTODO: Módulos separados para cada tela")
    print("📝 NOTA: Recebe JSON via linha de comando")
    print("=" * 80)
    
    # Carregar e validar parâmetros
    print("�� CARREGANDO PARÂMETROS...")
    parametros = carregar_parametros()
    validar_parametros(parametros)
    
    # Exibir parâmetros carregados
    print("\n📊 PARÂMETROS CARREGADOS:")
    for key, value in parametros.items():
        print(f"   {key}: {value}")
    
    inicio = datetime.now()
    print(f"\n⏰ Início: {inicio.strftime('%Y-%m-%d %H:%M:%S')}")
    
    driver = None
    temp_dir = None
    
    try:
        # Configurar Chrome
        driver, temp_dir = configurar_chrome()
        print("✅ Chrome configurado")
        
        # Executar todas as telas em sequência
        telas = [
            ("Tela 1: Seleção Carro", implementar_tela1),
            ("Tela 2: Inserção placa", implementar_tela2),
            ("Tela 3: Confirmação veículo", implementar_tela3),
            ("Tela 4: Veículo segurado", implementar_tela4),
            ("Tela 5: Estimativa inicial", implementar_tela5),
            ("Tela 6: Tipo combustível", implementar_tela6),
            ("Tela 7: Endereço pernoite", implementar_tela7),
            ("Tela 8: Finalidade veículo", implementar_tela8),
            ("Tela 9: Dados pessoais", implementar_tela9),
            ("Tela 10: Contato", implementar_tela10),
            ("Tela 11: Coberturas", implementar_tela11),
            ("Tela 12: Finalização", implementar_tela12)
        ]
        
        for descricao, funcao in telas:
            print(f"\n{'='*80}")
            print(f"🎯 EXECUTANDO: {descricao}")
            print(f"{'='*80}")
            
            if not funcao(driver, parametros):
                print(f"❌ Erro: Falha ao implementar {descricao}")
                return
            
            print(f"✅ {descricao} implementada com sucesso!")
        
        print("\n" + "=" * 80)
        print("🎉 **RPA EXECUTADO COM SUCESSO TOTAL! TODAS AS 12 TELAS IMPLEMENTADAS!**")
        print("=" * 80)
        print(f"✅ Total de telas executadas: 12")
        print(f"✅ Tela 1: Seleção Carro (URL: {parametros['url']})")
        print(f"✅ Tela 2: Inserção placa {parametros['placa']}")
        print(f"✅ Tela 3: Confirmação {parametros['marca']} {parametros['modelo']} → Sim")
        print(f"✅ Tela 4: Veículo segurado → {parametros['veiculo_segurado']}")
        print(f"✅ Tela 5: Estimativa inicial")
        print(f"✅ Tela 6: Tipo combustível {parametros['combustivel']}")
        print(f"✅ Tela 7: Endereço pernoite (CEP {parametros['cep']})")
        print(f"✅ Tela 8: Finalidade veículo → {parametros['uso_veiculo']}")
        print(f"✅ Tela 9: Dados pessoais - {parametros['nome']}")
        print(f"✅ Tela 10: Contato - {parametros['email']}")
        print(f"✅ Tela 11: Coberturas adicionais")
        print(f"✅ Tela 12: Finalização e resultado")
        print(f"📁 Todos os arquivos salvos em: /opt/imediatoseguros-rpa/temp/")
        print(f"🔧 Parâmetros utilizados: {len(parametros)} parâmetros do JSON")
        print(f"🌐 URL utilizada: {parametros['url']}")
        print(f"�� Endereço completo: {parametros.get('endereco_completo', 'N/A')}")
        
    except Exception as e:
        print(f"❌ **ERRO GERAL DURANTE EXECUÇÃO:** {e}")
    
    finally:
        # Limpeza
        if driver:
            driver.quit()
        if temp_dir and os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
            print(f"🗑️ Diretório temporário removido: {temp_dir}")
        
        fim = datetime.now()
        print(f"⏰ Fim: {fim.strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
