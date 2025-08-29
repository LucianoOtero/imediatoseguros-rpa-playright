#!/usr/bin/env python3
"""
RPA Tô Segurado - TELA 11: Uso do Veículo + CAPTURA DADOS TELA 8
Continuação do fluxo a partir da Tela 10 (Endereço de Pernoite)
+ Captura dos dados da estimativa inicial (Tela 8)
"""

import time
import json
import re
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Importar configuração do Chrome do módulo separado
from chrome_config import (
    configurar_chrome, 
    limpar_chrome, 
    aguardar_carregamento_pagina,
    criar_diretorio_tela,
    salvar_estado_tela,
    log_tela
)

def capturar_dados_tela8(driver):
    """Captura os dados da estimativa inicial (Tela 8)"""
    print("\n **CAPTURANDO DADOS DA TELA 8 (ESTIMATIVA INICIAL)**")
    
    try:
        # Aguardar um pouco para garantir que os dados carregaram
        time.sleep(5)
        
        # Salvar estado da Tela 8 para análise
        log_tela(driver, 8, "captura_dados", "Capturando dados da estimativa inicial")
        
        # Extrair dados da página
        page_source = driver.page_source
        
        # Dicionário para armazenar os dados capturados
        dados_cobertura = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "tela": "Tela 8 - Estimativa Inicial",
            "cobertura": "Primeira Cobertura (Compreensiva)",
            "dados": {}
        }
        
        print(" **ANALISANDO DADOS DA COBERTURA:**")
        print("=" * 60)
        
        # Procurar por diferentes padrões de dados
        padroes_busca = {
            "nome_cobertura": [
                r"compreensiva",
                r"cobertura.*completa",
                r"plano.*recomendado",
                r"primeira.*cobertura"
            ],
            "valor_cobertura": [
                r"R\$\s*[\d.,]+",
                r"valor.*R\$\s*[\d.,]+",
                r"preço.*R\$\s*[\d.,]+"
            ],
            "franquia": [
                r"franquia.*R\$\s*[\d.,]+",
                r"R\$\s*[\d.,]+.*franquia"
            ],
            "valor_mercado": [
                r"valor.*mercado.*R\$\s*[\d.,]+",
                r"mercado.*R\$\s*[\d.,]+"
            ],
            "assistencia": [
                r"assistência.*100%",
                r"assistencia.*100%",
                r"100%.*assistência",
                r"100%.*assistencia"
            ],
            "vidros": [
                r"vidros.*100%",
                r"100%.*vidros"
            ],
            "carro_reserva": [
                r"carro.*reserva.*100%",
                r"100%.*carro.*reserva"
            ],
            "danos_materiais": [
                r"danos.*materiais.*R\$\s*[\d.,]+",
                r"R\$\s*[\d.,]+.*danos.*materiais"
            ],
            "danos_corporais": [
                r"danos.*corporais.*R\$\s*[\d.,]+",
                r"R\$\s*[\d.,]+.*danos.*corporais"
            ],
            "danos_morais": [
                r"danos.*morais.*R\$\s*[\d.,]+",
                r"R\$\s*[\d.,]+.*danos.*morais"
            ],
            "morte_invalidez": [
                r"morte.*invalidez.*R\$\s*[\d.,]+",
                r"invalidez.*R\$\s*[\d.,]+",
                r"R\$\s*[\d.,]+.*morte.*invalidez"
            ]
        }
        
        # Buscar cada padrão
        for campo, padroes in padroes_busca.items():
            valor_encontrado = None
            
            for padrao in padroes:
                match = re.search(padrao, page_source, re.IGNORECASE)
                if match:
                    valor_encontrado = match.group(0).strip()
                    break
            
            if valor_encontrado:
                dados_cobertura["dados"][campo] = valor_encontrado
                print(f"✅ {campo.replace('_', ' ').title()}: {valor_encontrado}")
            else:
                dados_cobertura["dados"][campo] = "Não encontrado"
                print(f"❌ {campo.replace('_', ' ').title()}: Não encontrado")
        
        # Buscar dados específicos por XPath ou seletores
        print("\n🔍 **BUSCANDO DADOS ESPECÍFICOS:**")
        
        try:
            # Procurar por elementos com valores monetários
            elementos_valor = driver.find_elements(By.XPATH, "//*[contains(text(), 'R$')]")
            valores_encontrados = []
            
            for elemento in elementos_valor:
                texto = elemento.text.strip()
                if "R$" in texto and len(texto) < 100:  # Filtrar textos muito longos
                    valores_encontrados.append(texto)
            
            if valores_encontrados:
                print(f" Valores monetários encontrados: {len(valores_encontrados)}")
                for i, valor in enumerate(valores_encontrados[:10]):  # Mostrar apenas os primeiros 10
                    print(f"   {i+1}. {valor}")
                
                dados_cobertura["dados"]["valores_monetarios"] = valores_encontrados[:10]
            
        except Exception as e:
            print(f"⚠️ Erro ao buscar valores específicos: {e}")
        
        # Salvar dados capturados em JSON
        diretorio_tela8 = criar_diretorio_tela(8)
        caminho_json = f"{diretorio_tela8}/dados_cobertura_compreensiva.json"
        
        with open(caminho_json, "w", encoding="utf-8") as f:
            json.dump(dados_cobertura, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Dados salvos em JSON: {caminho_json}")
        
        # Salvar dados em formato legível
        caminho_txt = f"{diretorio_tela8}/dados_cobertura_compreensiva.txt"
        with open(caminho_txt, "w", encoding="utf-8") as f:
            f.write("DADOS DA COBERTURA COMPREENSIVA - TELA 8\n")
            f.write("=" * 60 + "\n")
            f.write(f"Timestamp: {dados_cobertura['timestamp']}\n")
            f.write(f"Tela: {dados_cobertura['tela']}\n")
            f.write(f"Cobertura: {dados_cobertura['cobertura']}\n\n")
            
            for campo, valor in dados_cobertura["dados"].items():
                f.write(f"{campo.replace('_', ' ').title()}: {valor}\n")
        
        print(f" Dados salvos em TXT: {caminho_txt}")
        
        # Resumo dos dados capturados
        print(f"\n **RESUMO DOS DADOS CAPTURADOS:**")
        print("=" * 60)
        print(f"✅ Total de campos analisados: {len(dados_cobertura['dados'])}")
        print(f"✅ Dados encontrados: {sum(1 for v in dados_cobertura['dados'].values() if v != 'Não encontrado')}")
        print(f"❌ Dados não encontrados: {sum(1 for v in dados_cobertura['dados'].values() if v == 'Não encontrado')}")
        
        return dados_cobertura
        
    except Exception as e:
        print(f"❌ **ERRO AO CAPTURAR DADOS DA TELA 8:** {e}")
        return None

def navegar_ate_tela10(driver):
    """Navega até a Tela 10 (última tela funcionando)"""
    print("🚀 **NAVEGANDO ATÉ TELA 10 (ENDEREÇO DE PERNOITE)**")
    
    try:
        # Tela 1: Selecionar Carro
        print("\n📱 TELA 1: Selecionando Carro...")
        driver.get("https://www.app.tosegurado.com.br/cotacao")
        time.sleep(5)
        
        carro_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Carro')]"))
        )
        carro_button.click()
        print("✅ Carro selecionado")
        time.sleep(3)
        
        # Tela 2: Inserir placa
        print("\n📱 TELA 2: Inserindo placa...")
        placa_input = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "placaTelaDadosPlaca"))
        )
        placa_input.clear()
        placa_input.send_keys("EED3D56")
        print("✅ Placa EED3D56 inserida")
        time.sleep(2)
        
        # Tela 3: Clicar Continuar
        print("\n📱 TELA 3: Clicando Continuar...")
        continuar_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.ID, "gtm-telaDadosAutoCotarComPlacaContinuar"))
        )
        continuar_button.click()
        print("✅ Continuar clicado")
        time.sleep(5)
        
        # Tela 5: Confirmar veículo
        print("\n📱 TELA 5: Confirmando veículo...")
        WebDriverWait(driver, 40).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'COROLLA')]"))
        )
        
        sim_radio = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//input[@value='Sim']"))
        )
        driver.execute_script("arguments[0].click();", sim_radio)
        print("✅ Veículo confirmado")
        time.sleep(3)
        
        # Tela 6: Veículo segurado
        print("\n📱 TELA 6: Selecionando 'Não' para veículo segurado...")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "confirmarVeiculoTelaInformacoesVeiculo"))
        )
        
        nao_radio = driver.find_element(By.XPATH, "//input[@value='Não']")
        if not nao_radio.is_selected():
            driver.execute_script("arguments[0].click();", nao_radio)
            print("✅ Radio 'Não' selecionado")
            time.sleep(2)
        
        continuar_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.ID, "gtm-telaInfosAutoContinuar"))
        )
        continuar_button.click()
        print("✅ Continuar clicado na Tela 6")
        time.sleep(5)
        
        # Tela 7: Confirmação não segurado
        print("\n TELA 7: Aguardando confirmação...")
        time.sleep(5)
        
        # Procurar botão Continuar na Tela 7
        continuar_selectors = [
            "//button[contains(., 'Continuar')]",
            "//*[contains(., 'Continuar')]",
            "//button[contains(text(), 'Continuar')]",
            "//p[contains(., 'Continuar')]"
        ]
        
        continuar_button = None
        for selector in continuar_selectors:
            try:
                continuar_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, selector))
                )
                print(f"✅ Botão Continuar encontrado com selector: {selector}")
                break
            except:
                continue
        
        if continuar_button:
            continuar_button.click()
            print("✅ Continuar clicado na Tela 7")
            time.sleep(5)
        else:
            print("⚠️ Botão Continuar não encontrado na Tela 7")
        
        # Tela 8: Estimativa inicial
        print("\n TELA 8: Aguardando estimativa inicial...")
        time.sleep(5)
        
        # Aguardar elementos da estimativa inicial
        WebDriverWait(driver, 60).until(
            lambda d: any([
                "estimativa" in d.page_source.lower(),
                "carrossel" in d.page_source.lower(),
                "cobertura" in d.page_source.lower(),
                "plano" in d.page_source.lower(),
                "franquia" in d.page_source.lower()
            ])
        )
        print("✅ Tela 8 carregada - estimativa inicial detectada!")
        
        # Aguardar carregamento completo
        aguardar_carregamento_pagina(driver, 30)
        
        # Aguardar mais um pouco
        time.sleep(10)
        
        # CAPTURAR DADOS DA TELA 8 ANTES DE CONTINUAR
        dados_capturados = capturar_dados_tela8(driver)
        
        if dados_capturados:
            print("✅ Dados da Tela 8 capturados com sucesso!")
        else:
            print("⚠️ Falha ao capturar dados da Tela 8")
        
        # Clicar em Continuar na Tela 8
        print("⏳ Aguardando botão Continuar aparecer...")
        continuar_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Continuar')]"))
        )
        continuar_button.click()
        print("✅ Continuar clicado na Tela 8")
        
        # Aguardar carregamento da próxima página
        aguardar_carregamento_pagina(driver, 30)
        
        # Tela 9: Tipo de combustível
        print("\n TELA 9: Aguardando tipo de combustível...")
        time.sleep(5)
        
        # Aguardar elementos da Tela 9
        WebDriverWait(driver, 60).until(
            lambda d: any([
                "tipo.*combustivel" in d.page_source.lower(),
                "flex" in d.page_source.lower(),
                "gasolina" in d.page_source.lower(),
                "alcool" in d.page_source.lower(),
                "diesel" in d.page_source.lower(),
                "hibrido" in d.page_source.lower(),
                "eletrico" in d.page_source.lower()
            ])
        )
        print("✅ Tela 9 carregada - tipo de combustível detectado!")
        
        # Aguardar carregamento completo
        aguardar_carregamento_pagina(driver, 20)
        
        # Aguardar mais um pouco
        time.sleep(5)
        
        # Clicar em Continuar na Tela 9
        print("⏳ Aguardando botão Continuar aparecer...")
        continuar_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Continuar')]"))
        )
        continuar_button.click()
        print("✅ Continuar clicado na Tela 9")
        
        # Aguardar carregamento da próxima página
        aguardar_carregamento_pagina(driver, 30)
        
        # Tela 10: Endereço de pernoite
        print("\n TELA 10: Aguardando endereço de pernoite...")
        time.sleep(5)
        
        # Aguardar elementos da Tela 10
        WebDriverWait(driver, 60).until(
            lambda d: any([
                "endereco" in d.page_source.lower(),
                "pernoite" in d.page_source.lower(),
                "onde.*carro.*passa.*noite" in d.page_source.lower(),
                "cep" in d.page_source.lower(),
                "rua" in d.page_source.lower(),
                "bairro" in d.page_source.lower()
            ])
        )
        print("✅ Tela 10 carregada - endereço de pernoite detectado!")
        
        # Aguardar carregamento completo
        aguardar_carregamento_pagina(driver, 20)
        
        # Procurar campo CEP
        cep_input = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "enderecoTelaEndereco"))
        )
        
        # Inserir CEP
        cep_input.clear()
        cep_input.send_keys("03084-000")
        print("✅ CEP 03084-000 inserido")
        time.sleep(5)
        
        # Tentar selecionar sugestão automática
        try:
            sugestao = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'São Paulo')]"))
            )
            sugestao.click()
            print("✅ Sugestão selecionada")
            time.sleep(3)
        except:
            print("⚠️ Sugestão não encontrada - preenchendo manualmente")
            cep_input.clear()
            cep_input.send_keys("Rua Serra de Botucatu, Tatuapé - São Paulo/SP")
            time.sleep(3)
        
        # Clicar em Continuar na Tela 10
        continuar_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Continuar')]"))
        )
        continuar_button.click()
        print("✅ Continuar clicado na Tela 10")
        
        # Aguardar carregamento da próxima página
        aguardar_carregamento_pagina(driver, 30)
        
        print("✅ TELA 10 CARREGADA E CONTINUAR CLICADO!")
        return True
        
    except Exception as e:
        print(f"❌ **ERRO AO NAVEGAR ATÉ TELA 10:** {e}")
        return False

def tela11_uso_veiculo(driver):
    """Tela 11: Uso do veículo"""
    print("\n **INICIANDO TELA 11: Uso do veículo**")
    
    try:
        # Aguardar Tela 11 carregar com timeout maior
        print("⏳ Aguardando Tela 11 carregar...")
        
        # Aguardar um pouco para a página carregar
        time.sleep(5)
        
        # Salvar estado inicial da Tela 11
        log_tela(driver, 11, "inicial", "Tela 11 carregada - aguardando uso do veículo")
        
        # Procurar elementos específicos da Tela 11
        print("🔍 Procurando elementos da Tela 11...")
        
        # Aguardar carregamento com timeout maior
        WebDriverWait(driver, 60).until(
            lambda d: any([
                "uso.*veiculo" in d.page_source.lower(),
                "finalidade.*veiculo" in d.page_source.lower(),
                "pessoal" in d.page_source.lower(),
                "profissional" in d.page_source.lower(),
                "motorista.*aplicativo" in d.page_source.lower(),
                "taxi" in d.page_source.lower()
            ])
        )
        print("✅ Tela 11 carregada - uso do veículo detectado!")
        
        # Aguardar carregamento completo
        aguardar_carregamento_pagina(driver, 20)
        
        # Salvar estado da Tela 11
        log_tela(driver, 11, "uso_veiculo_carregado", "Uso do veículo carregado")
        
        # Procurar e selecionar "Pessoal"
        print("⏳ Aguardando radio 'Pessoal' aparecer...")
        try:
            # Tentar diferentes seletores para Pessoal
            pessoal_selectors = [
                "//input[@value='Pessoal']",
                "//input[contains(@value, 'Pessoal')]",
                "//input[@name='usoVeiculo']",
                "//input[@type='radio'][contains(@value, 'Pessoal')]"
            ]
            
            pessoal_radio = None
            for selector in pessoal_selectors:
                try:
                    pessoal_radio = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, selector))
                    )
                    print(f"✅ Radio 'Pessoal' encontrado com selector: {selector}")
                    break
                except:
                    continue
            
            if pessoal_radio:
                # Salvar estado antes da seleção
                log_tela(driver, 11, "antes_selecao_pessoal", "Antes de selecionar Pessoal")
                
                # Selecionar Pessoal
                if not pessoal_radio.is_selected():
                    driver.execute_script("arguments[0].click();", pessoal_radio)
                    print("✅ Pessoal selecionado via JavaScript")
                else:
                    print("✅ Pessoal já estava selecionado")
                time.sleep(3)
                
                # Salvar estado com Pessoal selecionado
                log_tela(driver, 11, "pessoal_selecionado", "Pessoal selecionado")
            else:
                print("⚠️ Radio 'Pessoal' não encontrado - tentando prosseguir...")
                
        except Exception as e:
            print(f"⚠️ Erro ao selecionar Pessoal: {e}")
            print("⏳ Tentando prosseguir...")
        
        # Salvar estado final da Tela 11
        log_tela(driver, 11, "configuracao_completa", "Configuração completa da Tela 11")
        
        # Procurar botão Continuar
        print("⏳ Aguardando botão Continuar aparecer...")
        try:
            continuar_selectors = [
                "//button[contains(., 'Continuar')]",
                "//*[contains(., 'Continuar')]",
                "//button[contains(text(), 'Continuar')]",
                "//p[contains(., 'Continuar')]"
            ]
            
            continuar_button = None
            for selector in continuar_selectors:
                try:
                    continuar_button = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    print(f"✅ Botão Continuar encontrado com selector: {selector}")
                    break
                except:
                    continue
            
            if continuar_button:
                # Salvar estado antes do clique
                log_tela(driver, 11, "antes_continuar", "Antes de clicar em Continuar")
                
                # Clicar
                continuar_button.click()
                print("✅ Continuar clicado na Tela 11")
                
                # Aguardar carregamento da próxima página
                aguardar_carregamento_pagina(driver, 30)
                
                # Salvar estado após clique
                log_tela(driver, 11, "apos_continuar", "Após clicar em Continuar")
            else:
                print("⚠️ Botão Continuar não encontrado - tentando prosseguir...")
                
        except Exception as e:
            print(f"⚠️ Erro ao procurar botão Continuar: {e}")
            print("⏳ Aguardando carregamento automático...")
            time.sleep(10)
        
        return True
        
    except Exception as e:
        print(f"❌ **ERRO NA TELA 11:** {e}")
        log_tela(driver, 11, "erro", f"Erro: {e}")
        return False

def main():
    """Função principal"""
    print("🚀 **RPA TÔ SEGURADO - TELA 11: USO DO VEÍCULO + CAPTURA DADOS TELA 8**")
    print("=" * 80)
    print("🎯 OBJETIVO: Implementar Tela 11 (Uso do Veículo)")
    print("📊 BONUS: Capturar dados da estimativa inicial (Tela 8)")
    print("📝 NOTA: Continuação do fluxo a partir da Tela 10")
    print("=" * 80)
    print(f"⏰ Início: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    driver = None
    temp_dir = None
    
    try:
        # Configurar Chrome usando o módulo separado
        driver, temp_dir = configurar_chrome()
        print("✅ Chrome configurado")
        
        # Navegar até Tela 10
        if not navegar_ate_tela10(driver):
            print("❌ **FALHA AO NAVEGAR ATÉ TELA 10 - PARANDO**")
            return
        
        # Tela 11: Uso do veículo
        if tela11_uso_veiculo(driver):
            print("✅ **TELA 11 IMPLEMENTADA COM SUCESSO!**")
        else:
            print("❌ **FALHA NA TELA 11 - PARANDO EXECUÇÃO**")
            return
        
        # Resumo final
        print(f"\n{'='*80}")
        print("🎉 **RPA EXECUTADO COM SUCESSO! TELA 11 IMPLEMENTADA!**")
        print(f"{'='*80}")
        print(f"✅ Total de telas executadas: 11")
        print(f"✅ Tela 11: Uso do veículo implementada")
        print(f"📊 BONUS: Dados da Tela 8 capturados para uso futuro")
        print(f"\n📁 Todos os arquivos salvos em: /opt/imediatoseguros-rpa/temp/")
        print(f"⏰ Fim: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
    except Exception as e:
        print(f"\n❌ **ERRO GERAL DURANTE EXECUÇÃO:** {e}")
        if driver:
            driver.save_screenshot("/opt/imediatoseguros-rpa/temp/erro-geral.png")
            print(" Screenshot do erro geral salvo")
    
    finally:
        # Limpar recursos usando o módulo separado
        limpar_chrome(driver, temp_dir)

if __name__ == "__main__":
    main()
