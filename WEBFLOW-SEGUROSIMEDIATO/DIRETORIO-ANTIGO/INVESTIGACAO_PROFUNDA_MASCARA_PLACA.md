# Investigação Profunda: Máscara de Placa - Por que funciona em Produção e não em Desenvolvimento?

**Data:** 2025-10-30  
**Objetivo:** Identificar a causa raiz da diferença de comportamento entre produção e desenvolvimento

---

## 📋 Configurações Identificadas

### Ambiente
- **jQuery Mask:** v1.14.16 (mesma versão em ambos)
- **jQuery:** v3.6.0 (mesma versão em ambos)
- **Plataforma:** Webflow (mesmo ambiente)

---

## 🔍 Diferença Principal: Ordem de Execução dos Eventos

### Produção (Funciona Perfeitamente):

```javascript
function aplicarMascaraPlaca($i){
  const t={'S':{pattern:/[A-Za-z]/},'0':{pattern:/\d/},'A':{pattern:/[A-Za-z0-9]/}};
  $i.on('input',function(){this.value=this.value.toUpperCase();});  // ✅ ANTES da máscara
  $i.mask('SSS-0A00',{translation:t, clearIfNotMatch:false});        // ✅ DEPOIS do evento
}
```

**Fluxo de execução em produção:**
1. Evento `input` é registrado PRIMEIRO
2. Máscara é aplicada DEPOIS
3. Quando usuário digita:
   - jQuery Mask processa a máscara primeiro (insere traço automaticamente)
   - Depois, evento `input` dispara e converte para uppercase
   - **Resultado:** `FPG-8D63` ✅

### Desenvolvimento (Não Funciona):

```javascript
function aplicarMascaraPlaca($i) {
  const t = {'S': {pattern: /[A-Za-z]/, recursive: true}, '0': {pattern: /\d/}, 'A': {pattern: /[A-Za-z0-9]/}};
  $i.mask('SSS-0A00', {
    translation: t, 
    clearIfNotMatch: false,
    onKeyPress: function(value, e, field, options) {  // ❌ DENTRO da máscara
      field.val(value.toUpperCase());
    }
  });
}
```

**Fluxo de execução em desenvolvimento:**
1. Máscara é aplicada com callback `onKeyPress`
2. Quando usuário digita:
   - `onKeyPress` é chamado DURANTE o processamento da máscara
   - Pode estar interferindo com o cálculo interno do jQuery Mask
   - **Resultado:** Traço não é inserido automaticamente ❌

---

## 🔬 Investigação Técnica: jQuery Mask Plugin

### Como jQuery Mask processa a máscara internamente:

1. **Evento `keypress` ou `input`** → Captura tecla digitada
2. **Processa máscara** → Calcula posição, insere caracteres fixos (traço, pontos)
3. **Atualiza valor do campo** → Aplica máscara formatada
4. **Callbacks** → `onKeyPress` é chamado APÓS processamento, mas pode receber valor já processado

### Problema com `onKeyPress` callback:

Segundo documentação do jQuery Mask:
- `onKeyPress` é chamado **DEPOIS** que a máscara já processou
- Mas recebe o `value` como parâmetro, que pode estar **incompleto** durante a digitação
- Quando chamamos `field.val(value.toUpperCase())` dentro do callback, podemos estar **sobrescrevendo** o valor que a máscara acabou de processar

### Por que `input` event funciona:

- `input` event dispara **DEPOIS** de toda a cadeia de eventos (keypress → mask processing → value update)
- Quando dispara, o valor já está **totalmente formatado** pela má医生ara
- Não interfere no processamento interno da máscara
- Apenas converte para uppercase após tudo estar processado

---

## 🎯 Causa Raiz Identificada

### HIPÓTESE PRINCIPAL:

**O callback `onKeyPress` está sendo executado em um momento que interfere com o processamento interno da máscara, impedindo que o traço seja inserido automaticamente.**

### Evidências:

1. **Produção usa `input` event:** Funciona perfeitamente
2. **Desenvolvimento usa `onKeyPress`:** Não funciona
3. **Mesma versão jQuery Mask:** Elimina diferença de versão
4. **Mesma plataforma Webflow:** Elimina diferença de ambiente

### Por que `onKeyPress` interfere:

1. **Ordem de execução:**
   - jQuery Mask processa → Calcula traço → Atualiza campo
   - `onKeyPress` é chamado → Modifica valor novamente → Pode resetar estado interno

2. **Parâmetro `value` no callback:**
   - Pode estar recebendo valor **parcial** durante digitação
   - Quando fazemos `field.val(value.toUpperCase())`, conseguiu estar sobrescrevendo o valor já formatado

3. **Conflito com processamento interno:**
   - jQuery Mask mantém estado interno durante digitação
   - Modificar o valor via `field.val()` pode quebrar esse estado

---

## 🔬 Diferenças Adicionais Identificadas

### 1. `recursive: true`

**Produção:** Não usa `recursive: true`  
**Desenvolvimento:** Usa `recursive: true` no pattern 'S'

**Impacto:** Pode estar causando comportamento diferente no processamento da máscara, mas provavelmente não é a causa principal.

### 2. Formato do código

**Produção:** Código inline, mais compacto  
**Desenvolvimento:** Código em função separada (Utils.js), carregado dinamicamente

**Possível impacto:** Timing de carregamento, mas com `async: false` não deveria ser problema.

---

## ✅ Solução Recomendada

### Reverter para código exato de produção:

```javascript
function aplicarMascaraPlaca($i){
  const t={'S':{pattern:/[A-Za-z]/},'0':{pattern:/\d/},'A':{pattern:/[A-Za-z0-9]/}};
  $i.on('input',function(){this.value=this.value.to平时的();});
  $i.mask('SSS-0A00',{translation:t, clearIfNotMatch:false});
}
```

**Razões:**
1. ✅ Funciona em produção (testado e validado)
2. ✅ Não interfere no processamento interno da máscara
3. ✅ Mais simples e elegante
4. ✅ Evento `input` é executado após toda a cadeia de processamento

---

## 🧪 Testes Recomendados para Validação

### Teste 1: Verificar ordem de eventos no console
```javascript
// Adicionar logs para ver ordem de execução
$i.on('input', function(){
  console.log('[INPUT EVENT] Valor:', this.value);
  this.value = this.value.toUpperCase();
});

$i.mask('SSS-0A00', {
  translation: t,
  clearIfNotMatch: false,
  onKeyPress: function(value, e, field, options) {
    console.log('[ONKEYPRESS] Valor recebido:', value);
    console.log('[ONKEYPRESS] Valor do campo:', field.val());
  }
});
```

### Teste 2: Comparar timing de execução
- Verificar quando cada evento é disparado
- Verificar se `onKeyPress` está recebendo valor completo ou parcial

### Teste 3: Testar sem `recursive: true`
- Remover `recursive: true` e manter apenas `onKeyPress`
- Verificar se comportamento muda

---

## 📝 Conclusão

**Causa raiz mais provável:** O callback `onKeyPress` está sendo executado em um momento que interfere com o processamento interno do jQuery Mask, impedindo que o traço seja inserido automaticamente. A solução de produção (evento `input` separado) funciona porque não interfere no processamento interno da máscara.








