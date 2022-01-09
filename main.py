import math
import sys
import time
import pygame
import entity
from credits import run_credits
from utils import path as p
from pygame.math import Vector2
from map import load_map, render_tile

pygame.init()

screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption('Bacteria')
clock = pygame.time.Clock()

bg = pygame.image.load(p('/assets/textures/bg_test.jpg')).convert()

bacteria = entity.Player()

tile_offset = Vector2((0, 0))

font = pygame.font.Font(p('/assets/font/PrStart.ttf'), 16)

map_buf = load_map(0)

run_credits(screen, clock)

while True:
    dt = clock.tick(30)
    dt /= 1000

    screen.fill((0, 0, 0))

    screen.blit(bg, ((-tile_offset[0]) * 32, (-tile_offset[1]) * 32))

    if bacteria.x > 795:
        bacteria.x = 0
        tile_offset.x += 25
    elif bacteria.x < -5:
        bacteria.x = 795
        tile_offset.x -= 25
    elif bacteria.y > 795:
        bacteria.y = 0
        tile_offset.y += 25
    elif bacteria.y < -5:
        bacteria.y = 795
        tile_offset.y -= 25

    bacteria.render(screen, dt, map_buf, tile_offset)

    for x in range(0, len(map_buf)):
        for y in range(0, len(map_buf[0])):
            render_tile(screen, map_buf[x][y], tile_offset)

    screen.blit(font.render('%.4s Fps' % clock.get_fps(), False, (255, 255, 255)), (5, 5))
    screen.blit(font.render('Scrolling: {0}:{1}'.format(*tile_offset), False, (255, 255, 255)), (5, 25))
    screen.blit(font.render('Pos: {0}:{1}'.format(bacteria.x, bacteria.y), False, (255, 255, 255)), (5, 45))

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                bacteria.vX = bacteria.speed
                bacteria.direction = 0
            elif event.key == pygame.K_LEFT:
                bacteria.vX = -bacteria.speed
                bacteria.direction = 2
            elif event.key == pygame.K_UP:
                bacteria.vY = -bacteria.speed
                bacteria.direction = 1
            elif event.key == pygame.K_DOWN:
                bacteria.vY = bacteria.speed
                bacteria.direction = 3
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit(0)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                bacteria.vX = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                bacteria.vY = 0
