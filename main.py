import pygame
import sys
from settings import *
from map_manager import create_initial_map, expand_map

# Inicialización de Pygame
pygame.init()

# Configuración de la pantalla
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Carga de imágenes
player_image = pygame.image.load('player.png')
player_image = pygame.transform.scale(player_image, (PLAYER_SIZE, PLAYER_SIZE))

# Posición inicial del jugador
player_x, player_y = WIDTH // 2, HEIGHT // 2

# Mapa del juego
game_map = create_initial_map()

# Desplazamientos del mapa
horizontal_offset = 0
vertical_offset = 0

def draw_map(horizontal_offset, vertical_offset):
    for y in range(len(game_map)):
        for x in range(len(game_map[y])):
            rect = pygame.Rect(x * TILE_SIZE - horizontal_offset, y * TILE_SIZE - vertical_offset, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, game_map[y][x], rect)
    for y in range(0, len(game_map) * TILE_SIZE, CHUNK_PIXEL_SIZE):
        pygame.draw.line(screen, BLACK, (0, y - vertical_offset), (WIDTH, y - vertical_offset))
    for x in range(0, len(game_map[0]) * TILE_SIZE, CHUNK_PIXEL_SIZE):
        pygame.draw.line(screen, BLACK, (x - horizontal_offset, 0), (x - horizontal_offset, HEIGHT))

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
        horizontal_offset += chunk_pixel_size
    elif direction == 'up':
        new_row = [(random.randint(100, 255), 0, 0) for _ in range(chunks_horizontal * chunk_size)]
        for _ in range(chunk_size):
            game_map.insert(0, new_row[:])
        vertical_offset += chunk_pixel_size
    elif direction == 'down':
        new_row = [(random.randint(100, 255), 0, 0) for _ in range(chunks_horizontal * chunk_size)]
        for _ in range(chunk_size):
            game_map.append(new_row[:])
        chunks_vertical += 1

# Bucle principal del juego
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        player_x += VELOCITY
        if player_x > WIDTH - WIDTH // 4:
            horizontal_offset += VELOCITY
            if horizontal_offset > (chunks_horizontal * CHUNK_PIXEL_SIZE) - WIDTH:
                add_tiles('right')

    if keys[pygame.K_LEFT]:
        player_x -= VELOCITY
        if player_x < WIDTH // 4 and horizontal_offset > 0:
            horizontal_offset -= VELOCITY

    if keys[pygame.K_UP]:
        player_y -= VELOCITY
        if player_y < HEIGHT // 4 and vertical_offset > 0:
            vertical_offset -= VELOCITY

    if keys[pygame.K_DOWN]:
        player_y += VELOCITY
        if player_y > HEIGHT - HEIGHT // 4:
            vertical_offset += VELOCITY
            if vertical_offset > (chunks_vertical * CHUNK_PIXEL_SIZE) - HEIGHT:
                add_tiles('down')

    screen.fill(WHITE)
    draw_map(horizontal_offset, vertical_offset)
    screen.blit(player_image, (player_x, player_y))
    pygame.display.flip()

pygame.quit()
sys.exit()
