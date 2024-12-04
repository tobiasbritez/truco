from typing import List, Tuple

Carta = Tuple[int, str]

def calcular_envido(cartas: List[Carta]) -> int:
    palos = {}
    for valor, palo in cartas:
        valor = int(valor)
        if palo not in palos:
            palos[palo] = []
        palos[palo].append(valor if valor < 10 else 0)

    max_envido = 0
    for valores in palos.values():
        if len(valores) > 1:
            valores.sort(reverse=True)
            max_envido = max(max_envido, sum(valores[:2]) + 20)
        elif valores:
            max_envido = max(max_envido, valores[0])

    return max_envido


def calcular_puntos_falta_envido(puntos_contrincante: int, puntaje_maximo: int = 30) -> int:
    return puntaje_maximo - puntos_contrincante

def determinar_envido(cartas: List[Carta], puntos_contrincante: int) -> dict:
    envido = calcular_envido(cartas)
    falta_envido = calcular_puntos_falta_envido(puntos_contrincante)

    return {
        "Envido": 2,
        "Real Envido": 3,
        "Falta Envido": falta_envido,
        "Puntaje Máximo": envido
    }