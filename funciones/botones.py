import pygame

class Boton:
    def __init__(self, texto, posicion, ancho, alto, color, color_texto, accion=None) -> None:
        self.texto = texto
        self.rect = pygame.Rect(posicion[0], posicion[1], ancho, alto)
        self.color = color
        self.color_texto = color_texto
        self.accion = accion

# Función para verificar si un botón fue clickeado.
def boton_clickeado(posicion, ancho, alto, evento) -> any:
    x, y = evento.pos
    return posicion[0] <= x <= posicion[0] + ancho and posicion[1] <= y <= posicion[1] + alto
    def dibujar(self, pantalla, fuente) -> None:
        pygame.draw.rect(pantalla, self.color, self.rect)
        texto_boton = fuente.render(self.texto, True, self.color_texto)
        texto_x = self.rect.x + (self.rect.width - texto_boton.get_width()) // 2
        texto_y = self.rect.y + (self.rect.height - texto_boton.get_height()) // 2
        pantalla.blit(texto_boton, (texto_x, texto_y))

    def boton_clickeado(self, evento) -> None:
        if evento.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(evento.pos):
            if self.accion:
                self.accion()
