class ObjetoNaoEncontradoException(Exception):
    """Objeto buscado (para alterar, excluir ou consultar) não existe."""

    def __init__(self, mensagem: str = "Objeto não encontrado."):
        super().__init__(mensagem)
