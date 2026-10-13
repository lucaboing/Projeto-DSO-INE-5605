from exception.objeto_nao_encontrado_exception import ObjetoNaoEncontradoException
from model.tipo_atendimento import TipoAtendimento
from view.tela_tipo_atendimento import TelaTipoAtendimento


class ControladorTipoAtendimento:
    def __init__(self, controlador_sistema):
        self.__tela_tipo = TelaTipoAtendimento()
        self.__tipos = []
        self.__controlador_sistema = controlador_sistema

    @property
    def tipos(self):
        return list(self.__tipos)

    def abre_tela(self):
        opcoes = {
            1: self.incluir_tipo,
            2: self.alterar_tipo,
            3: self.excluir_tipo,
            4: self.listar_tipos,
        }
        while True:
            opcao = self.__tela_tipo.tela_opcoes()
            if opcao == 0:
                return
            try:
                opcoes[opcao]()
            except (ObjetoNaoEncontradoException, ValueError, TypeError) as e:
                self.__tela_tipo.mostra_mensagem(str(e))

    def incluir_tipo(self):
        dados = self.__tela_tipo.pega_dados_tipo()
        tipo = TipoAtendimento(dados["codigo"], dados["tipo_atendimento"])
        if any(t.codigo == tipo.codigo for t in self.__tipos):
            raise ValueError("Já existe tipo de atendimento com este código.")
        self.__tipos.append(tipo)
        self.__tela_tipo.mostra_mensagem("Tipo de atendimento cadastrado com sucesso.")

    def alterar_tipo(self):
        """O código é o identificador do tipo e não é alterado."""
        tipo = self.__selecionar_tipo()
        dados = self.__tela_tipo.pega_dados_tipo(editar=True)
        novo = TipoAtendimento(tipo.codigo, dados["tipo_atendimento"])  # valida antes de alterar
        tipo.tipo_atendimento = novo.tipo_atendimento
        self.__tela_tipo.mostra_mensagem("Tipo de atendimento alterado com sucesso.")

    def excluir_tipo(self):
        tipo = self.__selecionar_tipo()
        atendimentos = self.__controlador_sistema.controlador_atendimento.atendimentos
        if any(a.tipo is tipo for a in atendimentos):
            raise ValueError("O tipo está em uso por atendimentos e não pode ser excluído.")
        self.__tipos.remove(tipo)
        self.__tela_tipo.mostra_mensagem("Tipo de atendimento excluído com sucesso.")

    def listar_tipos(self):
        if not self.__tipos:
            self.__tela_tipo.mostra_mensagem("Nenhum tipo de atendimento cadastrado.")
            return
        for t in self.__tipos:
            self.__tela_tipo.mostra_tipo({
                "codigo": t.codigo,
                "tipo_atendimento": t.tipo_atendimento,
            })

    def buscar_tipo_por_codigo(self, codigo: int) -> TipoAtendimento:
        for tipo in self.__tipos:
            if tipo.codigo == codigo:
                return tipo
        raise ObjetoNaoEncontradoException(f"Tipo de atendimento com código {codigo} não encontrado.")

    def __selecionar_tipo(self) -> TipoAtendimento:
        if not self.__tipos:
            raise ObjetoNaoEncontradoException("Nenhum tipo de atendimento cadastrado.")
        self.listar_tipos()
        return self.buscar_tipo_por_codigo(self.__tela_tipo.seleciona_tipo())
