import pygame
import sys
import random
import pickle
from settings import width, height, screen, WHITE, player_x, player_y, player_size, velocity, player_image, chunk_size, tile_size, chunk_pixel_size, chunks_horizontal, chunks_vertical, map_width, map_height, bush_image, bush_fuego_image, bush_desierto_image, pueblo_image, chunk_types
from map_generador import create_initial_map, valid_position
from game_menu import show_menu

# Inicialización de Pygame
pygame.init()

# Variable de estado inicial
state = 'inicio'

# Variables globales para el mapa y el desplazamiento
game_map = None
horizontal_offset = 0
vertical_offset = 0

def serialize_map(game_map):
    chunk_type_to_path = {v: k for k, v in chunk_types.items()}
    bush_image_to_path = {
        bush_image: 'bush_image',
        bush_fuego_image: 'bush_fuego_image',
        bush_desierto_image: 'bush_desierto_image',
        pueblo_image: 'pueblo_image',
    }
    
    serialized_map = []
    for row in game_map:
        serialized_row = []
        for tile, decoration in row:
            tile_key = chunk_type_to_path.get(tile, None)
            decoration_key = bush_image_to_path.get(decoration, None)
            serialized_row.append((tile_key, decoration_key))
        serialized_map.append(serialized_row)
    print("Mapa serializado:", serialized_map)
    return serialized_map

def deserialize_map(serialized_map):
    deserialized_map = []
    for row in serialized_map:
        deserialized_row = []
        for tile_type, decoration_key in row:
            tile = chunk_types.get(tile_type, None)
            decoration = None
            if decoration_key == 'bush_image':
                decoration = bush_image
            elif decoration_key == 'bush_fuego_image':
                decoration = bush_fuego_image
            elif decoration_key == 'bush_desierto_image':
                decoration = bush_desierto_image
            elif decoration_key == 'pueblo_image':
                decoration = pueblo_image
            deserialized_row.append([tile, decoration])
        deserialized_map.append(deserialized_row)
    print("Mapa deserializado:", deserialized_map)
    return deserialized_map

def save_map(game_map):
    serialized_map = serialize_map(game_map)
    with open('saved_map.pkl', 'wb') as f:
        pickle.dump(serialized_map, f)
    print("Mapa guardado con éxito.")

def load_map():
    global game_map
    with open('saved_map.pkl', 'rb') as f:
        serialized_map = pickle.load(f)
    game_map = deserialize_map(serialized_map)
    print("Mapa cargado con éxito. Tamaño del mapa:", len(game_map), "x", len(game_map[0]))

def draw_map(horizontal_offset, vertical_offset):
    for y in range(len(game_map)):
        for x in range(len(game_map[y])):
            tile, decoration = game_map[y][x]
            if tile:
                rect = pygame.Rect(x * tile_size - horizontal_offset, y * tile_size - vertical_offset, tile_size, tile_size)
                screen.blit(tile, rect)
            if decoration:
                rect = pygame.Rect(x * tile_size - horizontal_offset, y * tile_size - vertical_offset, tile_size, tile_size)
                screen.blit(decoration, rect)

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
                        row.extend([[chunk_types[new_chunk], None] for _ in range(chunk_size)])
                        break
        chunks_horizontal += 1

    # Expandir hacia abajo si es necesario
    if player_chunk_y >= chunks_vertical - 1:
        for _ in range(chunk_size):
            while True:
                new_row_type = random.choice(list(chunk_types.keys()))
                if valid_position(game_map, len(game_map[0]) // chunk_size, len(game_map) // chunk_size, new_row_type):
                    new_row = [[chunk_types[new_row_type], None] for _ in range(chunks_horizontal * chunk_size)]
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
                        game_map[y + j][x + i] = [chunk_types[chosen_type], None]
                if chosen_type == "pradera":
                    for _ in range(3):
                        while True:
                            tile_x = x + random.randint(0, chunk_size - 1)
                            tile_y = y + random.randint(0, chunk_size - 1)
                            if game_map[tile_y][tile_x][0] == chunk_types["pradera"]:
                                game_map[tile_y][tile_x][1] = bush_image
                                break
                elif chosen_type == "volcan":
                    for _ in range(1):
                        while True:
                            tile_x = x + random.randint(0, chunk_size - 1)
                            tile_y = y + random.randint(0, chunk_size - 1)
                            if game_map[tile_y][tile_x][0] == chunk_types["volcan"]:
                                game_map[tile_y][tile_x][1] = bush_fuego_image
                                break
                elif chosen_type == "desierto":
                    for _ in range(2):
                        while True:
                            tile_x = x + random.randint(0, chunk_size - 1)
                            tile_y = y + random.randint(0, chunk_size - 1)
                            if game_map[tile_y][tile_x][0] == chunk_types["desierto"]:
                                game_map[tile_y][tile_x][1] = bush_desierto_image
                                break
                elif chosen_type == "pueblo":
                    for _ in range(1):
                        while True:
                            tile_x = x + random.randint(0, chunk_size - 1)
                            tile_y = y + random.randint(0, chunk_size - 1)
                            if game_map[tile_y][tile_x][0] == chunk_types["pueblo"]:
                                game_map[tile_y][tile_x][1] = pueblo_image
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
    if state == 'inicio':
        state = show_menu(screen, width, height)
    elif state == 'new_game':
        game_map = create_initial_map()
        print("Mapa generado:", game_map)
        state = 'game'
    elif state == 'load_game':
        load_map()
        print("Mapa cargado:", game_map)
        state = 'game'
    elif state == 'game':
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    save_map(game_map)

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
