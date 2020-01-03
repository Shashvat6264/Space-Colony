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
pygame.display.set_caption("Space Colony")
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

# Explosion Graphics
expl_folder = os.path.join(img_folder,"explosion")
explosion_anim = []
for i in range(0,10):
    filename = 'E000{}.png'.format(i)
    img = pygame.image.load(path.join(expl_folder, filename)).convert()
    img.set_colorkey(BLACK)
    img_final = pygame.transform.scale(img, (55,55))
    explosion_anim.append(img_final)

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
        self.life = 100

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
        self.speedx = random.randrange(-3,3)
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
                expl = Explosion(self.rect.center)
                all_sprites.add(expl)
                self.kill()
                return 0
            for hit in ghits:
                expl = Explosion(self.rect.center)
                all_sprites.add(expl)
                self.kill()
                return 1
            for hit in bhits:
                expl = Explosion(self.rect.center)
                all_sprites.add(expl)
                self.kill()
                return 1
            for hit in whits:
                expl = Explosion(self.rect.center)
                all_sprites.add(expl)
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
                expl = Explosion(self.rect.center)
                all_sprites.add(expl)
                self.kill()
                return 0
            for hit in rhits:
                expl = Explosion(self.rect.center)
                all_sprites.add(expl)
                self.kill()
                return 1
            for hit in bhits:
                expl = Explosion(self.rect.center)
                all_sprites.add(expl)
                self.kill()
                return 1
            for hit in whits:
                expl = Explosion(self.rect.center)
                all_sprites.add(expl)
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
                expl = Explosion(self.rect.center)
                all_sprites.add(expl)
                self.kill()
                return 0
            for hit in ghits:
                expl = Explosion(self.rect.center)
                all_sprites.add(expl)
                self.kill()
                return 1
            for hit in rhits:
                expl = Explosion(self.rect.center)
                all_sprites.add(expl)
                self.kill()
                return 1
            for hit in whits:
                expl = Explosion(self.rect.center)
                all_sprites.add(expl)
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
                expl = Explosion(self.rect.center)
                all_sprites.add(expl)
                self.kill()
                return 0
            for hit in ghits:
                expl = Explosion(self.rect.center)
                all_sprites.add(expl)
                self.kill()
                return 1
            for hit in bhits:
                expl = Explosion(self.rect.center)
                all_sprites.add(expl)
                self.kill()
                return 1
            for hit in rhits:
                expl = Explosion(self.rect.center)
                all_sprites.add(expl)
                self.kill()
                return 1

# Explosion Sprite
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.image = explosion_anim[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.frame += 1
            if self.frame == len(explosion_anim):
                self.kill()
            else: 
                center = self.rect.center
                self.image = explosion_anim[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

# Initilize all elements
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
rmobs = pygame.sprite.Group()
gmobs = pygame.sprite.Group()
bmobs = pygame.sprite.Group()
wmobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()

def get_high_score():
    high_score = 0
    try:
        high_score_file = open("high_score.txt","r")
        high_score = int(high_score_file.read())
        high_score_file.close()
    except:
        print("Error")
    return high_score

def save_high_score(new_high_score):
    try:
        high_score_file = open("high_score.txt","w")
        high_score_file.write(str(new_high_score))
        high_score_file.close()
    except:
        print("Error")

def show_go_screen():
    screen.fill(BLACK)
    high_score = get_high_score()
    draw_text(screen, "Welcome to Space Colony", 25, WIDTH/2, (HEIGHT/2)-30)
    draw_text(screen, "Press Space to Continue", 18, WIDTH/2, HEIGHT/2)
    draw_text(screen,"High Score: " + str(high_score), 18, WIDTH/2, HEIGHT/2 + 30)
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
    high_score = get_high_score()
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
        diflvl = 0
        lvl = 1

    clock.tick(FPS)
    #Process Input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #Update
    all_sprites.update()
    hits = pygame.sprite.spritecollide(player,mobs,True)
    for hit in hits:
        player.life -= 20
        expl = Explosion(player.rect.center)
        all_sprites.add(expl)
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
        if player.life <= 0:
            game_over = True
            if score > high_score:
                save_high_score(score)
    for bullet in bullets:
        res = bullet.mobcollide(mobs,rmobs,gmobs,bmobs,wmobs)
        if res==1 :
            game_over = True
            if score > high_score:
                save_high_score(score)
        elif res==0 :
            score += 1
            diflvl += 1
    for mi in mobs:
        if mi.rect.top > HEIGHT + 10 or mi.rect.left < -25 or mi.rect.right > WIDTH + 25:
            mi.kill()
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


            
    
    if diflvl >= 5:
        diflvl -= 5
        lvl += 1
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

    
    #Draw
    screen.fill(BLACK)
    screen.blit(background,background_rect)
    draw_text(screen, "Level: " + str(lvl), 18, 32, 9)
    draw_text(screen, "Score: " + str(score), 18, WIDTH/2 , 10)
    draw_text(screen,"Life: "+ str(player.life), 18, WIDTH - 35, 9)
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()
