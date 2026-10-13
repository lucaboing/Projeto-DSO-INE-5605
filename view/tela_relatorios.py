from view.tela_abstrata import TelaAbstrata


class TelaRelatorios(TelaAbstrata):
    def tela_opcoes(self) -> int:
        return self._le_opcao("RELATÓRIOS", {
            1: "Clínicas com maior número de atendimentos",
            2: "Atendimentos mais caros e mais baratos",
            3: "Procedimentos mais realizados",
            4: "Procedimentos mais caros e mais baratos",
            0: "Retornar",
        })

    def mostra_relatorio_clinicas(self, dados: list):
        print("\n--- Clínicas com mais atendimentos ---")
        for posicao, d in enumerate(dados, start=1):
            print(f"{posicao}. {d['nome']} ({d['cidade']}) - {d['total_atendimentos']} atendimento(s)")

    def mostra_relatorio_atendimentos(self, dados: dict):
        print("\n--- Atendimentos mais caros ---")
        self.__lista_atendimentos(dados["mais_caros"])
        print("\n--- Atendimentos mais baratos ---")
        self.__lista_atendimentos(dados["mais_baratos"])

    def mostra_relatorio_procedimentos_populares(self, dados: list):
        print("\n--- Procedimentos mais realizados ---")
        for posicao, d in enumerate(dados, start=1):
            print(f"{posicao}. {d['descricao']} - {d['quantidade']} vez(es)")

    def mostra_relatorio_procedimentos_valores(self, dados: dict):
        print("\n--- Procedimentos mais caros ---")
        self.__lista_procedimentos(dados["mais_caros"])
        print("\n--- Procedimentos mais baratos ---")
        self.__lista_procedimentos(dados["mais_baratos"])

    def __lista_atendimentos(self, atendimentos: list):
        for posicao, a in enumerate(atendimentos, start=1):
            print(f"{posicao}. Atend. nº {a['codigo']} | {self.fmt_data(a['data'])} | {a['tipo']} | "
                  f"{a['clinica']} | {a['paciente']} | {self.fmt_moeda(a['valor_total'])}")

    def __lista_procedimentos(self, procedimentos: list):
        for posicao, p in enumerate(procedimentos, start=1):
            print(f"{posicao}. {p['descricao']} | {self.fmt_moeda(p['custo'])} | "
                  f"resp.: {p['profissional']} | atend. nº {p['codigo_atendimento']}")
