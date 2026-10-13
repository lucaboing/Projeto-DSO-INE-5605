from abc import ABC, abstractmethod
from datetime import date

from model.validacoes import validar_data, validar_numero


class Pagamento(ABC):
    @abstractmethod
    def __init__(self, data: date, valor_pago: float):
        self.data = data
        self.valor_pago = valor_pago

    @property
    def data(self) -> date:
        return self.__data

    @data.setter
    def data(self, data: date):
        self.__data = validar_data(data, "Data do pagamento")

    @property
    def valor_pago(self) -> float:
        return self.__valor_pago

    @valor_pago.setter
    def valor_pago(self, valor_pago: float):
        self.__valor_pago = validar_numero(valor_pago, "Valor pago")
