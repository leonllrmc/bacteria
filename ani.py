# ANI stands for ArtificialNonIntelligence, it's inspired from Zelda 1 enemies AI
import random


class ANI:
    def __init__(self, entity_max_speed: int):
        """
        :type entity_max_speed: int
        :param entity_max_speed: the max speed the entity should go
        """
        self.action_tick = 0  # ticks before next action
        self.direction = 0  # direction of the entity 0: right, 1: down, 2: left, 3: up
        self.speed = 0  # speed of the entity
        self.max_speed = entity_max_speed

    def update(self):
        if self.action_tick <= 0:
            self.action_tick = random.randint(10, 250)
            self.direction = random.randint(0, 3)
            self.speed = random.randint(0, self.max_speed)
        else:
            self.action_tick -= 1

        return self.direction, self.speed
