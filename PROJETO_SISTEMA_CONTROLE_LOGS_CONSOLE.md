# PROJETO: SISTEMA DE CONTROLE UNIFICADO DE LOGS DO CONSOLE

**Data de Criação:** 30/10/2025 23:35  
**Status:** Planejamento (NÃO EXECUTAR)  
**Workspace:** imediatoseguros-rpa-playwright

---

## 📋 OBJETIVO

Implementar um sistema unificado de controle de logs do console no arquivo `FooterCodeSiteDefinitivoCompleto.js`, permitindo habilitar/desabilitar todos os logs através de uma variável hardcode definida no início do arquivo, com suporte a níveis de log e filtros por categoria.

---

## 🎯 PROBLEMA ATUAL

O arquivo `FooterCodeSiteDefinitivoCompleto.js` possui **115 ocorrências** de `console.log`, `console.error`, `console.warn` espalhadas por todo o código.

**IMPORTANTE:** A função `logDebug()` (linhas 727-788) contém **13 ocorrências** que **NÃO serão substituídas**, pois esta função será utilizada posteriormente para mapear o fluxo da chamada do RPA e deve permanecer intacta.

**Total a substituir:** ~102 ocorrências (115 - 13 dentro de `logDebug()`)

**Problemas que isso causa:**
- **Desenvolvimento:** Logs excessivos em produção atrapalham o console do navegador
- **Performance:** Console.logs em produção podem impactar performance em alguns navegadores
- **Debugging:** Dificuldade para filtrar logs relevantes durante debugging
- **Manutenção:** Não há forma centralizada de controlar o nível de verbosidade

**Exemplos de logs encontrados:**
- `console.log('🔄 [UTILS] Carregando Footer Code Utils...')`
- `console.error('❌ [UTILS] Funções de CPF não disponíveis')`
- `console.warn('⚠️ [UTILS] VALIDAR_PH3A não disponível')`
- `console.log('[LOG DEBUG] Status: ${response.status}')`

---

## 📁 ARQUIVOS ENVOLVIDOS

### Arquivos a Modificar:
1. `02-DEVELOPMENT/custom-codes/FooterCodeSiteDefinitivoCompleto.js`
   - Adicionar sistema de controle de logs no início
   - Substituir todas as ocorrências de `console.log/error/warn/info` pela função unificada

### Backups a Criar:
- ✅ `FooterCodeSiteDefinitivoCompleto.js.backup_YYYYMMDD_HHMMSS`

### Destino no Servidor:
- `/var/www/html/dev/webhooks/FooterCodeSiteDefinitivoCompleto.js`

---

## 🔧 FASE 1: IMPLEMENTAÇÃO DO SISTEMA DE CONTROLE DE LOGS

### 1.1. Sistema Proposto

**⚠️ ATENÇÃO: Após revisão técnica, a solução foi ajustada para uma versão intermediária (ver seção REVISÃO TÉCNICA).**

**Solução Intermediária (Aprovada após revisão):**

```javascript
// ======================
// SISTEMA DE CONTROLE DE LOGS
// ======================
// Controle global de logs - alterar conforme necessário
window.DEBUG_CONFIG = {
  // Nível global: 'none' | 'error' | 'warn' | 'info' | 'debug' | 'all'
  level: 'info',
  
  // Habilitar/desabilitar logs completamente
  enabled: true,
  
  // Categorias a ignorar (array vazio = nenhuma ignorada)
  exclude: [], // Exemplo: ['DEBUG'] = ignora esta categoria
  
  // Ambiente (auto-detectado uma vez, depois cached)
  environment: 'auto' // 'auto' | 'dev' | 'prod'
};

// Cache para ambiente detectado (otimização de performance)
let _envCache = null;

// Função unificada de log
window.logUnified = function(level, category, message, data) {
  const config = window.DEBUG_CONFIG || {};
  
  // Se desabilitado globalmente, retornar imediatamente
  if (config.enabled === false) return;
  
  // Auto-detectar ambiente UMA VEZ (cache para performance)
  if (config.environment === 'auto' && _envCache === null) {
    _envCache = (window.location.hostname.includes('webflow.io') || 
                 window.location.hostname.includes('localhost') ||
                 window.location.hostname.includes('dev.')) ? 'dev' : 'prod';
  }
  
  const env = (config.environment === 'auto') ? _envCache : config.environment;
  
  // Em produção, usar nível mais restritivo se não especificado
  if (env === 'prod' && !config.level) {
    config.level = 'error';
  }
  
  // Mapeamento de níveis (ordem de prioridade)
  const levels = { 'none': 0, 'error': 1, 'warn': 2, 'info': 3, 'debug': 4, 'all': 5 };
  const currentLevel = levels[config.level] || levels['info'];
  const messageLevel = levels[level] || levels['info'];
  
  // Verificar se deve exibir o log baseado no nível
  if (messageLevel > currentLevel) return;
  
  // Verificar exclusão de categoria (apenas um tipo de filtro para simplicidade)
  if (config.exclude && config.exclude.length > 0) {
    if (category && config.exclude.includes(category)) return;
  }
  
  // Formatar mensagem com categoria
  const formattedMessage = category ? `[${category}] ${message}` : message;
  
  // Escolher método de console apropriado
  switch(level) {
    case 'error':
      console.error(formattedMessage, data || '');
      break;
    case 'warn':
      console.warn(formattedMessage, data || '');
      break;
    case 'info':
    case 'debug':
    default:
      console.log(formattedMessage, data || '');
      break;
  }
};

// Aliases para facilitar uso
window.logInfo = (cat, msg, data) => window.logUnified('info', cat, msg, data);
window.logError = (cat, msg, data) => window.logUnified('error', cat, msg, data);
window.logWarn = (cat, msg, data) => window.logUnified('warn', cat, msg, data);
window.logDebug = (cat, msg, data) => window.logUnified('debug', cat, msg, data);
```

### 1.2. Substituições Necessárias

**Padrão de substituição:**

```javascript
// ANTES:
console.log('🔄 [UTILS] Carregando Footer Code Utils...');

// DEPOIS:
window.logInfo('UTILS', 'Carregando Footer Code Utils...');
```

**Exemplos de mapeamento:**

| Original | Novo |
|----------|------|
| `console.log('🔄 [UTILS] ...')` | `window.logInfo('UTILS', '...')` |
| `console.error('❌ [UTILS] ...')` | `window.logError('UTILS', '...')` |
| `console.warn('⚠️ [UTILS] ...')` | `window.logWarn('UTILS', '...')` |
| `console.log('[LOG DEBUG] ...')` | `window.logDebug('DEBUG', '...')` |
| `console.log('✅ [FOOTER] ...')` | `window.logInfo('FOOTER', '...')` |

### 1.3. Regras de Categorização

Baseado nos logs existentes, identificar categorias:

- `UTILS` - Logs do FooterCodeSiteDefinitivoUtils.js
- `FOOTER` - Logs do Footer Code principal
- `MODAL` - Logs relacionados ao modal WhatsApp
- `ESPOCRM` - Logs de integração EspoCRM
- `OCTADESK` - Logs de integração Octadesk
- `GTM` - Logs do Google Tag Manager
- `RPA` - Logs do sistema RPA
- `CONFIG` - Logs de configuração
- `DEBUG` - Logs de debug detalhados
- `STATE` - Logs de estado/estado do localStorage
- `PARALLEL` - Logs de processamento paralelo

---

## 📤 FASE 2: CÓPIA DO ARQUIVO PARA O SERVIDOR

### 2.1. Comando SCP

```bash
scp "02-DEVELOPMENT/custom-codes/FooterCodeSiteDefinitivoCompleto.js" \
    root@46.62.174.150:/var/www/html/dev/webhooks/FooterCodeSiteDefinitivoCompleto.js
```

### 2.2. Verificação

```bash
curl -I https://dev.bpsegurosimediato.com.br/webhooks/FooterCodeSiteDefinitivoCompleto.js
```

**Verificar:**
- Status HTTP 200
- Content-Type: `application/javascript`
- Tamanho do arquivo atualizado

---

## 🧪 FASE 3: TESTE E VERIFICAÇÃO

### 3.1. Testes de Controle

**Teste 1: Logs Desabilitados**
```javascript
// No início do arquivo, alterar:
window.DEBUG_CONFIG = { enabled: false };
// Resultado esperado: Nenhum log no console
```

**Teste 2: Nível 'error' apenas**
```javascript
window.DEBUG_CONFIG = { level: 'error', enabled: true };
// Resultado esperado: Apenas console.error visíveis
```

**Teste 3: Filtrar categoria específica**
```javascript
window.DEBUG_CONFIG = { level: 'all', enabled: true, categories: ['UTILS'] };
// Resultado esperado: Apenas logs da categoria UTILS
```

**Teste 4: Excluir categoria**
```javascript
window.DEBUG_CONFIG = { level: 'all', enabled: true, exclude: ['DEBUG'] };
// Resultado esperado: Todos os logs exceto categoria DEBUG
```

### 3.2. Verificação de Compatibilidade

- [ ] Todos os logs funcionam quando `enabled: true`
- [ ] Nenhum log aparece quando `enabled: false`
- [ ] Níveis de log respeitam a configuração
- [ ] Filtros de categoria funcionam corretamente
- [ ] Código existente continua funcionando normalmente
- [ ] Performance não degrada significativamente

---

## ✅ CHECKLIST DE VERIFICAÇÃO

### Preparação:
- [ ] Backup do arquivo `FooterCodeSiteDefinitivoCompleto.js` criado
- [ ] Contagem de console.log/error/warn realizada (115 total, 102 a substituir, 13 dentro de `logDebug()` a manter)

### Implementação:
- [ ] Sistema de controle de logs adicionado no início do arquivo
- [ ] Função `window.logUnified` implementada
- [ ] Aliases `logInfo`, `logError`, `logWarn`, `logDebug` criados
- [ ] Todas as ocorrências de `console.log` substituídas
- [ ] Todas as ocorrências de `console.error` substituídas
- [ ] Todas as ocorrências de `console.warn` substituídas
- [ ] Categorias identificadas e aplicadas corretamente
- [ ] Emojis removidos ou movidos para dentro da função (opcional)

### Testes:
- [ ] Teste com `enabled: false` - nenhum log
- [ ] Teste com `level: 'error'` - apenas errors
- [ ] Teste com `level: 'all'` - todos os logs
- [ ] Teste com filtro de categoria - apenas categoria específica
- [ ] Teste com exclusão de categoria - categoria excluída não aparece
- [ ] Teste de funcionalidade completa do site

### Deploy:
- [ ] Arquivo copiado para servidor
- [ ] URL testada (200 OK)
- [ ] Content-Type verificado
- [ ] Cache limpo (versão atualizada)

---

## 🔄 ROLLBACK (Se Necessário)

### Procedimento de Reversão:

1. **Restaurar backup:**
   ```bash
   cp FooterCodeSiteDefinitivoCompleto.js.backup_YYYYMMDD_HHMMSS \
      FooterCodeSiteDefinitivoCompleto.js
   ```

2. **Copiar para servidor:**
   ```bash
   scp FooterCodeSiteDefinitivoCompleto.js \
       root@46.62.174.150:/var/www/html/dev/webhooks/FooterCodeSiteDefinitivoCompleto.js
   ```

3. **Verificar funcionamento:**
   - Acessar site no Webflow
   - Verificar console do navegador
   - Confirmar que funcionalidades estão operando

---

## 📊 CRONOGRAMA

1. **Fase 1 - Implementação:** ~1h30min
   - Análise detalhada dos logs existentes: 15min
   - Implementação do sistema de controle: 20min
   - Substituição de todas as ocorrências: 40min
   - Categorização e refinamento: 15min

2. **Fase 2 - Cópia para Servidor:** ~5min
   - Criação de backup: 2min
   - Cópia via SCP: 2min
   - Verificação: 1min

3. **Fase 3 - Testes:** ~30min
   - Testes de controle: 15min
   - Testes de compatibilidade: 10min
   - Verificação final: 5min

**Total Estimado:** ~2h05min

---

## 🎯 RESULTADO ESPERADO

### Benefícios:

1. **Controle Centralizado:**
   - Uma única variável controla todos os logs
   - Fácil ativar/desativar para produção

2. **Níveis de Log:**
   - Controle granular (error, warn, info, debug)
   - Otimização para produção (apenas errors)

3. **Filtros por Categoria:**
   - Foco em categorias específicas durante debugging
   - Exclusão de categorias ruidosas

4. **Auto-Detecção de Ambiente:**
   - Logs mais verbosos em desenvolvimento
   - Logs mínimos em produção (auto)

5. **Manutenibilidade:**
   - Função unificada facilita futuras melhorias
   - Padronização de formato de logs

### Configuração Recomendada:

**Produção:**
```javascript
window.DEBUG_CONFIG = {
  level: 'error',
  enabled: true,
  environment: 'prod'
};
```

**Desenvolvimento:**
```javascript
window.DEBUG_CONFIG = {
  level: 'all',
  enabled: true,
  environment: 'dev'
};
```

**Debug Específico:**
```javascript
window.DEBUG_CONFIG = {
  level: 'all',
  enabled: true,
  categories: ['UTILS', 'MODAL']
};
```

---

## 🔍 REVISÃO TÉCNICA

### Engenheiro de Software: Auto (AI Assistant)
**Data da Revisão:** 31/10/2025 00:15

#### Comentários:

**✅ PONTOS POSITIVOS:**
1. **Problema bem identificado:** 115 ocorrências de console.log/error/warn realmente justificam uma solução unificada
2. **Documentação excelente:** Projeto bem estruturado, com fases claras e checklist completo
3. **Abordagem defensiva:** Consideração de backup, rollback e testes antes de deploy
4. **Flexibilidade:** Solução proposta permite níveis e filtros, mas também oferece alternativa simplificada

**⚠️ PONTOS DE ATENÇÃO IDENTIFICADOS:**

1. **Função `logDebug` existente:** 
   - Há uma função `logDebug()` que envia logs para servidor PHP (`debug_logger_db.php`)
   - Esta função usa `console.log` internamente para feedback imediato
   - **Ação:** Manter compatibilidade com `logDebug()` ou integrar no sistema unificado

2. **Complexidade vs Contexto da Empresa:**
   - Solução proposta é sofisticada (níveis, categorias, auto-detecção)
   - Contexto: empresa pequena, aplicativos não críticos, equipe minúscula
   - **Risco:** Over-engineering para necessidades atuais
   - **Recomendação:** Começar com solução intermediária (não minimalista, mas simplificada)

3. **Performance:**
   - Auto-detecção de ambiente (`window.location.hostname.includes()`) executa a cada log
   - **Otimização:** Cachear resultado da detecção ao invés de verificar sempre
   - **Impacto:** Baixo, mas pode ser otimizado

4. **Emojis nos logs:**
   - Logs atuais usam emojis (🔄, ❌, ⚠️, ✅)
   - **Recomendação:** Manter emojis como opcional na função unificada
   - **Benefício:** Facilita leitura visual durante debugging

5. **Função `logDebug()` existente:**
   - Função `logDebug()` envia logs para servidor PHP (linhas 727-788)
   - **Decisão:** Manter completamente separada do sistema unificado
   - **Razão:** Será utilizada posteriormente para mapear fluxo da chamada do RPA
   - **Ação:** NÃO modificar `logDebug()`, apenas substituir console.log/error/warn que estão fora dela

#### Alterações Recomendadas:

**1. SOLUÇÃO HÍBRIDA (Recomendada):**

Implementar uma versão intermediária que atende necessidades sem complexidade excessiva:

```javascript
// ======================
// SISTEMA DE CONTROLE DE LOGS (Versão Intermediária)
// ======================
window.DEBUG_CONFIG = {
  // Nível global: 'none' | 'error' | 'warn' | 'info' | 'debug' | 'all'
  level: 'info',
  
  // Habilitar/desabilitar logs completamente
  enabled: true,
  
  // Categorias a ignorar (array vazio = nenhuma ignorada)
  exclude: [], // Exemplo: ['DEBUG'] = ignora esta categoria
  
  // Ambiente (auto-detectado uma vez, depois cached)
  environment: 'auto' // 'auto' | 'dev' | 'prod'
};

// Cache para ambiente detectado
let _envCache = null;

// Função unificada de log
window.logUnified = function(level, category, message, data) {
  const config = window.DEBUG_CONFIG || {};
  
  // Se desabilitado globalmente, retornar imediatamente
  if (config.enabled === false) return;
  
  // Auto-detectar ambiente UMA VEZ (cache)
  if (config.environment === 'auto' && _envCache === null) {
    _envCache = (window.location.hostname.includes('webflow.io') || 
                 window.location.hostname.includes('localhost') ||
                 window.location.hostname.includes('dev.')) ? 'dev' : 'prod';
  }
  
  const env = (config.environment === 'auto') ? _envCache : config.environment;
  
  // Em produção, usar nível mais restritivo se não especificado
  if (env === 'prod' && !config.level) {
    config.level = 'error';
  }
  
  // Mapeamento de níveis
  const levels = { 'none': 0, 'error': 1, 'warn': 2, 'info': 3, 'debug': 4, 'all': 5 };
  const currentLevel = levels[config.level] || levels['info'];
  const messageLevel = levels[level] || levels['info'];
  
  // Verificar se deve exibir baseado no nível
  if (messageLevel > currentLevel) return;
  
  // Verificar exclusão de categoria
  if (config.exclude && config.exclude.length > 0) {
    if (category && config.exclude.includes(category)) return;
  }
  
  // Formatar mensagem (manter emojis se presentes na mensagem original)
  const formattedMessage = category ? `[${category}] ${message}` : message;
  
  // Escolher método de console apropriado
  switch(level) {
    case 'error':
      console.error(formattedMessage, data || '');
      break;
    case 'warn':
      console.warn(formattedMessage, data || '');
      break;
    case 'info':
    case 'debug':
    default:
      console.log(formattedMessage, data || '');
      break;
  }
};

// Aliases para facilitar uso
window.logInfo = (cat, msg, data) => window.logUnified('info', cat, msg, data);
window.logError = (cat, msg, data) => window.logUnified('error', cat, msg, data);
window.logWarn = (cat, msg, data) => window.logUnified('warn', cat, msg, data);
window.logDebug = (cat, msg, data) => window.logUnified('debug', cat, msg, data);
```

**Diferenças da solução proposta:**
- ✅ Removido filtro por `categories` (mantém apenas `exclude`)
- ✅ Simplificado: apenas um tipo de filtro
- ✅ Otimizado: cache de detecção de ambiente
- ✅ Mantém níveis de log e controle básico
- ✅ Menos código, mais fácil de manter

**2. FUNÇÃO `logDebug()` PERMANECE SEPARADA:**

**Decisão:** A função `logDebug()` NÃO será modificada ou integrada ao sistema unificado.

**Razão:** Esta função será utilizada posteriormente para mapear o fluxo da chamada do RPA e deve permanecer independente.

**Ação:** 
- NÃO substituir console.log/error/warn que estão **dentro** da função `logDebug()`
- Substituir apenas console.log/error/warn que estão **fora** da função `logDebug()`
- Manter `logDebug()` exatamente como está (linhas 727-788)

**3. MANTER EMOJIS:**

- Não remover emojis das mensagens originais
- Permitir que mensagens venham com emojis já incluídos
- Exemplo: `window.logInfo('UTILS', '🔄 Carregando Footer Code Utils...')`

**4. PRIORIDADE DE SUBSTITUIÇÃO E EXCEÇÕES:**

**Total de logs a substituir:** ~102 ocorrências (115 total - 13 dentro de `logDebug()`)

Ordem sugerida para substituir os logs:
1. **Fase 1:** Logs simples (sem contextos complexos) - ~55 ocorrências
2. **Fase 2:** Logs dentro de funções assíncronas - ~30 ocorrências  
3. **Fase 3:** Logs dentro de funções complexas (exceto `logDebug()`) - ~17 ocorrências

**⚠️ EXCEÇÃO IMPORTANTE:**
- **NÃO substituir** os **13 logs** que estão **dentro** da função `logDebug()` (linhas 727-788)
- Estes logs são: linhas 749, 750, 759, 763, 766, 768, 771, 772, 776, 777, 778, 782, 787
- A função `logDebug()` permanece **completamente intacta**, pois será usada para mapear fluxo RPA
- Manter `logDebug()` exatamente como está, sem qualquer modificação

#### Status da Revisão:
- [x] **Aprovado com alterações**

**Decisão:** Projeto aprovado para execução, mas com a **versão intermediária** ao invés da versão completa. A solução intermediária oferece 80% dos benefícios com 40% da complexidade, alinhada com o contexto da empresa.

**Próximos Passos:**
1. ✅ Projeto atualizado com versão intermediária proposta
2. ✅ Decisão sobre `logDebug()`: manter completamente separada (não unificar)
3. Criar backup do arquivo antes de iniciar
4. Implementar substituição em fases (prioridade sugerida acima)
5. **NÃO modificar** função `logDebug()` (linhas 727-788) - manter intacta
6. Testar localmente antes de deploy

---

## 💡 ALTERNATIVAS E CONSIDERAÇÕES

### Alternativa 1: Solução Minimalista

Se a solução proposta for considerada complexa demais, uma versão simplificada:

```javascript
// Controle simples
window.LOGS_ENABLED = true; // false para desabilitar todos

window.logUnified = function(level, category, message, data) {
  if (!window.LOGS_ENABLED) return;
  
  const prefix = category ? `[${category}]` : '';
  const msg = `${prefix} ${message}`;
  
  if (level === 'error') console.error(msg, data || '');
  else if (level === 'warn') console.warn(msg, data || '');
  else console.log(msg, data || '');
};
```

**Vantagens:**
- Mais simples
- Menos código
- Mais fácil de entender

**Desvantagens:**
- Menos flexível
- Sem filtros por categoria
- Sem níveis granulares

### Alternativa 2: Manter Emojis

**Opção A:** Remover todos os emojis (logs mais limpos)
**Opção B:** Manter emojis na mensagem (mais visual)

**Recomendação:** Manter emojis na mensagem, mas de forma opcional dentro da função.

---

## 📝 NOTAS IMPORTANTES

### ⚠️ PONTOS CRÍTICOS:

1. **SEMPRE criar backup** antes de modificar o arquivo
2. **NUNCA executar** sem aprovação explícita
3. **TESTAR completamente** antes de copiar para servidor
4. **VERIFICAR compatibilidade** - garantir que não quebra funcionalidades existentes

### 📋 PROCEDIMENTOS:

1. Criar backup com data/hora
2. Implementar sistema de controle no início do arquivo
3. Substituir logs sistematicamente (usar busca e substituição com cuidado)
4. Testar localmente antes de deploy
5. Atualizar `PROJETOS_imediatoseguros-rpa-playwright.md` após conclusão

### 🎯 CONTEXTO DA EMPRESA:

- **Empresa pequena** → Solução deve ser simples de entender e manter
- **Aplicativos não críticos** → Foco em simplicidade sobre complexidade
- **Equipe minúscula** → Documentação clara é essencial

---

**Status:** Planejamento (Aguardando Testes do Projeto Anterior)  
**Próxima ação:** Aguardar testes extensivos do Projeto 5 (Unificação Footer Code) e commit no GitHub antes de iniciar implementação


