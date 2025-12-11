/* ========= CPF + API PH3A ========= */

// Função para extrair apenas dígitos
function onlyDigits(str) {
  return str.replace(/[^0-9]/g, '');
}

// Função para validar formato do CPF
function validarCPFFormato(cpf) {
  const cpfLimpo = onlyDigits(cpf);
  return cpfLimpo.length === 11 && !/^(\d)\1{10}$/.test(cpfLimpo);
}

// Função para validar CPF (algoritmo)
function validarCPFAlgoritmo(cpf) {
  cpf = onlyDigits(cpf);
  if (cpf.length !== 11 || /^(\d)\1{10}$/.test(cpf)) return false;
  
  let soma = 0, resto = 0;
  for (let i = 1; i <= 9; i++) {
    soma += parseInt(cpf[i-1], 10) * (11 - i);
  }
  resto = (soma * 10) % 11;
  if (resto === 10 || resto === 11) resto = 0;
  if (resto !== parseInt(cpf[9], 10)) return false;
  
  soma = 0;
  for (let i = 1; i <= 10; i++) {
    soma += parseInt(cpf[i-1], 10) * (12 - i);
  }
  resto = (soma * 10) % 11;
  if (resto === 10 || resto === 11) resto = 0;
  return resto === parseInt(cpf[10], 10);
}

// Função para extrair dados da API PH3A
function extractDataFromPH3A(apiJson) {
  const data = apiJson && apiJson.data;
  if (!data || typeof data !== 'object') {
    return {
      sexo: '',
      dataNascimento: '',
      estadoCivil: ''
    };
  }
  
  // Mapear sexo
  let sexo = '';
  if (data.sexo !== undefined) {
    switch (data.sexo) {
      case 1: sexo = 'Masculino'; break;
      case 2: sexo = 'Feminino'; break;
      default: sexo = ''; break;
    }
  }
  
  // Mapear estado civil
  let estadoCivil = '';
  if (data.estado_civil !== undefined) {
    switch (data.estado_civil) {
      case 0: estadoCivil = 'Solteiro'; break;
      case 1: estadoCivil = 'Casado'; break;
      case 2: estadoCivil = 'Divorciado'; break;
      case 3: estadoCivil = 'Viúvo'; break;
      default: estadoCivil = ''; break;
    }
  }
  
  // Formatar data de nascimento (de ISO para DD/MM/YYYY)
  let dataNascimento = '';
  if (data.data_nascimento) {
    try {
      const date = new Date(data.data_nascimento);
      if (!isNaN(date.getTime())) {
        const day = String(date.getDate()).padStart(2, '0');
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const year = date.getFullYear();
        dataNascimento = `${day}/${month}/${year}`;
      }
    } catch (e) {
      // Se não conseguir formatar, usar como está
      dataNascimento = data.data_nascimento;
    }
  }
  
  return {
    sexo: sexo,
    dataNascimento: dataNascimento,
    estadoCivil: estadoCivil
  };
}

// Função para validar CPF via API PH3A
function validarCPFApi(cpf) {
  const cpfLimpo = onlyDigits(cpf);
  
  // Primeiro validar formato e algoritmo
  if (!validarCPFFormato(cpfLimpo) || !validarCPFAlgoritmo(cpfLimpo)) {
    return Promise.resolve({
      ok: false, 
      reason: 'formato'
    });
  }
  
  // Consultar API PH3A via proxy
  return fetch('https://mdmidia.com.br/cpf-validate.php', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      cpf: cpfLimpo
    })
  })
  .then(r => r.json())
  .then(j => {
    const ok = !!j && (j.codigo === 1 || j.success === true);
    return {
      ok, 
      reason: ok ? 'ok' : 'nao_encontrado', 
      parsed: ok ? extractDataFromPH3A(j) : {
        sexo: '',
        dataNascimento: '',
        estadoCivil: ''
      }
    };
  })
  .catch(_ => ({
    ok: false, 
    reason: 'erro_api'
  }));
}

// Função de compatibilidade para código existente
function validarCPF(cpf) {
  const cpfLimpo = onlyDigits(cpf);
  return validarCPFFormato(cpfLimpo) && validarCPFAlgoritmo(cpfLimpo);
}

// Função para validar CPF completo (formato + algoritmo + API)
function validarCPFCompleto(cpf) {
  return validarCPFApi(cpf);
}



































