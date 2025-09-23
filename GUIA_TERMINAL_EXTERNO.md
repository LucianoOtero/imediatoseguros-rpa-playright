# 🖥️ GUIA PARA USO DO TERMINAL EXTERNO

## 📋 **INSTRUÇÕES PARA TERMINAL EXTERNO**

### **🎯 OBJETIVO:**
Evitar travamentos do Git usando terminal externo ao invés do terminal integrado do Cursor.

---

## 🚀 **COMO USAR TERMINAL EXTERNO**

### **📁 OPÇÃO 1: PowerShell Externo (RECOMENDADO)**

#### **1. Abrir PowerShell:**
- Pressione `Win + X`
- Selecione "Windows PowerShell" ou "Terminal"
- Ou pesquise "PowerShell" no menu Iniciar

#### **2. Navegar para o projeto:**
```powershell
cd "C:\Users\Luciano\OneDrive - Imediato Soluções em Seguros\Imediato\imediatoseguros-rpa-playwright"
```

#### **3. Verificar status:**
```powershell
git status
git log --oneline -5
```

### **📁 OPÇÃO 2: Git Bash Externo**

#### **1. Abrir Git Bash:**
- Clique com botão direito na pasta do projeto
- Selecione "Git Bash Here"

#### **2. Comandos Git:**
```bash
git status
git log --oneline -5
git branch -v
```

### **📁 OPÇÃO 3: CMD Externo**

#### **1. Abrir CMD:**
- Pressione `Win + R`
- Digite `cmd` e pressione Enter

#### **2. Navegar:**
```cmd
cd /d "C:\Users\Luciano\OneDrive - Imediato Soluções em Seguros\Imediato\imediatoseguros-rpa-playwright"
```

---

## 🔧 **COMANDOS GIT ESSENCIAIS**

### **📊 Verificação de Status:**
```bash
# Status do repositório
git status

# Últimos commits
git log --oneline -10

# Branches
git branch -v

# Tags
git tag -l | tail -10
```

### **🔄 Sincronização:**
```bash
# Buscar mudanças do GitHub
git fetch origin

# Baixar e integrar mudanças
git pull origin master

# Enviar mudanças para GitHub
git push origin master

# Enviar tag específica
git push origin v3.7.0.12
```

### **📝 Trabalho Diário:**
```bash
# Adicionar arquivos
git add arquivo.py
git add .

# Criar commit
git commit -m "feat: Nova funcionalidade"

# Criar tag
git tag v3.7.0.13

# Enviar tudo
git push origin master
git push origin v3.7.0.13
```

---

## ⚡ **VANTAGENS DO TERMINAL EXTERNO**

### **✅ Benefícios:**
1. **Sem travamentos** - Git funciona normalmente
2. **Performance melhor** - Sem overhead do Cursor
3. **Controle total** - Todos os comandos disponíveis
4. **Histórico completo** - Comandos anteriores visíveis
5. **Múltiplas abas** - Trabalhar em vários projetos

### **✅ Comandos que funcionam melhor:**
- `git log` com paginação
- `git tag -l` sem travamento
- `git status` instantâneo
- `git diff` completo
- `git branch -v` sem problemas

---

## 📋 **WORKFLOW RECOMENDADO**

### **🔄 Processo Diário:**

#### **1. Iniciar Trabalho:**
```bash
# Abrir terminal externo
# Navegar para projeto
cd "C:\Users\Luciano\OneDrive - Imediato Soluções em Seguros\Imediato\imediatoseguros-rpa-playwright"

# Verificar status
git status
git log --oneline -3
```

#### **2. Durante Desenvolvimento:**
```bash
# Usar Cursor para editar código
# Usar terminal externo para comandos Git
git add .
git commit -m "feat: Implementação v3.7.0.13"
```

#### **3. Finalizar Trabalho:**
```bash
# Criar tag
git tag v3.7.0.13

# Enviar para GitHub
git push origin master
git push origin v3.7.0.13

# Verificar sincronização
git status
```

---

## 🎯 **COMANDOS DE VERIFICAÇÃO**

### **📊 Status Completo:**
```bash
# Verificar se está sincronizado
git status
git log --oneline -5
git branch -v

# Verificar tags
git tag -l | tail -5

# Verificar remoto
git remote -v
```

### **🔍 Diagnóstico:**
```bash
# Verificar configurações
git config --get core.fscache
git config --get http.sslbackend
git --version

# Verificar PowerShell
$PSVersionTable
Get-ExecutionPolicy
```

---

## 📚 **RECURSOS ADICIONAIS**

### **📖 Documentação:**
- [Git Documentation](https://git-scm.com/doc)
- [PowerShell Documentation](https://docs.microsoft.com/powershell/)
- [GitHub CLI](https://cli.github.com/)

### **🔧 Ferramentas Úteis:**
- **GitHub Desktop** - Interface gráfica
- **GitKraken** - Cliente Git visual
- **SourceTree** - Cliente Git da Atlassian

---

## 🏆 **RESUMO**

### **✅ Estratégia:**
1. **Cursor** para edição de código
2. **Terminal externo** para comandos Git
3. **Melhor performance** e sem travamentos
4. **Controle total** sobre Git

### **🎯 Resultado Esperado:**
- ✅ Git funcionando perfeitamente
- ✅ Sem travamentos
- ✅ Performance otimizada
- ✅ Workflow eficiente

---

**📅 Criado em**: 10/01/2025  
**🎯 Objetivo**: Resolver travamentos Git usando terminal externo  
**✅ Status**: Pronto para uso
