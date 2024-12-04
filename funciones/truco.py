import random
from funciones.valores import *
from funciones.envido import *
from funciones.mazo import *

# Función para manejar el turno del jugador.
def turno_jugador(cartas: list[tuple[int, str]], envido_cantado: bool, truco_cantado: bool) -> tuple[str, bool, bool]:
    print("\n--- Tu turno ---")
    print("Tus cartas:", ", ".join([f"{c[0]} de {c[1]}" for c in cartas]))
    print("¿Qué deseas hacer?")
    print("1. Jugar carta")
    print("2. Cantar Envido")
    print("3. Cantar Truco")
    print("4. Irse al mazo")

    opcion = input("Elige una opción (1-4): ")

    if opcion == "2":
        print("Has cantado Envido.")
        return "Envido", True, truco_cantado
    elif opcion == "3":
        print("Has cantado Truco.")
        return "Truco", envido_cantado, True
    elif opcion == "4":
        print("Te has ido al mazo.")
        return "Mazo", envido_cantado, truco_cantado
    return "Carta", envido_cantado, truco_cantado

# Función para manejar el turno del rival.
def turno_rival(cartas: list[tuple[int, str]], envido_cantado: bool, truco_cantado: bool) -> tuple[str, bool, bool]:
    print("\n--- Turno del rival ---")
    decision = random.choice(["Envido", "Truco", "Carta", "Mazo"])

    if decision == "Envido" and not envido_cantado:
        print("El rival ha cantado Envido.")
        return "Envido", True, truco_cantado
    elif decision == "Truco" and not truco_cantado:
        print("El rival ha cantado Truco.")
        return "Truco", envido_cantado, True
    elif decision == "Carta":
        print("El rival ha jugado una carta.")
        return "Carta", envido_cantado, truco_cantado
    print("El rival se ha ido al mazo.")
    return "Mazo", envido_cantado, truco_cantado

def manejar_envido(cartas_jugador: List[Carta], cartas_rival: List[Carta], es_jugador_quien_canta: bool) -> int:
    puntos_jugador = calcular_envido(cartas_jugador)
    puntos_rival = calcular_envido(cartas_rival)

    print(f"\nTu envido: {puntos_jugador}")
    if es_jugador_quien_canta:  # Si el jugador canta Envido.
        # El rival elige aleatoriamente entre aceptar, rechazar o subir.
        decision_rival = random.choice(["A", "R", "S"])

        if decision_rival == "A":
            print(f"El rival ha aceptado el Envido.")
            print(f"Envido del rival: {puntos_rival}")
            if puntos_jugador > puntos_rival:
                print("¡Has ganado el Envido!")
                return 2  # El jugador gana el Envido.
            elif puntos_jugador < puntos_rival:
                print("El rival ha ganado el Envido.")
                return 0  # El rival gana el Envido.
            else:
                print("Empate en el Envido.")
                return 1  # Empate
        elif decision_rival == "R":
            print("El rival ha rechazado el Envido. Ganas 1 punto.")
            return 1  # El jugador gana 1 punto.
        elif decision_rival == "S":
            # El rival sube el Envido a Real Envido o Falta Envido.
            tipo_envido = random.choice(["R", "F"])
            if tipo_envido == "R":
                print("El rival ha subido a Real Envido.")
                respuesta_jugador = input("¿Aceptar el Real Envido? (A/R): ").strip().lower()
                if respuesta_jugador == "a":
                    print("Has aceptado el Real Envido.")
                    return 3  # Real Envido
                else:
                    print("Has rechazado el Real Envido. El rival gana 2 puntos.")
                    return 0  # El rival gana 2 puntos
            elif tipo_envido == "F":
                print("El rival ha subido a Falta Envido.")
                respuesta_jugador = input("¿Aceptar el Falta Envido? (A/R): ").strip().lower()
                if respuesta_jugador == "a":
                    print("Has aceptado el Falta Envido.")
                    return 4  # Falta Envido
                else:
                    print("Has rechazado el Falta Envido. El rival gana 2 puntos.")
                    return 0  # El rival gana 2 puntos
    else:  # Si el rival canta Envido.
        decision_jugador = random.choice(["A", "R", "S"])

        if decision_jugador == "A":
            print(f"Tu envido: {puntos_jugador}")
            if puntos_jugador > puntos_rival:
                print("¡Has ganado el Envido!")
                return 2  # El jugador gana el Envido
            elif puntos_jugador < puntos_rival:
                print("El rival ha ganado el Envido.")
                return 0  # El rival gana el Envido
            else:
                print("Empate en el Envido.")
                return 1  # Empate
        elif decision_jugador == "R":
            print("Has rechazado el Envido. El rival gana 1 punto.")
            return 1  # El jugador gana 1 punto, no el rival
        elif decision_jugador == "S":
            tipo_envido = input("¿Subir el Envido a Real Envido o Falta Envido? (R/F): ").strip().lower()
            if tipo_envido == "r":
                print("Has subido a Real Envido.")
                return 3  # Real Envido
            elif tipo_envido == "f":
                print("Has subido a Falta Envido.")
                return 4  # Falta Envido

# Función para manejar la parte del truco.
def manejar_truco(cartas_jugador: list[tuple[int, str]], cartas_rival: list[tuple[int, str]]) -> int:
    puntuaciones = {"Jugador": 0, "Rival": 0}
    ronda = 1
    while ronda <= 3:
        print(f"\n--- Ronda {ronda} del Truco ---")

        print(f"Tus cartas: {', '.join([f'{c[0]} de {c[1]}' for c in cartas_jugador])}")
        eleccion_jugador = input("¿Qué carta deseas jugar? (1, 2 o 3): ")
        carta_jugador = cartas_jugador.pop(int(eleccion_jugador) - 1)
        carta_rival = cartas_rival.pop(random.randint(0, len(cartas_rival) - 1))

        print(f"Has jugado: {carta_jugador[0]} de {carta_jugador[1]}")
        print(f"El rival juega: {carta_rival[0]} de {carta_rival[1]}")

        valor_jugador = (carta_jugador[0], carta_jugador[1].capitalize())
        valor_rival = (carta_rival[0], carta_rival[1].capitalize())

        if VALORES_MAZO[valor_jugador] > VALORES_MAZO[valor_rival]:
            puntuaciones["Jugador"] += 1
            print("¡Has ganado esta ronda!")
        else:
            puntuaciones["Rival"] += 1
            print("El rival ha ganado esta ronda.")

        ronda += 1

    if puntuaciones["Jugador"] > puntuaciones["Rival"]:
        print("¡Has ganado el Truco!")
        return 2
    else:
        print("El rival ha ganado el Truco.")
        return 0

# Función principal para jugar al truco.
def jugar_truco(nombre_jugador: str, puntos_objetivo: int) -> None:
    puntos_jugador = 0
    puntos_rival = 0
    turno_jugador_actual = True

    while puntos_jugador < puntos_objetivo and puntos_rival < puntos_objetivo:
        cartas_jugador, cartas_rival = repartir_cartas()

        envido_cantado = False
        truco_cantado = False

        while True:
            if turno_jugador_actual:
                accion_jugador, envido_cantado, truco_cantado = turno_jugador(cartas_jugador, envido_cantado, truco_cantado)
                if accion_jugador == "Mazo":
                    break
            else:
                accion_rival, envido_cantado, truco_cantado = turno_rival(cartas_rival, envido_cantado, truco_cantado)
                if accion_rival == "Mazo":
                    break

            if accion_jugador == "Carta":
                resultado_truco = manejar_truco(cartas_jugador, cartas_rival)
                if resultado_truco == 2:
                    puntos_jugador += 1
                elif resultado_truco == 0:
                    puntos_rival += 1

            # Verificar si alguien ha alcanzado el puntaje objetivo.
            if puntos_jugador >= puntos_objetivo:
                print(f"\n¡Felicidades, {nombre_jugador}! Has ganado el juego con {puntos_jugador} puntos.")
                break

            if puntos_rival >= puntos_objetivo:
                print(f"\nEl rival ha ganado el juego con {puntos_rival} puntos.")
                break

    # Imprimir los puntos finales si el juego ha terminado.
    if puntos_jugador >= puntos_objetivo:
        print(f"El juego ha terminado. {nombre_jugador} ha ganado con {puntos_jugador} puntos.")
    else:
        print("El juego ha terminado. El rival ha ganado.")