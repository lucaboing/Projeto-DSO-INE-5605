from view.tela_abstrata import TelaAbstrata


class TelaProfissional(TelaAbstrata):
    def tela_opcoes(self) -> int:
        return self._le_opcao("PROFISSIONAIS DE SAÚDE", {
            1: "Incluir profissional",
            2: "Alterar profissional",
            3: "Excluir profissional",
            4: "Listar profissionais",
            0: "Retornar",
        })

    def pega_dados_profissional(self, editar: bool = False) -> dict:
        print("\n--- Dados do profissional ---")
        dados = {
            "nome": self.le_texto("Nome: "),
            "cpf": self.le_texto("CPF: "),
            "celular": self.le_texto("Celular (com DDD): "),
            "especialidade": self.le_texto("Especialidade: "),
        }
        if not editar:
            dados["registro"] = self.le_texto("Registro profissional: ")
        return dados

    def mostra_profissional(self, dados_profissional: dict):
        print("-" * 40)
        print(f"Nome:          {dados_profissional['nome']}")
        print(f"CPF:           {self.fmt_cpf(dados_profissional['cpf'])}")
        print(f"Celular:       {self.fmt_celular(dados_profissional['celular'])}")
        print(f"Especialidade: {dados_profissional['especialidade']}")
        print(f"Registro:      {dados_profissional['registro']}")

    def seleciona_profissional(self) -> str:
        return self.le_texto("\nRegistro do profissional selecionado: ")
