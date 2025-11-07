/**
 * TESTE DE DIAGNÓSTICO: Máscara de Placa
 * 
 * Este script deve ser injetado no console do navegador para diagnosticar
 * o comportamento da máscara de placa em tempo real.
 * 
 * USO:
 * 1. Abrir console do navegador (F12)
 * 2. Colar este código
 * 3. Digitar no campo de placa
 * 4. Observar logs no console
 */

(function() {
  console.log('🔍 [DIAGNÓSTICO] Iniciando diagnóstico de máscara de placa...');
  
  const $PLACA = $('#PLACA, [name="PLACA"]');
  
  if (!$PLACA.length) {
    console.error('❌ [DIAGNÓSTICO] Campo PLACA não encontrado');
    return;
  }
  
  console.log('✅ [DIAGNÓSTICO] Campo PLACA encontrado:', $PLACA[0]);
  
  // Verificar se jQuery Mask está disponível
  if (typeof $.fn.mask !== 'function') {
    console.error('❌ [DIAGNÓSTICO] jQuery Mask não está disponível');
    return;
  }
  
  console.log('✅ [DIAGNÓSTICO] jQuery Mask disponível');
  
  // Verificar se já tem máscara aplicada
  const hasMask = $PLACA.data('mask');
  console.log('🔍 [DIAGNÓSTICO] Máscara já aplicada?', hasMask ? 'Sim: ' + hasMask : 'Não');
  
  // Verificar eventos registrados
  const events = $._data($PLACA[0], 'events');
  console.log('🔍 [DIAGNÓSTICO] Eventos registrados:', events);
  
  // Remover máscara atual para teste limpo
  console.log('🔧 [DIAGNÓSTICO] Removendo máscara atual...');
  $PLACA.unmask();
  $PLACA.off('input');
  
  // TESTE 1: Código de PRODUÇÃO (deve funcionar)
  console.log('🧪 [TESTE 1] Aplicando código de PRODUÇÃO...');
  const t1 = {'S':{pattern:/[A-Za-z]/},'0':{pattern:/\d/},'A':{pattern:/[A-Za-z0-9]/}};
  
  $PLACA.on('input.producao', function(){
    console.log('[INPUT EVENT] Valor antes uppercase:', this.value);
    this.value = this.value.toUpperCase();
    console.log('[INPUT EVENT] Valor após uppercase:', this.value);
  });
  
  $PLACA.mask('SSS-0A00', {translation: t1, clearIfNotMatch: false});
  console.log('✅ [TESTE 1] Máscara de produção aplicada');
  
  // Adicionar listener para keypress para ver ordem de execução
  $PLACA.on('keypress.diagnostico', function(e) {
    console.log('[KEYPRESS] Tecla pressionada:', e.key, '| Valor atual:', this.value);
  });
  
  // Adicionar listener para input para ver ordem de execução
  $PLACA.on('input.diagnostico', function(e) {
    console.log('[INPUT] Disparado | Valor:', this.value);
  });
  
  // TESTE 2: Código de DESENVOLVIMENTO (com onKeyPress)
  console.log('🧪 [TESTE 2] Preparando código de DESENVOLVIMENTO (será aplicado após teste 1)...');
  
  // Função para testar código de desenvolvimento
  window.testarCodigoDesenvolvimento = function() {
    console.log('🧪 [TESTE 2] Aplicando código de DESENVOLVIMENTO...');
    
    $PLACA.unmask();
    $PLACA.off('.producao');
    $PLACA.off('.diagnostico');
    
    const t2 = {'S': {pattern: /[A-Za-z]/, recursive: true}, '0': {pattern: /\d/}, 'A': {pattern: /[A-Za-z0-9]/}};
    
    $PLACA.mask('SSS-0A00 publicación {
      translation: t2, 
      clearIfNotMatch: false,
      onKeyPress: function(value, e, field, options) {
        console.log('[ONKEYPRESS CALLBACK] Valor recebido:', value);
        console.log('[ONKEYPRESS CALLBACK] Valor do campo antes:', field.val());
        field.val(value.toUpperCase());
        console.log('[ONKEYPRESS CALLBACK] Valor do campo após:', field.val());
      }
    });
    
    $PLACA.on('keypress.diagnostico', function(e) {
      console.log('[KEYPRESS] Tecla pressionada:', e.key, '| Valor atual:', this.value);
    });
    
    $PLACA.on('input.diagnostico', function(e) {
      console.log('[INPUT] Disparado | Valor:', this.value);
    });
    
    console.log('✅ [TESTE 2] Máscara de desenvolvimento aplicada');
  };
  
  console.log('📝 [DIAGNÓSTICO] Para testar código de desenvolvimento, execute: testarCodigoDesenvolvimento()');
  console.log('📝 [DIAGNÓSTICO] Agora digite no campo PLACA e observe os logs no console');
  
})();








