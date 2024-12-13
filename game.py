import pygame
import sys
import random

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 1024, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Juego de Cubo de Minecraft")

# Cargar imagen de fondo
background_image = pygame.image.load('static/background.png')
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

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
grass_image = pygame.Surface((WIDTH, 50))
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
player_y = HEIGHT - 150
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
    global player_x, player_y, is_jumping, jump_count, velocity_y, current_sprite_index
    player_x = 50
    player_y = HEIGHT - 150
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
    y = HEIGHT - 150
    for _ in range(10):
        x = random.randint(50, WIDTH - 150)
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
            running = False

    keys = pygame.key.get_pressed()

    # Movimiento horizontal con límites de pantalla
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= velocity_x
        animation_timer = (animation_timer + 1) % (len(player_sprites) * animation_delay)
        if animation_timer % animation_delay == 0:
            current_sprite_index = (current_sprite_index - 1) % len(player_sprites)
    if keys[pygame.K_RIGHT] and player_x < WIDTH - 100:
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
    if player_y + 100 >= HEIGHT - 50 and not landed_on_platform:
        player_y = HEIGHT - 150
        velocity_y = 0
        is_jumping = False
        current_sprite_index = 2  # Sprite de parado en el piso

    # Límites horizontales
    player_x = max(0, min(player_x, WIDTH - 100))

    # Comprobar colisiones con monedas
    for coin in coins:
        if player_rect.colliderect(coin.rect):
            coins.remove(coin)
            game_won = True

    # Dibujar fondo
    screen.blit(background_image, (0, 0))

    # Dibujar pasto
    screen.blit(grass_image, (0, HEIGHT - 50))

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

    # Comprobar si el jugador ganó
    if game_won:
        font = pygame.font.Font(None, 36)
        text = font.render("¡Ganaste!", True, (255, 255, 255))
        text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        screen.blit(text, text_rect)
        pygame.display.update()
        pygame.time.delay(2000)
        reset_game()
        game_won = False

    # Actualizar pantalla
    pygame.display.update()

# Salir del juego
pygame.quit()
sys.exit()
