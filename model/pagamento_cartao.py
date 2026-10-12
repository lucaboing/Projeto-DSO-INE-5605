import re
from datetime import date

from model.pagamento import Pagamento
from model.validacoes import validar_texto


class PagamentoCartao(Pagamento):
    def __init__(self, data: date, valor_pago: float, numero_cartao: str, bandeira: str):
        super().__init__(data, valor_pago)
        self.numero_cartao = numero_cartao
        self.bandeira = bandeira

    @property
    def numero_cartao(self) -> str:
        return self.__numero_cartao

    @numero_cartao.setter
    def numero_cartao(self, numero_cartao: str):
        digitos = re.sub(r"[\s-]", "", validar_texto(numero_cartao, "Número do cartão"))
        if not digitos.isdigit() or not 13 <= len(digitos) <= 19:
            raise ValueError("Número do cartão inválido: deve conter de 13 a 19 dígitos.")
        self.__numero_cartao = digitos

    @property
    def bandeira(self) -> str:
        return self.__bandeira

    @bandeira.setter
    def bandeira(self, bandeira: str):
        self.__bandeira = validar_texto(bandeira, "Bandeira")
