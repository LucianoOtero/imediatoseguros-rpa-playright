const fs = require('fs');

console.log('🔧 Fazendo limpeza específica da classe MainPage...');

// Ler o arquivo limpo
let content = fs.readFileSync('webflow_injection_limpo.js', 'utf8');

// Métodos específicos da MainPage que devem ser removidos (já existem no Footer Code)
const mainPageMethodsToRemove = [
    'setupEventListeners',
    'setupFormSubmission', 
    'collectFormData',
    'removeDuplicateFields',
    'applyFieldConversions',
    'convertEstadoCivil',
    'convertSexo', 
    'convertTipoVeiculo',
    'validateFormData',
    'showValidationAlert',
    'focusFirstErrorField',
    'setFieldValue'
];

let totalRemoved = 0;

// Remover métodos específicos da MainPage
mainPageMethodsToRemove.forEach(methodName => {
    // Padrão mais específico para métodos da MainPage
    const regex = new RegExp(`\\s+${methodName}\\s*\\([^}]*\\}\\s*`, 'g');
    const matches = content.match(regex);
    
    if (matches) {
        matches.forEach(match => {
            totalRemoved += match.length;
            content = content.replace(match, '');
            console.log(`🗑️ Removido método MainPage: ${methodName} (${match.length} caracteres)`);
        });
    }
});

// Remover chamadas para métodos removidos dentro da MainPage
const methodCallsToRemove = [
    'this.setupEventListeners()',
    'this.setupFormSubmission()',
    'this.collectFormData(',
    'this.removeDuplicateFields(',
    'this.applyFieldConversions(',
    'this.validateFormData(',
    'this.showValidationAlert(',
    'this.focusFirstErrorField(',
    'this.setFieldValue('
];

methodCallsToRemove.forEach(call => {
    const regex = new RegExp(`\\s*${call.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}[^;]*;?`, 'g');
    const matches = content.match(regex);
    
    if (matches) {
        matches.forEach(match => {
            totalRemoved += match.length;
            content = content.replace(match, '');
            console.log(`🗑️ Removida chamada: ${call} (${match.length} caracteres)`);
        });
    }
});

// Limpar linhas vazias excessivas
content = content.replace(/\n\s*\n\s*\n/g, '\n\n');

console.log(`📊 Total adicional removido: ${totalRemoved} caracteres`);
console.log(`📊 Tamanho final: ${content.length} caracteres`);

// Salvar arquivo final limpo
fs.writeFileSync('webflow_injection_limpo.js', content);
console.log('✅ Arquivo final limpo salvo!');

// Verificar se as classes essenciais ainda estão presentes
const essentialClasses = ['SpinnerTimer', 'ProgressModalRPA', 'MainPage'];
essentialClasses.forEach(className => {
    if (content.includes(className)) {
        console.log(`✅ Classe essencial mantida: ${className}`);
    } else {
        console.log(`❌ ATENÇÃO: Classe essencial removida: ${className}`);
    }
});

// Verificar se métodos essenciais do RPA estão presentes
const essentialRPAMethods = ['handleFormSubmit', 'openProgressModal', 'initializeProgressModal'];
essentialRPAMethods.forEach(method => {
    if (content.includes(method)) {
        console.log(`✅ Método RPA essencial mantido: ${method}`);
    } else {
        console.log(`❌ ATENÇÃO: Método RPA essencial removido: ${method}`);
    }
});

console.log('🎉 Limpeza específica concluída!');

