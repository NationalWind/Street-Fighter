import pygame
import textwrap
from button import Button
from pygame import mixer
from fighter import Fighter

mixer.init()
pygame.init()

#create game window
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Street Fighter")
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
BROWN = (100, 40, 0)

#define game variables
intro_count = 3
last_count_update = pygame.time.get_ticks()
score = [0, 0]#player scores. [P1, P2]
round_over = False
ROUND_OVER_COOLDOWN = 2000
choose_character = 0
sound_fx = 0


#define fighter variables
YASUO_SIZE = 200
YASUO_SCALE = 4
YASUO_OFFSET = [90, 77]
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
yasuo_fx = pygame.mixer.Sound("assets/audio/Yasuo.mp3")
yasuo_fx.set_volume(1.5)
ko_fx = pygame.mixer.Sound("assets/audio/KO.mp3")
ko_fx.set_volume(0.75)

#load background image
bg_image = pygame.image.load("assets/images/background/background.jpg").convert_alpha()
menu_image = pygame.image.load("assets/images/background/background_street.png").convert_alpha()

#load item icon
timer_img = pygame.image.load("assets/images/icons/timer.png")
border_img = pygame.image.load("assets/images/buttons/frame.png")

#load beginning buttons
back_image = pygame.image.load("assets/images/buttons/back.png").convert_alpha()
back_button = Button(0, 0, back_image, 0.5)
start_image = pygame.image.load("assets/images/buttons/start.png").convert_alpha()
start_button = Button(370, 150, start_image, 0.75)
setting_image = pygame.image.load("assets/images/buttons/setting.png").convert_alpha()
setting_button = Button(370, 300, setting_image, 0.75)
exit_image = pygame.image.load("assets/images/buttons/exit.png").convert_alpha()
exit_button = Button(370, 450, exit_image, 0.75)
sound_on_image = pygame.image.load("assets/images/buttons/sound_on.png").convert_alpha()
sound_on_button = Button(300, 175, sound_on_image, 1)
sound_off_image = pygame.image.load("assets/images/buttons/sound_off.png").convert_alpha()
sound_off_button = Button(500, 175, sound_off_image, 1)
credits_image = pygame.image.load("assets/images/buttons/credits.png").convert_alpha()
credits_button = Button(811, 531, credits_image, 1)


#load avatar
avatar_yasuo = pygame.image.load("assets/images/avatar/yasuo.png").convert_alpha()
avatar_karthus = pygame.image.load("assets/images/avatar/karthus.png").convert_alpha()
avatar_masteryi = pygame.image.load("assets/images/avatar/masteryi.png").convert_alpha()
avatar_cassiopeia = pygame.image.load("assets/images/avatar/cassiopeia.png").convert_alpha()

#load character choosing buttons
yasuo_button = Button(100, 250, avatar_yasuo, 1.5)
yasuo_check = [False, False]
karthus_button = Button(300, 250, avatar_karthus, 1.5)
karthus_check = [False, False]
masteryi_button = Button(500, 250, avatar_masteryi, 1.5)
masteryi_check = [False, False]
cassiopeia_button = Button(700, 250, avatar_cassiopeia, 1.5)
cassiopeia_check = [False, False]


#load spritesheets
yasuo_sheet = pygame.image.load("assets/images/characters/yasuo.png").convert_alpha()
karthus_sheet = pygame.image.load("assets/images/characters/karthus.png").convert_alpha()
masteryi_sheet = pygame.image.load("assets/images/characters/masteryi.png").convert_alpha()
cassiopeia_sheet = pygame.image.load("assets/images/characters/cassiopeia.png").convert_alpha()

#load projectile image
yasuo_projectile = pygame.image.load("assets/images/warrior/Skillwave_Yasuo.png").convert_alpha()
karthus_projectile = pygame.image.load("assets/images/warrior/Skillwave_Karthus.png").convert_alpha()
masteryi_projectile = pygame.image.load("assets/images/warrior/Skillwave_MasterYi.png").convert_alpha()
cassiopeia_projectile = pygame.image.load("assets/images/warrior/Skillwave_Karthus.png").convert_alpha()

#load health and mana bar image
health_border_img = pygame.image.load("assets/images/health_bar/border2.png")
yellow_health_img = pygame.image.load("assets/images/health_bar/yellow_health_crop.png")
red_health_img = pygame.image.load("assets/images/health_bar/red_health.png")
mana_bar_img = pygame.image.load("assets/images/health_bar/mana_bar.png")
white_bar_img = pygame.image.load("assets/images/health_bar/white_bar.png")

#load game icons image
KO_img = pygame.image.load("assets/images/icons/KO_resize.png").convert_alpha()
player1_img = pygame.image.load("assets/images/icons/player1.png").convert_alpha()
player2_img = pygame.image.load("assets/images/icons/player2.png").convert_alpha()
sound_img = pygame.image.load("assets/images/icons/sound.png").convert_alpha()
button_img = pygame.image.load("assets/images/icons/button.png").convert_alpha()

#load key images
w_key_image = pygame.image.load("assets/images/keys/W-Key.png").convert_alpha()
a_key_image = pygame.image.load("assets/images/keys/A-Key.png").convert_alpha()
s_key_image = pygame.image.load("assets/images/keys/S-Key.png").convert_alpha()
d_key_image = pygame.image.load("assets/images/keys/D-Key.png").convert_alpha()
r_key_image = pygame.image.load("assets/images/keys/R-Key.png").convert_alpha()
t_key_image = pygame.image.load("assets/images/keys/T-Key.png").convert_alpha()

up_key_image = pygame.image.load("assets/images/keys/Up-Key.png").convert_alpha()
left_key_image = pygame.image.load("assets/images/keys/Left-Key.png").convert_alpha()
down_key_image = pygame.image.load("assets/images/keys/Down-Key.png").convert_alpha()
right_key_image = pygame.image.load("assets/images/keys/Right-Key.png").convert_alpha()
one_key_image = pygame.image.load("assets/images/keys/1-Key.png").convert_alpha()
two_key_image = pygame.image.load("assets/images/keys/2-Key.png").convert_alpha()
n_key_image = pygame.image.load("assets/images/keys/N-Key.png").convert_alpha()
m_key_image = pygame.image.load("assets/images/keys/M-Key.png").convert_alpha()

#define number of steps in each animation
YASUO_ANIMATION_STEPS = [8, 8, 2, 6, 6, 4, 6]
KARTHUS_ANIMATION_STEPS = [8, 8, 1, 8, 8, 3, 7]
MASTERYI_ANIMATION_STEPS = [10, 8, 1, 7, 7, 3, 7]
CASSIOPEIA_ANIMATION_STEPS = [9, 9, 1, 16, 16, 3, 8]
  
#define font
count_font = pygame.font.Font("assets/fonts/turok.ttf", 80)
name_font = pygame.font.Font("assets/fonts/gunfighter-academy.ttf", 20)
main_font = pygame.font.Font("assets/fonts/gunfighter-academy.ttf", 50)
score_font = pygame.font.Font("assets/fonts/turok.ttf", 30)
credits_font = pygame.font.Font("assets/fonts/FVF Fernando 08.ttf", 20)

#function for drawing text
def draw_text(text, font, text_col, x, y):
  img = font.render(text, True, text_col)
  screen.blit(img, (x, y))

def draw_text_right(text, font, text_col, x, y):
  img = font.render(text, True, text_col)
  text_rect = font.render(text, True, text_col).get_rect()
  text_rect.x = x - text_rect.width
  text_rect.y = y
  screen.blit(img, text_rect)

def draw_text_center(text, font, text_col, y):
  img = font.render(text, True, text_col)
  rect = img.get_rect()
  x = (SCREEN_WIDTH - rect.width) // 2
  screen.blit(img, (x, y))
  
#function for drawing background
def draw_bg(bg):
  scaled_bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
  screen.blit(scaled_bg, (0, 0))

#function for drawing fighter health bars
def draw_health_bar(health, x, y, flip):
  ratio = health / 100
  health_bar = pygame. Rect(x - 65, y - 130, 400, 34)
  health_bar_red = pygame.Rect(x - 40, y - 30, 400, 34)
  if flip == True:
    health_bar_yellow = pygame.Rect(x + 400 * (1 - ratio), y, 400, 30)
  else:
    health_bar_yellow = pygame.Rect(x - 5, y, 400, 30)

  #Khung mau den
  scaled_border = pygame.transform.scale(health_border_img, (SCREEN_WIDTH / 2 + 50, SCREEN_HEIGHT / 2 + 15))
  scaled_border = pygame.transform.flip(scaled_border, flip, False)
  screen.blit(scaled_border, health_bar)

  #Thanh hp mau do
  scaled_red = pygame.transform.scale(red_health_img, ((SCREEN_WIDTH / 2), SCREEN_HEIGHT / 5 - 10))
  screen.blit(scaled_red, health_bar_red)

  #Thanh hp mau vang
  scaled_yellow = pygame.transform.scale(yellow_health_img, ((SCREEN_WIDTH / 2 - 80)* ratio, SCREEN_HEIGHT / 15))
  screen.blit(scaled_yellow, health_bar_yellow)

def draw_mana_bar(mana, x, y, flip):
  ratio = mana / 100
  scaled_white = pygame.transform.scale(white_bar_img, ((SCREEN_WIDTH / 3), SCREEN_HEIGHT / 50))
  screen.blit(scaled_white, (x, y + 5))
  scaled_cyan = pygame.transform.scale(mana_bar_img, ((SCREEN_WIDTH / 3) * ratio, SCREEN_HEIGHT / 50))

  if flip == True:
    screen.blit(scaled_cyan, (x + (SCREEN_WIDTH / 3) * (1 - ratio), y + 5))
  else: 
    screen.blit(scaled_cyan, (x, y + 5))

#function for drawing avatar
def draw_avatar(avatar1, avatar2):
  screen.blit(avatar1, (400, 0))

  avatar2 = pygame.transform.flip(avatar2, True, False)
  screen.blit(avatar2, (500, 0))

def draw_timer():
  scaled_timer = pygame.transform.scale(timer_img, (SCREEN_WIDTH / 4, SCREEN_HEIGHT / 4))
  screen.blit(scaled_timer, (375, 0))

#create two instances of fighters
yasuo_1 = Fighter(1, 200, 310, False, YASUO_DATA, yasuo_sheet, YASUO_ANIMATION_STEPS, yasuo_fx, object_yasuo_data, yasuo_projectile)
yasuo_2 = Fighter(2, 700, 310, True, YASUO_DATA, yasuo_sheet, YASUO_ANIMATION_STEPS, yasuo_fx, object_yasuo_data, yasuo_projectile)
karthus_1 = Fighter(1, 200, 310, False, KARTHUS_DATA, karthus_sheet, KARTHUS_ANIMATION_STEPS, magic_fx, object_karthus_data, karthus_projectile)
karthus_2 = Fighter(2, 700, 310, True, KARTHUS_DATA, karthus_sheet, KARTHUS_ANIMATION_STEPS, magic_fx, object_karthus_data, karthus_projectile)
masteryi_1 = Fighter(1, 200, 310, False, MASTERYI_DATA, masteryi_sheet, MASTERYI_ANIMATION_STEPS, sword_fx, object_masteryi_data, masteryi_projectile)
masteryi_2 = Fighter(2, 700, 310, True, MASTERYI_DATA, masteryi_sheet, MASTERYI_ANIMATION_STEPS, sword_fx, object_masteryi_data, masteryi_projectile)
cassiopeia_1 = Fighter(1, 200, 310, False, CASSIOPEIA_DATA, cassiopeia_sheet, CASSIOPEIA_ANIMATION_STEPS, magic_fx, object_cassiopeia_data, cassiopeia_projectile)
cassiopeia_2 = Fighter(2, 700, 310, True, CASSIOPEIA_DATA, cassiopeia_sheet, CASSIOPEIA_ANIMATION_STEPS, magic_fx, object_cassiopeia_data, cassiopeia_projectile)

#init variables
fighter_1 = type(yasuo_1)
fighter_2 = type(yasuo_1)
avatar_1 = type(avatar_yasuo)
avatar_2 = type(avatar_yasuo)
name_1 = ""
name_2 = ""

#game loop
run = True
while run:
  if game_state == "menu":
    screen.fill(WHITE)
    draw_bg(bg_image)
    draw_text_center("STREET FIGHTER", main_font, BROWN, 55)
    if start_button.draw(screen):
      game_state = "character"
      
    if setting_button.draw(screen):
      game_state = "setting"
      
    if exit_button.draw(screen):
      run = False
      
  if game_state == "setting":
    screen.fill(WHITE)
    draw_bg(bg_image)
    draw_text_center("GAME SETTINGS", main_font, BROWN, 55)
    screen.blit(sound_img, (150, 190))
    screen.blit(button_img, (150, 400))
    screen.blit(player1_img, (400, 350))
    screen.blit(player2_img, (700, 350))

    screen.blit(w_key_image, (400, 400))
    screen.blit(s_key_image, (400, 432))
    screen.blit(a_key_image, (368, 432))
    screen.blit(d_key_image, (432, 432))
    screen.blit(r_key_image, (464, 400))
    screen.blit(t_key_image, (496, 400))
    
    screen.blit(up_key_image, (700, 400))
    screen.blit(down_key_image, (700, 432))
    screen.blit(left_key_image, (668, 432))
    screen.blit(right_key_image, (732, 432))
    screen.blit(one_key_image, (764, 400))
    screen.blit(two_key_image, (796, 400))
    draw_text("OR", credits_font, WHITE, 848, 390)
    screen.blit(n_key_image, (900, 400))
    screen.blit(m_key_image, (932, 400))

    if credits_button.draw(screen):
      game_state = "credits"
    if back_button.draw(screen):
      game_state = "menu"
    if (sound_fx % 2 == 0):
      pygame.mixer.music.set_volume(0.5)
      sword_fx.set_volume(0.5)
      magic_fx.set_volume(0.75)
      yasuo_fx.set_volume(1.5)
      ko_fx.set_volume(0.75)
      if (sound_on_button.draw(screen)):
        sound_fx += 1
    else:
      pygame.mixer.music.set_volume(0)
      sword_fx.set_volume(0)
      magic_fx.set_volume(0)
      yasuo_fx.set_volume(0)
      ko_fx.set_volume(0)
      if (sound_off_button.draw(screen)):
        sound_fx += 1

  if game_state == "credits":
    screen.fill(WHITE)
    draw_bg(bg_image)
    draw_text_center("CREDITS", main_font, BROWN, 55)
    draw_text_center("ORIGINAL IDEAS: CODING WITH RUSS", credits_font, BLACK, 150)
    draw_text_center("Group 4", score_font, BLACK, 250)
    draw_text_center("LEADER: Trần Quốc Phong - 22127327", credits_font, WHITE, 350)
    draw_text_center("MEMBER: Lê Ngọc Vĩ - 22127452", credits_font, WHITE, 400)
    draw_text_center("MEMBER: Lâm Chí Tài - 22127370", credits_font, WHITE, 450)
    draw_text_center("MEMBER: Lê Quốc Khánh - 22127186", credits_font, WHITE, 500)
    draw_text_center("MEMBER: Trang Ngọc Châu - 22127044", credits_font, WHITE, 550)
    if (back_button.draw(screen)):
      game_state = "setting"
    
  if game_state == "character":
    screen.fill(WHITE)
    draw_bg(bg_image)
    if back_button.draw(screen):
      game_state = "menu"
      choose_character = 0
      yasuo_check = [False, False]
      karthus_check = [False, False]
      masteryi_check = [False, False]
      cassiopeia_check = [False, False]
    #draw character buttons
    screen.blit(border_img, (100, 253))
    screen.blit(border_img, (300, 253))
    screen.blit(border_img, (500, 253))
    screen.blit(border_img, (700, 253))

    draw_text_center("CHOOSE YOUR FIGHTER", main_font, BROWN, 55)
    #write character names
    draw_text("Yasuo", name_font, WHITE, 100, 400)
    draw_text("Karthus", name_font, WHITE, 300, 400)
    draw_text("Master Yi", name_font, WHITE, 500, 400)
    draw_text("Cassiopeia", name_font, WHITE, 700, 400)
    
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
      if choose_character == 0:
        fighter_1 = yasuo_1
        avatar_1 = avatar_yasuo
        yasuo_check[0] = True
        choose_character += 1
        name_1 = "Yasuo"
      elif choose_character == 1:
        fighter_2 = yasuo_2
        avatar_2 = avatar_yasuo
        yasuo_check[1] = True
        choose_character += 1
        name_2 = "Yasuo"
        before_player2 = pygame.time.get_ticks()

    if karthus_button.draw(screen) and choose_character < 2:
      if choose_character == 0:
        fighter_1 = karthus_1
        avatar_1 = avatar_karthus
        karthus_check[0] = True
        choose_character += 1
        name_1 = "Karthus"
      elif choose_character == 1:
        fighter_2 = karthus_2
        avatar_2 = avatar_karthus
        karthus_check[1] = True
        choose_character += 1
        name_2 = "Karthus"
        before_player2 = pygame.time.get_ticks()
        
    if masteryi_button.draw(screen) and choose_character < 2:
      if choose_character == 0:
        fighter_1 = masteryi_1
        avatar_1 = avatar_masteryi
        masteryi_check[0] = True
        choose_character += 1
        name_1 = "Master Yi"
      elif choose_character == 1:
        fighter_2 = masteryi_2
        avatar_2 = avatar_masteryi
        masteryi_check[1] = True
        choose_character += 1
        name_2 = "Master Yi"
        before_player2 = pygame.time.get_ticks()
        
    if cassiopeia_button.draw(screen) and choose_character < 2:
      if choose_character == 0:
        fighter_1 = cassiopeia_1
        avatar_1 = avatar_cassiopeia
        cassiopeia_check[0] = True
        choose_character += 1
        name_1 = "Cassiopeia"
      elif choose_character == 1:
        fighter_2 = cassiopeia_2
        avatar_2 = avatar_cassiopeia
        cassiopeia_check[1] = True
        choose_character += 1
        name_2 = "Cassiopeia"
        before_player2 = pygame.time.get_ticks()

  if game_state == "game":
    clock.tick(FPS)

    #draw background
    draw_bg(bg_image)

    #show player stats
    draw_health_bar(fighter_1.health, 20, 20, False)
    draw_health_bar(fighter_2.health, 580, 20, True)
    draw_mana_bar(fighter_1.mana, 20, 55, False)
    draw_mana_bar(fighter_2.mana, 650, 55, True)
    draw_text("P1: " + str(score[0]), score_font, RED, 360, 60)
    draw_text("P2: " + str(score[1]), score_font, BLUE, 580, 60)
    draw_text(name_1, name_font, RED, 20, 70)
    draw_text_right(name_2, name_font, BLUE, 985, 70)
    draw_timer()

    draw_avatar(avatar_1, avatar_2)
    
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
      #display KO
      screen.blit(KO_img, (SCREEN_WIDTH / 4 - 50, SCREEN_HEIGHT / 4))
      ko_fx.play()
      if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
        round_over = False
        intro_count = 3
        game_state = "character"
        choose_character = False
        fighter_2.alive = True
        fighter_2.health = 100
        fighter_1.alive = True
        fighter_1.health = 100
        fighter_1.mana = 100
        fighter_2.mana = 100
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
