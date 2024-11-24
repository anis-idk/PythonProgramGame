import pygame  #library used to create games
import math    #import math module to use mathematical operations like trigonometry , angles ...
import random  #makes the game more unpredictable, for example, by allowing zombies to appear at random points
import time    #offers time-related features, such as the ability to get the current cooldown or delay time.
import os      #manages file paths, enabling the loading of resources and images from designated directories.
import json    #Used for to store data (saved data) , used especially for leaderbord


pygame.init() #launches every Pygame like the sounds, graphics modules...
pygame.font.init()   #initialize the font module

WIDTH, HEIGHT = 800, 600 #defines the dimensions of the screen
FPS = 60                 #frame rate per second
screen = pygame.display.set_mode((WIDTH, HEIGHT)) #creates the game window
