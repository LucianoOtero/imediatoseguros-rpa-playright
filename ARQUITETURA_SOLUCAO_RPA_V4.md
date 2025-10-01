# ARQUITETURA DA SOLUÇÃO RPA V4

**Data:** 01/10/2025  
**Versão:** 4.0  
**Status:** ✅ PRODUÇÃO - SISTEMA FUNCIONAL  
**Ambiente:** Hetzner Cloud (Ubuntu 22.04)  

---

## 📋 VISÃO GERAL

Sistema RPA V4 para automação de cotação de seguros no portal `app.tosegurado.com.br`, executando em background com monitoramento em tempo real via API REST.

### Objetivo Principal
Executar `executar_rpa_imediato_playwright.py` em sessões concorrentes em background, chamado via JSON de parâmetros via linha de comando a partir de JavaScript no `segurosimediato.com.br` (Webflow), com monitoramento de progresso em tempo real.

---

## 🏗️ ARQUITETURA DO SISTEMA

### Componentes Principais

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

---

## 🔧 COMPONENTES TÉCNICOS

### 1. **API REST V4** (`/api/rpa/`)

#### Endpoint: `POST /api/rpa/start`
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

#### Endpoint: `GET /api/rpa/progress/{session_id}`
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

### 2. **SessionService.php**
**Localização**: `/opt/imediatoseguros-rpa-v4/src/Services/SessionService.php`

**Funções**:
- Validar dados de entrada
- Criar diretório de sessão
- Gerar script bash para execução RPA
- Iniciar processo em background
- Gerenciar arquivos temporários

**Fluxo**:
1. Receber JSON via POST
2. Validar dados obrigatórios
3. Criar `session_id` único
4. Gerar script bash com parâmetros
5. Executar RPA em background
6. Retornar `session_id` para monitoramento

### 3. **get_progress_completo.php**
**Localização**: `/opt/imediatoseguros-rpa-v4/get_progress_completo.php`

**Funções**:
- Ler arquivos de progresso JSON
- Detectar histórico vs. progresso atual
- Retornar status formatado
- Incluir estimativas e resultados finais

**Arquivos Monitorados**:
- `progress_{session_id}.json` - Progresso atual
- `history_{session_id}.json` - Histórico completo

### 4. **RPA Python Principal**
**Localização**: `/opt/imediatoseguros-rpa/executar_rpa_imediato_playwright.py`

**Características**:
- 15 telas de automação
- Playwright + Chromium headless
- Progress tracker em tempo real
- Captura de estimativas (Tela 4)
- Cálculo final (Tela 15)
- Logs detalhados

**Parâmetros de Linha de Comando**:
```bash
python executar_rpa_imediato_playwright.py \
    --config /tmp/rpa_data_{session_id}.json \
    --session {session_id} \
    --progress-tracker json
```

---

## 📁 ESTRUTURA DE DIRETÓRIOS

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

---

## 🔄 FLUXO DE EXECUÇÃO

### 1. **Início da Sessão**
```
Webflow → POST /api/rpa/start → SessionService.php → Script Bash → RPA Python
```

### 2. **Monitoramento**
```
Webflow → GET /api/rpa/progress/{session_id} → get_progress_completo.php → JSON Response
```

### 3. **Progress Tracker**
```
RPA Python → progress_{session_id}.json → get_progress_completo.php → Webflow
```

---

## 📊 DADOS E FORMATOS

### Progress Tracker JSON
```json
{
    "session_id": "rpa_v4_20251001_222340_28563ee9",
    "status": "running",
    "etapa_atual": 4,
    "total_etapas": 15,
    "percentual": 26.67,
    "timestamp": "2025-10-01T22:23:45Z",
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
```

### Status da Sessão
```json
{
    "status": "completed",
    "completed_at": "2025-10-01T22:25:30Z"
}
```

---

## 🚀 CONFIGURAÇÃO DE PRODUÇÃO

### Servidor
- **OS**: Ubuntu 22.04 LTS
- **CPU**: 2 vCPUs
- **RAM**: 4GB
- **Storage**: 40GB SSD
- **IP**: 37.27.92.160

### Serviços
- **Nginx**: 1.18.0 (Proxy reverso)
- **PHP-FPM**: 8.1 (Backend API)
- **Python**: 3.10 (RPA automation)
- **Playwright**: 1.40.0 (Browser automation)

### Permissões
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

---

## 🔒 SEGURANÇA

### CORS
```php
header('Access-Control-Allow-Origin: https://segurosimediato.com.br');
header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type, X-Requested-With');
```

### Validação de Dados
- CPF: Formato e dígitos verificadores
- Placa: Formato brasileiro
- CEP: Formato e existência
- Email: Formato válido
- Telefone: Formato brasileiro

### Logs de Segurança
- Todas as requisições logadas
- Tentativas de acesso não autorizado
- Erros de validação registrados

---

## 📈 MONITORAMENTO

### Métricas de Performance
- Tempo de resposta da API
- Taxa de sucesso das sessões RPA
- Uso de CPU e memória
- Tempo de execução por sessão

### Alertas
- Falha na criação de sessão
- RPA não iniciando
- Progress tracker não atualizando
- Erros de permissão

### Logs
- **Nginx**: `/var/log/nginx/`
- **PHP-FPM**: `/var/log/php8.1-fpm.log`
- **RPA**: `/opt/imediatoseguros-rpa/logs/`
- **Sistema**: `/var/log/syslog`

---

## 🧪 TESTES E VALIDAÇÃO

### Testes Automatizados
- Criação de sessão
- Execução RPA completa
- Captura de estimativas
- Cálculo final
- Progress tracker

### Dados de Teste
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

### Critérios de Sucesso
- ✅ Sessão criada em < 2 segundos
- ✅ RPA executado em < 3 minutos
- ✅ Progress tracker atualizando em tempo real
- ✅ Estimativas capturadas na Tela 4
- ✅ Cálculo final na Tela 15
- ✅ Status "success" ao finalizar

---

## 🔧 MANUTENÇÃO

### Backup
- Código fonte: Git repository
- Configurações: Ansible playbooks
- Logs: Rotação automática
- Dados: Backup diário

### Atualizações
- Código: Deploy via Git
- Dependências: Composer + pip
- Sistema: apt update
- Browsers: playwright install

### Troubleshooting
- Logs detalhados em todos os componentes
- Scripts de diagnóstico
- Monitoramento de recursos
- Alertas automáticos

---

## 📞 INTEGRAÇÃO WEBFLOW

### JavaScript para Chamada da API
```javascript
// Criar sessão RPA
const response = await fetch('https://37.27.92.160/api/rpa/start', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        cpf: '12345678901',
        nome: 'João Silva',
        placa: 'ABC1234',
        cep: '01234567',
        email: 'joao@email.com',
        telefone: '11999999999'
    })
});

const data = await response.json();
const sessionId = data.session_id;

// Monitorar progresso
const progressInterval = setInterval(async () => {
    const progressResponse = await fetch(`https://37.27.92.160/api/rpa/progress/${sessionId}`);
    const progressData = await progressResponse.json();
    
    // Atualizar modal de progresso
    updateProgressModal(progressData.progress);
    
    if (progressData.progress.status === 'success') {
        clearInterval(progressInterval);
        showFinalResults(progressData.progress.resultados_finais);
    }
}, 2000);
```

### Modal de Progresso
- Barra de progresso (0-100%)
- Etapa atual (1-15)
- Estimativas iniciais (Tela 4)
- Resultados finais (Tela 15)
- Tratamento de erros

---

## ✅ STATUS ATUAL

**Sistema 100% funcional e pronto para produção**

### Validações Concluídas
- ✅ API REST V4 operacional
- ✅ RPA Python executando como www-data
- ✅ Progress tracker em tempo real
- ✅ Captura de estimativas funcionando
- ✅ Cálculo final funcionando
- ✅ Logs sendo gravados corretamente
- ✅ Permissões configuradas
- ✅ Browsers Playwright instalados

### Próximos Passos
1. Integração com Webflow
2. Testes de carga
3. Monitoramento em produção
4. Documentação de usuário

---

**Arquitetura documentada e pronta para implementação.**
