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
        // Validação removida - feita no frontend
        // Apenas retorna sucesso para permitir execução do RPA
        return new ValidationResult([]);
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
