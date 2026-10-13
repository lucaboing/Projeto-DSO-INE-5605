from view.tela_abstrata import TelaAbstrata


class TelaPaciente(TelaAbstrata):
    def tela_opcoes(self) -> int:
        return self._le_opcao("PACIENTES", {
            1: "Incluir paciente",
            2: "Alterar paciente",
            3: "Excluir paciente",
            4: "Listar pacientes",
            0: "Retornar",
        })

    def pega_dados_paciente(self, editar: bool = False) -> dict:
        """Na alteração o CPF (identificador) não é pedido de novo."""
        print("\n--- Dados do paciente ---")
        dados = {"nome": self.le_texto("Nome: ")}
        if not editar:
            dados["cpf"] = self.le_texto("CPF: ")
        dados["celular"] = self.le_texto("Celular (com DDD): ")
        dados["idade"] = self.le_inteiro("Idade: ")
        return dados

    def mostra_paciente(self, dados_paciente: dict):
        print("-" * 40)
        print(f"Nome:    {dados_paciente['nome']}")
        print(f"CPF:     {self.fmt_cpf(dados_paciente['cpf'])}")
        print(f"Celular: {self.fmt_celular(dados_paciente['celular'])}")
        print(f"Idade:   {dados_paciente['idade']} anos")

    def seleciona_paciente(self) -> str:
        return self.le_texto("\nCPF do paciente selecionado: ")
