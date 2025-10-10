# 🔄 FLUXO PH3A + WEBHOOKS PRIMEIRO V6.9.0

## 📊 **DIAGRAMA DO FLUXO ATUALIZADO**

```
┌─────────────────────────────────────────────────────────────────┐
│                    WEBFLOW (Frontend)                          │
│  segurosimediato.com.br                                         │
│  - Formulário de cotação                                        │
│  - JavaScript captura GCLID/UTM                                 │
│  - Modal de progresso                                            │
└─────────────────────┬───────────────────────────────────────────┘
                      │ HTTP/HTTPS POST
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                    API RPA V6.9.0                              │
│  rpaimediatoseguros.com.br/api/rpa/start                        │
│                                                                 │
│  🔍 ETAPA 1: CONSULTA PH3A (0-3 segundos)                      │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ 1. Validar dados do formulário                          │   │
│  │ 2. Verificar campos PH3A em branco                      │   │
│  │ 3. Consultar API PH3A (SEXO, DATA, ESTADO-CIVIL)       │   │
│  │ 4. Preencher campos automaticamente                     │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  🚀 ETAPA 2: WEBHOOKS PRIMEIRO (3-5 segundos)                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ 5. Preparar dados completos para webhooks              │   │
│  │ 6. Chamar add_travelangels.php (EspoCRM)               │   │
│  │ 7. Chamar add_webflow_octa.php (Octadesk)              │   │
│  │ 8. Logar resultados dos webhooks                       │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  🤖 ETAPA 3: RPA EM BACKGROUND (5-75 segundos)                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ 9. Iniciar executar_rpa_imediato_playwright.py          │   │
│  │ 10. Processar 15 telas de cotação                       │   │
│  │ 11. Capturar dados dos planos                           │   │
│  │ 12. Salvar resultados em JSON                          │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────┬───────────────────────────────────────────┘
                      │ JSON Response
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                    WEBFLOW (Frontend)                          │
│  - Modal atualizado com progresso                              │
│  - Resultados finais exibidos                                  │
└─────────────────────────────────────────────────────────────────┘
```

## 🎯 **VANTAGENS DA NOVA ORDEM**

### **🔍 DADOS COMPLETOS**
- **PH3A**: Preenche SEXO, DATA-DE-NASCIMENTO, ESTADO-CIVIL automaticamente
- **Campos completos**: Lead com informações completas no CRM
- **Menos erros**: Dados validados e preenchidos automaticamente

### **⚡ RESPOSTA IMEDIATA**
- **WhatsApp**: Cliente recebe mensagem em <5 segundos
- **EspoCRM**: Lead criado instantaneamente
- **Feedback**: Usuário vê confirmação imediata

### **🛡️ PROTEÇÃO DE DADOS**
- **Lead salvo**: Mesmo se RPA falhar, lead já está no CRM
- **WhatsApp enviado**: Cliente já foi contatado
- **Dados protegidos**: Informações não se perdem

### **📈 MÉTRICAS PRECISAS**
- **Conversão registrada**: Imediatamente após envio do formulário
- **GCLID capturado**: Para rastreamento de campanhas
- **UTM parameters**: Para análise de origem do tráfego

## 🔄 **COMPARAÇÃO: ANTES vs DEPOIS**

### **❌ FLUXO ANTERIOR (PH3A desabilitado + Webhooks depois)**
```
1. Usuário preenche formulário
2. PH3A desabilitado (campos em branco)
3. RPA processa (70 segundos)
4. Webhooks chamados (2 segundos)
5. Cliente recebe WhatsApp (72 segundos total)
6. Lead criado no CRM (72 segundos total)
```

### **✅ FLUXO NOVO (PH3A + Webhooks primeiro)**
```
1. Usuário preenche formulário
2. PH3A consulta campos (3 segundos)
3. Webhooks chamados (2 segundos)
4. Cliente recebe WhatsApp (5 segundos)
5. Lead criado no CRM (5 segundos)
6. RPA processa em background (70 segundos)
7. Resultados exibidos (75 segundos total)
```

## 📊 **IMPACTO NA EXPERIÊNCIA DO USUÁRIO**

### **ANTES**
- ⏳ **72 segundos** para receber WhatsApp
- 😰 **Ansiedade** do usuário aguardando
- 📉 **Abandono** potencial durante espera
- ❌ **Perda de leads** se RPA falhar
- 📋 **Campos incompletos** (PH3A desabilitado)

### **DEPOIS**
- ⚡ **5 segundos** para receber WhatsApp
- 😊 **Confiança** do usuário imediata
- 📈 **Maior conversão** por feedback rápido
- ✅ **Leads protegidos** independente do RPA
- 🔍 **Dados completos** (PH3A ativo)

## 🚀 **IMPLEMENTAÇÃO TÉCNICA**

### **Código PHP Atualizado (com medições de tempo)**
```php
// ETAPA 1: CONSULTA PH3A (SE NECESSÁRIO)
$start_time = microtime(true);
echo "🔍 ETAPA 1: VERIFICANDO CAMPOS PH3A\n";

// Verificar campos PH3A em branco
$campos_ph3a_vazios = [];
if (empty($data['sexo'])) $campos_ph3a_vazios[] = 'sexo';
if (empty($data['data_nascimento'])) $campos_ph3a_vazios[] = 'data_nascimento';
if (empty($data['estado_civil'])) $campos_ph3a_vazios[] = 'estado_civil';

if (!empty($campos_ph3a_vazios) && !empty($data['cpf'])) {
    // Consultar API PH3A
    $ph3a_result = callPH3AApi($data['cpf']);
    if ($ph3a_result['success']) {
        // Preencher campos automaticamente
        if (empty($data['sexo']) && isset($ph3a_data['sexo'])) {
            $data['sexo'] = ($ph3a_data['sexo'] == 1) ? 'Masculino' : 'Feminino';
        }
        // ... outros campos
    }
}

$ph3a_time = microtime(true) - $start_time;
echo "⏱️ Tempo PH3A: " . round($ph3a_time, 3) . "s\n";

// ETAPA 2: WEBHOOKS PRIMEIRO
$webhooks_start = microtime(true);
echo "\n🚀 ETAPA 2: CHAMANDO WEBHOOKS PRIMEIRO\n";

// Chamar EspoCRM
$travelangels_result = callWebhook('https://mdmidia.com.br/add_travelangels.php', $webhook_data);
if ($travelangels_result['success']) {
    echo "✅ EspoCRM: Lead criado com sucesso\n";
}

// Chamar Octadesk
$octa_result = callWebhook('https://mdmidia.com.br/add_webflow_octa.php', $webhook_data);
if ($octa_result['success']) {
    echo "✅ Octadesk: Mensagem WhatsApp enviada\n";
}

$webhooks_time = microtime(true) - $webhooks_start;
echo "⏱️ Tempo Webhooks: " . round($webhooks_time, 3) . "s\n";

// ETAPA 3: RPA EM BACKGROUND
$rpa_start = microtime(true);
echo "\n🤖 ETAPA 3: INICIANDO RPA EM BACKGROUND\n";
$rpa_command = "cd /opt/imediatoseguros-rpa && source venv/bin/activate && python executar_rpa_imediato_playwright.py '" . json_encode($data) . "' > /dev/null 2>&1 & echo $!";
$rpa_pid = shell_exec($rpa_command);

$rpa_time = microtime(true) - $rpa_start;
echo "⏱️ Tempo RPA: " . round($rpa_time, 3) . "s\n";

$total_time = microtime(true) - $start_time;
echo "⏱️ Tempo Total: " . round($total_time, 3) . "s\n";
```

### **Resposta da API (com medições de tempo)**
```json
{
  "success": true,
  "session_id": "rpa_v6.9.0_20250110_153000_abc12345",
  "message": "PH3A consultado, webhooks executados e RPA iniciado com sucesso",
  "performance": {
    "ph3a_time": 0.245,
    "webhooks_time": 1.892,
    "rpa_time": 0.156,
    "total_time": 2.293
  },
  "ph3a_consulted": true,
  "ph3a_fields_filled": ["sexo", "data_nascimento", "estado_civil"],
  "webhook_results": {
    "travelangels": {
      "success": true,
      "http_code": 200,
      "response": "..."
    },
    "octadesk": {
      "success": true,
      "http_code": 200,
      "response": "..."
    }
  },
  "webhook_success_count": 2,
  "rpa_pid": "12345",
  "execution_order": "ph3a_then_webhooks_then_rpa",
  "timestamp": "2025-01-10T15:30:00Z"
}
```

## 📝 **LOGS DETALHADOS**

### **Estrutura do Log (com medições de tempo)**
```json
{
  "session_id": "rpa_v6.9.0_20250110_153000_abc12345",
  "timestamp": "2025-01-10T15:30:00Z",
  "performance": {
    "ph3a_time": 0.245,
    "webhooks_time": 1.892,
    "rpa_time": 0.156,
    "total_time": 2.293
  },
  "ph3a_result": {
    "success": true,
    "http_code": 200,
    "response": "...",
    "error": null
  },
  "ph3a_data": {
    "sexo": 1,
    "estado_civil": 0,
    "data_nascimento": "1990-01-01"
  },
  "campos_ph3a_vazios": [],
  "webhook_results": {
    "travelangels": {
      "success": true,
      "http_code": 200,
      "response": "...",
      "error": null
    },
    "octadesk": {
      "success": true,
      "http_code": 200,
      "response": "...",
      "error": null
    }
  },
  "webhook_success_count": 2,
  "execution_order": "ph3a_then_webhooks_then_rpa",
  "input_data": {
    "cpf": "12345678901",
    "nome": "João Silva",
    "sexo": "Masculino",
    "data_nascimento": "01/01/1990",
    "estado_civil": "Solteiro",
    "gclid": "TesteRPA123"
  }
}
```

## 🎯 **RESULTADO ESPERADO**

### **✅ BENEFÍCIOS ALCANÇADOS**
1. **🔍 Dados completos**: PH3A preenche campos automaticamente
2. **⚡ Resposta imediata**: WhatsApp em 5 segundos
3. **📊 CRM atualizado**: Lead criado instantaneamente
4. **🎯 Melhor UX**: Feedback imediato para o usuário
5. **🛡️ Dados protegidos**: Lead salvo mesmo se RPA falhar
6. **📈 Métricas precisas**: Conversão registrada imediatamente
7. **🔄 Processo paralelo**: PH3A, webhooks e RPA executam independentemente

### **📊 MÉTRICAS DE SUCESSO**
- **Taxa de sucesso PH3A**: >90%
- **Tempo de resposta PH3A**: <3 segundos
- **Tempo de resposta webhooks**: <2 segundos
- **Tempo de resposta WhatsApp**: <5 segundos
- **Taxa de sucesso dos webhooks**: >95%
- **Captura de GCLID**: 100% dos casos
- **Ordem de execução**: PH3A → Webhooks → RPA

---

**📅 Data de Criação**: 2025-01-10  
**📅 Última Revisão**: 2025-10-09  
**👤 Responsável**: Sistema RPA Imediato Seguros  
**🏷️ Versão**: V6.9.0  
**📋 Status**: Implementado - PH3A + Webhooks Primeiro (com medições de tempo)
