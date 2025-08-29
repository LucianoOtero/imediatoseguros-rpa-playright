# PARTE 2: FUNÇÕES DE NAVEGAÇÃO

def navegar_ate_tela3(driver):
    """Navega o RPA até a Tela 3 com seletores que funcionaram"""
    print("🚀 **NAVEGANDO ATÉ TELA 3 COM SELETORES TESTADOS**")
    
    # TELA 1: Seleção do tipo de seguro
    print("\n📱 TELA 1: Selecionando Carro...")
    driver.get("https://www.app.tosegurado.com.br/cotacao")
    
    if not aguardar_carregamento_pagina(driver, 60):
        print("❌ Erro: Página não carregou")
        return False
    
    salvar_estado_tela(driver, 1, "inicial", None)
    
    # AGUARDAR ESTABILIZAÇÃO EXTREMA
    aguardar_estabilizacao(driver, 20)
    
    # Clicar no botão Carro com seletor que funcionou
    salvar_estado_tela(driver, 1, "antes_clique", None)
    
    if not clicar_com_delay_extremo(driver, By.XPATH, "//button[contains(., 'Carro')]", "botão Carro"):
        print("❌ Erro: Falha ao clicar no botão Carro")
        return False
    
    # AGUARDAR CARREGAMENTO COMPLETO
    print("⏳ Aguardando carregamento completo da página...")
    time.sleep(10)
    
    if not aguardar_carregamento_pagina(driver, 60):
        print("❌ Erro: Página não carregou após selecionar Carro")
        return False
    
    # AGUARDAR ESTABILIZAÇÃO EXTREMA
    aguardar_estabilizacao(driver, 20)
    
    salvar_estado_tela(driver, 1, "apos_clique", None)
    
    # TELA 2: Inserção da placa
    print("\n📱 TELA 2: Inserindo placa...")
    
    # AGUARDAR ESTABILIZAÇÃO EXTREMA
    aguardar_estabilizacao(driver, 15)
    
    salvar_estado_tela(driver, 2, "inicial", None)
    
    # Preencher placa com delay extremo
    if not preencher_com_delay_extremo(driver, By.ID, "placaTelaDadosPlaca", "EED3D56", "placa"):
        print("❌ Erro: Falha ao preencher placa")
        return False
    
    # AGUARDAR ESTABILIZAÇÃO EXTREMA
    aguardar_estabilizacao(driver, 15)
    
    salvar_estado_tela(driver, 2, "placa_inserida", None)
    
    # TELA 3: Clicar em Continuar
    print("\n📱 TELA 3: Clicando Continuar...")
    
    # USAR O SELETOR QUE FUNCIONOU!
    if not clicar_com_delay_extremo(driver, By.ID, "gtm-telaDadosAutoCotarComPlacaContinuar", "botão Continuar Tela 3"):
        print("❌ Erro: Falha ao clicar Continuar na Tela 3")
        return False
    
    # AGUARDAR CARREGAMENTO COMPLETO
    print("⏳ Aguardando carregamento da página...")
    time.sleep(15)
    
    if not aguardar_carregamento_pagina(driver, 60):
        print("⚠️ Página pode não ter carregado completamente")
    
    # AGUARDAR ESTABILIZAÇÃO EXTREMA
    aguardar_estabilizacao(driver, 20)
    
    salvar_estado_tela(driver, 3, "apos_clique", None)
    
    print("✅ **NAVEGAÇÃO ATÉ TELA 3 CONCLUÍDA COM SUCESSO!**")
    return True

def implementar_tela4(driver):
    """Implementa a Tela 4 (Veículo já está segurado) - CORREÇÃO: NÃO"""
    print("\n **INICIANDO TELA 4: Veículo já está segurado**")
    
    # Aguardar Tela 4 carregar
    print("⏳ Aguardando Tela 4 carregar...")
    
    try:
        # Aguardar elementos da pergunta
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'segurado') or contains(text(), 'Segurado')]"))
        )
        print("✅ Tela 4 carregada - pergunta sobre veículo segurado detectada!")
        
        salvar_estado_tela(driver, 4, "inicial", None)
        
        if not aguardar_carregamento_pagina(driver, 30):
            print("❌ Erro: Página não carregou completamente")
            return False
        
        salvar_estado_tela(driver, 4, "pergunta_carregada", None)
        
        # CORREÇÃO: Selecionar "Não" para veículo já segurado
        print("⏳ Selecionando 'Não' para veículo já segurado (CORREÇÃO!)...")
        
        if not clicar_radio_via_javascript(driver, "Não", "Não para veículo segurado"):
            print("⚠️ Radio 'Não' não encontrado - tentando prosseguir...")
        
        # Clicar em Continuar
        print("⏳ Aguardando botão Continuar aparecer...")
        
        if not clicar_com_delay_extremo(driver, By.XPATH, "//button[contains(., 'Continuar')]", "botão Continuar Tela 4"):
            print("❌ Erro: Falha ao clicar Continuar na Tela 4")
            return False
        
        # AGUARDAR CARREGAMENTO COMPLETO
        print("⏳ Aguardando carregamento da página...")
        time.sleep(15)
        
        if not aguardar_carregamento_pagina(driver, 60):
            print("⚠️ Página pode não ter carregado completamente")
        
        # AGUARDAR ESTABILIZAÇÃO EXTREMA
        aguardar_estabilizacao(driver, 20)
        
        salvar_estado_tela(driver, 4, "apos_continuar", None)
        print("✅ **TELA 4 IMPLEMENTADA COM SUCESSO! (Não selecionado)**")
        return True
        
    except Exception as e:
        print(f"❌ Erro na Tela 4: {e}")
        return False

def implementar_tela5(driver):
    """Implementa a Tela 5 (Estimativa inicial) - AGORA DEVE FUNCIONAR!"""
    print("\n **INICIANDO TELA 5: Estimativa inicial**")
    
    # Aguardar Tela 5 carregar
    print("⏳ Aguardando Tela 5 carregar...")
    
    try:
        # Aguardar elementos da estimativa
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'estimativa') or contains(text(), 'inicial') or contains(text(), 'carrossel')]"))
        )
        print("✅ Tela 5 carregada - estimativa inicial detectada!")
        
        salvar_estado_tela(driver, 5, "inicial", None)
        
        if not aguardar_carregamento_pagina(driver, 30):
            print("❌ Erro: Página não carregou completamente")
            return False
        
        salvar_estado_tela(driver, 5, "estimativa_carregada", None)
        
        # CAPTURAR DADOS DA TELA 5
        capturar_dados_tela5(driver, None)
        
        # Clicar em Continuar
        print("⏳ Aguardando botão Continuar aparecer...")
        
        if not clicar_com_delay_extremo(driver, By.XPATH, "//button[contains(., 'Continuar')]", "botão Continuar Tela 5"):
            print("❌ Erro: Falha ao clicar Continuar na Tela 5")
            return False
        
        # AGUARDAR CARREGAMENTO COMPLETO
        print("⏳ Aguardando carregamento da página...")
        time.sleep(15)
        
        if not aguardar_carregamento_pagina(driver, 60):
            print("⚠️ Página pode não ter carregado completamente")
        
        # AGUARDAR ESTABILIZAÇÃO EXTREMA
        aguardar_estabilizacao(driver, 20)
        
        salvar_estado_tela(driver, 5, "apos_continuar", None)
        print("✅ **TELA 5 IMPLEMENTADA COM SUCESSO! (Estimativa inicial)**")
        return True
        
    except Exception as e:
        print(f"❌ Erro na Tela 5: {e}")
        return False

# CONTINUA NA PARTE 3...
