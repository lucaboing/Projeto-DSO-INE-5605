from exception.horario_fora_expediente_exception import HorarioForaExpedienteException
from exception.objeto_nao_encontrado_exception import ObjetoNaoEncontradoException
from exception.pagamento_atrasado_exception import PagamentoAtrasadoException
from exception.paciente_menor_idade_exception import PacienteMenorIdadeException
from model.atendimento import Atendimento
from model.pagamento import Pagamento
from model.pagamento_cartao import PagamentoCartao
from model.pagamento_dinheiro import PagamentoDinheiro
from model.pagamento_pix import PagamentoPix
from model.procedimento import Procedimento
from view.tela_atendimento import TelaAtendimento


class ControladorAtendimento:
    def __init__(self, controlador_sistema):
        self.__tela_atendimento = TelaAtendimento()
        self.__atendimentos = []
        self.__controlador_sistema = controlador_sistema
        self.__proximo_codigo = 1

    @property
    def atendimentos(self):
        return list(self.__atendimentos)

    def abre_tela(self):
        opcoes = {
            1: self.incluir_atendimento,
            2: self.alterar_atendimento,
            3: self.excluir_atendimento,
            4: self.listar_atendimentos,
            5: self.incluir_procedimento,
            6: self.alterar_procedimento,
            7: self.excluir_procedimento,
            8: self.listar_procedimentos,
            9: self.incluir_pagamento,
            10: self.alterar_pagamento,
            11: self.excluir_pagamento,
            12: self.listar_pagamentos,
        }
        while True:
            opcao = self.__tela_atendimento.tela_opcoes()
            if opcao == 0:
                return
            try:
                opcoes[opcao]()
            except (ObjetoNaoEncontradoException, PacienteMenorIdadeException,
                    HorarioForaExpedienteException, PagamentoAtrasadoException,
                    ValueError, TypeError) as e:
                self.__tela_atendimento.mostra_mensagem(str(e))

    # ------------------------------------------------------------------ atendimento
    def incluir_atendimento(self):
        """O model (Atendimento) valida idade do paciente, horário de funcionamento e valores."""
        dados = self.__tela_atendimento.pega_dados_agendamento()
        atendimento = self.__montar_atendimento(self.__proximo_codigo, dados)
        self.__atendimentos.append(atendimento)
        self.__proximo_codigo += 1
        self.__tela_atendimento.mostra_mensagem(
            f"Atendimento nº {atendimento.codigo} agendado com sucesso."
        )

    def alterar_atendimento(self):
        antigo = self.__selecionar_atendimento()
        dados = self.__tela_atendimento.pega_dados_agendamento()
        # Monta um atendimento novo com o mesmo código e reaplica procedimentos e pagamentos.
        # Se algo for inválido (idade, horário, pagamento depois da nova data, saldo...),
        # a exceção sobe e o atendimento original permanece intacto.
        novo = self.__montar_atendimento(antigo.codigo, dados)
        for procedimento in antigo.procedimentos:
            novo.adicionar_procedimento(procedimento)
        for pagamento in antigo.pagamentos:
            novo.registrar_pagamento(pagamento)
        self.__atendimentos[self.__atendimentos.index(antigo)] = novo
        self.__tela_atendimento.mostra_mensagem("Atendimento alterado com sucesso.")

    def excluir_atendimento(self):
        atendimento = self.__selecionar_atendimento()
        # Procedimentos e pagamentos são compostos pelo atendimento e saem junto com ele.
        self.__atendimentos.remove(atendimento)
        self.__tela_atendimento.mostra_mensagem("Atendimento excluído com sucesso.")

    def listar_atendimentos(self):
        if not self.__atendimentos:
            self.__tela_atendimento.mostra_mensagem("Nenhum atendimento registrado.")
            return
        for atendimento in self.__atendimentos:
            self.__tela_atendimento.mostra_atendimento(self.montar_dados_atendimento(atendimento))

    def buscar_atendimento_por_codigo(self, codigo: int) -> Atendimento:
        for atendimento in self.__atendimentos:
            if atendimento.codigo == codigo:
                return atendimento
        raise ObjetoNaoEncontradoException(f"Atendimento com código {codigo} não encontrado.")

    # ---------------------------------------------------------------- procedimentos
    def incluir_procedimento(self):
        atendimento = self.__selecionar_atendimento()
        procedimento = self.__criar_procedimento(self.__tela_atendimento.pega_dados_procedimento())
        if self.__buscar_procedimento(atendimento, procedimento.descricao, falhar=False):
            raise ValueError("Este procedimento já foi registrado neste atendimento.")
        atendimento.adicionar_procedimento(procedimento)
        self.__tela_atendimento.mostra_mensagem("Procedimento registrado com sucesso.")

    def alterar_procedimento(self):
        atendimento = self.__selecionar_atendimento()
        antigo = self.__selecionar_procedimento(atendimento)
        novo = self.__criar_procedimento(self.__tela_atendimento.pega_dados_procedimento())
        outro = self.__buscar_procedimento(atendimento, novo.descricao, falhar=False)
        if outro is not None and outro is not antigo:
            raise ValueError("Já existe outro procedimento com esta descrição neste atendimento.")
        antigo.descricao = novo.descricao
        antigo.custo = novo.custo
        antigo.profissional_responsavel = novo.profissional_responsavel
        self.__tela_atendimento.mostra_mensagem("Procedimento alterado com sucesso.")

    def excluir_procedimento(self):
        atendimento = self.__selecionar_atendimento()
        procedimento = self.__selecionar_procedimento(atendimento)
        atendimento.remover_procedimento(procedimento.descricao)
        self.__tela_atendimento.mostra_mensagem("Procedimento excluído com sucesso.")

    def listar_procedimentos(self):
        atendimento = self.__selecionar_atendimento()
        self.__tela_atendimento.mostra_procedimentos(self.__dados_procedimentos(atendimento))

    # ------------------------------------------------------------------- pagamentos
    def incluir_pagamento(self):
        atendimento = self.__selecionar_atendimento()
        pagamento = self.__criar_pagamento(self.__tela_atendimento.pega_dados_pagamento())
        # O model valida a data (até o dia do atendimento) e se o valor cabe no saldo devedor.
        atendimento.registrar_pagamento(pagamento)
        self.__tela_atendimento.mostra_mensagem(
            f"Pagamento registrado. Saldo devedor: R$ {atendimento.calcular_saldo_devedor():.2f}."
        )

    def alterar_pagamento(self):
        atendimento = self.__selecionar_atendimento()
        antigo = self.__selecionar_pagamento(atendimento)
        novo = self.__criar_pagamento(self.__tela_atendimento.pega_dados_pagamento())
        atendimento.remover_pagamento(antigo)
        try:
            atendimento.registrar_pagamento(novo)
        except Exception:
            atendimento.registrar_pagamento(antigo)  # desfaz: o pagamento antigo era válido
            raise
        self.__tela_atendimento.mostra_mensagem(
            f"Pagamento alterado. Saldo devedor: R$ {atendimento.calcular_saldo_devedor():.2f}."
        )

    def excluir_pagamento(self):
        atendimento = self.__selecionar_atendimento()
        pagamento = self.__selecionar_pagamento(atendimento)
        atendimento.remover_pagamento(pagamento)
        self.__tela_atendimento.mostra_mensagem(
            f"Pagamento excluído. Saldo devedor: R$ {atendimento.calcular_saldo_devedor():.2f}."
        )

    def listar_pagamentos(self):
        atendimento = self.__selecionar_atendimento()
        self.__tela_atendimento.mostra_pagamentos(self.__dados_pagamentos(atendimento))

    # -------------------------------------------------------------------- auxiliares
    def montar_dados_atendimento(self, atendimento: Atendimento) -> dict:
        """Converte o atendimento em dict para as telas e para os relatórios."""
        return {
            "codigo": atendimento.codigo,
            "data": atendimento.data,
            "horario_inicio": atendimento.horario_inicio,
            "horario_fim": atendimento.horario_fim,
            "tipo": atendimento.tipo.tipo_atendimento,
            "valor_base": atendimento.valor_base,
            "paciente": atendimento.paciente.nome,
            "profissional": atendimento.profissional.nome,
            "clinica": atendimento.clinica.nome,
            "procedimentos": self.__dados_procedimentos(atendimento),
            "pagamentos": self.__dados_pagamentos(atendimento),
            "valor_total": atendimento.calcular_valor_total(),
            "saldo_devedor": atendimento.calcular_saldo_devedor(),
        }

    @staticmethod
    def __dados_procedimentos(atendimento: Atendimento) -> list:
        return [
            {
                "descricao": p.descricao,
                "custo": p.custo,
                "profissional": p.profissional_responsavel.nome,
            }
            for p in atendimento.procedimentos
        ]

    @staticmethod
    def __dados_pagamentos(atendimento: Atendimento) -> list:
        lista = []
        for p in atendimento.pagamentos:
            item = {"data": p.data, "valor_pago": p.valor_pago}
            if isinstance(p, PagamentoPix):
                item["modalidade"] = "PIX"
                item["cpf_pagador"] = p.cpf_pagador
            elif isinstance(p, PagamentoCartao):
                item["modalidade"] = "Cartão de crédito"
                item["bandeira"] = p.bandeira
                item["final_cartao"] = p.numero_cartao[-4:]
            else:
                item["modalidade"] = "Dinheiro"
            lista.append(item)
        return lista

    def __montar_atendimento(self, codigo: int, dados: dict) -> Atendimento:
        sistema = self.__controlador_sistema
        paciente = sistema.controlador_paciente.buscar_paciente_por_cpf(dados["cpf_paciente"])
        profissional = sistema.controlador_profissional \
            .buscar_profissional_por_registro(dados["registro_profissional"])
        clinica = sistema.controlador_clinica.buscar_clinica_por_nome(dados["nome_clinica"])
        tipo = sistema.controlador_tipo_atendimento.buscar_tipo_por_codigo(dados["codigo_tipo"])
        return Atendimento(
            codigo, dados["data"], dados["horario_inicio"], dados["horario_fim"],
            tipo, dados["valor_base"], paciente, profissional, clinica,
        )

    def __criar_procedimento(self, dados: dict) -> Procedimento:
        profissional = self.__controlador_sistema.controlador_profissional \
            .buscar_profissional_por_registro(dados["registro_profissional"])
        return Procedimento(dados["descricao"], dados["custo"], profissional)

    @staticmethod
    def __criar_pagamento(dados: dict) -> Pagamento:
        modalidade = dados["modalidade"]
        if modalidade == 1:
            return PagamentoDinheiro(dados["data"], dados["valor_pago"])
        if modalidade == 2:
            return PagamentoPix(dados["data"], dados["valor_pago"], dados["cpf_pagador"])
        if modalidade == 3:
            return PagamentoCartao(
                dados["data"], dados["valor_pago"], dados["numero_cartao"], dados["bandeira"]
            )
        raise ValueError("Modalidade de pagamento inválida.")

    def __selecionar_atendimento(self) -> Atendimento:
        if not self.__atendimentos:
            raise ObjetoNaoEncontradoException("Nenhum atendimento registrado.")
        self.listar_atendimentos()
        return self.buscar_atendimento_por_codigo(self.__tela_atendimento.seleciona_atendimento())

    @staticmethod
    def __buscar_procedimento(atendimento: Atendimento, descricao: str, falhar: bool = True):
        alvo = descricao.strip().lower()
        for procedimento in atendimento.procedimentos:
            if procedimento.descricao.lower() == alvo:
                return procedimento
        if falhar:
            raise ObjetoNaoEncontradoException(
                f"Procedimento '{descricao}' não encontrado no atendimento {atendimento.codigo}."
            )
        return None

    def __selecionar_procedimento(self, atendimento: Atendimento) -> Procedimento:
        if not atendimento.procedimentos:
            raise ObjetoNaoEncontradoException("Este atendimento não possui procedimentos.")
        self.__tela_atendimento.mostra_procedimentos(self.__dados_procedimentos(atendimento))
        descricao = self.__tela_atendimento.seleciona_procedimento()
        return self.__buscar_procedimento(atendimento, descricao)

    def __selecionar_pagamento(self, atendimento: Atendimento) -> Pagamento:
        pagamentos = atendimento.pagamentos
        if not pagamentos:
            raise ObjetoNaoEncontradoException("Este atendimento não possui pagamentos.")
        self.__tela_atendimento.mostra_pagamentos(self.__dados_pagamentos(atendimento))
        numero = self.__tela_atendimento.seleciona_pagamento()
        if not 1 <= numero <= len(pagamentos):
            raise ObjetoNaoEncontradoException(f"Pagamento nº {numero} não encontrado.")
        return pagamentos[numero - 1]
