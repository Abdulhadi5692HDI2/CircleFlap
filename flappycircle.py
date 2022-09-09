# FlappyCircle
# Sprites in same dir
import os
from time import sleep
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

pygame.display.set_caption("Flappy Circle v1")

class Text(pygame.sprite.Sprite):
    def __init__(self):
        super(Text, self).__init__()
        self.surf = pygame.image.load("data/gfx/text.ptxt").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("data/gfx/circle.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()
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

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCR_WIDTH:
            self.rect.right = SCR_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCR_HEIGHT:
            self.rect.bottom = SCR_HEIGHT
        
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
# Variables for screen height and width
SCR_HEIGHT = 640
SCR_WIDTH = 800

# Create a screen object
screen = pygame.display.set_mode((SCR_WIDTH, SCR_HEIGHT))

# Init the text
text = Text()
# Make a custom event for adding a enemy and a cloud
SPAWN_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_ENEMY, 250)
SPAWN_CLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(SPAWN_CLOUD, 1000)
# Init the player.
player = Player()
# Create sprite groups to hold data of the sprites
enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(text)
# Make a clock to cap the fps
fpsClock = pygame.time.Clock()
# Main loop running or not?
running = True

# Main loop :) [YAY The game wont close after 1 ms]
while running:
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
    #moving_sound = pygame.mixer.Sound("data/sound/moving.wav")
    collide = pygame.mixer.Sound("data/sound/collision.wav")
    # Create pressed_keys variable for player movement
    pressed_keys = pygame.key.get_pressed()
    # Make sure player can move
    player.update(pressed_keys)

    # Update enemy and cloud position
    enemies.update()
    clouds.update()
    # Fill the screen with a sky-blueish color
    screen.fill((71, 139, 191))
    # Draw all sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
    # Check if any enemys collided with the player
    if pygame.sprite.spritecollideany(player, enemies):
        # If so , murder the player and crash the game
        player.kill()

        # Stop every sound and play the collide sound
        #moving_sound.stop()
        collide.play()

        # Quit the game
        running = False
    # Caps the fps at 60
    fpsClock.tick(60)
    # Shows the display! Without this there will only be the color black on the screen
    pygame.display.flip()
# Stop sound mixer
pygame.mixer.music.stop()
pygame.mixer.quit()