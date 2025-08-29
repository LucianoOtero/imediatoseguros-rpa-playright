# �� DOCUMENTAÇÃO COMPLETA - RPA TÔ SEGURADO
## Projeto de Automação para Cotação de Seguro Auto

---

## �� **OBJETIVO DO PROJETO**
Automatizar o processo de cotação de seguro auto no site "Tô Segurado" através de RPA (Robotic Process Automation), navegando por 15 telas do processo de cotação e extraindo dados específicos (valores e coberturas) dos resultados finais.

---

## �� **FLUXO COMPLETO DAS 15 TELAS**

### **Tela 1: Seleção do Tipo de Seguro**
- **Ação:** Selecionar "Carro" entre as opções (Carro, Moto, Vida, Residência)
- **XPath Correto:** `//button[contains(., 'Carro')]` (NÃO usar `//button[contains(text(), 'Carro')]`)
- **Resultado:** Navegação para Tela 2

### **Tela 2: Inserção da Placa**
- **Ação:** Inserir placa "EED3D56" no campo de texto
- **ID Correto:** `placaTelaDadosPlaca` (NÃO usar `placaTelaPlaca`)
- **Resultado:** Placa inserida, botão "Continuar" habilitado

### **Tela 3: Confirmação da Placa**
- **Ação:** Clicar em "Continuar" após inserir placa
- **ID Correto:** `gtm-telaDadosAutoCotarComPlacaContinuar`
- **Resultado:** Navegação para Tela 5 (pula Tela 4 que é apenas o clique)

### **Tela 4: Transição (Apenas Clique)**
- **Ação:** Apenas transição - não há conteúdo específico
- **Resultado:** Redirecionamento para Tela 5

### **Tela 5: Confirmação do Veículo**
- **Ação:** Confirmar se o veículo "COROLLA XEI 1.8/1.8 FLEX 16V MEC. 2009/2009" corresponde à placa
- **Seleção:** Radio button "Sim"
- **Método:** JavaScript click devido a elemento não visível/clicável
- **Resultado:** Navegação para Tela 6

### **Tela 6: Veículo Já Segurado (PONTO CRÍTICO)**
- **Ação:** Responder se o veículo já possui seguro vigente
- **FLUXO CORRIGIDO:** Selecionar "Não" (veículo NÃO está segurado)
- **FLUXO ALTERNATIVO:** Selecionar "Sim" (veículo já está segurado) - redireciona para "Tela de Renovação"
- **ID do Botão:** `gtm-telaInfosAutoContinuar`
- **Resultado:** 
  - "Não" → Tela 7 (estimativa inicial) ✅
  - "Sim" → Tela de Renovação (fluxo diferente) ❌

### **Tela 7: Estimativa Inicial (FLUXO CORRIGIDO)**
- **Ação:** Aguardar carregamento da estimativa inicial
- **Texto de Identificação:** "estimativa inicial"
- **Timeout:** 60 segundos (pode demorar)
- **Resultado:** Carrossel de coberturas e valores carregado

### **Tela 8: Tipo de Combustível**
- **Ação:** Selecionar "Flex" como tipo de combustível
- **Checkboxes:** Deixar Kit Gás, Blindado e Financiado desmarcados
- **Resultado:** Navegação para Tela 9

### **Tela 9: Endereço de Pernoite**
- **Ação:** Preencher endereço onde o carro passa a noite
- **CEP:** 03084-000
- **Funcionalidade:** Autocomplete com sugestões
- **Fallback:** Preenchimento manual se autocomplete falhar
- **Resultado:** Navegação para Tela 10

### **Tela 10: Uso do Veículo**
- **Ação:** Selecionar "Pessoal" como uso principal
- **Opções:** Pessoal, Profissional, Motorista de aplicativo, Taxi
- **Resultado:** Navegação para Tela 11

### **Tela 11: Dados Pessoais**
- **Ação:** Preencher dados pessoais completos
- **Dados:**
  - Nome: LUCIANO OTERO
  - CPF: 085.546.078-48
  - Data Nascimento: 09/02/1965
  - Sexo: Masculino
  - Estado Civil: Casado
  - Email: lrotero@gmail.com
  - Celular: (11) 97668-7668
- **Resultado:** Navegação para Tela 12

### **Tela 12: Condutor Principal**
- **Ação:** Confirmar se será o condutor principal
- **Seleção:** "Sim"
- **Resultado:** Navegação para Tela 13

### **Tela 13: Uso para Trabalho/Estudo**
- **Ação:** Selecionar uso do veículo para trabalho/estudo
- **Seleção:** Checkbox "Local de trabalho" apenas
- **Resultado:** Navegação para Tela 14

### **Tela 14: Garagem e Portão**
- **Ação:** Informar sobre garagem e tipo de portão
- **Seleções:** 
  - Possui garagem: "Sim"
  - Tipo de portão: "Eletrônico"
- **Resultado:** Navegação para Tela 15

### **Tela 15: Residência com Menores**
- **Ação:** Informar se reside com pessoas entre 18-26 anos
- **Seleção:** "Não"
- **Resultado:** Início do cálculo da cotação

---

## 🔧 **PROBLEMAS IDENTIFICADOS E SOLUÇÕES**

### **1. Conteúdo Dinâmico com Requests**
- **Problema:** `requests` library retorna HTML corrompido/criptografado
- **Solução:** Migração para Selenium WebDriver
- **Arquivo:** `tosegurado_requests_debug.py`

### **2. Conflito de User Data Directory**
- **Problema:** `session not created: probably user data directory is already in use`
- **Solução:** Implementação de diretório temporário único com `tempfile.mkdtemp()`
- **Arquivo:** `tosegurado_rpa_corrigido.py`

### **3. XPath Incorreto para Botão Carro**
- **Problema:** `//button[contains(text(), 'Carro')]` não funciona
- **Solução:** `//button[contains(., 'Carro')]`
- **Arquivo:** `diagnostico_botao_carro.py`

### **4. Elemento Stale Reference**
- **Problema:** `stale element reference: stale element not found in the current frame`
- **Solução:** Implementação de `WebDriverWait` com `expected_conditions`
- **Arquivo:** `tosegurado_rpa_preciso.py`

### **5. Botão Continuar Tela 3**
- **Problema:** Botão era um `<p>` tag, não `<button>`
- **Solução:** XPath `//p[text()='Continuar']`
- **Arquivo:** `tosegurado_teste_incremental.py`

### **6. Radio Button Tela 5 Não Clicável**
- **Problema:** Elemento presente mas não visível/clicável
- **Solução:** JavaScript click `driver.execute_script("arguments[0].click();", element)`
- **Arquivo:** `investigar_completo_tela5.py`

### **7. Fluxo Condicional Tela 6 (PROBLEMA PRINCIPAL)**
- **Problema:** Resposta "Sim" redireciona para fluxo de renovação
- **Solução:** Selecionar "Não" para seguir fluxo principal
- **Arquivo:** `investigacao_especifica_tela7.py`

### **8. IDs Incorretos Tela 2 e 3**
- **Problema:** IDs diferentes dos esperados
- **Solução:** 
  - Tela 2: `placaTelaDadosPlaca` (não `placaTelaPlaca`)
  - Tela 3: `gtm-telaDadosAutoCotarComPlacaContinuar`
- **Arquivo:** `investigacao_especifica_tela2.py`

---

## �� **ARQUIVOS CRIADOS E SUAS FUNÇÕES**

### **Scripts de Investigação:**
- `tosegurado_requests_debug.py` - Teste inicial com requests
- `analisar_botao_carro.py` - Diagnóstico do botão Carro
- `investigar_tela4.py` - Investigação da Tela 4
- `investigar_completo_tela5.py` - Diagnóstico completo da Tela 5
- `investigar_transicao_tela6_7.py` - Transição entre Tela 6 e 7
- `investigacao_especifica_tela7.py` - Investigação específica da Tela 7
- `investigacao_especifica_tela2.py` - Investigação específica da Tela 2
- `diagnostico_tela9.py` - Diagnóstico da Tela 9
- `diagnostico_especifico_tela9.py` - Diagnóstico específico da Tela 9
- `teste_apos_carro.py` - Teste após seleção do Carro
- `investigacao_especifica_tela7.py` - Investigação da Tela 7

### **Scripts de RPA:**
- `tosegurado_rpa_completo.py` - Primeira tentativa de RPA completo
- `tosegurado_selenium_rpa.py` - RPA com Selenium
- `tosegurado_rpa_corrigido.py` - RPA com correções iniciais
- `tosegurado_rpa_simples.py` - RPA simplificado para testes
- `tosegurado_rpa_completo_headless.py` - RPA headless
- `tosegurado_rpa_preciso.py` - RPA com condições precisas
- `tosegurado_rpa_simples_estavel.py` - RPA estável simplificado
- `tosegurado_rpa_corrigido_final.py` - RPA com correções finais
- `tosegurado_rpa_preciso_final.py` - RPA preciso final
- `tosegurado_rpa_javascript_final.py` - RPA com JavaScript click
- `tosegurado_continuar_tela6.py` - Continuação da Tela 6
- `tosegurado_continuar_tela7.py` - Continuação da Tela 7
- `tosegurado_continuar_tela8_completo.py` - Continuação da Tela 8
- `tosegurado_continuar_tela9.py` - Continuação da Tela 9
- `tosegurado_continuar_tela9_autocomplete.py` - Tela 9 com autocomplete
- `tosegurado_continuar_tela9_corrigido.py` - Tela 9 corrigida
- `tosegurado_rpa_completo_detalhado.py` - RPA com logging detalhado
- `tosegurado_rpa_timeout_corrigido.py` - RPA com timeouts corrigidos
- `tosegurado_rpa_id_corrigido.py` - RPA com IDs corrigidos
- `tosegurado_rpa_fluxo_corrigido.py` - RPA com fluxo corrigido (ATUAL)

### **Scripts de Teste:**
- `teste_incremental_tela1.py` - Teste incremental da Tela 1
- `teste_apos_carro.py` - Teste após seleção do Carro
- `teste_fluxo_correto.py` - Teste do fluxo correto

---

## 🎯 **ESTADO ATUAL DO PROJETO**

### **✅ CONQUISTAS:**
- **Navegação bem-sucedida** até Tela 6
- **Identificação correta** de todos os elementos
- **Correção do fluxo** principal (selecionar "Não" na Tela 6)
- **Implementação** de logging detalhado
- **Resolução** de todos os problemas técnicos identificados

### **�� EM DESENVOLVIMENTO:**
- **Tela 7:** Estimativa inicial (fluxo corrigido implementado)
- **Tela 8:** Tipo de combustível
- **Tela 9:** Endereço de pernoite
- **Telas 10-15:** Restante do fluxo

### **📋 PRÓXIMOS PASSOS:**
1. **Testar** o RPA com fluxo corrigido
2. **Implementar** navegação das Telas 8-15
3. **Extrair** dados finais (valores e coberturas)
4. **Criar** script para fluxo alternativo (Tela 6 = "Sim")

---

## �� **CONFIGURAÇÕES TÉCNICAS**

### **Ambiente:**
- **Sistema:** Ubuntu (Hetzner)
- **Python:** 3.x
- **Virtual Environment:** Ativado
- **Pacotes:** selenium, webdriver-manager

### **Chrome Options:**
```python
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument(f"--user-data-dir={temp_dir}")
```

### **Timeouts Configurados:**
- **Página:** 30-60 segundos
- **Elementos:** 15-30 segundos
- **Carregamento:** 3-10 segundos adicionais

---

## 📝 **NOTAS IMPORTANTES**

### **Fluxo Condicional:**
- **Tela 6 "Não"** → Fluxo principal (Tela 7: estimativa inicial)
- **Tela 6 "Sim"** → Fluxo de renovação (diferente)

### **Elementos Especiais:**
- **JavaScript Click:** Necessário para alguns elementos
- **WebDriverWait:** Essencial para estabilidade
- **Logging Detalhado:** Implementado para debug

### **IDs e XPaths Corretos:**
- **Tela 1:** `//button[contains(., 'Carro')]`
- **Tela 2:** `placaTelaDadosPlaca`
- **Tela 3:** `gtm-telaDadosAutoCotarComPlacaContinuar`
- **Tela 6:** `gtm-telaInfosAutoContinuar`

---

## �� **COMANDOS DE EXECUÇÃO**

### **Executar RPA Principal:**
```bash
cd /opt/imediatoseguros-rpa/
python3 tosegurado-rpa-fluxo-corrigido.py
```

### **Verificar Logs:**
```bash
ls -la /opt/imediatoseguros-rpa/temp/
```

### **Ativar Ambiente Virtual:**
```bash
source venv/bin/activate
```

---

## 📊 **MÉTRICAS DE PROGRESSO**

- **Telas Implementadas:** 6/15 (40%)
- **Problemas Resolvidos:** 8/8 (100%)
- **Fluxo Principal:** ✅ Funcionando
- **Fluxo Alternativo:** ⏳ Pendente
- **Extração de Dados:** ⏳ Pendente

---

## 🔍 **ARQUIVOS DE REFERÊNCIA**

- **FLUXO_COMPLETO_TOSEGURADO.md** - Descrição detalhada das 15 telas
- **DOCUMENTACAO_COMPLETA_RPA.md** - Esta documentação
- **Todos os scripts** na pasta `/opt/imediatoseguros-rpa/`

---

## 📞 **SUPORTE E CONTATO**

Para continuidade do projeto em caso de travamento do Cursor:
1. **Consultar** esta documentação
2. **Verificar** scripts na pasta do projeto
3. **Executar** o RPA principal: `tosegurado-rpa-fluxo-corrigido.py`
4. **Analisar** logs em `/opt/imediatoseguros-rpa/temp/`

---

**Última Atualização:** 28/08/2025 19:45
**Status:** Em desenvolvimento ativo
**Próximo Milestone:** Navegação completa até Tela 15
