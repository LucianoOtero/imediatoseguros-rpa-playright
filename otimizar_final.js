const fs = require('fs');

console.log('🎯 Fazendo limpeza final e otimização...');

// Ler o arquivo limpo
let content = fs.readFileSync('webflow_injection_limpo.js', 'utf8');

console.log(`📊 Tamanho antes da otimização: ${content.length} caracteres`);

// Remover comentários de bloco /* */
content = content.replace(/\/\*[\s\S]*?\*\//g, '');

// Remover comentários de linha // (exceto os essenciais)
content = content.replace(/\/\/.*$/gm, '');

// Remover linhas vazias excessivas
content = content.replace(/\n\s*\n\s*\n+/g, '\n\n');

// Remover espaços desnecessários no início e fim das linhas
content = content.replace(/^\s+|\s+$/gm, '');

// Remover espaços múltiplos
content = content.replace(/\s{2,}/g, ' ');

// Remover quebras de linha desnecessárias em objetos/arrays
content = content.replace(/{\s*\n\s*/g, '{');
content = content.replace(/\s*\n\s*}/g, '}');
content = content.replace(/\[\s*\n\s*/g, '[');
content = content.replace(/\s*\n\s*\]/g, ']');

console.log(`📊 Tamanho após otimização: ${content.length} caracteres`);
console.log(`📊 Redução total: ${((137573 - content.length) / 137573 * 100).toFixed(1)}%`);

// Salvar arquivo otimizado
fs.writeFileSync('webflow_injection_limpo.js', content);
console.log('✅ Arquivo otimizado salvo!');

// Verificar funcionalidades essenciais
const essentialChecks = [
    'SpinnerTimer',
    'ProgressModalRPA', 
    'MainPage',
    'handleFormSubmit',
    'openProgressModal',
    'cssStyles',
    'window.MainPage',
    'window.SpinnerTimer',
    'window.ProgressModalRPA'
];

console.log('\n🔍 Verificação de funcionalidades essenciais:');
essentialChecks.forEach(check => {
    if (content.includes(check)) {
        console.log(`✅ ${check}`);
    } else {
        console.log(`❌ ${check} - ATENÇÃO!`);
    }
});

console.log('\n🎉 Otimização final concluída!');

