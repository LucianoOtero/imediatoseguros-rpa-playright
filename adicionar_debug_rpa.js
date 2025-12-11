const fs = require('fs');

console.log('🔍 Criando script de debug para verificação de injeção...');

// Ler o arquivo Footer Code modificado
const footerContent = fs.readFileSync('C:\\Users\\Luciano\\OneDrive - Imediato Soluções em Seguros\\Imediato\\mdmidia\\custom code webflow\\Footer Code Site Definitivo.js', 'utf8');

// Script de debug para adicionar ao Footer Code
const debugScript = `
<!-- ====================== -->
<!-- 🔍 DEBUG: VERIFICAÇÃO DE INJEÇÃO RPA -->
<script>
console.log('🔍 [DEBUG] Iniciando verificação de injeção RPA...');

// Função para verificar se a injeção foi bem-sucedida
function debugRPAModule() {
  console.log('🔍 [DEBUG] === VERIFICAÇÃO DE INJEÇÃO RPA ===');
  
  // 1. Verificar se window.rpaEnabled existe
  if (typeof window.rpaEnabled !== 'undefined') {
    console.log('✅ [DEBUG] window.rpaEnabled encontrado:', window.rpaEnabled);
  } else {
    console.error('❌ [DEBUG] window.rpaEnabled NÃO encontrado!');
  }
  
  // 2. Verificar se loadRPAScript existe
  if (typeof window.loadRPAScript === 'function') {
    console.log('✅ [DEBUG] window.loadRPAScript encontrado');
  } else {
    console.error('❌ [DEBUG] window.loadRPAScript NÃO encontrado!');
  }
  
  // 3. Verificar se jQuery está disponível
  if (typeof $ !== 'undefined') {
    console.log('✅ [DEBUG] jQuery disponível:', $.fn.jquery);
  } else {
    console.error('❌ [DEBUG] jQuery NÃO disponível!');
  }
  
  // 4. Verificar se SweetAlert2 está disponível
  if (typeof Swal !== 'undefined') {
    console.log('✅ [DEBUG] SweetAlert2 disponível');
  } else {
    console.warn('⚠️ [DEBUG] SweetAlert2 NÃO disponível (pode ser carregado dinamicamente)');
  }
  
  // 5. Verificar conflitos de nomes de função
  const globalFunctions = Object.keys(window).filter(key => typeof window[key] === 'function');
  const rpaFunctions = globalFunctions.filter(func => func.toLowerCase().includes('rpa') || func.toLowerCase().includes('load'));
  console.log('🔍 [DEBUG] Funções globais relacionadas ao RPA:', rpaFunctions);
  
  // 6. Verificar se há elementos de formulário
  const forms = document.querySelectorAll('form');
  console.log('🔍 [DEBUG] Formulários encontrados:', forms.length);
  
  // 7. Verificar se há botões de submit
  const submitButtons = document.querySelectorAll('button[type="submit"], input[type="submit"]');
  console.log('🔍 [DEBUG] Botões de submit encontrados:', submitButtons.length);
  
  console.log('🔍 [DEBUG] === FIM DA VERIFICAÇÃO ===');
}

// Função para testar carregamento dinâmico
function testDynamicLoading() {
  console.log('🔍 [DEBUG] Testando carregamento dinâmico...');
  
  if (typeof window.loadRPAScript === 'function') {
    console.log('🔍 [DEBUG] Tentando carregar script RPA...');
    
    window.loadRPAScript()
      .then(() => {
        console.log('✅ [DEBUG] Script RPA carregado com sucesso!');
        
        // Verificar se as classes RPA foram carregadas
        if (typeof window.MainPage !== 'undefined') {
          console.log('✅ [DEBUG] window.MainPage disponível');
        } else {
          console.error('❌ [DEBUG] window.MainPage NÃO disponível após carregamento');
        }
        
        if (typeof window.ProgressModalRPA !== 'undefined') {
          console.log('✅ [DEBUG] window.ProgressModalRPA disponível');
        } else {
          console.error('❌ [DEBUG] window.ProgressModalRPA NÃO disponível após carregamento');
        }
        
        if (typeof window.SpinnerTimer !== 'undefined') {
          console.log('✅ [DEBUG] window.SpinnerTimer disponível');
        } else {
          console.error('❌ [DEBUG] window.SpinnerTimer NÃO disponível após carregamento');
        }
        
      })
      .catch(error => {
        console.error('❌ [DEBUG] Erro ao carregar script RPA:', error);
      });
  } else {
    console.error('❌ [DEBUG] window.loadRPAScript não está disponível para teste');
  }
}

// Função para detectar conflitos
function detectConflicts() {
  console.log('🔍 [DEBUG] === DETECÇÃO DE CONFLITOS ===');
  
  // Verificar se há múltiplas definições de funções
  const functionNames = [];
  const scripts = document.querySelectorAll('script');
  
  scripts.forEach((script, index) => {
    if (script.textContent) {
      const content = script.textContent;
      
      // Verificar se há definições de loadRPAScript
      if (content.includes('loadRPAScript')) {
        functionNames.push(\`Script \${index + 1}: loadRPAScript\`);
      }
      
      // Verificar se há definições de rpaEnabled
      if (content.includes('rpaEnabled')) {
        functionNames.push(\`Script \${index + 1}: rpaEnabled\`);
      }
    }
  });
  
  if (functionNames.length > 1) {
    console.warn('⚠️ [DEBUG] Possível conflito detectado - múltiplas definições:', functionNames);
  } else {
    console.log('✅ [DEBUG] Nenhum conflito de múltiplas definições detectado');
  }
  
  // Verificar se há erros no console
  const originalError = console.error;
  const errors = [];
  console.error = function(...args) {
    errors.push(args.join(' '));
    originalError.apply(console, args);
  };
  
  setTimeout(() => {
    console.error = originalError;
    if (errors.length > 0) {
      console.warn('⚠️ [DEBUG] Erros detectados durante inicialização:', errors);
    } else {
      console.log('✅ [DEBUG] Nenhum erro detectado durante inicialização');
    }
  }, 2000);
  
  console.log('🔍 [DEBUG] === FIM DA DETECÇÃO DE CONFLITOS ===');
}

// Executar verificações após DOM estar pronto
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    setTimeout(debugRPAModule, 100);
    setTimeout(detectConflicts, 200);
  });
} else {
  setTimeout(debugRPAModule, 100);
  setTimeout(detectConflicts, 200);
}

// Expor funções de debug globalmente para teste manual
window.debugRPAModule = debugRPAModule;
window.testDynamicLoading = testDynamicLoading;
window.detectConflicts = detectConflicts;

console.log('🔍 [DEBUG] Funções de debug disponíveis:');
console.log('  - window.debugRPAModule()');
console.log('  - window.testDynamicLoading()');
console.log('  - window.detectConflicts()');
</script>
<!-- ====================== -->
`;

// Adicionar script de debug ao Footer Code
const updatedContent = footerContent + debugScript;

// Salvar arquivo com debug
fs.writeFileSync('C:\\Users\\Luciano\\OneDrive - Imediato Soluções em Seguros\\Imediato\\mdmidia\\custom code webflow\\Footer Code Site Definitivo.js', updatedContent);

console.log('✅ Script de debug adicionado ao Footer Code Site Definitivo.js');
console.log('📊 Tamanho final:', updatedContent.length, 'caracteres');

// Criar arquivo de teste HTML para verificar funcionamento
const testHTML = `<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Teste Debug RPA</title>
</head>
<body>
    <h1>Teste de Debug RPA</h1>
    <form id="test-form">
        <input type="text" name="test" placeholder="Campo de teste">
        <button type="submit">Testar Submit</button>
    </form>
    
    <div id="debug-output"></div>
    
    <script>
        // Simular ambiente de teste
        console.log('🧪 [TEST] Página de teste carregada');
        
        // Função para mostrar resultados no DOM
        function showDebugResults() {
            const output = document.getElementById('debug-output');
            output.innerHTML = '<h2>Resultados do Debug:</h2><pre id="console-output"></pre>';
            
            // Capturar logs do console
            const originalLog = console.log;
            const originalError = console.error;
            const originalWarn = console.warn;
            const logs = [];
            
            console.log = function(...args) {
                logs.push('[LOG] ' + args.join(' '));
                originalLog.apply(console, args);
            };
            
            console.error = function(...args) {
                logs.push('[ERROR] ' + args.join(' '));
                originalError.apply(console, args);
            };
            
            console.warn = function(...args) {
                logs.push('[WARN] ' + args.join(' '));
                originalWarn.apply(console, args);
            };
            
            setTimeout(() => {
                document.getElementById('console-output').textContent = logs.join('\n');
                console.log = originalLog;
                console.error = originalError;
                console.warn = originalWarn;
            }, 3000);
        }
        
        // Executar debug após carregar Footer Code
        setTimeout(showDebugResults, 1000);
    </script>
</body>
</html>`;

fs.writeFileSync('teste_debug_rpa.html', testHTML);

console.log('✅ Arquivo de teste criado: teste_debug_rpa.html');
console.log('');
console.log('🔍 INSTRUÇÕES DE TESTE:');
console.log('1. Abra o arquivo teste_debug_rpa.html no navegador');
console.log('2. Abra o Console do navegador (F12)');
console.log('3. Verifique os logs de debug');
console.log('4. Execute manualmente: window.debugRPAModule()');
console.log('5. Execute manualmente: window.testDynamicLoading()');
console.log('6. Execute manualmente: window.detectConflicts()');
