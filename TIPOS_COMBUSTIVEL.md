# Tipos de Combustível - Tela 6

## 📋 **TIPOS DISPONÍVEIS**

Baseado na análise da gravação Selenium IDE, os seguintes tipos de combustível estão disponíveis na Tela 6:

### **🎯 Valores Aceitos:**

1. **"Flex"** (padrão)
   - Valor padrão se não especificado
   - Combustível flexível (gasolina + álcool)

2. **"Gasolina"**
   - Combustível exclusivamente gasolina

3. **"Álcool"**
   - Combustível exclusivamente álcool

4. **"Diesel"**
   - Combustível diesel

5. **"Híbrido"** ou **"Hibrido"**
   - Veículo híbrido (combustível + elétrico)

6. **"Elétrico"**
   - Veículo 100% elétrico

## 🔧 **IMPLEMENTAÇÃO**

### **Parâmetro JSON:**
```json
{
  "combustivel": "Flex"
}
```

### **Uso no Código:**
```python
# Selecionar tipo de combustível baseado no parâmetro JSON
combustivel = parametros.get('combustivel', 'Flex')
exibir_mensagem(f"⏳ Selecionando '{combustivel}' como tipo de combustível...")

if not clicar_radio_via_javascript(driver, combustivel, f"{combustivel} como combustível"):
    exibir_mensagem(f"⚠️ Radio '{combustivel}' não encontrado - tentando prosseguir...")
```

## 📊 **EXEMPLOS DE USO**

### **Exemplo 1: Flex (padrão)**
```json
{
  "combustivel": "Flex"
}
```

### **Exemplo 2: Gasolina**
```json
{
  "combustivel": "Gasolina"
}
```

### **Exemplo 3: Elétrico**
```json
{
  "combustivel": "Elétrico"
}
```

## ⚠️ **NOTAS IMPORTANTES**

- **Validação:** O código usa `clicar_radio_via_javascript()` para selecionar o radio correto
- **Fallback:** Se o tipo especificado não for encontrado, o sistema tenta prosseguir
- **Compatibilidade:** Todos os tipos são baseados na gravação Selenium IDE real
- **Case Sensitive:** Os valores devem corresponder exatamente aos da interface

## 🔍 **DETECÇÃO**

A Tela 6 é detectada usando:
```xpath
//*[contains(text(), 'combustível') or contains(text(), 'Combustível') or contains(text(), 'Flex') or contains(text(), 'Gasolina')]
```

## 📝 **HISTÓRICO**

- **Data:** 31/08/2025
- **Base:** Análise da gravação Selenium IDE
- **Implementação:** Seleção dinâmica baseada no parâmetro JSON
- **Status:** ✅ Implementado e testado
