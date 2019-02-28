import pygame
import random

from block import Block

pygame.init()

screen_w = 700
screen_h = 900

grid_w = 10 * 30
grid_h = 20 * 30

# grid 시작 점 (x,y) 좌표 (왼쪽 위 꼭지점)
grid_x = (screen_w - grid_w) // 2
grid_y = (screen_h - grid_h) // 2

blockSize = 30
# 테두리 두께
outline_w = 3
# 내부 선 두께
inline_w = 1

def getRandomBlock():
    return Block(5, 0, random.randrange(0, 7))

def drawGrid(surface, grid):
    # 회색 배경
    pygame.draw.rect(surface, (160, 160, 160), (grid_x, grid_y, grid_w + 8 * inline_w, grid_h + 18 * inline_w))

    for i in range(len(grid)):
        y = grid_y + (i * (inline_w + blockSize))
        for j in range(len(grid[i])):
            x = grid_x + (j * (inline_w + blockSize))
            pygame.draw.rect(surface, grid[i][j], (x, y, blockSize, blockSize))

    pygame.draw.rect(surface, (180, 0, 180), (grid_x - 3, grid_y - 3, grid_w + (8 * inline_w) + 6, grid_h + (18 * inline_w) + 6), outline_w)
    
# grid는 한 칸에 표현할 색을 갖고있음.
def createGrid():
    return [[(0,0,0) for _ in range(10)] for _ in range(20)]

def updateScreen(surface, grid):
    surface.fill((0,0,0))

    drawGrid(surface, grid)
    pygame.display.flip()

def gameStart(surface):

    run = True
    grid = createGrid()
    currentBlock = getRandomBlock()

    while run:

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False

        updateScreen(surface, grid)

def menu(surface):
    run = True

    while run:
        surface.fill((0,0,0)) # 메뉴 창 검정색 바탕

        font = pygame.font.SysFont("Arial", 20)
        # 둥근 모서리로 흰색 글자 그리기
        textBox = font.render("Press Any Key ...", 1, (255, 255, 255))
        surface.blit(textBox, (350, 450))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    break
                gameStart(surface)

    pygame.display.quit()


surface = pygame.display.set_mode((screen_w, screen_h))
pygame.display.set_caption('KiMiCa\'s Tetris')

menu(surface)
