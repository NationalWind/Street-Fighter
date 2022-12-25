import pygame
import os
from fighter import Fighter

os.chdir('D:\Code\Python\Street_Fighter_Fake')

pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
RED = (255,0,0)
YELLOW = (255,255,0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 255)

#
WARRIOR_SIZE = 162
WARRIOR_SCALE = 4
WARRIOR_OFFSET = [72, 56]
WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]
WIZARD_SIZE = 200
WIZARD_SCALE = 3
WIZARD_OFFSET = [112, 107]
WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Yanghoo Fighter")

#set framerate
clock = pygame.time.Clock()
FPS = 60

#ảnh background
bg_img = pygame.image.load("assets/background/background_forest.png").convert_alpha()

#anh nhan vat
warrior_sheet = pygame.image.load("assets/images/warrior/Sprites/Warrior.png").convert_alpha()
wizard_sheet = pygame.image.load("assets/images/wizard/Sprites/Wizard.png").convert_alpha()

#Khai bao khung hinh nhan vat
WARRIOR_ANIMATION_STEPS = [10, 8, 1, 7, 7, 3, 7]
WIZARD_ANIMATION_STEPS = [8, 8, 1, 8, 8, 3, 7]

#hàm vẽ background
def draw_bg():
    scaled_bg = pygame.transform.scale(bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_bg,  (0, 0))

#ve thanh HP
def draw_health_bar(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))
    pygame.draw.rect(screen, RED, (x, y, 400, 30))
    pygame.draw.rect(screen, YELLOW, (x, y, ratio * 400, 30))

#Tạo 2 thằng fighters
fighter_1 = Fighter(200, 360, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS)
fighter_2 = Fighter(700, 360, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS)

run = True
while run:

    clock.tick(FPS)

    #vẽ background và nhân vật
    draw_bg()
    fighter_1.draw(screen)


    draw_health_bar(fighter_1.health, 20, 20)


    #move fighters
    fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2)
    fighter_1.update()

    for event in pygame.event.get():
        if event.type == pygame. QUIT:
            run = False

    #cập nhật màn hình
    pygame.display.update()

pygame.quit()