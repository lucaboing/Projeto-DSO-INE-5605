class PacienteMenorIdadeException(Exception):
    """Paciente com menos de 18 anos tentando realizar atendimento independente."""

    def __init__(self, mensagem: str = "Paciente menor de idade."):
        super().__init__(mensagem)
