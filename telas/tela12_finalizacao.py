#!/usr/bin/env python3
"""
Tela 12: Finalização e resultado
"""

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.helpers import (
    aguardar_carregamento_pagina, aguardar_estabilizacao,
    clicar_continuar_corrigido, salvar_estado_tela
)

def implementar_tela12(driver, parametros):
    """Implementa a Tela 12: Finalização e resultado"""
    print("\n **INICIANDO TELA 12: Finalização e resultado**")
    
    try:
        # Aguardar elementos de finalização
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'finalizar') or contains(text(), 'Finalizar') or contains(text(), 'resultado') or contains(text(), 'Resultado') or contains(text(), 'cotação') or contains(text(), 'Cotação')]"))
        )
        print("✅ Tela 12 carregada - finalização detectada!")
        
        salvar_estado_tela(driver, 12, "inicial", None)
        
        if not aguardar_carregamento_pagina(driver, 20):
            print("❌ Erro: Página não carregou completamente")
            return False
        
        salvar_estado_tela(driver, 12, "finalizacao_carregada", None)
        
        # Aguardar processamento da cotação
        print("⏳ Aguardando processamento da cotação...")
        time.sleep(10)
        
        salvar_estado_tela(driver, 12, "processamento_aguardado", None)
        
        # Verificar se há botão para finalizar
        try:
            if clicar_continuar_corrigido(driver, "botão Finalizar Tela 12"):
                print("✅ Botão Finalizar clicado com sucesso!")
            else:
                print("⚠️ Botão Finalizar não encontrado - cotação pode estar completa")
        except:
            print("⚠️ Erro ao clicar Finalizar - tentando prosseguir...")
        
        # Aguardar resultado final
        print("⏳ Aguardando resultado final...")
        time.sleep(8)
        
        if not aguardar_carregamento_pagina(driver, 60):
            print("⚠️ Página pode não ter carregado completamente")
        
        aguardar_estabilizacao(driver, 5)
        salvar_estado_tela(driver, 12, "resultado_final", None)
        print("✅ **TELA 12 IMPLEMENTADA COM SUCESSO!**")
        return True
        
    except Exception as e:
        print(f"❌ Erro na Tela 12: {e}")
        return False
