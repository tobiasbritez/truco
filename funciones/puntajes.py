import os
import csv


PUNTUAJES_FILE = 'puntajes.csv'

# Función para mostrar el historial de puntajes.
def mostrar_puntajes() -> None:
    if not os.path.exists(PUNTUAJES_FILE):
        print("\nNo hay historial de puntajes.")
        return

    with open(PUNTUAJES_FILE, mode='r', newline='', encoding='utf-8') as archivo:
        lector = csv.reader(archivo)
        print("\nHistorial de Puntajes:")
        print("Jugador, Puntos")
        for fila in lector:
            print(f"{fila[0]}, {fila[1]}")

# Función para guardar los puntajes en el archivo CSV.
def guardar_puntajes(jugador: str, puntos: int) -> None:
    # Asegurarnos de que el archivo exista, si no, lo creamos.
    if not os.path.exists(PUNTUAJES_FILE):
        with open(PUNTUAJES_FILE, mode='w', newline='', encoding='utf-8') as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow(['Jugador', 'Puntos'])  # Encabezado

    # Guardamos el puntaje.
    with open(PUNTUAJES_FILE, mode='a', newline='', encoding='utf-8') as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow([jugador, puntos])