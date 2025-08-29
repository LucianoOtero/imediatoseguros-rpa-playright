# PARTE 4: FUNÇÃO PRINCIPAL E MONTAGEM FINAL

def main():
    """Função principal"""
    print("🚀 **RPA TÔ SEGURADO - FLUXO CORRIGIDO FINAL**")
    print("=" * 80)
    print("🎯 OBJETIVO: Fluxo correto das telas com seletores que funcionaram")
    print(" CORREÇÃO: Tela 4 = Veículo segurado, Tela 5 = Estimativa inicial")
    print("⚡ MÉTODO: Delays extremos + Seletores testados + Fluxo correto")
    print("📊 BONUS: Capturar dados da estimativa inicial (Tela 5)")
    print("📝 NOTA: Fluxo real das telas corrigido pelo usuário")
    print("=" * 80)
    
    inicio = datetime.now()
    print(f"⏰ Início: {inicio.strftime('%Y-%m-%d %H:%M:%S')}")
    
    driver = None
    temp_dir = None
    
    try:
        # Configurar Chrome
        driver, temp_dir = configurar_chrome()
        print("✅ Chrome configurado")
        
        # Navegar até Tela 3
        if not navegar_ate_tela3(driver):
            print("❌ Erro: Falha ao navegar até Tela 3")
            return
        
        # Implementar Tela 4 (CORREÇÃO: Veículo já está segurado)
        if not implementar_tela4(driver):
            print("❌ Erro: Falha ao implementar Tela 4")
            return
        
        # Implementar Tela 5 (Estimativa inicial - AGORA DEVE FUNCIONAR!)
        if not implementar_tela5(driver):
            print("❌ Erro: Falha ao implementar Tela 5")
            return
        
        # Implementar Tela 6 (Tipo de combustível + checkboxes)
        if not implementar_tela6(driver):
            print("❌ Erro: Falha ao implementar Tela 6")
            return
        
        # Implementar Tela 7 (Endereço de pernoite)
        if not implementar_tela7(driver):
            print("❌ Erro: Falha ao implementar Tela 7")
            return
        
        # Implementar Tela 8 (Finalidade do veículo)
        if not implementar_tela8(driver):
            print("❌ Erro: Falha ao implementar Tela 8")
            return
        
        # Implementar Tela 9 (Dados pessoais)
        if not implementar_tela9(driver):
            print("❌ Erro: Falha ao implementar Tela 9")
            return
        
        # Implementar Tela 10 (Condutor principal)
        if not implementar_tela10(driver):
            print("❌ Erro: Falha ao implementar Tela 10")
            return
        
        print("\n" + "=" * 80)
        print("🎉 **RPA EXECUTADO COM SUCESSO! TODAS AS 10 TELAS IMPLEMENTADAS!**")
        print("=" * 80)
        print(f"✅ Total de telas executadas: 10")
        print(f"✅ Tela 1: Seleção do tipo de seguro (Carro)")
        print(f"✅ Tela 2: Inserção da placa (EED3D56)")
        print(f"✅ Tela 3: Confirmação da placa")
        print(f"✅ Tela 4: Veículo já está segurado (Não selecionado)")
        print(f"✅ Tela 5: Estimativa inicial (dados capturados!)")
        print(f"✅ Tela 6: Tipo de combustível (Flex)")
        print(f"✅ Tela 7: Endereço de pernoite (CEP 03084-000)")
        print(f"✅ Tela 8: Finalidade do veículo (Pessoal)")
        print(f"✅ Tela 9: Dados pessoais (LUCIANO OTERO)")
        print(f"✅ Tela 10: Condutor principal (Sim)")
        print(f"📁 Todos os arquivos salvos em: /opt/imediatoseguros-rpa/temp/")
        
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
