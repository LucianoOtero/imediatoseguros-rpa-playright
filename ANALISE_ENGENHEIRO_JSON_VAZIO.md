# ANÁLISE TÉCNICA - ENGENHEIRO DE SOFTWARE
## PROBLEMA: JSON VAZIO NO PHP - RPA V4

**Data:** 01/10/2025  
**Analista:** Engenheiro de Software  
**Sistema:** RPA V4 - API PHP  
**Prioridade:** CRÍTICA  

---

## 📋 RESUMO EXECUTIVO

### Problema Identificado
O sistema RPA V4 não está recebendo dados JSON corretamente via API. Mesmo enviando dados válidos via `curl`, o PHP recebe um array vazio (`[]`) em vez dos dados esperados, causando falha na execução do RPA com dados dinâmicos.

### Impacto
- **Funcionalidade:** RPA não executa com dados dinâmicos
- **Fallback:** Sistema usa `parametros.json` em vez de dados da requisição
- **Progress Tracker:** Não funciona corretamente
- **Produção:** Sistema não está pronto para uso

### Recomendação
**Implementar correção defensiva imediata** e executar plano de investigação priorizado para identificar causa raiz.

---

## 🔍 ANÁLISE TÉCNICA DETALHADA

### Arquitetura do Sistema
```
Frontend (Webflow) → Nginx → PHP-FPM → index.php → SessionService → RPA Python
```

### Ponto de Falha Identificado
**Localização:** `/opt/imediatoseguros-rpa-v4/public/index.php` linha 78
```php
$input = json_decode(file_get_contents('php://input'), true);
$response = $controller->startRPA($input ?: []);
```

### Evidências
```json
// Log do sistema mostra dados vazios
{"timestamp":"2025-10-01 17:09:13","level":"INFO","message":"RPA start request received","context":{"data":[]}}

// Script gerado usa fallback
"Fonte de dados: parametros.json (fallback)"

// RPA não inicia automaticamente
"status": "pending"
```

### Possíveis Causas (Ordenadas por Probabilidade)
1. **Nginx (60%):** Configuração incorreta para POST requests
2. **PHP-FPM (25%):** Problemas de buffer ou timeout
3. **PHP (10%):** Configurações restritivas (post_max_size, etc.)
4. **Encoding (3%):** Problemas de charset ou BOM
5. **JSON (2%):** Dados corrompidos durante transmissão

---

## 🧪 PLANO DE INVESTIGAÇÃO REVISADO

### Fase 0: Diagnóstico Rápido (15 minutos)
**Objetivo:** Identificar se problema é intermitente e coletar dados básicos

#### Teste 0.1: Verificar Conectividade
```bash
# Teste básico de conectividade
curl -X POST http://37.27.92.160/api/rpa/start \
  -H 'Content-Type: application/json' \
  -d '{"test":"data"}' \
  -w "HTTP_CODE:%{http_code}\nTIME:%{time_total}\n"
```

#### Teste 0.2: Monitoramento de Logs
```bash
# Monitorar logs em tempo real
ssh root@37.27.92.160 "tail -f /var/log/nginx/access.log /var/log/nginx/error.log /var/log/php8.3-fpm.log" &
```

**Critério de Sucesso:** Identificar padrão de falha e coletar dados básicos

### Fase 1: Teste PHP Direto (10 minutos)
**Objetivo:** Confirmar se problema é específico do endpoint ou geral

#### Teste 1.1: Script de Diagnóstico Completo
```bash
# Criar script de diagnóstico
ssh root@37.27.92.160 "cat > /tmp/diagnostic.php << 'EOF'
<?php
header('Content-Type: application/json');
\$data = [
    'timestamp' => date('Y-m-d H:i:s'),
    'raw_input' => file_get_contents('php://input'),
    'raw_length' => strlen(file_get_contents('php://input')),
    'post_data' => \$_POST,
    'server_vars' => [
        'REQUEST_METHOD' => \$_SERVER['REQUEST_METHOD'],
        'CONTENT_TYPE' => \$_SERVER['CONTENT_TYPE'] ?? 'not_set',
        'CONTENT_LENGTH' => \$_SERVER['CONTENT_LENGTH'] ?? 'not_set',
        'HTTP_CONTENT_TYPE' => \$_SERVER['HTTP_CONTENT_TYPE'] ?? 'not_set'
    ],
    'php_info' => [
        'post_max_size' => ini_get('post_max_size'),
        'upload_max_filesize' => ini_get('upload_max_filesize'),
        'max_input_vars' => ini_get('max_input_vars')
    ]
];
echo json_encode(\$data, JSON_PRETTY_PRINT);
?>
EOF"
```

#### Teste 1.2: Execução do Diagnóstico
```bash
# Testar com dados reais
curl -X POST http://37.27.92.160/tmp/diagnostic.php \
  -H 'Content-Type: application/json' \
  -d '{"cpf":"97137189768","nome":"ALEX KAMINSKI","placa":"EYQ4J41","cep":"03317-000","email":"alex.kaminski@imediatoseguros.com.br","celular":"11953288466","ano":"2009"}'
```

**Critério de Sucesso:** `raw_input` contém dados JSON válidos

### Fase 2: Verificação Nginx (10 minutos)
**Objetivo:** Confirmar configuração do Nginx para POST requests

#### Teste 2.1: Configuração Específica
```bash
# Verificar configuração do endpoint
ssh root@37.27.92.160 "grep -A 20 -B 5 'location.*api' /etc/nginx/sites-available/imediatoseguros-rpa-v4"

# Verificar tipo de proxy
ssh root@37.27.92.160 "grep -E 'proxy_pass|fastcgi_pass' /etc/nginx/sites-available/imediatoseguros-rpa-v4"
```

#### Teste 2.2: Logs do Nginx
```bash
# Verificar logs de acesso e erro
ssh root@37.27.92.160 "tail -20 /var/log/nginx/access.log | grep POST"
ssh root@37.27.92.160 "tail -20 /var/log/nginx/error.log"
```

**Critério de Sucesso:** Requisição aparece nos logs, sem erros

### Fase 3: Teste de Conectividade (5 minutos)
**Objetivo:** Verificar se problema é específico do endpoint

#### Teste 3.1: Endpoint de Health
```bash
# Testar endpoint de health
curl -X POST http://37.27.92.160/api/rpa/health \
  -H 'Content-Type: application/json' \
  -d '{"test":"health"}'
```

#### Teste 3.2: Endpoint Alternativo
```bash
# Testar endpoint alternativo
curl -X POST http://37.27.92.160/start \
  -H 'Content-Type: application/json' \
  -d '{"test":"alternative"}'
```

**Critério de Sucesso:** Identificar se problema é específico do endpoint

---

## 🔧 SOLUÇÕES PROPOSTAS

### Solução 1: Correção Nginx (Mais Provável - 60%)
**Se problema for no Nginx:**

```nginx
# Adicionar ao location /api/ em /etc/nginx/sites-available/imediatoseguros-rpa-v4
location /api/ {
    client_max_body_size 10M;
    client_body_buffer_size 128k;
    client_body_timeout 60s;
    client_header_timeout 60s;
    
    # Garantir que headers são passados
    proxy_set_header Content-Type $content_type;
    proxy_set_header Content-Length $content_length;
    
    # Configuração existente...
    fastcgi_pass unix:/var/run/php/php8.3-fpm.sock;
    fastcgi_index index.php;
    include fastcgi_params;
}
```

**Comandos de Aplicação:**
```bash
# Aplicar configuração
ssh root@37.27.92.160 "cp /etc/nginx/sites-available/imediatoseguros-rpa-v4 /etc/nginx/sites-available/imediatoseguros-rpa-v4.backup"
# Editar arquivo com configuração acima
ssh root@37.27.92.160 "nginx -t && systemctl reload nginx"
```

### Solução 2: Correção PHP-FPM (25%)
**Se problema for no PHP-FPM:**

```ini
# /etc/php/8.3/fpm/php.ini
post_max_size = 10M
upload_max_filesize = 10M
max_input_vars = 3000
max_execution_time = 300
max_input_time = 300
```

**Comandos de Aplicação:**
```bash
# Aplicar configuração
ssh root@37.27.92.160 "cp /etc/php/8.3/fpm/php.ini /etc/php/8.3/fpm/php.ini.backup"
# Editar arquivo com configuração acima
ssh root@37.27.92.160 "systemctl restart php8.3-fpm"
```

### Solução 3: Correção de Código (Defensiva - 100%)
**Implementar independentemente da causa:**

```php
// Substituir linha 78 em /opt/imediatoseguros-rpa-v4/public/index.php
$rawInput = file_get_contents('php://input');
$inputLength = strlen($rawInput);

// Log para debug
error_log("DEBUG: Raw input length: $inputLength");

if ($inputLength === 0) {
    error_log("ERROR: Empty input received");
    return ['success' => false, 'error' => 'No data received'];
}

$input = json_decode($rawInput, true);
if (json_last_error() !== JSON_ERROR_NONE) {
    error_log("ERROR: JSON decode failed: " . json_last_error_msg());
    return ['success' => false, 'error' => 'Invalid JSON: ' . json_last_error_msg()];
}

$response = $controller->startRPA($input);
```

**Comandos de Aplicação:**
```bash
# Backup do arquivo
ssh root@37.27.92.160 "cp /opt/imediatoseguros-rpa-v4/public/index.php /opt/imediatoseguros-rpa-v4/public/index.php.backup"

# Aplicar correção
ssh root@37.27.92.160 "sed -i '78s/.*/                \$rawInput = file_get_contents(\"php:\/\/input\");\n                \$inputLength = strlen(\$rawInput);\n                error_log(\"DEBUG: Raw input length: \$inputLength\");\n                if (\$inputLength === 0) {\n                    error_log(\"ERROR: Empty input received\");\n                    return [\"success\" => false, \"error\" => \"No data received\"];\n                }\n                \$input = json_decode(\$rawInput, true);\n                if (json_last_error() !== JSON_ERROR_NONE) {\n                    error_log(\"ERROR: JSON decode failed: \" . json_last_error_msg());\n                    return [\"success\" => false, \"error\" => \"Invalid JSON: \" . json_last_error_msg()];\n                }/' /opt/imediatoseguros-rpa-v4/public/index.php"
```

### Solução 4: Implementação de Fallback Robusto
**Se problema for intermitente:**

```php
// Adicionar após linha 78 em index.php
if (empty($input) || json_last_error() !== JSON_ERROR_NONE) {
    // Log do problema
    error_log("JSON input failed, using fallback");
    // Usar dados padrão ou retornar erro
    $input = $this->getDefaultData();
}
```

---

## 🚀 PLANO DE IMPLEMENTAÇÃO

### Imediato (30 minutos)
1. **Executar Fase 0** - Diagnóstico rápido
2. **Executar Fase 1** - Teste PHP direto
3. **Identificar causa raiz** - Baseado nos resultados
4. **Implementar Solução 3** - Correção defensiva

### Validação (15 minutos)
1. **Testar com dados reais** - Usar dados do parametros.json
2. **Verificar logs** - Confirmar que dados chegam
3. **Validar progress tracker** - Confirmar funcionamento
4. **Testar RPA** - Confirmar execução com dados corretos

### Rollback (5 minutos)
```bash
# Se correção falhar
ssh root@37.27.92.160 "cp /opt/imediatoseguros-rpa-v4/public/index.php.backup /opt/imediatoseguros-rpa-v4/public/index.php"
ssh root@37.27.92.160 "systemctl restart php8.3-fpm nginx"
```

---

## 🎯 CRITÉRIOS DE SUCESSO

### Funcionalidade
- [ ] JSON chega corretamente no PHP
- [ ] `json_decode` funciona sem erros
- [ ] Dados são passados para o RPA
- [ ] Script é gerado com JSON dinâmico
- [ ] RPA executa com dados corretos

### Performance
- [ ] Tempo de resposta < 2 segundos
- [ ] Sem erros nos logs
- [ ] Progress tracker funciona

### Qualidade
- [ ] Código defensivo implementado
- [ ] Logs adequados para debug
- [ ] Tratamento de erros robusto

---

## 📊 MÉTRICAS DE MONITORAMENTO

### Logs a Monitorar
- `/var/log/nginx/access.log` - Requisições HTTP
- `/var/log/nginx/error.log` - Erros do Nginx
- `/var/log/php8.3-fpm.log` - Erros do PHP-FPM
- `/opt/imediatoseguros-rpa-v4/logs/rpa/app.log` - Logs da aplicação

### Métricas Importantes
- Taxa de sucesso das requisições POST
- Tempo de resposta da API
- Erros de JSON decode
- Uso de fallback para parametros.json

### Alertas Recomendados
- Erro de JSON decode > 5% das requisições
- Tempo de resposta > 5 segundos
- Uso de fallback > 10% das requisições

---

## 🔄 ESTRATÉGIA DE ROLLBACK

### Nível 1: Rollback de Código
```bash
# Restaurar arquivo original
ssh root@37.27.92.160 "cp /opt/imediatoseguros-rpa-v4/public/index.php.backup /opt/imediatoseguros-rpa-v4/public/index.php"
```

### Nível 2: Rollback de Configuração
```bash
# Restaurar configuração Nginx
ssh root@37.27.92.160 "cp /etc/nginx/sites-available/imediatoseguros-rpa-v4.backup /etc/nginx/sites-available/imediatoseguros-rpa-v4"
ssh root@37.27.92.160 "nginx -t && systemctl reload nginx"
```

### Nível 3: Rollback de PHP
```bash
# Restaurar configuração PHP
ssh root@37.27.92.160 "cp /etc/php/8.3/fpm/php.ini.backup /etc/php/8.3/fpm/php.ini"
ssh root@37.27.92.160 "systemctl restart php8.3-fpm"
```

---

## 📝 OBSERVAÇÕES TÉCNICAS

### Dados de Teste
```json
{
  "cpf": "97137189768",
  "nome": "ALEX KAMINSKI",
  "placa": "EYQ4J41",
  "cep": "03317-000",
  "email": "alex.kaminski@imediatoseguros.com.br",
  "celular": "11953288466",
  "ano": "2009"
}
```

### Ambiente de Teste
- **Servidor:** Hetzner (37.27.92.160)
- **OS:** Ubuntu 22.04 LTS
- **Nginx:** 1.24.0
- **PHP:** 8.3-FPM
- **Python:** 3.11 (venv)

### Arquivos Envolvidos
- `/opt/imediatoseguros-rpa-v4/public/index.php`
- `/opt/imediatoseguros-rpa-v4/src/Services/SessionService.php`
- `/etc/nginx/sites-available/imediatoseguros-rpa-v4`
- `/opt/imediatoseguros-rpa/parametros.json`

---

## 🛠️ FERRAMENTAS DE DEBUG RECOMENDADAS

### Xdebug + Cursor (Recomendação Principal)
**Por que usar:**
- Debug visual com breakpoints
- Step-through do código
- Inspeção de variáveis em tempo real
- Integração nativa com Cursor
- Sem dependência de terceiros
- Logs detalhados

**Configuração no Servidor:**
```bash
# Instalar Xdebug
sudo apt install php8.3-xdebug

# Configurar Xdebug
sudo tee /etc/php/8.3/fpm/conf.d/20-xdebug.ini > /dev/null << 'EOF'
zend_extension=xdebug.so
xdebug.mode=debug,develop
xdebug.start_with_request=yes
xdebug.client_host=127.0.0.1
xdebug.client_port=9003
xdebug.log=/var/log/xdebug.log
xdebug.log_level=7
xdebug.var_display_max_depth=10
xdebug.var_display_max_children=256
xdebug.var_display_max_data=1024
EOF

# Reiniciar PHP-FPM
sudo systemctl restart php8.3-fpm
```

**Configuração no Cursor:**
```json
// .vscode/launch.json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Listen for Xdebug",
            "type": "php",
            "request": "launch",
            "port": 9003,
            "pathMappings": {
                "/opt/imediatoseguros-rpa-v4": "${workspaceFolder}"
            },
            "log": true
        }
    ]
}
```

**Uso para o Problema Atual:**
1. Definir breakpoints no `index.php` linha 78
2. Inspecionar `$rawInput` e `$input`
3. Rastrear fluxo de dados até o RPA
4. Identificar onde os dados se perdem

### Ferramentas Alternativas
- **Monolog:** Logging estruturado
- **Symfony VarDumper:** Dump de variáveis
- **phpdbg:** Debug via linha de comando
- **tcpdump:** Análise de tráfego HTTP (requer sudo)

### Comparação de Ferramentas
| Ferramenta | Facilidade | Visual | Tempo Real | Independência |
|------------|------------|--------|------------|---------------|
| Xdebug + Cursor | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Logging Manual | ⭐⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| VarDumper | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| phpdbg | ⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

---

## 🎯 RECOMENDAÇÕES FINAIS

### Imediato (Hoje)
1. **Instalar Xdebug + Cursor** - Debug visual
2. **Implementar Solução 3** - Correção defensiva
3. **Executar Fase 0 e 1** - Diagnóstico
4. **Testar com dados reais** - Validação
5. **Monitorar logs** - Confirmar funcionamento

### Curto Prazo (Esta Semana)
1. **Implementar monitoramento** - Alertas automáticos
2. **Documentar solução** - Para futuras referências
3. **Treinar equipe** - Procedimentos de debug
4. **Preparar para produção** - Validação final

### Médio Prazo (Próxima Semana)
1. **Revisar arquitetura** - Otimizações
2. **Implementar cache** - Melhor performance
3. **Otimizar performance** - Reduzir latência
4. **Preparar para escala** - Suporte a mais usuários

---

## 🚨 ALERTAS E CONTINGÊNCIAS

### Alertas Críticos
- Falha na recepção de JSON > 10% das requisições
- Tempo de resposta > 10 segundos
- Erro de RPA > 5% das execuções

### Contingências
- **Fallback automático** para parametros.json
- **Retry automático** em caso de falha
- **Notificação imediata** para equipe técnica

---

## 📋 CHECKLIST DE IMPLEMENTAÇÃO

### Pré-Implementação
- [ ] Backup de todos os arquivos
- [ ] Verificação de conectividade
- [ ] Confirmação de ambiente de teste

### Implementação
- [ ] Aplicar Solução 3 (correção defensiva)
- [ ] Executar testes de validação
- [ ] Verificar logs de erro
- [ ] Confirmar funcionamento

### Pós-Implementação
- [ ] Monitorar por 24 horas
- [ ] Documentar resultados
- [ ] Treinar equipe
- [ ] Preparar para produção

---

## 👥 EQUIPE ENVOLVIDA

**Engenheiro de Software:** Análise e validação  
**Desenvolvedor:** Implementação das correções  
**DevOps:** Configuração de servidor e monitoramento  

---

## 📞 CONTATOS DE EMERGÊNCIA

**Engenheiro de Software:** Disponível para suporte técnico  
**DevOps:** Disponível para configuração de servidor  
**Desenvolvedor:** Disponível para implementação  

---

**Documento preparado para implementação imediata das correções.**
