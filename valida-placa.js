/* ========= PLACA ========= */

// Função para converter para maiúsculas e remover espaços
function toUpperNospace(str) {
  return str.toUpperCase().replace(/\s/g, '');
}

// Função para extrair apenas dígitos
function onlyDigits(str) {
  return str.replace(/[^0-9]/g, '');
}

function validarPlacaFormato(p){
  const placaLimpa = p.toUpperCase().replace(/[^A-Z0-9]/g,'');
  const antigo=/^[A-Z]{3}[0-9]{4}$/;
  const mercosul=/^[A-Z]{3}[0-9][A-Z][0-9]{2}$/;
  return antigo.test(placaLimpa)||mercosul.test(placaLimpa);
}
function extractVehicleFromPlacaFipe(apiJson){
  const r = apiJson && (apiJson.informacoes_veiculo || apiJson);
  if(!r || typeof r !== 'object') return {marcaTxt:'', anoModelo:'', tipoVeiculo:''};
  
  // Extrair dados da API Placa Fipe
  const fabricante = r.marca || '';
  const modelo = r.modelo || '';
  const anoMod = r.ano || r.ano_modelo || '';
  
  // Determinar tipo de veículo baseado no segmento
  let tipoVeiculo = '';
  if(r.segmento) {
    const segmento = r.segmento.toLowerCase();
    if(segmento.includes('moto')) {
      tipoVeiculo = 'moto';
    } else if(segmento.includes('auto')) {
      tipoVeiculo = 'carro';
    } else {
      // Fallback baseado em marcas conhecidas
      const modeloLower = modelo.toLowerCase();
      const marcaLower = fabricante.toLowerCase();
      
      if(marcaLower.includes('honda') || marcaLower.includes('yamaha') || 
         marcaLower.includes('suzuki') || marcaLower.includes('kawasaki') ||
         modeloLower.includes('cg') || modeloLower.includes('cb') || 
         modeloLower.includes('fazer') || modeloLower.includes('ninja')) {
        tipoVeiculo = 'moto';
      } else {
        tipoVeiculo = 'carro';
      }
    }
  } else {
    // Fallback baseado em marcas conhecidas
    const modeloLower = modelo.toLowerCase();
    const marcaLower = fabricante.toLowerCase();
    
    if(marcaLower.includes('honda') || marcaLower.includes('yamaha') || 
       marcaLower.includes('suzuki') || marcaLower.includes('kawasaki') ||
       modeloLower.includes('cg') || modeloLower.includes('cb') || 
       modeloLower.includes('fazer') || modeloLower.includes('ninja')) {
      tipoVeiculo = 'moto';
    } else {
      tipoVeiculo = 'carro';
    }
  }
  
  return { 
    marcaTxt: [fabricante, modelo].filter(Boolean).join(' / '), 
    anoModelo: onlyDigits(String(anoMod)).slice(0,4),
    tipoVeiculo: tipoVeiculo
  };
}
function validarPlacaApi(placa){
  const raw = toUpperNospace(placa).replace(/[^A-Z0-9]/g,'');
  if(!validarPlacaFormato(raw)) return Promise.resolve({ok:false, reason:'formato'});
  
  // Usar o proxy local para evitar problemas de CORS
  return fetch(`proxy_placa_fipe_final.php?placa=${raw}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json'
    }
  })
    .then(r => r.json())
    .then(j => {
      const ok = !!j && (j.codigo === 1 || j.success === true);
      return {
        ok, 
        reason: ok ? 'ok' : 'nao_encontrada', 
        parsed: ok ? extractVehicleFromPlacaFipe(j) : {marcaTxt:'', anoModelo:'', tipoVeiculo:''}
      };
    })
    .catch(_ => ({ok:false, reason:'erro_api'}));
}

// Função de compatibilidade para código existente
function validarPlaca(placa) {
  return validarPlacaApi(placa);
}
