from exception.objeto_nao_encontrado_exception import ObjetoNaoEncontradoException
from model.profissional_saude import ProfissionalSaude
from view.tela_profissional import TelaProfissional


class ControladorProfissional:
    def __init__(self, controlador_sistema):
        self.__tela_profissional = TelaProfissional()
        self.__profissionais = []
        self.__controlador_sistema = controlador_sistema

    @property
    def profissionais(self):
        return list(self.__profissionais)

    def abre_tela(self):
        opcoes = {
            1: self.incluir_profissional,
            2: self.alterar_profissional,
            3: self.excluir_profissional,
            4: self.listar_profissionais,
        }
        while True:
            opcao = self.__tela_profissional.tela_opcoes()
            if opcao == 0:
                return
            try:
                opcoes[opcao]()
            except (ObjetoNaoEncontradoException, ValueError, TypeError) as e:
                self.__tela_profissional.mostra_mensagem(str(e))

    def incluir_profissional(self):
        dados = self.__tela_profissional.pega_dados_profissional()
        profissional = ProfissionalSaude(
            dados["nome"], dados["cpf"], dados["celular"],
            dados["especialidade"], dados["registro"],
        )
        if any(p.registro == profissional.registro for p in self.__profissionais):
            raise ValueError("Já existe profissional cadastrado com este registro.")
        self.__profissionais.append(profissional)
        self.__tela_profissional.mostra_mensagem("Profissional cadastrado com sucesso.")

    def alterar_profissional(self):
        """O registro profissional é o identificador e não é alterado."""
        profissional = self.selecionar_profissional()
        dados = self.__tela_profissional.pega_dados_profissional(editar=True)
        # Profissional temporário: valida tudo antes de alterar qualquer campo.
        novo = ProfissionalSaude(
            dados["nome"], dados["cpf"], dados["celular"],
            dados["especialidade"], profissional.registro,
        )
        profissional.nome = novo.nome
        profissional.cpf = novo.cpf
        profissional.celular = novo.celular
        profissional.especialidade = novo.especialidade
        self.__tela_profissional.mostra_mensagem("Profissional alterado com sucesso.")

    def excluir_profissional(self):
        profissional = self.selecionar_profissional()
        if self.__em_uso(profissional):
            raise ValueError(
                "O profissional está vinculado a atendimentos ou procedimentos e não pode ser excluído."
            )
        # Desvincula das clínicas (agregação) antes de remover do cadastro.
        for clinica in self.__controlador_sistema.controlador_clinica.clinicas:
            if any(p.registro == profissional.registro for p in clinica.listar_profissionais()):
                clinica.remover_profissional(profissional.registro)
        self.__profissionais.remove(profissional)
        self.__tela_profissional.mostra_mensagem("Profissional excluído com sucesso.")

    def listar_profissionais(self):
        if not self.__profissionais:
            self.__tela_profissional.mostra_mensagem("Nenhum profissional cadastrado.")
            return
        for p in self.__profissionais:
            self.__tela_profissional.mostra_profissional({
                "nome": p.nome,
                "cpf": p.cpf,
                "celular": p.celular,
                "especialidade": p.especialidade,
                "registro": p.registro,
            })

    def buscar_profissional_por_registro(self, registro: str) -> ProfissionalSaude:
        registro = registro.strip()
        for profissional in self.__profissionais:
            if profissional.registro == registro:
                return profissional
        raise ObjetoNaoEncontradoException(f"Profissional com registro {registro} não encontrado.")

    def selecionar_profissional(self) -> ProfissionalSaude:
        """Lista os profissionais e pede o registro (também usado pelo ControladorClinica)."""
        if not self.__profissionais:
            raise ObjetoNaoEncontradoException("Nenhum profissional cadastrado.")
        self.listar_profissionais()
        return self.buscar_profissional_por_registro(self.__tela_profissional.seleciona_profissional())

    def __em_uso(self, profissional) -> bool:
        atendimentos = self.__controlador_sistema.controlador_atendimento.atendimentos
        for a in atendimentos:
            if a.profissional is profissional:
                return True
            if any(proc.profissional_responsavel is profissional for proc in a.procedimentos):
                return True
        return False
