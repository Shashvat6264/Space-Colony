import pygame
import random
import os
from os import path

FPS = 60
WIDTH = 480
HEIGHT = 600
NMOBS = 6

# Colours
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
WHITE = (255,255,255)

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("WOW")
clock = pygame.time.Clock()

game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder,"img")

font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

#Load all Graphics

# Load Background
background = pygame.image.load(os.path.join(img_folder, "background.png"))
background_rect = background.get_rect()

# Player Graphics
player_folder = os.path.join(img_folder,"player")
red_player = pygame.transform.scale(pygame.image.load(os.path.join(player_folder, "red.png")).convert(),(50,50))
blue_player = pygame.transform.scale(pygame.image.load(os.path.join(player_folder, "blue.png")).convert(),(50,50))
green_player = pygame.transform.scale(pygame.image.load(os.path.join(player_folder, "green.png")).convert(),(50,50))
white_player = pygame.transform.scale(pygame.image.load(os.path.join(player_folder, "white.png")).convert(),(50,50))

# Laser Graphics
laser_folder = os.path.join(img_folder,"laser")
red_laser = pygame.image.load(os.path.join(laser_folder, "red.png")).convert()
blue_laser = pygame.image.load(os.path.join(laser_folder, "blue.png")).convert()
green_laser = pygame.image.load(os.path.join(laser_folder, "green.png")).convert()
white_laser = pygame.transform.scale(pygame.image.load(os.path.join(laser_folder, "white.png")).convert(),(10,10))

# Mob Graphics
mob_folder = os.path.join(img_folder,"mob")
red_mob = pygame.transform.scale(pygame.image.load(os.path.join(mob_folder, "red.png")).convert(),(35,35))
blue_mob = pygame.transform.scale(pygame.image.load(os.path.join(mob_folder, "blue.png")).convert(),(35,35))
green_mob = pygame.transform.scale(pygame.image.load(os.path.join(mob_folder, "green.png")).convert(),(35,35))
white_mob = pygame.transform.scale(pygame.image.load(os.path.join(mob_folder, "white.png")).convert(),(35,35))

# Player Sprite
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 40))
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.colist_ind = random.randrange(0,4)
        if self.colist_ind == 0:
            self.image = red_player
        elif self.colist_ind == 1:
            self.image = green_player
        elif self.colist_ind == 2:
            self.image = blue_player
        elif self.colist_ind == 3:
            self.image = white_player
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.image.set_colorkey(BLACK)

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        if keystate[pygame.K_SPACE]:
            self.shoot()
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        self.rect.x += self.speedx
       

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.centerx,self.rect.top,self.colist_ind)
            bullets.add(bullet)
            all_sprites.add(bullet)
            self.colist_ind = random.randrange(0,4)
            if self.colist_ind == 0:
                self.image = red_player
            elif self.colist_ind == 1:
                self.image = green_player
            elif self.colist_ind == 2:
                self.image = blue_player
            elif self.colist_ind == 3:
                self.image = white_player
            self.image.set_colorkey(BLACK)

# Mob Elements   
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30,40))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100,-40)
        self.speedy = random.randrange(3,8)
        self.speedx = random.randrange(-1,3)
        self.colist_ind = random.randrange(0,4)
        if self.colist_ind == 0:
            self.image = red_mob
        elif self.colist_ind == 1:
            self.image = green_mob
        elif self.colist_ind == 2:
            self.image = blue_mob
        elif self.colist_ind == 3:
            self.image = white_mob
        self.image.set_colorkey(BLACK)

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 25:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100,-40)
            self.speedy = random.randrange(1,8)

# Bullet Sprite
class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y,color):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10,30))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -20
        self.colist_ind = color
        if color == 0:
            self.image = red_laser
        elif color == 1:
            self.image = green_laser
        elif color == 2:
            self.image = blue_laser
        elif color == 3:
            self.image = white_laser
        self.image.set_colorkey(BLACK)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0 :
            self.kill()

    def mobcollide(self,mobs,rmobs,gmobs,bmobs,wmobs):
        rhits = pygame.sprite.spritecollide(self, rmobs, True)
        ghits = pygame.sprite.spritecollide(self, gmobs, True)
        bhits = pygame.sprite.spritecollide(self, bmobs, True)
        whits = pygame.sprite.spritecollide(self, wmobs, True)
        if self.colist_ind == 0:
            for hit in rhits:
                m = Mob()
                mobs.add(m)
                all_sprites.add(m)
                if m.colist_ind == 0:
                    rmobs.add(m)
                elif m.colist_ind == 1:
                    gmobs.add(m)
                elif m.colist_ind == 2:
                    bmobs.add(m)
                elif m.colist_ind == 3:
                    wmobs.add(m)
                self.kill()
                return 0
            for hit in ghits:
                self.kill()
                return 1
            for hit in bhits:
                self.kill()
                return 1
            for hit in whits:
                self.kill()
                return 1
        elif self.colist_ind == 1:
            for hit in ghits:
                m = Mob()
                mobs.add(m)
                all_sprites.add(m)
                if m.colist_ind == 0:
                    rmobs.add(m)
                elif m.colist_ind == 1:
                    gmobs.add(m)
                elif m.colist_ind == 2:
                    bmobs.add(m)
                elif m.colist_ind == 3:
                    wmobs.add(m)
                self.kill()
                return 0
            for hit in rhits:
                self.kill()
                return 1
            for hit in bhits:
                self.kill()
                return 1
            for hit in whits:
                self.kill()
                return 1

        elif self.colist_ind == 2:
            for hit in bhits:
                m = Mob()
                mobs.add(m)
                all_sprites.add(m)
                if m.colist_ind == 0:
                    rmobs.add(m)
                elif m.colist_ind == 1:
                    gmobs.add(m)
                elif m.colist_ind == 2:
                    bmobs.add(m)
                elif m.colist_ind == 3:
                    wmobs.add(m)
                self.kill()
                return 0
            for hit in ghits:
                self.kill()
                return 1
            for hit in rhits:
                self.kill()
                return 1
            for hit in whits:
                self.kill()
                return 1
        elif self.colist_ind == 3:
            for hit in whits:
                m = Mob()
                mobs.add(m)
                all_sprites.add(m)
                if m.colist_ind == 0:
                    rmobs.add(m)
                elif m.colist_ind == 1:
                    gmobs.add(m)
                elif m.colist_ind == 2:
                    bmobs.add(m)
                elif m.colist_ind == 3:
                    wmobs.add(m)
                self.kill()
                return 0
            for hit in ghits:
                self.kill()
                return 1
            for hit in bhits:
                self.kill()
                return 1
            for hit in rhits:
                self.kill()
                return 1

# Initilize all elements
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
rmobs = pygame.sprite.Group()
gmobs = pygame.sprite.Group()
bmobs = pygame.sprite.Group()
wmobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()


def show_go_screen():
    screen.fill(BLACK)
    draw_text(screen, "Welcome to Space Colony", 25, WIDTH/2, (HEIGHT/2)-30)
    draw_text(screen, "Press Space to Continue", 18, WIDTH/2, HEIGHT/2)
    loop = True
    pygame.display.flip()
    while loop:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                loop = False
        
# Game Loop
game_over = True
running = True
while running:
    if game_over:
        show_go_screen()
        game_over = False
        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        rmobs = pygame.sprite.Group()
        gmobs = pygame.sprite.Group()   
        bmobs = pygame.sprite.Group()
        wmobs = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        for i in range(1,NMOBS):
            m = Mob()
            mobs.add(m)
            all_sprites.add(m)
            if m.colist_ind == 0:
                rmobs.add(m)
            elif m.colist_ind == 1:
                gmobs.add(m)
            elif m.colist_ind == 2:
                bmobs.add(m)
            elif m.colist_ind == 3:
                wmobs.add(m)
        player = Player()
        all_sprites.add(player)
        score = 0

    clock.tick(FPS)
    #Process Input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #Update
    all_sprites.update()
    hits = pygame.sprite.spritecollide(player,mobs,True)
    for hit in hits:
        game_over = True
    for bullet in bullets:
        res = bullet.mobcollide(mobs,rmobs,gmobs,bmobs,wmobs)
        if res==1 :
            game_over = True
        elif res==0 :
            score += 1
    
    #Draw
    screen.fill(BLACK)
    screen.blit(background,background_rect)
    draw_text(screen, "Score: " + str(score), 18, WIDTH/2 , 10)
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()
