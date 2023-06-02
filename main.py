'''
make this from -> https://youtu.be/Q-__8Xw9KTM
all constant variable should be in captial letters    

'''


#from venv import create
from itertools import count
from tkinter.tix import MAX
from turtle import color, title
import pygame
import os
import time
import random
pygame.font.init()

WIDTH , HEIGHT =800,800  #declare WIDTH , HEIGHT of window
WIN = pygame.display.set_mode((WIDTH, HEIGHT))# make a window name as WIN
pygame.display.set_caption("Space Shooter")

#load image's 
    #aliens SHIP'S
RED_SPACE_SHIP =pygame.image.load(os.path.join("assets", "pixel_ship_red_small.png"))
GREEN_SPACE_SHIP =pygame.image.load(os.path.join("assets", "pixel_ship_green_small.png"))
BLUE_SPACE_SHIP =pygame.image.load(os.path.join("assets", "pixel_ship_blue_small.png"))

    #PLAYER SHIP'S
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png"))

    #laser
RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
YELLOW_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))

    #background 'for backgroung to fit in as same size as screen we use pygame.transform.scale(load pic , size of pic )'
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")),(WIDTH ,HEIGHT))

class Laser:#(timestamp: 01:13:00)
    def __init__(self,x,y,img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self ,window):
        window.blit(self.img ,(self.x, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return not (self.y <= height and self.y >= 0)

    def collision(self, obj):
        return collide(self, obj )

class Ship:#create class (timestamp : 37:22)
    COOLDOWN = 30#cooldown is for shoot laser only two time per sec for increase shoot time the just drecrease COOLDOWN  

    def __init__(self,x,y,health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self , window):
        window.blit(self.ship_img, (self.x,self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self , vel , obj):#timestamp 1:25:00
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10 
                self.lasers.remove(laser)






    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1  

    def get_width(self):
        return self.ship_img.get_width()
    def get_height(self):
        return self.ship_img.get_height()



class Player(Ship):#create player class with extend ship (timestamp: 46:30)
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)  
        self.ship_img = YELLOW_SPACE_SHIP#set player's ship colour as yellow
        self.laser_img = YELLOW_LASER#set player's Laser colour as yellow
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health 

    def move_lasers(self , vel , objs):#timestamp 1:29:00
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj) 
                        if laser in self.lasers:
                            self.lasers.remove(laser)
    
    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):
        pygame.draw.rect(window, (255,0,0), (self.x, self.y + self.ship_img.get_height() + 10 , self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0,255,0), (self.x, self.y + self.ship_img.get_height() + 10 , self.ship_img.get_width() * ( self.health/self.max_health), 10))



class Enemy(Ship):#timestamp 53:10
    COLOR_MAP = {
                    "red":(RED_SPACE_SHIP,RED_LASER),
                    "green":(GREEN_SPACE_SHIP,GREEN_LASER),
                    "blue":(BLUE_SPACE_SHIP,BLUE_LASER)
                }
    
    def __init__(self, x, y, color,health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self , vel):
        self.y += vel

        def shoot(self):
            if self.cool_down_counter == 0:
                laser = Laser(self.x - 20, self.y, self.laser_img)
                self.lasers.append(laser)
                self.cool_down_counter = 1  


def collide(obj1 , obj2):
    offset_x = obj2.x - obj1.x 
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask , (offset_x, offset_y)) != None 


def main():
    run = True
    FPS = 60#set frame per second So it check every things 60 times per second
    level = 0
    lives = 5
    main_font = pygame.font.SysFont("comicsans" , 50 )#make font size 50 & font to comicsans
    lost_font = pygame.font.SysFont("comicsans" , 60 )#make font size 50 & font to comicsans


    enemies = []
    wave_length = 5#no. of enemy in gruop 
    enemy_vel = 1#enemy velocity or speed at which enemy move's 

    player_vel = 7#player velocity or speed at which players move's 
    laser_vel = 15#laser velocity or speed at which laser move's

    player = Player(300 ,630)

    clock = pygame.time.Clock()

    lost = False
    lost_count = 0

    def redraw_window():
        WIN.blit(BG,(0,0))#add background pic in window 
        #draw text
        lives_label = main_font.render(f"Lives: {lives}", 1 , (255,255,255))#create label 
        level_label = main_font.render(f"Level: {level}", 1 , (255,255,255))#create label 

        #add label to window "timestamp 32:00"
        WIN.blit(lives_label, (10,10))#syntax : name of window.blit(name of label , location)
        WIN.blit(level_label, (WIDTH - level_label.get_width()- 10,10))
        #in location we want it to be rigth side always that why  WIDTH - level_label.get_width() So take width 
        
        for enemy in enemies:
            enemy.draw(WIN)
        
        player.draw(WIN)

        if lost:
            lost_label = lost_font.render("You Lost !!!",1 , (255,255,255))#create lost label
            WIN.blit(lost_label,(WIDTH/2 - lost_label.get_width()/2, 350))#add lost label at center of window

        pygame.display.update()#refesh window 

    while run:
        #this make run all bellow code 60 times per sec (clock.tick(FPS)) 
        clock.tick(FPS)#set game fps to 60 So any devies have same speed in game
        redraw_window()

        if lives <= 0 or player.health <= 0:#cheching if lost [timestamp:1:07:00]  
            lost = True
            lost_count += 1

            if lost:
                if lost_count > FPS * 3:#reset the after 3 sec of show lost_label
                    run = False#Stop the game
                else:
                    continue

        if len(enemies)==0:
            level += 1#increase level every time player kill all enemy
            wave_length += 5 #increase no. of enemy every time player kill all enemy
            for i in range(wave_length):#timestamp 59:20
                enemy = Enemy(random.randrange(50, WIDTH -100), random.randrange(-1500,-100),random.choice(["red","blue","green"]))
                #this above line is make enemy come in random time at diff location & color
                enemies.append(enemy)

        for event in pygame.event.get():#check for any key is press and if it is then what to do 
            if event.type == pygame.QUIT:
                quit()

        keys = pygame.key.get_pressed()#timestamp 40:00
        if keys[pygame.K_a] and player.x - player_vel > 0:#left
            player.x -= player_vel
        if keys[pygame.K_LEFT] and player.x - player_vel > 0:#left
            player.x -= player_vel
        if keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH:#rigth
            player.x += player_vel
        if keys[pygame.K_RIGHT] and player.x + player_vel + player.get_width() < WIDTH:#rigth
            player.x += player_vel
        if keys[pygame.K_w] and player.y - player_vel > 0:#up
            player.y -= player_vel
        if keys[pygame.K_UP] and player.y - player_vel > 0:#up
            player.y -= player_vel
        if keys[pygame.K_s] and player.y - player_vel + player.get_height() + 25 < HEIGHT:#down
            player.y += player_vel
        if keys[pygame.K_DOWN] and player.y - player_vel + player.get_height() + 25 < HEIGHT:#down
            player.y += player_vel
        if keys[pygame.K_SPACE]:
            player.shoot()
        
        for enemy in enemies[:]:#make emeny move down [timestamp 1:01:00] 
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)

            if random.randrange(0, 2*60)== 1:#this make shoot every sec for two time's
                enemy.shoot()

            if collide(enemy, player):
                player.health -= 10 #if player touch enemy then drecuase health by 10
                enemies.remove(enemy)
            elif enemy.y + enemy.get_height() > HEIGHT:#chech for enemy is below window
                lives -= 1# if enemy is gone below window then drecease live of player
                enemies.remove(enemy)# romove the enemy from list 

            
        
        player.move_lasers(-laser_vel, enemies)


def main_menu():
    title_front = pygame.font.SysFont("comicsans",40)
    run = True
    while run:
        WIN.blit(BG, (0,0))
        title_label = title_front.render("Press the mouse the mouse to begin.!!", 1,(255,255,255))
        WIN.blit(title_label, (WIDTH/2 - title_label.get_width()/2,350))
        pygame.display.update()
        for event in pygame.event.get():
            if  event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
            
    pygame.quit()




main_menu()
