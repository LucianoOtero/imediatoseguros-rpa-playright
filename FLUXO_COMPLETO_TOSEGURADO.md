# �� FLUXO COMPLETO - TÔ SEGURADO - COTAÇÃO DE SEGURO AUTO

## 📍 **PROBLEMA IDENTIFICADO:**
O RPA está tentando acessar **DIRETAMENTE** uma tela avançada, mas precisa navegar por **15 telas** sequencialmente.

## �� **FLUXO COMPLETO (15 TELAS):**

### **Tela 1: Seleção do Tipo de Seguro**
- **Ação:** Clicar no botão "Carro"
- **Elemento:** Botão com texto "Carro" e ícone de carro

### **Tela 2: Formulário de Placa**
- **Ação:** Preencher placa "EED3D56" e clicar "Continuar"
- **Elemento:** Campo "Placa *" com placeholder "ABC-1D34"

### **Tela 3: Confirmação do Veículo**
- **Ação:** Selecionar "Sim" e clicar "Continuar"
- **Elemento:** Radio button "Sim" para confirmar veículo COROLLA XEI 1.8/1.8 FLEX 16V MEC. 2009/2009

### **Tela 4: Veículo Já Segurado**
- **Ação:** Selecionar "Não" e clicar "Continuar"
- **Elemento:** Radio button "Não" para seguro vigente

### **Tela 5: Carrossel de Coberturas**
- **Ação:** Clicar "Continuar" (não nos interessa)
- **Elemento:** Botão "Continuar" após carrossel de 3 coberturas

### **Tela 6: Questionário do Veículo**
- **Ação:** Selecionar "Flex" + deixar checkboxes vazios + "Continuar"
- **Elementos:** 
  - Radio button "Flex" para combustível
  - Checkboxes vazios: Kit Gás, Blindado, Financiado

### **Tela 7: Endereço Noturno**
- **Ação:** Digitar CEP + selecionar endereço no balão + "Continuar"
- **Elementos:** Campo "Endereço*" + balão de sugestões

### **Tela 8: Uso do Veículo**
- **Ação:** Selecionar "Pessoal" e clicar "Continuar"
- **Elemento:** Radio button "Pessoal"

### **Tela 9: Dados Pessoais**
- **Ação:** Preencher todos os campos e clicar "Continuar"
- **Elementos:**
  - Nome: LUCIANO OTERO
  - CPF: 085.546.078-48
  - Data: 09/02/1965
  - Sexo: Masculino
  - Estado Civil: Casado
  - Email: lrotero@gmail.com
  - Celular: (11) 97668-7668

### **Tela 10: Condutor Principal**
- **Ação:** Selecionar "Sim" e clicar "Continuar"
- **Elemento:** Radio button "Sim" para condutor principal

### **Tela 11: Local Trabalho/Estudo**
- **Ação:** Selecionar "Local de trabalho" e clicar "Continuar"
- **Elemento:** Checkbox "Local de trabalho"

### **Tela 12: Garagem e Portão**
- **Ação:** Selecionar "Sim" + "Eletrônico" e clicar "Continuar"
- **Elementos:** 
  - Radio button "Sim" para garagem
  - Radio button "Eletrônico" para tipo de portão

### **Tela 13: Reside com 18-26 anos**
- **Ação:** Selecionar "Não" e clicar "Continuar"
- **Elemento:** Radio button "Não"

### **Tela 14: Tela de Carregamento**
- **Ação:** Aguardar cálculo automático (02:09)
- **Elemento:** Timer automático com mensagem "Por favor, aguarde. Estamos realizando o cálculo para você!"

### **Tela 15: Resultado Final**
- **Ação:** Extrair dados das cotações + Clicar "Agora não"
- **Elementos:** 
  - 2 planos de cotação com valores
  - Botão "Agora não" para finalizar

## 🎯 **DADOS A EXTRAIR (Tela 15):**
- **Plano 1:** R$ 2.731,56 anual
- **Plano 2:** R$ 2.891,74 anual
- **Coberturas:** Franquia, Valor de Mercado, Assistência, Vidros, Carro Reserva, Danos Materiais, Danos Corporais, Danos Morais, Morte/Invalidez

## 🚀 **PRÓXIMO PASSO:**
Corrigir o RPA para navegar por todas as 15 telas sequencialmente.

---
**Data:** $(date)
**Status:** Documentado e pronto para implementação
