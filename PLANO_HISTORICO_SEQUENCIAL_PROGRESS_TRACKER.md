# PLANO: HISTÓRICO SEQUENCIAL NO PROGRESS TRACKER

## **Objetivo**
Implementar gravação sequencial de todas as etapas da execução RPA em arquivos JSON por sessão, incluindo estimativas, cálculos finais e mensagens de erro/conclusão.

## **Análise Atual**

### **Estrutura Atual do ProgressTracker**
- **Arquivo:** `utils/progress_database_json.py`
- **Método:** Sobrescreve o arquivo a cada atualização
- **Localização:** `rpa_data/progress_{session_id}.json`
- **Conteúdo:** Apenas o estado atual (última etapa)

### **Estrutura Atual do JSON**
```json
{
  "etapa_atual": 5,
  "total_etapas": 5,
  "percentual": 100.0,
  "status": "success",
  "mensagem": "RPA concluído com sucesso",
  "timestamp_inicio": "2024-09-29T17:30:00",
  "timestamp_atualizacao": "2024-09-29T17:35:00",
  "dados_extra": {
    "estimativas_tela_5": {
      "coberturas_detalhadas": [...],
      "beneficios_gerais": [...],
      "valores_encontrados": 3
    }
  },
  "erros": []
}
```

## **Nova Estrutura Proposta**

### **Arquivo de Histórico Sequencial**
- **Localização:** `rpa_data/history_{session_id}.json`
- **Formato:** Array de objetos, um para cada etapa
- **Conteúdo:** Histórico completo da execução

### **Estrutura do Histórico**
```json
{
  "session_id": "teste_001",
  "timestamp_inicio": "2024-09-29T17:30:00",
  "timestamp_fim": "2024-09-29T17:35:00",
  "status_final": "success",
  "total_etapas": 5,
  "historico": [
    {
      "etapa": 1,
      "timestamp": "2024-09-29T17:30:15",
      "status": "in_progress",
      "mensagem": "Iniciando tela 1 - Dados do veículo",
      "dados_extra": null,
      "erro": null
    },
    {
      "etapa": 1,
      "timestamp": "2024-09-29T17:30:45",
      "status": "completed",
      "mensagem": "Tela 1 concluída com sucesso",
      "dados_extra": {
        "dados_veiculo": {
          "placa": "ABC1234",
          "marca": "Toyota",
          "modelo": "Corolla"
        }
      },
      "erro": null
    },
    {
      "etapa": 2,
      "timestamp": "2024-09-29T17:31:00",
      "status": "in_progress",
      "mensagem": "Iniciando tela 2 - Dados do condutor",
      "dados_extra": null,
      "erro": null
    },
    {
      "etapa": 5,
      "timestamp": "2024-09-29T17:35:00",
      "status": "completed",
      "mensagem": "Estimativas capturadas com sucesso",
      "dados_extra": {
        "estimativas_tela_5": {
          "coberturas_detalhadas": [
            {
              "nome_cobertura": "Cobertura Total",
              "valores": {"de": "R$ 1.200,00", "ate": "R$ 1.800,00"},
              "beneficios": ["Proteção total", "Assistência 24h"]
            }
          ],
          "beneficios_gerais": ["Assistência 24h", "Carro reserva"],
          "valores_encontrados": 3
        }
      },
      "erro": null
    },
    {
      "etapa": "final",
      "timestamp": "2024-09-29T17:35:30",
      "status": "success",
      "mensagem": "RPA concluído com sucesso",
      "dados_extra": {
        "resultado_final": {
          "total_coberturas": 3,
          "melhor_opcao": "Cobertura Total",
          "valor_recomendado": "R$ 1.500,00"
        }
      },
      "erro": null
    }
  ]
}
```

## **Plano de Implementação**

### **Fase 1: Análise e Preparação (1 dia)**

#### **1.1 Backup e Versionamento**
- [ ] Criar backup dos arquivos atuais
- [ ] Documentar estrutura atual
- [ ] Criar branch para desenvolvimento

#### **1.2 Análise de Impacto**
- [ ] Identificar todos os pontos de uso do ProgressTracker
- [ ] Mapear dependências do PHP `get_progress.php`
- [ ] Verificar compatibilidade com Redis (quando disponível)

### **Fase 2: Modificação do ProgressTracker (2 dias)**

#### **2.1 Criação da Classe HistoryTracker**
- [ ] Criar `utils/progress_history.py`
- [ ] Implementar gravação sequencial
- [ ] Manter compatibilidade com interface atual

#### **2.2 Modificação do DatabaseProgressTracker**
- [ ] Adicionar gravação de histórico
- [ ] Manter arquivo de progresso atual (compatibilidade)
- [ ] Implementar rotação de logs (opcional)

#### **2.3 Modificação do RedisProgressTracker**
- [ ] Adicionar gravação de histórico em Redis
- [ ] Manter compatibilidade com fallback JSON
- [ ] Implementar TTL para histórico

### **Fase 3: Integração e Testes (2 dias)**

#### **3.1 Modificação do ProgressTracker Principal**
- [ ] Atualizar `utils/progress_realtime.py`
- [ ] Adicionar parâmetro para habilitar histórico
- [ ] Manter retrocompatibilidade

#### **3.2 Testes Unitários**
- [ ] Testar gravação sequencial
- [ ] Testar captura de estimativas
- [ ] Testar tratamento de erros
- [ ] Testar performance

#### **3.3 Testes de Integração**
- [ ] Testar com RPA modular (1-5)
- [ ] Testar com RPA completo (1-15)
- [ ] Testar com PHP `get_progress.php`
- [ ] Testar concorrência

### **Fase 4: Otimização e Documentação (1 dia)**

#### **4.1 Otimizações**
- [ ] Implementar compressão de histórico (opcional)
- [ ] Adicionar limpeza automática de arquivos antigos
- [ ] Otimizar performance de escrita

#### **4.2 Documentação**
- [ ] Documentar nova estrutura
- [ ] Criar exemplos de uso
- [ ] Atualizar README

## **Detalhes Técnicos**

### **Estrutura de Arquivos**
```
rpa_data/
├── progress_{session_id}.json          # Estado atual (compatibilidade)
├── history_{session_id}.json           # Histórico sequencial
├── result_{session_id}.json            # Resultado final
└── session_{session_id}.json           # Dados da sessão
```

### **Métodos a Implementar**

#### **DatabaseProgressTracker**
```python
def _adicionar_entrada_historico(self, etapa, status, mensagem, dados_extra=None, erro=None):
    """Adiciona entrada ao histórico sequencial"""
    
def _salvar_historico_arquivo(self):
    """Salva histórico em arquivo JSON"""
    
def get_historico(self):
    """Retorna histórico completo da sessão"""
    
def limpar_historico_antigo(self, dias=7):
    """Remove históricos antigos"""
```

#### **RedisProgressTracker**
```python
def _adicionar_entrada_historico_redis(self, etapa, status, mensagem, dados_extra=None, erro=None):
    """Adiciona entrada ao histórico no Redis"""
    
def _salvar_historico_redis(self):
    """Salva histórico no Redis"""
    
def get_historico_redis(self):
    """Retorna histórico do Redis"""
```

### **Configurações**
```python
# Configurações do histórico
HISTORICO_HABILITADO = True
HISTORICO_MAX_ENTRADAS = 1000
HISTORICO_RETENCAO_DIAS = 7
HISTORICO_COMPRESSÃO = False
```

## **Cronograma**

### **Semana 1**
- **Dia 1:** Fase 1 - Análise e Preparação
- **Dia 2-3:** Fase 2 - Modificação do ProgressTracker
- **Dia 4-5:** Fase 3 - Integração e Testes

### **Semana 2**
- **Dia 1:** Fase 4 - Otimização e Documentação
- **Dia 2:** Testes finais e deploy
- **Dia 3:** Monitoramento e ajustes

## **Riscos e Mitigações**

### **Risco 1: Incompatibilidade com PHP**
- **Mitigação:** Manter arquivo de progresso atual
- **Teste:** Validar `get_progress.php` após mudanças

### **Risco 2: Performance**
- **Mitigação:** Implementar gravação assíncrona
- **Teste:** Medir impacto em execuções longas

### **Risco 3: Espaço em disco**
- **Mitigação:** Implementar limpeza automática
- **Teste:** Monitorar uso de espaço

### **Risco 4: Concorrência**
- **Mitigação:** Usar locks de arquivo
- **Teste:** Executar múltiplas sessões simultâneas

## **Critérios de Sucesso**

### **Funcionais**
- [ ] Histórico sequencial completo
- [ ] Estimativas capturadas corretamente
- [ ] Erros registrados adequadamente
- [ ] Compatibilidade com PHP mantida

### **Não Funcionais**
- [ ] Performance < 5% de impacto
- [ ] Uso de disco < 100MB por sessão
- [ ] Tempo de resposta < 100ms
- [ ] 99.9% de disponibilidade

## **Próximos Passos**

1. **Aprovação do plano**
2. **Criação do branch de desenvolvimento**
3. **Implementação da Fase 1**
4. **Testes incrementais**
5. **Deploy em ambiente de teste**
6. **Validação com usuário**
7. **Deploy em produção**

---

**Data:** 29/09/2024  
**Versão:** 1.0  
**Autor:** Sistema RPA  
**Status:** Aguardando aprovação



























