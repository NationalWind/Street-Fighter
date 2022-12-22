import pygame
import time

class Projectile():
    def __init__(self, x, y, flip):
        self.size = 16
        self.image_scale = 20
        self.offset = [12, 5]
        self.image  = pygame.image.load("assets\images\warrior\Sprites\skillwave.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.size * self.image_scale, self.size * self.image_scale))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.flip = flip
        self.speed = 15
        #self.image2 = self.load_images(self.image, 1)


    def move(self):
        # move projectile in the correct direction
        if self.flip:
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed
    
    #def load_images(self, skill_sheet, skill_steps):
      #animation_list = []
      #for x in range(skill_steps):
        #temp_img = self.image.subsurface(x * self.size, self.size, self.size, self.size)
        #animation_list.append(pygame.transform.scale(temp_img, (self.size * self.image_scale, self.size * self.image_scale)))
      #return animation_list
    
    def draw(self, surface):
      if self.flip:
            surface.blit(pygame.transform.flip(self.image, True, False), (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))
      else:
            surface.blit(self.image, (self.rect.x - (self.offset[0] * self.image_scale) + 100, self.rect.y - (self.offset[1] * self.image_scale)))


class Fighter():
  def __init__(self, player, x, y, flip, data, sprite_sheet, animation_steps, sound):
    self.player = player
    self.size = data[0]
    self.image_scale = data[1]
    self.offset = data[2]
    self.flip = flip
    self.animation_list = self.load_images(sprite_sheet, animation_steps)
    self.action = 0#0:idle #1:run #2:jump #3:attack1 #4: attack2 #5:hit #6:death
    self.frame_index = 0
    self.image = self.animation_list[self.action][self.frame_index]
    self.update_time = pygame.time.get_ticks()
    self.rect = pygame.Rect((x, y, 80, 180))
    self.vel_y = 0
    self.running = False
    self.jump = False
    self.attacking = False
    self.skilling = False
    self.attack_type = 0
    self.attack_cooldown = 1
    self.attack_sound = sound
    self.hit = False
    self.health = 100
    self.alive = True
    self.projectiles = []
    self.skill_cooldown = 0
    self.attack_start_time = time.time() + 1000
    self.label_time = 0
    self.mana = 100
  

  def load_images(self, sprite_sheet, animation_steps):
    #extract images from spritesheet
    animation_list = []
    for y, animation in enumerate(animation_steps):
      temp_img_list = []
      for x in range(animation):
        temp_img = sprite_sheet.subsurface(x * self.size, y * self.size, self.size, self.size)
        temp_img_list.append(pygame.transform.scale(temp_img, (self.size * self.image_scale, self.size * self.image_scale)))
      animation_list.append(temp_img_list)
    return animation_list


  def move(self, screen_width, screen_height, surface, target, round_over):
    SPEED = 10
    GRAVITY = 2
    dx = 0
    dy = 0
    self.running = False
    self.attack_type = 0

    #get keypresses
    key = pygame.key.get_pressed()

    #can only perform other actions if not currently attacking
    if self.attacking == False and self.skilling == False and self.alive == True and round_over == False:
      #check player 1 controls
      if self.player == 1:
        #movement
        if key[pygame.K_a]:
          dx = -SPEED
          self.running = True
        if key[pygame.K_d]:
          dx = SPEED
          self.running = True
        #jump
        if key[pygame.K_w] and self.jump == False:
          self.vel_y = -30
          self.jump = True
        #attack
        if key[pygame.K_r] or key[pygame.K_t]:
          #determine which attack type was used
          if key[pygame.K_r]:
            self.attack_type = 1
            self.attack(target)
          if key[pygame.K_t]:
            self.attack_type = 2
            self.skill1(target)

      #check player 2 controls
      if self.player == 2:
        #movement
        if key[pygame.K_LEFT]:
          dx = -SPEED
          self.running = True
        if key[pygame.K_RIGHT]:
          dx = SPEED
          self.running = True
        #jump
        if key[pygame.K_UP] and self.jump == False:
          self.vel_y = -30
          self.jump = True
        #attack
        if key[pygame.K_KP1] or key[pygame.K_KP2]:
          #determine which attack type was used
          if key[pygame.K_KP1]:
            self.attack_type = 1
            self.attack(target)
          if key[pygame.K_KP2]:
            self.attack_type = 2
            self.skill1(target)

    #apply gravity
    self.vel_y += GRAVITY
    dy += self.vel_y

    #ensure player stays on screen
    if self.rect.left + dx < 0:
      dx = -self.rect.left
    if self.rect.right + dx > screen_width:
      dx = screen_width - self.rect.right
    if self.rect.bottom + dy > screen_height - 110:
      self.vel_y = 0
      self.jump = False
      dy = screen_height - 110 - self.rect.bottom

    #ensure players face each other
    if target.rect.centerx > self.rect.centerx:
      self.flip = False
    else:
      self.flip = True

    #apply attack cooldown
    if self.attack_cooldown > 0:
      self.attack_cooldown -= 1
      self.skill_cooldown -= 1

    #update player position
    self.rect.x += dx
    self.rect.y += dy

  #handle animation updates
  def update(self, target):
    #check what action the player is performing
    if self.health <= 0:
      self.health = 0
      self.alive = False
      self.update_action(6)#6:death
    elif self.hit == True:
      self.update_action(5)#5:hit
    elif self.attacking == True:
      self.update_action(3)#3:attack1
    elif self.skilling == True:
        self.update_action(4)#4:attack2
    elif self.jump == True:
      self.update_action(2)#2:jump
    elif self.running == True:
      self.update_action(1)#1:run
    else:
      self.update_action(0)#0:idle
    if (self.skilling == True):
      self.label_time = time.time() - self.attack_start_time
    if self.label_time >= 0.3:
      self.projectiles.append(Projectile(self.rect.x + 20, self.rect.y, self.flip))
      self.attack_start_time = time.time() + 1000

    animation_cooldown = 50
    #update image
    self.image = self.animation_list[self.action][self.frame_index]
    #check if enough time has passed since the last update
    if pygame.time.get_ticks() - self.update_time > animation_cooldown:
      self.frame_index += 1
      self.update_time = pygame.time.get_ticks()
    #check if the animation has finished
    if self.frame_index >= len(self.animation_list[self.action]):
      #if the player is dead then end the animation
      if self.alive == False:
        self.frame_index = len(self.animation_list[self.action]) - 1
      else:
        self.frame_index = 0
        #check if an attack was executed
        if self.action == 3 or self.action == 4:
          self.attacking = False
          self.skilling = False
          self.attack_cooldown = 20
          self.skill_cooldown = 21
        #check if damage was taken
        if self.action == 5:
          self.hit = False
          #if the player was in the middle of an attack, then the attack is stopped
          self.attacking = False
          self.skilling = False
          self.attack_cooldown = 20
          self.skill_cooldown = 20
    
    for projectile in self.projectiles:
      projectile.move()
      if projectile.rect.left > 1280 or projectile.rect.right < 0:
        self.projectiles.remove(projectile)
      projectile_rect = pygame.Rect(projectile.rect.x, projectile.rect.y + 30, 30, 30)
      if projectile_rect.colliderect(target.rect) and target.hit == False:
        target.health -= 10
        target.hit = True
        self.projectiles.remove(projectile)


  def attack(self, target):
    if self.attack_cooldown == 0:
      #execute attack
      self.attacking = True
      self.attack_sound.play()
      attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, 2 * self.rect.width, self.rect.height)
      if attacking_rect.colliderect(target.rect):
        target.health -= 10
        target.hit = True
      self.attack_cooldown = pygame.time.get_ticks()
    
  def skill1(self, target):
    if self.attack_cooldown == 0:
      #execute attack
      self.skilling = True
      self.attack_sound.play()
      self.attack_start_time = time.time()
      #self.projectiles.append(Projectile(self.rect.x, self.rect.y, self.flip))
      self.attack_cooldown = pygame.time.get_ticks()

  def update_action(self, new_action):
    #check if the new action is different to the previous one
    if new_action != self.action:
      self.action = new_action
      #update the animation settings
      self.frame_index = 0
      self.update_time = pygame.time.get_ticks()

  def draw(self, surface):
    img = pygame.transform.flip(self.image, self.flip, False)
    surface.blit(img, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))

    for projectile in self.projectiles:
      projectile.draw(surface)