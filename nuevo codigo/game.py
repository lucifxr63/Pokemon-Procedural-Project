import pygame
from settings import width, height, screen, WHITE, player_x, player_y, player_size, velocity, player_image, map_width, map_height
from mapa import create_initial_map, load_map, save_map, draw_map, expand_map_if_needed

def run_game(state):
    global player_x, player_y

    if state == 'new_game':
        game_map = create_initial_map()
    elif state == 'load_game':
        game_map = load_map()

    horizontal_offset = 0
    vertical_offset = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit', False
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
        draw_map(game_map, horizontal_offset, vertical_offset)
        screen.blit(player_image, (player_x, player_y))
        pygame.display.flip()

    return 'quit', False
