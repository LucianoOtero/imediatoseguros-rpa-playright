# Plano de Produção - RPA V4 (Estratégia Conservadora)

## Objetivo
Implementar RPA V4 em produção utilizando estratégia conservadora com as seguintes melhorias:
1. PHP para acompanhar execução do RPA (consultando progress tracker)
2. Ajustar chamada para receber JSON ao invés de ler parametros.json
3. Migrar RPA modular para arquivo principal

## Estratégia Conservadora

### Princípios
- **Compatibilidade total** com sistema V3 existente
- **Fallback automático** para parametros.json em caso de falha
- **Dados reais obrigatórios** para testes (placa, CPF, CEP válidos)
- **Validação robusta** antes de qualquer mudança
- **Testes incrementais** com rollback imediato
- **Preservação de funcionalidades** existentes

### Dados de Teste Obrigatórios
**IMPORTANTE**: Para todos os testes da chamada do RPA modular ou arquivo principal via linha de comando, deve ser utilizado JSON idêntico ao gravado no `parametros.json`, pois:
- **Placas devem ser reais** - app.tosegurado valida placa no sistema
- **CPF deve ser válido** - sistema verifica dígitos verificadores
- **CEP deve existir** - validação de endereço é obrigatória
- **Dados pessoais devem ser consistentes** - sistema faz validações cruzadas

**Consequência**: Sem dados reais, o app.tosegurado não prossegue e os testes falham.

## Situação Atual

### V4 Implementada
- ✅ Arquitetura modular completa
- ✅ API REST funcionando
- ✅ Dashboard web responsivo
- ✅ Compatibilidade com V3 (parametros.json)
- ✅ Testes realizados com sucesso

### RPA Modular Atual
- **Arquivo**: `executar_rpa_modular_telas_1_a_5.py`
- **Status**: Funcionando com parametros.json
- **Progress Tracker**: Redis funcionando
- **Estimativas**: Capturadas corretamente

## Próximos Passos

### 1. Testar PHP para Acompanhar Execução do RPA

#### 1.1 Implementar Monitoramento em Tempo Real
**Objetivo**: Criar endpoint PHP que consulta periodicamente o progress tracker

**Arquivos a Modificar**:
- `rpa-v4/src/Services/MonitorService.php`
- `rpa-v4/src/Controllers/RPAController.php`
- `rpa-v4/public/js/dashboard.js`

**Implementação**:
```php
// Novo endpoint para progress em tempo real
GET /api/rpa/progress/{session_id}

// Resposta
{
    "success": true,
    "progress": {
        "etapa_atual": 3,
        "total_etapas": 5,
        "percentual": 60.0,
        "status": "running",
        "mensagem": "Processando tela 3",
        "estimativas": {...}
    }
}
```

#### 1.2 Dashboard em Tempo Real
**Objetivo**: Atualizar dashboard para mostrar progresso em tempo real

**Funcionalidades**:
- Polling automático a cada 2 segundos
- Barra de progresso visual
- Logs em tempo real
- Estimativas capturadas

#### 1.3 Testes de Monitoramento
**Cenários de Teste**:
- Execução completa (5 telas)
- Falha em tela intermediária
- Timeout de execução
- Recuperação de falhas

### 2. Ajustar Chamada para Receber JSON

#### 2.1 Modificar SessionService (Estratégia Conservadora)
**Arquivo**: `rpa-v4/src/Services/SessionService.php`

**Estratégia**: Manter fallback para parametros.json
```php
// Implementação conservadora com fallback
if (!empty($data) && $this->validateData($data)) {
    // Usar dados JSON dinâmicos
    $dataJson = json_encode($data, JSON_UNESCAPED_UNICODE);
    $command = "/opt/imediatoseguros-rpa/venv/bin/python executar_rpa_modular_telas_1_a_5.py --data '$dataJson' --session $SESSION_ID";
} else {
    // Fallback para parametros.json (compatibilidade V3)
    $command = "/opt/imediatoseguros-rpa/venv/bin/python executar_rpa_modular_telas_1_a_5.py --config /opt/imediatoseguros-rpa/parametros.json --session $SESSION_ID";
}
```

**Validação de Dados**:
```php
private function validateData(array $data): bool
{
    // Validar campos obrigatórios com dados reais
    $required = ['cpf', 'nome', 'placa', 'cep'];
    foreach ($required as $field) {
        if (empty($data[$field])) {
            return false;
        }
    }
    
    // Validar CPF (11 dígitos)
    if (!preg_match('/^\d{11}$/', $data['cpf'])) {
        return false;
    }
    
    // Validar placa (formato brasileiro)
    if (!preg_match('/^[A-Z]{3}\d{4}$/', $data['placa'])) {
        return false;
    }
    
    // Validar CEP (8 dígitos)
    if (!preg_match('/^\d{8}$/', $data['cep'])) {
        return false;
    }
    
    return true;
}
```

#### 2.2 Modificar Script Python (Estratégia Conservadora)
**Arquivo**: `executar_rpa_modular_telas_1_a_5.py`

**Implementação com fallback**:
```python
import argparse
import json
import sys

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', type=str, help='JSON data for RPA execution')
    parser.add_argument('--config', type=str, help='Path to parametros.json file')
    parser.add_argument('--session', type=str, help='Session ID for tracking')
    args = parser.parse_args()
    
    # Estratégia conservadora: priorizar --data, fallback para --config
    if args.data:
        try:
            data = json.loads(args.data)
            print(f"[INFO] Usando dados JSON dinâmicos para sessão {args.session}")
        except json.JSONDecodeError as e:
            print(f"[ERROR] JSON inválido: {e}")
            sys.exit(1)
    elif args.config:
        try:
            with open(args.config, 'r') as f:
                data = json.load(f)
            print(f"[INFO] Usando parametros.json para sessão {args.session}")
        except FileNotFoundError:
            print(f"[ERROR] Arquivo {args.config} não encontrado")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"[ERROR] JSON inválido em {args.config}: {e}")
            sys.exit(1)
    else:
        print("[ERROR] Deve fornecer --data ou --config")
        sys.exit(1)
    
    # Validar dados obrigatórios
    required_fields = ['cpf', 'nome', 'placa', 'cep']
    for field in required_fields:
        if field not in data or not data[field]:
            print(f"[ERROR] Campo obrigatório '{field}' não encontrado ou vazio")
            sys.exit(1)
    
    # Executar RPA com dados validados
    execute_rpa(data, args.session)

def execute_rpa(data, session_id):
    # Inicializar progress tracker
    progress_tracker = DatabaseProgressTracker(
        total_etapas=5,
        session_id=session_id
    )
    
    # Executar telas 1-5 com dados fornecidos
    for tela in range(1, 6):
        progress_tracker.update_progress(tela, f"Processando Tela {tela}")
        # ... lógica da tela ...
        
        if tela == 4:
            # Capturar estimativas
            estimativas = capturar_estimativas()
            progress_tracker.update_progress(
                tela, 
                "Estimativas capturadas",
                dados_extra={'estimativas_tela_4': estimativas}
            )
    
    progress_tracker.update_progress(5, "Execução concluída", status="success")
```

#### 2.3 Validação de Entrada
**Arquivo**: `rpa-v4/src/Services/ValidationService.php`

**Implementação**:
```php
// Reativar validação
public function validate(array $data): ValidationResult
{
    $errors = [];
    
    // Validar campos obrigatórios
    if (empty($data['cpf'])) {
        $errors[] = 'CPF é obrigatório';
    }
    
    if (empty($data['nome'])) {
        $errors[] = 'Nome é obrigatório';
    }
    
    // Validar formato CPF
    if (!preg_match('/^\d{11}$/', $data['cpf'])) {
        $errors[] = 'CPF deve conter 11 dígitos';
    }
    
    return new ValidationResult($errors);
}
```

#### 2.4 Testes de Validação (Estratégia Conservadora)
**IMPORTANTE**: Todos os testes devem usar dados reais do `parametros.json`

**Cenários de Teste**:
1. **Dados JSON válidos** (idênticos ao parametros.json)
   - CPF real com dígitos verificadores válidos
   - Placa real existente no sistema
   - CEP real com endereço válido
   - Nome e dados pessoais consistentes

2. **Fallback para parametros.json**
   - JSON inválido ou incompleto
   - Campos obrigatórios ausentes
   - Validação de formato falhando

3. **Dados parciais**
   - Campos obrigatórios ausentes
   - Validação de formato incorreto
   - Fallback automático

4. **Dados inválidos**
   - CPF com dígitos verificadores incorretos
   - Placa inexistente no sistema
   - CEP inválido
   - Formato de dados incorreto

**Comando de Teste**:
```bash
# Teste com dados reais (copiados do parametros.json)
curl -X POST http://localhost/api/rpa/start \
  -H "Content-Type: application/json" \
  -d '{
    "cpf": "12345678901",
    "nome": "João Silva",
    "placa": "ABC1234",
    "cep": "01234567",
    "email": "joao@email.com",
    "celular": "11999999999"
  }'
```

**Validação de Sucesso**:
- RPA executa todas as 5 telas
- Progress tracker atualiza corretamente
- Estimativas capturadas na Tela 4
- Sem erros de validação do app.tosegurado

### 3. Migrar RPA Modular para Arquivo Principal

#### 3.1 Análise do Arquivo Principal (Estratégia Conservadora)
**Arquivo**: `executar_rpa_imediato_playwright.py`

**Análise Conservadora**:
- **Backup obrigatório** antes de qualquer modificação
- **Comparação detalhada** com arquivo modular
- **Testes de compatibilidade** com dados reais
- **Preservação de funcionalidades** existentes

**Verificações**:
- Funcionalidades disponíveis (15 telas vs 5 telas)
- Compatibilidade com telas 1-5
- Progress tracker implementado
- Captura de estimativas na Tela 4
- Suporte a argumentos de linha de comando
- Validação de dados de entrada

**Comando de Análise**:
```bash
# Backup do arquivo principal
cp executar_rpa_imediato_playwright.py executar_rpa_imediato_playwright.py.backup

# Comparar funcionalidades
diff -u executar_rpa_modular_telas_1_a_5.py executar_rpa_imediato_playwright.py

# Testar arquivo principal com dados reais
python3 executar_rpa_imediato_playwright.py --help
```

#### 3.2 Plano de Migração (Estratégia Conservadora)
**Opção A: Integrar funcionalidades (RECOMENDADA)**
- **Backup completo** antes da modificação
- Copiar lógica das telas 1-5 para arquivo principal
- Manter compatibilidade com progress tracker
- Preservar captura de estimativas
- **Testes incrementais** com dados reais
- **Rollback imediato** em caso de falha

**Opção B: Substituir arquivo modular (ALTERNATIVA)**
- **Backup completo** do arquivo modular
- Renomear arquivo principal para modular
- Manter funcionalidades existentes
- Atualizar referências no SessionService
- **Testes de compatibilidade** com V4

**Critérios de Decisão**:
- **Opção A** se arquivo principal suportar argumentos de linha de comando
- **Opção B** se arquivo principal for incompatível
- **Manter ambos** se houver dúvidas sobre compatibilidade

#### 3.3 Implementação da Migração (Estratégia Conservadora)
**Passos Conservadores**:
1. **Backup completo** do arquivo atual
2. **Análise detalhada** de diferenças
3. **Integração incremental** de funcionalidades
4. **Testes de compatibilidade** com dados reais
5. **Atualização de referências** no SessionService
6. **Validação completa** antes do deploy
7. **Rollback automático** em caso de falha

**Comandos de Backup**:
```bash
# Backup do arquivo principal
cp executar_rpa_imediato_playwright.py executar_rpa_imediato_playwright.py.backup.$(date +%Y%m%d_%H%M%S)

# Backup do arquivo modular
cp executar_rpa_modular_telas_1_a_5.py executar_rpa_modular_telas_1_a_5.py.backup.$(date +%Y%m%d_%H%M%S)

# Backup do SessionService
cp rpa-v4/src/Services/SessionService.php rpa-v4/src/Services/SessionService.php.backup.$(date +%Y%m%d_%H%M%S)
```

**Testes de Validação**:
```bash
# Teste com dados reais do parametros.json
python3 executar_rpa_imediato_playwright.py --data '{"cpf":"12345678901","nome":"João Silva","placa":"ABC1234","cep":"01234567"}' --session teste_migracao

# Verificar progress tracker
cat rpa_data/progress_teste_migracao.json

# Verificar estimativas
cat rpa_data/history_teste_migracao.json | grep -A 10 "estimativas"
```

#### 3.4 Testes Pós-Migração (Estratégia Conservadora)
**IMPORTANTE**: Todos os testes devem usar dados reais do `parametros.json`

**Cenários de Teste**:
1. **Execução completa (5 telas)**
   - Dados reais (CPF, placa, CEP válidos)
   - Progress tracker funcionando
   - Estimativas capturadas na Tela 4
   - Compatibilidade com V4

2. **Testes de compatibilidade**
   - Fallback para parametros.json
   - Validação de dados de entrada
   - Tratamento de erros
   - Rollback automático

3. **Testes de performance**
   - Múltiplas sessões simultâneas
   - Tempo de execução
   - Uso de recursos
   - Estabilidade do sistema

**Comandos de Teste**:
```bash
# Teste 1: Execução completa com dados reais
curl -X POST http://localhost/api/rpa/start \
  -H "Content-Type: application/json" \
  -d '{
    "cpf": "12345678901",
    "nome": "João Silva",
    "placa": "ABC1234",
    "cep": "01234567",
    "email": "joao@email.com",
    "celular": "11999999999"
  }'

# Teste 2: Fallback para parametros.json
curl -X POST http://localhost/api/rpa/start \
  -H "Content-Type: application/json" \
  -d '{}'

# Teste 3: Dados inválidos
curl -X POST http://localhost/api/rpa/start \
  -H "Content-Type: application/json" \
  -d '{
    "cpf": "00000000000",
    "placa": "XXX0000",
    "cep": "00000000"
  }'
```

**Critérios de Sucesso**:
- RPA executa todas as 5 telas sem erros
- Progress tracker atualiza corretamente
- Estimativas capturadas na Tela 4
- Fallback funciona quando necessário
- Sem erros de validação do app.tosegurado
- Performance mantida ou melhorada

## Cronograma de Implementação (Estratégia Conservadora)

### Semana 1: Monitoramento em Tempo Real
- **Dia 1-2**: Implementar endpoint de progress
- **Dia 3-4**: Atualizar dashboard
- **Dia 5**: Testes de monitoramento com dados reais

### Semana 2: Chamada com JSON (Estratégia Conservadora)
- **Dia 1-2**: Modificar SessionService com fallback
- **Dia 3-4**: Atualizar script Python com validação
- **Dia 5**: Testes de validação com dados reais do parametros.json

### Semana 3: Migração RPA Principal (Estratégia Conservadora)
- **Dia 1-2**: Análise, backup e comparação
- **Dia 3-4**: Implementação incremental da migração
- **Dia 5**: Testes de compatibilidade com dados reais

### Semana 4: Testes e Deploy (Estratégia Conservadora)
- **Dia 1-2**: Testes integrados com dados reais
- **Dia 3-4**: Ajustes finais e validação
- **Dia 5**: Deploy gradual em produção

### Semana 5: Validação e Monitoramento (NOVA)
- **Dia 1-2**: Monitoramento pós-deploy
- **Dia 3-4**: Ajustes baseados em feedback
- **Dia 5**: Documentação final e treinamento

## Arquivos a Modificar

### PHP (V4)
- `rpa-v4/src/Services/MonitorService.php`
- `rpa-v4/src/Services/SessionService.php`
- `rpa-v4/src/Services/ValidationService.php`
- `rpa-v4/src/Controllers/RPAController.php`
- `rpa-v4/public/js/dashboard.js`

### Python (RPA)
- `executar_rpa_modular_telas_1_a_5.py`
- `executar_rpa_imediato_playwright.py` (migração)

### Configuração
- `rpa-v4/config/app.php`
- `rpa-v4/VERSION_CONTROL.md`

## Testes Necessários (Estratégia Conservadora)

### Testes Unitários
- Validação de entrada com dados reais
- Monitoramento de progress
- Geração de scripts
- Fallback para parametros.json

### Testes de Integração
- API REST completa
- Dashboard em tempo real
- Compatibilidade com V3
- Rollback automático

### Testes de Validação (OBRIGATÓRIOS)
**IMPORTANTE**: Todos os testes devem usar dados reais do `parametros.json`

**Dados de Teste Obrigatórios**:
- CPF real com dígitos verificadores válidos
- Placa real existente no sistema
- CEP real com endereço válido
- Nome e dados pessoais consistentes

**Cenários de Teste**:
1. **Dados válidos completos** (idênticos ao parametros.json)
2. **Fallback para parametros.json** (JSON inválido)
3. **Dados parciais** (campos obrigatórios ausentes)
4. **Dados inválidos** (formato incorreto)
5. **Múltiplas sessões simultâneas**
6. **Recuperação de falhas**
7. **Rollback automático**

**Comandos de Teste**:
```bash
# Teste com dados reais (copiados do parametros.json)
curl -X POST http://localhost/api/rpa/start \
  -H "Content-Type: application/json" \
  -d '{
    "cpf": "12345678901",
    "nome": "João Silva",
    "placa": "ABC1234",
    "cep": "01234567",
    "email": "joao@email.com",
    "celular": "11999999999"
  }'
```

**Critérios de Sucesso**:
- RPA executa todas as 5 telas sem erros
- Progress tracker atualiza corretamente
- Estimativas capturadas na Tela 4
- Fallback funciona quando necessário
- Sem erros de validação do app.tosegurado
- Performance mantida ou melhorada
- Execução do RPA

### Testes de Produção
- Carga e performance
- Estabilidade
- Recuperação de falhas

## Critérios de Sucesso

### Funcionalidades
- ✅ Monitoramento em tempo real funcionando
- ✅ Chamada com JSON funcionando
- ✅ RPA principal migrado
- ✅ Estimativas capturadas
- ✅ Progress tracker funcionando

### Performance
- ✅ Tempo de resposta < 2 segundos
- ✅ Execução RPA < 30 segundos
- ✅ Dashboard responsivo
- ✅ Logs estruturados

### Estabilidade
- ✅ Sem falhas em 24h
- ✅ Recuperação automática
- ✅ Rollback disponível
- ✅ Monitoramento ativo

## Riscos e Mitigações

### Riscos
- **Risco**: Incompatibilidade entre arquivos
- **Mitigação**: Backup completo e testes extensivos

- **Risco**: Perda de funcionalidades
- **Mitigação**: Análise detalhada e preservação de código

- **Risco**: Instabilidade em produção
- **Mitigação**: Deploy gradual e monitoramento

### Plano de Rollback
1. Restaurar backup do arquivo principal
2. Reverter mudanças no PHP
3. Ativar modo de emergência
4. Notificar equipe

## Próximos Passos Imediatos

### 1. Implementar Monitoramento (Prioridade Alta)
- Criar endpoint `/api/rpa/progress/{session_id}`
- Atualizar dashboard para polling
- Testar em ambiente de desenvolvimento

### 2. Modificar Chamada JSON (Prioridade Alta)
- Atualizar SessionService para usar --data
- Modificar script Python para aceitar JSON
- Reativar validação de entrada

### 3. Análise de Migração (Prioridade Média)
- Comparar arquivos principal vs modular
- Identificar funcionalidades a preservar
- Planejar estratégia de migração

### 4. Testes Preparatórios (Prioridade Média)
- Configurar ambiente de testes
- Criar cenários de teste
- Preparar dados de teste

## Conclusão

Este plano estabelece um caminho claro para implementar a RPA V4 em produção com as melhorias solicitadas. A abordagem incremental permite testar cada funcionalidade antes de prosseguir, minimizando riscos e garantindo estabilidade.

**Próximo passo**: Implementar monitoramento em tempo real no PHP.
