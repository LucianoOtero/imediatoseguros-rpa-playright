# 🚀 Configuração do GitHub para o RPA Tô Segurado

## 📋 **Pré-requisitos**
- ✅ Conta no GitHub criada
- ✅ Git configurado localmente
- ✅ Repositório local inicializado e com commit

## 🔧 **Passo a Passo para Conectar ao GitHub**

### **1. Criar Repositório no GitHub**
1. Acesse: https://github.com
2. Faça login na sua conta
3. Clique em **"New repository"** (botão verde)
4. Configure o repositório:
   - **Repository name**: `imediatoseguros-rpa`
   - **Description**: `RPA Tô Segurado - Automação de Cotação de Seguros Auto`
   - **Visibility**: `Public` ou `Private` (sua escolha)
   - **NÃO marque** "Add a README file" (já temos)
   - **NÃO marque** "Add .gitignore" (já temos)
   - **NÃO marque** "Choose a license" (já temos)
5. Clique em **"Create repository"**

### **2. Conectar Repositório Local ao GitHub**

#### **Opção A: HTTPS (Recomendado para iniciantes)**
```bash
# Adicionar remote origin
git remote add origin https://github.com/SEU_USUARIO/imediatoseguros-rpa.git

# Verificar remote
git remote -v

# Fazer push da branch master
git push -u origin master

# Fazer push das tags
git push origin --tags
```

#### **Opção B: SSH (Para usuários avançados)**
```bash
# Adicionar remote origin via SSH
git remote add origin git@github.com:SEU_USUARIO/imediatoseguros-rpa.git

# Verificar remote
git remote -v

# Fazer push da branch master
git push -u origin master

# Fazer push das tags
git push origin --tags
```

### **3. Verificar Conexão**
```bash
# Verificar status
git status

# Verificar remotes
git remote -v

# Verificar branches
git branch -a
```

## 📁 **Estrutura do Repositório no GitHub**

Após o push, você verá:
```
imediatoseguros-rpa/
├── 📄 README.md                    # Documentação principal
├── 📄 LICENSE                      # Licença MIT
├── 📄 requirements.txt             # Dependências Python
├── 📄 .gitignore                   # Arquivos ignorados
├── 📄 executar_todas_telas_corrigido.py  # Script principal
├── 📄 parametros_exemplo.json     # Exemplo de parâmetros
├── 📄 install_windows.bat         # Instalação Windows (batch)
└── 📄 install_windows.ps1         # Instalação Windows (PowerShell)
```

## 🔄 **Comandos Git Úteis para o Futuro**

### **Fazer Mudanças e Commits**
```bash
# Ver status
git status

# Adicionar arquivos
git add .

# Fazer commit
git commit -m "feat: Nova funcionalidade"

# Fazer push
git push origin master
```

### **Criar Nova Versão**
```bash
# Fazer commit das mudanças
git add .
git commit -m "feat: Nova funcionalidade implementada"

# Criar nova tag
git tag -a v1.1.0 -m "Versão 1.1.0 - Nova funcionalidade"

# Fazer push das mudanças e tag
git push origin master
git push origin --tags
```

### **Voltar para Versão Anterior (Rollback)**
```bash
# Ver histórico de commits
git log --oneline

# Ver tags disponíveis
git tag -l

# Voltar para versão específica
git checkout v1.0.0

# Ou voltar para commit específico
git checkout 919cb25
```

## 🚨 **Importante: Segurança**

### **Arquivos NÃO Versionados (por segurança)**
- `parametros.json` - Dados pessoais
- `chromedriver/` - Driver do Chrome
- `temp/` - Arquivos temporários
- `venv/` - Ambiente virtual
- `*.log` - Logs de execução

### **Arquivos Versionados (seguros)**
- `parametros_exemplo.json` - Exemplo sem dados pessoais
- Scripts Python principais
- Documentação
- Scripts de instalação

## 📊 **Benefícios do GitHub**

1. **Backup na Nuvem** - Seu código está seguro
2. **Controle de Versão** - Histórico completo de mudanças
3. **Rollback Fácil** - Volte para qualquer versão anterior
4. **Colaboração** - Outros desenvolvedores podem contribuir
5. **Issues** - Rastrear problemas e melhorias
6. **Actions** - Automação de testes futuros
7. **Documentação** - README sempre atualizado

## 🎯 **Próximos Passos**

1. ✅ **Conectar ao GitHub** (seguir passos acima)
2. 🔄 **Fazer push inicial** da versão 1.0.0
3. 📝 **Criar Issues** para melhorias futuras
4. 🚀 **Compartilhar** o repositório com a equipe
5. 🔧 **Configurar Actions** para automação (opcional)

## 📞 **Suporte**

- **GitHub Docs**: https://docs.github.com
- **Git Tutorial**: https://git-scm.com/docs/gittutorial
- **Issues**: Use o sistema de issues do GitHub para problemas

---

**🎉 Parabéns!** Seu RPA Tô Segurado agora está versionado e seguro no GitHub!
