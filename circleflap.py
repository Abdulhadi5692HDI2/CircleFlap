# CircleFlap
# Sprites in same dir
import sys
import pygame
import random

# Import <List> from pygame.locals to make access to key coords easier
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# INIT SOUND MIXER
pygame.mixer.init()
# Initilaize pygame
pygame.init()

pygame.display.set_caption("Circle Flap v2")
font_name = pygame.font.match_font('arial')
def mktext(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("data/gfx/circle.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()

    # Move the sprite based on user keypresses
    def update(self, pressed_keys):
        if pressed_keys[K_UP] is True:
            self.rect.move_ip(0, -5)
            #moving_sound.play()
        if pressed_keys[K_DOWN] is True:
            self.rect.move_ip(0, 5)
            #moving_sound.play()
        if pressed_keys[K_LEFT] is True:
            self.rect.move_ip(-5, 0)
            #moving_sound.play()
        if pressed_keys[K_RIGHT] is True:
            self.rect.move_ip(5, 0)
            #moving_sound.play()
        if pressed_keys[pygame.K_SPACE] is True:
            self.rect.move_ip(0, -10)
            self.rect.move_ip(0, -5)
            self.rect.move_ip(0, 0)

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCR_WIDTH:
            self.rect.right = SCR_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCR_HEIGHT:
            self.rect.bottom = SCR_HEIGHT
    # The player can shoot
    def shoot(self):
        laser = Laser(self.rect.centerx, self.rect.right)
        all_sprites.add(laser)
        lasers.add(laser)
        lasers.update()


        
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("data/gfx/cube.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(center=(
                random.randint(SCR_WIDTH + 20, SCR_WIDTH + 100),
                random.randint(0, SCR_HEIGHT),
            )
        )
        self.speed = random.randint(5, 20)
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()
class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load("data/gfx/cloud.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        # Random start position for the cloud
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCR_WIDTH + 20, SCR_WIDTH + 100),
                random.randint(0, SCR_HEIGHT)
            )
        )
    # Move the cloud
    # Make the cloud disappear when it touches the left edge of the screen [game area]
    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()
class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Laser, self).__init__()
        self.surf = pygame.image.load("data/gfx/laser.bmp").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = 5
    def update(self):
        sp1 = self.speedy
        self.rect.move_ip(sp1, 0)
        if self.rect.right < 0:
            self.kill()

# Variables for screen height and width
SCR_HEIGHT = 1080
SCR_WIDTH = 1080

# Create a screen object
screen = pygame.display.set_mode(
    (SCR_WIDTH, SCR_HEIGHT),
    pygame.FULLSCREEN
)

def show_title_scr():
    screen.fill((71, 139, 191))
    mktext(screen, "CircleFlap!!", 64, SCR_WIDTH / 2, SCR_HEIGHT / 4)
    mktext(screen, "Use the arrow keys [up, down, left, right] to move! More coming soon", 22, SCR_WIDTH / 2, SCR_HEIGHT / 2)
    mktext(screen, "Press a key to start", 18, SCR_WIDTH / 2, SCR_HEIGHT * 3 / 4)
    mktext(screen, "v2", 16, SCR_WIDTH / 2, SCR_HEIGHT * 2 / 5)
    pygame.display.flip()
    waitingForKey = True
    while waitingForKey:
        fpsClock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(1)
            if event.type == pygame.KEYUP:
                waitingForKey = False

# Make a custom event for adding a enemy and a cloud
SPAWN_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_ENEMY, 250)
SPAWN_CLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(SPAWN_CLOUD, 1000)
# Init the player.
player = Player()
# Make a clock to cap the fps
fpsClock = pygame.time.Clock()
# Game over logic
game_over = True
# Main loop running or not?
running = True

# Main loop :) [YAY The game wont close after 1 ms]
while running:
    # if game_over
    if game_over:
        show_title_scr()
        game_over = False
        # Create sprite groups to hold data of the sprites
        enemies = pygame.sprite.Group()
        lasers = pygame.sprite.Group()
        clouds = pygame.sprite.Group()
        all_sprites = pygame.sprite.Group()
        all_sprites.add(player)
    # Search for E V E R Y event in the G A M E
    for event in pygame.event.get():
        # Did a user smash a key on the keyboard???
        if event.type == KEYDOWN:
            # If it was the ESC key destroy the main loop
            if event.key == K_ESCAPE:
                pygame.display.set_caption("Game ended")
                print("You pressed ESC which is the main key to close the game")
                running = False
        # Did the user click the X button (or pressed ALT+F4) If they did also destroy the loop
        elif event.type == QUIT:
            print("You pressed the X button or did ALT+F4")
            running = False 
        elif event.type == SPAWN_ENEMY:
            # Create a enemy and add to sprite groups
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
        elif event.type == SPAWN_CLOUD:
            # Create a cloud and add it to sprite groups
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)
    # Load sounds
    moving_sound = pygame.mixer.Sound("data/sound/moving.wav")
    collide = pygame.mixer.Sound("data/sound/collision.wav")
    # Create pressed_keys variable for player movement
    pressed_keys = pygame.key.get_pressed()
    # Make a deaths variable
    deaths = 0
    # Make sure player can move
    player.update(pressed_keys)
    # clod and enemy update
    enemies.update()
    clouds.update()
    # Fill the screen with a sky-blueish color
    screen.fill((71, 139, 191))
    # Draw all sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
    # Check if any enemys collided with the player
    if pygame.sprite.spritecollideany(player, enemies):
        if player.lives == 0:
            player.kill()

        # Set game over to true
        game_over = True
    
    # Caps the fps
    fpsClock.tick(30)
    # Shows the display! Without this there will only be the color black on the screen
    pygame.display.flip()
# Stop sound mixer
pygame.mixer.music.stop()
pygame.mixer.quit()
