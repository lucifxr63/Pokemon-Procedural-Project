import pygame
import sys
import random

from settings import width, height, screen, WHITE, BLACK,player_x,player_y, player_size, velocity, player_image,chunk_size,tile_size,chunk_pixel_size,chunks_horizontal,chunks_vertical,map_width,map_height
from map_generador import create_initial_map,chunk_types,valid_position

# Inicialización de Pygame
pygame.init()
# se crea el mapa inicial 
game_map = create_initial_map()

# Desplazamientos del mapa
horizontal_offset = 0
vertical_offset = 0

def draw_map(horizontal_offset, vertical_offset):
    # Dibujar los tiles con colores de gradientes
    for y in range(len(game_map)):
        for x in range(len(game_map[y])):
            rect = pygame.Rect(x * tile_size - horizontal_offset, y * tile_size - vertical_offset, tile_size, tile_size)
            pygame.draw.rect(screen, game_map[y][x], rect)
    
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

    # Dibujar líneas finas de separación de tiles dentro de cada chunk
    for x in range(0, chunks_horizontal * chunk_pixel_width, tile_size):
        adjusted_x = x - horizontal_offset
        if 0 <= adjusted_x <= width:
            pygame.draw.line(screen, BLACK, (adjusted_x, 0), (adjusted_x, height))

    for y in range(0, chunks_vertical * chunk_pixel_width, tile_size):
        adjusted_y = y - vertical_offset
        if 0 <= adjusted_y <= height:
            pygame.draw.line(screen, BLACK, (0, adjusted_y), (width, adjusted_y))


def expand_map_if_needed():
    global game_map, chunks_horizontal, chunks_vertical, horizontal_offset, vertical_offset
    player_chunk_x = (player_x + horizontal_offset) // tile_size // chunk_size
    player_chunk_y = (player_y + vertical_offset) // tile_size // chunk_size

    # Expandir hacia la derecha si es necesario
    if player_chunk_x >= chunks_horizontal - 1:
        # Agregar una nueva columna de chunks al final
        for row in game_map:
            row.extend([random.choice(list(chunk_types.values())) for _ in range(chunk_size)])
        chunks_horizontal += 1

    # Expandir hacia abajo si es necesario
    if player_chunk_y >= chunks_vertical - 1:
        # Agregar una nueva fila de chunks al final
        new_row = [[random.choice(list(chunk_types.values())) for _ in range(chunks_horizontal * chunk_size)] for _ in range(chunk_size)]
        game_map.extend(new_row)
        chunks_vertical += 1


def add_tiles(direction):
    global game_map, chunks_horizontal, chunks_vertical, horizontal_offset, vertical_offset
    new_chunks = []
    
    # Función para agregar un nuevo chunk respetando las reglas
    def add_new_chunk(x, y):
        # Elegir un tipo de chunk válido
        while True:
            chosen_type = random.choice(list(chunk_types.keys()))
            if valid_position(game_map, x, y, chosen_type):
                return chunk_types[chosen_type]
    
    if direction == 'right':
        # Agregar columnas a la derecha
        for _ in range(chunk_size):
            for row_index, row in enumerate(game_map):
                new_color = add_new_chunk(len(row), row_index // chunk_size)
                row.append(new_color)
            chunks_horizontal += 1
        
        
    elif direction == 'left':
        # Agregar columnas a la izquierda
        horizontal_offset += chunk_pixel_size  # Ajuste para mantener el punto de vista
        for _ in range(chunk_size):
            for row_index, row in enumerate(game_map):
                new_color = add_new_chunk(0, row_index // chunk_size)
                row.insert(0, new_color)
            chunks_horizontal += 1
        
    elif direction == 'up':
        # Agregar filas arriba
        vertical_offset += chunk_pixel_size  # Ajuste para mantener el punto de vista
        for _ in range(chunk_size):
            new_row = [add_new_chunk(col_index, 0) for col_index in range(len(game_map[0]))]
            game_map.insert(0, new_row)
        chunks_vertical += 1
        
    elif direction == 'down':
        # Agregar filas abajo
        for _ in range(chunk_size):
            new_row = [add_new_chunk(col_index, len(game_map)) for col_index in range(len(game_map[0]))]
            game_map.append(new_row)
        chunks_vertical += 1
# Bucle principal del juego
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    old_x, old_y = player_x, player_y  # Guardar la posición antigua para revertir si es necesario

    keys = pygame.key.get_pressed()
    player_x += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * velocity
    player_y += (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * velocity

    # Mantener al jugador dentro de los límites del mapa
    player_x = max(0, min(player_x, width - player_size))
    player_y = max(0, min(player_y, height - player_size))

    # Ajustar los desplazamientos solo dentro de los límites efectivos del mapa
    if player_x == width - player_size and horizontal_offset < map_width - width:
        horizontal_offset += velocity
    elif player_x == 0 and horizontal_offset > 0:
        horizontal_offset -= velocity

    if player_y == height - player_size and vertical_offset < map_height - height:
        vertical_offset += velocity
    elif player_y == 0 and vertical_offset > 0:
        vertical_offset -= velocity

    screen.fill(WHITE)
    draw_map(horizontal_offset, vertical_offset)
    screen.blit(player_image, (player_x, player_y))
    pygame.display.flip()

pygame.quit()
sys.exit()
