import pygame

pygame.init()

screen_w = 700
screen_h = 900

def gameStart(surface):

    run = True

    while run:
        surface.fill((0,0,0))
        font = pygame.font.SysFont("Arial", 20)
        # 둥근 모서리로 흰색 글자 그리기
        textBox = font.render("Playing...", 1, (255, 255, 255))
        surface.blit(textBox, (350, 450))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False


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