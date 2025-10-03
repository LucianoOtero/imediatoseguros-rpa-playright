/**
 * Debug Modal RPA Real
 * JavaScript para debugar problemas de conexão e execução
 */

console.log('🔍 DEBUG: Carregando script de debug...');

// Debug function para testar API connectivity
async function debugAPIConnectivity() {
    console.log('🔍 DEBUG: Testando conectividade com API...');
    
    const apiUrl = 'https://rpaimediatoseguros.com.br/api/rpa';
    
    try {
        // Testar endpoint health
        console.log('🔍 DEBUG: Testando /health...');
        const healthResponse = await fetch(`${apiUrl}/health`, {
            method: 'GET',
            headers: {
                'Accept': 'application/json'
            }
        });
        
        console.log('📊 DEBUG: Response status:', healthResponse.status);
        console.log('📊 DEBUG: Response headers:', [...healthResponse.headers.entries()]);
        
        if (healthResponse.ok) {
            const healthData = await healthResponse.json();
            console.log('✅ DEBUG: Health check OK:', healthData);
            return true;
        } else {
            const errorText = await healthResponse.text();
            console.log('❌ DEBUG: Health check FAILED:', errorText);
            return false;
        }
        
    } catch (error) {
        console.error('❌ DEBUG: Exception na conexão:', error);
        return false;
    }
}

// Debug function para testar dados do formulário
function debugFormData() {
    console.log('🔍 DEBUG: Testando coleta de dados do formulário...');
    
    const form = document.getElementById('rpa-form');
    if (!form) {
        console.error('❌ DEBUG: Formulário não encontrado!');
        return null;
    }
    
    console.log('✅ DEBUG: Formulário encontrado');
    
    const formData = new FormData(form);
    const data = {};
    
    // Convert FormData to object
    for (let [key, value] of formData.entries()) {
        data[key] = value;
        console.log(`📋 DEBUG: Campo ${key}: ${value}`);
    }
    
    // Validate required fields
    const requiredFields = ['cpf', 'nome', 'placa', 'cep'];
    for (let field of requiredFields) {
        if (!data[field] || data[field]. trim() === '') {
            console.error(`❌ DEBUG: Campo obrigatório vazio: ${field}`);
            return null;
        }
    }
    
    console.log('✅ DEBUG: Todos os campos obrigatórios preenchidos');
    return data;
}

// Debug function para testar POST para /start
async function debugStartRPA(formData) {
    console.log('🔍 DEBUG: Testando POST para /start...');
    
    const apiUrl = 'https://rpaimediatoseguros.com.br/api/rpa';
    
    try {
        const response = await fetch(`${apiUrl}/start`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        console.log('📊 DEBUG: Start status:', response.status);
        console.log('📊 DEBUG: Start headers:', [...response.headers.entries()]);
        
        if (response.ok) {
            const result = await response.json();
            console.log('✅ DEBUG: Start successful:', result);
            return result.session_id;
        } else {
            const errorText = await response.text();
            console.log('❌ DEBUG: Start failed:', errorText);
            
            try {
                const errorJson = JSON.parse(errorText);
                console.log('📊 DEBUG: Error JSON:', errorJson);
            } catch (e) {
                console.log('📊 DEBUG: Error não é JSON válido');
            }
            
            return null;
        }
        
    } catch (error) {
        console.error('❌ DEBUG: Exception no start:', error);
        return null;
    }
}

// Debug function para testar GET para /progress
async function debugProgressCheck(sessionId) {
    console.log('🔍 DEBUG: Testando GET para /progress...');
    
    const apiUrl = 'https://rpaimediatoseguros.com.br/api/rpa';
    
    try {
        const response = await fetch(`${apiUrl}/progress/${sessionId}`, {
            method: 'GET',
            headers: {
                'Accept': 'application/json'
            }
        });
        
        console.log('📊 DEBUG: Progress status:', response.status);
        
        if (response.ok) {
            const result = await response.json();
            console.log('✅ DEBUG: Progress successful:', result);
            return true;
        } else {
            const errorText = await response.text();
            console.log('❌ DEBUG: Progress failed:', errorText);
            return false;
        }
        
    } catch (error) {
        console.error('❌ DEBUG: Exception no progress:', error);
        return false;
    }
}

// Debug completo
async function runCompleteDebug() {
    console.log('🚀 DEBUG: Iniciando debug completo...');
    
    // 1. Testar conectividade
    const connectivityOk = await debugAPIConnectivity();
    
    // 2. Testar dados do formulário
    const formData = debugFormData();
    
    // 3. Se dados OK e conectividade OK, testar start
    if (formData && connectivityOk) {
        const response = await fetch('https://rpaimediatoseguros.com.br/api/rpa/health', {
            method: 'GET',
            headers: {
                'Accept': 'application/json'
            }
        });
        
        if (response.ok) {
            const sessionId = await debugStartRPA(formData);
            
            // 4. Se start OK, testar progress
            if (sessionId) {
                await debugProgressCheck(sessionId);
            }
        }
    }
    
    console.log('🏁 DEBUG: Debug completo finalizado');
}

// Expor funções globalmente para teste
window.debugAPI = {
    connectivity: debugAPIConnectivity,
    formData: debugFormData,
    startRPA: debugStartRPA,
    progress: debugProgressCheck,
    runComplete: runCompleteDebug
};

// Auto-executar quando página carregar
document.addEventListener('DOMContentLoaded', () => {
    console.log('🔍 DEBUG: Página carregada, funções de debug disponíveis');
    console.log('🔧 DEBUG: Use debugAPI.runComplete() para teste completo');
});

console.log('✅ DEBUG: Script de debug carregado');
