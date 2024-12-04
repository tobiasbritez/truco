import pygame
import os
import random

# Inicializar pygame.mixer
pygame.mixer.init()

# Ruta de la carpeta donde están las canciones.
carpeta_musica = "musica"  # Cambia esta ruta a donde estén tus canciones.

# Obtener todas las canciones de la carpeta.
lista_canciones = [os.path.join(carpeta_musica, archivo) for archivo in os.listdir(carpeta_musica) if archivo.endswith(".mp3")]

# Elegir una canción aleatoria.
cancion_actual = random.choice(lista_canciones)

# Cargar y reproducir la canción seleccionada.
pygame.mixer.music.load(cancion_actual)
pygame.mixer.music.set_volume(0.5)  # Ajusta el volumen (0.0 a 1.0).
pygame.mixer.music.play(-1)  # Reproduce en bucle infinito.