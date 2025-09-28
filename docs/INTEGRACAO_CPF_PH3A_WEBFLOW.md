# Integração CPF + API PH3A para Webflow

## **Resumo da Implementação**

Implementação completa da validação de CPF com consulta à API PH3A DataBusca para preenchimento automático dos campos:
- **SEXO**
- **DATA-DE-NASCIMENTO** 
- **ESTADO-CIVIL**

Seguindo o mesmo padrão da validação de placa com API Placa Fipe.

---

## **Arquitetura da Solução**

### **1. Frontend (Webflow)**
- **Validação local:** Formato e algoritmo do CPF
- **Validação externa:** Consulta à API PH3A via proxy
- **Preenchimento automático:** Campos SEXO, DATA-DE-NASCIMENTO, ESTADO-CIVIL

### **2. Proxy (mdmidia.com.br)**
- **Arquivo:** `cpf-validate.php`
- **Função:** Bypass de CORS + autenticação na API PH3A
- **Credenciais:** Gerenciadas no servidor

### **3. API PH3A DataBusca**
- **Endpoint:** `https://api.ph3a.com.br/DataBusca`
- **Autenticação:** Username/Password → Token
- **Consulta:** Dados pessoais por CPF

---

## **Fluxo de Funcionamento**

### **1. Validação no Frontend**
```javascript
// Evento onChange do campo CPF
$CPF.on('change', function(){
  const cpfValue = $(this).val();
  
  // 1. Validação local (formato + algoritmo)
  if (!validarCPFAlgoritmo(cpfValue)) {
    // Exibe alerta de CPF inválido
    return;
  }
  
  // 2. Consulta API PH3A
  showLoading('Consultando dados do CPF…');
  validarCPFApi(cpfValue).then(res => {
    if (res.ok && res.parsed) {
      // 3. Preenchimento automático
      setFieldValue('SEXO', res.parsed.sexo);
      setFieldValue('DATA-DE-NASCIMENTO', res.parsed.dataNascimento);
      setFieldValue('ESTADO-CIVIL', res.parsed.estadoCivil);
    }
  });
});
```

### **2. Consulta via Proxy**
```javascript
function validarCPFApi(cpf) {
  const cpfLimpo = onlyDigits(cpf);
  
  return fetch('https://mdmidia.com.br/cpf-validate.php', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ cpf: cpfLimpo })
  })
  .then(r => r.json())
  .then(j => {
    const ok = !!j && (j.codigo === 1 || j.success === true);
    return {
      ok, 
      parsed: ok ? extractDataFromPH3A(j) : {}
    };
  });
}
```

### **3. Processamento no Proxy**
```php
// cpf-validate.php
$input = json_decode(file_get_contents('php://input'), true);
$cpf = $input['cpf'] ?? '';

// 1. Login na API PH3A
$login_response = curl_exec(/* login request */);
$token = $login_data['data']['Token'];

// 2. Consulta dados do CPF
$data_response = curl_exec(/* data request com token */);

// 3. Retorna dados formatados
echo json_encode([
  "codigo" => 1,
  "success" => true,
  "data" => [
    "sexo" => $mapped_gender,
    "data_nascimento" => $formatted_date,
    "estado_civil" => $mapped_marital_status
  ]
]);
```

---

## **Mapeamento de Dados**

### **Sexo (Gender)**
```javascript
switch (data.sexo) {
  case 1: sexo = 'Masculino'; break;
  case 2: sexo = 'Feminino'; break;
  default: sexo = ''; break;
}
```

### **Estado Civil (MaritalStatus)**
```javascript
switch (data.estado_civil) {
  case 0: estadoCivil = 'Solteiro'; break;
  case 1: estadoCivil = 'Casado'; break;
  case 2: estadoCivil = 'Divorciado'; break;
  case 3: estadoCivil = 'Viúvo'; break;
  default: estadoCivil = ''; break;
}
```

### **Data de Nascimento**
```javascript
// Conversão de ISO para DD/MM/YYYY
const date = new Date(data.data_nascimento);
const day = String(date.getDate()).padStart(2, '0');
const month = String(date.getMonth() + 1).padStart(2, '0');
const year = date.getFullYear();
dataNascimento = `${day}/${month}/${year}`;
```

---

## **Tratamento de Cenários**

### **1. CPF Inválido (Formato/Algoritmo)**
```javascript
if (!validarCPFAlgoritmo(cpfValue)) {
  saWarnConfirmCancel({
    title: 'CPF inválido',
    html: 'Deseja corrigir?'
  });
}
```

### **2. CPF Não Encontrado na Base PH3A**
```javascript
if (res.reason === 'nao_encontrado') {
  saInfoConfirmCancel({
    title: 'CPF não encontrado',
    html: 'O CPF é válido, mas não foi encontrado na nossa base de dados.<br><br>Deseja preencher os dados manualmente?'
  });
}
```

### **3. Erro na API**
```javascript
.catch(_ => {
  hideLoading();
  // Não bloqueia o usuário, apenas registra o erro
  console.log('Erro na consulta da API PH3A');
});
```

---

## **Credenciais da API PH3A**

### **Autenticação**
```php
// Credenciais (no proxy PHP)
$username = 'alex.kaminski@imediatoseguros.com.br';
$password = 'ImdSeg2025$$';
$api_key = '691dd2aa-9af4-84f2-06f9-350e1d709602';
```

### **Endpoints**
- **Login:** `https://api.ph3a.com.br/DataBusca/api/Account/Login`
- **Consulta:** `https://api.ph3a.com.br/DataBusca/data`

---

## **Arquivos Criados**

### **1. Proxy PHP**
- **`cpf-validate.php`** - Proxy para API PH3A (deploy no mdmidia.com.br)

### **2. JavaScript para Webflow**
- **`webflow-cpf-ph3a-integration.js`** - Código para integrar no Webflow
- **`valida-cpf-ph3a.js`** - Funções de validação standalone

### **3. Testes**
- **`teste_cpf_ph3a.html`** - Interface de teste completa

---

## **Integração no Webflow**

### **1. Substituir Validação de CPF Existente**
```javascript
// ANTES (apenas algoritmo local)
$CPF.on('change', function(){
  if (!validarCPF($(this).val())){
    // alerta de CPF inválido
  }
});

// DEPOIS (algoritmo + API PH3A)
$CPF.on('change', function(){
  const cpfValue = $(this).val();
  
  if (!validarCPFAlgoritmo(cpfValue)) {
    // alerta de CPF inválido
    return;
  }
  
  // Consultar API PH3A e preencher campos
  showLoading('Consultando dados do CPF…');
  validarCPFApi(cpfValue).then(res => {
    hideLoading();
    if (res.ok && res.parsed) {
      if (res.parsed.sexo) setFieldValue('SEXO', res.parsed.sexo);
      if (res.parsed.dataNascimento) setFieldValue('DATA-DE-NASCIMENTO', res.parsed.dataNascimento);
      if (res.parsed.estadoCivil) setFieldValue('ESTADO-CIVIL', res.parsed.estadoCivil);
    }
  });
});
```

### **2. Atualizar Validação no Submit**
```javascript
// No Promise.all do submit, substituir:
Promise.resolve($CPF.length ? validarCPF($CPF.val()) : true)

// Por:
$CPF.length ? validarCPFApi($CPF.val()) : Promise.resolve({ok: true})
```

### **3. Campos do Formulário**
Certificar-se de que existem os campos:
- **`#SEXO`** ou **`[name="SEXO"]`**
- **`#DATA-DE-NASCIMENTO`** ou **`[name="DATA-DE-NASCIMENTO"]`**
- **`#ESTADO-CIVIL`** ou **`[name="ESTADO-CIVIL"]`**

---

## **Deploy e Configuração**

### **1. Deploy do Proxy**
1. Fazer upload do `cpf-validate.php` para `mdmidia.com.br`
2. Testar endpoint: `https://mdmidia.com.br/cpf-validate.php`
3. Verificar CORS headers estão configurados

### **2. Atualização do Webflow**
1. Adicionar funções JavaScript no Custom Code
2. Substituir validação de CPF existente
3. Testar preenchimento automático dos campos

### **3. Testes de Validação**
- CPF inválido (formato/algoritmo)
- CPF válido não encontrado na base
- CPF válido encontrado na base
- Erro de conexão com API

---

## **Limitações e Considerações**

### **1. Disponibilidade de Dados**
- Nem todos os CPFs estão na base da API PH3A
- Campos podem retornar vazios mesmo para CPFs válidos
- Usuário pode preencher manualmente se dados não encontrados

### **2. Performance**
- Consulta adicional por CPF pode adicionar latência
- Loading indicator informa usuário sobre processamento
- Timeout configurado para 30 segundos

### **3. Privacidade**
- Dados pessoais consultados via API externa
- Logs devem ser configurados adequadamente
- Conformidade com LGPD deve ser considerada

---

## **Status da Implementação**

- ✅ **Proxy PHP:** Implementado e testado
- ✅ **JavaScript:** Funções de validação e integração
- ✅ **Mapeamento:** Sexo, data nascimento, estado civil
- ✅ **Tratamento de Erros:** Cenários cobertos
- ✅ **Interface de Teste:** Disponível
- ⏳ **Deploy Proxy:** Pendente no mdmidia.com.br
- ⏳ **Integração Webflow:** Aguardando deploy do proxy

**A integração está pronta para deploy e uso em produção.**








