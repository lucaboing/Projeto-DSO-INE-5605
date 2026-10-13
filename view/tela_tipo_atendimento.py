from view.tela_abstrata import TelaAbstrata


class TelaTipoAtendimento(TelaAbstrata):
    def tela_opcoes(self) -> int:
        return self._le_opcao("TIPOS DE ATENDIMENTO", {
            1: "Incluir tipo",
            2: "Alterar tipo",
            3: "Excluir tipo",
            4: "Listar tipos",
            0: "Retornar",
        })

    def pega_dados_tipo(self, editar: bool = False) -> dict:
        """Na alteração o código (identificador) não é pedido de novo."""
        print("\n--- Dados do tipo de atendimento ---")
        dados = {}
        if not editar:
            dados["codigo"] = self.le_inteiro("Código: ")
        dados["tipo_atendimento"] = self.le_texto("Descrição do tipo (ex.: consulta, exame, retorno): ")
        return dados

    def mostra_tipo(self, dados_tipo: dict):
        print("-" * 40)
        print(f"Código: {dados_tipo['codigo']}")
        print(f"Tipo:   {dados_tipo['tipo_atendimento']}")

    def seleciona_tipo(self) -> int:
        return self.le_inteiro("\nCódigo do tipo selecionado: ")
