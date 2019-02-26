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

def getRandomBlock():
    return Block(5, 0, random.randrange(0, 7))

def drawGrid(surface, grid):
    pygame.draw.rect(surface, (200, 0, 200), (grid_x, grid_y, grid_w, grid_h), 3)

    # 줄로 격자 나누기
    for i in range(1, len(grid)):
        row_y = grid_y + (i * blockSize)
        pygame.draw.line(surface, (160, 160, 160), (grid_x, row_y), (grid_x+grid_w, row_y))
        for j in range(1, len(grid[i])):
            col_x = grid_x + (j * blockSize)
            pygame.draw.line(surface, (160, 160, 160), (col_x, grid_y), (col_x, grid_y + grid_h))

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
                gameStart(surface)

    pygame.display.quit()


surface = pygame.display.set_mode((screen_w, screen_h))
pygame.display.set_caption('KiMiCa\'s Tetris')

menu(surface)