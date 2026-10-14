import math
from abc import ABC, abstractmethod
from datetime import date, datetime, time


class TelaAbstrata(ABC):
    """Base das telas: leitura validada (só o FORMATO) e formatação de saída.

    As regras de negócio ficam no model; aqui só garantimos que o texto digitado
    vira o tipo certo (int, float, date, time) antes de ir para o controlador.
    """

    @abstractmethod
    def tela_opcoes(self) -> int:
        pass

    def mostra_mensagem(self, msg: str):
        print(f"\n>> {msg}")

    # ------------------------------------------------------------------ menu
    def _le_opcao(self, titulo: str, itens: dict) -> int:
        print(f"\n======== {titulo} ========")
        for numero, rotulo in itens.items():
            print(f"  {numero} - {rotulo}")
        return self.le_inteiro("Escolha a opção: ", list(itens))

    # ---------------------------------------------------------------- leitura
    def le_texto(self, mensagem: str) -> str:
        while True:
            valor = input(mensagem).strip()
            if valor:
                return valor
            print("   Campo obrigatório. Tente novamente.")

    def le_inteiro(self, mensagem: str, validos: list = None) -> int:
        while True:
            texto = input(mensagem).strip()
            try:
                valor = int(texto)
            except ValueError:
                print("   Digite um número inteiro.")
                continue
            if validos is not None and valor not in validos:
                print(f"   Opção inválida. Valores aceitos: {', '.join(map(str, validos))}.")
                continue
            return valor

    def le_decimal(self, mensagem: str) -> float:
        while True:
            texto = input(mensagem).strip().replace("R$", "").strip()
            if "," in texto:  # aceita 1.234,50 / 1234,50 / 1234.50
                texto = texto.replace(".", "").replace(",", ".")
            try:
                valor = float(texto)
            except ValueError:
                print("   Digite um valor numérico (ex.: 150,00).")
                continue
            if not math.isfinite(valor):
                print("   Valor inválido.")
                continue
            return valor

    def le_data(self, mensagem: str) -> date:
        while True:
            texto = input(mensagem + " (dd/mm/aaaa): ").strip()
            try:
                return datetime.strptime(texto, "%d/%m/%Y").date()
            except ValueError:
                print("   Data inválida. Use o formato dd/mm/aaaa.")

    def le_horario(self, mensagem: str) -> time:
        while True:
            texto = input(mensagem + " (hh:mm): ").strip()
            try:
                return datetime.strptime(texto, "%H:%M").time()
            except ValueError:
                print("   Horário inválido. Use o formato hh:mm.")

    # ------------------------------------------------------------- formatação
    def fmt_data(self, valor: date) -> str:
        return valor.strftime("%d/%m/%Y")

    def fmt_hora(self, valor: time) -> str:
        return valor.strftime("%H:%M")

    def fmt_moeda(self, valor: float) -> str:
        texto = f"{valor:,.2f}"
        return "R$ " + texto.replace(",", "X").replace(".", ",").replace("X", ".")

    def fmt_cpf(self, cpf: str) -> str:
        if len(cpf) == 11 and cpf.isdigit():
            return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
        return cpf

    def fmt_celular(self, celular: str) -> str:
        if celular.isdigit() and len(celular) == 11:
            return f"({celular[:2]}) {celular[2:7]}-{celular[7:]}"
        if celular.isdigit() and len(celular) == 10:
            return f"({celular[:2]}) {celular[2:6]}-{celular[6:]}"
        return celular
