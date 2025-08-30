# 🚀 ESTRATÉGIA DE VERSIONAMENTO RPA TÔ SEGURADO

## 📋 **VISÃO GERAL**

A partir da versão v2.5.1, implementamos uma estratégia de versionamento automatizada que facilita o controle de versões e manutenção do sistema RPA.

## 🎯 **CONCEITO PRINCIPAL**

### **Arquivo Oficial:**
- **`executar_rpa_imediato.py`** - Sempre o arquivo principal para desenvolvimento e produção
- Este arquivo é continuamente atualizado com novas funcionalidades
- É o arquivo que deve ser executado em produção

### **Arquivos de Versão:**
- **`executar_rpa_imediato_v<versao>.py`** - Snapshots de cada versão commitada no GitHub
- Permitem comparação entre versões
- Servem como backup e referência histórica

## 🔄 **FLUXO DE TRABALHO**

### **1. Desenvolvimento:**
```
📝 Desenvolver → executar_rpa_imediato.py
🧪 Testar funcionalidades
✅ Validar funcionamento
```

### **2. Versionamento:**
```
🚀 python versionar_rpa.py <versao>
📁 Criar executar_rpa_imediato_v<versao>.py
🔍 Verificar arquivos idênticos
```

### **3. Commit no GitHub:**
```
📤 git add .
💾 git commit -m "v<versao> - <descrição>"
🚀 git push origin master
```

### **4. Continuar Desenvolvimento:**
```
📝 Continuar em executar_rpa_imediato.py
🔄 Repetir ciclo para nova versão
```

## 🛠️ **SCRIPT DE VERSIONAMENTO**

### **Comando Principal:**
```bash
python versionar_rpa.py <versao>
```

### **Exemplos de Uso:**
```bash
# Criar versão 2.6.0
python versionar_rpa.py 2.6.0

# Criar versão 3.0.0
python versionar_rpa.py 3.0.0

# Listar versões existentes
python versionar_rpa.py --list

# Mostrar ajuda
python versionar_rpa.py --help
```

### **Funcionalidades do Script:**
- ✅ Criação automática de versões numeradas
- 🔍 Verificação de integridade dos arquivos
- 📊 Informações detalhadas (tamanho, timestamp)
- ⚠️ Proteção contra sobrescrita acidental
- 📋 Listagem de todas as versões disponíveis

## 📁 **ESTRUTURA DE ARQUIVOS**

```
imediatoseguros-rpa/
├── executar_rpa_imediato.py          # 🎯 ARQUIVO OFICIAL (sempre atualizado)
├── executar_rpa_imediato_v2.5.1.py  # 📁 VERSÃO v2.5.1 (commitada)
├── executar_rpa_imediato_v2.6.0.py  # 📁 VERSÃO v2.6.0 (futura)
├── versionar_rpa.py                  # 🛠️ SCRIPT DE VERSIONAMENTO
├── parametros.json                   # ⚙️ CONFIGURAÇÕES
└── ... outros arquivos
```

## 🎯 **BENEFÍCIOS DA ESTRATÉGIA**

### **1. Controle de Versões:**
- ✅ Histórico completo de todas as versões
- 🔍 Comparação fácil entre versões
- 📊 Rastreamento de mudanças

### **2. Manutenção:**
- 🛠️ Rollback rápido para versões anteriores
- 🔧 Debug de problemas específicos de versão
- 📝 Documentação automática de releases

### **3. Produção:**
- 🚀 Arquivo oficial sempre disponível
- 🔒 Versões estáveis preservadas
- 📋 Seleção de versão para deploy

### **4. Desenvolvimento:**
- 💻 Fluxo de trabalho simplificado
- 🔄 Versionamento automatizado
- 📁 Organização clara dos arquivos

## 📋 **EXEMPLO PRÁTICO**

### **Cenário: Implementar nova funcionalidade**

```bash
# 1. Desenvolver no arquivo oficial
📝 executar_rpa_imediato.py ← Nova funcionalidade

# 2. Testar
🧪 python executar_rpa_imediato.py

# 3. Versionar
🚀 python versionar_rpa.py 2.6.0

# 4. Commit no GitHub
💾 git add .
💾 git commit -m "v2.6.0 - Nova funcionalidade implementada"
🚀 git push origin master

# 5. Continuar desenvolvimento
📝 executar_rpa_imediato.py ← Próxima funcionalidade
```

## 🔍 **COMANDOS ÚTEIS**

### **Listar Versões:**
```bash
python versionar_rpa.py --list
```

### **Verificar Arquivo Oficial:**
```bash
ls -la executar_rpa_imediato.py
```

### **Comparar Versões:**
```bash
# Windows
fc executar_rpa_imediato_v2.5.1.py executar_rpa_imediato_v2.6.0.py

# Linux/Mac
diff executar_rpa_imediato_v2.5.1.py executar_rpa_imediato_v2.6.0.py
```

## ⚠️ **REGRAS IMPORTANTES**

### **1. NUNCA editar arquivos de versão:**
- ❌ `executar_rpa_imediato_v2.5.1.py` ← NÃO EDITAR
- ✅ `executar_rpa_imediato.py` ← SEMPRE EDITAR

### **2. Sempre versionar antes do commit:**
- 🔄 Desenvolver → Testar → Versionar → Commit
- 📁 Manter histórico organizado

### **3. Nomenclatura consistente:**
- 🏷️ Formato: `executar_rpa_imediato_v<versao>.py`
- 📝 Versões: 2.5.1, 2.6.0, 3.0.0, etc.

## 🎉 **CONCLUSÃO**

Esta estratégia de versionamento proporciona:

- **Organização clara** dos arquivos
- **Controle total** das versões
- **Facilidade** na manutenção
- **Segurança** para produção
- **Automação** do processo

**🚀 Sistema RPA Tô Segurado - Versionamento Profissional Implementado!**
