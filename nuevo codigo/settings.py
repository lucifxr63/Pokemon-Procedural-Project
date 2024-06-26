import pygame

# Inicialización de Pygame
pygame.init()

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
velocity = 12

# Dimensiones del chunk (por ejemplo, cada 4x4 tiles)
chunk_size = 4
tile_size = 80
chunk_pixel_size = chunk_size * tile_size  # Tamaño de un chunk en píxeles

# Variables para controlar la cantidad de chunks
chunks_horizontal = 10
chunks_vertical = 10

# Dimensiones totales del mapa en píxeles
map_width = chunks_horizontal * chunk_size * tile_size
map_height = chunks_vertical * chunk_size * tile_size

# Carga de imágenes
chunk_types = {
    "pueblo": pygame.image.load('./imagenes/grasspueblo.jpg').convert_alpha(),
    "pradera": pygame.image.load('./imagenes/praderabonita.jpg').convert_alpha(),
    "desierto": pygame.image.load('./imagenes/desiertopixel.jpg').convert_alpha(),
    "volcan": pygame.image.load('./imagenes/lava.jpg').convert_alpha()
}

# Escalar imágenes a tamaño de un chunk completo
for key in chunk_types:
    chunk_types[key] = pygame.transform.scale(chunk_types[key], (chunk_pixel_size, chunk_pixel_size))

player_image = pygame.image.load('./imagenes/player.png')
player_image = pygame.transform.scale(player_image, (player_size, player_size))
bush_image = pygame.image.load('./imagenes/c.png')
bush_image = pygame.transform.scale(bush_image, (tile_size, tile_size))
bush_fuego_image = pygame.image.load('./imagenes/b.png')
bush_fuego_image = pygame.transform.scale(bush_fuego_image, (tile_size, tile_size))
bush_desierto_image = pygame.image.load('./imagenes/a.png')
bush_desierto_image = pygame.transform.scale(bush_desierto_image, (tile_size, tile_size))
pueblo_image = pygame.image.load('./imagenes/pueblo.png')
pueblo_image = pygame.transform.scale(pueblo_image, (tile_size, tile_size))
