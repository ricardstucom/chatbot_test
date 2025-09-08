def llegir_missatge() -> str:
    """Demana l'entrada a l'usuari i la retorna neta."""
    try:
        return input("Tu: ").strip()
    except EOFError:
        return "sortir"
