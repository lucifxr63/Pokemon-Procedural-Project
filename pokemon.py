import pygame
import sys
import random

from settings import width, height, screen, WHITE, BLACK, player_x, player_y, player_size, velocity, player_image, chunk_size, tile_size, chunk_pixel_size, chunks_horizontal, chunks_vertical, map_width, map_height
from map_generador import create_initial_map

# Inicialización de Pygame
pygame.init()
# Se crea el mapa inicial
game_map = create_initial_map()

# Desplazamientos del mapa
horizontal_offset = 0
vertical_offset = 0

def draw_map(horizontal_offset, vertical_offset):
    # Dibujar los chunks utilizando las imágenes asignadas
    for y in range(len(game_map)):
        for x in range(len(game_map[y])):
            rect = pygame.Rect(x * tile_size - horizontal_offset, y * tile_size - vertical_offset, tile_size, tile_size)
            screen.blit(game_map[y][x], rect.topleft)
    
    # Dibujar líneas de separación de los chunks más gruesas
    chunk_pixel_width = chunk_size * tile_size
    for x in range(0, chunks_horizontal * chunk_pixel_width, chunk_pixel_width):
        adjusted_x = x - horizontal_offset
        if 0 <= adjusted_x <= width:
            pygame.draw.line(screen, BLACK, (adjusted_x, 0), (adjusted_x, height), 2)

    for y in range(0, chunks_vertical * chunk_pixel_width, chunk_pixel_width):
        adjusted_y = y - vertical_offset
        if 0 <= adjusted_y <= height:
            pygame.draw.line(screen, BLACK, (0, adjusted_y), (width, adjusted_y), 2)

def main_loop():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        player_x += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * velocity
        player_y += (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * velocity

        # Mantener al jugador dentro de los límites del mapa
        player_x = max(0, min(player_x, width - player_size))
        player_y = max(0, min(player_y, height - player_size))

        # Ajustar los desplazamientos solo dentro de los límites efectivos del mapa
        adjust_map_offsets()

        screen.fill(WHITE)
        draw_map(horizontal_offset, vertical_offset)
        screen.blit(player_image, (player_x, player_y))
        pygame.display.flip()

    pygame.quit()
    sys.exit()

def adjust_map_offsets():
    global horizontal_offset, vertical_offset
    if player_x == width - player_size and horizontal_offset < map_width - width:
        horizontal_offset += velocity
    elif player_x == 0 and horizontal_offset > 0:
        horizontal_offset -= velocity

    if player_y == height - player_size and vertical_offset < map_height - height:
        vertical_offset += velocity
    elif player_y == 0 and vertical_offset > 0:
        vertical_offset -= velocity

if __name__ == "__main__":
    main_loop()
