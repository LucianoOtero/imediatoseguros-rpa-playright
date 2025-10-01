# PLANO DE IMPLEMENTAÇÃO - DESENVOLVEDOR
## PROBLEMA: JSON VAZIO NO PHP - RPA V4

**Data:** 01/10/2025  
**Desenvolvedor:** Responsável pela implementação  
**Baseado em:** Análise do Engenheiro de Software  
**Prioridade:** CRÍTICA  

---

## 📋 RESUMO EXECUTIVO

### Problema
O sistema RPA V4 não recebe dados JSON corretamente via API. O PHP recebe array vazio (`[]`) em vez dos dados esperados, causando falha na execução do RPA com dados dinâmicos.

### Solução Proposta
Implementar **Xdebug + Cursor** para debug visual e **correção defensiva** no código PHP para identificar e resolver a causa raiz.

### Tempo Estimado
- **Setup inicial:** 30 minutos
- **Debug e correção:** 2-4 horas
- **Testes e validação:** 1 hora
- **Total:** 3.5-5.5 horas

---

## 🎯 OBJETIVOS

### Primário
- Identificar por que JSON chega vazio no PHP
- Implementar correção definitiva
- Validar funcionamento com dados reais

### Secundário
- Configurar ambiente de debug profissional
- Documentar solução para futuras referências
- Preparar sistema para produção

---

## 🛠️ FASE 1: CONFIGURAÇÃO DO AMBIENTE DE DEBUG

### 1.1 Instalação do Xdebug no Servidor
**Tempo:** 10 minutos

```bash
# Conectar ao servidor
ssh root@37.27.92.160

# Instalar Xdebug
sudo apt update
sudo apt install php8.3-xdebug

# Verificar instalação
php -m | grep xdebug
```

### 1.2 Configuração do Xdebug
**Tempo:** 10 minutos

```bash
# Criar arquivo de configuração
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
xdebug.idekey=CURSOR
EOF

# Reiniciar PHP-FPM
sudo systemctl restart php8.3-fpm

# Verificar se Xdebug está ativo
php -i | grep xdebug
```

### 1.3 Configuração do Cursor
**Tempo:** 10 minutos

```bash
# Criar diretório .vscode se não existir
mkdir -p .vscode

# Criar arquivo launch.json
cat > .vscode/launch.json << 'EOF'
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
            "log": true,
            "stopOnEntry": false,
            "xdebugSettings": {
                "max_children": 256,
                "max_data": 1024,
                "max_depth": 10
            }
        }
    ]
}
EOF
```

### 1.4 Instalação da Extensão PHP no Cursor
**Tempo:** 5 minutos

1. Abrir Cursor
2. Ir para Extensions (Ctrl+Shift+X)
3. Buscar "PHP Debug"
4. Instalar extensão "PHP Debug" (Xdebug)
5. Reiniciar Cursor

---

## 🔍 FASE 2: DEBUG E INVESTIGAÇÃO

### 2.1 Backup dos Arquivos
**Tempo:** 5 minutos

```bash
# Backup do index.php
ssh root@37.27.92.160 "cp /opt/imediatoseguros-rpa-v4/public/index.php /opt/imediatoseguros-rpa-v4/public/index.php.backup"

# Backup do SessionService.php
ssh root@37.27.92.160 "cp /opt/imediatoseguros-rpa-v4/src/Services/SessionService.php /opt/imediatoseguros-rpa-v4/src/Services/SessionService.php.backup"
```

### 2.2 Configuração de Debug no Cursor
**Tempo:** 10 minutos

1. **Abrir projeto no Cursor**
2. **Configurar breakpoints:**
   - Linha 78 em `index.php`: `$input = json_decode(file_get_contents('php://input'), true);`
   - Linha 79 em `index.php`: `$response = $controller->startRPA($input ?: []);`
   - Linha 297 em `SessionService.php`: `$useJsonData = !empty($data) && $this->validateData($data);`

3. **Iniciar debug:**
   - Pressionar F5 ou ir em Run > Start Debugging
   - Selecionar "Listen for Xdebug"

### 2.3 Teste de Debug
**Tempo:** 15 minutos

```bash
# Testar com dados reais
curl -X POST http://37.27.92.160/api/rpa/start \
  -H 'Content-Type: application/json' \
  -d '{"cpf":"97137189768","nome":"ALEX KAMINSKI","placa":"EYQ4J41","cep":"03317-000","email":"alex.kaminski@imediatoseguros.com.br","celular":"11953288466","ano":"2009"}'
```

**Durante o debug, inspecionar:**
- `$_SERVER['REQUEST_METHOD']`
- `$_SERVER['CONTENT_TYPE']`
- `$_SERVER['CONTENT_LENGTH']`
- `file_get_contents('php://input')`
- `json_decode()` resultado
- `$input` final

### 2.4 Análise dos Resultados
**Tempo:** 20 minutos

**Verificar:**
1. **Se dados chegam ao PHP:** `file_get_contents('php://input')` não está vazio
2. **Se JSON é válido:** `json_decode()` não retorna erro
3. **Se dados passam para controller:** `$input` contém dados esperados
4. **Se problema está no SessionService:** `$data` chega vazio

---

## 🔧 FASE 3: IMPLEMENTAÇÃO DE CORREÇÕES

### 3.1 Correção Defensiva no index.php
**Tempo:** 15 minutos

```php
// Substituir linha 78 em /opt/imediatoseguros-rpa-v4/public/index.php
$rawInput = file_get_contents('php://input');
$inputLength = strlen($rawInput);

// Log para debug
error_log("DEBUG: Raw input length: $inputLength");
error_log("DEBUG: Raw input content: " . substr($rawInput, 0, 500));

if ($inputLength === 0) {
    error_log("ERROR: Empty input received");
    return ['success' => false, 'error' => 'No data received'];
}

$input = json_decode($rawInput, true);
if (json_last_error() !== JSON_ERROR_NONE) {
    error_log("ERROR: JSON decode failed: " . json_last_error_msg());
    error_log("ERROR: Raw input was: " . $rawInput);
    return ['success' => false, 'error' => 'Invalid JSON: ' . json_last_error_msg()];
}

$response = $controller->startRPA($input);
```

### 3.2 Correção no SessionService.php
**Tempo:** 10 minutos

```php
// Adicionar logs no método generateStartScript
private function generateStartScript(string $sessionId, array $data): string
{
    // Log dos dados recebidos
    $this->logger->info('Generating start script', [
        'session_id' => $sessionId,
        'data_received' => !empty($data),
        'data_keys' => array_keys($data),
        'data_sample' => array_slice($data, 0, 3, true)
    ]);
    
    // Resto do método...
}
```

### 3.3 Teste das Correções
**Tempo:** 15 minutos

```bash
# Testar correção
curl -X POST http://37.27.92.160/api/rpa/start \
  -H 'Content-Type: application/json' \
  -d '{"cpf":"97137189768","nome":"ALEX KAMINSKI","placa":"EYQ4J41","cep":"03317-000","email":"alex.kaminski@imediatoseguros.com.br","celular":"11953288466","ano":"2009"}'

# Verificar logs
ssh root@37.27.92.160 "tail -20 /var/log/php8.3-fpm.log"
ssh root@37.27.92.160 "tail -20 /opt/imediatoseguros-rpa-v4/logs/rpa/app.log"
```

---

## 🧪 FASE 4: TESTES E VALIDAÇÃO

### 4.1 Teste com Dados Reais
**Tempo:** 20 minutos

```bash
# Teste 1: Dados completos
curl -X POST http://37.27.92.160/api/rpa/start \
  -H 'Content-Type: application/json' \
  -d '{"cpf":"97137189768","nome":"ALEX KAMINSKI","placa":"EYQ4J41","cep":"03317-000","email":"alex.kaminski@imediatoseguros.com.br","celular":"11953288466","ano":"2009"}'

# Teste 2: Dados mínimos
curl -X POST http://37.27.92.160/api/rpa/start \
  -H 'Content-Type: application/json' \
  -d '{"cpf":"12345678901","nome":"TEST","placa":"TEST123","cep":"01234567"}'

# Teste 3: JSON inválido
curl -X POST http://37.27.92.160/api/rpa/start \
  -H 'Content-Type: application/json' \
  -d '{"cpf":"12345678901","nome":"TEST"'
```

### 4.2 Validação do Progress Tracker
**Tempo:** 15 minutos

```bash
# Verificar se progress tracker funciona
curl -s http://37.27.92.160/api/rpa/progress/{session_id} | jq

# Verificar se arquivo JSON é criado
ssh root@37.27.92.160 "ls -la /opt/imediatoseguros-rpa/rpa_data/progress_*.json"
```

### 4.3 Validação do RPA
**Tempo:** 20 minutos

```bash
# Verificar se RPA executa com dados corretos
ssh root@37.27.92.160 "ls -la /opt/imediatoseguros-rpa/scripts/start_rpa_v4_* | tail -5"

# Verificar logs do RPA
ssh root@37.27.92.160 "tail -20 /opt/imediatoseguros-rpa/logs/rpa_v4_*.log"
```

---

## 📊 FASE 5: MONITORAMENTO E DOCUMENTAÇÃO

### 5.1 Configuração de Monitoramento
**Tempo:** 15 minutos

```bash
# Criar script de monitoramento
ssh root@37.27.92.160 "cat > /opt/imediatoseguros-rpa-v4/scripts/monitor_json.sh << 'EOF'
#!/bin/bash
echo \"=== JSON DEBUG MONITOR ===\"
echo \"Timestamp: \$(date)\"
echo \"\"

# Verificar logs recentes
echo \"1. Logs PHP-FPM (últimos 5):\"
tail -5 /var/log/php8.3-fpm.log | grep -E 'DEBUG|ERROR'
echo \"\"

# Verificar logs da aplicação
echo \"2. Logs Aplicação (últimos 5):\"
tail -5 /opt/imediatoseguros-rpa-v4/logs/rpa/app.log | grep -E 'DEBUG|ERROR'
echo \"\"

# Verificar status da API
echo \"3. Status da API:\"
curl -s http://37.27.92.160/api/rpa/health | jq
echo \"\"

# Verificar processos PHP
echo \"4. Processos PHP:\"
ps aux | grep php-fpm | head -3
EOF"

chmod +x /opt/imediatoseguros-rpa-v4/scripts/monitor_json.sh
```

### 5.2 Documentação da Solução
**Tempo:** 20 minutos

```markdown
# SOLUÇÃO: JSON VAZIO NO PHP - RPA V4

## Problema Identificado
- JSON chegava vazio no PHP
- Causa: [IDENTIFICAR APÓS DEBUG]

## Solução Implementada
- Correção defensiva no index.php
- Logs detalhados para debug
- Validação de input

## Configuração Xdebug
- Instalado e configurado
- Integração com Cursor
- Breakpoints funcionais

## Testes Realizados
- Dados completos: ✅
- Dados mínimos: ✅
- JSON inválido: ✅
- Progress tracker: ✅

## Monitoramento
- Script: /opt/imediatoseguros-rpa-v4/scripts/monitor_json.sh
- Logs: /var/log/php8.3-fpm.log
- Aplicação: /opt/imediatoseguros-rpa-v4/logs/rpa/app.log
```

---

## 🚨 CONTINGÊNCIA E ROLLBACK

### 6.1 Plano de Rollback
**Tempo:** 5 minutos

```bash
# Se correção falhar
ssh root@37.27.92.160 "cp /opt/imediatoseguros-rpa-v4/public/index.php.backup /opt/imediatoseguros-rpa-v4/public/index.php"
ssh root@37.27.92.160 "cp /opt/imediatoseguros-rpa-v4/src/Services/SessionService.php.backup /opt/imediatoseguros-rpa-v4/src/Services/SessionService.php"
ssh root@37.27.92.160 "systemctl restart php8.3-fpm nginx"
```

### 6.2 Verificação de Rollback
**Tempo:** 5 minutos

```bash
# Testar se rollback funcionou
curl -X POST http://37.27.92.160/api/rpa/start \
  -H 'Content-Type: application/json' \
  -d '{"test":"rollback"}'
```

---

## 📋 CHECKLIST DE IMPLEMENTAÇÃO

### Pré-Implementação
- [ ] Backup de todos os arquivos
- [ ] Verificação de conectividade
- [ ] Confirmação de ambiente de teste

### Fase 1: Configuração
- [ ] Xdebug instalado no servidor
- [ ] Xdebug configurado corretamente
- [ ] Cursor configurado para debug
- [ ] Extensão PHP instalada no Cursor

### Fase 2: Debug
- [ ] Breakpoints configurados
- [ ] Debug funcionando
- [ ] Dados inspecionados
- [ ] Causa raiz identificada

### Fase 3: Correção
- [ ] Correção defensiva implementada
- [ ] Logs adicionados
- [ ] Código testado
- [ ] Funcionalidade validada

### Fase 4: Testes
- [ ] Teste com dados reais
- [ ] Teste com dados mínimos
- [ ] Teste com JSON inválido
- [ ] Progress tracker validado
- [ ] RPA executando corretamente

### Fase 5: Monitoramento
- [ ] Script de monitoramento criado
- [ ] Documentação atualizada
- [ ] Logs configurados
- [ ] Alertas implementados

### Pós-Implementação
- [ ] Monitorar por 24 horas
- [ ] Documentar resultados
- [ ] Treinar equipe
- [ ] Preparar para produção

---

## ⏰ CRONOGRAMA DETALHADO

### Dia 1 (Hoje)
- **09:00-09:30:** Fase 1 - Configuração do ambiente
- **09:30-10:30:** Fase 2 - Debug e investigação
- **10:30-11:00:** Fase 3 - Implementação de correções
- **11:00-11:30:** Fase 4 - Testes e validação
- **11:30-12:00:** Fase 5 - Monitoramento e documentação

### Dia 2 (Amanhã)
- **09:00-09:30:** Monitoramento e ajustes
- **09:30-10:00:** Documentação final
- **10:00-10:30:** Preparação para produção

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
- [ ] Documentação completa

---

## 📞 SUPORTE E CONTATOS

**Engenheiro de Software:** Disponível para suporte técnico  
**DevOps:** Disponível para configuração de servidor  
**Equipe:** Disponível para testes e validação  

---

## 🔄 PRÓXIMOS PASSOS

### Imediato
1. Executar Fase 1 - Configuração do ambiente
2. Iniciar Fase 2 - Debug e investigação
3. Identificar causa raiz
4. Implementar correção

### Curto Prazo
1. Validar correção com testes
2. Configurar monitoramento
3. Documentar solução
4. Preparar para produção

### Médio Prazo
1. Otimizar performance
2. Implementar cache
3. Preparar para escala
4. Treinar equipe

---

**Plano preparado para implementação imediata.**
