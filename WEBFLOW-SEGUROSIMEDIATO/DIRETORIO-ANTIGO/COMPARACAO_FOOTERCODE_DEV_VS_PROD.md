# COMPARAÇÃO: FooterCodeSiteDefinitivoCompleto.js (DEV vs PROD)

**Data da Análise:** 02/11/2025  
**Arquivo DEV:** `FooterCodeSiteDefinitivoCompleto.js` (1.772 linhas)  
**Arquivo PROD:** `FooterCodeSiteDefinitivoCompleto_prod.js` (1.785 linhas)  
**Diferença:** +13 linhas no arquivo de produção

---

## 📊 RESUMO EXECUTIVO

### **Alterações Identificadas:**

1. ✅ **Parametrizações esperadas** (migração de ambiente)
   - URLs atualizadas para produção
   - Headers de versão atualizados
   - Comentários de ambiente atualizados

2. ⚠️ **Alterações além das parametrizações:**
   - **REORDENAÇÃO DE CONSTANTES GLOBAIS** (correção de bug)
   - **URL DO MODAL WHATSAPP** (workaround temporário)

---

## 🔍 ANÁLISE DETALHADA

### **1. PARAMETRIZAÇÕES DE MIGRAÇÃO (Esperadas)**

#### 1.1. Header do Arquivo
**DEV:**
```javascript
* ÚLTIMA ALTERAÇÃO: 01/11/2025 10:12
* VERSÃO: 1.3 - Correção da captura de GCLID
* Localização: https://dev.bpsegurosimediato.com.br/webhooks/FooterCodeSiteDefinitivoCompleto.js
* ⚠️ AMBIENTE: DEV
```

**PROD:**
```javascript
* ÚLTIMA ALTERAÇÃO: 02/11/2025 09:42
* VERSÃO: 1.3_PROD - Versão de Produção
* Localização: https://bpsegurosimediato.com.br/webhooks/FooterCodeSiteDefinitivoCompleto_prod.js
* ⚠️ AMBIENTE: PRODUÇÃO
```

**✅ Status:** Esperado - Parametrização normal de migração

---

#### 1.2. Comentários de Credenciais
**DEV:**
```javascript
* - SafetyMails Ticket: fc5e18c10c4aa883b2c31a305f1c09fea3834138
* - SafetyMails API Key: 20a7a1c297e39180bd80428ac13c363e882a531f
```

**PROD:**
```javascript
* - SafetyMails Ticket: fc5e18c10c4aa883b2c31a305f1c09fea3834138 (mesmo que DEV)
* - SafetyMails API Key: 20a7a1c297e39180bd80428ac13c363e882a531f (mesmo que DEV)
```

**✅ Status:** Esperado - Mesmas credenciais (conforme documentado)

---

### **2. ALTERAÇÕES ALÉM DAS PARAMETRIZAÇÕES**

#### 2.1. ⚠️ REORDENAÇÃO DE CONSTANTES GLOBAIS (CORREÇÃO DE BUG)

**Problema Identificado:**
No arquivo DEV, as constantes globais eram definidas **DEPOIS** do início do IIFE do Footer Code Utils, causando aviso "Constantes faltando" quando o Utils verificava sua existência.

**DEV (Linha ~702):**
```javascript
    // ======================
    // PARTE 2: FOOTER CODE PRINCIPAL (modificado)
    // ======================
    
    // Constantes globais (expor ANTES de qualquer uso - Recomendação do Engenheiro)
    // ⚠️ AMBIENTE: DEV (segurosimediato dev)
    window.USE_PHONE_API = true;
    window.APILAYER_KEY = 'dce92fa84152098a3b5b7b8db24debbc';
    window.SAFETY_TICKET = 'fc5e18c10c4aa883b2c31a305f1c09fea3834138'; // DEV: segurosimediato dev
    window.SAFETY_API_KEY = '20a7a1c297e39180bd80428ac13c363e882a531f'; // Mesmo para DEV e PROD
    window.VALIDAR_PH3A = false;
```

**Estrutura DEV:**
```
1. Tratamento de erro global (try { ... })
2. Footer Code Utils IIFE (começa na linha ~53)
   - console.log('🔄 [UTILS] Carregando Footer Code Utils...') // linha ~56
   - Verifica constantes (linha ~681)
3. PARTE 2 (linha ~698)
   - Constantes definidas aqui (linha ~702) ← PROBLEMA: DEPOIS da verificação
```

**PROD (Linha ~63-72):**
```javascript
  // ======================
  // CONSTANTES GLOBAIS (definir ANTES de qualquer uso)
  // ======================
  // ⚠️ AMBIENTE: PRODUÇÃO
  window.USE_PHONE_API = true;
  window.APILAYER_KEY = 'dce92fa84152098a3b5b7b8db24debbc'; // Mesmo para DEV e PROD
  window.SAFETY_TICKET = 'fc5e18c10c4aa883b2c31a305f1c09fea3834138'; // PROD: Mesmo que DEV
  window.SAFETY_API_KEY = '20a7a1c297e39180bd80428ac13c363e882a531f'; // PROD: Mesmo que DEV
  window.VALIDAR_PH3A = false;
  // ======================
  
  console.log('🔄 [UTILS] Carregando Footer Code Utils...'); // linha ~74
```

**Estrutura PROD:**
```
1. Tratamento de erro global (try { ... })
2. Footer Code Utils IIFE (começa na linha ~60)
   - Constantes definidas ANTES (linha ~63-72) ← CORREÇÃO
   - console.log('🔄 [UTILS] Carregando Footer Code Utils...') // linha ~74
   - Verifica constantes (linha ~699)
3. PARTE 2 (linha ~708)
   - NÃO redefine constantes (já definidas antes)
```

**✅ Status:** Correção necessária aplicada em PROD  
**🎯 Motivo:** Resolver aviso "Constantes faltando" no console  
**📌 Impacto:** Positivo - Elimina avisos e garante disponibilidade das constantes quando o Utils verifica

---

#### 2.2. ⚠️ URL DO MODAL WHATSAPP (WORKAROUND TEMPORÁRIO)

**DEV (Linha ~1019):**
```javascript
        script.src = 'https://dev.bpsegurosimediato.com.br/webhooks/MODAL_WHATSAPP_DEFINITIVO.js?v=23&force=' + Math.random();
```

**PROD (Linha ~1032):**
```javascript
        console.log('🔄 [MODAL] Carregando modal de dev.bpsegurosimediato.com.br...');
        // TEMPORÁRIO: Usando diretório dev enquanto corrigimos nginx de produção
        script.src = 'https://dev.bpsegurosimediato.com.br/webhooks/MODAL_WHATSAPP_DEFINITIVO.js?v=23&force=' + Math.random();
```

**✅ Status:** Workaround temporário documentado  
**🎯 Motivo:** Nginx de produção não está servindo arquivos JS de `/webhooks/` (problema identificado e planejado para correção)  
**📌 Impacto:** Temporário - Modal funciona usando diretório DEV enquanto aguarda correção do Nginx  
**📝 Nota:** Após correção do Nginx, deve ser atualizado para:
```javascript
script.src = 'https://bpsegurosimediato.com.br/webhooks/MODAL_WHATSAPP_DEFINITIVO.js?v=23&force=' + Math.random();
```

---

## 📋 COMPARAÇÃO LINHA POR LINHA (Principais Diferenças)

| Linha | DEV | PROD | Tipo | Status |
|-------|-----|------|------|--------|
| **Header** | `VERSÃO: 1.3` | `VERSÃO: 1.3_PROD` | Parametrização | ✅ Esperado |
| **Header** | `Localização: dev.bp...` | `Localização: bp...` | Parametrização | ✅ Esperado |
| **Header** | `⚠️ AMBIENTE: DEV` | `⚠️ AMBIENTE: PRODUÇÃO` | Parametrização | ✅ Esperado |
| **~63** | (não existe) | **Constantes globais definidas ANTES do Utils** | Reordenação | ⚠️ Correção de bug |
| **~56 vs ~74** | `console.log` antes das constantes | `console.log` depois das constantes | Reordenação | ⚠️ Correção de bug |
| **~702** | Constantes definidas aqui | (não redefinidas - já estão antes) | Reordenação | ⚠️ Correção de bug |
| **~1019 vs ~1032** | URL modal: `dev.bp...` | URL modal: `dev.bp...` + comentário temporário | Workaround | ⚠️ Temporário |

---

## ✅ CONCLUSÃO

### **Alterações Apropriadas:**

1. **✅ Reordenação de Constantes Globais**
   - **Motivo:** Correção de bug (aviso "Constantes faltando")
   - **Necessário:** Sim, é uma melhoria importante
   - **Recomendação:** Aplicar a mesma correção no arquivo DEV para manter consistência

2. **✅ Workaround Modal WhatsApp**
   - **Motivo:** Problema temporário com Nginx em produção
   - **Necessário:** Sim, enquanto aguarda correção do Nginx
   - **Recomendação:** Após correção do Nginx, atualizar para URL de produção

### **Alterações Apenas Parametrização:**

- ✅ Headers de versão
- ✅ URLs de localização
- ✅ Comentários de ambiente
- ✅ Mesmas credenciais (conforme esperado)

---

## 🎯 RECOMENDAÇÕES

### **1. Sincronizar Correção de Constantes Globais**

O arquivo DEV ainda tem o problema de constantes definidas depois da verificação. Recomenda-se aplicar a mesma correção:

**Ação:** Mover definição de constantes globais para ANTES do `console.log('🔄 [UTILS] Carregando...')` no arquivo DEV.

### **2. Atualizar Modal WhatsApp Após Correção do Nginx**

Após correção do problema do Nginx (planejada para a semana), atualizar URL do modal:

**De:**
```javascript
script.src = 'https://dev.bpsegurosimediato.com.br/webhooks/MODAL_WHATSAPP_DEFINITIVO.js?v=23&force=' + Math.random();
```

**Para:**
```javascript
script.src = 'https://bpsegurosimediato.com.br/webhooks/MODAL_WHATSAPP_DEFINITIVO.js?v=23&force=' + Math.random();
```

---

## 📊 ESTATÍSTICAS

- **Linhas DEV:** 1.772
- **Linhas PROD:** 1.785
- **Diferença:** +13 linhas
- **Diferenças funcionais:** 2 (reordenação de constantes + workaround modal)
- **Diferenças de parametrização:** Todas as esperadas para migração

---

**Análise concluída em:** 02/11/2025  
**Status geral:** ✅ Alterações apropriadas - apenas correções de bug e workaround temporário documentado


