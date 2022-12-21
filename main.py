import pygame
from button import Button
from pygame import mixer
from fighter import Fighter
import time

mixer.init()
pygame.init()

#create game window
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Brawler")
game_state = "menu"

#set framerate
clock = pygame.time.Clock()
FPS = 60

#define colours
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

#define game variables
intro_count = 3
last_count_update = pygame.time.get_ticks()
score = [0, 0]#player scores. [P1, P2]
round_over = False
ROUND_OVER_COOLDOWN = 2000

#define fighter variables
YONE_SIZE = 200
YONE_SCALE = 4
YONE_OFFSET = [80, 77]
YONE_DATA = [YONE_SIZE, YONE_SCALE, YONE_OFFSET]
KARTHUS_SIZE = 250
KARTHUS_SCALE = 3
KARTHUS_OFFSET = [112, 107]
KARTHUS_DATA = [KARTHUS_SIZE, KARTHUS_SCALE, KARTHUS_OFFSET]
MASTERYI_SIZE = 162
MASTERYI_SCALE = 4
MASTERYI_OFFSET = [72, 56]
MASTERYI_DATA = [MASTERYI_SIZE, MASTERYI_SCALE, MASTERYI_OFFSET]
CASSIOPEIA_SIZE = 125
CASSIOPEIA_SCALE = 2
CASSIOPEIA_OFFSET = [112, 107]
CASSIOPEIA_DATA = [CASSIOPEIA_SIZE, CASSIOPEIA_SCALE, CASSIOPEIA_OFFSET]

#load music and sounds
pygame.mixer.music.load("assets/audio/music.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1, 0.0, 5000)
sword_fx = pygame.mixer.Sound("assets/audio/sword.wav")
sword_fx.set_volume(0.5)
magic_fx = pygame.mixer.Sound("assets/audio/magic.wav")
magic_fx.set_volume(0.75)

#load background image
bg_image = pygame.image.load("assets/images/background/background.jpg").convert_alpha()

#load buttons
back_image = pygame.image.load("assets/images/buttons/back.png").convert_alpha()
back_button = Button(0, 0, back_image, 1)
start_image = pygame.image.load("assets/images/buttons/start.png").convert_alpha()
start_button = Button(322, 50, start_image, 1)
setting_image = pygame.image.load("assets/images/buttons/setting.png").convert_alpha()
setting_button = Button(322, 250, setting_image, 1)
exit_image = pygame.image.load("assets/images/buttons/exit.png").convert_alpha()
exit_button = Button(322, 450, exit_image, 1)

#load avatar
avatar_yone = pygame.image.load("assets/images/avatar/yone.png").convert_alpha()
avatar_karthus = pygame.image.load("assets/images/avatar/karthus.png").convert_alpha()
avatar_masteryi = pygame.image.load("assets/images/avatar/masteryi.png").convert_alpha()
avatar_cassiopeia = pygame.image.load("assets/images/avatar/cassiopeia.png").convert_alpha()

#load character choosing buttons
yone_button = Button(100, 50, avatar_yone, 1)
karthus_button = Button(300, 50, avatar_karthus, 1)
masteryi_button = Button(500, 50, avatar_masteryi, 1)
cassiopeia_button = Button(700, 50, avatar_cassiopeia, 1)


#load spritesheets
yone_sheet = pygame.image.load("assets/images/characters/yone.png").convert_alpha()
karthus_sheet = pygame.image.load("assets/images/characters/karthus.png").convert_alpha()
masteryi_sheet = pygame.image.load("assets/images/characters/masteryi.png").convert_alpha()
cassiopeia_sheet = pygame.image.load("assets/images/characters/cassiopeia.png").convert_alpha()


#load vicory image
victory_img = pygame.image.load("assets/images/icons/victory.png").convert_alpha()

#define number of steps in each animation
YONE_ANIMATION_STEPS = [8, 8, 2, 6, 6, 4, 6]
KARTHUS_ANIMATION_STEPS = [8, 8, 1, 8, 8, 3, 7]
MASTERYI_ANIMATION_STEPS = [10, 8, 1, 7, 7, 3, 7]
CASSIOPEIA_ANIMATION_STEPS = [9, 9, 1, 16, 16, 3, 8]
  
#define font
count_font = pygame.font.Font("assets/fonts/turok.ttf", 80)
score_font = pygame.font.Font("assets/fonts/turok.ttf", 30)

#function for drawing text
def draw_text(text, font, text_col, x, y):
  img = font.render(text, True, text_col)
  screen.blit(img, (x, y))

#function for drawing background
def draw_bg():
  scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
  screen.blit(scaled_bg, (0, 0))

#function for drawing fighter health bars
def draw_health_bar(health, x, y):
  ratio = health / 100
  pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))
  pygame.draw.rect(screen, RED, (x, y, 400, 30))
  pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 30))

#function for drawing avatar
def draw_avatar(avatar1, avatar2):
  screen.blit(avatar1, (400, 20))
  screen.blit(avatar2, (500, 0))
  

#create two instances of fighters
yone_1 = Fighter(1, 200, 310, False, YONE_DATA, yone_sheet, YONE_ANIMATION_STEPS, sword_fx)
yone_2 = Fighter(2, 700, 310, True, YONE_DATA, yone_sheet, YONE_ANIMATION_STEPS, sword_fx)
karthus_1 = Fighter(1, 200, 310, False, KARTHUS_DATA, karthus_sheet, KARTHUS_ANIMATION_STEPS, magic_fx)
karthus_2 = Fighter(2, 700, 310, True, KARTHUS_DATA, karthus_sheet, KARTHUS_ANIMATION_STEPS, magic_fx)
masteryi_1 = Fighter(1, 200, 310, False, MASTERYI_DATA, masteryi_sheet, MASTERYI_ANIMATION_STEPS, sword_fx)
masteryi_2 = Fighter(2, 700, 310, True, MASTERYI_DATA, masteryi_sheet, MASTERYI_ANIMATION_STEPS, sword_fx)
cassiopeia_1 = Fighter(1, 200, 310, False, CASSIOPEIA_DATA, cassiopeia_sheet, CASSIOPEIA_ANIMATION_STEPS, magic_fx)
cassiopeia_2 = Fighter(2, 700, 310, True, CASSIOPEIA_DATA, cassiopeia_sheet, CASSIOPEIA_ANIMATION_STEPS, magic_fx)

fighter_1 = type(yone_1)
fighter_2 = type(yone_1)
avatar_1 = type(avatar_yone)
avatar_2 = type(avatar_yone)

choose_character = False

#game loop
run = True
while run:
  if game_state == "menu":
    screen.fill(WHITE)
    if start_button.draw(screen):
      game_state = "character"
    if setting_button.draw(screen):
      game_state = "setting"
    if exit_button.draw(screen):
      run = False
  if game_state == "setting":
    screen.fill(WHITE)
    if back_button.draw(screen):
      game_state = "menu"
  if game_state == "character":
    screen.fill(WHITE)
    if back_button.draw(screen):
      game_state = "menu"
    if yone_button.draw(screen):
      if choose_character == False:
        fighter_1 = yone_1
        avatar_1 = avatar_yone
        choose_character = True
      else:
        fighter_2 = yone_2
        avatar_2 = avatar_yone
        choose_character = False
        game_state = "game"
        
    if karthus_button.draw(screen):
      if choose_character == False:
        fighter_1 = karthus_1
        avatar_1 = avatar_karthus
        choose_character = True
      else:
        fighter_2 = karthus_2
        avatar_2 = avatar_karthus
        choose_character = False
        game_state = "game"
        
    if masteryi_button.draw(screen):
      if choose_character == False:
        fighter_1 = masteryi_1
        avatar_1 = avatar_masteryi
        choose_character = True
      else:
        fighter_2 = masteryi_2
        avatar_2 = avatar_masteryi
        choose_character = False
        game_state = "game"
        
    if cassiopeia_button.draw(screen):
      if choose_character == False:
        fighter_1 = cassiopeia_1
        avatar_1 = avatar_cassiopeia
        choose_character = True
      else:
        fighter_2 = cassiopeia_2
        avatar_2 = avatar_cassiopeia
        choose_character = False
        game_state = "game"

  if game_state == "game":
    clock.tick(FPS)

    #draw background
    draw_bg()
    draw_avatar(avatar_1, avatar_2)

    #show player stats
    draw_health_bar(fighter_1.health, 20, 20)
    draw_health_bar(fighter_2.health, 580, 20)
    draw_text("P1: " + str(score[0]), score_font, RED, 360, 60)
    draw_text("P2: " + str(score[1]), score_font, BLUE, 580, 60)

    #update countdown
    if intro_count <= 0:
      #move fighters
      fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2, round_over)
      fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1, round_over)
    else:
      #display count timer
      draw_text(str(intro_count), count_font, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
      #update count timer
      if (pygame.time.get_ticks() - last_count_update) >= 1000:
        intro_count -= 1
        last_count_update = pygame.time.get_ticks()

    #update fighters
    fighter_1.update()
    fighter_2.update()

    #draw fighters
    fighter_1.draw(screen)
    fighter_2.draw(screen)

    #check for player defeat
    if round_over == False:
      if fighter_1.alive == False:
        score[1] += 1
        round_over = True
        round_over_time = pygame.time.get_ticks()
        fighter_1.alive = True
        fighter_1.health = 100
      elif fighter_2.alive == False:
        score[0] += 1
        round_over = True
        round_over_time = pygame.time.get_ticks()
        fighter_2.alive = True
        fighter_2.health = 100
    else:
      #display victory image
      screen.blit(victory_img, (360, 150))
      if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
        round_over = False
        intro_count = 3
        game_state = "character"
        choose_character = False


  #event handler
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False

  #update display
  pygame.display.update()

#exit pygame
pygame.quit()
