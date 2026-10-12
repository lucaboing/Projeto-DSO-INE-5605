import re
from datetime import date, datetime, time


def validar_texto(valor, campo: str) -> str:
    if not isinstance(valor, str):
        raise TypeError(f"{campo} deve ser um texto.")
    valor = valor.strip()
    if not valor:
        raise ValueError(f"{campo} não pode ser vazio.")
    return valor


def validar_cpf(valor, campo: str = "CPF") -> str:
    """Retorna o CPF somente com dígitos (11 dígitos, não todos iguais)."""
    digitos = re.sub(r"\D", "", validar_texto(valor, campo))
    if len(digitos) != 11 or digitos == digitos[0] * 11:
        raise ValueError(f"{campo} inválido: deve conter 11 dígitos.")
    return digitos


def validar_celular(valor, campo: str = "Celular") -> str:
    """Retorna o celular somente com dígitos (DDD + número: 10 ou 11 dígitos)."""
    digitos = re.sub(r"\D", "", validar_texto(valor, campo))
    if len(digitos) not in (10, 11):
        raise ValueError(f"{campo} inválido: informe DDD + número (10 ou 11 dígitos).")
    return digitos


def validar_numero(valor, campo: str, permitir_zero: bool = False) -> float:
    if isinstance(valor, bool) or not isinstance(valor, (int, float)):
        raise TypeError(f"{campo} deve ser um número.")
    if valor < 0 or (valor == 0 and not permitir_zero):
        raise ValueError(
            f"{campo} deve ser {'maior ou igual a' if permitir_zero else 'maior que'} zero."
        )
    return float(valor)


def validar_inteiro(valor, campo: str) -> int:
    if isinstance(valor, bool) or not isinstance(valor, int):
        raise TypeError(f"{campo} deve ser um número inteiro.")
    return valor


def validar_data(valor, campo: str = "Data") -> date:
    if isinstance(valor, datetime) or not isinstance(valor, date):
        raise TypeError(f"{campo} deve ser um objeto datetime.date.")
    return valor


def validar_horario(valor, campo: str = "Horário") -> time:
    if not isinstance(valor, time):
        raise TypeError(f"{campo} deve ser um objeto datetime.time.")
    return valor
