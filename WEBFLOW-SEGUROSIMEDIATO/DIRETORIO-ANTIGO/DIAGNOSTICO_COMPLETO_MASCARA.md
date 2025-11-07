# 🔍 Diagnóstico Completo: Máscara de Placa NÃO Aplicada

**Data:** 2025-10-30  
**Problema Identificado:** A máscara não está sendo aplicada ao campo PLACA

---

## 📋 Resultado do Teste no Console

```javascript
const $PLACA = $('#PLACA, [name="PLACA"]');
console.log('Campo encontrado:', $PLACA[0]);  // ✅ Campo existe
console.log('Valor atual:', $PLACA.val());    // "fpg8d63" (sem traço)
console.log('Máscara aplicada?', $PLACA.data('mask'));  // ❌ undefined
```

**Conclusão:** A máscara **NÃO ESTÁ APLICADA** ao campo!

---

## 🔍 Possíveis Causas

### 1. Função `aplicarMascaraPlaca` não está disponível

**Verificar no console:**
```javascript
typeof window.aplicarMascaraPlaca
```

Se retornar `"undefined"`, significa que:
- Utils.js não carregou
- Função não foi exposta globalmente
- Erro durante carregamento

### 2. Função não está sendo chamada

**Código em Footer Code (linha 593-595):**
```javascript
if ($PLACA.length && typeof window.aplicarMascaraPlaca === 'function') {
  window.aplicarMascaraPlaca($PLACA);
}
```

**Possíveis problemas:**
- Condição `typeof window.aplicarMascaraPlaca === 'function'` retorna `false`
- `$PLACA.length` retorna `0` (campo não existe quando código executa)
- Erro silencioso durante execução

### 3. Timing: Campo não existe quando código executa

**Problema:** Código executa antes do campo existir no DOM.

**Solução:** Garantir que código execute após DOM estar pronto.

---

## 🧪 Testes Adicionais no Console

Execute estes comandos no console do navegador:

### Teste 1: Verificar se função existe
```javascript
typeof window.aplicarMascaraPlaca
```
**Esperado:** `"function"`  
**Se for `"undefined"`:** Utils.js não carregou

### Teste 2: Verificar se campo existe quando Footer Code executa
```javascript
// Verificar quando campo foi criado
$('#PLACA').length
```

### Teste 3: Aplicar máscara manualmente
```javascript
const $PLACA = $('#PLACA, [name="PLACA"]');
if (typeof window.aplicarMascaraPlaca === 'function') {
  window.aplicarMascaraPlaca($PLACA);
  console.log('Máscara aplicada manualmente');
  console.log('Máscara aplicada?', $PLACA.data('mask'));
} else {
  console.log('Função aplicarMascaraPlaca não existe!');
}
```

### Teste 4: Aplicar máscara diretamente (código de produção)
```javascript
const $PLACA = $('#PLACA, [name="PLACA"]');
const t = {'S':{pattern:/[A-Za-z]/},'0':{pattern:/\d/},'A':{pattern:/[A-Za-z0-9]/}};
$PLACA.on('input', function(){this.value=this.value.toUpperCase();});
$PLACA.mask('SSS-0A00',{translation:t, clearIfNotMatch:false});
console.log('Máscara aplicada diretamente');
console.log('Máscara aplicada?', $PLACA.data('mask'));
```

---

## ✅ Próximos Passos

1. **Execute Teste 1** → Verificar se função existe
2. **Execute Teste 3** → Tentar aplicar máscara manualmente
3. **Execute Teste 4** → Aplicar máscara diretamente (código de produção)

**Se Teste 4 funcionar:** Problema é timing ou função não está sendo chamada  
**Se Teste 1 retornar `undefined`:** Utils.js não carregou corretamente







