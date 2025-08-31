# Tipos de Valores - Tela 10 (Condutor Principal)

## 📋 **TIPOS DISPONÍVEIS**
Baseado na análise da gravação Selenium IDE, os seguintes tipos de valores estão disponíveis na Tela 10 "Você será o condutor principal do veículo?":

## 🎯 **RADIO BUTTONS PRINCIPAIS**

### **condutor_principal**
- **Tipo**: boolean
- **Descrição**: Seleção se você será o condutor principal do veículo
- **Valores Aceitos**:
  - `true` - "Sim" (será o condutor principal)
  - `false` - "Não" (não será o condutor principal)

## 📝 **CAMPOS CONDICIONAIS (quando condutor_principal = false)**

### **nome_condutor**
- **Tipo**: string
- **Descrição**: Nome completo do condutor principal
- **Obrigatório**: Sim (quando condutor_principal = false)
- **Exemplo**: `"SANDRA LOUREIRO"`

### **cpf_condutor**
- **Tipo**: string
- **Descrição**: CPF do condutor principal
- **Obrigatório**: Sim (quando condutor_principal = false)
- **Formato**: XXX.XXX.XXX-XX
- **Exemplo**: `"251.517.878-29"`

### **data_nascimento_condutor**
- **Tipo**: string
- **Descrição**: Data de nascimento do condutor principal
- **Obrigatório**: Sim (quando condutor_principal = false)
- **Formato**: DD/MM/AAAA
- **Exemplo**: `"28/08/1975"`

### **sexo_condutor**
- **Tipo**: string
- **Descrição**: Sexo do condutor principal
- **Obrigatório**: Sim (quando condutor_principal = false)
- **Valores Aceitos**:
  1. **"Masculino"**
  2. **"Feminino"**

### **estado_civil_condutor**
- **Tipo**: string
- **Descrição**: Estado civil do condutor principal
- **Obrigatório**: Sim (quando condutor_principal = false)
- **Valores Aceitos**:
  1. **"Casado ou União Estável"**
  2. **"Divorciado"**
  3. **"Separado"**
  4. **"Solteiro"**
  5. **"Viúvo"**

## 🔧 **IMPLEMENTAÇÃO**

### **Parâmetro JSON:**
```json
{
  "condutor_principal": true,
  "nome_condutor": "SANDRA LOUREIRO",
  "cpf_condutor": "251.517.878-29",
  "data_nascimento_condutor": "28/08/1975",
  "sexo_condutor": "Feminino",
  "estado_civil_condutor": "Casado ou União Estável"
}
```

### **Cenários de Uso:**

#### **Cenário 1: Condutor Principal (Sim)**
```json
{
  "condutor_principal": true
}
```
- **Comportamento**: Vai direto para próxima tela
- **Campos do condutor**: Não preenchidos

#### **Cenário 2: Condutor Principal (Não)**
```json
{
  "condutor_principal": false,
  "nome_condutor": "SANDRA LOUREIRO",
  "cpf_condutor": "251.517.878-29",
  "data_nascimento_condutor": "28/08/1975",
  "sexo_condutor": "Feminino",
  "estado_civil_condutor": "Casado ou União Estável"
}
```
- **Comportamento**: Aparecem campos adicionais para preenchimento
- **Campos do condutor**: Todos obrigatórios

## 🎯 **LOCATORS SELENIUM**

### **Radio Buttons:**
```python
# Radio "Sim"
"css=.cursor-pointer:nth-child(1) > .border .font-workSans"

# Radio "Não"  
"css=.cursor-pointer:nth-child(2) > .border .font-workSans"
```

### **Campos de Texto:**
```python
# Nome Completo
"id=nomeTelaCondutorPrincipal"

# CPF
"id=cpfTelaCondutorPrincipal"

# Data de Nascimento
"id=dataNascimentoTelaCondutorPrincipal"
```

### **Dropdowns MUI:**
```python
# Sexo
"id=sexoTelaCondutorPrincipal"
"css=#sexoTelaCondutorPrincipal .text-zinc-400"

# Estado Civil
"id=estadoCivilTelaCondutorPrincipal"
"css=#estadoCivilTelaCondutorPrincipal .text-zinc-400"
```

### **Botão Continuar:**
```python
"id=gtm-telaCondutorPrincipalContinuar"
```

## 📊 **DADOS DE TESTE**

### **Dados Usados na Gravação:**
- **Nome**: "SANDRA LOUREIRO"
- **CPF**: "251.517.878-29"
- **Data**: "28/08/1975"
- **Sexo**: "Feminino"
- **Estado Civil**: "Casado ou União Estável"

## ⚠️ **VALIDAÇÕES**

### **Campos Obrigatórios (quando condutor_principal = false):**
- ✅ nome_condutor
- ✅ cpf_condutor
- ✅ data_nascimento_condutor
- ✅ sexo_condutor
- ✅ estado_civil_condutor

### **Formatos Específicos:**
- **CPF**: XXX.XXX.XXX-XX
- **Data**: DD/MM/AAAA
- **Nome**: Texto livre (sem caracteres especiais)

## 🔄 **FLUXO CONDICIONAL**

1. **Se condutor_principal = true**:
   - Clica em "Sim"
   - Vai para próxima tela
   - Campos do condutor não aparecem

2. **Se condutor_principal = false**:
   - Clica em "Não"
   - Campos do condutor aparecem
   - Preenche todos os campos obrigatórios
   - Clica em "Continuar"

## 📝 **LOGS ESPERADOS**

### **Cenário "Sim":**
```
>>> TELA 10: Condutor Principal
>>> Selecionando 'Sim' como condutor principal...
>>> Radio 'Sim' clicado via JavaScript
>>> Continuando para próxima tela...
```

### **Cenário "Não":**
```
>>> TELA 10: Condutor Principal
>>> Selecionando 'Não' como condutor principal...
>>> Radio 'Não' clicado via JavaScript
>>> Preenchendo dados do condutor...
>>> Nome: SANDRA LOUREIRO
>>> CPF: 251.517.878-29
>>> Data: 28/08/1975
>>> Sexo: Feminino
>>> Estado Civil: Casado ou União Estável
>>> Continuando para próxima tela...
```

---

**📝 Última atualização**: 30/08/2025  
**🔧 Versão**: v2.8.1  
**📋 Baseado na**: Gravação Selenium IDE - Tela 10
