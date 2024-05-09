import pygame


# Dimensiones de la ventana
width, height = 640, 480
screen = pygame.display.set_mode((width, height))

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)  # Color para las líneas de separación de chunks

# Posición del jugador
player_x, player_y = width // 2, height // 2
player_size = 20

# Velocidad del jugador
velocity = 5

# Carga de imágenes
player_image = pygame.image.load('player.png')
player_image = pygame.transform.scale(player_image, (player_size, player_size))

# Dimensiones del chunk (por ejemplo, cada 4x4 tiles)
chunk_size = 4
tile_size = 80
chunk_pixel_size = chunk_size * tile_size

# Variables para controlar la cantidad de chunks
chunks_horizontal = 30
chunks_vertical = 30

# En settings.py
map_width = chunks_horizontal * chunk_size * tile_size
map_height = chunks_vertical * chunk_size * tile_size
