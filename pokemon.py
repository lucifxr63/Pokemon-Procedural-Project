import pygame
import sys
import random

from settings import width, height, screen, WHITE, player_x, player_y, player_size, velocity, player_image, chunk_size, tile_size, chunk_pixel_size, chunks_horizontal, chunks_vertical, map_width, map_height, bush_image, bush_fuego_image, bush_desierto_image, pueblo_image
from map_generador import create_initial_map, chunk_types, valid_position

# Inicialización de Pygame
pygame.init()
# Se crea el mapa inicial
game_map = create_initial_map()

# Desplazamientos del mapa
horizontal_offset = 0
vertical_offset = 0

def draw_map(horizontal_offset, vertical_offset):
    for y in range(len(game_map)):
        for x in range(len(game_map[y])):
            img = game_map[y][x]
            rect = pygame.Rect(x * tile_size - horizontal_offset, y * tile_size - vertical_offset, tile_size, tile_size)
            screen.blit(img, rect)

def expand_map_if_needed():
    global game_map, chunks_horizontal, chunks_vertical, horizontal_offset, vertical_offset
    player_chunk_x = (player_x + horizontal_offset) // chunk_pixel_size
    player_chunk_y = (player_y + vertical_offset) // chunk_pixel_size

    # Expandir hacia la derecha si es necesario
    if player_chunk_x >= chunks_horizontal - 1:
        for row in game_map:
            for _ in range(chunk_size):
                while True:
                    new_chunk = random.choice(list(chunk_types.keys()))
                    if valid_position(game_map, len(row) // chunk_size, len(game_map) // chunk_size, new_chunk):
                        row.extend([chunk_types[new_chunk] for _ in range(chunk_size)])
                        break
        chunks_horizontal += 1

    # Expandir hacia abajo si es necesario
    if player_chunk_y >= chunks_vertical - 1:
        for _ in range(chunk_size):
            while True:
                new_row_type = random.choice(list(chunk_types.keys()))
                if valid_position(game_map, len(game_map[0]) // chunk_size, len(game_map) // chunk_size, new_row_type):
                    new_row = [chunk_types[new_row_type] for _ in range(chunks_horizontal * chunk_size)]
                    game_map.extend([new_row])
                    break
        chunks_vertical += 1

def add_tiles(direction):
    global game_map, chunks_horizontal, chunks_vertical, horizontal_offset, vertical_offset
    
    def add_new_chunk(x, y):
        while True:
            chosen_type = random.choice(list(chunk_types.keys()))
            if valid_position(game_map, x // chunk_size, y // chunk_size, chosen_type):
                for i in range(chunk_size):
                    for j in range(chunk_size):
                        game_map[y + j][x + i] = chunk_types[chosen_type]
                if chosen_type == "pradera":
                    for _ in range(3):
                        while True:
                            tile_x = x + random.randint(0, chunk_size - 1)
                            tile_y = y + random.randint(0, chunk_size - 1)
                            if game_map[tile_y][tile_x] == chunk_types["pradera"]:
                                game_map[tile_y][tile_x] = bush_image
                                break
                elif chosen_type == "volcan":
                    for _ in range(1):
                        while True:
                            tile_x = x + random.randint(0, chunk_size - 1)
                            tile_y = y + random.randint(0, chunk_size - 1)
                            if game_map[tile_y][tile_x] == chunk_types["volcan"]:
                                game_map[tile_y][tile_x] = bush_fuego_image
                                break
                elif chosen_type == "desierto":
                    for _ in range(2):
                        while True:
                            tile_x = x + random.randint(0, chunk_size - 1)
                            tile_y = y + random.randint(0, chunk_size - 1)
                            if game_map[tile_y][tile_x] == chunk_types["desierto"]:
                                game_map[tile_y][tile_x] = bush_desierto_image
                                break
                elif chosen_type == "pueblo":
                    for _ in range(1):
                        while True:
                            tile_x = x + random.randint(0, chunk_size - 1)
                            tile_y = y + random.randint(0, chunk_size - 1)
                            if game_map[tile_y][tile_x] == chunk_types["pueblo"]:
                                game_map[tile_y][tile_x] = pueblo_image
                                break
                break

    if direction == 'right':
        for _ in range(chunk_size):
            for row_index, row in enumerate(game_map):
                new_chunk_x = len(row) // tile_size
                add_new_chunk(new_chunk_x * chunk_size, row_index)
        chunks_horizontal += 1
        
    elif direction == 'left':
        horizontal_offset += chunk_pixel_size
        for _ in range(chunk_size):
            for row_index, row in enumerate(game_map):
                add_new_chunk(0, row_index)
        chunks_horizontal += 1
        
    elif direction == 'up':
        vertical_offset += chunk_pixel_size
        for _ in range(chunk_size):
            new_row = [add_new_chunk(col_index, 0) for col_index in range(len(game_map[0]) // chunk_size)]
            game_map.insert(0, new_row)
        chunks_vertical += 1
        
    elif direction == 'down':
        for _ in range(chunk_size):
            new_row = [add_new_chunk(col_index, len(game_map) // chunk_size) for col_index in range(len(game_map[0]) // chunk_size)]
            game_map.append(new_row)
        chunks_vertical += 1

# Bucle principal del juego
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    player_x += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * velocity
    player_y += (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * velocity

    player_x = max(0, min(player_x, width - player_size))
    player_y = max(0, min(player_y, height - player_size))

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
