# Plano de Testes RPA V4.1.0 - Estratégia Conservadora

## Objetivo
Validar completamente a implementação da RPA V4.1.0 com estratégia conservadora, garantindo compatibilidade com V3, funcionamento de todas as funcionalidades implementadas e estabilidade em produção.

## Estratégia de Testes

### Princípios
- **Dados reais obrigatórios** para todos os testes
- **Compatibilidade total** com V3
- **Fallback automático** validado
- **Testes incrementais** com rollback
- **Cobertura completa** de funcionalidades
- **Validação de performance** e estabilidade

### Dados de Teste Obrigatórios
**IMPORTANTE**: Todos os testes devem usar dados reais do `parametros.json`:
- **CPF**: 12345678901 (válido com dígitos verificadores)
- **Placa**: ABC1234 (formato brasileiro válido)
- **CEP**: 01234567 (8 dígitos válidos)
- **Nome**: João Silva
- **Email**: joao@email.com
- **Celular**: 11999999999 (11 dígitos)

## Fases de Teste

### Fase 1: Testes Unitários (2 dias)

#### 1.1 Testes de Validação
**Objetivo**: Validar sistema de validação robusta

**Cenários**:
1. **Dados válidos completos**
   ```json
   {
     "cpf": "12345678901",
     "nome": "João Silva",
     "placa": "ABC1234",
     "cep": "01234567",
     "email": "joao@email.com",
     "celular": "11999999999"
   }
   ```

2. **CPF inválido**
   ```json
   {
     "cpf": "00000000000",
     "nome": "João Silva",
     "placa": "ABC1234",
     "cep": "01234567"
   }
   ```

3. **Placa inválida**
   ```json
   {
     "cpf": "12345678901",
     "nome": "João Silva",
     "placa": "XXX0000",
     "cep": "01234567"
   }
   ```

4. **CEP inválido**
   ```json
   {
     "cpf": "12345678901",
     "nome": "João Silva",
     "placa": "ABC1234",
     "cep": "00000000"
   }
   ```

5. **Campos obrigatórios ausentes**
   ```json
   {
     "nome": "João Silva"
   }
   ```

**Comandos de Teste**:
```bash
# Teste 1: Dados válidos
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

# Teste 2: CPF inválido
curl -X POST http://localhost/api/rpa/start \
  -H "Content-Type: application/json" \
  -d '{
    "cpf": "00000000000",
    "nome": "João Silva",
    "placa": "ABC1234",
    "cep": "01234567"
  }'
```

**Critérios de Sucesso**:
- Dados válidos: Status 200, session_id retornado
- Dados inválidos: Status 400, mensagem de erro específica
- Validação de CPF, placa, CEP funcionando
- Campos obrigatórios validados

#### 1.2 Testes de Monitoramento
**Objetivo**: Validar sistema de monitoramento em tempo real

**Cenários**:
1. **Session ID válido**
2. **Session ID inválido**
3. **Session ID inexistente**
4. **Arquivos JSON ausentes**
5. **Arquivos JSON corrompidos**

**Comandos de Teste**:
```bash
# Teste 1: Session ID válido
curl -X GET http://localhost/api/rpa/progress/rpa_v4_20250930_201530_abc123

# Teste 2: Session ID inválido
curl -X GET http://localhost/api/rpa/progress/invalid_session_id

# Teste 3: Session ID inexistente
curl -X GET http://localhost/api/rpa/progress/rpa_v4_20250930_201530_nonexistent
```

**Critérios de Sucesso**:
- Session ID válido: Status 200, dados de progresso
- Session ID inválido: Status 400, mensagem de erro
- Session ID inexistente: Status 200, status inicial
- Tratamento de erros adequado

#### 1.3 Testes de Fallback
**Objetivo**: Validar estratégia conservadora com fallback

**Cenários**:
1. **Dados JSON válidos** (deve usar JSON dinâmico)
2. **Dados JSON inválidos** (deve usar fallback)
3. **Dados vazios** (deve usar fallback)
4. **parametros.json ausente** (deve falhar graciosamente)

**Comandos de Teste**:
```bash
# Teste 1: Dados JSON válidos
curl -X POST http://localhost/api/rpa/start \
  -H "Content-Type: application/json" \
  -d '{
    "cpf": "12345678901",
    "nome": "João Silva",
    "placa": "ABC1234",
    "cep": "01234567"
  }'

# Teste 2: Dados JSON inválidos
curl -X POST http://localhost/api/rpa/start \
  -H "Content-Type: application/json" \
  -d '{
    "cpf": "00000000000",
    "placa": "XXX0000"
  }'

# Teste 3: Dados vazios
curl -X POST http://localhost/api/rpa/start \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Critérios de Sucesso**:
- Dados válidos: Usa JSON dinâmico, log confirma
- Dados inválidos: Usa fallback, log confirma
- Dados vazios: Usa fallback, log confirma
- Fallback funcionando corretamente

### Fase 2: Testes de Integração (3 dias)

#### 2.1 Testes de API Completa
**Objetivo**: Validar fluxo completo da API

**Cenários**:
1. **Fluxo completo com dados válidos**
2. **Fluxo completo com fallback**
3. **Monitoramento em tempo real**
4. **Múltiplas sessões simultâneas**

**Comandos de Teste**:
```bash
# Teste 1: Fluxo completo
# 1. Iniciar RPA
SESSION_ID=$(curl -X POST http://localhost/api/rpa/start \
  -H "Content-Type: application/json" \
  -d '{
    "cpf": "12345678901",
    "nome": "João Silva",
    "placa": "ABC1234",
    "cep": "01234567",
    "email": "joao@email.com",
    "celular": "11999999999"
  }' | jq -r '.session_id')

# 2. Monitorar progresso
curl -X GET http://localhost/api/rpa/progress/$SESSION_ID

# 3. Verificar logs
curl -X GET http://localhost/api/rpa/logs/$SESSION_ID

# 4. Verificar métricas
curl -X GET http://localhost/api/rpa/metrics

# 5. Health check
curl -X GET http://localhost/api/rpa/health
```

**Critérios de Sucesso**:
- RPA inicia com sucesso
- Progress tracker atualiza corretamente
- Estimativas capturadas na Tela 4
- Resultados finais na Tela 15
- Logs estruturados
- Métricas atualizadas
- Health check OK

#### 2.2 Testes de Script Python
**Objetivo**: Validar scripts Python modificados

**Cenários**:
1. **executar_rpa_imediato_playwright.py com --data**
2. **executar_rpa_imediato_playwright.py com --config**
3. **executar_rpa_modular_telas_1_a_5.py com --data**
4. **executar_rpa_modular_telas_1_a_5.py com --config**

**Comandos de Teste**:
```bash
# Teste 1: Arquivo principal com JSON dinâmico
cd /opt/imediatoseguros-rpa
/opt/imediatoseguros-rpa/venv/bin/python executar_rpa_imediato_playwright.py \
  --data '{"cpf":"12345678901","nome":"João Silva","placa":"ABC1234","cep":"01234567"}' \
  --session teste_principal_json

# Teste 2: Arquivo principal com fallback
/opt/imediatoseguros-rpa/venv/bin/python executar_rpa_imediato_playwright.py \
  --config /opt/imediatoseguros-rpa/parametros.json \
  --session teste_principal_fallback

# Teste 3: Arquivo modular com JSON dinâmico
/opt/imediatoseguros-rpa/venv/bin/python executar_rpa_modular_telas_1_a_5.py \
  --data '{"cpf":"12345678901","nome":"João Silva","placa":"ABC1234","cep":"01234567"}' \
  --session teste_modular_json

# Teste 4: Arquivo modular com fallback
/opt/imediatoseguros-rpa/venv/bin/python executar_rpa_modular_telas_1_a_5.py \
  --config /opt/imediatoseguros-rpa/parametros.json \
  --session teste_modular_fallback
```

**Critérios de Sucesso**:
- Scripts executam sem erros
- Progress tracker atualiza
- Estimativas capturadas
- Logs gerados corretamente
- Fallback funcionando

#### 2.3 Testes de Dashboard
**Objetivo**: Validar dashboard web

**Cenários**:
1. **Carregamento inicial**
2. **Criação de nova sessão**
3. **Monitoramento em tempo real**
4. **Exibição de estimativas**
5. **Exibição de resultados finais**

**Comandos de Teste**:
```bash
# Teste 1: Acessar dashboard
curl -X GET http://localhost/dashboard.html

# Teste 2: Verificar JavaScript
curl -X GET http://localhost/js/dashboard.js

# Teste 3: Verificar integração Webflow
curl -X GET http://localhost/js/webflow-integration.js
```

**Critérios de Sucesso**:
- Dashboard carrega corretamente
- JavaScript sem erros
- Polling automático funcionando
- Estimativas exibidas
- Resultados finais exibidos

### Fase 3: Testes de Compatibilidade (2 dias)

#### 3.1 Testes V3 vs V4
**Objetivo**: Validar compatibilidade entre V3 e V4

**Cenários**:
1. **V3 com parametros.json**
2. **V4 com parametros.json (fallback)**
3. **V4 com JSON dinâmico**
4. **Comparação de resultados**

**Comandos de Teste**:
```bash
# Teste 1: V3 tradicional
cd /opt/imediatoseguros-rpa
/opt/imediatoseguros-rpa/venv/bin/python executar_rpa_v3.php

# Teste 2: V4 com fallback
curl -X POST http://localhost/api/rpa/start \
  -H "Content-Type: application/json" \
  -d '{}'

# Teste 3: V4 com JSON dinâmico
curl -X POST http://localhost/api/rpa/start \
  -H "Content-Type: application/json" \
  -d '{
    "cpf": "12345678901",
    "nome": "João Silva",
    "placa": "ABC1234",
    "cep": "01234567"
  }'
```

**Critérios de Sucesso**:
- V3 funciona normalmente
- V4 com fallback = V3
- V4 com JSON dinâmico = V3
- Resultados idênticos
- Compatibilidade total

#### 3.2 Testes de Migração
**Objetivo**: Validar migração do modular para principal

**Cenários**:
1. **Modular (5 telas)**
2. **Principal (15 telas)**
3. **Comparação de funcionalidades**
4. **Validação de estimativas**

**Comandos de Teste**:
```bash
# Teste 1: Modular
/opt/imediatoseguros-rpa/venv/bin/python executar_rpa_modular_telas_1_a_5.py \
  --config /opt/imediatoseguros-rpa/parametros.json \
  --session teste_modular

# Teste 2: Principal
/opt/imediatoseguros-rpa/venv/bin/python executar_rpa_imediato_playwright.py \
  --config /opt/imediatoseguros-rpa/parametros.json \
  --session teste_principal

# Teste 3: Comparar resultados
diff /opt/imediatoseguros-rpa/rpa_data/progress_teste_modular.json \
     /opt/imediatoseguros-rpa/rpa_data/progress_teste_principal.json
```

**Critérios de Sucesso**:
- Modular executa 5 telas
- Principal executa 15 telas
- Estimativas capturadas em ambos
- Progress tracker funcionando
- Migração bem-sucedida

### Fase 4: Testes de Performance (2 dias)

#### 4.1 Testes de Carga
**Objetivo**: Validar performance sob carga

**Cenários**:
1. **1 sessão simultânea**
2. **5 sessões simultâneas**
3. **10 sessões simultâneas**
4. **20 sessões simultâneas**

**Comandos de Teste**:
```bash
# Teste 1: 1 sessão
time curl -X POST http://localhost/api/rpa/start \
  -H "Content-Type: application/json" \
  -d '{
    "cpf": "12345678901",
    "nome": "João Silva",
    "placa": "ABC1234",
    "cep": "01234567"
  }'

# Teste 2: 5 sessões simultâneas
for i in {1..5}; do
  curl -X POST http://localhost/api/rpa/start \
    -H "Content-Type: application/json" \
    -d '{
      "cpf": "12345678901",
      "nome": "João Silva",
      "placa": "ABC1234",
      "cep": "01234567"
    }' &
done
wait

# Teste 3: 10 sessões simultâneas
for i in {1..10}; do
  curl -X POST http://localhost/api/rpa/start \
    -H "Content-Type: application/json" \
    -d '{
      "cpf": "12345678901",
      "nome": "João Silva",
      "placa": "ABC1234",
      "cep": "01234567"
    }' &
done
wait
```

**Critérios de Sucesso**:
- 1 sessão: < 30 segundos
- 5 sessões: < 2 minutos
- 10 sessões: < 5 minutos
- 20 sessões: < 10 minutos
- Sem erros de timeout
- Performance estável

#### 4.2 Testes de Estabilidade
**Objetivo**: Validar estabilidade em execução prolongada

**Cenários**:
1. **Execução contínua por 1 hora**
2. **Múltiplas sessões por 2 horas**
3. **Monitoramento de recursos**
4. **Detecção de vazamentos de memória**

**Comandos de Teste**:
```bash
# Teste 1: Execução contínua
for i in {1..20}; do
  echo "Execução $i"
  curl -X POST http://localhost/api/rpa/start \
    -H "Content-Type: application/json" \
    -d '{
      "cpf": "12345678901",
      "nome": "João Silva",
      "placa": "ABC1234",
      "cep": "01234567"
    }'
  sleep 180  # 3 minutos entre execuções
done

# Teste 2: Monitoramento de recursos
while true; do
  echo "=== $(date) ==="
  ps aux | grep python | grep -v grep
  free -h
  df -h /opt/imediatoseguros-rpa
  sleep 60
done
```

**Critérios de Sucesso**:
- Execução contínua sem erros
- Recursos estáveis
- Sem vazamentos de memória
- Logs limpos
- Performance consistente

### Fase 5: Testes de Integração Webflow (2 dias)

#### 5.1 Testes de JavaScript
**Objetivo**: Validar integração JavaScript

**Cenários**:
1. **Carregamento do script**
2. **Inicialização da classe**
3. **Criação do modal**
4. **Polling automático**
5. **Exibição de dados**

**Comandos de Teste**:
```bash
# Teste 1: Verificar script
curl -X GET http://localhost/js/webflow-integration.js

# Teste 2: Verificar exemplo
curl -X GET http://localhost/webflow-integration-example.html

# Teste 3: Testar em browser
# Abrir http://localhost/webflow-integration-example.html
# Preencher formulário com dados reais
# Clicar em "Iniciar Cotação"
# Verificar modal e polling
```

**Critérios de Sucesso**:
- Script carrega sem erros
- Modal criado corretamente
- Polling funcionando
- Dados exibidos corretamente
- Tratamento de erros adequado

#### 5.2 Testes de Modal
**Objetivo**: Validar funcionalidade do modal

**Cenários**:
1. **Abertura do modal**
2. **Fechamento do modal**
3. **Atualização em tempo real**
4. **Exibição de estimativas**
5. **Exibição de resultados finais**
6. **Tratamento de erros**

**Comandos de Teste**:
```bash
# Teste 1: Abrir modal
# No browser, executar:
# startRPACotacao({
#   "cpf": "12345678901",
#   "nome": "João Silva",
#   "placa": "ABC1234",
#   "cep": "01234567"
# });

# Teste 2: Verificar polling
# Verificar no console do browser se há requisições a cada 2 segundos

# Teste 3: Verificar estimativas
# Aguardar até Tela 4 e verificar se estimativas aparecem

# Teste 4: Verificar resultados finais
# Aguardar até Tela 15 e verificar se resultados aparecem
```

**Critérios de Sucesso**:
- Modal abre corretamente
- Polling a cada 2 segundos
- Estimativas exibidas na Tela 4
- Resultados finais exibidos na Tela 15
- Erros tratados adequadamente
- Modal fecha corretamente

### Fase 6: Testes de Produção (3 dias)

#### 6.1 Testes de Deploy
**Objetivo**: Validar deploy em produção

**Cenários**:
1. **Deploy sem downtime**
2. **Verificação de serviços**
3. **Testes de conectividade**
4. **Validação de configurações**

**Comandos de Teste**:
```bash
# Teste 1: Verificar serviços
systemctl status nginx
systemctl status php8.3-fpm
systemctl status redis

# Teste 2: Verificar conectividade
curl -X GET http://37.27.92.160/api/rpa/health
curl -X GET http://37.27.92.160/dashboard.html

# Teste 3: Verificar logs
tail -f /var/log/nginx/rpa-v4.access.log
tail -f /var/log/nginx/rpa-v4.error.log
tail -f /opt/imediatoseguros-rpa-v4/logs/rpa/app.log
```

**Critérios de Sucesso**:
- Serviços ativos
- Conectividade OK
- Logs limpos
- Configurações corretas
- Deploy sem erros

#### 6.2 Testes de Monitoramento
**Objetivo**: Validar monitoramento em produção

**Cenários**:
1. **Health checks**
2. **Métricas de sistema**
3. **Logs estruturados**
4. **Alertas automáticos**

**Comandos de Teste**:
```bash
# Teste 1: Health check
curl -X GET http://37.27.92.160/api/rpa/health

# Teste 2: Métricas
curl -X GET http://37.27.92.160/api/rpa/metrics

# Teste 3: Sessões
curl -X GET http://37.27.92.160/api/rpa/sessions

# Teste 4: Monitoramento de recursos
htop
iotop
netstat -tulpn
```

**Critérios de Sucesso**:
- Health check OK
- Métricas atualizadas
- Sessões listadas
- Recursos estáveis
- Monitoramento ativo

#### 6.3 Testes de Rollback
**Objetivo**: Validar capacidade de rollback

**Cenários**:
1. **Rollback para V3**
2. **Rollback para V4.0.1**
3. **Verificação de funcionalidade**
4. **Restauração de dados**

**Comandos de Teste**:
```bash
# Teste 1: Backup atual
cp -r /opt/imediatoseguros-rpa-v4 /opt/imediatoseguros-rpa-v4.backup

# Teste 2: Rollback para V3
# Restaurar configuração V3
# Reiniciar serviços

# Teste 3: Verificar funcionamento
curl -X GET http://37.27.92.160/health

# Teste 4: Restaurar V4.1.0
# Restaurar backup
# Reiniciar serviços
```

**Critérios de Sucesso**:
- Rollback executado
- V3 funcionando
- V4.1.0 restaurada
- Dados preservados
- Serviços estáveis

## Cronograma de Execução

### Semana 1: Testes Unitários e Integração
- **Dia 1**: Testes de validação e monitoramento
- **Dia 2**: Testes de fallback e API completa
- **Dia 3**: Testes de script Python e dashboard
- **Dia 4**: Testes de compatibilidade V3 vs V4
- **Dia 5**: Testes de migração e performance

### Semana 2: Testes de Performance e Webflow
- **Dia 1**: Testes de carga e estabilidade
- **Dia 2**: Testes de JavaScript e modal
- **Dia 3**: Testes de deploy e monitoramento
- **Dia 4**: Testes de rollback e validação final
- **Dia 5**: Documentação e relatório final

## Critérios de Aprovação

### Critérios Obrigatórios
- ✅ **Compatibilidade total** com V3
- ✅ **Fallback automático** funcionando
- ✅ **Dados reais** validados
- ✅ **Monitoramento em tempo real** ativo
- ✅ **Integração Webflow** funcionando
- ✅ **Validação robusta** implementada
- ✅ **Performance estável** sob carga
- ✅ **Rollback** testado e funcionando

### Critérios de Qualidade
- ✅ **Cobertura de testes** > 90%
- ✅ **Tempo de resposta** < 2 segundos
- ✅ **Disponibilidade** > 99.9%
- ✅ **Logs estruturados** e limpos
- ✅ **Métricas** atualizadas
- ✅ **Documentação** completa

### Critérios de Produção
- ✅ **Deploy sem downtime**
- ✅ **Monitoramento ativo**
- ✅ **Backup e restore** testados
- ✅ **Segurança** validada
- ✅ **Escalabilidade** comprovada
- ✅ **Manutenibilidade** garantida

## Relatório Final

### Template de Relatório
```markdown
# Relatório de Testes RPA V4.1.0

## Resumo Executivo
- **Data**: [DATA]
- **Versão**: 4.1.0
- **Status**: [APROVADO/REPROVADO]
- **Cobertura**: [%]
- **Tempo Total**: [HORAS]

## Resultados por Fase
### Fase 1: Testes Unitários
- **Status**: [APROVADO/REPROVADO]
- **Testes Executados**: [X/Y]
- **Falhas**: [X]
- **Observações**: [TEXTO]

### Fase 2: Testes de Integração
- **Status**: [APROVADO/REPROVADO]
- **Testes Executados**: [X/Y]
- **Falhas**: [X]
- **Observações**: [TEXTO]

### Fase 3: Testes de Compatibilidade
- **Status**: [APROVADO/REPROVADO]
- **Testes Executados**: [X/Y]
- **Falhas**: [X]
- **Observações**: [TEXTO]

### Fase 4: Testes de Performance
- **Status**: [APROVADO/REPROVADO]
- **Testes Executados**: [X/Y]
- **Falhas**: [X]
- **Observações**: [TEXTO]

### Fase 5: Testes de Integração Webflow
- **Status**: [APROVADO/REPROVADO]
- **Testes Executados**: [X/Y]
- **Falhas**: [X]
- **Observações**: [TEXTO]

### Fase 6: Testes de Produção
- **Status**: [APROVADO/REPROVADO]
- **Testes Executados**: [X/Y]
- **Falhas**: [X]
- **Observações**: [TEXTO]

## Problemas Identificados
### Críticos
- [ ] [PROBLEMA 1]
- [ ] [PROBLEMA 2]

### Importantes
- [ ] [PROBLEMA 1]
- [ ] [PROBLEMA 2]

### Menores
- [ ] [PROBLEMA 1]
- [ ] [PROBLEMA 2]

## Recomendações
1. [RECOMENDAÇÃO 1]
2. [RECOMENDAÇÃO 2]
3. [RECOMENDAÇÃO 3]

## Conclusão
[TEXTO DA CONCLUSÃO]

## Aprovação para Produção
- [ ] **APROVADO** - Pode ser deployado em produção
- [ ] **REPROVADO** - Necessita correções antes do deploy

**Responsável**: [NOME]
**Data**: [DATA]
**Assinatura**: [ASSINATURA]
```

## Ferramentas de Teste

### Ferramentas Automatizadas
- **curl**: Testes de API
- **jq**: Processamento de JSON
- **bash**: Scripts de teste
- **htop**: Monitoramento de recursos
- **netstat**: Verificação de conectividade

### Ferramentas de Monitoramento
- **Nginx logs**: Logs de acesso e erro
- **PHP logs**: Logs da aplicação
- **System logs**: Logs do sistema
- **Redis logs**: Logs do cache

### Ferramentas de Validação
- **Browser DevTools**: Testes de JavaScript
- **Postman**: Testes de API
- **JMeter**: Testes de carga
- **Selenium**: Testes automatizados

## Contatos e Responsabilidades

### Equipe de Testes
- **Líder**: [NOME]
- **Desenvolvedor**: [NOME]
- **QA**: [NOME]
- **DevOps**: [NOME]

### Escalação
- **Nível 1**: Equipe de Testes
- **Nível 2**: Líder Técnico
- **Nível 3**: Gerente de Projeto
- **Nível 4**: Diretor Técnico

### Contatos de Emergência
- **Telefone**: [NÚMERO]
- **Email**: [EMAIL]
- **Slack**: [CANAL]
- **WhatsApp**: [GRUPO]

---

**Documento**: Plano de Testes RPA V4.1.0  
**Versão**: 1.0  
**Data**: 30/09/2025  
**Status**: Aprovado  
**Próxima Revisão**: 07/10/2025
