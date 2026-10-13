from exception.horario_fora_expediente_exception import HorarioForaExpedienteException
from exception.objeto_nao_encontrado_exception import ObjetoNaoEncontradoException
from model.clinica import Clinica
from view.tela_clinica import TelaClinica


class ControladorClinica:
    def __init__(self, controlador_sistema):
        self.__tela_clinica = TelaClinica()
        self.__clinicas = []
        self.__controlador_sistema = controlador_sistema

    @property
    def clinicas(self):
        return list(self.__clinicas)

    def abre_tela(self):
        opcoes = {
            1: self.incluir_clinica,
            2: self.alterar_clinica,
            3: self.excluir_clinica,
            4: self.listar_clinicas,
            5: self.vincular_profissional,
        }
        while True:
            opcao = self.__tela_clinica.tela_opcoes()
            if opcao == 0:
                return
            try:
                opcoes[opcao]()
            except (ObjetoNaoEncontradoException, HorarioForaExpedienteException,
                    ValueError, TypeError) as e:
                self.__tela_clinica.mostra_mensagem(str(e))

    def incluir_clinica(self):
        dados = self.__tela_clinica.pega_dados_clinica()
        clinica = Clinica(
            dados["nome"], dados["cidade"], dados["descricao"],
            dados["horario_abertura"], dados["horario_fechamento"],
        )
        if any(c.nome == clinica.nome for c in self.__clinicas):
            raise ValueError("Já existe clínica cadastrada com este nome.")
        self.__clinicas.append(clinica)
        self.__tela_clinica.mostra_mensagem("Clínica cadastrada com sucesso.")

    def alterar_clinica(self):
        """O nome é o identificador da clínica e não é alterado."""
        clinica = self.__selecionar_clinica()
        dados = self.__tela_clinica.pega_dados_clinica(editar=True)
        # Clínica temporária: valida tudo antes de alterar qualquer campo.
        nova = Clinica(
            clinica.nome, dados["cidade"], dados["descricao"],
            dados["horario_abertura"], dados["horario_fechamento"],
        )
        atendimentos = self.__controlador_sistema.controlador_atendimento.atendimentos
        for a in atendimentos:
            if a.clinica is clinica and (a.horario_inicio < nova.horario_abertura
                                         or a.horario_fim > nova.horario_fechamento):
                raise HorarioForaExpedienteException(
                    f"O atendimento nº {a.codigo} ficaria fora do novo horário de funcionamento."
                )
        clinica.alterar_horario_funcionamento(nova.horario_abertura, nova.horario_fechamento)
        clinica.cidade = nova.cidade
        clinica.descricao = nova.descricao
        self.__tela_clinica.mostra_mensagem("Clínica alterada com sucesso.")

    def excluir_clinica(self):
        clinica = self.__selecionar_clinica()
        atendimentos = self.__controlador_sistema.controlador_atendimento.atendimentos
        if any(a.clinica is clinica for a in atendimentos):
            raise ValueError("A clínica possui atendimentos registrados e não pode ser excluída.")
        self.__clinicas.remove(clinica)
        self.__tela_clinica.mostra_mensagem("Clínica excluída com sucesso.")

    def listar_clinicas(self):
        if not self.__clinicas:
            self.__tela_clinica.mostra_mensagem("Nenhuma clínica cadastrada.")
            return
        for c in self.__clinicas:
            self.__tela_clinica.mostra_clinica({
                "nome": c.nome,
                "cidade": c.cidade,
                "descricao": c.descricao,
                "horario_abertura": c.horario_abertura,
                "horario_fechamento": c.horario_fechamento,
                "profissionais": [p.nome for p in c.listar_profissionais()],
            })

    def buscar_clinica_por_nome(self, nome: str) -> Clinica:
        nome = nome.strip()
        for clinica in self.__clinicas:
            if clinica.nome == nome:
                return clinica
        raise ObjetoNaoEncontradoException(f"Clínica '{nome}' não encontrada.")

    def vincular_profissional(self):
        clinica = self.__selecionar_clinica()
        profissional = self.__controlador_sistema.controlador_profissional.selecionar_profissional()
        clinica.adicionar_profissional(profissional)  # o model rejeita registro duplicado
        self.__tela_clinica.mostra_mensagem("Profissional vinculado à clínica com sucesso.")

    def __selecionar_clinica(self) -> Clinica:
        if not self.__clinicas:
            raise ObjetoNaoEncontradoException("Nenhuma clínica cadastrada.")
        self.listar_clinicas()
        return self.buscar_clinica_por_nome(self.__tela_clinica.seleciona_clinica())
