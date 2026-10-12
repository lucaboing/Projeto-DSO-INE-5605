class HorarioForaExpedienteException(Exception):
    """Atendimento fora do período de funcionamento da clínica."""

    def __init__(self, mensagem: str = "Horário fora do expediente da clínica."):
        super().__init__(mensagem)
