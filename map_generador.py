import random
from settings import chunks_vertical, chunks_horizontal, chunk_size
import pygame

# Añadir esto en el diccionario chunk_types en map_generador.py o en el archivo donde gestiones tus tipos de chunks
chunk_types = {
    "pueblo": (0, 0, 255),   # Azul
    "pradera": (0, 255, 0),  # Verde
    "desierto": (255, 255, 0),  # Amarillo
    "volcan": (255, 0, 0)    # Rojo
}



def get_gradient_color(base_color, variation):
    # Genera un color en el gradiente a partir del color base y una variación dada. """
    r, g, b = base_color
    new_r = max(0, min(255, r + variation))
    new_g = max(0, min(255, g + variation))
    new_b = max(0, min(255, b + variation))
    return (new_r, new_g, new_b)


def valid_position(map_colors, x, y, chunk_type):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    count = {key: 0 for key in chunk_types.keys()}  # Inicializa el contador para cada tipo de chunk

    # Recorre todas las direcciones para contar los chunks adyacentes
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < chunks_horizontal and 0 <= ny < chunks_vertical and map_colors[ny][nx] is not None:
            adjacent_color = map_colors[ny][nx]
            for type_key, color in chunk_types.items():
                if adjacent_color == color:
                    count[type_key] += 1

    # Condiciones para la colocación de un chunk de tipo 'pueblo'
    if chunk_type == "pueblo":
        # No debe haber otro pueblo adyacente
        if count["pueblo"] > 0:
            return False
        # No debe haber pueblos en un radio de 6 chunks
        min_separation = 6
        for j in range(-min_separation, min_separation + 1):
            for i in range(-min_separation, min_separation + 1):
                nx, ny = x + i, y + j
                if 0 <= nx < chunks_horizontal and 0 <= ny < chunks_vertical:
                    if map_colors[ny][nx] == chunk_types["pueblo"]:
                        return False
        return True

    # Condiciones para la colocación de un chunk de tipo 'pradera'
    elif chunk_type == "pradera":
        # Debe tener al menos una pradera adyacente
        return count["pradera"] > 0

    # Condiciones para la colocación de un chunk de tipo 'desierto'
    elif chunk_type == "desierto":
        # Debe formar un grupo de al menos y no más de tres desiertos
        return count["desierto"] < 3

    # Condiciones para la colocación de un chunk de tipo 'volcan'
    elif chunk_type == "volcan":
        # Ejemplo de regla: no permitir volcanes adyacentes a pueblos
        if count["pueblo"] > 0:
            return False
        # No permitir volcanes adyacentes a otros volcanes para evitar saturación
        if count["volcan"] > 0:
            return False
        return True

    return True

def create_initial_map():
    map_colors = [[None for _ in range(chunks_horizontal)] for _ in range(chunks_vertical)]

    # Asegúrate de asignar colores válidos a cada posición
    for y in range(chunks_vertical):
        for x in range(chunks_horizontal):
            possible_chunks = list(chunk_types.keys())
            random.shuffle(possible_chunks)
            for chunk_type in possible_chunks:
                if valid_position(map_colors, x, y, chunk_type):
                    # Asignar el color base del chunk
                    base_color = chunk_types[chunk_type]
                    map_colors[y][x] = base_color
                    break
            if map_colors[y][x] is None:  # Asignar un color por defecto si ninguna condición es válida
                map_colors[y][x] = random.choice(list(chunk_types.values()))

    # Crear el game_map con gradientes en los tiles
    game_map = []
    for chunk_y in range(chunks_vertical):
        for tile_y in range(chunk_y * chunk_size, (chunk_y + 1) * chunk_size):
            row = []
            for chunk_x in range(chunks_horizontal):
                for tile_x in range(chunk_x * chunk_size, (chunk_x + 1) * chunk_size):
                    base_color = map_colors[chunk_y][chunk_x]
                    variation = random.randint(-15, 15)  # Rango de variación del color
                    color = get_gradient_color(base_color, variation)
                    row.append(color)
            game_map.append(row)

    return game_map