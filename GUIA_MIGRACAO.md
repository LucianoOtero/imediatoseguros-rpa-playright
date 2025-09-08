# 🚀 GUIA DE MIGRAÇÃO - IMEDIATO SEGUROS RPA

## 📋 VISÃO GERAL

Este guia facilita a **migração completa** do ambiente de desenvolvimento do RPA Imediato Seguros para outro computador.

**Data de Criação**: 04/09/2025  
**Versão**: 1.0.0  
**Autor**: Luciano Otero

---

## 🎯 **OBJETIVO**

Migrar **todos os componentes, aplicativos e extensões** do ambiente atual para um novo computador, mantendo a funcionalidade 100% operacional.

---

## 📦 **ARQUIVOS DE MIGRAÇÃO**

### **📄 Documentação Completa**
- `AMBIENTE_DE_DESENVOLVIMENTO_COMPLETO.md` - Lista completa de todos os componentes
- `requirements.txt` - Todas as dependências Python com versões exatas
- `setup_ambiente.py` - Script de instalação automatizada

### **🔧 Arquivos de Configuração**
- `parametros.json` - Configurações do RPA
- `docs/CONTROLE_VERSAO.md` - Histórico completo de versões
- `.env` - Variáveis de ambiente (criado pelo script)

---

## 🚀 **PROCESSO DE MIGRAÇÃO**

### **1️⃣ PREPARAÇÃO DO NOVO COMPUTADOR**

#### **📋 Pré-requisitos**
- Windows 10/11 (recomendado)
- PowerShell 7+ (opcional, mas recomendado)
- Conexão com internet
- Acesso de administrador

#### **🔧 Instalações Básicas**
```bash
# 1. Instalar Python 3.13.7+
# Baixar de: https://www.python.org/downloads/
# ✅ Marcar "Add Python to PATH"

# 2. Instalar Git 2.50.1+
# Baixar de: https://git-scm.com/download/win

# 3. Instalar Node.js v22.18.0+ (opcional)
# Baixar de: https://nodejs.org/
```

### **2️⃣ CLONAGEM DO REPOSITÓRIO**

```bash
# Clonar repositório
git clone https://github.com/LucianoOtero/imediatoseguros-rpa-playright.git

# Entrar no diretório
cd imediatoseguros-rpa-playright

# Verificar arquivos
ls -la
```

### **3️⃣ INSTALAÇÃO AUTOMATIZADA**

```bash
# Executar script de instalação
python setup_ambiente.py
```

**O script irá:**
- ✅ Verificar Python e pip
- ✅ Criar ambiente virtual
- ✅ Instalar todas as dependências
- ✅ Instalar Playwright e navegadores
- ✅ Criar arquivo .env
- ✅ Testar instalação

### **4️⃣ CONFIGURAÇÃO MANUAL**

#### **🔐 Configurar Git**
```bash
git config --global user.name "Seu Nome"
git config --global user.email "seu.email@exemplo.com"
```

#### **📝 Configurar parametros.json**
Editar `parametros.json` com seus dados:
```json
{
  "autenticacao": {
    "email_login": "seu_email@exemplo.com",
    "senha_login": "sua_senha"
  },
  "dados_pessoais": {
    "nome": "Seu Nome",
    "cpf": "12345678901",
    "data_nascimento": "01/01/1990",
    "cep": "12345-678",
    "endereco": "Rua Exemplo, 123",
    "bairro": "Bairro Exemplo",
    "cidade": "Cidade Exemplo",
    "estado": "SP",
    "celular": "11987654321",
    "email": "seu_email@exemplo.com"
  }
}
```

#### **🌐 Configurar .env (se necessário)**
```bash
# Editar arquivo .env
notepad .env

# Adicionar suas configurações específicas
RPA_LOG_LEVEL=INFO
RPA_TIMEOUT=30
```

### **5️⃣ TESTE DE FUNCIONAMENTO**

```bash
# Ativar ambiente virtual
venv\Scripts\activate

# Testar Python
python --version
# Deve retornar: Python 3.13.7

# Testar Playwright
python -m playwright --version
# Deve retornar: Version 1.55.0

# Testar RPA
python executar_rpa_imediato_playwright.py --help
# Deve exibir a ajuda do sistema

# Testar execução (opcional)
python executar_rpa_imediato_playwright.py
```

---

## 📊 **CHECKLIST DE MIGRAÇÃO**

### **✅ Pré-requisitos**
- [ ] Python 3.13.7+ instalado
- [ ] Git 2.50.1+ instalado
- [ ] Node.js v22.18.0+ (opcional)
- [ ] PowerShell 7+ disponível

### **✅ Repositório**
- [ ] Repositório clonado
- [ ] Git configurado
- [ ] Arquivos de migração presentes

### **✅ Instalação**
- [ ] Script de instalação executado
- [ ] Ambiente virtual criado
- [ ] Dependências instaladas
- [ ] Playwright instalado
- [ ] Navegadores instalados

### **✅ Configuração**
- [ ] parametros.json configurado
- [ ] .env criado
- [ ] Git configurado

### **✅ Testes**
- [ ] Python funcionando
- [ ] Playwright funcionando
- [ ] RPA funcionando
- [ ] Execução de teste realizada

---

## 🔧 **SOLUÇÃO DE PROBLEMAS**

### **❌ Python não encontrado**
```bash
# Verificar instalação
where python
python --version

# Se não encontrado, reinstalar Python
# Baixar de: https://www.python.org/downloads/
```

### **❌ Pip não encontrado**
```bash
# Verificar pip
python -m pip --version

# Se não encontrado, reinstalar Python
# Ou executar: python -m ensurepip --upgrade
```

### **❌ Playwright não funciona**
```bash
# Reinstalar Playwright
pip install playwright==1.55.0
python -m playwright install

# Verificar navegadores
python -m playwright install --list
```

### **❌ Dependências faltando**
```bash
# Reinstalar dependências
pip install -r requirements.txt

# Ou instalar individualmente
pip install playwright==1.55.0
pip install selenium==4.35.0
pip install requests==2.32.4
```

### **❌ Git não funciona**
```bash
# Verificar Git
git --version

# Se não encontrado, reinstalar Git
# Baixar de: https://git-scm.com/download/win
```

---

## 📞 **SUPORTE**

### **📧 Contato Direto**
- **Email**: lrotero@gmail.com
- **Desenvolvedor**: Luciano Otero

### **📚 Documentação**
- **Ambiente Completo**: `AMBIENTE_DE_DESENVOLVIMENTO_COMPLETO.md`
- **Controle de Versão**: `docs/CONTROLE_VERSAO.md`
- **Repositório**: https://github.com/LucianoOtero/imediatoseguros-rpa-playright

### **🔧 Problemas Comuns**
1. **Python não no PATH**: Reinstalar Python marcando "Add to PATH"
2. **Playwright sem navegadores**: Executar `python -m playwright install`
3. **Dependências conflitantes**: Usar ambiente virtual
4. **Git não encontrado**: Verificar instalação e PATH

---

## 🎉 **CONFIRMAÇÃO DE SUCESSO**

### **✅ Indicadores de Sucesso**
- ✅ Python 3.13.7 funcionando
- ✅ Playwright 1.55.0 funcionando
- ✅ Navegadores instalados (Chromium, Firefox, WebKit)
- ✅ RPA executando sem erros
- ✅ Help do sistema funcionando
- ✅ Logs sendo gerados

### **📊 Teste Final**
```bash
# Executar teste completo
python executar_rpa_imediato_playwright.py --help

# Verificar saída esperada:
# - Opções de ajuda
# - Versão do sistema
# - Lista de funcionalidades
# - Exemplos de uso
```

---

**Status**: ✅ **GUIA DE MIGRAÇÃO COMPLETO**  
**Última Atualização**: 04/09/2025  
**Versão**: 1.0.0

**🎯 RESULTADO**: Ambiente 100% migrável e funcional!

