# 📋 PROJETO: VALIDAÇÃO COMPLETA DE FORMULÁRIO NO RPA

## 🎯 **OBJETIVO**
Replicar exatamente a validação do Footer Code Site.js no `new_webflow-injection-complete.js`, incluindo SweetAlert com opção "Prosseguir assim mesmo", mas **SEM executar o RPA** quando dados estão inválidos.

## 🔍 **ANÁLISE ATUAL**

### **Footer Code Site.js (Validação Completa):**
- ✅ **CPF**: Algoritmo + PH3A (desabilitada)
- ✅ **CEP**: ViaCEP API
- ✅ **Placa**: API FIPE (mdmidia.com.br)
- ✅ **Celular**: Apilayer + validação local
- ✅ **Email**: Regex + SafetyMails
- ✅ **SweetAlert**: "Corrigir" ou "Prosseguir assim mesmo"
- ✅ **Auto-preenchimento**: MARCA/ANO/TIPO (placa) + SEXO/DATA/ESTADO-CIVIL (CPF)

### **new_webflow-injection-complete.js (Atual):**
- ❌ **Sem validação** de campos
- ❌ **Sem SweetAlert** de validação
- ❌ **Executa RPA** mesmo com dados inválidos
- ❌ **Sem auto-preenchimento**

## 📋 **PLANO DE IMPLEMENTAÇÃO**

### **FASE 1: ANÁLISE E PREPARAÇÃO**

#### **1.0 BACKUP LOCAL (CRÍTICO)**
```bash
# Criar backup do JavaScript atual
copy new_webflow-injection-complete.js new_webflow-injection-complete_BACKUP_V6.12.1.js
```
**✅ BACKUP CRIADO**: `new_webflow-injection-complete_BACKUP_V6.12.1.js`

#### **1.1 Mapear Funções de Validação**
```javascript
// Funções a replicar do Footer Code:
- validarCPFFormato(cpf)
- validarCPFAlgoritmo(cpf)
- validarCepViaCep(cep)
- validarPlacaFormato(p)
- validarPlacaApi(placa)
- validarCelularLocal(ddd, numero)
- validarCelularApi(nat)
- validarEmailLocal(v)
- extractVehicleFromPlacaFipe(apiJson)
- extractDataFromPH3A(apiJson)
```

#### **1.2 Mapear Configurações**
```javascript
// Configurações a replicar:
const USE_PHONE_API = true;
const APILAYER_KEY = 'dce92fa84152098a3b5b7b8db24debbc';
const SAFETY_BASE = 'https://optin.safetymails.com/main/safetyoptin/...';
const VALIDAR_PH3A = false; // Manter desabilitada
```

#### **1.3 Mapear Helpers**
```javascript
// Helpers a replicar:
- onlyDigits(s)
- toUpperNospace(s)
- showLoading(txt)
- hideLoading()
- setFieldValue(id, val)
```

### **FASE 2: IMPLEMENTAÇÃO DAS VALIDAÇÕES**

#### **2.1 Adicionar Classe de Validação**
```javascript
class FormValidator {
    constructor() {
        this.config = {
            USE_PHONE_API: true,
            APILAYER_KEY: 'dce92fa84152098a3b5b7b8db24debbc',
            SAFETY_BASE: 'https://optin.safetymails.com/main/safetyoptin/...',
            VALIDAR_PH3A: false
        };
    }
    
    // Implementar todas as funções de validação
    // CPF, CEP, Placa, Celular, Email
}
```

#### **2.2 Implementar Loading Overlay**
```javascript
// Replicar exatamente o loading do Footer Code
initLoading() {
    // Criar overlay com spinner
    // showLoading() e hideLoading()
}
```

#### **2.3 Implementar Auto-preenchimento**
```javascript
// Replicar setFieldValue() do Footer Code
setFieldValue(id, val) {
    const $field = $(`#${id}, [name="${id}"]`);
    if ($field.length) {
        $field.val(val).trigger('input').trigger('change');
    }
}
```

### **FASE 3: INTEGRAÇÃO COM RPA**

#### **3.1 Modificar handleFormSubmit()**
```javascript
async handleFormSubmit(form) {
    try {
        // 1. Coletar dados do formulário
        const formData = this.collectFormData(form);
        
        // 2. VALIDAÇÃO COMPLETA (NOVO)
        const validationResult = await this.validateFormData(formData);
        
        // 3. Se inválido, mostrar SweetAlert
        if (!validationResult.isValid) {
            await this.showValidationAlert(validationResult.errors);
            return; // NÃO executar RPA
        }
        
        // 4. Se válido, executar RPA normalmente
        await this.executeRPA(formData);
        
    } catch (error) {
        console.error('Erro no handleFormSubmit:', error);
    }
}
```

#### **3.2 Implementar Validação Completa**
```javascript
async validateFormData(formData) {
    const validator = new FormValidator();
    
    // Executar todas as validações em paralelo
    const [cpfResult, cepResult, placaResult, celularResult, emailResult] = await Promise.all([
        validator.validateCPF(formData.cpf),
        validator.validateCEP(formData.cep),
        validator.validatePlaca(formData.placa),
        validator.validateCelular(formData.ddd_celular, formData.celular),
        validator.validateEmail(formData.email)
    ]);
    
    // Auto-preenchimento se válido
    if (placaResult.ok && placaResult.parsed) {
        this.setFieldValue('MARCA', placaResult.parsed.marcaTxt);
        this.setFieldValue('ANO', placaResult.parsed.anoModelo);
        this.setFieldValue('TIPO-DE-VEICULO', placaResult.parsed.tipoVeiculo);
    }
    
    if (cpfResult.ok && cpfResult.parsed && this.config.VALIDAR_PH3A) {
        this.setFieldValue('SEXO', cpfResult.parsed.sexo);
        this.setFieldValue('DATA-DE-NASCIMENTO', cpfResult.parsed.dataNascimento);
        this.setFieldValue('ESTADO-CIVIL', cpfResult.parsed.estadoCivil);
    }
    
    return {
        isValid: cpfResult.ok && cepResult.ok && placaResult.ok && celularResult.ok && emailResult.ok,
        errors: {
            cpf: cpfResult,
            cep: cepResult,
            placa: placaResult,
            celular: celularResult,
            email: emailResult
        }
    };
}
```

#### **3.3 Implementar SweetAlert de Validação**
```javascript
async showValidationAlert(errors) {
    let errorLines = "";
    if (!errors.cpf.ok) errorLines += "• CPF inválido\n";
    if (!errors.cep.ok) errorLines += "• CEP inválido\n";
    if (!errors.placa.ok) errorLines += "• Placa inválida\n";
    if (!errors.celular.ok) errorLines += "• Celular inválido\n";
    if (!errors.email.ok) errorLines += "• E-mail inválido\n";
    
    const result = await Swal.fire({
        icon: 'info',
        title: 'Atenção!',
        html: 
            "⚠️ Os campos CPF, CEP, PLACA, CELULAR e E-MAIL corretamente preenchidos são necessários para efetuar o cálculo do seguro.\n\n" +
            "Campos com problema:\n\n" + errorLines + "\n" +
            "Caso decida prosseguir assim mesmo, um especialista entrará em contato para coletar esses dados.",
        showCancelButton: true,
        confirmButtonText: 'Prosseguir assim mesmo',
        cancelButtonText: 'Corrigir',
        reverseButtons: true,
        allowOutsideClick: false,
        allowEscapeKey: true
    });
    
    if (result.isConfirmed) {
        // NÃO executar RPA - redirecionar para página de sucesso
        window.location.href = 'https://www.segurosimediato.com.br/sucesso';
    } else {
        // Focar no primeiro campo com erro
        this.focusFirstErrorField(errors);
    }
}
```

### **FASE 4: DESABILITAR VALIDAÇÃO DO FOOTER**

#### **4.1 Comentar Interceptação do Footer**
```javascript
// Footer Code Site.js - COMENTAR estas linhas:
// $form.on('submit', function(ev){
//     ev.preventDefault();
//     // ... toda a validação
// });
```

#### **4.2 Manter Apenas Bibliotecas**
```javascript
// Footer Code Site.js - MANTER apenas:
- jQuery e jQuery.mask
- SweetAlert2 (ou remover se duplicado)
- Máscaras de campos
- Funções de GCLID
```

### **FASE 5: TESTES E VALIDAÇÃO**

#### **5.1 Testes de Validação**
- [ ] CPF inválido → SweetAlert + não executa RPA
- [ ] CEP inválido → SweetAlert + não executa RPA
- [ ] Placa inválida → SweetAlert + não executa RPA
- [ ] Celular inválido → SweetAlert + não executa RPA
- [ ] Email inválido → SweetAlert + não executa RPA
- [ ] Múltiplos erros → SweetAlert com lista + não executa RPA

#### **5.2 Testes de Auto-preenchimento**
- [ ] Placa válida → preenche MARCA/ANO/TIPO
- [ ] CPF válido (se PH3A ativa) → preenche SEXO/DATA/ESTADO-CIVIL

#### **5.3 Testes de Fluxo**
- [ ] Dados válidos → executa RPA normalmente
- [ ] Dados inválidos + "Prosseguir" → redireciona para página de sucesso
- [ ] Dados inválidos + "Corrigir" → foca campo com erro

## 🎯 **RESULTADO ESPERADO**

### **✅ COMPORTAMENTO CORRETO:**
1. **Validação Completa**: CPF, CEP, Placa, Celular, Email
2. **SweetAlert**: "Corrigir" ou "Prosseguir assim mesmo"
3. **Auto-preenchimento**: MARCA/ANO/TIPO + SEXO/DATA/ESTADO-CIVIL
4. **RPA Bloqueado**: Não executa com dados inválidos
5. **Redirecionamento**: Se prosseguir com dados inválidos → página de sucesso

### **❌ COMPORTAMENTO ATUAL:**
1. **Sem Validação**: Executa RPA com qualquer dado
2. **Sem SweetAlert**: Não avisa sobre problemas
3. **Sem Auto-preenchimento**: Usuário preenche tudo manualmente
4. **RPA Sempre Executa**: Mesmo com dados inválidos

## 📊 **ARQUIVOS A MODIFICAR**

### **PRINCIPAIS:**
- `new_webflow-injection-complete.js` → Adicionar validação completa
- `Footer Code Site.js` → Comentar interceptação de submit

### **BACKUPS:**
- `new_webflow-injection-complete_BACKUP_V6.12.1.js` → ✅ BACKUP CRIADO
- `Footer Code Site_BACKUP.js` → Criar antes de comentar

### **TESTES:**
- `new_index.html` → Testar validação
- `test-timer-local.html` → Testar integração

## ⚠️ **CONSIDERAÇÕES IMPORTANTES**

### **1. Compatibilidade com SweetAlert2**
- Verificar se versão do Footer Code é compatível
- Manter tema personalizado do Footer Code

### **2. APIs Externas**
- Manter mesmas URLs (ViaCEP, mdmidia.com.br, Apilayer)
- Manter mesmas chaves de API

### **3. Performance**
- Validações em paralelo (Promise.all)
- Loading overlay durante validação

### **4. UX/UI**
- Manter exatamente o mesmo texto do SweetAlert
- Manter mesmo comportamento de foco nos campos

## 🚀 **CRONOGRAMA ESTIMADO**

- **Fase 1**: 2 horas (análise e mapeamento)
- **Fase 2**: 4 horas (implementação das validações)
- **Fase 3**: 3 horas (integração com RPA)
- **Fase 4**: 1 hora (desabilitar Footer)
- **Fase 5**: 2 horas (testes)

**Total**: ~12 horas de desenvolvimento

---

## 📝 **NOTAS FINAIS**

Este projeto garante que o RPA só seja executado com dados válidos, mantendo a mesma experiência de validação do Footer Code, mas integrada ao fluxo do RPA. A opção "Prosseguir assim mesmo" não executa o RPA, mas sim redireciona para a página de sucesso, evitando falhas no processo automatizado.
