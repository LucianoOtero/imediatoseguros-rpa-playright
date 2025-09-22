# 🔍 AUDITORIA COMPLETA DE SELETORES GENÉRICOS - v1.2.0 (10/01/2025)

## 📋 **INFORMAÇÕES DA AUDITORIA**
- **Data**: 09/09/2025 (Auditoria Original) → **Atualizada**: 10/01/2025
- **Arquivo Analisado**: `executar_rpa_imediato_playwright.py`
- **Total de Linhas**: 4568 (atualizado)
- **Objetivo**: Identificar todos os seletores genéricos para substituição por específicos
- **Status**: ✅ **AUDITORIA CONCLUÍDA E ATUALIZADA**

---

## 🎯 **RESUMO EXECUTIVO**

### **📊 ESTATÍSTICAS GERAIS ATUALIZADAS**
- **Total de Seletores Genéricos Identificados**: 47
- **Seletores de Alto Risco Implementados**: 10 ✅
- **Seletores de Alto Risco Restantes**: 4 🔴
- **Seletores de Médio Risco**: 32 🟡
- **Seletores de Baixo Risco**: 1 🟢
- **Telas Afetadas**: 15 (todas as telas)
- **Tipos de Seletores Genéricos**: 8 categorias
- **Risco de Falha**: 🔴 **ALTO** → 🟡 **REDUZIDO** (10 de 14 alto risco implementados - 71.4%)

### **🚨 PROBLEMAS CRÍTICOS IDENTIFICADOS**
1. **Seletores baseados em classes CSS** - Falham em diferentes regiões
2. **Seletores por texto** - Sensíveis a mudanças de idioma/localização
3. **Seletores por atributos genéricos** - Instáveis com mudanças na UI
4. **Seletores por posição** - Quebram com mudanças de layout

---

## 📱 **ANÁLISE DETALHADA POR TELA**

### **TELA 1: Seleção do Tipo de Seguro**
**Função**: `navegar_tela_1_playwright()`

#### **✅ SELETOR IMPLEMENTADO**
1. **`button.group`** (Linha 745) ✅ **IMPLEMENTADO v3.7.0.1**
   - **Finalidade**: Selecionar botão "Carro"
   - **Problema**: Classe CSS genérica, pode mudar
   - **Risco**: 🔴 **ALTO** → 🟢 **RESOLVIDO**
   - **Alternativa Implementada**: `button:has(img[alt="Icone car"])`
   - **Status**: ✅ **IMPLEMENTADO E TESTADO COM SUCESSO**
   - **Data Implementação**: 09/09/2025
   - **Estratégia**: Híbrida com fallbacks múltiplos
   - **Teste**: ✅ Execução completa bem-sucedida (dados gerados às 14:20)

---

### **TELA 2: Inserção da Placa**
**Função**: `navegar_tela_2_playwright()`

#### **✅ SELETORES ESPECÍFICOS (OK)**
- `#placaTelaDadosPlaca` - Campo de placa
- `#gtm-telaDadosAutoCotarComPlacaContinuar` - Botão continuar

#### **🔴 SELETORES GENÉRICOS IDENTIFICADOS**
1. **`.first`** (Linhas 769, 775)
   - **Finalidade**: Acessar primeiro elemento encontrado
   - **Problema**: Depende de ordem dos elementos
   - **Risco**: 🟡 **MÉDIO**

---

### **TELA 3: Confirmação do Veículo**
**Função**: `navegar_tela_3_playwright()`

#### **✅ SELETORES ESPECÍFICOS (OK)**
- `#gtm-telaInfosAutoContinuar` - Botão continuar

---

### **TELA 4: Veículo Segurado**
**Função**: `navegar_tela_4_playwright()`

#### **✅ SELETORES ESPECÍFICOS (OK)**
- `#gtm-telaRenovacaoVeiculoContinuar` - Botão continuar

---

### **TELA 5: Estimativa Inicial**
**Função**: `navegar_tela_5_playwright()`

#### **✅ SELETOR IMPLEMENTADO**
1. **`div.bg-primary`** (Linha 854) ✅ **IMPLEMENTADO v3.7.0.2-main**
   - **Finalidade**: Detectar cards de estimativa
   - **Problema**: Classe CSS genérica, pode mudar
   - **Risco**: 🔴 **ALTO** → 🟢 **RESOLVIDO**
   - **Alternativa Implementada**: `div[role="group"][aria-roledescription="slide"]`
   - **Status**: ✅ **IMPLEMENTADO E TESTADO COM SUCESSO**
   - **Data Implementação**: 09/09/2025
   - **Estratégia**: Híbrida com fallbacks múltiplos
   - **Funções Auxiliares**: `aguardar_cards_estimativa_playwright()`, `localizar_cards_estimativa_playwright()`

2. **`text=R$`** (Linha 867)
   - **Finalidade**: Detectar elementos com preços
   - **Problema**: Depende de texto específico
   - **Risco**: 🟡 **MÉDIO**
   - **Alternativa Sugerida**: `[data-testid="preco-estimativa"]`

3. **`text=Continuar`** (Linha 1051)
   - **Finalidade**: Fallback para botão continuar
   - **Problema**: Texto pode mudar
   - **Risco**: 🟡 **MÉDIO**
   - **Alternativa Sugerida**: `#gtm-telaEstimativaContinuarParaCotacaoFinal`

---

### **TELA 6: Itens do Veículo**
**Função**: `navegar_tela_6_playwright()`

#### **🔴 SELETORES GENÉRICOS IDENTIFICADOS**
1. **`input[name='tipoCombustivelTelaItens'][value='{valor_radio}']`** (Linha 1108)
   - **Finalidade**: Selecionar tipo de combustível
   - **Problema**: Depende de valor dinâmico
   - **Risco**: 🟡 **MÉDIO**
   - **Alternativa Sugerida**: IDs específicos por tipo

2. **`input[value="Kit Gás"]`** (Linha 1128)
   - **Finalidade**: Checkbox Kit Gás
   - **Problema**: Depende de valor específico
   - **Risco**: 🟡 **MÉDIO**
   - **Alternativa Sugerida**: `#checkbox-kit-gas`

3. **`input[value="Blindado"]`** (Linha 1146)
   - **Finalidade**: Checkbox Blindado
   - **Problema**: Depende de valor específico
   - **Risco**: 🟡 **MÉDIO**
   - **Alternativa Sugerida**: `#checkbox-blindado`

4. **`input[value="Financiado"]`** (Linha 1164)
   - **Finalidade**: Checkbox Financiado
   - **Problema**: Depende de valor específico
   - **Risco**: 🟡 **MÉDIO**
   - **Alternativa Sugerida**: `#checkbox-financiado`

---

### **TELA 7: Endereço**
**Função**: `navegar_tela_7_playwright()`

#### **🔴 SELETORES GENÉRICOS IDENTIFICADOS**
1. **`.overflow-hidden`** (Linha 1233) ✅ **IMPLEMENTADO v3.7.0.3-main**
   - **Finalidade**: Selecionar endereço sugerido
   - **Problema**: Classe CSS genérica
   - **Risco**: 🔴 **ALTO** → 🟢 **RESOLVIDO**
   - **Alternativa Implementada**: `[data-testid="sugestao-endereco"]`

2. **`document.querySelector('.overflow-hidden').classList.contains('selected')`** (Linha 1238) ✅ **IMPLEMENTADO v3.7.0.3-main**
   - **Finalidade**: Verificar se endereço está selecionado
   - **Problema**: JavaScript com classe genérica
   - **Risco**: 🔴 **ALTO** → 🟢 **RESOLVIDO**
   - **Alternativa Implementada**: `document.querySelector('[data-testid="sugestao-endereco"]').classList.contains('selected')`

---

### **TELA 8: Uso do Veículo**
**Função**: `navegar_tela_8_playwright()`

#### **🔴 SELETORES GENÉRICOS IDENTIFICADOS**
1. **`xpath=//*[contains(text(), 'finalidade') or contains(text(), 'uso')]`** (Linha 1250)
   - **Finalidade**: Detectar elementos da tela
   - **Problema**: XPath baseado em texto
   - **Risco**: 🟢 **RESOLVIDO**
   - **Status**: ✅ **IMPLEMENTADO v3.7.0.4**
   - **Alternativa Implementada**: `#finalidadeVeiculoTelaUsoVeiculo` + `[role="radiogroup"]` + `p:has-text("Qual é o uso do veículo?")`

2. **`xpath=//*[contains(text(), 'finalidade') or contains(text(), 'Finalidade') or contains(text(), 'uso') or contains(text(), 'Uso') or contains(text(), 'veículo')]`** (Linha 1269)
   - **Finalidade**: Detectar elementos da tela
   - **Problema**: XPath complexo baseado em texto
   - **Risco**: 🔴 **ALTO**
   - **Alternativa Sugerida**: `[data-testid="tela-uso-veiculo"]`

3. **`input[value="{valor_radio}"][name="finalidadeVeiculoTelaUsoVeiculo"]`** (Linha 1297)
   - **Finalidade**: Selecionar uso do veículo
   - **Problema**: Depende de valor dinâmico
   - **Risco**: 🟡 **MÉDIO**
   - **Alternativa Sugerida**: IDs específicos por uso

---

### **TELA 9: Dados Pessoais**
**Função**: `navegar_tela_9_playwright()`

#### **✅ SELETORES IMPLEMENTADOS**
1. **`xpath=//*[contains(text(), 'dados pessoais') or contains(text(), 'Dados pessoais')]`** ✅ **IMPLEMENTADO v3.7.0.5**
   - **Finalidade**: Detectar elementos da tela
   - **Problema**: XPath baseado em texto
   - **Risco**: 🔴 **ALTO** → 🟢 **RESOLVIDO**
   - **Alternativa Implementada**: `#dadosPessoaisTelaSegurado` + `[role="radiogroup"]` + `p:has-text("Dados pessoais")`
   - **Status**: ✅ **IMPLEMENTADO E TESTADO COM SUCESSO**
   - **Data Implementação**: 10/09/2025
   - **Estratégia**: Híbrida com fallbacks múltiplos

2. **`xpath=//li[contains(text(), 'Casado') or contains(text(), 'Solteiro') or contains(text(), 'Divorciado') or contains(text(), 'Viúvo') or contains(text(), 'Separado')]`** ✅ **IMPLEMENTADO v3.7.0.8**
   - **Finalidade**: Selecionar estado civil
   - **Problema**: XPath complexo baseado em texto
   - **Risco**: 🔴 **ALTO** → 🟢 **RESOLVIDO**
   - **Alternativa Implementada**: `li[data-value="{valor}"]` + `li[role="option"]` + `li.MuiMenuItem-root`
   - **Status**: ✅ **IMPLEMENTADO E TESTADO COM SUCESSO**
   - **Data Implementação**: 10/01/2025
   - **Estratégia**: Híbrida com 4 níveis de fallback

3. **`xpath=//li[contains(text(), '" + variacao + "')]`** ✅ **IMPLEMENTADO v3.7.0.8**
   - **Finalidade**: Selecionar variação de estado civil
   - **Problema**: XPath dinâmico baseado em texto
   - **Risco**: 🔴 **ALTO** → 🟢 **RESOLVIDO**
   - **Alternativa Implementada**: Função `localizar_estado_civil_playwright()` com estratégia híbrida
   - **Status**: ✅ **IMPLEMENTADO E TESTADO COM SUCESSO**
   - **Data Implementação**: 10/01/2025

#### **✅ SELETORES IMPLEMENTADOS**
4. **`text={sexo}`** ✅ **IMPLEMENTADO v3.7.0.10**
   - **Finalidade**: Selecionar opção de sexo
   - **Problema**: Depende de texto específico
   - **Risco**: 🔴 **ALTO** → 🟢 **RESOLVIDO**
   - **Alternativa Implementada**: Função `localizar_sexo_playwright()` com estratégia híbrida
   - **Status**: ✅ **IMPLEMENTADO E TESTADO COM SUCESSO**
   - **Data Implementação**: 10/01/2025
   - **Estratégia**: Híbrida com 5 níveis de fallback

#### **✅ SELETORES ESPECÍFICOS (OK)**
- **Botão Continuar**: `#gtm-telaDadosSeguradoContinuar` - ✅ **ESPECÍFICO** (nunca foi genérico)

---

### **TELA 10: Condutor Principal**
**Função**: `navegar_tela_10_playwright()`

#### **✅ SELETORES IMPLEMENTADOS**
1. **`input[value="sim"][name="condutorPrincipalTelaCondutorPrincipal"]`** ✅ **IMPLEMENTADO v3.7.0.6**
   - **Finalidade**: Radio button "Sim"
   - **Problema**: Depende de valor específico
   - **Risco**: 🟡 **MÉDIO** → 🟢 **RESOLVIDO**
   - **Alternativa Implementada**: Função `localizar_radio_condutor_playwright()` com estratégia híbrida
   - **Status**: ✅ **IMPLEMENTADO E TESTADO COM SUCESSO**
   - **Data Implementação**: 10/09/2025
   - **Estratégia**: Híbrida com 4 níveis de fallback

2. **`input[value="nao"][name="condutorPrincipalTelaCondutorPrincipal"]`** ✅ **IMPLEMENTADO v3.7.0.6**
   - **Finalidade**: Radio button "Não"
   - **Problema**: Depende de valor específico
   - **Risco**: 🟡 **MÉDIO** → 🟢 **RESOLVIDO**
   - **Alternativa Implementada**: Função `localizar_radio_condutor_playwright()` com estratégia híbrida
   - **Status**: ✅ **IMPLEMENTADO E TESTADO COM SUCESSO**
   - **Data Implementação**: 10/09/2025

3. **`ul`** (Linha 1587)
   - **Finalidade**: Aguardar lista de opções
   - **Problema**: Tag genérica
   - **Risco**: 🟡 **MÉDIO**
   - **Alternativa Sugerida**: `[data-testid="lista-opcoes"]`

4. **`text={sexo_condutor}`** (Linha 1592)
   - **Finalidade**: Selecionar sexo do condutor
   - **Problema**: Depende de texto específico
   - **Risco**: 🟡 **MÉDIO**
   - **Alternativa Sugerida**: `[data-testid="opcao-sexo-condutor-{sexo}"]`

5. **`text={estado_civil_condutor}`** (Linha 1620)
   - **Finalidade**: Selecionar estado civil do condutor
   - **Problema**: Depende de texto específico
   - **Risco**: 🟡 **MÉDIO**
   - **Alternativa Sugerida**: `[data-testid="opcao-estado-civil-condutor-{estado}"]`

---

### **TELA 11: Atividade do Veículo**
**Função**: `navegar_tela_11_playwright()`

#### **✅ SELETORES IMPLEMENTADOS**
1. **`input[type="checkbox"][value="trabalho"]`** ✅ **IMPLEMENTADO v3.7.0.9**
   - **Finalidade**: Checkbox local de trabalho
   - **Problema**: Depende de valor específico
   - **Risco**: 🔴 **ALTO** → 🟢 **RESOLVIDO**
   - **Alternativa Implementada**: Função `localizar_checkbox_trabalho_playwright()` com estratégia híbrida
   - **Status**: ✅ **IMPLEMENTADO E TESTADO COM SUCESSO**
   - **Data Implementação**: 10/01/2025
   - **Estratégia**: Híbrida com 4 níveis de fallback

2. **`input[type="checkbox"][value="estudo"]`** ✅ **IMPLEMENTADO v3.7.0.9**
   - **Finalidade**: Checkbox local de estudo
   - **Problema**: Depende de valor específico
   - **Risco**: 🔴 **ALTO** → 🟢 **RESOLVIDO**
   - **Alternativa Implementada**: Função `localizar_checkbox_estudo_playwright()` com estratégia híbrida
   - **Status**: ✅ **IMPLEMENTADO E TESTADO COM SUCESSO**
   - **Data Implementação**: 10/01/2025

3. **`input[type="checkbox"][data-gtm-form-interact-field-id="10"]`** ✅ **IMPLEMENTADO v3.7.0.9**
   - **Finalidade**: Switch estacionamento trabalho
   - **Problema**: Depende de atributo GTM
   - **Risco**: 🔴 **ALTO** → 🟢 **RESOLVIDO**
   - **Alternativa Implementada**: Função `localizar_switch_trabalho_playwright()` com estratégia híbrida
   - **Status**: ✅ **IMPLEMENTADO E TESTADO COM SUCESSO**
   - **Data Implementação**: 10/01/2025

4. **`input[type="checkbox"][data-gtm-form-interact-field-id="11"]`** ✅ **IMPLEMENTADO v3.7.0.9**
   - **Finalidade**: Switch estacionamento estudo
   - **Problema**: Depende de atributo GTM
   - **Risco**: 🔴 **ALTO** → 🟢 **RESOLVIDO**
   - **Alternativa Implementada**: Função `localizar_switch_estudo_playwright()` com estratégia híbrida
   - **Status**: ✅ **IMPLEMENTADO E TESTADO COM SUCESSO**
   - **Data Implementação**: 10/01/2025

---

### **TELA 12: Garagem na Residência**
**Função**: `navegar_tela_12_playwright()`

#### **🔴 SELETORES GENÉRICOS IDENTIFICADOS**
1. **`p.font-semibold.font-workSans.cursor-pointer`** (Linha 1794)
   - **Finalidade**: Botão continuar
   - **Problema**: Classes CSS genéricas
   - **Risco**: 🔴 **ALTO**
   - **Alternativa Sugerida**: `#botao-continuar-garagem`

2. **`input[value="sim"][name="possuiGaragemTelaGaragemResidencia"]`** (Linha 1804)
   - **Finalidade**: Radio button "Sim"
   - **Problema**: Depende de valor específico
   - **Risco**: 🟡 **MÉDIO**
   - **Alternativa Sugerida**: `#radio-possui-garagem-sim`

3. **`input[value="nao"][name="possuiGaragemTelaGaragemResidencia"]`** (Linha 1844)
   - **Finalidade**: Radio button "Não"
   - **Problema**: Depende de valor específico
   - **Risco**: 🟡 **MÉDIO**
   - **Alternativa Sugerida**: `#radio-possui-garagem-nao`

4. **`input[value="eletronico"][name="tipoPortaoTelaGaragemResidencia"]`** (Linha 1820)
   - **Finalidade**: Radio button portão eletrônico
   - **Problema**: Depende de valor específico
   - **Risco**: 🟡 **MÉDIO**
   - **Alternativa Sugerida**: `#radio-portao-eletronico`

5. **`input[value="manual"][name="tipoPortaoTelaGaragemResidencia"]`** (Linha 1831)
   - **Finalidade**: Radio button portão manual
   - **Problema**: Depende de valor específico
   - **Risco**: 🟡 **MÉDIO**
   - **Alternativa Sugerida**: `#radio-portao-manual`

---

### **TELA 13: Residência com Menores**
**Função**: `navegar_tela_13_playwright()`

#### **🔴 SELETORES GENÉRICOS IDENTIFICADOS**
1. **`input[type='radio'][value='nao']`** (Linha 1933)
   - **Finalidade**: Radio button "Não"
   - **Problema**: Depende de valor específico
   - **Risco**: 🟡 **MÉDIO**
   - **Alternativa Sugerida**: `#radio-reside-menores-nao`

2. **`input[type='radio'][value='sim_nao_utilizam']`** (Linha 1948)
   - **Finalidade**: Radio button "Sim, mas não utilizam"
   - **Problema**: Depende de valor específico
   - **Risco**: 🟡 **MÉDIO**
   - **Alternativa Sugerida**: `#radio-reside-menores-sim-nao-utilizam`

3. **`input[type='radio'][value='sim_utilizam']`** (Linha 1957)
   - **Finalidade**: Radio button "Sim e utilizam"
   - **Problema**: Depende de valor específico
   - **Risco**: 🟡 **MÉDIO**
   - **Alternativa Sugerida**: `#radio-reside-menores-sim-utilizam`

---

### **TELA 14: Dados do Condutor Adicional**
**Função**: `navegar_tela_14_playwright()`

#### **🔴 SELETORES GENÉRICOS IDENTIFICADOS**
1. **`input[type='radio'][value='nao']`** (Linha 2003)
   - **Finalidade**: Radio button "Não"
   - **Problema**: Depende de valor específico
   - **Risco**: 🟡 **MÉDIO**
   - **Alternativa Sugerida**: `#radio-condutor-adicional-nao`

2. **`input[type='radio'][value='sim']`** (Linha 2010)
   - **Finalidade**: Radio button "Sim"
   - **Problema**: Depende de valor específico
   - **Risco**: 🟡 **MÉDIO**
   - **Alternativa Sugerida**: `#radio-condutor-adicional-sim`

3. **`ul`** (Linha 2025)
   - **Finalidade**: Aguardar lista de opções
   - **Problema**: Tag genérica
   - **Risco**: 🟡 **MÉDIO**
   - **Alternativa Sugerida**: `[data-testid="lista-opcoes-condutor"]`

4. **`text={sexo_condutor_adicional}`** (Linha 2030)
   - **Finalidade**: Selecionar sexo do condutor adicional
   - **Problema**: Depende de texto específico
   - **Risco**: 🟡 **MÉDIO**
   - **Alternativa Sugerida**: `[data-testid="opcao-sexo-condutor-adicional-{sexo}"]`

5. **`text={estado_civil_condutor_adicional}`** (Linha 2058)
   - **Finalidade**: Selecionar estado civil do condutor adicional
   - **Problema**: Depende de texto específico
   - **Risco**: 🟡 **MÉDIO**
   - **Alternativa Sugerida**: `[data-testid="opcao-estado-civil-condutor-adicional-{estado}"]`

---

### **TELA 15: Resultados Finais**
**Função**: `navegar_tela_15_playwright()`

#### **🔴 SELETORES GENÉRICOS IDENTIFICADOS**
1. **`//*[contains(text(), 'Plano recomendado')]`** (Linha 2896)
   - **Finalidade**: Detectar planos recomendados
   - **Problema**: XPath baseado em texto
   - **Risco**: 🔴 **ALTO**
   - **Alternativa Sugerida**: `[data-testid="plano-recomendado"]`

2. **`//div[contains(@class, 'md:w-80') or contains(@class, 'border-4') or contains(@class, 'border-primary')]`** (Linha 2899)
   - **Finalidade**: Detectar cards de planos
   - **Problema**: Classes CSS genéricas
   - **Risco**: 🔴 **ALTO**
   - **Alternativa Sugerida**: `[data-testid="card-plano"]`

3. **`//*[contains(text(), 'R$')]`** (Linha 2902)
   - **Finalidade**: Detectar elementos com preços
   - **Problema**: XPath baseado em texto
   - **Risco**: 🔴 **ALTO**
   - **Alternativa Sugerida**: `[data-testid="preco-plano"]`

---

## 📊 **RESUMO POR CATEGORIA DE RISCO ATUALIZADO**

### **🔴 RISCO ALTO (14 seletores)**
- **Implementados**: 10 ✅ (71.4%)
- **Restantes**: 4 ⏳ (28.6%)
- **Tipos**: Seletores baseados em classes CSS genéricas, XPath baseados em texto, JavaScript com classes genéricas

### **🟡 RISCO MÉDIO (32 seletores)**
- **Implementados**: 0 ⏳ (0%)
- **Restantes**: 32 ⏳ (100%)
- **Tipos**: Seletores baseados em valores específicos
- Seletores baseados em atributos GTM
- Seletores baseados em texto específico

### **🟢 RISCO BAIXO (1 seletor)**
- **Implementados**: 1 ✅ (100%)
- **Restantes**: 0 ✅ (0%)
- **Tipos**: Seletores por IDs específicos

### **📈 PROGRESSO GERAL**
- **Total de Seletores**: 47
- **Implementados**: 11 ✅ (23.4%)
- **Restantes**: 36 ⏳ (76.6%)
- **Foco Atual**: Seletores de Alto Risco (4 restantes)

---

## 🎯 **SELETORES DE ALTO RISCO RESTANTES (4)**

### **🔴 PENDENTES DE IMPLEMENTAÇÃO:**

1. **Tela 12**: `p.font-semibold.font-workSans.cursor-pointer` ✅ **IMPLEMENTADO v3.7.0.11**
   - **Finalidade**: Botão continuar garagem
   - **Risco**: 🔴 **ALTO** → ✅ **IMPLEMENTADO**
   - **Alternativa Implementada**: Estratégia híbrida com 5 níveis de fallback
   - **Função**: `localizar_botao_continuar_garagem_playwright()`

2. **Tela 15**: `//*[contains(text(), 'Plano recomendado')]` (Linha 3571)
   - **Finalidade**: Detecção de planos recomendados
   - **Risco**: 🔴 **ALTO**
   - **Alternativa Sugerida**: `[data-testid="plano-recomendado"]`

3. **Tela 15**: `//div[contains(@class, 'md:w-80')...]` (Linha 3574)
   - **Finalidade**: Detecção de cards de planos
   - **Risco**: 🔴 **ALTO**
   - **Alternativa Sugerida**: `[data-testid="card-plano"]`

4. **Tela 15**: `//*[contains(text(), 'R$')]` (Linha 3577)
   - **Finalidade**: Detecção de valores monetários
   - **Risco**: 🔴 **ALTO**
   - **Alternativa Sugerida**: `[data-testid="preco-plano"]`

### **✅ SELETORES DE ALTO RISCO IMPLEMENTADOS (11):**

1. **v3.7.0.1**: `button.group` → `button:has(img[alt="Icone car"])` (Tela 1)
2. **v3.7.0.2**: `div.bg-primary` → `div[role="group"][aria-roledescription="slide"]` (Tela 5)
3. **v3.7.0.3**: `.overflow-hidden` → `[data-testid="sugestao-endereco"]` (Tela 7)
4. **v3.7.0.4**: XPath finalidade → Estratégia híbrida (Tela 8)
5. **v3.7.0.5**: XPath dados pessoais → Estratégia híbrida (Tela 9)
6. **v3.7.0.6**: Radio buttons condutor → Estratégia híbrida (Tela 10)
7. **v3.7.0.8**: XPath estado civil → Estratégia híbrida (Tela 9)
8. **v3.7.0.9**: Checkboxes/switches → Estratégia híbrida (Tela 11)
9. **v3.7.0.9**: Switch estacionamento → Estratégia híbrida (Tela 11)
10. **v3.7.0.10**: `text={sexo}` → Estratégia híbrida (Tela 9)
11. **v3.7.0.11**: `p.font-semibold.font-workSans.cursor-pointer` → Estratégia híbrida (Tela 12)

---

## 🎯 **ESTRATÉGIA DE SUBSTITUIÇÃO RECOMENDADA**

### **FASE 1: Seletores de Alto Risco (Prioridade Crítica)**
1. **Classes CSS genéricas** → IDs específicos ou data-testid
2. **XPath baseados em texto** → Seletores por atributos específicos
3. **JavaScript com classes genéricas** → Seletores específicos

### **FASE 2: Seletores de Médio Risco (Prioridade Alta)**
1. **Valores específicos** → IDs específicos
2. **Atributos GTM** → IDs específicos
3. **Texto específico** → Seletores por atributos

### **FASE 3: Otimizações Finais (Prioridade Média)**
1. **Tags genéricas** → Seletores específicos
2. **Seletores dinâmicos** → Seletores estáticos
3. **Fallbacks** → Seletores primários específicos

---

## 🛡️ **MITIGAÇÃO DE RISCOS**

### **ESTRATÉGIA HÍBRIDA**
- **Primário**: Seletor específico (ID ou data-testid)
- **Fallback**: Seletor genérico atual
- **Validação**: Verificação de existência antes do uso

### **IMPLEMENTAÇÃO CONSERVADORA**
- **Teste por tela**: Implementar uma tela por vez
- **Validação extensiva**: Testar em ambas as regiões
- **Rollback automático**: Voltar ao seletor original em caso de falha

---

## 📋 **PRÓXIMOS PASSOS**

### **IMEDIATO (Hoje)**
1. ✅ Auditoria completa concluída
2. 🔄 Criar plano de implementação detalhado
3. 🔄 Identificar alternativas específicas para cada seletor
4. 🔄 Implementar estratégia híbrida

### **CURTO PRAZO (Esta Semana)**
1. Implementar Fase 1 (seletores de alto risco)
2. Testar em ambiente de desenvolvimento
3. Validar em ambas as regiões
4. Documentar resultados

### **MÉDIO PRAZO (Próximas Semanas)**
1. Implementar Fase 2 (seletores de médio risco)
2. Implementar Fase 3 (otimizações finais)
3. Monitoramento contínuo
4. Documentação final

---

## 📚 **ARQUIVOS RELACIONADOS**

### **Documentação Existente**
- `docs/ANALISE_PROBLEMA_BRASIL_PORTUGAL_v1.0.0_20250908.md`
- `docs/OTIMIZACAO_PERFORMANCE_STRATEGY_REPORT.md`
- `docs/ITENS_PENDENTES_v3.7.0_20250908.md`

### **Arquivos de Referência**
- `executar_rpa_imediato_playwright.py` - Arquivo principal
- `executar_rpa_imediato_playwright_pt.py` - Arquivo de referência Portugal

---

**📅 Data da Auditoria**: 09/09/2025  
**⏰ Duração**: Análise completa  
**✅ Status**: Concluída com sucesso  
**🎯 Próximo Passo**: Criação do plano de implementação detalhado

---

## 🔍 **DETALHES TÉCNICOS ADICIONAIS**

### **PADRÕES DE SELETORES IDENTIFICADOS**

#### **1. Seletores por Classe CSS**
```python
# PROBLEMÁTICO
page.locator("button.group")
page.locator("div.bg-primary")
page.locator(".overflow-hidden")

# RECOMENDADO
page.locator("#botao-carro")
page.locator("[data-testid='card-estimativa']")
page.locator("[data-testid='sugestao-endereco']")
```

#### **2. Seletores por Texto**
```python
# PROBLEMÁTICO
page.locator("text=Continuar")
page.locator("text=R$")
page.locator(f"text={sexo}")

# RECOMENDADO
page.locator("#botao-continuar")
page.locator("[data-testid='preco-estimativa']")
page.locator(f"[data-testid='opcao-sexo-{sexo}']")
```

#### **3. XPath Baseados em Texto**
```python
# PROBLEMÁTICO
page.locator("xpath=//*[contains(text(), 'finalidade')]")
page.locator("xpath=//li[contains(text(), 'Casado')]")

# RECOMENDADO
page.locator("[data-testid='tela-uso-veiculo']")
page.locator("[data-testid='opcao-estado-civil-casado']")
```

#### **4. Seletores por Valor Específico**
```python
# PROBLEMÁTICO
page.locator('input[value="Kit Gás"]')
page.locator('input[value="sim"][name="condutorPrincipalTelaCondutorPrincipal"]')

# RECOMENDADO
page.locator("#checkbox-kit-gas")
page.locator("#radio-condutor-principal-sim")
```

---

## ⚠️ **ALERTAS IMPORTANTES**

### **🚨 CRÍTICO**
- **15 seletores** com risco alto de falha
- **Especialmente problemáticos** em Portugal
- **Podem quebrar** com mudanças na UI

### **⚠️ ATENÇÃO**
- **32 seletores** com risco médio
- **Dependem de valores específicos** que podem mudar
- **Requerem monitoramento** contínuo

### **✅ SEGURO**
- **Seletores por ID** são estáveis
- **Seletores por data-testid** são recomendados
- **Fallbacks** devem ser mantidos

---

## ✅ **IMPLEMENTAÇÕES REALIZADAS**

### **IMPLEMENTAÇÃO v3.7.0.1 - 09/09/2025**

#### **🎯 SELETOR IMPLEMENTADO**
- **Tela**: 1
- **Função**: `navegar_tela_1_playwright()`
- **Seletor Original**: `button.group`
- **Seletor Novo**: `button:has(img[alt="Icone car"])`
- **Status**: ✅ **IMPLEMENTADO**

#### **📋 DETALHES DA IMPLEMENTAÇÃO**
- **Estratégia**: Híbrida (Específico + Fallback)
- **Seletores Testados**: 4 opções
- **Fallback Mantido**: Sim (`button.group`)
- **Logs Adicionados**: Sim (monitoramento de seletor usado)
- **Testes Realizados**: ✅ Sintaxe validada

#### **🧪 RESULTADOS DOS TESTES**
- **Ambiente Local**: ✅ Sucesso (sintaxe validada)
- **Região Brasil**: ✅ Sucesso (teste funcional completo)
- **Região Portugal**: 🔄 Pendente teste
- **Performance**: ✅ Sem impacto negativo
- **Regressão**: ✅ Nenhuma funcionalidade quebrada

#### **📈 MÉTRICAS OBTIDAS**
- **Taxa de Sucesso**: 100% (Telas 1 e 5)
- **Tempo de Execução**: 210.76s (otimizado)
- **Uso de Recursos**: Estável
- **Logs de Erro**: 0 erros relacionados
- **Seletores Usados**: Específicos (não fallbacks)
- **Telas Executadas**: 15 de 15 (100% - execução completa)
- **Estimativas Capturadas**: 3 coberturas com valores precisos
- **Benefícios Identificados**: 12 benefícios únicos

#### **🔄 PRÓXIMAS IMPLEMENTAÇÕES**

##### **✅ IMPLEMENTAÇÃO v3.7.0.2 - Cards Estimativa (Tela 5) - CONCLUÍDA**
- **Tela**: 5
- **Seletor**: `div.bg-primary` → `div[role="group"][aria-roledescription="slide"]`
- **Prioridade**: Alta
- **Data Implementação**: 09/09/2025
- **Status**: ✅ **IMPLEMENTADO E TESTADO COM SUCESSO**
- **Estratégia**: Híbrida com fallbacks múltiplos
- **Teste**: ✅ Execução completa bem-sucedida (210.76s)
- **Estimativas**: ✅ 3 coberturas capturadas com valores precisos
- **Commit**: `0e8df2a`

##### **✅ IMPLEMENTAÇÃO v3.7.0.3-main - Sugestões Endereço (Tela 7) - CONCLUÍDA**
- **Tela**: 7
- **Seletor**: `.overflow-hidden` → `[data-testid="sugestao-endereco"]`
- **Prioridade**: Alta
- **Data Implementação**: 09/09/2025
- **Status**: ✅ **IMPLEMENTADO E TESTADO COM SUCESSO NO ARQUIVO PRINCIPAL**
- **Estratégia**: Híbrida com fallbacks múltiplos
- **Teste**: ✅ Execução completa bem-sucedida (103.48s)
- **Sugestões**: ✅ Funcionamento perfeito das sugestões de endereço
- **Commit**: `ec9703e`

##### **✅ IMPLEMENTAÇÃO v3.7.0.4 - Detecção Tela 8 (Finalidade Veículo) - CONCLUÍDA**
- **Tela**: 8
- **Seletor**: `xpath=//*[contains(text(), 'finalidade') or contains(text(), 'uso')]` → `#finalidadeVeiculoTelaUsoVeiculo`
- **Prioridade**: Alta
- **Data Implementação**: 09/09/2025
- **Status**: ✅ **IMPLEMENTADO E TESTADO COM SUCESSO**
- **Estratégia**: Híbrida com 4 níveis de fallback
- **Teste**: ✅ Execução completa bem-sucedida (151.91s)
- **Detecção**: ✅ Funcionamento perfeito da detecção da Tela 8
- **Commit**: `efd8634`

##### **IMPLEMENTAÇÃO v3.7.0.4 - Otimização de Timeouts (Telas 14-15)**
- **Problema**: Timeouts excessivos prejudicam experiência do usuário
- **Tela 14**: 5s (adequado)
- **Tela 15**: 180s (excessivo - reduzir para 30-60s)
- **Prioridade**: Média
- **Data Planejada**: 11/09/2025
- **Benefício**: Falha mais rápida em problemas externos

---

**🎯 OBJETIVO**: Substituir todos os seletores genéricos por específicos, mantendo 100% da funcionalidade e melhorando a estabilidade regional.
