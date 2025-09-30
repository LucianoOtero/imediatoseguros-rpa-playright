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

        foreach ($this->rules as $field => $rule) {
            $value = $data[$field] ?? null;
            $fieldErrors = $this->validateField($field, $value, $rule);
            $errors = array_merge($errors, $fieldErrors);
        }

        return new ValidationResult($errors);
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
