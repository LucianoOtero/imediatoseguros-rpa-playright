#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Debug específico para verificar o campo estado civil na API PH3A
"""

import requests
import json

# Configurações da API PH3A
PH3A_BASE_URL = "https://api.ph3a.com.br/DataBusca"
PH3A_USERNAME = "alex.kaminski@imediatoseguros.com.br"
PH3A_PASSWORD = "ImdSeg2025$$"

def debug_estado_civil():
    """Debug específico do estado civil"""
    print("🔍 Debug Estado Civil - API PH3A")
    print("=" * 50)
    
    # Login
    login_data = {
        "UserName": PH3A_USERNAME,
        "Password": PH3A_PASSWORD
    }
    
    response = requests.post(
        f"{PH3A_BASE_URL}/api/Account/Login",
        json=login_data,
        headers={"Content-Type": "application/json"},
        timeout=30
    )
    
    if response.status_code != 200:
        print("❌ Erro no login")
        return
    
    result = response.json()
    token = result["data"]["Token"]
    print("✅ Login realizado")
    
    # Consultar CPF
    cpf = "97137189768"  # ALEX KAMINSKI
    
    consulta_data = {
        "Document": cpf,
        "Type": 0,
        "HashType": 0
    }
    
    response = requests.post(
        f"{PH3A_BASE_URL}/data",
        json=consulta_data,
        headers={
            "Content-Type": "application/json",
            "Token": token
        },
        timeout=30
    )
    
    if response.status_code == 200:
        resultado = response.json()
        data = resultado.get("Data", {})
        person = data.get("Person", {})
        
        print(f"\n📊 Dados completos da API para CPF: {cpf}")
        print("=" * 50)
        
        # Dados principais
        print(f"Nome: {data.get('NameBrasil', 'N/A')}")
        print(f"Sexo: {data.get('Gender', 'N/A')}")
        print(f"Data Nascimento: {data.get('BirthDate', 'N/A')}")
        print(f"Idade: {data.get('Age', 'N/A')}")
        
        # Dados da pessoa (Person)
        print(f"\n👤 Dados Person:")
        print(f"   Dependents: {person.get('Dependents', 'N/A')}")
        print(f"   Nationality: {person.get('Nationality', 'N/A')}")
        print(f"   MaritalStatus: {person.get('MaritalStatus', 'N/A')}")
        print(f"   EducationLevel: {person.get('EducationLevel', 'N/A')}")
        print(f"   MotherName: {person.get('MotherName', 'N/A')}")
        print(f"   FatherName: {person.get('FatherName', 'N/A')}")
        
        # Mapear estado civil
        estado_civil_map = {
            0: "Solteiro",
            1: "Casado", 
            2: "Divorciado",
            3: "Viúvo"
        }
        
        marital_status = person.get("MaritalStatus", 0)
        estado_civil = estado_civil_map.get(marital_status, "Não informado")
        
        print(f"\n💍 Estado Civil:")
        print(f"   Código: {marital_status}")
        print(f"   Descrição: {estado_civil}")
        
        # Verificar se há outros campos relacionados
        print(f"\n🔍 Outros campos que podem indicar estado civil:")
        for key, value in person.items():
            if any(word in key.lower() for word in ['marital', 'civil', 'spouse', 'conjuge', 'casado']):
                print(f"   {key}: {value}")
        
        # Salvar dados completos para análise
        with open("debug_estado_civil_completo.json", "w", encoding="utf-8") as f:
            json.dump(resultado, f, ensure_ascii=False, indent=2)
        print(f"\n💾 Dados completos salvos em: debug_estado_civil_completo.json")
        
    else:
        print(f"❌ Erro na consulta: {response.status_code}")
        print(f"Response: {response.text}")

if __name__ == "__main__":
    debug_estado_civil()
























