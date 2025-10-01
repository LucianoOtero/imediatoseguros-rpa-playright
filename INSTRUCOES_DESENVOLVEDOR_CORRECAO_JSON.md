# INSTRUÇÕES PARA DESENVOLVEDOR - CORREÇÃO JSON
## PROBLEMA IDENTIFICADO E SOLUÇÃO RECOMENDADA

**Data:** 01/10/2025  
**Desenvolvedor:** Responsável pela implementação  
**Status:** ✅ PROBLEMA IDENTIFICADO - SOLUÇÃO DEFINIDA  
**Prioridade:** CRÍTICA  

---

## 📋 RESUMO EXECUTIVO

### Problema Identificado
O RPA Python não consegue ler o JSON do arquivo temporário quando passado via `--data @/tmp/rpa_data_*.json`.

### Causa Raiz
O RPA Python espera receber o **conteúdo JSON como string**, mas está recebendo um **caminho de arquivo com prefixo @**.

### Solução Recomendada
Modificar **apenas 1 linha** no `SessionService.php` para passar o conteúdo do arquivo em vez do caminho.

---

## 🔍 ANÁLISE TÉCNICA DETALHADA

### Como o RPA Python Processa `--data`

O RPA Python já implementa corretamente a leitura de JSON:

```python
# executar_rpa_imediato_playwright.py - linha 1163-1171
if dados_json:
    try:
        parametros = json.loads(dados_json)  # ✅ JÁ IMPLEMENTADO
        exibir_mensagem("[INFO] Usando dados JSON dinâmicos")
    except json.JSONDecodeError as e:
        exibir_mensagem(f"[AVISO] JSON inválido: {e}")
        exibir_mensagem("[FALLBACK] Usando parametros.json")
        raise RPAException(f"JSON inválido: {e}")
```

### Problema Atual

```bash
# ❌ PROBLEMA: RPA Python recebe string literal
--data @/tmp/rpa_data_*.json

# Resultado: RPA Python tenta fazer json.loads("@/tmp/rpa_data_*.json")
# Erro: JSON inválido: Expecting value: line 1 column 1 (char 0)
```

### Solução

```bash
# ✅ SOLUÇÃO: RPA Python recebe conteúdo do arquivo
--data "$(cat /tmp/rpa_data_*.json)"

# Resultado: RPA Python recebe o JSON real e funciona
```

---

## 🛠️ IMPLEMENTAÇÃO

### Arquivo a Modificar
**`rpa-v4/src/Services/SessionService.php`**

### Linha a Modificar
**Linha 304** (aproximadamente)

### Modificação Específica

#### Antes (não funciona):
```php
$command = "/opt/imediatoseguros-rpa/venv/bin/python executar_rpa_imediato_playwright.py --data @{$tempJsonFile} --session \$SESSION_ID --progress-tracker json";
```

#### Depois (funciona):
```php
$command = "/opt/imediatoseguros-rpa/venv/bin/python executar_rpa_imediato_playwright.py --data \"\$(cat {$tempJsonFile})\" --session \$SESSION_ID --progress-tracker json";
```

### Contexto Completo da Função

```php
private function generateStartScript(string $sessionId, array $data): string
{
    // Estratégia conservadora: validar dados e usar fallback
    $useJsonData = !empty($data) && $this->validateData($data);
    
    // ✅ CORREÇÃO: Definir variáveis sempre para evitar erro no heredoc
    $tempJsonFile = "/tmp/rpa_data_{$sessionId}.json";
    $jsonContent = json_encode($data, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT);
    
    if ($useJsonData) {
        // ✅ CORREÇÃO: Usar $(cat arquivo) em vez de @arquivo
        $command = "/opt/imediatoseguros-rpa/venv/bin/python executar_rpa_imediato_playwright.py --data \"\$(cat {$tempJsonFile})\" --session \$SESSION_ID --progress-tracker json";
        $dataSource = "JSON dinâmico (arquivo temporário)";
        $cleanupCommand = "rm -f {$tempJsonFile}";
    } else {
        $command = "/opt/imediatoseguros-rpa/venv/bin/python executar_rpa_imediato_playwright.py --config /opt/imediatoseguros-rpa/parametros.json --session \$SESSION_ID --progress-tracker json";
        $dataSource = "parametros.json (fallback)";
        $cleanupCommand = "";
    }
    
    // ... resto da função permanece igual
}
```

---

## 🧪 TESTES OBRIGATÓRIOS

### Teste 1: Validação de Sintaxe PHP
```bash
php -l rpa-v4/src/Services/SessionService.php
```
**Resultado esperado:** `No syntax errors detected`

### Teste 2: Criação de Sessão
```bash
curl -X POST http://37.27.92.160/api/rpa/start \
  -H 'Content-Type: application/json' \
  -d '{
    "cpf":"97137189768",
    "nome":"ALEX KAMINSKI",
    "placa":"EYQ4J41",
    "cep":"03317-000",
    "email":"alex.kaminski@imediatoseguros.com.br",
    "celular":"11953288466",
    "ano":"2009"
  }'
```
**Resultado esperado:** `{"success": true, "session_id": "rpa_v4_...", "message": "Sessão RPA criada com sucesso"}`

### Teste 3: Verificação do Script Gerado
```bash
# Substituir SESSION_ID pelo ID retornado no teste anterior
ls -la /opt/imediatoseguros-rpa/scripts/start_rpa_v4_SESSION_ID.sh
```
**Resultado esperado:** Arquivo existe e é executável

### Teste 4: Conteúdo do Script
```bash
# Verificar se a linha contém $(cat em vez de @
grep -n "cat.*tempJsonFile" /opt/imediatoseguros-rpa/scripts/start_rpa_v4_SESSION_ID.sh
```
**Resultado esperado:** Linha encontrada com `$(cat /tmp/rpa_data_*.json)`

### Teste 5: Execução Manual do Script
```bash
# Executar o script manualmente para verificar se o RPA inicia
bash -x /opt/imediatoseguros-rpa/scripts/start_rpa_v4_SESSION_ID.sh
```
**Resultado esperado:** RPA inicia sem erro de JSON inválido

### Teste 6: Progress Tracker
```bash
# Verificar se o progress tracker atualiza
curl -s http://37.27.92.160/api/rpa/progress/SESSION_ID
```
**Resultado esperado:** Status muda de "waiting" para "running" e depois "completed"

---

## 🧪 TESTES DE FUNCIONALIDADE DETALHADOS

### Fase 1: Testes de Validação Básica

#### Teste 1.1: Validação de Sintaxe PHP
**Objetivo:** Verificar se a modificação não introduziu erros de sintaxe
```bash
php -l rpa-v4/src/Services/SessionService.php
```
**Critério de Sucesso:** `No syntax errors detected`
**Tempo Estimado:** 5 segundos

#### Teste 1.2: Validação de Permissões
**Objetivo:** Verificar se o arquivo tem permissões corretas
```bash
ls -la /opt/imediatoseguros-rpa-v4/src/Services/SessionService.php
```
**Critério de Sucesso:** `-rw-r--r-- 1 www-data www-data`
**Tempo Estimado:** 5 segundos

#### Teste 1.3: Validação de PHP-FPM
**Objetivo:** Verificar se o PHP-FPM está funcionando
```bash
systemctl status php8.3-fpm
```
**Critério de Sucesso:** `Active: active (running)`
**Tempo Estimado:** 10 segundos

### Fase 2: Testes de API

#### Teste 2.1: Criação de Sessão com JSON Válido
**Objetivo:** Verificar se a API aceita JSON válido
```bash
curl -X POST http://37.27.92.160/api/rpa/start \
  -H 'Content-Type: application/json' \
  -d '{
    "cpf":"97137189768",
    "nome":"ALEX KAMINSKI",
    "placa":"EYQ4J41",
    "cep":"03317-000",
    "email":"alex.kaminski@imediatoseguros.com.br",
    "celular":"11953288466",
    "ano":"2009"
  }' \
  -w "\nHTTP Status: %{http_code}\n"
```
**Critério de Sucesso:** 
- HTTP Status: 200
- JSON: `{"success": true, "session_id": "rpa_v4_...", "message": "Sessão RPA criada com sucesso"}`
**Tempo Estimado:** 10 segundos

#### Teste 2.2: Criação de Sessão com JSON Inválido
**Objetivo:** Verificar se a API rejeita JSON inválido
```bash
curl -X POST http://37.27.92.160/api/rpa/start \
  -H 'Content-Type: application/json' \
  -d '{"cpf":"123","nome":}' \
  -w "\nHTTP Status: %{http_code}\n"
```
**Critério de Sucesso:** 
- HTTP Status: 400 ou 422
- JSON contém mensagem de erro
**Tempo Estimado:** 5 segundos

#### Teste 2.3: Criação de Sessão sem JSON
**Objetivo:** Verificar se a API funciona sem JSON (fallback)
```bash
curl -X POST http://37.27.92.160/api/rpa/start \
  -H 'Content-Type: application/json' \
  -d '{}' \
  -w "\nHTTP Status: %{http_code}\n"
```
**Critério de Sucesso:** 
- HTTP Status: 200
- JSON: `{"success": true, "session_id": "rpa_v4_...", "message": "Sessão RPA criada com sucesso"}`
**Tempo Estimado:** 10 segundos

### Fase 3: Testes de Geração de Script

#### Teste 3.1: Verificação de Existência do Script
**Objetivo:** Verificar se o script é gerado corretamente
```bash
# Após criar sessão no Teste 2.1, usar o SESSION_ID retornado
SESSION_ID="rpa_v4_20251001_191409_2d5ec5b5"  # Substituir pelo ID real
ls -la /opt/imediatoseguros-rpa/scripts/start_rpa_v4_${SESSION_ID}.sh
```
**Critério de Sucesso:** 
- Arquivo existe
- Permissões: `-rwxr-xr-x`
- Proprietário: `www-data www-data`
**Tempo Estimado:** 5 segundos

#### Teste 3.2: Verificação de Conteúdo do Script
**Objetivo:** Verificar se o script contém a correção
```bash
grep -n "cat.*tempJsonFile" /opt/imediatoseguros-rpa/scripts/start_rpa_v4_${SESSION_ID}.sh
```
**Critério de Sucesso:** 
- Linha encontrada
- Contém: `$(cat /tmp/rpa_data_*.json)`
- NÃO contém: `@/tmp/rpa_data_*.json`
**Tempo Estimado:** 5 segundos

#### Teste 3.3: Verificação de Shebang e Encoding
**Objetivo:** Verificar se o script tem formato correto
```bash
head -1 /opt/imediatoseguros-rpa/scripts/start_rpa_v4_${SESSION_ID}.sh
file /opt/imediatoseguros-rpa/scripts/start_rpa_v4_${SESSION_ID}.sh
```
**Critério de Sucesso:** 
- Shebang: `#!/bin/bash`
- Encoding: `UTF-8 text executable`
**Tempo Estimado:** 5 segundos

### Fase 4: Testes de Execução do RPA

#### Teste 4.1: Execução Manual do Script
**Objetivo:** Verificar se o script executa sem erros
```bash
bash -x /opt/imediatoseguros-rpa/scripts/start_rpa_v4_${SESSION_ID}.sh 2>&1 | head -20
```
**Critério de Sucesso:** 
- Script inicia sem erros
- RPA Python inicia
- NÃO aparece: `JSON inválido: Expecting value: line 1 column 1 (char 0)`
**Tempo Estimado:** 30 segundos

#### Teste 4.2: Verificação de Arquivo JSON Temporário
**Objetivo:** Verificar se o arquivo JSON temporário é criado
```bash
ls -la /tmp/rpa_data_${SESSION_ID}.json
cat /tmp/rpa_data_${SESSION_ID}.json
```
**Critério de Sucesso:** 
- Arquivo existe
- Contém JSON válido
- Dados corretos (cpf, nome, placa, etc.)
**Tempo Estimado:** 10 segundos

#### Teste 4.3: Verificação de Logs do RPA
**Objetivo:** Verificar se o RPA processa os dados corretamente
```bash
tail -20 /opt/imediatoseguros-rpa/logs/rpa_v4_${SESSION_ID}.log
```
**Critério de Sucesso:** 
- Logs mostram início do RPA
- NÃO aparece: `JSON inválido`
- Aparece: `[INFO] Usando dados JSON dinâmicos`
**Tempo Estimado:** 10 segundos

### Fase 5: Testes de Progress Tracker

#### Teste 5.1: Status Inicial
**Objetivo:** Verificar status inicial da sessão
```bash
curl -s http://37.27.92.160/api/rpa/progress/${SESSION_ID} | jq '.progress.status'
```
**Critério de Sucesso:** `"waiting"`
**Tempo Estimado:** 5 segundos

#### Teste 5.2: Status Durante Execução
**Objetivo:** Verificar se o status muda para "running"
```bash
# Aguardar 10 segundos e verificar novamente
sleep 10
curl -s http://37.27.92.160/api/rpa/progress/${SESSION_ID} | jq '.progress.status'
```
**Critério de Sucesso:** `"running"`
**Tempo Estimado:** 15 segundos

#### Teste 5.3: Status Final
**Objetivo:** Verificar status final da sessão
```bash
# Aguardar conclusão (pode levar 2-3 minutos)
sleep 180
curl -s http://37.27.92.160/api/rpa/progress/${SESSION_ID} | jq '.progress.status'
```
**Critério de Sucesso:** `"completed"`
**Tempo Estimado:** 3 minutos

#### Teste 5.4: Verificação de Dados Capturados
**Objetivo:** Verificar se os dados foram capturados corretamente
```bash
curl -s http://37.27.92.160/api/rpa/progress/${SESSION_ID} | jq '.progress.estimativas'
```
**Critério de Sucesso:** 
- `"capturadas": true`
- Dados não nulos
**Tempo Estimado:** 5 segundos

### Fase 6: Testes de Concorrência

#### Teste 6.1: Múltiplas Sessões Simultâneas
**Objetivo:** Verificar se o sistema suporta múltiplas sessões
```bash
# Criar 3 sessões simultâneas
for i in {1..3}; do
  curl -X POST http://37.27.92.160/api/rpa/start \
    -H 'Content-Type: application/json' \
    -d "{\"cpf\":\"9713718976${i}\",\"nome\":\"TESTE ${i}\",\"placa\":\"EYQ4J4${i}\",\"cep\":\"03317-000\",\"email\":\"teste${i}@teste.com\",\"celular\":\"1195328846${i}\",\"ano\":\"2009\"}" &
done
wait
```
**Critério de Sucesso:** 
- 3 sessões criadas com sucesso
- 3 scripts gerados
- 3 processos RPA iniciados
**Tempo Estimado:** 30 segundos

#### Teste 6.2: Verificação de Isolamento
**Objetivo:** Verificar se as sessões são isoladas
```bash
# Verificar se cada sessão tem seu próprio arquivo JSON
ls -la /tmp/rpa_data_*.json
```
**Critério de Sucesso:** 
- 3 arquivos JSON diferentes
- Cada um com dados únicos
**Tempo Estimado:** 10 segundos

### Fase 7: Testes de Robustez

#### Teste 7.1: Teste com Dados Especiais
**Objetivo:** Verificar se o sistema lida com caracteres especiais
```bash
curl -X POST http://37.27.92.160/api/rpa/start \
  -H 'Content-Type: application/json' \
  -d '{
    "cpf":"97137189768",
    "nome":"JOÃO DA SILVA & FILHOS",
    "placa":"EYQ4J41",
    "cep":"03317-000",
    "email":"joao.silva@empresa.com.br",
    "celular":"11953288466",
    "ano":"2009"
  }'
```
**Critério de Sucesso:** 
- Sessão criada com sucesso
- Script gerado corretamente
- RPA inicia sem erros
**Tempo Estimado:** 30 segundos

#### Teste 7.2: Teste com JSON Grande
**Objetivo:** Verificar se o sistema lida com JSON grande
```bash
# Criar JSON com muitos campos
LARGE_JSON='{"cpf":"97137189768","nome":"ALEX KAMINSKI","placa":"EYQ4J41","cep":"03317-000","email":"alex.kaminski@imediatoseguros.com.br","celular":"11953288466","ano":"2009","campo_extra1":"valor1","campo_extra2":"valor2","campo_extra3":"valor3"}'

curl -X POST http://37.27.92.160/api/rpa/start \
  -H 'Content-Type: application/json' \
  -d "$LARGE_JSON"
```
**Critério de Sucesso:** 
- Sessão criada com sucesso
- Script gerado corretamente
- RPA inicia sem erros
**Tempo Estimado:** 30 segundos

### Fase 8: Testes de Limpeza

#### Teste 8.1: Verificação de Limpeza de Arquivos Temporários
**Objetivo:** Verificar se os arquivos temporários são limpos
```bash
# Aguardar conclusão do RPA
sleep 300
ls -la /tmp/rpa_data_*.json
```
**Critério de Sucesso:** 
- Arquivos temporários removidos
- NÃO há arquivos órfãos
**Tempo Estimado:** 5 minutos

#### Teste 8.2: Verificação de Limpeza de Scripts
**Objetivo:** Verificar se os scripts são limpos (se auto-delete estiver habilitado)
```bash
ls -la /opt/imediatoseguros-rpa/scripts/start_rpa_v4_*.sh
```
**Critério de Sucesso:** 
- Scripts removidos (se auto-delete habilitado)
- Ou scripts mantidos (se auto-delete desabilitado)
**Tempo Estimado:** 5 segundos

---

## 📊 CRONOGRAMA DE TESTES

### Tempo Total Estimado: 45 minutos

| Fase | Testes | Tempo | Dependências |
|------|--------|-------|--------------|
| 1 | Validação Básica | 5 min | - |
| 2 | API | 10 min | Fase 1 |
| 3 | Geração de Script | 10 min | Fase 2 |
| 4 | Execução RPA | 5 min | Fase 3 |
| 5 | Progress Tracker | 3 min | Fase 4 |
| 6 | Concorrência | 5 min | Fase 5 |
| 7 | Robustez | 5 min | Fase 6 |
| 8 | Limpeza | 2 min | Fase 7 |

### Ordem de Execução Recomendada
1. **Fases 1-3:** Executar sequencialmente
2. **Fase 4:** Executar em paralelo com Fase 5
3. **Fases 6-7:** Executar em paralelo
4. **Fase 8:** Executar no final

---

## 🎯 CRITÉRIOS DE APROVAÇÃO

### Testes Críticos (Obrigatórios)
- [ ] Teste 1.1: Validação de Sintaxe PHP
- [ ] Teste 2.1: Criação de Sessão com JSON Válido
- [ ] Teste 3.1: Verificação de Existência do Script
- [ ] Teste 3.2: Verificação de Conteúdo do Script
- [ ] Teste 4.1: Execução Manual do Script
- [ ] Teste 5.2: Status Durante Execução
- [ ] Teste 5.3: Status Final

### Testes Importantes (Recomendados)
- [ ] Teste 2.2: Criação de Sessão com JSON Inválido
- [ ] Teste 2.3: Criação de Sessão sem JSON
- [ ] Teste 4.2: Verificação de Arquivo JSON Temporário
- [ ] Teste 4.3: Verificação de Logs do RPA
- [ ] Teste 5.4: Verificação de Dados Capturados
- [ ] Teste 6.1: Múltiplas Sessões Simultâneas

### Testes Opcionais (Se houver tempo)
- [ ] Teste 6.2: Verificação de Isolamento
- [ ] Teste 7.1: Teste com Dados Especiais
- [ ] Teste 7.2: Teste com JSON Grande
- [ ] Teste 8.1: Verificação de Limpeza de Arquivos Temporários
- [ ] Teste 8.2: Verificação de Limpeza de Scripts

---

## 🚨 TRATAMENTO DE FALHAS

### Se um teste falhar:
1. **Documentar o erro** com logs completos
2. **Identificar a causa** raiz
3. **Implementar correção** se necessário
4. **Re-executar** o teste
5. **Validar** que não quebrou outros testes

### Se múltiplos testes falharem:
1. **Parar** a execução
2. **Analisar** padrões de falha
3. **Identificar** problema sistêmico
4. **Implementar** correção abrangente
5. **Re-iniciar** testes do início

### Se testes críticos falharem:
1. **Não prosseguir** para produção
2. **Investigar** profundamente
3. **Considerar** rollback
4. **Revisar** implementação
5. **Re-testar** extensivamente

---

## 📋 CHECKLIST DE IMPLEMENTAÇÃO

### Pré-Implementação
- [ ] Fazer backup do arquivo atual
- [ ] Verificar se está no branch correto
- [ ] Confirmar que não há mudanças não commitadas

### Implementação
- [ ] Modificar linha 304 do `SessionService.php`
- [ ] Trocar `@{$tempJsonFile}` por `"$(cat {$tempJsonFile})"`
- [ ] Verificar sintaxe PHP
- [ ] Fazer commit da alteração

### Deploy
- [ ] Fazer upload para o servidor Hetzner
- [ ] Ajustar permissões (www-data:www-data)
- [ ] Reiniciar PHP-FPM
- [ ] Verificar se não há erros de sintaxe

### Testes
- [ ] Teste 1: Validação de sintaxe PHP
- [ ] Teste 2: Criação de sessão
- [ ] Teste 3: Verificação do script gerado
- [ ] Teste 4: Conteúdo do script
- [ ] Teste 5: Execução manual do script
- [ ] Teste 6: Progress tracker

### Validação Final
- [ ] RPA inicia corretamente
- [ ] Progress tracker atualiza em tempo real
- [ ] Dados JSON são processados corretamente
- [ ] Não há erros de JSON inválido
- [ ] Sistema funciona end-to-end

---

## 🚨 PONTOS DE ATENÇÃO

### 1. Escape de Caracteres
```php
// ✅ CORRETO: Escape duplo para bash
--data \"\$(cat {$tempJsonFile})\"

// ❌ INCORRETO: Escape simples
--data "$(cat {$tempJsonFile})"
```

### 2. Permissões do Arquivo
```bash
# Após upload, ajustar permissões
chown www-data:www-data /opt/imediatoseguros-rpa-v4/src/Services/SessionService.php
```

### 3. Reinício do PHP-FPM
```bash
# Sempre reiniciar após modificação
systemctl restart php8.3-fpm
```

### 4. Backup Obrigatório
```bash
# Fazer backup antes de modificar
cp /opt/imediatoseguros-rpa-v4/src/Services/SessionService.php /opt/imediatoseguros-rpa-v4/src/Services/SessionService.php.backup.$(date +%Y%m%d_%H%M%S)
```

---

## 🔄 ROLLBACK (SE NECESSÁRIO)

### Se a correção não funcionar:
```bash
# Restaurar backup
cp /opt/imediatoseguros-rpa-v4/src/Services/SessionService.php.backup.20251001_* /opt/imediatoseguros-rpa-v4/src/Services/SessionService.php

# Ajustar permissões
chown www-data:www-data /opt/imediatoseguros-rpa-v4/src/Services/SessionService.php

# Reiniciar PHP-FPM
systemctl restart php8.3-fpm
```

---

## 📊 CRITÉRIOS DE SUCESSO

### Funcionalidade
- [ ] Sessão RPA é criada com sucesso
- [ ] Script é gerado corretamente
- [ ] RPA Python inicia sem erro de JSON
- [ ] Progress tracker atualiza em tempo real
- [ ] Dados JSON são processados corretamente

### Qualidade
- [ ] Sem erros de sintaxe PHP
- [ ] Sem erros de JSON inválido
- [ ] Logs limpos e informativos
- [ ] Performance mantida
- [ ] Sistema estável

### Monitoramento
- [ ] Logs da aplicação sem erros
- [ ] Logs do RPA sem erros
- [ ] Progress tracker funcionando
- [ ] API respondendo corretamente

---

## 🎯 PRÓXIMOS PASSOS

### Imediato (hoje)
1. Implementar a correção
2. Executar todos os testes
3. Validar funcionamento end-to-end
4. Documentar resultados

### Curto Prazo (esta semana)
1. Monitorar sistema em produção
2. Verificar se não há regressões
3. Otimizar se necessário
4. Preparar documentação final

### Médio Prazo (próxima semana)
1. Reabilitar auto-delete do script (se desejado)
2. Implementar melhorias adicionais
3. Preparar para próxima versão

---

## 📞 SUPORTE

### Em caso de problemas:
1. Verificar logs da aplicação: `/var/log/nginx/error.log`
2. Verificar logs do PHP-FPM: `/var/log/php8.3-fpm.log`
3. Verificar logs do RPA: `/opt/imediatoseguros-rpa/logs/`
4. Executar testes de diagnóstico
5. Fazer rollback se necessário

### Contatos:
- **Engenheiro de Testes:** Responsável pela análise
- **Desenvolvedor:** Responsável pela implementação
- **Arquivo de Referência:** `RELATORIO_FINAL_DEBUG_SCRIPT.md`

---

**Documento preparado com base em análise técnica detalhada e evidências concretas.**
