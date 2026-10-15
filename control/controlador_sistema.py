import sys

from control.controlador_atendimento import ControladorAtendimento
from control.controlador_clinica import ControladorClinica
from control.controlador_paciente import ControladorPaciente
from control.controlador_profissional import ControladorProfissional
from control.controlador_relatorios import ControladorRelatorios
from control.controlador_tipo_atendimento import ControladorTipoAtendimento
from view.tela_principal import TelaPrincipal


class ControladorSistema:
    def __init__(self):
        self.__tela_principal = TelaPrincipal()
        self.__controlador_paciente = ControladorPaciente(self)
        self.__controlador_profissional = ControladorProfissional(self)
        self.__controlador_clinica = ControladorClinica(self)
        self.__controlador_tipo_atendimento = ControladorTipoAtendimento(self)
        self.__controlador_atendimento = ControladorAtendimento(self)
        self.__controlador_relatorios = ControladorRelatorios(self)

    @property
    def controlador_paciente(self) -> ControladorPaciente:
        return self.__controlador_paciente

    @property
    def controlador_profissional(self) -> ControladorProfissional:
        return self.__controlador_profissional

    @property
    def controlador_clinica(self) -> ControladorClinica:
        return self.__controlador_clinica

    @property
    def controlador_tipo_atendimento(self) -> ControladorTipoAtendimento:
        return self.__controlador_tipo_atendimento

    @property
    def controlador_atendimento(self) -> ControladorAtendimento:
        return self.__controlador_atendimento

    @property
    def controlador_relatorios(self) -> ControladorRelatorios:
        return self.__controlador_relatorios

    def inicializa_sistema(self):
        opcoes = {
            1: self.abre_cadastros,
            2: self.abre_registros,
            3: self.__controlador_relatorios.abre_tela,
            0: self.encerra_sistema,
        }
        while True:
            opcoes[self.__tela_principal.tela_opcoes()]()

    def abre_cadastros(self):
        opcoes = {
            1: self.__controlador_paciente.abre_tela,
            2: self.__controlador_profissional.abre_tela,
            3: self.__controlador_clinica.abre_tela,
            4: self.__controlador_tipo_atendimento.abre_tela,
        }
        while True:
            opcao = self.__tela_principal.tela_opcoes_cadastros()
            if opcao == 0:
                return
            opcoes[opcao]()

    def abre_registros(self):
        opcoes = {
            1: self.__controlador_atendimento.abre_tela,
            2: self.__controlador_atendimento.abre_tela_procedimentos,
            3: self.__controlador_atendimento.abre_tela_pagamentos,
        }
        while True:
            opcao = self.__tela_principal.tela_opcoes_registros()
            if opcao == 0:
                return
            opcoes[opcao]()

    def encerra_sistema(self):
        self.__tela_principal.mostra_mensagem("Encerrando o sistema...")
        sys.exit(0)
