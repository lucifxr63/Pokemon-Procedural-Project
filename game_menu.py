import pygame

def draw_start_screen(screen, width, height):
    screen.fill((0, 255, 0))  # Fondo verde
    font = pygame.font.Font(None, 36)
    title_text = font.render("POKEMON PROCEDURAL", True, (0, 0, 0))
    title_rect = title_text.get_rect(center=(width // 2, height // 3))
    screen.blit(title_text, title_rect)

    create_button = pygame.Rect(width // 2 - 100, height // 2 - 25, 200, 50)
    pygame.draw.rect(screen, (0, 0, 255), create_button)
    create_text = font.render("Crear Mapa", True, (255, 255, 255))
    create_text_rect = create_text.get_rect(center=create_button.center)
    screen.blit(create_text, create_text_rect)

    pygame.display.flip()

def show_menu(screen, width, height):
    start_screen = True
    while start_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                create_button = pygame.Rect(width // 2 - 100, height // 2 - 25, 200, 50)
                if create_button.collidepoint(mouse_pos):
                    return 'game'

        draw_start_screen(screen, width, height)

    return 'quit'
