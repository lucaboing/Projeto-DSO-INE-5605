from model.validacoes import validar_inteiro, validar_texto


class TipoAtendimento:
    def __init__(self, codigo: int, tipo_atendimento: str):
        self.codigo = codigo
        self.tipo_atendimento = tipo_atendimento

    @property
    def codigo(self) -> int:
        return self.__codigo

    @codigo.setter
    def codigo(self, codigo: int):
        self.__codigo = validar_inteiro(codigo, "Código do tipo de atendimento")

    @property
    def tipo_atendimento(self) -> str:
        return self.__tipo_atendimento

    @tipo_atendimento.setter
    def tipo_atendimento(self, tipo_atendimento: str):
        self.__tipo_atendimento = validar_texto(tipo_atendimento, "Tipo de atendimento")
