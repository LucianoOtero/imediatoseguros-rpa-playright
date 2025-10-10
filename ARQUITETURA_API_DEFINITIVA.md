# 🏗️ ARQUITETURA DEFINITIVA DA API - IMEDIATO SEGUROS RPA

## 📋 **RESUMO EXECUTIVO**

A API do Hetzner funciona como uma ponte inteligente entre o frontend Webflow e o RPA Python, gerenciando sessões e monitoramento em tempo real através de múltiplas camadas de processamento.

---

## 🎯 **COMPONENTES PRINCIPAIS**

### **1. FRONTEND (Webflow)**
- **Localização**: segurosimediato.com.br
- **Tecnologia**: JavaScript injetado dinamicamente
- **Responsabilidades**:
  - Coleta dados do formulário de cotação
  - Chama API do Hetzner via endpoints REST
  - Monitora progresso em tempo real (polling a cada 2 segundos)
  - Exibe resultados finais e alertas de erro

### **2. API PHP (Hetzner - 37.27.92.160)**
- **Servidor**: Ubuntu (37.27.92.160)
- **Arquivos principais**:
  - `rpa-v4/src/Controllers/RPAController.php` - Controlador principal
  - `rpa-v4/src/Services/SessionService.php` - Gerenciamento de sessões
  - `rpa-v4/src/Services/MonitorService.php` - Monitoramento de progresso
  - `rpa-v4/public/index.php` - Roteamento principal
- **Responsabilidades**:
  - Validação de dados de entrada
  - Consulta API PH3A para dados complementares
  - Execução de webhooks (EspoCRM, Octadesk)
  - Inicialização do RPA Python
  - Monitoramento de progresso em tempo real

### **3. RPA PYTHON**
- **Localização**: `/opt/imediatoseguros-rpa/executar_rpa_imediato_playwright.py`
- **Tecnologia**: Playwright + Python
- **Responsabilidades**:
  - Execução de 15 telas sequenciais de cotação
  - Captura de dados do site da seguradora
  - Tratamento de erros e exceções
  - Comunicação com progress tracker
  - Retorno de resultados estruturados

---

## 🔄 **FLUXO DE EXECUÇÃO COMPLETO**

### **FASE 1: INICIALIZAÇÃO**
```
Frontend → RPAController.php → SessionService.php → RPA Python
```

**1. Frontend (JavaScript):**
```javascript
// webflow-injection-complete.js linha 2135
const response = await fetch('https://rpaimediatoseguros.com.br/api/rpa/start', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(formData)
});
```

**2. RPAController.php:**
```php
// rpa-v4/src/Controllers/RPAController.php
public function startRPA(array $data): array
{
    // Rate limiting
    // Validação de entrada
    // Criação de sessão via SessionService
    return $this->sessionService->create($data);
}
```

**3. SessionService.php:**
```php
// rpa-v4/src/Services/SessionService.php linha 339-340
cd /opt/imediatoseguros-rpa
$command = "/opt/imediatoseguros-rpa/venv/bin/python executar_rpa_imediato_playwright.py --config {$tempJsonFile} --session \$SESSION_ID --progress-tracker json";
```

### **FASE 2: EXECUÇÃO RPA**
```
RPA Python → 15 Telas → Progress Tracker → MonitorService.php
```

**1. RPA Python:**
- Executa `executar_rpa_imediato_playwright.py`
- Processa 15 telas sequenciais
- Atualiza progress tracker em tempo real
- Captura dados e trata erros

**2. Progress Tracker:**
- Arquivo JSON: `/opt/imediatoseguros-rpa/sessions/$SESSION_ID/progress.json`
- Atualizações em tempo real durante execução
- Status: `starting`, `started`, `completed`, `error`, `timeout`

### **FASE 3: MONITORAMENTO**
```
Frontend → MonitorService.php → Progress JSON → Resposta
```

**1. Frontend (Polling):**
```javascript
// modal_rpa_real.js linha 483
const response = await this.fetchWithRetry(`${this.apiBaseUrl}/api/rpa/progress/${this.sessionId}`, {
    method: 'GET',
    headers: { 'Accept': 'application/json' }
});
```

**2. MonitorService.php:**
```php
// rpa-v4/src/Services/MonitorService.php
public function getProgress(string $sessionId): array
{
    // Lê progress.json
    // Retorna status atual
    // Trata erros e timeouts
}
```

---

## 📁 **ESTRUTURA COMPLETA DE DIRETÓRIOS HETZNER**

### **1. RPA PYTHON (ATIVO):**
```
/opt/imediatoseguros-rpa/
├── executar_rpa_imediato_playwright.py    # RPA principal ✅ ATIVO
├── executar_rpa_modular_telas_1_a_5.py    # ❌ DESCONTINUADO (backup antigo)
├── tosegurado_complete.py                 # ❌ DESCONTINUADO (Selenium antigo)
├── tasks.py                               # Tarefas Celery
├── app.py                                 # Aplicação Flask
├── parametros.json                        # Configuração padrão ✅ ATIVO
├── venv/                                  # Virtual environment ✅ ATIVO
│   └── bin/python                        # Python executável
├── sessions/                             # Sessões ativas ✅ ATIVO
│   └── $SESSION_ID/
│       ├── progress.json                 # Progresso em tempo real
│       ├── status.json                   # Status final
│       └── data.json                     # Dados da sessão
├── rpa_data/                             # Progress tracker ✅ ATIVO
│   ├── progress_rpa_v4_*.json           # ✅ GERANDO ARQUIVOS
│   ├── history_rpa_v4_*.json            # ✅ GERANDO ARQUIVOS
│   ├── result_rpa_v4_*.json             # ✅ GERANDO ARQUIVOS
│   └── session_rpa_v4_*.json            # ✅ GERANDO ARQUIVOS
├── logs/                                 # Logs de execução ✅ ATIVO
│   ├── rpa_v4_$SESSION_ID.log           # Log específico da sessão
│   └── scripts/                          # Scripts bash gerados
└── utils/                                # Utilitários ✅ ATIVO
    ├── progress_realtime.py
    ├── progress_database_json.py
    └── bidirectional_integration_wrapper.py
```

### **2. API PHP V4 (ATIVA):**
```
/opt/imediatoseguros-rpa-v4/
├── src/
│   ├── Controllers/
│   │   └── RPAController.php            # Controlador principal ✅ ATIVO
│   ├── Services/
│   │   ├── SessionService.php           # Gerenciamento de sessões ✅ ATIVO
│   │   ├── MonitorService.php           # Monitoramento ✅ ATIVO
│   │   ├── ConfigService.php            # Configurações ✅ ATIVO
│   │   ├── ValidationService.php        # Validações ✅ ATIVO
│   │   └── RateLimitService.php         # Rate limiting ✅ ATIVO
│   └── Interfaces/                      # Interfaces ✅ ATIVO
│       ├── SessionServiceInterface.php
│       ├── MonitorServiceInterface.php
│       └── LoggerInterface.php
├── public/
│   ├── index.php                        # Entry point ✅ FUNCIONANDO
│   └── diagnostic.php                   # Health check
├── config/
│   └── app.php                          # Configurações
└── vendor/                              # Dependências Composer
```

### **3. API PHP V3 (DESCONTINUADA):**
```
/var/www/rpaimediatoseguros.com.br/       # API ANTIGA (V3) ❌ DESCONTINUADA
├── executar_rpa_v3.php                  # ❌ ÚLTIMA EXECUÇÃO: 29/09/2025
├── executar_rpa_v2.php                  # ❌ DESCONTINUADA
├── executar_rpa.php                     # ❌ DESCONTINUADA
├── get_progress.php                     # ❌ DESCONTINUADA
├── websocket/                           # WebSocket (se existir)
│   ├── websocket_server.js
│   └── package.json
├── api/                                 # Endpoints antigos
├── logs/                                # Logs antigos
└── index.html                           # Frontend antigo
```

### **4. ARQUIVOS PHP INVÁLIDOS (NÃO UTILIZAR):**
```
❌ ARQUIVOS DESCONTINUADOS E INVÁLIDOS:

/var/www/rpaimediatoseguros.com.br/
├── start.php                            # ❌ NÃO EXECUTADO pelo Nginx
├── RPAController_novo.php              # ❌ VERSÃO ANTIGA do controlador
├── executar_rpa_v3.php                 # ❌ API V3 descontinuada
├── executar_rpa_v2.php                 # ❌ API V2 descontinuada
├── executar_rpa.php                    # ❌ API V1 descontinuada
├── get_progress.php                     # ❌ Monitoramento antigo
├── monitor_tempo_real.php               # ❌ Monitor antigo
├── dashboard_basic.html                 # ❌ Dashboard antigo
├── status.php                          # ❌ Status antigo
├── monitor_basic.sh                     # ❌ Script antigo
└── teste_*.php                          # ❌ Arquivos de teste

/opt/imediatoseguros-rpa-v4/public/api/rpa/
├── start.php                            # ❌ DUPLICADO - não executado
└── [outros arquivos antigos]            # ❌ VERSÕES ANTIGAS

ARQUIVOS LOCAIS (APENAS DESENVOLVIMENTO):
├── teste-endpoint.php                  # ❌ APENAS TESTE LOCAL
├── teste_implementacao_completa.php     # ❌ APENAS TESTE LOCAL
├── teste_rpa_*.php                     # ❌ APENAS TESTE LOCAL
├── test_rpa_v*.php                     # ❌ APENAS TESTE LOCAL
└── teste_*.php                         # ❌ APENAS TESTE LOCAL
```

### **5. CONFIGURAÇÕES DO SERVIDOR:**
```
/etc/nginx/sites-available/
└── rpaimediatoseguros.com.br.conf       # Configuração Nginx ✅ ATIVO

/var/log/
├── nginx/
│   ├── access.log                       # Logs de acesso
│   └── error.log                        # Logs de erro
└── php/
    └── error.log                        # Logs PHP

/var/www/.cache/                         # Cache Playwright
└── ms-playwright/                       # Browsers Playwright
    ├── chromium-1187/
    └── chromium_headless_shell-1187/
```

### **6. SISTEMA E SERVIÇOS:**
```
/etc/systemd/system/
├── rpa-websocket.service                # Serviço WebSocket (se ativo)
└── nginx.service                        # Serviço Nginx ✅ ATIVO

/root/.cache/                            # Cache root
└── ms-playwright/                       # Browsers Playwright (root)
```

---

## ⚠️ **ARQUIVOS PHP - VÁLIDOS vs INVÁLIDOS**

### **✅ ARQUIVOS PHP VÁLIDOS (UTILIZAR):**
```
/opt/imediatoseguros-rpa-v4/src/Controllers/
└── RPAController.php                     # ✅ ÚNICO CONTROLADOR VÁLIDO

/opt/imediatoseguros-rpa-v4/src/Services/
├── SessionService.php                    # ✅ GERENCIAMENTO DE SESSÕES
├── MonitorService.php                    # ✅ MONITORAMENTO
├── ConfigService.php                     # ✅ CONFIGURAÇÕES
├── ValidationService.php                 # ✅ VALIDAÇÕES
└── RateLimitService.php                  # ✅ RATE LIMITING

/opt/imediatoseguros-rpa-v4/public/
└── index.php                             # ✅ ENTRY POINT PRINCIPAL
```

### **❌ ARQUIVOS PHP INVÁLIDOS (NÃO UTILIZAR):**
```
❌ CONTROLADORES ANTIGOS:
├── RPAController_novo.php               # ❌ VERSÃO ANTIGA
├── start.php                            # ❌ NÃO EXECUTADO pelo Nginx
└── executar_rpa*.php                    # ❌ TODAS AS VERSÕES ANTIGAS

❌ MONITORAMENTO ANTIGO:
├── get_progress.php                     # ❌ DESCONTINUADO
├── monitor_tempo_real.php               # ❌ DESCONTINUADO
└── status.php                           # ❌ DESCONTINUADO

❌ ARQUIVOS DE TESTE:
├── teste-endpoint.php                   # ❌ APENAS DESENVOLVIMENTO
├── teste_implementacao_completa.php     # ❌ APENAS DESENVOLVIMENTO
├── teste_rpa_*.php                      # ❌ APENAS DESENVOLVIMENTO
├── test_rpa_v*.php                      # ❌ APENAS DESENVOLVIMENTO
└── teste_*.php                          # ❌ APENAS DESENVOLVIMENTO
```

### **🎯 REGRA FUNDAMENTAL:**
**APENAS os arquivos em `/opt/imediatoseguros-rpa-v4/` são válidos e funcionais.**
**TODOS os arquivos em `/var/www/rpaimediatoseguros.com.br/` são descontinuados.**

---

## 🐍 **ARQUIVOS PYTHON - VÁLIDOS vs DESCONTINUADOS**

### **✅ ARQUIVOS PYTHON VÁLIDOS (UTILIZAR):**
```
/opt/imediatoseguros-rpa/
├── executar_rpa_imediato_playwright.py    # ✅ RPA PRINCIPAL ATIVO
├── tasks.py                               # ✅ CELERY TASKS
├── app.py                                 # ✅ FLASK APP
└── utils/
    ├── progress_realtime.py              # ✅ PROGRESS TRACKER
    ├── progress_database_json.py         # ✅ PROGRESS DATABASE
    └── bidirectional_integration_wrapper.py # ✅ INTEGRATION WRAPPER
```

### **❌ ARQUIVOS PYTHON DESCONTINUADOS (NÃO UTILIZAR):**
```
/opt/imediatoseguros-rpa/
├── executar_rpa_modular_telas_1_a_5.py    # ❌ DESCONTINUADO (backup antigo)
└── tosegurado_complete.py                 # ❌ DESCONTINUADO (Selenium antigo)
```

### **🎯 REGRA FUNDAMENTAL PYTHON:**
**APENAS `executar_rpa_imediato_playwright.py` é o RPA principal ativo.**
**TODOS os outros arquivos Python são utilitários ou descontinuados.**

---

### **1. INICIAR RPA:**
- **URL**: `https://rpaimediatoseguros.com.br/api/rpa/start`
- **Método**: `POST`
- **Payload**: Dados do formulário de cotação
- **Resposta**: `{ "success": true, "session_id": "uuid" }`

### **2. MONITORAR PROGRESSO:**
- **URL**: `https://rpaimediatoseguros.com.br/api/rpa/progress/{session_id}`
- **Método**: `GET`
- **Resposta**: Status atual do RPA
- **Frequência**: Polling a cada 2 segundos

### **3. VERIFICAR STATUS:**
- **URL**: `https://rpaimediatoseguros.com.br/api/rpa/status/{session_id}`
- **Método**: `GET`
- **Resposta**: Status final da sessão

---

## 🔧 **CONFIGURAÇÕES TÉCNICAS**

### **NGINX (Servidor Web):**
```nginx
# nginx_rpaimediatoseguros.conf
location /api/ {
    root /opt/imediatoseguros-rpa-v4/public;
    try_files $uri $uri/ /index.php?$query_string;
}
```

### **COMANDO DE EXECUÇÃO:**
```bash
cd /opt/imediatoseguros-rpa
/opt/imediatoseguros-rpa/venv/bin/python executar_rpa_imediato_playwright.py \
    --config /tmp/rpa_data_$SESSION_ID.json \
    --session $SESSION_ID \
    --progress-tracker json
```

### **VARIÁVEIS DE AMBIENTE:**
- **Working Directory**: `/opt/imediatoseguros-rpa`
- **Python Path**: `/opt/imediatoseguros-rpa/venv/bin/python`
- **Session ID**: UUID único por execução
- **Progress Tracker**: JSON em tempo real

---

## 🚨 **TRATAMENTO DE ERROS**

### **CÓDIGOS DE ERRO:**
- **9001**: Erro geral do sistema
- **9002**: Timeout de execução
- **9003**: Cotação manual necessária
- **9004**: Tela final não detectada
- **9005**: Erro de validação de dados

### **FLUXO DE ERRO:**
```
RPA Python → Progress Tracker → MonitorService → Frontend → SweetAlert2
```

### **ARQUIVOS DE LOG:**
- **Log principal**: `/opt/imediatoseguros-rpa/logs/rpa_v4_$SESSION_ID.log`
- **Log da API**: `/var/log/nginx/access.log`
- **Log do PHP**: `/var/log/php/error.log`

---

## 📊 **MONITORAMENTO E LOGS**

### **PROGRESS TRACKER (JSON):**
```json
{
    "status": "started",
    "etapa_atual": "Tela 5 - Dados do Veículo",
    "percentual": 33,
    "mensagem": "Processando dados do veículo...",
    "timestamp": "2025-01-15T10:30:00Z"
}
```

### **STATUS FINAL:**
```json
{
    "status": "completed",
    "completed_at": "2025-01-15T10:35:00Z",
    "resultado": {
        "sucesso": true,
        "dados_capturados": {...}
    }
}
```

---

## 🔄 **INTEGRAÇÕES EXTERNAS**

### **1. API PH3A:**
- **Propósito**: Consulta dados complementares
- **Integração**: Via SessionService.php
- **Dados**: Informações adicionais do cliente

### **2. EspoCRM:**
- **Propósito**: Cadastro de leads
- **Integração**: Webhook após cotação
- **Dados**: Dados do formulário + resultado

### **3. Octadesk:**
- **Propósito**: Notificação de atendimento
- **Integração**: Webhook após cotação
- **Dados**: Status da cotação + dados do cliente

---

## ⚡ **PERFORMANCE E OTIMIZAÇÕES**

### **TIMEOUTS:**
- **Tela de sucesso**: 10 segundos (otimizado de 3 minutos)
- **Tela de cotação manual**: 10 segundos
- **Polling frontend**: 2 segundos
- **Timeout geral**: 15 minutos

### **RATE LIMITING:**
- **Implementado**: Via RateLimitService.php
- **Limite**: Por IP de origem
- **Janela**: 1 minuto

### **CLEANUP:**
- **Arquivos temporários**: Removidos automaticamente
- **Sessões antigas**: Limpeza periódica
- **Logs**: Rotação automática

---

## 🛠️ **MANUTENÇÃO E DEPLOY**

### **ARQUIVOS PRINCIPAIS PARA ATUALIZAÇÃO:**
1. **`executar_rpa_imediato_playwright.py`** - Lógica do RPA
2. **`RPAController.php`** - Controlador da API
3. **`SessionService.php`** - Gerenciamento de sessões
4. **`webflow-injection-complete.js`** - Frontend JavaScript

### **PROCESSO DE DEPLOY:**
1. **Backup**: Arquivos atuais
2. **Upload**: Novos arquivos via SSH
3. **Teste**: Validação de funcionamento
4. **Monitoramento**: Logs e performance

### **LOCALIZAÇÕES CRÍTICAS:**
- **RPA Python**: `/opt/imediatoseguros-rpa/executar_rpa_imediato_playwright.py`
- **API PHP**: `/opt/imediatoseguros-rpa-v4/src/Controllers/RPAController.php`
- **JavaScript**: Injetado dinamicamente no frontend

---

## 📝 **NOTAS IMPORTANTES**

### **VERSÕES ATUAIS:**
- **API PHP**: V4.0.1 (atualizada com PH3A e webhooks)
- **RPA Python**: Versão local corrigida (timeout 10s, lógica de erro)
- **Frontend**: JavaScript com tratamento de erro 9003

### **PROBLEMAS CONHECIDOS:**
- **Timeout excessivo**: Corrigido de 3min para 10s
- **Lógica de cotação manual**: Corrigida para retornar erro
- **Progress tracker**: Escopo corrigido

### **PRÓXIMOS PASSOS:**
1. **Upload**: `executar_rpa_imediato_playwright.py` corrigido para Hetzner
2. **Teste**: Validação completa da correção
3. **Monitoramento**: Acompanhamento de logs

---

**📅 Última atualização**: 15 de Janeiro de 2025  
**👨‍💻 Responsável**: Assistente AI  
**📋 Status**: Documento definitivo para consulta
