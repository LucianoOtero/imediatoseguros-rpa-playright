# 🚀 RPA Tô Segurado - Automação de Cotação de Seguros

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Selenium](https://img.shields.io/badge/Selenium-4.15.2-green.svg)](https://selenium-python.readthedocs.io/)
[![Windows](https://img.shields.io/badge/Windows-10+-lightgrey.svg)](https://www.microsoft.com/windows)
[![Status](https://img.shields.io/badge/Status-Funcionando-brightgreen.svg)](https://github.com/seu-usuario/imediatoseguros-rpa)

## 📋 **Descrição do Projeto**

RPA (Robotic Process Automation) desenvolvido para automatizar o processo de cotação de seguros auto no portal **Tô Segurado**. O sistema navega automaticamente por todas as 8 telas do processo de cotação, preenchendo formulários e selecionando opções conforme configurado.

## 🎯 **Funcionalidades**

- ✅ **Automação completa** das 8 telas de cotação
- ✅ **Navegação inteligente** com delays otimizados
- ✅ **Fallback JavaScript** para elementos problemáticos
- ✅ **Sistema de debug** com screenshots e HTML
- ✅ **Tratamento de erros** robusto
- ✅ **Configuração Windows** otimizada
- ✅ **Logs detalhados** de execução

## 🏗️ **Arquitetura do Sistema**

### **Fluxo de Telas:**
1. **Tela 1**: Seleção do tipo de seguro (Carro)
2. **Tela 2**: Inserção da placa do veículo
3. **Tela 3**: Confirmação do modelo ECOSPORT
4. **Tela 4**: Pergunta sobre veículo já segurado
5. **Tela 5**: Estimativa inicial de cobertura
6. **Tela 6**: Tipo de combustível + checkboxes
7. **Tela 7**: Endereço de pernoite (CEP)
8. **Tela 8**: Finalidade do veículo

### **Estratégias Implementadas:**
- **Delays extremos** para estabilização (15-20s)
- **Fallback JavaScript** para cliques problemáticos
- **Detecção inteligente** de elementos por texto
- **Sistema de debug** completo com salvamento de estado

## 🚀 **Instalação e Configuração**

### **Pré-requisitos:**
- Windows 10 ou superior
- Python 3.8+
- Google Chrome instalado
- Conta no GitHub (para controle de versão)

### **Passo a Passo:**

#### **1. Clone o Repositório:**
```bash
git clone https://github.com/seu-usuario/imediatoseguros-rpa.git
cd imediatoseguros-rpa
```

#### **2. Crie um Ambiente Virtual:**
```bash
python -m venv venv
venv\Scripts\activate
```

#### **3. Instale as Dependências:**
```bash
pip install -r requirements.txt
```

#### **4. Baixe o ChromeDriver:**
- Acesse: https://chromedriver.chromium.org/
- Baixe a versão compatível com seu Chrome
- Extraia para: `./chromedriver/chromedriver-win64/`

#### **5. Configure os Parâmetros:**
Edite o arquivo `parametros.json` com seus dados:
```json
{
  "url_base": "https://www.app.tosegurado.com.br/imediatoseguros",
  "placa": "SUA_PLACA",
  "marca": "SUA_MARCA",
  "modelo": "SEU_MODELO",
  "email": "seu@email.com",
  "celular": "(11) 99999-9999"
}
```

## 🎮 **Como Usar**

### **Execução Básica:**
```bash
python executar_todas_telas_corrigido.py
```

### **Execução com Debug:**
O sistema automaticamente:
- Salva screenshots de cada etapa
- Gera logs detalhados
- Cria arquivos HTML para análise
- Salva informações em `temp/tela_XX/`

### **Monitoramento:**
- Acompanhe os logs no terminal
- Verifique arquivos gerados em `temp/`
- Analise screenshots para debug

## 🔧 **Configurações Avançadas**

### **Modo Headless:**
Por padrão, o Chrome roda em modo headless. Para visualizar:
```python
# Em configurar_chrome(), comente a linha:
# chrome_options.add_argument("--headless")
```

### **Delays Personalizados:**
Ajuste os tempos de espera em:
```python
def aguardar_estabilizacao(driver, segundos=15):
    # Ajuste o valor padrão conforme necessário
```

### **Seletores Personalizados:**
Modifique os seletores em cada função de tela conforme necessário.

## 📁 **Estrutura do Projeto**

```
imediatoseguros-rpa/
├── 📄 executar_todas_telas_corrigido.py  # Script principal
├── 📄 parametros.json                    # Configurações
├── 📄 requirements.txt                   # Dependências
├── 📄 README.md                         # Documentação
├── 📄 .gitignore                        # Arquivos ignorados
├── 📁 chromedriver/                     # ChromeDriver (não versionado)
│   └── 📁 chromedriver-win64/
│       └── 📄 chromedriver.exe
├── 📁 temp/                             # Arquivos de debug (gerados)
│   ├── 📁 tela_01/
│   ├── 📁 tela_02/
│   └── ...
└── 📁 telas/                            # Módulos de telas (se houver)
```

## 🐛 **Solução de Problemas**

### **Erro: ChromeDriver não encontrado**
```bash
# Verifique se o arquivo existe em:
./chromedriver/chromedriver-win64/chromedriver.exe
```

### **Erro: Elemento não encontrado**
- Verifique se a página carregou completamente
- Analise os arquivos HTML salvos em `temp/`
- Ajuste os seletores se necessário

### **Erro: Timeout**
- Aumente os delays nas funções
- Verifique a conexão com a internet
- Analise se o site mudou

### **Erro: [WinError 193]**
- Use ChromeDriver local (não webdriver-manager)
- Verifique se o ChromeDriver é compatível com seu Chrome

## 📊 **Logs e Debug**

### **Arquivos Gerados:**
- **HTML**: Código fonte de cada tela
- **PNG**: Screenshots de cada etapa
- **TXT**: Informações de execução

### **Localização:**
```
temp/
├── tela_01/
│   ├── tela_01_inicial.html
│   ├── tela_01_inicial.png
│   └── tela_01_inicial.txt
└── ...
```

## 🔄 **Controle de Versão**

### **Comandos Git Úteis:**
```bash
# Ver status
git status

# Adicionar mudanças
git add .

# Fazer commit
git commit -m "Descrição da mudança"

# Ver histórico
git log --oneline

# Voltar para versão anterior
git checkout <hash_commit>
```

### **Estrutura de Commits:**
- `feat:` Nova funcionalidade
- `fix:` Correção de bug
- `docs:` Documentação
- `refactor:` Refatoração de código
- `test:` Testes

## 🤝 **Contribuição**

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 **Histórico de Versões**

### **v1.0.0 (29/08/2025)**
- ✅ Implementação inicial das 8 telas
- ✅ Sistema de debug completo
- ✅ Fallback JavaScript implementado
- ✅ Configuração Windows otimizada
- ✅ Documentação completa

### **Correções Implementadas:**
- Resolvido erro [WinError 193] do ChromeDriver
- Corrigido fluxo de navegação entre telas
- Implementado sistema de delays extremos
- Adicionado tratamento de erros robusto

## 📞 **Suporte**

- **Issues**: Abra uma issue no GitHub
- **Documentação**: Consulte este README
- **Logs**: Analise os arquivos em `temp/`

## 📄 **Licença**

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 🙏 **Agradecimentos**

- Equipe de desenvolvimento
- Comunidade Python
- Documentação do Selenium
- Usuários que testaram e reportaram bugs

---

**⚠️ IMPORTANTE**: Este RPA está funcionando perfeitamente. NÃO altere o código sem testar extensivamente, pois está baseado no que funcionou em produção.

**🚀 Status**: ✅ FUNCIONANDO PERFEITAMENTE - Todas as 8 telas executadas com sucesso!
