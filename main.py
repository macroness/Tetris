import pygame
import random
import copy
import enum
import os
import wave
import pyaudio
import sys

from block import Block
from block import BlockType

pygame.init()

screen_w = 700
screen_h = 900

surface = pygame.display.set_mode((screen_w, screen_h))
pygame.display.set_caption('KiMiCa\'s Tetris')

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# TODO : UserState에 grid류도 다 넣자.
class UserState:
    def __init__(self):
        self.reverseLR = False
        self.swappedBlock = False
        self.changeBgm()
        return super().__init__()

    def checkMusicFinish(self):
        return pygame.mixer.music.get_busy() == False

    def changeBgm(self):
        pygame.mixer.music.stop()
        num = random.randrange(0, len(bgmPathList))
        pygame.mixer.music.load(bgmPathList[num])
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play()

    def stopBgm(self):
        pygame.mixer.music.fadeout(1000)

    def isSwappedBlock(self):
        return self.swappedBlock

    def setSwappedBlock(self, checker):
        self.swappedBlock = checker

# menu imageList
# index 0   : 현재 선택된 menu의 index
# index 1 ~ : 각 메뉴의 img들
menuImgList = []

# menu images
selectedNormalModePlayImg = pygame.image.load(resource_path(os.path.join('img', 'selectedNormalModePlay.png'))).convert()
selectedNormalModePlayImg = pygame.transform.scale(selectedNormalModePlayImg, (301, 60))
unselectedNormalModePlayImg = pygame.image.load(resource_path(os.path.join('img', 'unselectedNormalModePlay.png'))).convert()
unselectedNormalModePlayImg = pygame.transform.scale(unselectedNormalModePlayImg, (301, 60))
selectedMarathonModePlayImg = pygame.image.load(resource_path(os.path.join('img', 'selectedMarathonModePlay.png'))).convert()
selectedMarathonModePlayImg = pygame.transform.scale(selectedMarathonModePlayImg, (301, 60))
unselectedMarathonModePlayImg = pygame.image.load(resource_path(os.path.join('img', 'unselectedMarathonModePlay.png'))).convert()
unselectedMarathonModePlayImg = pygame.transform.scale(unselectedMarathonModePlayImg, (301, 60))
selectedGameFinishImg = pygame.image.load(resource_path(os.path.join('img', 'selectedGameFinish.png'))).convert()
selectedGameFinishImg = pygame.transform.scale(selectedGameFinishImg, (301, 60))
unselectedGameFinishImg = pygame.image.load(resource_path(os.path.join('img', 'unselectedGameFinish.png'))).convert()
unselectedGameFinishImg = pygame.transform.scale(unselectedGameFinishImg, (301, 60))
selectedOpInfoImg = pygame.image.load(resource_path(os.path.join('img', 'selectedOpInfo.png'))).convert()
selectedOpInfoImg = pygame.transform.scale(selectedOpInfoImg, (301, 60))
unselectedOpInfoImg = pygame.image.load(resource_path(os.path.join('img', 'unselectedOpInfo.png'))).convert()
unselectedOpInfoImg = pygame.transform.scale(unselectedOpInfoImg, (301, 60))

#menu explain images
normalModeExplainImg =  pygame.image.load(resource_path(os.path.join('img', 'normalModeExplain.png'))).convert()
normalModeExplainImg = pygame.transform.scale(normalModeExplainImg, (250, 50))
marathonModeExplainImg =  pygame.image.load(resource_path(os.path.join('img', 'marathonModeExplain.png'))).convert()
marathonModeExplainImg = pygame.transform.scale(marathonModeExplainImg, (250, 50))
operationExplainImg =  pygame.image.load(resource_path(os.path.join('img', 'operationExplain.png'))).convert()
operationExplainImg = pygame.transform.scale(operationExplainImg, (250, 50))
finishExplainImg =  pygame.image.load(resource_path(os.path.join('img', 'finishExplain.png'))).convert()
finishExplainImg = pygame.transform.scale(finishExplainImg, (250, 50))

# operation Information page image
opInfoImg = pygame.image.load(resource_path(os.path.join('img', 'operationInfoPage.png'))).convert()
opInfoImg = pygame.transform.scale(opInfoImg, (644, 600))

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

# item image load
plus1Img = pygame.image.load(resource_path(os.path.join('img', 'plus1.png'))).convert()
plus1Img = pygame.transform.scale(plus1Img, (30, 30))
plus2Img = pygame.image.load(resource_path(os.path.join('img', 'plus2.png'))).convert()
plus2Img = pygame.transform.scale(plus2Img, (30, 30))
minus1Img = pygame.image.load(resource_path(os.path.join('img', 'minus1.png'))).convert()
minus1Img = pygame.transform.scale(minus1Img, (30, 30))
minus2Img = pygame.image.load(resource_path(os.path.join('img', 'minus2.png'))).convert()
minus2Img = pygame.transform.scale(minus2Img, (30, 30))
zigzag2Img = pygame.image.load(resource_path(os.path.join('img', 'zigzag.png'))).convert()
zigzag2Img = pygame.transform.scale(zigzag2Img, (30, 30))
hole2Img = pygame.image.load(resource_path(os.path.join('img', 'hole.png'))).convert()
hole2Img = pygame.transform.scale(hole2Img, (30, 30))
reverseLRItem2Img = pygame.image.load(resource_path(os.path.join('img', 'reverseLRItem.png'))).convert()
reverseLRItem2Img = pygame.transform.scale(reverseLRItem2Img, (30, 30))

# item의 이미지들을 담고있는 list (index 1부터 유효함)
# item의 color 값에서 맨앞 숫자가 itemList의 인덱스임.
itemImgList = []
itemImgList.append(0)
itemImgList.append(plus1Img)
itemImgList.append(plus2Img)
itemImgList.append(minus1Img)
itemImgList.append(minus2Img)
itemImgList.append(zigzag2Img)
itemImgList.append(hole2Img)
itemImgList.append(reverseLRItem2Img)

# item을 구분하기 위해 color 맵을 이용함
plus1 = (1,0,0)
plus2 = (2,0,0)
minus1 = (3,0,0)
minus2 = (4,0,0)
zigzag = (5,0,0)
hole = (6,0,0)
reverseLRItem = (1,0,0)

# Sound
pygame.mixer.init()
pygame.init()

# bgm
bgmPathList = []
bgmPathList.append(resource_path(os.path.join('bgm', 'Butchers.mp3')))
bgmPathList.append(resource_path(os.path.join('bgm', 'Arms_Dealer.mp3')))
bgmPathList.append(resource_path(os.path.join('bgm', 'OK_POP_KO.mp3')))
bgmPathList.append(resource_path(os.path.join('bgm', 'I_m_Happy_For_This_Guitar.mp3')))
bgmPathList.append(resource_path(os.path.join('bgm', 'Always_Be_My_Unicorn.mp3')))
bgmPathList.append(resource_path(os.path.join('bgm', 'How_it_Began.mp3')))
bgmPathList.append(resource_path(os.path.join('bgm', 'We_Share_This.mp3')))

# sound effect

pyAudioObj = pyaudio.PyAudio()

def callbackBlockDeletedSound(in_data, frame_count, time_info, status):
    data = blockDeletedSoundWave.readframes(frame_count)
    return (data, pyaudio.paContinue)

blockDeletedSoundWave = wave.open(resource_path(os.path.join('sounds', 'blockDeletedSound.wav')), 'rb')
blockDeletedSoundStream = pyAudioObj.open(format=pyAudioObj.get_format_from_width(blockDeletedSoundWave.getsampwidth()),
                channels=blockDeletedSoundWave.getnchannels(),
                rate=blockDeletedSoundWave.getframerate(),
                output=True,
                start = False,
                stream_callback=callbackBlockDeletedSound)

def callbackBlockDropSound(in_data, frame_count, time_info, status):
    data = blockDropSoundWave.readframes(frame_count)
    return (data, pyaudio.paContinue)

blockDropSoundWave = wave.open(resource_path(os.path.join('sounds', 'blockDropSound.wav')), 'rb')
blockDropSoundStream = pyAudioObj.open(format=pyAudioObj.get_format_from_width(blockDropSoundWave.getsampwidth()),
                channels=blockDropSoundWave.getnchannels(),
                rate=blockDropSoundWave.getframerate(),
                output=True,
                start = False,
                stream_callback=callbackBlockDropSound)

def callbackBlockDownSound(in_data, frame_count, time_info, status):
    data = blockDownSoundWave.readframes(frame_count)
    return (data, pyaudio.paContinue)

blockDownSoundWave = wave.open(resource_path(os.path.join('sounds', 'blockDownSound.wav')), 'rb')
blockDownSoundStream = pyAudioObj.open(format=pyAudioObj.get_format_from_width(blockDownSoundWave.getsampwidth()),
                channels=blockDownSoundWave.getnchannels(),
                rate=blockDownSoundWave.getframerate(),
                output=True,
                start = False,
                stream_callback=callbackBlockDownSound)

def callbackBlockMoveSound(in_data, frame_count, time_info, status):
    data = blockMoveSoundWave.readframes(frame_count)
    return (data, pyaudio.paContinue)

blockMoveSoundWave = wave.open(resource_path(os.path.join('sounds', 'blockMoveSound.wav')), 'rb')
blockMoveSoundStream = pyAudioObj.open(format=pyAudioObj.get_format_from_width(blockMoveSoundWave.getsampwidth()),
                channels=blockMoveSoundWave.getnchannels(),
                rate=blockMoveSoundWave.getframerate(),
                output=True,
                start = False,
                stream_callback=callbackBlockMoveSound)

def callbackBlockRotationSound(in_data, frame_count, time_info, status):
    data = blockRotationSoundWave.readframes(frame_count)
    return (data, pyaudio.paContinue)

blockRotationSoundWave = wave.open(resource_path(os.path.join('sounds', 'blockRotationSound2.wav')), 'rb')
blockRotationSoundStream = pyAudioObj.open(format=pyAudioObj.get_format_from_width(blockRotationSoundWave.getsampwidth()),
                channels=blockRotationSoundWave.getnchannels(),
                rate=blockRotationSoundWave.getframerate(),
                output=True,
                start = False,
                stream_callback=callbackBlockRotationSound)

def callbackSwapSound(in_data, frame_count, time_info, status):
    data = swapSoundWave.readframes(frame_count)
    return (data, pyaudio.paContinue)

swapSoundWave = wave.open(resource_path(os.path.join('sounds', 'swapSound.wav')), 'rb')
swapSoundStream = pyAudioObj.open(format=pyAudioObj.get_format_from_width(swapSoundWave.getsampwidth()),
                channels=swapSoundWave.getnchannels(),
                rate=swapSoundWave.getframerate(),
                output=True,
                start = False,
                stream_callback=callbackSwapSound)

def callbackTetrisSound(in_data, frame_count, time_info, status):
    data = tetrisSoundWave.readframes(frame_count)
    return (data, pyaudio.paContinue)

tetrisSoundWave = wave.open(resource_path(os.path.join('sounds', 'tetrisSound.wav')), 'rb')
tetrisSoundStream = pyAudioObj.open(format=pyAudioObj.get_format_from_width(tetrisSoundWave.getsampwidth()),
                channels=tetrisSoundWave.getnchannels(),
                rate=tetrisSoundWave.getframerate(),
                output=True,
                start = False,
                stream_callback=callbackTetrisSound)

blockSize = 30
topLineBlockSize = 10
nextBlockSize = 20
# 테두리 두께
outline_w = 3
# 내부 선 두께
inline_w = 1

grid_w = (10*blockSize) + (9*inline_w) + (2*outline_w)
grid_h = (20*blockSize) + (19*inline_w) + (2*outline_w) + (1*inline_w) + (1*blockSize) # 뒤 두개는 맨윗줄 조금보이는 것을 위해 넣음

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
defaultLevelUpTime = 10

# 중력 레벨업시 배수
gravityLevelUp = 0.8
# 중력 레벨다운시 배수
gravityLevelDown= 1.25 

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
    pygame.draw.rect(surface, gray, (outline_w, outline_w, grid_w - (2*outline_w), grid_h - (2*outline_w)))

    for i in range(0, grid_row - 4):
        y = 3 + i * (inline_w + blockSize)
        for j in range(0, grid_col - 2):
            x = 3 + j * (inline_w + blockSize)
            if isItem(grid[i+3][j+1]):
                imgRect = itemImgList[grid[i+3][j+1][0]].get_rect()
                imgRect.x = x
                imgRect.y = y
                surface.blit(itemImgList[grid[i+3][j+1][0]], imgRect)
            else:
                pygame.draw.rect(surface, grid[i+3][j+1], (x, y, blockSize, blockSize))

    pygame.draw.rect(surface, black, (outline_w, outline_w, grid_w - (2*outline_w), blockSize - topLineBlockSize - inline_w))
    pygame.draw.rect(surface, purple, (0, blockSize - topLineBlockSize - inline_w, grid_w - outline_w, grid_h - (blockSize - topLineBlockSize - inline_w)), outline_w)

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

def deleteLine(grid, itemList, isNoitem):
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
            if isNoitem == False:
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


def updateScreen(surface, gridSurface, nextBlockSurface, holdBlockSurface, itemSlotSurface, grid, nextBlock, holdBlock, itemList, score, isNoitem):
    surface.fill(black)

    drawGrid(gridSurface, grid)

    updateBlockBoxSurface(nextBlockSurface, nextBlock)
    updateBlockBoxSurface(holdBlockSurface, holdBlock)
    drawMessage(surface, "Arial", 20, yellow, black, "Next Block", nextBlockRect_centerX, nextBlockRect_centerY - 85)
    drawMessage(surface, "Arial", 20, yellow, black, "Hold Block", holdBlockRect_centerX, holdBlockRect_centerY - 85)

    if isNoitem == False:
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

def zigzagGrid(grid):
    moveRight = False
    for i in range(1, grid_row - 1):
        for j in range(2,grid_col - 1):
            if moveRight == True:
                grid[i][j-1] = grid[i][j]
            else:
                grid[i][grid_col - j] = grid[i][grid_col - j - 1]
        if moveRight == True:
            grid[i][1] = black
        else:
            grid[i][grid_col - 2] = black
        moveRight = not moveRight

def holeGrid(grid):
    for i in range(1, grid_row - 1):
        for j in range(1 + (i%2),grid_col - 1, 2):
            grid[i][j] = black

def useItem(grid, item, userState):
    if item[0] == 1:
        lineUp(grid, 1)
    elif item[0] == 2:
        lineUp(grid, 2)
    elif item[0] == 3:
        lineDown(grid,1)
    elif item[0] == 4:
        lineDown(grid,2)
    elif item[0] == 5:
        zigzagGrid(grid)
    elif item[0] == 6:
        holeGrid(grid)
    elif item[0] == 7:
        userState.reverseLR = True

def isRightInput(key, reversed):
    if (key == pygame.K_RIGHT or key == pygame.K_9) and reversed == 0:
        return True
    if (key == pygame.K_LEFT or pygame.K_7) and reversed != 0:
        return True

    return False

def isLeftInput(key, reversed):
    if (key == pygame.K_LEFT or key == pygame.K_7) and reversed == 0:
        return True
    if (key == pygame.K_RIGHT or key == pygame.K_9) and reversed != 0:
        return True

    return False

def gameStart(surface, dropSpeed, levelUpTime, limitTime, isNoItem):
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
    updateScreen(surface, gridSurface, nextBlockSurface, holdBlockSurface, itemSlotSurface, copiedGrid, nextBlock, holdBlock, itemList, score, isNoItem)

    # 회전이나 좌우 이동에 성공했을때 블럭이 바닥에 고정되지 않게 해준다.
    infinity = 0

    pygame.key.set_repeat(130, 30)

    # 전체 게임 플레이 시간 관리
    totalPlayTime = 0
    # 떨어지는 시간 관리
    dropTime = 0
    # 떨어지는 단계 시간 관리
    dropLevelTime = 0
    delayTime = 0
    # infinity 초기화 시간
    infinityMaxTime = 0.3

    # keyChanger 지속 시간 관리
    reverseLRTimer = 0
    reverseLRMaxTime = 5

    comboStack = 0
    tetrisComboStack = 0

    # 유저 상태
    user1State = UserState()

    isFinish = False

    # 시간 한 번 초기화
    clock.tick(gameFPS)
    while run:
        clock.tick(gameFPS)
        droppedBlock = False
        # 1/1000 sec
        delayTime += clock.get_time()
        dropLevelTime += clock.get_time()
        totalPlayTime += clock.get_time()

        if user1State.checkMusicFinish():
            user1State.changeBgm()

        if limitTime != 0 and (totalPlayTime / 1000) >= limitTime:
            isFinish = True

        if (delayTime / 1000) > dropSpeed:
            currentBlock.x += 1
            if len(checkConflict(grid, currentBlock, [Conflict.TOP])) != 0:
                currentBlock.x -= 1
                if (delayTime - infinity) / 1000 > infinityMaxTime:
                    droppedBlock = True
                    delayTime = 0
                    infinity = 0
            else:
                delayTime = 0
                infinity = 0

        # levelUpTime == 0 이면 레벨업 하지 않음.(싱글 모드)
        if levelUpTime != 0 and (dropLevelTime / 1000) > levelUpTime:
            dropLevelTime = 0
            dropSpeed = dropSpeed * gravityLevelUp

        if reverseLRTimer != 0:
            reverseLRTimer += clock.get_time()
            if (reverseLRTimer / 1000) > reverseLRMaxTime:
                reverseLRTimer = 0
                user1State.reverseLR = False

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
                    if user1State.isSwappedBlock() == False:
                        if swapSoundStream.is_stopped() == False and swapSoundStream.is_active() == False:
                            swapSoundStream.stop_stream()
                        swapSoundWave.rewind()
                        swapSoundStream.start_stream()

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

                        user1State.setSwappedBlock(True)

                elif event.key == pygame.K_DOWN:
                    currentBlock.x += 1
                    if len(checkConflict(grid, currentBlock, [Conflict.TOP])) != 0:
                        currentBlock.x -= 1
                        droppedBlock = True
                    else:
                        if blockDownSoundStream.is_stopped() == False and blockDownSoundStream.is_active() == False:
                            blockDownSoundStream.stop_stream()
                        blockDownSoundWave.rewind()
                        blockDownSoundStream.start_stream()
                        infinity = delayTime
                elif isLeftInput(event.key, reverseLRTimer):
                    currentBlock.y -= 1
                    if len(checkConflict(grid, currentBlock, [Conflict.BOTTOM, Conflict.TOP])) != 0:
                        currentBlock.y += 1
                    else:
                        if blockMoveSoundStream.is_stopped() == False and blockMoveSoundStream.is_active() == False:
                            blockMoveSoundStream.stop_stream()
                        blockMoveSoundWave.rewind()
                        blockMoveSoundStream.start_stream()
                        infinity = delayTime
                elif isRightInput(event.key, reverseLRTimer):
                    currentBlock.y += 1
                    if len(checkConflict(grid, currentBlock, [Conflict.BOTTOM, Conflict.TOP])) != 0:
                        currentBlock.y -= 1
                    else:
                        if blockMoveSoundStream.is_stopped() == False and blockMoveSoundStream.is_active() == False:
                            blockMoveSoundStream.stop_stream()
                        blockMoveSoundWave.rewind()
                        blockMoveSoundStream.start_stream()
                        infinity = delayTime
                elif event.key == pygame.K_UP or event.key == pygame.K_8:
                    if blockRotationSoundStream.is_stopped() == False and blockRotationSoundStream.is_active() == False:
                        blockRotationSoundStream.stop_stream()
                    blockRotationSoundWave.rewind()
                    blockRotationSoundStream.start_stream()

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
                elif event.key == pygame.K_z:
                    if dropSpeed < 2:
                        dropSpeed = dropSpeed * gravityLevelDown
                elif event.key == pygame.K_x:
                    if dropSpeed > 0.017:
                        dropSpeed = dropSpeed * gravityLevelUp
                elif event.key == pygame.K_1:
                    if isNoItem == False:
                        if 0 < len(itemList):
                            useItem(grid, itemList.pop(0), user1State)
                            copiedGrid = copy.deepcopy(grid)
                            if user1State.reverseLR == True:
                                reverseLRTimer = delayTime

                ghostBlock = setGhostBlock(copiedGrid, currentBlock)

        blockValidPositions = getValidPositions(currentBlock)
        ghostValidPositions = getValidPositions(ghostBlock)
        drawBlock(copiedGrid, ghostValidPositions, ghostBlock.color)
        drawBlock(copiedGrid, blockValidPositions, currentBlock.color)

        if droppedBlock:
            delayTime = 0

            if blockDropSoundStream.is_stopped() == False and blockDropSoundStream.is_active() == False:
                blockDropSoundStream.stop_stream()
            blockDropSoundWave.rewind()
            blockDropSoundStream.start_stream()

            currentBlock = nextBlock

            nextBlock = getRandomBlock()
            grid = copy.deepcopy(copiedGrid)
            delLineCount = deleteLine(grid, itemList, isNoItem)

            if delLineCount > 0:
                comboStack += 1
                if delLineCount == 4:
                    tetrisComboStack += 1
                else:
                    tetrisComboStack = 0
                if isNoItem == False:
                    randNum = random.randrange(0,10)
                    # TODO : Test를 위해 아이템 생성률을 100%로 해둠. 나중에 적절한 수치로 수정해야함.
                    if randNum >= 0:
                        createItemInGrid(grid)
            else:
                comboStack = 0

            comboScoreMulti = (comboStack // 3) + 1
            if comboStack > 1:
                comboScoreMulti += 1

            if delLineCount == 4:
                if tetrisSoundStream.is_stopped() == False and tetrisSoundStream.is_active() == False:
                    swapSoundStream.stop_stream()
                tetrisSoundWave.rewind()
                tetrisSoundStream.start_stream()
                # tetris(4줄을 한번에 없애는 것)는 점수 2배
                score += delLineCount * 10 * 2 * comboScoreMulti * tetrisComboStack
            else:
                score += delLineCount * 10 * comboScoreMulti

            ghostBlock = setGhostBlock(grid, currentBlock)
            user1State.setSwappedBlock(False)


        updateScreen(surface, gridSurface, nextBlockSurface, holdBlockSurface, itemSlotSurface, copiedGrid, nextBlock, holdBlock, itemList, score, isNoItem)

        if isFinish or checkFinish(grid, currentBlock):

            user1State.stopBgm()
            drawMessageCenter(surface, "Arial", 40, white, (40, 40, 40), "Game Over!")
            drawMessageCenter(surface, "Arial", 40, white, (40, 40, 40), "Press ESC to Check to Your Score", 50)

            pygame.display.flip()
            goScorePage = False
            while goScorePage == False:
                pygame.time.delay(100)
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            goScorePage = True
                            break

            surface.fill(black)
            drawMessageCenter(surface, "Arial", 40, white, (40, 40, 40), "Your Score : " + str(score))
            drawMessageCenter(surface, "Arial", 40, white, (40, 40, 40), "Press ESC to go to the menu", 50)
            pygame.display.flip()
            while run:
                pygame.time.delay(100)
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            run = False
                            break

        copiedGrid = copy.deepcopy(grid)

    user1State.stopBgm()

def updateMenuScreen(surface):
    surface.fill(black) # 메뉴 창 검정색 바탕
    
    drawSubsurfaceCenter(surface, menuImgList[1], 0, -100)
    drawSubsurfaceCenter(surface, menuImgList[2], 0, -33)
    drawSubsurfaceCenter(surface, menuImgList[3], 0, 33)
    drawSubsurfaceCenter(surface, menuImgList[4], 0, 100)

    pygame.display.flip()

def changeSelectedMenu():
    if menuImgList[0] == 1:
        menuImgList[1] = selectedNormalModePlayImg
        menuImgList[2] = unselectedMarathonModePlayImg
        menuImgList[3] = unselectedOpInfoImg
        menuImgList[4] = unselectedGameFinishImg
    if menuImgList[0] == 2:
        menuImgList[1] = unselectedNormalModePlayImg
        menuImgList[2] = selectedMarathonModePlayImg
        menuImgList[3] = unselectedOpInfoImg
        menuImgList[4] = unselectedGameFinishImg
    elif menuImgList[0] == 3:
        menuImgList[1] = unselectedNormalModePlayImg
        menuImgList[2] = unselectedMarathonModePlayImg
        menuImgList[3] = selectedOpInfoImg
        menuImgList[4] = unselectedGameFinishImg
    elif menuImgList[0] == 4:
        menuImgList[1] = unselectedNormalModePlayImg
        menuImgList[2] = unselectedMarathonModePlayImg
        menuImgList[3] = unselectedOpInfoImg
        menuImgList[4] = selectedGameFinishImg

def operationInfoPage(surface):
    surface.fill(black)
    drawSubsurfaceCenter(surface, opInfoImg)

    pygame.display.flip()

    while True:
        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                return

def menu(surface):
    run = True

    # menu 초기 설정
    menuImgList.append(1)
    menuImgList.append(selectedNormalModePlayImg)
    menuImgList.append(unselectedMarathonModePlayImg)
    menuImgList.append(unselectedOpInfoImg)
    menuImgList.append(unselectedGameFinishImg)

    while run:
        updateMenuScreen(surface)
        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    break
                elif event.key == pygame.K_RETURN:
                    if menuImgList[0] == 1:
                        gameStart(surface, 1, 0, 30, True)
                    elif menuImgList[0] == 2:
                        gameStart(surface, 1, 0, 0, True);
                    elif menuImgList[0] == 3:
                        operationInfoPage(surface)
                    elif menuImgList[0] == 4:
                        run = False
                        break
                elif event.key == pygame.K_DOWN:
                    menuImgList[0] = menuImgList[0] + 1
                    if menuImgList[0] == len(menuImgList):
                        menuImgList[0] = 1
                    changeSelectedMenu()
                elif event.key == pygame.K_UP:
                    menuImgList[0] = menuImgList[0] - 1
                    if menuImgList[0] == 0:
                        menuImgList[0] = len(menuImgList) - 1
                    changeSelectedMenu()

    pygame.display.quit()

menu(surface)

blockDeletedSoundStream.stop_stream()
blockDeletedSoundStream.close()
blockDropSoundStream.stop_stream()
blockDropSoundStream.close()
blockDownSoundStream.stop_stream()
blockDownSoundStream.close()
blockMoveSoundStream.stop_stream()
blockMoveSoundStream.close()
blockRotationSoundStream.stop_stream()
blockRotationSoundStream.close()
swapSoundStream.stop_stream()
swapSoundStream.close()
tetrisSoundStream.stop_stream()
tetrisSoundStream.close()

pyAudioObj.terminate()