#Создай собственный Шутер!

from pygame import *
from random import randint

COLOR_WHITLER = (255,255,255)
COLOR_WIN = (0, 255, 255)
COLOR_LOSE = (255, 5, 5)

class GameSprite(sprite.Sprite):
    def __init__(self, imagePath, corX, corY, width, height, speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(imagePath), (width, height))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = corX
        self.rect.y = corY
    
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x < 900:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx - 7, self.rect.top - 7, 15, 25, -5)
        bullets.add(bullet)
        
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 700:
            self.rect.x = randint(10, 1000-70)
            self.rect.y = 0
            global lost
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

window = display.set_mode((1000, 700))
display.set_caption('Шутер')
clock = time.Clock()

mixer.init()
font.init()

mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

lost = 0
point = 0

background = transform.scale(image.load('galaxy.jpg'), (1000, 700))
rocket = Player('rocket.png', 500, 600, 80, 100, 3)
aliens = sprite.Group()

for i in range(1, 6):
    alien = Enemy('ufo.png', randint(10, 1000-120), 50, 120, 72, randint(1, 3))
    aliens.add(alien)
    
bullets = sprite.Group()

text_lose = font.SysFont('Segoe Script', 110).render('ТЫ ПРОИГРАЛ!', 1, COLOR_LOSE)
text_win = font.SysFont('Segoe Script', 110).render('ТЫ ВЫИГРАЛ!', 1, COLOR_WIN)

FPS = 60
run = True
finish = False
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                rocket.fire()
                fire_sound.play()

    if not finish:
        window.blit(background, (0, 0))
        rocket.reset()
        rocket.update()
        aliens.draw(window)
        aliens.update()
        bullets.draw(window)
        bullets.update()
        collides = sprite.groupcollide(aliens, bullets, True, True)
        for c in collides:
            point += 1
            alien = Enemy('ufo.png', randint(10, 1000-100), 20, 120, 72, randint(1, 3))
            aliens.add(alien)

        text_lost = font.SysFont('Segoe Print', 31).render('Пропущено: ' + str(lost), 1, COLOR_WHITLER)
        window.blit(text_lost, (10, 70))

        text_point = font.SysFont('Segoe Print', 25).render('Счёт: ' + str(point), 1, COLOR_WHITLER)
        window.blit(text_point, (10, 30))

        if point >= 10:
            finish = True
            window.blit(text_win, (40,300))
            mixer.music.stop()
        if lost >= 3 or sprite.spritecollide(rocket, aliens, False):
            finish = True
            window.blit(text_lose, (10,300))
            mixer.music.stop()

    display.update()
    clock.tick(FPS)