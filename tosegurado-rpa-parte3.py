# PARTE 3: FUNÇÕES DAS TELAS 6-10

def implementar_tela6(driver):
    """Implementa a Tela 6 (Tipo de combustível + checkboxes)"""
    print("\n **INICIANDO TELA 6: Tipo de combustível + checkboxes**")
    
    # Aguardar Tela 6 carregar
    print("⏳ Aguardando Tela 6 carregar...")
    
    try:
        # Aguardar elementos do combustível
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'combustível') or contains(text(), 'combustivel')]"))
        )
        print("✅ Tela 6 carregada - tipo de combustível detectado!")
        
        salvar_estado_tela(driver, 6, "inicial", None)
        
        if not aguardar_carregamento_pagina(driver, 30):
            print("❌ Erro: Página não carregou completamente")
            return False
        
        salvar_estado_tela(driver, 6, "combustivel_carregado", None)
        
        # Selecionar "Flex" como tipo de combustível
        print("⏳ Selecionando 'Flex' como tipo de combustível...")
        
        if not clicar_radio_via_javascript(driver, "Flex", "Flex para combustível"):
            print("⚠️ Radio 'Flex' não encontrado - tentando prosseguir...")
        
        # Deixar checkboxes em branco (kit gas, blindado, financiado)
        print("⏳ Deixando checkboxes em branco...")
        
        # Clicar em Continuar
        print("⏳ Aguardando botão Continuar aparecer...")
        
        if not clicar_com_delay_extremo(driver, By.XPATH, "//button[contains(., 'Continuar')]", "botão Continuar Tela 6"):
            print("❌ Erro: Falha ao clicar Continuar na Tela 6")
            return False
        
        # AGUARDAR CARREGAMENTO COMPLETO
        print("⏳ Aguardando carregamento da página...")
        time.sleep(15)
        
        if not aguardar_carregamento_pagina(driver, 60):
            print("⚠️ Página pode não ter carregado completamente")
        
        # AGUARDAR ESTABILIZAÇÃO EXTREMA
        aguardar_estabilizacao(driver, 20)
        
        salvar_estado_tela(driver, 6, "apos_continuar", None)
        print("✅ **TELA 6 IMPLEMENTADA COM SUCESSO! (Combustível Flex)**")
        return True
        
    except Exception as e:
        print(f"❌ Erro na Tela 6: {e}")
        return False

def implementar_tela7(driver):
    """Implementa a Tela 7 (Endereço de pernoite)"""
    print("\n **INICIANDO TELA 7: Endereço de pernoite**")
    
    # Aguardar Tela 7 carregar
    print("⏳ Aguardando Tela 7 carregar...")
    
    try:
        # Aguardar elementos do endereço
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'pernoite') or contains(text(), 'endereço') or contains(text(), 'CEP')]"))
        )
        print("✅ Tela 7 carregada - endereço de pernoite detectado!")
        
        salvar_estado_tela(driver, 7, "inicial", None)
        
        if not aguardar_carregamento_pagina(driver, 30):
            print("❌ Erro: Página não carregou completamente")
            return False
        
        salvar_estado_tela(driver, 7, "endereco_carregado", None)
        
        # Inserir CEP 03084-000
        print("⏳ Inserindo CEP 03084-000...")
        
        # Procurar campo CEP
        try:
            campo_cep = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[contains(@placeholder, 'CEP') or contains(@name, 'cep')]"))
            )
            campo_cep.clear()
            campo_cep.send_keys("03084-000")
            print("✅ CEP inserido: 03084-000")
        except:
            print("⚠️ Campo CEP não encontrado - tentando prosseguir...")
        
        # Aguardar sugestões de endereço
        time.sleep(5)
        
        # Selecionar primeira sugestão de endereço
        try:
            sugestao = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(@class, 'sugestao') or contains(@class, 'suggestion')]"))
            )
            sugestao.click()
            print("✅ Sugestão de endereço selecionada")
        except:
            print("⚠️ Sugestão de endereço não encontrada - tentando prosseguir...")
        
        # Clicar em Continuar
        print("⏳ Aguardando botão Continuar aparecer...")
        
        if not clicar_com_delay_extremo(driver, By.XPATH, "//button[contains(., 'Continuar')]", "botão Continuar Tela 7"):
            print("❌ Erro: Falha ao clicar Continuar na Tela 7")
            return False
        
        # AGUARDAR CARREGAMENTO COMPLETO
        print("⏳ Aguardando carregamento da página...")
        time.sleep(15)
        
        if not aguardar_carregamento_pagina(driver, 60):
            print("⚠️ Página pode não ter carregado completamente")
        
        # AGUARDAR ESTABILIZAÇÃO EXTREMA
        aguardar_estabilizacao(driver, 20)
        
        salvar_estado_tela(driver, 7, "apos_continuar", None)
        print("✅ **TELA 7 IMPLEMENTADA COM SUCESSO! (Endereço inserido)**")
        return True
        
    except Exception as e:
        print(f"❌ Erro na Tela 7: {e}")
        return False

def implementar_tela8(driver):
    """Implementa a Tela 8 (Finalidade do veículo)"""
    print("\n **INICIANDO TELA 8: Finalidade do veículo**")
    
    # Aguardar Tela 8 carregar
    print("⏳ Aguardando Tela 8 carregar...")
    
    try:
        # Aguardar elementos da finalidade
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'finalidade') or contains(text(), 'utilizado') or contains(text(), 'Pessoal')]"))
        )
        print("✅ Tela 8 carregada - finalidade do veículo detectada!")
        
        salvar_estado_tela(driver, 8, "inicial", None)
        
        if not aguardar_carregamento_pagina(driver, 30):
            print("❌ Erro: Página não carregou completamente")
            return False
        
        salvar_estado_tela(driver, 8, "finalidade_carregada", None)
        
        # Selecionar "Pessoal" como finalidade
        print("⏳ Selecionando 'Pessoal' como finalidade do veículo...")
        
        if not clicar_radio_via_javascript(driver, "Pessoal", "Pessoal para finalidade"):
            print("⚠️ Radio 'Pessoal' não encontrado - tentando prosseguir...")
        
        # Clicar em Continuar
        print("⏳ Aguardando botão Continuar aparecer...")
        
        if not clicar_com_delay_extremo(driver, By.XPATH, "//button[contains(., 'Continuar')]", "botão Continuar Tela 8"):
            print("❌ Erro: Falha ao clicar Continuar na Tela 8")
            return False
        
        # AGUARDAR CARREGAMENTO COMPLETO
        print("⏳ Aguardando carregamento da página...")
        time.sleep(15)
        
        if not aguardar_carregamento_pagina(driver, 60):
            print("⚠️ Página pode não ter carregado completamente")
        
        # AGUARDAR ESTABILIZAÇÃO EXTREMA
        aguardar_estabilizacao(driver, 20)
        
        salvar_estado_tela(driver, 8, "apos_continuar", None)
        print("✅ **TELA 8 IMPLEMENTADA COM SUCESSO! (Finalidade Pessoal)**")
        return True
        
    except Exception as e:
        print(f"❌ Erro na Tela 8: {e}")
        return False

def implementar_tela9(driver):
    """Implementa a Tela 9 (Dados pessoais)"""
    print("\n **INICIANDO TELA 9: Dados pessoais**")
    
    # Aguardar Tela 9 carregar
    print("⏳ Aguardando Tela 9 carregar...")
    
    try:
        # Aguardar elementos dos dados pessoais
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'dados pessoais') or contains(text(), 'Nome Completo')]"))
        )
        print("✅ Tela 9 carregada - dados pessoais detectados!")
        
        salvar_estado_tela(driver, 9, "inicial", None)
        
        if not aguardar_carregamento_pagina(driver, 30):
            print("❌ Erro: Página não carregou completamente")
            return False
        
        salvar_estado_tela(driver, 9, "dados_carregados", None)
        
        # Preencher dados pessoais
        print("⏳ Preenchendo dados pessoais...")
        
        # Nome Completo
        if not preencher_com_delay_extremo(driver, By.XPATH, "//input[@placeholder='Digite seu nome completo']", "LUCIANO OTERO", "nome completo"):
            print("⚠️ Campo nome não encontrado - tentando alternativas...")
            # Tentar alternativas
            try:
                campo_nome = driver.find_element(By.XPATH, "//input[contains(@name, 'nome') or contains(@id, 'nome')]")
                campo_nome.clear()
                campo_nome.send_keys("LUCIANO OTERO")
                print("✅ Nome preenchido via alternativa")
            except:
                print("❌ Campo nome não encontrado")
        
        # CPF
        if not preencher_com_delay_extremo(driver, By.XPATH, "//input[@placeholder='Digite seu CPF']", "085.546.078-48", "CPF"):
            print("⚠️ Campo CPF não encontrado - tentando alternativas...")
            try:
                campo_cpf = driver.find_element(By.XPATH, "//input[contains(@name, 'cpf') or contains(@id, 'cpf')]")
                campo_cpf.clear()
                campo_cpf.send_keys("085.546.078-48")
                print("✅ CPF preenchido via alternativa")
            except:
                print("❌ Campo CPF não encontrado")
        
        # Data de nascimento
        if not preencher_com_delay_extremo(driver, By.XPATH, "//input[@placeholder='DD/MM/AAAA']", "09/02/1965", "data nascimento"):
            print("⚠️ Campo data não encontrado - tentando alternativas...")
            try:
                campo_data = driver.find_element(By.XPATH, "//input[contains(@name, 'nascimento') or contains(@id, 'nascimento') or contains(@type, 'date')]")
                campo_data.clear()
                campo_data.send_keys("09/02/1965")
                print("✅ Data preenchida via alternativa")
            except:
                print("❌ Campo data não encontrado")
        
        # Sexo (Masculino)
        if not clicar_radio_via_javascript(driver, "Masculino", "Masculino para sexo"):
            print("⚠️ Radio Masculino não encontrado - tentando prosseguir...")
        
        # Estado civil (Casado)
        if not clicar_radio_via_javascript(driver, "Casado", "Casado para estado civil"):
            print("⚠️ Radio Casado não encontrado - tentando prosseguir...")
        
        # E-mail
        if not preencher_com_delay_extremo(driver, By.XPATH, "//input[@type='email']", "lrotero@gmail.com", "e-mail"):
            print("⚠️ Campo e-mail não encontrado - tentando alternativas...")
            try:
                campo_email = driver.find_element(By.XPATH, "//input[contains(@name, 'email') or contains(@id, 'email')]")
                campo_email.clear()
                campo_email.send_keys("lrotero@gmail.com")
                print("✅ E-mail preenchido via alternativa")
            except:
                print("❌ Campo e-mail não encontrado")
        
        # Celular
        if not preencher_com_delay_extremo(driver, By.XPATH, "//input[@placeholder='Celular']", "(11) 97668-7668", "celular"):
            print("⚠️ Campo celular não encontrado - tentando alternativas...")
            try:
                campo_celular = driver.find_element(By.XPATH, "//input[contains(@name, 'celular') or contains(@id, 'celular') or contains(@name, 'telefone')]")
                campo_celular.clear()
                campo_celular.send_keys("(11) 97668-7668")
                print("✅ Celular preenchido via alternativa")
            except:
                print("❌ Campo celular não encontrado")
        
        # Clicar em Continuar
        print("⏳ Aguardando botão Continuar aparecer...")
        
        if not clicar_com_delay_extremo(driver, By.XPATH, "//button[contains(., 'Continuar')]", "botão Continuar Tela 9"):
            print("❌ Erro: Falha ao clicar Continuar na Tela 9")
            return False
        
        # AGUARDAR CARREGAMENTO COMPLETO
        print("⏳ Aguardando carregamento da página...")
        time.sleep(15)
        
        if not aguardar_carregamento_pagina(driver, 60):
            print("⚠️ Página pode não ter carregado completamente")
        
        # AGUARDAR ESTABILIZAÇÃO EXTREMA
        aguardar_estabilizacao(driver, 20)
        
        salvar_estado_tela(driver, 9, "apos_continuar", None)
        print("✅ **TELA 9 IMPLEMENTADA COM SUCESSO! (Dados pessoais preenchidos)**")
        return True
        
    except Exception as e:
        print(f"❌ Erro na Tela 9: {e}")
        return False

def implementar_tela10(driver):
    """Implementa a Tela 10 (Condutor principal)"""
    print("\n📱 **INICIANDO TELA 10: Condutor principal**")
    
    # Aguardar Tela 10 carregar
    print("⏳ Aguardando Tela 10 carregar...")
    
    try:
        # Aguardar elementos da pergunta
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'condutor principal') or contains(text(), 'condutor')]"))
        )
        print("✅ Tela 10 carregada - pergunta sobre condutor principal detectada!")
        
        salvar_estado_tela(driver, 10, "inicial", None)
        
        if not aguardar_carregamento_pagina(driver, 30):
            print("❌ Erro: Página não carregou completamente")
            return False
        
        salvar_estado_tela(driver, 10, "pergunta_carregada", None)
        
        # Selecionar "Sim" para condutor principal
        print("⏳ Selecionando 'Sim' para condutor principal...")
        
        if not clicar_radio_via_javascript(driver, "Sim", "Sim para condutor principal"):
            print("⚠️ Radio 'Sim' não encontrado - tentando prosseguir...")
        
        # Clicar em Continuar
        print("⏳ Aguardando botão Continuar aparecer...")
        
        if not clicar_com_delay_extremo(driver, By.XPATH, "//button[contains(., 'Continuar')]", "botão Continuar Tela 10"):
            print("❌ Erro: Falha ao clicar Continuar na Tela 10")
            return False
        
        # AGUARDAR CARREGAMENTO COMPLETO
        print("⏳ Aguardando carregamento da página...")
        time.sleep(15)
        
        if not aguardar_carregamento_pagina(driver, 60):
            print("⚠️ Página pode não ter carregado completamente")
        
        # AGUARDAR ESTABILIZAÇÃO EXTREMA
        aguardar_estabilizacao(driver, 20)
        
        salvar_estado_tela(driver, 10, "apos_continuar", None)
        print("✅ **TELA 10 IMPLEMENTADA COM SUCESSO! (Condutor principal Sim)**")
        return True
        
    except Exception as e:
        print(f"❌ Erro na Tela 10: {e}")
        return False

# CONTINUA NA PARTE 4...
