import random
import pygame
from settings import chunks_vertical, chunks_horizontal, chunk_size, tile_size

# Inicialización de Pygame
pygame.init()

# Diccionario de tipos de chunks con imágenes cargadas y escaladas
chunk_types = {
    "pueblo": pygame.image.load('./imagenes/grasspueblo.jpg').convert_alpha(),
    "pradera": pygame.image.load('./imagenes/praderabonita.jpg').convert_alpha(),
    "desierto": pygame.image.load('./imagenes/desiertopixel.jpg').convert_alpha(),
    "volcan": pygame.image.load('./imagenes/lava.jpg').convert_alpha()
}

# Escalar imágenes a tamaño de un chunk completo
chunk_pixel_size = chunk_size * tile_size  # Asegúrate de que estas variables están definidas apropiadamente
for key in chunk_types:
    chunk_types[key] = pygame.transform.scale(chunk_types[key], (chunk_pixel_size, chunk_pixel_size))

def valid_position(map_colors, x, y, chunk_type):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    count = {key: 0 for key in chunk_types.keys()}  # Inicializa el contador para cada tipo de chunk

    # Recorre todas las direcciones para contar los chunks adyacentes
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < chunks_horizontal and 0 <= ny < chunks_vertical and map_colors[ny][nx] is not None:
            adjacent_img = map_colors[ny][nx]
            for type_key, img in chunk_types.items():
                if adjacent_img == img:
                    count[type_key] += 1

    # Condiciones de validación adaptadas a la lógica original
    if chunk_type == "pueblo":
        if count["pueblo"] > 0:
            return False
        min_separation = 6
        for j in range(-min_separation, min_separation + 1):
            for i in range(-min_separation, min_separation + 1):
                nx, ny = x + i, y + j
                if 0 <= nx < chunks_horizontal and 0 <= ny < chunks_vertical:
                    if map_colors[ny][nx] == chunk_types["pueblo"]:
                        return False
        return True
    elif chunk_type == "pradera":
        return count["pradera"] > 0
    elif chunk_type == "desierto":
        return count["desierto"] < 3
    elif chunk_type == "volcan":
        if count["pueblo"] > 0 or count["volcan"] > 0:
            return False
        return True
    return True

def create_initial_map():
    map_colors = [[None for _ in range(chunks_horizontal)] for _ in range(chunks_vertical)]

    # Asignar imágenes válidas a cada posición
    for y in range(chunks_vertical):
        for x in range(chunks_horizontal):
            possible_chunks = list(chunk_types.keys())
            random.shuffle(possible_chunks)
            for chunk_type in possible_chunks:
                if valid_position(map_colors, x, y, chunk_type):
                    map_colors[y][x] = chunk_types[chunk_type]
                    break
            if map_colors[y][x] is None:
                map_colors[y][x] = random.choice(list(chunk_types.values()))

    return map_colors
