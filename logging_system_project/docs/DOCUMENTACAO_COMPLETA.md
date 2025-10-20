# 📚 DOCUMENTAÇÃO COMPLETA - SISTEMA DE LOGGING PHP
## **PROJETO RPA IMEDIATO SEGUROS**

---

## 📋 **ÍNDICE**

1. [Visão Geral](#visão-geral)
2. [Instalação](#instalação)
3. [Configuração](#configuração)
4. [Uso](#uso)
5. [API](#api)
6. [Manutenção](#manutenção)
7. [Troubleshooting](#troubleshooting)
8. [Segurança](#segurança)
9. [Performance](#performance)
10. [Desenvolvimento](#desenvolvimento)

---

## 🎯 **VISÃO GERAL**

### **Objetivo**
Sistema completo de logging para análise profunda do fluxo de execução dos JavaScripts no projeto RPA Imediato Seguros, com foco na investigação do problema "RPA não executa no segurosimediato.com.br".

### **Características Principais**
- ✅ **Logging Estruturado:** Banco de dados MySQL com campos padronizados
- ✅ **Análise Temporal:** Correlação precisa de eventos por sessão
- ✅ **Interface Web:** Visualização e análise em tempo real
- ✅ **Segurança Robusta:** Validação, rate limiting, CORS
- ✅ **Performance Otimizada:** Índices, prepared statements, cleanup automático
- ✅ **Testes Automatizados:** Programa de teste local para Windows

### **Arquitetura**
```
JavaScript (Footer Code/Injection) 
    ↓ POST JSON
debug_logger_db.php 
    ↓ INSERT
MySQL Database 
    ↓ SELECT
log_viewer.php (Interface Web)
```

---

## 🚀 **INSTALAÇÃO**

### **Pré-requisitos**
- **Servidor:** Ubuntu 22.04 LTS (mdmidia.com.br)
- **PHP:** 7.4+ com extensões PDO, JSON, MySQL
- **MySQL:** 8.0+ com suporte a JSON
- **Permissões:** Acesso SSH ao servidor

### **Passo 1: Preparar Servidor**
```bash
# Conectar via SSH
ssh mdmidiac@mdmidia.com.br

# Criar diretório do projeto
mkdir -p /home/mdmidiac/public_html/logging_system
cd /home/mdmidiac/public_html/logging_system
```

### **Passo 2: Upload dos Arquivos**
```bash
# Upload de todos os arquivos PHP via SCP/SFTP
# Estrutura final:
/home/mdmidiac/public_html/logging_system/
├── debug_logger_db.php
├── config/
│   ├── database.php
│   └── security.php
├── utils/
│   ├── helpers.php
│   └── cleanup.php
├── viewer/
│   ├── log_viewer.php
│   └── api/
│       └── analytics.php
└── install/
    └── setup_database.sql
```

### **Passo 3: Configurar Banco de Dados**
```bash
# Executar script de criação do banco
mysql -u root -p < install/setup_database.sql
```

### **Passo 4: Configurar Permissões**
```bash
# Definir permissões adequadas
chmod 755 /home/mdmidiac/public_html/logging_system
chmod 644 /home/mdmidiac/public_html/logging_system/*.php
chmod 755 /home/mdmidiac/public_html/logging_system/utils/cleanup.php
```

### **Passo 5: Testar Instalação**
```bash
# Testar endpoint de logging
curl -X POST https://mdmidia.com.br/logging_system/debug_logger_db.php \
  -H "Content-Type: application/json" \
  -d '{"level":"INFO","message":"Teste de instalação","sessionId":"test_001"}'
```

---

## ⚙️ **CONFIGURAÇÃO**

### **Configuração do Banco de Dados**
Editar `config/database.php`:
```php
$db_config = [
    'host' => 'localhost',
    'port' => 3306,
    'database' => 'rpa_logs',
    'username' => 'rpa_logger',
    'password' => 'sua_senha_segura_aqui',
    'charset' => 'utf8mb4'
];
```

### **Configuração de Segurança**
Editar `config/security.php`:
```php
$security_config = [
    'rate_limit' => [
        'enabled' => true,
        'max_requests_per_minute' => 100,
        'max_requests_per_hour' => 1000
    ],
    'cors' => [
        'allowed_origins' => [
            'https://www.segurosimediato.com.br',
            'https://segurosimediato.com.br'
        ]
    ]
];
```

### **Configuração de Limpeza Automática**
```bash
# Adicionar ao crontab
crontab -e

# Executar limpeza diária às 2h
0 2 * * * /usr/bin/php /home/mdmidiac/public_html/logging_system/utils/cleanup.php
```

---

## 📖 **USO**

### **Integração com Footer Code**
```javascript
// Função para logging persistente
function logDebug(level, message, data = null) {
    const logData = {
        level: level,
        message: message,
        data: data,
        url: window.location.href,
        sessionId: window.sessionId || generateSessionId(),
        timestamp: new Date().toISOString(),
        userAgent: navigator.userAgent
    };

    // Enviar para PHP (não bloquear execução)
    fetch('https://mdmidia.com.br/logging_system/debug_logger_db.php', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(logData)
    }).catch(error => {
        console.warn('Logging failed:', error);
    });

    // Manter console.log para desenvolvimento local
    console.log(`[${level}] ${message}`, data);
}

// Expor função globalmente
window.logDebug = logDebug;
```

### **Integração com Injection Script**
```javascript
// Logs específicos do RPA
logDebug('INFO', 'Webflow Injection Limpo carregado', {
    timestamp: new Date().toISOString(),
    MainPageWillBeDefined: typeof window.MainPage
});

logDebug('DEBUG', 'MainPage constructor chamado', {
    timestamp: new Date().toISOString(),
    sessionId: window.sessionId
});

logDebug('INFO', 'handleFormSubmit chamado', {
    form: form.tagName,
    formId: form.id,
    formType: typeof form
});
```

### **Visualização de Logs**
Acesse: `https://mdmidia.com.br/logging_system/viewer/log_viewer.php`

**Funcionalidades:**
- 📊 Estatísticas em tempo real
- 🔍 Filtros avançados (nível, sessão, URL, data)
- 📋 Visualização de logs com dados estruturados
- 📥 Exportação em CSV/JSON
- 🔄 Atualização automática

---

## 🔌 **API**

### **Endpoint Principal**
```
POST https://mdmidia.com.br/logging_system/debug_logger_db.php
Content-Type: application/json

{
    "level": "INFO",
    "message": "Mensagem do log",
    "data": {"key": "value"},
    "url": "https://www.segurosimediato.com.br",
    "sessionId": "sess_123456789",
    "timestamp": "2025-01-10T15:30:45.123Z",
    "userAgent": "Mozilla/5.0..."
}
```

### **API de Análise**
```
GET https://mdmidia.com.br/logging_system/viewer/api/analytics.php?action=stats
GET https://mdmidia.com.br/logging_system/viewer/api/analytics.php?action=logs&page=1&limit=20
GET https://mdmidia.com.br/logging_system/viewer/api/analytics.php?action=sessions&session_id=sess_123
```

### **Respostas da API**
```json
{
    "success": true,
    "logged": {
        "log_id": "log_123456789",
        "session_id": "sess_123456789",
        "timestamp": "2025-01-10 15:30:45",
        "level": "INFO",
        "message": "Mensagem do log"
    }
}
```

---

## 🔧 **MANUTENÇÃO**

### **Limpeza Manual**
```bash
# Limpeza com simulação
php utils/cleanup.php --dry-run --verbose

# Limpeza real (manter 30 dias)
php utils/cleanup.php

# Limpeza personalizada (manter 7 dias)
php utils/cleanup.php --days=7
```

### **Backup do Banco**
```bash
# Backup completo
mysqldump -u root -p rpa_logs > backup_rpa_logs_$(date +%Y%m%d).sql

# Backup apenas estrutura
mysqldump -u root -p --no-data rpa_logs > schema_rpa_logs.sql
```

### **Monitoramento**
```bash
# Verificar tamanho do banco
mysql -u root -p -e "
SELECT 
    table_name,
    ROUND(((data_length + index_length) / 1024 / 1024), 2) AS 'Size (MB)'
FROM information_schema.tables 
WHERE table_schema = 'rpa_logs'
ORDER BY (data_length + index_length) DESC;
"

# Verificar logs recentes
mysql -u root -p -e "
SELECT COUNT(*) as total_logs,
       COUNT(DISTINCT session_id) as unique_sessions
FROM debug_logs 
WHERE timestamp > DATE_SUB(NOW(), INTERVAL 1 HOUR);
"
```

---

## 🚨 **TROUBLESHOOTING**

### **Problemas Comuns**

#### **1. Erro de Conexão com Banco**
```bash
# Verificar se MySQL está rodando
systemctl status mysql

# Verificar usuário e permissões
mysql -u root -p -e "SELECT User, Host FROM mysql.user WHERE User='rpa_logger';"

# Testar conexão
mysql -u rpa_logger -p -e "USE rpa_logs; SELECT 1;"
```

#### **2. Erro de Permissões**
```bash
# Verificar permissões do diretório
ls -la /home/mdmidiac/public_html/logging_system/

# Corrigir permissões
chmod 755 /home/mdmidiac/public_html/logging_system
chmod 644 /home/mdmidiac/public_html/logging_system/*.php
```

#### **3. Rate Limiting Muito Restritivo**
```php
// Ajustar em config/security.php
'max_requests_per_minute' => 200, // Aumentar limite
```

#### **4. Logs Não Aparecem na Interface**
```bash
# Verificar se há logs no banco
mysql -u root -p -e "SELECT COUNT(*) FROM debug_logs;"

# Verificar logs de erro do PHP
tail -f /var/log/apache2/error.log
```

### **Logs de Debug**
```bash
# Ativar logs de erro do PHP
echo "log_errors = On" >> /etc/php/8.1/apache2/php.ini
echo "error_log = /var/log/php_errors.log" >> /etc/php/8.1/apache2/php.ini

# Reiniciar Apache
systemctl restart apache2
```

---

## 🔒 **SEGURANÇA**

### **Medidas Implementadas**
- ✅ **Validação de Entrada:** Todos os dados são validados
- ✅ **Prepared Statements:** Proteção contra SQL injection
- ✅ **Rate Limiting:** Proteção contra spam e ataques
- ✅ **CORS Seguro:** Apenas origens autorizadas
- ✅ **Sanitização:** Limpeza de dados maliciosos
- ✅ **Logs de Segurança:** Auditoria de tentativas de ataque

### **Configurações Recomendadas**
```php
// Em config/security.php
'rate_limit' => [
    'enabled' => true,
    'max_requests_per_minute' => 100,
    'ban_duration_minutes' => 60
],
'input_validation' => [
    'max_message_length' => 1000,
    'max_data_size' => 50000,
    'sanitize_input' => true
]
```

### **Monitoramento de Segurança**
```bash
# Verificar tentativas de ataque
mysql -u root -p -e "
SELECT message, COUNT(*) as count
FROM debug_logs 
WHERE session_id = 'security'
AND timestamp > DATE_SUB(NOW(), INTERVAL 24 HOUR)
GROUP BY message
ORDER BY count DESC;
"
```

---

## ⚡ **PERFORMANCE**

### **Otimizações Implementadas**
- ✅ **Índices Otimizados:** Para consultas frequentes
- ✅ **Prepared Statements:** Reutilização de queries
- ✅ **Connection Pooling:** Conexões eficientes
- ✅ **Cleanup Automático:** Limpeza de dados antigos
- ✅ **Paginação:** Para grandes volumes de dados

### **Monitoramento de Performance**
```sql
-- Verificar performance das queries
EXPLAIN SELECT * FROM debug_logs 
WHERE session_id = 'test_session' 
AND timestamp > DATE_SUB(NOW(), INTERVAL 1 DAY);

-- Verificar uso de índices
SHOW INDEX FROM debug_logs;

-- Verificar tamanho das tabelas
SELECT 
    table_name,
    ROUND(((data_length + index_length) / 1024 / 1024), 2) AS 'Size (MB)'
FROM information_schema.tables 
WHERE table_schema = 'rpa_logs';
```

### **Limites Recomendados**
- **Logs por sessão:** Máximo 1000
- **Tamanho de dados:** Máximo 50KB por log
- **Retenção:** 30 dias (configurável)
- **Rate limit:** 100 req/min por IP

---

## 🧪 **DESENVOLVIMENTO**

### **Testes Locais**
```bash
# Instalar dependências
cd local_test
pip install -r requirements.txt

# Executar todos os testes
python test_runner.py --all

# Executar teste específico
python test_runner.py --test connectivity
```

### **Estrutura de Desenvolvimento**
```
logging_system_project/
├── 📁 local_test/           # Testes automatizados
├── 📁 install/              # Scripts de instalação
├── 📁 config/               # Configurações
├── 📁 utils/                # Utilitários
├── 📁 viewer/               # Interface web
└── 📄 debug_logger_db.php   # Endpoint principal
```

### **Adicionando Novos Logs**
```javascript
// Padrão recomendado para novos logs
logDebug('INFO', 'Descrição clara da ação', {
    // Dados relevantes para análise
    context: 'valor_contexto',
    timestamp: new Date().toISOString(),
    // Outros dados úteis
});
```

### **Extensões Futuras**
- 📊 **Dashboard Avançado:** Gráficos e métricas em tempo real
- 🔔 **Alertas:** Notificações por email/Slack
- 📱 **API Mobile:** Aplicativo para monitoramento
- 🤖 **IA/ML:** Análise preditiva de erros

---

## 📞 **SUPORTE**

### **Contatos**
- **Desenvolvedor:** Sistema de Logging RPA
- **Servidor:** mdmidia.com.br
- **Documentação:** Este arquivo

### **Recursos Adicionais**
- **Logs do Sistema:** `/var/log/apache2/error.log`
- **Logs do MySQL:** `/var/log/mysql/error.log`
- **Logs de Segurança:** Tabela `debug_logs` com `session_id = 'security'`

### **Status do Sistema**
- ✅ **Banco de Dados:** Funcionando
- ✅ **API de Logging:** Funcionando
- ✅ **Interface Web:** Funcionando
- ✅ **Limpeza Automática:** Configurada
- ✅ **Testes:** Disponíveis

---

**Versão:** 1.0.0  
**Última Atualização:** Janeiro 2025  
**Status:** ✅ **PRODUÇÃO**
