from model.profissional_saude import ProfissionalSaude
from model.validacoes import validar_numero, validar_texto


class Procedimento:
    def __init__(self, descricao: str, custo: float, profissional_responsavel: ProfissionalSaude):
        self.descricao = descricao
        self.custo = custo
        self.profissional_responsavel = profissional_responsavel

    @property
    def descricao(self) -> str:
        return self.__descricao

    @descricao.setter
    def descricao(self, descricao: str):
        self.__descricao = validar_texto(descricao, "Descrição do procedimento")

    @property
    def custo(self) -> float:
        return self.__custo

    @custo.setter
    def custo(self, custo: float):
        self.__custo = validar_numero(custo, "Custo do procedimento", permitir_zero=True)

    @property
    def profissional_responsavel(self) -> ProfissionalSaude:
        return self.__profissional_responsavel

    @profissional_responsavel.setter
    def profissional_responsavel(self, profissional: ProfissionalSaude):
        if not isinstance(profissional, ProfissionalSaude):
            raise TypeError("O responsável pelo procedimento deve ser um ProfissionalSaude.")
        self.__profissional_responsavel = profissional
