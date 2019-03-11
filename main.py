import pygame
import random
import copy
import enum

from block import Block

pygame.init()

screen_w = 700
screen_h = 900

blockSize = 30
# 테두리 두께
outline_w = 3
# 내부 선 두께
inline_w = 1

grid_w = (10*blockSize) + (9*inline_w) + (2*outline_w)
grid_h = (20*blockSize) + (19*inline_w) + (2*outline_w)

grid_col = 12
grid_row = 22

# grid 시작 점 (x,y) 좌표 (왼쪽 위 꼭지점)
grid_x = (screen_w - grid_w) // 2
grid_y = (screen_h - grid_h) // 2

# 초당 프레임
gameFPS = 30
clock = pygame.time.Clock()

class Conflict(enum.Enum):
    NONE = 0 # 충돌하지 않음
    TOP = 1
    BOTTOM = 2
    LEFT = 3
    RIGHT = 4
    BLOCK = 5

def getRandomBlock():
    return Block(-2, 3, random.randrange(0, 7))

def drawSubsurface(surface, subSurface, centerX, centerY):
    rect = subSurface.get_rect()
    rect.center = (centerX, centerY)

    surface.blit(subSurface, rect)

def drawObjectCenter(surface, obj, adjX = 0, adjY = 0):
    centerX = screen_w // 2 + adjX
    centerY = screen_h // 2 + adjY
    drawSubsurface(surface, obj, centerX, centerY)

def drawMessageCenter(surface, fontName, fontSize, fontColor, bgColor, msg, adjY = 0):
    font = pygame.font.SysFont(fontName, fontSize)
    # 둥근 모서리로 흰색 글자 그리기
    textBox = font.render(msg, True, fontColor, bgColor)
    drawObjectCenter(surface, textBox, 0, adjY)

def drawMessage(surface, fontName, fontSize, fontColor, bgColor, msg, msgX, msgY):
    font = pygame.font.SysFont(fontName, fontSize)
    # 둥근 모서리로 흰색 글자 그리기
    textBox = font.render(msg, True, fontColor, bgColor)
    drawObjectCenter(surface, textBox, 0, adjY)

# 블럭 영역에서 실제로 블럭이 그려질 좌표 list 반환
def getValidPositions(block):
    positions = []
    for i in range(5):
        for j in range(5):
            if block.block[block.rotation][i][j] == 'X':
                positions.append((i + block.x, j + block.y))
    return positions

def drawBlock(grid, positions, color):
    for pos in positions:
        if pos[0] >= 0:
            grid[pos[0]][pos[1]] = color

def drawGrid(surface, grid):
    # 회색 배경
    pygame.draw.rect(surface, (160, 160, 160), (3, 3, grid_w - (2*outline_w), grid_h - (2*outline_w)))

    for i in range(0, grid_row - 2):
        y = 3 + i * (inline_w + blockSize)
        for j in range(0, grid_col - 2):
            x = 3 + j * (inline_w + blockSize)
            pygame.draw.rect(surface, grid[i+1][j+1], (x, y, blockSize, blockSize))

    pygame.draw.rect(surface, (180, 0, 180), (0, 0, grid_w - outline_w, grid_h - outline_w), outline_w)

# grid는 한 칸에 표현할 색을 갖고있음.
def createGrid():
    grid = [[(0,0,0) for _ in range(grid_col)] for _ in range(grid_row)]
    for i in range(grid_row):
        for j in range(grid_col):
            # TOP wall
            if i == 0:
                grid[i][j] = (1,1,1)

            # BOTTOM wall
            if i == grid_row - 1:
                grid[i][j] = (2,2,2)

            # LEFT, RIGHT를 뒤에 배치시켜서 각꼭지점의 경우 LEFT와 RIGHT로 구분 되도록 했음. ex) grid[0][0]의 경우 LEFT와 TOP의 영역을 공유하는데 LEFT로 설정되도록함.
            # LEFT wall
            if j == 0:
                grid[i][j] = (3,3,3)

            # RIGHT wall
            if j == grid_col - 1:
                grid[i][j] = (4,4,4)

    return grid

def createGridSurface(surface):
    rectCenter = (screen_w/2, screen_h/2)
    rectWidth = grid_w
    rectHeight = grid_h
    rect = surface.get_rect(w = rectWidth, h = rectHeight, center = rectCenter)
    gridSurface = surface.subsurface(rect)

    return gridSurface

def createNextBlockSurface(surface):
    rectWidth = (((screen_w - grid_w) // 2) * 0.70) // 1
    rectHeight = rectW
    rectX = ((screen_w + grid_w) // 2) + ((((screen_w - grid_w) / 2) - rectW) // 2)
    rectY = (screen_h * 0.25) // 1

# 충돌한 위치를 반환.
def checkConflict(grid, block, ignoreList = []):
    positions = getValidPositions(block)

    for pos in positions:
        if pos[0] >= 0 and pos[1] >= 0:
            pixelColor = grid[pos[0]][pos[1]]
            if (Conflict.TOP not in ignoreList) and (pixelColor == (1,1,1)):
                return Conflict.TOP
            if (Conflict.BOTTOM not in ignoreList) and (pixelColor == (2,2,2)):
                return Conflict.BOTTOM
            if (Conflict.LEFT not in ignoreList) and (pixelColor == (3,3,3)):
                return Conflict.LEFT
            if (Conflict.RIGHT not in ignoreList) and (pixelColor == (4,4,4)):
                return Conflict.RIGHT
            if pixelColor[0] > 4 or pixelColor[1] > 4 or pixelColor[2] > 4:
                return Conflict.BLOCK

    return Conflict.NONE

def fillDeletedLine(grid, x):
    for i in range(x, 1, -1):
        grid[i] = copy.deepcopy(grid[i - 1])
    grid[0] = [(1,1,1) for _ in range(grid_col)]
    grid[0][0] = (3,3,3)
    grid[0][11] = (4,4,4)

def deleteLine(grid):
    for i in range(1, 21):
        delLine = False
        for j in range(1, 11):
            if grid[i][j] != (0,0,0):
                delLine = True
            else:
                delLine = False
                break

        if delLine:
            for j in range(1,11):
                grid[i][j] = (0,0,0)
            fillDeletedLine(grid, i)

def getDroppedDistance(grid, block):
    tmpBlock = copy.deepcopy(block)
    while True:
        tmpBlock.x += 1
        if checkConflict(grid, tmpBlock, [Conflict.TOP]) != Conflict.NONE:
            tmpBlock.x -= 1
            break

    return tmpBlock.x - block.x

def checkFinish(grid):
    for i in range(1,11):
        if grid[0][i] != (1,1,1):
            return True
    return False

def updateNextBlock(surface, nextBlock):
    rectW = (((screen_w - grid_w) // 2) * 0.70) // 1
    rectH = rectW
    rectX = ((screen_w + grid_w) // 2) + ((((screen_w - grid_w) / 2) - rectW) // 2)
    rectY = (screen_h * 0.25) // 1
    pygame.draw.rect(surface, (100, 0, 100), (rectX, rectY, rectW, rectH), outline_w)

    drawMessageCenter(surface, "Arial", 26, (80, 100, 160), (0, 0, 0), "Next Block", 50)

def updateScreen(surface, gridSurface, grid):
    surface.fill((0,0,0))

    drawGrid(gridSurface, grid)

    updateNextBlock(surface, 0)
    pygame.display.flip()

def gameStart(surface):
    run = True
    grid = createGrid()
    gridSurface = createGridSurface(surface)

    currentBlock = getRandomBlock()
    nextBlock = getRandomBlock()

    blockValidPositions = getValidPositions(currentBlock)
    copiedGrid = copy.deepcopy(grid)

    drawBlock(copiedGrid, blockValidPositions, currentBlock.color)

    updateScreen(surface, gridSurface, copiedGrid)

    # 최초 2초에 한칸!
    dropSpeed = 2
    # 떨어지는 시간 관리
    dropTime = 0
    # 떨어지는 단계 시간 관리
    dropLevelTime = 0
    delayTime = 0
    while run:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    break

#    while run:
#        clock.tick(gameFPS)
#        droppedBlock = False
#        # 1/1000 sec
#        delayTime += clock.get_time()
#        dropLevelTime += clock.get_time()
#
#        if (delayTime / 1000) > dropSpeed:
#            delayTime = 0
#            currentBlock.x += 1
#            if checkConflict(grid, currentBlock, [Conflict.TOP]) != Conflict.NONE:
#                currentBlock.x -= 1
#                droppedBlock = True
#
#        if (dropLevelTime / 1000) > 10:
#            dropLevelTime = 0
#            dropSpeed = dropSpeed * 0.7
#
#        for event in pygame.event.get():
#            if event.type == pygame.KEYDOWN:
#                if event.key == pygame.K_ESCAPE:
#                    run = False
#                    break
#                elif event.key == pygame.K_SPACE:
#                    distance = getDroppedDistance(copiedGrid, currentBlock)
#                    currentBlock.x += distance
#                    droppedBlock = True
#                elif event.key == pygame.K_DOWN:
#                    currentBlock.x += 1
#                    if checkConflict(grid, currentBlock, [Conflict.TOP]) != Conflict.NONE:
#                        currentBlock.x -= 1
#                        droppedBlock = True
#                elif event.key == pygame.K_LEFT:
#                    currentBlock.y -= 1
#                    if checkConflict(grid, currentBlock, [Conflict.BOTTOM, Conflict.TOP]) != Conflict.NONE:
#                        currentBlock.y += 1
#                elif event.key == pygame.K_RIGHT:
#                    currentBlock.y += 1
#                    if checkConflict(grid, currentBlock, [Conflict.BOTTOM, Conflict.TOP]) != Conflict.NONE:
#                        currentBlock.y -= 1
#                elif event.key == pygame.K_UP:
#                    currentBlock.rotation = (currentBlock.rotation + 1) % len(currentBlock.block)
#                    if checkConflict(grid, currentBlock,[Conflict.TOP]) != Conflict.NONE:
#                        currentBlock.rotation = (currentBlock.rotation - 1 + len(currentBlock.block)) % len(currentBlock.block)
#
#        blockValidPositions = getValidPositions(currentBlock)
#        drawBlock(copiedGrid, blockValidPositions, currentBlock.color)
#
#
#        if droppedBlock:
#            currentBlock = nextBlock
#            nextBlock = getRandomBlock()
#            grid = copy.deepcopy(copiedGrid)
#            deleteLine(grid)
#
#        updateScreen(surface, copiedGrid)
#
#        if checkFinish(grid):
#            drawMessageCenter(surface, "Arial", 40, (255, 255, 255), (40, 40, 40), "Game Over! Gga Bi!")
#            drawMessageCenter(surface, "Arial", 40, (255, 255, 255), (40, 40, 40), "Press ESC to go to the menu", 50)
#            pygame.display.flip()
#            while run:
#                for event in pygame.event.get():
#                    if event.type == pygame.KEYDOWN:
#                        if event.key == pygame.K_ESCAPE:
#                            run = False
#                            break
#
#        copiedGrid = copy.deepcopy(grid)

def menu(surface):
    run = True

    while run:
        surface.fill((0,0,0)) # 메뉴 창 검정색 바탕
        drawMessageCenter(surface, "Arial", 20, (255, 255, 255), (0, 0, 0),  "Press Any Key...")

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
