# PROJETO MIGRAÇÃO RPAController.php V6.9.1

## 📋 RESUMO EXECUTIVO

**Objetivo**: Migrar as funcionalidades do `start.php` para o `RPAController.php` com melhorias baseadas nas discussões técnicas sobre PH3A, timeouts e validação de campos obrigatórios.

**Problema Identificado**: O `start.php` contém toda a lógica de PH3A e webhooks, mas não é executado pelo roteamento Nginx. O `RPAController.php` é o arquivo correto, mas não possui essas funcionalidades.

**Melhorias Implementadas**: 
- Timeout PH3A ajustado para 5 segundos (baseado no teste de performance)
- Validação obrigatória de campos PH3A
- Novo código de erro específico para falha na validação do CPF
- Tratamento adequado de campos vazios

---

## 🔍 ANÁLISE TÉCNICA DETALHADA

### Problemas Identificados no start.php Atual

#### 1. Timeout PH3A Insuficiente
```php
// ❌ Configuração atual (insuficiente)
curl_setopt($ch, CURLOPT_TIMEOUT, 15);        // 15 segundos
curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 5);   // 5 segundos
```

#### 2. Falta de Validação de Campos Obrigatórios
```php
// ❌ Comportamento atual: Continua mesmo com campos vazios
if ($ph3a_result['success']) {
    // Preencher campos
} else {
    echo "❌ PH3A: Falha na consulta\n";
    // ← Continua execução sem dados obrigatórios
}
```

#### 3. Impacto nos Sistemas
- **Webhooks**: Recebem campos vazios
- **RPA**: Executa com dados incompletos
- **Experiência do usuário**: Ruim

### Soluções Implementadas

#### 1. Timeout PH3A Otimizado
```php
// ✅ Configuração otimizada (baseada no teste de performance)
curl_setopt($ch, CURLOPT_TIMEOUT, 5);         // 5 segundos
curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 2);  // 2 segundos
```

#### 2. Validação Obrigatória de Campos
```php
// ✅ Validação implementada
if (!$ph3a_result['success'] && !empty($campos_obrigatorios_vazios)) {
    return $this->errorResponse('Não foi possível validar o CPF', 9001);
}
```

#### 3. Novo Código de Erro
- **Código**: 9001
- **Descrição**: "Não foi possível validar o CPF"
- **Condição**: PH3A falha + campos obrigatórios vazios

---

## 🚀 IMPLEMENTAÇÃO DETALHADA

### FASE 1: PREPARAÇÃO E BACKUP

#### 1.1 Backup do Arquivo Atual
```bash
# Backup do RPAController.php atual
cp /opt/imediatoseguros-rpa-v4/src/Controllers/RPAController.php /opt/imediatoseguros-rpa-v4/src/Controllers/RPAController.php.backup.$(date +%Y%m%d_%H%M%S)
```

#### 1.2 Verificação de Dependências
- Verificar se `ConfigService` pode ser usado para configurações PH3A/webhooks
- Verificar se `LoggerInterface` pode ser usado para logs detalhados
- Verificar se `SessionService` pode ser usado para criação de sessões

### FASE 2: IMPLEMENTAÇÃO DAS FUNCIONALIDADES

#### 2.1 Adicionar Métodos Privados no RPAController.php

```php
/**
 * Call PH3A API to fill missing fields
 * Timeout otimizado para 5 segundos baseado no teste de performance
 */
private function callPH3AApi(string $cpf): array
{
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, 'https://mdmidia.com.br/cpf-validate.php');
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode(['cpf' => $cpf]));
    curl_setopt($ch, CURLOPT_HTTPHEADER, [
        'Content-Type: application/json',
        'User-Agent: RPA-API-v6.9.1'
    ]);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_TIMEOUT, 5);         // ✅ 5 segundos (otimizado)
    curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 2);   // ✅ 2 segundos (otimizado)
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
    
    $response = curl_exec($ch);
    $http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    $error = curl_error($ch);
    curl_close($ch);
    
    return [
        'success' => $http_code >= 200 && $http_code < 300,
        'http_code' => $http_code,
        'response' => $response,
        'error' => $error
    ];
}

/**
 * Call webhook endpoint
 */
private function callWebhook(string $url, array $data): array
{
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
    curl_setopt($ch, CURLOPT_HTTPHEADER, [
        'Content-Type: application/json',
        'User-Agent: RPA-API-v6.9.1'
    ]);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_TIMEOUT, 30);
    curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 10);
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
    
    $response = curl_exec($ch);
    $http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    $error = curl_error($ch);
    curl_close($ch);
    
    return [
        'success' => $http_code >= 200 && $http_code < 300,
        'http_code' => $http_code,
        'response' => $response,
        'error' => $error
    ];
}

/**
 * Start RPA process (síncrono - aguarda dados PH3A)
 */
private function startRPAProcess(array $data): array
{
    $rpa_command = "cd /opt/imediatoseguros-rpa && source venv/bin/activate && python executar_rpa_imediato_playwright.py '" . json_encode($data) . "'";
    $output = shell_exec($rpa_command);
    
    return [
        'success' => !empty($output),
        'output' => $output,
        'command' => $rpa_command
    ];
}

/**
 * Log webhook results with performance metrics
 */
private function logWebhookResults(string $sessionId, array $logData): void
{
    $log_file = "/opt/imediatoseguros-rpa/logs/webhook_calls_" . date('Y-m-d') . ".log";
    if (!is_dir(dirname($log_file))) {
        mkdir(dirname($log_file), 0755, true);
    }
    file_put_contents($log_file, json_encode($logData) . "\n", FILE_APPEND | LOCK_EX);
}

/**
 * Validate required PH3A fields
 */
private function validatePH3AFields(array $data): array
{
    $campos_obrigatorios = ['sexo', 'data_nascimento', 'estado_civil'];
    $campos_vazios = [];
    
    foreach ($campos_obrigatorios as $campo) {
        if (empty($data[$campo])) {
            $campos_vazios[] = $campo;
        }
    }
    
    return [
        'valid' => empty($campos_vazios),
        'campos_vazios' => $campos_vazios
    ];
}
```

#### 2.2 Modificar o Método startRPA()

```php
public function startRPA(array $data): array
{
    $start_time = microtime(true);
    
    try {
        $this->logger->info('RPA start request received', ['data' => $data]);
        
        // Rate limiting
        $clientIp = $_SERVER['REMOTE_ADDR'] ?? 'unknown';
        if (!$this->rateLimitService->isAllowed($clientIp)) {
            $this->logger->warning('Rate limit exceeded', ['ip' => $clientIp]);
            return $this->errorResponse('Rate limit exceeded. Try again later.');
        }
        
        // Validação de entrada
        $validation = $this->validationService->validate($data);
        if ($validation->hasErrors()) {
            $this->logger->warning('Validation failed', [
                'errors' => $validation->getErrors(),
                'data' => $data
            ]);
            return $this->errorResponse('Dados inválidos: ' . implode(', ', $validation->getErrors()));
        }
        
        // ========================================
        // ETAPA 1: CONSULTAR API PH3A (SE NECESSÁRIO)
        // ========================================
        $ph3a_start = microtime(true);
        $campos_ph3a_vazios = [];
        if (empty($data['sexo'])) $campos_ph3a_vazios[] = 'sexo';
        if (empty($data['data_nascimento'])) $campos_ph3a_vazios[] = 'data_nascimento';
        if (empty($data['estado_civil'])) $campos_ph3a_vazios[] = 'estado_civil';
        
        $ph3a_data = [];
        $ph3a_result = null;
        
        if (!empty($campos_ph3a_vazios) && !empty($data['cpf'])) {
            $this->logger->info('Consulting PH3A API', ['fields' => $campos_ph3a_vazios]);
            $ph3a_result = $this->callPH3AApi($data['cpf']);
            
            if ($ph3a_result['success']) {
                $ph3a_json = json_decode($ph3a_result['response'], true);
                
                if ($ph3a_json && $ph3a_json['codigo'] == 1 && isset($ph3a_json['data'])) {
                    $ph3a_data = $ph3a_json['data'];
                    
                    // Mapear campos PH3A
                    if (empty($data['sexo']) && isset($ph3a_data['sexo'])) {
                        $data['sexo'] = ($ph3a_data['sexo'] == 1) ? 'Masculino' : 'Feminino';
                    }
                    
                    if (empty($data['estado_civil']) && isset($ph3a_data['estado_civil'])) {
                        $estado_civil_map = [0 => 'Solteiro', 1 => 'Casado', 2 => 'Divorciado', 3 => 'Viúvo'];
                        $data['estado_civil'] = $estado_civil_map[$ph3a_data['estado_civil']] ?? '';
                    }
                    
                    if (empty($data['data_nascimento']) && isset($ph3a_data['data_nascimento'])) {
                        try {
                            $date = new DateTime($ph3a_data['data_nascimento']);
                            $data['data_nascimento'] = $date->format('d/m/Y');
                        } catch (Exception $e) {
                            $data['data_nascimento'] = $ph3a_data['data_nascimento'];
                        }
                    }
                    
                    $this->logger->info('PH3A data filled successfully');
                } else {
                    $this->logger->warning('PH3A: CPF válido mas não encontrado na base');
                }
            } else {
                // PH3A falhou - verificar se campos obrigatórios estão vazios
                $campos_obrigatorios_vazios = array_intersect($campos_ph3a_vazios, ['sexo', 'data_nascimento', 'estado_civil']);
                
                if (!empty($campos_obrigatorios_vazios)) {
                    $this->logger->error('PH3A failed and required fields empty', [
                        'required_fields' => $campos_obrigatorios_vazios,
                        'ph3a_error' => $ph3a_result['error']
                    ]);
                    
                    return $this->errorResponse('Não foi possível validar o CPF', 9001);
                }
                
                $this->logger->warning('PH3A failed but continuing', [
                    'error' => $ph3a_result['error']
                ]);
            }
        } else {
            $this->logger->info('PH3A: Campos já preenchidos ou CPF vazio');
        }
        
        $ph3a_time = microtime(true) - $ph3a_start;
        
        // ========================================
        // ETAPA 2: CHAMAR WEBHOOKS PRIMEIRO
        // ========================================
        $webhooks_start = microtime(true);
        
        // Prepare webhook data
        $webhook_data = [
            'data' => [
                'NOME' => $data['nome'],
                'DDD-CELULAR' => $data['ddd_celular'] ?? '11',
                'CELULAR' => $data['celular'] ?? substr($data['telefone'], 2),
                'Email' => $data['email'],
                'CEP' => $data['cep'],
                'CPF' => $data['cpf'],
                'MARCA' => $data['marca'] ?? '',
                'PLACA' => $data['placa'],
                'VEICULO' => $data['marca'] ?? '',
                'ANO' => $data['ano'] ?? '',
                'GCLID_FLD' => $data['gclid'] ?? '',
                'SEXO' => $data['sexo'] ?? '',
                'DATA-DE-NASCIMENTO' => $data['data_nascimento'] ?? '',
                'ESTADO-CIVIL' => $data['estado_civil'] ?? '',
                'produto' => $data['produto'] ?? 'seguro-auto',
                'landing_url' => $data['landing_url'] ?? '',
                'utm_source' => $data['utm_source'] ?? '',
                'utm_campaign' => $data['utm_campaign'] ?? ''
            ],
            'd' => date('c'),
            'name' => 'Formulário de Cotação RPA'
        ];
        
        // Call webhooks
        $webhook_results = [];
        $webhook_success_count = 0;
        
        $this->logger->info('Calling EspoCRM webhook');
        $travelangels_result = $this->callWebhook('https://mdmidia.com.br/add_travelangels.php', $webhook_data);
        $webhook_results['travelangels'] = $travelangels_result;
        
        if ($travelangels_result['success']) {
            $webhook_success_count++;
            $this->logger->info('EspoCRM webhook successful');
        } else {
            $this->logger->error('EspoCRM webhook failed', ['error' => $travelangels_result['error']]);
        }
        
        $this->logger->info('Calling Octadesk webhook');
        $octa_result = $this->callWebhook('https://mdmidia.com.br/add_webflow_octa.php', $webhook_data);
        $webhook_results['octadesk'] = $octa_result;
        
        if ($octa_result['success']) {
            $webhook_success_count++;
            $this->logger->info('Octadesk webhook successful');
        } else {
            $this->logger->error('Octadesk webhook failed', ['error' => $octa_result['error']]);
        }
        
        $webhooks_time = microtime(true) - $webhooks_start;
        
        // ========================================
        // ETAPA 3: INICIAR RPA (SÍNCRONO - AGUARDA DADOS PH3A)
        // ========================================
        $rpa_start = microtime(true);
        
        $this->logger->info('Starting RPA process');
        $rpa_result = $this->startRPAProcess($data);
        
        if ($rpa_result['success']) {
            $this->logger->info('RPA completed successfully');
        } else {
            $this->logger->error('RPA process failed', ['output' => $rpa_result['output']]);
        }
        
        $rpa_time = microtime(true) - $rpa_start;
        $total_time = microtime(true) - $start_time;
        
        // ========================================
        // LOGS E RESPOSTA
        // ========================================
        
        // Log webhook results
        $masked_cpf = substr($data['cpf'], -4);
        $log_data = [
            'session_id' => $session_id ?? 'unknown',
            'timestamp' => date('c'),
            'performance' => [
                'ph3a_time' => round($ph3a_time, 3),
                'webhooks_time' => round($webhooks_time, 3),
                'rpa_time' => round($rpa_time, 3),
                'total_time' => round($total_time, 3)
            ],
            'ph3a_result' => $ph3a_result ?? null,
            'ph3a_data' => $ph3a_data ?? null,
            'campos_ph3a_vazios' => $campos_ph3a_vazios ?? [],
            'webhook_results' => $webhook_results,
            'webhook_success_count' => $webhook_success_count,
            'rpa_result' => $rpa_result,
            'input_data' => [
                'cpf' => '***' . $masked_cpf,
                'nome' => $data['nome'],
                'placa' => $data['placa'],
                'cep' => $data['cep'],
                'email' => $data['email'],
                'gclid' => $data['gclid'] ?? ''
            ]
        ];
        
        $this->logWebhookResults($session_id ?? 'unknown', $log_data);
        
        // Criar sessão RPA
        $result = $this->sessionService->create($data);
        
        if ($result['success']) {
            $this->logger->info('RPA started successfully', [
                'session_id' => $result['session_id']
            ]);
            
            // Adicionar dados de webhooks e performance à resposta
            $result['performance'] = [
                'ph3a_time' => round($ph3a_time, 3),
                'webhooks_time' => round($webhooks_time, 3),
                'rpa_time' => round($rpa_time, 3),
                'total_time' => round($total_time, 3)
            ];
            $result['ph3a_consulted'] = !empty($campos_ph3a_vazios) && !empty($data['cpf']);
            $result['ph3a_fields_filled'] = array_diff(['sexo', 'data_nascimento', 'estado_civil'], $campos_ph3a_vazios ?? []);
            $result['webhook_results'] = $webhook_results;
            $result['webhook_success_count'] = $webhook_success_count;
            $result['rpa_result'] = $rpa_result;
            $result['execution_order'] = 'ph3a_then_webhooks_then_rpa';
        } else {
            $this->logger->error('RPA start failed', [
                'error' => $result['error'] ?? 'Unknown error'
            ]);
        }
        
        return $result;
        
    } catch (\Exception $e) {
        $this->logger->error('RPA start exception', [
            'error' => $e->getMessage(),
            'trace' => $e->getTraceAsString()
        ]);
        
        return $this->errorResponse('Erro interno: ' . $e->getMessage());
    }
}
```

#### 2.3 Adicionar Novo Código de Erro

```php
/**
 * Error response with specific error code for PH3A validation failure
 */
private function errorResponse(string $message, int $code = 400): array
{
    return [
        'success' => false,
        'error' => $message,
        'code' => $code,
        'timestamp' => date('Y-m-d H:i:s')
    ];
}
```

### FASE 3: NOVO CÓDIGO DE ERRO

#### 3.1 Código de Erro Específico
- **Código**: 9001
- **Descrição**: "Não foi possível validar o CPF"
- **Condição**: PH3A falha + campos obrigatórios vazios
- **Ação**: Retornar erro e parar execução

#### 3.2 Implementação do Código de Erro
```php
// Verificar se PH3A falhou e campos obrigatórios estão vazios
$campos_obrigatorios_vazios = array_intersect($campos_ph3a_vazios, ['sexo', 'data_nascimento', 'estado_civil']);

if (!$ph3a_result['success'] && !empty($campos_obrigatorios_vazios)) {
    $this->logger->error('PH3A failed and required fields empty', [
        'required_fields' => $campos_obrigatorios_vazios,
        'ph3a_error' => $ph3a_result['error']
    ]);
    
    return $this->errorResponse('Não foi possível validar o CPF', 9001);
}
```

### FASE 4: TESTES E VALIDAÇÃO

#### 4.1 Testes Unitários
- Testar chamada PH3A com timeout de 60 segundos
- Testar validação de campos obrigatórios
- Testar código de erro 9001
- Testar webhooks com dados completos
- Testar RPA síncrono

#### 4.2 Testes de Integração
- Testar fluxo completo: PH3A → Webhooks → RPA
- Testar cenário de falha PH3A com campos vazios
- Testar logs de performance
- Testar tratamento de erros

#### 4.3 Testes de Performance
- Medir tempo de execução de cada etapa
- Verificar se webhooks são chamados primeiro
- Verificar se RPA aguarda dados PH3A

### FASE 5: DEPLOY E MONITORAMENTO

#### 5.1 Deploy
```bash
# 1. Backup do arquivo atual
cp /opt/imediatoseguros-rpa-v4/src/Controllers/RPAController.php /opt/imediatoseguros-rpa-v4/src/Controllers/RPAController.php.backup.$(date +%Y%m%d_%H%M%S)

# 2. Aplicar modificações
# (usar editor ou scp para aplicar as mudanças)

# 3. Verificar sintaxe
php -l /opt/imediatoseguros-rpa-v4/src/Controllers/RPAController.php

# 4. Reiniciar serviços se necessário
systemctl reload nginx
```

#### 5.2 Monitoramento
- Verificar logs de webhooks
- Verificar performance metrics
- Verificar se EspoCRM está sendo atualizado
- Verificar se Octadesk está enviando mensagens
- Verificar código de erro 9001

---

## ⚠️ RISCOS E MITIGAÇÕES

### Riscos Identificados

| Risco | Probabilidade | Impacto | Mitigação |
|-------|---------------|---------|-----------|
| **Quebra da arquitetura OO** | Baixa | Alto | Manter estrutura existente |
| **Perda de funcionalidades** | Média | Alto | Backup completo antes da migração |
| **Problemas de performance** | Baixa | Médio | Manter timeouts configurados |
| **Falha nos webhooks** | Média | Médio | Logs detalhados e tratamento de erro |
| **Problemas de sessão** | Baixa | Alto | Usar SessionService existente |
| **Timeout PH3A** | Média | Médio | Timeout otimizado para 5s |
| **Campos obrigatórios vazios** | Média | Alto | Validação obrigatória implementada |

### Mitigações Implementadas

1. **Backup Completo**: Backup do arquivo antes de qualquer modificação
2. **Testes Incrementais**: Testar cada funcionalidade separadamente
3. **Logs Detalhados**: Manter logs para debugging
4. **Tratamento de Erro**: Try-catch em todas as operações críticas
5. **Rollback Plan**: Plano de rollback em caso de problemas
6. **Timeout Otimizado**: PH3A com 5 segundos
7. **Validação Obrigatória**: Campos obrigatórios validados
8. **Código de Erro Específico**: 9001 para falha na validação do CPF

---

## 📊 CRONOGRAMA

| Fase | Duração | Atividades |
|------|---------|------------|
| **Fase 1** | 30 min | Backup e análise de dependências |
| **Fase 2** | 3 horas | Implementação das funcionalidades |
| **Fase 3** | 30 min | Implementação do código de erro 9001 |
| **Fase 4** | 1 hora | Testes e validação |
| **Fase 5** | 30 min | Deploy e monitoramento |
| **Total** | **5 horas** | **Migração completa** |

---

## ✅ CHECKLIST DE IMPLEMENTAÇÃO

### Pré-Implementação
- [ ] Backup do `RPAController.php` atual
- [ ] Análise de dependências existentes
- [ ] Verificação de configurações necessárias

### Implementação
- [ ] Adicionar método `callPH3AApi()` com timeout de 60s
- [ ] Adicionar método `callWebhook()`
- [ ] Adicionar método `startRPAProcess()` síncrono
- [ ] Adicionar método `logWebhookResults()`
- [ ] Adicionar método `validatePH3AFields()`
- [ ] Modificar método `startRPA()` com nova lógica
- [ ] Implementar código de erro 9001
- [ ] Manter rate limiting existente
- [ ] Manter validação existente

### Pós-Implementação
- [ ] Testes unitários
- [ ] Testes de integração
- [ ] Testes de performance
- [ ] Deploy em produção
- [ ] Monitoramento de logs
- [ ] Verificação de webhooks
- [ ] Verificação de EspoCRM
- [ ] Verificação de Octadesk
- [ ] Verificação do código de erro 9001

---

## 🎯 RESULTADO ESPERADO

Após a implementação, o `RPAController.php` terá:

1. **✅ PH3A API**: Consulta automática para campos vazios (timeout 5s)
2. **✅ Validação Obrigatória**: Campos obrigatórios validados
3. **✅ Código de Erro 9001**: "Não foi possível validar o CPF"
4. **✅ Webhooks EspoCRM**: Criação de leads automaticamente
5. **✅ Webhooks Octadesk**: Envio de mensagens WhatsApp
6. **✅ RPA Síncrono**: Execução completa aguardando dados PH3A
7. **✅ Performance Metrics**: Medição de tempo por etapa
8. **✅ Logs Detalhados**: Logs para debugging e monitoramento
9. **✅ Rate Limiting**: Proteção contra abuso (mantido)
10. **✅ Validação Avançada**: Validação robusta (mantida)
11. **✅ Arquitetura OO**: Estrutura orientada a objetos (mantida)

**Fluxo Final**: PH3A (5s) → Webhooks → RPA (síncrono) → Resposta com dados completos

---

## 📝 NOTAS IMPORTANTES

1. **Ordem de Execução**: PH3A primeiro, webhooks segundo, RPA síncrono por último
2. **Performance**: PH3A com timeout de 5 segundos
3. **Validação**: Campos obrigatórios validados obrigatoriamente
4. **Erros**: Código 9001 para falha na validação do CPF
5. **Logs**: Todos os logs devem mascarar dados sensíveis (CPF)
6. **Compatibilidade**: Manter compatibilidade com código existente

---

**Data de Criação**: 2025-10-09  
**Versão**: 6.9.1  
**Status**: Pronto para Implementação  
**Autor**: Assistente IA  
**Revisão**: Baseada nas discussões técnicas sobre PH3A, timeouts e validação
