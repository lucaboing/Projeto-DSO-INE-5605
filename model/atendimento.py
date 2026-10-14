from datetime import date, time

from exception.horario_fora_expediente_exception import HorarioForaExpedienteException
from exception.objeto_nao_encontrado_exception import ObjetoNaoEncontradoException
from exception.pagamento_atrasado_exception import PagamentoAtrasadoException
from exception.paciente_menor_idade_exception import PacienteMenorIdadeException
from model.clinica import Clinica
from model.paciente import Paciente
from model.pagamento import Pagamento
from model.procedimento import Procedimento
from model.profissional_saude import ProfissionalSaude
from model.tipo_atendimento import TipoAtendimento
from model.validacoes import validar_data, validar_horario, validar_inteiro, validar_numero


class Atendimento:
    IDADE_MINIMA = 18

    def __init__(self, codigo: int, data: date, horario_inicio: time, horario_fim: time,
                 tipo: TipoAtendimento, valor_base: float, paciente: Paciente,
                 profissional: ProfissionalSaude, clinica: Clinica):
        self.__codigo = validar_inteiro(codigo, "Código do atendimento")
        self.__data = validar_data(data, "Data do atendimento")
        self.__tipo = self.__validar_tipo(tipo)
        self.__valor_base = validar_numero(valor_base, "Valor base", permitir_zero=True)
        self.__paciente = self.__validar_paciente(paciente)
        self.__profissional = self.__validar_profissional(profissional)
        self.__clinica = self.__validar_clinica(clinica)
        self.__validar_horario(horario_inicio, horario_fim, self.__clinica)
        self.__horario_inicio = horario_inicio
        self.__horario_fim = horario_fim
        self.__procedimentos: list[Procedimento] = []
        self.__pagamentos: list[Pagamento] = []

    # ---------- validações internas ----------
    def __validar_horario(self, inicio: time, fim: time, clinica: Clinica):
        validar_horario(inicio, "Horário de início")
        validar_horario(fim, "Horário de fim")
        if inicio >= fim:
            raise ValueError("O horário de início deve ser anterior ao horário de fim.")
        if inicio < clinica.horario_abertura or fim > clinica.horario_fechamento:
            raise HorarioForaExpedienteException(
                f"O atendimento ({inicio:%H:%M} às {fim:%H:%M}) está fora do funcionamento "
                f"da clínica ({clinica.horario_abertura:%H:%M} às {clinica.horario_fechamento:%H:%M})."
            )

    def __validar_tipo(self, tipo: TipoAtendimento) -> TipoAtendimento:
        if not isinstance(tipo, TipoAtendimento):
            raise TypeError("O tipo deve ser um TipoAtendimento.")
        return tipo

    def __validar_paciente(self, paciente: Paciente) -> Paciente:
        if not isinstance(paciente, Paciente):
            raise TypeError("O paciente deve ser um objeto Paciente.")
        if paciente.idade < self.IDADE_MINIMA:
            raise PacienteMenorIdadeException(
                f"O paciente {paciente.nome} tem {paciente.idade} anos. É necessário ter "
                f"{self.IDADE_MINIMA} anos completos para realizar atendimento de forma independente."
            )
        return paciente

    def __validar_profissional(self, profissional: ProfissionalSaude) -> ProfissionalSaude:
        if not isinstance(profissional, ProfissionalSaude):
            raise TypeError("O profissional deve ser um objeto ProfissionalSaude.")
        return profissional

    def __validar_clinica(self, clinica: Clinica) -> Clinica:
        if not isinstance(clinica, Clinica):
            raise TypeError("A clínica deve ser um objeto Clinica.")
        return clinica

    # ---------- propriedades ----------
    @property
    def codigo(self) -> int:
        return self.__codigo

    @property
    def data(self) -> date:
        return self.__data

    @data.setter
    def data(self, data: date):
        self.__data = validar_data(data, "Data do atendimento")

    @property
    def horario_inicio(self) -> time:
        return self.__horario_inicio

    @horario_inicio.setter
    def horario_inicio(self, horario_inicio: time):
        self.__validar_horario(horario_inicio, self.__horario_fim, self.__clinica)
        self.__horario_inicio = horario_inicio

    @property
    def horario_fim(self) -> time:
        return self.__horario_fim

    @horario_fim.setter
    def horario_fim(self, horario_fim: time):
        self.__validar_horario(self.__horario_inicio, horario_fim, self.__clinica)
        self.__horario_fim = horario_fim

    def alterar_horario(self, horario_inicio: time, horario_fim: time):
        """Altera início e fim juntos, validando o par de uma só vez."""
        self.__validar_horario(horario_inicio, horario_fim, self.__clinica)
        self.__horario_inicio = horario_inicio
        self.__horario_fim = horario_fim

    @property
    def tipo(self) -> TipoAtendimento:
        return self.__tipo

    @tipo.setter
    def tipo(self, tipo: TipoAtendimento):
        self.__tipo = self.__validar_tipo(tipo)

    @property
    def valor_base(self) -> float:
        return self.__valor_base

    @valor_base.setter
    def valor_base(self, valor_base: float):
        self.__valor_base = validar_numero(valor_base, "Valor base", permitir_zero=True)

    @property
    def paciente(self) -> Paciente:
        return self.__paciente

    @paciente.setter
    def paciente(self, paciente: Paciente):
        self.__paciente = self.__validar_paciente(paciente)

    @property
    def profissional(self) -> ProfissionalSaude:
        return self.__profissional

    @profissional.setter
    def profissional(self, profissional: ProfissionalSaude):
        self.__profissional = self.__validar_profissional(profissional)

    @property
    def clinica(self) -> Clinica:
        return self.__clinica

    @clinica.setter
    def clinica(self, clinica: Clinica):
        clinica = self.__validar_clinica(clinica)
        self.__validar_horario(self.__horario_inicio, self.__horario_fim, clinica)
        self.__clinica = clinica

    @property
    def procedimentos(self) -> list[Procedimento]:
        return list(self.__procedimentos)

    @property
    def pagamentos(self) -> list[Pagamento]:
        return list(self.__pagamentos)

    # ---------- procedimentos (composição) ----------
    def adicionar_procedimento(self, procedimento: Procedimento):
        if not isinstance(procedimento, Procedimento):
            raise TypeError("Só é possível adicionar objetos do tipo Procedimento.")
        self.__procedimentos.append(procedimento)

    def remover_procedimento(self, descricao: str):
        """Remove o primeiro procedimento com a descrição informada."""
        alvo = str(descricao).strip().lower()
        for procedimento in self.__procedimentos:
            if procedimento.descricao.lower() == alvo:
                self.__procedimentos.remove(procedimento)
                return
        raise ObjetoNaoEncontradoException(
            f"Procedimento '{descricao}' não encontrado no atendimento {self.__codigo}."
        )

    # ---------- pagamentos (composição) ----------
    def registrar_pagamento(self, pagamento: Pagamento):
        if not isinstance(pagamento, Pagamento):
            raise TypeError("Só é possível registrar objetos do tipo Pagamento.")
        if pagamento.data > self.__data:
            raise PagamentoAtrasadoException(
                f"O pagamento ({pagamento.data:%d/%m/%Y}) deve ser realizado até a data "
                f"do atendimento ({self.__data:%d/%m/%Y})."
            )
        saldo = self.calcular_saldo_devedor()
        if round(pagamento.valor_pago, 2) > saldo:
            raise ValueError(
                f"O valor pago (R$ {pagamento.valor_pago:.2f}) excede o saldo devedor "
                f"(R$ {saldo:.2f})."
            )
        self.__pagamentos.append(pagamento)

    def remover_pagamento(self, pagamento: Pagamento):
        if pagamento not in self.__pagamentos:
            raise ObjetoNaoEncontradoException(
                f"Pagamento não encontrado no atendimento {self.__codigo}."
            )
        self.__pagamentos.remove(pagamento)

    # ---------- cálculos ----------
    def calcular_valor_total(self) -> float:
        total = self.__valor_base + sum(p.custo for p in self.__procedimentos)
        return round(total, 2)

    def calcular_saldo_devedor(self) -> float:
        pago = sum(p.valor_pago for p in self.__pagamentos)
        return round(self.calcular_valor_total() - pago, 2)
