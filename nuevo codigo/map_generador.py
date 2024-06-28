import random
import pygame
from settings import chunks_vertical, chunks_horizontal, chunk_size, tile_size, bush_image, bush_fuego_image, bush_desierto_image, pueblo_image, chunk_types

# Inicialización de Pygame
pygame.init()

def valid_position(map_colors, x, y, chunk_type):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    count = {key: 0 for key in chunk_types.keys()}

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < chunks_horizontal * chunk_size and 0 <= ny < chunks_vertical * chunk_size and map_colors[ny][nx][0] is not None:
            adjacent_img = map_colors[ny][nx][0]
            for type_key, img in chunk_types.items():
                if adjacent_img == img:
                    count[type_key] += 1

    if chunk_type == "pueblo":
        if count["pueblo"] > 0:
            return False
        min_separation = 6
        for j in range(-min_separation, min_separation + 1):
            for i in range(-min_separation, min_separation + 1):
                nx, ny = x + i, y + j
                if 0 <= nx < chunks_horizontal * chunk_size and 0 <= ny < chunks_vertical * chunk_size:
                    if map_colors[ny][nx][0] == chunk_types["pueblo"]:
                        return False
        return True
    elif chunk_type == "pradera":
        return count["pradera"] < 3
    elif chunk_type == "desierto":
        return count["desierto"] == 0
    elif chunk_type == "volcan":
        return count["volcan"] == 0  # No otros volcanes adyacentes
    return True

def add_bushes(map_tiles, chunk_x, chunk_y, chunk_type):
    if chunk_type == "pradera":
        num_bushes = 5
        bush_image_to_use = bush_image
    elif chunk_type == "volcan":
        num_bushes = 3
        bush_image_to_use = bush_fuego_image
    elif chunk_type == "desierto":
        num_bushes = 3
        bush_image_to_use = bush_desierto_image
    elif chunk_type == "pueblo":
        num_bushes = 1
        bush_image_to_use = pueblo_image

    for _ in range(num_bushes):
        while True:
            tile_x = chunk_x * chunk_size + random.randint(0, chunk_size - 1)
            tile_y = chunk_y * chunk_size + random.randint(0, chunk_size - 1)
            if 0 <= tile_x < len(map_tiles[0]) and 0 <= tile_y < len(map_tiles):
                if map_tiles[tile_y][tile_x][0] == chunk_types[chunk_type]:
                    map_tiles[tile_y][tile_x][1] = bush_image_to_use
                    break

def create_initial_map():
    map_tiles = [[(None, None) for _ in range(chunks_horizontal * chunk_size)] for _ in range(chunks_vertical * chunk_size)]
    print("Mapa inicial creado con None:", map_tiles)

    for chunk_y in range(chunks_vertical):
        for chunk_x in range(chunks_horizontal):
            possible_chunks = (["pueblo"] * 1 + ["pradera"] * 10 + ["desierto"] * 2 + ["volcan"] * 1)
            random.shuffle(possible_chunks)
            for chunk_type in possible_chunks:
                if valid_position(map_tiles, chunk_x, chunk_y, chunk_type):
                    for i in range(chunk_size):
                        for j in range(chunk_size):
                            map_tiles[chunk_y * chunk_size + i][chunk_x * chunk_size + j] = [chunk_types[chunk_type], None]
                    if chunk_type in ["pradera", "volcan", "desierto", "pueblo"]:
                        add_bushes(map_tiles, chunk_x, chunk_y, chunk_type)
                    break
            if map_tiles[chunk_y * chunk_size][chunk_x * chunk_size][0] is None:
                chosen_chunk = random.choice(list(chunk_types.values()))
                for i in range(chunk_size):
                    for j in range(chunk_size):
                        map_tiles[chunk_y * chunk_size + i][chunk_x * chunk_size + j] = [chosen_chunk, None]

    print("Mapa inicial con datos:", map_tiles)
    return map_tiles
