const fs = require('fs');

console.log('🧹 Iniciando limpeza do webflow_injection_definitivo.js...');

// Ler o arquivo original
const content = fs.readFileSync('webflow_injection_definitivo.js', 'utf8');
console.log(`📊 Tamanho original: ${content.length} caracteres`);

// Funções e classes que devem ser REMOVIDAS (já existem no Footer Code)
const functionsToRemove = [
    // Classe FormValidator completa
    'class FormValidator',
    
    // Métodos de validação individuais
    'validarCPFFormato',
    'validarCPFAlgoritmo', 
    'validateCPF',
    'validateCEP',
    'validarPlacaFormato',
    'validatePlaca',
    'validarCelularLocal',
    'validarCelularApi',
    'validateCelular',
    'validarEmailLocal',
    'validateEmail',
    
    // Métodos de conversão de campos
    'convertEstadoCivil',
    'convertSexo',
    'convertTipoVeiculo',
    
    // Métodos de coleta e processamento de dados
    'collectFormData',
    'removeDuplicateFields',
    'applyFieldConversions',
    
    // Métodos de validação e alertas
    'validateFormData',
    'showValidationAlert',
    'focusFirstErrorField',
    'setFieldValue',
    
    // Event listeners duplicados
    'setupEventListeners',
    'setupFormSubmission'
];

let cleanedContent = content;
let totalRemoved = 0;

// Remover cada função/classe
functionsToRemove.forEach(funcName => {
    const regex = new RegExp(`\\b${funcName}\\b[^}]*\\}`, 'g');
    const matches = cleanedContent.match(regex);
    
    if (matches) {
        matches.forEach(match => {
            totalRemoved += match.length;
            cleanedContent = cleanedContent.replace(match, '');
            console.log(`🗑️ Removido: ${funcName} (${match.length} caracteres)`);
        });
    }
});

// Remover linhas vazias excessivas (mais de 2 consecutivas)
cleanedContent = cleanedContent.replace(/\n\s*\n\s*\n/g, '\n\n');

// Remover comentários de debug excessivos (manter apenas os essenciais)
const debugComments = [
    /\/\/ DEBUG:.*$/gm,
    /\/\/ Teste:.*$/gm,
    /\/\/ Verificar:.*$/gm
];

debugComments.forEach(pattern => {
    cleanedContent = cleanedContent.replace(pattern, '');
});

console.log(`📊 Total removido: ${totalRemoved} caracteres`);
console.log(`📊 Tamanho final: ${cleanedContent.length} caracteres`);
console.log(`📊 Redução: ${((totalRemoved / content.length) * 100).toFixed(1)}%`);

// Salvar arquivo limpo
fs.writeFileSync('webflow_injection_limpo.js', cleanedContent);
console.log('✅ Arquivo limpo salvo como: webflow_injection_limpo.js');

// Verificar se as classes essenciais ainda estão presentes
const essentialClasses = ['SpinnerTimer', 'ProgressModalRPA', 'MainPage'];
essentialClasses.forEach(className => {
    if (cleanedContent.includes(className)) {
        console.log(`✅ Classe essencial mantida: ${className}`);
    } else {
        console.log(`❌ ATENÇÃO: Classe essencial removida: ${className}`);
    }
});

console.log('🎉 Limpeza concluída!');

