import math
from pygame.math import Vector2
import utils
import pygame
import animator as anim
from utils import path as p
from pygame.rect import Rect
from utils import collision_side


def bl(n):
    return pygame.transform.flip(pygame.image.load(p('/assets/textures/' + f'bacteria_{n}.png')), True, False)


class Entity:
    def __init__(self, x: int, y: int, animator=None, texture: pygame.Surface = None):
        self.x = x
        self.y = y
        self.animator = animator
        self.texture = texture
        self.vX = 0
        self.vY = 0

    def render(self, screen: pygame.Surface, delta_time: float = 0.1, rotation: int = 0, animate_frame: bool = True):
        if self.animator is not None:
            img = self.animator.update(delta_time, animate_frame)
        elif self.texture is not None:
            img = self.texture
        else:
            raise ValueError('You must provide either an animator or a texture')

        if rotation != 0:
            img = pygame.transform.rotate(img, rotation)

        screen.blit(img, (self.x, self.y))

    def update(self, delta_time: float):
        self.x += self.vX
        self.vY += self.vY


class Player(Entity):
    """
    note - direction: int from 0 to 3
    """

    def __init__(self):
        self.tick = 0
        self.direction = 0
        self.speed = 6
        super().__init__(75, 75, anim.Sin((bl(1), bl(2), bl(3)), 300))

    def render(self, screen: pygame.Surface, delta_time: float, map_buf, offset: Vector2):
        use_anim = False
        if abs(self.vX) > 0 or abs(self.vY) > 0:
            use_anim = True

        self.update(delta_time, map_buf, offset)

        super().render(screen, delta_time, self.direction * 90, use_anim)
        utils.draw_rect_frame(screen, (0, 0, 255), Rect(self.x, self.y, 35, 35))
        for col in map_buf:
            for tile in col:
                if 'collision' in tile and tile['collision'] is True:
                    utils.draw_rect_frame(screen, (255, 0, 0),
                                          Rect((tile['x'] - offset.x) * 32, (tile['y'] - offset.y) * 32, 32, 32))

    def update(self, delta_time: float, map_buf, offset: Vector2):
        self.tick += 1
        if self.tick >= 30:
            self.tick = 0
        self.update_collision(map_buf, delta_time, offset)
        self.x += math.floor(abs(math.sin((self.tick * delta_time / 0.3) + 5)) * self.vX)
        self.y += math.floor(abs(math.sin((self.tick * delta_time / 0.3) + 5)) * self.vY)

    def update_collision(self, map_buf, delta_time: float, offset: Vector2):
        for col in map_buf:
            for tile in col:
                if 'collision' in tile and tile['collision'] is True:
                    if 'collision_condition' in tile and not exec(tile['collision_condition'], self):
                        continue
                    x, y = (tile['x'] - offset.x) * 32, (tile['y'] - offset.y) * 32
                    collide_box = Rect(self.x, self.y, 35, 35)
                    collision_directions = collision_side(collide_box, Rect(x, y, 32, 32))
                    if len(collision_directions) < 1:
                        continue
                    # print(f'collision with tile at {collide_tile["x"] * math.floor(16*1.5)}, {collide_tile["y"] * math.floor(16*1.5)} on side {collision_direction} link is at {player.x}, {player.y}')
                    if 'bottom' in collision_directions:
                        self.y += self.speed
                    if 'left' in collision_directions:
                        self.x -= self.speed
                    if 'right' in collision_directions:
                        self.x += self.speed
                    if 'top' in collision_directions:
                        self.y -= self.speed
