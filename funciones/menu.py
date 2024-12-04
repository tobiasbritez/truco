import pygame
import os
from funciones.mazo import *
from funciones.envido import *
from funciones.truco import *
from funciones.botones import *
from funciones.puntajes import *
from funciones.musica import *

# Inicializar pygame
pygame.init()

# Aca se encuentra el repertorio de la pantalla.
ANCHO = 900
ALTO = 700
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Truco Argentino")

# En esta parte se encuentra las el iconop y las imagenes del juego del truco.
icono = pygame.image.load("cartas/imagen.truco.jpg")
pygame.display.set_icon(icono)
fondo_img = pygame.image.load("cartas/fondo-de-messi-4k-v0-msgusjg63l7a1.jpg")
fondo_img = pygame.transform.scale(fondo_img, (ANCHO, ALTO))
dorso_img = pygame.image.load("cartas/dorso.jpg")
mazo_img = pygame.image.load("cartas/mazo.jpg")

# El tamaño de la carta y imagen .
ANCHO_CARTA = 100
ALTO_CARTA = 130
dorso_img = pygame.transform.scale(dorso_img, (ANCHO_CARTA, ALTO_CARTA))
mazo_img = pygame.transform.scale(mazo_img, (ANCHO_CARTA, ALTO_CARTA))

# La fuente del texto.
fuente = pygame.font.Font(None, 36)

# Los colores.
COLOR_BOTON = (22, 51, 224)
COLOR_TEXTO = (255, 255, 255)

# Turno inicial (True para jugador, False para rival).
turno_jugador = True

# Velocidad de animación (mayor valor = más lenta).
TIEMPO_ANIMACION = 10

# Función para cargar imágenes de cartas.
def cargar_imagen_carta(cartas) -> any:
    valor, palo = cartas
    nombre_archivo = f"{valor} {palo}.jpg".lower()
    ruta = os.path.join("cartas", nombre_archivo)
    try:
        imagen = pygame.image.load(ruta)
        return pygame.transform.scale(imagen, (ANCHO_CARTA, ALTO_CARTA))
    except FileNotFoundError:
        print(f"Imagen no encontrada: {ruta}")
        return dorso_img  # Usar el dorso como respaldo si no se encuentra la imagen.

# Función para mostrar su respectivo boton.
def dibujar_boton(texto, posicion, ancho, alto):
    pygame.draw.rect(pantalla, COLOR_BOTON, (posicion[0], posicion[1], ancho, alto))
    texto_boton = fuente.render(texto, True, COLOR_TEXTO)
    texto_x = posicion[0] + (ancho - texto_boton.get_width()) // 2
    texto_y = posicion[1] + (alto - texto_boton.get_height()) // 2
    pantalla.blit(texto_boton, (texto_x, texto_y))
    
# Función para verificar si un botón fue clickeado.
def boton_clickeado(posicion, ancho, alto, evento) -> any:
    x, y = evento.pos
    return posicion[0] <= x <= posicion[0] + ancho and posicion[1] <= y <= posicion[1] + alto

# Función para mostrar las cartas de manera grafica.
def mostrar_cartas(cartas, posicion_central, espacio_entre_cartas, usar_dorso=False) -> None:
    total_ancho = len(cartas) * ANCHO_CARTA + (len(cartas) - 1) * espacio_entre_cartas
    inicio_x = posicion_central[0] - total_ancho // 2
    y = posicion_central[1]
    for i, carta in enumerate(cartas):
        imagen = dorso_img if usar_dorso else cargar_imagen_carta(carta)
        x = inicio_x + i * (ANCHO_CARTA + espacio_entre_cartas)
        pantalla.blit(imagen, (x, y))

# Función para mover carta al centro de la pantalla y agregarla a la mesa.
def mover_carta_al_centro(carta, posicion_final, cartas_jugador, cartas_en_mesa, tiempo=10) -> None:
    indice = cartas_jugador.index(carta)
    x_inicial = ANCHO // 2 - len(cartas_jugador) * (ANCHO_CARTA + 20) // 2 + indice * (ANCHO_CARTA + 20)
    y_inicial = ALTO - 200

    x_final, y_final = posicion_final
    imagen_carta = cargar_imagen_carta(carta)

    for i in range(tiempo):
        pantalla.blit(fondo_img, (0, 0))
        mostrar_cartas(cartas_jugador, (ANCHO // 2, ALTO - 200), 20)
        mostrar_cartas(cartas_en_mesa, (ANCHO // 2, ALTO // 2 - ALTO_CARTA // 2), 20)
        pantalla.blit(mazo_img, (ANCHO - 150, ALTO // 2 - ALTO_CARTA // 2))

        desplazamiento_x = (x_final - x_inicial) / tiempo
        desplazamiento_y = (y_final - y_inicial) / tiempo

        x_actual = x_inicial + i * desplazamiento_x
        y_actual = y_inicial + i * desplazamiento_y
        pantalla.blit(imagen_carta, (x_actual, y_actual))
        pygame.display.update()
        pygame.time.delay(30)

    cartas_en_mesa.append(carta)

def turno_rival(cartas_rival, cartas_en_mesa):
    """El rival selecciona automáticamente la carta a jugar y la mueve a la mesa."""
    if cartas_rival:
        carta = cartas_rival[0]  # Selección simplificada: juega la primera carta.
        posicion_carta_mesa = (
            ANCHO // 2 - len(cartas_en_mesa) * (ANCHO_CARTA + 20) // 2 + len(cartas_en_mesa) * (ANCHO_CARTA + 20),
            ALTO // 2 - ALTO_CARTA // 2,
        )
        # Mover la carta seleccionada al centro y agregarla a la mesa.
        posicion_carta_mesa = (ANCHO // 2 - ANCHO_CARTA // 2, ALTO // 2 - ALTO_CARTA // 2)
        mover_carta_al_centro(carta, posicion_carta_mesa, cartas_rival, cartas_en_mesa, tiempo=20)

# Función principal para mostrar todo el juego.
def mostrar_menu_() -> None:
    cartas_jugador, cartas_rival = repartir_cartas()
    puntos_jugador = 0
    puntos_rival = 0
    cartas_en_mesa = []
    truco_cantado = False
    envido_cantado = False
    turno_jugador = True

    while True:
        pantalla.blit(fondo_img, (0, 0))
        mostrar_cartas(cartas_jugador, (ANCHO // 2, ALTO - 200), 20)
        mostrar_cartas(cartas_rival, (ANCHO // 2, 50), 20, usar_dorso=True)
        mostrar_cartas(cartas_en_mesa, (ANCHO // 2, ALTO // 2 - ALTO_CARTA // 2), 20)
        pantalla.blit(mazo_img, (ANCHO - 150, ALTO // 2 - ALTO_CARTA // 2))

        texto_puntos = fuente.render(f"Jugador: {puntos_jugador}  Rival: {puntos_rival}", True, (255, 255, 255))
        pantalla.blit(texto_puntos, (10, 10))

        # Dimensiones de los botones.
        boton_ancho = 100
        boton_alto = 45
        espacio_vertical = 20  # Espacio entre botones.

        # Coordenadas para centrar los botones.
        total_ancho = (3 * boton_ancho) + (2 * espacio_vertical)  # Ancho total de los botones con espacios.
        x_inicio = (ANCHO - total_ancho) // 2  # Posición inicial para centrar vertical.
        y_posicion = ALTO - boton_alto - 20  # Posición vertical (20 píxeles).

        # Dibujar botones alineados verticalmente.
        dibujar_boton("Envido", (x_inicio, y_posicion), boton_ancho, boton_alto)
        dibujar_boton("Truco", (x_inicio + boton_ancho + espacio_vertical, y_posicion), boton_ancho, boton_alto)
        dibujar_boton("Mazo", (x_inicio + 2 * (boton_ancho + espacio_vertical), y_posicion), boton_ancho, boton_alto)

        pygame.display.update()

        # Turno del rival si no es turno del jugador.
        if not turno_jugador and cartas_rival:
            pygame.time.delay(500)  # Pausa para que la acción sea visible.
            turno_rival(cartas_rival, cartas_en_mesa)
            turno_jugador = True  # Cambia al turno del jugador.
    
        # Aca se muestra el manejo de eventos.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        
        if event.type == pygame.MOUSEBUTTONDOWN:
        # Manejo de clic en botones.
            if boton_clickeado((x_inicio, y_posicion), boton_ancho, boton_alto, event):  # Envido
                if not envido_cantado:
                    print("¡Se cantó Envido!")
                    resultado_envido = manejar_envido(cartas_jugador, cartas_rival, puntos_jugador, puntos_rival)
                    puntos_jugador += resultado_envido[0]
                    puntos_rival += resultado_envido[1]
                    envido_cantado = True

            if boton_clickeado((x_inicio + boton_ancho + espacio_vertical, y_posicion), boton_ancho, boton_alto, event):
                if not truco_cantado:
                    print("¡Se cantó Truco!")
                    resultado_truco = manejar_truco(cartas_jugador, cartas_rival)
                    if resultado_truco == 2:
                        puntos_jugador += 2
                    elif resultado_truco == 0:
                        puntos_rival += 2
                    truco_cantado = True
            
        # Detectar si el usuario hizo clic en el botón "Mazo".
            if boton_clickeado((x_inicio + 2 * (boton_ancho + espacio_vertical), y_posicion), boton_ancho, boton_alto, event):
                print("Se terminó la ronda y vamos al mazo.")
                cartas_jugador, cartas_rival = repartir_cartas()  # Repartir nuevas cartas.
                cartas_en_mesa.clear()  # Limpiar las cartas en la mesa.
                # Guardar puntajes en el archivo CSV al final de cada ronda.
                guardar_puntajes("Jugador", puntos_jugador)
                guardar_puntajes("Rival", puntos_rival)
                break  # Termina la ronda actual y empieza una nueva.

        # Manejo de clic en cartas.    
            for i, carta in enumerate(cartas_jugador):
                carta_rect = pygame.Rect(ANCHO // 2 - len(cartas_jugador) * (ANCHO_CARTA + 20) // 2 + i * (ANCHO_CARTA + 20), ALTO - 200, ANCHO_CARTA, ALTO_CARTA)
                if carta_rect.collidepoint(event.pos):
                    posicion_carta_mesa = (ANCHO // 2 - len(cartas_en_mesa) * (ANCHO_CARTA + 20) // 2 + len(cartas_en_mesa) * (ANCHO_CARTA + 20), ALTO // 2 - ALTO_CARTA // 2)
                    mover_carta_al_centro(carta, posicion_carta_mesa, cartas_jugador, cartas_en_mesa)
                    cartas_jugador.remove(carta)

        # Clic en cartas del jugador.
            for i, carta in enumerate(cartas_jugador):
                carta_rect = pygame.Rect(
                    ANCHO // 2 - len(cartas_jugador) * (ANCHO_CARTA + 20) // 2 + i * (ANCHO_CARTA + 20),
                    ALTO - 200,
                    ANCHO_CARTA,
                    ALTO_CARTA,
                )
                if carta_rect.collidepoint(event.pos):
                    if turno_jugador:
                        posicion_carta_mesa = (
                            ANCHO // 2 - len(cartas_en_mesa) * (ANCHO_CARTA + 20) // 2 + len(cartas_en_mesa) * (ANCHO_CARTA + 20),
                            ALTO // 2 - ALTO_CARTA // 2,
                        )
                        posicion_carta_mesa = (ANCHO // 2 - ANCHO_CARTA // 2, ALTO // 2 - ALTO_CARTA // 2)
                        mover_carta_al_centro(carta, posicion_carta_mesa, cartas_jugador, cartas_en_mesa)
                        cartas_jugador.remove(carta)
                        turno = "rival" # Cambia el turno al rival


    if len(cartas_en_mesa) == 6:  # Si ya se han jugado las 6 cartas, termina la ronda.
            print("Se terminó la ronda, vamos al mazo.")
            cartas_jugador, cartas_rival = repartir_cartas()  # Repartir nuevas cartas.
            cartas_en_mesa.clear()  # Limpiar las cartas en la mesa.

        # Guardar puntajes en el archivo CSV al final de cada ronda.
            guardar_puntajes("Jugador", puntos_jugador)
            guardar_puntajes("Rival", puntos_rival)

def manejar_envido(cartas_jugador, cartas_rival, puntos_jugador, puntos_rival):
    """Maneja las modalidades del Envido: Envido, Real Envido y Falta Envido."""
    puntos_envido_jugador = calcular_envido(cartas_jugador)
    puntos_envido_rival = calcular_envido(cartas_rival)

    print(f"Jugador: {puntos_envido_jugador} puntos de Envido.")
    print(f"Rival: {puntos_envido_rival} puntos de Envido.")

    # Base de puntos para Envido.
    puntos_base = 2
    puntos_extra = 0
    falta = 30 - max(puntos_jugador, puntos_rival)  # Puntos necesarios para ganar por Falta Envido.

    modalidad_envido = "Envido"

    # Mostrar opciones de respuesta.
    opciones = ["Aceptar", "Real Envido", "Falta Envido", "No Quiero"]
    seleccion = seleccionar_opcion("¿Qué quieres hacer?", opciones)

    if seleccion == "Aceptar":
        puntos_extra = puntos_base
        print(f"Ganaste {puntos_extra} puntos por Envido.")
    elif seleccion == "Real Envido":
        modalidad_envido = "Real Envido"
        puntos_base += 3
        print("¡Cantaste Real Envido!")
        seleccion_rival = respuesta_rival()
        if seleccion_rival == "No Quiero":
            print("El rival no quiso el Real Envido. Ganas 3 puntos.")
            return puntos_base, 0
        else:
            print("El rival aceptó el Real Envido.")
            puntos_extra = puntos_base
    elif seleccion == "Falta Envido":
        modalidad_envido = "Falta Envido"
        puntos_base = falta
        print("¡Cantaste Falta Envido!")
        seleccion_rival = respuesta_rival()
        if seleccion_rival == "No Quiero":
            print(f"El rival no quiso la Falta Envido. Ganas {puntos_base // 2} puntos.")
            return puntos_base // 2, 0
        else:
            print("El rival aceptó la Falta Envido.")
            puntos_extra = puntos_base
    elif seleccion == "No Quiero":
        print(f"No quisiste el Envido. El rival gana {puntos_base} puntos.")
        return 0, puntos_base

    # Comparar puntos del Envido.
    if puntos_envido_jugador > puntos_envido_rival:
        print(f"Ganaste el {modalidad_envido}.")
        return puntos_extra, 0
    elif puntos_envido_jugador < puntos_envido_rival:
        print(f"El rival ganó el {modalidad_envido}.")
        return 0, puntos_extra
    else:
        print(f"Empate en {modalidad_envido}. Ambos ganan 1 punto.")
        return 1, 1


def respuesta_rival():
    """Simula la respuesta del rival al Envido, Real Envido o Falta Envido."""
    import random

    opciones_rival = ["Aceptar", "No Quiero"]
    if random.random() > 0.7:  # 70% probabilidad de aceptar.
        return "Aceptar"
    else:
        return "No Quiero"


def seleccionar_opcion(pregunta, opciones):
    """
    Muestra las opciones al jugador y permite seleccionar.
    En este caso, simularemos automáticamente para prueba.
    """
    print(pregunta)
    for i, opcion in enumerate(opciones):
        print(f"{i + 1}. {opcion}")

    seleccion = input("Elige una opción: ")
    try:
        seleccion = int(seleccion) - 1
        if 0 <= seleccion < len(opciones):
            return opciones[seleccion]
    except ValueError:
        pass
    return "Aceptar"  # Por defecto, aceptar.