import sys
import pygame
from utils import path as p


def run_credits(screen, clock):
    credit = True
    font = pygame.font.Font(p('/assets/font/PrStart.ttf'), 22)

    credits_strs = [
        "leonllr: main developer",
        "Ds: lead developer",
        "ScriptlineStudios: lead developer"
    ]

    while credit:
        clock.tick(30)
        screen.fill((0, 0, 0))

        for credit_str in credits_strs:
            i = credits_strs.index(credit_str) + 1
            img = font.render(credit_str, False, (255, 255, 255))
            screen.blit(img, (400 - (img.get_width() // 2), i * img.get_height() * 2))
        screen.blit(font.render("Press Esc to exit", False, (255, 255, 255)), (400 - (img.get_width() // 2), len(credits_strs) * img.get_height() * 3))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    credit = False
