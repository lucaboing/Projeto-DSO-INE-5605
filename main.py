from control.controlador_sistema import ControladorSistema

if __name__ == "__main__":
    try:
        ControladorSistema().inicializa_sistema()
    except (KeyboardInterrupt, EOFError):
        print("\nSistema encerrado.")
