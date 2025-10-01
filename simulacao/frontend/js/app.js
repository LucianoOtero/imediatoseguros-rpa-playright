// Aplicação principal
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('seguro-form');
    
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Coletar dados do formulário
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());
        
        // Executar RPA
        const result = await executeRPA(data);
        
        if (result.success) {
            console.log('RPA iniciado com sucesso!');
        } else {
            alert('Erro ao iniciar cálculo: ' + result.error);
        }
    });
});


