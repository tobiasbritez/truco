import random

# Esta es una funcion para repartir las cartas a los jugadores.
def repartir_cartas() -> tuple[list[tuple[str, str]], list[tuple[str, str]]]:
    """Reparte tres cartas a cada jugador."""
    valores = ["1", "2", "3", "4", "5", "6", "7", "10", "11", "12"]
    palos = ["espada", "basto", "oro", "copa"]
    mazo = [(valor, palo) for valor in valores for palo in palos]

    random.shuffle(mazo)
    return mazo[:3], mazo[3:6]