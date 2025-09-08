#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tela 5 - Carrossel de Estimativas
Módulo isolado para navegação e captura de dados da Tela 5
"""

import time
import json
import os
from datetime import datetime
from typing import Dict, Any
from playwright.sync_api import Page


def exibir_mensagem(mensagem: str):
    """Exibe mensagem formatada"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {mensagem}")


def esperar_carregamento_pagina(page: Page, timeout: int = 30):
    """Espera o carregamento completo da página"""
    try:
        page.wait_for_load_state("networkidle", timeout=timeout * 1000)
        time.sleep(2)
    except Exception as e:
        exibir_mensagem(f"⚠️ Timeout no carregamento da página: {e}")


def navegar_tela_5_playwright(page: Page) -> bool:
    """
    Navega para a Tela 5 e aguarda carregamento do carrossel de estimativas
    """
    try:
        exibir_mensagem("🎯 NAVEGANDO PARA TELA 5 - CARROSSEL DE ESTIMATIVAS")
        
        # Aguardar carregamento inicial
        esperar_carregamento_pagina(page)
        
        # Aguardar carrossel de estimativas
        exibir_mensagem("⏳ Aguardando carrossel de estimativas...")
        
        # Aguardar elementos do carrossel
        carrossel_selector = "div[data-testid='carrossel-estimativas']"
        try:
            page.wait_for_selector(carrossel_selector, timeout=30000)
            exibir_mensagem("✅ Carrossel de estimativas detectado")
        except Exception as e:
            exibir_mensagem(f"⚠️ Carrossel não encontrado com selector específico: {e}")
            
            # Tentar selector alternativo
            try:
                page.wait_for_selector(".carrossel-estimativas", timeout=10000)
                exibir_mensagem("✅ Carrossel detectado com selector alternativo")
            except Exception as e2:
                exibir_mensagem(f"⚠️ Selector alternativo também falhou: {e2}")
                
                # Aguardar qualquer elemento que possa ser o carrossel
                try:
                    page.wait_for_function("""
                        () => {
                            const elements = document.querySelectorAll('div');
                            return Array.from(elements).some(el => 
                                el.textContent && (
                                    el.textContent.includes('estimativa') || 
                                    el.textContent.includes('cobertura') ||
                                    el.textContent.includes('plano')
                                )
                            );
                        }
                    """, timeout=15000)
                    exibir_mensagem("✅ Elementos de estimativa detectados via JavaScript")
                except Exception as e3:
                    exibir_mensagem(f"❌ Falha na detecção de elementos de estimativa: {e3}")
                    return False
        
        # Aguardar carregamento dos dados
        exibir_mensagem("⏳ Aguardando carregamento dos dados...")
        time.sleep(5)  # Aguarda carregamento dos dados
        
        # Verificar se há skeletons de carregamento
        try:
            skeletons = page.query_selector_all(".MuiSkeleton-root")
            if skeletons:
                exibir_mensagem(f"⏳ Aguardando {len(skeletons)} skeletons de carregamento...")
                page.wait_for_function("""
                    () => {
                        const skeletons = document.querySelectorAll('.MuiSkeleton-root');
                        return skeletons.length === 0;
                    }
                """, timeout=20000)
                exibir_mensagem("✅ Skeletons de carregamento finalizados")
        except Exception as e:
            exibir_mensagem(f"⚠️ Não foi possível aguardar skeletons: {e}")
        
        # Aguarda adicional para garantir carregamento completo
        time.sleep(3)
        
        exibir_mensagem("✅ TELA 5 CARREGADA COM SUCESSO!")
        return True
        
    except Exception as e:
        exibir_mensagem(f"❌ ERRO NA TELA 5: {e}")
        return False


def capturar_dados_carrossel_estimativas_playwright(page: Page) -> Dict[str, Any]:
    """
    Captura dados detalhados do carrossel de estimativas na Tela 5
    """
    try:
        exibir_mensagem("🔍 CAPTURANDO DADOS DO CARROSSEL DE ESTIMATIVAS")
        
        # Aguardar carregamento adicional
        time.sleep(2)
        
        # Capturar dados via JavaScript
        dados_capturados = page.evaluate("""
            () => {
                const dados = {
                    coberturas_detalhadas: [],
                    valores_encontrados: 0,
                    timestamp_captura: new Date().toISOString()
                };
                
                // Função para extrair texto limpo
                const limparTexto = (texto) => {
                    if (!texto) return '';
                    return texto.replace(/\\s+/g, ' ').trim();
                };
                
                // Função para extrair valores monetários
                const extrairValor = (texto) => {
                    if (!texto) return null;
                    const match = texto.match(/R\\$\\s*([\\d.,]+)/);
                    return match ? match[1].replace('.', '').replace(',', '.') : null;
                };
                
                // Buscar elementos de cobertura
                const elementosCobertura = document.querySelectorAll('div[data-testid*="cobertura"], div[class*="cobertura"], div[class*="plano"], div[class*="estimativa"]');
                
                console.log('Elementos de cobertura encontrados:', elementosCobertura.length);
                
                // Se não encontrar com data-testid, buscar por texto
                if (elementosCobertura.length === 0) {
                    const todosDivs = document.querySelectorAll('div');
                    for (let div of todosDivs) {
                        const texto = div.textContent || '';
                        if (texto.includes('cobertura') || texto.includes('plano') || texto.includes('estimativa')) {
                            elementosCobertura.push(div);
                        }
                    }
                }
                
                // Processar cada elemento de cobertura
                elementosCobertura.forEach((elemento, index) => {
                    const textoCompleto = elemento.textContent || '';
                    const textoLimpo = limparTexto(textoCompleto);
                    
                    if (textoLimpo.length > 10) {  // Filtrar elementos com texto significativo
                        const cobertura = {
                            indice: index + 1,
                            texto_completo: textoCompleto,
                            texto_limpo: textoLimpo,
                            nome_cobertura: '',
                            valores: {},
                            beneficios: [],
                            elemento_html: elemento.outerHTML.substring(0, 500)  // Primeiros 500 chars
                        };
                        
                        // Tentar extrair nome da cobertura
                        const linhas = textoLimpo.split('\\n').filter(linha => linha.trim());
                        if (linhas.length > 0) {
                            cobertura.nome_cobertura = linhas[0];
                        }
                        
                        // Extrair valores monetários
                        const valores = textoCompleto.match(/R\\$\\s*([\\d.,]+)/g);
                        if (valores) {
                            cobertura.valores = {
                                de: valores[0] ? valores[0].replace('R$', '').trim() : null,
                                ate: valores[1] ? valores[1].replace('R$', '').trim() : null
                            };
                        }
                        
                        // Extrair benefícios
                        const beneficios = textoCompleto.match(/[•\\-]\\s*([^\\n]+)/g);
                        if (beneficios) {
                            cobertura.beneficios = beneficios.map(b => ({
                                nome: b.replace(/[•\\-]\\s*/, '').trim()
                            }));
                        }
                        
                        dados.coberturas_detalhadas.push(cobertura);
                    }
                });
                
                dados.valores_encontrados = dados.coberturas_detalhadas.length;
                
                // Log para debug
                console.log('Dados capturados:', dados);
                
                return dados;
            }
        """)
        
        exibir_mensagem(f"📊 DADOS CAPTURADOS:")
        exibir_mensagem(f"   • Total de coberturas: {dados_capturados['valores_encontrados']}")
        exibir_mensagem(f"   • Timestamp: {dados_capturados['timestamp_captura']}")
        
        # Exibir detalhes das coberturas encontradas
        for i, cobertura in enumerate(dados_capturados['coberturas_detalhadas']):
            exibir_mensagem(f"   📋 Cobertura {i+1}: {cobertura['nome_cobertura']}")
            if cobertura['valores']:
                exibir_mensagem(f"      💰 Valores: {cobertura['valores']}")
            if cobertura['beneficios']:
                beneficios = [b['nome'] for b in cobertura['beneficios']]
                exibir_mensagem(f"      🎁 Benefícios: {', '.join(beneficios[:3])}...")
        
        return dados_capturados
        
    except Exception as e:
        exibir_mensagem(f"❌ ERRO NA CAPTURA DE DADOS: {e}")
        return {
            "coberturas_detalhadas": [],
            "valores_encontrados": 0,
            "erro": str(e),
            "timestamp_captura": datetime.now().isoformat()
        }


def salvar_dados_json(dados: Dict[str, Any], nome_arquivo: str = None):
    """Salva dados em arquivo JSON"""
    if not nome_arquivo:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_arquivo = f"temp/dados_tela_5_{timestamp}.json"
    
    # Criar diretório temp se não existir
    os.makedirs("temp", exist_ok=True)
    
    try:
        with open(nome_arquivo, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)
        exibir_mensagem(f"💾 Dados salvos em: {nome_arquivo}")
        return nome_arquivo
    except Exception as e:
        exibir_mensagem(f"❌ Erro ao salvar arquivo: {e}")
        return None








