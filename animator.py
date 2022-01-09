from typing import Tuple
import pygame
import math


class Sin:
    def __init__(self, frames: Tuple[pygame.Surface, ...], delay: int):
        """
        :param frames: list of pygame images
        :param delay: delay between frames in milliseconds
        """
        self.frames = frames
        self.delay = delay
        self.tick = 0

    def update(self, delta_time: float, animate_frame: bool = True) -> pygame.Surface:
        """
        :param animate_frame: if False, skip animation for this frame
        :param delta_time: delta time in seconds
        """
        self.tick += 1
        if self.tick >= 30:
            self.tick = 0
        if not animate_frame:
            self.tick -= 1

        i = math.floor(abs(math.sin(self.tick * delta_time / (self.delay / 1000))) * (len(self.frames) - 1))
        return self.frames[i]
