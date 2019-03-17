import pygame
import random
import copy
import enum

from block import Block
from block import BlockType

pygame.init()

screen_w = 700
screen_h = 900

blockSize = 30
nextBlockSize = 20
# 테두리 두께
outline_w = 3
# 내부 선 두께
inline_w = 1

grid_w = (10*blockSize) + (9*inline_w) + (2*outline_w)
grid_h = (20*blockSize) + (19*inline_w) + (2*outline_w)

nextBlockRect_w = ((((screen_w - grid_w) // 2) * 0.70) + outline_w) // 1
nextBlockRect_h = nextBlockRect_w

nextBlockRect_centerX = (((screen_w - grid_w) * 0.75) + grid_w) // 1
nextBlockRect_centerY = (screen_h * 0.3) // 1

holdBlockRect_w = nextBlockRect_w
holdBlockRect_h = nextBlockRect_h

holdBlockRect_centerX = ((screen_w - grid_w) * 0.25) // 1
holdBlockRect_centerY = nextBlockRect_centerY

grid_col = 12
grid_row = 22

# grid 시작 점 (x,y) 좌표 (왼쪽 위 꼭지점)
grid_x = (screen_w - grid_w) // 2
grid_y = (screen_h - grid_h) // 2

# 초당 프레임
gameFPS = 60
clock = pygame.time.Clock()

class Conflict(enum.Enum):
    NONE = 0 # 충돌하지 않음
    TOP = 1
    BOTTOM = 2
    LEFT = 3
    RIGHT = 4
    BLOCK = 5

def getRandomBlock():
    return Block(-2, 4, random.randrange(0, 7))

def drawSubsurface(surface, subsurface, centerX, centerY):
    rect = subsurface.get_rect()
    rect.center = (centerX, centerY)

    surface.blit(subsurface, rect)

def drawSubsurfaceCenter(surface, subSurface, adjX = 0, adjY = 0):
    centerX = screen_w // 2 + adjX
    centerY = screen_h // 2 + adjY
    drawSubsurface(surface, subSurface, centerX, centerY)

def drawMessageCenter(surface, fontName, fontSize, fontColor, bgColor, msg, adjY = 0):
    font = pygame.font.SysFont(fontName, fontSize)
    # 둥근 모서리로 흰색 글자 그리기
    textBox = font.render(msg, True, fontColor, bgColor)
    drawSubsurfaceCenter(surface, textBox, 0, adjY)

def drawMessage(surface, fontName, fontSize, fontColor, bgColor, msg, centerX, centerY):
    font = pygame.font.SysFont(fontName, fontSize)
    # 둥근 모서리로 흰색 글자 그리기
    textBox = font.render(msg, True, fontColor, bgColor)
    drawSubsurface(surface, textBox, centerX, centerY)

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

def drawBlockBox(surface, blockType, color):
    pygame.draw.rect(surface, (160,160,160), surface.get_rect())
    if blockType == BlockType.I.value:
        pygame.draw.rect(surface, (160,160,160), surface.get_rect())
        for i in range(4):
            x = 1 + i*(nextBlockSize + inline_w)
            y = 1
            pygame.draw.rect(surface, color, (x, y, nextBlockSize, nextBlockSize))
    elif blockType == BlockType.O.value:
        pygame.draw.rect(surface, (160,160,160), surface.get_rect())
        for i in range(2):
            x = 1 + i*(nextBlockSize + inline_w)
            for j in range(2):
                y = 1 + j*(nextBlockSize + inline_w)
                pygame.draw.rect(surface, color, (x, y, nextBlockSize, nextBlockSize))
    elif blockType == BlockType.T.value:
        posList = [(0,1), (1,0), (1,1), (1,2)]
        for i in range(2):
            x = 1 + i*(nextBlockSize + inline_w)
            for j in range(3):
                y = 1 + j*(nextBlockSize + inline_w)
                if (i,j) in posList:
                    pygame.draw.rect(surface, color, (y, x, nextBlockSize, nextBlockSize))
        # 빈칸 검은색으로 채우기
        pygame.draw.rect(surface, (0,0,0), (0,0,21,21))
        pygame.draw.rect(surface, (0,0,0), (43,0,21,21))
    elif blockType == BlockType.J.value:
        posList = [(0,0), (1,0), (1,1), (1,2)]
        for i in range(2):
            x = 1 + i*(nextBlockSize + inline_w)
            for j in range(3):
                y = 1 + j*(nextBlockSize + inline_w)
                if (i,j) in posList:
                    pygame.draw.rect(surface, color, (y, x, nextBlockSize, nextBlockSize))
        # 빈칸 검은색으로 채우기
        pygame.draw.rect(surface, (0,0,0), (22,0,42,21))
    elif blockType == BlockType.L.value:
        posList = [(0,2), (1,0), (1,1), (1,2)]
        for i in range(2):
            x = 1 + i*(nextBlockSize + inline_w)
            for j in range(3):
                y = 1 + j*(nextBlockSize + inline_w)
                if (i,j) in posList:
                    pygame.draw.rect(surface, color, (y, x, nextBlockSize, nextBlockSize))
        # 빈칸 검은색으로 채우기
        pygame.draw.rect(surface, (0,0,0), (0,0,42,21))
    elif blockType == BlockType.Z.value:
        posList = [(0,0), (0,1), (1,1), (1,2)]
        for i in range(2):
            x = 1 + i*(nextBlockSize + inline_w)
            for j in range(3):
                y = 1 + j*(nextBlockSize + inline_w)
                if (i,j) in posList:
                    pygame.draw.rect(surface, color, (y, x, nextBlockSize, nextBlockSize))
        # 빈칸 검은색으로 채우기
        pygame.draw.rect(surface, (0,0,0), (43,0,21,21))
        pygame.draw.rect(surface, (0,0,0), (0,22,21,21))
    elif blockType == BlockType.S.value:
        posList = [(0,1), (0,2), (1,0), (1,1)]
        for i in range(2):
            x = 1 + i*(nextBlockSize + inline_w)
            for j in range(3):
                y = 1 + j*(nextBlockSize + inline_w)
                if (i,j) in posList:
                    pygame.draw.rect(surface, color, (y, x, nextBlockSize, nextBlockSize))
        # 빈칸 검은색으로 채우기
        pygame.draw.rect(surface, (0,0,0), (0,0,21,21))
        pygame.draw.rect(surface, (0,0,0), (43,22,21,21))

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

    return surface.subsurface(rect)

def createNextBlockSurface(surface):
    rect = surface.get_rect(w = nextBlockRect_w, h = nextBlockRect_h, center = (nextBlockRect_centerX, nextBlockRect_centerY))

    return surface.subsurface(rect)

def createHoldBlockSurface(surface):
    rect = surface.get_rect(w = holdBlockRect_w, h = holdBlockRect_h, center = (holdBlockRect_centerX, holdBlockRect_centerY))

    return surface.subsurface(rect)

# 충돌한 위치를 반환.
def checkConflict(grid, block, ignoreList = []):
    positions = getValidPositions(block)
    retList = []

    for pos in positions:
        if pos[0] >= 0 and pos[0] < 22 and pos[1] >= 0 and pos[1] < 12:
            pixelColor = grid[pos[0]][pos[1]]
            if (Conflict.TOP not in ignoreList) and (pixelColor == (1,1,1)):
                retList.append(Conflict.TOP)
            if (Conflict.BOTTOM not in ignoreList) and (pixelColor == (2,2,2)):
                retList.append(Conflict.BOTTOM)
            if (Conflict.LEFT not in ignoreList) and (pixelColor == (3,3,3)):
                retList.append(Conflict.LEFT)
            if (Conflict.RIGHT not in ignoreList) and (pixelColor == (4,4,4)):
                retList.append(Conflict.RIGHT)
            if pixelColor[0] > 4 or pixelColor[1] > 4 or pixelColor[2] > 4:
                retList.append(Conflict.BLOCK)

    return retList

def checkRightRotationConflict(grid, currentBlock):
    adjustX = 0
    adjustY = 0
    if currentBlock.blockType == BlockType.I.value:
        adjustY = -2
    else:
        adjustY = -1
    currentBlock.y += adjustY
    conflictTypeList = checkConflict(grid, currentBlock, [Conflict.TOP])
    # 왼쪽으로 한 칸 갔는데도 블럭과 충돌이나면 위로도 보내본다.
    if len(conflictTypeList) != 0:
        adjustX = -1
        currentBlock.x += adjustX
        if len(checkConflict(grid, currentBlock, [Conflict.TOP])) != 0:
            # 위로도 보내봤는데 충돌나면 다시 원래 위치로.
            currentBlock.x -= adjustX
            currentBlock.y -= adjustY
            currentBlock.rotation = (currentBlock.rotation - 1 + len(currentBlock.block)) % len(currentBlock.block)
            return False
    return True

def checkLeftRotationConflict(grid, currentBlock):
    adjustY = 1
    currentBlock.y += adjustY
    conflictTypeList = checkConflict(grid, currentBlock, [Conflict.TOP])
    # 오른쪽으로 한 칸 갔는데도 블럭과 충돌이나면 위로도 보내본다.
    if len(conflictTypeList) != 0:
        adjustX = -1
        currentBlock.x += adjustX
        if len(checkConflict(grid, currentBlock, [Conflict.TOP])) != 0:
            # 위로도 보내봤는데 충돌나면 다시 원래 위치로.
            currentBlock.x -= adjustX
            currentBlock.y -= adjustY
            currentBlock.rotation = (currentBlock.rotation - 1 + len(currentBlock.block)) % len(currentBlock.block)
            return False
    return True

def fillDeletedLine(grid, x):
    for i in range(x, 1, -1):
        grid[i] = copy.deepcopy(grid[i - 1])
    grid[0] = [(1,1,1) for _ in range(grid_col)]
    grid[0][0] = (3,3,3)
    grid[0][11] = (4,4,4)

def deleteLine(grid):
    count = 0
    for i in range(1, 21):
        delLine = False
        for j in range(1, 11):
            if grid[i][j] != (0,0,0):
                delLine = True
            else:
                delLine = False
                break

        if delLine:
            count += 1
            for j in range(1,11):
                grid[i][j] = (0,0,0)
            fillDeletedLine(grid, i)
    return count

def getDroppedDistance(grid, block):
    tmpBlock = copy.deepcopy(block)
    while True:
        tmpBlock.x += 1
        if len(checkConflict(grid, tmpBlock, [Conflict.TOP])) != 0:
            tmpBlock.x -= 1
            break

    return tmpBlock.x - block.x

def checkFinish(grid):
    for i in range(1,11):
        if grid[0][i] != (1,1,1):
            return True
    return False

def setGhostBlock(copiedGrid, currentBlock):
    ghostBlock = copy.deepcopy(currentBlock)
    ghostDistance = getDroppedDistance(copiedGrid, currentBlock)
    ghostBlock.x += ghostDistance
    ghostBlock.color = (70,70,70)

    return ghostBlock

def updateBlockBoxSurface(surface, block):
    pygame.draw.rect(surface, (100, 0, 100), (0, 0, nextBlockRect_w, nextBlockRect_w), outline_w)
    if block == None:
        return

    centerX = nextBlockRect_w // 2
    centerY = nextBlockRect_h // 2

    width = 0
    height = 0
    if block.blockType == BlockType.I.value:
        width = (4*nextBlockSize) + (5*inline_w)
        height = (1*nextBlockSize) + (2*inline_w)
    elif block.blockType == BlockType.O.value:
        width = (2*nextBlockSize) + (3*inline_w)
        height = width
    else:
        width = (3*nextBlockSize) + (4*inline_w)
        height = (2*nextBlockSize) + (3*inline_w)
    rect = surface.get_rect(w = width, h = height, center = (centerX, centerY))
    drawBlockBox(surface.subsurface(rect), block.blockType, block.color)


def updateScreen(surface, gridSurface, nextBlockSurface, holdBlockSurface, grid, nextBlock, holdBlock, score):
    surface.fill((0,0,0))

    drawGrid(gridSurface, grid)

    updateBlockBoxSurface(nextBlockSurface, nextBlock)
    updateBlockBoxSurface(holdBlockSurface, holdBlock)
    drawMessage(surface, "Ariel", 20, (150,150,0), (0,0,0), "Next Block", nextBlockRect_centerX, nextBlockRect_centerY - 85)
    drawMessage(surface, "Ariel", 20, (150,150,0), (0,0,0), "Hold Block", holdBlockRect_centerX, holdBlockRect_centerY - 85)

    drawMessageCenter(surface, "Arial", 30, (255, 255, 255), (0, 0, 0), "SCORE : " + str(score), -360)
    pygame.display.flip()

def gameStart(surface):
    run = True
    grid = createGrid()
    copiedGrid = copy.deepcopy(grid)

    gridSurface = createGridSurface(surface)
    nextBlockSurface = createNextBlockSurface(surface)
    holdBlockSurface = createHoldBlockSurface(surface)

    currentBlock = getRandomBlock()
    ghostBlock = setGhostBlock(copiedGrid, currentBlock)

    nextBlock = getRandomBlock()
    holdBlock = None

    blockValidPositions = getValidPositions(currentBlock)
    ghostValidPositions = getValidPositions(ghostBlock)

    drawBlock(copiedGrid, ghostValidPositions, ghostBlock.color)
    drawBlock(copiedGrid, blockValidPositions, currentBlock.color)

    score = 0
    updateScreen(surface, gridSurface, nextBlockSurface, holdBlockSurface, copiedGrid, nextBlock, holdBlock, score)

    pygame.key.set_repeat(200, 50)
    # 최초 2초에 한칸!
    dropSpeed = 2
    # 떨어지는 시간 관리
    dropTime = 0
    # 떨어지는 단계 시간 관리
    dropLevelTime = 0
    delayTime = 0

    while run:
        clock.tick(gameFPS)
        droppedBlock = False
        # 1/1000 sec
        delayTime += clock.get_time()
        dropLevelTime += clock.get_time()

        if (delayTime / 1000) > dropSpeed:
            delayTime = 0
            currentBlock.x += 1
            if len(checkConflict(grid, currentBlock, [Conflict.TOP])) != 0:
                currentBlock.x -= 1
                droppedBlock = True

        if (dropLevelTime / 1000) > 10:
            dropLevelTime = 0
            dropSpeed = dropSpeed * 0.7

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    break
                elif event.key == pygame.K_SPACE:
                    distance = getDroppedDistance(copiedGrid, currentBlock)
                    currentBlock.x += distance
                    droppedBlock = True
                elif event.key == pygame.K_LSHIFT:
                    if holdBlock == None:
                        holdBlock = currentBlock
                        currentBlock = nextBlock
                        nextBlock = getRandomBlock()
                    else:
                        tmpBlock = holdBlock
                        holdBlock = currentBlock
                        currentBlock = tmpBlock
                    holdBlock.x = -2
                    holdBlock.y = 4
                    holdBlock.rotation = 0

                elif event.key == pygame.K_DOWN:
                    currentBlock.x += 1
                    if len(checkConflict(grid, currentBlock, [Conflict.TOP])) != 0:
                        currentBlock.x -= 1
                        droppedBlock = True
                elif event.key == pygame.K_LEFT:
                    currentBlock.y -= 1
                    if len(checkConflict(grid, currentBlock, [Conflict.BOTTOM, Conflict.TOP])) != 0:
                        currentBlock.y += 1
                elif event.key == pygame.K_RIGHT:
                    currentBlock.y += 1
                    if len(checkConflict(grid, currentBlock, [Conflict.BOTTOM, Conflict.TOP])) != 0:
                        currentBlock.y -= 1
                elif event.key == pygame.K_UP:
                    currentBlock.rotation = (currentBlock.rotation + 1) % len(currentBlock.block)
#                    if len(checkConflict(grid, currentBlock,[Conflict.TOP])) != 0:
#                        currentBlock.rotation = (currentBlock.rotation - 1 + len(currentBlock.block)) % len(currentBlock.block)
                    conflictTypeList = checkConflict(grid, currentBlock,[Conflict.TOP])
                    if len(conflictTypeList) != 0:
                        if Conflict.LEFT in conflictTypeList:
                            checkLeftRotationConflict(grid, currentBlock)
                        elif Conflict.RIGHT in conflictTypeList:
                            checkRightRotationConflict(grid, currentBlock)
                        elif Conflict.BLOCK in conflictTypeList:
                            # 블럭과 충돌이면 일단 위로한칸 올려보고 안되면 왼쪽오른쪽 해본다.
                            currentBlock.x -= 1
                            if len(checkConflict(grid, currentBlock, [Conflict.TOP])) != 0:
                                currentBlock.x += 1

                                if checkLeftRotationConflict(grid, currentBlock):
                                    break
                                currentBlock.rotation = (currentBlock.rotation + 1) % len(currentBlock.block)
                                if checkRightRotationConflict(grid, currentBlock):
                                    break

                ghostBlock = setGhostBlock(copiedGrid, currentBlock)

        blockValidPositions = getValidPositions(currentBlock)
        ghostValidPositions = getValidPositions(ghostBlock)
        drawBlock(copiedGrid, ghostValidPositions, ghostBlock.color)
        drawBlock(copiedGrid, blockValidPositions, currentBlock.color)

        if droppedBlock:
            currentBlock = nextBlock
            ghostBlock = setGhostBlock(copiedGrid, currentBlock)

            nextBlock = getRandomBlock()
            grid = copy.deepcopy(copiedGrid)
            delLineCount = deleteLine(grid)
            if delLineCount == 4:
                # tetris(4줄을 한번에 없애는 것)는 점수 2배
                score += delLineCount * 10 * 2
            else:
                score += delLineCount * 10

        updateScreen(surface, gridSurface, nextBlockSurface, holdBlockSurface, copiedGrid, nextBlock, holdBlock, score)

        if checkFinish(grid):
            drawMessageCenter(surface, "Arial", 40, (255, 255, 255), (40, 40, 40), "Game Over! Gga Bi!")
            drawMessageCenter(surface, "Arial", 40, (255, 255, 255), (40, 40, 40), "Press ESC to go to the menu", 50)
            pygame.display.flip()
            while run:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            run = False
                            break

        copiedGrid = copy.deepcopy(grid)

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
