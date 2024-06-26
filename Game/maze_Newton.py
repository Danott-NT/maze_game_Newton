x = 2500
y = 200
import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)

from pygame import *
from random import randint

window_width = 700
window_height = 500
window = display.set_mode( (window_width, window_height) )
display.set_caption("Catch")

bg = transform.scale( image.load("background.jpg"), (window_width, window_height) )

class Character():
    def __init__(self, filename, size_x, size_y, pos_x, pos_y, speed):
        self.filename = filename
        self.size_x = size_x
        self.size_y = size_y
        self.image = transform.scale( image.load(filename), (size_x, size_y) )
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.speed = speed
    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Wall(Character):
    def __init__(self, size_x, size_y, pos_x, pos_y):
        self.size_x = size_x
        self.size_y = size_y
        self.image = Surface( (size_x, size_y) )
        self.image.fill( (209, 48, 88) )
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y

player1 = Character("hero.png", 50, 50, 100, 400, 8)
player2 = Character("cyborg.png", 50, 50, 100, 100, 5)
player3 = Character("treasure.png", 50, 50, 400, 400, 0)

wall_list = []
wall_list.append( Wall(30, 100, 200, 200) )

clock = time.Clock()
fps = 60
game = True
finish = False
route = 0
# route_list = [(500, 200), (500, 400), (300, 100), (200, 400), (200, 200)]
route_list = []
for i in range(10):
    x = randint(50, window_width-50)
    y = randint(50, window_height-50)
    route_list.append( (x, y) )

ok_x = False
ok_y = False

font.init()
style = font.SysFont(None, 70)
isWin = True

player1.hp = 3
while game:
    window.blit(bg, (0, 0))
    player1.draw()
    player2.draw()
    player3.draw()
    for w in wall_list:
        w.draw()

    for e in event.get():
        if e.type == QUIT:
            game = False

    if finish == False:
        safety_x = player1.rect.x
        safety_y = player1.rect.y

        keys_pressed = key.get_pressed()
        if keys_pressed[K_RIGHT] and player1.rect.x < window_width-player1.size_x:
            player1.rect.x += player1.speed
        elif keys_pressed[K_LEFT]:
            player1.rect.x -= player1.speed
        elif keys_pressed[K_UP]:
            player1.rect.y -= player1.speed
        elif keys_pressed[K_DOWN]:
            player1.rect.y += player1.speed

        for w in wall_list:
            if sprite.collide_rect(player1, w):
                player1.rect.x = safety_x
                player1.rect.y = safety_y

        goto_x, goto_y = route_list[route]
        if player2.rect.x == goto_x:
            ok_x = True
        else: #move
            dist = abs(goto_x - player2.rect.x)
            if player2.rect.x < goto_x:
                player2.rect.x += min(player2.speed, dist)
            elif player2.rect.x > goto_x:
                player2.rect.x -= min(player2.speed, dist)
        
        if player2.rect.y == goto_y:
            ok_y = True
        else: #move
            dist = abs(goto_y - player2.rect.y)
            if player2.rect.y < goto_y:
                player2.rect.y += min(player2.speed, dist)
            elif player2.rect.y > goto_y:
                player2.rect.y -= min(player2.speed, dist)
        
        if ok_x and ok_y:
            player2.speed = randint(2, 5)
            route += 1
            ok_x = False
            ok_y = False
            if route == len(route_list):
                route = 0

        # if sprite.collide_rect(player1, player2):
        #     ลด hp 1 แต้ม
        #     รีเซตตำแหน่ง
        #     if
        #         isWin = False
        #         finish = True
        if sprite.collide_rect(player1, player3):
            isWin = True
            finish = True
    else:
        if isWin == True:
            text = style.render("YOU WIN", 1, (41, 186, 70))
            window.blit(text, (200, 300))
        else:
            text = style.render("YOU LOSE", 1, (191, 44, 36))
            window.blit(text, (200, 300))

    

    display.update()
    clock.tick(fps)