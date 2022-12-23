import pygame
from button import Button
from pygame import mixer
from fighter import Fighter

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

#define colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
GRAY = (127, 127, 127)

#define game variables
intro_count = 3
last_count_update = pygame.time.get_ticks()
score = [0, 0]#player scores. [P1, P2]
round_over = False
ROUND_OVER_COOLDOWN = 2000
choose_character = 0


#define fighter variables
YASUO_SIZE = 200
YASUO_SCALE = 4
YASUO_OFFSET = [80, 77]
YASUO_DATA = [YASUO_SIZE, YASUO_SCALE, YASUO_OFFSET]
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
CASSIOPEIA_OFFSET = [50, -10]
CASSIOPEIA_DATA = [CASSIOPEIA_SIZE, CASSIOPEIA_SCALE, CASSIOPEIA_OFFSET]

#define projectile variables
object_yasuo_size = 16
object_yasuo_scale = 20
object_yasuo_offset = [12, 5]
object_yasuo_data = [object_yasuo_size, object_yasuo_scale, object_yasuo_offset]
object_karthus_size = 5
object_karthus_scale = 20
object_karthus_offset = [5, 0]
object_karthus_data = [object_karthus_size, object_karthus_scale, object_karthus_offset]
object_masteryi_size = 16
object_masteryi_scale = 20
object_masteryi_offset = [12, 5]
object_masteryi_data = [object_masteryi_size, object_masteryi_scale, object_masteryi_offset]
object_cassiopeia_size = 5
object_cassiopeia_scale = 15
object_cassiopeia_offset = [5, -5]
object_cassiopeia_data = [object_cassiopeia_size, object_cassiopeia_scale, object_cassiopeia_offset]

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
back_button = Button(0, 0, back_image, 0.5)
start_image = pygame.image.load("assets/images/buttons/start.png").convert_alpha()
start_button = Button(322, 50, start_image, 1)
setting_image = pygame.image.load("assets/images/buttons/setting.png").convert_alpha()
setting_button = Button(322, 250, setting_image, 1)
exit_image = pygame.image.load("assets/images/buttons/exit.png").convert_alpha()
exit_button = Button(322, 450, exit_image, 1)

#load avatar
avatar_yasuo = pygame.image.load("assets/images/avatar/yasuo.png").convert_alpha()
avatar_karthus = pygame.image.load("assets/images/avatar/karthus.png").convert_alpha()
avatar_masteryi = pygame.image.load("assets/images/avatar/masteryi.png").convert_alpha()
avatar_cassiopeia = pygame.image.load("assets/images/avatar/cassiopeia.png").convert_alpha()

#load character choosing buttons
yasuo_button = Button(100, 250, avatar_yasuo, 1)
yasuo_check = [False, False]
karthus_button = Button(300, 250, avatar_karthus, 1)
karthus_check = [False, False]
masteryi_button = Button(500, 250, avatar_masteryi, 1)
masteryi_check = [False, False]
cassiopeia_button = Button(700, 250, avatar_cassiopeia, 1)
cassiopeia_check = [False, False]


#load spritesheets
yasuo_sheet = pygame.image.load("assets/images/characters/yasuo.png").convert_alpha()
karthus_sheet = pygame.image.load("assets/images/characters/karthus.png").convert_alpha()
masteryi_sheet = pygame.image.load("assets/images/characters/masteryi.png").convert_alpha()
cassiopeia_sheet = pygame.image.load("assets/images/characters/cassiopeia.png").convert_alpha()

#load projectile image
yasuo_projectile = pygame.image.load("assets/images/warrior/Skillwave_MasterYi.png").convert_alpha()
karthus_projectile = pygame.image.load("assets/images/warrior/Skillwave_Karthus.png").convert_alpha()
masteryi_projectile = pygame.image.load("assets/images/warrior/Skillwave_MasterYi.png").convert_alpha()
cassiopeia_projectile = pygame.image.load("assets/images/warrior/Skillwave_Karthus.png").convert_alpha()

#load vicory image
victory_img = pygame.image.load("assets/images/icons/victory.png").convert_alpha()
player1_img = pygame.image.load("assets/images/icons/player1.png").convert_alpha()
player2_img = pygame.image.load("assets/images/icons/player2.png").convert_alpha()

#define number of steps in each animation
YASUO_ANIMATION_STEPS = [8, 8, 2, 6, 6, 4, 6]
KARTHUS_ANIMATION_STEPS = [8, 8, 1, 8, 8, 3, 7]
MASTERYI_ANIMATION_STEPS = [10, 8, 1, 7, 7, 3, 7]
CASSIOPEIA_ANIMATION_STEPS = [9, 9, 1, 16, 16, 3, 8]
  
#define font
count_font = pygame.font.Font("assets/fonts/turok.ttf", 80)
name_font = pygame.font.Font("assets/fonts/turok.ttf", 40)
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

def draw_mana_bar(mana, x, y):
  ratio = mana / 100
  pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 12))
  pygame.draw.rect(screen, GRAY, (x, y, 400, 8))
  pygame.draw.rect(screen, CYAN, (x, y, 400 * ratio, 8))

#function for drawing avatar
def draw_avatar(avatar1, avatar2):
  screen.blit(avatar1, (400, 0))
  screen.blit(avatar2, (500, 0))
  

#create two instances of fighters
yasuo_1 = Fighter(1, 200, 310, False, YASUO_DATA, yasuo_sheet, YASUO_ANIMATION_STEPS, sword_fx, object_yasuo_data, yasuo_projectile)
yasuo_2 = Fighter(2, 700, 310, True, YASUO_DATA, yasuo_sheet, YASUO_ANIMATION_STEPS, sword_fx, object_yasuo_data, yasuo_projectile)
karthus_1 = Fighter(1, 200, 310, False, KARTHUS_DATA, karthus_sheet, KARTHUS_ANIMATION_STEPS, magic_fx, object_karthus_data, karthus_projectile)
karthus_2 = Fighter(2, 700, 310, True, KARTHUS_DATA, karthus_sheet, KARTHUS_ANIMATION_STEPS, magic_fx, object_karthus_data, karthus_projectile)
masteryi_1 = Fighter(1, 200, 310, False, MASTERYI_DATA, masteryi_sheet, MASTERYI_ANIMATION_STEPS, sword_fx, object_masteryi_data, masteryi_projectile)
masteryi_2 = Fighter(2, 700, 310, True, MASTERYI_DATA, masteryi_sheet, MASTERYI_ANIMATION_STEPS, sword_fx, object_masteryi_data, masteryi_projectile)
cassiopeia_1 = Fighter(1, 200, 310, False, CASSIOPEIA_DATA, cassiopeia_sheet, CASSIOPEIA_ANIMATION_STEPS, magic_fx, object_cassiopeia_data, cassiopeia_projectile)
cassiopeia_2 = Fighter(2, 700, 310, True, CASSIOPEIA_DATA, cassiopeia_sheet, CASSIOPEIA_ANIMATION_STEPS, magic_fx, object_cassiopeia_data, cassiopeia_projectile)

fighter_1 = type(yasuo_1)
fighter_2 = type(yasuo_1)
avatar_1 = type(avatar_yasuo)
avatar_2 = type(avatar_yasuo)

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

    #draw character buttons
    yasuo_button.draw_border(screen)
    karthus_button.draw_border(screen)
    masteryi_button.draw_border(screen)
    cassiopeia_button.draw_border(screen)

    #write character names
    draw_text("Yasuo", name_font, BLACK, 100, 350)
    draw_text("Karthus", name_font, BLACK, 300, 350)
    draw_text("Master Yi", name_font, BLACK, 500, 350)
    draw_text("Cassiopeia", name_font, BLACK, 700, 350)
    
    if yasuo_check[0] == True:
      screen.blit(player1_img, (80, 212))
    if yasuo_check[1] == True:
      screen.blit(player2_img, (150, 212))
      if (pygame.time.get_ticks() - before_player2 > 2000):
        choose_character = 0
        yasuo_check = [False, False]
        karthus_check = [False, False]
        masteryi_check = [False, False]
        cassiopeia_check = [False, False]
        game_state = "game"
        
    if karthus_check[0] == True:
      screen.blit(player1_img, (280, 212))
    if karthus_check[1] == True:
      screen.blit(player2_img, (350, 212))
      if (pygame.time.get_ticks() - before_player2 > 2000):
        choose_character = 0
        yasuo_check = [False, False]
        karthus_check = [False, False]
        masteryi_check = [False, False]
        cassiopeia_check = [False, False]
        game_state = "game"
        
    if masteryi_check[0] == True:
      screen.blit(player1_img, (480, 212))
    if masteryi_check[1] == True:
      screen.blit(player2_img, (550, 212))
      if (pygame.time.get_ticks() - before_player2 > 2000):
        choose_character = 0
        yasuo_check = [False, False]
        karthus_check = [False, False]
        masteryi_check = [False, False]
        cassiopeia_check = [False, False]
        game_state = "game"
        
    if cassiopeia_check[0] == True:
      screen.blit(player1_img, (680, 212))
    if cassiopeia_check[1] == True:
      screen.blit(player2_img, (750, 212))
      if (pygame.time.get_ticks() - before_player2 > 2000):
        choose_character = 0
        yasuo_check = [False, False]
        karthus_check = [False, False]
        masteryi_check = [False, False]
        cassiopeia_check = [False, False]
        game_state = "game"
        
    if yasuo_button.draw(screen) and choose_character < 2:
      if choose_character == False:
        fighter_1 = yasuo_1
        avatar_1 = avatar_yasuo
        yasuo_check[0] = True
        choose_character += 1
      else:
        fighter_2 = yasuo_2
        avatar_2 = avatar_yasuo
        yasuo_check[1] = True
        choose_character += 1
        before_player2 = pygame.time.get_ticks()

    if karthus_button.draw(screen) and choose_character < 2:
      if choose_character == False:
        fighter_1 = karthus_1
        avatar_1 = avatar_karthus
        karthus_check[0] = True
        choose_character += 1
      else:
        fighter_2 = karthus_2
        avatar_2 = avatar_karthus
        karthus_check[1] = True
        choose_character += 1
        before_player2 = pygame.time.get_ticks()
        
    if masteryi_button.draw(screen) and choose_character < 2:
      if choose_character == False:
        fighter_1 = masteryi_1
        avatar_1 = avatar_masteryi
        masteryi_check[0] = True
        choose_character += 1
      else:
        fighter_2 = masteryi_2
        avatar_2 = avatar_masteryi
        masteryi_check[1] = True
        choose_character += 1
        before_player2 = pygame.time.get_ticks()
        
    if cassiopeia_button.draw(screen) and choose_character < 2:
      if choose_character == False:
        fighter_1 = cassiopeia_1
        avatar_1 = avatar_cassiopeia
        cassiopeia_check[0] = True
        choose_character += 1
      else:
        fighter_2 = cassiopeia_2
        avatar_2 = avatar_cassiopeia
        cassiopeia_check[1] = True
        choose_character += 1
        before_player2 = pygame.time.get_ticks()

  if game_state == "game":
    clock.tick(FPS)

    #draw background
    draw_bg()
    draw_avatar(avatar_1, avatar_2)

    #show player stats
    draw_health_bar(fighter_1.health, 20, 20)
    draw_health_bar(fighter_2.health, 580, 20)
    draw_mana_bar(fighter_1.mana, 20, 55)
    draw_mana_bar(fighter_2.mana, 580, 55)
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
    fighter_1.update(fighter_2)
    fighter_2.update(fighter_1)

    #update mana for fighters
    fighter_1.update_mana()
    fighter_2.update_mana()

    #draw fighters
    fighter_1.draw(screen)
    fighter_2.draw(screen)

      #check for player defeat
    if round_over == False:
      if fighter_1.alive == False:
        score[1] += 1
        round_over = True
        round_over_time = pygame.time.get_ticks()
      elif fighter_2.alive == False:
        score[0] += 1
        round_over = True
        round_over_time = pygame.time.get_ticks()
    else:
      #display victory image
      screen.blit(victory_img, (360, 150))
      if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
        round_over = False
        intro_count = 3
        game_state = "character"
        choose_character = False
        fighter_2.alive = True
        fighter_2.health = 100
        fighter_1.alive = True
        fighter_1.health = 100
        yasuo_1 = Fighter(1, 200, 310, False, YASUO_DATA, yasuo_sheet, YASUO_ANIMATION_STEPS, sword_fx, object_yasuo_data, yasuo_projectile)
        yasuo_2 = Fighter(2, 700, 310, True, YASUO_DATA, yasuo_sheet, YASUO_ANIMATION_STEPS, sword_fx, object_yasuo_data, yasuo_projectile)
        karthus_1 = Fighter(1, 200, 310, False, KARTHUS_DATA, karthus_sheet, KARTHUS_ANIMATION_STEPS, magic_fx, object_karthus_data, karthus_projectile)
        karthus_2 = Fighter(2, 700, 310, True, KARTHUS_DATA, karthus_sheet, KARTHUS_ANIMATION_STEPS, magic_fx, object_karthus_data, karthus_projectile)
        masteryi_1 = Fighter(1, 200, 310, False, MASTERYI_DATA, masteryi_sheet, MASTERYI_ANIMATION_STEPS, sword_fx, object_masteryi_data, masteryi_projectile)
        masteryi_2 = Fighter(2, 700, 310, True, MASTERYI_DATA, masteryi_sheet, MASTERYI_ANIMATION_STEPS, sword_fx, object_masteryi_data, masteryi_projectile)
        cassiopeia_1 = Fighter(1, 200, 310, False, CASSIOPEIA_DATA, cassiopeia_sheet, CASSIOPEIA_ANIMATION_STEPS, magic_fx, object_cassiopeia_data, cassiopeia_projectile)
        cassiopeia_2 = Fighter(2, 700, 310, True, CASSIOPEIA_DATA, cassiopeia_sheet, CASSIOPEIA_ANIMATION_STEPS, magic_fx, object_cassiopeia_data, cassiopeia_projectile)


  #event handler
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False

  #update display
  pygame.display.update()

#exit pygame
pygame.quit()
