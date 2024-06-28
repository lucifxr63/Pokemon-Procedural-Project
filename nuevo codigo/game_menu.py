import pygame

def draw_start_screen(screen, width, height):
    # Fondo con una imagen
    background_image = pygame.image.load('./imagenes/portada.png')
    background_image = pygame.transform.scale(background_image, (width, height))
    screen.blit(background_image, (0, 0))

    # Texto del título con una fuente personalizada
    title_font = pygame.font.Font('./fuentes/Pokemon Solid.ttf', 48)
    title_text = title_font.render("POKEMON PROCEDURAL", True, (255, 255, 0))  # Texto amarillo
    title_rect = title_text.get_rect(center=(width // 2, height // 4))
    screen.blit(title_text, title_rect)

    # Botones con imágenes
    new_game_button = pygame.Rect(width // 2 - 100, height // 2 - 75, 200, 50)
    load_game_button = pygame.Rect(width // 2 - 100, height // 2 + 25, 200, 50)

    button_image = pygame.image.load('./imagenes/button.png')
    button_image = pygame.transform.scale(button_image, (200, 50))

    screen.blit(button_image, new_game_button.topleft)
    screen.blit(button_image, load_game_button.topleft)

    # Texto de los botones
    button_font = pygame.font.Font('./fuentes/Pokemon Solid.ttf', 36)
    new_game_text = button_font.render("Nueva Partida", True, (0, 0, 0))
    load_game_text = button_font.render("Cargar Partida", True, (0, 0, 0))

    new_game_text_rect = new_game_text.get_rect(center=new_game_button.center)
    load_game_text_rect = load_game_text.get_rect(center=load_game_button.center)

    screen.blit(new_game_text, new_game_text_rect)
    screen.blit(load_game_text, load_game_text_rect)

    pygame.display.flip()

def show_menu(screen, width, height):
    start_screen = True
    while start_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                new_game_button = pygame.Rect(width // 2 - 100, height // 2 - 75, 200, 50)
                load_game_button = pygame.Rect(width // 2 - 100, height // 2 + 25, 200, 50)
                
                if new_game_button.collidepoint(mouse_pos):
                    return 'new_game'
                elif load_game_button.collidepoint(mouse_pos):
                    return 'load_game'

        draw_start_screen(screen, width, height)

    return 'quit'
