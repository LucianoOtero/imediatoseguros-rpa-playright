# PLANO: LÓGICA DE RESULTADOS FINAIS NO GET_PROGRESS.PHP

## **Análise da Estrutura Atual**

### **Arquivo de Resultados Finais:**
- **Localização:** `rpa_data/result_{session_id}.json`
- **Estrutura:** Dados finais do cálculo completo (1-15 telas)
- **Conteúdo:** Planos recomendados, valores, coberturas, etc.

### **Estrutura do Arquivo de Resultados:**
```json
{
  "status": "success",
  "timestamp_fim": "2025-09-29T11:50:52.267173",
  "dados_finais": {
    "plano_recomendado": {
      "plano": "Plano recomendado",
      "valor": "R$3.661,32",
      "forma_pagamento": "Crédito em até 10x sem juros!",
      "parcelamento": "anual",
      "valor_franquia": "R$ 4.989,65",
      "valor_mercado": "100% da tabela FIPE",
      "assistencia": true,
      "vidros": true,
      "carro_reserva": true,
      "danos_materiais": "R$ 100.000,00",
      "danos_corporais": "R$ 100.000,00",
      "danos_morais": "R$ 10.000,00",
      "morte_invalidez": "R$ 5.000,00",
      "tipo_franquia": "Reduzida"
    },
    "plano_alternativo": {
      "plano": "Plano alternativo",
      "valor": "R$4.059,15",
      "forma_pagamento": "Crédito em até 10x sem juros!",
      "parcelamento": "anual",
      "valor_franquia": "R$ 5.239,13",
      "valor_mercado": "100% da tabela FIPE",
      "assistencia": true,
      "vidros": true,
      "carro_reserva": true,
      "danos_materiais": "R$ 100.000,00",
      "danos_corporais": "R$ 100.000,00",
      "danos_morais": "R$ 10.000,00",
      "morte_invalidez": "R$ 5.000,00",
      "tipo_franquia": "Reduzida"
    }
  },
  "session_id": "teste_principal_001"
}
```

### **Histórico Sequencial:**
- **Entrada "final":** Última entrada do histórico
- **Status:** "success" indica RPA concluído com sucesso
- **Dados extras:** Podem conter resultados finais

## **Plano de Implementação**

### **Objetivo:**
Implementar lógica no `get_progress.php` para:
1. **Detectar se o RPA foi finalizado** (entrada "final" com status "success")
2. **Buscar resultados finais** do arquivo `result_{session_id}.json`
3. **Extrair dados dos planos** (recomendado e alternativo)
4. **Retornar resultados finais** na resposta da API

### **Estratégia:**
1. **Verificar entrada "final"** no histórico
2. **Confirmar status "success"** na finalização
3. **Ler arquivo de resultados** se disponível
4. **Processar dados dos planos** e coberturas
5. **Incluir resultados na resposta** da API

## **Implementação Detalhada**

### **Fase 1: Função de Detecção de Resultados Finais (1 dia)**

#### **1.1 Função Principal**
```php
function detectarResultadosFinais($historico) {
    $final_entry = null;
    $rpa_finalizado = false;
    $status_final = 'running';
    
    // Buscar entrada "final"
    foreach ($historico as $entry) {
        if ($entry['etapa'] === 'final') {
            $final_entry = $entry;
            $status_final = $entry['status'];
            $rpa_finalizado = ($entry['status'] === 'success');
            break;
        }
    }
    
    return [
        'rpa_finalizado' => $rpa_finalizado,
        'status_final' => $status_final,
        'final_entry' => $final_entry,
        'timestamp_fim' => $final_entry['timestamp'] ?? null
    ];
}
```

#### **1.2 Função de Leitura de Resultados**
```php
function lerResultadosFinais($session_id) {
    $result_file = "/opt/imediatoseguros-rpa/rpa_data/result_{$session_id}.json";
    
    if (!file_exists($result_file)) {
        return null;
    }
    
    try {
        $content = file_get_contents($result_file);
        $data = json_decode($content, true);
        
        if (!$data) {
            return null;
        }
        
        return $data;
    } catch (Exception $e) {
        return null;
    }
}
```

#### **1.3 Função de Processamento de Planos**
```php
function processarPlanos($dados_finais) {
    if (!$dados_finais || !isset($dados_finais['dados_finais'])) {
        return null;
    }
    
    $dados = $dados_finais['dados_finais'];
    $planos = [];
    
    // Processar plano recomendado
    if (isset($dados['plano_recomendado'])) {
        $planos['recomendado'] = processarPlano($dados['plano_recomendado'], 'recomendado');
    }
    
    // Processar plano alternativo
    if (isset($dados['plano_alternativo'])) {
        $planos['alternativo'] = processarPlano($dados['plano_alternativo'], 'alternativo');
    }
    
    return $planos;
}

function processarPlano($plano_data, $tipo) {
    return [
        'tipo' => $tipo,
        'nome' => $plano_data['plano'] ?? 'N/A',
        'valor' => $plano_data['valor'] ?? 'N/A',
        'forma_pagamento' => $plano_data['forma_pagamento'] ?? 'N/A',
        'parcelamento' => $plano_data['parcelamento'] ?? 'N/A',
        'valor_franquia' => $plano_data['valor_franquia'] ?? 'N/A',
        'valor_mercado' => $plano_data['valor_mercado'] ?? 'N/A',
        'coberturas' => [
            'assistencia' => $plano_data['assistencia'] ?? false,
            'vidros' => $plano_data['vidros'] ?? false,
            'carro_reserva' => $plano_data['carro_reserva'] ?? false
        ],
        'limites' => [
            'danos_materiais' => $plano_data['danos_materiais'] ?? 'N/A',
            'danos_corporais' => $plano_data['danos_corporais'] ?? 'N/A',
            'danos_morais' => $plano_data['danos_morais'] ?? 'N/A',
            'morte_invalidez' => $plano_data['morte_invalidez'] ?? 'N/A'
        ],
        'franquia' => [
            'tipo' => $plano_data['tipo_franquia'] ?? 'N/A'
        ]
    ];
}
```

### **Fase 2: Integração com get_progress.php (1 dia)**

#### **2.1 Modificação da Resposta**
```php
// No processamento do histórico
$resultados_info = detectarResultadosFinais($historico);

// Adicionar à resposta
$response['data']['resultados_finais'] = [
    'rpa_finalizado' => $resultados_info['rpa_finalizado'],
    'status_final' => $resultados_info['status_final'],
    'timestamp_fim' => $resultados_info['timestamp_fim'],
    'dados' => $resultados_info['rpa_finalizado'] 
        ? processarPlanos(lerResultadosFinais($session_id))
        : null,
    'arquivo_resultado' => $resultados_info['rpa_finalizado'] 
        ? "result_{$session_id}.json"
        : null
];
```

#### **2.2 Estrutura da Nova Resposta**
```json
{
  "success": true,
  "data": {
    "etapa_atual": 15,
    "status": "success",
    "mensagem": "RPA success",
    
    "resultados_finais": {
      "rpa_finalizado": true,
      "status_final": "success",
      "timestamp_fim": "2025-09-29T11:50:52.267173",
      "dados": {
        "recomendado": {
          "tipo": "recomendado",
          "nome": "Plano recomendado",
          "valor": "R$3.661,32",
          "forma_pagamento": "Crédito em até 10x sem juros!",
          "parcelamento": "anual",
          "valor_franquia": "R$ 4.989,65",
          "valor_mercado": "100% da tabela FIPE",
          "coberturas": {
            "assistencia": true,
            "vidros": true,
            "carro_reserva": true
          },
          "limites": {
            "danos_materiais": "R$ 100.000,00",
            "danos_corporais": "R$ 100.000,00",
            "danos_morais": "R$ 10.000,00",
            "morte_invalidez": "R$ 5.000,00"
          },
          "franquia": {
            "tipo": "Reduzida"
          }
        },
        "alternativo": {
          "tipo": "alternativo",
          "nome": "Plano alternativo",
          "valor": "R$4.059,15",
          "forma_pagamento": "Crédito em até 10x sem juros!",
          "parcelamento": "anual",
          "valor_franquia": "R$ 5.239,13",
          "valor_mercado": "100% da tabela FIPE",
          "coberturas": {
            "assistencia": true,
            "vidros": true,
            "carro_reserva": true
          },
          "limites": {
            "danos_materiais": "R$ 100.000,00",
            "danos_corporais": "R$ 100.000,00",
            "danos_morais": "R$ 10.000,00",
            "morte_invalidez": "R$ 5.000,00"
          },
          "franquia": {
            "tipo": "Reduzida"
          }
        }
      },
      "arquivo_resultado": "result_teste_principal_001.json"
    },
    
    "estimativas": {...},
    "historico": [...],
    "timeline": [...]
  }
}
```

### **Fase 3: Tratamento de Casos Especiais (1 dia)**

#### **3.1 Casos de Erro**
```php
function tratarCasosResultados($resultados_info, $historico) {
    $casos = [
        'rpa_nao_finalizado' => !$resultados_info['rpa_finalizado'],
        'rpa_finalizado_com_erro' => $resultados_info['status_final'] === 'error',
        'arquivo_resultado_ausente' => $resultados_info['rpa_finalizado'] && !file_exists("result_{$session_id}.json"),
        'dados_resultado_vazios' => $resultados_info['rpa_finalizado'] && empty($dados_finais)
    ];
    
    return $casos;
}
```

#### **3.2 Mensagens de Status**
```php
function getMensagemResultados($casos) {
    if ($casos['rpa_nao_finalizado']) {
        return 'RPA ainda em execução';
    }
    
    if ($casos['rpa_finalizado_com_erro']) {
        return 'RPA finalizado com erro';
    }
    
    if ($casos['arquivo_resultado_ausente']) {
        return 'Arquivo de resultados não encontrado';
    }
    
    if ($casos['dados_resultado_vazios']) {
        return 'Dados de resultados vazios';
    }
    
    return 'Resultados finais disponíveis';
}
```

### **Fase 4: Otimizações e Validações (1 dia)**

#### **4.1 Cache de Resultados**
```php
function getCacheKeyResultados($session_id) {
    return "resultados_{$session_id}";
}

function getResultadosFromCache($session_id) {
    $cache_key = getCacheKeyResultados($session_id);
    if (apcu_exists($cache_key)) {
        return apcu_fetch($cache_key);
    }
    return null;
}

function setResultadosCache($session_id, $resultados_data) {
    $cache_key = getCacheKeyResultados($session_id);
    apcu_store($cache_key, $resultados_data, 60); // 60 segundos
}
```

#### **4.2 Validação de Dados**
```php
function validarResultados($resultados_data) {
    if (!$resultados_data) {
        return false;
    }
    
    // Validar se há pelo menos um plano
    if (!isset($resultados_data['recomendado']) && !isset($resultados_data['alternativo'])) {
        return false;
    }
    
    // Validar plano recomendado
    if (isset($resultados_data['recomendado'])) {
        $plano = $resultados_data['recomendado'];
        if (!isset($plano['valor']) || !isset($plano['nome'])) {
            return false;
        }
    }
    
    // Validar plano alternativo
    if (isset($resultados_data['alternativo'])) {
        $plano = $resultados_data['alternativo'];
        if (!isset($plano['valor']) || !isset($plano['nome'])) {
            return false;
        }
    }
    
    return true;
}
```

## **Estrutura Final da Resposta**

### **Resposta com Resultados Finais:**
```json
{
  "success": true,
  "data": {
    "etapa_atual": 15,
    "status": "success",
    "mensagem": "RPA success",
    
    "resultados_finais": {
      "rpa_finalizado": true,
      "status_final": "success",
      "timestamp_fim": "2025-09-29T11:50:52.267173",
      "dados": {
        "recomendado": {
          "tipo": "recomendado",
          "nome": "Plano recomendado",
          "valor": "R$3.661,32",
          "forma_pagamento": "Crédito em até 10x sem juros!",
          "coberturas": {
            "assistencia": true,
            "vidros": true,
            "carro_reserva": true
          },
          "limites": {
            "danos_materiais": "R$ 100.000,00",
            "danos_corporais": "R$ 100.000,00"
          }
        },
        "alternativo": {
          "tipo": "alternativo",
          "nome": "Plano alternativo",
          "valor": "R$4.059,15",
          "forma_pagamento": "Crédito em até 10x sem juros!",
          "coberturas": {
            "assistencia": true,
            "vidros": true,
            "carro_reserva": true
          },
          "limites": {
            "danos_materiais": "R$ 100.000,00",
            "danos_corporais": "R$ 100.000,00"
          }
        }
      },
      "arquivo_resultado": "result_teste_principal_001.json"
    },
    
    "estimativas": {...},
    "historico": [...],
    "timeline": [...]
  }
}
```

### **Resposta sem Resultados Finais:**
```json
{
  "success": true,
  "data": {
    "etapa_atual": 5,
    "status": "executando",
    "mensagem": "Tela 5 concluída",
    
    "resultados_finais": {
      "rpa_finalizado": false,
      "status_final": "running",
      "timestamp_fim": null,
      "dados": null,
      "arquivo_resultado": null
    },
    
    "estimativas": {...},
    "historico": [...],
    "timeline": [...]
  }
}
```

## **Cronograma de Implementação**

### **Semana 1:**
- **Dia 1:** Fase 1 - Função de detecção de resultados finais
- **Dia 2:** Fase 2 - Integração com get_progress.php
- **Dia 3:** Fase 3 - Tratamento de casos especiais
- **Dia 4:** Fase 4 - Otimizações e validações
- **Dia 5:** Testes e ajustes

### **Semana 2:**
- **Dia 1:** Testes de integração
- **Dia 2:** Deploy e validação
- **Dia 3:** Monitoramento e ajustes

## **Riscos e Mitigações**

### **Risco 1: Arquivo de resultados ausente**
- **Mitigação:** Verificar existência + fallback para dados_extra do histórico
- **Teste:** Validar com sessões que não geraram resultados

### **Risco 2: Dados corrompidos**
- **Mitigação:** Validação robusta + tratamento de exceções
- **Teste:** Simular arquivos corrompidos

### **Risco 3: Performance**
- **Mitigação:** Cache de resultados + leitura otimizada
- **Teste:** Medir tempo de resposta

### **Risco 4: RPA não finalizado**
- **Mitigação:** Verificação de status + mensagens apropriadas
- **Teste:** Testar com RPA em execução

## **Critérios de Sucesso**

### **Funcionais:**
- [ ] Detecção correta de RPA finalizado
- [ ] Leitura correta do arquivo de resultados
- [ ] Processamento correto dos planos
- [ ] Resposta estruturada com resultados finais

### **Não Funcionais:**
- [ ] Tempo de resposta < 150ms
- [ ] Cache funcionando
- [ ] Validação robusta
- [ ] Compatibilidade mantida

## **Próximos Passos**

1. **Aprovação do plano**
2. **Implementação da Fase 1**
3. **Testes incrementais**
4. **Deploy em ambiente de teste**
5. **Validação com frontend**
6. **Deploy em produção**

---

**Data:** 29/09/2024  
**Versão:** 1.0  
**Autor:** Sistema RPA  
**Status:** Aguardando aprovação
















