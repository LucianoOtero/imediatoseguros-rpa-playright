# 🚀 SCRIPTS DE INSTALAÇÃO AUTOMATIZADA - IMEDIATO SEGUROS RPA

## 📋 VISÃO GERAL

Este diretório contém **scripts de instalação automatizada** que fazem todo o processo de configuração do ambiente RPA Imediato Seguros automaticamente.

**Data de Criação**: 04/09/2025  
**Versão**: 1.0.0  
**Autor**: Luciano Otero

---

## 📦 **ARQUIVOS DISPONÍVEIS**

### **🖥️ Scripts de Instalação**

| **Arquivo** | **Tipo** | **Descrição** |
|---|---|---|
| `INSTALAR_TUDO.bat` | Batch (CMD) | Script principal para Windows |
| `INSTALAR_TUDO.ps1` | PowerShell | Script avançado para Windows |
| `setup_ambiente.py` | Python | Script multiplataforma |

### **📄 Documentação**

| **Arquivo** | **Descrição** |
|---|---|
| `AMBIENTE_DE_DESENVOLVIMENTO_COMPLETO.md` | Lista completa de componentes |
| `GUIA_MIGRACAO.md` | Guia de migração passo-a-passo |
| `requirements.txt` | Dependências Python |

---

## 🚀 **COMO USAR**

### **🎯 OPÇÃO 1: Script .bat (RECOMENDADO)**

```bash
# 1. Baixe o arquivo INSTALAR_TUDO.bat
# 2. Execute no terminal:
INSTALAR_TUDO.bat

# Ou clique duas vezes no arquivo
```

### **🎯 OPÇÃO 2: Script PowerShell**

```bash
# 1. Abra PowerShell como administrador
# 2. Execute:
.\INSTALAR_TUDO.ps1
```

### **🎯 OPÇÃO 3: Script Python**

```bash
# 1. Execute:
python setup_ambiente.py
```

---

## 📋 **O QUE OS SCRIPTS FAZEM**

### **✅ VERIFICAÇÃO DE PRÉ-REQUISITOS**
- 🔍 Verifica se Python está instalado
- 🔍 Verifica se Git está instalado
- ❌ Para se algo estiver faltando

### **✅ CLONAGEM AUTOMÁTICA**
- 📥 Clona o repositório do GitHub
- 🔧 Remove versões antigas se existirem
- 📁 Entra no diretório automaticamente

### **✅ INSTALAÇÃO DE DEPENDÊNCIAS**
- 🔧 Atualiza pip
- 🌐 Instala Playwright 1.55.0
- 🌐 Instala navegadores (Chromium, Firefox, WebKit)
- 📦 Instala todas as dependências Python

### **✅ CONFIGURAÇÃO DO AMBIENTE**
- 🔧 Cria arquivo .env
- 📝 Configura variáveis de ambiente
- 🎯 Define caminhos do Playwright

### **✅ TESTE DE FUNCIONAMENTO**
- 🧪 Testa Python
- 🧪 Testa Playwright
- 🧪 Testa RPA
- ✅ Confirma sucesso

### **✅ ASSISTÊNCIA PÓS-INSTALAÇÃO**
- 📝 Oferece abrir parametros.json
- 📚 Oferece abrir documentação
- 📋 Mostra próximos passos

---

## 🎯 **PRÉ-REQUISITOS**

### **📋 ANTES de executar os scripts:**

#### **1. Python 3.13.7+**
```bash
# Baixar de: https://www.python.org/downloads/
# ✅ IMPORTANTE: Marcar "Add Python to PATH"
```

#### **2. Git 2.50.1+**
```bash
# Baixar de: https://git-scm.com/download/win
```

---

## 🔧 **EXECUÇÃO DETALHADA**

### **📋 Passo 1: Preparação**
```bash
# 1. Instalar Python (se não tiver)
# 2. Instalar Git (se não tiver)
# 3. Abrir terminal/PowerShell
```

### **📋 Passo 2: Execução**
```bash
# Opção A - Batch (mais simples)
INSTALAR_TUDO.bat

# Opção B - PowerShell (mais avançado)
.\INSTALAR_TUDO.ps1

# Opção C - Python (multiplataforma)
python setup_ambiente.py
```

### **📋 Passo 3: Configuração**
```bash
# 1. Preencher parametros.json
# 2. Testar funcionamento
python executar_rpa_imediato_playwright.py --help
```

---

## 🚨 **SOLUÇÃO DE PROBLEMAS**

### **❌ Python não encontrado**
```bash
# Solução: Instalar Python
# https://www.python.org/downloads/
# ✅ Marcar "Add Python to PATH"
```

### **❌ Git não encontrado**
```bash
# Solução: Instalar Git
# https://git-scm.com/download/win
```

### **❌ Erro de permissão (PowerShell)**
```bash
# Solução: Executar como administrador
# Ou executar: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### **❌ Erro de conexão**
```bash
# Solução: Verificar internet
# Ou usar proxy se necessário
```

---

## 📊 **COMPARAÇÃO DOS SCRIPTS**

| **Recurso** | **.bat** | **PowerShell** | **Python** |
|---|---|---|---|
| **Facilidade** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Funcionalidades** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Compatibilidade** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Cores/Interface** | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Tratamento de Erros** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |

### **🎯 RECOMENDAÇÃO:**
- **Iniciantes**: Use `INSTALAR_TUDO.bat`
- **Avançados**: Use `INSTALAR_TUDO.ps1`
- **Multiplataforma**: Use `setup_ambiente.py`

---

## 📞 **SUPORTE**

### **📧 Contato**
- **Email**: lrotero@gmail.com
- **Desenvolvedor**: Luciano Otero

### **📚 Documentação**
- **Ambiente Completo**: `AMBIENTE_DE_DESENVOLVIMENTO_COMPLETO.md`
- **Guia de Migração**: `GUIA_MIGRACAO.md`
- **Controle de Versão**: `docs/CONTROLE_VERSAO.md`

### **🔧 Problemas Comuns**
1. **Python não no PATH**: Reinstalar Python marcando "Add to PATH"
2. **Erro de permissão**: Executar PowerShell como administrador
3. **Erro de conexão**: Verificar internet e firewall
4. **Dependências conflitantes**: Usar ambiente virtual

---

## 🎉 **RESULTADO ESPERADO**

### **✅ Após execução bem-sucedida:**
- ✅ Python 3.13.7 funcionando
- ✅ Playwright 1.55.0 instalado
- ✅ Navegadores instalados (Chromium, Firefox, WebKit)
- ✅ Todas as dependências instaladas
- ✅ Arquivo .env criado
- ✅ RPA funcionando
- ✅ Documentação disponível

### **📋 Próximos passos:**
1. Configurar `parametros.json`
2. Testar RPA: `python executar_rpa_imediato_playwright.py --help`
3. Executar RPA: `python executar_rpa_imediato_playwright.py`

---

**Status**: ✅ **SCRIPTS PRONTOS PARA USO**  
**Última Atualização**: 04/09/2025  
**Versão**: 1.0.0

**🎯 RESULTADO**: Instalação 100% automatizada!













