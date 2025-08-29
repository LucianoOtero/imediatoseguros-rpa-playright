#!/usr/bin/env python3
"""
Tela 11: Coberturas adicionais
"""

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.helpers import (
    aguardar_carregamento_pagina, aguardar_estabilizacao,
    clicar_radio_via_javascript, clicar_continuar_corrigido, 
    salvar_estado_tela
)

def implementar_tela11(driver, parametros):
    """Implementa a Tela 11: Coberturas adicionais"""
    print("\n **INICIANDO TELA 11: Coberturas adicionais**")
    
    try:
        # Aguardar elementos de coberturas
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'cobertura') or contains(text(), 'Cobertura') or contains(text(), 'seguro') or contains(text(), 'Seguro')]"))
        )
        print("✅ Tela 11 carregada - coberturas adicionais detectadas!")
        
        salvar_estado_tela(driver, 11, "inicial", None)
        
        if not aguardar_carregamento_pagina(driver, 20):
            print("❌ Erro: Página não carregou completamente")
            return False
        
        salvar_estado_tela(driver, 11, "coberturas_carregadas", None)
        
        # Selecionar coberturas padrão (se disponíveis)
        print("⏳ Verificando coberturas disponíveis...")
        
        # Tentar selecionar coberturas comuns
        coberturas_comuns = ["Assistência 24h", "Carro reserva", "Vidros", "Roubo", "Furto"]
        
        for cobertura in coberturas_comuns:
            try:
                if clicar_radio_via_javascript(driver, cobertura, f"{cobertura} como cobertura"):
                    print(f"✅ Cobertura {cobertura} selecionada")
                else:
                    print(f"⚠️ Cobertura {cobertura} não encontrada")
            except:
                print(f"⚠️ Erro ao selecionar cobertura {cobertura}")
        
        # Clicar em Continuar
        print("⏳ Aguardando botão Continuar aparecer...")
        
        if not clicar_continuar_corrigido(driver, "botão Continuar Tela 11"):
            print("❌ Erro: Falha ao clicar Continuar na Tela 11")
            return False
        
        print("⏳ Aguardando carregamento da página...")
        time.sleep(8)
        
        if not aguardar_carregamento_pagina(driver, 30):
            print("⚠️ Página pode não ter carregado completamente")
        
        aguardar_estabilizacao(driver, 5)
        salvar_estado_tela(driver, 11, "apos_continuar", None)
        print("✅ **TELA 11 IMPLEMENTADA COM SUCESSO!**")
        return True
        
    except Exception as e:
        print(f"❌ Erro na Tela 11: {e}")
        return False
