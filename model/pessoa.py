from abc import ABC, abstractmethod

from model.validacoes import validar_celular, validar_cpf, validar_texto


class Pessoa(ABC):
    @abstractmethod
    def __init__(self, nome: str, cpf: str, celular: str):
        self.nome = nome
        self.cpf = cpf
        self.celular = celular

    @property
    def nome(self) -> str:
        return self.__nome

    @nome.setter
    def nome(self, nome: str):
        self.__nome = validar_texto(nome, "Nome")

    @property
    def cpf(self) -> str:
        return self.__cpf

    @cpf.setter
    def cpf(self, cpf: str):
        self.__cpf = validar_cpf(cpf)

    @property
    def celular(self) -> str:
        return self.__celular

    @celular.setter
    def celular(self, celular: str):
        self.__celular = validar_celular(celular)
