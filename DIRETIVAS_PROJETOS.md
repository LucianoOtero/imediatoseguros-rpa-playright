# 📋 DIRETIVAS DE GERENCIAMENTO DE PROJETOS

**Criado em:** 30/10/2025 12:05  
**Última atualização:** 31/10/2025 14:30  
**Workspace:** imediatoseguros-rpa-playwright

---

## 🎯 DIRETIVAS OBRIGATÓRIAS

### 1. **Preparação de Projetos**
- Quando solicitado "prepare um projeto", criar documento detalhado **SEM EXECUTAR**
- Incluir backup local de todos os arquivos que serão alterados
- Adicionar data/hora no nome do backup: `arquivo.backup_YYYYMMDD_HHMMSS`
- Referenciar backups na documentação

### 2. **Arquivo de Controle de Projetos**
- Criar/atualizar `PROJETOS_imediatoseguros-rpa-playwright.md`
- Listar todos os projetos com:
  - Nome do projeto
  - Data de início
  - Data de conclusão (quando aplicável)
  - Status (Planejado/Em Andamento/Concluído)
  - Breve descrição
  - Referência ao arquivo do projeto

### 3. **Comentários Padrão em Arquivos JavaScript (.js)**
- **OBRIGATÓRIO:** Incluir no início de cada arquivo `.js` criado/modificado:
- **Formato mínimo para arquivos simples:**
```javascript
/**
 * PROJETO: [NOME_EXATO_DO_PROJETO]
 * INÍCIO: [DD/MM/AAAA HH:MM]
 * ÚLTIMA ALTERAÇÃO: [DD/MM/AAAA HH:MM]
 * 
 * VERSÃO: [X.Y] - [NOME_DESCRITIVO_DA_VERSÃO]
 * 
 * ALTERAÇÕES NESTA VERSÃO:
 * - [Descrição da alteração 1]
 * - [Descrição da alteração 2]
 * - [Descrição da alteração 3]
 */
```

- **Formato completo para arquivos complexos/produção:**
```javascript
/**
 * PROJETO: [NOME_EXATO_DO_PROJETO]
 * INÍCIO: [DD/MM/AAAA HH:MM]
 * ÚLTIMA ALTERAÇÃO: [DD/MM/AAAA HH:MM]
 * 
 * VERSÃO: [X.Y] - [NOME_DESCRITIVO_DA_VERSÃO]
 * 
 * ALTERAÇÕES NESTA VERSÃO:
 * - [Descrição da alteração 1]
 * - [Descrição da alteração 2]
 * - [Descrição da alteração 3]
 * 
 * ARQUIVOS RELACIONADOS:
 * - [Nome do arquivo/documentação relacionada]
 * 
 * LOCAIS DE USO:
 * - [Localização 1]
 * - [Localização 2]
 * 
 * NOTAS IMPORTANTES:
 * - [Nota relevante, se houver]
 */
```

#### **Regras de Versionamento:**
- **Versão inicial:** `1.0` (primeira implementação completa)
- **Correções/melhorias menores:** `1.1`, `1.2`, `1.3...`
- **Novas funcionalidades significativas:** `2.0`, `3.0...`
- **Formato:** `X.Y` onde:
  - `X` = versão principal (mudanças grandes)
  - `Y` = versão secundária (correções, pequenas melhorias)
- **Nome descritivo:** Identificar claramente o que foi implementado na versão
- **Lista de alterações:** Detalhar todas as mudanças relevantes desta versão

#### **Exemplos Práticos:**

**Exemplo 1 - Arquivo simples:**
```javascript
/**
 * PROJETO: CORREÇÃO NA DEFINIÇÃO DOS CAMPOS GCLID
 * INÍCIO: 31/10/2025 13:06
 * ÚLTIMA ALTERAÇÃO: 31/10/2025 13:06
 * 
 * VERSÃO: 1.1 - Correção na definição dos campos gclid
 * 
 * ALTERAÇÕES NESTA VERSÃO:
 * - Implementada verificação defensiva antes de acessar propriedade .value
 * - Adicionada validação de existência de elementos antes de ler valores
 * - Correção do erro "Cannot read properties of null (reading 'value')"
 * - Salvamento no localStorage apenas quando valores são válidos
 */
```

**Exemplo 2 - Arquivo complexo:**
```javascript
/**
 * PROJETO: UNIFICAÇÃO DE ARQUIVOS FOOTER CODE
 * INÍCIO: 30/10/2025 19:55
 * ÚLTIMA ALTERAÇÃO: 31/10/2025 01:30
 * 
 * VERSÃO: 1.1
 * 
 * Arquivo unificado contendo:
 * - FooterCodeSiteDefinitivoUtils.js (Parte 1)
 * - Footer Code Site Definitivo.js (Parte 2 - modificado)
 * 
 * ALTERAÇÕES NESTA VERSÃO:
 * - Integração completa de Utils no arquivo unificado
 * - Implementação de waitForDependencies()
 * - Consolidação do código em função init()
 * - Atualização de credenciais SafetyMails para DEV
 * 
 * Localização: https://dev.bpsegurosimediato.com.br/webhooks/FooterCodeSiteDefinitivoCompleto.js
 * 
 * ⚠️ AMBIENTE: DEV
 * - SafetyMails Ticket: [CREDENTIAL]
 * - SafetyMails API Key: [CREDENTIAL]
 */
```

#### **Atualização de Versão:**
- **SEMPRE atualizar** `ÚLTIMA ALTERAÇÃO` quando houver mudanças
- **SEMPRE incrementar** versão (ex: 1.1 → 1.2)
- **SEMPRE documentar** alterações na lista `ALTERAÇÕES NESTA VERSÃO`
- **MANTER histórico:** Não remover alterações anteriores, apenas adicionar novas

### 4. **Revisão por Engenheiro de Software**
- **SEMPRE** submeter documento do projeto para revisão
- Engenheiro: Especialista em infraestrutura e arquitetura
- Guardar comentários no arquivo do projeto
- Atualizar projeto conforme orientações do engenheiro
- Incluir seção "REVISÃO TÉCNICA" no documento

### 5. **Contexto da Empresa**
- **Empresa pequena** - soluções simples e diretas
- **Aplicativos não críticos** - sem complexidade desnecessária
- **Volumes baixos** - otimizações básicas suficientes
- **Equipe minúscula** - 3 pessoas (desenvolvedor, gestor, engenheiro)
- **Abordagem:** Segurança + Estabilidade + Simplicidade
- **Evitar:** Estruturas complexas para missão crítica/grandes volumes

### 6. **Atualizações de Status**
- Marcar conclusão no arquivo do projeto
- Atualizar `PROJETOS_imediatoseguros-rpa-playwright.md` com data de conclusão
- Incluir briefing sobre o sucesso/resultados

### 7. **Estrutura de Documentos**
- Nome do arquivo: `PROJETO_<NOME_DESCRITIVO>.md`
- Seção de backups obrigatória
- Seção de rollback
- Cronograma detalhado
- Checklist de verificação
- **Seção de revisão técnica obrigatória**

---

## 📁 TEMPLATE DE PROJETO

```markdown
# PROJETO: [NOME_DESCRITIVO]

**Data de Criação:** [DD/MM/AAAA HH:MM]  
**Status:** Planejamento (NÃO EXECUTAR)  
**Workspace:** imediatoseguros-rpa-playwright

---

## 📋 OBJETIVO
[Descrição clara do objetivo]

---

## 🎯 PROBLEMA ATUAL
[Descrição do problema a ser resolvido]

---

## 📁 ARQUIVOS ENVOLVIDOS

### Arquivos a Modificar:
1. `[caminho/arquivo1]`
2. `[caminho/arquivo2]`

### Backups Criados:
- ✅ `arquivo1.backup_YYYYMMDD_HHMMSS`
- ✅ `arquivo2.backup_YYYYMMDD_HHMMSS`

### Destino no Servidor:
- `[caminho/servidor/arquivo1]`
- `[caminho/servidor/arquivo2]`

---

## 🔧 FASE 1: IMPLEMENTAÇÃO DAS ALTERAÇÕES
[Detalhes das alterações]

---

## 📤 FASE 2: CÓPIA DOS ARQUIVOS PARA O SERVIDOR
[Comandos e procedimentos]

---

## 🧪 FASE 3: TESTE E VERIFICAÇÃO
[Procedimentos de teste]

---

## ✅ CHECKLIST DE VERIFICAÇÃO
- [ ] Backups criados
- [ ] Alterações implementadas
- [ ] Arquivos copiados para servidor
- [ ] Testes realizados
- [ ] Documentação atualizada

---

## 🔄 ROLLBACK (Se Necessário)
[Procedimentos de reversão]

---

## 📊 CRONOGRAMA
1. **Fase 1:** [tempo estimado]
2. **Fase 2:** [tempo estimado]
3. **Fase 3:** [tempo estimado]

**Total Estimado:** [tempo total]

---

## 🎯 RESULTADO ESPERADO
[Descrição do resultado final]

---

## 🔍 REVISÃO TÉCNICA

### Engenheiro de Software: [NOME]
**Data da Revisão:** [DD/MM/AAAA HH:MM]

#### Comentários:
- [Comentário 1]
- [Comentário 2]
- [Comentário 3]

#### Alterações Recomendadas:
- [Alteração 1]
- [Alteração 2]
- [Alteração 3]

#### Status da Revisão:
- [ ] Aprovado sem alterações
- [ ] Aprovado com alterações
- [ ] Requer nova revisão

---

## 📝 NOTAS IMPORTANTES

### ⚠️ PONTOS CRÍTICOS:
1. **SEMPRE criar backups** antes de qualquer alteração
2. **NUNCA executar** sem aprovação explícita
3. **SEMPRE documentar** todas as alterações
4. **SEMPRE atualizar** o arquivo de controle de projetos

### 📋 PROCEDIMENTOS:
1. Consultar este arquivo antes de preparar qualquer projeto
2. Seguir o template exato
3. Criar backups com data/hora
4. Atualizar `PROJETOS_imediatoseguros-rpa-playwright.md`
5. Incluir comentários padrão em arquivos modificados **com versionamento completo**
6. **SEMPRE submeter para revisão técnica**
7. **SEMPRE considerar contexto da empresa pequena**
8. **SEMPRE atualizar versão e lista de alterações** ao modificar arquivos `.js`

---

**Status:** Ativo  
**Próxima revisão:** Conforme necessário
