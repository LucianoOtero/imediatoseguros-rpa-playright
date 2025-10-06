/**
 * Página Principal - Imediato Seguros V6.3.0
 * Versão simplificada sem estimativas iniciais
 */

class MainPage {
    constructor() {
        this.sessionId = null;
        this.modalProgress = null;
        
        // Dados fixos (hardcoded)
        this.fixedData = {
            // Dados pessoais fixos
            telefone: "11999999999",
            email: "cliente@exemplo.com",
            profissao: "Empresário",
            renda_mensal: "10000",
            
            // Dados do veículo fixos
            modelo: "Civic",
            ano: "2020",
            cor: "Prata",
            combustivel: "Flex",
            zero_km: "false",
            uso: "Particular",
            garagem: "true",
            
            // Dados do seguro fixos
            tipo_seguro: "Comprehensive",
            franquia: "500",
            cobertura_adicional: "true",
            assistencia_24h: "true",
            
            // Dados adicionais fixos
            cnh_categoria: "B",
            tempo_habilitacao: "5",
            sinistros_ultimos_5_anos: "0",
            condutores_adicionais: "1"
        };
        
        this.init();
    }
    
    /**
     * Inicializar página
     */
    init() {
        console.log('🚀 Inicializando Página Principal V6.3.0...');
        
        // Aguardar DOM estar pronto
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.setupEventListeners());
        } else {
            this.setupEventListeners();
        }
        
        // Configurar validação em tempo real removida - não necessária
        console.log('✅ Página Principal inicializada');
        console.log('📋 Modal simplificado - apenas resultados finais');
    }
    
    /**
     * Configurar event listeners
     */
    setupEventListeners() {
        const form = document.getElementById('rpa-form');
        const btnCalculate = document.getElementById('btnCalculate');
        
        if (!form || !btnCalculate) {
            console.error('❌ Elementos do formulário não encontrados');
            return;
        }
        
        form.addEventListener('submit', (e) => this.handleFormSubmit(e));
        
        console.log('📝 Event listeners configurados');
    }
    
    /**
     * Mostrar erro no formulário
     */
    showFormError(message) {
        // Remover modal se existir
        const modal = document.getElementById('rpaModal');
        if (modal) {
            modal.remove();
        }
        
        // Mostrar erro
        alert(message);
    }
}

// Inicializar quando DOM estiver pronto
document.addEventListener('DOMContentLoaded', () => {
    window.mainPage = new MainPage();
});
