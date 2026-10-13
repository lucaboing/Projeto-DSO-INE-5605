from view.tela_abstrata import TelaAbstrata


class TelaPrincipal(TelaAbstrata):
    def tela_opcoes(self) -> int:
        return self._le_opcao("SISTEMA DE CLÍNICAS", {
            1: "Pacientes",
            2: "Profissionais de saúde",
            3: "Clínicas",
            4: "Tipos de atendimento",
            5: "Atendimentos, procedimentos e pagamentos",
            6: "Relatórios",
            0: "Sair",
        })
