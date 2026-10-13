from model.pessoa import Pessoa
from model.validacoes import validar_inteiro


class Paciente(Pessoa):
    def __init__(self, nome: str, cpf: str, celular: str, idade: int):
        super().__init__(nome, cpf, celular)
        self.idade = idade

    @property
    def idade(self) -> int:
        return self.__idade

    @idade.setter
    def idade(self, idade: int):
        idade = validar_inteiro(idade, "Idade")
        if idade < 0 or idade > 130:
            raise ValueError("Idade inválida: informe um valor entre 0 e 130.")
        self.__idade = idade
