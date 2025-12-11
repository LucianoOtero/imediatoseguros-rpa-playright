# 🔧 IMPLEMENTAÇÃO DA NOVA LÓGICA DE DETECÇÃO

## 📊 **RESUMO DA IMPLEMENTAÇÃO**

### ✅ **MUDANÇAS IMPLEMENTADAS**

#### **1. Nova Ordem de Detecção**
- **ANTES**: Modal de login → Login → Aguarda tela final
- **AGORA**: Aguarda tela final → Modal de login → Login → Captura dados

#### **2. Timeouts Otimizados**
- **Tela Final**: 180 segundos (3 minutos)
- **Modal de Login**: 10 segundos
- **Cotação Manual**: 10 segundos (era 180 segundos)

#### **3. Fluxo Corrigido**
```python
# ETAPA 1: PRIMEIRO - Aguardar tela final com resultados (REGRA)
page.wait_for_selector("text=Parabéns, chegamos ao resultado final da cotação!", timeout=180000)

# ETAPA 2: Aguardar modal de login aparecer SOBRE a tela final
modal_login = page.locator("text=Acesse sua conta para visualizar o resultado final")
modal_login.wait_for(timeout=10000)

# ETAPA 3: Fazer login no modal
# ... código de login ...

# ETAPA 4: Capturar dados dos planos
dados_planos = capturar_dados_planos_seguro(page, parametros_tempo)
```

#### **4. Detecção de Cotação Manual (Exceção)**
```python
# ETAPA 3: SEGUNDO - Verificar se apareceu tela de cotação manual (EXCEÇÃO)
tela_cotacao_manual = page.locator('p.text-center.text-base')
tela_cotacao_manual.wait_for(timeout=10000)  # 10 segundos

# Verificar se o texto é realmente de cotação manual
texto_elemento = tela_cotacao_manual.text_content()
if "Ops, ainda não encontramos resultados para você" in texto_elemento:
    # Processar cotação manual e retornar erro 9003
    return processar_cotacao_manual(page, parametros)
```

### 🎯 **CENÁRIOS DE EXECUÇÃO**

#### **Cenário 1: Tela Final Aparece (Regra)**
1. ✅ Aguarda até 3 minutos pela tela final
2. ✅ Modal de login aparece sobre a tela
3. ✅ Login feito (email, senha, clicar)
4. ✅ Modal CPF divergente tratado (se aparecer)
5. ✅ Dados dos planos capturados
6. ✅ Retorna sucesso

#### **Cenário 2: Tela de Cotação Manual (Exceção)**
1. ❌ Tela final não aparece (timeout 3 minutos)
2. ✅ Tela de cotação manual aparece (10 segundos)
3. ✅ Valida texto "Ops, ainda não encontramos resultados..."
4. ✅ Processa cotação manual
5. ✅ Retorna erro 9003

#### **Cenário 3: Nada Aparece (Erro)**
1. ❌ Tela final não aparece (timeout 3 minutos)
2. ❌ Tela de cotação manual não aparece (timeout 10 segundos)
3. ✅ Retorna erro 9004

### 📋 **ARQUIVOS MODIFICADOS**

#### **executar_rpa_imediato_playwright.py**
- **Função**: `navegar_tela_15_playwright()`
- **Linhas modificadas**: 3869-4033
- **Mudanças**: Nova lógica de detecção implementada

#### **Backup Criado**
- **Arquivo**: `backup_executar_rpa_imediato_playwright_YYYYMMDD_HHMMSS.py`
- **Motivo**: Segurança antes da implementação

### 🔧 **CÓDIGO IMPLEMENTADO**

#### **Nova FASE 2**
```python
# ========================================
# FASE 2: AGUARDAR TELA POR BAIXO CARREGAR
# ========================================
exibir_mensagem("[ATUALIZANDO] FASE 2: Aguardando tela por baixo carregar...")
exibir_mensagem("[INFO] A tela pode demorar até 3 minutos para aparecer...")

# ETAPA 1: PRIMEIRO - Aguardar tela final com resultados (REGRA)
exibir_mensagem("[BUSCAR] Verificando se apareceu tela final com resultados...")
try:
    # Aguardar até 3 minutos pela tela final
    page.wait_for_selector("text=Parabéns, chegamos ao resultado final da cotação!", timeout=180000)
    exibir_mensagem("[OK] Página principal dos planos carregada!")
    
    # ETAPA 2: Aguardar modal de login aparecer SOBRE a tela final
    # ... código de login ...
    
    # ETAPA 3: Capturar dados dos planos
    dados_planos = capturar_dados_planos_seguro(page, parametros_tempo)
    return True
    
except Exception as e:
    # ETAPA 3: SEGUNDO - Verificar se apareceu tela de cotação manual (EXCEÇÃO)
    try:
        tela_cotacao_manual = page.locator('p.text-center.text-base')
        tela_cotacao_manual.wait_for(timeout=10000)
        
        texto_elemento = tela_cotacao_manual.text_content()
        if "Ops, ainda não encontramos resultados para você" in texto_elemento:
            return processar_cotacao_manual(page, parametros)
    except Exception as e2:
        pass
    
    # ETAPA 4: Se nada for detectado, retornar erro 9004
    return criar_retorno_erro_tela_final_nao_detectada(...)
```

### ✅ **VALIDAÇÃO**

#### **Sintaxe**
- ✅ Arquivo compila sem erros de sintaxe
- ✅ Função `navegar_tela_15_playwright()` modificada corretamente
- ✅ Lógica de detecção implementada

#### **Lógica**
- ✅ Ordem de prioridade correta (regra primeiro, exceção depois)
- ✅ Timeouts otimizados
- ✅ Detecção de cotação manual movida para o local correto
- ✅ Validação de texto implementada

### 🚀 **PRÓXIMOS PASSOS**

1. **Teste Local**: Executar com dados de teste
2. **Deploy**: Copiar arquivo para servidor
3. **Validação**: Testar cenários reais
4. **Monitoramento**: Verificar logs de execução

## 📊 **RESUMO TÉCNICO**

- **Arquivo**: `executar_rpa_imediato_playwright.py`
- **Função**: `navegar_tela_15_playwright()`
- **Linhas**: 3869-4033
- **Status**: ✅ Implementado
- **Sintaxe**: ✅ Válida
- **Backup**: ✅ Criado






