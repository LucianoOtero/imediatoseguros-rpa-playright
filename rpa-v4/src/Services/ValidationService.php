<?php

namespace RPA\Services;

class ValidationService
{
    private array $rules;

    public function __construct(array $rules = [])
    {
        $this->rules = $rules;
    }

    public function validate(array $data): ValidationResult
    {
        $errors = [];

        // Validação robusta com dados reais obrigatórios
        $requiredFields = ['cpf', 'nome', 'placa', 'cep'];
        foreach ($requiredFields as $field) {
            if (empty($data[$field])) {
                $errors[] = "Campo '{$field}' é obrigatório";
            }
        }

        // Validação de CPF (11 dígitos + dígitos verificadores)
        if (!empty($data['cpf'])) {
            if (!$this->validateCPF($data['cpf'])) {
                $errors[] = "CPF inválido";
            }
        }

        // Validação de placa (formato brasileiro)
        if (!empty($data['placa'])) {
            if (!$this->validatePlaca($data['placa'])) {
                $errors[] = "Placa inválida (formato: ABC1234)";
            }
        }

        // Validação de CEP (8 dígitos)
        if (!empty($data['cep'])) {
            if (!$this->validateCEP($data['cep'])) {
                $errors[] = "CEP inválido (8 dígitos)";
            }
        }

        // Validação de email
        if (!empty($data['email'])) {
            if (!filter_var($data['email'], FILTER_VALIDATE_EMAIL)) {
                $errors[] = "Email inválido";
            }
        }

        // Validação de celular (11 dígitos)
        if (!empty($data['celular'])) {
            if (!$this->validateCelular($data['celular'])) {
                $errors[] = "Celular inválido (11 dígitos)";
            }
        }

        // Validação de ano do veículo
        if (!empty($data['ano'])) {
            if (!$this->validateAnoVeiculo($data['ano'])) {
                $errors[] = "Ano do veículo inválido";
            }
        }

        // Validações adicionais das regras configuradas
        foreach ($this->rules as $field => $rule) {
            $value = $data[$field] ?? null;
            $fieldErrors = $this->validateField($field, $value, $rule);
            $errors = array_merge($errors, $fieldErrors);
        }

        return new ValidationResult($errors);
    }

    /**
     * Valida CPF com dígitos verificadores
     */
    private function validateCPF(string $cpf): bool
    {
        // Remove caracteres não numéricos
        $cpf = preg_replace('/\D/', '', $cpf);
        
        // Verifica se tem 11 dígitos
        if (strlen($cpf) !== 11) {
            return false;
        }
        
        // Verifica se não são todos os dígitos iguais
        if (preg_match('/(\d)\1{10}/', $cpf)) {
            return false;
        }
        
        // Calcula o primeiro dígito verificador
        $sum = 0;
        for ($i = 0; $i < 9; $i++) {
            $sum += intval($cpf[$i]) * (10 - $i);
        }
        $remainder = $sum % 11;
        $digit1 = $remainder < 2 ? 0 : 11 - $remainder;
        
        // Verifica o primeiro dígito
        if (intval($cpf[9]) !== $digit1) {
            return false;
        }
        
        // Calcula o segundo dígito verificador
        $sum = 0;
        for ($i = 0; $i < 10; $i++) {
            $sum += intval($cpf[$i]) * (11 - $i);
        }
        $remainder = $sum % 11;
        $digit2 = $remainder < 2 ? 0 : 11 - $remainder;
        
        // Verifica o segundo dígito
        return intval($cpf[10]) === $digit2;
    }

    /**
     * Valida placa brasileira (formato: ABC1234)
     */
    private function validatePlaca(string $placa): bool
    {
        // Remove espaços e converte para maiúsculo
        $placa = strtoupper(trim($placa));
        
        // Verifica formato: 3 letras + 4 números
        return preg_match('/^[A-Z]{3}\d{4}$/', $placa);
    }

    /**
     * Valida CEP (8 dígitos)
     */
    private function validateCEP(string $cep): bool
    {
        // Remove caracteres não numéricos
        $cep = preg_replace('/\D/', '', $cep);
        
        // Verifica se tem 8 dígitos
        return strlen($cep) === 8;
    }

    /**
     * Valida celular (11 dígitos)
     */
    private function validateCelular(string $celular): bool
    {
        // Remove caracteres não numéricos
        $celular = preg_replace('/\D/', '', $celular);
        
        // Verifica se tem 11 dígitos
        return strlen($celular) === 11;
    }

    /**
     * Valida ano do veículo
     */
    private function validateAnoVeiculo(string $ano): bool
    {
        // Remove caracteres não numéricos
        $ano = preg_replace('/\D/', '', $ano);
        
        // Verifica se tem 4 dígitos
        if (strlen($ano) !== 4) {
            return false;
        }
        
        $anoInt = intval($ano);
        $anoAtual = date('Y');
        
        // Verifica se está entre 1900 e ano atual + 1
        return $anoInt >= 1900 && $anoInt <= ($anoAtual + 1);
    }

    private function validateField(string $field, $value, array $rule): array
    {
        $errors = [];

        // Required validation
        if (($rule['required'] ?? false) && empty($value)) {
            $errors[] = "Campo '{$field}' é obrigatório";
            return $errors;
        }

        // Skip other validations if field is empty and not required
        if (empty($value)) {
            return $errors;
        }

        // Pattern validation
        if (isset($rule['pattern']) && !preg_match($rule['pattern'], $value)) {
            $errors[] = "Campo '{$field}' não atende ao padrão esperado";
        }

        // Min length validation
        if (isset($rule['min_length']) && strlen($value) < $rule['min_length']) {
            $errors[] = "Campo '{$field}' deve ter pelo menos {$rule['min_length']} caracteres";
        }

        // Max length validation
        if (isset($rule['max_length']) && strlen($value) > $rule['max_length']) {
            $errors[] = "Campo '{$field}' deve ter no máximo {$rule['max_length']} caracteres";
        }

        // Custom validation
        if (isset($rule['custom']) && is_callable($rule['custom'])) {
            $customResult = $rule['custom']($value);
            if ($customResult !== true) {
                $errors[] = $customResult ?: "Campo '{$field}' é inválido";
            }
        }

        return $errors;
    }

    public function validateCPF(string $cpf): bool
    {
        // Remove caracteres não numéricos
        $cpf = preg_replace('/\D/', '', $cpf);

        // Verifica se tem 11 dígitos
        if (strlen($cpf) !== 11) {
            return false;
        }

        // Verifica se todos os dígitos são iguais
        if (preg_match('/(\d)\1{10}/', $cpf)) {
            return false;
        }

        // Validação do primeiro dígito verificador
        $sum = 0;
        for ($i = 0; $i < 9; $i++) {
            $sum += intval($cpf[$i]) * (10 - $i);
        }
        $remainder = $sum % 11;
        $digit1 = $remainder < 2 ? 0 : 11 - $remainder;

        if (intval($cpf[9]) !== $digit1) {
            return false;
        }

        // Validação do segundo dígito verificador
        $sum = 0;
        for ($i = 0; $i < 10; $i++) {
            $sum += intval($cpf[$i]) * (11 - $i);
        }
        $remainder = $sum % 11;
        $digit2 = $remainder < 2 ? 0 : 11 - $remainder;

        return intval($cpf[10]) === $digit2;
    }
}

class ValidationResult
{
    private array $errors;

    public function __construct(array $errors = [])
    {
        $this->errors = $errors;
    }

    public function isValid(): bool
    {
        return empty($this->errors);
    }

    public function getErrors(): array
    {
        return $this->errors;
    }

    public function getFirstError(): ?string
    {
        return $this->errors[0] ?? null;
    }

    public function hasErrors(): bool
    {
        return !$this->isValid();
    }
}
