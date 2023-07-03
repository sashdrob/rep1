import pygame as p
import random as r
import math as m
WIDTH=600
HEIGHT=1000
player_img=p.transform.scale(p.image.load('img/Player.png'),(96,112))
enemy1_img=p.transform.scale(p.image.load('img/Enemy1.png'),(32,36))
enemy2_img=p.transform.scale(p.image.load('img/Enemy2.png'),(48,60))
enemy3_img=p.transform.scale(p.image.load('img/Enemy3.png'),(64,72))
rocket_img=p.transform.scale(p.image.load('img/Rocket.png'),(4,28))
enemy_rocket_img=p.transform.scale(p.image.load('img/Enemy_Rocket.png'),(4,20))
explosion_anim=[]
for i in range(8):
    explosion_anim.append(p.transform.scale(p.image.load(f'img/Explosion{i}.png'),(56,56)))
class Player(p.sprite.Sprite):
    def __init__(self):
        p.sprite.Sprite.__init__(self)
        self.image = player_img
        self.rect = self.image.get_rect()
        self.radius = 37
        self.rect.center = (WIDTH/2, HEIGHT-60)
        self.speedx=0
        self.speedy=0
        self.health=3
        self.maxhealth=3
    def update(self):
        self.speedx=0
        self.speedy=0
        keystate = p.key.get_pressed()
        if keystate[p.K_LEFT] and self.rect.left>0:
            self.speedx = -8
        if keystate[p.K_RIGHT] and self.rect.right<WIDTH:
            self.speedx = 8
        if keystate[p.K_UP] and self.rect.top>0:
            self.speedy = -8
        if keystate[p.K_DOWN] and self.rect.bottom<HEIGHT:
            self.speedy = 8
        self.rect.x += self.speedx
        self.rect.y += self.speedy
    def shoot(self):
        rocket = Rocket(rocket_img,self.rect.centerx+15, self.rect.top)
        all_sprites.add(rocket)
        rockets.add(rocket)
        rocket = Rocket(rocket_img,self.rect.centerx-15, self.rect.top)
        all_sprites.add(rocket)
        rockets.add(rocket)
class Rocket(p.sprite.Sprite):
    def __init__(self,image, x, y):
        p.sprite.Sprite.__init__(self)
        self.image=image
        self.rect = self.image.get_rect()
        self.rect.centerx=x
        if image==rocket_img:
            self.speedy = -16
            self.rect.bottom = y
        if image==enemy_rocket_img:
            self.speedy=8*speedgame
            self.rect.top=y+75
    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()
class Enemy(p.sprite.Sprite):
    def __init__(self,image,health):
        p.sprite.Sprite.__init__(self)
        self.image = image
        self.health=health
        self.rect = self.image.get_rect()
        self.rect.x = r.randrange(WIDTH - self.rect.width)
        self.rect.y = r.randrange(-100,-50)
        if self.image==enemy3_img:
            self.rect.centerx=r.randint(0,WIDTH/2-100)
            if r.randint(-1,0)<0:
                self.rect.centerx=-1*self.rect.centerx+WIDTH
            self.rect.centery=-50
            self.rad=self.rect.centerx-WIDTH/2
            self.o=0
        self.t=0
    def update(self):
        if self.image==enemy1_img:
            self.rect.y+=4*speedgame
        if self.image==enemy2_img:
            self.rect.y+=2*speedgame
            self.t+=1
            if self.t*speedgame>100:
                self.shoot()
                self.t=0
        if self.image==enemy3_img:
            x1=m.cos(self.o)
            y1=m.sin(self.o)
            self.o += m.pi*speedgame/self.rad
            self.rect.x+=(m.cos(self.o)-x1)*self.rad
            self.rect.y+=(m.sin(self.o)-y1)*self.rad+1*speedgame
            self.t+=1
            if self.t*speedgame>100:
                self.shoot()
                self.t=0
        if self.rect.y>1000 or self.health<1:
            self.kill()
    def shoot(self):
        rocket = Rocket(enemy_rocket_img,self.rect.centerx, self.rect.top)
        all_sprites.add(rocket)
        rockets.add(rocket)
class Explosion(p.sprite.Sprite):
    def __init__(self, center):
        p.sprite.Sprite.__init__(self)
        self.image = explosion_anim[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = p.time.get_ticks()
        self.frame_rate = 50
    def update(self):
        now=p.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update=now
            self.frame+=1
            if self.frame==len(explosion_anim):
                self.kill()
            else:
                center=self.rect.center
                self.image=explosion_anim[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center
font_name = p.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = p.font.Font(font_name, size)
    text_surface = font.render(text, True, (255,255,255))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)
def show_go_screen():
    screen.blit(background, background_rect)
    screen.blit(menu,(200, HEIGHT/2, 200, 200))
    draw_text(screen, "STARSHIPS", 100, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, f"Рекорд:{record}", 30,WIDTH / 2, HEIGHT / 2-100)
    draw_text(screen, "Нажмите клавишу, чтобы начать", 30, WIDTH / 2, HEIGHT * 3 / 4)
    p.display.flip()
    waiting = True
    while waiting:
        clock.tick(60)
        for event in p.event.get():
            if event.type == p.QUIT:
                waiting = False
                global but
                but = True
            if event.type == p.KEYDOWN:
                waiting = False
def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct / player.maxhealth) * BAR_LENGTH
    outline_rect = p.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = p.Rect(x, y, fill, BAR_HEIGHT)
    p.draw.rect(surf,(0,255,0), fill_rect)
    p.draw.rect(surf,(255,255,255), outline_rect, 2)
p.init()
p.mixer.init()
screen=p.display.set_mode((WIDTH,HEIGHT))
p.display.set_caption("Starships")
background=p.transform.scale(p.image.load('img/Space.png').convert(),(600,1000))
background_rect = background.get_rect()
menu=p.transform.scale(p.image.load('img/Menu.png'),(200,200))
clock=p.time.Clock()
but=False
game_over=True
running=True
record=0
score=0
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, background_rect)
    if game_over:
        record=max(score,record)
        show_go_screen()
        if but:
            running=False
        game_over=False
        score=0
        all_sprites = p.sprite.Group()
        mobs = p.sprite.Group()
        rockets = p.sprite.Group()
        player = Player()
        all_sprites.add(player)
        speedgame=1
        last1,last2,last3,reg=p.time.get_ticks(),p.time.get_ticks(),p.time.get_ticks(),p.time.get_ticks()
    clock.tick(60)
    for event in p.event.get():
        if event.type == p.QUIT:
            running = False
        elif event.type == p.KEYDOWN:
            if event.key == p.K_SPACE:
                player.shoot()
    all_sprites.update()
    if p.time.get_ticks()-last1>500/speedgame:
        last1=p.time.get_ticks()
        enemy1=Enemy(enemy1_img,1)
        all_sprites.add(enemy1)
        mobs.add(enemy1)
    if p.time.get_ticks()-last2>3000/speedgame:
        last2=p.time.get_ticks()
        enemy2=Enemy(enemy2_img,3)
        all_sprites.add(enemy2)
        mobs.add(enemy2)
    if p.time.get_ticks()-last3>10000/speedgame:
        last3=p.time.get_ticks()
        enemy3=Enemy(enemy3_img,5)
        all_sprites.add(enemy3)
        mobs.add(enemy3)
    draw_text(screen, str(score), 40, WIDTH / 2, 60)
    draw_shield_bar(screen, 250, 50, player.health)
    for i in p.sprite.spritecollide(player,mobs,True,p.sprite.collide_circle)+p.sprite.spritecollide(player,rockets,True,p.sprite.collide_circle):
        all_sprites.add(Explosion(i.rect.center))
        player.health-=1
        reg = p.time.get_ticks()
        if player.health<1:
            game_over=True
    for i in p.sprite.groupcollide(mobs,rockets, False, True):
        all_sprites.add(Explosion(i.rect.center))
        i.health-=1
        if i.image==enemy1_img:
            score+=100
        if i.image==enemy2_img:
            score+=500
        if i.image==enemy3_img:
            score+=2000
    if p.time.get_ticks()-reg>10000 and player.health<player.maxhealth:
        reg=p.time.get_ticks()
        player.health+=1
    speedgame+=0.0001
    all_sprites.draw(screen)
    p.display.flip()
p.quit()