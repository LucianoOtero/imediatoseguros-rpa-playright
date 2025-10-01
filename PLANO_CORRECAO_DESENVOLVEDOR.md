# 🛠️ Plano de Correção e Testes - Desenvolvedor

## 📋 **Resumo Executivo**

**Papel**: Desenvolvedor responsável pela implementação das correções no sistema RPA V4.

**Problema**: Scripts de inicialização RPA não estão sendo gerados devido a permissões insuficientes no diretório `/opt/imediatoseguros-rpa/scripts/`.

**Objetivo**: Implementar correções robustas e testes abrangentes para garantir 100% de funcionalidade do sistema.

**Prazo**: 2 horas (incluindo testes e validação)

---

## 🎯 **Análise da Situação Atual**

### **Problema Identificado**
- **Causa Raiz**: Permissões insuficientes no diretório de scripts
- **Impacto**: 100% das sessões RPA falham imediatamente
- **Evidência**: Logs mostram "script criado" mas arquivo não existe no filesystem
- **Urgência**: 🔴 **CRÍTICA** - Sistema completamente inoperante

### **Arquivos Afetados**
- `rpa-v4/src/Services/SessionService.php` - Método `startRPABackground()`
- `/opt/imediatoseguros-rpa/scripts/` - Diretório de scripts
- Logs do sistema - Para monitoramento

### **Dependências**
- PHP 8.3 + PHP-FPM
- Usuário `www-data` (execução do PHP-FPM)
- Diretório `/opt/imediatoseguros-rpa/scripts/`
- Comando `dos2unix` (conversão de encoding)

---

## 🔧 **Plano de Correção Detalhado**

### **Fase 1: Diagnóstico e Preparação (15 minutos)**

#### **1.1 Verificação do Ambiente Atual**
```bash
#!/bin/bash
# diagnose_environment.sh

echo "=== Diagnóstico do Ambiente RPA V4 ==="

# 1. Verificar permissões do diretório de scripts
echo "1. Verificando permissões do diretório de scripts..."
ls -la /opt/imediatoseguros-rpa/scripts/

# 2. Verificar proprietário e grupo
echo "2. Verificando proprietário do diretório..."
stat /opt/imediatoseguros-rpa/scripts/

# 3. Verificar usuário do PHP-FPM
echo "3. Verificando usuário do PHP-FPM..."
ps aux | grep php-fpm | head -5

# 4. Verificar se www-data pode escrever
echo "4. Testando escrita como www-data..."
sudo -u www-data touch /opt/imediatoseguros-rpa/scripts/test_write_$(date +%s).txt
if [ $? -eq 0 ]; then
    echo "✅ Escrita bem-sucedida"
    sudo -u www-data rm /opt/imediatoseguros-rpa/scripts/test_write_*.txt
else
    echo "❌ Falha na escrita - PERMISSÕES INCORRETAS"
fi

# 5. Verificar espaço em disco
echo "5. Verificando espaço em disco..."
df -h /opt/imediatoseguros-rpa/

# 6. Verificar logs recentes
echo "6. Verificando logs recentes..."
tail -20 /opt/imediatoseguros-rpa-v4/logs/rpa/app.log

echo "=== Diagnóstico concluído ==="
```

#### **1.2 Backup das Configurações Atuais**
```bash
#!/bin/bash
# backup_current_state.sh

echo "=== Backup do Estado Atual ==="

# Criar diretório de backup
BACKUP_DIR="/opt/imediatoseguros-rpa/backup_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

# Backup das permissões
echo "1. Fazendo backup das permissões..."
ls -la /opt/imediatoseguros-rpa/scripts/ > "$BACKUP_DIR/permissions_backup.txt"
stat /opt/imediatoseguros-rpa/scripts/ >> "$BACKUP_DIR/permissions_backup.txt"

# Backup do código atual
echo "2. Fazendo backup do código..."
cp /opt/imediatoseguros-rpa-v4/src/Services/SessionService.php "$BACKUP_DIR/SessionService_backup.php"

# Backup dos logs
echo "3. Fazendo backup dos logs..."
cp /opt/imediatoseguros-rpa-v4/logs/rpa/app.log "$BACKUP_DIR/app_log_backup.log"

echo "Backup criado em: $BACKUP_DIR"
echo "=== Backup concluído ==="
```

### **Fase 2: Correção de Permissões (10 minutos)**

#### **2.1 Correção Imediata de Permissões**
```bash
#!/bin/bash
# fix_permissions.sh

echo "=== Correção de Permissões ==="

# 1. Parar serviços para evitar conflitos
echo "1. Parando serviços..."
systemctl stop php8.3-fpm
systemctl stop nginx

# 2. Corrigir proprietário do diretório de scripts
echo "2. Corrigindo proprietário..."
chown -R www-data:www-data /opt/imediatoseguros-rpa/scripts/

# 3. Corrigir permissões do diretório
echo "3. Corrigindo permissões..."
chmod 755 /opt/imediatoseguros-rpa/scripts/

# 4. Verificar se www-data pode escrever
echo "4. Testando escrita após correção..."
sudo -u www-data touch /opt/imediatoseguros-rpa/scripts/test_write_$(date +%s).txt
if [ $? -eq 0 ]; then
    echo "✅ Escrita bem-sucedida após correção"
    sudo -u www-data rm /opt/imediatoseguros-rpa/scripts/test_write_*.txt
else
    echo "❌ Falha na escrita - CORREÇÃO INSUFICIENTE"
    exit 1
fi

# 5. Reiniciar serviços
echo "5. Reiniciando serviços..."
systemctl start php8.3-fpm
systemctl start nginx

# 6. Verificar status dos serviços
echo "6. Verificando status dos serviços..."
systemctl status php8.3-fpm --no-pager -l
systemctl status nginx --no-pager -l

echo "=== Correção de permissões concluída ==="
```

#### **2.2 Teste de Criação de Script**
```bash
#!/bin/bash
# test_script_creation.sh

echo "=== Teste de Criação de Script ==="

# Simular criação de script
SCRIPT_PATH="/opt/imediatoseguros-rpa/scripts/test_script_$(date +%s).sh"
SCRIPT_CONTENT='#!/bin/bash
echo "Teste de script criado em $(date)"
echo "Script executado com sucesso"
rm -f "$0"'

echo "1. Criando script em: $SCRIPT_PATH"
echo "$SCRIPT_CONTENT" > "$SCRIPT_PATH"

if [ $? -eq 0 ]; then
    echo "✅ Script criado com sucesso"
    
    echo "2. Verificando se arquivo existe"
    if [ -f "$SCRIPT_PATH" ]; then
        echo "✅ Arquivo existe"
        
        echo "3. Definindo permissões"
        chmod 755 "$SCRIPT_PATH"
        
        if [ -x "$SCRIPT_PATH" ]; then
            echo "✅ Arquivo é executável"
            
            echo "4. Executando script"
            "$SCRIPT_PATH"
            
            if [ $? -eq 0 ]; then
                echo "✅ Script executado com sucesso"
                echo "✅ Teste de criação de script PASSOU"
            else
                echo "❌ Falha na execução do script"
                echo "❌ Teste de criação de script FALHOU"
                exit 1
            fi
        else
            echo "❌ Arquivo não é executável"
            echo "❌ Teste de criação de script FALHOU"
            exit 1
        fi
    else
        echo "❌ Arquivo não existe"
        echo "❌ Teste de criação de script FALHOU"
        exit 1
    fi
else
    echo "❌ Falha na criação do script"
    echo "❌ Teste de criação de script FALHOU"
    exit 1
fi

echo "=== Teste de criação de script concluído ==="
```

### **Fase 3: Melhoria do Código (45 minutos)**

#### **3.1 Implementação da Correção no SessionService.php**

**Arquivo**: `rpa-v4/src/Services/SessionService.php`

**Método**: `startRPABackground()`

**Código Corrigido**:
```php
private function startRPABackground(string $sessionId, array $data): void
{
    try {
        $this->logger->debug('Starting RPA background process', [
            'session_id' => $sessionId,
            'scripts_path' => $this->scriptsPath,
            'scripts_path_exists' => is_dir($this->scriptsPath),
            'scripts_path_writable' => is_writable($this->scriptsPath),
            'scripts_path_permissions' => substr(sprintf('%o', fileperms($this->scriptsPath)), -4)
        ]);

        // Gerar conteúdo do script
        $scriptContent = $this->generateStartScript($sessionId, $data);
        $scriptPath = $this->scriptsPath . "/start_rpa_v4_{$sessionId}.sh";
        
        // ✅ VERIFICAR se diretório existe e é gravável
        if (!is_dir($this->scriptsPath)) {
            throw new \RuntimeException("Diretório de scripts não existe: {$this->scriptsPath}");
        }
        
        if (!is_writable($this->scriptsPath)) {
            throw new \RuntimeException("Diretório de scripts não é gravável: {$this->scriptsPath}");
        }
        
        // ✅ CRIAR script com verificação de erro
        $bytes = file_put_contents($scriptPath, $scriptContent);
        if ($bytes === false) {
            throw new \RuntimeException("Falha ao criar script em: {$scriptPath}. Verifique permissões.");
        }
        
        // ✅ VERIFICAR se arquivo foi criado
        if (!file_exists($scriptPath)) {
            throw new \RuntimeException("Script não foi criado: {$scriptPath}");
        }
        
        // ✅ DEFINIR permissões de execução
        if (!chmod($scriptPath, 0755)) {
            throw new \RuntimeException("Falha ao definir permissões do script: {$scriptPath}");
        }
        
        // ✅ CONVERTER encoding
        exec("dos2unix {$scriptPath} 2>/dev/null", $output, $returnCode);
        if ($returnCode !== 0) {
            $this->logger->warning('dos2unix failed', [
                'script_path' => $scriptPath,
                'return_code' => $returnCode,
                'output' => $output
            ]);
        }
        
        // ✅ VERIFICAR se é executável
        if (!is_executable($scriptPath)) {
            throw new \RuntimeException("Script não é executável: {$scriptPath}");
        }
        
        // ✅ EXECUTAR em background
        $command = "nohup {$scriptPath} > /dev/null 2>&1 &";
        exec($command, $output, $returnCode);
        
        if ($returnCode !== 0) {
            throw new \RuntimeException("Falha ao executar script em background: {$command}");
        }
        
        // ✅ LOG de sucesso com detalhes
        $this->logger->info('RPA background process started successfully', [
            'session_id' => $sessionId,
            'script_path' => $scriptPath,
            'file_size' => filesize($scriptPath),
            'is_executable' => is_executable($scriptPath),
            'command' => $command,
            'bytes_written' => $bytes
        ]);
        
    } catch (\Exception $e) {
        // ✅ LOG de erro detalhado
        $this->logger->error('Failed to start RPA background process', [
            'session_id' => $sessionId,
            'error' => $e->getMessage(),
            'script_path' => $scriptPath ?? 'unknown',
            'scripts_path' => $this->scriptsPath,
            'scripts_path_exists' => is_dir($this->scriptsPath),
            'scripts_path_writable' => is_writable($this->scriptsPath),
            'scripts_path_permissions' => is_dir($this->scriptsPath) ? substr(sprintf('%o', fileperms($this->scriptsPath)), -4) : 'unknown'
        ]);
        
        // ✅ ATUALIZAR status da sessão para failed
        $this->repository->updateSession($sessionId, [
            'status' => 'failed',
            'failed_at' => date('Y-m-d H:i:s'),
            'error' => $e->getMessage()
        ]);
        
        throw $e;
    }
}
```

#### **3.2 Script de Deploy da Correção**
```bash
#!/bin/bash
# deploy_code_fix.sh

echo "=== Deploy da Correção de Código ==="

# 1. Fazer backup do arquivo atual
echo "1. Fazendo backup do SessionService.php..."
cp /opt/imediatoseguros-rpa-v4/src/Services/SessionService.php /opt/imediatoseguros-rpa-v4/src/Services/SessionService.php.backup.$(date +%Y%m%d_%H%M%S)

# 2. Aplicar correção (assumindo que o arquivo corrigido está em /tmp/SessionService_fixed.php)
echo "2. Aplicando correção..."
if [ -f "/tmp/SessionService_fixed.php" ]; then
    cp /tmp/SessionService_fixed.php /opt/imediatoseguros-rpa-v4/src/Services/SessionService.php
    echo "✅ Correção aplicada"
else
    echo "❌ Arquivo de correção não encontrado em /tmp/SessionService_fixed.php"
    echo "Por favor, crie o arquivo com o código corrigido"
    exit 1
fi

# 3. Verificar sintaxe PHP
echo "3. Verificando sintaxe PHP..."
php -l /opt/imediatoseguros-rpa-v4/src/Services/SessionService.php
if [ $? -eq 0 ]; then
    echo "✅ Sintaxe PHP válida"
else
    echo "❌ Erro de sintaxe PHP"
    exit 1
fi

# 4. Reiniciar PHP-FPM para carregar o novo código
echo "4. Reiniciando PHP-FPM..."
systemctl restart php8.3-fpm

# 5. Verificar status do PHP-FPM
echo "5. Verificando status do PHP-FPM..."
systemctl status php8.3-fpm --no-pager -l

echo "=== Deploy da correção concluído ==="
```

### **Fase 4: Testes Abrangentes (30 minutos)**

#### **4.1 Teste de Criação de Sessão**
```bash
#!/bin/bash
# test_session_creation.sh

echo "=== Teste de Criação de Sessão ==="

# 1. Testar criação de sessão via API
echo "1. Testando criação de sessão via API..."
SESSION_RESPONSE=$(curl -s -X POST http://37.27.92.160/api/rpa/start \
  -H "Content-Type: application/json" \
  -d '{"cpf":"12345678901","nome":"TESTE AUTOMATIZADO","placa":"ABC1234","cep":"01234567","email":"teste@imediatoseguros.com.br","celular":"11999999999","ano":"2020"}')

echo "Resposta da API: $SESSION_RESPONSE"

# 2. Extrair session_id
SESSION_ID=$(echo "$SESSION_RESPONSE" | jq -r '.session_id')
echo "Session ID: $SESSION_ID"

# 3. Verificar se sessão foi criada
if [ "$SESSION_ID" != "null" ] && [ "$SESSION_ID" != "" ]; then
    echo "✅ Sessão criada com sucesso"
    
    # 4. Aguardar alguns segundos
    echo "4. Aguardando 10 segundos para o script ser criado..."
    sleep 10
    
    # 5. Verificar se script foi criado
    echo "5. Verificando se script foi criado..."
    if [ -f "/opt/imediatoseguros-rpa/scripts/start_rpa_v4_${SESSION_ID}.sh" ]; then
        echo "✅ Script criado com sucesso"
        
        # 6. Verificar permissões do script
        echo "6. Verificando permissões do script..."
        ls -la "/opt/imediatoseguros-rpa/scripts/start_rpa_v4_${SESSION_ID}.sh"
        
        # 7. Verificar se script é executável
        if [ -x "/opt/imediatoseguros-rpa/scripts/start_rpa_v4_${SESSION_ID}.sh" ]; then
            echo "✅ Script é executável"
        else
            echo "❌ Script não é executável"
        fi
        
        # 8. Verificar status da sessão
        echo "8. Verificando status da sessão..."
        STATUS_RESPONSE=$(curl -s http://37.27.92.160/api/rpa/status/$SESSION_ID)
        echo "Status da sessão: $STATUS_RESPONSE"
        
        # 9. Verificar logs
        echo "9. Verificando logs..."
        tail -10 /opt/imediatoseguros-rpa-v4/logs/rpa/app.log
        
        echo "✅ Teste de criação de sessão PASSOU"
    else
        echo "❌ Script não foi criado"
        echo "❌ Teste de criação de sessão FALHOU"
        exit 1
    fi
else
    echo "❌ Falha na criação da sessão"
    echo "❌ Teste de criação de sessão FALHOU"
    exit 1
fi

echo "=== Teste de criação de sessão concluído ==="
```

#### **4.2 Teste de Execução do RPA**
```bash
#!/bin/bash
# test_rpa_execution.sh

echo "=== Teste de Execução do RPA ==="

# 1. Criar sessão
echo "1. Criando sessão para teste..."
SESSION_RESPONSE=$(curl -s -X POST http://37.27.92.160/api/rpa/start \
  -H "Content-Type: application/json" \
  -d '{"cpf":"97137189768","nome":"ALEX KAMINSKI","placa":"EYQ4J41","cep":"03317000","email":"alex.kaminski@imediatoseguros.com.br","celular":"11953288466","ano":"2009"}')

SESSION_ID=$(echo "$SESSION_RESPONSE" | jq -r '.session_id')
echo "Session ID: $SESSION_ID"

# 2. Monitorar execução por 5 minutos
echo "2. Monitorando execução por 5 minutos..."
START_TIME=$(date +%s)
TIMEOUT=300  # 5 minutos

while true; do
    CURRENT_TIME=$(date +%s)
    ELAPSED=$((CURRENT_TIME - START_TIME))
    
    if [ $ELAPSED -gt $TIMEOUT ]; then
        echo "Timeout atingido (${TIMEOUT}s)"
        break
    fi
    
    # Verificar status da sessão
    STATUS_RESPONSE=$(curl -s http://37.27.92.160/api/rpa/status/$SESSION_ID)
    STATUS=$(echo "$STATUS_RESPONSE" | jq -r '.session.status')
    
    echo "$(date): Status: $STATUS"
    
    if [ "$STATUS" = "completed" ]; then
        echo "✅ RPA executado com sucesso"
        break
    elif [ "$STATUS" = "failed" ]; then
        echo "❌ RPA falhou"
        echo "Logs de erro:"
        tail -20 /opt/imediatoseguros-rpa/logs/rpa_v4_${SESSION_ID}.log
        exit 1
    fi
    
    sleep 10
done

# 3. Verificar arquivos gerados
echo "3. Verificando arquivos gerados..."
if [ -f "/opt/imediatoseguros-rpa/rpa_data/progress_${SESSION_ID}.json" ]; then
    echo "✅ Arquivo de progresso criado"
else
    echo "❌ Arquivo de progresso não criado"
fi

if [ -f "/opt/imediatoseguros-rpa/rpa_data/history_${SESSION_ID}.json" ]; then
    echo "✅ Arquivo de histórico criado"
else
    echo "❌ Arquivo de histórico não criado"
fi

echo "=== Teste de execução do RPA concluído ==="
```

#### **4.3 Teste de Múltiplas Sessões**
```bash
#!/bin/bash
# test_multiple_sessions.sh

echo "=== Teste de Múltiplas Sessões ==="

# 1. Criar 3 sessões simultâneas
echo "1. Criando 3 sessões simultâneas..."
SESSION_IDS=()

for i in {1..3}; do
    SESSION_RESPONSE=$(curl -s -X POST http://37.27.92.160/api/rpa/start \
      -H "Content-Type: application/json" \
      -d "{\"cpf\":\"1234567890${i}\",\"nome\":\"TESTE ${i}\",\"placa\":\"ABC123${i}\",\"cep\":\"0123456${i}\",\"email\":\"teste${i}@imediatoseguros.com.br\",\"celular\":\"1199999999${i}\",\"ano\":\"2020\"}")
    
    SESSION_ID=$(echo "$SESSION_RESPONSE" | jq -r '.session_id')
    SESSION_IDS+=("$SESSION_ID")
    echo "Sessão $i: $SESSION_ID"
done

# 2. Verificar se todos os scripts foram criados
echo "2. Verificando criação de scripts..."
ALL_SCRIPTS_CREATED=true

for SESSION_ID in "${SESSION_IDS[@]}"; do
    if [ -f "/opt/imediatoseguros-rpa/scripts/start_rpa_v4_${SESSION_ID}.sh" ]; then
        echo "✅ Script criado para sessão: $SESSION_ID"
    else
        echo "❌ Script não criado para sessão: $SESSION_ID"
        ALL_SCRIPTS_CREATED=false
    fi
done

if [ "$ALL_SCRIPTS_CREATED" = true ]; then
    echo "✅ Todos os scripts foram criados"
else
    echo "❌ Alguns scripts não foram criados"
    exit 1
fi

# 3. Monitorar execução das sessões
echo "3. Monitorando execução das sessões..."
START_TIME=$(date +%s)
TIMEOUT=600  # 10 minutos

while true; do
    CURRENT_TIME=$(date +%s)
    ELAPSED=$((CURRENT_TIME - START_TIME))
    
    if [ $ELAPSED -gt $TIMEOUT ]; then
        echo "Timeout atingido (${TIMEOUT}s)"
        break
    fi
    
    ALL_COMPLETED=true
    ANY_FAILED=false
    
    for SESSION_ID in "${SESSION_IDS[@]}"; do
        STATUS_RESPONSE=$(curl -s http://37.27.92.160/api/rpa/status/$SESSION_ID)
        STATUS=$(echo "$STATUS_RESPONSE" | jq -r '.session.status')
        
        if [ "$STATUS" != "completed" ]; then
            ALL_COMPLETED=false
        fi
        
        if [ "$STATUS" = "failed" ]; then
            ANY_FAILED=true
        fi
    done
    
    if [ "$ALL_COMPLETED" = true ]; then
        echo "✅ Todas as sessões foram concluídas com sucesso"
        break
    elif [ "$ANY_FAILED" = true ]; then
        echo "❌ Alguma sessão falhou"
        exit 1
    fi
    
    echo "$(date): Aguardando conclusão das sessões..."
    sleep 15
done

echo "=== Teste de múltiplas sessões concluído ==="
```

### **Fase 5: Validação Final (20 minutos)**

#### **5.1 Teste de Health Check**
```bash
#!/bin/bash
# test_health_check.sh

echo "=== Teste de Health Check ==="

# 1. Verificar health check da API
echo "1. Verificando health check da API..."
HEALTH_RESPONSE=$(curl -s http://37.27.92.160/api/rpa/health)
echo "Health check: $HEALTH_RESPONSE"

# 2. Verificar se todos os componentes estão OK
STATUS=$(echo "$HEALTH_RESPONSE" | jq -r '.health.status')
if [ "$STATUS" = "healthy" ]; then
    echo "✅ Health check passou"
else
    echo "❌ Health check falhou"
    exit 1
fi

# 3. Verificar métricas
echo "3. Verificando métricas..."
METRICS_RESPONSE=$(curl -s http://37.27.92.160/api/rpa/metrics)
echo "Métricas: $METRICS_RESPONSE"

echo "=== Teste de health check concluído ==="
```

#### **5.2 Teste de Stress**
```bash
#!/bin/bash
# test_stress.sh

echo "=== Teste de Stress ==="

# 1. Criar 10 sessões rapidamente
echo "1. Criando 10 sessões rapidamente..."
SESSION_IDS=()

for i in {1..10}; do
    SESSION_RESPONSE=$(curl -s -X POST http://37.27.92.160/api/rpa/start \
      -H "Content-Type: application/json" \
      -d "{\"cpf\":\"1234567890${i}\",\"nome\":\"STRESS TEST ${i}\",\"placa\":\"STR${i}\",\"cep\":\"0123456${i}\",\"email\":\"stress${i}@test.com\",\"celular\":\"1199999999${i}\",\"ano\":\"2020\"}")
    
    SESSION_ID=$(echo "$SESSION_RESPONSE" | jq -r '.session_id')
    SESSION_IDS+=("$SESSION_ID")
    echo "Sessão $i: $SESSION_ID"
    
    # Pequena pausa entre requisições
    sleep 1
done

# 2. Verificar se todos os scripts foram criados
echo "2. Verificando criação de scripts..."
ALL_SCRIPTS_CREATED=true

for SESSION_ID in "${SESSION_IDS[@]}"; do
    if [ -f "/opt/imediatoseguros-rpa/scripts/start_rpa_v4_${SESSION_ID}.sh" ]; then
        echo "✅ Script criado para sessão: $SESSION_ID"
    else
        echo "❌ Script não criado para sessão: $SESSION_ID"
        ALL_SCRIPTS_CREATED=false
    fi
done

if [ "$ALL_SCRIPTS_CREATED" = true ]; then
    echo "✅ Teste de stress PASSOU - Todos os scripts criados"
else
    echo "❌ Teste de stress FALHOU - Alguns scripts não criados"
    exit 1
fi

echo "=== Teste de stress concluído ==="
```

---

## 📊 **Métricas de Sucesso**

### **Antes da Correção**
- ❌ **Taxa de sucesso**: 0%
- ❌ **Scripts criados**: 0%
- ❌ **Sessões funcionais**: 0%
- ❌ **Health check**: Degradado

### **Após a Correção (Esperado)**
- ✅ **Taxa de sucesso**: 100%
- ✅ **Scripts criados**: 100%
- ✅ **Sessões funcionais**: 100%
- ✅ **Health check**: Healthy
- ✅ **Múltiplas sessões**: Funcionando
- ✅ **Stress test**: Passando

---

## 🚨 **Plano de Rollback**

### **Cenários de Rollback**
1. **Falha na correção de permissões**
2. **Erro no código corrigido**
3. **Problemas de performance**
4. **Falha nos testes**

### **Procedimento de Rollback**
```bash
#!/bin/bash
# rollback.sh

echo "=== Rollback do Sistema ==="

# 1. Parar serviços
echo "1. Parando serviços..."
systemctl stop php8.3-fpm
systemctl stop nginx

# 2. Restaurar permissões originais
echo "2. Restaurando permissões originais..."
if [ -f "/opt/imediatoseguros-rpa/backup_*/permissions_backup.txt" ]; then
    # Restaurar permissões do backup
    chown -R root:root /opt/imediatoseguros-rpa/scripts/
    chmod 755 /opt/imediatoseguros-rpa/scripts/
    echo "✅ Permissões restauradas"
else
    echo "⚠️ Backup de permissões não encontrado"
fi

# 3. Restaurar código original
echo "3. Restaurando código original..."
if [ -f "/opt/imediatoseguros-rpa-v4/src/Services/SessionService.php.backup.*" ]; then
    BACKUP_FILE=$(ls -t /opt/imediatoseguros-rpa-v4/src/Services/SessionService.php.backup.* | head -1)
    cp "$BACKUP_FILE" /opt/imediatoseguros-rpa-v4/src/Services/SessionService.php
    echo "✅ Código restaurado"
else
    echo "⚠️ Backup de código não encontrado"
fi

# 4. Reiniciar serviços
echo "4. Reiniciando serviços..."
systemctl start php8.3-fpm
systemctl start nginx

# 5. Verificar status
echo "5. Verificando status..."
systemctl status php8.3-fpm --no-pager -l
systemctl status nginx --no-pager -l

echo "=== Rollback concluído ==="
```

---

## 📋 **Checklist de Implementação**

### **Fase 1: Diagnóstico e Preparação**
- [ ] Executar `diagnose_environment.sh`
- [ ] Executar `backup_current_state.sh`
- [ ] Verificar logs de diagnóstico
- [ ] Confirmar causa raiz

### **Fase 2: Correção de Permissões**
- [ ] Executar `fix_permissions.sh`
- [ ] Executar `test_script_creation.sh`
- [ ] Verificar se www-data pode escrever
- [ ] Confirmar permissões corretas

### **Fase 3: Melhoria do Código**
- [ ] Aplicar correção no `SessionService.php`
- [ ] Executar `deploy_code_fix.sh`
- [ ] Verificar sintaxe PHP
- [ ] Reiniciar PHP-FPM

### **Fase 4: Testes Abrangentes**
- [ ] Executar `test_session_creation.sh`
- [ ] Executar `test_rpa_execution.sh`
- [ ] Executar `test_multiple_sessions.sh`
- [ ] Verificar logs de teste

### **Fase 5: Validação Final**
- [ ] Executar `test_health_check.sh`
- [ ] Executar `test_stress.sh`
- [ ] Verificar métricas de sucesso
- [ ] Confirmar funcionamento completo

---

## 🎯 **Conclusão**

### **Objetivos do Plano**
1. **Corrigir permissões** do diretório de scripts
2. **Implementar verificação robusta** de erros no código
3. **Executar testes abrangentes** para validar correções
4. **Garantir 100% de funcionalidade** do sistema

### **Tempo Estimado**
- **Total**: 2 horas
- **Diagnóstico**: 15 minutos
- **Correção**: 10 minutos
- **Código**: 45 minutos
- **Testes**: 30 minutos
- **Validação**: 20 minutos

### **Riscos Mitigados**
- ✅ **Backup completo** do estado atual
- ✅ **Plano de rollback** preparado
- ✅ **Testes abrangentes** para validação
- ✅ **Monitoramento contínuo** durante implementação

### **Próximos Passos**
1. **Executar diagnóstico** para confirmar causa raiz
2. **Aplicar correções** seguindo o plano
3. **Executar testes** para validar funcionamento
4. **Monitorar sistema** após implementação

---

**Desenvolvedor**: Responsável pela implementação  
**Data**: 2025-10-01  
**Versão**: 1.0  
**Status**: Plano completo - Pronto para execução
