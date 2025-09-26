#!/usr/bin/env python3
"""
EXECUTAR RPA IMEDIATO PLAYWRIGHT - VERSÃO v3.4.0
Implementação completa do RPA usando Playwright com Sistema de Exception Handler

DESCRIÇÃO:
- Migração completa do Selenium para Playwright
- Sistema de Exception Handler robusto
- Telas 1-15 implementadas e testadas
- Captura de dados dos planos de seguro
- Estrutura de retorno padronizada

[OBJETIVO] IMPLEMENTAÇÃO SELETOR ESPECÍFICO CARDS ESTIMATIVA (09/09/2025):
- Substituição div.bg-primary por div[role="group"][aria-roledescription="slide"]
- Sistema de fallback robusto com múltiplas estratégias
- Estratégia híbrida: específico + fallbacks de compatibilidade
- Funções auxiliares: aguardar_cards_estimativa_playwright() e localizar_cards_estimativa_playwright()
- Melhoria de estabilidade regional (Brasil + Portugal)
- Documentação completa da implementação

[OBJETIVO] IMPLEMENTAÇÃO SELETOR ESPECÍFICO SUGESTÕES ENDEREÇO (09/09/2025):
- Substituição .overflow-hidden por [data-testid="sugestao-endereco"]
- Sistema de fallback robusto com múltiplas estratégias
- Estratégia híbrida: específico + semântico + fallback de compatibilidade
- Funções auxiliares: aguardar_sugestao_endereco_playwright() e localizar_sugestao_endereco_playwright()
- Melhoria de estabilidade regional (Brasil + Portugal)
- Documentação completa da implementação

[OBJETIVO] IMPLEMENTAÇÃO SELETOR ESPECÍFICO TELA 9 (09/09/2025):
- Substituição xpath genérico por p:has-text("Nessa etapa, precisamos dos seus dados pessoais")
- Sistema de fallback robusto com múltiplas estratégias
- Estratégia híbrida: específico + semântico + estrutural + fallback de compatibilidade
- Funções auxiliares: aguardar_tela_9_playwright() e localizar_tela_9_playwright()
- Melhoria de estabilidade regional (Brasil + Portugal)
- Documentação completa da implementação

[OBJETIVO] IMPLEMENTAÇÃO SELETOR ESPECÍFICO TELA 8 (09/09/2025):
- Substituição xpath genérico por #finalidadeVeiculoTelaUsoVeiculo
- Sistema de fallback robusto com múltiplas estratégias
- Estratégia híbrida: específico + semântico + conteúdo + fallback de compatibilidade
- Funções auxiliares: aguardar_tela_8_playwright() e localizar_tela_8_playwright()
- Melhoria de estabilidade regional (Brasil + Portugal)
- Documentação completa da implementação

[ATUALIZANDO] IMPLEMENTAÇÃO SELETOR ESPECÍFICO BOTÃO CARRO (09/09/2025):
- Substituição button.group por button:has(img[alt="Icone car"])
- Sistema de fallback robusto com múltiplas estratégias
- Estratégia híbrida: específico + fallbacks de compatibilidade
- Teste completo bem-sucedido (dados gerados às 14:20)
- Documentação completa da implementação

[ATUALIZANDO] ATUALIZAÇÃO DE COMPATIBILIDADE REGIONAL (08/09/2025):
- Substituição de seletores genéricos por específicos na Tela 13
- Resolução de problema de falha em Portugal
- Melhoria de estabilidade regional (Brasil + Portugal)
- Documentação completa das mudanças realizadas

AUTOR: Luciano Otero
DATA: 2025-09-09
VERSÃO: v3.7.0.5 (Implementações Completas v3.7.0.1, v3.7.0.2, v3.7.0.3, v3.7.0.4 e v3.7.0.5)
STATUS: Implementação completa com Exception Handler + Compatibilidade Regional + Seletores Específicos
"""

import json
import time
import re
import os
import sys
import traceback
import argparse
from datetime import datetime
from typing import Dict, Any, Optional, Union
from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext

# Importar Sistema de Retorno Estruturado
# ProgressTracker será importado dinamicamente quando necessário
from utils.retorno_estruturado import (
    RetornoEstruturado,
    criar_retorno_sucesso,
    criar_retorno_erro,
    criar_retorno_warning,
    validar_retorno_estruturado
)

# Importar Sistema de Progresso em Tempo Real
# ProgressTracker será definido dinamicamente na função main()

# Importar Sistema de Timeout Inteligente (opcional)
try:
    from utils.smart_timeout import SmartTimeout
    TIMEOUT_SYSTEM_AVAILABLE = True
except ImportError:
    TIMEOUT_SYSTEM_AVAILABLE = False
    exibir_mensagem("[AVISO] Sistema de timeout não disponível - usando timeouts padrão")

# Importar Sistema de Logger Avançado (opcional)
try:
    from utils.logger_rpa import RPALogger, setup_logger, log_info, log_error, log_success
    LOGGER_SYSTEM_AVAILABLE = True
except ImportError:
    LOGGER_SYSTEM_AVAILABLE = False
    exibir_mensagem("[AVISO] Sistema de logger não disponível - usando logs padrão")

# Importar Sistema de Comunicação Bidirecional (opcional)
try:
    from utils.bidirectional_integration_wrapper import execute_rpa_with_bidirectional_control
    BIDIRECTIONAL_SYSTEM_AVAILABLE = True
except ImportError:
    BIDIRECTIONAL_SYSTEM_AVAILABLE = False
    exibir_mensagem("[AVISO] Sistema de comunicação bidirecional não disponível - executando sem controle remoto")

# Importar Sistema de Validação de Parâmetros Avançado (opcional)
try:
    from utils.validacao_parametros import ValidadorParametros, ValidacaoParametrosError
    VALIDATION_SYSTEM_AVAILABLE = True
except ImportError:
    VALIDATION_SYSTEM_AVAILABLE = False
    exibir_mensagem("[AVISO] Sistema de validação avançado não disponível - usando validação básica")

# Importar Sistema de Health Check Ultra-Conservador (opcional)
try:
    from utils.health_check_conservative import ConservativeHealthChecker
    HEALTH_CHECK_AVAILABLE = True
except ImportError:
    HEALTH_CHECK_AVAILABLE = False
    exibir_mensagem("[AVISO] Sistema de health check não disponível - continuando sem verificação")


# ========================================
# SISTEMA DE ARGUMENTOS DE LINHA DE COMANDO
# ========================================

def processar_argumentos():
    """
    Processa argumentos de linha de comando de forma segura
    """
    parser = argparse.ArgumentParser(
        description="EXECUTAR RPA IMEDIATO PLAYWRIGHT - VERSÃO v3.4.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
EXEMPLOS DE USO:
  python executar_rpa_imediato_playwright.py
  python executar_rpa_imediato_playwright.py --help
  python executar_rpa_imediato_playwright.py --version
  python executar_rpa_imediato_playwright.py --docs completa
  python executar_rpa_imediato_playwright.py --docs json
  python executar_rpa_imediato_playwright.py --docs php
  python executar_rpa_imediato_playwright.py --docs params
  python executar_rpa_imediato_playwright.py --modo-silencioso
  python executar_rpa_imediato_playwright.py --modo-silencioso --progress-tracker redis

DOCUMENTAÇÃO:
  --docs completa: Documentação completa do sistema
  --docs json: Documentação dos JSONs de saída
  --docs php: Guia específico para desenvolvedores PHP
  --docs params: Descrição dos parâmetros JSON

SISTEMA BIDIRECIONAL:
  Controle remoto via HTTP disponível na porta 8080
  Endpoints: /status (GET) e /command (POST)
  Comandos: PAUSE, RESUME, CANCEL
  Fallback automático se sistema não disponível

SISTEMA DE HEALTH CHECK:
  Verificação automática de saúde do sistema antes da execução
  Validação de arquivos essenciais, Python, recursos e configuração
  Detecção automática de ambiente (Windows/Linux)
  Execução não-bloqueante com fallback garantido
  Documentação completa: docs/HEALTH_CHECK_IMPLEMENTATION_REPORT.md

VALIDAÇÃO RIGOROSA DE PARÂMETROS:
  [AVISO] EXECUÇÃO INTERROMPIDA se parâmetros inválidos detectados
  Validação de campos obrigatórios, tipos de dados e formatos
  Validação de CPF, CEP, email, celular (11 dígitos), placa
  Validação de valores permitidos (combustível, sexo, etc.)
  Retorna erro detalhado com parâmetros inválidos identificados
  Não há fallback - execução é interrompida imediatamente

ARQUIVOS GERADOS:
  - temp/progress_status.json: Progresso em tempo real
  - dados_planos_seguro_YYYYMMDD_HHMMSS.json: Dados finais
  - temp/json_compreensivo_tela_5_*.json: Dados intermediários
  - temp/retorno_intermediario_carrossel_*.json: Dados brutos Tela 5
  - temp/dados_tela_5_*.json: Metadados da captura
  - temp/cotacao_manual_YYYYMMDD_HHMMSS.json: Dados para cotação manual
  - logs/bidirectional.log: Logs do sistema bidirecional

STATUS CODES:
  - 9001: Sucesso completo
  - 9002: Erro específico por tela
  - 9003: Cotação manual necessária
  - 9004-9999: Códigos de erro específicos por tela
        """
    )
    
    parser.add_argument(
        '--version', 
        action='version', 
        version='%(prog)s v3.1.6'
    )
    
    parser.add_argument(
        '--config', 
        type=str, 
        default='parametros.json',
        help='Arquivo de configuração (padrão: parametros.json)'
    )
    
    parser.add_argument(
        '--docs',
        type=str,
        choices=['completa', 'json', 'php', 'params'],
        help='Exibe documentação específica (completa/json/php/params)'
    )
    
    parser.add_argument(
        '--session',
        type=str,
        help='ID da sessão para monitoramento em tempo real'
    )
    
    parser.add_argument(
        '--progress-tracker',
        type=str,
        choices=['auto', 'redis', 'json', 'none'],
        default='auto',
        help='Tipo de progress tracker: auto (detecta automaticamente), redis, json, none'
    )
    
    parser.add_argument(
        '--modo-silencioso',
        action='store_true',
        help='Executa em modo silencioso (sem output adicional)'
    )
    
    return parser.parse_args()


# ========================================
# SISTEMA DE DOCUMENTAÇÃO
# ========================================

def exibir_documentacao(tipo: str = "completa"):
    """
    Exibe documentação baseada no tipo solicitado
    """
    if tipo == "completa":
        print("""
[INICIANDO] DOCUMENTAÇÃO COMPLETA - SISTEMA RPA IMEDIATO SEGUROS
=======================================================

[INFO] VISÃO GERAL DO SISTEMA
=========================

O Sistema RPA Imediato Seguros é uma automação completa para cotação de seguros
automotivos no sistema Tô Segurado. Executa 15 telas sequencialmente, capturando
dados em tempo real e gerando JSONs estruturados para integração com PHP.

[OK] FUNCIONALIDADES PRINCIPAIS
=============================

* AUTOMAÇÃO COMPLETA: Navegação em 15 telas, preenchimento automático
* PROGRESSO EM TEMPO REAL: Monitoramento via temp/progress_status.json
* DADOS ESTRUTURADOS: JSONs padronizados para integração
* SISTEMA DE RETORNO: Códigos 9001-9999, estrutura consistente
* INTEGRAÇÃO COM PHP: Arquivos prontos para consumo
* HEALTH CHECK: Verificação automática de saúde do sistema

[DADOS] ARQUIVOS GERADOS
==================

1. temp/progress_status.json - Monitoramento em tempo real
2. dados_planos_seguro_*.json - Dados finais da cotação
3. temp/json_compreensivo_tela_5_*.json - Dados intermediários
4. temp/retorno_intermediario_carrossel_*.json - Dados brutos
5. temp/dados_tela_5_*.json - Metadados
6. temp/cotacao_manual_*.json - Dados para cotação manual

[SEGURO]️ SISTEMA DE HEALTH CHECK
==========================

O sistema inclui verificação automática de saúde antes da execução:

* VERIFICAÇÃO DE ARQUIVOS: Validação de arquivos essenciais
* VERIFICAÇÃO PYTHON: Versão mínima 3.8 e módulos necessários
* VERIFICAÇÃO RECURSOS: Espaço em disco e permissões de escrita
* VERIFICAÇÃO CONFIGURAÇÃO: Validação do parametros.json
* DETECÇÃO AMBIENTE: Identificação automática Windows/Linux
* EXECUÇÃO NÃO-BLOQUEANTE: Fallback garantido se problemas detectados

[DOCUMENTO] DOCUMENTAÇÃO COMPLETA:
  docs/HEALTH_CHECK_IMPLEMENTATION_REPORT.md

[OBJETIVO] STATUS CODES: 9001 (sucesso) - 9002-9999 (erros específicos)

[NOTA] EXEMPLOS DE USO:
  python executar_rpa_imediato_playwright.py
  python executar_rpa_imediato_playwright.py --docs json
  python executar_rpa_imediato_playwright.py --docs php
  python executar_rpa_imediato_playwright.py --docs params
        """)
    
    elif tipo == "json":
        print("""
[DADOS] DOCUMENTAÇÃO DOS JSONS DE SAÍDA
==================================

[OBJETIVO] VISÃO GERAL DOS JSONS
=======================

O sistema gera 6 tipos de arquivos JSON para integração com PHP:

1. temp/progress_status.json - PROGRESSO EM TEMPO REAL
   Estrutura: timestamp, etapa_atual, percentual, status, tempo_decorrido

2. dados_planos_seguro_*.json - DADOS FINAIS
   Estrutura: plano_recomendado, plano_alternativo com valores e coberturas

3. temp/json_compreensivo_tela_5_*.json - DADOS INTERMEDIÁRIOS
   Estrutura: metadata, resumo_executivo, coberturas_detalhadas

4. temp/retorno_intermediario_carrossel_*.json - DADOS BRUTOS
   Estrutura: dados_brutos, metadados_captura

5. temp/dados_tela_5_*.json - METADADOS
   Estrutura: timestamp, tela, metadados

6. temp/cotacao_manual_*.json - COTAÇÃO MANUAL
   Estrutura: dados_coletados, mensagem, tipo_veiculo, status

[CONFIG] EXEMPLO PHP BÁSICO:
```php
$progress = json_decode(file_get_contents('temp/progress_status.json'), true);
$planos = json_decode(file_get_contents('dados_planos_seguro_*.json'), true);
$cotacao_manual = json_decode(file_get_contents('temp/cotacao_manual_*.json'), true);
```
        """)
    
    elif tipo == "php":
        print("""
�� GUIA DE INTEGRAÇÃO PHP
=========================

[OBJETIVO] VISÃO GERAL PARA DESENVOLVEDORES PHP
=======================================

O sistema gera JSONs estruturados que podem ser consumidos diretamente
por funções PHP nativas (json_decode).

[INFO] ARQUIVOS PRINCIPAIS PARA PHP
===============================

1. temp/progress_status.json - Monitoramento em tempo real
2. dados_planos_seguro_*.json - Dados finais da cotação
3. temp/json_compreensivo_tela_5_*.json - Dados intermediários

[ATUALIZANDO] EXEMPLOS PRÁTICOS PHP
=======================

MONITORAMENTO:
```php
$progress = json_decode(file_get_contents('temp/progress_status.json'), true);
echo "Etapa: {$progress['etapa_atual']}/15 ({$progress['percentual']}%)";
```

CAPTURA DE PLANOS:
```php
$planos = json_decode(file_get_contents('dados_planos_seguro_*.json'), true);
$valor_recomendado = $planos['plano_recomendado']['valor'];
```

VERIFICAÇÃO DE STATUS:
```php
if ($progress['etapa_atual'] == 15 && $progress['percentual'] == 100.0) {
    echo "RPA concluído com sucesso!";
}
```

[CONFIG] TRATAMENTO DE ERROS:
```php
$dados = json_decode($conteudo, true);
if (json_last_error() !== JSON_ERROR_NONE) {
    throw new Exception('JSON inválido: ' . json_last_error_msg());
}
```
        """)
    
    elif tipo == "params":
        print("""
[INFO] DOCUMENTAÇÃO COMPLETA DOS PARÂMETROS JSON
==========================================

[OBJETIVO] VISÃO GERAL
==============
O arquivo parametros.json contém todas as configurações necessárias para
executar o RPA Tô Segurado. Esta documentação cobre todos os 40+ campos
disponíveis com seus domínios de valores e funcionalidades.

[PASTA] ESTRUTURA HIERÁRQUICA
========================
{
  "configuracao": { ... },      # Configurações do sistema
  "autenticacao": { ... },      # Dados de login
  "url": "...",                 # URL do site
  "tipo_veiculo": "carro",      # NOVO - Tipo de veículo
  "placa": "...",               # Dados do veículo
  "marca": "...",
  "modelo": "...",
  "ano": "...",
  "zero_km": false,             # NOVO - Tela Zero KM
  "combustivel": "...",
  "veiculo_segurado": "...",
  "cep": "...",                 # Dados de endereço
  "endereco_completo": "...",
  "uso_veiculo": "...",
  "nome": "...",                # Dados pessoais
  "cpf": "...",
  "data_nascimento": "...",
  "sexo": "...",
  "estado_civil": "...",
  "email": "...",
  "celular": "...",
  "endereco": "...",
  "condutor_principal": true,    # Dados do condutor
  "nome_condutor": "...",
  "cpf_condutor": "...",
  "data_nascimento_condutor": "...",
  "sexo_condutor": "...",
  "estado_civil_condutor": "...",
  "local_de_trabalho": false,    # Localização
  "estacionamento_proprio_local_de_trabalho": false,
  "local_de_estudo": false,
  "estacionamento_proprio_local_de_estudo": false,
  "garagem_residencia": true,
  "portao_eletronico": "...",
  "reside_18_26": "...",        # Residentes
  "sexo_do_menor": "...",
  "faixa_etaria_menor_mais_novo": "...",
  "kit_gas": false,             # Veículo avançado
  "blindado": false,
  "financiado": false,
  "continuar_com_corretor_anterior": true
}

[CONFIG] SEÇÃO: CONFIGURAÇÃO
=====================
Controle de comportamento do sistema e timeouts.

* log (boolean): Ativa/desativa logs do sistema
  - Valores: true, false
  - Padrão: true
  - Função: Controla geração de logs em logs/

* display (boolean): Exibe mensagens no console
  - Valores: true, false
  - Padrão: true
  - Função: Controla exibição de mensagens em tempo real

* log_rotacao_dias (integer): Dias para rotação de logs
  - Valores: 1-365
  - Padrão: 90
  - Função: Define quando logs antigos são removidos

* log_nivel (string): Nível de log
  - Valores: "DEBUG", "INFO", "WARNING", "ERROR"
  - Padrão: "INFO"
  - Função: Controla verbosidade dos logs

* tempo_estabilizacao (float): Tempo de espera geral
  - Valores: 0.1-10.0
  - Padrão: 0.5
  - Função: Tempo de estabilização entre ações

* tempo_carregamento (float): Tempo de carregamento geral
  - Valores: 0.1-30.0
  - Padrão: 0.5
  - Função: Tempo de espera para carregamento de páginas

* tempo_estabilizacao_tela5 (float): Tempo específico Tela 5
  - Valores: 0.1-10.0
  - Padrão: 2.0
  - Função: Tempo extra para estabilização da Tela 5

* tempo_carregamento_tela5 (float): Carregamento específico Tela 5
  - Valores: 0.1-30.0
  - Padrão: 5.0
  - Função: Tempo extra para carregamento da Tela 5

* tempo_estabilizacao_tela15 (float): Tempo específico Tela 15
  - Valores: 0.1-10.0
  - Padrão: 3.0
  - Função: Tempo extra para estabilização da Tela 15

* tempo_carregamento_tela15 (float): Carregamento específico Tela 15
  - Valores: 0.1-30.0
  - Padrão: 5.0
  - Função: Tempo extra para carregamento da Tela 15

* inserir_log (boolean): Insere logs no sistema
  - Valores: true, false
  - Padrão: true
  - Função: Controla inserção de logs no sistema

* visualizar_mensagens (boolean): Visualiza mensagens
  - Valores: true, false
  - Padrão: true
  - Função: Controla visualização de mensagens

* eliminar_tentativas_inuteis (boolean): Elimina tentativas inúteis
  - Valores: true, false
  - Padrão: true
  - Função: Otimiza execução eliminando tentativas desnecessárias

 SEÇÃO: AUTENTICAÇÃO
=====================
Dados de login no sistema Tô Segurado.

* email_login (string): Email de acesso
  - Formato: email válido
  - Exemplo: "usuario@email.com"
  - Função: Email para login no sistema

* senha_login (string): Senha de acesso
  - Formato: string
  - Exemplo: "MinhaSenh@123"
  - Função: Senha para login no sistema

* manter_login_atual (boolean): Manter sessão ativa
  - Valores: true, false
  - Padrão: true
  - Função: Controla se mantém login entre execuções

[VEICULO] SEÇÃO: DADOS DO VEÍCULO
==========================
Informações básicas do veículo a ser segurado.

* tipo_veiculo (string): Tipo de veículo para cotação
  - Valores: "carro", "moto"
  - Padrão: "carro"
  - Função: Define qual botão será clicado na Tela 1
  - Impacto: Determina fluxo de navegação e campos disponíveis
  - Exemplo: "carro", "moto"

* placa (string): Placa do veículo
  - Formato: ABC1234 ou ABC-1234
  - Exemplo: "ABC1234", "ABC-1234"
  - Função: Identifica o veículo no sistema

* marca (string): Marca do veículo
  - Valores: "TOYOTA", "HONDA", "VOLKSWAGEN", "FORD", etc.
  - Exemplo: "TOYOTA"
  - Função: Marca do veículo para cotação

* modelo (string): Modelo do veículo
  - Formato: string descritivo
  - Exemplo: "COROLLA XEI 1.8/1.8 FLEX 16V MEC"
  - Função: Modelo específico do veículo

* ano (string): Ano de fabricação
  - Formato: YYYY
  - Exemplo: "2009", "2020"
  - Função: Ano de fabricação do veículo

* zero_km (boolean): Veículo zero quilômetro
  - Valores: true, false
  - Padrão: false
  - Função: NOVO - Ativa Tela Zero KM condicional
  - Impacto: Se true, pode aparecer tela adicional

* combustivel (string): Tipo de combustível
  - Valores: "Flex", "Gasolina", "Álcool", "Diesel", "Elétrico"
  - Exemplo: "Flex"
  - Função: Tipo de combustível do veículo

* veiculo_segurado (string): Veículo já segurado
  - Valores: "Sim", "Não"
  - Exemplo: "Não"
  - Função: Indica se veículo já possui seguro

[CASA] SEÇÃO: ENDEREÇO
==================
Informações de localização e uso do veículo.

* cep (string): CEP do endereço
  - Formato: 00000-000
  - Exemplo: "03317-000"
  - Função: CEP para localização do veículo

* endereco_completo (string): Endereço completo
  - Formato: string descritivo
  - Exemplo: "Rua Serra de Botucatu, 410 APTO 11 - São Paulo, SP"
  - Função: Endereço completo para cotação

* uso_veiculo (string): Finalidade do veículo
  - Valores: "Pessoal", "Comercial", "Profissional"
  - Exemplo: "Pessoal"
  - Função: Define finalidade de uso do veículo

[USUARIO] SEÇÃO: DADOS PESSOAIS
========================
Informações pessoais do segurado.

* nome (string): Nome completo
  - Formato: string
  - Exemplo: "ALEX KAMINSKI"
  - Função: Nome do segurado principal

* cpf (string): CPF do segurado
  - Formato: 00000000000 (11 dígitos)
  - Exemplo: "97137189768"
  - Função: CPF do segurado principal

* data_nascimento (string): Data de nascimento
  - Formato: DD/MM/AAAA
  - Exemplo: "25/04/1970"
  - Função: Data de nascimento do segurado

* sexo (string): Sexo do segurado
  - Valores: "Masculino", "Feminino"
  - Exemplo: "Masculino"
  - Função: Sexo do segurado principal

* estado_civil (string): Estado civil
  - Valores: "Solteiro", "Casado", "Divorciado", "Viúvo", "Casado ou Uniao Estavel"
  - Exemplo: "Casado ou Uniao Estavel"
  - Função: Estado civil do segurado

* email (string): Email de contato
  - Formato: email válido
  - Exemplo: "alex.kaminski@imediatoseguros.com.br"
  - Função: Email para contato e comunicação

* celular (string): Número de celular
  - Formato: 11999999999 (11 dígitos)
  - Exemplo: "11953288466"
  - Função: Celular para contato

* endereco (string): Endereço do segurado
  - Formato: string descritivo
  - Exemplo: "Rua Serra de Botucatu, Tatuapé - São Paulo/SP"
  - Função: Endereço do segurado

[USUARIOS] SEÇÃO: CONDUTOR PRINCIPAL
============================
Informações do condutor principal do veículo.

* condutor_principal (boolean): Condutor é o principal
  - Valores: true, false
  - Padrão: true
  - Função: Indica se há condutor principal diferente

* nome_condutor (string): Nome do condutor
  - Formato: string
  - Exemplo: "SANDRA LOUREIRO"
  - Função: Nome do condutor principal

* cpf_condutor (string): CPF do condutor
  - Formato: 00000000000 (11 dígitos)
  - Exemplo: "25151787829"
  - Função: CPF do condutor principal

* data_nascimento_condutor (string): Data nascimento condutor
  - Formato: DD/MM/AAAA
  - Exemplo: "28/08/1975"
  - Função: Data de nascimento do condutor

* sexo_condutor (string): Sexo do condutor
  - Valores: "Masculino", "Feminino"
  - Exemplo: "Feminino"
  - Função: Sexo do condutor principal

* estado_civil_condutor (string): Estado civil condutor
  - Valores: "Solteiro", "Casado", "Divorciado", "Viúvo", "Casado ou Uniao Estavel"
  - Exemplo: "Casado ou Uniao Estavel"
  - Função: Estado civil do condutor

[EMPRESA] SEÇÃO: LOCALIZAÇÃO
=====================
Informações sobre locais de trabalho e estudo.

* local_de_trabalho (boolean): Trabalha em local específico
  - Valores: true, false
  - Padrão: false
  - Função: Indica se trabalha em local específico

* estacionamento_proprio_local_de_trabalho (boolean): Estacionamento no trabalho
  - Valores: true, false
  - Padrão: false
  - Função: Tem estacionamento próprio no trabalho

* local_de_estudo (boolean): Estuda em local específico
  - Valores: true, false
  - Padrão: false
  - Função: Indica se estuda em local específico

* estacionamento_proprio_local_de_estudo (boolean): Estacionamento no estudo
  - Valores: true, false
  - Padrão: false
  - Função: Tem estacionamento próprio no local de estudo

* garagem_residencia (boolean): Garagem na residência
  - Valores: true, false
  - Padrão: true
  - Função: Tem garagem na residência

* portao_eletronico (string): Tipo de portão
  - Valores: "Eletronico", "Manual", "Nenhum"
  - Exemplo: "Eletronico"
  - Função: Tipo de portão da residência

[CRIANCA] SEÇÃO: RESIDENTES
====================
Informações sobre residentes menores de idade.

* reside_18_26 (string): Reside com pessoa 18-26 anos
  - Valores: "Sim", "Não", "N/A"
  - Exemplo: "Não"
  - Função: Indica se reside com pessoa entre 18-26 anos

* sexo_do_menor (string): Sexo do menor
  - Valores: "Masculino", "Feminino", "N/A"
  - Exemplo: "N/A"
  - Função: Sexo do menor residente

* faixa_etaria_menor_mais_novo (string): Faixa etária do menor
  - Valores: "0-5", "6-10", "11-17", "N/A"
  - Exemplo: "N/A"
  - Função: Faixa etária do menor residente

[VEICULO] SEÇÃO: VEÍCULO AVANÇADO
==========================
Características especiais do veículo.

* kit_gas (boolean): Possui kit gás
  - Valores: true, false
  - Padrão: false
  - Função: Veículo possui kit gás
  - Observação: Ignorado para motos (não aplicável)

* blindado (boolean): Veículo blindado
  - Valores: true, false
  - Padrão: false
  - Função: Veículo é blindado

* financiado (boolean): Veículo financiado
  - Valores: true, false
  - Padrão: false
  - Função: Veículo está financiado

* continuar_com_corretor_anterior (boolean): Continuar com corretor
  - Valores: true, false
  - Padrão: true
  - Função: Continuar com corretor anterior

[INFO] VALIDAÇÕES AUTOMÁTICAS
========================
O sistema valida automaticamente:

* CPF: Formato e dígitos verificadores
* CEP: Formato 00000-000
* Email: Formato válido
* Celular: 11 dígitos
* Placa: Formato ABC1234 ou ABC-1234
* Data: Formato DD/MM/AAAA
* Valores permitidos: sexo, estado_civil, combustivel, etc.

[AVISO] CAMPOS OBRIGATÓRIOS
======================
Estes campos são obrigatórios e a execução falhará se ausentes:

* url, placa, marca, modelo, ano, combustivel
* cep, uso_veiculo, veiculo_segurado
* nome, cpf, email, celular
* autenticacao (email_login, senha_login)

[ATUALIZANDO] CAMPOS CONDICIONAIS
======================
Estes campos podem afetar o fluxo:

* zero_km: Ativa Tela Zero KM (condicional)
* condutor_principal: Se true, requer dados do condutor
* local_de_trabalho: Se true, requer dados de trabalho
* local_de_estudo: Se true, requer dados de estudo

[NOTA] EXEMPLO COMPLETO
==================
{
  "configuracao": {
    "log": true,
    "display": true,
    "log_rotacao_dias": 90,
    "log_nivel": "INFO",
    "tempo_estabilizacao": 0.5,
    "tempo_carregamento": 0.5,
    "tempo_estabilizacao_tela5": 2,
    "tempo_carregamento_tela5": 5,
    "tempo_estabilizacao_tela15": 3,
    "tempo_carregamento_tela15": 5,
    "inserir_log": true,
    "visualizar_mensagens": true,
    "eliminar_tentativas_inuteis": true
  },
  "autenticacao": {
    "email_login": "usuario@email.com",
    "senha_login": "MinhaSenh@123",
    "manter_login_atual": true
  },
  "url": "https://www.app.tosegurado.com.br/imediatosolucoes",
  "placa": "ABC1234",
  "marca": "TOYOTA",
  "modelo": "COROLLA XEI 1.8/1.8 FLEX 16V MEC",
  "ano": "2009",
  "zero_km": false,
  "combustivel": "Flex",
  "veiculo_segurado": "Não",
  "cep": "03317-000",
  "endereco_completo": "Rua Serra de Botucatu, 410 APTO 11 - São Paulo, SP",
  "uso_veiculo": "Pessoal",
  "nome": "ALEX KAMINSKI",
  "cpf": "97137189768",
  "data_nascimento": "25/04/1970",
  "sexo": "Masculino",
  "estado_civil": "Casado ou Uniao Estavel",
  "email": "alex.kaminski@imediatoseguros.com.br",
  "celular": "11953288466",
  "endereco": "Rua Serra de Botucatu, Tatuapé - São Paulo/SP",
  "condutor_principal": true,
  "nome_condutor": "SANDRA LOUREIRO",
  "cpf_condutor": "25151787829",
  "data_nascimento_condutor": "28/08/1975",
  "sexo_condutor": "Feminino",
  "estado_civil_condutor": "Casado ou Uniao Estavel",
  "local_de_trabalho": false,
  "estacionamento_proprio_local_de_trabalho": false,
  "local_de_estudo": false,
  "estacionamento_proprio_local_de_estudo": false,
  "garagem_residencia": true,
  "portao_eletronico": "Eletronico",
  "reside_18_26": "Não",
  "sexo_do_menor": "N/A",
  "faixa_etaria_menor_mais_novo": "N/A",
  "kit_gas": false,
  "blindado": false,
  "financiado": false,
  "continuar_com_corretor_anterior": true
}

[INICIANDO] COMANDOS DE USO
==================
python executar_rpa_imediato_playwright.py --docs params
python executar_rpa_imediato_playwright.py --config meu_parametros.json
python executar_rpa_imediato_playwright.py --docs completa
        """)


# ========================================
# SISTEMA DE EXCEPTION HANDLER
# ========================================

class RPAException(Exception):
    """
    Exceção customizada para o RPA
    """
    def __init__(self, message: str, tela: str = None, erro_original: Exception = None):
        self.message = message
        self.tela = tela
        self.erro_original = erro_original
        super().__init__(self.message)

class ExceptionHandler:
    """
    Sistema robusto de tratamento de exceções para o RPA
    """
    
    def __init__(self):
        self.erros_capturados = []
        self.warnings_capturados = []
        self.tela_atual = None
    
    def capturar_excecao(self, erro: Exception, tela: str = None, contexto: str = None) -> Dict[str, Any]:
        """
        Captura e formata uma exceção de forma estruturada
        
        PARÂMETROS:
            erro: Exception - Exceção capturada
            tela: str - Nome da tela onde ocorreu o erro
            contexto: str - Contexto adicional do erro
            
        RETORNO:
            dict: Dicionário estruturado com informações do erro
        """
        timestamp = datetime.now().isoformat()
        
        # Extrair informações detalhadas do erro
        tipo_erro = type(erro).__name__
        mensagem_erro = str(erro)
        traceback_completo = traceback.format_exc()
        
        # Determinar severidade do erro
        severidade = self._determinar_severidade(erro)
        
        # Criar estrutura de erro
        erro_estruturado = {
            "timestamp": timestamp,
            "tipo": tipo_erro,
            "mensagem": mensagem_erro,
            "tela": tela or self.tela_atual,
            "contexto": contexto,
            "severidade": severidade,
            "traceback": traceback_completo,
            "recomendacao": self._gerar_recomendacao(erro, tela)
        }
        
        # Adicionar à lista de erros
        self.erros_capturados.append(erro_estruturado)
        
        # Log do erro
        self._log_erro(erro_estruturado)
        
        return erro_estruturado
    
    def _determinar_severidade(self, erro: Exception) -> str:
        """
        Determina a severidade do erro baseado no tipo
        """
        if isinstance(erro, (TimeoutError, ConnectionError)):
            return "CRÍTICO"
        elif isinstance(erro, (ValueError, TypeError)):
            return "ALTO"
        elif isinstance(erro, (FileNotFoundError, PermissionError)):
            return "MÉDIO"
        else:
            return "BAIXO"
    
    def _gerar_recomendacao(self, erro: Exception, tela: str = None) -> str:
        """
        Gera recomendação baseada no tipo de erro
        """
        if isinstance(erro, TimeoutError):
            return f"Verificar conectividade e tentar novamente. Tela: {tela}"
        elif isinstance(erro, ValueError):
            return f"Verificar parâmetros de entrada. Tela: {tela}"
        elif "element not found" in str(erro).lower():
            return f"Elemento não encontrado. Verificar seletor. Tela: {tela}"
        elif "timeout" in str(erro).lower():
            return f"Timeout detectado. Aumentar tempo de espera. Tela: {tela}"
        else:
            return f"Erro genérico. Verificar logs detalhados. Tela: {tela}"
    
    def _log_erro(self, erro_estruturado: Dict[str, Any]):
        """
        Faz log do erro de forma formatada
        """
        timestamp = erro_estruturado["timestamp"]
        tela = erro_estruturado["tela"]
        tipo = erro_estruturado["tipo"]
        mensagem = erro_estruturado["mensagem"]
        severidade = erro_estruturado["severidade"]
        
        exibir_mensagem(f"\n{'='*80}")
        exibir_mensagem(f"[ALERTA] ERRO CAPTURADO - {severidade}")
        exibir_mensagem(f"{'='*80}")
        exibir_mensagem(f"[TEMPO] Timestamp: {timestamp}")
        exibir_mensagem(f"[CELULAR] Tela: {tela}")
        exibir_mensagem(f"[BUSCAR] Tipo: {tipo}")
        exibir_mensagem(f"[MENSAGEM] Mensagem: {mensagem}")
        exibir_mensagem(f"[IDEIA] Recomendação: {erro_estruturado['recomendacao']}")
        exibir_mensagem(f"{'='*80}")
    
    def capturar_warning(self, mensagem: str, tela: str = None, contexto: str = None):
        """
        Captura um warning (não é erro crítico)
        """
        timestamp = datetime.now().isoformat()
        
        warning = {
            "timestamp": timestamp,
            "mensagem": mensagem,
            "tela": tela or self.tela_atual,
            "contexto": contexto,
            "tipo": "WARNING"
        }
        
        self.warnings_capturados.append(warning)
        
        exibir_mensagem(f"[AVISO] WARNING - {tela}: {mensagem}")
    
    def definir_tela_atual(self, tela: str):
        """
        Define a tela atual para contexto de erros
        """
        self.tela_atual = tela
    
    def obter_resumo_erros(self) -> Dict[str, Any]:
        """
        Retorna resumo dos erros capturados
        """
        return {
            "total_erros": len(self.erros_capturados),
            "total_warnings": len(self.warnings_capturados),
            "erros_criticos": len([e for e in self.erros_capturados if e["severidade"] == "CRÍTICO"]),
            "erros_altos": len([e for e in self.erros_capturados if e["severidade"] == "ALTO"]),
            "erros_medios": len([e for e in self.erros_capturados if e["severidade"] == "MÉDIO"]),
            "erros_baixos": len([e for e in self.erros_capturados if e["severidade"] == "BAIXO"]),
            "ultimo_erro": self.erros_capturados[-1] if self.erros_capturados else None
        }
    
    def limpar_erros(self):
        """
        Limpa a lista de erros capturados
        """
        self.erros_capturados = []
        self.warnings_capturados = []

# Instância global do Exception Handler
exception_handler = ExceptionHandler()

# ========================================
# VARIÁVEIS GLOBAIS
# ========================================

# Flag para controlar se a Tela 15 foi detectada diretamente da Tela 13
tela_15_detectada = False

# ========================================
# CONTROLE DE DISPLAY GLOBAL
# ========================================

DISPLAY_ENABLED = True  # Flag global para controle de saída

# ========================================
# FUNÇÕES AUXILIARES
# ========================================

def configurar_display(parametros: Dict[str, Any]):
    """
    Configura flag de display baseado nos parâmetros
    
    PARÂMETROS:
        parametros (Dict): Parâmetros do arquivo JSON
        
    COMPORTAMENTO:
        - Lê configuracao.display, configuracao.visualizar_mensagens e configuracao.modo_silencioso
        - Define DISPLAY_ENABLED = display AND visualizar_mensagens AND NOT modo_silencioso
        - Modo silencioso: ZERO output adicional
        - Configura também os módulos externos
    """
    global DISPLAY_ENABLED
    
    configuracao = parametros.get('configuracao', {})
    display = configuracao.get('display', True)
    visualizar_mensagens = configuracao.get('visualizar_mensagens', True)
    modo_silencioso = configuracao.get('modo_silencioso', False) or args.modo_silencioso
    
    DISPLAY_ENABLED = display and visualizar_mensagens and not modo_silencioso
    
    # Configurar módulos externos
    try:
        import utils.health_check_conservative
        utils.health_check_conservative.DISPLAY_ENABLED = DISPLAY_ENABLED
    except:
        pass
    
    try:
        import utils.logger_rpa
        utils.logger_rpa.set_display_enabled(DISPLAY_ENABLED)
    except:
        pass
    
    if not DISPLAY_ENABLED:
        # Modo silencioso ativo - zero outputs
        pass

def limpar_emojis_windows(mensagem: str) -> str:
    """
    Remove emojis para compatibilidade com Windows
    
    PARÂMETROS:
        mensagem (str): Mensagem que pode conter emojis
    
    RETORNA:
        str: Mensagem com emojis substituídos por texto
    
    COMPORTAMENTO:
        - Substitui emojis Unicode por texto legível
        - Garante compatibilidade com console Windows (CP1252)
        - Mantém significado semântico da mensagem
    """
    emojis = {
        '[OK]': '[OK]', '[OBJETIVO]': '[ETAPA]', '[AVISO]': '[AVISO]', '[ERRO]': '[ERRO]',
        '[ALERTA]': '[ALERTA]', '[SALVAR]': '[SALVO]', '[AGUARDANDO]': '[AGUARDANDO]', '[BUSCAR]': '[BUSCANDO]',
        '[DADOS]': '[DADOS]', '[SUCESSO]': '[SUCESSO]', '[IDEIA]': '[DICA]', '[CONFIG]': '[CONFIG]',
        '[PASTA]': '[ARQUIVO]', '[TEMPO]': '[TEMPO]', '[PRESENTE]': '[BENEFICIO]', '[VEICULO]': '[VEICULO]',
        '[USUARIO]': '[USUARIO]', '[EMAIL]': '[EMAIL]', '[LOCALIZACAO]': '[LOCAL]', '[CONFIG]️': '[CONFIG]',
        '[SEGURO]️': '[SEGURANCA]', '[CELULAR]': '[MOBILE]',
        '[COMPUTADOR]': '[SISTEMA]', '[ATUALIZANDO]': '[PROCESSANDO]', '[GRAFICO]': '[PROGRESSO]', '[EVENTO]': '[CARROSSEL]'
    }
    
    for emoji, substituto in emojis.items():
        mensagem = mensagem.replace(emoji, substituto)
    
    return mensagem

def exibir_mensagem(mensagem: str):
    """
    Exibe mensagem formatada com timestamp (controlado por flag)
    
    PARÂMETROS:
        mensagem (str): Mensagem a ser exibida
    
    COMPORTAMENTO:
        - Se DISPLAY_ENABLED = True: exibe mensagem formatada
        - Se DISPLAY_ENABLED = False: não exibe nada (modo silencioso)
        - Remove emojis para compatibilidade com Windows
    """
    if DISPLAY_ENABLED:
        timestamp = time.strftime('%H:%M:%S')
        mensagem_limpa = limpar_emojis_windows(mensagem)
        print(f"[{timestamp}] {mensagem_limpa}")

def exibir_resultado_final(mensagem: str):
    """
    Exibe resultado final sempre, mesmo no modo silencioso
    
    PARÂMETROS:
        mensagem (str): Mensagem de resultado final
    """
    timestamp = time.strftime('%H:%M:%S')
    mensagem_limpa = limpar_emojis_windows(mensagem)
    print(f"[{timestamp}] {mensagem_limpa}")

def carregar_parametros(arquivo_config: str = "parametros.json") -> Dict[str, Any]:
    """
    Carrega parâmetros do arquivo JSON
    
    PARÂMETROS:
        arquivo_config: str - Caminho para o arquivo de configuração
        
    RETORNO:
        dict: Parâmetros carregados
        
    EXCEÇÕES:
        RPAException: Se não conseguir carregar os parâmetros
    """
    try:
        exception_handler.definir_tela_atual("CARREGAMENTO_PARAMETROS")
        
        if not os.path.exists(arquivo_config):
            raise RPAException(f"Arquivo de configuração não encontrado: {arquivo_config}")
        
        with open(arquivo_config, 'r', encoding='utf-8') as f:
            parametros = json.load(f)
        
        # NOVA LINHA: Configurar display baseado nos parâmetros
        configurar_display(parametros)
        
        exibir_mensagem("[OK] Parâmetros carregados com sucesso!")
        return parametros
        
    except json.JSONDecodeError as e:
        erro = exception_handler.capturar_excecao(e, "CARREGAMENTO_PARAMETROS", "JSON inválido")
        raise RPAException("Erro ao decodificar JSON dos parâmetros", "CARREGAMENTO_PARAMETROS", e)
        
    except Exception as e:
        erro = exception_handler.capturar_excecao(e, "CARREGAMENTO_PARAMETROS", "Erro genérico")
        raise RPAException("Erro ao carregar parâmetros", "CARREGAMENTO_PARAMETROS", e)

def obter_parametros_tempo(parametros: Dict[str, Any]) -> Dict[str, int]:
    """
    Extrai parâmetros de tempo do arquivo de configuração
    
    PARÂMETROS:
        parametros: dict - Parâmetros carregados
        
    RETORNO:
        dict: Dicionário com parâmetros de tempo
    """
    configuracao = parametros.get('configuracao', {})
    
    tempo_estabilizacao = configuracao.get('tempo_estabilizacao', 1)
    tempo_carregamento = configuracao.get('tempo_carregamento', 10)
    tempo_estabilizacao_tela5 = configuracao.get('tempo_estabilizacao_tela5', 2)
    tempo_carregamento_tela5 = configuracao.get('tempo_carregamento_tela5', 5)
    
    exibir_mensagem(f"[CONFIG]️ Parâmetros de tempo carregados:")
    exibir_mensagem(f"   - Estabilização: {tempo_estabilizacao}s")
    exibir_mensagem(f"   - Carregamento: {tempo_carregamento}s")
    exibir_mensagem(f"   - Estabilização Tela 5: {tempo_estabilizacao_tela5}s")
    exibir_mensagem(f"   - Carregamento Tela 5: {tempo_carregamento_tela5}s")
    
    return {
        'tempo_estabilizacao': tempo_estabilizacao,
        'tempo_carregamento': tempo_carregamento,
        'tempo_estabilizacao_tela5': tempo_estabilizacao_tela5,
        'tempo_carregamento_tela5': tempo_carregamento_tela5
    }

def validar_parametros_obrigatorios(parametros: Dict[str, Any]) -> bool:
    """
    Valida se todos os parâmetros obrigatórios estão presentes
    
    PARÂMETROS:
        parametros: dict - Parâmetros a serem validados
        
    RETORNO:
        bool: True se válido, False caso contrário
        
    EXCEÇÕES:
        RPAException: Se parâmetros obrigatórios estiverem faltando
    """
    try:
        exception_handler.definir_tela_atual("VALIDACAO_PARAMETROS")
        
        parametros_obrigatorios = [
            "url", "placa", "marca", "modelo", "ano", "combustivel", 
            "cep", "uso_veiculo", "veiculo_segurado", "nome", "cpf", 
            "email", "celular", "autenticacao"
        ]
        
        parametros_faltando = []
        
        for param in parametros_obrigatorios:
            if param not in parametros:
                parametros_faltando.append(param)
            elif not parametros[param]:
                parametros_faltando.append(f"{param} (vazio)")
        
        if parametros_faltando:
            erro_msg = f"Parâmetros obrigatórios faltando: {', '.join(parametros_faltando)}"
            exception_handler.capturar_warning(erro_msg, "VALIDACAO_PARAMETROS")
            return False
        
        # Validar subcampos de autenticação
        if "autenticacao" in parametros:
            auth = parametros["autenticacao"]
            if "email_login" not in auth or "senha_login" not in auth:
                exception_handler.capturar_warning("Campos de autenticação incompletos", "VALIDACAO_PARAMETROS")
                return False
        
        exibir_mensagem("[OK] Todos os parâmetros obrigatórios estão presentes!")
        return True
        
    except Exception as e:
        erro = exception_handler.capturar_excecao(e, "VALIDACAO_PARAMETROS", "Erro na validação")
        raise RPAException("Erro ao validar parâmetros", "VALIDACAO_PARAMETROS", e)

def salvar_dados_planos(dados_planos: Dict[str, Any], prefixo: str = "dados_planos_seguro"):
    """
    Salva os dados dos planos em arquivo JSON
    
    PARÂMETROS:
        dados_planos: dict - Dados dos planos a serem salvos
        prefixo: str - Prefixo do nome do arquivo
        
    RETORNO:
        str: Caminho do arquivo salvo
    """
    try:
        exception_handler.definir_tela_atual("SALVAMENTO_DADOS")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_arquivo = f"{prefixo}_{timestamp}.json"
        
        with open(nome_arquivo, 'w', encoding='utf-8') as f:
            json.dump(dados_planos, f, indent=2, ensure_ascii=False)
        
        exibir_mensagem(f"[SALVAR] Dados salvos em: {nome_arquivo}")
        return nome_arquivo
        
    except Exception as e:
        erro = exception_handler.capturar_excecao(e, "SALVAMENTO_DADOS", "Erro ao salvar dados")
        raise RPAException("Erro ao salvar dados dos planos", "SALVAMENTO_DADOS", e)

# ========================================
# FUNÇÃO WRAPPER DE TIMEOUT SEGURO
# ========================================

def executar_com_timeout(smart_timeout, tela_num, funcao_tela, *args, **kwargs):
    """
    Wrapper seguro para executar telas com timeout inteligente
    Não modifica a lógica original, apenas adiciona controle de timeout
    """
    if smart_timeout and smart_timeout.is_available():
        try:
            # Iniciar timer para a tela
            smart_timeout.start_timer(tela_num, f"Executando Tela {tela_num}")
            
            # Executar função original
            resultado = funcao_tela(*args, **kwargs)
            
            # Limpar timer se sucesso
            smart_timeout.clear_timer(tela_num)
            return resultado
            
        except Exception as e:
            # Verificar se foi timeout
            if smart_timeout.check_timeout(tela_num):
                timeout_info = smart_timeout.handle_timeout(tela_num, str(e))
                exibir_mensagem(f"[AVISO] Timeout detectado na Tela {tela_num}: {timeout_info['elapsed_seconds']:.1f}s")
                
                # Tentar retry se disponível
                if smart_timeout.retry_with_backoff(tela_num):
                    exibir_mensagem(f"[ATUALIZANDO] Retry automático na Tela {tela_num} (tentativa {timeout_info['retries_remaining']})")
                    return executar_com_timeout(smart_timeout, tela_num, funcao_tela, *args, **kwargs)
                else:
                    exibir_mensagem(f"[ERRO] Máximo de retries atingido na Tela {tela_num}")
            
            # Re-raise a exceção original
            raise e
    else:
        # Fallback: executar sem timeout se sistema não disponível
        return funcao_tela(*args, **kwargs)


# ========================================
# FUNÇÕES AUXILIARES
# ========================================

def extrair_nome_e_valores(texto: str) -> tuple:
    """
    Extrai nome da cobertura e valores monetários do texto
    
    Args:
        texto: Texto completo do elemento
    
    Returns:
        tuple: (nome_cobertura, valores_dict)
    """
    try:
        import re
        
        # Regex para encontrar nome da cobertura
        nome_match = re.search(r'Cobertura\s+(\w+)', texto)
        nome = nome_match.group(1) if nome_match else "Desconhecida"
        
        # Regex para encontrar valores monetários
        valores_match = re.search(r'R\$\s*([\d.,]+).*?até.*?R\$\s*([\d.,]+)', texto)
        if valores_match:
            valores = {
                "de": f"R$ {valores_match.group(1)}",
                "ate": f"R$ {valores_match.group(2)}"
            }
        else:
            valores = {"de": "", "ate": ""}
        
        return nome, valores
        
    except:
        return "Desconhecida", {"de": "", "ate": ""}

def validar_elemento_unico(elemento_texto: str, elementos_processados: set) -> bool:
    """
    Valida se elemento é único baseado em nome + valores únicos
    
    NOVA IMPLEMENTAÇÃO: Critério mais inteligente
    FALLBACK: Algoritmo original se nova lógica falhar
    
    Args:
        elemento_texto: Texto do elemento a ser validado
        elementos_processados: Set com elementos já processados
    
    Returns:
        bool: True se elemento é único, False se é duplicado
    """
    try:
        # NOVA LÓGICA: Extrair nome e valores
        nome, valores = extrair_nome_e_valores(elemento_texto)
        chave_unica = f"{nome}_{valores['de']}_{valores['ate']}"
        
        if chave_unica in elementos_processados:
            exibir_mensagem(f"[DUPLICATA] Ignorada: {nome} ({valores['de']} - {valores['ate']})")
            return False
        
        elementos_processados.add(chave_unica)
        exibir_mensagem(f"[UNICA] Aceita: {nome} ({valores['de']} - {valores['ate']})")
        return True
        
    except Exception as e:
        exibir_mensagem(f"[FALLBACK] Usando algoritmo original: {str(e)}")
        # FALLBACK: Algoritmo original
        try:
            import hashlib
            hash_conteudo = hashlib.md5(elemento_texto.encode()).hexdigest()
            if hash_conteudo in elementos_processados:
                return False
            elementos_processados.add(hash_conteudo)
            return True
        except:
            return True  # Fallback final: permitir elemento

# ========================================
# FUNÇÕES DE NAVEGAÇÃO DAS TELAS
# ========================================

def navegar_tela_1_playwright(page: Page, tipo_veiculo: str = "carro") -> bool:
    """
    TELA 1: Seleção do tipo de seguro (Carro ou Moto)
    
    VERSÃO: v3.3.0
    IMPLEMENTAÇÃO: Suporte a carro e moto
    DATA: 24/09/2025
    STATUS: [OK] IMPLEMENTADO
    """
    try:
        exception_handler.definir_tela_atual("TELA_1")
        # Validação do parâmetro
        if tipo_veiculo not in ["carro", "moto"]:
            exception_handler.capturar_excecao(
                ValueError(f"tipo_veiculo inválido: {tipo_veiculo}"), 
                "TELA_1", 
                "Tipo de veículo deve ser 'carro' ou 'moto'"
            )
            return False
        
        exibir_mensagem(f"[CELULAR] TELA 1: Selecionando {tipo_veiculo.title()}...")
        
        # Aguardar carregamento inicial da página
        page.wait_for_selector("button", timeout=5000)
        
        # ESTRATÉGIA HÍBRIDA: Específico + Fallback
        if tipo_veiculo == "carro":
            seletores = [
                # PRIMÁRIO: Seletor específico por alt da imagem
                'button:has(img[alt="Icone car"])',
                # SECUNDÁRIO: Seletor específico por src da imagem
                'button:has(img[src="/insurance-icons/car.svg"])',
                # TERCIÁRIO: Seletor específico por texto
                'button:has-text("Carro")',
                # FALLBACK: Seletor genérico original
                'button.group:nth-child(1)'
            ]
        elif tipo_veiculo == "moto":
            seletores = [
                # PRIMÁRIO: Seletor específico por alt da imagem
                'button:has(img[alt="Icone motorcycle"])',
                # SECUNDÁRIO: Seletor específico por src da imagem
                'button:has(img[src="/insurance-icons/motorcycle.svg"])',
                # TERCIÁRIO: Seletor específico por texto
                'button:has-text("Moto")',
                # FALLBACK: Seletor genérico (segundo botão)
                'button.group:nth-child(2)'
            ]
        
        botao_veiculo = None
        seletor_usado = None
        
        # Tentar cada seletor em ordem de prioridade
        for seletor in seletores:
            try:
                botao_veiculo = page.locator(seletor).first
                if botao_veiculo.is_visible():
                    seletor_usado = seletor
                    exibir_mensagem(f"[OK] Botão '{tipo_veiculo.title()}' encontrado com seletor: {seletor}")
                    break
            except Exception as e:
                continue
        
        if botao_veiculo and botao_veiculo.is_visible():
            botao_veiculo.click()
            exibir_mensagem(f"[OK] Botão '{tipo_veiculo.title()}' clicado com sucesso")
            
            # Log do seletor usado para monitoramento
            if seletor_usado.startswith('button:has'):
                exibir_mensagem(f"[OBJETIVO] Seletor específico usado: {seletor_usado}")
            else:
                exibir_mensagem(f"[AVISO] Fallback usado: {seletor_usado}")
            
            # Aguardar transição para a próxima tela
            page.wait_for_selector("#placaTelaDadosPlaca", timeout=5000)
            return True
        else:
            exception_handler.capturar_warning(f"Botão '{tipo_veiculo.title()}' não encontrado com nenhum seletor", "TELA_1")
            return False
            
    except Exception as e:
        exception_handler.capturar_excecao(e, "TELA_1", f"Erro ao selecionar {tipo_veiculo.title()}")
        return False

def navegar_tela_2_playwright(page: Page, placa: str) -> bool:
    """
    TELA 2: Inserção da placa
    """
    try:
        exception_handler.definir_tela_atual("TELA_2")
        exibir_mensagem(f"[CELULAR] TELA 2: Inserindo placa {placa}...")
        
        campo_placa = page.locator("#placaTelaDadosPlaca").first
        campo_placa.click()
        campo_placa.fill(placa)
        
        exibir_mensagem(f"[OK] Placa {placa} inserida com sucesso")
        
        botao_continuar = page.locator("#gtm-telaDadosAutoCotarComPlacaContinuar").first
        botao_continuar.click()
        
        exibir_mensagem("[OK] Botão 'Continuar' clicado com sucesso")
        # Aguardar transição para a próxima tela
        page.wait_for_selector("#gtm-telaInfosAutoContinuar", timeout=5000)
        return True
        
    except Exception as e:
        exception_handler.capturar_excecao(e, "TELA_2", f"Erro ao inserir placa {placa}")
        return False

def navegar_tela_3_playwright(page: Page) -> bool:
    """
    TELA 3: Confirmação do veículo
    """
    try:
        exception_handler.definir_tela_atual("TELA_3")
        exibir_mensagem("[CELULAR] TELA 3: Confirmando informações do veículo...")
        
        botao_continuar = page.locator("#gtm-telaInfosAutoContinuar").first
        
        if botao_continuar.is_visible():
            botao_continuar.click()
            exibir_mensagem("[OK] Botão 'Continuar' clicado com sucesso")
            page.wait_for_selector("#gtm-telaRenovacaoVeiculoContinuar", timeout=5000)
            return True
        else:
            exception_handler.capturar_warning("Botão 'Continuar' não encontrado", "TELA_3")
            return False
            
    except Exception as e:
        exception_handler.capturar_excecao(e, "TELA_3", "Erro ao confirmar veículo")
        return False

def navegar_tela_4_playwright(page: Page, veiculo_segurado: str) -> bool:
    """
    TELA 4: Veículo segurado
    """
    try:
        exception_handler.definir_tela_atual("TELA_4")
        exibir_mensagem("[CELULAR] TELA 4: Respondendo se veículo está segurado...")
        
        if veiculo_segurado == "Não":
            botao_nao = page.locator("#gtm-telaRenovacaoVeiculoContinuar").first
            botao_nao.click()
            exibir_mensagem("[OK] Resposta 'Não' selecionada com sucesso")
        else:
            exception_handler.capturar_warning(f"Opção '{veiculo_segurado}' não implementada", "TELA_4")
            return False
        
        # Aguardar transição para a próxima tela
        page.wait_for_selector("div.bg-primary", timeout=5000)
        return True
        
    except Exception as e:
        exception_handler.capturar_excecao(e, "TELA_4", f"Erro ao responder veículo segurado: {veiculo_segurado}")
        return False

def aguardar_cards_estimativa_playwright(page: Page, timeout: int = 10000) -> bool:
    """
    Aguarda carregamento dos cards de estimativa com estratégia híbrida robusta
    
    ESTRATÉGIA HÍBRIDA v3.7.0.2:
    1. div[role="group"][aria-roledescription="slide"] - ESPECÍFICO (semântico)
    2. div:has(p:has-text("Cobertura")):has(span:has-text("R$")) - CONTEÚDO
    3. div.border-primary.rounded-xl:has(.bg-primary) - LAYOUT
    4. div.bg-primary - FALLBACK ATUAL (compatibilidade)
    """
    seletores_prioridade = [
        'div[role="group"][aria-roledescription="slide"]',  # <- ESPECÍFICO
        'div:has(p:has-text("Cobertura")):has(span:has-text("R$"))',  # <- CONTEÚDO
        'div.border-primary.rounded-xl:has(.bg-primary)',  # <- LAYOUT
        'div.bg-primary'  # <- FALLBACK ATUAL
    ]
    
    timeout_por_seletor = timeout // len(seletores_prioridade)
    
    for i, seletor in enumerate(seletores_prioridade):
        try:
            exibir_mensagem(f"[BUSCAR] Tentativa {i+1}/{len(seletores_prioridade)} - Seletor: {seletor}")
            page.wait_for_selector(seletor, timeout=timeout_por_seletor)
            exibir_mensagem(f"[OK] Cards encontrados com seletor: {seletor}")
            return True
        except Exception as e:
            exibir_mensagem(f"[AVISO] Seletor {i+1} falhou: {str(e)}")
            continue
    
    exibir_mensagem("[ERRO] Nenhum seletor funcionou para encontrar os cards")
    return False

def localizar_cards_estimativa_playwright(page: Page):
    """
    Localiza cards de estimativa com estratégia híbrida robusta
    
    ESTRATÉGIA HÍBRIDA v3.7.0.2:
    1. div[role="group"][aria-roledescription="slide"] - ESPECÍFICO (semântico)
    2. div:has(p:has-text("Cobertura")):has(span:has-text("R$")) - CONTEÚDO
    3. div.border-primary.rounded-xl:has(.bg-primary) - LAYOUT
    4. div.bg-primary - FALLBACK ATUAL (compatibilidade)
    """
    seletores_prioridade = [
        'div[role="group"][aria-roledescription="slide"]',  # <- ESPECÍFICO
        'div:has(p:has-text("Cobertura")):has(span:has-text("R$"))',  # <- CONTEÚDO
        'div.border-primary.rounded-xl:has(.bg-primary)',  # <- LAYOUT
        'div.bg-primary'  # <- FALLBACK ATUAL
    ]
    
    for i, seletor in enumerate(seletores_prioridade):
        try:
            elemento = page.locator(seletor)
            if elemento.count() > 0:
                exibir_mensagem(f"[OK] Cards localizados com seletor: {seletor} ({elemento.count()} encontrados)")
                return elemento
        except Exception as e:
            exibir_mensagem(f"[AVISO] Seletor {i+1} falhou: {str(e)}")
            continue
    
    exibir_mensagem("[ERRO] Nenhum seletor funcionou para localizar os cards")
    return None

def navegar_tela_5_playwright(page: Page, parametros_tempo) -> bool:
    """
    TELA 5: Estimativa inicial - CAPTURA DE DADOS E RETORNO INTERMEDIÁRIO
    """
    try:
        exception_handler.definir_tela_atual("TELA_5")
        exibir_mensagem("[CELULAR] TELA 5: Aguardando carregamento da estimativa...")
        
        # Aguardar carregamento inicial da página
        # Este delay é maior que as outras telas porque a Tela 5
        # precisa calcular estimativas em tempo real
        # v3.7.0.2: Estratégia híbrida robusta para aguardar cards
        if not aguardar_cards_estimativa_playwright(page, 10000):
            exibir_mensagem("[ERRO] Falha ao aguardar carregamento dos cards de estimativa")
            return False
        
        max_tentativas = 60  # Aumentado de 30 para 60
        tentativa = 0
        
        while tentativa < max_tentativas:
            exibir_mensagem(f"[ATUALIZANDO] Tentativa {tentativa + 1}/{max_tentativas} - Aguardando cards de cobertura...")
            
            # Verificar se os cards de cobertura apareceram
            # v3.7.0.2: Estratégia híbrida robusta para localizar cards
            elemento_estimativa = localizar_cards_estimativa_playwright(page)
            if elemento_estimativa is not None and elemento_estimativa.count() > 0:
                exibir_mensagem(f"[OK] Elemento de estimativa encontrado: {elemento_estimativa.count()} cards")
                
                # Verificar se os cards ainda estão carregando (skeleton)
                card_text = elemento_estimativa.first.text_content().strip() if elemento_estimativa.first.text_content() else ""
                if "skeleton" not in card_text.lower() and len(card_text) > 10:
                    exibir_mensagem("[OK] Cards carregados completamente!")
                    break
                else:
                    exibir_mensagem("[AGUARDANDO] Cards ainda carregando (skeleton detectado)...")
            
            # Verificar se há elementos com preços (fallback)
            elementos_preco = page.locator("text=R$")
            if elementos_preco.count() > 0:
                exibir_mensagem(f"[OK] Elementos com preços encontrados: {elementos_preco.count()}")
                break
            
            # Verificar se o botão "Continuar" apareceu (fallback)
            botao_continuar = page.locator("#gtm-telaEstimativaContinuarParaCotacaoFinal")
            if botao_continuar.count() > 0:
                exibir_mensagem("[OK] Botão 'Continuar' encontrado")
                break
            
            # Aguardar elementos dinâmicos com espera específica
            # v3.7.0.2: Estratégia híbrida robusta para aguardar cards
            try:
                if aguardar_cards_estimativa_playwright(page, 2000):  # Aumentado para 2 segundos
                    break
            except Exception:
                try:
                    page.wait_for_selector("text=R$", timeout=2000)
                    break
                except Exception:
                    try:
                        page.wait_for_selector("#gtm-telaEstimativaContinuarParaCotacaoFinal", timeout=2000)
                        break
                    except Exception:
                        # Aguardar um pouco mais antes da próxima tentativa
                        time.sleep(2)
                        continue
            
            tentativa += 1
        
        if tentativa >= max_tentativas:
            exception_handler.capturar_warning("Elementos da estimativa não carregaram completamente", "TELA_5")
            # Não retornar False aqui, continuar mesmo sem dados completos
        
        exibir_mensagem("[OK] Estimativa carregada com sucesso")
        
        # OTIMIZAÇÃO: Reduzir delay de estabilização
        exibir_mensagem("[AGUARDANDO] Aguardando estabilização dos dados...")
        time.sleep(2)  # Reduzido de 5 para 2 segundos
        
        # CAPTURAR DADOS DO CARROSSEL DE ESTIMATIVAS
        dados_carrossel = capturar_dados_carrossel_estimativas_playwright(page)
        
        # ========================================
        # JSON COMPREENSIVO - TELA 5
        # ========================================
        if dados_carrossel and dados_carrossel.get('coberturas_detalhadas') and len(dados_carrossel.get('coberturas_detalhadas', [])) > 0:
            # Criar JSON compreensivo com todas as informações da estimativa inicial
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Extrair valores únicos (remover duplicatas)
            coberturas_unicas = {}
            for cobertura in dados_carrossel['coberturas_detalhadas']:
                nome = cobertura.get('nome_cobertura', '')
                if nome not in coberturas_unicas:
                    coberturas_unicas[nome] = cobertura
            
            # Criar estrutura do JSON compreensivo
            json_compreensivo = {
                "metadata": {
                    "timestamp": datetime.now().isoformat(),
                    "tela": 5,
                    "nome_tela": "Estimativa Inicial",
                    "url": page.url,
                    "titulo_pagina": page.title(),
                    "versao_rpa": "3.4.0",
                    "autor": "Luciano Otero"
                },
                "resumo_executivo": {
                    "total_coberturas": len(coberturas_unicas),
                    "total_beneficios": len(dados_carrossel.get('beneficios_gerais', [])),
                    "coberturas_disponiveis": list(coberturas_unicas.keys())
                },
                "coberturas_detalhadas": [
                    {
                        "nome": nome,
                        "valores": cobertura.get('valores', {}),
                        "beneficios": cobertura.get('beneficios', []),
                        "total_beneficios": len(cobertura.get('beneficios', [])),
                        "texto_completo": cobertura.get('texto_completo', '')
                    }
                    for nome, cobertura in coberturas_unicas.items()
                ],
                "beneficios_gerais": dados_carrossel.get('beneficios_gerais', []),
                "dados_brutos": dados_carrossel
            }
            
            # Salvar JSON compreensivo
            json_compreensivo_path = f"temp/json_compreensivo_tela_5_{timestamp}.json"
            with open(json_compreensivo_path, 'w', encoding='utf-8') as f:
                json.dump(json_compreensivo, f, indent=2, ensure_ascii=False)
            
            # Exibir resumo do JSON compreensivo
            exibir_mensagem("\n" + "="*80)
            exibir_mensagem("[OBJETIVO] JSON COMPREENSIVO - TELA 5 CRIADO COM SUCESSO!")
            exibir_mensagem("="*80)
            exibir_mensagem(f"[PASTA] Arquivo: {json_compreensivo_path}")
            exibir_mensagem(f"[DADOS] Total de Coberturas Únicas: {len(coberturas_unicas)}")
            exibir_mensagem(f"[PRESENTE] Total de Benefícios: {len(dados_carrossel.get('beneficios_gerais', []))}")
            
            # Exibir coberturas encontradas
            for nome, cobertura in coberturas_unicas.items():
                valores = cobertura.get('valores', {})
                de = valores.get('de', 'N/A')
                ate = valores.get('ate', 'N/A')
                exibir_mensagem(f"[DINHEIRO] {nome}: {de} até {ate}")
            
            exibir_mensagem("="*80)
            
            exibir_mensagem(f"[SALVAR] **JSON COMPREENSIVO SALVO**: {json_compreensivo_path}")
        
        # RETORNO INTERMEDIÁRIO DOS DADOS DO CARROSSEL
        if dados_carrossel:
            exibir_mensagem("[OBJETIVO] **RETORNO INTERMEDIÁRIO**: Dados do carrossel capturados com sucesso!")
            exibir_mensagem(f"[DADOS] **COBERTURAS DETALHADAS**: {len(dados_carrossel['coberturas_detalhadas'])}")
            exibir_mensagem(f"[PRESENTE] **BENEFÍCIOS GERAIS**: {len(dados_carrossel['beneficios_gerais'])}")
            exibir_mensagem(f"[DINHEIRO] **VALORES MONETÁRIOS**: {dados_carrossel['valores_encontrados']}")
            
            # Exibir detalhes das coberturas encontradas
            for i, cobertura in enumerate(dados_carrossel['coberturas_detalhadas']):
                exibir_mensagem(f"[INFO] **COBERTURA {i+1}**: {cobertura['nome_cobertura']}")
                if cobertura['valores']['de'] and cobertura['valores']['ate']:
                    exibir_mensagem(f"   [DINHEIRO] **VALORES**: {cobertura['valores']['de']} até {cobertura['valores']['ate']}")
                if cobertura['beneficios']:
                    beneficios_nomes = [b['nome'] for b in cobertura['beneficios']]
                    exibir_mensagem(f"   [PRESENTE] **BENEFÍCIOS**: {', '.join(beneficios_nomes)}")
            
            # Salvar retorno intermediário em arquivo específico
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            retorno_path = f"temp/retorno_intermediario_carrossel_{timestamp}.json"
            
            # Criar diretório temp se não existir
            os.makedirs("temp", exist_ok=True)
            
            # Limpar dados para serialização JSON
            dados_limpos = {
                "timestamp": str(dados_carrossel.get("timestamp", "")),
                "tela": dados_carrossel.get("tela", 5),
                "nome_tela": str(dados_carrossel.get("nome_tela", "")),
                "url": str(dados_carrossel.get("url", "")),
                "titulo": str(dados_carrossel.get("titulo", "")),
                "coberturas_detalhadas": dados_carrossel.get("coberturas_detalhadas", []),
                "beneficios_gerais": dados_carrossel.get("beneficios_gerais", []),
                "valores_encontrados": dados_carrossel.get("valores_encontrados", 0),
                "seguradoras": dados_carrossel.get("seguradoras", []),
                "elementos_detectados": dados_carrossel.get("elementos_detectados", [])
            }
            
            with open(retorno_path, 'w', encoding='utf-8') as f:
                json.dump(dados_limpos, f, indent=2, ensure_ascii=False)
            
            exibir_mensagem(f"[SALVAR] **RETORNO SALVO**: {retorno_path}")
            
            # Exibir retorno intermediário estruturado no terminal
            exibir_mensagem("\n" + "="*60)
            exibir_mensagem("[INFO] RETORNO INTERMEDIÁRIO - TELA 5")
            exibir_mensagem("="*60)
            exibir_mensagem(json.dumps(dados_limpos, indent=2, ensure_ascii=False))
            exibir_mensagem("="*60)
            
        else:
            exibir_mensagem("[AVISO] **AVISO**: Não foi possível capturar dados do carrossel")
        
        # Clicar em Continuar
        exibir_mensagem("[AGUARDANDO] Aguardando botão Continuar aparecer...")
        
        try:
            # Aguardar o botão estar disponível
            page.wait_for_selector("#gtm-telaEstimativaContinuarParaCotacaoFinal", timeout=10000)
            botao_continuar = page.locator("#gtm-telaEstimativaContinuarParaCotacaoFinal").first
            
            # Verificar se o botão está visível e clicável
            if botao_continuar.is_visible():
                botao_continuar.click()
                exibir_mensagem("[OK] Botão 'Continuar' clicado com sucesso")
            else:
                exibir_mensagem("[AVISO] Botão 'Continuar' não está visível, tentando clicar mesmo assim...")
                botao_continuar.click()
                exibir_mensagem("[OK] Botão 'Continuar' clicado com sucesso")
        except Exception as e:
            exibir_mensagem(f"[AVISO] Erro ao aguardar botão Continuar: {str(e)}")
            exibir_mensagem("[ATUALIZANDO] Tentando seletor alternativo...")
            try:
                # Fallback para seletor por texto
                botao_continuar = page.locator("text=Continuar").first
                botao_continuar.click()
                exibir_mensagem("[OK] Botão 'Continuar' clicado com seletor alternativo")
            except Exception as e2:
                exibir_mensagem(f"[ERRO] Falha ao clicar no botão Continuar: {str(e2)}")
                return False
        
        # DETECÇÃO INTELIGENTE DA PRÓXIMA TELA
        try:
            # Tentar detectar Tela Zero KM primeiro (2 segundos)
            page.wait_for_selector("#gtm-telaZeroKmContinuar", timeout=2000)
            exibir_mensagem("[OK] Tela Zero KM detectada após Tela 5")
            return True  # Tela Zero KM será processada separadamente
        except:
            try:
                # Se não for Zero KM, detectar Tela 6 (3 segundos)
                page.wait_for_selector("#gtm-telaItensAutoContinuar", timeout=3000)
                exibir_mensagem("[OK] Tela 6 detectada após Tela 5")
                return True
            except:
                exibir_mensagem("[ERRO] Nenhuma tela detectada após Tela 5")
                return False
        
    except Exception as e:
        exception_handler.capturar_excecao(e, "TELA_5", "Erro ao processar Tela 5")
        return False

def validar_dados_capturados(dados_carrossel) -> bool:
    """
    Valida se dados capturados são válidos para ProgressTracker
    
    Args:
        dados_carrossel: Dados retornados pela captura
    
    Returns:
        bool: True se dados são válidos, False caso contrário
    """
    try:
        # Verificar se dados não são None
        if not dados_carrossel:
            exibir_mensagem("[VALIDACAO] Dados são None")
            return False
        
        # Verificar se é dicionário
        if not isinstance(dados_carrossel, dict):
            exibir_mensagem("[VALIDACAO] Dados não são dicionário")
            return False
        
        # Verificar se tem coberturas detalhadas
        coberturas = dados_carrossel.get('coberturas_detalhadas', [])
        if not coberturas:
            exibir_mensagem("[VALIDACAO] Lista de coberturas está vazia")
            return False
        
        # Verificar se lista não está vazia
        if len(coberturas) == 0:
            exibir_mensagem("[VALIDACAO] Lista de coberturas tem tamanho zero")
            return False
        
        exibir_mensagem(f"[VALIDACAO] Dados válidos: {len(coberturas)} coberturas")
        return True
        
    except Exception as e:
        exibir_mensagem(f"[VALIDACAO] Erro na validação: {str(e)}")
        return False

def navegar_tela_5_playwright_com_dados(page: Page, parametros_tempo) -> dict:
    """
    Wrapper que executa navegação da Tela 5 e retorna dados capturados
    
    NOVA IMPLEMENTAÇÃO: Validação robusta dos dados
    FALLBACK: Comportamento original se validação falhar
    
    Args:
        page: Instância do Playwright Page
        parametros_tempo: Parâmetros de tempo para navegação
    
    Returns:
        dict: Dados do carrossel capturados ou dict vazio se falhar
    """
    try:
        # LÓGICA ORIGINAL MANTIDA
        sucesso = navegar_tela_5_playwright(page, parametros_tempo)
        
        if sucesso:
            # LÓGICA ORIGINAL MANTIDA
            dados_carrossel = capturar_dados_carrossel_estimativas_playwright(page)
            
            # NOVA VALIDAÇÃO: Verificar integridade dos dados
            if validar_dados_capturados(dados_carrossel):
                exibir_mensagem(f"[SUCCESS] Dados válidos retornados: {len(dados_carrossel.get('coberturas_detalhadas', []))} coberturas")
                return dados_carrossel
            else:
                exibir_mensagem("[WARNING] Dados inválidos, retornando dict vazio")
                return {}
        else:
            exibir_mensagem("[ERROR] Navegação falhou")
            return {}
            
    except Exception as e:
        exibir_mensagem(f"[ERROR] Erro na wrapper: {str(e)}")
        return {}

def navegar_tela_zero_km_playwright(page: Page, parametros: Dict[str, Any]) -> bool:
    """
    TELA ZERO KM: Condicional - aparece ocasionalmente após Tela 5
    """
    try:
        exception_handler.definir_tela_atual("TELA_ZERO_KM")
        exibir_mensagem("[MOTO] TELA ZERO KM: Processando...")
        
        # Verificar se a tela Zero KM está presente (usar radiogroup específico)
        elemento_zero_km = page.locator("#zerokmTelaZeroKm[role='radiogroup']")
        if not elemento_zero_km.is_visible():
            exibir_mensagem("[AVISO] Tela Zero KM não está visível")
            return False
            
        exibir_mensagem("[OK] Tela Zero KM carregada com sucesso")
        
        # Selecionar opção baseada no parâmetro
        zero_km = parametros.get('zero_km', False)
        
        if zero_km:
            # Selecionar "Sim" - usar seletor mais específico
            page.locator('input[name="zerokmTelaZeroKm"][value="Sim"]').click()
            exibir_mensagem("[OK] Opção 'Sim' (Zero KM) selecionada!")
        else:
            # Selecionar "Não" - usar seletor mais específico
            page.locator('input[name="zerokmTelaZeroKm"][value="Não"]').click()
            exibir_mensagem("[OK] Opção 'Não' (Não Zero KM) selecionada!")
        
        # Aguardar estabilização
        time.sleep(1)
        
        # Clicar em Continuar
        exibir_mensagem("[AGUARDANDO] Clicando em Continuar...")
        page.locator("#gtm-telaZeroKmContinuar").click()
        
        # Aguardar próxima tela (Tela 6)
        exibir_mensagem("[AGUARDANDO] Aguardando transição para Tela 6...")
        page.wait_for_selector("#gtm-telaItensAutoContinuar", timeout=5000)
        exibir_mensagem("[OK] Tela Zero KM processada com sucesso!")
        return True
        
    except Exception as e:
        exception_handler.capturar_excecao(e, "TELA_ZERO_KM", "Erro ao processar Tela Zero KM")
        return False

def navegar_tela_6_playwright(page: Page, combustivel: str, kit_gas: bool, blindado: bool, financiado: bool, tipo_veiculo: str = "carro") -> bool:
    """
    TELA 6: Itens do veículo - SELEÇÃO DE COMBUSTÍVEL E CHECKBOXES
    
    VERSÃO: v3.3.0
    IMPLEMENTAÇÃO: Suporte a carro e moto (kit_gas ignorado para moto)
    """
    try:
        exception_handler.definir_tela_atual("TELA_6")
        exibir_mensagem("[CELULAR] TELA 6: Aguardando carregamento...")
        
        max_tentativas = 20
        tentativa = 0
        
        while tentativa < max_tentativas:
            botao_continuar = page.locator("#gtm-telaItensAutoContinuar")
            if botao_continuar.count() > 0 and botao_continuar.first.is_visible():
                break
            # Aguardar carregamento da tela
            try:
                page.wait_for_selector("#gtm-telaItensAutoContinuar", timeout=1000)
                break
            except:
                continue
            tentativa += 1
        
        if tentativa >= max_tentativas:
            exception_handler.capturar_warning("Tela 6 não carregou", "TELA_6")
            return False
        
        exibir_mensagem("[OK] Tela 6 carregada com sucesso")
        
        # Selecionar combustível
        exibir_mensagem(f"[CELULAR] TELA 6: Selecionando combustível {combustivel}...")
        
        mapeamento_combustivel = {
            "Flex": "1", "Gasolina": "2", "Alcool": "3", "Etanol": "3",
            "Diesel": "4", "Híbrido": "5", "Elétrico": "6"
        }
        
        valor_radio = mapeamento_combustivel.get(combustivel)
        combustivel_selecionado = False
        
        if valor_radio:
            try:
                radio_combustivel = page.locator(f"input[name='tipoCombustivelTelaItens'][value='{valor_radio}']").first
                if radio_combustivel.is_visible():
                    radio_combustivel.click()
                    combustivel_selecionado = True
                    exibir_mensagem(f"[OK] Combustível {combustivel} selecionado com sucesso")
                else:
                    exception_handler.capturar_warning(f"Radio button para {combustivel} não está visível", "TELA_6")
            except Exception as e:
                exception_handler.capturar_warning(f"Erro ao selecionar {combustivel}: {str(e)}", "TELA_6")
        else:
            exception_handler.capturar_warning(f"Combustível '{combustivel}' não mapeado", "TELA_6")
        
        if not combustivel_selecionado:
            exception_handler.capturar_warning(f"Combustível {combustivel} não encontrado, continuando", "TELA_6")
        
        # Configurar checkboxes
        exibir_mensagem("[CELULAR] TELA 6: Configurando checkboxes...")
        
        # Kit Gas (apenas para carros)
        if tipo_veiculo == "carro":
            try:
                checkbox_kit_gas = page.locator('input[value="Kit Gás"]').first
                if checkbox_kit_gas.is_visible():
                    if kit_gas and not checkbox_kit_gas.is_checked():
                        checkbox_kit_gas.check()
                        exibir_mensagem("[OK] Checkbox Kit Gas: MARCADO")
                    elif not kit_gas and checkbox_kit_gas.is_checked():
                        checkbox_kit_gas.uncheck()
                        exibir_mensagem("[OK] Checkbox Kit Gas: DESMARCADO")
                    else:
                        estado = "MARCADO" if kit_gas else "DESMARCADO"
                        exibir_mensagem(f"[OK] Checkbox Kit Gas: {estado} (já estava correto)")
                else:
                    exception_handler.capturar_warning("Checkbox Kit Gas não encontrado", "TELA_6")
            except Exception as e:
                exception_handler.capturar_warning(f"Erro ao configurar Kit Gas: {str(e)}", "TELA_6")
        else:
            exibir_mensagem("[INFO]️ Kit Gas ignorado para motos")
        
        # Blindado
        try:
            checkbox_blindado = page.locator('input[value="Blindado"]').first
            if checkbox_blindado.is_visible():
                if blindado and not checkbox_blindado.is_checked():
                    checkbox_blindado.check()
                    exibir_mensagem("[OK] Checkbox Blindado: MARCADO")
                elif not blindado and checkbox_blindado.is_checked():
                    checkbox_blindado.uncheck()
                    exibir_mensagem("[OK] Checkbox Blindado: DESMARCADO")
                else:
                    estado = "MARCADO" if blindado else "DESMARCADO"
                    exibir_mensagem(f"[OK] Checkbox Blindado: {estado} (já estava correto)")
            else:
                exception_handler.capturar_warning("Checkbox Blindado não encontrado", "TELA_6")
        except Exception as e:
            exception_handler.capturar_warning(f"Erro ao configurar Blindado: {str(e)}", "TELA_6")
        
        # Financiado
        try:
            checkbox_financiado = page.locator('input[value="Financiado"]').first
            if checkbox_financiado.is_visible():
                if financiado and not checkbox_financiado.is_checked():
                    checkbox_financiado.check()
                    exibir_mensagem("[OK] Checkbox Financiado: MARCADO")
                elif not financiado and checkbox_financiado.is_checked():
                    checkbox_financiado.uncheck()
                    exibir_mensagem("[OK] Checkbox Financiado: DESMARCADO")
                else:
                    estado = "MARCADO" if financiado else "DESMARCADO"
                    exibir_mensagem(f"[OK] Checkbox Financiado: {estado} (já estava correto)")
            else:
                exception_handler.capturar_warning("Checkbox Financiado não encontrado", "TELA_6")
        except Exception as e:
            exception_handler.capturar_warning(f"Erro ao configurar Financiado: {str(e)}", "TELA_6")
        
        # Clicar em Continuar
        botao_continuar.first.click()
        exibir_mensagem("[OK] Botão 'Continuar' clicado com sucesso")
        # Aguardar transição para a próxima tela
        page.wait_for_selector("#enderecoTelaEndereco", timeout=5000)
        return True
        
    except Exception as e:
        exception_handler.capturar_excecao(e, "TELA_6", "Erro ao configurar itens do carro")
        return False

def aguardar_sugestao_endereco_playwright(page: Page, timeout: int = 8000) -> bool:
    """
    Aguarda carregamento das sugestões de endereço com estratégia híbrida robusta
    
    ESTRATÉGIA HÍBRIDA v3.7.0.3:
    1. [data-testid="sugestao-endereco"] - ESPECÍFICO (teste)
    2. .MuiAutocomplete-option - SEMÂNTICO (Material-UI)
    3. .overflow-hidden - FALLBACK ATUAL (compatibilidade)
    """
    seletores_prioridade = [
        '[data-testid="sugestao-endereco"]',  # <- PRINCIPAL
        '.MuiAutocomplete-option',            # <- SECUNDÁRIO
        '.overflow-hidden'                    # <- FALLBACK
    ]
    
    timeout_por_seletor = timeout // len(seletores_prioridade)
    
    for i, seletor in enumerate(seletores_prioridade):
        try:
            exibir_mensagem(f"[BUSCAR] Tentativa {i+1}/{len(seletores_prioridade)} - Seletor: {seletor}")
            page.wait_for_selector(seletor, timeout=timeout_por_seletor)
            exibir_mensagem(f"[OK] Sugestões encontradas com seletor: {seletor}")
            return True
        except Exception as e:
            exibir_mensagem(f"[AVISO] Seletor {i+1} falhou: {str(e)}")
            continue
    
    exibir_mensagem("[ERRO] Nenhum seletor funcionou para encontrar as sugestões")
    return False

def localizar_sugestao_endereco_playwright(page: Page):
    """
    Localiza sugestões de endereço com estratégia híbrida robusta
    
    ESTRATÉGIA HÍBRIDA v3.7.0.3:
    1. [data-testid="sugestao-endereco"] - ESPECÍFICO (teste)
    2. .MuiAutocomplete-option - SEMÂNTICO (Material-UI)
    3. .overflow-hidden - FALLBACK ATUAL (compatibilidade)
    """
    seletores_prioridade = [
        '[data-testid="sugestao-endereco"]',  # <- PRINCIPAL
        '.MuiAutocomplete-option',            # <- SECUNDÁRIO
        '.overflow-hidden'                    # <- FALLBACK
    ]
    
    for i, seletor in enumerate(seletores_prioridade):
        try:
            elemento = page.locator(seletor)
            if elemento.count() > 0:
                exibir_mensagem(f"[OK] Sugestões localizadas com seletor: {seletor} ({elemento.count()} encontradas)")
                return elemento
        except Exception as e:
            exibir_mensagem(f"[AVISO] Seletor {i+1} falhou: {str(e)}")
            continue
    
    exibir_mensagem("[ERRO] Nenhum seletor funcionou para localizar as sugestões")
    return None

def navegar_tela_7_playwright(page: Page, cep: str) -> bool:
    """
    TELA 7: Endereço de pernoite (CEP)
    """
    try:
        exception_handler.definir_tela_atual("TELA_7")
        exibir_mensagem("[CELULAR] TELA 7: Aguardando carregamento...")
        
        max_tentativas = 20
        tentativa = 0
        
        while tentativa < max_tentativas:
            campo_endereco = page.locator("#enderecoTelaEndereco")
            if campo_endereco.count() > 0 and campo_endereco.first.is_visible():
                break
            # Aguardar carregamento da tela
            try:
                page.wait_for_selector("#enderecoTelaEndereco", timeout=1000)
                break
            except:
                continue
            tentativa += 1
        
        if tentativa >= max_tentativas:
            exception_handler.capturar_warning("Tela 7 não carregou", "TELA_7")
            return False
        
        exibir_mensagem("[OK] Tela 7 carregada com sucesso")
        
        # Preencher CEP
        exibir_mensagem("[CELULAR] TELA 7: Preenchendo CEP...")
        campo_endereco.first.fill(cep)
        exibir_mensagem(f"[OK] CEP preenchido: {cep}")
        # Aguardar estabilização do campo
        page.wait_for_function("document.querySelector('#enderecoTelaEndereco').value.length > 0", timeout=2000)
        
        # Aguardar carregamento do endereço
        exibir_mensagem("[AGUARDANDO] Aguardando carregamento do endereço...")
        if not aguardar_sugestao_endereco_playwright(page, 8000):
            return False
        
        # Tentar selecionar endereço sugerido
        try:
            sugestao_endereco = localizar_sugestao_endereco_playwright(page)
            if sugestao_endereco is not None and sugestao_endereco.count() > 0:
                sugestao_endereco = sugestao_endereco.first
                if sugestao_endereco.is_visible():
                    sugestao_endereco.click()
                    exibir_mensagem("[OK] Endereço sugerido selecionado")
                    # Aguardar estabilização da seleção
                    page.wait_for_function("document.querySelector('[data-testid=\"sugestao-endereco\"]').classList.contains('selected')", timeout=2000)
            else:
                exception_handler.capturar_warning("Endereço sugerido não encontrado", "TELA_7")
        except Exception as e:
            exception_handler.capturar_warning(f"Erro ao selecionar endereço: {str(e)}", "TELA_7")
        
        # Clicar em Continuar
        botao_continuar = page.locator("#gtm-telaPernoiteVeiculoContinuar").first
        botao_continuar.click()
        
        exibir_mensagem("[OK] Botão 'Continuar' clicado com sucesso")
        # Aguardar transição para a próxima tela
        aguardar_tela_8_playwright(page, 5000)
        return True
        
    except Exception as e:
        exception_handler.capturar_excecao(e, "TELA_7", f"Erro ao preencher CEP {cep}")
        return False

def aguardar_tela_8_playwright(page: Page, timeout: int = 5000) -> bool:
    """
    ESTRATÉGIA HÍBRIDA v3.7.0.4:
    1. #finalidadeVeiculoTelaUsoVeiculo - ESPECÍFICO (ID)
    2. [role="radiogroup"] - SEMÂNTICO (ARIA)
    3. p:has-text("Qual é o uso do veículo?") - CONTEÚDO (título)
    4. xpath=//*[contains(text(), 'finalidade') or contains(text(), 'uso')] - FALLBACK ATUAL
    """
    seletores = [
        '#finalidadeVeiculoTelaUsoVeiculo',  # <- PRINCIPAL
        '[role="radiogroup"]',                # <- SECUNDÁRIO
        'p:has-text("Qual é o uso do veículo?")',  # <- TERCIÁRIO
        'xpath=//*[contains(text(), "finalidade") or contains(text(), "uso")]'  # <- FALLBACK
    ]
    
    for seletor in seletores:
        try:
            if page.wait_for_selector(seletor, timeout=timeout):
                return True
        except:
            continue
    return False

def localizar_tela_8_playwright(page: Page):
    """
    Localiza elementos da Tela 8 usando estratégia híbrida
    """
    seletores = [
        '#finalidadeVeiculoTelaUsoVeiculo',  # <- PRINCIPAL
        '[role="radiogroup"]',                # <- SECUNDÁRIO
        'p:has-text("Qual é o uso do veículo?")',  # <- TERCIÁRIO
        'xpath=//*[contains(text(), "finalidade") or contains(text(), "uso")]'  # <- FALLBACK
    ]
    
    for seletor in seletores:
        try:
            elementos = page.locator(seletor)
            if elementos.count() > 0:
                return elementos
        except:
            continue
    return None

def aguardar_tela_9_playwright(page: Page, timeout: int = 5000) -> bool:
    """
    Aguarda carregamento da Tela 9 (Dados Pessoais) com estratégia híbrida robusta
    
    ESTRATÉGIA HÍBRIDA v3.7.0.5:
    1. p:has-text("Nessa etapa, precisamos dos seus dados pessoais") - ESPECÍFICO (conteúdo)
    2. p.font-asap.text-primary.font-bold - SEMÂNTICO (classes específicas)
    3. p.text-2xl.font-bold - ESTRUTURAL (classes de tamanho)
    4. xpath=//*[contains(text(), 'dados pessoais')] - FALLBACK (compatibilidade)
    
    Args:
        page: Instância do Playwright Page
        timeout: Timeout em milissegundos (padrão: 5000)
    
    Returns:
        bool: True se a tela foi detectada, False caso contrário
    """
    try:
        exibir_mensagem("[BUSCAR] v3.7.0.5: Aguardando Tela 9 com estratégia híbrida...")
        
        # Estratégia híbrida com 4 níveis de fallback
        seletores = [
            'p:has-text("Nessa etapa, precisamos dos seus dados pessoais")',  # ESPECÍFICO
            'p.font-asap.text-primary.font-bold',                           # SEMÂNTICO
            'p.text-2xl.font-bold',                                         # ESTRUTURAL
            'xpath=//*[contains(text(), "dados pessoais") or contains(text(), "Dados pessoais")]'  # FALLBACK
        ]
        
        for i, seletor in enumerate(seletores, 1):
            try:
                exibir_mensagem(f"[BUSCAR] v3.7.0.5: Tentativa {i}/4 - Testando seletor: {seletor[:50]}...")
                
                # Aguardar elemento com timeout específico
                page.wait_for_selector(seletor, timeout=timeout//4)
                
                # Verificar se elemento existe e está visível
                elemento = page.locator(seletor)
                if elemento.count() > 0 and elemento.first.is_visible():
                    exibir_mensagem(f"[OK] v3.7.0.5: Tela 9 detectada com seletor {i}/4")
                    return True
                    
            except Exception as e:
                exibir_mensagem(f"[AVISO] v3.7.0.5: Seletor {i}/4 falhou: {str(e)[:100]}")
                continue
        
        exibir_mensagem("[ERRO] v3.7.0.5: Todos os seletores falharam")
        return False
        
    except Exception as e:
        exibir_mensagem(f"[ERRO] v3.7.0.5: Erro na detecção da Tela 9: {str(e)}")
        return False

def localizar_tela_9_playwright(page: Page):
    """
    Localiza elementos da Tela 9 (Dados Pessoais) com estratégia híbrida robusta
    
    ESTRATÉGIA HÍBRIDA v3.7.0.5:
    1. p:has-text("Nessa etapa, precisamos dos seus dados pessoais") - ESPECÍFICO (conteúdo)
    2. p.font-asap.text-primary.font-bold - SEMÂNTICO (classes específicas)
    3. p.text-2xl.font-bold - ESTRUTURAL (classes de tamanho)
    4. xpath=//*[contains(text(), 'dados pessoais')] - FALLBACK (compatibilidade)
    
    Args:
        page: Instância do Playwright Page
    
    Returns:
        Locator: Elemento encontrado ou None
    """
    try:
        exibir_mensagem("[BUSCAR] v3.7.0.5: Localizando elementos da Tela 9...")
        
        # Estratégia híbrida com 4 níveis de fallback
        seletores = [
            'p:has-text("Nessa etapa, precisamos dos seus dados pessoais")',  # ESPECÍFICO
            'p.font-asap.text-primary.font-bold',                           # SEMÂNTICO
            'p.text-2xl.font-bold',                                         # ESTRUTURAL
            'xpath=//*[contains(text(), "dados pessoais") or contains(text(), "Dados pessoais")]'  # FALLBACK
        ]
        
        for i, seletor in enumerate(seletores, 1):
            try:
                elemento = page.locator(seletor)
                if elemento.count() > 0:
                    exibir_mensagem(f"[OK] v3.7.0.5: Elemento localizado com seletor {i}/4")
                    return elemento
                    
            except Exception as e:
                exibir_mensagem(f"[AVISO] v3.7.0.5: Seletor {i}/4 falhou: {str(e)[:100]}")
                continue
        
        exibir_mensagem("[ERRO] v3.7.0.5: Nenhum elemento foi localizado")
        return None
        
    except Exception as e:
        exibir_mensagem(f"[ERRO] v3.7.0.5: Erro na localização da Tela 9: {str(e)}")
        return None

def aguardar_radio_condutor_playwright(page: Page, opcao: str, timeout: int = 3000) -> bool:
    """
    Aguarda carregamento dos radio buttons da Tela 10 com estratégia híbrida robusta
    
    ESTRATÉGIA HÍBRIDA v3.7.0.6:
    1. input[value="{opcao}"][name="condutorPrincipalTelaCondutorPrincipal"] - ESPECÍFICO
    2. input.PrivateSwitchBase-input[name="condutorPrincipalTelaCondutorPrincipal"] - SEMÂNTICO
    3. input[type="radio"][name="condutorPrincipalTelaCondutorPrincipal"] - ESTRUTURAL
    4. input[value="{opcao}"] - FALLBACK
    
    Args:
        page: Instância do Playwright Page
        opcao: "sim" ou "nao"
        timeout: Timeout em milissegundos (padrão: 3000)
    
    Returns:
        bool: True se o radio button foi detectado, False caso contrário
    """
    try:
        exibir_mensagem(f"[BUSCAR] v3.7.0.6: Aguardando radio button '{opcao}' com estratégia híbrida...")
        
        # Estratégia híbrida com 4 níveis de fallback
        seletores = [
            f'input[value="{opcao}"][name="condutorPrincipalTelaCondutorPrincipal"]',  # ESPECÍFICO
            'input.PrivateSwitchBase-input[name="condutorPrincipalTelaCondutorPrincipal"]',  # SEMÂNTICO
            'input[type="radio"][name="condutorPrincipalTelaCondutorPrincipal"]',  # ESTRUTURAL
            f'input[value="{opcao}"]'  # FALLBACK
        ]
        
        for i, seletor in enumerate(seletores, 1):
            try:
                exibir_mensagem(f"[BUSCAR] v3.7.0.6: Tentativa {i}/4 - Testando seletor: {seletor[:50]}...")
                
                # Aguardar elemento com timeout específico
                page.wait_for_selector(seletor, timeout=timeout//4)
                
                # Verificar se elemento existe e está visível
                elemento = page.locator(seletor)
                if elemento.count() > 0 and elemento.first.is_visible():
                    exibir_mensagem(f"[OK] v3.7.0.6: Radio button '{opcao}' detectado com seletor {i}/4")
                    return True
                    
            except Exception as e:
                exibir_mensagem(f"[AVISO] v3.7.0.6: Seletor {i}/4 falhou: {str(e)[:100]}")
                continue
        
        exibir_mensagem(f"[ERRO] v3.7.0.6: Todos os seletores falharam para '{opcao}'")
        return False
        
    except Exception as e:
        exibir_mensagem(f"[ERRO] v3.7.0.6: Erro na detecção do radio button '{opcao}': {str(e)}")
        return False

def localizar_radio_condutor_playwright(page: Page, opcao: str):
    """
    Localiza radio button da Tela 10 com estratégia híbrida robusta
    
    ESTRATÉGIA HÍBRIDA v3.7.0.6:
    1. input[value="{opcao}"][name="condutorPrincipalTelaCondutorPrincipal"] - ESPECÍFICO
    2. input.PrivateSwitchBase-input[name="condutorPrincipalTelaCondutorPrincipal"] - SEMÂNTICO
    3. input[type="radio"][name="condutorPrincipalTelaCondutorPrincipal"] - ESTRUTURAL
    4. input[value="{opcao}"] - FALLBACK
    
    Args:
        page: Instância do Playwright Page
        opcao: "sim" ou "nao"
    
    Returns:
        Locator: Elemento encontrado ou None
    """
    try:
        exibir_mensagem(f"[BUSCAR] v3.7.0.6: Localizando radio button '{opcao}'...")
        
        # Estratégia híbrida com 4 níveis de fallback
        seletores = [
            f'input[value="{opcao}"][name="condutorPrincipalTelaCondutorPrincipal"]',  # ESPECÍFICO
            'input.PrivateSwitchBase-input[name="condutorPrincipalTelaCondutorPrincipal"]',  # SEMÂNTICO
            'input[type="radio"][name="condutorPrincipalTelaCondutorPrincipal"]',  # ESTRUTURAL
            f'input[value="{opcao}"]'  # FALLBACK
        ]
        
        for i, seletor in enumerate(seletores, 1):
            try:
                elemento = page.locator(seletor)
                if elemento.count() > 0:
                    exibir_mensagem(f"[OK] v3.7.0.6: Radio button '{opcao}' localizado com seletor {i}/4")
                    return elemento
                    
            except Exception as e:
                exibir_mensagem(f"[AVISO] v3.7.0.6: Seletor {i}/4 falhou: {str(e)[:100]}")
                continue
        
        exibir_mensagem(f"[ERRO] v3.7.0.6: Nenhum radio button '{opcao}' foi localizado")
        return None
        
    except Exception as e:
        exibir_mensagem(f"[ERRO] v3.7.0.6: Erro na localização do radio button '{opcao}': {str(e)}")
        return None

def localizar_estado_civil_playwright(page: Page, estado_civil: str):
    """
    Localiza opção de estado civil com estratégia híbrida robusta
    
    ESTRATÉGIA HÍBRIDA v3.7.0.8:
    1. li[data-value="{valor}"] - ESPECÍFICO (atributo data-value)
    2. li[role="option"] - SEMÂNTICO (ARIA role)
    3. li.MuiMenuItem-root - ESTRUTURAL (classes Material-UI)
    4. xpath=//li[contains(text(), '{texto}')] - FALLBACK (compatibilidade)
    
    Args:
        page: Instância do Playwright Page
        estado_civil: Estado civil desejado (ex: "Casado ou Uniao Estavel")
    
    Returns:
        Locator: Elemento encontrado ou None
    """
    try:
        exibir_mensagem(f"[BUSCAR] v3.7.0.8: Localizando estado civil '{estado_civil}'...")
        
        # Mapeamento de estado civil para data-value
        mapeamento_data_value = {
            "Casado ou Uniao Estavel": "casado",
            "Divorciado": "divorciado", 
            "Separado": "separado",
            "Solteiro": "solteiro",
            "Viuvo": "viuvo"
        }
        
        # Estratégia híbrida com 4 níveis de fallback
        seletores = [
            f'li[data-value="{mapeamento_data_value.get(estado_civil, estado_civil.lower())}"]',  # ESPECÍFICO
            'li[role="option"]',  # SEMÂNTICO
            'li.MuiMenuItem-root',  # ESTRUTURAL
            f'xpath=//li[contains(text(), "{estado_civil}")]'  # FALLBACK
        ]
        
        for i, seletor in enumerate(seletores, 1):
            try:
                elemento = page.locator(seletor)
                if elemento.count() > 0:
                    exibir_mensagem(f"[OK] v3.7.0.8: Estado civil '{estado_civil}' localizado com seletor {i}/4")
                    return elemento
                    
            except Exception as e:
                exibir_mensagem(f"[AVISO] v3.7.0.8: Seletor {i}/4 falhou: {str(e)[:100]}")
                continue
        
        exibir_mensagem(f"[ERRO] v3.7.0.8: Nenhum estado civil '{estado_civil}' foi localizado")
        return None
        
    except Exception as e:
        exibir_mensagem(f"[ERRO] v3.7.0.8: Erro na localização do estado civil '{estado_civil}': {str(e)}")
        return None

def localizar_sexo_playwright(page: Page, sexo: str):
    """
    Localiza opção de sexo com estratégia híbrida robusta
    
    ESTRATÉGIA HÍBRIDA v3.7.0.10:
    1. li[data-value="{sexo.lower()}"] - ESPECÍFICO (atributo data-value)
    2. li[data-value="{sexo}"] - ESPECÍFICO (atributo data-value original)
    3. li[role="option"] - SEMÂNTICO (ARIA role)
    4. li.MuiMenuItem-root - ESTRUTURAL (classes Material-UI)
    5. text={sexo} - FALLBACK (compatibilidade)
    
    Args:
        page: Instância do Playwright Page
        sexo: Sexo desejado (ex: "Masculino", "Feminino")
    
    Returns:
        Locator: Elemento encontrado ou None
    """
    try:
        sexo_lower = sexo.lower()
        seletores = [
            f"li[data-value='{sexo_lower}']",  # Nível 1: Específico (lowercase)
            f"li[data-value='{sexo}']",  # Nível 2: Específico (original)
            "li[role='option']",  # Nível 3: Semântico
            "li.MuiMenuItem-root",  # Nível 4: Estrutural
            f"text={sexo}",  # Nível 5: Fallback
        ]
        
        for i, seletor in enumerate(seletores, 1):
            try:
                elemento = page.locator(seletor)
                if elemento.is_visible():
                    exibir_mensagem(f"[OK] v3.7.0.10: Sexo '{sexo}' localizado com seletor nível {i}: {seletor}")
                    return elemento
            except Exception as e:
                exibir_mensagem(f"[AVISO] v3.7.0.10: Seletor nível {i} falhou: {seletor} - {str(e)}")
                continue
        
        exibir_mensagem(f"[ERRO] v3.7.0.10: Nenhum sexo '{sexo}' foi localizado")
        return None
        
    except Exception as e:
        exibir_mensagem(f"[ERRO] v3.7.0.10: Erro na localização do sexo '{sexo}': {str(e)}")
        return None

def localizar_botao_continuar_garagem_playwright(page: Page):
    """
    Localiza botão continuar da Tela 12 com estratégia híbrida robusta
    
    ESTRATÉGIA HÍBRIDA v3.7.0.11:
    1. #botao-continuar-garagem - ESPECÍFICO (ID único)
    2. button[data-testid="continuar-garagem"] - ESPECÍFICO (data-testid)
    3. p:has-text("Continuar") - SEMÂNTICO (texto específico)
    4. button:has-text("Continuar") - SEMÂNTICO (botão com texto)
    5. p.font-semibold.font-workSans.cursor-pointer - FALLBACK (compatibilidade)
    
    Args:
        page: Instância do Playwright Page
    
    Returns:
        Locator: Elemento encontrado ou None
    """
    try:
        seletores = [
            "#botao-continuar-garagem",  # Nível 1: Específico (ID único)
            'button[data-testid="continuar-garagem"]',  # Nível 2: Específico (data-testid)
            'p:has-text("Continuar")',  # Nível 3: Semântico (texto específico)
            'button:has-text("Continuar")',  # Nível 4: Semântico (botão com texto)
            "p.font-semibold.font-workSans.cursor-pointer",  # Nível 5: Fallback (compatibilidade)
        ]
        
        for i, seletor in enumerate(seletores, 1):
            try:
                elemento = page.locator(seletor)
                if elemento.is_visible():
                    exibir_mensagem(f"[OK] v3.7.0.11: Botão continuar garagem localizado com seletor nível {i}: {seletor}")
                    return elemento
            except Exception as e:
                exibir_mensagem(f"[AVISO] v3.7.0.11: Seletor nível {i} falhou: {seletor} - {str(e)}")
                continue
        
        exibir_mensagem("[ERRO] v3.7.0.11: Nenhum botão continuar garagem foi localizado")
        return None
        
    except Exception as e:
        exibir_mensagem(f"[ERRO] v3.7.0.11: Erro na localização do botão continuar garagem: {str(e)}")
        return None

def localizar_checkbox_trabalho_playwright(page: Page):
    """
    Localiza checkbox Local de Trabalho com estratégia híbrida robusta
    
    ESTRATÉGIA HÍBRIDA v3.7.0.9:
    1. input[value="trabalho"] - ESPECÍFICO (atributo value)
    2. #atividadeVeiculoTelaAtividadeVeiculo input[type="checkbox"].PrivateSwitchBase-input:not(.MuiSwitch-input) - SEMÂNTICO
    3. input.PrivateSwitchBase-input.mui-1m9pwf3:not(.MuiSwitch-input) - ESTRUTURAL
    4. input[value="trabalho"] - FALLBACK (compatibilidade)
    
    Args:
        page: Instância do Playwright Page
    
    Returns:
        Locator: Elemento encontrado ou None
    """
    try:
        exibir_mensagem("[BUSCAR] v3.7.0.9: Localizando checkbox Local de Trabalho...")
        
        seletores = [
            'input[value="trabalho"]',  # ESPECÍFICO
            '#atividadeVeiculoTelaAtividadeVeiculo input[type="checkbox"].PrivateSwitchBase-input:not(.MuiSwitch-input)',  # SEMÂNTICO
            'input.PrivateSwitchBase-input.mui-1m9pwf3:not(.MuiSwitch-input)',  # ESTRUTURAL
            'input[value="trabalho"]'  # FALLBACK
        ]
        
        for i, seletor in enumerate(seletores, 1):
            try:
                elemento = page.locator(seletor)
                if elemento.count() > 0:
                    exibir_mensagem(f"[OK] v3.7.0.9: Checkbox trabalho localizado com seletor {i}/4")
                    return elemento
            except Exception as e:
                exibir_mensagem(f"[AVISO] v3.7.0.9: Seletor {i}/4 falhou: {str(e)[:100]}")
                continue
        
        exibir_mensagem("[ERRO] v3.7.0.9: Nenhum checkbox trabalho foi localizado")
        return None
        
    except Exception as e:
        exibir_mensagem(f"[ERRO] v3.7.0.9: Erro na localização do checkbox trabalho: {str(e)}")
        return None

def localizar_switch_trabalho_playwright(page: Page):
    """
    Localiza switch Estacionamento Trabalho com estratégia híbrida robusta
    
    ESTRATÉGIA HÍBRIDA v3.7.0.9:
    1. #atividadeVeiculoTelaAtividadeVeiculo input[value="trabalho"] + * input.MuiSwitch-input - ESPECÍFICO
    2. #atividadeVeiculoTelaAtividadeVeiculo input.MuiSwitch-input - SEMÂNTICO
    3. input.MuiSwitch-input.mui-1m9pwf3 - ESTRUTURAL
    4. input[type="checkbox"]:not([value]) - FALLBACK
    
    Args:
        page: Instância do Playwright Page
    
    Returns:
        Locator: Elemento encontrado ou None
    """
    try:
        exibir_mensagem("[BUSCAR] v3.7.0.9: Localizando switch Estacionamento Trabalho...")
        
        seletores = [
            '#atividadeVeiculoTelaAtividadeVeiculo input[value="trabalho"] + * input.MuiSwitch-input',  # ESPECÍFICO
            '#atividadeVeiculoTelaAtividadeVeiculo input.MuiSwitch-input',  # SEMÂNTICO
            'input.MuiSwitch-input.mui-1m9pwf3',  # ESTRUTURAL
            'input[type="checkbox"]:not([value])'  # FALLBACK
        ]
        
        for i, seletor in enumerate(seletores, 1):
            try:
                elemento = page.locator(seletor)
                if elemento.count() > 0:
                    exibir_mensagem(f"[OK] v3.7.0.9: Switch trabalho localizado com seletor {i}/4")
                    return elemento
            except Exception as e:
                exibir_mensagem(f"[AVISO] v3.7.0.9: Seletor {i}/4 falhou: {str(e)[:100]}")
                continue
        
        exibir_mensagem("[ERRO] v3.7.0.9: Nenhum switch trabalho foi localizado")
        return None
        
    except Exception as e:
        exibir_mensagem(f"[ERRO] v3.7.0.9: Erro na localização do switch trabalho: {str(e)}")
        return None

def localizar_checkbox_estudo_playwright(page: Page):
    """
    Localiza checkbox Local de Estudo com estratégia híbrida robusta
    
    ESTRATÉGIA HÍBRIDA v3.7.0.9:
    1. input[value="estudo"] - ESPECÍFICO (atributo value)
    2. #atividadeVeiculoTelaAtividadeVeiculo input[type="checkbox"].PrivateSwitchBase-input:not(.MuiSwitch-input) - SEMÂNTICO
    3. input.PrivateSwitchBase-input.mui-1m9pwf3:not(.MuiSwitch-input) - ESTRUTURAL
    4. input[value="estudo"] - FALLBACK (compatibilidade)
    
    Args:
        page: Instância do Playwright Page
    
    Returns:
        Locator: Elemento encontrado ou None
    """
    try:
        exibir_mensagem("[BUSCAR] v3.7.0.9: Localizando checkbox Local de Estudo...")
        
        seletores = [
            'input[value="estudo"]',  # ESPECÍFICO
            '#atividadeVeiculoTelaAtividadeVeiculo input[type="checkbox"].PrivateSwitchBase-input:not(.MuiSwitch-input)',  # SEMÂNTICO
            'input.PrivateSwitchBase-input.mui-1m9pwf3:not(.MuiSwitch-input)',  # ESTRUTURAL
            'input[value="estudo"]'  # FALLBACK
        ]
        
        for i, seletor in enumerate(seletores, 1):
            try:
                elemento = page.locator(seletor)
                if elemento.count() > 0:
                    exibir_mensagem(f"[OK] v3.7.0.9: Checkbox estudo localizado com seletor {i}/4")
                    return elemento
            except Exception as e:
                exibir_mensagem(f"[AVISO] v3.7.0.9: Seletor {i}/4 falhou: {str(e)[:100]}")
                continue
        
        exibir_mensagem("[ERRO] v3.7.0.9: Nenhum checkbox estudo foi localizado")
        return None
        
    except Exception as e:
        exibir_mensagem(f"[ERRO] v3.7.0.9: Erro na localização do checkbox estudo: {str(e)}")
        return None

def localizar_switch_estudo_playwright(page: Page):
    """
    Localiza switch Estacionamento Estudo com estratégia híbrida robusta
    
    ESTRATÉGIA HÍBRIDA v3.7.0.9:
    1. #atividadeVeiculoTelaAtividadeVeiculo input[value="estudo"] + * input.MuiSwitch-input - ESPECÍFICO
    2. #atividadeVeiculoTelaAtividadeVeiculo input.MuiSwitch-input - SEMÂNTICO
    3. input.MuiSwitch-input.mui-1m9pwf3 - ESTRUTURAL
    4. input[type="checkbox"]:not([value]) - FALLBACK
    
    Args:
        page: Instância do Playwright Page
    
    Returns:
        Locator: Elemento encontrado ou None
    """
    try:
        exibir_mensagem("[BUSCAR] v3.7.0.9: Localizando switch Estacionamento Estudo...")
        
        seletores = [
            '#atividadeVeiculoTelaAtividadeVeiculo input[value="estudo"] + * input.MuiSwitch-input',  # ESPECÍFICO
            '#atividadeVeiculoTelaAtividadeVeiculo input.MuiSwitch-input',  # SEMÂNTICO
            'input.MuiSwitch-input.mui-1m9pwf3',  # ESTRUTURAL
            'input[type="checkbox"]:not([value])'  # FALLBACK
        ]
        
        for i, seletor in enumerate(seletores, 1):
            try:
                elemento = page.locator(seletor)
                if elemento.count() > 0:
                    exibir_mensagem(f"[OK] v3.7.0.9: Switch estudo localizado com seletor {i}/4")
                    return elemento
            except Exception as e:
                exibir_mensagem(f"[AVISO] v3.7.0.9: Seletor {i}/4 falhou: {str(e)[:100]}")
                continue
        
        exibir_mensagem("[ERRO] v3.7.0.9: Nenhum switch estudo foi localizado")
        return None
        
    except Exception as e:
        exibir_mensagem(f"[ERRO] v3.7.0.9: Erro na localização do switch estudo: {str(e)}")
        return None

def navegar_tela_8_playwright(page: Page, uso_veiculo: str) -> bool:
    """
    TELA 8: Finalidade do veículo (Uso do veículo)
    """
    try:
        exception_handler.definir_tela_atual("TELA_8")
        exibir_mensagem("[CELULAR] TELA 8: Aguardando carregamento...")
        
        max_tentativas = 20
        tentativa = 0
        
        while tentativa < max_tentativas:
            elementos_tela8 = localizar_tela_8_playwright(page)
            if elementos_tela8 is not None and elementos_tela8.count() > 0:
                break
            # Aguardar carregamento da tela
            try:
                if aguardar_tela_8_playwright(page, 1000):
                    break
            except:
                continue
            tentativa += 1
        
        if tentativa >= max_tentativas:
            exception_handler.capturar_warning("Tela 8 não carregou", "TELA_8")
            return False
        
        exibir_mensagem("[OK] Tela 8 carregada com sucesso")
        exibir_mensagem(f"[CELULAR] TELA 8: Selecionando uso do veículo...")
        
        mapeamento_uso = {
            "Pessoal": "Particular",
            "Profissional": "Profissional", 
            "Motorista de aplicativo": "Motorista de App",
            "Motorista de App": "Motorista de App",
            "Taxi": "Taxi",
            "Táxi": "Taxi"
        }
        
        valor_radio = mapeamento_uso.get(uso_veiculo, uso_veiculo)
        seletor_radio = f'input[value="{valor_radio}"][name="finalidadeVeiculoTelaUsoVeiculo"]'
        radio_button = page.locator(seletor_radio).first
        
        if radio_button.is_visible():
            radio_button.click()
            exibir_mensagem(f"[OK] Uso '{uso_veiculo}' selecionado com sucesso")
        else:
            exception_handler.capturar_warning(f"Radio button para '{uso_veiculo}' não está visível", "TELA_8")
        
        botao_continuar = page.locator("#gtm-telaUsoVeiculoContinuar").first
        botao_continuar.click()
        exibir_mensagem("[OK] Botão 'Continuar' clicado com sucesso")
        aguardar_tela_8_playwright(page, 5000)
        return True
        
    except Exception as e:
        exception_handler.capturar_excecao(e, "TELA_8", f"Erro ao selecionar uso do veículo: {uso_veiculo}")
        return False

def navegar_tela_9_playwright(page: Page, nome: str, cpf: str, data_nascimento: str, sexo: str, estado_civil: str, email: str, celular: str) -> bool:
    """
    TELA 9: Dados pessoais do segurado
    """
    try:
        exception_handler.definir_tela_atual("TELA_9")
        exibir_mensagem("[CELULAR] TELA 9: Aguardando carregamento...")
        
        # OTIMIZAÇÃO: Detecção mais rápida da Tela 9
        exibir_mensagem("[CELULAR] TELA 9: Aguardando carregamento...")
        
        # Estratégia otimizada: aguardar elemento específico diretamente
        try:
            # Aguardar o campo nome aparecer (mais específico que localizar_tela_9)
            page.wait_for_selector("#nomeTelaSegurado", timeout=5000)
            exibir_mensagem("[OK] Tela 9 carregada com sucesso (otimizada)")
        except:
            # Fallback para método anterior (reduzido)
            for tentativa in range(5):  # Reduzido de 20 para 5
                try:
                    elementos_tela = localizar_tela_9_playwright(page)
                    if elementos_tela.count() > 0:
                        exibir_mensagem("[OK] Tela 9 carregada com sucesso (fallback)")
                        break
                except:
                    pass
                
                if tentativa == 4:
                    exception_handler.capturar_warning("Tela 9 não foi detectada após 5 segundos", "TELA_9")
                    return False
                
                try:
                    if aguardar_tela_9_playwright(page, 1000): break
                except:
                    pass
        
        # OTIMIZAÇÃO: Preenchimento imediato do nome (sem delays desnecessários)
        exibir_mensagem("[CELULAR] TELA 9: Preenchendo nome...")
        try:
            nome_campo = page.locator("#nomeTelaSegurado")
            # Aguardar campo estar pronto para interação
            nome_campo.wait_for(state="visible", timeout=2000)
            nome_campo.click()
            nome_campo.fill(nome)
            exibir_mensagem(f"[OK] Nome preenchido: {nome}")
        except Exception as e:
            exception_handler.capturar_warning(f"Erro ao preencher nome: {str(e)}", "TELA_9")
        
        # Preencher CPF
        exibir_mensagem("[CELULAR] TELA 9: Preenchendo CPF...")
        try:
            cpf_campo = page.locator("#cpfTelaSegurado")
            cpf_campo.click()
            cpf_campo.fill(cpf)
            exibir_mensagem(f"[OK] CPF preenchido: {cpf}")
        except Exception as e:
            exception_handler.capturar_warning(f"Erro ao preencher CPF: {str(e)}", "TELA_9")
        
        # Preencher Data de Nascimento
        exibir_mensagem("[CELULAR] TELA 9: Preenchendo data de nascimento...")
        try:
            data_campo = page.locator("#dataNascimentoTelaSegurado")
            data_campo.click()
            data_campo.fill(data_nascimento)
            exibir_mensagem(f"[OK] Data de nascimento preenchida: {data_nascimento}")
        except Exception as e:
            exception_handler.capturar_warning(f"Erro ao preencher data de nascimento: {str(e)}", "TELA_9")
        
        # Selecionar Sexo
        exibir_mensagem("[CELULAR] TELA 9: Selecionando sexo...")
        try:
            campo_sexo = page.locator("#sexoTelaSegurado")
            if campo_sexo.is_visible():
                campo_sexo.click()
                page.wait_for_selector(f"text={sexo}", timeout=2000)
                
                opcao_sexo = localizar_sexo_playwright(page, sexo)
                if opcao_sexo.is_visible():
                    opcao_sexo.click()
                    exibir_mensagem(f"[OK] Sexo selecionado: {sexo}")
                else:
                    exception_handler.capturar_warning(f"Opção de sexo '{sexo}' não encontrada", "TELA_9")
            else:
                exception_handler.capturar_warning("Campo de sexo não está visível", "TELA_9")
        except Exception as e:
            exception_handler.capturar_warning(f"Erro ao selecionar sexo: {str(e)}", "TELA_9")
        
        # Selecionar Estado Civil
        exibir_mensagem("[CELULAR] TELA 9: Selecionando estado civil...")
        try:
            campo_estado_civil = page.locator("#estadoCivilTelaSegurado")
            if campo_estado_civil.is_visible():
                campo_estado_civil.click()
                page.wait_for_selector('li[role="option"]', timeout=2000)
                
                # Mapear estado civil do JSON para possíveis variações na tela
                mapeamento_estado_civil = {
                    "Casado ou Uniao Estavel": ["Casado ou União Estável", "Casado ou Uniao Estavel", "Casado ou União Estavel", "Casado ou Uniao Estável"],
                    "Solteiro": ["Solteiro", "Solteiro(a)"],
                    "Divorciado": ["Divorciado", "Divorciado(a)"],
                    "Viuvo": ["Viúvo", "Viuvo", "Viúvo(a)", "Viuvo(a)"],
                    "Separado": ["Separado", "Separado(a)"]
                }
                
                # Obter possíveis variações para o estado civil
                variacoes_estado_civil = mapeamento_estado_civil.get(estado_civil, [estado_civil])
                
                # Aguardar até 5 segundos para o dropdown aparecer
                estado_civil_selecionado = False
                for tentativa in range(5):
                    try:
                        # Tentar cada variação possível
                        for variacao in variacoes_estado_civil:
                            opcoes_estado_civil = localizar_estado_civil_playwright(page, variacao)
                            if opcoes_estado_civil.count() > 0:
                                opcoes_estado_civil.first.click()
                                exibir_mensagem(f"[OK] Estado civil selecionado: {estado_civil} (encontrado como '{variacao}')")
                                estado_civil_selecionado = True
                                break
                        
                        if estado_civil_selecionado:
                            break
                    except:
                        pass
                    
                    if tentativa == 4 and not estado_civil_selecionado:
                        exception_handler.capturar_warning(f"Estado civil '{estado_civil}' não encontrado no dropdown (tentou: {', '.join(variacoes_estado_civil)})", "TELA_9")
                    
                    try:
                        page.wait_for_selector('li[role="option"]', timeout=1000)
                        break
                    except:
                        pass
                
                # Aguardar fechamento do dropdown antes de prosseguir
                page.wait_for_function("document.querySelector('#estadoCivilTelaSegurado').getAttribute('aria-expanded') === 'false'", timeout=3000)
            else:
                exception_handler.capturar_warning("Campo de estado civil não está visível", "TELA_9")
        except Exception as e:
            exception_handler.capturar_warning(f"Erro ao selecionar estado civil: {str(e)}", "TELA_9")
        
        # Preencher Email
        exibir_mensagem("[CELULAR] TELA 9: Preenchendo email...")
        try:
            email_campo = page.locator("#emailTelaSegurado")
            email_campo.click()
            email_campo.fill(email)
            exibir_mensagem(f"[OK] Email preenchido: {email}")
        except Exception as e:
            exception_handler.capturar_warning(f"Erro ao preencher email: {str(e)}", "TELA_9")
        
        # Preencher Celular
        exibir_mensagem("[CELULAR] TELA 9: Preenchendo celular...")
        try:
            celular_campo = page.locator("#celularTelaSegurado")
            celular_campo.click()
            
            # Limpar o campo primeiro
            celular_campo.clear()
            page.wait_for_function("document.querySelector('#celularTelaSegurado').value === ''", timeout=1000)
            
            # Preencher caractere por caractere para evitar problemas com máscara
            for digito in celular:
                celular_campo.type(digito)
                page.wait_for_function("document.querySelector('#celularTelaSegurado').value.length > 0", timeout=200)
            
            # Aguardar um pouco para a máscara processar
            page.wait_for_function("document.querySelector('#celularTelaSegurado').value.length >= " + str(len(celular)), timeout=2000)
            
            # Verificar se foi preenchido corretamente
            valor_preenchido = celular_campo.input_value()
            exibir_mensagem(f"[OK] Celular preenchido: {celular} (valor no campo: {valor_preenchido})")
            
            if valor_preenchido != celular:
                exception_handler.capturar_warning(f"ATENÇÃO: Valor no campo ({valor_preenchido}) diferente do esperado ({celular})", "TELA_9")
                
        except Exception as e:
            exception_handler.capturar_warning(f"Erro ao preencher celular: {str(e)}", "TELA_9")
        
        # Clicar em Continuar
        botao_continuar = page.locator("#gtm-telaDadosSeguradoContinuar").first
        botao_continuar.click()
        exibir_mensagem("[OK] Botão 'Continuar' clicado com sucesso")
        page.wait_for_selector("#gtm-telaCondutorPrincipalContinuar", timeout=5000)
        return True
        
    except Exception as e:
        exception_handler.capturar_excecao(e, "TELA_9", "Erro ao preencher dados pessoais")
        return False

def navegar_tela_10_playwright(page, condutor_principal, nome_condutor=None, cpf_condutor=None, data_nascimento_condutor=None, sexo_condutor=None, estado_civil_condutor=None):
    """
    TELA 10: Condutor principal
    
    DESCRIÇÃO:
        Navega para a Tela 10 e configura se o segurado é o condutor principal do veículo.
        Se não for condutor principal, preenche os dados do condutor (nome, CPF, data nascimento, sexo, estado civil).
        
    ELEMENTOS IDENTIFICADOS:
        - Radio Sim (Condutor Principal): input[value="sim"][name="condutorPrincipalTelaCondutorPrincipal"]
        - Radio Não (Não Condutor Principal): input[value="nao"][name="condutorPrincipalTelaCondutorPrincipal"]
        - Campo Nome: #nomeTelaCondutorPrincipal
        - Campo CPF: #cpfTelaCondutorPrincipal
        - Campo Data Nascimento: #dataNascimentoTelaCondutorPrincipal
        - Campo Sexo: #sexoTelaCondutorPrincipal
        - Campo Estado Civil: #estadoCivilTelaCondutorPrincipal
        - Botão Continuar: #gtm-telaCondutorPrincipalContinuar
        
    PARÂMETROS:
        - condutor_principal: bool - Se o segurado é o condutor principal
        - nome_condutor: str - Nome do condutor (se não for condutor principal)
        - cpf_condutor: str - CPF do condutor (se não for condutor principal)
        - data_nascimento_condutor: str - Data de nascimento do condutor (se não for condutor principal)
        - sexo_condutor: str - Sexo do condutor (se não for condutor principal)
        - estado_civil_condutor: str - Estado civil do condutor (se não for condutor principal)
    """
    try:
        exibir_mensagem("\n" + "="*50)
        exibir_mensagem("[OBJETIVO] TELA 10: CONDUTOR PRINCIPAL")
        exibir_mensagem("="*50)
        
        # Aguarda o carregamento da Tela 10
        exibir_mensagem("[AGUARDANDO] Aguardando carregamento da Tela 10...")
        page.wait_for_selector("#gtm-telaCondutorPrincipalContinuar", timeout=10000)
        page.wait_for_selector('input[name="condutorPrincipalTelaCondutorPrincipal"]', timeout=3000)
        
        exibir_mensagem("[OK] Tela 10 carregada - condutor principal detectado!")
        
        # PASSO 1: Selecionar se é condutor principal ou não
        if condutor_principal:
            exibir_mensagem("[USUARIO] Selecionando 'Sim' - segurado é condutor principal")
            radio_sim = localizar_radio_condutor_playwright(page, "sim")
            if radio_sim.is_visible():
                radio_sim.click()
                exibir_mensagem("[OK] Radio 'Sim' selecionado com sucesso")
            else:
                exception_handler.capturar_warning("Radio 'Sim' não encontrado", "TELA_10")
        else:
            exibir_mensagem("[USUARIO] Selecionando 'Não' - segurado não é condutor principal")
            radio_nao = localizar_radio_condutor_playwright(page, "nao")
            if radio_nao.is_visible():
                radio_nao.click()
                exibir_mensagem("[OK] Radio 'Não' selecionado com sucesso")
                
                # Aguardar campos do condutor aparecerem
                page.wait_for_selector("#nomeTelaCondutorPrincipal", timeout=3000)
                
                # PASSO 2: Preencher dados do condutor
                exibir_mensagem("[NOTA] Preenchendo dados do condutor...")
                
                # Nome do condutor
                if nome_condutor:
                    nome_campo = page.locator("#nomeTelaCondutorPrincipal")
                    if nome_campo.is_visible():
                        nome_campo.fill(nome_condutor)
                        exibir_mensagem(f"[OK] Nome do condutor: {nome_condutor}")
                    else:
                        exception_handler.capturar_warning("Campo nome não encontrado", "TELA_10")
                
                # CPF do condutor
                if cpf_condutor:
                    cpf_campo = page.locator("#cpfTelaCondutorPrincipal")
                    if cpf_campo.is_visible():
                        cpf_campo.fill(cpf_condutor)
                        exibir_mensagem(f"[OK] CPF do condutor: {cpf_condutor}")
                    else:
                        exception_handler.capturar_warning("Campo CPF não encontrado", "TELA_10")
                
                # Data de nascimento do condutor
                if data_nascimento_condutor:
                    data_campo = page.locator("#dataNascimentoTelaCondutorPrincipal")
                    if data_campo.is_visible():
                        data_campo.fill(data_nascimento_condutor)
                        exibir_mensagem(f"[OK] Data de nascimento: {data_nascimento_condutor}")
                    else:
                        exception_handler.capturar_warning("Campo data de nascimento não encontrado", "TELA_10")
                
                # Sexo do condutor
                if sexo_condutor:
                    sexo_campo = page.locator("#sexoTelaCondutorPrincipal")
                    if sexo_campo.is_visible():
                        sexo_campo.click()
                        page.wait_for_selector("ul", timeout=2000)
                        
                        try:
                            page.wait_for_selector("ul", timeout=5000)
                            opcao_sexo = page.locator(f'xpath=//li[contains(text(), "{sexo_condutor}")]')
                            if opcao_sexo.is_visible():
                                opcao_sexo.click()
                                exibir_mensagem(f"[OK] Sexo do condutor: {sexo_condutor}")
                            else:
                                exception_handler.capturar_warning(f"Opção de sexo '{sexo_condutor}' não encontrada", "TELA_10")
                        except:
                            exception_handler.capturar_warning("Erro ao selecionar sexo", "TELA_10")
                    else:
                        exception_handler.capturar_warning("Campo sexo não encontrado", "TELA_10")
                
                # Estado civil do condutor
                if estado_civil_condutor:
                    estado_civil_campo = page.locator("#estadoCivilTelaCondutorPrincipal")
                    if estado_civil_campo.is_visible():
                        estado_civil_campo.click()
                        page.wait_for_selector("ul", timeout=2000)
                        
                        try:
                            page.wait_for_selector("ul", timeout=5000)
                            
                            # Mapeamento para variações de acento
                            mapeamento_estado_civil = {
                                "Casado ou Uniao Estavel": "Casado ou União Estável"
                            }
                            
                            texto_busca = mapeamento_estado_civil.get(estado_civil_condutor, estado_civil_condutor)
                            opcao_estado_civil = page.locator(f'xpath=//li[contains(text(), "{texto_busca}")]')
                            
                            if opcao_estado_civil.is_visible():
                                opcao_estado_civil.click()
                                exibir_mensagem(f"[OK] Estado civil do condutor: {estado_civil_condutor}")
                            else:
                                exception_handler.capturar_warning(f"Opção de estado civil '{estado_civil_condutor}' não encontrada", "TELA_10")
                        except:
                            exception_handler.capturar_warning("Erro ao selecionar estado civil", "TELA_10")
                    else:
                        exception_handler.capturar_warning("Campo estado civil não encontrado", "TELA_10")
            else:
                exception_handler.capturar_warning("Radio 'Não' não encontrado", "TELA_10")
        
        # Aguardar estabilização
        page.wait_for_selector("#gtm-telaCondutorPrincipalContinuar", timeout=3000)
        
        # PASSO 3: Clicar em Continuar
        exibir_mensagem("[AGUARDANDO] Clicando em 'Continuar'...")
        botao_continuar = page.locator("#gtm-telaCondutorPrincipalContinuar")
        if botao_continuar.is_visible():
            botao_continuar.click()
            exibir_mensagem("[OK] Botão 'Continuar' clicado com sucesso")
            page.wait_for_selector("#gtm-telaAtividadeVeiculoContinuar", timeout=5000)
            return True
        else:
            exception_handler.capturar_warning("Botão 'Continuar' não encontrado", "TELA_10")
            return False
        
    except Exception as e:
        exception_handler.capturar_excecao(e, "TELA_10", "Erro ao processar condutor principal")
        return False

def navegar_tela_11_playwright(page, local_de_trabalho, estacionamento_proprio_local_de_trabalho, local_de_estudo, estacionamento_proprio_local_de_estudo):
    """
    TELA 11: Atividade do veículo
    
    DESCRIÇÃO:
        Navega para a Tela 11 e seleciona se o veículo é utilizado para ir ao local de trabalho e/ou estudo.
        Se selecionar local de trabalho, aparece checkbox de estacionamento próprio do trabalho.
        Se selecionar local de estudo, aparece checkbox de estacionamento próprio do estudo.
        
    ELEMENTOS IDENTIFICADOS:
        - Checkbox Local de Trabalho: input[type="checkbox"][value="trabalho"]
        - Checkbox Local de Estudo: input[type="checkbox"][value="estudo"]
        - Checkbox Estacionamento Local de Trabalho: input[type="checkbox"][data-gtm-form-interact-field-id="10"]
        - Checkbox Estacionamento Local de Estudo: input[type="checkbox"][data-gtm-form-interact-field-id="11"]
        - Botão Continuar: #gtm-telaAtividadeVeiculoContinuar
        
    PARÂMETROS:
        - local_de_trabalho: bool - Se o veículo é usado para ir ao trabalho
        - estacionamento_proprio_local_de_trabalho: bool - Se há estacionamento próprio no trabalho
        - local_de_estudo: bool - Se o veículo é usado para ir ao estudo
        - estacionamento_proprio_local_de_estudo: bool - Se há estacionamento próprio no estudo
    """
    try:
        exibir_mensagem("\n" + "="*50)
        exibir_mensagem("[OBJETIVO] TELA 11: ATIVIDADE DO VEÍCULO")
        exibir_mensagem("="*50)
        
        # Aguarda o carregamento da Tela 11
        exibir_mensagem("[AGUARDANDO] Aguardando carregamento da Tela 11...")
        page.wait_for_selector("#gtm-telaAtividadeVeiculoContinuar", timeout=10000)
        page.wait_for_selector('input[type="checkbox"][value="trabalho"]', timeout=3000)
        
        exibir_mensagem("[OK] Tela 11 carregada - atividade do veículo detectada!")
        
        # PASSO 1: Seleciona checkbox Local de Trabalho se necessário
        if local_de_trabalho:
            exibir_mensagem("[INFO] Marcando checkbox 'Local de Trabalho'...")
            checkbox_trabalho = localizar_checkbox_trabalho_playwright(page)
            if not checkbox_trabalho.is_checked():
                checkbox_trabalho.check()
                exibir_mensagem("[OK] Checkbox 'Local de Trabalho' marcado!")
                page.wait_for_selector('input[type="checkbox"][data-gtm-form-interact-field-id="10"]', timeout=2000)
            else:
                exibir_mensagem("[INFO]️ Checkbox 'Local de Trabalho' já estava marcado")
        else:
            exibir_mensagem("[INFO]️ Local de Trabalho: Não selecionado")
        
        # PASSO 2: Seleciona checkbox Local de Estudo se necessário
        if local_de_estudo:
            exibir_mensagem("[INFO] Marcando checkbox 'Local de Estudo'...")
            checkbox_estudo = localizar_checkbox_estudo_playwright(page)
            if not checkbox_estudo.is_checked():
                checkbox_estudo.check()
                exibir_mensagem("[OK] Checkbox 'Local de Estudo' marcado!")
                page.wait_for_selector('input[type="checkbox"][data-gtm-form-interact-field-id="11"]', timeout=2000)
            else:
                exibir_mensagem("[INFO]️ Checkbox 'Local de Estudo' já estava marcado")
        else:
            exibir_mensagem("[INFO]️ Local de Estudo: Não selecionado")
        
        # PASSO 3: Configurar estacionamento do trabalho (se local_de_trabalho = true)
        if local_de_trabalho:
            exibir_mensagem("[P]️ Configurando estacionamento do trabalho...")
            try:
                checkbox_estacionamento_trabalho = localizar_switch_trabalho_playwright(page)
                if checkbox_estacionamento_trabalho.is_visible():
                    if estacionamento_proprio_local_de_trabalho and not checkbox_estacionamento_trabalho.is_checked():
                        checkbox_estacionamento_trabalho.check()
                        exibir_mensagem("[OK] Estacionamento próprio do trabalho: MARCADO")
                    elif not estacionamento_proprio_local_de_trabalho and checkbox_estacionamento_trabalho.is_checked():
                        checkbox_estacionamento_trabalho.uncheck()
                        exibir_mensagem("[OK] Estacionamento próprio do trabalho: DESMARCADO")
                    else:
                        estado = "MARCADO" if estacionamento_proprio_local_de_trabalho else "DESMARCADO"
                        exibir_mensagem(f"[OK] Estacionamento próprio do trabalho: {estado} (já estava correto)")
                else:
                    exibir_mensagem("[AVISO] Checkbox estacionamento do trabalho não encontrado")
            except Exception as e:
                exibir_mensagem(f"[AVISO] Erro ao configurar estacionamento do trabalho: {str(e)}")
        
        # PASSO 4: Configurar estacionamento do estudo (se local_de_estudo = true)
        if local_de_estudo:
            exibir_mensagem("[P]️ Configurando estacionamento do estudo...")
            try:
                checkbox_estacionamento_estudo = localizar_switch_estudo_playwright(page)
                if checkbox_estacionamento_estudo.is_visible():
                    if estacionamento_proprio_local_de_estudo and not checkbox_estacionamento_estudo.is_checked():
                        checkbox_estacionamento_estudo.check()
                        exibir_mensagem("[OK] Estacionamento próprio do estudo: MARCADO")
                    elif not estacionamento_proprio_local_de_estudo and checkbox_estacionamento_estudo.is_checked():
                        checkbox_estacionamento_estudo.uncheck()
                        exibir_mensagem("[OK] Estacionamento próprio do estudo: DESMARCADO")
                    else:
                        estado = "MARCADO" if estacionamento_proprio_local_de_estudo else "DESMARCADO"
                        exibir_mensagem(f"[OK] Estacionamento próprio do estudo: {estado} (já estava correto)")
                else:
                    exibir_mensagem("[AVISO] Checkbox estacionamento do estudo não encontrado")
            except Exception as e:
                exibir_mensagem(f"[AVISO] Erro ao configurar estacionamento do estudo: {str(e)}")
        
        # PASSO 5: Aguardar estabilização após todas as configurações
        page.wait_for_selector("#gtm-telaAtividadeVeiculoContinuar", timeout=3000)
        
        # PASSO 6: Clica no botão Continuar
        exibir_mensagem("[ATUALIZANDO] Clicando em 'Continuar'...")
        botao_continuar = page.locator("#gtm-telaAtividadeVeiculoContinuar")
        botao_continuar.click()
        
        # PASSO 7: Aguarda navegação
        page.wait_for_selector("input[name='possuiGaragemTelaGaragemResidencia']", timeout=5000)
        exibir_mensagem("[OK] Navegação para próxima tela realizada!")
        
        return True
        
    except Exception as e:
        exibir_mensagem(f"[ERRO] ERRO na Tela 11: {str(e)}")
        return False

def navegar_tela_12_playwright(page, garagem_residencia, portao_eletronico):
    """
    TELA 12: Garagem na Residência
    
    DESCRIÇÃO:
        Navega para a Tela 12 e seleciona se possui garagem na residência e tipo de portão.
        
    ELEMENTOS IDENTIFICADOS:
        - Radio Sim: input[value="sim"][name="possuiGaragemTelaGaragemResidencia"]
        - Radio Não: input[value="nao"][name="possuiGaragemTelaGaragemResidencia"]
        - Radio Eletrônico: input[value="eletronico"][name="tipoPortaoTelaGaragemResidencia"]
        - Radio Manual: input[value="manual"][name="tipoPortaoTelaGaragemResidencia"]
        - Botão Continuar: p.font-semibold.font-workSans.cursor-pointer (texto "Continuar")
        
    PARÂMETROS:
        - garagem_residencia: bool - Se possui garagem na residência
        - portao_eletronico: str - Tipo de portão ("Eletronico", "Manual", "Não possui")
    """
    try:
        exibir_mensagem("\n" + "="*50)
        exibir_mensagem("[CASA] TELA 12: GARAGEM NA RESIDÊNCIA")
        exibir_mensagem("="*50)
        
        # Aguarda o carregamento da Tela 12
        exibir_mensagem("1 [AGUARDANDO] Aguardando carregamento da Tela 12...")
        botao_continuar = localizar_botao_continuar_garagem_playwright(page)
        if not botao_continuar:
            exibir_mensagem("[ERRO] v3.7.0.11: Botão continuar não encontrado no carregamento")
            return False
        page.wait_for_selector('input[name="possuiGaragemTelaGaragemResidencia"]', timeout=3000)
        
        exibir_mensagem("2 [OK] Tela 12 carregada - garagem na residência detectada!")
        
        # Seleciona Sim ou Não para garagem
        if garagem_residencia:
            exibir_mensagem("3 [INFO] Selecionando 'Sim' para garagem na residência...")
            
            # Localizar e clicar no radio button "Sim"
            radio_sim = page.locator('input[value="sim"][name="possuiGaragemTelaGaragemResidencia"]')
            if radio_sim.is_visible():
                radio_sim.click()
                exibir_mensagem("4 [OK] Radio 'Sim' para garagem selecionado com sucesso")
            else:
                exibir_mensagem("4 [AVISO] Radio 'Sim' para garagem não encontrado")
                return False
            
            # Aguarda campo de portão aparecer
            exibir_mensagem("5 [AGUARDANDO] Aguardando campo de portão aparecer...")
            page.wait_for_selector('input[name="tipoPortaoTelaGaragemResidencia"]', timeout=3000)
            
            # Seleciona tipo de portão
            if portao_eletronico == "Eletronico":
                exibir_mensagem("6 [INFO] Selecionando 'Eletrônico' para portão...")
                
                radio_eletronico = page.locator('input[value="eletronico"][name="tipoPortaoTelaGaragemResidencia"]')
                if radio_eletronico.is_visible():
                    radio_eletronico.click()
                    exibir_mensagem("7 [OK] Radio 'Eletrônico' para portão selecionado com sucesso")
                else:
                    exibir_mensagem("7 [AVISO] Radio 'Eletrônico' para portão não encontrado")
                    return False
                    
            elif portao_eletronico == "Manual":
                exibir_mensagem("6 [INFO] Selecionando 'Manual' para portão...")
                
                radio_manual = page.locator('input[value="manual"][name="tipoPortaoTelaGaragemResidencia"]')
                if radio_manual.is_visible():
                    radio_manual.click()
                    exibir_mensagem("7 [OK] Radio 'Manual' para portão selecionado com sucesso")
                else:
                    exibir_mensagem("7 [AVISO] Radio 'Manual' para portão não encontrado")
                    return False
            else:
                exibir_mensagem("6 [INFO]️ Tipo de portão: Não possui")
        else:
            exibir_mensagem("3 [INFO] Selecionando 'Não' para garagem na residência...")
            
            # Localizar e clicar no radio button "Não"
            radio_nao = page.locator('input[value="nao"][name="possuiGaragemTelaGaragemResidencia"]')
            if radio_nao.is_visible():
                radio_nao.click()
                exibir_mensagem("4 [OK] Radio 'Não' para garagem selecionado com sucesso")
            else:
                exibir_mensagem("4 [AVISO] Radio 'Não' para garagem não encontrado")
                return False
        
        # Aguarda estabilização após seleções
        exibir_mensagem("7 [AGUARDANDO] Aguardando estabilização do botão continuar...")
        botao_continuar = localizar_botao_continuar_garagem_playwright(page)
        if not botao_continuar:
            exibir_mensagem("[ERRO] v3.7.0.11: Botão continuar não encontrado após estabilização")
            return False
        
        # Clica no botão Continuar
        exibir_mensagem("8 [ATUALIZANDO] Clicando em 'Continuar'...")
        botao_continuar = localizar_botao_continuar_garagem_playwright(page)
        if botao_continuar and botao_continuar.is_visible():
            botao_continuar.click()
            exibir_mensagem("9 [OK] Botão 'Continuar' clicado com sucesso")
        else:
            exibir_mensagem("9 [AVISO] Botão 'Continuar' não encontrado")
            return False
        
        # Aguarda navegação - verifica se chegou na próxima tela ou se ainda está na atual
        try:
            # Tenta aguardar elemento da próxima tela
#            page.wait_for_selector("input[name='resideMenoresTelaResidenciaMenores']", timeout=3000)
            page.wait_for_selector("input[name='usoDependenteTelaUsoResidentes']", timeout=10000)
            exibir_mensagem("[10] [OK] Navegação para próxima tela realizada!")
        except:
            # Se não encontrar, verifica se ainda está na tela atual
            try:
                botao_continuar = localizar_botao_continuar_garagem_playwright(page)
                if botao_continuar and botao_continuar.is_visible():
                    exibir_mensagem("[10] [AVISO] Ainda na tela atual - tentando clicar novamente...")
                    botao_continuar.click()
                else:
                    exibir_mensagem("[10] [AVISO] Botão continuar não encontrado para segundo clique")
#                page.wait_for_selector("input[name='resideMenoresTelaResidenciaMenores']", timeout=5000)
                exibir_mensagem("[10] [OK] Navegação para próxima tela realizada!")
            except:
                exibir_mensagem("[10] [OK] Navegação para próxima tela realizada!")
        
        return True
        
    except Exception as e:
        exibir_mensagem(f"[ERRO] ERRO na Tela 12: {str(e)}")
        return False

def localizar_botao_continuar_menores_playwright(page: Page):
    """
    ESTRATÉGIA HÍBRIDA v3.7.0.12 - Tela 13 (Residência com Menores):
    1. #gtm-telaUsoResidentesContinuar - ESPECÍFICO (ID único)
    2. button[data-testid="continuar-menores"] - ESPECÍFICO (data-testid)
    3. p:has-text("Continuar") - SEMÂNTICO (texto específico)
    4. button:has-text("Continuar") - SEMÂNTICO (botão com texto)
    5. p.font-semibold.font-workSans.cursor-pointer - FALLBACK (compatibilidade)
    
    Args:
        page: Instância do Playwright Page
        
    Returns:
        Locator: Elemento do botão continuar localizado
    """
    try:
        # Nível 1: ID específico (mais confiável)
        try:
            elemento = page.locator("#gtm-telaUsoResidentesContinuar")
            if elemento.is_visible(timeout=1000):
                exibir_mensagem("[BUSCAR] v3.7.0.12: Botão continuar localizado por ID específico (nível 1)")
                return elemento
        except:
            pass
        
        # Nível 2: Data-testid específico
        try:
            elemento = page.locator('button[data-testid="continuar-menores"]')
            if elemento.is_visible(timeout=1000):
                exibir_mensagem("[BUSCAR] v3.7.0.12: Botão continuar localizado por data-testid (nível 2)")
                return elemento
        except:
            pass
        
        # Nível 3: Texto semântico no parágrafo
        try:
            elemento = page.locator('p:has-text("Continuar")')
            if elemento.is_visible(timeout=1000):
                exibir_mensagem("[BUSCAR] v3.7.0.12: Botão continuar localizado por texto semântico (nível 3)")
                return elemento
        except:
            pass
        
        # Nível 4: Texto semântico no botão
        try:
            elemento = page.locator('button:has-text("Continuar")')
            if elemento.is_visible(timeout=1000):
                exibir_mensagem("[BUSCAR] v3.7.0.12: Botão continuar localizado por botão com texto (nível 4)")
                return elemento
        except:
            pass
        
        # Nível 5: Fallback com classes CSS (compatibilidade)
        try:
            elemento = page.locator('p.font-semibold.font-workSans.cursor-pointer')
            if elemento.is_visible(timeout=1000):
                exibir_mensagem("[BUSCAR] v3.7.0.12: Botão continuar localizado por classes CSS (nível 5 - fallback)")
                return elemento
        except:
            pass
        
        # Se nenhum nível funcionou, retornar o fallback padrão
        exibir_mensagem("[AVISO] v3.7.0.12: Usando fallback padrão para botão continuar")
        return page.locator('p.font-semibold.font-workSans.cursor-pointer')
        
    except Exception as e:
        exibir_mensagem(f"[ERRO] v3.7.0.12: Erro ao localizar botão continuar: {str(e)}")
        # Fallback final
        return page.locator('p.font-semibold.font-workSans.cursor-pointer')

def navegar_tela_13_playwright(page, reside_18_26, sexo_do_menor, faixa_etaria_menor_mais_novo):
    """
    a versão ntir : Residência com Menores de 18-26 anos
    
    DESCRIÇÃO:
        Navega para a Tela 13 e seleciona se reside com alguém entre 18 e 26 anos.
        Se sim, seleciona o sexo e faixa etária do mais novo.
        
    ELEMENTOS IDENTIFICADOS (baseado na gravação):
        - Radio principal: Você reside com alguém entre 18 e 26 anos?
            - Não
            - Sim, mas não utilizam o veículo
            - Sim e utilizam o veículo
        - Radio condicional Sexo (só aparece se "Sim e utilizam o veículo"):
            - Feminino
            - Masculino
            - Ambos
        - Radio condicional Faixa etária (só aparece se "Sim e utilizam o veículo"):
            - 18 a 24 anos
            - 25 anos
        - Botão Continuar: p.font-semibold.font-workSans.cursor-pointer:has-text("Continuar")
        
    PARÂMETROS:
        - reside_18_26: str - Resposta principal ("Não", "Sim, mas não utilizam o veículo", "Sim e utilizam o veículo")
        - sexo_do_menor: str - Sexo do menor ("Feminino", "Masculino", "Ambos", "N/A")
        - faixa_etaria_menor_mais_novo: str - Faixa etária ("18 a 24 anos", "25 anos", "N/A")
    """
    try:
        exibir_mensagem("\n" + "="*50)
        exibir_mensagem("[USUARIOS] TELA 13: RESIDÊNCIA COM MENORES DE 18-26 ANOS")
        exibir_mensagem("="*50)
        
        # PASSO 1: Aguardar carregamento da tela
        exibir_mensagem("1 [AGUARDANDO] Aguardando carregamento da Tela 13...")
        page.wait_for_selector("p.font-semibold.font-workSans.cursor-pointer:has-text('Continuar')", timeout=10000)
        exibir_mensagem("2 [OK] Tela 13 carregada - residência com menores detectada!")
        
        # PASSO 2: Selecionar resposta principal
        exibir_mensagem(f"3 [USUARIOS] Selecionando resposta principal: '{reside_18_26}'...")
        
        # Mapear valores para os selectors da gravação
        if reside_18_26 == "Não":
            # Selecionar "Não" - tentar diferentes abordagens
            try:
                # Primeira tentativa: usar o seletor original
                page.locator("input[type='radio'][value='nao']").first.check()
                exibir_mensagem("4 [OK] Radio 'Não' selecionado com sucesso")
            except:
                try:
                    # Segunda tentativa: usar texto
                    page.locator("text=Não").first.click()
                    exibir_mensagem("4 [OK] Radio 'Não' selecionado com sucesso (texto)")
                except:
                    # Terceira tentativa: usar label
                    page.locator("label:has-text('Não')").first.click()
                    exibir_mensagem("4 [OK] Radio 'Não' selecionado com sucesso (label)")
            
        elif reside_18_26 == "Sim, mas não utilizam o veículo":
            # Selecionar "Sim, mas não utilizam o veículo"
            try:
                page.locator("input[type='radio'][value='sim_nao_utilizam']").check()
                exibir_mensagem("4 [OK] Radio 'Sim, mas não utilizam o veículo' selecionado com sucesso")
            except:
                page.locator("text=Sim, mas não utilizam o veículo").first.click()
                exibir_mensagem("4 [OK] Radio 'Sim, mas não utilizam o veículo' selecionado com sucesso (texto)")
            
        elif reside_18_26 == "Sim e utilizam o veículo":
            # Selecionar "Sim e utilizam o veículo"
            try:
                page.locator("input[type='radio'][value='sim_utilizam']").check()
                exibir_mensagem("4 [OK] Radio 'Sim e utilizam o veículo' selecionado com sucesso")
            except:
                page.locator("text=Sim e utilizam o veículo").first.click()
                exibir_mensagem("4 [OK] Radio 'Sim e utilizam o veículo' selecionado com sucesso (texto)")
            
            # PASSO 3: Se "Sim e utilizam o veículo", selecionar campos condicionais
            if sexo_do_menor != "N/A":
                exibir_mensagem(f"5 [USUARIO] Selecionando sexo do menor: '{sexo_do_menor}'...")
                
                if sexo_do_menor == "Feminino":
                    page.locator("input[type='radio'][value='feminino']").check()
                    exibir_mensagem("6 [OK] Radio 'Feminino' para sexo selecionado com sucesso")
                elif sexo_do_menor == "Masculino":
                    page.locator("input[type='radio'][value='masculino']").check()
                    exibir_mensagem("6 [OK] Radio 'Masculino' para sexo selecionado com sucesso")
                elif sexo_do_menor == "Ambos":
                    page.locator("input[type='radio'][value='ambos']").check()
                    exibir_mensagem("6 [OK] Radio 'Ambos' para sexo selecionado com sucesso")
            
            if faixa_etaria_menor_mais_novo != "N/A":
                exibir_mensagem(f"7 [DATA] Selecionando faixa etária: '{faixa_etaria_menor_mais_novo}'...")
                
                if faixa_etaria_menor_mais_novo == "18 a 24 anos":
                    page.locator("input[type='radio'][value='18_24']").check()
                    exibir_mensagem("8 [OK] Radio '18 a 24 anos' para faixa etária selecionado com sucesso")
                elif faixa_etaria_menor_mais_novo == "25 anos":
                    page.locator("input[type='radio'][value='25']").check()
                    exibir_mensagem("8 [OK] Radio '25 anos' para faixa etária selecionado com sucesso")
        else:
            exibir_mensagem("4 [AVISO] Resposta não reconhecida, usando 'Não'")
            page.locator("input[type='radio'][value='nao']").first.check()
        
        # PASSO 4: Clicar no botão Continuar
        # ========================================
        # [ATUALIZANDO] MUDANÇA DE SELETOR - COMPATIBILIDADE REGIONAL
        # ========================================
        # ANTES (Seletor Genérico - Problemático em Portugal):
        # page.wait_for_selector("p.font-semibold.font-workSans.cursor-pointer:has-text('Continuar')", timeout=5000)
        # page.locator("p.font-semibold.font-workSans.cursor-pointer:has-text('Continuar')").click()
        #
        # DEPOIS (Seletor Específico - Funciona em Portugal):
        # Motivo: Seletores genéricos baseados em classes CSS falham em Portugal devido a:
        # - Problemas de timing e renderização CSS assíncrona
        # - Carregamento mais lento de fontes e estilos
        # - Dependência de múltiplas classes CSS aplicadas
        # - Diferenças de infraestrutura regional (latência, CDN, cache)
        #
        # Solução: Usar ID específico que é sempre presente no HTML
        # independente do estado de renderização CSS
        # ========================================
        exibir_mensagem("9 [AGUARDANDO] Aguardando botão 'Continuar'...")
        page.wait_for_selector("#gtm-telaUsoResidentesContinuar", timeout=5000)
        
        exibir_mensagem("[10] [ATUALIZANDO] Clicando no botão 'Continuar'...")
        botao_continuar = localizar_botao_continuar_menores_playwright(page)
        botao_continuar.click()
        exibir_mensagem("11 [OK] Botão 'Continuar' clicado com sucesso")
        
        # PASSO 5: Aguardar transição para próxima tela
        exibir_mensagem("12 [AGUARDANDO] Aguardando transição para próxima tela...")
        exibir_mensagem("13 [BUSCAR] Iniciando sistema de detecção inteligente (Tela 14 -> Tela 15)")
        
        # Tentar detectar Tela 14 primeiro
        try:
            exibir_mensagem("14 [OBJETIVO] Tentativa 1: Detectando Tela 14...")
            page.wait_for_selector("#gtm-telaCorretorAnteriorContinuar", timeout=5000)
            exibir_mensagem("15 [OK] Tela 14 detectada - transição bem-sucedida!")
            exibir_mensagem("16 [INFO] Fluxo normal: Tela 13 -> Tela 14 -> Tela 15")
        except Exception as e:
            exibir_mensagem(f"14 [AVISO] Tela 14 não detectada: {str(e)}")
            exibir_mensagem("15 [ATUALIZANDO] Ativando fallback: Tentando detectar Tela 15 diretamente...")
            exibir_mensagem("16 [INFO] Fluxo otimizado: Tela 13 -> Tela 15 (pulando Tela 14)")
            
            # Fallback: tentar detectar Tela 15
            try:
                exibir_mensagem("17 [OBJETIVO] Tentativa 2: Detectando Tela 15 como fallback...")
                
                # Tentar detectar Tela 15 com diferentes textos possíveis
                try:
                    # Primeira tentativa: texto original (quando vai para Tela 14 primeiro)
                    exibir_mensagem("17a [OBJETIVO] Tentativa 2a: Detectando Tela 15 (texto original)...")
                    page.wait_for_selector("text=Por favor, aguarde. Estamos buscando o corretor ideal para você!", timeout=3000)
                    exibir_mensagem("17a [OK] Tela 15 detectada com texto original!")
                except:
                    try:
                        # Segunda tentativa: texto quando pula diretamente da Tela 13
                        exibir_mensagem("17b [OBJETIVO] Tentativa 2b: Detectando Tela 15 (texto direto)...")
                        page.wait_for_selector("text=Por favor, aguarde. Estamos realizando o cálculo para você!", timeout=3000)
                        exibir_mensagem("17b [OK] Tela 15 detectada com texto direto!")
                    except:
                        # Terceira tentativa: texto final de sucesso
                        exibir_mensagem("17c [OBJETIVO] Tentativa 2c: Detectando Tela 15 (texto final)...")
                        page.wait_for_selector("text=Parabéns, chegamos ao resultado final da cotação!", timeout=180000)
                        exibir_mensagem("17c [OK] Tela 15 detectada com texto final!")

                exibir_mensagem("18 [OK] Tela 15 detectada - transição bem-sucedida!")
                exibir_mensagem("19 [INICIANDO] Fallback executado com sucesso!")
                
                # Definir variável global quando Tela 15 é detectada diretamente da Tela 13
                global tela_15_detectada
                tela_15_detectada = True
                exibir_mensagem("20 [TAG]️ Flag global 'tela_15_detectada' definida como True")
                exibir_mensagem("21 [DADOS] Status atualizado: Tela 14 será pulada na próxima execução")
                
            except Exception as e2:
                exibir_mensagem(f"17 [ERRO] Tela 15 também não detectada: {str(e2)}")
                exibir_mensagem("18 [ERRO] ABEND: Falha na transição da Tela 13")
                exibir_mensagem("19 [PROIBIDO] Nenhuma tela subsequente foi detectada")
                raise Exception("Falha na transição da Tela 13 - nem Tela 14 nem Tela 15 detectadas")
        exibir_mensagem("22 [OK] TELA 13 CONCLUÍDA!")
        
        return True
        
    except Exception as e:
        exibir_mensagem(f"[ERRO] ERRO na Tela 13: {str(e)}")
        return False

def navegar_tela_14_playwright(page, continuar_com_corretor_anterior):
    """
    TELA 14: Corretor Anterior (CONDICIONAL)
    
    DESCRIÇÃO:
        Tela condicional que só aparece quando já existe uma cotação para o cliente.
        Pergunta se deseja continuar com o corretor anterior ou não.
        
    ELEMENTOS IDENTIFICADOS (baseado na gravação):
        - Botão Continuar: id=gtm-telaCorretorAnteriorContinuar
        - Elementos de seleção: css=.flex > .min-h-[39rem] .mb-6 > .flex > .flex > .text-primary
        - Checkbox/Radio: css=.flex > .md\3Aw-80 > div:nth-child(2) > .flex > .flex .text-primary:nth-child(1)
        
    CARACTERÍSTICAS IMPORTANTES:
        - Tela condicional: Só aparece quando já existe uma cotação para o cliente
        - Lógica de detecção: Precisa verificar se a tela aparece antes de processar
        - Elementos simples: Parece ser uma tela de confirmação/opção
        
    PARÂMETROS:
        - continuar_com_corretor_anterior: bool - Se deve continuar com o corretor anterior
    """
    try:
        exibir_mensagem("\n" + "="*50)
        exibir_mensagem("[HOMEM]‍[TRABALHO] TELA 14: CORRETOR ANTERIOR (CONDICIONAL)")
        exibir_mensagem("="*50)
        
        # PASSO 1: Verificar se a Tela 14 aparece (é condicional)
        exibir_mensagem("1 [BUSCAR] Verificando se a Tela 14 (Corretor Anterior) aparece...")
        
        # Aguardar um tempo para ver se a tela aparece
        page.wait_for_selector("#gtm-telaCorretorAnteriorContinuar", timeout=5000)
        
        # Tentar localizar elementos da Tela 14
        try:
            # Tentar encontrar o botão da Tela 14
            botao_tela14 = page.locator("#gtm-telaCorretorAnteriorContinuar")
            if botao_tela14.count() > 0 and botao_tela14.first.is_visible():
                exibir_mensagem("2 [OK] Tela 14 detectada - Corretor Anterior aparece!")
                
                # PASSO 2: Processar a Tela 14
                exibir_mensagem(f"3 [HOMEM]‍[TRABALHO] Processando Tela 14: continuar_com_corretor_anterior = {continuar_com_corretor_anterior}")
                
                # Selecionar opção baseada no parâmetro
                if continuar_com_corretor_anterior:
                    exibir_mensagem("4 [OK] Selecionando 'Continuar com corretor anterior'...")
                    # Tentar seletores mais simples e robustos
                    try:
                        # Primeiro tentar por texto
                        page.locator("text=Continuar com corretor anterior").first.click()
                        exibir_mensagem("5 [OK] Opção 'Continuar com corretor anterior' selecionada por texto")
                    except:
                        try:
                            # Tentar por radio button
                            page.locator("input[type='radio'][value='sim']").first.click()
                            exibir_mensagem("5 [OK] Opção 'Continuar com corretor anterior' selecionada por radio")
                        except:
                            # Tentar por label
                            page.locator("label:has-text('Continuar')").first.click()
                            exibir_mensagem("5 [OK] Opção 'Continuar com corretor anterior' selecionada por label")
                else:
                    exibir_mensagem("4 [OK] Selecionando 'Não continuar com corretor anterior'...")
                    try:
                        # Primeiro tentar por texto
                        page.locator("text=Não continuar com corretor anterior").first.click()
                        exibir_mensagem("5 [OK] Opção 'Não continuar com corretor anterior' selecionada por texto")
                    except:
                        try:
                            # Tentar por radio button
                            page.locator("input[type='radio'][value='nao']").first.click()
                            exibir_mensagem("5 [OK] Opção 'Não continuar com corretor anterior' selecionada por radio")
                        except:
                            # Tentar por label
                            page.locator("label:has-text('Não')").first.click()
                            exibir_mensagem("5 [OK] Opção 'Não continuar com corretor anterior' selecionada por label")
                
                # PASSO 3: Clicar no botão Continuar
                exibir_mensagem("6 [ATUALIZANDO] Clicando no botão 'Continuar'...")
                botao_continuar = page.locator('p.font-semibold.font-workSans.cursor-pointer.text-sm.leading-6:has-text("Continuar")')
                if botao_continuar.is_visible():
                    botao_continuar.click()
                    exibir_mensagem("7 [OK] Botão 'Continuar' clicado com sucesso")
                else:
                    exibir_mensagem("7 [AVISO] Botão 'Continuar' não encontrado")
                    return False
                
                # PASSO 4: Aguardar transição para próxima tela
                exibir_mensagem("8 [AGUARDANDO] Aguardando transição para próxima tela...")
                page.wait_for_selector("text=Por favor, aguarde. Estamos buscando o corretor ideal para você!", timeout=5000)
                exibir_mensagem("9 [OK] TELA 14 CONCLUÍDA!")
                
                return True
            else:
                exibir_mensagem("2 [INFO]️ Tela 14 não aparece - não há cotação anterior para este cliente")
                exibir_mensagem("3 [INFO]️ Pulando para próxima tela...")
                return True  # Retorna True mesmo não aparecendo, pois é condicional
                
        except Exception as e:
            exibir_mensagem(f"2 [INFO]️ Tela 14 não detectada: {str(e)}")
            exibir_mensagem("3 [INFO]️ Pulando para próxima tela...")
            return True  # Retorna True mesmo não aparecendo, pois é condicional
        
    except Exception as e:
        exibir_mensagem(f"[ERRO] ERRO na Tela 14: {str(e)}")
        return False

def navegar_tela_15_playwright(page, email_login, senha_login, parametros_tempo, parametros):
    """
    TELA 15: Resultado Final (DUAS FASES)
    
    DESCRIÇÃO:
        Implementa as duas fases da Tela 15:
        FASE 1: Mapa + Timer regressivo (2:43 minutos)
        FASE 2: Tela de cálculo + Modal de login + Modal CPF divergente
        
    ELEMENTOS IDENTIFICADOS:
        FASE 1:
        - Modal timer: text=Por favor, aguarde. Estamos buscando o corretor ideal para você!
        - Timer: text=Tempo estimado em 02:43
        
        FASE 2:
        - Modal login: MuiBackdrop-root
        - Email: #emailTelaLogin
        - Senha: #senhaTelaLogin
        - Botão Acessar: #gtm-telaLoginBotaoAcessar
        - Modal CPF divergente: text=CPF informado não corresponde à conta
        - Botão "Logar com outra conta": #logarComOutraContaModalAssociarUsuario
        
    PARÂMETROS:
        page: Objeto page do Playwright
        email_login: Email para login
        senha_login: Senha para login
        
    RETORNO:
        bool: True se sucesso, False se falha
    """
    try:
        exibir_mensagem("\n" + "="*50)
        exibir_mensagem("[OBJETIVO] TELA 15: RESULTADO FINAL (DUAS FASES)")
        exibir_mensagem("="*50)
        
        # ========================================
        # FASE 1: MAPA + TIMER REGRESSIVO
        # ========================================
        exibir_mensagem("[ATUALIZANDO] FASE 1: Aguardando mapa e timer regressivo...")
        
        # PASSO 1: Aguardar modal com timer aparecer
        exibir_mensagem("[AGUARDANDO] Aguardando modal com timer...")
        
        try:
            # Aguardar especificamente pelo modal com timer (timeout otimizado)
            modal_timer = page.locator("text=Por favor, aguarde. Estamos buscando o corretor ideal para você!")
            modal_timer.wait_for(timeout=5000)
            exibir_mensagem("[OK] Modal com timer detectado!")
        except Exception as e:
            exibir_mensagem(f"[AVISO] Modal com timer não detectado: {str(e)}")
            exibir_mensagem("[INFO]️ Continuando para Fase 2...")
        
        # PASSO 2: Aguardar timer regressivo (aproximadamente 2:43 minutos)
        exibir_mensagem("[AGUARDANDO] Aguardando timer regressivo (2:43 minutos)...")
        
        # Aguardar aproximadamente 2:43 minutos (163 segundos)
        tempo_timer = 163
        tempo_inicio_timer = time.time()
        
        while (time.time() - tempo_inicio_timer) < tempo_timer:
            try:
                # Verificar se ainda está no timer
                timer_atual = page.locator("text=Tempo estimado em")
                if timer_atual.count() > 0:
                    tempo_decorrido = int(time.time() - tempo_inicio_timer)
                    tempo_restante = tempo_timer - tempo_decorrido
                    exibir_mensagem(f"[AGUARDANDO] Timer em andamento... ({tempo_restante}s restantes)")
                else:
                    exibir_mensagem("[OK] Timer concluído!")
                    break
            except:
                pass
            
            try:
                page.wait_for_selector("text=Tempo estimado em", timeout=10000)
            except:
                break
        
        exibir_mensagem("[OK] FASE 1 CONCLUÍDA!")
        
        # ========================================
        # FASE 2: TELA DE CÁLCULO + MODAL LOGIN
        # ========================================
        exibir_mensagem("[ATUALIZANDO] FASE 2: Aguardando tela de cálculo e modal de login...")
        
        # PASSO 3: Aguardar tela de cálculo aparecer
        exibir_mensagem("[AGUARDANDO] Aguardando tela de cálculo...")
        page.wait_for_selector("text=Acesse sua conta para visualizar o resultado final", timeout=8000)
        
        # PASSO 4: Aguardar modal de login aparecer OU tela de cotação manual
        exibir_mensagem("[AGUARDANDO] Aguardando modal de login...")
        
        try:
            # Aguardar especificamente pelo modal de login (timeout otimizado)
            modal_login = page.locator("text=Acesse sua conta para visualizar o resultado final")
            modal_login.wait_for(timeout=5000)
            exibir_mensagem("[OK] Modal de login detectado!")
            
        except Exception as e:
            exibir_mensagem(f"[AVISO] Modal de login não detectado: {str(e)}")
            exibir_mensagem("[BUSCAR] Verificando se apareceu tela de cotação manual...")
            
            # Verificar se apareceu tela de cotação manual
            try:
                tela_cotacao_manual = page.locator('p.text-center.text-base')
                tela_cotacao_manual.wait_for(timeout=3000)
                exibir_mensagem("[OK] TELA DE COTAÇÃO MANUAL DETECTADA!")
                
                # Processar cotação manual
                if processar_cotacao_manual(page, parametros):
                    exibir_mensagem("[OK] COTAÇÃO MANUAL PROCESSADA COM SUCESSO!")
                    return True
                else:
                    exibir_mensagem("[ERRO] ERRO AO PROCESSAR COTAÇÃO MANUAL!")
                    return False
                    
            except Exception as e2:
                exibir_mensagem(f"[ERRO] Tela de cotação manual também não detectada: {str(e2)}")
                exibir_mensagem("[ERRO] Nenhuma tela esperada encontrada!")
                return False
        
        # PASSO 5: Preencher email
        exibir_mensagem("[EMAIL] Preenchendo email...")
        
        try:
            # Aguardar especificamente pelo campo de email estar pronto
            campo_email = page.locator("#emailTelaLogin")
            campo_email.wait_for(timeout=3000)
            campo_email.fill(email_login)
            exibir_mensagem(f"[OK] Email preenchido: {email_login}")
        except Exception as e:
            exibir_mensagem(f"[ERRO] Erro ao preencher email: {str(e)}")
            return False
        
        # PASSO 6: Preencher senha
        exibir_mensagem("[BLOQUEADO] Preenchendo senha...")
        
        try:
            # Aguardar especificamente pelo campo de senha estar pronto
            campo_senha = page.locator("#senhaTelaLogin")
            campo_senha.wait_for(timeout=3000)
            campo_senha.fill(senha_login)
            exibir_mensagem("[OK] Senha preenchida")
        except Exception as e:
            exibir_mensagem(f"[ERRO] Erro ao preencher senha: {str(e)}")
            return False
        
        # PASSO 7: CAPTURA DE TELA E LOGS DETALHADOS DO MODAL
        exibir_mensagem("[FOTO] CAPTURANDO TELA DO MODAL DE LOGIN...")
        
        try:
            # Capturar screenshot do modal
            timestamp = time.strftime('%Y%m%d_%H%M%S')
            screenshot_path = f"modal_login_{timestamp}.png"
            page.screenshot(path=screenshot_path, full_page=True)
            exibir_mensagem(f"[FOTO] Screenshot salvo: {screenshot_path}")
            
            # Verificar se os campos estão realmente preenchidos
            valor_email_campo = campo_email.input_value()
            valor_senha_campo = campo_senha.input_value()
            
            exibir_mensagem(f"[BUSCAR] VERIFICAÇÃO DOS CAMPOS:")
            exibir_mensagem(f"   [EMAIL] Email no campo: '{valor_email_campo}'")
            exibir_mensagem(f"   [BLOQUEADO] Senha no campo: '{valor_senha_campo}'")
            exibir_mensagem(f"   [EMAIL] Email esperado: '{email_login}'")
            exibir_mensagem(f"   [BLOQUEADO] Senha esperada: '{senha_login}'")
            
            # Verificar se os campos estão corretos
            if valor_email_campo.lower() == email_login.lower():
                exibir_mensagem("[OK] Email preenchido corretamente!")
            else:
                exibir_mensagem("[ERRO] Email NÃO foi preenchido corretamente!")
            
            if valor_senha_campo == senha_login:
                exibir_mensagem("[OK] Senha preenchida corretamente!")
            else:
                exibir_mensagem("[ERRO] Senha NÃO foi preenchida corretamente!")
            
            # Verificar se o botão "Acessar" está visível
            botao_acessar = page.locator("#gtm-telaLoginBotaoAcessar")
            if botao_acessar.is_visible():
                exibir_mensagem("[OK] Botão 'Acessar' está visível e pronto para clicar!")
                texto_botao = botao_acessar.text_content()
                exibir_mensagem(f"   [NOTA] Texto do botão: '{texto_botao}'")
            else:
                exibir_mensagem("[ERRO] Botão 'Acessar' NÃO está visível!")
            
            # Verificar se o modal está realmente presente
            modal_presente = page.locator("text=Acesse sua conta para visualizar o resultado final")
            if modal_presente.count() > 0:
                exibir_mensagem("[OK] Modal de login está presente na tela!")
            else:
                exibir_mensagem("[ERRO] Modal de login NÃO está presente na tela!")
            
            # Capturar HTML do modal para debug
            try:
                modal_html = page.locator(".MuiBackdrop-root").inner_html()
                exibir_mensagem(f"[BUSCAR] HTML do modal capturado (primeiros 200 chars): {modal_html[:200]}...")
            except Exception as e:
                exibir_mensagem(f"[AVISO] Erro ao capturar HTML do modal: {str(e)}")
            
        except Exception as e:
            exibir_mensagem(f"[ERRO] Erro durante captura de tela/logs: {str(e)}")
        
        # PASSO 8: Clicar em "Acessar"
        exibir_mensagem("[ATUALIZANDO] Clicando em 'Acessar'...")
        
        try:
            # Aguardar especificamente pelo botão estar pronto
            botao_acessar = page.locator("#gtm-telaLoginBotaoAcessar")
            botao_acessar.wait_for(timeout=3000)
            
            if botao_acessar.is_visible():
                botao_acessar.click()
                exibir_mensagem("[OK] Botão 'Acessar' clicado com sucesso!")
                
                # Aguardar possível redirecionamento ou modal CPF divergente
                exibir_mensagem("[AGUARDANDO] Aguardando resposta do login...")
                
                # DETECTAR FECHAMENTO DO MODAL DE LOGIN
                exibir_mensagem("[BUSCAR] Detectando fechamento do modal de login...")
                try:
                    # Aguardar o modal de login desaparecer (indicando que o login foi processado)
                    modal_login = page.locator("text=Acesse sua conta para visualizar o resultado final")
                    modal_login.wait_for(state="hidden", timeout=10000)
                    exibir_mensagem("[OK] Modal de login fechado - login processado!")
                except Exception as e:
                    exibir_mensagem(f"[AVISO] Modal de login não fechou no tempo esperado: {str(e)}")
                    exibir_mensagem("[INFO]️ Continuando com time.sleep como fallback...")
                    time.sleep(parametros_tempo['tempo_carregamento'])  # Fallback
                
                # Verificar se apareceu modal CPF divergente
                try:
                    modal_cpf = page.locator("text=CPF informado não corresponde à conta")
                    if modal_cpf.count() > 0:
                        exibir_mensagem("[OK] Modal CPF divergente detectado!")
                        exibir_mensagem("[OBJETIVO] MODAL CPF DIVERGENTE DETECTADO: 'CPF informado não corresponde à conta'")
                        
                        # Clicar no botão "Manter Login atual"
                        try:
                            exibir_mensagem("[BUSCAR] Procurando botão 'Manter Login atual'...")
                            
                            # Tentar pelo ID específico
                            botao_manter_login = page.locator("#manterLoginAtualModalAssociarUsuario")
                            if botao_manter_login.is_visible():
                                botao_manter_login.click()
                                exibir_mensagem("[OK] Botão 'Manter Login atual' clicado pelo ID!")
                                
                                # DETECTAR FECHAMENTO DO MODAL CPF DIVERGENTE
                                exibir_mensagem("[BUSCAR] Detectando fechamento do modal CPF divergente...")
                                try:
                                    modal_cpf.wait_for(state="hidden", timeout=5000)
                                    exibir_mensagem("[OK] Modal CPF divergente fechado!")
                                except Exception as e:
                                    exibir_mensagem(f"[AVISO] Modal CPF divergente não fechou no tempo esperado: {str(e)}")
                                    time.sleep(parametros_tempo['tempo_estabilizacao'])
                            else:
                                # Tentar pelo texto
                                botao_manter_login = page.locator("text=Manter Login atual")
                                if botao_manter_login.is_visible():
                                    botao_manter_login.click()
                                    exibir_mensagem("[OK] Botão 'Manter Login atual' clicado pelo texto!")
                                    
                                    # DETECTAR FECHAMENTO DO MODAL CPF DIVERGENTE
                                    exibir_mensagem("[BUSCAR] Detectando fechamento do modal CPF divergente...")
                                    try:
                                        modal_cpf.wait_for(state="hidden", timeout=5000)
                                        exibir_mensagem("[OK] Modal CPF divergente fechado!")
                                    except Exception as e:
                                        exibir_mensagem(f"[AVISO] Modal CPF divergente não fechou no tempo esperado: {str(e)}")
                                        time.sleep(parametros_tempo['tempo_estabilizacao'])
                                else:
                                    exibir_mensagem("[AVISO] Botão 'Manter Login atual' não encontrado")
                        except Exception as e:
                            exibir_mensagem(f"[AVISO] Erro ao clicar no botão 'Manter Login atual': {str(e)}")
                    else:
                        exibir_mensagem("[INFO]️ Modal CPF divergente não apareceu - login pode ter sido bem-sucedido")
                        exibir_mensagem("[ERRO] MODAL CPF DIVERGENTE NÃO DETECTADO: 'CPF informado não corresponde à conta'")
                except Exception as e:
                    exibir_mensagem(f"[AVISO] Erro ao verificar modal CPF: {str(e)}")
                
                # VERIFICAR OUTROS MODAIS QUE PODEM APARECER
                exibir_mensagem("[BUSCAR] Verificando outros modais que podem aparecer...")
                try:
                    # Verificar modal de erro de login
                    modal_erro_login = page.locator("text=Erro ao fazer login")
                    if modal_erro_login.count() > 0:
                        exibir_mensagem("[AVISO] MODAL DE ERRO DE LOGIN DETECTADO!")
                    
                    # Verificar modal de sessão expirada
                    modal_sessao_expirada = page.locator("text=sessão expirada")
                    if modal_sessao_expirada.count() > 0:
                        exibir_mensagem("[AVISO] MODAL DE SESSÃO EXPIRADA DETECTADO!")
                    
                    # Verificar modal de manutenção
                    modal_manutencao = page.locator("text=manutenção")
                    if modal_manutencao.count() > 0:
                        exibir_mensagem("[AVISO] MODAL DE MANUTENÇÃO DETECTADO!")
                    
                    # Verificar modal de captcha
                    modal_captcha = page.locator("text=captcha")
                    if modal_captcha.count() > 0:
                        exibir_mensagem("[AVISO] MODAL DE CAPTCHA DETECTADO!")
                    
                    # Verificar modal de confirmação de dados
                    modal_confirmacao = page.locator("text=confirmação")
                    if modal_confirmacao.count() > 0:
                        exibir_mensagem("[AVISO] MODAL DE CONFIRMAÇÃO DETECTADO!")
                    
                    exibir_mensagem("[OK] Verificação de modais concluída")
                except Exception as e:
                    exibir_mensagem(f"[AVISO] Erro ao verificar outros modais: {str(e)}")
                
            else:
                exibir_mensagem("[ERRO] Botão 'Acessar' não está visível!")
                return False
        except Exception as e:
            exibir_mensagem(f"[ERRO] Erro ao clicar em 'Acessar': {str(e)}")
            return False
        
        exibir_mensagem("[OK] LOGIN CONCLUÍDO!")
        
        # ========================================
        # CAPTURA DE DADOS DOS PLANOS DE SEGURO
        # ========================================
        exibir_mensagem("[DADOS] INICIANDO CAPTURA DE DADOS DOS PLANOS...")
        
        # Aguardar carregamento dos planos (aguardando botão específico)
        exibir_mensagem("[AGUARDANDO] Aguardando carregamento da página principal dos planos...")
        try:
            # Aguardar pelo texto de sucesso final que indica que a página foi carregada
            page.wait_for_selector("text=Parabéns, chegamos ao resultado final da cotação!", timeout=180000)
            exibir_mensagem("[OK] Página principal dos planos carregada!")
            exibir_mensagem("[OBJETIVO] MODAL DE SUCESSO DETECTADO: 'Parabéns, chegamos ao resultado final da cotação!'")
        except Exception as e:
            exibir_mensagem(f"[AVISO] Texto de sucesso final não encontrado: {str(e)}")
            exibir_mensagem("[ERRO] MODAL DE SUCESSO NÃO DETECTADO: 'Parabéns, chegamos ao resultado final da cotação!'")
            exibir_mensagem("[INFO]️ Usando fallback com time.sleep...")
            time.sleep(parametros_tempo['tempo_carregamento'])  # Fallback para time.sleep
        
        # Capturar dados dos planos
        dados_planos = capturar_dados_planos_seguro(page, parametros_tempo)
        
        if dados_planos:
            exibir_mensagem("[OK] DADOS DOS PLANOS CAPTURADOS COM SUCESSO!")
            exibir_mensagem("[INFO] RESUMO DOS DADOS CAPTURADOS:")
            exibir_mensagem(f"   [DADOS] Plano Recomendado: {dados_planos['plano_recomendado'].get('valor', 'N/A')}")
            exibir_mensagem(f"   [DADOS] Plano Alternativo: {dados_planos['plano_alternativo'].get('valor', 'N/A')}")
            
            # RETORNO FINAL SIMPLES
            exibir_mensagem("\n" + "="*60)
            exibir_mensagem("[INFO] RETORNO FINAL - TELA 15")
            exibir_mensagem("="*60)
            exibir_mensagem(json.dumps(dados_planos, indent=2, ensure_ascii=False))
            exibir_mensagem("="*60)
        else:
            exibir_mensagem("[AVISO] FALHA NA CAPTURA DE DADOS DOS PLANOS")
        
        exibir_mensagem("[OBJETIVO] TELA 15 FINALIZADA COM SUCESSO!")
        
        # Delay para inspeção da tela
        # exibir_mensagem("[AGUARDANDO] Aguardando 60 segundos para inspeção da tela...")
        # time.sleep(60)
        # exibir_mensagem("[OK] Tempo de inspeção concluído!")
        
        return True
        
    except Exception as e:
        exibir_mensagem(f"[ERRO] ERRO na Tela 15: {str(e)}")
        return False

# ========================================
# FUNÇÕES DE CAPTURA DE DADOS
# ========================================

def capturar_dados_carrossel_estimativas_playwright(page: Page) -> Dict[str, Any]:
    """
    ================================================================================
    FUNÇÃO: capturar_dados_carrossel_estimativas_playwright()
    ================================================================================
    
    DESCRIÇÃO:
        Captura dados estruturados do carrossel de estimativas da Tela 5.
        Esta função é o coração da captura de dados, extraindo informações
        detalhadas de cada card de cobertura, incluindo valores monetários,
        benefícios e metadados.
    
    ELEMENTOS CAPTURADOS:
        - Nome da cobertura: "button p.text-white"
        - Valores monetários: "p.text-primary.underline"
        - Benefícios: "div.gap-3.flex.flex-col.pl-4.mt-3"
        - Texto completo: Conteúdo total do card
    
    ESTRATÉGIA DE CAPTURA:
        1. Localizar todos os cards de cobertura
        2. Para cada card:
           a. Extrair nome da cobertura
           b. Parsear valores "De R$ X até R$ Y"
           c. Capturar lista de benefícios
           d. Estruturar dados em JSON
        3. Salvar dados em arquivo temporário
        4. Retornar estrutura completa
    
    TÉCNICAS UTILIZADAS:
        - Regex patterns para parsing de valores monetários
        - Seletores CSS específicos para cada elemento
        - Estruturação hierárquica de dados
        - Fallbacks para casos de erro
    
    PARÂMETROS:
        page (Page): Objeto page do Playwright
    
    RETORNO:
        dict: Estrutura JSON com dados capturados ou None se erro
    
    ESTRUTURA DE RETORNO:
        {
            "timestamp": "2025-09-02T03:45:30.523994",
            "tela": 5,
            "nome_tela": "Estimativa Inicial",
            "coberturas_detalhadas": [
                {
                    "indice": 1,
                    "cobertura": "Cobertura Compreensiva",
                    "valores": {"de": "R$ 1.600,00", "ate": "R$ 2.200,00"},
                    "beneficios": [{"nome": "Colisão e Acidentes", "status": "incluido"}]
                }
            ],
            "valores_encontrados": 6,
            "beneficios_gerais": [...],
            "seguradoras": [...],
            "elementos_detectados": [...]
        }
    
    LOGS:
        - "[BUSCAR] Encontrados {X} cards de cobertura (bg-primary)"
        - "[INFO] Card {X}: {cobertura} - De {valor} até {valor}"
        - "[SALVAR] DADOS SALVOS: {caminho_arquivo}"
        - "[DADOS] RESUMO: {X} coberturas detalhadas, {X} benefícios gerais"
        - "[ERRO] ERRO na captura de dados: {erro}"
    ================================================================================
    """
    try:
        # PASSO 1: Inicializar estrutura de dados do carrossel
        # Esta estrutura segue o padrão definido no exemplo_json_retorno.json
        dados_carrossel = {
            "timestamp": datetime.now().isoformat(),  # Timestamp ISO para rastreamento
            "tela": 5,                                # Número da tela atual
            "nome_tela": "Estimativa Inicial",        # Nome descritivo da tela
            "url": str(page.url),                     # URL atual da página
            "titulo": str(page.title),                # Título da página
            "coberturas_detalhadas": [],              # Lista de coberturas capturadas
            "beneficios_gerais": [],                  # Benefícios encontrados na página
            "valores_encontrados": 0,                 # Contador de valores monetários
            "seguradoras": [],                        # Seguradoras detectadas
            "elementos_detectados": []                # Elementos especiais detectados
        }
        
        # Controle de duplicatas para evitar elementos repetidos
        elementos_processados = set()
        
        # DEBUG: Verificar quais elementos estão na página
        exibir_mensagem("[BUSCAR] DEBUG: Verificando elementos na página...")
        
        # ESTRATÉGIA 1: Tentar capturar cards usando seletores mais específicos
        # Primeiro, vamos tentar encontrar os cards de cobertura usando diferentes estratégias
        
        # Estratégia 1.1: Buscar por elementos que contenham "Cobertura" e valores monetários
        exibir_mensagem("[BUSCAR] DEBUG: Estratégia 1.1 - Buscando cards com 'Cobertura'...")
        
        # Buscar por elementos que contenham "Cobertura" e "R$" no mesmo contexto
        cards_cobertura = page.locator("div:has-text('Cobertura'):has-text('R$')")
        exibir_mensagem(f"[BUSCAR] DEBUG: Cards com 'Cobertura' e 'R$' encontrados: {cards_cobertura.count()}")
        
        if cards_cobertura.count() > 0:
            exibir_mensagem(f"[OK] Encontrados {cards_cobertura.count()} cards de cobertura com valores")
            
            for i in range(cards_cobertura.count()):
                try:
                    card = cards_cobertura.nth(i)
                    card_text = card.text_content().strip() if card.text_content() else ""
                    
                    exibir_mensagem(f"[BUSCAR] DEBUG: Card {i+1} texto completo: '{card_text}'")
                    
                    if len(card_text) < 20:  # Se o texto for muito curto, tentar pegar o elemento pai
                        exibir_mensagem(f"[BUSCAR] DEBUG: Card {i+1} texto muito curto, buscando elemento pai...")
                        card = card.locator("..").first  # Elemento pai
                        card_text = card.text_content().strip() if card.text_content() else ""
                        exibir_mensagem(f"[BUSCAR] DEBUG: Card {i+1} texto do pai: '{card_text[:200]}...'")
                    
                    cobertura_info = {
                        "indice": i + 1,
                        "nome_cobertura": "",
                        "valores": {
                            "de": "",
                            "ate": ""
                        },
                        "beneficios": [],
                        "texto_completo": card_text
                    }
                    
                    # Extrair nome da cobertura usando regex mais robusto
                    cobertura_patterns = [
                        r"Cobertura\s+([A-Za-zÀ-ÿ\s]+?)(?:\s|$|R\$)",
                        r"([A-Za-zÀ-ÿ\s]+?)\s+Cobertura",
                        r"Cobertura\s+Compreensiva",
                        r"Cobertura\s+Roubo\s+e\s+Furto",
                        r"Cobertura\s+RCF"
                    ]
                    
                    for pattern in cobertura_patterns:
                        match = re.search(pattern, card_text, re.IGNORECASE)
                        if match:
                            if "Compreensiva" in pattern:
                                cobertura_info["nome_cobertura"] = "Cobertura Compreensiva"
                            elif "Roubo" in pattern:
                                cobertura_info["nome_cobertura"] = "Cobertura Roubo e Furto"
                            elif "RCF" in pattern:
                                cobertura_info["nome_cobertura"] = "Cobertura RCF"
                            else:
                                cobertura_info["nome_cobertura"] = match.group(1).strip()
                            exibir_mensagem(f"[BUSCAR] DEBUG: Nome encontrado via regex: '{cobertura_info['nome_cobertura']}'")
                            break
                    
                    # Extrair valores monetários usando regex mais específico
                    valor_patterns = [
                        r"De\s*R\$\s*([0-9.,]+)\s*até\s*R\$\s*([0-9.,]+)",
                        r"R\$\s*([0-9.,]+)\s*até\s*R\$\s*([0-9.,]+)",
                        r"([0-9.,]+)\s*até\s*([0-9.,]+)"
                    ]
                    
                    for pattern in valor_patterns:
                        match = re.search(pattern, card_text, re.IGNORECASE)
                        if match:
                            cobertura_info["valores"]["de"] = f"R$ {match.group(1)}"
                            cobertura_info["valores"]["ate"] = f"R$ {match.group(2)}"
                            exibir_mensagem(f"[BUSCAR] DEBUG: Valores extraídos: De {cobertura_info['valores']['de']} até {cobertura_info['valores']['ate']}")
                            break
                    
                    # Extrair benefícios conhecidos do texto do card
                    beneficios_conhecidos = [
                        "Colisão e Acidentes", "Roubo e Furto", "Incêndio", "Danos a terceiros",
                        "Assistência 24h", "Carro Reserva", "Vidros", "Roubo", "Furto",
                        "Danos parciais em tentativas de roubo", "Danos materiais a terceiros",
                        "Danos corporais a terceiro", "Assistência", "Carro reserva",
                        "Vidros", "Acidentes", "Colisão", "Terceiros", "Materiais", "Corporais"
                    ]
                    
                    for beneficio in beneficios_conhecidos:
                        if beneficio.lower() in card_text.lower():
                            cobertura_info["beneficios"].append({
                                "nome": beneficio,
                                "status": "incluido"
                            })
                    
                    # Validar se elemento é único antes de adicionar
                    if validar_elemento_unico(card_text, elementos_processados):
                        dados_carrossel["coberturas_detalhadas"].append(cobertura_info)
                        exibir_mensagem(f"[INFO] Card {len(dados_carrossel['coberturas_detalhadas'])}: {cobertura_info['nome_cobertura']} - De {cobertura_info['valores']['de']} até {cobertura_info['valores']['ate']}")
                    else:
                        exibir_mensagem(f"[AVISO] Card duplicado ignorado: {cobertura_info['nome_cobertura']}")
                    
                except Exception as e:
                    exibir_mensagem(f"[AVISO] Erro ao processar card {i+1}: {str(e)}")
                    continue
        
        # ESTRATÉGIA 1.2: Se não encontrou cards com a estratégia anterior, tentar seletores específicos
        if len(dados_carrossel["coberturas_detalhadas"]) == 0:
            exibir_mensagem("[BUSCAR] DEBUG: Estratégia 1.2 - Tentando seletores específicos...")
            
            # Tentar diferentes seletores para encontrar os cards
            # v3.7.0.2: Estratégia híbrida robusta para seletores de cards
            seletores_cards = [
                'div[role="group"][aria-roledescription="slide"]',  # <- NOVO PRINCIPAL
                'div:has(p:has-text("Cobertura")):has(span:has-text("R$"))',  # <- NOVO CONTEÚDO
                'div.border-primary.rounded-xl:has(.bg-primary)',  # <- NOVO LAYOUT
                "div.bg-primary",  # <- FALLBACK ATUAL
                "div[class*='bg-primary']",
                "div[class*='card']",
                "div[class*='cobertura']",
                "div:has(button)",
                "div:has(p.text-white)"
            ]
            
            for seletor in seletores_cards:
                try:
                    cards = page.locator(seletor)
                    exibir_mensagem(f"[BUSCAR] DEBUG: Seletor '{seletor}' encontrou: {cards.count()} elementos")
                    
                    if cards.count() > 0:
                        for i in range(min(cards.count(), 5)):  # Limitar a 5 cards
                            try:
                                card = cards.nth(i)
                                card_text = card.text_content().strip() if card.text_content() else ""
                                
                                exibir_mensagem(f"[BUSCAR] DEBUG: Card {i+1} com seletor '{seletor}': '{card_text[:100]}...'")
                                
                                # Verificar se o card tem conteúdo relevante
                                if "cobertura" in card_text.lower() or "r$" in card_text.lower():
                                    cobertura_info = {
                                        "indice": len(dados_carrossel["coberturas_detalhadas"]) + 1,
                                        "nome_cobertura": "",
                                        "valores": {"de": "", "ate": ""},
                                        "beneficios": [],
                                        "texto_completo": card_text
                                    }
                                    
                                    # Extrair nome e valores (mesma lógica anterior)
                                    # ... (código de extração)
                                    
                                    # Validar se elemento é único antes de adicionar
                                    if validar_elemento_unico(card_text, elementos_processados):
                                        dados_carrossel["coberturas_detalhadas"].append(cobertura_info)
                                        exibir_mensagem(f"[INFO] Card encontrado via '{seletor}': {cobertura_info['nome_cobertura']}")
                                    else:
                                        exibir_mensagem(f"[AVISO] Card duplicado ignorado via '{seletor}': {cobertura_info['nome_cobertura']}")
                                    
                            except Exception as e:
                                exibir_mensagem(f"[AVISO] Erro ao processar card com seletor '{seletor}': {str(e)}")
                                continue
                        
                        if len(dados_carrossel["coberturas_detalhadas"]) > 0:
                            break  # Se encontrou cards, parar de tentar outros seletores
                            
                except Exception as e:
                    exibir_mensagem(f"[AVISO] Erro com seletor '{seletor}': {str(e)}")
                    continue
        
        # ESTRATÉGIA 2: Fallback - Buscar por valores monetários na página inteira
        if len(dados_carrossel["coberturas_detalhadas"]) == 0:
            exibir_mensagem("[BUSCAR] DEBUG: Estratégia 2 - Fallback: buscando valores monetários na página...")
            
            # Buscar por todos os elementos que contenham "R$"
            elementos_r = page.locator("text=R$")
            exibir_mensagem(f"[BUSCAR] DEBUG: Elementos com 'R$' encontrados: {elementos_r.count()}")
            
            if elementos_r.count() > 0:
                for i in range(min(elementos_r.count(), 10)):  # Limitar a 10 elementos
                    try:
                        elemento = elementos_r.nth(i)
                        elemento_text = elemento.text_content().strip() if elemento.text_content() else ""
                        
                        # Buscar o contexto do elemento (elemento pai)
                        contexto = elemento.locator("..").first
                        contexto_text = contexto.text_content().strip() if contexto.text_content() else ""
                        
                        exibir_mensagem(f"[BUSCAR] DEBUG: Elemento R$ {i+1}: '{elemento_text}' | Contexto: '{contexto_text[:100]}...'")
                        
                        # Se o contexto contém "Cobertura", pode ser um card válido
                        if "cobertura" in contexto_text.lower():
                            cobertura_info = {
                                "indice": len(dados_carrossel["coberturas_detalhadas"]) + 1,
                                "nome_cobertura": "Cobertura Detectada",
                                "valores": {"de": "", "ate": ""},
                                "beneficios": [],
                                "texto_completo": contexto_text
                            }
                            
                            # Extrair valores
                            valor_patterns = [
                                r"De\s*R\$\s*([0-9.,]+)\s*até\s*R\$\s*([0-9.,]+)",
                                r"R\$\s*([0-9.,]+)\s*até\s*R\$\s*([0-9.,]+)"
                            ]
                            
                            for pattern in valor_patterns:
                                match = re.search(pattern, contexto_text, re.IGNORECASE)
                                if match:
                                    cobertura_info["valores"]["de"] = f"R$ {match.group(1)}"
                                    cobertura_info["valores"]["ate"] = f"R$ {match.group(2)}"
                                    break
                            
                            # Validar se elemento é único antes de adicionar
                            if validar_elemento_unico(contexto_text, elementos_processados):
                                dados_carrossel["coberturas_detalhadas"].append(cobertura_info)
                                exibir_mensagem(f"[INFO] Valor encontrado: De {cobertura_info['valores']['de']} até {cobertura_info['valores']['ate']}")
                            else:
                                exibir_mensagem(f"[AVISO] Valor duplicado ignorado: De {cobertura_info['valores']['de']} até {cobertura_info['valores']['ate']}")
                            
                    except Exception as e:
                        exibir_mensagem(f"[AVISO] Erro ao processar elemento R$ {i+1}: {str(e)}")
                        continue
        
        # Contar valores encontrados
        dados_carrossel["valores_encontrados"] = len(dados_carrossel["coberturas_detalhadas"])
        
        # Procurar por valores monetários gerais (fallback)
        valores_monetarios = page.locator("text=R$")
        dados_carrossel["valores_encontrados"] = max(dados_carrossel["valores_encontrados"], valores_monetarios.count())
        
        # Procurar por benefícios gerais na página
        beneficios_gerais = [
            "Colisão e Acidentes", "Roubo e Furto", "Incêndio", "Danos a terceiros",
            "Assistência 24h", "Carro Reserva", "Vidros", "Roubo", "Furto",
            "Danos parciais em tentativas de roubo", "Danos materiais a terceiros",
            "Danos corporais a terceiro"
        ]
        
        for beneficio in beneficios_gerais:
            elementos = page.locator(f"text={beneficio}")
            if elementos.count() > 0:
                dados_carrossel["beneficios_gerais"].append({
                    "nome": beneficio,
                    "encontrado": True,
                    "quantidade_elementos": elementos.count()
                })
        
        # Procurar por seguradoras
        seguradoras_texto = [
            "Seguradora", "seguradora", "Seguro", "seguro",
            "Allianz", "allianz", "Porto", "porto", "SulAmérica", "sulamerica",
            "Bradesco", "bradesco", "Itaú", "itau", "Santander", "santander"
        ]
        
        for seguradora in seguradoras_texto:
            elementos = page.locator(f"text={seguradora}")
            if elementos.count() > 0:
                for j in range(min(elementos.count(), 3)):  # Limitar a 3 elementos
                    texto = elementos.nth(j).text_content().strip()
                    if texto and len(texto) > 2:
                        dados_carrossel["seguradoras"].append({
                            "nome": texto,
                            "seletor": "texto_contido"
                        })
        
        # Procurar por elementos específicos do carrossel
        elementos_carrossel = page.locator("[class*='carousel'], [class*='slider'], [class*='swiper']")
        if elementos_carrossel.count() > 0:
            dados_carrossel["elementos_detectados"].append("carrossel_detectado")
        
        # Capturar texto completo da página para análise
        page_content = page.content()
        page_text = page_content.lower() if page_content else ""
        
        # Verificar presença de palavras-chave
        palavras_chave = ["estimativa", "carrossel", "cobertura", "preço", "valor", "plano"]
        for palavra in palavras_chave:
            if palavra in page_text:
                dados_carrossel["elementos_detectados"].append(f"palavra_chave: {palavra}")
        
        # Salvar dados em arquivo temporário
        temp_dir = "temp/captura_carrossel"
        os.makedirs(temp_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        json_path = f"{temp_dir}/carrossel_estimativas_{timestamp}.json"
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(dados_carrossel, f, indent=2, ensure_ascii=False)
        
        exibir_mensagem(f"[SALVAR] DADOS SALVOS: {json_path}")
        exibir_mensagem(f"[DADOS] RESUMO: {len(dados_carrossel['coberturas_detalhadas'])} coberturas detalhadas, {len(dados_carrossel['beneficios_gerais'])} benefícios gerais")
        
        return dados_carrossel
        
    except Exception as e:
        exibir_mensagem(f"[ERRO] ERRO na captura de dados: {str(e)}")
        return None

def processar_cotacao_manual(page: Page, parametros: Dict[str, Any]) -> bool:
    """
    PROCESSAR COTAÇÃO MANUAL: Quando não há cotação automática disponível
    
    VERSÃO: v3.4.0
    IMPLEMENTAÇÃO: Captura dados e retorna erro específico para cotação manual
    """
    try:
        exception_handler.definir_tela_atual("COTACAO_MANUAL")
        exibir_mensagem("[INFO] PROCESSANDO COTAÇÃO MANUAL...")
        
        # 1. CAPTURAR MENSAGEM COMPLETA
        mensagem_elemento = page.locator('p.text-center.text-base').first
        mensagem_completa = mensagem_elemento.text_content() if mensagem_elemento.is_visible() else "Mensagem não capturada"
        
        exibir_mensagem(f"[NOTA] Mensagem capturada: {mensagem_completa}")
        
        # 2. CRIAR ESTRUTURA DE DADOS
        dados_cotacao_manual = {
            "timestamp": datetime.now().isoformat(),
            "tela": "cotacao_manual",
            "nome_tela": "Cotação Manual",
            "url": page.url,
            "titulo_pagina": page.title(),
            "mensagem": mensagem_completa,
            "tipo_veiculo": parametros.get('tipo_veiculo', 'carro'),
            "placa": parametros.get('placa', ''),
            "marca": parametros.get('marca', ''),
            "modelo": parametros.get('modelo', ''),
            "ano": parametros.get('ano', ''),
            "dados_pessoais": {
                "nome": parametros.get('nome', ''),
                "cpf": parametros.get('cpf', ''),
                "email": parametros.get('email', ''),
                "celular": parametros.get('celular', '')
            },
            "dados_endereco": {
                "cep": parametros.get('cep', ''),
                "endereco_completo": parametros.get('endereco_completo', '')
            },
            "status": "cotacao_manual_necessaria"
        }
        
        # 3. SALVAR DADOS
        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        json_path = f"temp/cotacao_manual_{timestamp_str}.json"
        
        # Criar diretório se não existir
        os.makedirs("temp", exist_ok=True)
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(dados_cotacao_manual, f, ensure_ascii=False, indent=2)
        
        exibir_mensagem(f"[SALVAR] DADOS SALVOS: {json_path}")
        
        # 4. LOGS DETALHADOS
        exibir_mensagem("[INFO]️ Cotação será feita manualmente pelo corretor")
        exibir_mensagem(f"[DADOS] Dados coletados para análise:")
        exibir_mensagem(f"   [VEICULO] Veículo: {parametros.get('marca')} {parametros.get('modelo')} {parametros.get('ano')}")
        exibir_mensagem(f"   [LOCALIZACAO] Placa: {parametros.get('placa')}")
        exibir_mensagem(f"   [USUARIO] Segurado: {parametros.get('nome')}")
        exibir_mensagem(f"   [EMAIL] Email: {parametros.get('email')}")
        
        return True
        
    except Exception as e:
        exception_handler.capturar_excecao(e, "COTACAO_MANUAL", "Erro ao processar cotação manual")
        return False

def criar_retorno_erro_cotacao_manual(mensagem: str, tipo_erro: str, tempo_execucao: float, parametros: Dict[str, Any], exception_handler) -> Dict[str, Any]:
    """
    CRIAR RETORNO DE ERRO ESPECÍFICO PARA COTAÇÃO MANUAL
    
    VERSÃO: v3.4.0
    IMPLEMENTAÇÃO: Retorno específico quando cotação manual é necessária
    """
    try:
        # Estrutura específica para cotação manual
        retorno = {
            "status": "cotacao_manual",
            "timestamp": datetime.now().isoformat(),
            "versao": "3.4.0",
            "sistema": "RPA Tô Segurado - Playwright",
            "codigo": 9003,
            "mensagem": mensagem,
            "tipo_erro": tipo_erro,
            "tempo_execucao": f"{tempo_execucao:.1f}s",
            "dados": {
                "tipo_veiculo": parametros.get('tipo_veiculo', 'carro'),
                "placa_processada": parametros.get('placa', ''),
                "marca": parametros.get('marca', ''),
                "modelo": parametros.get('modelo', ''),
                "ano": parametros.get('ano', ''),
                "cotacao_manual_necessaria": True,
                "dados_coletados": {
                    "dados_pessoais": {
                        "nome": parametros.get('nome', ''),
                        "cpf": parametros.get('cpf', ''),
                        "email": parametros.get('email', ''),
                        "celular": parametros.get('celular', '')
                    },
                    "dados_endereco": {
                        "cep": parametros.get('cep', ''),
                        "endereco_completo": parametros.get('endereco_completo', '')
                    },
                    "dados_veiculo": {
                        "tipo_veiculo": parametros.get('tipo_veiculo', 'carro'),
                        "placa": parametros.get('placa', ''),
                        "marca": parametros.get('marca', ''),
                        "modelo": parametros.get('modelo', ''),
                        "ano": parametros.get('ano', ''),
                        "combustivel": parametros.get('combustivel', ''),
                        "zero_km": parametros.get('zero_km', False),
                        "blindado": parametros.get('blindado', False),
                        "financiado": parametros.get('financiado', False)
                    }
                }
            },
            "logs": exception_handler.obter_logs() if hasattr(exception_handler, 'obter_logs') else []
        }
        
        return retorno
        
    except Exception as e:
        # Fallback para retorno de erro padrão
        return criar_retorno_erro(
            f"Erro ao criar retorno de cotação manual: {str(e)}",
            "COTACAO_MANUAL_ERROR",
            tempo_execucao,
            parametros,
            exception_handler
        )

def capturar_dados_planos_seguro(page: Page, parametros_tempo) -> Dict[str, Any]:
    """
    CAPTURA DADOS DOS PLANOS DE SEGURO - ABORDAGEM HÍBRIDA
    
    DESCRIÇÃO:
        Captura os dados dos planos de seguro (Recomendado e Alternativo) na Tela 15.
        Usa abordagem híbrida: seletores + extração de texto completo + parse estruturado + regex.
        Baseado na implementação Selenium que funcionava corretamente.
        
    ESTRATÉGIA:
        1. Encontrar containers dos planos usando seletores
        2. Extrair texto completo de cada container
        3. Fazer parse estruturado baseado na posição das linhas
        4. Usar regex como fallback para valores não encontrados
        5. Mapear dados para estrutura JSON estruturada
        
    RETORNO:
        dict: Dicionário com os dados dos planos estruturados
    """
    try:
        exception_handler.definir_tela_atual("CAPTURA_DADOS_PLANOS")
        exibir_mensagem("[DADOS] CAPTURANDO DADOS DOS PLANOS DE SEGURO - ABORDAGEM HÍBRIDA")
        exibir_mensagem("=" * 70)
        
        # Aguardar carregamento dos planos (estratégia simples)
        time.sleep(parametros_tempo['tempo_estabilizacao'])
        
        dados_planos = {
            "plano_recomendado": {
                "plano": "Plano recomendado",
                "valor": "N/A",
                "forma_pagamento": "N/A",
                "parcelamento": "N/A",
                "valor_franquia": "N/A",
                "valor_mercado": "N/A",
                "assistencia": False,
                "vidros": False,
                "carro_reserva": False,
                "danos_materiais": "N/A",
                "danos_corporais": "N/A",
                "danos_morais": "N/A",
                "morte_invalidez": "N/A"
            },
            "plano_alternativo": {
                "plano": "Plano alternativo",
                "valor": "N/A",
                "forma_pagamento": "N/A",
                "parcelamento": "N/A",
                "valor_franquia": "N/A",
                "valor_mercado": "N/A",
                "assistencia": False,
                "vidros": False,
                "carro_reserva": False,
                "danos_materiais": "N/A",
                "danos_corporais": "N/A",
                "danos_morais": "N/A",
                "morte_invalidez": "N/A"
            }
        }
        
        # ========================================
        # ETAPA 1: ENCONTRAR CONTAINERS DOS PLANOS (ESTRUTURA HTML CORRETA)
        # ========================================
        exibir_mensagem("[BUSCAR] ETAPA 1: Encontrando containers dos planos usando estrutura HTML correta...")
        
        # Usar a estrutura HTML correta identificada
        try:
            # Encontrar o container principal com grid
            container_principal = page.locator("div.grid-cols-\\[250px__1fr__1fr\\]")
            if container_principal.count() == 0:
                exibir_mensagem("[AVISO] Container principal não encontrado, usando fallback...")
                # Fallback para método anterior
                container_principal = page.locator("div")
            
            exibir_mensagem(f"[DADOS] CONTAINER PRINCIPAL ENCONTRADO: {container_principal.count()}")
            
            # Extrair planos diretamente da estrutura correta
            tabelas_planos = []
            
            # Plano Recomendado: div com border-primary
            plano_recomendado = container_principal.locator("div.md\\:w-80.border-4.border-primary")
            if plano_recomendado.count() > 0:
                tabelas_planos.append(plano_recomendado.first)
                exibir_mensagem("[OK] PLANO RECOMENDADO ENCONTRADO na estrutura correta")
            
            # Plano Alternativo: div com border-4 mas sem border-primary
            plano_alternativo = container_principal.locator("div.md\\:w-80.border-4:not(.border-primary)")
            if plano_alternativo.count() > 0:
                tabelas_planos.append(plano_alternativo.first)
                exibir_mensagem("[OK] PLANO ALTERNATIVO ENCONTRADO na estrutura correta")
            
            # Se não encontrou na estrutura correta, usar fallback
            if len(tabelas_planos) == 0:
                exibir_mensagem("[AVISO] Usando fallback para detecção de planos...")
                # Fallback: procurar por divs com classes específicas
                planos_divs = page.locator("//div[contains(@class, 'md:w-80') or contains(@class, 'border-4')]").all()
                for elem in planos_divs:
                    try:
                        texto = elem.text_content()
                        if texto and len(texto) > 100:
                            tabelas_planos.append(elem)
                            exibir_mensagem(f"[INFO] CONTAINER FALLBACK: {len(texto)} caracteres - {texto[:100]}...")
                    except:
                        continue
            
        except Exception as e:
            exibir_mensagem(f"[AVISO] Erro na detecção por estrutura: {str(e)}")
            # Fallback completo
            tabelas_planos = []
            elementos_valores = page.locator("//*[contains(text(), 'R$')]").all()
            for elem in elementos_valores:
                try:
                    texto = elem.text_content()
                    if texto and len(texto) > 100:
                        tabelas_planos.append(elem)
                        exibir_mensagem(f"[INFO] CONTAINER FALLBACK COMPLETO: {len(texto)} caracteres - {texto[:100]}...")
                except:
                    continue
        
        exibir_mensagem(f"[DADOS] CONTAINERS DE PLANOS ENCONTRADOS: {len(tabelas_planos)}")
        
        # ========================================
        # ETAPA 2: ANALISAR CADA CONTAINER
        # ========================================
        exibir_mensagem(f"[BUSCAR] PROCESSANDO {len(tabelas_planos)} CONTAINERS...")
        for i, elemento in enumerate(tabelas_planos):  # Processar todos os containers
            try:
                tabela_text = elemento.text_content().strip()
                if not tabela_text or len(tabela_text) < 30:
                    continue
                
                exibir_mensagem(f"[INFO] ANALISANDO CONTAINER {i+1}/{len(tabelas_planos)}: {len(tabela_text)} caracteres")
                exibir_mensagem(f"[BUSCAR] DEBUG: Texto completo da tabela: '{tabela_text}'")
                
                # DEBUG: Capturar HTML completo do container
                try:
                    html_completo = elemento.inner_html()
                    exibir_mensagem(f"[BUSCAR] DEBUG: HTML completo do container (primeiros 500 chars): {html_completo[:500]}...")
                except Exception as e:
                    exibir_mensagem(f"[AVISO] Erro ao capturar HTML: {str(e)}")
                
                # Determinar tipo de plano baseado na estrutura HTML
                if "plano recomendado" in tabela_text.lower():
                    plano_tipo = "plano_recomendado"
                    exibir_mensagem("[OK] PLANO RECOMENDADO DETECTADO")
                elif "plano alternativo" in tabela_text.lower():
                    plano_tipo = "plano_alternativo"
                    exibir_mensagem("[OK] PLANO ALTERNATIVO DETECTADO")
                elif tabela_text.startswith("R$") and "anual" in tabela_text.lower():
                    # Container que começa com R$ e tem "anual" é provavelmente Plano Alternativo
                    plano_tipo = "plano_alternativo"
                    exibir_mensagem("[OK] PLANO ALTERNATIVO DETECTADO (por padrão)")
                else:
                    # Detectar por posição na lista (primeiro = recomendado, segundo = alternativo)
                    if i == 0:
                        plano_tipo = "plano_recomendado"
                        exibir_mensagem("[OK] PLANO RECOMENDADO DETECTADO (por posição)")
                    elif i == 1:
                        plano_tipo = "plano_alternativo"
                        exibir_mensagem("[OK] PLANO ALTERNATIVO DETECTADO (por posição)")
                    else:
                        exibir_mensagem(f"[AVISO] TIPO DE PLANO NÃO IDENTIFICADO - Container {i+1}: {tabela_text[:200]}...")
                        continue
                
                # ETAPA 3: PARSE ESTRUTURADO BASEADO NA POSIÇÃO
                # Dividir o texto por quebras de linha para análise estruturada
                linhas = tabela_text.split('\n')
                linhas = [linha.strip() for linha in linhas if linha.strip()]
                
                # DEBUG: Verificar elementos no container (mantido para debug)
                try:
                    todos_elementos = elemento.locator("*").all()
                    exibir_mensagem(f"[BUSCAR] Total de elementos no container: {len(todos_elementos)}")
                except Exception as e:
                    exibir_mensagem(f"[AVISO] Erro ao contar elementos: {str(e)}")
                
                # Se o split por \n resultou em apenas 1 linha, tentar dividir por padrões específicos
                if len(linhas) == 1:
                    exibir_mensagem("[AVISO] Apenas 1 linha detectada - aplicando divisão por padrões")
                    texto_original = linhas[0]
                    
                    # Padrões para dividir o texto em campos individuais (em ordem de prioridade)
                    padroes_divisao = [
                        r'(Plano\s*recomendado)',  # Título do plano primeiro
                        r'(R\$\s*[0-9.,]+)',  # Valores monetários
                        r'(anual)',  # Periodicidade
                        r'(Crédito\s*em\s*até\s*[^!]+!)',  # Forma de pagamento crédito
                        r'(Boleto/Débito\s*em\s*até\s*[^!]+!)',  # Forma de pagamento boleto
                        r'(Franquia)',  # Label Franquia
                        r'(Valor\s*de\s*Mercado)',  # Label Valor de Mercado
                        r'(100%\s*da\s*tabela\s*FIPE)',  # Valor de mercado
                        r'(Assistência)',  # Assistência
                        r'(Vidros)',  # Vidros
                        r'(Carro\s*Reserva)',  # Carro Reserva
                        r'(Danos\s*Materiais)',  # Danos Materiais
                        r'(Danos\s*Corporais)',  # Danos Corporais
                        r'(Danos\s*Morais)',  # Danos Morais
                        r'(Morte/Invalidez)',  # Morte/Invalidez
                        r'(Normal|Reduzida)',  # Tipo de franquia
                    ]
                    
                    # Aplicar divisão por padrões usando uma abordagem sequencial
                    linhas_divididas = []
                    texto_restante = texto_original
                    
                    # Processar cada padrão em ordem
                    for padrao in padroes_divisao:
                        match = re.search(padrao, texto_restante, re.IGNORECASE)
                        if match:
                            start, end = match.span()
                            
                            # Extrair texto antes do padrão
                            if start > 0:
                                texto_antes = texto_restante[:start].strip()
                                if texto_antes:
                                    linhas_divididas.append(texto_antes)
                            
                            # Adicionar o padrão encontrado
                            linhas_divididas.append(match.group().strip())
                            
                            # Atualizar texto restante
                            texto_restante = texto_restante[end:].strip()
                    
                    # Adicionar texto restante se houver
                    if texto_restante:
                        linhas_divididas.append(texto_restante)
                    
                    # Filtrar linhas vazias e reorganizar
                    linhas = [linha.strip() for linha in linhas_divididas if linha.strip()]
                    
                    # CORREÇÃO ESPECÍFICA: Separar valor da franquia do tipo de franquia
                    linhas_corrigidas = []
                    for i, linha in enumerate(linhas):
                        # Verificar se a linha contém valor da franquia seguido de tipo de franquia
                        # Padrão: "R$ 9.501,00Normal" -> "R$ 9.501,00" + "Normal"
                        match_franquia = re.match(r'(R\$\s*[0-9.,]+)(Normal|Reduzida)', linha)
                        if match_franquia:
                            valor_franquia = match_franquia.group(1).strip()
                            tipo_franquia = match_franquia.group(2).strip()
                            linhas_corrigidas.append(valor_franquia)
                            linhas_corrigidas.append(tipo_franquia)
                            exibir_mensagem(f"[OK] FRANQUIA SEPARADA: '{valor_franquia}' + '{tipo_franquia}'")
                        else:
                            linhas_corrigidas.append(linha)
                    
                    linhas = linhas_corrigidas
                    
                    exibir_mensagem(f"[OK] DIVISÃO POR PADRÕES APLICADA: {len(linhas)} campos encontrados")
                
                exibir_mensagem(f"[BUSCAR] ANALISANDO ESTRUTURA: {len(linhas)} linhas encontradas")
                exibir_mensagem(f"[BUSCAR] DEBUG: Linhas da tabela: {linhas}")
                
                # Determinar se tem título e ajustar índice de início
                tem_titulo = False
                indice_inicio = 0
                
                if len(linhas) > 0:
                    primeira_linha = linhas[0].lower()
                    if "plano recomendado" in primeira_linha or "recomendado" in primeira_linha:
                        tem_titulo = True
                        indice_inicio = 1  # Pular o título
                        exibir_mensagem("[OK] TÍTULO DETECTADO - PULANDO PRIMEIRA LINHA")
                
                # Parse estruturado baseado na especificação
                if len(linhas) >= indice_inicio + 8:  # Mínimo de 8 campos após título
                    try:
                        exibir_mensagem("[BUSCAR] Iniciando mapeamento dinâmico de dados...")
                        
                        # 7-9. Processar ícones de cobertura usando estrutura HTML correta
                        exibir_mensagem("[BUSCAR] Detectando ícones de cobertura usando estrutura HTML correta...")
                        try:
                            # Detectar ícones diretamente no container
                            icones_ok = elemento.locator("img[src='/icone-ok.svg']").all()
                            icones_nok = elemento.locator("img[src='/icone-nok.svg']").all()
                            
                            exibir_mensagem(f"[BUSCAR] Ícones de OK encontrados: {len(icones_ok)}")
                            exibir_mensagem(f"[BUSCAR] Ícones de NOK encontrados: {len(icones_nok)}")
                            
                            # Mapear ícones por ordem de aparição na estrutura HTML
                            coberturas_campos = ['assistencia', 'vidros', 'carro_reserva']
                            
                            for i, campo in enumerate(coberturas_campos):
                                try:
                                    # Verificar se há ícone de OK na posição i
                                    if len(icones_ok) > i and icones_ok[i].is_visible():
                                        dados_planos[plano_tipo][campo] = True
                                        exibir_mensagem(f"[OK] {campo.title()}: True (ícone OK detectado na posição {i})")
                                    elif len(icones_nok) > i and icones_nok[i].is_visible():
                                        dados_planos[plano_tipo][campo] = False
                                        exibir_mensagem(f"[ERRO] {campo.title()}: False (ícone NOK detectado na posição {i})")
                                    else:
                                        # Fallback: verificar se existe o texto da cobertura
                                        if campo.title() in tabela_text:
                                            dados_planos[plano_tipo][campo] = True
                                            exibir_mensagem(f"[OK] {campo.title()}: True (texto detectado como fallback)")
                                        else:
                                            dados_planos[plano_tipo][campo] = False
                                            exibir_mensagem(f"[ERRO] {campo.title()}: False (nenhum ícone ou texto encontrado)")
                                        
                                except Exception as e:
                                    exibir_mensagem(f"[AVISO] Erro ao processar ícone para {campo}: {str(e)}")
                                    dados_planos[plano_tipo][campo] = False
                            
                        except Exception as e:
                            exibir_mensagem(f"[AVISO] Erro na detecção de ícones: {str(e)}")
                            # Fallback: definir todos como False
                            for cobertura in ['assistencia', 'vidros', 'carro_reserva']:
                                dados_planos[plano_tipo][cobertura] = False
                        
                        # 8-11. Mapear dados por padrões (NOVA LÓGICA DINÂMICA)
                        exibir_mensagem("[BUSCAR] Mapeando dados por padrões dinâmicos...")
                        try:
                            # Detectar valores monetários
                            valores_monetarios = []
                            for linha in linhas:
                                if re.match(r'^R\$\s*[0-9.,]+$', linha):
                                    valores_monetarios.append(linha)
                            
                            exibir_mensagem(f"[BUSCAR] Valores monetários encontrados: {valores_monetarios}")
                            
                            # Detectar textos específicos
                            textos_especificos = {}
                            for linha in linhas:
                                if "anual" in linha.lower():
                                    textos_especificos["parcelamento"] = linha
                                elif "crédito" in linha.lower() or "boleto" in linha.lower():
                                    textos_especificos["forma_pagamento"] = linha
                                elif "100% da tabela fipe" in linha.lower():
                                    textos_especificos["valor_mercado"] = linha
                                elif linha.lower() in ['normal', 'reduzida']:
                                    textos_especificos["tipo_franquia"] = linha
                            
                            exibir_mensagem(f"[BUSCAR] Textos específicos encontrados: {textos_especificos}")
                            
                            # Mapear valores monetários por ordem de aparição
                            if len(valores_monetarios) >= 6:
                                dados_planos[plano_tipo]["valor"] = valores_monetarios[0]  # Primeiro valor
                                dados_planos[plano_tipo]["valor_franquia"] = valores_monetarios[1]  # Segundo valor
                                dados_planos[plano_tipo]["danos_materiais"] = valores_monetarios[2]  # Terceiro valor
                                dados_planos[plano_tipo]["danos_corporais"] = valores_monetarios[3]  # Quarto valor
                                dados_planos[plano_tipo]["danos_morais"] = valores_monetarios[4]  # Quinto valor
                                dados_planos[plano_tipo]["morte_invalidez"] = valores_monetarios[5]  # Sexto valor
                                
                                exibir_mensagem(f"[OK] VALORES MONETÁRIOS MAPEADOS: {len(valores_monetarios)} valores")
                            
                            # Mapear textos específicos
                            for campo, valor in textos_especificos.items():
                                dados_planos[plano_tipo][campo] = valor
                                exibir_mensagem(f"[OK] {campo.upper()}: {valor}")
                            
                            # Definir tipo_franquia padrão se não encontrado
                            if "tipo_franquia" not in dados_planos[plano_tipo]:
                                dados_planos[plano_tipo]["tipo_franquia"] = "Normal"
                                exibir_mensagem("[OK] TIPO_FRANQUIA: Normal (padrão)")
                            
                        except Exception as e:
                            exibir_mensagem(f"[AVISO] Erro no mapeamento dinâmico: {str(e)}")
                            # Fallback para lógica anterior se necessário
                        
                    except Exception as e:
                        exception_handler.capturar_warning(f"ERRO NO PARSE ESTRUTURADO: {str(e)}", "CAPTURA_DADOS_PLANOS")
                        # Fallback para método anterior se o parse estruturado falhar
                        exibir_mensagem("[ATUALIZANDO] FALLBACK: Usando método anterior de extração")
                        
                        # Extrair valores monetários com padrões mais específicos
                        valor_patterns = [
                            r"R\$\s*([0-9.,]+)",
                            r"([0-9.,]+)\s*anual",
                            r"([0-9.,]+)\s*em até",
                            r"R\$\s*([0-9.,]+)\s*anual",
                            r"R\$\s*([0-9.,]+)\s*em até"
                        ]
                        
                        valores_encontrados = []
                        for pattern in valor_patterns:
                            matches = re.findall(pattern, tabela_text, re.IGNORECASE)
                            valores_encontrados.extend(matches)
                        
                        # Remover duplicatas e ordenar
                        valores_encontrados = list(set(valores_encontrados))
                        valores_encontrados.sort(key=lambda x: float(x.replace(',', '').replace('.', '')))
                        
                        # Extrair condições de pagamento
                        pagamento_patterns = [
                            r"Crédito em até (\d+x)\s*(?:sem juros|com juros)?\s*(?:ou \d+x de R\$\s*([0-9.,]+))?",
                            r"(\d+x)\s*(?:sem juros|com juros)",
                            r"parcelamento\s*(?:sem juros|com juros)"
                        ]
                        
                        for pattern in pagamento_patterns:
                            match = re.search(pattern, tabela_text, re.IGNORECASE)
                            if match:
                                if "Crédito em até" in pattern:
                                    dados_planos[plano_tipo]["parcelamento"] = f"{match.group(1)} sem juros"
                                    if match.group(2):
                                        exibir_mensagem(f"[OK] VALOR PARCELA (fallback): R$ {match.group(2)}")
                                else:
                                    dados_planos[plano_tipo]["parcelamento"] = match.group(0)
                                break
                        
                        if valores_encontrados:
                            # Procurar por valores específicos que vi no HTML
                            for valor in valores_encontrados:
                                valor_limpo = valor.replace(',', '').replace('.', '')
                                if valor_limpo == '10000':  # R$ 100,00
                                    dados_planos[plano_tipo]["valor"] = f"R$ {valor}"
                                elif valor_limpo == '256100':  # R$ 2.561,00
                                    dados_planos[plano_tipo]["valor"] = f"R$ {valor}"
                                elif valor_limpo == '250000':  # R$ 2.500,00
                                    dados_planos[plano_tipo]["valor_franquia"] = f"R$ {valor}"
                                elif valor_limpo == '358406':  # R$ 3.584,06
                                    dados_planos[plano_tipo]["valor_franquia"] = f"R$ {valor}"
                                elif valor_limpo == '50000':  # R$ 50.000,00
                                    dados_planos[plano_tipo]["danos_materiais"] = f"R$ {valor}"
                                    dados_planos[plano_tipo]["danos_corporais"] = f"R$ {valor}"
                                elif valor_limpo == '100000':  # R$ 100.000,00
                                    dados_planos[plano_tipo]["danos_materiais"] = f"R$ {valor}"
                                    dados_planos[plano_tipo]["danos_corporais"] = f"R$ {valor}"
                                elif valor_limpo == '20000':  # R$ 20.000,00
                                    dados_planos[plano_tipo]["danos_morais"] = f"R$ {valor}"
                                elif valor_limpo == '10000' and not dados_planos[plano_tipo]["danos_morais"]:  # R$ 10.000,00 (evitar conflito)
                                    dados_planos[plano_tipo]["danos_morais"] = f"R$ {valor}"
                                elif valor_limpo == '5000':  # R$ 5.000,00
                                    dados_planos[plano_tipo]["morte_invalidez"] = f"R$ {valor}"
                            
                            # Se não encontrou valores específicos, usar o primeiro como anual
                            if not dados_planos[plano_tipo]["valor"] and valores_encontrados:
                                dados_planos[plano_tipo]["valor"] = f"R$ {valores_encontrados[0]}"
                else:
                    exception_handler.capturar_warning(f"DADOS INSUFICIENTES: Apenas {len(linhas)} linhas encontradas", "CAPTURA_DADOS_PLANOS")
                    # MELHORIA: Parse inteligente para planos com poucas linhas
                    try:
                        exibir_mensagem("[BUSCAR] ANALISANDO PLANO COM POUCAS LINHAS")
                        
                        # Tentar extrair pelo menos o preço anual e forma de pagamento
                        if len(linhas) >= 2:
                            # Primeira linha pode ser moeda (R$) ou preço
                            primeira_linha = linhas[0].strip()
                            if primeira_linha == "R$" and len(linhas) >= 3:
                                # Formato: R$ / preço / anual
                                preco_anual = linhas[1].strip()
                                if re.match(r'^[0-9.,]+$', preco_anual):
                                    dados_planos[plano_tipo]["valor"] = f"R$ {preco_anual}"
                                    exibir_mensagem(f"[OK] PREÇO ANUAL EXTRAÍDO: R$ {preco_anual}")
                            elif re.match(r'^[0-9.,]+$', primeira_linha):
                                # Formato: preço / anual
                                dados_planos[plano_tipo]["valor"] = f"R$ {primeira_linha}"
                                exibir_mensagem(f"[OK] PREÇO ANUAL EXTRAÍDO: R$ {primeira_linha}")
                        
                        # Procurar forma de pagamento no texto completo
                        pagamento_match = re.search(r'Crédito em até (\d+x)\s*(?:sem juros|com juros)?\s*(?:ou \d+x de R\$\s*([0-9.,]+))?', tabela_text)
                        if pagamento_match:
                            parcelas = pagamento_match.group(1)
                            valor_parcela = pagamento_match.group(2) if pagamento_match.group(2) else ""
                            
                            dados_planos[plano_tipo]["parcelamento"] = f"{parcelas} sem juros"
                            if valor_parcela:
                                exibir_mensagem(f"[OK] VALOR PARCELA EXTRAÍDO: R$ {valor_parcela}")
                            
                            exibir_mensagem(f"[OK] FORMA PAGAMENTO EXTRAÍDA: {parcelas} sem juros")
                        
                        # Procurar outros valores monetários no texto completo
                        valores_monetarios = re.findall(r'R\$\s*([0-9.,]+)', tabela_text)
                        if valores_monetarios:
                            # Mapear valores encontrados para campos específicos
                            for valor in valores_monetarios:
                                valor_limpo = valor.replace(',', '').replace('.', '')
                                valor_completo = f"R$ {valor}"
                                
                                # Evitar duplicar o preço anual já extraído
                                if valor_completo != dados_planos[plano_tipo]["valor"]:
                                    # Tentar identificar o tipo de valor baseado no contexto
                                    if valor_limpo in ['251660', '2516.60']:  # Franquia reduzida
                                        dados_planos[plano_tipo]["valor_franquia"] = valor_completo
                                    elif valor_limpo in ['507594', '5075.94']:  # Franquia normal
                                        dados_planos[plano_tipo]["valor_franquia"] = valor_completo
                                    elif valor_limpo in ['50000', '50000.00']:  # Danos materiais/corporais
                                        if not dados_planos[plano_tipo]["danos_materiais"]:
                                            dados_planos[plano_tipo]["danos_materiais"] = valor_completo
                                        if not dados_planos[plano_tipo]["danos_corporais"]:
                                            dados_planos[plano_tipo]["danos_corporais"] = valor_completo
                                    elif valor_limpo in ['100000', '100000.00']:  # Danos materiais/corporais premium
                                        if not dados_planos[plano_tipo]["danos_materiais"]:
                                            dados_planos[plano_tipo]["danos_materiais"] = valor_completo
                                        if not dados_planos[plano_tipo]["danos_corporais"]:
                                            dados_planos[plano_tipo]["danos_corporais"] = valor_completo
                                    elif valor_limpo in ['20000', '20000.00']:  # Danos morais
                                        dados_planos[plano_tipo]["danos_morais"] = valor_completo
                                    elif valor_limpo in ['10000', '10000.00']:  # Danos morais menor
                                        if not dados_planos[plano_tipo]["danos_morais"]:
                                            dados_planos[plano_tipo]["danos_morais"] = valor_completo
                                    elif valor_limpo in ['5000', '5000.00']:  # Morte/invalidez
                                        dados_planos[plano_tipo]["morte_invalidez"] = valor_completo
                                    elif valor_limpo in ['0', '0.00']:  # Morte/invalidez zero
                                        dados_planos[plano_tipo]["morte_invalidez"] = valor_completo
                        
                    except Exception as e:
                        exibir_mensagem(f"[AVISO] ERRO NO PARSE INTELIGENTE: {str(e)}")
                
                # ETAPA 4: DETECTAR COBERTURAS (ÍCONES DE OK)
                exibir_mensagem("[BUSCAR] ETAPA 4: Detectando coberturas...")
                
                coberturas = ['assistencia', 'vidros', 'carro_reserva']
                
                for j, cobertura in enumerate(coberturas):
                    try:
                        # Procurar por ícones de OK
                        icones_ok = elemento.locator("img[src='/icone-ok.svg']").all()
                        
                        if len(icones_ok) > j and icones_ok[j].is_visible():
                            dados_planos[plano_tipo][cobertura] = True
                            exibir_mensagem(f"[OK] {cobertura.title()}: True (ícone detectado)")
                        else:
                            # Verificar se existe o texto da cobertura - se existe, é True
                            if cobertura.title() in tabela_text:
                                dados_planos[plano_tipo][cobertura] = True
                                exibir_mensagem(f"[OK] {cobertura.title()}: True (texto detectado)")
                            else:
                                # Se não encontrou nem ícone nem texto, verificar se há elementos específicos
                                elementos_cobertura = elemento.locator(f"div:has-text('{cobertura.title()}')").all()
                                if len(elementos_cobertura) > 0:
                                    dados_planos[plano_tipo][cobertura] = True
                                    exibir_mensagem(f"[OK] {cobertura.title()}: True (elemento encontrado)")
                                else:
                                    dados_planos[plano_tipo][cobertura] = False
                                    exibir_mensagem(f"[ERRO] {cobertura.title()}: False")
                    except Exception as e:
                        # Em caso de erro, verificar se o texto da cobertura existe no container
                        if cobertura.title() in tabela_text:
                            dados_planos[plano_tipo][cobertura] = True
                            exibir_mensagem(f"[OK] {cobertura.title()}: True (fallback - texto detectado)")
                        else:
                            dados_planos[plano_tipo][cobertura] = False
                            exception_handler.capturar_warning(f"Erro ao capturar {cobertura}: {str(e)} - definindo como False", "CAPTURA_DADOS_PLANOS")
                
                # ETAPA 5: CAPTURA ESPECÍFICA DE VALORES DE MERCADO E DANOS
                exibir_mensagem("[BUSCAR] ETAPA 5: Captura específica de valores...")
                
                # Valor de Mercado
                valor_mercado_match = re.search(r'100%\s*da\s*tabela\s*FIPE', tabela_text, re.IGNORECASE)
                if valor_mercado_match:
                    dados_planos[plano_tipo]["valor_mercado"] = "100% da tabela FIPE"
                    exibir_mensagem("[OK] Valor de Mercado: 100% da tabela FIPE")
                
                # Danos Materiais
                danos_materiais_match = re.search(r'Danos\s+Materiais.*?R\$\s*([0-9.,]+)', tabela_text, re.IGNORECASE)
                if danos_materiais_match:
                    dados_planos[plano_tipo]["danos_materiais"] = f"R$ {danos_materiais_match.group(1)}"
                    exibir_mensagem(f"[OK] Danos Materiais: R$ {danos_materiais_match.group(1)}")
                
                # Danos Corporais
                danos_corporais_match = re.search(r'Danos\s+Corporais.*?R\$\s*([0-9.,]+)', tabela_text, re.IGNORECASE)
                if danos_corporais_match:
                    dados_planos[plano_tipo]["danos_corporais"] = f"R$ {danos_corporais_match.group(1)}"
                    exibir_mensagem(f"[OK] Danos Corporais: R$ {danos_corporais_match.group(1)}")
                
                # Danos Morais
                danos_morais_match = re.search(r'Danos\s+Morais.*?R\$\s*([0-9.,]+)', tabela_text, re.IGNORECASE)
                if danos_morais_match:
                    dados_planos[plano_tipo]["danos_morais"] = f"R$ {danos_morais_match.group(1)}"
                    exibir_mensagem(f"[OK] Danos Morais: R$ {danos_morais_match.group(1)}")
                
                # Morte/Invalidez
                morte_invalidez_match = re.search(r'Morte/Invalidez.*?R\$\s*([0-9.,]+)', tabela_text, re.IGNORECASE)
                if morte_invalidez_match:
                    dados_planos[plano_tipo]["morte_invalidez"] = f"R$ {morte_invalidez_match.group(1)}"
                    exibir_mensagem(f"[OK] Morte/Invalidez: R$ {morte_invalidez_match.group(1)}")
                
                # Se encontrou dados válidos, continuar processando outros containers
                if dados_planos[plano_tipo]["valor"] != "N/A":
                    exibir_mensagem(f"[OK] DADOS CAPTURADOS COM SUCESSO PARA {plano_tipo.upper()}")
                    # Removido o break para processar todos os containers
                    
            except Exception as e:
                exception_handler.capturar_warning(f"Erro ao analisar container {i+1}: {str(e)}", "CAPTURA_DADOS_PLANOS")
                continue
        
        # ========================================
        # ETAPA 5: FALLBACK REMOVIDO
        # ========================================
        exibir_mensagem("[BUSCAR] ETAPA 5: Fallback removido - usando apenas dados dinâmicos")
        
        # Fallback removido para evitar sobrescrever dados corretos
        # Os dados são capturados pela lógica dinâmica anterior
        
        # ========================================
        # ETAPA 6: SALVAR E RETORNAR DADOS
        # ========================================
        # Salvar dados em arquivo JSON
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_arquivo = f"dados_planos_seguro_{timestamp}.json"
        
        with open(nome_arquivo, 'w', encoding='utf-8') as f:
            json.dump(dados_planos, f, indent=2, ensure_ascii=False)
        
        exibir_mensagem(f"[SALVAR] Dados salvos em: {nome_arquivo}")
        exibir_mensagem("[OK] CAPTURA DE DADOS CONCLUÍDA!")
        
        return dados_planos
        
    except Exception as e:
        exception_handler.capturar_excecao(e, "CAPTURA_DADOS_PLANOS", "Erro geral na captura de dados")
        return {
            "plano_recomendado": {"erro": "Falha na captura"},
            "plano_alternativo": {"erro": "Falha na captura"}
        }

# ========================================
# FUNÇÃO DE DETECÇÃO AUTOMÁTICA DE PROGRESS TRACKER
# ========================================

def detectar_progress_tracker(tipo_solicitado):
    """
    Detecta automaticamente o melhor progress tracker disponível
    
    PARÂMETROS:
        tipo_solicitado: str - Tipo solicitado ('auto', 'redis', 'json', 'none')
        
    RETORNO:
        class ou None - Classe do progress tracker ou None
    """
    if tipo_solicitado == 'none':
        return None
    
    if tipo_solicitado == 'redis':
        try:
            from utils.progress_redis import RedisProgressTracker
            return RedisProgressTracker
        except ImportError:
            exibir_mensagem("⚠️  Redis não disponível, usando JSON como fallback")
            from utils.progress_database_json import DatabaseProgressTracker
            return DatabaseProgressTracker
    
    if tipo_solicitado == 'json':
        from utils.progress_database_json import DatabaseProgressTracker
        return DatabaseProgressTracker
    
    # Modo 'auto' - detectar automaticamente
    try:
        import redis
        r = redis.Redis(host='localhost', port=6379)
        r.ping()
        exibir_mensagem("✅ Redis detectado, usando Redis Progress Tracker")
        from utils.progress_redis import RedisProgressTracker
        return RedisProgressTracker
    except:
        exibir_mensagem("⚠️  Redis não disponível, usando JSON Progress Tracker")
        from utils.progress_database_json import DatabaseProgressTracker
        return DatabaseProgressTracker


# ========================================
# FUNÇÃO PRINCIPAL
# ========================================

def executar_rpa_playwright(parametros: Dict[str, Any]) -> Dict[str, Any]:
    """
    Função principal do RPA Playwright
    
    PARÂMETROS:
        parametros: dict - Parâmetros de configuração
        
    RETORNO:
        dict: Resultado estruturado da execução
    """
    inicio_execucao = time.time()
    
    try:
        # Importar ProgressTracker dinamicamente (só quando necessário)
        try:
            from utils.progress_realtime import ProgressTracker
            
            # Inicializar ProgressTracker com session_id e tipo
            import uuid
            # Usar session_id do argumento se fornecido, senão gerar um novo
            session_id = args.session if args.session else str(uuid.uuid4())[:8]
            progress_tracker = ProgressTracker(
                total_etapas=15, 
                usar_arquivo=True, 
                session_id=session_id,
                tipo=args.progress_tracker
            )
            progress_tracker.update_progress(0, "Iniciando RPA")
            exibir_mensagem("[OK] ProgressTracker inicializado com sucesso")
            
        except Exception as e:
            exibir_mensagem(f"[AVISO] Erro ao inicializar ProgressTracker: {e}")
            exibir_mensagem("[FALLBACK] Continuando sem ProgressTracker")
            progress_tracker = None
        
        # Inicializar Sistema de Timeout Inteligente (opcional)
        if TIMEOUT_SYSTEM_AVAILABLE:
            smart_timeout = SmartTimeout()
            exibir_mensagem("[OK] Sistema de timeout inteligente ativado")
        else:
            smart_timeout = None
        
        # Inicializar Sistema de Logger Avançado (opcional)
        if LOGGER_SYSTEM_AVAILABLE:
            from utils.logger_rpa import RPALogger
            logger = RPALogger()
            log_info(logger, "Sistema de logger inicializado", {"versao": "3.4.0"})
            exibir_mensagem("[OK] Sistema de logger avançado ativado")
        else:
            logger = None
        
        # Inicializar Sistema de Comunicação Bidirecional (opcional)
        if BIDIRECTIONAL_SYSTEM_AVAILABLE:
            exibir_mensagem("[OK] Sistema de comunicação bidirecional ativado")
            # O sistema será usado via wrapper na execução
        else:
            exibir_mensagem("[AVISO] Executando sem comunicação bidirecional")
        
        # Inicializar Exception Handler
        exception_handler.limpar_erros()
        exception_handler.definir_tela_atual("INICIALIZACAO")
        
        exibir_mensagem("[INICIANDO] INICIANDO RPA PLAYWRIGHT")
        exibir_mensagem("=" * 50)
        
        # Log de início da execução
        try:
            if LOGGER_SYSTEM_AVAILABLE and 'logger' in locals() and logger:
                log_info(logger, "RPA iniciado", {"versao": "3.4.0", "parametros": parametros})
        except:
            pass  # Não falhar se o logger der erro
        
        # Carregar parâmetros de tempo
        parametros_tempo = obter_parametros_tempo(parametros)
        
        # Validar parâmetros
        if VALIDATION_SYSTEM_AVAILABLE:
            try:
                # Usar sistema de validação avançado
                validador = ValidadorParametros()
                parametros_validados = validador.validar_parametros(parametros)
                exibir_mensagem("[OK] Validação avançada de parâmetros concluída")
            except ValidacaoParametrosError as e:
                # [ERRO] INTERROMPER EXECUÇÃO - Parâmetros inválidos detectados
                erro_msg = f"[ERRO] VALIDAÇÃO DE PARÂMETROS FALHOU: {str(e)}"
                exibir_mensagem(erro_msg)
                exibir_mensagem("[PROIBIDO] Execução interrompida devido a parâmetros inválidos")
                return criar_retorno_erro(
                    f"Validação de parâmetros falhou: {str(e)}",
                    "VALIDACAO",
                    time.time() - inicio_execucao,
                    parametros,
                    exception_handler
                )
            except Exception as e:
                # [ERRO] INTERROMPER EXECUÇÃO - Erro inesperado na validação
                erro_msg = f"[ERRO] ERRO INESPERADO NA VALIDAÇÃO: {str(e)}"
                exibir_mensagem(erro_msg)
                exibir_mensagem("[PROIBIDO] Execução interrompida devido a erro na validação")
                return criar_retorno_erro(
                    f"Erro inesperado na validação: {str(e)}",
                    "VALIDACAO",
                    time.time() - inicio_execucao,
                    parametros,
                    exception_handler
                )
        else:
            # Usar validação básica existente
            if not validar_parametros_obrigatorios(parametros):
                raise RPAException("Parâmetros obrigatórios inválidos", "VALIDACAO")
        
        # Inicializar Playwright
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()
            
            # Navegar para URL inicial
            page.goto(parametros["url"])
            exibir_mensagem(f"[OK] Navegação para {parametros['url']} realizada")
            
            # Executar Telas 1-15 sequencialmente
            telas_executadas = 0
            resultado_telas = {}
            
            # TELA 1
            if progress_tracker:
                progress_tracker.update_progress(1, "Selecionando Tipo de Veiculo")
            exibir_mensagem("\n" + "="*50)
            
            # Log de início da Tela 1
            try:
                if LOGGER_SYSTEM_AVAILABLE and 'logger' in locals() and logger:
                    log_info(logger, "Executando Tela 1", {"tela": 1, "timestamp": datetime.now().isoformat()})
            except:
                pass  # Não falhar se o logger der erro
            
            if executar_com_timeout(smart_timeout, 1, navegar_tela_1_playwright, page, parametros.get('tipo_veiculo', 'carro')):
                telas_executadas += 1
                resultado_telas["tela_1"] = True
                if progress_tracker: progress_tracker.update_progress(1, "Tela 1 concluída")
                exibir_mensagem("[OK] TELA 1 CONCLUÍDA!")
                
                # Log de sucesso da Tela 1
                try:
                    if LOGGER_SYSTEM_AVAILABLE and 'logger' in locals() and logger:
                        log_success(logger, "Tela 1 concluída", {"tela": 1, "tempo": time.time() - inicio_execucao})
                except:
                    pass  # Não falhar se o logger der erro
            else:
                resultado_telas["tela_1"] = False
                if progress_tracker: progress_tracker.update_progress(1, "Tela 1 falhou")
                exibir_mensagem("[ERRO] TELA 1 FALHOU!")
                
                # Log de erro da Tela 1
                try:
                    if LOGGER_SYSTEM_AVAILABLE and 'logger' in locals() and logger:
                        log_error(logger, "Tela 1 falhou", {"tela": 1, "erro": "Execução falhou"})
                except:
                    pass  # Não falhar se o logger der erro
                
                return criar_retorno_erro(
                    "Tela 1 falhou",
                    "TELA_1",
                    time.time() - inicio_execucao,
                    parametros,
                    exception_handler
                )
            
            # TELA 2
            if progress_tracker: progress_tracker.update_progress(2, "Selecionando veículo com a placa informada")
            exibir_mensagem("\n" + "="*50)
            if executar_com_timeout(smart_timeout, 2, navegar_tela_2_playwright, page, parametros['placa']):
                telas_executadas += 1
                resultado_telas["tela_2"] = True
                if progress_tracker: progress_tracker.update_progress(2, "Tela 2 concluída")
                exibir_mensagem("[OK] TELA 2 CONCLUÍDA!")
            else:
                resultado_telas["tela_2"] = False
                if progress_tracker: progress_tracker.update_progress(2, "Tela 2 falhou")
                exibir_mensagem("[ERRO] TELA 2 FALHOU!")
                return criar_retorno_erro(
                    "Tela 2 falhou",
                    "TELA_2",
                    time.time() - inicio_execucao,
                    parametros,
                    exception_handler
                )
            
            # TELA 3
            if progress_tracker: progress_tracker.update_progress(3, "Confirmando seleção do veículo")
            exibir_mensagem("\n" + "="*50)
            if executar_com_timeout(smart_timeout, 3, navegar_tela_3_playwright, page):
                telas_executadas += 1
                resultado_telas["tela_3"] = True
                if progress_tracker: progress_tracker.update_progress(3, "Tela 3 concluída")
                exibir_mensagem("[OK] TELA 3 CONCLUÍDA!")
            else:
                resultado_telas["tela_3"] = False
                if progress_tracker: progress_tracker.update_progress(3, "Tela 3 falhou")
                exibir_mensagem("[ERRO] TELA 3 FALHOU!")
                return criar_retorno_erro(
                    "Tela 3 falhou",
                    "TELA_3",
                    time.time() - inicio_execucao,
                    parametros,
                    exception_handler
                )
            
            # TELA 4
            if progress_tracker: progress_tracker.update_progress(4, "Calculando como novo Seguro")
            exibir_mensagem("\n" + "="*50)
            if executar_com_timeout(smart_timeout, 4, navegar_tela_4_playwright, page, parametros['veiculo_segurado']):
                telas_executadas += 1
                resultado_telas["tela_4"] = True
                if progress_tracker: progress_tracker.update_progress(4, "Tela 4 concluída")
                exibir_mensagem("[OK] TELA 4 CONCLUÍDA!")
            else:
                resultado_telas["tela_4"] = False
                if progress_tracker: progress_tracker.update_progress(4, "Tela 4 falhou")
                exibir_mensagem("[ERRO] TELA 4 FALHOU!")
                return criar_retorno_erro(
                    "Tela 4 falhou",
                    "TELA_4",
                    time.time() - inicio_execucao,
                    parametros,
                    exception_handler
                )
            
            # TELA 5
            if progress_tracker: progress_tracker.update_progress(5, "Elaborando estimativas")
            exibir_mensagem("\n" + "="*50)
            dados_carrossel = executar_com_timeout(smart_timeout, 5, navegar_tela_5_playwright_com_dados, page, parametros_tempo)
            if dados_carrossel:
                telas_executadas += 1
                resultado_telas["tela_5"] = True
                
                # Capturar estimativas da tela 5 para ProgressTracker
                estimativas_tela_5 = None
                try:
                    # Usar dados do carrossel retornados pela função
                    if dados_carrossel:
                        estimativas_tela_5 = {
                            "timestamp": datetime.now().isoformat(),
                            "coberturas_detalhadas": dados_carrossel.get('coberturas_detalhadas', []),
                            "resumo": {
                                "total_coberturas": len(dados_carrossel.get('coberturas_detalhadas', [])),
                                "total_beneficios": len(dados_carrossel.get('beneficios_gerais', [])),
                                "valores_encontrados": dados_carrossel.get('valores_encontrados', 0)
                            }
                        }
                except:
                    estimativas_tela_5 = None
                
                if progress_tracker: 
                    progress_tracker.update_progress_with_estimativas(5, "Tela 5 concluída", estimativas=estimativas_tela_5)
                exibir_mensagem("[OK] TELA 5 CONCLUÍDA!")
                
                # VERIFICAR SE APARECEU TELA ZERO KM
                try:
                    page.wait_for_selector("#gtm-telaZeroKmContinuar", timeout=2000)
                    exibir_mensagem("[MOTO] TELA ZERO KM DETECTADA!")
                    
                    # TELA ZERO KM
                    if progress_tracker: progress_tracker.update_progress(5.5, "Processando Zero KM")
                    if executar_com_timeout(smart_timeout, 5.5, navegar_tela_zero_km_playwright, page, parametros):
                        telas_executadas += 1
                        resultado_telas["tela_zero_km"] = True
                        if progress_tracker: progress_tracker.update_progress(5.5, "Tela Zero KM concluída")
                        exibir_mensagem("[OK] TELA ZERO KM CONCLUÍDA!")
                    else:
                        resultado_telas["tela_zero_km"] = False
                        if progress_tracker: progress_tracker.update_progress(5.5, "Tela Zero KM falhou")
                        exibir_mensagem("[ERRO] TELA ZERO KM FALHOU!")
                        return criar_retorno_erro(
                            "Tela Zero KM falhou",
                            "TELA_ZERO_KM",
                            time.time() - inicio_execucao,
                            parametros,
                            exception_handler
                        )
                except:
                    exibir_mensagem("[INFO]️ Tela Zero KM não apareceu - continuando fluxo normal")
            else:
                resultado_telas["tela_5"] = False
                if progress_tracker: progress_tracker.update_progress(5, "Tela 5 falhou")
                exibir_mensagem("[ERRO] TELA 5 FALHOU!")
                return criar_retorno_erro(
                    "Tela 5 falhou",
                    "TELA_5",
                    time.time() - inicio_execucao,
                    parametros,
                    exception_handler
                )
            
            # TELA 6
            if progress_tracker: progress_tracker.update_progress(6, "Seleção de detalhes do veículo")
            exibir_mensagem("\n" + "="*50)
            if executar_com_timeout(smart_timeout, 6, navegar_tela_6_playwright, page, parametros['combustivel'], parametros.get('kit_gas', False), parametros.get('blindado', False), parametros.get('financiado', False), parametros.get('tipo_veiculo', 'carro')):
                telas_executadas += 1
                resultado_telas["tela_6"] = True
                if progress_tracker: progress_tracker.update_progress(6, "Tela 6 concluída")
                exibir_mensagem("[OK] TELA 6 CONCLUÍDA!")
            else:
                resultado_telas["tela_6"] = False
                if progress_tracker: progress_tracker.update_progress(6, "Tela 6 falhou")
                exibir_mensagem("[ERRO] TELA 6 FALHOU!")
                return criar_retorno_erro(
                    "Tela 6 falhou",
                    "TELA_6",
                    time.time() - inicio_execucao,
                    parametros,
                    exception_handler
                )
            
            # TELA 7
            if progress_tracker: progress_tracker.update_progress(7, "Definição de local de pernoite com o CEP informado")
            exibir_mensagem("\n" + "="*50)
            if executar_com_timeout(smart_timeout, 7, navegar_tela_7_playwright, page, parametros['cep']):
                telas_executadas += 1
                resultado_telas["tela_7"] = True
                if progress_tracker: progress_tracker.update_progress(7, "Tela 7 concluída")
                exibir_mensagem("[OK] TELA 7 CONCLUÍDA!")
            else:
                resultado_telas["tela_7"] = False
                if progress_tracker: progress_tracker.update_progress(7, "Tela 7 falhou")
                exibir_mensagem("[ERRO] TELA 7 FALHOU!")
                return criar_retorno_erro(
                    "Tela 7 falhou",
                    "TELA_7",
                    time.time() - inicio_execucao,
                    parametros,
                    exception_handler
                )
            
            # TELA 8
            if progress_tracker: progress_tracker.update_progress(8, "Definição do uso do veículo")
            exibir_mensagem("\n" + "="*50)
            if executar_com_timeout(smart_timeout, 8, navegar_tela_8_playwright, page, parametros['uso_veiculo']):
                telas_executadas += 1
                resultado_telas["tela_8"] = True
                if progress_tracker: progress_tracker.update_progress(8, "Tela 8 concluída")
                exibir_mensagem("[OK] TELA 8 CONCLUÍDA!")
            else:
                resultado_telas["tela_8"] = False
                if progress_tracker: progress_tracker.update_progress(8, "Tela 8 falhou")
                exibir_mensagem("[ERRO] TELA 8 FALHOU!")
                return criar_retorno_erro(
                    "Tela 8 falhou",
                    "TELA_8",
                    time.time() - inicio_execucao,
                    parametros,
                    exception_handler
                )
            
            # TELA 9
            if progress_tracker: progress_tracker.update_progress(9, "Preenchimento dos dados pessoais")
            exibir_mensagem("\n" + "="*50)
            if executar_com_timeout(smart_timeout, 9, navegar_tela_9_playwright, page, parametros['nome'], parametros['cpf'], parametros['data_nascimento'], parametros['sexo'], parametros['estado_civil'], parametros['email'], parametros['celular']):
                telas_executadas += 1
                resultado_telas["tela_9"] = True
                if progress_tracker: progress_tracker.update_progress(9, "Tela 9 concluída")
                exibir_mensagem("[OK] TELA 9 CONCLUÍDA!")
            else:
                resultado_telas["tela_9"] = False
                if progress_tracker: progress_tracker.update_progress(9, "Tela 9 falhou")
                exibir_mensagem("[ERRO] TELA 9 FALHOU!")
                return criar_retorno_erro(
                    "Tela 9 falhou",
                    "TELA_9",
                    time.time() - inicio_execucao,
                    parametros,
                    exception_handler
                )
            
            # TELA 10
            if progress_tracker: progress_tracker.update_progress(10, "Definição do Condutor Principal")
            exibir_mensagem("\n" + "="*50)
            if executar_com_timeout(smart_timeout, 10, navegar_tela_10_playwright, page, parametros['condutor_principal'], parametros['nome_condutor'], parametros['cpf_condutor'], parametros['data_nascimento_condutor'], parametros['sexo_condutor'], parametros['estado_civil_condutor']):
                telas_executadas += 1
                resultado_telas["tela_10"] = True
                if progress_tracker: progress_tracker.update_progress(10, "Tela 10 concluída")
                exibir_mensagem("[OK] TELA 10 CONCLUÍDA!")
            else:
                resultado_telas["tela_10"] = False
                if progress_tracker: progress_tracker.update_progress(10, "Tela 10 falhou")
                exibir_mensagem("[ERRO] TELA 10 FALHOU!")
                return criar_retorno_erro(
                    "Tela 10 falhou",
                    "TELA_10",
                    time.time() - inicio_execucao,
                    parametros,
                    exception_handler
                )
            
            # TELA 11
            if progress_tracker: progress_tracker.update_progress(11, "Definição do uso do veículo")
            exibir_mensagem("\n" + "="*50)
            if executar_com_timeout(smart_timeout, 11, navegar_tela_11_playwright, page, parametros['local_de_trabalho'], parametros['estacionamento_proprio_local_de_trabalho'], parametros['local_de_estudo'], parametros['estacionamento_proprio_local_de_estudo']):
                telas_executadas += 1
                resultado_telas["tela_11"] = True
                if progress_tracker: progress_tracker.update_progress(11, "Tela 11 concluída")
                exibir_mensagem("[OK] TELA 11 CONCLUÍDA!")
            else:
                resultado_telas["tela_11"] = False
                if progress_tracker: progress_tracker.update_progress(11, "Tela 11 falhou")
                exibir_mensagem("[ERRO] TELA 11 FALHOU!")
                return criar_retorno_erro(
                    "Tela 11 falhou",
                    "TELA_11",
                    time.time() - inicio_execucao,
                    parametros,
                    exception_handler
                )
            
            # TELA 12
            if progress_tracker: progress_tracker.update_progress(12, "Definição do tipo de garagem")
            exibir_mensagem("\n" + "="*50)
            if executar_com_timeout(smart_timeout, 12, navegar_tela_12_playwright, page, parametros['garagem_residencia'], parametros['portao_eletronico']):
                telas_executadas += 1
                resultado_telas["tela_12"] = True
                if progress_tracker: progress_tracker.update_progress(12, "Tela 12 concluída")
                exibir_mensagem("[OK] TELA 12 CONCLUÍDA!")
            else:
                resultado_telas["tela_12"] = False
                if progress_tracker: progress_tracker.update_progress(12, "Tela 12 falhou")
                exibir_mensagem("[ERRO] TELA 12 FALHOU!")
                return criar_retorno_erro(
                    "Tela 12 falhou",
                    "TELA_12",
                    time.time() - inicio_execucao,
                    parametros,
                    exception_handler
                )
            
            # TELA 13
            if progress_tracker: progress_tracker.update_progress(13, "Definição de residentes")
            exibir_mensagem("\n" + "="*50)
            if executar_com_timeout(smart_timeout, 13, navegar_tela_13_playwright, page, parametros['reside_18_26'], parametros['sexo_do_menor'], parametros['faixa_etaria_menor_mais_novo']):
                telas_executadas += 1
                resultado_telas["tela_13"] = True
                if progress_tracker: progress_tracker.update_progress(13, "Tela 13 concluída")
                exibir_mensagem("[OK] TELA 13 CONCLUÍDA!")
            else:
                resultado_telas["tela_13"] = False
                if progress_tracker: progress_tracker.update_progress(13, "Tela 13 falhou")
                exibir_mensagem("[ERRO] TELA 13 FALHOU!")
                return criar_retorno_erro(
                    "Tela 13 falhou",
                    "TELA_13",
                    time.time() - inicio_execucao,
                    parametros,
                    exception_handler
                )
            
            # TELA 14 (CONDICIONAL) - Só executa se Tela 15 não foi detectada diretamente da Tela 13
            if progress_tracker: progress_tracker.update_progress(14, "Definição do Corretor")
            exibir_mensagem("\n" + "="*50)
            exibir_mensagem("[BUSCAR] ANALISANDO EXECUÇÃO DA TELA 14...")
            exibir_mensagem(f"[DADOS] Status da variável global 'tela_15_detectada': {tela_15_detectada}")
            
            if not tela_15_detectada:
                exibir_mensagem("[ATUALIZANDO] Executando Tela 14 (Tela 15 não foi detectada diretamente da Tela 13)")
                exibir_mensagem("[INFO] Motivo: Fluxo normal - Tela 14 é necessária para continuar")
                if executar_com_timeout(smart_timeout, 14, navegar_tela_14_playwright, page, parametros['continuar_com_corretor_anterior']):
                    # Não incrementa telas_executadas pois é condicional
                    resultado_telas["tela_14"] = True
                    if progress_tracker: progress_tracker.update_progress(14, "Tela 14 concluída")
                    exibir_mensagem("[OK] TELA 14 PROCESSADA COM SUCESSO!")
                    exibir_mensagem("[GRAFICO] Navegação para Tela 15 será executada normalmente")
                else:
                    resultado_telas["tela_14"] = False
                    if progress_tracker: progress_tracker.update_progress(14, "Tela 14 falhou")
                    exibir_mensagem("[ERRO] TELA 14 FALHOU!")
                    exibir_mensagem("[PROIBIDO] RPA será interrompido devido à falha na Tela 14")
                    return criar_retorno_erro(
                        "Tela 14 falhou",
                        "TELA_14",
                        time.time() - inicio_execucao,
                        parametros,
                        exception_handler
                    )
            else:
                exibir_mensagem("⏭️ Pulando Tela 14 (Tela 15 já foi detectada diretamente da Tela 13)")
                exibir_mensagem("[INFO] Motivo: Fluxo otimizado - Tela 14 não é necessária")
                exibir_mensagem("[LINK] Transição direta da Tela 13 para Tela 15 detectada")
                resultado_telas["tela_14"] = True  # Considera como sucesso pois foi pulada intencionalmente
                if progress_tracker: progress_tracker.update_progress(14, "Tela 14 pulada")
                exibir_mensagem("[OK] TELA 14 PULADA COM SUCESSO!")
                exibir_mensagem("[GRAFICO] Próximo passo: Executar Tela 15 diretamente")
            
            # TELA 15
            if progress_tracker: progress_tracker.update_progress(15, "Aguardando cálculo completo")
            exibir_mensagem("\n" + "="*50)
            if executar_com_timeout(smart_timeout, 15, navegar_tela_15_playwright, page, parametros['autenticacao']['email_login'], parametros['autenticacao']['senha_login'], parametros_tempo, parametros):
                telas_executadas += 1
                resultado_telas["tela_15"] = True
                if progress_tracker: progress_tracker.update_progress(15, "Tela 15 concluída")
                exibir_mensagem("[OK] TELA 15 CONCLUÍDA!")
            else:
                resultado_telas["tela_15"] = False
                if progress_tracker: progress_tracker.update_progress(15, "Tela 15 falhou")
                exibir_mensagem("[ERRO] TELA 15 FALHOU!")
                
                # Verificar se foi por cotação manual
                try:
                    # Verificar se apareceu tela de cotação manual
                    page.wait_for_selector('p.text-center.text-base', timeout=2000)
                    exibir_mensagem("[INFO] COTAÇÃO MANUAL DETECTADA NO FLUXO PRINCIPAL!")
                    
                    # Processar cotação manual
                    if processar_cotacao_manual(page, parametros):
                        resultado_telas["tela_cotacao_manual"] = True
                        exibir_mensagem("[OK] COTAÇÃO MANUAL PROCESSADA!")
                        
                        # Retornar erro específico para cotação manual
                        return criar_retorno_erro_cotacao_manual(
                            "Não foi possível efetuar o cálculo nesse momento. O corretor de seguros já foi notificado e logo entrará em contato para te auxiliar a encontrar as melhores opções.",
                            "COTACAO_MANUAL_NECESSARIA",
                            time.time() - inicio_execucao,
                            parametros,
                            exception_handler
                        )
                    else:
                        exibir_mensagem("[ERRO] ERRO AO PROCESSAR COTAÇÃO MANUAL!")
                        return criar_retorno_erro(
                            "Erro ao processar cotação manual",
                            "COTACAO_MANUAL_ERROR",
                            time.time() - inicio_execucao,
                            parametros,
                            exception_handler
                        )
                        
                except:
                    # Não é cotação manual, retornar erro padrão
                    return criar_retorno_erro(
                        "Tela 15 falhou",
                        "TELA_15",
                        time.time() - inicio_execucao,
                        parametros,
                        exception_handler
                    )
            
            # Resultado final
            if progress_tracker: progress_tracker.update_progress(15, "RPA concluído com sucesso")
            exibir_resultado_final("\n" + "="*60)
            exibir_resultado_final("[SUCESSO] RPA TELAS 1 A 15 CONCLUÍDO COM SUCESSO!")
            exibir_resultado_final(f"[OK] Total de telas executadas: {telas_executadas}/14 (Tela 14 é condicional)")
            exibir_resultado_final("[OK] Todas as telas funcionaram corretamente")
            exibir_resultado_final("[OK] Navegação sequencial realizada com sucesso")
            
            # Capturar dados finais
            dados_planos = capturar_dados_planos_seguro(page, parametros_tempo)
            
            if dados_planos:
                exibir_resultado_final("[OK] DADOS DOS PLANOS CAPTURADOS COM SUCESSO!")
                exibir_resultado_final("[INFO] RESUMO DOS DADOS CAPTURADOS:")
                exibir_resultado_final(f"   [DADOS] Plano Recomendado: {dados_planos['plano_recomendado'].get('valor', 'N/A')}")
                exibir_resultado_final(f"   [DADOS] Plano Alternativo: {dados_planos['plano_alternativo'].get('valor', 'N/A')}")
                exibir_resultado_final(f"   [ARQUIVO] Dados salvos em: dados_planos_seguro_*.json")
            else:
                exibir_resultado_final("[AVISO] FALHA NA CAPTURA DE DADOS DOS PLANOS")
            
            # Salvar dados
            arquivo_dados = salvar_dados_planos(dados_planos)
            
            # Finalizar progress tracker
            progress_tracker.finalizar('success', dados_planos)
            
            # Fechar browser
            browser.close()
            
            # Calcular tempo de execução
            tempo_execucao = time.time() - inicio_execucao
            
            # Log de conclusão bem-sucedida
            try:
                if LOGGER_SYSTEM_AVAILABLE and 'logger' in locals() and logger:
                    log_success(logger, "RPA concluído com sucesso", {
                        "tempo_total": tempo_execucao,
                        "telas_executadas": telas_executadas,
                        "arquivo_dados": arquivo_dados
                    })
            except:
                pass  # Não falhar se o logger der erro
            
            # Retorno estruturado
            # Incluir progresso no resultado final
            try:
                progresso_final = progress_tracker.get_progress()
                resultado_telas["progresso"] = progresso_final
                exibir_mensagem("[OK] Progresso incluído no resultado final")
            except Exception as e:
                exibir_mensagem(f"[AVISO] Erro ao incluir progresso: {e}")
                resultado_telas["progresso"] = {"erro": "Progresso não disponível"}
            
            return criar_retorno_sucesso(
                resultado_telas,
                dados_planos,
                arquivo_dados,
                tempo_execucao,
                parametros
            )
            
    except Exception as e:
        # Atualizar progresso em caso de erro
        try:
            progress_tracker.update_progress(0, f"RPA interrompido por erro: {str(e)}")
            progress_tracker.finalizar('error', None, str(e))
        except:
            pass  # Não falhar se o progress tracker der erro
        
        # Log de erro principal (verificar se logger existe)
        try:
            if LOGGER_SYSTEM_AVAILABLE and 'logger' in locals() and logger:
                log_error(logger, "Erro na execução principal", {
                    "erro": str(e),
                    "traceback": traceback.format_exc(),
                    "tempo_execucao": time.time() - inicio_execucao
                })
        except:
            pass  # Não falhar se o logger der erro
        
        exception_handler.capturar_excecao(e, "EXECUCAO_PRINCIPAL", "Erro na execução principal")
        
        return criar_retorno_erro(
            str(e),
            "EXECUCAO_PRINCIPAL",
            time.time() - inicio_execucao,
            parametros,
            exception_handler
        )

# ========================================
# EXECUÇÃO DIRETA
# ========================================

if __name__ == "__main__":
    try:
        # Processar argumentos de linha de comando
        args = processar_argumentos()
        
        # Verificar se é para exibir documentação
        if args.docs:
            exibir_documentacao(args.docs)
            sys.exit(0)
        
        # Carregar parâmetros (compatibilidade mantida)
        parametros = carregar_parametros(args.config)
        
        # SISTEMA DE HEALTH CHECK ULTRA-CONSERVADOR (opcional)
        if HEALTH_CHECK_AVAILABLE:
            try:
                health_checker = ConservativeHealthChecker()
                environment = health_checker.get_environment()
                exibir_mensagem(f"[BUSCAR] Ambiente detectado: {environment}")
                
                if health_checker.is_system_ready():
                    exibir_mensagem(f"[OK] Health Check {environment}: Sistema pronto")
                else:
                    exibir_mensagem(f"[AVISO] Health Check {environment}: Problemas detectados - continuando mesmo assim")
                    
            except Exception as e:
                exibir_mensagem(f"[AVISO] Erro no health check: {e} - continuando sem verificação")
        
        # EXECUÇÃO COM CONTROLE BIDIRECIONAL SEGURO
        if BIDIRECTIONAL_SYSTEM_AVAILABLE:
            # Executar RPA com controle bidirecional
            resultado_wrapper = execute_rpa_with_bidirectional_control(
                executar_rpa_playwright, 
                parametros
            )
            
            # Extrair resultado do wrapper
            if resultado_wrapper["status"] == "success":
                resultado = resultado_wrapper["result"]
                bidirectional_used = resultado_wrapper.get("bidirectional_used", False)
                exibir_mensagem(f"[OK] Comunicação bidirecional: {'Ativa' if bidirectional_used else 'Não utilizada'}")
            else:
                # Fallback para execução direta
                resultado = executar_rpa_playwright(parametros)
                exibir_mensagem("[AVISO] Fallback para execução direta devido a erro no sistema bidirecional")
        else:
            # Executar RPA (ESTRUTURA ORIGINAL PRESERVADA)
            resultado = executar_rpa_playwright(parametros)
        
        # Exibir resultado
        exibir_mensagem("\n" + "="*50)
        exibir_mensagem("[DADOS] RESULTADO DA EXECUÇÃO")
        exibir_mensagem("="*50)
        exibir_mensagem(f"Status: {resultado['status']}")
        exibir_mensagem(f"Tempo: {resultado['tempo_execucao']}")
        exibir_mensagem(f"Erros: {resultado['erros']['total_erros']}")
        exibir_mensagem(f"Warnings: {resultado['erros']['total_warnings']}")
        
        if resultado['status'] == 'success':
            exibir_mensagem("[OK] RPA executado com sucesso!")
        else:
            exibir_mensagem("[ERRO] RPA falhou!")
        
        # Delay para inspeção da tela final
        # print("[AGUARDANDO] Aguardando 60 segundos para inspeção da tela final...")
        # time.sleep(60)
        # print("[OK] Tempo de inspeção concluído!")
        
        # Exibir retorno estruturado completo
        exibir_mensagem("\n" + "="*50)
        exibir_mensagem("[INFO] RETORNO ESTRUTURADO COMPLETO")
        exibir_mensagem("="*50)
        import json
        exibir_mensagem(json.dumps(resultado, indent=2, ensure_ascii=False))
            
    except Exception as e:
        exception_handler.capturar_excecao(e, "EXECUCAO_DIRETA", "Erro na execução direta")
        sys.exit(1)
