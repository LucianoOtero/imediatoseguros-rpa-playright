# Tipos de Uso do Veículo - Tela 8

## 📋 **TIPOS DISPONÍVEIS**

Baseado na análise da gravação Selenium IDE, os seguintes tipos de uso do veículo estão disponíveis na Tela 8 "Qual é o uso do veículo?":

### **🎯 Valores Aceitos:**

1. **"Pessoal"** (padrão)
   - Valor padrão se não especificado
   - Uso pessoal/familiar do veículo

2. **"Profissional"**
   - Uso profissional/empresarial do veículo
   - Para trabalho e atividades comerciais

3. **"Motorista de aplicativo"**
   - Uso como motorista de aplicativos (Uber, 99, etc.)
   - Atividade de transporte remunerado

4. **"Taxi"**
   - Uso como táxi
   - Atividade de transporte público

## 🔧 **IMPLEMENTAÇÃO**

### **Parâmetro JSON:**
```json
{
  "uso_veiculo": "Pessoal"
}
```

### **Uso no Código:**
```python
# Selecionar tipo de uso baseado no parâmetro JSON
uso_veiculo = parametros.get('uso_veiculo', 'Pessoal')
exibir_mensagem(f"Selecionando '{uso_veiculo}' como uso do veículo...")

if not clicar_radio_via_javascript(driver, uso_veiculo, f"{uso_veiculo} como uso"):
    exibir_mensagem(f"Radio '{uso_veiculo}' não encontrado - tentando prosseguir...")
```

## 📊 **Mapeamento de Valores**

### **Valores Antigos → Novos:**
- `"Particular"` → `"Pessoal"`
- `"Profissional"` → `"Profissional"`
- `"Aplicativo"` → `"Motorista de aplicativo"`
- `"Taxi"` → `"Taxi"`

## 🎯 **EXEMPLOS DE USO**

### **Uso Pessoal:**
```json
{
  "uso_veiculo": "Pessoal"
}
```

### **Uso Profissional:**
```json
{
  "uso_veiculo": "Profissional"
}
```

### **Motorista de Aplicativo:**
```json
{
  "uso_veiculo": "Motorista de aplicativo"
}
```

### **Taxi:**
```json
{
  "uso_veiculo": "Taxi"
}
```

## ⚠️ **IMPORTANTE**

- Os valores devem corresponder **exatamente** aos textos exibidos na tela
- A seleção é feita via JavaScript para maior confiabilidade
- Se o valor não for encontrado, o sistema tentará prosseguir com aviso
