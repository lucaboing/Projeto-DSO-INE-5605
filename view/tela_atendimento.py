from view.tela_abstrata import TelaAbstrata


class TelaAtendimento(TelaAbstrata):
    def tela_opcoes(self) -> int:
        return self._le_opcao("ATENDIMENTOS", {
            1: "Agendar atendimento",
            2: "Alterar atendimento",
            3: "Excluir atendimento",
            4: "Listar atendimentos",
            5: "Incluir procedimento",
            6: "Alterar procedimento",
            7: "Excluir procedimento",
            8: "Listar procedimentos de um atendimento",
            9: "Incluir pagamento",
            10: "Alterar pagamento",
            11: "Excluir pagamento",
            12: "Listar pagamentos de um atendimento",
            0: "Retornar",
        })

    # ------------------------------------------------------------------ entrada
    def pega_dados_agendamento(self) -> dict:
        print("\n--- Dados do atendimento ---")
        return {
            "cpf_paciente": self.le_texto("CPF do paciente: "),
            "registro_profissional": self.le_texto("Registro do profissional: "),
            "nome_clinica": self.le_texto("Nome da clínica: "),
            "codigo_tipo": self.le_inteiro("Código do tipo de atendimento: "),
            "data": self.le_data("Data do atendimento"),
            "horario_inicio": self.le_horario("Horário de início"),
            "horario_fim": self.le_horario("Horário de fim"),
            "valor_base": self.le_decimal("Valor base (R$): "),
        }

    def pega_dados_procedimento(self) -> dict:
        print("\n--- Dados do procedimento ---")
        return {
            "descricao": self.le_texto("Descrição: "),
            "custo": self.le_decimal("Custo (R$): "),
            "registro_profissional": self.le_texto("Registro do profissional responsável: "),
        }

    def pega_dados_pagamento(self) -> dict:
        print("\n--- Dados do pagamento ---")
        print("Modalidade: 1 - Dinheiro | 2 - PIX | 3 - Cartão de crédito")
        modalidade = self.le_inteiro("Modalidade: ", [1, 2, 3])
        dados = {
            "modalidade": modalidade,
            "data": self.le_data("Data do pagamento"),
            "valor_pago": self.le_decimal("Valor pago (R$): "),
        }
        if modalidade == 2:
            dados["cpf_pagador"] = self.le_texto("CPF do pagador: ")
        elif modalidade == 3:
            dados["numero_cartao"] = self.le_texto("Número do cartão: ")
            dados["bandeira"] = self.le_texto("Bandeira: ")
        return dados

    def seleciona_atendimento(self) -> int:
        return self.le_inteiro("\nCódigo do atendimento selecionado: ")

    def seleciona_procedimento(self) -> str:
        return self.le_texto("\nDescrição do procedimento selecionado: ")

    def seleciona_pagamento(self) -> int:
        return self.le_inteiro("\nNúmero do pagamento selecionado: ")

    # ------------------------------------------------------------------- saída
    def mostra_atendimento(self, dados_atendimento: dict):
        d = dados_atendimento
        print("=" * 50)
        print(f"Atendimento nº {d['codigo']} - {d['tipo']}")
        print(f"Data:         {self.fmt_data(d['data'])} "
              f"({self.fmt_hora(d['horario_inicio'])} às {self.fmt_hora(d['horario_fim'])})")
        print(f"Clínica:      {d['clinica']}")
        print(f"Paciente:     {d['paciente']}")
        print(f"Profissional: {d['profissional']}")
        print(f"Valor base:   {self.fmt_moeda(d['valor_base'])}")
        self.mostra_procedimentos(d["procedimentos"])
        self.mostra_pagamentos(d["pagamentos"])
        print(f"Valor total:  {self.fmt_moeda(d['valor_total'])}")
        print(f"Saldo devedor: {self.fmt_moeda(d['saldo_devedor'])}")

    def mostra_procedimentos(self, dados_procedimentos: list):
        if not dados_procedimentos:
            print("Procedimentos: nenhum")
            return
        print("Procedimentos:")
        for p in dados_procedimentos:
            print(f"  - {p['descricao']} | {self.fmt_moeda(p['custo'])} | resp.: {p['profissional']}")

    def mostra_pagamentos(self, dados_pagamentos: list):
        if not dados_pagamentos:
            print("Pagamentos: nenhum")
            return
        print("Pagamentos:")
        for numero, p in enumerate(dados_pagamentos, start=1):
            extra = ""
            if "cpf_pagador" in p:
                extra = f" (CPF {self.fmt_cpf(p['cpf_pagador'])})"
            elif "bandeira" in p:
                extra = f" ({p['bandeira']} final {p['final_cartao']})"
            print(f"  {numero}) {self.fmt_data(p['data'])} | {self.fmt_moeda(p['valor_pago'])} | "
                  f"{p['modalidade']}{extra}")
