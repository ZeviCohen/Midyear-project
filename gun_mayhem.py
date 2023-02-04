import pygame, math

#Color Palette
color_dict = {"white":(255, 255, 255),"red":(255, 0, 0), "green":(0, 255, 0), "blue":(0, 0, 255), "black":(0, 0, 0)}

bullet_list = []

def update_window():
    #Makes the background and all of the objects
    win.fill((0,0,0))
    pygame.draw.rect(win,color_dict["red"],platform1.rect)
    pygame.draw.rect(win,color_dict["red"],platform2.rect)
    pygame.draw.rect(win,color_dict['red'],platform3.rect)

class Gun ():
    def __init__(self, owner, ammo, bulletvel, cooldown):
        self.bulletvel = bulletvel
        self.cooldown = cooldown
        self.ammo = ammo
        self.last = pygame.time.get_ticks()
        self.owner = owner
    #Shoot method(Outputs a bullet)
    def shoot(self):
        now = pygame.time.get_ticks()
        #Checks for cooldown
        if now - self.last >= self.cooldown and self.ammo > 0:
            self.last = now
            self.ammo -= 1
            bullet_list.append(Bullet(self.owner, self.bulletvel))
        #Delays and then reloads the gun
        elif self.ammo <= 0:
            if now - self.last >= 3000:
                self.last = now
                self.ammo = 10
                bullet_list.append(Bullet(self.owner, self.bulletvel))

# Bullet Class
class Bullet(object):
    #Constructor
    def __init__(self, owner, velocity):
        self.owner = owner
        if self.owner.lastrecorded == 'LEFT':
            self.x = self.owner.square.x - 20
            self.direction = -1
        if self.owner.lastrecorded == 'RIGHT' or self.owner.lastrecorded == None:
            self.x = self.owner.square.x + 20
            self.direction = 1
        self.y = owner.square.y
        self.velocity = velocity
        self.width = 10
        self.height = 5
        #self.bullet = pygame.Rect(self.x,self.y,10,5)
    def move(self):
        self.velocity = self.direction * abs(self.velocity)
        self.x += self.velocity
    def check_collision(self):
        pass
        #if player2.square.x == self.x + self.width:
            #player2.x += 1
#Our player class
class Player(object):
    def __init__(self,x,y,width,height,yvel,xvel, mass, jvel, player_num, lives):
        self.lastrecorded = None
        self.yvel = yvel
        self.xvel = xvel
        self.mass = mass
        self.y = y
        self.square = pygame.Rect(x,y,width,height)
        self.ammo = 100
        self.isJump = False
        self.jvel = jvel
        self.player_num = player_num
        self.lives = lives
    def move(self):
        if self.isJump == False:
            self.square.y += self.yvel
        self.square.x += self.xvel
        #Checks for key presses(Player 1)
        if self.player_num == 1:
            if keys[pygame.K_LEFT]:
                self.square.x-= 10
                self.lastrecorded = 'LEFT'
            if keys[pygame.K_RIGHT]:
                self.square.x += 10
                self.lastrecorded = 'RIGHT'
            if keys[pygame.K_DOWN]:
                if (self.square.x >= platform1.rect.x and self.square.x <= platform1.rect.x + 70 and self.square.y <= platform1.rect.y - 15 and self.square.y >= platform1.rect.y - 18) or (self.square.x >= platform2.rect.x and self.square.x <= platform2.rect.x + 70 and self.square.y <= platform2.rect.y - 15 and self.square.y >= platform2.rect.y - 18) or (self.square.x >= platform3.rect.x and self.square.x <= platform3.rect.x + 300 and self.square.y <= platform3.rect.y - 15 and self.square.y >= platform3.rect.y - 18):
                    self.square.y += 5
                    self.yvel = 10
        #Checks for key presses(Player 2)
        elif self.player_num == 2:
            if keys[pygame.K_a]:
                self.square.x-= 10
                self.lastrecorded = 'LEFT'
            if keys[pygame.K_d]:
                self.square.x += 10
                self.lastrecorded = 'RIGHT'
            if keys[pygame.K_s]:
                if (self.square.x >= platform1.rect.x and self.square.x <= platform1.rect.x + 70 and self.square.y <= platform1.rect.y - 15 and self.square.y >= platform1.rect.y - 18) or (self.square.x >= platform2.rect.x and self.square.x <= platform2.rect.x + 70 and self.square.y <= platform2.rect.y - 15 and self.square.y >= platform2.rect.y - 18) or (self.square.x >= platform3.rect.x and self.square.x <= platform3.rect.x + 300 and self.square.y <= platform3.rect.y - 15 and self.square.y >= platform3.rect.y - 18):
                    self.square.y += 5
                    self.yvel = 10
    def jumpy(self):
        #This kind of works
        if self.isJump == True:
            self.yvel = 10
            if self.jvel>= 0:
                F =(1 / 2)* self.mass *(self.jvel**2)
                self.square.y-= F
                self.jvel-=1
            else:
                self.isJump = False
                self.jvel = 10
    def respawn(self):
        pygame.time.delay(100)
        self.square.y = 50
        self.square.x = 300 - (self.square.width/2)
        self.lives -= 1
        #End of game
        if self.lives == 0:
            pygame.QUIT()
class Platform(object):
    def __init__(self,x,y,width,height,vel):
        self.rect = pygame.Rect(x,y,width,height)
        self.vel = vel
    def moves(self):
        self.rect.x += self.vel
        if self.rect.x > 530:
            self.vel *= -1
        if self.rect.x < 0:
            self.vel *= -1
        pygame.display.update()
#Order goes as follows: x, y, width, height, vel
platform1 = Platform(0,550,70,10, 5)
platform2 = Platform(530,550,70,10, -5)
platform3 = Platform(150,400,300,10,0)
#Order goes as follows: x,y,width,height,yvel,xvel, mass, jvel, player_num, lives
player1 = Player(300,300,15,15,10,0,1,10, 1, 1)
player2 = Player(300,300,15,15,10,0,1,10, 2, 10)
#Order goes as follows: owner, ammo, bulletvel, cooldown
gun1 = Gun(player1, 10, 50, 400)
gun2 = Gun(player2, 10, 50, 400)
win = pygame.display.set_mode((600, 600))
pygame.display.set_caption("This is pygame")
run = True
while run:
    pygame.time.delay(100)
    #To let the user quit the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run=False
    keys = pygame.key.get_pressed()
    update_window()
    #Code for player 1
    if player1.isJump == False:
        if keys[pygame.K_UP] and player1.yvel == 0:
            #This still doesn't work but it is a start
            player1.isJump = True
        else:
            player1.isJump = False
    #Player moves
    player1.jumpy()
    pygame.draw.rect(win,color_dict["green"],(player1.square))
    player1.move()
    if keys[pygame.K_SPACE]:
        gun1.shoot()
    if keys[pygame.K_z]:
        gun2.shoot()
    for bullet in bullet_list:
        if bullet.x > 600 or bullet.x < 0:
            bullet_list.remove(bullet)
        else:
            if bullet.owner == player1:
                color = color_dict['white']
                pygame.draw.rect(win,color,(bullet.x, player1.square.y,bullet.width,bullet.height))
            else:
                color = color_dict['red']
                pygame.draw.rect(win,color,(bullet.x, player2.square.y,bullet.width,bullet.height))
            bullet.move()
    if player2.isJump == False:
        if keys[pygame.K_w] and player2.yvel == 0:
            #This still doesn't work but it is a start
            player2.isJump = True
        else:
            player2.isJump = False
    player2.jumpy()
    pygame.draw.rect(win,color_dict['red'],(player2.square))
    player2.move()
    #Makes the platforms move
    platform1.moves()
    platform2.moves()
    platform3.moves()
    if player1.square.y > 600:
        player1.respawn()
    if player2.square.y > 600:
        player2.respawn()
    #Detecs if player is on platform or not(Platform Collision)
    if player1.square.x >= platform1.rect.x and player1.square.x <= platform1.rect.x + 70 and player1.square.y <= platform1.rect.y - 15 and player1.square.y >= platform1.rect.y - 18:
        player1.yvel = 0
        player1.xvel = platform1.vel
        player1.jumpcount = 0
    elif player1.square.x >= platform2.rect.x and player1.square.x <= platform2.rect.x + 70 and player1.square.y <= platform2.rect.y - 15 and player1.square.y >= platform2.rect.y - 18:
        player1.yvel = 0
        player1.xvel = platform2.vel
        player1.jumpcount = 0
    elif player1.square.x >= platform3.rect.x and player1.square.x <= platform3.rect.x + 300 and player1.square.y <= platform3.rect.y - 15 and player1.square.y >= platform3.rect.y - 18:
        player1.yvel = 0
        player1.xvel = platform3.vel
        player1.jumpcount = 0
    else:
        player1.yvel = 5
        player1.xvel = 0
        player1.jumpcount = 0
    if player2.square.x >= platform1.rect.x and player2.square.x <= platform1.rect.x + 70 and player2.square.y <= platform1.rect.y - 15 and player2.square.y >= platform1.rect.y - 18:
        player2.yvel = 0
        player2.xvel = platform1.vel
    elif player2.square.x >= platform2.rect.x and player2.square.x <= platform2.rect.x + 70 and player2.square.y <= platform2.rect.y - 15 and player2.square.y >= platform2.rect.y - 18:
        player2.yvel = 0
        player2.xvel = platform2.vel
    elif player2.square.x >= platform3.rect.x and player2.square.x <= platform3.rect.x + 300 and player2.square.y <= platform3.rect.y - 15 and player2.square.y >= platform3.rect.y - 18:
        player2.yvel = 0
        player2.xvel = platform3.vel
    else:
        player2.yvel = 5
        player2.xvel = 0
    pygame.display.update()
pygame.quit()