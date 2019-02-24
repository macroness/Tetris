import pygame

pygame.init()

screen_w = 700
screen_h = 900

win = pygame.display.set_mode((screen_w, screen_h))
pygame.display.set_caption('KiMiCa\'s Tetris')

run = True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        pygame.display.update()