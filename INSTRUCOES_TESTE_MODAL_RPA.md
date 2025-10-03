# 📋 Instruções de Teste - Modal RPA Real

## 🎯 Objetivo do Teste
Testar o fluxo completo de execução do RPA com modal de progresso em tempo real.

## 📁 Arquivos Criados
- `modal_rpa_real.html` - Formulário completo com dados pré-preenchidos
- `modal_rpa_real.css` - Estilos responsivos e animações
- `modal_rpa_real.js` - JavaScript de integração completo

## 🚀 Como Testar

### 1. Abrir o Arquivo
```bash
# Abrir no navegador
start modal_rpa_real.html
# ou
# Clique duplo no arquivo HTML no Windows Explorer
```

### 2. Verificar Formulário
- ✅ Campos pré-preenchidos com dados do `parametros.json`
- ✅ Validação em tempo real de CPF, placa e CEP
- ✅ Estilos responsivos e animações

### 3. Executar Teste Completo
1. **Clique em "Calcular Seguro"**
2. **Observe o modal de progresso:**
   - Barra de progresso (0-100%)
   - 15 fases do RPA com ícones
   - Estimações iniciais e finais
3. **Monitore em tempo real:**
   - Polling a cada 2 segundos
   - Atualização automática da fase atual
   - Captura de valores das Telas 4 e 15

## 🔍 Pontos de Verificação

### Formulário HTML
- [ ] Todos os 30+ campos do `parametros.json` presentes
- [ ] Dados pré-preenchidos corretamente
- [ ] Validação visual em tempo real
- [ ] Design responsivo

### Integração JavaScript
- [ ] Coleta automática de dados do formulário
- [ ] Validação antes do envio
- [ ] Chamada POST para `/api/rpa/start`
- [ ] JSON dinâmico (não estático)

### Modal de Progresso
- [ ] SweetAlert2 integrado corretamente
- [ ] Barra de progresso animada
- [ ] 15 fases do RPA listadas
- [ ] Ícones dinâmicos (pendente → ativo → concluído)

### API e Progresso
- [ ] POST para iniciar RPA funciona
- [ ] GET para progresso retorna dados
- [ ] Polling a cada 2 segundos
- [ ] Session ID gerado corretamente

### Captura de Dados
- [ ] Estimativa inicial (Tela 4)
- [ ] Cálculo final (Tela 15) 
- [ ] Exibição dos valores no modal
- [ ] Botão "Concluído" habilitado no final

## 🛠️ Dados de Teste Utilizados
```json
{
  "cpf": "97137189768",
  "nome": "ALEX KAMINSKI",
  "data_nascimento": "25/04/1970",
  "sexo": "Masculino",
  "estado_civil": "Casado ou Uniao Estavel",
  "email": "alex.kaminski@imediatoseguros.com.br",
  "celular": "11953288466",
  "placa": "EYQ4J41",
  "marca": "TOYOTA",
  "modelo": "COROLLA XEI 1.8/1.8 FLEX 16V MEC",
  "ano": "2009",
  "combustivel": "Flex",
  "tipo_veiculo": "carro",
  "cep": "03317-000",
  "uso_veiculo": "Pessoal",
  "endereco": "Rua Serra de Botucatu, Tatuapé - São Paulo/SP",
  "endereco_completo": "Rua Serra de Botucatu, 410 APTO 11 - São Paulo, SP",
  "condutor_principal": true,
  "nome_condutor": "SANDRA LOUREIRO",
  "cpf_condutor": "25151787829",
  "data_nascimento_condutor": "28/08/1975",
  "sexo_condutor": "Feminino",
  "estado_civil_condutor": "Casado ou Uniao Estavel",
  "garagem_residencia": true,
  "portao_eletronico": "Eletronico",
  "local_de_trabalho": false,
  "estacionamento_proprio_local_de_trabalho": false,
  "local_de_estudo": false,
  "estacionamento_proprio_local_de_estudo": false,
  "zero_km": false,
  "veiculo_segurado": "Não",
  "kit_gas": false,
  "blindado": false,
  "financiado": false,
  "reside_18_26": "Não",
  "continuar_com_corretor_anterior": true
}
```

## 🔧 Configurações do Sistema

### API Endpoint
- **URL**: `https://37.27.92.160/api/rpa`
- **Start**: `POST /start`
- **Progress**: `GET /progress/{session_id}`

### Polling
- **Intervalo**: 2 segundos
- **Retry**: 3 tentativas com backoff exponencial
- **Timeout**: 30 segundos

### Modal
- **Framework**: SweetAlert2
- **Font**: Titillium Web
- **Animações**: CSS smooth transitions
- **Responsivo**: 3 breakpoints (desktop/tablet/mobile)

## 📊 Resultados Esperados

### Sucesso
1. ✅ Formulário enviado com dados JSON coletados
2. ✅ Modal de progresso abre imediatamente
3. ✅ Barra de progresso atualiza de 0% a 100%
4. ✅ 15 fases mostram progresso visual em tempo real
5. ✅ Estimativa inicial aparece na Tela 4
6. ✅ Cálculo final aparece na Tela 15
7. ✅ Botão "Concluído" habilitado no final

### Fluxo de Dados
```
HTML Form → JavaScript → API Start → RPA Exec → Progress API → Modal Update
```

## 🚨 Tratamento de Erros

### Validação
- CPF deve ter 11 dígitos
- Email deve ser válido (se fornecido)
- Campos obrigatórios não podem estar vazios

### Rede
- Retry automático com backoff exponencial
- Timeout de 30 segundos
- Mensagens de erro amigáveis

### RPA
- Erro na execução: mostrar no modal
- Timeout: avisar sobre problema de conectividade
- Falha progressiva: botão de retry disponível

## 🎯 Critérios de Aprovação

### ✅ Objetivos Atendidos
- [ ] HTML de teste com formulário completo
- [ ] JavaScript integra modal de acompanhamento
- [ ] Chamadas RPA com JSON via linha de comando (não parametros.json)
- [ ] Script de progresso atualiza barra em tempo real
- [ ] Modal utiliza design do webdesigner
- [ ] Formulário pré-preenchido com dados do parametros.json

### ✅ Funcionalidades Implementadas
- [ ] Coleta automática de dados do formulário
- [ ] Validação em tempo real
- [ ] Comunicação com API RPA V4
- [ ] Modal responsivo com SweetAlert2
- [ ] Polling de progresso (2 segundos)
- [ ] Captura de estimativas (Telas 4 e 15)
- [ ] Tratamento de erros robusto
- [ ] Retry automático
- [ ] UI responsiva

## 📝 Logs de Debug
Abra o Console do navegador (F12) para acompanhar:
- `🚀 Inicializando Modal RPA Real...`
- `📋 Dados coletados:`
- `🆔 Session ID:`
- `📊 Verificando progresso da sessão:`
- `📊 Atualizando progresso:`
- `✅ Processamento concluído com sucesso`

## 🎉 Conclusão
Se todos os pontos de verificação passarem, o projeto está **PROJETO APROVADO** ✅

O sistema executa o RPA principal inteiro (15 telas) com modal de progresso em tempo real, capturando estimativas iniciais e cálculos finais, exatamente conforme especificado nos objetivos.
