# 📝 **SISTEMA DE LOGGING V2.3.0 - RPA TÔ SEGURADO**

## 🎯 **VISÃO GERAL**

O sistema de logging implementado na versão 2.3.0 oferece um controle completo sobre o registro de eventos e exibição de mensagens durante a execução do RPA. Todas as funcionalidades são configuráveis via arquivo `parametros.json`.

## ⚙️ **CONFIGURAÇÕES DISPONÍVEIS**

### **Arquivo: `parametros.json`**

```json
{
  "configuracao": {
    "log": true,                    // Ativa/desativa logging em arquivo
    "display": true,                // Ativa/desativa exibição no console
    "log_rotacao_dias": 90,         // Rotação automática de logs (dias)
    "log_nivel": "INFO"             // Nível de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
  },
  // ... outros parâmetros do RPA
}
```

### **Parâmetros de Configuração:**

| Parâmetro | Tipo | Padrão | Descrição |
|-----------|------|--------|-----------|
| `log` | boolean | `true` | Ativa/desativa o sistema de logging |
| `display` | boolean | `true` | Ativa/desativa exibição no console |
| `log_rotacao_dias` | integer | `90` | Rotação automática de logs (dias) |
| `log_nivel` | string | `"INFO"` | Nível mínimo de logging |

## 📁 **ESTRUTURA DE ARQUIVOS**

### **Diretório de Logs:**
```
logs/
├── rpa_tosegurado_20250829.log    # Log atual
├── rpa_tosegurado_20250828.log    # Log anterior
├── rpa_tosegurado_20250827.log    # Log anterior
└── ...                            # Logs anteriores
```

### **Formato do Nome:**
- **Padrão**: `rpa_tosegurado_YYYYMMDD.log`
- **Exemplo**: `rpa_tosegurado_20250829.log`

## 🔍 **NÍVEIS DE LOGGING**

### **Hierarquia de Níveis:**

1. **DEBUG** - Informações detalhadas para desenvolvimento
2. **INFO** - Informações gerais sobre o progresso
3. **WARNING** - Avisos que não impedem a execução
4. **ERROR** - Erros que podem afetar funcionalidades
5. **CRITICAL** - Erros críticos que podem parar o sistema

### **Configuração de Nível:**
- **Nível configurado**: `"INFO"`
- **Logs registrados**: INFO, WARNING, ERROR, CRITICAL
- **Logs ignorados**: DEBUG

## 📊 **CÓDIGOS DE ERRO PADRONIZADOS**

### **Categorias de Erro:**

#### **🔧 Erros de Configuração (1000-1999)**
- `1001` - Erro ao carregar arquivo de configuração
- `1002` - Configuração inválida ou incompleta
- `1003` - Erro no ChromeDriver
- `1004` - Erro ao inicializar navegador

#### **🧭 Erros de Navegação (2000-2999)**
- `2001` - Timeout na navegação
- `2002` - Elemento não encontrado na página
- `2003` - Elemento não está clicável
- `2004` - Página não carregou completamente
- `2005` - Erro no redirecionamento

#### **🤖 Erros de Automação (3000-3999)**
- `3001` - Falha ao clicar no elemento
- `3002` - Falha ao inserir dados no campo
- `3003` - Timeout aguardando elemento
- `3004` - Elemento obsoleto (stale)
- `3005` - Erro na execução de JavaScript

#### **💻 Erros de Sistema (4000-4999)**
- `4001` - Erro de conexão de rede
- `4002` - Erro de memória insuficiente
- `4003` - Erro de disco/arquivo
- `4004` - Erro de permissão

#### **✅ Sucessos (9000-9999)**
- `9001` - Tela executada com sucesso
- `9002` - RPA executado com sucesso
- `9003` - Elemento encontrado e processado
- `9004` - Ação realizada com sucesso

## 📝 **FORMATO DO LOG**

### **Estrutura da Mensagem:**

```
2025-08-29 14:30:15 | INFO     | executar_todas_telas_otimizado_v2.py:45 | [SUC-9002] RPA executado com sucesso | Caller: main.py:123:main
```

### **Componentes:**

1. **Timestamp**: `2025-08-29 14:30:15`
2. **Nível**: `INFO`
3. **Arquivo:Linha**: `executar_todas_telas_otimizado_v2.py:45`
4. **Mensagem**: `[SUC-9002] RPA executado com sucesso`
5. **Caller**: `main.py:123:main`

## 🚀 **FUNÇÕES DE LOGGING DISPONÍVEIS**

### **Importação:**
```python
from utils.logger_rpa import (
    rpa_logger,           # Instância principal do logger
    log_info,             # Log de informação
    log_error,            # Log de erro
    log_success,          # Log de sucesso
    log_exception         # Log de exceção com traceback
)
```

### **Uso Básico:**
```python
# Log de informação
log_info("Iniciando execução da Tela 1")

# Log de erro com código
log_error("Elemento não encontrado", 2002, {"tela": 1, "seletor": "button"})

# Log de sucesso
log_success("Tela 1 executada com sucesso", {"tempo": "5.2s"})

# Log de exceção
log_exception("Erro crítico na execução", 4001, {"error": str(e)})
```

### **Uso Avançado:**
```python
# Log com dados extras
log_info("Processando dados", extra_data={
    "placa": "KVA1791",
    "marca": "FORD",
    "tempo_processamento": "2.1s"
})

# Log de erro com contexto completo
log_error("Falha na automação", 3001, {
    "tela": 5,
    "acao": "clicar_botao",
    "seletor": "//button[contains(., 'Continuar')]",
    "tentativa": 1
})
```

## 🔄 **ROTAÇÃO AUTOMÁTICA**

### **Funcionamento:**
- **Frequência**: Diária (à meia-noite)
- **Retenção**: 90 dias (configurável)
- **Limpeza**: Automática de logs antigos
- **Formato**: `rpa_tosegurado_YYYYMMDD.log`

### **Exemplo de Rotação:**
```
Hoje: 29/08/2025
├── rpa_tosegurado_20250829.log    # Log atual
├── rpa_tosegurado_20250828.log    # Mantido (1 dia)
├── rpa_tosegurado_20250827.log    # Mantido (2 dias)
└── rpa_tosegurado_20250530.log    # Removido (90+ dias)
```

## 🎛️ **CONTROLE DE EXIBIÇÃO**

### **Modo Display Ativado (`"display": true`):**
```
ℹ️ 14:30:15 | INFO     | [SUC-9002] RPA executado com sucesso
❌ 14:30:16 | ERROR    | [ERR-2002] Elemento não encontrado na página
⚠️ 14:30:17 | WARNING  | Timeout aguardando elemento
🚨 14:30:18 | CRITICAL | [ERR-4001] Erro de conexão de rede
```

### **Modo Display Desativado (`"display": false`):**
- **Console**: Silencioso (apenas logs em arquivo)
- **Arquivo**: Logging completo mantido
- **Performance**: Ligeiramente melhorada

## 🔧 **CONFIGURAÇÕES AVANÇADAS**

### **Fallback Automático:**
- Se o sistema de logging não estiver disponível
- Fallback para `print()` padrão
- Mensagem de aviso sobre logging indisponível

### **Tratamento de Erros:**
- Logs de erro não interrompem a execução
- Exceções são capturadas e logadas
- Traceback completo preservado

### **Performance:**
- Logging assíncrono para não impactar execução
- Rotação automática em background
- Limpeza de logs antigos otimizada

## 📋 **EXEMPLOS DE USO**

### **1. Logging Básico:**
```python
# Configuração padrão
{
  "configuracao": {
    "log": true,
    "display": true,
    "log_rotacao_dias": 90,
    "log_nivel": "INFO"
  }
}
```

### **2. Logging Silencioso:**
```python
# Apenas arquivo, sem console
{
  "configuracao": {
    "log": true,
    "display": false,
    "log_rotacao_dias": 90,
    "log_nivel": "INFO"
  }
}
```

### **3. Logging Desabilitado:**
```python
# Sem logging
{
  "configuracao": {
    "log": false,
    "display": false,
    "log_rotacao_dias": 90,
    "log_nivel": "INFO"
  }
}
```

### **4. Logging Debug:**
```python
# Logging detalhado
{
  "configuracao": {
    "log": true,
    "display": true,
    "log_rotacao_dias": 90,
    "log_nivel": "DEBUG"
  }
}
```

## 🌟 **BENEFÍCIOS IMPLEMENTADOS**

### **1. Controle Total:**
- ✅ Logging configurável via JSON
- ✅ Display configurável via JSON
- ✅ Níveis de logging ajustáveis
- ✅ Rotação automática configurável

### **2. Rastreabilidade:**
- ✅ Timestamp preciso em cada log
- ✅ Localização exata (arquivo:linha)
- ✅ Informações do caller
- ✅ Códigos de erro padronizados

### **3. Manutenibilidade:**
- ✅ Logs estruturados e legíveis
- ✅ Rotação automática de arquivos
- ✅ Limpeza automática de logs antigos
- ✅ Fallback para sistema padrão

### **4. Performance:**
- ✅ Logging não bloqueia execução
- ✅ Rotação em background
- ✅ Limpeza otimizada
- ✅ Configuração flexível

## 🔮 **FUTURAS MELHORIAS**

### **Possíveis Expansões:**
1. **Logs Estruturados**: Formato JSON para análise automatizada
2. **Métricas**: Contadores de eventos e performance
3. **Alertas**: Notificações para erros críticos
4. **Dashboard**: Interface web para visualização de logs
5. **Integração**: Envio de logs para sistemas externos

---

## 📞 **SUPORTE**

Para dúvidas sobre o sistema de logging:

1. **Verifique** o arquivo `parametros.json`
2. **Consulte** os códigos de erro na documentação
3. **Teste** diferentes configurações
4. **Monitore** os arquivos de log na pasta `logs/`

**🎯 O sistema de logging v2.3.0 oferece controle total sobre o registro de eventos do RPA, mantendo a flexibilidade e performance!**
