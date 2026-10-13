from datetime import date

from model.pagamento import Pagamento
from model.validacoes import validar_cpf


class PagamentoPix(Pagamento):
    def __init__(self, data: date, valor_pago: float, cpf_pagador: str):
        super().__init__(data, valor_pago)
        self.cpf_pagador = cpf_pagador

    @property
    def cpf_pagador(self) -> str:
        return self.__cpf_pagador

    @cpf_pagador.setter
    def cpf_pagador(self, cpf_pagador: str):
        self.__cpf_pagador = validar_cpf(cpf_pagador, "CPF do pagador")
