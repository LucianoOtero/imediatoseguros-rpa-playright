# 🏗️ ARQUITETURA DA API HETZNER - ANÁLISE COMPLETA

## 📋 **RESUMO EXECUTIVO**

A API do Hetzner funciona como uma ponte entre o frontend (Webflow) e o RPA Python, gerenciando sessões e monitoramento em tempo real através de múltiplas camadas de processamento.

---

## 🎯 **COMPONENTES PRINCIPAIS**

### **1. FRONTEND (Webflow)**
- **Localização**: segurosimediato.com.br
- **Tecnologia**: JavaScript injetado
- **Responsabilidades**:
  - Coleta dados do formulário
  - Chama API do Hetzner
  - Monitora progresso em tempo real
  - Exibe resultados finais

### **2. API PHP (Hetzner)**
- **Servidor**: 37.27.92.160 (Ubuntu)
- **Arquivos principais**:
  - `start.php` - Endpoint de início
  - `get_progress.php` - Monitoramento
  - `RPAController_novo.php` - Controlador principal
- **Responsabilidades**:
  - Validação de dados
  - Consulta API PH3A
  - Execução de webhooks
  - Inicialização do RPA
  - Monitoramento de progresso

### **3. RPA Python**
- **Arquivo**: `/opt/imediatoseguros-rpa/executar_rpa_imediato_playwright.py`
- **Tecnologia**: Playwright + Chromium
- **Responsabilidades**:
  - Execução das 15 telas
  - Progress tracking
  - Captura de dados
  - Tratamento de erros

---

## 🔄 **FLUXO DE EXECUÇÃO DETALHADO**

### **FASE 1: INICIALIZAÇÃO**
```
1. Usuário preenche formulário no Webflow
2. JavaScript coleta dados
3. POST para /api/rpa/start
4. Validação de campos obrigatórios
5. Geração de session_id único
```

### **FASE 2: PROCESSAMENTO PH3A**
```
6. Verificação de campos vazios (sexo, data_nascimento, estado_civil)
7. Se vazios → Consulta API PH3A com CPF
8. Preenchimento automático dos campos
9. Log de resultados PH3A
```

### **FASE 3: WEBHOOKS**
```
10. Disparo de webhooks para MDMIDIA
11. Log de resultados dos webhooks
12. Continuação independente do resultado
```

### **FASE 4: EXECUÇÃO RPA**
```
13. Criação de arquivo JSON temporário
14. Execução do RPA Python em background
15. Inicialização do progress tracker
16. Retorno de session_id para frontend
```

### **FASE 5: MONITORAMENTO**
```
17. Frontend inicia polling (2 segundos)
18. GET para /get_progress.php?session={id}
19. Leitura de arquivo progress_{session_id}.json
20. Atualização do modal de progresso
21. Repetição até conclusão ou erro
```

---

## 📊 **ESTRUTURA DE DADOS**

### **Request (Frontend → API)**
```json
{
  "cpf": "12345678901",
  "nome": "João Silva",
  "email": "joao@email.com",
  "telefone": "11999999999",
  "placa": "ABC1234",
  "cep": "01234567",
  "sexo": "Masculino",
  "data_nascimento": "01/01/1990",
  "estado_civil": "Solteiro"
}
```

### **Response (API → Frontend)**
```json
{
  "success": true,
  "session_id": "rpa_v6.9.0_20250101_120000_abc12345",
  "message": "RPA iniciado com sucesso",
  "timestamp": "2025-01-01 12:00:00"
}
```

### **Progress Data (RPA → Frontend)**
```json
{
  "success": true,
  "data": {
    "etapa_atual": 7,
    "total_etapas": 15,
    "percentual": 46.7,
    "status": "running",
    "mensagem": "Processando dados do veículo",
    "estimativas": {...},
    "dados_extra": {...}
  }
}
```

---

## 🗂️ **ESTRUTURA DE ARQUIVOS NO HETZNER**

```
/opt/imediatoseguros-rpa/
├── executar_rpa_imediato_playwright.py    # RPA principal
├── parametros.json                         # Configuração base
├── venv/                                   # Ambiente Python
├── logs/                                   # Logs de execução
├── rpa_data/                               # Progress tracker
│   ├── progress_{session_id}.json
│   └── history_{session_id}.json
└── sessions/                               # Sessões ativas
    └── {session_id}/
        └── status.json

/var/www/rpaimediatoseguros.com.br/
├── api/                                    # Backend PHP
│   ├── start.php                          # Endpoint de início
│   ├── get_progress.php                   # Monitoramento
│   └── RPAController_novo.php            # Controlador
└── logs/                                   # Logs do sistema
    ├── access.log
    └── error.log
```

---

## ⚡ **ENDPOINTS DA API**

### **1. Iniciar RPA**
```
POST /api/rpa/start
Content-Type: application/json

Body: { dados do formulário }
Response: { session_id, success, message }
```

### **2. Monitorar Progresso**
```
GET /get_progress.php?session={session_id}

Response: { progress data, status, estimativas }
```

### **3. Health Check**
```
GET /api/rpa/health

Response: { status: "healthy", timestamp }
```

---

## 🔧 **TECNOLOGIAS UTILIZADAS**

### **Backend**
- **PHP 8.3** - API REST
- **Nginx** - Web server
- **PHP-FPM** - Process manager
- **cURL** - Comunicação HTTP

### **RPA**
- **Python 3.11** - Linguagem principal
- **Playwright** - Automação de browser
- **Chromium** - Browser headless
- **JSON** - Progress tracking

### **Frontend**
- **JavaScript ES6+** - Lógica cliente
- **Fetch API** - Comunicação HTTP
- **SweetAlert2** - Modais
- **CSS3** - Estilização

---

## 🚨 **PONTOS CRÍTICOS IDENTIFICADOS**

### **1. VERSÃO DO RPA**
- **Problema**: Arquivo no Hetzner pode estar desatualizado
- **Impacto**: Correções não aplicadas
- **Solução**: Upload do arquivo corrigido

### **2. TIMEOUTS**
- **Problema**: Timeout de 3 minutos para tela de sucesso
- **Impacto**: Demora na detecção de cotação manual
- **Solução**: Reduzido para 10 segundos

### **3. LÓGICA DE ERRO**
- **Problema**: "COTAÇÃO MANUAL PROCESSADA COM SUCESSO!"
- **Impacto**: Mensagem incorreta para usuário
- **Solução**: Retorno de erro 9003

### **4. PROGRESS TRACKER**
- **Problema**: Métodos não existentes
- **Impacto**: Falhas na atualização
- **Solução**: Correção dos métodos

---

## 📈 **PERFORMANCE E MONITORAMENTO**

### **Tempos de Resposta**
- **API Start**: ~2-5 segundos
- **PH3A Query**: ~1-3 segundos
- **Webhooks**: ~0.5-2 segundos
- **RPA Init**: ~1-2 segundos
- **Progress Poll**: ~0.1-0.5 segundos

### **Logs Disponíveis**
- **Nginx Access**: `/var/log/nginx/access.log`
- **Nginx Error**: `/var/log/nginx/error.log`
- **PHP Error**: `/var/log/php/error.log`
- **RPA Logs**: `/opt/imediatoseguros-rpa/logs/`

---

## 🎯 **PRÓXIMOS PASSOS**

1. ✅ **Verificar versão atual** do RPA no Hetzner
2. ✅ **Comparar com versão local** corrigida
3. ✅ **Fazer backup** do arquivo atual
4. ✅ **Upload do arquivo corrigido**
5. ✅ **Testar funcionamento** completo

**Status**: Pronto para upload das correções! 🚀
