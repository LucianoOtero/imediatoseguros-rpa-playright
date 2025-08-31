# 📋 **PARÂMETROS JSON COMPLETO - RPA TÔ SEGURADO**

## 🎯 **DESCRIÇÃO GERAL**

Este documento descreve **todos os parâmetros** disponíveis no arquivo `parametros.json` para configurar o RPA de cotação de seguros do Tô Segurado. Os parâmetros são organizados por categoria e incluem valores aceitos, tipos de dados e exemplos de uso.

---

## ⚙️ **CONFIGURAÇÃO DO SISTEMA**

### **configuracao**
Configurações gerais do sistema de execução e logging.

| Parâmetro | Tipo | Padrão | Descrição |
|-----------|------|--------|-----------|
| `log` | boolean | `true` | Ativa/desativa o sistema de logging |
| `display` | boolean | `true` | Exibe mensagens no terminal durante execução |
| `log_rotacao_dias` | integer | `90` | Dias para rotação automática dos logs |
| `log_nivel` | string | `"INFO"` | Nível de log (DEBUG, INFO, WARNING, ERROR) |
| `tempo_estabilizacao` | integer | `1` | Tempo de espera para estabilização (segundos) |
| `tempo_carregamento` | integer | `10` | Timeout para carregamento de páginas (segundos) |
| `inserir_log` | boolean | `true` | Insere logs no arquivo de log |
| `visualizar_mensagens` | boolean | `true` | Exibe mensagens detalhadas |
| `eliminar_tentativas_inuteis` | boolean | `true` | Elimina tentativas que falharam anteriormente |

**Exemplo:**
```json
{
  "configuracao": {
    "log": true,
    "display": true,
    "log_rotacao_dias": 90,
    "log_nivel": "INFO",
    "tempo_estabilizacao": 1,
    "tempo_carregamento": 10,
    "inserir_log": true,
    "visualizar_mensagens": true,
    "eliminar_tentativas_inuteis": true
  }
}
```

---

## 🚗 **DADOS DO VEÍCULO**

### **Informações Básicas**
| Parâmetro | Tipo | Obrigatório | Descrição | Exemplo |
|-----------|------|-------------|-----------|---------|
| `url_base` | string | ✅ | URL base do portal Tô Segurado | `"https://www.app.tosegurado.com.br/imediatoseguros"` |
| `placa` | string | ✅ | Placa do veículo (formato: ABC-1234) | `"EED3D56"` |
| `marca` | string | ✅ | Marca do veículo | `"FORD"` |
| `modelo` | string | ✅ | Modelo do veículo | `"ECOSPORT XLS 1.6 1.6 8V"` |
| `ano` | string | ✅ | Ano de fabricação | `"2006"` |

### **Características Especiais**
| Parâmetro | Tipo | Padrão | Descrição | Valores Aceitos |
|-----------|------|--------|-----------|-----------------|
| `zero_km` | boolean | `false` | Veículo zero quilômetro | `true` / `false` |
| `combustivel` | string | `"Flex"` | Tipo de combustível | `"Flex"`, `"Gasolina"`, `"Álcool"`, `"Diesel"`, `"Híbrido"`, `"Elétrico"` |
| `veiculo_segurado` | string | `"Não"` | Veículo já possui seguro | `"Sim"` / `"Não"` |

### **Itens Opcionais**
| Parâmetro | Tipo | Padrão | Descrição |
|-----------|------|--------|-----------|
| `kit_gas` | boolean | `false` | Veículo possui kit gás |
| `blindado` | boolean | `false` | Veículo é blindado |
| `financiado` | boolean | `false` | Veículo é financiado |

---

## 🏠 **DADOS DE ENDEREÇO**

| Parâmetro | Tipo | Obrigatório | Descrição | Exemplo |
|-----------|------|-------------|-----------|---------|
| `cep` | string | ✅ | CEP do endereço | `"03317-000"` |
| `endereco_completo` | string | ✅ | Endereço completo | `"Rua Serra de Botucatu, 410 APTO 11 - São Paulo, SP"` |
| `endereco` | string | ✅ | Endereço simplificado | `"Rua Serra de Botucatu, Tatuapé - São Paulo/SP"` |

---

## 🚦 **USO DO VEÍCULO**

| Parâmetro | Tipo | Obrigatório | Descrição | Valores Aceitos |
|-----------|------|-------------|-----------|-----------------|
| `uso_veiculo` | string | ✅ | Finalidade do uso do veículo | `"Pessoal"`, `"Profissional"`, `"Motorista de aplicativo"`, `"Taxi"` |

---

## 👤 **DADOS PESSOAIS DO SEGURADO**

### **Informações Básicas**
| Parâmetro | Tipo | Obrigatório | Descrição | Exemplo |
|-----------|------|-------------|-----------|---------|
| `nome` | string | ✅ | Nome completo do segurado | `"LUCIANO OTERO"` |
| `cpf` | string | ✅ | CPF do segurado (formato: XXX.XXX.XXX-XX) | `"085.546.078-48"` |
| `data_nascimento` | string | ✅ | Data de nascimento (formato: DD/MM/AAAA) | `"09/02/1965"` |
| `email` | string | ✅ | Email do segurado | `"lrotero@gmail.com"` |
| `celular` | string | ✅ | Celular do segurado | `"(11) 97668-7668"` |

### **Dados Demográficos**
| Parâmetro | Tipo | Obrigatório | Descrição | Valores Aceitos |
|-----------|------|-------------|-----------|-----------------|
| `sexo` | string | ✅ | Sexo do segurado | `"Masculino"`, `"Feminino"` |
| `estado_civil` | string | ✅ | Estado civil do segurado | `"Solteiro"`, `"Casado"`, `"Divorciado"`, `"Separado"`, `"Viúvo"` |

---

## 👥 **DADOS DO CONDUTOR PRINCIPAL (TELA 10)**

### **Seleção do Condutor**
| Parâmetro | Tipo | Obrigatório | Descrição | Valores Aceitos |
|-----------|------|-------------|-----------|-----------------|
| `condutor_principal` | boolean | ✅ | Você será o condutor principal? | `true` / `false` |

### **Dados do Condutor (quando condutor_principal = false)**
| Parâmetro | Tipo | Obrigatório | Descrição | Exemplo |
|-----------|------|-------------|-----------|---------|
| `nome_condutor` | string | ⚠️ | Nome completo do condutor | `"SANDRA LOUREIRO"` |
| `cpf_condutor` | string | ⚠️ | CPF do condutor | `"251.517.878-29"` |
| `data_nascimento_condutor` | string | ⚠️ | Data de nascimento do condutor | `"28/08/1975"` |
| `sexo_condutor` | string | ⚠️ | Sexo do condutor | `"Feminino"` |
| `estado_civil_condutor` | string | ⚠️ | Estado civil do condutor | `"Casado ou União Estável"` |

**⚠️ Obrigatório apenas quando `condutor_principal = false`**

---

## 🏢 **ATIVIDADE DO VEÍCULO (TELA 11)**

| Parâmetro | Tipo | Padrão | Descrição |
|-----------|------|--------|-----------|
| `local_de_trabalho` | boolean | `false` | Veículo usado para ir ao trabalho |
| `estacionamento_proprio_local_de_trabalho` | boolean | `false` | Possui estacionamento próprio no trabalho |
| `local_de_estudo` | boolean | `false` | Veículo usado para ir ao estudo |
| `estacionamento_proprio_local_de_estudo` | boolean | `false` | Possui estacionamento próprio no estudo |

---

## 🏠 **GARAGEM NA RESIDÊNCIA (TELA 12)**

| Parâmetro | Tipo | Padrão | Descrição | Valores Aceitos |
|-----------|------|--------|-----------|-----------------|
| `garagem_residencia` | boolean | `true` | Possui garagem na residência | `true` / `false` |
| `portao_eletronico` | string | `"Eletronico"` | Tipo de portão (quando garagem_residencia = true) | `"Eletronico"`, `"Manual"`, `"Não possui"` |

---

## 👨‍👩‍👧‍👦 **USO POR RESIDENTES (TELA 13)**

| Parâmetro | Tipo | Padrão | Descrição | Valores Aceitos |
|-----------|------|--------|-----------|-----------------|
| `reside_18_26` | string | `"Não"` | Reside com alguém entre 18-26 anos | `"Sim"` / `"Não"` |
| `sexo_do_menor` | string | `"N/A"` | Sexo do menor (quando reside_18_26 = "Sim") | `"Masculino"`, `"Feminino"`, `"N/A"` |
| `faixa_etaria_menor_mais_novo` | string | `"N/A"` | Faixa etária do menor (quando reside_18_26 = "Sim") | `"18-21"`, `"22-26"`, `"N/A"` |

---

## 📋 **EXEMPLO COMPLETO**

```json
{
  "configuracao": {
    "log": true,
    "display": true,
    "log_rotacao_dias": 90,
    "log_nivel": "INFO",
    "tempo_estabilizacao": 1,
    "tempo_carregamento": 10,
    "inserir_log": true,
    "visualizar_mensagens": true,
    "eliminar_tentativas_inuteis": true
  },
  "url_base": "https://www.app.tosegurado.com.br/imediatoseguros",
  "placa": "EED3D56",
  "marca": "FORD",
  "modelo": "ECOSPORT XLS 1.6 1.6 8V",
  "ano": "2006",
  "zero_km": false,
  "combustivel": "Elétrico",
  "veiculo_segurado": "Não",
  "cep": "03317-000",
  "endereco_completo": "Rua Serra de Botucatu, 410 APTO 11 - São Paulo, SP",
  "uso_veiculo": "Profissional",
  "nome": "LUCIANO OTERO",
  "cpf": "085.546.078-48",
  "data_nascimento": "09/02/1965",
  "sexo": "Masculino",
  "estado_civil": "Casado",
  "email": "lrotero@gmail.com",
  "celular": "(11) 97668-7668",
  "endereco": "Rua Serra de Botucatu, Tatuapé - São Paulo/SP",
  "condutor_principal": true,
  "nome_condutor": "SANDRA LOUREIRO",
  "cpf_condutor": "251.517.878-29",
  "data_nascimento_condutor": "28/08/1975",
  "sexo_condutor": "Feminino",
  "estado_civil_condutor": "Casado ou União Estável",
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
  "financiado": false
}
```

---

## 🔧 **CENÁRIOS DE USO**

### **Cenário 1: Condutor Principal (Sim)**
```json
{
  "condutor_principal": true
}
```
- Não preencher campos do condutor
- Irá direto para próxima tela

### **Cenário 2: Condutor Principal (Não)**
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
- Preencher todos os campos do condutor
- Campos obrigatórios quando condutor_principal = false

### **Cenário 3: Veículo Zero KM**
```json
{
  "zero_km": true
}
```
- Pode aparecer tela adicional específica
- Tratamento condicional implementado

---

## ⚠️ **VALIDAÇÕES IMPORTANTES**

### **CPF**
- Formato: XXX.XXX.XXX-XX
- Validação de dígitos verificadores
- Exemplo: `"085.546.078-48"`

### **Data de Nascimento**
- Formato: DD/MM/AAAA
- Exemplo: `"09/02/1965"`

### **CEP**
- Formato: XXXXX-XXX
- Exemplo: `"03317-000"`

### **Celular**
- Formato: (XX) XXXXX-XXXX
- Exemplo: `"(11) 97668-7668"`

---

## 🚀 **COMO USAR**

### **1. Execução Básica**
```bash
type parametros.json | python executar_rpa_imediato.py -
```

### **2. Execução com Parâmetros Customizados**
```bash
echo '{"placa": "ABC1234", "nome": "João Silva"}' | python executar_rpa_imediato.py -
```

### **3. Validação de Parâmetros**
O sistema valida automaticamente:
- ✅ Campos obrigatórios
- ✅ Formatos corretos
- ✅ Tipos de dados
- ✅ Valores aceitos

---

## 📞 **SUPORTE**

Para dúvidas sobre parâmetros:
1. Consulte este documento
2. Verifique os exemplos fornecidos
3. Analise os logs de execução
4. Abra uma issue no GitHub

---

**📝 Última atualização**: 30/08/2025  
**🔧 Versão**: v2.8.1  
**📋 Total de parâmetros**: 45 parâmetros configuráveis
