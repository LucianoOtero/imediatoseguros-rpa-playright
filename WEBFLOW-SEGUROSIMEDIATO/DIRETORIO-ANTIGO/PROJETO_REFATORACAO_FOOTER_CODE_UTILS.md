# Projeto: Refatoração Footer Code - Extração de Funções Utilitárias

## 📋 Objetivo
Extrair todas as funções utilitárias (utils/helpers) do arquivo `Footer Code Site Definitivo.js` para um arquivo separado `Footer Code Site Definitivo Utils.js`, reduzindo o tamanho do arquivo principal e melhorando a organização e manutenibilidade do código.

## 🎯 Justificativa
- **Problema atual**: O arquivo `Footer Code Site Definitivo.js` possui **50.309 caracteres**, excedendo o limite de 50.000 caracteres do Webflow
- **Solução**: Extrair **7.437 caracteres** de funções utilitárias para arquivo separado, reduzindo o Footer Code para aproximadamente **42.872 caracteres**

## 📊 Funções Utilitárias Identificadas (18 funções - 7.437 caracteres)

### Funções de Manipulação de Dados (5 funções - 1.157 caracteres)
1. `onlyDigits` - 58 caracteres
2. `toUpperNospace` - 64 caracteres  
3. `setFieldValue` - 131 caracteres
4. `readCookie` - 255 caracteres
5. `generateSessionId` - 195 caracteres
6. `nativeSubmit` - 129 caracteres

### Funções de Validação Local (4 funções - 1.503 caracteres)
7. `validarEmailLocal` - 94 caracteres
8. `validarCPFFormato` - 138 caracteres
9. `validarCPFAlgoritmo` - 587 caracteres
10. `validarPlacaFormato` - 244 caracteres
11. `validarCelularLocal` - 286 caracteres
12. `aplicarMascaraPlaca` - 249 caracteres

### Funções de Criptografia (2 funções - 758 caracteres)
13. `sha1` - 276 caracteres
14. `hmacSHA256` - 482 caracteres

### Funções de Extração/Transformação de Dados (3 funções - 4.159 caracteres)
15. `extractDataFromPH3A` - 1.410 caracteres
16. `extractVehicleFromPlacaFipe` - 1.881 caracteres
17. `preencherEnderecoViaCEP` - 125 caracteres
18. `isDevelopmentEnvironment` - 833 caracteres

**TOTAL**: 18 funções = **7.437 caracteres**

## 📁 Arquivos Envolvidos

### Arquivo Base (backup)
- **Fonte**: `02-DEVELOPMENT/custom-codes/Footer Code Site Definitivo.backup_20251029_123729.js`
- **Tamanho atual**: 50.309 caracteres
- **Linhas**: 1.366 linhas

### Arquivo a ser criado
- **Novo arquivo**: `02-DEVELOPMENT/custom-codes/Footer Code Site Definitivo Utils.js`
- **Conteúdo**: Todas as 18 funções utilitárias
- **Estrutura**: Funções organizadas por categoria

### Arquivo a ser modificado
- **Arquivo principal**: `02-DEVELOPMENT/custom-codes/Footer Code Site Definitivo.js`
- **Após refatoração**: ~42.872 caracteres
- **Mudanças**: Remover funções utilitárias e adicionar carregamento do Utils.js

## 🏗️ Estrutura do Novo Arquivo Utils.js

```javascript
<!-- ====================== -->
<!-- 🛠️ FOOTER CODE UTILS - Funções Utilitárias -->
<script>
(function() {
  'use strict';
  
  // ========= MANIPULAÇÃO DE DADOS =========
  
  /**
   * Extrai apenas dígitos de uma string
   * @param {string} s - String a processar
   * @returns {string} String contendo apenas dígitos
   */
  function onlyDigits(s) {
    return (s || '').replace(/\D+/g, '');
  }
  
  /**
   * Converte para maiúsculas e remove espaços
   * @param {string} s - String a processar
   * @returns {string} String em maiúsculas sem espaços
   */
  function toUpperNospace(s) {
    return (s || '').toUpperCase().trim();
  }
  
  // ... (todas as outras funções utilitárias)
  
  // ========= EXPOSIÇÃO GLOBAL =========
  
  // Expor funções globalmente para uso no Footer Code principal
  window.onlyDigits = onlyDigits;
  window.toUpperNospace = toUpperNospace;
  window.setFieldValue = setFieldValue;
  window.readCookie = readCookie;
  window.generateSessionId = generateSessionId;
  window.nativeSubmit = nativeSubmit;
  window.validarEmailLocal = validarEmailLocal;
  window.validarCPFFormato = validarCPFFormato;
  window.validarCPFAlgoritmo = validarCPFAlgoritmo;
  window.validarPlacaFormato = validarPlacaFormato;
  window.validarCelularLocal = validarCelularLocal;
  window.aplicarMascaraPlaca = aplicarMascaraPlaca;
  window.sha1 = sha1;
  window.hmacSHA256 = hmacSHA256;
  window.extractDataFromPH3A = extractDataFromPH3A;
  window.extractVehicleFromPlacaFipe = extractVehicleFromPlacaFipe;
  window.preencherEnderecoViaCEP = preencherEnderecoViaCEP;
  window.isDevelopmentEnvironment = isDevelopmentEnvironment;
  
  console.log('✅ [UTILS] Footer Code Utils carregado - 18 funções disponíveis');
})();
</script>
<!-- ====================== -->
```

## 📝 Modificações no Footer Code Site Definitivo.js

### 1. Adicionar Carregamento do Utils.js (no início, após bibliotecas base)

**Localização**: Após linha 34 (após SweetAlert2)

```javascript
<!-- ====================== -->
<!-- 🛠️ Footer Code Utils - Carregar funções utilitárias -->
<script>
(function() {
  // Carregar Utils.js dinamicamente
  const utilsScript = document.createElement('script');
  utilsScript.src = 'https://dev.bpsegurosimediato.com.br/webhooks/Footer Code Site Definitivo Utils.js?v=1';
  utilsScript.onload = function() {
    console.log('✅ [FOOTER] Utils.js carregado com sucesso');
    
    // Verificar se todas as funções foram carregadas
    const requiredFunctions = [
      'onlyDigits', 'toUpperNospace', 'setFieldValue', 'readCookie',
      'generateSessionId', 'nativeSubmit', 'validarEmailLocal',
      'validarCPFFormato', 'validarCPFAlgoritmo', 'validarPlacaFormato',
      'validarCelularLocal', 'aplicarMascaraPlaca', 'sha1', 'hmacSHA256',
      'extractDataFromPH3A', 'extractVehicleFromPlacaFipe',
      'preencherEnderecoViaCEP', 'isDevelopmentEnvironment'
    ];
    
    const missing = requiredFunctions.filter(fn => typeof window[fn] !== 'function');
    if (missing.length > 0) {
      console.error('❌ [FOOTER] Funções faltando:', missing);
    } else {
      console.log('✅ [FOOTER] Todas as funções utilitárias disponíveis');
    }
  };
  utilsScript.onerror = function() {
    console.error('❌ [FOOTER] Erro ao carregar Utils.js');
  };
  document.head.appendChild(utilsScript);
})();
</script>
<!-- ====================== -->
```

### 2. Remover Funções Utilitárias do Footer Code

**Linhas a remover do arquivo original**:

- Linha 108-113: `generateSessionId` (já está, será removida)
- Linha 203-210: `readCookie`
- Linha 127-153: `isDevelopmentEnvironment` (manter no Footer Code? Ou mover?)
- Linha 359-366: `sha1`
- Linha 368-380: `hmacSHA256`
- Linha 432: `onlyDigits`
- Linha 433: `toUpperNospace`
- Linha 434: `nativeSubmit`
- Linha 435: `setFieldValue`
- Linha 438-441: `validarCPFFormato`
- Linha 443-462: `validarCPFAlgoritmo`
- Linha 464-517: `extractDataFromPH3A`
- Linha 565: `preencherEnderecoViaCEP`
- Linha 578-585: Duplicações de `toUpperNospace` e `onlyDigits` (remover)
- Linha 587-592: `validarPlacaFormato`
- Linha 593-644: `extractVehicleFromPlacaFipe`
- Linha 680-686: `validarCelularLocal`
- Linha 702: `validarEmailLocal`
- Linha 705-709: `aplicarMascaraPlaca`

**Nota**: `isDevelopmentEnvironment` pode ser mantida no Footer Code pois é usada logo na inicialização, antes do carregamento assíncrono do Utils.js. Decisão: **Manter no Footer Code** por enquanto.

### 3. Adicionar Verificação de Dependências

Antes de usar as funções utilitárias no código, adicionar verificação:

```javascript
// Exemplo de uso com verificação
if (typeof window.onlyDigits === 'function') {
  const cpfLimpo = window.onlyDigits($CPF.val());
} else {
  console.error('❌ [FOOTER] onlyDigits não disponível');
  // Fallback ou erro
}
```

**OU** utilizar wrapper functions que aguardam o carregamento.

## 🚀 Fase 1: Preparação

### 1.1 Backup
- [ ] Criar backup completo do arquivo atual: `Footer Code Site Definitivo.backup_pre_refatoracao_YYYYMMDD.js`
- [ ] Verificar se backup anterior (`backup_20251029_123729.js`) está íntegro

### 1.2 Análise
- [ ] Confirmar todas as 18 funções no arquivo de backup
- [ ] Verificar dependências entre funções
- [ ] Identificar pontos de uso de cada função no código

## 🔨 Fase 2: Desenvolvimento

### 2.1 Criar Arquivo Utils.js
- [ ] Criar arquivo `Footer Code Site Definitivo Utils.js`
- [ ] Adicionar estrutura base (IIFE para evitar conflitos)
- [ ] Copiar função `onlyDigits` (linha 432)
- [ ] Copiar função `toUpperNospace` (linha 433)
- [ ] Copiar função `setFieldValue` (linha 435)
- [ ] Copiar função `readCookie` (linha 203-210)
- [ ] Copiar função `generateSessionId` (linha 108-113)
- [ ] Copiar função `nativeSubmit` (linha 434)
- [ ] Copiar função `validarEmailLocal` (linha 702)
- [ ] Copiar função `validarCPFFormato` (linha 438-441)
- [ ] Copiar função `validarCPFAlgoritmo` (linha 443-462)
- [ ] Copiar função `extractDataFromPH3A` (linha 464-517)
- [ ] Copiar função `preencherEnderecoViaCEP` (linha 565)
- [ ] Copiar função `validarPlacaFormato` (linha 587-592)
- [ ] Copiar função `extractVehicleFromPlacaFipe` (linha 593-644)
- [ ] Copiar função `validarCelularLocal` (linha 680-686)
- [ ] Copiar função `aplicarMascaraPlaca` (linha 705-709)
- [ ] Copiar função `sha1` (linha 359-366)
- [ ] Copiar função `hmacSHA256` (linha 368-380)
- [ ] Adicionar exposição global de todas as funções
- [ ] Adicionar log de inicialização

### 2.2 Modificar Footer Code Principal
- [ ] Adicionar script de carregamento do Utils.js (após linha 34)
- [ ] Remover função `onlyDigits` (linha 432)
- [ ] Remover função `toUpperNospace` (linha 433, e duplicação 578-580)
- [ ] Remover função `setFieldValue` (linha 435)
- [ ] Remover função `readCookie` (linha 203-210, mover para início do script se necessário)
- [ ] Remover função `generateSessionId` (linha 108-113)
- [ ] Remover função `nativeSubmit` (linha 434)
- [ ] Remover função `validarEmailLocal` (linha 702)
- [ ] Remover função `validarCPFFormato` (linha 438-441)
- [ ] Remover função `validarCPFAlgoritmo` (linha 443-462)
- [ ] Remover função `extractDataFromPH3A` (linha 464-517)
- [ ] Remover função `preencherEnderecoViaCEP` (linha 565)
- [ ] Remover função `validarPlacaFormato` (linha 587-592)
- [ ] Remover função `extractVehicleFromPlacaFipe` (linha 593-644)
- [ ] Remover função `validarCelularLocal` (linha 680-686)
- [ ] Remover função `aplicarMascaraPlaca` (linha 705-709)
- [ ] Remover função `sha1` (linha 359-366)
- [ ] Remover função `hmacSHA256` (linha 368-380)
- [ ] Remover duplicações de funções (linha 578-585)
- [ ] Verificar se todas as chamadas às funções ainda funcionam

### 2.3 Ajustes e Compatibilidade
- [ ] Verificar se `readCookie` precisa estar disponível antes de outros scripts
- [ ] Considerar mover `readCookie` para Footer Code (usada antes do carregamento assíncrono)
- [ ] Adicionar verificação de dependências antes de uso das funções
- [ ] Implementar sistema de espera (polling) caso Utils.js não tenha carregado ainda
- [ ] Garantir que funções assíncronas (`sha1`, `hmacSHA256`) funcionem corretamente

## 📤 Fase 3: Deploy Desenvolvimento

### 3.1 Upload do Utils.js
- [ ] Verificar acesso SSH ao servidor de desenvolvimento
- [ ] Criar diretório se necessário: `/var/www/html/dev/webhooks/`
- [ ] Fazer upload do arquivo `Footer Code Site Definitivo Utils.js` para:
  - **Caminho**: `/var/www/html/dev/webhooks/Footer Code Site Definitivo Utils.js`
- [ ] Ajustar permissões: `chmod 644` e `chown www-data:www-data`
- [ ] Verificar URL de acesso: `https://dev.bpsegurosimediato.com.br/webhooks/Footer Code Site Definitivo Utils.js`

### 3.2 Testes em Desenvolvimento
- [ ] Abrir console do navegador
- [ ] Verificar se Utils.js carrega corretamente
- [ ] Verificar log: `✅ [UTILS] Footer Code Utils carregado - 18 funções disponíveis`
- [ ] Verificar log: `✅ [FOOTER] Utils.js carregado com sucesso`
- [ ] Verificar log: `✅ [FOOTER] Todas as funções utilitárias disponíveis`
- [ ] Testar validação de CPF
- [ ] Testar validação de CEP
- [ ] Testar validação de Placa
- [ ] Testar validação de Celular
- [ ] Testar validação de Email
- [ ] Testar preenchimento automático de campos
- [ ] Testar envio de formulário
- [ ] Verificar se não há erros no console

### 3.3 Validação de Tamanho
- [ ] Verificar tamanho do Footer Code após refatoração (~42.872 caracteres)
- [ ] Confirmar que está abaixo do limite de 50.000 caracteres
- [ ] Verificar tamanho do Utils.js (~7.437 + overhead)

## 📦 Fase 4: Estrutura de Arquivos no Servidor

### Estrutura Desenvolvimento
```
/var/www/html/dev/webhooks/
├── Footer Code Site Definitivo Utils.js    (NOVO)
├── MODAL_WHATSAPP_DEFINITIVO.js
├── add_travelangels.php
└── add_webflow_octa.php
```

### URLs de Acesso
- **Utils.js**: `https://dev.bpsegurosimediato.com.br/webhooks/Footer Code Site Definitivo Utils.js?v=1`

## ⚠️ Considerações Importantes

### Ordem de Carregamento
- Utils.js **deve** ser carregado antes das funções que o utilizam
- Footer Code deve aguardar carregamento do Utils.js antes de executar lógica principal
- Considerar usar Promise ou polling para garantir carregamento

### Compatibilidade
- Manter compatibilidade com código existente
- Todas as funções devem estar disponíveis em `window.*`
- Não quebrar funcionalidades existentes

### Nomes de Arquivos
- **Problema**: Espaços no nome do arquivo podem causar problemas em URLs
- **Solução**: Usar encoding de URL ou renomear para `FooterCodeSiteDefinitivoUtils.js`
- **Decisão**: Usar `FooterCodeSiteDefinitivoUtils.js` (sem espaços)

### Versionamento
- Adicionar parâmetro `?v=1` na URL do Utils.js
- Incrementar versão a cada atualização para evitar cache

## 🔄 Plano de Rollback

### Em caso de problemas:
1. Restaurar backup: `Footer Code Site Definitivo.backup_pre_refatoracao_YYYYMMDD.js`
2. Remover referência ao Utils.js do Footer Code
3. Verificar se site funciona normalmente

## 📋 Checklist Final

### Antes de Produção
- [ ] Todos os testes em desenvolvimento passaram
- [ ] Sem erros no console
- [ ] Validações funcionando corretamente
- [ ] Formulários submetem corretamente
- [ ] Performance não degradou
- [ ] Tamanho do Footer Code reduzido conforme esperado
- [ ] Backup completo realizado
- [ ] Documentação atualizada

## 📊 Métricas Esperadas

### Antes da Refatoração
- **Footer Code**: 50.309 caracteres
- **Status**: ❌ Excede limite de 50.000 caracteres

### Após Refatoração
- **Footer Code**: ~42.872 caracteres
- **Utils.js**: ~7.437 caracteres (+ overhead ~500) = ~8.000 caracteres
- **Status**: ✅ Footer Code dentro do limite

### Redução
- **Redução no Footer Code**: -7.437 caracteres (-14,8%)
- **Novo arquivo Utils.js**: +8.000 caracteres
- **Total**: Mesmo volume de código, melhor organizado

## 🎯 Decisões Pendentes

1. **`isDevelopmentEnvironment`**: Mover para Utils.js ou manter no Footer Code?
   - **Recomendação**: Manter no Footer Code (usada na inicialização)
   
2. **`readCookie`**: Mover para Utils.js ou manter no Footer Code?
   - **Recomendação**: Manter no Footer Code (usada antes do carregamento assíncrono)

3. **Nome do arquivo**: Com ou sem espaços?
   - **Decisão**: `FooterCodeSiteDefinitivoUtils.js` (sem espaços)

4. **Sistema de espera**: Como garantir que Utils.js carregou?
   - **Recomendação**: Polling ou Promise com timeout

## 📝 Próximos Passos

1. Revisar projeto com equipe
2. Aprovar decisões pendentes
3. Criar branch de desenvolvimento
4. Implementar Fase 2 (Desenvolvimento)
5. Testar em desenvolvimento
6. Deploy em desenvolvimento
7. Validação completa
8. Preparar para produção

---

**Versão do Projeto**: 1.0  
**Data de Criação**: 2025-10-29  
**Baseado em**: Footer Code Site Definitivo.backup_20251029_123729.js











