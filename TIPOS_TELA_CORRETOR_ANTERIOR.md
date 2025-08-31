# TELA DE CONFIRMAÇÃO DO CORRETOR ATUAL

## Descrição
Tela condicional que aparece quando já existe um corretor associado à placa/usuário no sistema. Permite ao usuário escolher se quer continuar com o corretor anterior ou selecionar um novo corretor.

## Parâmetro
- **`continuar_com_corretor_anterior`**: Controla a seleção na tela

## Tipos Aceitos

### continuar_com_corretor_anterior
- **Tipo**: `boolean`
- **Valores aceitos**: `true` ou `false`
- **Padrão**: `true`
- **Descrição**: 
  - `true`: Seleciona "Sim, continuar com meu corretor"
  - `false`: Seleciona "Não, quero outro corretor"

## Comportamento da Tela

### Quando aparece
- Após a Tela 13 (Uso por Residentes)
- Antes da Tela 14 (Cálculo automático)
- Apenas quando há um corretor anterior associado

### Opções disponíveis
1. **"Sim, continuar com meu corretor"**
   - Mantém o corretor atual
   - Selecionado quando `continuar_com_corretor_anterior = true`

2. **"Não, quero outro corretor"**
   - Permite selecionar um novo corretor
   - Selecionado quando `continuar_com_corretor_anterior = false`

### Elementos da tela
- **ID principal**: `corretorAnteriorTelaCorretorAnterior`
- **Botão Continuar**: `gtm-telaCorretorAnteriorContinuar`
- **Opção 1**: `.cursor-pointer:nth-child(1) > .border .font-workSans`
- **Opção 2**: `.cursor-pointer:nth-child(2) > .border .font-workSans`

## Exemplo de uso

```json
{
  "continuar_com_corretor_anterior": true
}
```

## Implementação
- **Função**: `implementar_tela_corretor_anterior()`
- **Estratégia**: Verificação condicional + seleção robusta
- **Fallbacks**: CSS direto → JavaScript → Texto
- **Logging**: Detalhado para debug

## Observações
- Tela **condicional** - pode não aparecer
- Não há campos adicionais baseados na seleção
- Navegação direta para próxima tela após seleção
