import os

# This class handles sprite sheets
# This was taken from www.scriptefun.com/transcript-2-using
# sprite-sheets-and-drawing-the-background
# I've added some code to fail if the file wasn't found..
# Note: When calling images_at the rect is the format:
# (x, y, x + offset, y + offset)

import pygame


class Spritesheet(object):
    def __init__(self, filename):
        try:
            self.sheet = pygame.image.load(filename).convert()
        except pygame.error as e:
            print('Unable to load spritesheet image:', filename)
            raise SystemExit(e)

    # Load a specific image from a specific rectangle
    def image_at(self, rectangle, colorkey=None):
        """Loads image from x,y,x+offset,y+offset"""
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image

    # Load a whole bunch of images and return them as a list
    def images_at(self, rects, colorkey=None):
        """Loads multiple images, supply a list of coordinates"""
        return [self.image_at(rect, colorkey) for rect in rects]

    # Load a whole strip of images
    def load_strip(self, rect, image_count, colorkey=None):
        "Loads a strip of images and returns them as a list"
        tups = [(rect[0] + rect[2] * x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, colorkey)


def path(p: str):
    return os.getcwd() + p.replace('/', os.path.sep)

def draw_rect_frame(screen, color, rect):
    pygame.draw.line(screen, color, rect.topleft, rect.topright)
    pygame.draw.line(screen, color, rect.bottomleft, rect.bottomright)
    pygame.draw.line(screen, color, rect.topleft, rect.bottomleft)
    pygame.draw.line(screen, color, rect.topright, rect.bottomright)

def collision_side(rect1, rect2):
    if not rect1.colliderect(rect2):
        return [] # False
    """
    :param rect1: pygame.Rect
    :param rect2: pygame.Rect
    :return: a list of collision side
    """
    collision_side = []
    if rect1.left < rect2.right < rect1.right:
        collision_side.append('right')
    if rect1.left < rect2.left < rect1.right:
        collision_side.append('left')
    if rect1.top < rect2.bottom < rect1.bottom:
        collision_side.append('bottom')
    if rect1.top < rect2.top < rect1.bottom:
        collision_side.append('top')
    return collision_side