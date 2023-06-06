import os
import random
import pygame
import math
from os import listdir
from os.path import isfile, join

pygame.init()

pygame.display.set_caption("Platformer")  # set window title

WIDTH, HEIGHT = 1000, 800
FPS = 60
PLAYER_VEL = 5

window = pygame.display.set_mode((WIDTH, HEIGHT))  # create window


def flip(sprites):  # flip sprites
    return [
        pygame.transform.flip(sprite, True, False) for sprite in sprites
    ]  # flip sprites


def load_sprite_sheets(dir1, dir2, width, height, direction=False):  # load sprite sheet
    path = join(
        "assets", dir1, dir2
    )  # path to spritesheet, change to whatever folder you have your sprites in
    images = [
        f for f in listdir(path) if isfile(join(path, f))
    ]  # get all images in spritesheet, change to whatever folder you have your sprites in

    all_sprites = {}  # list of sprites,
    for image in images:
        sprite_sheet = pygame.image.load(
            join(path, image)
        ).convert_alpha()  # load sprite sheet, conver to alpha for transparency

        sprites = []
        for i in range(sprite_sheet.get_width() // width):
            surface = pygame.Surface(
                (width, height), pygame.SRCALPHA, 32
            )  # create surface, used to cut out individual sprites, SRCALPHA for transparency.
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0, 0), rect)  # draw sprite on surface
            sprites.append(
                pygame.transform.scale2x(surface)
            )  # add sprite to list of sprites

        if direction:
            all_sprites[image.replace(".png", "") + "_right"] = sprites
            all_sprites[image.replace(".png", "") + "_left"] = flip(sprites)
        else:
            all_sprites[image.replace(".png", "")] = sprites

    return all_sprites


def get_block(size):
    path = join("assets", "Terrain", "Terrain.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(
        96, 64, size, size
    )  # 96, 85 is the top left corner of the block in the sprite sheet. Adjust accordingly
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)


class Player(pygame.sprite.Sprite):
    COLOR = (255, 0, 0)  # player color
    GRAVITY = 1  # gravity constant
    SPRITES = load_sprite_sheets("MainCharacters", "NinjaFrog", 32, 32, True)
    ANIMATION_DELAY = 3  # how long to wait before changing animation frame

    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)  # create rect
        self.x_vel = 0  # x velocity
        self.y_vel = 0  # y velocity
        self.mask = None  # mask for collision
        self.direction = "left"  # direction player is facing
        self.animation_count = 0  # current animation frame
        self.fall_count = 0  # current fall frame, how long we have been falling
        self.jump_count = 0  # current jump frame, how long we have been jumping

    def jump(self):
        self.y_vel = -self.GRAVITY * 8  # set y velocity to negative because going up
        self.animation_count = 0  # reset animation count
        self.jump_count += 1  # increment jump count
        if self.jump_count == 1:
            self.fall_count = 0

    def move(self, dx, dy):
        self.rect.x += dx  # move x
        self.rect.y += dy  # move y

    def move_left(self, vel):
        self.x_vel = -vel  # set velocity. Negative because moving left
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self, vel):
        self.x_vel = vel  # set velocity. Positive because moving right
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    def loop(self, fps):
        self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)
        self.move(self.x_vel, self.y_vel)  # move player
        self.fall_count += 1  # increment fall count
        self.update_sprite()  # update sprite

    def landed(self):
        self.fall_count = 0  # reset fall count
        self.y_vel = 0  # reset y velocity
        self.jump_count = 0  # reset jump count

    def hit_head(self):
        self.count = 0
        self.y_vel *= -1

    def update_sprite(self):
        sprite_sheet = "idle"
        if self.hit:
            sprite_sheet = "hit"
        elif self.y_vel < 0:
            if self.jump_count == 1:
                sprite_sheet = "jump"
            elif self.jump_count == 2:
                sprite_sheet = "double_jump"
        elif self.y_vel > self.GRAVITY * 2:
            sprite_sheet = "fall"
        elif self.x_vel != 0:
            sprite_sheet = "run"

        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.update()

    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)

    def draw(self, win):
        win.blit(self.sprite, (self.rect.x, self.rect.y))  # draw sprite


class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)  # create rect
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)  # create surface
        self.width = width  # width of object
        self.height = height  # height of object
        self.name = name  # name of object

    def draw(self, window, offset_x):
        window.blit(self.image, (self.rect.x - offset_x, self.rect.y))


class Block(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        block = get_block(size)
        self.image.blit(block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)


def get_background(name):
    image = pygame.image.load(join("assets", "Background", name))  # load image
    _, _, width, height = image.get_rect()  # get image dimensions
    tiles = []  # list of tiles

    for i in range(WIDTH // width + 1):  # loop through x axis
        for j in range(HEIGHT // height + 1):  # loop through y axis
            pos = (i * width, j * height)  # position of tile
            tiles.append(pos)  # add tile to list
    return tiles, image  # return list of tiles and image


def draw(window, background, bg_image, player, objects, offset_x):
    for tile in background:
        window.blit(bg_image, tile)  # draw background

    for object in objects:
        object.draw(window, offset_x)  # draw objects

    player.draw(window, offset_x)  # draw player

    pygame.display.update()  # update display


def handle_vertical_collision(player, objects, dy):
    collided_objects = []

    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            if dy > 0:
                player.rect.bottom = obj.rect.top
                player.landed()
            elif dy < 0:
                player.rect.top = obj.rect.bottom
                player.hit_head()
        collided_objects.append(obj)
    return collided_objects


def handle_move(player, objects):
    keys = pygame.key.get_pressed()  # get all pressed keys

    player.x_vel = 0  # reset x velocity. If we dont do this, the player will keep moving after we let go of the key
    if keys[pygame.K_a]:
        player.move_left(PLAYER_VEL)  # move left
    if keys[pygame.K_d]:
        player.move_right(PLAYER_VEL)  # move right

    handle_vertical_collision(
        player, objects, player.y_vel
    )  # handle vertical collision


def main(window):  # main function
    clock = pygame.time.Clock()  # create clock
    background, bg_image = get_background(
        "Yellow.png"
    )  # get background, change to whatever background you want

    block_size = 96

    player = Player(100, 100, 50, 50)  # create player
    floor = [
        Block(i * block_size, HEIGHT - block_size, block_size)
        for i in range(-WIDTH // block_size, WIDTH * 2 // block_size)
    ]

    offset_x = 0
    scroll_area_width = 200

    run = True  # main loop variable
    while run:  # main loop
        clock.tick(
            FPS
        )  # set FPS, used to regulate framerate accross different computers

        for event in pygame.event.get():  # get all events
            if event.type == pygame.QUIT:  # if the user clicks the X button
                run = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.jump_count < 2:
                    player.jump()

        player.loop(FPS)  # loop player
        handle_move(player, floor)  # handle player movement
        draw(window, background, bg_image, player, floor, offset_x)  # draw background

        if (
            player.rect.right - offset_x >= WIDTH - scroll_area_width
            and player.x_vel > 0
        ) or (player.rect.left - offset_x <= scroll_area_width and player.x_vel < 0):
            offset_x += player.x_vel

    pygame.quit()  # quit pygame
    quit()  # quit python


if __name__ == "__main__":  # if the file is being run directly
    main(window)  # run the main function
