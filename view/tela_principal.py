from view.tela_abstrata import TelaAbstrata


class TelaPrincipal(TelaAbstrata):
    def tela_opcoes(self) -> int:
        return self._le_opcao("SISTEMA DE CLÍNICAS", {
            1: "Cadastros",
            2: "Registros",
            3: "Relatórios",
            0: "Sair",
        })

    def tela_opcoes_cadastros(self) -> int:
        return self._le_opcao("CADASTROS", {
            1: "Pacientes",
            2: "Profissionais de saúde",
            3: "Clínicas",
            4: "Tipos de atendimento",
            0: "Voltar",
        })

    def tela_opcoes_registros(self) -> int:
        return self._le_opcao("REGISTROS", {
            1: "Atendimentos",
            2: "Procedimentos",
            3: "Pagamentos",
            0: "Voltar",
        })
