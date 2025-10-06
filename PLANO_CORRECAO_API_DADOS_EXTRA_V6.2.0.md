# 📋 **PLANO DETALHADO PARA CORREÇÃO DA API - DADOS_EXTRA**

## 🎯 **OBJETIVO**
Corrigir a função `processarHistoricoArray` para coletar e preservar corretamente os `dados_extra` da entrada "estimativas" sem prejudicar outras funcionalidades.

---

## 🔍 **ANÁLISE DO PROBLEMA ATUAL**

### **CÓDIGO PROBLEMÁTICO** (Linhas 239-241):
```php
if ($entry['dados_extra']) {
    $dados_extra = array_merge($dados_extra, $entry['dados_extra']);
}
```

### **PROBLEMAS IDENTIFICADOS**:
1. **`array_merge`** sobrescreve chaves numéricas
2. **Não preserva estrutura** `estimativas_tela_5`
3. **Perde dados específicos** das estimativas

### **EVIDÊNCIA DO PROBLEMA**:
- ✅ **Arquivo de histórico** contém dados em `etapa: "estimativas"`
- ❌ **API retorna** `dados_extra: null`
- ❌ **JavaScript não recebe** os dados de estimativa

---

## 📋 **PLANO DE CORREÇÃO**

### **FASE 1: ANÁLISE E BACKUP**
1. **Fazer backup** do arquivo atual:
   ```bash
   cp /var/www/rpaimediatoseguros.com.br/get_progress.php /var/www/rpaimediatoseguros.com.br/get_progress.php.backup.$(date +%Y%m%d_%H%M%S)
   ```

2. **Documentar** todas as funcionalidades atuais que dependem de `dados_extra`

3. **Identificar** todas as entradas do histórico que usam `dados_extra`

### **FASE 2: CORREÇÃO CIRÚRGICA**

#### **2.1 Modificar função `processarHistoricoArray`**:
```php
// ANTES (problemático):
if ($entry['dados_extra']) {
    $dados_extra = array_merge($dados_extra, $entry['dados_extra']);
}

// DEPOIS (corrigido):
if ($entry['dados_extra']) {
    // Preservar estrutura específica para estimativas
    if ($entry['etapa'] === 'estimativas') {
        $dados_extra['estimativas_tela_5'] = $entry['dados_extra'];
    }
    
    // Preservar estrutura específica para resultados finais
    if ($entry['etapa'] === 'final') {
        $dados_extra['plano_recomendado'] = $entry['dados_extra']['plano_recomendado'] ?? null;
        $dados_extra['plano_alternativo'] = $entry['dados_extra']['plano_alternativo'] ?? null;
    }
    
    // Para outras entradas, usar merge seguro
    if ($entry['etapa'] !== 'estimativas' && $entry['etapa'] !== 'final') {
        $dados_extra = array_merge_recursive($dados_extra, $entry['dados_extra']);
    }
}
```

#### **2.2 Adicionar função auxiliar para merge seguro**:
```php
function mergeDadosExtraSeguro($dados_extra, $novos_dados, $etapa) {
    switch ($etapa) {
        case 'estimativas':
            $dados_extra['estimativas_tela_5'] = $novos_dados;
            break;
        case 'final':
            if (isset($novos_dados['plano_recomendado'])) {
                $dados_extra['plano_recomendado'] = $novos_dados['plano_recomendado'];
            }
            if (isset($novos_dados['plano_alternativo'])) {
                $dados_extra['plano_alternativo'] = $novos_dados['plano_alternativo'];
            }
            break;
        default:
            $dados_extra = array_merge_recursive($dados_extra, $novos_dados);
    }
    return $dados_extra;
}
```

### **FASE 3: VALIDAÇÃO E TESTES**

#### **3.1 Testes de Regressão**:
1. **Testar sessões antigas** com histórico existente
2. **Testar sessões novas** em andamento
3. **Testar diferentes tipos** de dados_extra
4. **Verificar compatibilidade** com JavaScript atual

#### **3.2 Testes Específicos**:
```php
// Teste 1: Verificar se estimativas são preservadas
$test_data = [
    'etapa' => 'estimativas',
    'dados_extra' => ['coberturas_detalhadas' => [...]]
];
$result = processarHistoricoArray([$test_data], []);
assert(isset($result['dados_extra']['estimativas_tela_5']));

// Teste 2: Verificar se resultados finais são preservados
$test_data = [
    'etapa' => 'final',
    'dados_extra' => ['plano_recomendado' => [...], 'plano_alternativo' => [...]]
];
$result = processarHistoricoArray([$test_data], []);
assert(isset($result['dados_extra']['plano_recomendado']));
assert(isset($result['dados_extra']['plano_alternativo']));
```

### **FASE 4: IMPLEMENTAÇÃO GRADUAL**

#### **4.1 Implementação em Ambiente de Teste**:
1. **Criar cópia** da API para testes
2. **Aplicar correção** na cópia
3. **Testar com dados reais** de sessões anteriores
4. **Validar** todas as funcionalidades

#### **4.2 Implementação em Produção**:
1. **Manter backup** do arquivo original
2. **Aplicar correção** durante horário de baixo tráfego
3. **Monitorar logs** para detectar problemas
4. **Ter plano de rollback** pronto

### **FASE 5: MONITORAMENTO**

#### **5.1 Métricas de Sucesso**:
- ✅ **Estimativas aparecem** no JavaScript após fase 5
- ✅ **Dados_extra não é null** nas respostas da API
- ✅ **Estrutura preservada** `estimativas_tela_5`
- ✅ **Outras funcionalidades** continuam funcionando

#### **5.2 Logs de Monitoramento**:
```php
// Adicionar logs para debug
error_log("DEBUG: Processando dados_extra para etapa: " . $entry['etapa']);
error_log("DEBUG: dados_extra antes: " . json_encode($dados_extra));
error_log("DEBUG: dados_extra depois: " . json_encode($dados_extra));
```

---

## ⚠️ **RISCOS E MITIGAÇÕES**

### **RISCOS IDENTIFICADOS**:
1. **Quebra de funcionalidades** existentes
2. **Perda de dados** de outras entradas
3. **Incompatibilidade** com JavaScript atual

### **MITIGAÇÕES**:
1. **Backup completo** antes de qualquer alteração
2. **Testes extensivos** em ambiente isolado
3. **Implementação gradual** com rollback rápido
4. **Monitoramento contínuo** após implementação

---

## 📅 **CRONOGRAMA DE IMPLEMENTAÇÃO**

### **DIA 1**: Análise e Backup
- Backup do arquivo atual
- Documentação das funcionalidades
- Análise detalhada do código

### **DIA 2**: Desenvolvimento e Testes
- Implementação da correção
- Testes unitários
- Testes de integração

### **DIA 3**: Validação e Deploy
- Testes em ambiente de produção
- Implementação gradual
- Monitoramento inicial

---

## ✅ **CRITÉRIOS DE SUCESSO**

1. **Estimativas aparecem** no modal após fase 5
2. **API retorna** `dados_extra` com estrutura correta
3. **Todas as funcionalidades** existentes continuam funcionando
4. **Performance** não é impactada
5. **Logs** não mostram erros relacionados

---

## 🔄 **PLANO DE ROLLBACK**

### **Se algo der errado**:
1. **Restaurar backup** imediatamente
2. **Verificar logs** para identificar problema
3. **Corrigir** em ambiente de teste
4. **Re-implementar** após correção

---

## 📊 **VALIDAÇÃO TÉCNICA**

### **ANTES DA CORREÇÃO**:
```json
{
  "dados_extra": null,
  "estimativas": {
    "capturadas": false,
    "dados": null
  }
}
```

### **APÓS A CORREÇÃO**:
```json
{
  "dados_extra": {
    "estimativas_tela_5": {
      "coberturas_detalhadas": [...],
      "timestamp": "2025-10-04T18:56:21.875503"
    }
  },
  "estimativas": {
    "capturadas": true,
    "dados": {...}
  }
}
```

---

## 🎯 **RESULTADO ESPERADO**

### **PARA O USUÁRIO**:
- ✅ **Estimativa inicial** aparece no modal após fase 5
- ✅ **Experiência melhorada** com feedback visual
- ✅ **Transparência** no processo de cotação

### **PARA O SISTEMA**:
- ✅ **API funcional** retornando dados corretos
- ✅ **JavaScript compatível** com estrutura de dados
- ✅ **Sistema robusto** sem quebras de funcionalidade

---

## 📝 **NOTAS TÉCNICAS**

### **ARQUIVOS ENVOLVIDOS**:
- `/var/www/rpaimediatoseguros.com.br/get_progress.php` (API principal)
- `js/modal-progress.js` (JavaScript já corrigido)

### **FUNÇÕES MODIFICADAS**:
- `processarHistoricoArray()` (função principal)
- `mergeDadosExtraSeguro()` (nova função auxiliar)

### **DEPENDÊNCIAS**:
- ✅ **JavaScript** já está preparado para receber os dados
- ✅ **Estrutura de dados** já está definida
- ✅ **Testes** podem ser executados imediatamente

---

## 🚀 **PRÓXIMOS PASSOS**

1. **Aprovação** do plano de correção
2. **Execução** da Fase 1 (Backup e Análise)
3. **Implementação** da correção
4. **Validação** com dados reais
5. **Deploy** em produção
6. **Monitoramento** contínuo

---

**Data de Criação**: 2025-10-04  
**Versão**: 6.2.0  
**Status**: Aguardando Aprovação  
**Prioridade**: Alta  

**Este plano garante correção segura sem prejudicar funcionalidades existentes!** 🎯


