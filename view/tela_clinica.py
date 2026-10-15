from view.tela_abstrata import TelaAbstrata


class TelaClinica(TelaAbstrata):
    def tela_opcoes(self) -> int:
        return self._le_opcao("CLÍNICAS", {
            1: "Incluir clínica",
            2: "Alterar clínica",
            3: "Excluir clínica",
            4: "Listar clínicas",
            5: "Vincular profissional à clínica",
            0: "Retornar",
        })

    def pega_dados_clinica(self, editar: bool = False) -> dict:
        print("\n--- Dados da clínica ---")
        dados = {}
        if not editar:
            dados["nome"] = self.le_texto("Nome: ")
        dados["cidade"] = self.le_texto("Cidade: ")
        dados["descricao"] = self.le_texto("Descrição: ")
        dados["horario_abertura"] = self.le_horario("Horário de abertura")
        dados["horario_fechamento"] = self.le_horario("Horário de fechamento")
        return dados

    def mostra_clinica(self, dados_clinica: dict):
        print("-" * 40)
        print(f"Nome:         {dados_clinica['nome']}")
        print(f"Cidade:       {dados_clinica['cidade']}")
        print(f"Descrição:    {dados_clinica['descricao']}")
        print(f"Funcionamento: {self.fmt_hora(dados_clinica['horario_abertura'])} às "
              f"{self.fmt_hora(dados_clinica['horario_fechamento'])}")
        profissionais = dados_clinica["profissionais"]
        print("Profissionais: " + (", ".join(profissionais) if profissionais else "nenhum vinculado"))

    def seleciona_clinica(self) -> str:
        return self.le_texto("\nNome da clínica selecionada: ")
