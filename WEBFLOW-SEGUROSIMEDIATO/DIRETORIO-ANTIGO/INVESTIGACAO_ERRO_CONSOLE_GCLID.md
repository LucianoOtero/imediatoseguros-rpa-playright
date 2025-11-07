# 🔍 INVESTIGAÇÃO DE ERRO NO CONSOLE - GCLID

**Data da Investigação:** 31/10/2025 00:45  
**Erro Reportado:**
```
Uncaught TypeError: Cannot read properties of null (reading 'value')
at anchors.<computed>.onclick (?gclid=test-lro-2025-10-30-17-27&v=3:189:70)
```

---

## 📋 ANÁLISE DO ERRO

### **Erro Identificado:**
- **Tipo:** `TypeError: Cannot read properties of null (reading 'value')`
- **Localização:** Handler `onclick` de elementos anchor (`anchors`)
- **Linha Aproximada:** 189 (provavelmente linha 49 do código após formatação)

### **Causa Raiz:**
O erro ocorre no arquivo **`Inside Head Tag Pagina.js`**, nas linhas **48-51**, onde o código acessa propriedades `.value` de elementos que podem não existir na página.

---

## 🐛 CÓDIGO PROBLEMÁTICO

**Arquivo:** `02-DEVELOPMENT/custom-codes/Inside Head Tag Pagina.js`  
**Linhas:** 46-56

```javascript
var anchors = document.querySelectorAll("[whenClicked='set']");
for (var i = 0; i < anchors.length; i++) {
  anchors[i].onclick = function () {
    // ❌ PROBLEMA: Acesso direto a .value sem verificar se elemento existe
    var global_email = document.getElementById("email").value;        // Pode ser null
    var global_gclid = document.getElementById("GCLID_FLD").value;    // Pode ser null
    var global_gclid_wp = document.getElementById("GCLID_FLD_WP").value; // Pode ser null
    
    window.localStorage.setItem("GCLID_FLD", global_gclid);
    window.localStorage.setItem("GCLID_FLD_WP", global_gclid_wp);
    window.localStorage.setItem("EMAIL_FLD", global_email);
  };
}
```

### **O Que Está Errado:**
1. `document.getElementById("email")` pode retornar `null` se o elemento não existir
2. `document.getElementById("GCLID_FLD")` pode retornar `null` se o elemento não existir
3. `document.getElementById("GCLID_FLD_WP")` pode retornar `null` se o elemento não existir
4. Tentar acessar `.value` de `null` causa o erro `TypeError`

### **Cenários Onde Ocorre:**
- Página não possui campo com `id="email"`
- Página não possui campo com `id="GCLID_FLD"`
- Página não possui campo com `id="GCLID_FLD_WP"`
- Elementos existem mas ainda não foram carregados no DOM quando o código executa
- Elementos foram removidos dinamicamente do DOM

---

## ✅ SOLUÇÃO PROPOSTA

### **Opção 1: Verificação Defensiva (Recomendada)**

```javascript
var anchors = document.querySelectorAll("[whenClicked='set']");
for (var i = 0; i < anchors.length; i++) {
  anchors[i].onclick = function () {
    // ✅ Verificar se elemento existe antes de acessar .value
    var emailEl = document.getElementById("email");
    var gclidEl = document.getElementById("GCLID_FLD");
    var gclidWpEl = document.getElementById("GCLID_FLD_WP");
    
    var global_email = emailEl ? emailEl.value : null;
    var global_gclid = gclidEl ? gclidEl.value : null;
    var global_gclid_wp = gclidWpEl ? gclidWpEl.value : null;
    
    // Só salvar se houver valores válidos
    if (global_gclid) {
      window.localStorage.setItem("GCLID_FLD", global_gclid);
    }
    if (global_gclid_wp) {
      window.localStorage.setItem("GCLID_FLD_WP", global_gclid_wp);
    }
    if (global_email) {
      window.localStorage.setItem("EMAIL_FLD", global_email);
    }
  };
}
```

### **Opção 2: Verificação com Fallback (Mais Robusta)**

```javascript
var anchors = document.querySelectorAll("[whenClicked='set']");
for (var i = 0; i < anchors.length; i++) {
  anchors[i].onclick = function () {
    // ✅ Função auxiliar para obter valor com fallback
    function getFieldValue(id, fallback = null) {
      var el = document.getElementById(id);
      return el && el.value !== undefined ? el.value : fallback;
    }
    
    var global_email = getFieldValue("email");
    var global_gclid = getFieldValue("GCLID_FLD");
    var global_gclid_wp = getFieldValue("GCLID_FLD_WP");
    
    // Salvar no localStorage (mesmo se null, para limpar valores antigos)
    window.localStorage.setItem("GCLID_FLD", global_gclid || "");
    window.localStorage.setItem("GCLID_FLD_WP", global_gclid_wp || "");
    window.localStorage.setItem("EMAIL_FLD", global_email || "");
  };
}
```

---

## 🎯 IMPACTO

### **Severidade:** Média
- **Bloqueia funcionalidade?** Não diretamente (mas pode causar erro no console)
- **Afeta UX?** Pode causar confusão se valores não forem salvos
- **Frequência:** Provavelmente ocorre quando:
  - Páginas não possuem todos os campos esperados
  - Campos têm IDs diferentes do esperado
  - Elementos não foram carregados ainda

### **Páginas Afetadas:**
- Qualquer página com elemento `<a>` que tenha atributo `whenClicked='set'`
- Páginas onde os campos `email`, `GCLID_FLD`, ou `GCLID_FLD_WP` não existem

---

## 📝 RECOMENDAÇÕES

1. **Implementar verificação defensiva** antes de acessar `.value`
2. **Adicionar logs** para debug (opcional em produção)
3. **Considerar usar jQuery** (já está disponível) para verificação mais robusta:
   ```javascript
   var global_email = $('#email').length ? $('#email').val() : null;
   ```
4. **Testar em todas as páginas** onde há elementos com `whenClicked='set'`

---

## 🔗 ARQUIVOS ENVOLVIDOS

- **Arquivo a Modificar:** `02-DEVELOPMENT/custom-codes/Inside Head Tag Pagina.js`
- **Linhas:** 46-56
- **Contexto:** Código que salva valores de campos em localStorage ao clicar em anchors

---

**Status:** ✅ **Problema Identificado e Solução Proposta**  
**Próxima Ação:** Aguardar aprovação para implementar correção





