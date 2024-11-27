import pygame  #library used to create games
import math    #import math module to use mathematical operations like trigonometry , angles ...
import random  #makes the game more unpredictable, for example, by allowing zombies to appear at random points
import time    #offers time-related features, such as the ability to get the current cooldown or delay time.
import os      #manages file paths, enabling the loading of resources and images from designated directories.
import json    #Used for to store data (saved data) , used especially for leaderboard


pygame.init()                                     #launches every Pygame like the sounds, graphics modules...
pygame.font.init()                                #initialize the font module

WIDTH, HEIGHT = 800, 600                          #defines the dimensions of the screen
FPS = 60                                          #frame rate per second
screen = pygame.display.set_mode((WIDTH, HEIGHT)) #creates the game window
pygame.display.set_caption("Zombie Shooter Game") #the title that display on game window
clock = pygame.time.Clock()                       #this optimizes the game by regulating the FPS

#setting colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
RED = (255, 0, 0)


title_font = pygame.font.SysFont("Arial", 64) #title font settings
menu_font = pygame.font.SysFont("Arial", 32)  #menu font settings
font = pygame.font.SysFont("Arial", 24)       #creating a font object to render and display text in my game


LOGIN = "login"             #indentify and check if the user in login screen
MAIN_MENU = "main_menu"     # Identify and Check if the user is in main menu
GAME = "game"               #identify and check if the user is in game (gameplay)
GAME_OVER = "game_over"     #identify and check if the user is in game over screen
LEADERBOARD = "leaderboard" #identify and check if the user is in the leaderboard menu
sort_ascending = False      #controls how the leaderboard should be sorted

current_state = LOGIN       #This variable records the game's current status , the program will always start with LOGIN
current_player = ""         #this variable initialize the username as empty space so it let the user put its own
current_score = 0           #this variable is basically the score of the player everytime he starts a game

pygame.init()


WIDTH, HEIGHT = 800, 600
FPS = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zombie Shooter Game")
clock = pygame.time.Clock()

#function to load image from local disk
def load_image(filename, size=None):
    try:
        image_path = os.path.join('assets', 'sprites', filename)  # Update the folder path where images are stored
        image = pygame.image.load(image_path).convert_alpha()
        if size:
            image = pygame.transform.scale(image, size)
        return image
    except pygame.error as e:
        print(f"Error loading image: {e}")
        return pygame.Surface(size or (50, 50))

#add images from disk local
background = load_image('background.png', (WIDTH, HEIGHT))
soldier = load_image('survivor-idle_shotgun.png', (50, 50))
bullet_img = load_image('yellow-ball-3d.png', (15, 15))
zombie_img = load_image('skeleton-attack.png', (50, 50))
heart_img = load_image('heart.png', (40, 40))

#soldier and bullet settings
soldier_rect = soldier.get_rect(center=(WIDTH // 2, HEIGHT // 2))
bullets = []
bullet_speed = 10
last_shot = 0
shoot_cooldown = 0.5
#zombies settings
zombies = []
zombie_speed = 1
last_zombie_spawn_time = 0
zombie_spawn_cooldown = 1

#health and score setup
health = 3
score = 0
font = pygame.font.SysFont("Arial", 24)
health_x, health_y = 10, 10


def spawn_zombie():
    edge = random.choice(['top', 'bottom', 'left', 'right'])
    if edge == 'top':
        x = random.randint(0, WIDTH)
        y = 0
    elif edge == 'bottom':
        x = random.randint(0, WIDTH)
        y = HEIGHT
    elif edge == 'left':
        x = 0
        y = random.randint(0, HEIGHT)
    elif edge == 'right':
        x = WIDTH
        y = random.randint(0, HEIGHT)

    zombie = {
        "x": x,
        "y": y,
        "rect": zombie_img.get_rect(center=(x, y)),
        "angle": 0,
    }
    zombies.append(zombie)

#Main Game Loop
running = True
while running:
    screen.blit(background, (0, 0))
#check quit event to close the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

#keys for soldier movements
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        soldier_rect.y -= 3
    if keys[pygame.K_s]:
        soldier_rect.y += 3
    if keys[pygame.K_a]:
        soldier_rect.x -= 3
    if keys[pygame.K_d]:
        soldier_rect.x += 3

    soldier_rect.x = max(0, min(WIDTH - soldier_rect.width, soldier_rect.x))
    soldier_rect.y = max(0, min(HEIGHT - soldier_rect.height, soldier_rect.y))

    # Mouse position and angle
    mouse_x, mouse_y = pygame.mouse.get_pos()
    angle = math.degrees(math.atan2(-(mouse_y - soldier_rect.centery), mouse_x - soldier_rect.centerx))

    # Rotate soldier
    rotated_soldier = pygame.transform.rotate(soldier, angle)
    soldier_pos = rotated_soldier.get_rect(center=soldier_rect.center)
    screen.blit(rotated_soldier, soldier_pos)

    # Shooting bullets
    if keys[pygame.K_SPACE] and time.time() - last_shot > shoot_cooldown:
        bullet_dx = math.cos(math.radians(angle))
        bullet_dy = -math.sin(math.radians(angle))
        bullet_x = soldier_rect.centerx + 30 * bullet_dx
        bullet_y = soldier_rect.centery + 10 * bullet_dy
        bullets.append({"x": bullet_x, "y": bullet_y, "dx": bullet_dx, "dy": bullet_dy})
        last_shot = time.time()

    # Update bullets
    for bullet in bullets[:]:
        bullet["x"] += bullet["dx"] * bullet_speed
        bullet["y"] += bullet["dy"] * bullet_speed

        if not (0 <= bullet["x"] <= WIDTH and 0 <= bullet["y"] <= HEIGHT):
            bullets.remove(bullet)


















