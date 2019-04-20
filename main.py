import pygame
import random
import copy
import enum
import os

from block import Block
from block import BlockType

pygame.init()

# colors
black = (0,0,0)
white = (255,255,255)
purple = (180,0,180)
gray = (160,160,160)
yellow = (150,150,0)
blueGray = (70,70,100)

# items
# item의 이미지들을 담고있는 list (index 1부터 유효함)
# item의 color 값에서 맨앞 숫자가 itemList의 인덱스임.
itemImgList = []
itemImgList.append(0)
# item을 구분하기 위해 color 맵을 이용함
plus1 = (1,0,0)
plus2 = (2,0,0)
minus1 = (3,0,0)
minus2 = (4,0,0)

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
grid_row = 25

# grid 시작 점 (x,y) 좌표 (왼쪽 위 꼭지점)
grid_x = (screen_w - grid_w) // 2
grid_y = (screen_h - grid_h) // 2

# 초당 프레임
gameFPS = 60
clock = pygame.time.Clock()

# 중력 레벨업 되는 시간
levelUpTime = 10

# 중력 레벨업시 배수
gravityMultiple = 0.7

class Conflict(enum.Enum):
    NONE = 0 # 충돌하지 않음
    TOP = 1
    BOTTOM = 2
    LEFT = 3
    RIGHT = 4
    BLOCK = 5

def getRandomBlock():
    return Block(1, 4, random.randrange(0, 7))

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
    pygame.draw.rect(surface, gray, surface.get_rect())
    if blockType == BlockType.I.value:
        pygame.draw.rect(surface, gray, surface.get_rect())
        for i in range(4):
            x = 1 + i*(nextBlockSize + inline_w)
            y = 1
            pygame.draw.rect(surface, color, (x, y, nextBlockSize, nextBlockSize))
    elif blockType == BlockType.O.value:
        pygame.draw.rect(surface, gray, surface.get_rect())
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
        pygame.draw.rect(surface, black, (0,0,21,21))
        pygame.draw.rect(surface, black, (43,0,21,21))
    elif blockType == BlockType.J.value:
        posList = [(0,0), (1,0), (1,1), (1,2)]
        for i in range(2):
            x = 1 + i*(nextBlockSize + inline_w)
            for j in range(3):
                y = 1 + j*(nextBlockSize + inline_w)
                if (i,j) in posList:
                    pygame.draw.rect(surface, color, (y, x, nextBlockSize, nextBlockSize))
        # 빈칸 검은색으로 채우기
        pygame.draw.rect(surface, black, (22,0,42,21))
    elif blockType == BlockType.L.value:
        posList = [(0,2), (1,0), (1,1), (1,2)]
        for i in range(2):
            x = 1 + i*(nextBlockSize + inline_w)
            for j in range(3):
                y = 1 + j*(nextBlockSize + inline_w)
                if (i,j) in posList:
                    pygame.draw.rect(surface, color, (y, x, nextBlockSize, nextBlockSize))
        # 빈칸 검은색으로 채우기
        pygame.draw.rect(surface, black, (0,0,42,21))
    elif blockType == BlockType.Z.value:
        posList = [(0,0), (0,1), (1,1), (1,2)]
        for i in range(2):
            x = 1 + i*(nextBlockSize + inline_w)
            for j in range(3):
                y = 1 + j*(nextBlockSize + inline_w)
                if (i,j) in posList:
                    pygame.draw.rect(surface, color, (y, x, nextBlockSize, nextBlockSize))
        # 빈칸 검은색으로 채우기
        pygame.draw.rect(surface, black, (43,0,21,21))
        pygame.draw.rect(surface, black, (0,22,21,21))
    elif blockType == BlockType.S.value:
        posList = [(0,1), (0,2), (1,0), (1,1)]
        for i in range(2):
            x = 1 + i*(nextBlockSize + inline_w)
            for j in range(3):
                y = 1 + j*(nextBlockSize + inline_w)
                if (i,j) in posList:
                    pygame.draw.rect(surface, color, (y, x, nextBlockSize, nextBlockSize))
        # 빈칸 검은색으로 채우기
        pygame.draw.rect(surface, black, (0,0,21,21))
        pygame.draw.rect(surface, black, (43,22,21,21))

def drawItemSlot(surface, itemList):
    # top
    pygame.draw.line(surface, purple, (surface.get_rect().left, surface.get_rect().top + 1) , (surface.get_rect().right, surface.get_rect().top + 1), outline_w)
    # left
    pygame.draw.line(surface, purple, (surface.get_rect().left + 1, surface.get_rect().top) , (surface.get_rect().left + 1, surface.get_rect().bottom - 3), outline_w)
    # bottom
    pygame.draw.line(surface, purple, (surface.get_rect().left, surface.get_rect().bottom - 2) , (surface.get_rect().right, surface.get_rect().bottom - 2), outline_w)
    # right
    pygame.draw.line(surface, purple, (surface.get_rect().right - 2, surface.get_rect().top) , (surface.get_rect().right - 2, surface.get_rect().bottom - 3), outline_w)

    for i in range(1,10):
        x = outline_w + i*blockSize + (i-1)*inline_w
        pygame.draw.line(surface, purple, (x, surface.get_rect().top) , (x, surface.get_rect().bottom))

    for i in range(len(itemList)):
        imgRect = itemImgList[itemList[i][0]].get_rect()
        imgRect.x = outline_w + i*(blockSize + inline_w)
        imgRect.y = outline_w
        surface.blit(itemImgList[itemList[i][0]], imgRect)

def isItem(block):
    if 0 < block[0] and block[0] < 50 and block[1] == 0 and block[2] == 0:
        return True
    return False

def drawGrid(surface, grid):
    # 회색 배경
    pygame.draw.rect(surface, gray, (3, 3, grid_w - (2*outline_w), grid_h - (2*outline_w)))

    for i in range(0, grid_row - 5):
        y = 3 + i * (inline_w + blockSize)
        for j in range(0, grid_col - 2):
            x = 3 + j * (inline_w + blockSize)
            if isItem(grid[i+4][j+1]):
                imgRect = itemImgList[grid[i+4][j+1][0]].get_rect()
                imgRect.x = x
                imgRect.y = y
                surface.blit(itemImgList[grid[i+4][j+1][0]], imgRect)
            else:
                pygame.draw.rect(surface, grid[i+4][j+1], (x, y, blockSize, blockSize))

    pygame.draw.rect(surface, purple, (0, 0, grid_w - outline_w, grid_h - outline_w), outline_w)

# grid는 각 칸마다 색 또는 아이템을 표현하는 값을 갖고있음.
def createGrid():
    grid = [[black for _ in range(grid_col)] for _ in range(grid_row)]
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

def createItemSlotSurface(surface):
    rectCenter = (screen_w/2, screen_h*8/9)
    rectWidth = grid_w
    rectHeight = blockSize + (2*outline_w)
    rect = surface.get_rect(w = rectWidth, h = rectHeight, center = rectCenter)

    return surface.subsurface(rect)

def isWall(block):
    if 0 < block[1] and block[1] < 5:
        return True
    return False

def isBlock(block):
    if (block[0] < 50 and block[1] == 0 and block[2] == 0) or isWall(block):
        return False
    return True

def createItemInGrid(grid):
    blockList = []

    for i in range(1, grid_row - 1):
        for j in range(1, grid_col - 1):
            if isBlock(grid[i][j]):
                blockList.append((i,j))

    # item을 만들 블럭이 없다면 리턴
    if len(blockList) == 0:
        return

    itemBlock = blockList[random.randrange(0, len(blockList))]
    itemNum = random.randrange(1,len(itemImgList))
    grid[itemBlock[0]][itemBlock[1]] = (itemNum, 0, 0)

# 충돌한 위치를 반환.
def checkConflict(grid, block, ignoreList = []):
    positions = getValidPositions(block)
    retList = []

    for pos in positions:
        if pos[0] >= 0 and pos[0] < grid_row and pos[1] >= 0 and pos[1] < grid_col:
            pixelColor = grid[pos[0]][pos[1]]
            if (Conflict.TOP not in ignoreList) and (pixelColor == (1,1,1)):
                retList.append(Conflict.TOP)
            if (Conflict.BOTTOM not in ignoreList) and (pixelColor == (2,2,2)):
                retList.append(Conflict.BOTTOM)
            if (Conflict.LEFT not in ignoreList) and (pixelColor == (3,3,3)):
                retList.append(Conflict.LEFT)
            if (Conflict.RIGHT not in ignoreList) and (pixelColor == (4,4,4)):
                retList.append(Conflict.RIGHT)
            if isBlock(pixelColor) or isItem(pixelColor) :
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

def fillDeletedLine(grid, x, num):
    for i in range(x, num, -1):
        grid[i] = copy.deepcopy(grid[i - num])

    for i in range(1, num + 1):
        grid[i] = [black for _ in range(grid_col)]
        grid[i][0] = (3,3,3)
        grid[i][11] = (4,4,4)

def deleteLine(grid, itemList):
    count = 0
    for i in range(1, grid_row - 1):
        delLine = False
        for j in range(1, grid_col - 1):
            if grid[i][j] != black:
                delLine = True
            else:
                delLine = False
                break

        if delLine:
            count += 1
            for j in range(1,11):
                if isItem(grid[i][j]) and len(itemList) < 10:
                    itemList.append(grid[i][j])
                grid[i][j] = black
            fillDeletedLine(grid, i, 1)
    return count

def getDroppedDistance(grid, block):
    tmpBlock = copy.deepcopy(block)
    while True:
        tmpBlock.x += 1
        if len(checkConflict(grid, tmpBlock, [Conflict.TOP])) != 0:
            tmpBlock.x -= 1
            break

    return tmpBlock.x - block.x

def checkFinish(grid, block):
    return len(checkConflict(grid, block, [Conflict.TOP])) != 0

def setGhostBlock(copiedGrid, currentBlock):
    ghostBlock = copy.deepcopy(currentBlock)
    ghostDistance = getDroppedDistance(copiedGrid, currentBlock)
    ghostBlock.x += ghostDistance
    ghostBlock.color = (70,70,70)

    return ghostBlock

def updateBlockBoxSurface(surface, block):
    pygame.draw.rect(surface, purple, (0, 0, nextBlockRect_w, nextBlockRect_w), outline_w)
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


def updateScreen(surface, gridSurface, nextBlockSurface, holdBlockSurface, itemSlotSurface, grid, nextBlock, holdBlock, itemList, score):
    surface.fill(black)

    drawGrid(gridSurface, grid)

    updateBlockBoxSurface(nextBlockSurface, nextBlock)
    updateBlockBoxSurface(holdBlockSurface, holdBlock)
    drawMessage(surface, "Ariel", 20, yellow, black, "Next Block", nextBlockRect_centerX, nextBlockRect_centerY - 85)
    drawMessage(surface, "Ariel", 20, yellow, black, "Hold Block", holdBlockRect_centerX, holdBlockRect_centerY - 85)

    drawItemSlot(itemSlotSurface, itemList)

    drawMessageCenter(surface, "Arial", 30, white, black, "SCORE : " + str(score), -360)
    pygame.display.flip()

# item 함수들

def lineUp(grid, num):
    for i in range(1, grid_row - num - 1):
        grid[i] = copy.deepcopy(grid[i+num])

    randPosition = random.randrange(1, grid_col - 2)
    for i in range(grid_row - 2, grid_row - 2 - num, -1):
        grid[i] = [blueGray for _ in range(grid_col)]
        grid[i][randPosition] = black
        grid[i][0] = (3,3,3)
        grid[i][11] = (4,4,4)

def lineDown(grid, num):
    fillDeletedLine(grid, 23, num)

def useItem(grid, item):
    if item[0] == 1:
        lineUp(grid, 1)
    elif item[0] == 2:
        lineUp(grid, 2)
    elif item[0] == 3:
        lineDown(grid,1)
    elif item[0] == 4:
        lineDown(grid,2)

def gameStart(surface):
    run = True
    grid = createGrid()
    copiedGrid = copy.deepcopy(grid)

    gridSurface = createGridSurface(surface)
    nextBlockSurface = createNextBlockSurface(surface)
    holdBlockSurface = createHoldBlockSurface(surface)
    itemSlotSurface = createItemSlotSurface(surface)

    currentBlock = getRandomBlock()
    ghostBlock = setGhostBlock(copiedGrid, currentBlock)

    nextBlock = getRandomBlock()
    holdBlock = None

    blockValidPositions = getValidPositions(currentBlock)
    ghostValidPositions = getValidPositions(ghostBlock)

    drawBlock(copiedGrid, ghostValidPositions, ghostBlock.color)
    drawBlock(copiedGrid, blockValidPositions, currentBlock.color)

    itemList = []

    score = 0
    updateScreen(surface, gridSurface, nextBlockSurface, holdBlockSurface, itemSlotSurface, copiedGrid, nextBlock, holdBlock, itemList, score)

    # 회전이나 좌우 이동에 성공했을때 블럭이 바닥에 고정되지 않게 해준다.
    infinity = 0

    pygame.key.set_repeat(200, 50)
    # 최초 2초에 한칸!
    dropSpeed = 2
    # 떨어지는 시간 관리
    dropTime = 0
    # 떨어지는 단계 시간 관리
    dropLevelTime = 0
    delayTime = 0

    comboStack = 0
    tetrisComboStack = 0

    while run:
        clock.tick(gameFPS)
        droppedBlock = False
        # 1/1000 sec
        delayTime += clock.get_time()
        dropLevelTime += clock.get_time()

        if (delayTime / 1000) > dropSpeed:
            currentBlock.x += 1
            if len(checkConflict(grid, currentBlock, [Conflict.TOP])) != 0:
                currentBlock.x -= 1
                if (delayTime - infinity) / 1000 > dropSpeed:
                    droppedBlock = True
                    delayTime = 0
                    infinity = 0
            else:
                delayTime = 0
                infinity = 0

        if (dropLevelTime / 1000) > levelUpTime:
            dropLevelTime = 0
            dropSpeed = dropSpeed * gravityMultiple

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
                    else:
                        infinity = delayTime
                elif event.key == pygame.K_RIGHT:
                    currentBlock.y += 1
                    if len(checkConflict(grid, currentBlock, [Conflict.BOTTOM, Conflict.TOP])) != 0:
                        currentBlock.y -= 1
                    else:
                        infinity = delayTime
                elif event.key == pygame.K_UP:
                    currentBlock.rotation = (currentBlock.rotation + 1) % len(currentBlock.block)
                    conflictTypeList = checkConflict(grid, currentBlock,[Conflict.TOP])
                    if len(conflictTypeList) != 0:
                        if Conflict.LEFT in conflictTypeList:
                            if checkLeftRotationConflict(grid, currentBlock):
                                infinity = delayTime
                        elif Conflict.RIGHT in conflictTypeList:
                            if checkRightRotationConflict(grid, currentBlock):
                                infinity = delayTime
                        elif Conflict.BLOCK in conflictTypeList or Conflict.BOTTOM in conflictTypeList:
                            # 블럭과 충돌이면 일단 위로한칸 올려보고 안되면 왼쪽오른쪽 해본다.
                            currentBlock.x -= 1
                            if len(checkConflict(grid, currentBlock, [Conflict.TOP])) != 0:
                                currentBlock.x += 1

                                if checkLeftRotationConflict(grid, currentBlock):
                                    infinity = delayTime
                                    break
                                currentBlock.rotation = (currentBlock.rotation + 1) % len(currentBlock.block)
                                if checkRightRotationConflict(grid, currentBlock):
                                    infinity = delayTime
                                    break
                            else:
                                infinity = delayTime
                    else:
                        infinity = delayTime
                elif event.key == pygame.K_1:
                    if 0 < len(itemList):
                        useItem(grid, itemList.pop(0))
                        copiedGrid = copy.deepcopy(grid)

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
            delLineCount = deleteLine(grid, itemList)

            if delLineCount > 0:
                comboStack += 1
                if delLineCount == 4:
                    tetrisComboStack += 1
                else:
                    tetrisComboStack = 0
                randNum = random.randrange(0,10)
                # TODO : Test를 위해 아이템 생성률을 100%로 해둠. 나중에 적절한 수치로 수정해야함.
                if randNum >= 0:
                    createItemInGrid(grid)
            else:
                comboStack = 0

            if delLineCount == 4:
                # tetris(4줄을 한번에 없애는 것)는 점수 2배
                score += delLineCount * 10 * 2 * comboStack * tetrisComboStack
            else:
                score += delLineCount * 10 * comboStack

        updateScreen(surface, gridSurface, nextBlockSurface, holdBlockSurface, itemSlotSurface, copiedGrid, nextBlock, holdBlock, itemList, score)

        if checkFinish(grid, currentBlock):
            drawMessageCenter(surface, "Arial", 40, white, (40, 40, 40), "Game Over! Gga Bi!")
            drawMessageCenter(surface, "Arial", 40, white, (40, 40, 40), "Press ESC to go to the menu", 50)
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
        surface.fill(black) # 메뉴 창 검정색 바탕
        drawMessageCenter(surface, "Arial", 20, white, black,  "Press Any Key...")

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

# image Load
plus1Img = pygame.image.load(os.path.join('img', 'plus1.png')).convert()
plus1Img = pygame.transform.scale(plus1Img, (30, 30))
plus2Img = pygame.image.load(os.path.join('img', 'plus2.png')).convert()
plus2Img = pygame.transform.scale(plus2Img, (30, 30))
minus1Img = pygame.image.load(os.path.join('img', 'minus1.png')).convert()
minus1Img = pygame.transform.scale(minus1Img, (30, 30))
minus2Img = pygame.image.load(os.path.join('img', 'minus2.png')).convert()
minus2Img = pygame.transform.scale(minus2Img, (30, 30))

itemImgList.append(plus1Img)
itemImgList.append(plus2Img)
itemImgList.append(minus1Img)
itemImgList.append(minus2Img)

menu(surface)
