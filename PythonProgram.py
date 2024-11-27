import pygame  #library used to create games
import math    #import math module to use mathematical operations like trigonometry , angles ...
import random  #makes the game more unpredictable, for example, by allowing zombies to appear at random points
import time    #offers time-related features, such as the ability to get the current cooldown or delay time.
import os      #manages file paths, enabling the loading of resources and images from designated directories.
import json    #Used for to store data (saved data) , used especially for leaderboard


pygame.init()                                     #launches every Pygame like the sounds, graphics modules...
pygame.font.init()                                #initialize the font module

#Screen and game setup
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

#Fonts type settings

title_font = pygame.font.SysFont("Arial", 64) #title font settings
menu_font = pygame.font.SysFont("Arial", 32)  #menu font settings
font = pygame.font.SysFont("Arial", 24)       #creating a font object to render and display text in my game

#Game state

LOGIN = "login"             #indentify and check if the user in login screen
MAIN_MENU = "main_menu"     # Identify and Check if the user is in main menu
GAME = "game"               #identify and check if the user is in game (gameplay)
GAME_OVER = "game_over"     #identify and check if the user is in game over screen
LEADERBOARD = "leaderboard" #identify and check if the user is in the leaderboard menu
sort_ascending = False      #controls how the leaderboard should be sorted

#current game state and player info
current_state = LOGIN       #This variable records the game's current status , the program will always start with LOGIN
current_player = ""         #this variable initialize the username as empty space so it let the user put its own
current_score = 0           #this variable is basically the score of the player everytime he starts a game

#initialize pygame
pygame.init()

#Screen and game setup

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
        return pygame.Surface(size or (50, 50))  # Return a placeholder image if loading fails


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

#zombies setting
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

# Button class for menu items
class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.is_hovered = False

    def draw(self, surface):
        color = GRAY if self.is_hovered else BLACK
        pygame.draw.rect(surface, color, self.rect, border_radius=12)
        pygame.draw.rect(surface, WHITE, self.rect, 2, border_radius=12)
        text_surface = menu_font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
            return False
        if event.type == pygame.MOUSEBUTTONDOWN and self.is_hovered:
            return True
        return False

# Load and save leaderboard
def load_leaderboard():
    try:
        with open('leaderboard.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_leaderboard(leaderboard):
    # Sort before saving (always save in descending order)
    leaderboard.sort(key=lambda x: x['score'], reverse=True)
    with open('leaderboard.json', 'w') as f:
        json.dump(leaderboard, f)

def update_leaderboard(username, score):
    leaderboard = load_leaderboard()
    leaderboard.append({"username": username, "score": score})
    leaderboard.sort(key=lambda x: x["score"], reverse=True)
    leaderboard = leaderboard[:10]  # Keep only top 10
    save_leaderboard(leaderboard)

# Create menu buttons
main_menu_buttons = [
    Button(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 50, "Play"),
    Button(WIDTH // 2 - 100, HEIGHT // 2 + 20, 200, 50, "Leaderboard"),
    Button(WIDTH // 2 - 100, HEIGHT // 2 + 90, 200, 50, "Quit")
]

game_over_buttons = [
    Button(WIDTH // 2 - 100, HEIGHT // 2 + 20, 200, 50, "Try Again"),
    Button(WIDTH // 2 - 100, HEIGHT // 2 + 90, 200, 50, "Main Menu")
]

leaderboard_buttons = [
    Button(WIDTH // 2 - 100, HEIGHT - 100, 200, 50, "Back to Menu"),
    Button(WIDTH//2 - 100, HEIGHT - 160, 200, 50, "Toggle Sort")
]

# Input box for username
input_box = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 32)
input_text = ""
input_active = False


def draw_login_screen():
    screen.fill(BLACK)
    title = title_font.render("Login", True, WHITE)
    title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 3))
    screen.blit(title, title_rect)

    pygame.draw.rect(screen, WHITE if input_active else GRAY, input_box, 2)
    text_surface = font.render(input_text, True, WHITE)
    width = max(200, text_surface.get_width() + 10)
    input_box.w = width
    screen.blit(text_surface, (input_box.x + 5, input_box.y + 5))

    prompt = font.render("Enter your username:", True, WHITE)
    prompt_rect = prompt.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30))
    screen.blit(prompt, prompt_rect)


def draw_main_menu():
    screen.fill(BLACK)
    title = title_font.render("Zombie Shooter", True, WHITE)
    title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 4))
    screen.blit(title, title_rect)
    for button in main_menu_buttons:
        button.draw(screen)


def draw_game_over():
    screen.fill(BLACK)
    title = title_font.render("Game Over", True, RED)
    title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 4))
    screen.blit(title, title_rect)

    score_text = menu_font.render(f"Player: {current_player}", True, WHITE)
    score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
    screen.blit(score_text, score_rect)

    score_text = menu_font.render(f"Score: {current_score}", True, WHITE)
    score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    screen.blit(score_text, score_rect)

    for button in game_over_buttons:
        button.draw(screen)


def draw_leaderboard():
    global sort_ascending
    screen.fill(BLACK)

    # Draw title
    title = title_font.render("Leaderboard", True, WHITE)
    title_rect = title.get_rect(center=(WIDTH // 2, 50))
    screen.blit(title, title_rect)

    # Draw sort order indicator
    sort_text = menu_font.render(
        "Sort: " + ("Lowest to Highest" if sort_ascending else "Highest to Lowest"),
        True,
        WHITE
    )
    sort_rect = sort_text.get_rect(center=(WIDTH // 2, 100))
    screen.blit(sort_text, sort_rect)

    # Get and sort leaderboard
    leaderboard = load_leaderboard()
    leaderboard.sort(key=lambda x: x['score'], reverse=not sort_ascending)

    # Draw entries
    for i, entry in enumerate(leaderboard):
        text = menu_font.render(
            f"{i + 1}. {entry['username']}: {entry['score']}",
            True,
            WHITE
        )
        rect = text.get_rect(center=(WIDTH // 2, 150 + i * 40))
        screen.blit(text, rect)

        # Draw buttons
        for button in leaderboard_buttons:
            button.draw(screen)


def reset_game():
    global health, score, zombies, bullets
    health = 3
    score = 0
    zombies = []
    bullets = []
    soldier_rect.center = (WIDTH // 2, HEIGHT // 2)


# Main Game Loop
running = True
while running:
    if current_state == GAME:
        screen.blit(background, (0, 0))

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    current_state = MAIN_MENU

                # Get keys for movement
                keys = pygame.key.get_pressed()
                if keys[pygame.K_w]:
                    soldier_rect.y -= 3
                if keys[pygame.K_s]:
                    soldier_rect.y += 3
                if keys[pygame.K_a]:
                    soldier_rect.x -= 3
                if keys[pygame.K_d]:
                    soldier_rect.x += 3

                # Keep soldier on screen
                soldier_rect.x = max(0, min(WIDTH - soldier_rect.width, soldier_rect.x))
                soldier_rect.y = max(0, min(HEIGHT - soldier_rect.height, soldier_rect.y))

                # Mouse position and angle
                mouse_x, mouse_y = pygame.mouse.get_pos()
                angle = math.degrees(math.atan2(-(mouse_y - soldier_rect.centery), mouse_x - soldier_rect.centerx))

                # Rotate soldier
                rotated_soldier = pygame.transform.rotate(soldier, angle)
                soldier_pos = rotated_soldier.get_rect(center=soldier_rect.center)
                screen.blit(rotated_soldier, soldier_pos)


























