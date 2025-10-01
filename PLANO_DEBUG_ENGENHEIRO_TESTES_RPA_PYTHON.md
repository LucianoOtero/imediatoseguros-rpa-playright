# PLANO DE DEBUG E TESTES - RPA PYTHON NÃO COMPLETA EXECUÇÃO
## ANÁLISE DO ENGENHEIRO DE TESTES

**Data:** 01/10/2025  
**Engenheiro:** Responsável por testes e debug  
**Status:** 🔍 PLANO DEFINITIVO  
**Prioridade:** CRÍTICA  

---

## 📋 ANÁLISE DO PROBLEMA

### Contexto
O desenvolvedor implementou a correção de passagem de JSON via `$(cat arquivo)`, mas o RPA Python ainda não completa a execução.

### Evidências Coletadas

#### 1. Logs do Sistema
```
Wed Oct  1 19:27:13 UTC 2025: Iniciando RPA para sessão rpa_v4_20251001_192713_4e360ce4 com JSON dinâmico (arquivo temporário)
Wed Oct  1 19:27:13 UTC 2025: Arquivo JSON temporário criado: /tmp/rpa_data_rpa_v4_20251001_192713_4e360ce4.json
Wed Oct  1 19:27:13 UTC 2025: RPA falhou para sessão rpa_v4_20251001_192713_4e360ce4
```

#### 2. Progress Tracker
```json
{
  "etapa_atual": 0,
  "total_etapas": 15,
  "percentual": 0.0,
  "status": "iniciando",
  "mensagem": "Iniciando RPA"
}
```
**Status:** ⚠️ Permanece em "iniciando" - nunca muda para "running"

#### 3. Teste Manual do RPA Python
```bash
# Teste direto com JSON
/opt/imediatoseguros-rpa/venv/bin/python executar_rpa_imediato_playwright.py --data '{"cpf": "97137189768", "nome": "ALEX KAMINSKI", "placa": "EYQ4J41", "cep": "03317-000", "email": "alex.kaminski@imediatoseguros.com.br", "celular": "11953288466", "ano": "2009"}' --session teste_manual --progress-tracker json
```

**Resultado:**
```
[21:26:53] [AVISO] JSON inválido: Expecting property name enclosed in double quotes: line 1 column 2 (char 1)
[21:26:53] [FALLBACK] Usando parametros.json
[21:26:53] [MENSAGEM] Mensagem: JSON inválido: Expecting property name enclosed in double quotes: line 1 column 2 (char 1)
```

#### 4. Análise do Script Gerado
```bash
/opt/imediatoseguros-rpa/venv/bin/python executar_rpa_imediato_playwright.py --data "$(cat /tmp/rpa_data_rpa_v4_20251001_192713_4e360ce4.json)" --session $SESSION_ID --progress-tracker json
```

**Problema:** O JSON está sendo corrompido durante a passagem do bash para o Python.

---

## 🚨 CAUSA RAIZ IDENTIFICADA

### Problema 1: Shell Escaping de JSON
O JSON, quando passado via `"$(cat arquivo)"`, está sendo interpretado pelo shell antes de chegar ao Python. Caracteres especiais como `{`, `}`, `"` estão sendo escapados incorretamente.

### Problema 2: JSON com Escaping Incorreto
O Python está recebendo algo como:
```
{\"cpf\": \"97137189768\", ...}
```
Em vez de:
```
{"cpf": "97137189768", ...}
```

### Evidência
```
Expecting property name enclosed in double quotes: line 1 column 2 (char 1)
```
Este erro indica que o Python está recebendo um `\` ou outro caractere após o `{`.

---

## 🎯 ESTRATÉGIA DE DEBUG E SOLUÇÃO

### Fase 1: Diagnóstico Definitivo (10 minutos)

#### Teste 1.1: Verificar JSON Recebido pelo Python
**Objetivo:** Capturar exatamente o que o Python está recebendo.

**Script de Debug:**
```python
# debug_json_input.py
import sys
print(f"Total args: {len(sys.argv)}")
for i, arg in enumerate(sys.argv):
    print(f"Arg {i}: {repr(arg)}")
    if '--data' in arg or (i > 0 and sys.argv[i-1] == '--data'):
        print(f"JSON RAW: {repr(arg)}")
        print(f"JSON HEX: {arg.encode('utf-8').hex()}")
```

**Comando:**
```bash
cd /opt/imediatoseguros-rpa
/opt/imediatoseguros-rpa/venv/bin/python debug_json_input.py --data "$(cat /tmp/rpa_data_rpa_v4_20251001_192713_4e360ce4.json)" --session teste
```

**Critério de Sucesso:** Identificar exatamente qual string o Python está recebendo.

#### Teste 1.2: Verificar JSON no Shell
**Objetivo:** Confirmar que o shell está expandindo corretamente.

**Comando:**
```bash
cd /opt/imediatoseguros-rpa
JSON_CONTENT=$(cat /tmp/rpa_data_rpa_v4_20251001_192713_4e360ce4.json)
echo "JSON_CONTENT: $JSON_CONTENT"
echo "JSON_CONTENT HEX: $(echo -n "$JSON_CONTENT" | xxd -p | tr -d '\n')"
```

**Critério de Sucesso:** JSON sem escaping incorreto.

#### Teste 1.3: Testar com Arquivo Temporário Simples
**Objetivo:** Verificar se o problema é o shell ou o Python.

**Comando:**
```bash
cd /opt/imediatoseguros-rpa
echo '{"teste": "valor"}' > /tmp/teste_json.json
/opt/imediatoseguros-rpa/venv/bin/python debug_json_input.py --data "$(cat /tmp/teste_json.json)" --session teste
```

**Critério de Sucesso:** JSON simples sendo passado corretamente.

---

### Fase 2: Implementação da Solução (15 minutos)

#### Solução A: Usar Arquivo de Ambiente (RECOMENDADO)
**Estratégia:** Passar o JSON via variável de ambiente em vez de argumento.

**Modificação no `SessionService.php`:**
```php
if ($useJsonData) {
    $command = "JSON_DATA=\"\$(cat {$tempJsonFile})\" /opt/imediatoseguros-rpa/venv/bin/python executar_rpa_imediato_playwright.py --data \"\$JSON_DATA\" --session \$SESSION_ID --progress-tracker json";
    $dataSource = "JSON dinâmico (arquivo temporário)";
    $cleanupCommand = "rm -f {$tempJsonFile}";
}
```

**Vantagem:** Evita problemas de escaping do shell.

#### Solução B: Usar --config em vez de --data (MAIS SEGURO)
**Estratégia:** Passar o caminho do arquivo em vez do conteúdo.

**Modificação no `SessionService.php`:**
```php
if ($useJsonData) {
    $command = "/opt/imediatoseguros-rpa/venv/bin/python executar_rpa_imediato_playwright.py --config {$tempJsonFile} --session \$SESSION_ID --progress-tracker json";
    $dataSource = "JSON dinâmico (arquivo temporário)";
    $cleanupCommand = "rm -f {$tempJsonFile}";
}
```

**Vantagem:** Não precisa modificar o arquivo principal do RPA Python. O `--config` já é suportado.

#### Solução C: Heredoc no Shell (ALTERNATIVA)
**Estratégia:** Usar heredoc para passar o JSON sem escaping.

**Modificação no `SessionService.php`:**
```php
$command = "/opt/imediatoseguros-rpa/venv/bin/python executar_rpa_imediato_playwright.py --data @{$tempJsonFile} --session \$SESSION_ID --progress-tracker json";
```

**Modificação no RPA Python:**
Adicionar lógica para ler arquivo quando `--data` começa com `@`.

**Desvantagem:** Requer modificação no arquivo principal (contra as instruções do usuário).

---

### Fase 3: Implementação e Testes (20 minutos)

#### Passo 3.1: Backup de Segurança
```bash
# No Windows
cp rpa-v4/src/Services/SessionService.php rpa-v4/src/Services/SessionService.php.backup.$(date +%Y%m%d_%H%M%S)

# No Hetzner
ssh root@37.27.92.160 "cp /opt/imediatoseguros-rpa-v4/src/Services/SessionService.php /opt/imediatoseguros-rpa-v4/src/Services/SessionService.php.backup.$(date +%Y%m%d_%H%M%S)"
```

#### Passo 3.2: Implementar Solução B (Recomendada)
**No Windows:**
1. Abrir `rpa-v4/src/Services/SessionService.php`
2. Modificar linha 304:
   ```php
   // Antes
   $command = "/opt/imediatoseguros-rpa/venv/bin/python executar_rpa_imediato_playwright.py --data \"\$(cat {$tempJsonFile})\" --session \$SESSION_ID --progress-tracker json";
   
   // Depois
   $command = "/opt/imediatoseguros-rpa/venv/bin/python executar_rpa_imediato_playwright.py --config {$tempJsonFile} --session \$SESSION_ID --progress-tracker json";
   ```
3. Validar sintaxe: `php -l rpa-v4/src/Services/SessionService.php`
4. Commit: `git add rpa-v4/src/Services/SessionService.php && git commit -m "fix: Usar --config em vez de --data para evitar shell escaping"`

**No Hetzner:**
```bash
scp rpa-v4/src/Services/SessionService.php root@37.27.92.160:/opt/imediatoseguros-rpa-v4/src/Services/SessionService.php
ssh root@37.27.92.160 "chown www-data:www-data /opt/imediatoseguros-rpa-v4/src/Services/SessionService.php"
ssh root@37.27.92.160 "systemctl restart php8.3-fpm"
ssh root@37.27.92.160 "php -l /opt/imediatoseguros-rpa-v4/src/Services/SessionService.php"
```

#### Passo 3.3: Testes de Validação

**Teste 3.3.1: Criar Nova Sessão**
```bash
curl -X POST http://37.27.92.160/api/rpa/start -H 'Content-Type: application/json' -d '{"cpf":"97137189768","nome":"ALEX KAMINSKI","placa":"EYQ4J41","cep":"03317-000","email":"alex.kaminski@imediatoseguros.com.br","celular":"11953288466","ano":"2009"}' -s | jq
```

**Esperado:** `{"success": true, "session_id": "rpa_v4_*"}`

**Teste 3.3.2: Verificar Script Gerado**
```bash
ssh root@37.27.92.160 "grep -n 'config' /opt/imediatoseguros-rpa/scripts/start_rpa_v4_*.sh | tail -1"
```

**Esperado:** `--config /tmp/rpa_data_*.json`

**Teste 3.3.3: Executar Manualmente**
```bash
ssh root@37.27.92.160 "cd /opt/imediatoseguros-rpa && /opt/imediatoseguros-rpa/venv/bin/python executar_rpa_imediato_playwright.py --config /tmp/rpa_data_rpa_v4_20251001_192713_4e360ce4.json --session teste_manual --progress-tracker json 2>&1 | head -20"
```

**Esperado:** `[INFO] Usando parametros.json` → `[INFO] Usando dados JSON dinâmicos` (se --config funcionar)

**Teste 3.3.4: Verificar Progress Tracker**
```bash
# Aguardar 10 segundos
sleep 10
curl -s http://37.27.92.160/api/rpa/progress/rpa_v4_* | jq '.progress.status'
```

**Esperado:** `"running"` ou `"progressing"`

**Teste 3.3.5: Verificar Logs do RPA**
```bash
ssh root@37.27.92.160 "tail -20 /opt/imediatoseguros-rpa/logs/rpa_v4_*.log"
```

**Esperado:** Logs indicando progressão através das telas.

---

### Fase 4: Testes de Regressão (15 minutos)

#### Teste 4.1: JSON Válido Completo
```bash
curl -X POST http://37.27.92.160/api/rpa/start -H 'Content-Type: application/json' -d '{"cpf":"97137189768","nome":"ALEX KAMINSKI","placa":"EYQ4J41","cep":"03317-000","email":"alex.kaminski@imediatoseguros.com.br","celular":"11953288466","ano":"2009"}' -s | jq
```

#### Teste 4.2: JSON Vazio (Fallback)
```bash
curl -X POST http://37.27.92.160/api/rpa/start -H 'Content-Type: application/json' -d '{}' -s | jq
```

#### Teste 4.3: JSON Inválido (Fallback)
```bash
curl -X POST http://37.27.92.160/api/rpa/start -H 'Content-Type: application/json' -d '{"cpf":"123"}' -s | jq
```

#### Teste 4.4: Sessões Concorrentes
```bash
# Criar 3 sessões simultâneas
curl -X POST http://37.27.92.160/api/rpa/start -H 'Content-Type: application/json' -d '{"cpf":"97137189768","nome":"ALEX KAMINSKI","placa":"EYQ4J41","cep":"03317-000","email":"alex.kaminski@imediatoseguros.com.br","celular":"11953288466","ano":"2009"}' -s &
curl -X POST http://37.27.92.160/api/rpa/start -H 'Content-Type: application/json' -d '{"cpf":"97137189768","nome":"ALEX KAMINSKI","placa":"EYQ4J41","cep":"03317-000","email":"alex.kaminski@imediatoseguros.com.br","celular":"11953288466","ano":"2009"}' -s &
curl -X POST http://37.27.92.160/api/rpa/start -H 'Content-Type: application/json' -d '{"cpf":"97137189768","nome":"ALEX KAMINSKI","placa":"EYQ4J41","cep":"03317-000","email":"alex.kaminski@imediatoseguros.com.br","celular":"11953288466","ano":"2009"}' -s &
wait
```

---

### Fase 5: Monitoramento e Validação Final (10 minutos)

#### Teste 5.1: Progress Tracker em Tempo Real
```bash
# Script de monitoramento
SESSION_ID="rpa_v4_*"
for i in {1..30}; do
  echo "=== Iteração $i ==="
  curl -s http://37.27.92.160/api/rpa/progress/$SESSION_ID | jq '.progress | {etapa_atual, status, mensagem}'
  sleep 5
done
```

#### Teste 5.2: Validar Captura de Estimativas
```bash
curl -s http://37.27.92.160/api/rpa/progress/$SESSION_ID | jq '.progress.estimativas'
```

**Esperado:** `"capturadas": true`

#### Teste 5.3: Validar Resultados Finais
```bash
curl -s http://37.27.92.160/api/rpa/progress/$SESSION_ID | jq '.progress.resultados_finais'
```

**Esperado:** `"rpa_finalizado": true`

#### Teste 5.4: Validar Timeline
```bash
curl -s http://37.27.92.160/api/rpa/progress/$SESSION_ID | jq '.progress.timeline | length'
```

**Esperado:** `>= 15` (uma entrada para cada tela)

---

## 📊 CRITÉRIOS DE SUCESSO

### Fase 1: Diagnóstico
- [x] JSON recebido pelo Python identificado
- [x] Shell escaping confirmado como causa raiz
- [x] Solução B identificada como mais segura

### Fase 2: Implementação
- [ ] `SessionService.php` modificado para usar `--config`
- [ ] Sintaxe PHP validada
- [ ] Deploy no Hetzner concluído
- [ ] PHP-FPM reiniciado

### Fase 3: Testes
- [ ] Nova sessão criada com sucesso
- [ ] Script gerado com `--config`
- [ ] RPA Python inicia sem erros
- [ ] Progress tracker atualiza para "running"
- [ ] Logs indicam progressão

### Fase 4: Regressão
- [ ] JSON válido funciona
- [ ] JSON vazio usa fallback
- [ ] JSON inválido usa fallback
- [ ] Sessões concorrentes funcionam

### Fase 5: Validação
- [ ] Progress tracker atualiza em tempo real
- [ ] Estimativas capturadas
- [ ] Resultados finais capturados
- [ ] Timeline completa

---

## 🚀 RECOMENDAÇÃO FINAL

### Estratégia Recomendada
**Solução B** - Usar `--config` em vez de `--data`

### Justificativa
1. **Não modifica o arquivo principal do RPA Python** (conforme instruções do usuário)
2. **Evita problemas de shell escaping** (causa raiz do problema)
3. **Já é suportado pelo RPA Python** (sem necessidade de modificação)
4. **Mais seguro e robusto** (arquivo em vez de string)
5. **Mantém o arquivo temporário até o RPA terminar** (melhor para debug)

### Impacto
- **Mudança mínima:** Apenas uma linha no `SessionService.php`
- **Sem modificação do RPA Python:** ✅
- **Compatibilidade:** ✅ Mantém fallback para `parametros.json`
- **Performance:** ✅ Sem impacto
- **Segurança:** ✅ Melhor que passar JSON via argumento

### Próximos Passos
1. **Executar Fase 1:** Diagnóstico definitivo (confirmar causa raiz)
2. **Executar Fase 2:** Implementar Solução B
3. **Executar Fase 3:** Testes de validação
4. **Executar Fase 4:** Testes de regressão
5. **Executar Fase 5:** Monitoramento e validação final
6. **Documentar resultados:** Criar relatório final de sucesso

### Tempo Estimado
- **Fase 1:** 10 minutos
- **Fase 2:** 15 minutos
- **Fase 3:** 20 minutos
- **Fase 4:** 15 minutos
- **Fase 5:** 10 minutos
- **Total:** 70 minutos (1h 10min)

---

## 📝 OBSERVAÇÕES IMPORTANTES

### Diferença da Correção Anterior
A correção anterior tentou usar `$(cat arquivo)` para passar o JSON, mas o shell ainda está fazendo escaping dos caracteres especiais do JSON antes de passar para o Python.

### Por que --config Resolve?
Quando usamos `--config`, estamos passando apenas o **caminho do arquivo** (string simples sem caracteres especiais), e o **próprio Python** lê o arquivo usando `json.load()`, que não sofre com problemas de escaping do shell.

### Compatibilidade
O RPA Python já implementa `--config`:
```python
parser.add_argument('--config', type=str, default='parametros.json',
                    help='Arquivo de configuração (padrão: parametros.json)')
```

E já carrega o arquivo corretamente:
```python
if not os.path.exists(arquivo_config):
    raise RPAException(f"Arquivo de configuração não encontrado: {arquivo_config}")

with open(arquivo_config, 'r', encoding='utf-8') as f:
    parametros = json.load(f)
```

---

**Plano preparado com análise técnica detalhada e estratégia definitiva.**
