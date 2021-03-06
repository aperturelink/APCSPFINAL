"""Module for managing platforms"""
import pygame
from spritesheet_functions import SpriteSheet

# These constants define our platform types:
#   Name of file
#   X location of sprite
#   Y location of sprite
#   Width of sprite
#   Height of sprite

GROUND_BLOCK = (0, 16, 16, 16)
VERT_BRICK_LINE = (17, 16, 16, 16)
VERT_BRICK_NOLINE = (33, 16, 16, 16)
EMPTY_BLOCK = (49, 16, 16, 16)
BRICK = (272, 16, 16, 16)
OTHER_BRICK = (288, 16, 16, 16)
COIN_BLOCK_YELLOW = (384, 16, 16, 16)
COIN_BLOCK_BROWN =(400, 16, 16, 16)
COIN_BLOCK_DARK_BROWN = (416, 16, 16, 16)
EMPTY_BLOCK_TWO = (432, 16, 16, 16)
STAIRCASE_BRICK = (0, 32, 16, 16)
WEIRD_BRICK = (1, 32, 16, 16)
GREEN_PIPE_BOTTOM =( 3, 160 , 28, 16 )
GREEN_PIPE_TOP = ( 1, 143 , 33, 15)

class Platform(pygame.sprite.Sprite):
    """Platform the user can jump on"""

    def __init__(self, sprite_sheet_data):
        """ Platformer Construction. Assumes constructed with user passing in
        an array of 5 numbers like what's defined at the top of this code."""
        super(Platform, self).__init__()

        sprite_sheet = SpriteSheet("resources\graphics\Tileset.png")
        #Grab the image for this platform
        self.image = sprite_sheet.get_image(sprite_sheet_data[0],
                                            sprite_sheet_data[1],
                                            sprite_sheet_data[2],
                                            sprite_sheet_data[3])
        self.rect = self.image.get_rect()

class MovingPlatform(Platform):
    """Platform that can move but I don't need it"""

    def __init__(self, sprite_sheet_data):
        super(MovingPlatform, self).__init__(sprite_sheet_data)

        self.change_x = 0
        self.change_y = 0

        self.boundary_top = 0
        self.boundary_bottom = 0
        self.boundary_left = 0
        self.boundary_right = 0

        self.level = None
        self.player = None

    def update(self):
        """ Move the platform.
                  If the player is in the way, it will shove the player
                  out of the way. This does NOT handle what happens if a
                  platform shoves a player into another object. Make sure
                  moving platforms have clearance to push the player around
                  or add code to handle what happens if they don't. """
        # Move left/right
        self.rect.x += self.change_x

        # See if we hit the player
        hit = pygame.sprite.collide_rect(self, self.player)
        if hit:
            # We did hit the player. Shove the player around and
            # assume he/she won't hit anything else.

            # If we are moving right, set our right side
            # to the left side of the item we hit
            if self.change_x < 0:
                self.player.rect.right = self.rect.left
            else:
                # Otherwise if we are moving left, do the opposite.
                self.player.rect.left = self.rect.right

        # Move up/down
        self.rect.y += self.change_y

        # Check and see if we the player
        hit = pygame.sprite.collide_rect(self, self.player)
        if hit:
            # We did hit the player. Shove the player around and
            # assume he/she won't hit anything else.

            # Reset our position based on the top/bottom of the object.
            if self.change_y < 0:
                self.player.rect.bottom = self.rect.top
            else:
                self.player.rect.top = self.rect.bottom

        # Check the boundaries and see if we need to reverse
        # direction.
        if self.rect.bottom > self.boundary_bottom or self.rect.top < self.boundary_top:
            self.change_y *= -1

        cur_pos = self.rect.x - self.level.world_shift
        if cur_pos < self.boundary_left or cur_pos > self.boundary_right:
            self.change_x *= -1