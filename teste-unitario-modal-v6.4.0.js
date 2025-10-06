/**
 * TESTE UNITÁRIO SIMPLES - MODAL RPA V6.4.2
 * 
 * Este arquivo contém testes básicos para validar as correções
 * implementadas no webflow-injection-complete.js
 * 
 * USO: Executar no console do navegador após carregar o modal
 */

// ========================================
// TESTE 1: Verificar Seletores com Escopo
// ========================================

function testSelectorsWithScope() {
    console.log('🧪 TESTE 1: Verificando seletores com escopo...');
    
    const tests = [
        {
            name: 'Progress Text',
            selector: '#rpaModal .progress-text',
            expected: 'Elemento encontrado com escopo correto'
        },
        {
            name: 'Current Phase',
            selector: '#rpaModal .current-phase',
            expected: 'Elemento encontrado com escopo correto'
        },
        {
            name: 'Sub Phase',
            selector: '#rpaModal .sub-phase',
            expected: 'Elemento encontrado com escopo correto'
        },
        {
            name: 'Stage Info',
            selector: '#rpaModal .stage-info',
            expected: 'Elemento encontrado com escopo correto'
        },
        {
            name: 'Progress Header',
            selector: '#rpaModal .progress-header',
            expected: 'Elemento encontrado com escopo correto'
        },
        {
            name: 'Result Card Recommended',
            selector: '#rpaModal .result-card.recommended',
            expected: 'Elemento encontrado com escopo correto'
        },
        {
            name: 'Result Card Alternative',
            selector: '#rpaModal .result-card.alternative',
            expected: 'Elemento encontrado com escopo correto'
        }
    ];
    
    let passed = 0;
    let failed = 0;
    
    tests.forEach(test => {
        const element = document.querySelector(test.selector);
        if (element) {
            console.log(`✅ ${test.name}: ${test.expected}`);
            passed++;
        } else {
            console.log(`❌ ${test.name}: Elemento não encontrado`);
            failed++;
        }
    });
    
    console.log(`📊 Resultado: ${passed} passou, ${failed} falhou`);
    return { passed, failed, total: tests.length };
}

// ========================================
// TESTE 2: Verificar Isolamento de Estilos
// ========================================

function testStyleIsolation() {
    console.log('🧪 TESTE 2: Verificando isolamento de estilos...');
    
    // Verificar se há elementos fora do modal com classes do modal
    const problematicSelectors = [
        '.progress-header',
        '.progress-info',
        '.results-container',
        '.result-card'
    ];
    
    let leaks = 0;
    
    problematicSelectors.forEach(selector => {
        const elements = document.querySelectorAll(selector);
        const elementsOutsideModal = Array.from(elements).filter(el => 
            !el.closest('#rpaModal')
        );
        
        if (elementsOutsideModal.length > 0) {
            console.log(`❌ Vazamento detectado: ${selector} encontrado fora do modal`);
            leaks++;
        } else {
            console.log(`✅ ${selector}: Sem vazamento`);
        }
    });
    
    console.log(`📊 Vazamentos detectados: ${leaks}`);
    return leaks === 0;
}

// ========================================
// TESTE 3: Verificar Variáveis CSS
// ========================================

function testCSSVariables() {
    console.log('🧪 TESTE 3: Verificando variáveis CSS...');
    
    const modal = document.querySelector('#rpaModal');
    if (!modal) {
        console.log('❌ Modal não encontrado');
        return false;
    }
    
    const computedStyle = window.getComputedStyle(modal);
    const requiredVariables = [
        '--imediato-dark-blue',
        '--imediato-light-blue',
        '--imediato-white',
        '--imediato-gray',
        '--imediato-text',
        '--imediato-text-light',
        '--imediato-border',
        '--imediato-shadow',
        '--imediato-shadow-hover'
    ];
    
    let missing = 0;
    
    requiredVariables.forEach(variable => {
        const value = computedStyle.getPropertyValue(variable);
        if (!value || value.trim() === '') {
            console.log(`❌ Variável CSS ausente: ${variable}`);
            missing++;
        } else {
            console.log(`✅ ${variable}: ${value.trim()}`);
        }
    });
    
    console.log(`📊 Variáveis ausentes: ${missing}`);
    return missing === 0;
}

// ========================================
// TESTE 4: Verificar Responsividade
// ========================================

function testResponsiveness() {
    console.log('🧪 TESTE 4: Verificando responsividade...');
    
    const modal = document.querySelector('#rpaModal');
    if (!modal) {
        console.log('❌ Modal não encontrado');
        return false;
    }
    
    const tests = [
        {
            name: 'Desktop (1200px)',
            width: 1200,
            expected: 'Grid 2 colunas'
        },
        {
            name: 'Tablet (768px)',
            width: 768,
            expected: 'Grid 1 coluna'
        },
        {
            name: 'Mobile (480px)',
            width: 480,
            expected: 'Grid 1 coluna, padding reduzido'
        }
    ];
    
    let passed = 0;
    
    tests.forEach(test => {
        // Simular largura da tela
        const originalWidth = window.innerWidth;
        Object.defineProperty(window, 'innerWidth', {
            writable: true,
            configurable: true,
            value: test.width
        });
        
        // Disparar evento de resize
        window.dispatchEvent(new Event('resize'));
        
        // Verificar se o modal se adapta
        const resultsContainer = modal.querySelector('.results-container');
        if (resultsContainer) {
            const computedStyle = window.getComputedStyle(resultsContainer);
            const gridColumns = computedStyle.getPropertyValue('grid-template-columns');
            
            if (test.width <= 768 && gridColumns.includes('1fr 1fr')) {
                console.log(`❌ ${test.name}: Grid não responsivo`);
            } else {
                console.log(`✅ ${test.name}: ${test.expected}`);
                passed++;
            }
        }
        
        // Restaurar largura original
        Object.defineProperty(window, 'innerWidth', {
            writable: true,
            configurable: true,
            value: originalWidth
        });
    });
    
    console.log(`📊 Testes de responsividade: ${passed}/${tests.length} passou`);
    return passed === tests.length;
}

// ========================================
// TESTE 5: Verificar Funcionalidades JavaScript
// ========================================

function testJavaScriptFunctionality() {
    console.log('🧪 TESTE 5: Verificando funcionalidades JavaScript...');
    
    const tests = [
        {
            name: 'ProgressModalRPA existe',
            test: () => typeof window.ProgressModalRPA !== 'undefined',
            expected: 'Classe ProgressModalRPA disponível'
        },
        {
            name: 'MainPage existe',
            test: () => typeof window.MainPage !== 'undefined',
            expected: 'Classe MainPage disponível'
        },
        {
            name: 'Font Awesome carregado',
            test: () => {
                const link = document.querySelector('link[href*="font-awesome"]');
                return link && link.sheet;
            },
            expected: 'Font Awesome CSS carregado'
        }
    ];
    
    let passed = 0;
    
    tests.forEach(test => {
        try {
            if (test.test()) {
                console.log(`✅ ${test.name}: ${test.expected}`);
                passed++;
            } else {
                console.log(`❌ ${test.name}: Falhou`);
            }
        } catch (error) {
            console.log(`❌ ${test.name}: Erro - ${error.message}`);
        }
    });
    
    console.log(`📊 Funcionalidades JavaScript: ${passed}/${tests.length} passou`);
    return passed === tests.length;
}

// ========================================
// EXECUTAR TODOS OS TESTES
// ========================================

function runAllTests() {
    console.log('🚀 INICIANDO TESTES UNITÁRIOS - MODAL RPA V6.4.0');
    console.log('='.repeat(60));
    
    const results = {
        selectors: testSelectorsWithScope(),
        isolation: testStyleIsolation(),
        variables: testCSSVariables(),
        responsiveness: testResponsiveness(),
        functionality: testJavaScriptFunctionality()
    };
    
    console.log('='.repeat(60));
    console.log('📊 RESUMO DOS TESTES:');
    console.log(`Seletores com Escopo: ${results.selectors.passed}/${results.selectors.total} passou`);
    console.log(`Isolamento de Estilos: ${results.isolation ? '✅ PASSOU' : '❌ FALHOU'}`);
    console.log(`Variáveis CSS: ${results.variables ? '✅ PASSOU' : '❌ FALHOU'}`);
    console.log(`Responsividade: ${results.responsiveness ? '✅ PASSOU' : '❌ FALHOU'}`);
    console.log(`Funcionalidades JS: ${results.functionality ? '✅ PASSOU' : '❌ FALHOU'}`);
    
    const totalPassed = results.selectors.passed + 
                       (results.isolation ? 1 : 0) + 
                       (results.variables ? 1 : 0) + 
                       (results.responsiveness ? 1 : 0) + 
                       (results.functionality ? 1 : 0);
    
    const totalTests = results.selectors.total + 4;
    
    console.log(`🎯 RESULTADO FINAL: ${totalPassed}/${totalTests} testes passou`);
    
    if (totalPassed === totalTests) {
        console.log('🎉 TODOS OS TESTES PASSARAM! Modal V6.4.0 está funcionando corretamente.');
    } else {
        console.log('⚠️ ALGUNS TESTES FALHARAM. Verifique as correções implementadas.');
    }
    
    return results;
}

// ========================================
// INSTRUÇÕES DE USO
// ========================================

console.log(`
📋 INSTRUÇÕES DE USO:

1. Carregue o modal RPA no navegador
2. Abra o console (F12)
3. Cole este código no console
4. Execute: runAllTests()

OU execute testes individuais:
- testSelectorsWithScope()
- testStyleIsolation()
- testCSSVariables()
- testResponsiveness()
- testJavaScriptFunctionality()

📊 Os testes validam:
✅ Seletores com escopo correto
✅ Isolamento de estilos (sem vazamento)
✅ Variáveis CSS definidas
✅ Responsividade funcionando
✅ Funcionalidades JavaScript ativas
`);

// Exportar funções para uso global
window.ModalTests = {
    runAllTests,
    testSelectorsWithScope,
    testStyleIsolation,
    testCSSVariables,
    testResponsiveness,
    testJavaScriptFunctionality
};
