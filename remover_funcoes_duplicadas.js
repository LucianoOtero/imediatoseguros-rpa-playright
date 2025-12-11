const fs = require('fs');

console.log('🧹 Iniciando remoção rigorosa de funções duplicadas...');

// Ler o arquivo limpo
const content = fs.readFileSync('webflow_injection_limpo.js', 'utf8');
console.log(`📊 Tamanho original: ${content.length} caracteres`);

let cleanedContent = content;
let totalRemoved = 0;

// 1. REMOVER CLASSE FormValidator COMPLETA
console.log('\n🗑️ Removendo classe FormValidator...');
const formValidatorRegex = /class FormValidator\s*\{[^}]*\}/g;
const formValidatorMatches = cleanedContent.match(formValidatorRegex);
if (formValidatorMatches) {
    formValidatorMatches.forEach(match => {
        totalRemoved += match.length;
        cleanedContent = cleanedContent.replace(match, '');
        console.log(`   ✅ FormValidator removida (${match.length} caracteres)`);
    });
}

// 2. REMOVER MÉTODOS DE VALIDAÇÃO INDIVIDUAIS
const validationMethods = [
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
    'validateEmail'
];

console.log('\n🗑️ Removendo métodos de validação...');
validationMethods.forEach(method => {
    const regex = new RegExp(`\\b${method}\\s*\\([^}]*\\}\\s*`, 'g');
    const matches = cleanedContent.match(regex);
    if (matches) {
        matches.forEach(match => {
            totalRemoved += match.length;
            cleanedContent = cleanedContent.replace(match, '');
            console.log(`   ✅ ${method} removido (${match.length} caracteres)`);
        });
    }
});

// 3. REMOVER MÉTODOS DE CONVERSÃO
const conversionMethods = [
    'convertEstadoCivil',
    'convertSexo',
    'convertTipoVeiculo'
];

console.log('\n🗑️ Removendo métodos de conversão...');
conversionMethods.forEach(method => {
    const regex = new RegExp(`\\b${method}\\s*\\([^}]*\\}\\s*`, 'g');
    const matches = cleanedContent.match(regex);
    if (matches) {
        matches.forEach(match => {
            totalRemoved += match.length;
            cleanedContent = cleanedContent.replace(match, '');
            console.log(`   ✅ ${method} removido (${match.length} caracteres)`);
        });
    }
});

// 4. REMOVER MÉTODOS DE COLETA E PROCESSAMENTO
const dataMethods = [
    'collectFormData',
    'removeDuplicateFields',
    'applyFieldConversions'
];

console.log('\n🗑️ Removendo métodos de coleta e processamento...');
dataMethods.forEach(method => {
    const regex = new RegExp(`\\b${method}\\s*\\([^}]*\\}\\s*`, 'g');
    const matches = cleanedContent.match(regex);
    if (matches) {
        matches.forEach(match => {
            totalRemoved += match.length;
            cleanedContent = cleanedContent.replace(match, '');
            console.log(`   ✅ ${method} removido (${match.length} caracteres)`);
        });
    }
});

// 5. REMOVER MÉTODOS DE ALERTA
const alertMethods = [
    'showValidationAlert',
    'focusFirstErrorField',
    'setFieldValue'
];

console.log('\n🗑️ Removendo métodos de alerta...');
alertMethods.forEach(method => {
    const regex = new RegExp(`\\b${method}\\s*\\([^}]*\\}\\s*`, 'g');
    const matches = cleanedContent.match(regex);
    if (matches) {
        matches.forEach(match => {
            totalRemoved += match.length;
            cleanedContent = cleanedContent.replace(match, '');
            console.log(`   ✅ ${method} removido (${match.length} caracteres)`);
        });
    }
});

// 6. REMOVER EVENT LISTENERS DUPLICADOS
const eventMethods = [
    'setupEventListeners',
    'setupFormSubmission'
];

console.log('\n🗑️ Removendo event listeners duplicados...');
eventMethods.forEach(method => {
    const regex = new RegExp(`\\b${method}\\s*\\([^}]*\\}\\s*`, 'g');
    const matches = cleanedContent.match(regex);
    if (matches) {
        matches.forEach(match => {
            totalRemoved += match.length;
            cleanedContent = cleanedContent.replace(match, '');
            console.log(`   ✅ ${method} removido (${match.length} caracteres)`);
        });
    }
});

console.log(`\n📊 Total removido: ${totalRemoved} caracteres`);
console.log(`📊 Tamanho final: ${cleanedContent.length} caracteres`);
console.log(`📊 Redução: ${((totalRemoved / content.length) * 100).toFixed(1)}%`);

// Salvar arquivo limpo
fs.writeFileSync('webflow_injection_limpo.js', cleanedContent);
console.log('\n✅ Arquivo limpo salvo como: webflow_injection_limpo.js');

// Verificar se as classes essenciais ainda estão presentes
console.log('\n🔍 Verificação de funcionalidades essenciais:');
const essentialClasses = ['SpinnerTimer', 'ProgressModalRPA', 'MainPage'];
essentialClasses.forEach(className => {
    if (cleanedContent.includes(className)) {
        console.log(`✅ Classe essencial mantida: ${className}`);
    } else {
        console.log(`❌ ATENÇÃO: Classe essencial removida: ${className}`);
    }
});

// Verificar se métodos essenciais do RPA estão presentes
const essentialRPAMethods = ['handleFormSubmit', 'openProgressModal', 'initializeProgressModal'];
essentialRPAMethods.forEach(method => {
    if (cleanedContent.includes(method)) {
        console.log(`✅ Método RPA essencial mantido: ${method}`);
    } else {
        console.log(`❌ ATENÇÃO: Método RPA essencial removido: ${method}`);
    }
});

console.log('\n🎉 Remoção de funções duplicadas concluída!');

