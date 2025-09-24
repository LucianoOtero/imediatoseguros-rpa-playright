# 🔧 TROUBLESHOOTING - TELA ZERO KM
## RPA Tô Segurado - Playwright v3.2.0

---

## 🚨 **PROBLEMAS COMUNS E SOLUÇÕES**

### **❌ ERRO: "Strict Mode Violation"**

#### **Sintoma:**
```
Error: strict mode violation: locator("#zerokmTelaZeroKm") resolved to 2 elements
```

#### **Causa:**
O seletor `#zerokmTelaZeroKm` é ambíguo, encontrando tanto o elemento `<label>` quanto o `<div>`.

#### **Solução:**
✅ **IMPLEMENTADA**: Usar seletor específico `#zerokmTelaZeroKm[role='radiogroup']`

#### **Código Corrigido:**
```python
# ❌ PROBLEMÁTICO
elemento_zero_km = page.locator("#zerokmTelaZeroKm")

# ✅ CORRETO
elemento_zero_km = page.locator("#zerokmTelaZeroKm[role='radiogroup']")
```

---

### **❌ ERRO: "Tela Zero KM não detectada"**

#### **Sintoma:**
```
ℹ️ Tela Zero KM não apareceu - continuando fluxo normal
```

#### **Causa:**
- Tela não apareceu para esta placa específica
- Carregamento muito lento da página
- Mudança na estrutura do site

#### **Solução:**
✅ **NÃO É ERRO**: Sistema continua fluxo normal automaticamente

#### **Verificação:**
```bash
# Verificar se a placa ativa a tela Zero KM
python executar_rpa_imediato_playwright.py --docs params
# Procurar por: "zero_km": false
```

---

### **❌ ERRO: "Timeout na transição para Tela 6"**

#### **Sintoma:**
```
TimeoutError: Waiting for selector "#gtm-telaItensAutoContinuar"
```

#### **Causa:**
- Tela 6 não carregou após clicar "Continuar"
- Problema de conectividade
- Site lento

#### **Solução:**
1. **Aumentar timeout** (temporário):
```python
page.wait_for_selector("#gtm-telaItensAutoContinuar", timeout=10000)  # 10s
```

2. **Verificar conectividade**:
```bash
ping www.app.tosegurado.com.br
```

3. **Verificar logs**:
```bash
tail -f logs/rpa_imediato_playwright_YYYYMMDD.log
```

---

### **❌ ERRO: "Tela Zero KM não está visível"**

#### **Sintoma:**
```
⚠️ Tela Zero KM não está visível
```

#### **Causa:**
- Elemento não carregou completamente
- Mudança na estrutura HTML
- Problema de timing

#### **Solução:**
1. **Aguardar carregamento**:
```python
# Aguardar elemento aparecer
page.wait_for_selector("#zerokmTelaZeroKm[role='radiogroup']", timeout=5000)
```

2. **Verificar seletor**:
```python
# Debug: verificar se elemento existe
elementos = page.locator("#zerokmTelaZeroKm").all()
print(f"Elementos encontrados: {len(elementos)}")
```

---

### **❌ ERRO: "Opção não selecionada"**

#### **Sintoma:**
```
❌ Falha ao selecionar opção Zero KM
```

#### **Causa:**
- Radio button não clicável
- Elemento sobreposto
- JavaScript não carregado

#### **Solução:**
1. **Usar click forçado**:
```python
page.locator('input[name="zerokmTelaZeroKm"][value="Sim"]').click(force=True)
```

2. **Aguardar elemento clicável**:
```python
page.wait_for_selector('input[name="zerokmTelaZeroKm"][value="Sim"]', state="visible")
```

---

## 🔍 **DIAGNÓSTICO AVANÇADO**

### **📊 Verificação de Elementos:**

#### **1. Listar todos os elementos Zero KM:**
```python
# Debug: verificar estrutura HTML
elementos = page.locator("#zerokmTelaZeroKm").all()
for i, elemento in enumerate(elementos):
    print(f"Elemento {i}: {elemento.get_attribute('outerHTML')}")
```

#### **2. Verificar radio buttons:**
```python
# Debug: verificar radio buttons
radio_sim = page.locator('input[name="zerokmTelaZeroKm"][value="Sim"]')
radio_nao = page.locator('input[name="zerokmTelaZeroKm"][value="Não"]')

print(f"Radio Sim visível: {radio_sim.is_visible()}")
print(f"Radio Não visível: {radio_nao.is_visible()}")
print(f"Radio Sim clicável: {radio_sim.is_enabled()}")
print(f"Radio Não clicável: {radio_nao.is_enabled()}")
```

#### **3. Verificar botão Continuar:**
```python
# Debug: verificar botão Continuar
botao_continuar = page.locator("#gtm-telaZeroKmContinuar")
print(f"Botão Continuar visível: {botao_continuar.is_visible()}")
print(f"Botão Continuar clicável: {botao_continuar.is_enabled()}")
```

---

## 🛠️ **FERRAMENTAS DE DEBUG**

### **📸 Screenshot de Debug:**
```python
# Capturar screenshot quando erro ocorrer
if not elemento_zero_km.is_visible():
    page.screenshot(path="debug_zero_km_error.png")
    print("Screenshot salvo: debug_zero_km_error.png")
```

### **📝 Log Detalhado:**
```python
# Log detalhado para debug
exibir_mensagem(f"🔍 DEBUG: Elementos Zero KM encontrados: {len(elementos)}")
exibir_mensagem(f"🔍 DEBUG: Radio Sim clicável: {radio_sim.is_enabled()}")
exibir_mensagem(f"🔍 DEBUG: Radio Não clicável: {radio_nao.is_enabled()}")
```

### **⏱️ Timing de Debug:**
```python
import time

# Medir tempo de cada operação
inicio = time.time()
elemento_zero_km = page.locator("#zerokmTelaZeroKm[role='radiogroup']")
tempo_deteccao = time.time() - inicio
exibir_mensagem(f"⏱️ Tempo detecção: {tempo_deteccao:.2f}s")
```

---

## 📋 **CHECKLIST DE VALIDAÇÃO**

### **✅ Antes de Reportar Problema:**

- [ ] **Placa correta**: Usar placa que ativa Zero KM (ex: EYQ4J41)
- [ ] **Parâmetro correto**: `"zero_km": false` no parametros.json
- [ ] **Conectividade**: Site carregando normalmente
- [ ] **Logs verificados**: Procurar por mensagens de erro específicas
- [ ] **Screenshot capturado**: Se possível, capturar tela do erro
- [ ] **Versão atualizada**: Usar versão v3.2.0 ou superior

### **🔍 Informações para Suporte:**

1. **Placa utilizada**: `EYQ4J41`
2. **Parâmetro zero_km**: `false` ou `true`
3. **Mensagem de erro completa**
4. **Logs relevantes** (últimas 10 linhas)
5. **Screenshot** (se disponível)
6. **Versão do RPA**: `v3.2.0`

---

## 🚀 **COMANDOS DE TESTE**

### **🧪 Teste Básico:**
```bash
# Teste com placa que ativa Zero KM
python executar_rpa_imediato_playwright.py
```

### **🔍 Teste de Documentação:**
```bash
# Verificar parâmetros
python executar_rpa_imediato_playwright.py --docs params
```

### **📊 Teste com Logs:**
```bash
# Executar com logs detalhados
python executar_rpa_imediato_playwright.py --log
```

### **🛠️ Teste de Debug:**
```python
# Adicionar ao código para debug
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

## 📞 **SUPORTE TÉCNICO**

### **🆘 Quando Contatar Suporte:**

- Erro persiste após seguir troubleshooting
- "Strict Mode Violation" não resolvido
- Timeout constante na transição
- Mudança na estrutura do site

### **📧 Informações para Envio:**

```
Assunto: [TELA ZERO KM] Erro específico

Placa: EYQ4J41
Parâmetro zero_km: false
Erro: [mensagem completa]
Logs: [últimas 10 linhas]
Screenshot: [anexar se disponível]
Versão: v3.2.0
```

---

## 📚 **RECURSOS ADICIONAIS**

### **📖 Documentação Relacionada:**
- [Documentação Técnica Zero KM](DOCUMENTACAO_TELA_ZERO_KM.md)
- [README Principal](../README.md)
- [README Playwright](../README_PLAYWRIGHT.md)

### **🔗 Arquivos Importantes:**
- **Implementação**: `executar_rpa_imediato_playwright.py` (linhas 1223-1266)
- **Configuração**: `parametros.json`
- **Logs**: `logs/rpa_imediato_playwright_YYYYMMDD.log`

### **🎯 Versões Suportadas:**
- **v3.2.0**: Implementação inicial ✅
- **v3.1.x**: Não suportado ❌
- **v3.0.x**: Não suportado ❌

---

**📅 Última Atualização**: 24/09/2025  
**👨‍💻 Desenvolvedor**: RPA Tô Segurado Team  
**🔖 Versão**: v3.2.0  
**📋 Status**: ✅ **IMPLEMENTADO E FUNCIONAL**
