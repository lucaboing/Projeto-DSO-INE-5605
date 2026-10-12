class PagamentoAtrasadoException(Exception):
    """Pagamento com data posterior à data do atendimento."""

    def __init__(self, mensagem: str = "Pagamento realizado após a data do atendimento."):
        super().__init__(mensagem)
