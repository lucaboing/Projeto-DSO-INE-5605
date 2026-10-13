from exception.objeto_nao_encontrado_exception import ObjetoNaoEncontradoException
from exception.paciente_menor_idade_exception import PacienteMenorIdadeException
from model.atendimento import Atendimento
from model.paciente import Paciente
from model.validacoes import validar_cpf
from view.tela_paciente import TelaPaciente


class ControladorPaciente:
    def __init__(self, controlador_sistema):
        self.__tela_paciente = TelaPaciente()
        self.__pacientes = []
        self.__controlador_sistema = controlador_sistema

    @property
    def pacientes(self):
        return list(self.__pacientes)

    def abre_tela(self):
        opcoes = {
            1: self.incluir_paciente,
            2: self.alterar_paciente,
            3: self.excluir_paciente,
            4: self.listar_pacientes,
        }
        while True:
            opcao = self.__tela_paciente.tela_opcoes()
            if opcao == 0:
                return
            try:
                opcoes[opcao]()
            except (ObjetoNaoEncontradoException, PacienteMenorIdadeException,
                    ValueError, TypeError) as e:
                self.__tela_paciente.mostra_mensagem(str(e))

    def incluir_paciente(self):
        dados = self.__tela_paciente.pega_dados_paciente()
        # O model valida nome, CPF, celular e idade ao instanciar.
        paciente = Paciente(dados["nome"], dados["cpf"], dados["celular"], dados["idade"])
        if any(p.cpf == paciente.cpf for p in self.__pacientes):
            raise ValueError("Já existe paciente cadastrado com este CPF.")
        self.__pacientes.append(paciente)
        self.__tela_paciente.mostra_mensagem("Paciente cadastrado com sucesso.")

    def alterar_paciente(self):
        """O CPF é o identificador do paciente e não é alterado."""
        paciente = self.__selecionar_paciente()
        dados = self.__tela_paciente.pega_dados_paciente(editar=True)
        # Instancia um paciente temporário: valida tudo antes de alterar qualquer campo.
        novo = Paciente(dados["nome"], paciente.cpf, dados["celular"], dados["idade"])
        atendimentos = self.__controlador_sistema.controlador_atendimento.atendimentos
        if novo.idade < Atendimento.IDADE_MINIMA and any(a.paciente is paciente for a in atendimentos):
            raise PacienteMenorIdadeException(
                "A nova idade tornaria o paciente menor de idade, mas ele já possui atendimentos."
            )
        paciente.nome = novo.nome
        paciente.celular = novo.celular
        paciente.idade = novo.idade
        self.__tela_paciente.mostra_mensagem("Paciente alterado com sucesso.")

    def excluir_paciente(self):
        paciente = self.__selecionar_paciente()
        atendimentos = self.__controlador_sistema.controlador_atendimento.atendimentos
        if any(a.paciente is paciente for a in atendimentos):
            raise ValueError("O paciente possui atendimentos registrados e não pode ser excluído.")
        self.__pacientes.remove(paciente)
        self.__tela_paciente.mostra_mensagem("Paciente excluído com sucesso.")

    def listar_pacientes(self):
        if not self.__pacientes:
            self.__tela_paciente.mostra_mensagem("Nenhum paciente cadastrado.")
            return
        for paciente in self.__pacientes:
            self.__tela_paciente.mostra_paciente({
                "nome": paciente.nome,
                "cpf": paciente.cpf,
                "celular": paciente.celular,
                "idade": paciente.idade,
            })

    def buscar_paciente_por_cpf(self, cpf: str) -> Paciente:
        cpf = validar_cpf(cpf)  # normaliza (só dígitos), igual ao que o model guarda
        for paciente in self.__pacientes:
            if paciente.cpf == cpf:
                return paciente
        raise ObjetoNaoEncontradoException(f"Paciente com CPF {cpf} não encontrado.")

    def __selecionar_paciente(self) -> Paciente:
        if not self.__pacientes:
            raise ObjetoNaoEncontradoException("Nenhum paciente cadastrado.")
        self.listar_pacientes()
        return self.buscar_paciente_por_cpf(self.__tela_paciente.seleciona_paciente())
