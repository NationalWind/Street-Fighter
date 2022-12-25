import pygame

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

class Fighter():
    def __init__(self, x, y, flip, data, character_sheet, animation_steps):
        self.size = data[0]
        self.image_scale = data[1]
        self.offset = data[2]
        self.flip = flip
        self.animation_list = self.load_images(character_sheet, animation_steps)
        self.action = 0 #0: idle #1: run #2:jump #3:attack #4:attack2 #5:hit #6:die
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks()
        self.rect = pygame.Rect((x, y, 80, 180))        #Tạo nv với khung là hình chữ nhật (Rectangle)
        self.vel_y = 0
        self.jump = False
        self.attacking = False
        self.moving = False
        self.attack_type = 0
        self.health = 100

    def load_images(self, character_sheet, animation_steps):
        animation_list =[]
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(10):
                temp_img = character_sheet.subsurface(x * self.size, y * self.size, self.size, self.size)
                temp_img_list.append(pygame.transform.scale(temp_img, (self.size * self.image_scale, self.size * self.image_scale)))
            animation_list.append(temp_img_list)
        return animation_list

    def move(self, screen_width, screen_height, surface, target):
        SPEED = 10
        GRAVITY = 2
        dx = 0
        dy = 0
        self.moving = False

        #get keypresses
        key = pygame.key.get_pressed()

        if self.attacking == False:
            #movement
            if key[pygame.K_a]:
                dx = -SPEED
                self.moving = True
                
            if key[pygame.K_d]:
                dx = SPEED
                self.moving = True

            #jump
            if key[pygame.K_w] and self.jump == False:
                self.vel_y = -30
                self.jump = True

            #attack
            if (key[pygame.K_r] or key[pygame.K_t]):
                self.attack(surface, target)

                #Check loai tan cong nao
                if key[pygame.K_r]:
                    self.attack_type = 1
                if key[pygame.K_t]:
                    self.attack_type = 2

        #Trong luc
        self.vel_y += GRAVITY

        dy += self.vel_y 

        #giữ nhân vật trong màn hình
        if self.rect.left + dx < 0:
            dx = 0
        if  self.rect.right + dx > SCREEN_WIDTH:
            dx = 0
        if self.rect.bottom + dy > SCREEN_HEIGHT - 60:
            self.vel_y = 0
            dy = SCREEN_HEIGHT - 60 - self.rect.bottom
            self.jump = False
        if self.rect.bottom + dy < 0:
            self.vel_y = 0

        #làm cho 2 nhân vật luôn nhìn nhau
        if target.rect.centerx > self.rect.centerx:
            self.flip = False
        else: 
            self.flip = True
            
        
        #cập nhật vị trí nhân vật
        self.rect.x += dx
        self.rect.y += dy

    def update(self):
        animation_cooldown = 100
        if self.jump:
            self.update_action(2)
        elif self.moving:
            self.update_action(1)
        else:
            self.update_action(0)
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            if self.frame_index >= len(self.animation_list[self.action]):
                self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    #Tan cong
    def attack(self, surface, target):
        self.attacking = True
        attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, 2 * self.rect.width, self.rect.height)
        if attacking_rect.colliderect(target.rect):
            target.health -= 10
        
        pygame.draw.rect(surface, (0, 255, 0), attacking_rect)

    def draw(self, surface):
        img = pygame.transform.flip(self.image, self.flip, False)
        
        surface.blit(img, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))