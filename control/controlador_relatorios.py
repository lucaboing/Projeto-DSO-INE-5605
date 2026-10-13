from collections import defaultdict

from view.tela_relatorios import TelaRelatorios

LIMITE = 3  # quantidade de itens nos rankings "mais caros" / "mais baratos"


class ControladorRelatorios:
    def __init__(self, controlador_sistema):
        self.__tela_relatorios = TelaRelatorios()
        self.__controlador_sistema = controlador_sistema

    def abre_tela(self):
        opcoes = {
            1: self.relatorio_clinicas_mais_atendimentos,
            2: self.relatorio_atendimentos_caros_baratos,
            3: self.relatorio_procedimentos_populares,
            4: self.relatorio_procedimentos_caros_baratos,
        }
        while True:
            opcao = self.__tela_relatorios.tela_opcoes()
            if opcao == 0:
                return
            opcoes[opcao]()

    def relatorio_clinicas_mais_atendimentos(self):
        atendimentos = self.__atendimentos()
        if not atendimentos:
            self.__tela_relatorios.mostra_mensagem("Não há atendimentos para gerar o relatório.")
            return
        contagem = defaultdict(int)
        cidades = {}
        for a in atendimentos:
            contagem[a.clinica.nome] += 1
            cidades[a.clinica.nome] = a.clinica.cidade
        dados = [
            {"nome": nome, "cidade": cidades[nome], "total_atendimentos": total}
            for nome, total in contagem.items()
        ]
        dados.sort(key=lambda d: (-d["total_atendimentos"], d["nome"]))
        self.__tela_relatorios.mostra_relatorio_clinicas(dados)

    def relatorio_atendimentos_caros_baratos(self):
        atendimentos = self.__atendimentos()
        if not atendimentos:
            self.__tela_relatorios.mostra_mensagem("Não há atendimentos para gerar o relatório.")
            return
        montar = self.__controlador_sistema.controlador_atendimento.montar_dados_atendimento
        ordenados = sorted(atendimentos, key=lambda a: a.calcular_valor_total(), reverse=True)
        self.__tela_relatorios.mostra_relatorio_atendimentos({
            "mais_caros": [montar(a) for a in ordenados[:LIMITE]],
            "mais_baratos": [montar(a) for a in list(reversed(ordenados))[:LIMITE]],
        })

    def relatorio_procedimentos_populares(self):
        procedimentos = self.__procedimentos()
        if not procedimentos:
            self.__tela_relatorios.mostra_mensagem("Não há procedimentos registrados.")
            return
        contagem = defaultdict(int)
        nomes = {}
        for p, _ in procedimentos:
            chave = p.descricao.lower()
            contagem[chave] += 1
            nomes.setdefault(chave, p.descricao)
        dados = [{"descricao": nomes[chave], "quantidade": qtd} for chave, qtd in contagem.items()]
        dados.sort(key=lambda d: (-d["quantidade"], d["descricao"]))
        self.__tela_relatorios.mostra_relatorio_procedimentos_populares(dados)

    def relatorio_procedimentos_caros_baratos(self):
        procedimentos = self.__procedimentos()
        if not procedimentos:
            self.__tela_relatorios.mostra_mensagem("Não há procedimentos registrados.")
            return
        ordenados = sorted(procedimentos, key=lambda par: par[0].custo, reverse=True)

        def para_dict(par):
            p, atendimento = par
            return {
                "descricao": p.descricao,
                "custo": p.custo,
                "profissional": p.profissional_responsavel.nome,
                "codigo_atendimento": atendimento.codigo,
            }

        self.__tela_relatorios.mostra_relatorio_procedimentos_valores({
            "mais_caros": [para_dict(par) for par in ordenados[:LIMITE]],
            "mais_baratos": [para_dict(par) for par in list(reversed(ordenados))[:LIMITE]],
        })

    # -------------------------------------------------------------------- auxiliares
    def __atendimentos(self):
        return self.__controlador_sistema.controlador_atendimento.atendimentos

    def __procedimentos(self):
        """Lista de pares (procedimento, atendimento) de todos os atendimentos."""
        return [(p, a) for a in self.__atendimentos() for p in a.procedimentos]
