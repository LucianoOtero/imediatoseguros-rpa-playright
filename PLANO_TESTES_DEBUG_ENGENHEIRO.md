# PLANO DE TESTES E DEBUG - ENGENHEIRO DE TESTES
## PROBLEMA: JSON VAZIO NO PHP - RPA V4

**Data:** 01/10/2025  
**Engenheiro de Testes:** Responsável pela análise e plano  
**Baseado em:** Diagnóstico Detalhado de Erros  
**Prioridade:** CRÍTICA  

---

## 📋 RESUMO EXECUTIVO

### Problema Identificado
O sistema RPA V4 não recebe dados JSON corretamente via API. O PHP recebe array vazio (`[]`) em vez dos dados esperados, causando falha na execução do RPA com dados dinâmicos.

### Causa Raiz Suspeita
**Nginx não repassa o body da requisição POST para PHP-FPM**, fazendo `file_get_contents('php://input')` retornar vazio.

### Objetivo do Plano
Identificar com precisão a causa raiz através de testes sistemáticos e implementar correções baseadas em evidências concretas.

---

## 🎯 ESTRATÉGIA DE TESTES

### Abordagem
1. **Testes de Isolamento** - Identificar componente específico com falha
2. **Testes de Integração** - Verificar comunicação entre componentes
3. **Testes de Regressão** - Validar que correções não quebram funcionalidade existente
4. **Testes de Performance** - Garantir que correções não impactam performance

### Metodologia
- **Bottom-up:** Testar componentes individuais primeiro
- **Black-box:** Testar interfaces sem conhecimento interno
- **White-box:** Analisar código e logs para identificar falhas
- **Grey-box:** Combinar abordagens para análise completa

---

## 🧪 FASE 1: TESTES DE ISOLAMENTO

### 1.1 Teste de Conectividade Básica
**Objetivo:** Verificar se o problema é de conectividade ou processamento

#### Teste 1.1.1: Ping e Conectividade
```bash
# Teste de conectividade básica
ping -c 3 37.27.92.160

# Teste de porta HTTP
telnet 37.27.92.160 80

# Teste de resposta HTTP básica
curl -I http://37.27.92.160/
```

**Critério de Sucesso:** Conectividade OK, porta 80 aberta, HTTP responde

#### Teste 1.1.2: Endpoint de Health
```bash
# Teste endpoint de health
curl -X GET http://37.27.92.160/api/rpa/health

# Teste com verbose para ver headers
curl -v -X GET http://37.27.92.160/api/rpa/health
```

**Critério de Sucesso:** Endpoint responde com status 200

### 1.2 Teste de Nginx
**Objetivo:** Verificar se Nginx está funcionando corretamente

#### Teste 1.2.1: Status do Nginx
```bash
# Verificar status do serviço
ssh root@37.27.92.160 "systemctl status nginx"

# Verificar configuração
ssh root@37.27.92.160 "nginx -t"

# Verificar logs de erro
ssh root@37.27.92.160 "tail -20 /var/log/nginx/error.log"
```

**Critério de Sucesso:** Nginx ativo, configuração válida, sem erros críticos

#### Teste 1.2.2: Configuração de POST
```bash
# Verificar configuração específica para POST
ssh root@37.27.92.160 "grep -A 10 -B 5 'location.*php' /etc/nginx/sites-available/rpa-v4"

# Verificar se há configurações específicas para POST
ssh root@37.27.92.160 "grep -i 'post\|body\|input' /etc/nginx/sites-available/rpa-v4"
```

**Critério de Sucesso:** Configuração correta para processamento de POST

### 1.3 Teste de PHP-FPM
**Objetivo:** Verificar se PHP-FPM está funcionando corretamente

#### Teste 1.3.1: Status do PHP-FPM
```bash
# Verificar status do serviço
ssh root@37.27.92.160 "systemctl status php8.3-fpm"

# Verificar processos
ssh root@37.27.92.160 "ps aux | grep php-fpm"

# Verificar logs
ssh root@37.27.92.160 "tail -20 /var/log/php8.3-fpm.log"
```

**Critério de Sucesso:** PHP-FPM ativo, processos rodando, sem erros críticos

#### Teste 1.3.2: Configuração PHP
```bash
# Verificar configurações relevantes
ssh root@37.27.92.160 "php -i | grep -E 'post_max_size|upload_max_filesize|max_input_vars|max_execution_time'"

# Verificar se Xdebug está ativo
ssh root@37.27.92.160 "php -m | grep xdebug"
```

**Critério de Sucesso:** Configurações adequadas, Xdebug ativo

---

## 🔍 FASE 2: TESTES DE INTEGRAÇÃO

### 2.1 Teste de Comunicação Nginx-PHP
**Objetivo:** Verificar se Nginx está passando dados corretamente para PHP

#### Teste 2.1.1: Script PHP Simples
```bash
# Criar script de teste simples
ssh root@37.27.92.160 "cat > /opt/imediatoseguros-rpa-v4/public/test_simple.php << 'EOF'
<?php
header('Content-Type: application/json');
echo json_encode([
    'method' => \$_SERVER['REQUEST_METHOD'],
    'content_type' => \$_SERVER['CONTENT_TYPE'] ?? 'not_set',
    'content_length' => \$_SERVER['CONTENT_LENGTH'] ?? 'not_set',
    'raw_input' => file_get_contents('php://input'),
    'raw_length' => strlen(file_get_contents('php://input')),
    'post_data' => \$_POST
]);
?>
EOF"

# Testar com GET
curl -X GET http://37.27.92.160/test_simple.php

# Testar com POST sem body
curl -X POST http://37.27.92.160/test_simple.php

# Testar com POST com body
curl -X POST http://37.27.92.160/test_simple.php -H 'Content-Type: application/json' -d '{"test":"data"}'
```

**Critério de Sucesso:** POST com body retorna dados corretos

#### Teste 2.1.2: Teste de Headers
```bash
# Testar com headers específicos
curl -X POST http://37.27.92.160/test_simple.php \
  -H 'Content-Type: application/json' \
  -H 'Content-Length: 16' \
  -d '{"test":"data"}'

# Testar com headers incorretos
curl -X POST http://37.27.92.160/test_simple.php \
  -H 'Content-Type: text/plain' \
  -d '{"test":"data"}'
```

**Critério de Sucesso:** Headers corretos permitem processamento

### 2.2 Teste de JSON Processing
**Objetivo:** Verificar se JSON está sendo processado corretamente

#### Teste 2.2.1: JSON Válido
```bash
# Testar com JSON válido
curl -X POST http://37.27.92.160/test_simple.php \
  -H 'Content-Type: application/json' \
  -d '{"cpf":"97137189768","nome":"ALEX KAMINSKI","placa":"EYQ4J41","cep":"03317-000","email":"alex.kaminski@imediatoseguros.com.br","celular":"11953288466","ano":"2009"}'
```

**Critério de Sucesso:** JSON é recebido e processado corretamente

#### Teste 2.2.2: JSON Inválido
```bash
# Testar com JSON inválido
curl -X POST http://37.27.92.160/test_simple.php \
  -H 'Content-Type: application/json' \
  -d '{"cpf":"97137189768","nome":"ALEX KAMINSKI"'
```

**Critério de Sucesso:** JSON inválido é detectado e tratado

### 2.3 Teste de API Endpoint
**Objetivo:** Verificar se o endpoint da API está funcionando

#### Teste 2.3.1: Endpoint Start
```bash
# Testar endpoint start com dados válidos
curl -X POST http://37.27.92.160/api/rpa/start \
  -H 'Content-Type: application/json' \
  -d '{"cpf":"97137189768","nome":"ALEX KAMINSKI","placa":"EYQ4J41","cep":"03317-000","email":"alex.kaminski@imediatoseguros.com.br","celular":"11953288466","ano":"2009"}' \
  -v
```

**Critério de Sucesso:** Endpoint responde com session_id

#### Teste 2.3.2: Monitoramento de Logs
```bash
# Monitorar logs em tempo real
ssh root@37.27.92.160 "tail -f /var/log/nginx/rpa-v4.error.log /var/log/php8.3-fpm.log /opt/imediatoseguros-rpa-v4/logs/rpa/app.log" &
```

**Critério de Sucesso:** Logs mostram processamento correto

---

## 🔧 FASE 3: TESTES DE DEBUG AVANÇADO

### 3.1 Teste de Xdebug
**Objetivo:** Verificar se Xdebug está funcionando para debug

#### Teste 3.1.1: Configuração Xdebug
```bash
# Verificar configuração
ssh root@37.27.92.160 "cat /etc/php/8.3/fpm/conf.d/20-xdebug.ini"

# Verificar se arquivo de log existe
ssh root@37.27.92.160 "ls -la /var/log/xdebug.log"

# Criar arquivo de log se não existir
ssh root@37.27.92.160 "sudo touch /var/log/xdebug.log && sudo chown www-data:www-data /var/log/xdebug.log"
```

**Critério de Sucesso:** Xdebug configurado, arquivo de log existe

#### Teste 3.1.2: Teste de Debug
```bash
# Criar script de teste com Xdebug
ssh root@37.27.92.160 "cat > /opt/imediatoseguros-rpa-v4/public/test_xdebug.php << 'EOF'
<?php
header('Content-Type: application/json');
\$rawInput = file_get_contents('php://input');
\$inputLength = strlen(\$rawInput);
\$decoded = json_decode(\$rawInput, true);
\$jsonError = json_last_error();

echo json_encode([
    'raw_input' => \$rawInput,
    'raw_length' => \$inputLength,
    'decoded' => \$decoded,
    'json_error' => \$jsonError,
    'json_error_msg' => json_last_error_msg()
]);
?>
EOF"

# Testar com dados
curl -X POST http://37.27.92.160/test_xdebug.php \
  -H 'Content-Type: application/json' \
  -d '{"test":"xdebug"}'
```

**Critério de Sucesso:** Xdebug processa dados corretamente

### 3.2 Teste de SessionService
**Objetivo:** Verificar se SessionService está funcionando

#### Teste 3.2.1: Variáveis Indefinidas
```bash
# Verificar código do SessionService
ssh root@37.27.92.160 "grep -n -A 5 -B 5 'tempJsonFile\|jsonContent' /opt/imediatoseguros-rpa-v4/src/Services/SessionService.php"

# Verificar se variáveis estão definidas
ssh root@37.27.92.160 "grep -n 'useJsonData' /opt/imediatoseguros-rpa-v4/src/Services/SessionService.php"
```

**Critério de Sucesso:** Variáveis estão definidas corretamente

#### Teste 3.2.2: Teste de Geração de Script
```bash
# Testar geração de script
curl -X POST http://37.27.92.160/api/rpa/start \
  -H 'Content-Type: application/json' \
  -d '{"cpf":"97137189768","nome":"ALEX KAMINSKI","placa":"EYQ4J41","cep":"03317-000","email":"alex.kaminski@imediatoseguros.com.br","celular":"11953288466","ano":"2009"}'

# Verificar se script foi gerado
ssh root@37.27.92.160 "ls -la /opt/imediatoseguros-rpa/scripts/start_rpa_v4_* | tail -3"
```

**Critério de Sucesso:** Script é gerado com dados corretos

---

## 📊 FASE 4: TESTES DE PERFORMANCE

### 4.1 Teste de Carga
**Objetivo:** Verificar se o sistema suporta carga normal

#### Teste 4.1.1: Carga Básica
```bash
# Teste com múltiplas requisições
for i in {1..5}; do
  curl -X POST http://37.27.92.160/api/rpa/start \
    -H 'Content-Type: application/json' \
    -d "{\"cpf\":\"97137189768\",\"nome\":\"TEST $i\",\"placa\":\"TEST$i\",\"cep\":\"03317-000\"}" &
done
wait
```

**Critério de Sucesso:** Todas as requisições são processadas

#### Teste 4.1.2: Teste de Timeout
```bash
# Teste com timeout
curl -X POST http://37.27.92.160/api/rpa/start \
  -H 'Content-Type: application/json' \
  -d '{"cpf":"97137189768","nome":"ALEX KAMINSKI","placa":"EYQ4J41","cep":"03317-000","email":"alex.kaminski@imediatoseguros.com.br","celular":"11953288466","ano":"2009"}' \
  --max-time 30
```

**Critério de Sucesso:** Requisição completa em menos de 30 segundos

---

## 🎯 FASE 5: TESTES DE REGRESSÃO

### 5.1 Teste de Funcionalidade Existente
**Objetivo:** Verificar se correções não quebram funcionalidade existente

#### Teste 5.1.1: RPA com parametros.json
```bash
# Testar RPA com arquivo de parâmetros
ssh root@37.27.92.160 "cd /opt/imediatoseguros-rpa && /opt/imediatoseguros-rpa/venv/bin/python executar_rpa_imediato_playwright.py --config parametros.json --session test_regression --progress-tracker json"
```

**Critério de Sucesso:** RPA executa com parametros.json

#### Teste 5.1.2: Progress Tracker
```bash
# Testar progress tracker
curl -s http://37.27.92.160/api/rpa/progress/test_regression
```

**Critério de Sucesso:** Progress tracker funciona

### 5.2 Teste de Compatibilidade
**Objetivo:** Verificar compatibilidade com diferentes tipos de dados

#### Teste 5.2.1: Dados Mínimos
```bash
# Testar com dados mínimos
curl -X POST http://37.27.92.160/api/rpa/start \
  -H 'Content-Type: application/json' \
  -d '{"cpf":"12345678901","nome":"TEST","placa":"TEST123","cep":"01234567"}'
```

**Critério de Sucesso:** Dados mínimos são aceitos

#### Teste 5.2.2: Dados Completos
```bash
# Testar com dados completos
curl -X POST http://37.27.92.160/api/rpa/start \
  -H 'Content-Type: application/json' \
  -d '{"cpf":"97137189768","nome":"ALEX KAMINSKI","placa":"EYQ4J41","cep":"03317-000","email":"alex.kaminski@imediatoseguros.com.br","celular":"11953288466","ano":"2009"}'
```

**Critério de Sucesso:** Dados completos são aceitos

---

## 📋 CRITÉRIOS DE ACEITAÇÃO

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
- [ ] Sistema suporta carga normal

### Qualidade
- [ ] Código defensivo implementado
- [ ] Logs adequados para debug
- [ ] Tratamento de erros robusto
- [ ] Compatibilidade mantida

---

## 🚨 PLANO DE CONTINGÊNCIA

### Se Testes Falharem
1. **Documentar falha** - Logs e evidências
2. **Analisar causa** - Identificar componente com problema
3. **Implementar correção** - Baseada em evidências
4. **Retestar** - Validar correção
5. **Regressão** - Verificar que não quebrou outras funcionalidades

### Se Correções Quebrarem Funcionalidade
1. **Rollback imediato** - Restaurar estado anterior
2. **Análise de impacto** - Identificar o que foi afetado
3. **Correção incremental** - Implementar mudanças menores
4. **Teste gradual** - Validar cada mudança
5. **Documentação** - Registrar lições aprendidas

---

## 📊 MÉTRICAS DE SUCESSO

### Métricas Técnicas
- **Taxa de sucesso:** > 95% das requisições POST
- **Tempo de resposta:** < 2 segundos
- **Erros de JSON:** < 1% das requisições
- **Uso de fallback:** < 5% das requisições

### Métricas de Qualidade
- **Cobertura de testes:** > 90% do código crítico
- **Logs de erro:** < 10 por dia
- **Tempo de debug:** < 30 minutos para identificar problema
- **Tempo de correção:** < 2 horas para implementar solução

---

## ⏰ CRONOGRAMA DE EXECUÇÃO

### Dia 1 (Hoje)
- **09:00-10:00:** Fase 1 - Testes de Isolamento
- **10:00-11:00:** Fase 2 - Testes de Integração
- **11:00-12:00:** Fase 3 - Testes de Debug Avançado

### Dia 2 (Amanhã)
- **09:00-10:00:** Fase 4 - Testes de Performance
- **10:00-11:00:** Fase 5 - Testes de Regressão
- **11:00-12:00:** Análise de resultados e correções

---

## 📝 RELATÓRIO DE TESTES

### Template de Relatório
```markdown
# RELATÓRIO DE TESTES - [DATA]

## Resumo Executivo
- Total de testes: [X]
- Sucessos: [X]
- Falhas: [X]
- Taxa de sucesso: [X]%

## Testes por Fase
### Fase 1: Isolamento
- [ ] Teste 1.1.1: Ping e Conectividade
- [ ] Teste 1.1.2: Endpoint de Health
- [ ] Teste 1.2.1: Status do Nginx
- [ ] Teste 1.2.2: Configuração de POST
- [ ] Teste 1.3.1: Status do PHP-FPM
- [ ] Teste 1.3.2: Configuração PHP

### Fase 2: Integração
- [ ] Teste 2.1.1: Script PHP Simples
- [ ] Teste 2.1.2: Teste de Headers
- [ ] Teste 2.2.1: JSON Válido
- [ ] Teste 2.2.2: JSON Inválido
- [ ] Teste 2.3.1: Endpoint Start
- [ ] Teste 2.3.2: Monitoramento de Logs

### Fase 3: Debug Avançado
- [ ] Teste 3.1.1: Configuração Xdebug
- [ ] Teste 3.1.2: Teste de Debug
- [ ] Teste 3.2.1: Variáveis Indefinidas
- [ ] Teste 3.2.2: Teste de Geração de Script

### Fase 4: Performance
- [ ] Teste 4.1.1: Carga Básica
- [ ] Teste 4.1.2: Teste de Timeout

### Fase 5: Regressão
- [ ] Teste 5.1.1: RPA com parametros.json
- [ ] Teste 5.1.2: Progress Tracker
- [ ] Teste 5.2.1: Dados Mínimos
- [ ] Teste 5.2.2: Dados Completos

## Problemas Identificados
1. [Problema 1]
2. [Problema 2]
3. [Problema 3]

## Correções Implementadas
1. [Correção 1]
2. [Correção 2]
3. [Correção 3]

## Próximos Passos
1. [Passo 1]
2. [Passo 2]
3. [Passo 3]
```

---

## 👥 EQUIPE ENVOLVIDA

**Engenheiro de Testes:** Responsável pelo plano e execução  
**Desenvolvedor:** Implementação de correções  
**Engenheiro de Software:** Análise e validação  
**DevOps:** Configuração de servidor  

---

## 📞 CONTATOS DE EMERGÊNCIA

**Engenheiro de Testes:** Disponível para suporte técnico  
**Desenvolvedor:** Disponível para implementação  
**Engenheiro de Software:** Disponível para análise  
**DevOps:** Disponível para configuração  

---

## 🔄 PRÓXIMOS PASSOS

### Imediato (Hoje)
1. **Executar Fase 1** - Testes de Isolamento
2. **Identificar componente com falha** - Baseado nos resultados
3. **Implementar correção específica** - Para o componente identificado

### Curto Prazo (Esta Semana)
1. **Executar todas as fases** - Validação completa
2. **Implementar correções** - Baseadas em evidências
3. **Validar funcionamento** - Testes de regressão

### Médio Prazo (Próxima Semana)
1. **Documentar solução** - Para futuras referências
2. **Implementar monitoramento** - Alertas automáticos
3. **Preparar para produção** - Validação final

---

**Plano preparado para execução imediata dos testes e debug.**
