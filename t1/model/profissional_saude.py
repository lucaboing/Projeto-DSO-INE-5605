from model.pessoa import Pessoa
from model.validacoes import validar_texto


class ProfissionalSaude(Pessoa):
    def __init__(self, nome: str, cpf: str, celular: str, especialidade: str, registro: str):
        super().__init__(nome, cpf, celular)
        self.especialidade = especialidade
        self.__registro = validar_texto(registro, "Registro profissional")

    @property
    def especialidade(self) -> str:
        return self.__especialidade

    @especialidade.setter
    def especialidade(self, especialidade: str):
        self.__especialidade = validar_texto(especialidade, "Especialidade")

    @property
    def registro(self) -> str:
        return self.__registro
