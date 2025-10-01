# RELATÓRIO DE ANÁLISE: CAPTURA DE ESTIMATIVAS VIA PHP

## RESUMO EXECUTIVO

**Problema Identificado:** O sistema RPA não captura estimativas quando executado via PHP, resultando em `dados_extra` vazio e funcionalidade principal comprometida.

**Causa Raiz:** O parâmetro `--modo-silencioso` suprime todas as mensagens de debug, ocultando falhas na captura de dados e impedindo o diagnóstico adequado.

**Solução:** Remover `--modo-silencioso` do wrapper script para restaurar a visibilidade de logs e garantir a captura de estimativas.

---

## 1. CONTEXTO E IMPACTO

### 1.1 Funcionalidade Principal
- **Objetivo:** Capturar estimativas de seguro e valores finais do cálculo
- **Importância:** Funcionalidade crítica - sem ela o sistema não serve para nada
- **Status Atual:** Funciona manualmente, falha via PHP

### 1.2 Impacto no Negócio
- **Modal:** Mostra "Dados extra não disponíveis" em vez de estimativas
- **Usuário:** Não recebe informações de cobertura e valores
- **Sistema:** Funcionalidade principal comprometida

---

## 2. ANÁLISE TÉCNICA DETALHADA

### 2.1 Fluxo de Execução

#### Execução Manual (Funciona)
```bash
python3 executar_rpa_modular_telas_1_a_5.py --session teste --progress-tracker json
```
- **DISPLAY_ENABLED:** `True`
- **Logs:** Visíveis
- **Captura:** Estimativas completas
- **Resultado:** `dados_extra` com estimativas

#### Execução via PHP (Falha)
```bash
python3 executar_rpa_modular_telas_1_a_5.py --session teste --progress-tracker json --modo-silencioso
```
- **DISPLAY_ENABLED:** `False`
- **Logs:** Suprimidos
- **Captura:** Falha silenciosa
- **Resultado:** `dados_extra` vazio

### 2.2 Código Crítico Analisado

#### Configuração de Display (Linhas 1053-1062)
```python
modo_silencioso = configuracao.get('modo_silencioso', False) or args.modo_silencioso
DISPLAY_ENABLED = display and visualizar_mensagens and not modo_silencioso

# Detectar se estamos em ambiente de servidor (sem display X)
if not os.environ.get('DISPLAY') or modo_silencioso:
    DISPLAY_ENABLED = False
```

#### Função de Exibição (Linhas 1123-1126)
```python
def exibir_mensagem(mensagem: str):
    if DISPLAY_ENABLED:  # ← AQUI ESTÁ O PROBLEMA
        timestamp = time.strftime('%H:%M:%S')
        mensagem_limpa = limpar_emojis_windows(mensagem)
        print(f"[{timestamp}] {mensagem_limpa}")
```

#### Captura de Dados (Linhas 4224-4234)
```python
# DEBUG: Verificar quais elementos estão na página
exibir_mensagem("[BUSCAR] DEBUG: Verificando elementos na página...")

# Estratégia 1.1: Buscar por elementos que contenham "Cobertura" e valores monetários
exibir_mensagem("[BUSCAR] DEBUG: Estratégia 1.1 - Buscando cards com 'Cobertura'...")

# Buscar por elementos que contenham "Cobertura" e "R$" no mesmo contexto
cards_cobertura = page.locator("div:has-text('Cobertura'):has-text('R$')")
exibir_mensagem(f"[BUSCAR] DEBUG: Cards com 'Cobertura' e 'R$' encontrados: {cards_cobertura.count()}")
```

### 2.3 Efeito em Cascata

#### 1. Mensagens de Debug Suprimidas
- `aguardar_cards_estimativa_playwright()`: Falhas não visíveis
- `capturar_dados_carrossel_estimativas_playwright()`: Erros ocultos
- `navegar_tela_5_playwright()`: Tentativas não logadas

#### 2. Falhas Silenciosas
- Seletores CSS podem falhar sem logs
- Timeouts podem ocorrer sem aviso
- Elementos podem não ser encontrados sem debug

#### 3. ProgressTracker Não Recebe Dados
```python
# Linha 1819-1831: Só executa se dados_carrossel existir
if progress_tracker and dados_carrossel and dados_carrossel.get('coberturas_detalhadas'):
    estimativas_tela_5 = {
        "timestamp": datetime.now().isoformat(),
        "coberturas_detalhadas": dados_carrossel.get('coberturas_detalhadas', []),
        "resumo": {
            "total_coberturas": len(dados_carrossel.get('coberturas_detalhadas', [])),
            "total_beneficios": len(dados_carrossel.get('beneficios_gerais', [])),
            "valores_encontrados": dados_carrossel.get('valores_encontrados', 0)
        }
    }
    progress_tracker.update_progress_with_estimativas(5, "Tela 5 concluída", estimativas=estimativas_tela_5)
else:
    # dados_carrossel é None ou vazio - não salva nada
```

---

## 3. EVIDÊNCIAS EMPÍRICAS

### 3.1 Testes Realizados

#### Teste 1: Execução Manual
```bash
python3 executar_rpa_modular_telas_1_a_5.py --session teste_manual --progress-tracker json
```
**Resultado:**
```json
{
  "dados_extra": {
    "estimativas_tela_5": {
      "coberturas_detalhadas": [
        {
          "indice": 1,
          "nome_cobertura": "CompreensivaDe",
          "valores": {
            "de": "R$ 2.400,00",
            "ate": "R$ 2.900,00"
          },
          "beneficios": [20 benefícios incluídos]
        }
      ]
    }
  }
}
```

#### Teste 2: Execução via PHP
```bash
python3 executar_rpa_modular_telas_1_a_5.py --session teste_php --progress-tracker json --modo-silencioso
```
**Resultado:**
```json
{
  "dados_extra": {},
  "erros": [],
  "session_id": "teste_php"
}
```

### 3.2 Arquivos Gerados

#### Execução Manual
- `temp/json_compreensivo_tela_5_20250929_161428.json` (14.117 bytes)
- `temp/retorno_intermediario_carrossel_20250929_161428.json` (7.445 bytes)
- `rpa_data/progress_teste_manual_estimativas.json` (5.493 bytes)

#### Execução via PHP
- Nenhum arquivo de tela 5 gerado
- `rpa_data/progress_teste_php.json` (318 bytes - apenas estrutura básica)

---

## 4. ANÁLISE DE CAUSA RAIZ

### 4.1 Por Que o Modo Silencioso Foi Implementado?
- **Objetivo:** Reduzir logs em produção
- **Contexto:** Execução via PHP em servidor
- **Problema:** Suprime logs críticos de debug

### 4.2 Por Que Funciona Manualmente?
- **DISPLAY_ENABLED:** `True`
- **Logs:** Visíveis para diagnóstico
- **Debug:** Falhas são detectadas e corrigidas

### 4.3 Por Que Falha via PHP?
- **DISPLAY_ENABLED:** `False`
- **Logs:** Suprimidos
- **Debug:** Falhas ficam ocultas
- **Resultado:** `dados_carrossel` fica `None`

---

## 5. SOLUÇÕES PROPOSTAS

### 5.1 Solução Principal (Recomendada)

#### Remover --modo-silencioso do Wrapper
```bash
# ANTES
python3 executar_rpa_modular_telas_1_a_5.py --session "$1" --progress-tracker json --modo-silencioso

# DEPOIS
python3 executar_rpa_modular_telas_1_a_5.py --session "$1" --progress-tracker json
```

**Vantagens:**
- Solução simples e direta
- Restaura visibilidade de logs
- Não altera lógica do RPA
- Mantém funcionalidade completa

**Desvantagens:**
- Aumenta volume de logs
- Pode impactar performance mínima

### 5.2 Solução Alternativa

#### Usar exibir_resultado_final() nas Funções Críticas
```python
# Substituir exibir_mensagem() por exibir_resultado_final() nas funções críticas
def exibir_resultado_final(mensagem: str):
    """Exibe resultado final sempre, mesmo no modo silencioso"""
    timestamp = time.strftime('%H:%M:%S')
    mensagem_limpa = limpar_emojis_windows(mensagem)
    print(f"[{timestamp}] {mensagem_limpa}")
```

**Vantagens:**
- Mantém modo silencioso para logs não críticos
- Preserva logs críticos de captura

**Desvantagens:**
- Requer modificação do código RPA
- Mais complexa de implementar

### 5.3 Solução Híbrida

#### Modo Silencioso Inteligente
```python
# Adicionar flag para logs críticos
CRITICAL_LOGS_ENABLED = True

def exibir_mensagem_critica(mensagem: str):
    """Exibe mensagens críticas sempre"""
    if DISPLAY_ENABLED or CRITICAL_LOGS_ENABLED:
        timestamp = time.strftime('%H:%M:%S')
        mensagem_limpa = limpar_emojis_windows(mensagem)
        print(f"[{timestamp}] {mensagem_limpa}")
```

---

## 6. RECOMENDAÇÃO FINAL

### 6.1 Solução Imediata
**Remover `--modo-silencioso` do wrapper script**

### 6.2 Justificativa
1. **Simplicidade:** Mudança mínima e direta
2. **Eficácia:** Resolve o problema imediatamente
3. **Segurança:** Não altera lógica do RPA
4. **Diagnóstico:** Restaura capacidade de debug

### 6.3 Implementação
```bash
# Modificar executar_rpa_wrapper_debug.sh
PLAYWRIGHT_BROWSERS_PATH=/opt/imediatoseguros-rpa/.playwright python3 executar_rpa_modular_telas_1_a_5.py --session "$1" --progress-tracker json
```

### 6.4 Validação
1. Executar teste via PHP
2. Verificar logs de debug
3. Confirmar captura de estimativas
4. Validar modal com dados

---

## 7. CONCLUSÃO

O problema da captura de estimativas via PHP é causado pela supressão de logs de debug através do parâmetro `--modo-silencioso`. Esta supressão oculta falhas na captura de dados, resultando em `dados_extra` vazio e comprometendo a funcionalidade principal do sistema.

A solução é simples: remover `--modo-silencioso` do wrapper script para restaurar a visibilidade de logs e garantir a captura adequada de estimativas. Esta mudança resolve o problema sem alterar a lógica do RPA e mantém a funcionalidade completa do sistema.

**Status:** Problema identificado e solução definida
**Próximo Passo:** Implementar correção no wrapper script
**Impacto:** Restaura funcionalidade principal do sistema


