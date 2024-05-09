# map_generador.py
import random
from settings import chunks_vertical, chunks_horizontal, chunk_images

def create_initial_map():
    """
    Crea el mapa inicial asignando una imagen a cada chunk según su tipo.
    Utiliza las imágenes predefinidas cargadas en settings para representar cada tipo de chunk.
    """
    # Inicializa una matriz para guardar la imagen de cada chunk
    map_images = [[None for _ in range(chunks_horizontal)] for _ in range(chunks_vertical)]

    # Asignar una imagen válida a cada posición
    for y in range(chunks_vertical):
        for x in range(chunks_horizontal):
            possible_chunks = list(chunk_images.keys())
            random.shuffle(possible_chunks)  # Mezclar los tipos de chunks para asignación aleatoria
            for chunk_type in possible_chunks:
                if valid_position(map_images, x, y, chunk_type):
                    map_images[y][x] = chunk_images[chunk_type]
                    break
            if map_images[y][x] is None:  # Asignar una imagen por defecto si ninguna condición es válida
                map_images[y][x] = random.choice(list(chunk_images.values()))

    return map_images

# La función valid_position debe ser ajustada si aún no se ha hecho para trabajar con imágenes
def valid_position(map_images, x, y, chunk_type):
    """
    Verifica si es válida la posición para colocar un nuevo chunk según las reglas establecidas.
    """
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    count = {key: 0 for key in chunk_images.keys()}  # Inicializa el contador para cada tipo de chunk

    # Recorrer todas las direcciones para contar los chunks adyacentes
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < chunks_horizontal and 0 <= ny < chunks_vertical and map_images[ny][nx] is not None:
            adjacent_image = map_images[ny][nx]
            for type_key, image in chunk_images.items():
                if adjacent_image == image:
                    count[type_key] += 1

    # Aplicar las reglas de validación según el tipo de chunk
    if chunk_type == "pueblo" and count["pueblo"] > 0:
        return False
    elif chunk_type == "pradera" and count["pradera"] == 0:
        return False
    elif chunk_type == "desierto" and count["desierto"] >= 3:
        return False
    elif chunk_type == "volcan" and (count["pueblo"] > 0 or count["volcan"] > 0):
        return False

    return True
