from datetime import time

from exception.objeto_nao_encontrado_exception import ObjetoNaoEncontradoException
from model.profissional_saude import ProfissionalSaude
from model.validacoes import validar_horario, validar_texto


class Clinica:
    def __init__(self, nome: str, cidade: str, descricao: str, abertura: time, fechamento: time):
        self.nome = nome
        self.cidade = cidade
        self.descricao = descricao
        self.alterar_horario_funcionamento(abertura, fechamento)
        self.__profissionais: list[ProfissionalSaude] = []

    @property
    def nome(self) -> str:
        return self.__nome

    @nome.setter
    def nome(self, nome: str):
        self.__nome = validar_texto(nome, "Nome da clínica")

    @property
    def cidade(self) -> str:
        return self.__cidade

    @cidade.setter
    def cidade(self, cidade: str):
        self.__cidade = validar_texto(cidade, "Cidade")

    @property
    def descricao(self) -> str:
        return self.__descricao

    @descricao.setter
    def descricao(self, descricao: str):
        self.__descricao = validar_texto(descricao, "Descrição da clínica")

    @property
    def horario_abertura(self) -> time:
        return self.__horario_abertura

    @property
    def horario_fechamento(self) -> time:
        return self.__horario_fechamento

    def alterar_horario_funcionamento(self, abertura: time, fechamento: time):
        """Altera abertura e fechamento juntos, para validar o par de uma só vez."""
        abertura = validar_horario(abertura, "Horário de abertura")
        fechamento = validar_horario(fechamento, "Horário de fechamento")
        if abertura >= fechamento:
            raise ValueError("O horário de abertura deve ser anterior ao de fechamento.")
        self.__horario_abertura = abertura
        self.__horario_fechamento = fechamento

    def adicionar_profissional(self, profissional: ProfissionalSaude):
        if not isinstance(profissional, ProfissionalSaude):
            raise TypeError("Só é possível adicionar objetos do tipo ProfissionalSaude.")
        if any(p.registro == profissional.registro for p in self.__profissionais):
            raise ValueError(
                f"Já existe um profissional com o registro {profissional.registro} nesta clínica."
            )
        self.__profissionais.append(profissional)

    def remover_profissional(self, registro: str):
        for profissional in self.__profissionais:
            if profissional.registro == registro:
                self.__profissionais.remove(profissional)
                return
        raise ObjetoNaoEncontradoException(
            f"Profissional com registro {registro} não encontrado na clínica {self.nome}."
        )

    def listar_profissionais(self) -> list[ProfissionalSaude]:
        return list(self.__profissionais)
