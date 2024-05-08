
import random
from settings import chunks_vertical,chunks_horizontal,chunk_size


# Tipos de chunks con sus colores correspondientes
chunk_types = {
    "pueblo": (0, 0, 255),  # Azul
    "pradera": (0, 255, 0),  # Verde
    "desierto": (255, 255, 0)  # Amarillo
}

def is_valid_position(map_colors, x, y, chunk_type):
    # Corrección: verificar si map_colors está completamente inicializado
    if any(col is None for row in map_colors for col in row):
        return True  # Asumimos válido si el mapa aún no está completamente inicializado

    max_x = len(map_colors[0]) - 1  # El máximo índice X accesible
    max_y = len(map_colors) - 1     # El máximo índice Y accesible

    if chunk_type == "pueblo":
        for dx in range(-12, 13):
            for dy in range(-12, 13):
                nx, ny = x + dx, y + dy
                if 0 <= nx <= max_x and 0 <= ny <= max_y:
                    if map_colors[ny][nx] == chunk_types["pueblo"]:
                        return False
    elif chunk_type == "pradera":
        adjacent_pradera = False
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx <= max_x and 0 <= ny <= max_y:
                if map_colors[ny][nx] == chunk_types["pradera"]:
                    adjacent_pradera = True
        return adjacent_pradera
    return True


def create_initial_map():
    map_colors = [[None for _ in range(chunks_horizontal)] for _ in range(chunks_vertical)]
    for y in range(chunks_vertical):
        for x in range(chunks_horizontal):
            # Elegir un tipo de chunk aleatorio inicialmente y validar
            while True:
                chosen_type = random.choice(list(chunk_types.keys()))
                if is_valid_position(map_colors, x, y, chosen_type):
                    map_colors[y][x] = chunk_types[chosen_type]
                    break

    # Generar el mapa de colores
    game_map = []
    for y in range(chunks_vertical * chunk_size):
        row = []
        for x in range(chunks_horizontal * chunk_size):
            chunk_x = x // chunk_size
            chunk_y = y // chunk_size
            row.append(map_colors[chunk_y][chunk_x])
        game_map.append(row)
    return game_map
