import pygame
import sys
import random

from settings import width, height, screen, WHITE, BLACK,player_x,player_y, player_size, velocity, player_image,chunk_size,tile_size,chunk_pixel_size,chunks_horizontal,chunks_vertical
from map_generador import create_initial_map,chunk_types,is_valid_position

# Inicialización de Pygame
pygame.init()
# se crea el mapa inicial 
game_map = create_initial_map()

# Desplazamientos del mapa
horizontal_offset = 0
vertical_offset = 0

def draw_map(horizontal_offset, vertical_offset):
    for y in range(len(game_map)):
        for x in range(len(game_map[y])):
            rect = pygame.Rect(x * tile_size - horizontal_offset, y * tile_size - vertical_offset, tile_size, tile_size)
            pygame.draw.rect(screen, game_map[y][x], rect)
    # Dibuja líneas de separación de los chunks
    for y in range(0, len(game_map) * tile_size, chunk_pixel_size):
        pygame.draw.line(screen, BLACK, (0, y - vertical_offset), (width, y - vertical_offset))
    for x in range(0, len(game_map[0]) * tile_size, chunk_pixel_size):
        pygame.draw.line(screen, BLACK, (x - horizontal_offset, 0), (x - horizontal_offset, height))

def add_tiles(direction):
    global game_map, chunks_horizontal, chunks_vertical, horizontal_offset, vertical_offset
    new_chunks = []
    
    # Función para agregar un nuevo chunk respetando las reglas
    def add_new_chunk(x, y):
        # Elegir un tipo de chunk válido
        while True:
            chosen_type = random.choice(list(chunk_types.keys()))
            if is_valid_position(game_map, x, y, chosen_type):
                return chunk_types[chosen_type]
    
    if direction == 'right':
        # Agregar columnas a la derecha
        for _ in range(chunk_size):
            for row_index, row in enumerate(game_map):
                new_color = add_new_chunk(len(row), row_index // chunk_size)
                row.append(new_color)
        
        
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

    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        player_x += velocity
        if player_x > width - width // 4:
            player_x = width - width // 4
            horizontal_offset += velocity
            if horizontal_offset > (chunks_horizontal * chunk_pixel_size) - width:
                add_tiles('right')

    if keys[pygame.K_LEFT]:
        player_x -= velocity
        if player_x < width // 4:
            player_x = width // 4
            horizontal_offset -= velocity
            if horizontal_offset < 0:
                add_tiles('left')

    if keys[pygame.K_UP]:
        player_y -= velocity
        if player_y < height // 4:
            player_y = height // 4
            vertical_offset -= velocity
            if vertical_offset < 0:
                add_tiles('up')

    if keys[pygame.K_DOWN]:
        player_y += velocity
        if player_y > height - height // 4:
            player_y = height - height // 4
            vertical_offset += velocity
            if vertical_offset > (chunks_vertical * chunk_pixel_size) - height:
                add_tiles('down')

    screen.fill(WHITE)
    draw_map(horizontal_offset, vertical_offset)
    screen.blit(player_image, (player_x, player_y))
    pygame.display.flip()

pygame.quit()
sys.exit()
