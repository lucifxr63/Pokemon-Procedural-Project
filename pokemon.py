import pygame
import sys
import random

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
velocity = 5

# Carga de imágenes
player_image = pygame.image.load('player.png')
player_image = pygame.transform.scale(player_image, (player_size, player_size))

# Dimensiones del chunk (por ejemplo, cada 4x4 tiles)
chunk_size = 4
tile_size = 80
chunk_pixel_size = chunk_size * tile_size

# Variables para controlar la cantidad de chunks
chunks_horizontal = 5
chunks_vertical = 3

# Función para crear un mapa inicial
def create_initial_map():
    map_colors = [[(random.randint(100, 255), 0, 0) for _ in range(chunks_horizontal)] for _ in range(chunks_vertical)]
    game_map = []
    for y in range(chunks_vertical * chunk_size):
        row = []
        for x in range(chunks_horizontal * chunk_size):
            chunk_x = x // chunk_size
            chunk_y = y // chunk_size
            row.append(map_colors[chunk_y][chunk_x])
        game_map.append(row)
    return game_map

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
    if direction == 'right':
        for _ in range(chunk_size):
            for row in game_map:
                row.append((random.randint(100, 255), 0, 0))
        chunks_horizontal += 1
    elif direction == 'left':
        for _ in range(chunk_size):
            for row in game_map:
                row.insert(0, (random.randint(100, 255), 0, 0))
        horizontal_offset += chunk_pixel_size  # Ajuste para mantener el punto de vista
    elif direction == 'up':
        for _ in range(chunk_size):
            new_row = [(random.randint(100, 255), 0, 0) for _ in range(chunks_horizontal * chunk_size)]
            game_map.insert(0, new_row)
        vertical_offset += chunk_pixel_size  # Ajuste para mantener el punto de vista
    elif direction == 'down':
        for _ in range(chunk_size):
            new_row = [(random.randint(100, 255), 0, 0) for _ in range(chunks_horizontal * chunk_size)]
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
