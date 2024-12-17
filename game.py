import pygame
import sys
import random

class GameSettings:
    def __init__(self):
        self.width = 1024
        self.height = 800
        self.player_name = ""

class Button:
    def __init__(self, x, y, width, height, text, font_size=32):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.Font(None, font_size)
        self.color_inactive = (200, 200, 200)
        self.color_active = (255, 255, 255)
        self.color = self.color_inactive

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = self.font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                self.color = self.color_active
            else:
                self.color = self.color_inactive

class InputBox:
    def __init__(self, x, y, width, height, text=''):
        self.rect = pygame.Rect(x, y, width, height)
        self.color_inactive = pygame.Color('lightskyblue3')
        self.color_active = pygame.Color('dodgerblue2')
        self.color = self.color_inactive
        self.text = text
        self.font = pygame.font.Font(None, 32)
        self.txt_surface = self.font.render(text, True, (255, 255, 255))  # Changed to white
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = self.color_active if self.active else self.color_inactive
        
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    return True
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = self.font.render(self.text, True, (255, 255, 255))  # White text
        return False

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

def options_menu(screen, settings):
    # Options menu background
    screen.fill((50, 50, 50))

    # Title
    title_font = pygame.font.Font(None, 64)
    title = title_font.render("Game Options", True, (255, 255, 255))
    title_rect = title.get_rect(center=(settings.width // 2, 100))
    screen.blit(title, title_rect)

    # Window Size Buttons
    size_buttons = [
        Button(settings.width // 2 - 200, 250, 150, 50, "800x600"),
        Button(settings.width // 2 - 25, 250, 150, 50, "1024x800"),
        Button(settings.width // 2 + 150, 250, 150, 50, "1280x720")
    ]

    # Back Button
    back_button = Button(settings.width // 2 - 100, 400, 200, 50, "Back to Main Menu")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            # Handle size buttons
            for button in size_buttons:
                button.handle_event(event)

            # Handle back button
            back_button.handle_event(event)

            # Check for mouse clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check size buttons
                for button in size_buttons:
                    if button.rect.collidepoint(event.pos):
                        if button.text == "800x600":
                            settings.width, settings.height = 800, 600
                        elif button.text == "1024x800":
                            settings.width, settings.height = 1024, 800
                        else:
                            settings.width, settings.height = 1280, 720

                # Check back button
                if back_button.rect.collidepoint(event.pos):
                    return True

        # Draw everything
        screen.fill((50, 50, 50))
        screen.blit(title, title_rect)

        # Draw size buttons
        for button in size_buttons:
            button.draw(screen)

        # Draw back button
        back_button.draw(screen)

        pygame.display.update()

    return False

def main_menu(screen, settings):
    # Menu background color
    screen.fill((50, 50, 50))

    # Title
    title_font = pygame.font.Font(None, 64)
    title = title_font.render("Minecraft Cube Game", True, (255, 255, 255))
    title_rect = title.get_rect(center=(settings.width // 2, 100))
    screen.blit(title, title_rect)

    # Player Name Input
    input_box = InputBox(settings.width // 2 - 200, 350, 400, 50)

    # Start Button
    start_button = Button(settings.width // 2 - 250, 450, 200, 50, "Start Game")

    # Options Button
    options_button = Button(settings.width // 2 + 50, 450, 200, 50, "Options")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            # Handle input box
            if input_box.handle_event(event):
                settings.player_name = input_box.text.strip() if input_box.text.strip() else "Player"

            # Handle start button
            start_button.handle_event(event)

            # Handle options button
            options_button.handle_event(event)

            # Check for mouse clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check start button
                if start_button.rect.collidepoint(event.pos):
                    # Ensure player name is not empty
                    if settings.player_name:
                        return True

                # Check options button
                if options_button.rect.collidepoint(event.pos):
                    options_menu(screen, settings)

        # Draw everything
        screen.fill((50, 50, 50))
        screen.blit(title, title_rect)

        # Draw input box
        input_box.draw(screen)

        # Draw player name label
        name_font = pygame.font.Font(None, 32)
        name_label = name_font.render("Enter Player Name:", True, (255, 255, 255))
        screen.blit(name_label, (settings.width // 2 - 200, 320))

        # Draw start and options buttons
        start_button.draw(screen)
        options_button.draw(screen)

        pygame.display.update()

    return False

def run_game(settings):
    # Inicializar Pygame
    pygame.init()

    # Configuración de la pantalla
    screen = pygame.display.set_mode((settings.width, settings.height))
    pygame.display.set_caption("Dinamo 2DGame")

    # Cargar imagen de fondo
    background_image = pygame.image.load('static/background.png')
    background_image = pygame.transform.scale(background_image, (settings.width, settings.height))

    # Colores
    SKY_BLUE = (135, 206, 235)
    GRASS_GREEN = (24, 40, 9)

    # Cargar los sprites del personaje
    player_sprites = [
        pygame.transform.scale(pygame.image.load('static/sprite/caida1.png'), (100, 100)),
        pygame.transform.scale(pygame.image.load('static/sprite/caida2.png'), (100, 100)),
        pygame.transform.scale(pygame.image.load('static/sprite/parado.png'), (100, 100)),
        pygame.transform.scale(pygame.image.load('static/sprite/parado2.png'), (100, 100)),
        pygame.transform.scale(pygame.image.load('static/sprite/parado3.png'), (100, 100)),
        pygame.transform.scale(pygame.image.load('static/sprite/salto1.png'), (100, 100)),
        pygame.transform.scale(pygame.image.load('static/sprite/salto2.png'), (100, 100)),
        pygame.transform.scale(pygame.image.load('static/sprite/salto3.png'), (100, 100))
    ]

    # Cargar la imagen de la moneda
    coin_image = pygame.transform.scale(pygame.image.load('static/coin.png'), (30, 30))

    # Cargar la imagen de la plataforma
    platform_image = pygame.transform.scale(pygame.image.load('static/plataforma.PNG'), (100, 20))

    # Cargar imagen de pasto
    grass_image = pygame.Surface((settings.width, 50))
    grass_image.fill(GRASS_GREEN)

    # Clase para las plataformas
    class Platform(pygame.sprite.Sprite):
        def __init__(self, x, y):
            super().__init__()
            self.image = platform_image
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y

    # Clase para la moneda
    class Coin(pygame.sprite.Sprite):
        def __init__(self, x, y):
            super().__init__()
            self.image = coin_image
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y

    # Configuración del jugador
    player_x = 50
    player_y = settings.height - 150
    velocity_x = 5  # Reducida la velocidad horizontal
    velocity_y = 0
    is_jumping = False
    jump_count = 0
    jump_height = 15
    gravity = 0.6
    current_sprite_index = 0  # Índice del sprite actual
    animation_timer = 0
    animation_delay = 10  # Cuántos frames deben pasar antes de cambiar de sprite

    # Grupo de plataformas y monedas
    platforms = pygame.sprite.Group()
    coins = pygame.sprite.Group()

    # Reiniciar el juego
    def reset_game():
        nonlocal player_x, player_y, is_jumping, jump_count, velocity_y, current_sprite_index
        player_x = 50
        player_y = settings.height - 150
        is_jumping = False
        jump_count = 0
        velocity_y = 0
        current_sprite_index = 2  # Sprite de parado
        platforms.empty()
        coins.empty()
        generate_platforms()
        generate_coin()

    # Generar plataformas de manera ordenada
    def generate_platforms():
        y = settings.height - 150
        for _ in range(10):
            x = random.randint(50, settings.width - 150)
            platform = Platform(x, y)
            platforms.add(platform)
            y -= 50

    # Generar una moneda siempre en la plataforma más alta
    def generate_coin():
        highest_platform = min(platforms, key=lambda p: p.rect.y)
        x = random.randint(highest_platform.rect.left, highest_platform.rect.right - 30)
        y = highest_platform.rect.top - 30
        coin = Coin(x, y)
        coins.add(coin)

    reset_game()

    # Banderas de estado
    game_won = False

    # Bucle principal del juego
    running = True
    clock = pygame.time.Clock()

    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        keys = pygame.key.get_pressed()

        # Movimiento horizontal con límites de pantalla
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= velocity_x
            animation_timer = (animation_timer + 1) % (len(player_sprites) * animation_delay)
            if animation_timer % animation_delay == 0:
                current_sprite_index = (current_sprite_index - 1) % len(player_sprites)
        if keys[pygame.K_RIGHT] and player_x < settings.width - 100:
            player_x += velocity_x
            animation_timer = (animation_timer + 1) % (len(player_sprites) * animation_delay)
            if animation_timer % animation_delay == 0:
                current_sprite_index = (current_sprite_index + 1) % len(player_sprites)

        # Salto
        if keys[pygame.K_UP] and not is_jumping:
            is_jumping = True
            velocity_y = -jump_height
            jump_count = 0
            current_sprite_index = 5  # Sprite de salto
            animation_timer = 0

        # Aplicar gravedad
        velocity_y += gravity
        player_y += velocity_y

        # Comprobar colisiones con plataformas
        player_rect = pygame.Rect(player_x, player_y, 100, 100)
        landed_on_platform = False
        for platform in platforms:
            if player_rect.colliderect(platform.rect) and velocity_y > 0:
                if player_y + 100 <= platform.rect.bottom:
                    player_y = platform.rect.top - 100
                    velocity_y = 0
                    is_jumping = False
                    landed_on_platform = True
                    current_sprite_index = 2  # Sprite de parado en plataforma
                    break

        # Colisión con el piso (pasto)
        if player_y + 100 >= settings.height - 50 and not landed_on_platform:
            player_y = settings.height - 150
            velocity_y = 0
            is_jumping = False
            current_sprite_index = 2  # Sprite de parado en el piso

        # Límites horizontales
        player_x = max(0, min(player_x, settings.width - 100))

        # Comprobar colisiones con monedas
        for coin in coins:
            if player_rect.colliderect(coin.rect):
                coins.remove(coin)
                game_won = True

        # Dibujar fondo
        screen.blit(background_image, (0, 0))

        # Dibujar pasto
        screen.blit(grass_image, (0, settings.height - 50))

        # Dibujar plataformas
        for platform in platforms:
            screen.blit(platform.image, platform.rect)

        # Dibujar monedas
        for coin in coins:
            screen.blit(coin.image, coin.rect)

        # Dibujar jugador (espejando si se mueve hacia la izquierda)
        sprite_to_draw = player_sprites[current_sprite_index]
        if keys[pygame.K_LEFT]:
            sprite_to_draw = pygame.transform.flip(sprite_to_draw, True, False)
        
        screen.blit(sprite_to_draw, (player_x, player_y))

        # Mostrar nombre del jugador
        font = pygame.font.Font(None, 36)
        name_text = font.render(f"Player: {settings.player_name}", True, (255, 255, 255))
        screen.blit(name_text, (10, 10))

        # Comprobar si el jugador ganó
        if game_won:
            font = pygame.font.Font(None, 36)
            text = font.render("¡Ganaste!", True, (255, 255, 255))
            text_rect = text.get_rect(center=(settings.width / 2, settings.height / 2))
            screen.blit(text, text_rect)
            pygame.display.update()
            pygame.time.delay(2000)
            reset_game()
            game_won = False

        # Actualizar pantalla
        pygame.display.update()

def main():
    pygame.init()
    
    # Initial settings
    settings = GameSettings()
    
    # Initial screen
    screen = pygame.display.set_mode((1024, 800))
    pygame.display.set_caption("Minecraft Cube Game")

    # Main menu loop
    while True:
        # Show main menu
        if not main_menu(screen, settings):
            break

        # Resize screen to selected dimensions
        screen = pygame.display.set_mode((settings.width, settings.height))
        pygame.display.set_caption(f"Minecraft Cube Game - {settings.player_name}")

        # Run the game
        run_game(settings)

    # salir del juego
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()