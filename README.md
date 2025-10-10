# 🚀 Imediato Seguros RPA - Playwright

## 🎯 **RESUMO EXECUTIVO**

### **Projeto**: RPA Tô Segurado - Migração Selenium → Playwright
### **Status**: ✅ **RPA V6.7.5 IMPLEMENTADA - VERSÃO VISUAL FINAL PARA PRODUÇÃO**
### **Versão**: v6.7.5 - Sistema RPA com Visual Profissional e Moderno
### **Resultado**: Sistema RPA V6.7.5 com interface moderna, sombra elegante, layout responsivo e visual profissional pronto para produção

---

## 🏆 **CONQUISTAS REALIZADAS**

### ✅ **RPA V6.7.5 - VERSÃO VISUAL FINAL PARA PRODUÇÃO**
- **Status**: ✅ **100% FUNCIONANDO - VISUAL PROFISSIONAL E MODERNO**
- **Arquitetura**: Modal completo com 2 cards (recomendado + alternativo) + 12 campos dinâmicos
- **Funcionalidade**: Sistema RPA executando perfeitamente todas as 16 fases (1-15 + finalização)
- **Resultados Finais**: Planos recomendado e alternativo sendo capturados e exibidos corretamente
- **Valores Principais**: R$2.950,38 (recomendado) e R$4.387,32 (alternativo) sendo atualizados
- **Campos Dinâmicos**: 12 campos detalhados sendo populados automaticamente (forma de pagamento, franquia, coberturas, etc.)
- **Interface**: Modal responsivo com visual moderno, sombra elegante e layout profissional
- **Ícones**: Font Awesome funcionando corretamente (calculadora, estrela, escudo)
- **Performance**: Sistema estável e testado com timeout de 3 minutos
- **Experiência**: Interface completa funcionando com progresso em tempo real
- **Layout**: Responsivo para desktop (2 colunas) e mobile (1 coluna)
- **Código**: JavaScript unificado funcionando perfeitamente
- **Conectividade**: URLs funcionando corretamente
- **Correções**: Vazamento de estilos eliminado, seletores JavaScript corrigidos
- **Isolamento**: CSS com escopo completo (#rpaModal), sem interferência na página principal
- **Data Mapping**: Busca robusta em múltiplas estruturas JSON para garantir captura de dados
- **Formatação**: Sistema de formatação de moeda e checkmarks funcionando perfeitamente
- **Segurança**: HTTPS implementado com certificados SSL Let's Encrypt
- **Criptografia**: Todos os dados trafegam protegidos por TLS 1.2/1.3
- **Performance**: Mantida com HTTPS (<1s resposta)
- **Visual**: Interface moderna com sombra elegante, títulos e valores equilibrados, botão 'X' profissional
- **Próxima Versão**: Sistema completo e pronto para produção

---

## 🔐 **IMPLEMENTAÇÃO HTTPS V6.6.0**

### **✅ SEGURANÇA MÁXIMA IMPLEMENTADA**
- **HTTPS**: 100% funcional no servidor Hetzner (37.27.92.160)
- **Certificados**: SSL Let's Encrypt válidos até 25/12/2025
- **Criptografia**: TLS 1.2/1.3 para proteção total dos dados
- **Redirecionamento**: HTTP → HTTPS automático (301 Moved Permanently)
- **Headers**: HSTS ativo para forçar HTTPS em todos os acessos

### **🧪 TESTES REALIZADOS E APROVADOS**
- **Health Check**: ✅ API RPA funcionando via HTTPS
- **API Start**: ✅ Sessões RPA criadas com sucesso via HTTPS
- **API Progress**: ✅ Monitoramento em tempo real via HTTPS
- **Certificado SSL**: ✅ Válido e confiável
- **Performance**: ✅ Mantida (<1s resposta com HTTPS)

### **🔧 CORREÇÕES JAVASCRIPT**
- **apiBaseUrl**: Atualizado para `https://rpaimediatoseguros.com.br`
- **Chamadas API**: Todas as requisições agora usam HTTPS
- **Segurança**: Dados sensíveis protegidos por criptografia

---

## ✅ **MELHORIAS IMPLEMENTADAS**

### **🎯 MODAL SIMPLIFICADO V6.2.2**
- **Decisão**: Remoção do card de estimativa inicial do modal
- **Motivo**: Melhorar experiência do usuário focando nos resultados finais
- **Resultado**: Interface mais limpa e direta
- **Layout**: Grid otimizado para 2 colunas (sem espaços vazios)
- **Status**: Implementado e funcionando perfeitamente

### **✅ FUNCIONALIDADES FUNCIONANDO PERFEITAMENTE**
- **Execução RPA**: Todas as 15 telas executando com sucesso
- **Captura de Dados**: Planos finais (recomendado e alternativo) sendo capturados
- **Progress Tracker**: Monitoramento em tempo real funcionando
- **Interface**: Modal simplificado com 2 cards funcionando
- **Responsividade**: Layout adaptativo para desktop e mobile
- **Conectividade**: APIs respondendo corretamente

---
- **Status**: ✅ **100% CONCLUÍDO**
- **Telas implementadas**: 1-15 (todas)
- **Funcionalidades críticas**: 100% migradas
- **Performance**: Superior ao Selenium original
- **Estabilidade**: Excelente

### ✅ **SISTEMA DE NAVEGAÇÃO ROBUSTO**
- **Navegação automática**: Todas as telas funcionando
- **Tratamento de acentuação**: Implementado
- **Case-sensitivity**: Resolvido
- **Timeouts**: Otimizados
- **Fallbacks**: Implementados

### ✅ **CAPTURA DE DADOS AVANÇADA**
- **Valores dos planos**: Capturados corretamente
- **Parcelamento**: Implementado
- **Coberturas**: Detectadas automaticamente
- **Estrutura JSON**: Padronizada
- **Logs detalhados**: Implementados

### ✅ **CORREÇÕES DE REGRESSÕES**
- **Tela 9**: Corrigida (Estado Civil, Email, Celular)
- **Tela 10**: Corrigida (navegação e dados)
- **Telas 11-15**: Implementadas com sucesso
- **Sintaxe**: Corrigida e validada

### ✅ **SUPORTE A TIPO DE VEÍCULO (v3.3.0)**
- **Carros e Motos**: Suporte completo implementado
- **Seletores específicos**: Para cada tipo de veículo
- **Validação de domínio**: `carro` ou `moto` apenas
- **Tratamento condicional**: Campo `kit_gas` ignorado para motos
- **Compatibilidade**: Total com versões anteriores

### ✅ **SISTEMA RPA V3 COM EXECUÇÃO EM BACKGROUND (v3.8.0)**
- **Execução em background**: Via systemd para gerenciamento robusto
- **API REST completa**: executar_rpa_v3.php com endpoints funcionais
- **Monitoramento em tempo real**: JSON progressivo por tela
- **Múltiplas sessões**: Execuções simultâneas isoladas
- **Scripts de controle**: start, monitor e cleanup automatizados
- **Health checks**: Verificação automática de dependências
- **Logs estruturados**: Sistema completo por sessão
- **Testado no Hetzner**: Validado em ambiente de produção

### ✅ **PROGRESSTRACKER COM ESTIMATIVAS DA TELA 5 (v3.5.1)**
- **ProgressTracker integrado**: Diretamente em `navegar_tela_5_playwright()`
- **Estimativas em tempo real**: Dados da Tela 5 transmitidos instantaneamente
- **Deduplicação inteligente**: 3 coberturas únicas (CompreensivaDe, Roubo, RCFDe)
- **Arquivo JSON populado**: Estimativas salvas em `rpa_data/progress_*.json`
- **Arquitetura simplificada**: 69 linhas removidas (wrapper desnecessário)
- **Backend Redis e JSON**: Ambos suportam estimativas da Tela 5
- **Interface unificada**: Detecção automática de backend
- **Session management**: Suporte a execuções concorrentes

### ✅ **DETECÇÃO DE COTAÇÃO MANUAL (v3.4.0)**
- **Detecção automática**: Quando não há cotação automática
- **Wait condicional**: Após modal de login
- **Captura de dados**: Para análise manual pelo corretor
- **Retorno específico**: `status: cotacao_manual`
- **Arquivo JSON**: Dados salvos para análise

---

## 🚀 **INSTALAÇÃO E CONFIGURAÇÃO**

### **Pré-requisitos**
```bash
# Python 3.8+
python --version

# Node.js (para Playwright)
node --version
```

### **Instalação**
```bash
# Clone o repositório
git clone https://github.com/LucianoOtero/imediatoseguros-rpa-playright.git
cd imediatoseguros-rpa-playwright

# Instale as dependências Python
pip install -r requirements.txt

# Instale os navegadores do Playwright
playwright install
```

### **Configuração**
```bash
# Configure os parâmetros no arquivo
config/parametros.json

# Exemplo de configuração:
{
  "placa": "EED-3D56",
  "nome": "João Silva",
  "cpf": "123.456.789-00",
  "data_nascimento": "01/01/1990",
  "email": "joao@email.com",
  "celular": "(11) 99999-9999"
}
```

---

## 📱 **EXECUÇÃO**

### **Execução Completa**
```bash
# Execute o RPA completo
python executar_rpa_imediato_playwright.py
```

### **Execução de Testes**
```bash
# Execute testes específicos
python teste_tela_1_a_15_sequencial.py
```

### **Resultados**
- **Arquivo de saída**: `dados_planos_seguro_YYYYMMDD_HHMMSS.json`
- **Logs**: Console em tempo real
- **Screenshots**: Capturados automaticamente em caso de erro

---

## 📊 **FUNCIONALIDADES IMPLEMENTADAS**

### **✅ Sistema de Retorno Estruturado (NOVO)**
- ✅ **Códigos de retorno padronizados** (9001-9999)
- ✅ **Estrutura JSON consistente** com status, código, mensagem
- ✅ **Validação automática** de retornos
- ✅ **Conversão de formatos antigos** para novo padrão
- ✅ **Logs estruturados** com timestamps precisos

### **✅ TELA ZERO KM (CONDICIONAL) - NOVO**
- ✅ **Detecção automática** após Tela 5
- ✅ **Seleção inteligente** baseada no parâmetro `zero_km`
- ✅ **Transição suave** para Tela 6
- ✅ **Tratamento de ambiguidade** de seletores
- ✅ **Suporte para carros e motos**

### **✅ DETECÇÃO DE COTAÇÃO MANUAL (v3.4.0) - NOVO**
- ✅ **Detecção automática** quando não há cotação automática
- ✅ **Wait condicional** após modal de login
- ✅ **Captura de dados** para análise manual pelo corretor
- ✅ **Retorno específico** (`status: cotacao_manual`)
- ✅ **Arquivo JSON** com dados coletados
- ✅ **Logs detalhados** para monitoramento

### **Telas Implementadas (16/16)**
- ✅ **Tela 1**: Seleção do Tipo de Seguro (Carro/Moto)
- ✅ **Tela 2**: Inserção da Placa
- ✅ **Tela 3**: Dados do Veículo
- ✅ **Tela 4**: Dados do Proprietário
- ✅ **Tela 5**: Carrossel de Estimativas
- ✅ **Tela Zero KM**: Detecção Condicional
- ✅ **Tela 6**: Seleção de Coberturas (Kit Gas condicional)
- ✅ **Tela 7**: Dados do Condutor
- ✅ **Tela 8**: Dados do Condutor (Continuação)
- ✅ **Tela 9**: Dados Pessoais
- ✅ **Tela 10**: Dados do Veículo (Continuação)
- ✅ **Tela 11**: Dados do Veículo (Finalização)
- ✅ **Tela 12**: Confirmação de Dados
- ✅ **Tela 13**: Seleção de Plano
- ✅ **Tela 14**: Dados de Pagamento (Condicional)
- ✅ **Tela 15**: Captura de Dados dos Planos

### **Captura de Dados**
- ✅ **Valores dos planos** (R$2.401,53, R$3.122,52)
- ✅ **Parcelamento** (12x sem juros, 1x sem juros)
- ✅ **Coberturas** (Assistência, Vidros, Carro Reserva)
- ✅ **Valores de danos** (Materiais, Corporais, Morais)
- ✅ **Tipo de franquia** (Normal, Reduzida)
- ✅ **Tipo de veículo** (Carro, Moto) - NOVO
- ✅ **Cotação manual** (Dados para análise) - NOVO
- ✅ **Estrutura JSON** padronizada

---

## 📁 **ESTRUTURA DO PROJETO**

```
imediatoseguros-rpa-playwright/
├── 📁 rpa-v4/                               # RPA V4 - Arquitetura Modular
│   ├── 📁 src/                              # Código fonte modular
│   │   ├── 📁 Controllers/                  # Controladores API
│   │   ├── 📁 Services/                     # Serviços de negócio
│   │   ├── 📁 Repositories/                 # Persistência de dados
│   │   └── 📁 Interfaces/                   # Contratos de interface
│   ├── 📁 public/                           # API e Dashboard
│   │   ├── 📄 index.php                     # Endpoint principal
│   │   ├── 📄 dashboard.html                # Dashboard web
│   │   └── 📁 js/                           # JavaScript do dashboard
│   ├── 📁 config/                           # Configurações
│   ├── 📁 tests/                            # Testes automatizados
│   ├── 📄 deploy.sh                         # Deploy automatizado
│   └── 📄 README.md                         # Documentação V4
├── 📄 executar_rpa_v3.php                   # RPA V3 - Sistema atual
├── 📄 get_progress_completo.php             # Monitoramento V3
├── 📄 parametros.json                       # Configurações V3
├── 📄 executar_rpa_imediato_playwright.py  # Script principal Python
├── 📁 utils/                                # Utilitários Python
├── 📁 scripts/                              # Scripts de controle
├── 📁 docs/                                 # Documentação
├── 📁 logs/                                 # Logs de execução
├── 📁 screenshots/                          # Screenshots de debug
├── 📁 temp/                                 # Arquivos temporários
├── 📄 requirements.txt                      # Dependências Python
├── 📄 README.md                             # Este arquivo
└── 📄 CHANGELOG.md                          # Histórico de versões
```

---

## 🔧 **CONFIGURAÇÃO AVANÇADA**

### **Parâmetros de Configuração**
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

### **Configuração do Browser**
```python
# Configurações padrão do Playwright
browser = playwright.chromium.launch(headless=False)
context = browser.new_context(
    viewport={'width': 1139, 'height': 1378},
    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
)
```

---

## 📊 **MÉTRICAS DE PERFORMANCE**

### **Tempos de Execução**
- **Tela 1**: ~3s
- **Tela 2**: ~6s
- **Tela 3**: ~3s
- **Tela 4**: ~3s
- **Tela 5**: ~30s (incluindo captura)
- **Tela 6**: ~3s
- **Tela 7**: ~3s
- **Tela 8**: ~3s
- **Tela 9**: ~3s
- **Tela 10**: ~3s
- **Tela 11**: ~3s
- **Tela 12**: ~3s
- **Tela 13**: ~3s
- **Tela 14**: ~3s (condicional)
- **Tela 15**: ~10s (captura de dados)
- **Total**: ~70s

### **Taxa de Sucesso**
- **Navegação**: 100%
- **Captura de dados**: 100%
- **Parse de valores**: 100%
- **Estruturação JSON**: 100%

---

## 🚨 **COMPONENTES PENDENTES**

### **Prioridade Alta**
- 🔄 **Sistema de Retorno Estruturado**
- 📊 **Sistema de Validação de Parâmetros**

### **Prioridade Média**
- 📝 **Sistema de Logger Avançado**
- 🔄 **Conversor Unicode → ASCII**
- 📊 **Sistema de Screenshots de Debug**
- 🔄 **Modo de Execução via Linha de Comando**

### **Não Implementar**
- 🔧 **Sistema de Helpers** (Específico do Selenium)
- 📊 **Captura de Dados da Tela 5** (Já funcionando)

---

## 🐛 **TROUBLESHOOTING**

### **Problemas Comuns**

#### **1. Elemento não encontrado**
```bash
# Verificar se a página carregou completamente
# Aguardar mais tempo de carregamento
# Verificar seletor CSS
```

#### **2. Timeout de carregamento**
```bash
# Aumentar tempo de timeout
# Verificar conexão com internet
# Verificar se o site está acessível
```

#### **3. Dados não capturados**
```bash
# Verificar estrutura da página
# Verificar seletores CSS
# Verificar logs de debug
```

### **Logs de Debug**
```bash
# Verificar logs em tempo real
# Verificar arquivo de log
# Verificar screenshots de erro
```

---

## 📈 **ROADMAP**

## 📈 **ROADMAP**

### **v3.4.0 (IMPLEMENTADO)**
- ✅ Detecção de Cotação Manual
- ✅ Wait Condicional após Modal de Login
- ✅ Captura de Dados para Análise Manual
- ✅ Retorno Específico (`status: cotacao_manual`)
- ✅ Arquivo JSON com Dados Coletados

### **v3.3.0 (IMPLEMENTADO)**
- ✅ Suporte a Tipo de Veículo (Carro/Moto)
- ✅ Seletores Específicos para Cada Tipo
- ✅ Validação de Domínio (`carro` ou `moto`)
- ✅ Tratamento Condicional do Campo `kit_gas`
- ✅ Compatibilidade Total com Versões Anteriores

### **v3.2.0 (IMPLEMENTADO)**
- ✅ Tela Zero KM Condicional
- ✅ Campo tipo_franquia na captura de dados
- ✅ Detecção automática de telas condicionais
- ✅ Tratamento de ambiguidade de seletores

### **v3.1.0 (IMPLEMENTADO)**
- ✅ Sistema de Retorno Estruturado
- ✅ Teste Ponta-a-Ponta Completo
- ✅ Validação e Estrutura JSON Padronizada

### **v3.5.1 (IMPLEMENTADO)**
- ✅ ProgressTracker com Estimativas da Tela 5
- ✅ Deduplicação Inteligente de Coberturas
- ✅ Arquitetura Simplificada
- ✅ Backend Redis e JSON Suportam Estimativas
- ✅ Interface Unificada com Detecção Automática
- ✅ Session Management para Execuções Concorrentes

### **v4.1.0 (PRÓXIMA VERSÃO)**
- 🔄 **Monitoramento em tempo real**: Implementar endpoint `/api/rpa/progress/{session_id}`
- 📊 **JSON dinâmico**: Modificar chamada do RPA para receber JSON via linha de comando
- 🔄 **Migração RPA principal**: Consolidar RPA modular no arquivo principal
- 🔧 **Integração Webflow**: JavaScript para modal de monitoramento
- 🔐 **Validação robusta**: Reativar validação de entrada com regras aprimoradas
- 📊 **Performance**: Otimizações de concorrência e cache

### **📋 Planos Registrados**
- **PLANO_PROJETO_RPA_V4_OBJETIVOS.md**: Objetivos detalhados para execução concorrente e integração Webflow
- **PLANO_PRODUCAO_RPA_V4.md**: Próximos passos para produção (monitoramento, JSON dinâmico, migração)
- **PROJETO_RPA_V4_INCREMENTAL.md**: Estratégia incremental de implementação

---

## 🏗️ **ARQUITETURA DA SOLUÇÃO RPA V4**

### **Visão Geral**
Sistema RPA V4 para automação de cotação de seguros no portal `app.tosegurado.com.br`, executando em background com monitoramento em tempo real via API REST.

### **Objetivo Principal**
Executar `executar_rpa_imediato_playwright.py` em sessões concorrentes em background, chamado via JSON de parâmetros via linha de comando a partir de JavaScript no `segurosimediato.com.br` (Webflow), com monitoramento de progresso em tempo real.

### **Componentes da Arquitetura**

```
┌─────────────────────────────────────────────────────────────┐
│                    WEBFLOW (Frontend)                      │
│  segurosimediato.com.br                                     │
│  - Formulário de cotação                                    │
│  - Modal de progresso                                       │
│  - JavaScript para chamadas API                             │
└─────────────────────┬───────────────────────────────────────┘
                      │ HTTP/HTTPS
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                    NGINX (Proxy Reverso)                   │
│  Porta 80/443                                               │
│  - SSL/TLS                                                  │
│  - Load balancing                                           │
│  - Static files                                             │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                    PHP-FPM (Backend)                       │
│  Porta 9000                                                 │
│  - API REST V4                                              │
│  - SessionService.php                                       │
│  - get_progress_completo.php                                │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                    RPA PYTHON (Automation)                 │
│  executar_rpa_imediato_playwright.py                       │
│  - 15 telas de automação                                    │
│  - Playwright + Chromium                                    │
│  - Progress tracker JSON                                    │
└─────────────────────────────────────────────────────────────┘
```

### **API REST V4**

#### **Endpoint: `POST /api/rpa/start`**
**Função**: Criar nova sessão RPA e iniciar execução em background

**Request**:
```json
{
    "cpf": "12345678901",
    "nome": "João Silva",
    "placa": "ABC1234",
    "cep": "01234567",
    "email": "joao@email.com",
    "telefone": "11999999999"
}
```

**Response**:
```json
{
    "success": true,
    "session_id": "rpa_v4_20251001_222340_28563ee9",
    "message": "Sessão RPA criada com sucesso",
    "timestamp": "2025-10-01T22:23:40Z"
}
```

#### **Endpoint: `GET /api/rpa/progress/{session_id}`**
**Função**: Obter progresso em tempo real da execução RPA

**Response**:
```json
{
    "success": true,
    "progress": {
        "etapa_atual": 15,
        "total_etapas": 15,
        "percentual": 100,
        "status": "success",
        "estimativas": {
            "capturadas": true,
            "dados": {
                "plano_recomendado": "R$ 3.743,52",
                "plano_alternativo": "R$ 3.962,68"
            }
        },
        "resultados_finais": {
            "rpa_finalizado": true,
            "dados": {
                "valor_final": "R$ 3.743,52",
                "cobertura": "Completa"
            }
        }
    }
}
```

### **Fluxo de Execução**

#### **1. Início da Sessão**
```
Webflow → POST /api/rpa/start → SessionService.php → Script Bash → RPA Python
```

#### **2. Monitoramento**
```
Webflow → GET /api/rpa/progress/{session_id} → get_progress_completo.php → JSON Response
```

#### **3. Progress Tracker**
```
RPA Python → progress_{session_id}.json → get_progress_completo.php → Webflow
```

### **Estrutura de Diretórios**

```
/opt/imediatoseguros-rpa/
├── executar_rpa_imediato_playwright.py    # RPA principal
├── parametros.json                        # Dados de teste
├── venv/                                  # Ambiente Python
├── logs/                                  # Logs de execução
│   └── rpa_v4_{session_id}.log
├── rpa_data/                              # Progress tracker
│   ├── progress_{session_id}.json
│   └── history_{session_id}.json
└── sessions/                              # Sessões ativas
    └── {session_id}/
        └── status.json

/opt/imediatoseguros-rpa-v4/
├── src/
│   └── Services/
│       └── SessionService.php             # API de criação
├── get_progress_completo.php              # API de progresso
└── public/
    └── api/
        └── rpa/
            ├── start.php                  # Endpoint de início
            └── progress.php               # Endpoint de progresso
```

### **Configuração de Produção**

#### **Servidor**
- **OS**: Ubuntu 22.04 LTS
- **CPU**: 2 vCPUs
- **RAM**: 4GB
- **Storage**: 40GB SSD
- **IP**: 37.27.92.160

#### **Serviços**
- **Nginx**: 1.18.0 (Proxy reverso)
- **PHP-FPM**: 8.1 (Backend API)
- **Python**: 3.10 (RPA automation)
- **Playwright**: 1.40.0 (Browser automation)

#### **Permissões**
```bash
# Diretórios principais
chown -R www-data:www-data /opt/imediatoseguros-rpa/
chmod -R 755 /opt/imediatoseguros-rpa/

# Logs
chown -R www-data:www-data /opt/imediatoseguros-rpa/logs/
chmod -R 755 /opt/imediatoseguros-rpa/logs/

# Cache Playwright
mkdir -p /var/www/.cache
chown -R www-data:www-data /var/www/.cache
```

### **Integração Webflow**

#### **🎯 WEBHOOKS PARA BOTÃO "CALCULAR AGORA"**

Quando o botão "Calcular agora" for clicado no website Webflow, o script JavaScript injetado deve disparar **4 webhooks obrigatórios**:

##### **📋 WEBHOOKS EXISTENTES (MDMIDIA)**
- **Webhook 1**: `https://mdmidia.com.br/add_travelangels.php`
- **Webhook 2**: `https://mdmidia.com.br/add_webflow_octa.php`

##### **🚀 WEBHOOKS RPA (NOVOS)**
- **Webhook 3**: `https://rpaimediatoseguros.com.br/api/rpa/start` (Iniciar RPA)
- **Webhook 4**: `https://rpaimediatoseguros.com.br/api/rpa/progress/{session_id}` (Monitorar RPA)

#### **📋 PADRÃO DE ENVIO DE PARÂMETROS WEBFLOW**

##### **🔧 ESTRUTURA PADRÃO DOS WEBHOOKS EXISTENTES**
Os webhooks existentes (`add_travelangels.php` e `add_webflow_octa.php`) esperam receber parâmetros no formato padrão do Webflow:

```javascript
// Estrutura padrão dos dados do Webflow
const webflowData = {
    // Dados do formulário
    name: "Nome do usuário",
    email: "email@exemplo.com", 
    phone: "(11) 99999-9999",
    
    // Dados específicos do formulário de cotação
    cpf: "123.456.789-00",
    placa: "ABC1234",
    cep: "01234-567",
    tipo_veiculo: "carro",
    
    // Metadados do Webflow
    form_name: "Formulário de Cotação",
    page_url: "https://segurosimediato.com.br/cotacao",
    timestamp: "2025-01-10T15:30:00Z",
    
    // Dados adicionais (se necessário)
    utm_source: "google",
    utm_medium: "cpc",
    utm_campaign: "seguros"
};
```

##### **📤 MÉTODOS DE ENVIO SUPORTADOS**
Os webhooks existentes suportam ambos os métodos:

**Método GET (Parâmetros na URL):**
```javascript
const sendWebhookGET = (url, data) => {
    const params = new URLSearchParams(data).toString();
    return fetch(`${url}?${params}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    });
};
```

**Método POST (JSON no Body):**
```javascript
const sendWebhookPOST = (url, data) => {
    return fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });
};
```

##### **🔗 COMPATIBILIDADE COM WEBHOOKS EXISTENTES**
Para garantir que os webhooks existentes (`add_travelangels.php` e `add_webflow_octa.php`) continuem funcionando, o script JavaScript deve:

1. **Manter o formato de dados original** do Webflow
2. **Enviar dados em paralelo** para não afetar a performance
3. **Tratar erros graciosamente** se algum webhook falhar
4. **Preservar a ordem de execução** (webhooks existentes primeiro, depois RPA)

```javascript
// Exemplo de implementação compatível
const sendExistingWebhooks = async (formData) => {
    const webflowData = {
        // Dados no formato esperado pelos webhooks existentes
        name: formData.nome,
        email: formData.email,
        phone: formData.telefone,
        cpf: formData.cpf,
        placa: formData.placa,
        cep: formData.cep,
        tipo_veiculo: formData.tipo_veiculo,
        form_name: "Formulário de Cotação",
        page_url: window.location.href,
        timestamp: new Date().toISOString()
    };
    
    // Enviar para ambos os webhooks existentes em paralelo
    const promises = [
        fetch('https://mdmidia.com.br/add_travelangels.php', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(webflowData)
        }),
        fetch('https://mdmidia.com.br/add_webflow_octa.php', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(webflowData)
        })
    ];
    
    try {
        const responses = await Promise.all(promises);
        return responses.every(response => response.ok);
    } catch (error) {
        console.warn('Erro nos webhooks existentes:', error);
        return false; // Continuar mesmo se falhar
    }
};
```

##### **1. 🚀 WEBHOOK DE INÍCIO - Criar Sessão RPA**
```javascript
// Webhook 1: Iniciar processo RPA
const startRPA = async (formData) => {
    try {
        const response = await fetch('https://rpaimediatoseguros.com.br/api/rpa/start', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                cpf: formData.cpf,
                nome: formData.nome,
                placa: formData.placa,
                cep: formData.cep,
                email: formData.email,
                telefone: formData.telefone,
                tipo_veiculo: formData.tipo_veiculo || 'carro'
            })
        });

        const data = await response.json();
        if (data.success) {
            return data.session_id;
        } else {
            throw new Error(data.message || 'Erro ao iniciar RPA');
        }
    } catch (error) {
        console.error('Erro no webhook de início:', error);
        throw error;
    }
};
```

##### **2. 📊 WEBHOOK DE MONITORAMENTO - Acompanhar Progresso**
```javascript
// Webhook 2: Monitorar progresso em tempo real
const monitorProgress = async (sessionId) => {
    try {
        const progressResponse = await fetch(`https://rpaimediatoseguros.com.br/api/rpa/progress/${sessionId}`);
        const progressData = await progressResponse.json();
        
        if (progressData.success) {
            // Atualizar modal de progresso
            updateProgressModal(progressData.progress);
            
            // Verificar se processo foi concluído
            if (progressData.progress.status === 'success') {
                showFinalResults(progressData.progress.resultados_finais);
                return true; // Processo concluído
            }
            return false; // Processo em andamento
        } else {
            throw new Error(progressData.message || 'Erro ao obter progresso');
        }
    } catch (error) {
        console.error('Erro no webhook de monitoramento:', error);
        throw error;
    }
};
```

##### **🔄 FLUXO COMPLETO DE EXECUÇÃO (4 WEBHOOKS)**
```javascript
// Função principal executada no clique do botão "Calcular agora"
const handleCalculateClick = async (formData) => {
    try {
        // 1. Preparar dados para todos os webhooks
        const webflowData = {
            // Dados do formulário Webflow
            name: formData.nome,
            email: formData.email,
            phone: formData.telefone,
            cpf: formData.cpf,
            placa: formData.placa,
            cep: formData.cep,
            tipo_veiculo: formData.tipo_veiculo,
            
            // Metadados
            form_name: "Formulário de Cotação",
            page_url: window.location.href,
            timestamp: new Date().toISOString()
        };
        
        // 2. Disparar webhooks existentes (MDMIDIA)
        await Promise.all([
            sendWebhookPOST('https://mdmidia.com.br/add_travelangels.php', webflowData),
            sendWebhookPOST('https://mdmidia.com.br/add_webflow_octa.php', webflowData)
        ]);
        console.log('Webhooks MDMIDIA enviados com sucesso');
        
        // 3. Abrir modal de progresso RPA
        openProgressModal();
        
        // 4. Disparar webhook de início RPA
        const sessionId = await startRPA(formData);
        console.log('Sessão RPA criada:', sessionId);
        
        // 5. Iniciar monitoramento RPA em tempo real
        const progressInterval = setInterval(async () => {
            try {
                const isComplete = await monitorProgress(sessionId);
                
                if (isComplete) {
                    clearInterval(progressInterval);
                    console.log('Processo RPA concluído com sucesso');
                }
            } catch (error) {
                clearInterval(progressInterval);
                showError('Erro no monitoramento: ' + error.message);
            }
        }, 2000); // Verificar a cada 2 segundos
        
        // 6. Timeout de segurança (3 minutos)
        setTimeout(() => {
            clearInterval(progressInterval);
            showTimeoutMessage();
        }, 180000); // 3 minutos
        
    } catch (error) {
        console.error('Erro na execução:', error);
        showError('Erro ao iniciar cálculo: ' + error.message);
    }
};
```

#### **📋 CONFIGURAÇÃO NO WEBFLOW**

##### **Estrutura do Formulário**
```html
<!-- Formulário de cotação no Webflow -->
<form id="cotacaoForm">
    <input type="text" name="cpf" placeholder="CPF" required>
    <input type="text" name="nome" placeholder="Nome completo" required>
    <input type="text" name="placa" placeholder="Placa do veículo" required>
    <input type="text" name="cep" placeholder="CEP" required>
    <input type="email" name="email" placeholder="E-mail" required>
    <input type="tel" name="telefone" placeholder="Telefone" required>
    <select name="tipo_veiculo">
        <option value="carro">Carro</option>
        <option value="moto">Moto</option>
    </select>
    <button type="submit" id="calcularAgora">Calcular Agora</button>
</form>
```

##### **Event Listener no JavaScript**
```javascript
// Event listener para o botão "Calcular agora"
document.getElementById('cotacaoForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    // Coletar dados do formulário
    const formData = {
        cpf: document.querySelector('[name="cpf"]').value,
        nome: document.querySelector('[name="nome"]').value,
        placa: document.querySelector('[name="placa"]').value,
        cep: document.querySelector('[name="cep"]').value,
        email: document.querySelector('[name="email"]').value,
        telefone: document.querySelector('[name="telefone"]').value,
        tipo_veiculo: document.querySelector('[name="tipo_veiculo"]').value
    };
    
    // Executar fluxo completo
    await handleCalculateClick(formData);
});
```

#### **🔧 JavaScript para Chamada da API (Versão Completa - 4 Webhooks)**
```javascript
// Versão completa do JavaScript para integração Webflow com 4 webhooks
const RPAIntegration = {
    // Configurações
    config: {
        apiBaseUrl: 'https://rpaimediatoseguros.com.br',
        webhookUrls: {
            travelangels: 'https://mdmidia.com.br/add_travelangels.php',
            webflowOcta: 'https://mdmidia.com.br/add_webflow_octa.php',
            rpaStart: 'https://rpaimediatoseguros.com.br/api/rpa/start',
            rpaProgress: 'https://rpaimediatoseguros.com.br/api/rpa/progress'
        },
        pollingInterval: 2000, // 2 segundos
        maxPolls: 90, // 3 minutos (180 segundos)
        timeoutMessage: 'O cálculo está demorando mais que o esperado. Tente novamente em alguns minutos.'
    },
    
    // Webhook 1 & 2: Enviar para MDMIDIA
    async sendToMDMIDIA(webflowData) {
        const promises = [
            fetch(this.config.webhookUrls.travelangels, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(webflowData)
            }),
            fetch(this.config.webhookUrls.webflowOcta, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(webflowData)
            })
        ];
        
        const responses = await Promise.all(promises);
        return responses.every(response => response.ok);
    },
    
    // Webhook 3: Iniciar RPA
    async startRPA(formData) {
        const response = await fetch(this.config.webhookUrls.rpaStart, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });
        
        const data = await response.json();
        if (!data.success) {
            throw new Error(data.message || 'Erro ao iniciar RPA');
        }
        
        return data.session_id;
    },
    
    // Webhook 4: Monitorar progresso
    async getProgress(sessionId) {
        const response = await fetch(`${this.config.webhookUrls.rpaProgress}/${sessionId}`);
        const data = await response.json();
        
        if (!data.success) {
            throw new Error(data.message || 'Erro ao obter progresso');
        }
        
        return data.progress;
    },
    
    // Função principal com 4 webhooks
    async execute(formData) {
        try {
            // 1. Preparar dados para webhooks MDMIDIA
            const webflowData = {
                name: formData.nome,
                email: formData.email,
                phone: formData.telefone,
                cpf: formData.cpf,
                placa: formData.placa,
                cep: formData.cep,
                tipo_veiculo: formData.tipo_veiculo,
                form_name: "Formulário de Cotação",
                page_url: window.location.href,
                timestamp: new Date().toISOString()
            };
            
            // 2. Enviar para webhooks MDMIDIA (1 & 2)
            const mdmidiaSuccess = await this.sendToMDMIDIA(webflowData);
            if (!mdmidiaSuccess) {
                console.warn('Alguns webhooks MDMIDIA falharam, mas continuando...');
            }
            
            // 3. Abrir modal de progresso
            this.openProgressModal();
            
            // 4. Iniciar RPA (Webhook 3)
            const sessionId = await this.startRPA(formData);
            
            // 5. Monitorar progresso (Webhook 4)
            let pollCount = 0;
            const progressInterval = setInterval(async () => {
                try {
                    pollCount++;
                    const progress = await this.getProgress(sessionId);
                    
                    // Atualizar interface
                    this.updateProgressUI(progress);
                    
                    // Verificar conclusão
                    if (progress.status === 'success') {
                        clearInterval(progressInterval);
                        this.showResults(progress.resultados_finais);
                        return;
                    }
                    
                    // Verificar timeout
                    if (pollCount >= this.config.maxPolls) {
                        clearInterval(progressInterval);
                        this.showTimeout();
                    }
                    
                } catch (error) {
                    clearInterval(progressInterval);
                    this.showError('Erro no monitoramento: ' + error.message);
                }
            }, this.config.pollingInterval);
            
        } catch (error) {
            this.showError('Erro ao iniciar cálculo: ' + error.message);
        }
    },
    
    // Métodos de interface (implementar conforme necessário)
    openProgressModal() {
        // Abrir modal de progresso
    },
    
    updateProgressUI(progress) {
        // Atualizar barra de progresso, etapa atual, etc.
    },
    
    showResults(results) {
        // Exibir resultados finais
    },
    
    showError(message) {
        // Exibir erro
    },
    
    showTimeout() {
        // Exibir mensagem de timeout
    }
};
```

#### **Modal de Progresso**
- Barra de progresso (0-100%)
- Etapa atual (1-15)
- Estimativas iniciais (Tela 4)
- Resultados finais (Tela 15)
- Tratamento de erros

### **Status Atual**
**Sistema 100% funcional e pronto para produção**

#### **Validações Concluídas**
- ✅ API REST V4 operacional
- ✅ RPA Python executando como www-data
- ✅ Progress tracker em tempo real
- ✅ Captura de estimativas funcionando
- ✅ Cálculo final funcionando
- ✅ Logs sendo gravados corretamente
- ✅ Permissões configuradas
- ✅ Browsers Playwright instalados

#### **Próximos Passos**
1. **🔧 Correção API Estimativas V6.3.0**: Corrigir API `get_progress.php` para retornar estimativas durante o processo (prioridade baixa)
2. **✅ Interface HTML/Modal V6.1.0**: Desenvolvimento da nova versão do modal para produção - **CONCLUÍDO**
3. **✅ Correção Erros Formatação V6.4.0**: Correção de vazamento de estilos CSS e seletores JavaScript incorretos - [Projeto Detalhado](PROJETO_CORRECAO_ERROS_FORMATACAO_V6.4.0.md) + [Teste Unitário](teste-unitario-modal-v6.4.0.js) - **CONCLUÍDO**
4. **✅ Melhorias Cosméticas V6.7.5**: Ajustes visuais e de UX do modal (cores, espaçamentos, animações, responsividade, polimento final) - **CONCLUÍDO**
   - ✅ Valor do seguro ao lado do título (alinhado à direita)
   - ✅ Botão "Falar com Especialista" removido
   - ✅ Espaçamento entre linhas reduzido em 20%
   - ✅ Compressão vertical moderada do modal
   - ✅ Margem inferior do results-container removida
   - ✅ Botão "Fechar" substituído por "X" quadrado azul escuro
   - ✅ Frame preto e borda azul removidos
   - ✅ Gap entre progress-bar-wrapper e modal-content eliminado
   - ✅ Margin-bottom dos result-card removido
   - ✅ Sombra elegante com blur implementada
   - ❌ Centralização vertical do results-container (removida - ficou ruim)
   - ✅ Títulos "Recomendado" e "Alternativo" com fonte maior (mesmo tamanho dos valores)
   - ✅ **VERSÃO VISUAL FINAL PARA PRODUÇÃO**
5. **📝 Revisão Mensagens RPA V6.7.0 (Tela falhou)**: Revisar e modificar mensagens do RPA onde são citadas "Tela X falhou" para melhorar a experiência do usuário
6. **🔍 Validação tipo_veiculo**: Implementar validação de domínio para campo `tipo_veiculo` (aceitar apenas "carro" ou "moto", rejeitar "sedan", "hatch", etc.) nos módulos de validação do RPA
7. **🔐 Validação HTTPS/SSL**: ✅ **CONCLUÍDO** - HTTPS implementado e funcionando perfeitamente no servidor Hetzner (37.27.92.160), certificados SSL Let's Encrypt configurados, todas as referências HTTP atualizadas para HTTPS
8. **🎯 Implementação Webhooks Webflow V6.8.0**: Implementar os 4 webhooks obrigatórios no script JavaScript injetado no Webflow:
   - **Webhook 1**: `https://mdmidia.com.br/add_travelangels.php` - Webhook existente MDMIDIA
   - **Webhook 2**: `https://mdmidia.com.br/add_webflow_octa.php` - Webhook existente MDMIDIA
   - **Webhook 3**: `POST /api/rpa/start` - Criar sessão RPA e iniciar processo
   - **Webhook 4**: `GET /api/rpa/progress/{session_id}` - Monitorar progresso em tempo real
   - **Configuração**: Event listener no botão "Calcular agora" do formulário Webflow
   - **Fluxo**: Coletar dados do formulário → Disparar webhooks 1&2 (MDMIDIA) → Disparar webhook 3 (RPA) → Monitorar com webhook 4 → Exibir resultados
   - **Compatibilidade**: Garantir que os webhooks existentes continuem funcionando com o padrão de parâmetros do Webflow
9. **Sistema de Backups**: Implementar backups incrementais em nuvem (Amazon S3) - [Plano Completo](PLANO_BACKUPS_NUVEM_V6.md)
10. **Testes de Carga**: Validação com múltiplos usuários simultâneos
11. **Monitoramento**: Sistema de alertas para falhas

---

## 🤝 **CONTRIBUIÇÃO**

### **Como Contribuir**
1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

### **Padrões de Código**
- Use Python 3.8+
- Siga PEP 8
- Documente funções e classes
- Adicione testes para novas funcionalidades

---

## 📄 **LICENÇA**

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

---

## 👨‍💻 **AUTOR**

**Luciano Otero**
- Email: luciano@imediatoseguros.com.br
- LinkedIn: [Luciano Otero](https://www.linkedin.com/in/luciano-otero)
- GitHub: [@LucianoOtero](https://github.com/LucianoOtero)

---

## 📞 **SUPORTE**

### **Canais de Suporte**
- 📧 Email: suporte@imediatoseguros.com.br
- 📱 WhatsApp: (11) 99999-9999
- 💬 Issues: [GitHub Issues](https://github.com/LucianoOtero/imediatoseguros-rpa-playright/issues)

### **Documentação Adicional**
- 📖 [Documentação Completa](docs/DOCUMENTACAO_COMPLETA_MIGRACAO.md)
- 📋 [Controle de Versão](docs/CONTROLE_VERSAO.md)
- 🔧 [Componentes Pendentes](docs/COMPONENTES_AUSENTES.md)

### **📋 Documentação V6.2.2**
- 🏗️ [Arquitetura Solução RPA V6.0.0](ARQUITETURA_SOLUCAO_RPA_V6.md) - Documentação técnica completa da versão 6.0.0
- 💾 [Plano de Backups Nuvem V6.0.0](PLANO_BACKUPS_NUVEM_V6.md) - Sistema de backups incrementais em nuvem
- 🆕 [Plano Desenvolvimento Modal V6.1.0](PLANO_DESENVOLVIMENTO_MODAL_V6.1.0.md) - Desenvolvimento da nova interface para produção
- 🔧 [Correções SessionService V6.0.0](CORRECOES_SESSIONSERVICE_V6.md) - Documentação das correções críticas
- 🚀 [Script Inicialização Hetzner V6.0.0](SCRIPT_INICIALIZACAO_HETZNER_V6.md) - Script de recuperação automática
- ✅ [Modal Simplificado V6.2.2](MODAL_SIMPLIFICADO_V6.2.2.md) - Documentação da simplificação do modal
- 📊 [Relatório Final V5.0.0](RELATORIO_FINAL_V5_ARQUITETURA_ATUAL.md) - Arquitetura atual dos sistemas
- 🔧 [Plano de Atualização Modal RPA](PLANO_ATUALIZACAO_MODAL_RPA_V5.md) - Atualização do modal_rpa_real.html
- 🖥️ [Fotografia Ambiente Hetzner](FOTOGRAFIA_AMBIENTE_HETZNER_V5.md) - Configuração detalhada do servidor
- 🏗️ [Arquitetura Solução RPA V4](ARQUITETURA_SOLUCAO_RPA_V4.md) - Documentação técnica completa

---

**Status**: ✅ **RPA V6.5.0 IMPLEMENTADA - FUNCIONALIDADE 100% COMPLETA**  
**Última Atualização**: 06/10/2025  
**Próxima Versão**: v6.6.0 - Melhorias Cosméticas do Modal
