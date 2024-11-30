import pygame  #library used to create games
import math    #import math module to use mathematical operations like trigonometry , angles ...
import random  #makes the game more unpredictable, for example, by allowing zombies to appear at random points
import time    #offers time-related features, such as the ability to get the current cooldown or delay time.
import os      #manages file paths, enabling the loading of resources and images from designated directories.
import json    #Used for to store data (saved data) , used especially for leaderboard


pygame.init()                                     #launches every Pygame like the sounds, graphics modules...
pygame.font.init()                                #initialize the font module

# Load the music
game_music = "game_music.wav"  # Replace with the actual path to your music file
Zombie_hit = "Zombie_hit.wav"  # Sound for zombie death, change path as necessary

# Function to play background music
def play_music():
    pygame.mixer.music.load(game_music)
    pygame.mixer.music.play(-1, 0.0)  # Play the music in a loop

# Function to stop background music
def stop_music():
    pygame.mixer.music.stop()              #Stop the music playing

# Function to play a sound effect (zombie dying)
def play_sound_effect(sound):
    sound_effect = pygame.mixer.Sound(sound)             #
    sound_effect.play()

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

WIDTH, HEIGHT = 800, 600                                #setting the width and the height of the screen
fps = 60                                                #number of frame rate which let the game run smoothly
SurfaceType = pygame.display.set_mode((WIDTH, HEIGHT))  #set the pygame program to the width and height initialized
pygame.display.set_caption("Zombie Shooter Game")       #display the title game in the window program
Clock = pygame.time.Clock()

#function to load image from local disk
def load_image(filename, size=None):
    try:
        image_path = os.path.join('assets', 'sprites', filename)  # Update the folder path where images are stored
        image = pygame.image.load(image_path).convert_alpha()     #load the image from the updated and specified math
        if size:
            image = pygame.transform.scale(image, size)            #scale the image to the given dimension if the size is specified
        return image
    except pygame.error as e:
        print(f"Error loading image: {e}")                         #print an error message if there is an error
        return pygame.Surface(size or (50, 50))                    # Return a placeholder image if loading fails


#add images from disk local
background = load_image('background.png', (WIDTH, HEIGHT))      #setting the background image to a specified size
soldier = load_image('survivor-idle_shotgun.png', (50, 50))     #load soldier image from disk
bullet_img = load_image('yellow-ball-3d.png', (15, 15))         #load the bullet from the disk
zombie_img = load_image('skeleton-attack.png', (50, 50))        #load zombie image from the disk
heart_img = load_image('heart.png', (40, 40))                   #load heart image from the disk

#soldier and bullet settings
soldier_rect = soldier.get_rect(center=(WIDTH // 0.5, HEIGHT // 0.5))        #creating and centering the soldier HitBox
bullets = []                                                                 #empty bullet list
bullet_speed = 10                                      #a variable which set the bullet speed to 10
last_shot = 0
shoot_cooldown = 0.5                                   #a variable which limit the number of bullet Shot in one frame

#zombies setting
zombies = []                                #zombie empty list
zombie_speed = 1                            #zombie movement speed
last_zombie_spawn_time = 0
zombie_spawn_cooldown = 0.60                #spawn zombie every frame per second

#health and score setup
health = 3                                              # starting with 3 hearts
score = 0                                               # starting with a score of 0
Font = pygame.font.SysFont("Arial", 24)      #setting the size and type of pygame font
health_x, health_y = 10, 10                             #position of the hearts


def spawn_zombie():
    edge = random.choice(['top', 'bottom', 'left', 'right'])       #a list with the 4 edges of the screen
    if edge == 'top':                                              #if the zombie spawn on top side of screen
        x = random.randint(0, WIDTH)                            #take a random position
        y = 0
    elif edge == 'bottom':                                         #if the zombie spawns on bottom of the screen
        x = random.randint(0, WIDTH)                            #take a random position of the bottom side screen
        y = HEIGHT
    elif edge == 'left':                                           #if the zombie spawns on left of the screen
        x = 0                                                      #take a random position of the left side of screen
        y = random.randint(0, HEIGHT)
    elif edge == 'right':                                          #if the zombie spawns on right of the screen
        x = WIDTH                                                  #take a random position of the right side of the screen
        y = random.randint(0, HEIGHT)

    zombie = {
        "x": x,                                                   #x position of the zombie
        "y": y,                                                   #y position of the zombie
        "rect": zombie_img.get_rect(center=(x, y)),               #colision of the zombie in it center
        "angle": 0,                                               #starting angle of zombie
    }
    zombies.append(zombie)                                        #adding zombie in the empty list

# Button class for menu items
class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)                #creating a rectangle for the button
        self.text = text                                            #save and store the text of the button
        self.is_hovered = False                     #boolean to check if the mouse is on the rectangle of the button

    def draw(self, surface):
        color = GRAY if self.is_hovered else BLACK    #set the grey color for the button if the mouse is on it
        pygame.draw.rect(surface, color, self.rect, border_radius=12)  #draw the button rectangle with rounded corners
        pygame.draw.rect(surface, WHITE, self.rect, 2, border_radius=12)
        text_surface = menu_font.render(self.text, True, WHITE)  #render the button text
        text_rect = text_surface.get_rect(center=self.rect.center) #center the text in the button
        surface.blit(text_surface, text_rect) #draw the text onto the surface of rectangle

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:   #check if there is a mouse movement
            self.is_hovered = self.rect.collidepoint(event.pos)
            return False
        if event.type == pygame.MOUSEBUTTONDOWN and self.is_hovered:
            return True   #return true to say that a button has been clicked
        return False

# Load and save leaderboard
def load_leaderboard():
    try:
        with open('leaderboard.json', 'r') as f:  #trying reading the json file
            return json.load(f)
    except FileNotFoundError:                 #if there is jason file or no data in jason file , return an empty leadearboard
        return []

def save_leaderboard(leaderboard):
    # Sort before saving (always save in descending order)
    leaderboard.sort(key=lambda x: x['score'], reverse=True)
    with open('leaderboard.json', 'w') as f: # writing the sorted leaderboard to leaderboard.json
        json.dump(leaderboard, f)

def update_leaderboard(username, score):
    leaderboard = load_leaderboard()
    leaderboard.append({"username": username, "score": score})   #display the username with its score
    leaderboard.sort(key=lambda x: x["score"], reverse=True)     #sorting the leaderboard
    leaderboard = leaderboard[:10]  # Keep only top 10           #keep the top 10 best players
    save_leaderboard(leaderboard)   #save the leaderboard in json file

# Create menu buttons
main_menu_buttons = [
    Button(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 50, "Play"),   #play button in main menu
    Button(WIDTH // 2 - 100, HEIGHT // 2 + 20, 200, 50, "Leaderboard"),#leaderboard button in main menu
    Button(WIDTH // 2 - 100, HEIGHT // 2 + 90, 200, 50, "Quit")#quit button in main menu
]

game_over_buttons = [
    Button(WIDTH // 2 - 100, HEIGHT // 2 + 20, 200, 50, "Try Again"), #try again button in game over screen
    Button(WIDTH // 2 - 100, HEIGHT // 2 + 90, 200, 50, "Main Menu")  #main menu button in game over screen
]

leaderboard_buttons = [
    Button(WIDTH // 2 - 100, HEIGHT - 100, 200, 50, "Back to Menu"), #main menu button in leaderboard screen
    Button(WIDTH//2 - 100, HEIGHT - 160, 200, 50, "Toggle Sort")     #sorting button in leaderboard screen
]

# Input box for username
input_box = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 32)  #box to enter user username
input_text = ""  #empty space to let the user enter its username
input_active = False  #boolean to check if the box is active


def draw_login_screen():
    screen.fill(BLACK)  #fill the login screen in black
    title = title_font.render("Login", True, WHITE) # Use the title font to render the title text "Login" in white.
    title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 3))# Position the title text one-third of the way down the screen's height and centre it horizontally.
    screen.blit(title, title_rect) # Draw the title text onto the screen at the specified position

    pygame.draw.rect(screen, WHITE if input_active else GRAY, input_box, 2)
    text_surface = font.render(input_text, True, WHITE)# Adapt the input box's width dynamically to the text, making sure it remains at least 200 pixels wide.
    width = max(200, text_surface.get_width() + 10)# Modify the width attribute of the input box.
    input_box.w = width
    screen.blit(text_surface, (input_box.x + 5, input_box.y + 5)) # Place the produced text with a little margin inside the input field.

    prompt = font.render("Enter your username:", True, WHITE)# Adapt the input box's width dynamically to the text, making sure it remains at least 200 pixels wide.
    prompt_rect = prompt.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30))
    screen.blit(prompt, prompt_rect)# At the determined location, draw the prompt text onto the screen.


def draw_main_menu():
    screen.fill(BLACK)  #filling the screen main menu with black screen
    title = title_font.render("Zombie Shooter", True, WHITE)#render the title text in the main menu
    title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 4))
    screen.blit(title, title_rect)#draw the title text in the main menu

    for button in main_menu_buttons:
        button.draw(screen)

# Create a "Game Over" screen with a black backdrop and a red title towards the top.fill (BLACK)
def draw_game_over():
    screen.fill(BLACK)
    title = title_font.render("Game Over", True, RED)
    title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 4))
    screen.blit(title, title_rect)
# Use white text to centre the name of the active player on the screen.
    score_text = menu_font.render(f"Player: {current_player}", True, WHITE)
    score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
    screen.blit(score_text, score_rect)
    # Show the player's score in white lettering, centrally located just above the screen's centre.
    score_text = menu_font.render(f"Score: {current_score}", True, WHITE)
    score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    screen.blit(score_text, score_rect)
    # Use the game_over_buttons list to go through and draw every button on the game over screen.
    for button in game_over_buttons:
        button.draw(screen)

# Display the leaderboard screen with a dark backdrop and the scores sorted globally.
def draw_leaderboard():
    global sort_ascending
    screen.fill(BLACK)

    
    title = title_font.render("Leaderboard", True, WHITE) #render a title for leaderboard button
    title_rect = title.get_rect(center=(WIDTH // 2, 50))  #create a rectangle with rounded corners for the leaderboard button
    screen.blit(title, title_rect)

    # Draw sort order indicator if its from lowest to highest vice versa
    sort_text = menu_font.render(
        "Sort: " + ("Lowest to Highest" if sort_ascending else "Highest to Lowest"),
        True,
        WHITE
    )
    sort_rect = sort_text.get_rect(center=(WIDTH // 2, 100)) #creating the sort text
    screen.blit(sort_text, sort_rect)#displaying the sort text in the sort rectangle button

    # Draw and sort leaderboard
    leaderboard = load_leaderboard()
    leaderboard.sort(key=lambda x: x['score'], reverse=not sort_ascending)

    # Draw entries
    for i, entry in enumerate(leaderboard):# Loop through each entry in the leaderboard
        text = menu_font.render(            # Create a text space for each entry
            f"{i + 1}. {entry['username']}: {entry['score']}",# Format the text to show the score, rank, and username.
            True,
            WHITE
        )
        rect = text.get_rect(center=(WIDTH // 2, 150 + i * 40))
        screen.blit(text, rect)

    # Draw buttons
    for button in leaderboard_buttons:
        button.draw(screen)

#reset the game every time the user click on try again
def reset_game():
    global health, score, zombies, bullets
    health = 3 #3 hearts at the begining
    score = 0  #score reset at 0
    zombies = [] #zombie list empty
    bullets = [] #bullets list empty
    soldier_rect.center = (WIDTH // 1, HEIGHT // 1)


# Main Game Loop
running = True
while running:
    if current_state == GAME:
        if not pygame.mixer.music.get_busy():  # If no music is playing
            play_music() #play the game music
        screen.blit(background, (0, 0))# rendering the background image in the top left corner of the screen

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False                 #close the game
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    current_state = MAIN_MENU   #back to main menu if the key escape is pressed

        # keys for the soldier movements
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            soldier_rect.y -= 3  #if W is pressed add 3 to the y position of the soldier
        if keys[pygame.K_s]:
            soldier_rect.y += 3  #if S is pressed add -3 to the y position of the soldier
        if keys[pygame.K_a]:
            soldier_rect.x -= 3  #if A is pressed add -3 to the x position of the soldier
        if keys[pygame.K_d]:
            soldier_rect.x += 3  #if D is pressed add 3 to the x position of the soldier

        # Keep soldier on screen and blocking him from going outside the screen
        soldier_rect.x = max(0, min(WIDTH - soldier_rect.width, soldier_rect.x))
        soldier_rect.y = max(0, min(HEIGHT - soldier_rect.height, soldier_rect.y))

        # Calculating Mouse position and angle
        mouse_x, mouse_y = pygame.mouse.get_pos()
        angle = math.degrees(math.atan2(-(mouse_y - soldier_rect.centery), mouse_x - soldier_rect.centerx))

        # Rotate soldier
        rotated_soldier = pygame.transform.rotate(soldier, angle)           #rotate soldier depending on the position of the mouse
        soldier_pos = rotated_soldier.get_rect(center=soldier_rect.center) # Obtain a rectangle that is centred at the original soldier's position for the rotated soldier picture.
        screen.blit(rotated_soldier, soldier_pos)                           # Display the rotated soldier picture on the screen at the given location.


        # Shooting bullets
        if keys[pygame.K_SPACE] and time.time() - last_shot > shoot_cooldown:#check if The shoot_cooldown period is exceeded by the time since the last shot, guaranteeing a lag between shoots.
            bullet_dx = math.cos(math.radians(angle))# Calculate the bullet's movement direction along the x-axis
            bullet_dy = -math.sin(math.radians(angle))# Calculate the bullet's movement direction along the y-axis
            bullet_x = soldier_rect.centerx + 30 * bullet_dx# Find the initial x-coordinate of the bullet, 30 units away from the soldier's centre, in the direction of bullet_dx.
            bullet_y = soldier_rect.centery + 10 * bullet_dy # Find the initial y-coordinate of the bullet, 10 units away from the soldier's centre, in the direction of bullet_dy.
            bullets.append({"x": bullet_x, "y": bullet_y, "dx": bullet_dx, "dy": bullet_dy})   # Add the bullet's position and movement direction to the list of bullets
            last_shot = time.time() #update the last bullet shot time with the current time

        # Update bullets
        for bullet in bullets[:]:# Loop through each bullet in the list
            bullet["x"] += bullet["dx"] * bullet_speed# Move the bullet horizontally
            bullet["y"] += bullet["dy"] * bullet_speed# Move the bullet vertically

            if not (0 <= bullet["x"] <= WIDTH and 0 <= bullet["y"] <= HEIGHT):
                bullets.remove(bullet) #if the bullet is outside the screen , remove the bullet
            else:
                rotated_bullet = pygame.transform.rotate(bullet_img, angle)# Rotate the bullet image
                bullet_rect = rotated_bullet.get_rect(center=(bullet["x"], bullet["y"]))# Determine where the rotating bullet is.
                screen.blit(rotated_bullet, bullet_rect)# Draw the rotated bullet on the screen

        # Spawn zombies with cooldown
        if time.time() - last_zombie_spawn_time > zombie_spawn_cooldown:
            spawn_zombie()
            last_zombie_spawn_time = time.time()

        # Update zombies
        for zombie in zombies[:]:#looping throught each zombie
            dx = soldier_rect.centerx - zombie["x"]#calculate the horizontal distance between the zombie and soldier
            dy = soldier_rect.centery - zombie["y"]#calculate the vertical distance between the zombie and soldier
            dist = math.hypot(dx, dy)#get the distance to the soldier
            zombie["x"] += (dx / dist) * zombie_speed#move horizontally to the soldier
            zombie["y"] += (dy / dist) * zombie_speed#move vertically towards the soldier

            angle_to_soldier = math.degrees(math.atan2(-dy, dx))#calculate the angle to the soldier
            zombie["angle"] = angle_to_soldier#set and update the zombie angle to face directly the soldier

            rotated_zombie = pygame.transform.rotate(zombie_img, zombie["angle"]) # Rotate the zombie image
            zombie["rect"] = rotated_zombie.get_rect(center=(zombie["x"], zombie["y"]))# Set the zombie's position
            screen.blit(rotated_zombie, zombie["rect"])# Draw the rotated zombie on the screen

            # Collision with soldier
            if soldier_rect.colliderect(zombie["rect"]):
                health -= 1
                zombies.remove(zombie)
                if health <= 0:
                    current_score = score
                    update_leaderboard(current_player, current_score)
                    current_state = GAME_OVER

            # Collision with bullets
            for bullet in bullets[:]:
                if zombie["rect"].collidepoint(bullet["x"], bullet["y"]):
                    zombies.remove(zombie)
                    bullets.remove(bullet)
                    score += 1
                    play_sound_effect(Zombie_hit)


        # Draw hearts (health)
        for i in range(health):
            screen.blit(heart_img, (health_x + i * (heart_img.get_width() + 10), health_y))

        # Display Score
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (health_x, health_y + heart_img.get_height() + 10))

    elif current_state == LOGIN:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                input_active = input_box.collidepoint(event.pos)
            elif event.type == pygame.KEYDOWN:
                if input_active:
                    if event.key == pygame.K_RETURN and input_text.strip():
                        current_player = input_text
                        current_state = MAIN_MENU
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        input_text += event.unicode

        draw_login_screen()


    elif current_state == MAIN_MENU:
        stop_music()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            for i, button in enumerate(main_menu_buttons):
                if button.handle_event(event):
                    if i == 0:  # Play
                        reset_game()
                        current_state = GAME
                    elif i == 1:  # Leaderboard
                        current_state = LEADERBOARD
                    elif i == 2:  # Quit
                        running = False

        draw_main_menu()

    elif current_state == GAME_OVER:
        stop_music()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            for i, button in enumerate(game_over_buttons):
                if button.handle_event(event):
                    if i == 0:  # Try Again
                        reset_game()
                        current_state = GAME
                    elif i == 1:  # Main Menu
                        current_state = MAIN_MENU

        draw_game_over()

    elif current_state == LEADERBOARD:
        stop_music()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            for i, button in enumerate(leaderboard_buttons):
                if button.handle_event(event):
                    if i == 0:  # Back to Menu
                        current_state = MAIN_MENU
                    elif i == 1:  # Toggle Sort
                        sort_ascending = not sort_ascending

        draw_leaderboard()


    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()












































