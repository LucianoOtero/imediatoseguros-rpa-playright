#!/usr/bin/env python3
"""
Validação de parâmetros
"""

import re
from datetime import datetime

def validar_placa(placa):
    """Valida formato da placa"""
    if not placa:
        return False, "Placa não pode estar vazia"
    
    # Formato Mercosul (ABC1D23)
    if re.match(r"^[A-Z]{3}[0-9]{1}[A-Z]{1}[0-9]{2}$", placa):
        return True, "Placa Mercosul válida"
    
    # Formato antigo (ABC1234)
    if re.match(r"^[A-Z]{3}[0-9]{4}$", placa):
        return True, "Placa antiga válida"
    
    return False, "Formato de placa inválido"

def validar_cpf(cpf):
    """Valida CPF"""
    if not cpf:
        return False, "CPF não pode estar vazio"
    
    # Remover caracteres especiais
    cpf_limpo = re.sub(r"[^0-9]", "", cpf)
    
    if len(cpf_limpo) != 11:
        return False, "CPF deve ter 11 dígitos"
    
    # Verificar se todos os dígitos são iguais
    if cpf_limpo == cpf_limpo[0] * 11:
        return False, "CPF inválido"
    
    # Validar dígitos verificadores
    soma = 0
    for i in range(9):
        soma += int(cpf_limpo[i]) * (10 - i)
    
    resto = soma % 11
    if resto < 2:
        digito1 = 0
    else:
        digito1 = 11 - resto
    
    soma = 0
    for i in range(10):
        soma += int(cpf_limpo[i]) * (11 - i)
    
    resto = soma % 11
    if resto < 2:
        digito2 = 0
    else:
        digito2 = 11 - resto
    
    if int(cpf_limpo[9]) == digito1 and int(cpf_limpo[10]) == digito2:
        return True, "CPF válido"
    
    return False, "CPF inválido"

def validar_email(email):
    """Valida email"""
    if not email:
        return False, "Email não pode estar vazio"
    
    padrao = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    
    if re.match(padrao, email):
        return True, "Email válido"
    
    return False, "Email inválido"

def validar_telefone(telefone):
    """Valida telefone"""
    if not telefone:
        return False, "Telefone não pode estar vazio"
    
    # Remover caracteres especiais
    telefone_limpo = re.sub(r"[^0-9]", "", telefone)
    
    # Verificar se tem 10 ou 11 dígitos
    if len(telefone_limpo) not in [10, 11]:
        return False, "Telefone deve ter 10 ou 11 dígitos"
    
    return True, "Telefone válido"

def validar_data_nascimento(data):
    """Valida data de nascimento"""
    if not data:
        return False, "Data de nascimento não pode estar vazia"
    
    try:
        data_obj = datetime.strptime(data, "%d/%m/%Y")
        
        # Verificar se não é no futuro
        if data_obj > datetime.now():
            return False, "Data de nascimento não pode ser no futuro"
        
        # Verificar se não é muito antiga (mais de 120 anos)
        if data_obj.year < datetime.now().year - 120:
            return False, "Data de nascimento muito antiga"
        
        return True, "Data de nascimento válida"
        
    except ValueError:
        return False, "Formato de data inválido (use DD/MM/AAAA)"

def validar_cep(cep):
    """Valida CEP"""
    if not cep:
        return False, "CEP não pode estar vazio"
    
    # Remover caracteres especiais
    cep_limpo = re.sub(r"[^0-9]", "", cep)
    
    if len(cep_limpo) != 8:
        return False, "CEP deve ter 8 dígitos"
    
    return True, "CEP válido"

def validar_todos_parametros(parametros):
    """Valida todos os parâmetros"""
    erros = []
    
    # Validar placa
    valido, mensagem = validar_placa(parametros.get("placa"))
    if not valido:
        erros.append(f"Placa: {mensagem}")
    
    # Validar CPF
    valido, mensagem = validar_cpf(parametros.get("cpf"))
    if not valido:
        erros.append(f"CPF: {mensagem}")
    
    # Validar email
    valido, mensagem = validar_email(parametros.get("email"))
    if not valido:
        erros.append(f"Email: {mensagem}")
    
    # Validar telefone
    valido, mensagem = validar_telefone(parametros.get("celular"))
    if not valido:
        erros.append(f"Telefone: {mensagem}")
    
    # Validar data de nascimento
    valido, mensagem = validar_data_nascimento(parametros.get("data_nascimento"))
    if not valido:
        erros.append(f"Data de nascimento: {mensagem}")
    
    # Validar CEP
    valido, mensagem = validar_cep(parametros.get("cep"))
    if not valido:
        erros.append(f"CEP: {mensagem}")
    
    if erros:
        return False, erros
    
    return True, "Todos os parâmetros são válidos"
