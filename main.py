import os
import random
import pygame
import math
from os import listdir
from os.path import isfile, join
pygame.init()

pygame.display.set_caption("Platformer") # set window title


class Player(pygame.sprite.Sprite): 
    COLOR = (255, 0, 0) # player color
    
    def __init__(self,x,y,width,height):
        self.rect = pygame.Rect(x,y,width,height) # create rect
        self.x_vel = 0 # x velocity
        self.y_vel = 0 # y velocity
        self.mask = None # mask for collision
        self.direction =  "left" # direction player is facing
        self.animation_count = 0 # current animation frame


    def move(self, dx, dy):
        self.rect.x += dx # move x
        self.rect.y += dy # move y

    def move_left(self,vel):
        self.x_vel = -vel # set velocity. Negative because moving left
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self,vel): 
        self.x_vel = vel   # set velocity. Positive because moving right
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    def loop(self,fps):
        self.move(self.x_vel, self.y_vel) # move player
    
    def draw(self,win):
        pygame.draw.rect(win, self.COLOR, self.rect) # draw player

WIDTH,HEIGHT = 1000, 800
FPS = 60
PLAYER_VEL = 5

window = pygame.display.set_mode((WIDTH, HEIGHT)) # create window

def get_background(name): 
    image = pygame.image.load(join("assets", "Background", name)) # load image
    _,_, width, height = image.get_rect() # get image dimensions
    tiles = [] # list of tiles

    for i in range(WIDTH// width +1): # loop through x axis
        for j in range(HEIGHT// height +1): # loop through y axis
            pos = (i * width, j * height) # position of tile
            tiles.append(pos) # add tile to list
    return tiles, image # return list of tiles and image


def draw(window,background, bg_image, player) :
    for tile in background:
        window.blit(bg_image, tile) # draw background
    
    player.draw(window) # draw player

    pygame.display.update() # update display


def handle_move(player):
    keys = pygame.key.get_pressed() # get all pressed keys

    player.x_vel = 0 # reset x velocity. If we dont do this, the player will keep moving after we let go of the key
    if keys[pygame.K_a]:
        player.move_left(PLAYER_VEL) # move left
    if keys[pygame.K_d]:
        player.move_right(PLAYER_VEL) # move right    

def main(window): # main function
    clock = pygame.time.Clock() # create clock
    background, bg_image = get_background("Blue.png") # get background, change to whatever background you want

    player = Player(100, 100, 50, 50) # create player

    run = True # main loop variable
    while run : # main loop
        clock.tick(FPS) # set FPS, used to regulate framerate accross different computers

        for event in pygame.event.get(): # get all events
            if event.type == pygame.QUIT: # if the user clicks the X button
                run = False
                break

        player.loop(FPS) # loop player
        handle_move(player) # handle player movement
        draw(window, background, bg_image, player) # draw background

    pygame.quit() # quit pygame
    quit() # quit python    

if __name__ == "__main__":  # if the file is being run directly
    main(window)        # run the main function

