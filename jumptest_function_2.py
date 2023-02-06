import pygame, math
color_dict = {"white":(255, 255, 255),"red":(255, 0, 0), "green":(0, 255, 0), "blue":(0, 0, 255), "black":(0, 0, 0)}
# Class Bullet(object):
#     def __init__(self,x,y,velocity,direction):
#         self.width = 10   
#         self.height = 5
#         self.bullet = pygame.Rect(x,y,self.width,self.height)
#     def move(self):
#         self.x += self.velocity
class Player(object):
    def __init__(self,x,y,width,height,yvel,xvel, mass, Force, jvel, player_num):
        self.lastrecorded = None
        self.yvel = yvel
        self.xvel = xvel
        self.mass = mass
        self.y = y
        self.square = pygame.Rect(x,y,width,height)
        self.bulletwidth = 10
        self.bulletheight = 5
        self.bulletvel = 100
        self.bulletx = self.square.x + 20
        self.bullety = self.square.y
        self.ammo = 100
        self.isJump = False
        self.Force = Force
        self.jvel = jvel
        self.player_num = player_num
        self.jumpcount = 0
    def move(self):
        if self.isJump == False:
            self.square.y += self.yvel
        self.square.x += self.xvel
        if self.player_num == 1:
            if keys[pygame.K_LEFT]:
                self.square.x-= 10
                self.lastrecorded = 'LEFT'
            if keys[pygame.K_RIGHT]:
                self.square.x += 10
                self.lastrecorded = 'RIGHT'
            if keys[pygame.K_DOWN]:
                if (self.square.x >= platform1.rect.x and self.square.x <= platform1.rect.x + platform1.rect.width and self.square.y <= platform1.rect.y and self.square.y >= platform1.rect.y - 20) or (self.square.x >= platform2.rect.x and self.square.x <= platform2.rect.x + platform2.rect.width and self.square.y <= platform2.rect.y and self.square.y >= platform2.rect.y - 20) or (self.square.x >= platform3.rect.x and self.square.x <= platform3.rect.x + platform3.rect.width and self.square.y <= platform3.rect.y and self.square.y >= platform3.rect.y - 20):
                    self.square.y += 5
        if self.player_num == 2:
            if keys[pygame.K_a]:
                self.square.x-= 10
                self.lastrecorded = 'LEFT'
            if keys[pygame.K_d]:
                self.square.x += 10
                self.lastrecorded = 'RIGHT'
            if keys[pygame.K_s]:
                if (self.square.x >= platform1.rect.x and self.square.x <= platform1.rect.x + platform1.rect.width and self.square.y <= platform1.rect.y and self.square.y >= platform1.rect.y - 20) or (self.square.x >= platform2.rect.x and self.square.x <= platform2.rect.x + platform2.rect.width and self.square.y <= platform2.rect.y and self.square.y >= platform2.rect.y - 20) or (self.square.x >= platform3.rect.x and self.square.x <= platform3.rect.x + platform3.rect.width and self.square.y <= platform3.rect.y and self.square.y >= platform3.rect.y - 20):
                    self.square.y += 5
        pygame.display.update()
    def shoot(self):
        pass
    def jumpy(self):
        #This kind of works
        if self.isJump == True:
            self.yvel = 5
            if self.jvel>= 0:
                F =(1 / 2)* self.mass *(self.jvel**2)
                self.square.y-= F
                self.jvel-=1
            else:
                self.isJump = False
                self.jvel = 8
    def shot(self):
        if player1.bulletvel < 0:
            if player1.bulletx > player1.square.x and player1.bulletx <= player1.square.x + player1.square.width and player1.bullety >= player1.square.y and player1.bullety <= player1.square.y + player1.square.height:
                self.square.x += 50
        if player1.bulletvel > 0:
            if player1.bulletx > player1.square.x and player1.bulletx <= player1.square.x + player1.square.width and player1.bullety >= player1.square.y and player1.bullety <= player1.square.y + player1.square.height:
                player2.square.x -= 50
        if player2.bulletvel < 0:
            if player2.bulletx > player2.square.x and player2.bulletx <= player2.square.x + player2.square.width and player2.bullety >= player2.square.y and player2.bullety <= player2.square.y + player2.square.height:
                player1.square.x += 50
        if player2.bulletvel > 0:
            if player2.bulletx > player2.square.x and player2.bulletx <= player2.square.x + player2.square.width and player2.bullety >= player2.square.y and player2.bullety <= player2.square.y + player2.square.height:
                player1.square.x -= 50
    def check_for_platform(self,platform1,platform2,platform3):
        #Detecs if player is on platform or not(Platform Collision)
        if self.square.x >= platform1.rect.x and self.square.x <= platform1.rect.x + platform1.rect.width and self.square.y <= platform1.rect.y and self.square.y >= platform1.rect.y - 20:
            self.xvel = platform1.vel
            self.jumpcount = 0
            self.yvel = 0
            self.square.y = (platform1.rect.y - self.square.height)
        elif self.square.x >= platform2.rect.x and self.square.x <= platform2.rect.x + platform2.rect.width and self.square.y <= platform2.rect.y and self.square.y >= platform2.rect.y - 20:
            self.xvel = platform2.vel
            self.jumpcount = 0
            self.yvel = 0
            self.square.y = (platform2.rect.y - self.square.height)
        elif self.square.x >= platform3.rect.x and self.square.x <= platform3.rect.x + platform3.rect.width and self.square.y <= platform3.rect.y and self.square.y >= platform3.rect.y - 20:
            self.xvel = platform3.vel
            self.jumpcount = 0
            self.yvel = 0
            self.square.y = (platform3.rect.y - self.square.height)
        else:
            self.xvel = 0
            self.yvel = 5           
                    
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
        
platform1 = Platform(0,550,70,10, 5)
platform2 = Platform(530,550,70,10, -5)
platform3 = Platform(150,400,300,10,0)
#Order goes as follows: x,y,width,height,yvel,xvel, mass, Force, jvel, player_num
player1 = Player(300,300,15,15,30,0,1,5, 8, 1)
player2 = Player(300,300,15,15,5,0,1, 5, 8, 2)
# bullet = Bullet(player1.x + 20, player1.y,10,5,50,player1.lastrecorded)
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
    #Makes the background and all of the objects
    win.fill((0,0,0))
    pygame.draw.rect(win,color_dict["red"],platform1.rect)
    pygame.draw.rect(win,color_dict["red"],platform2.rect)
    pygame.draw.rect(win,color_dict['red'],platform3.rect)
    if player1.isJump == False:
        if keys[pygame.K_UP]:
            if player1.jumpcount == 0:
                player1.jvel = 8
                player1.jumpcount += 1
                player1.isJump = True
            elif player1.jumpcount == 1:
                player1.jvel = 8
                player1.jumpcount += 1
                player1.isJump = True
        else:
            player1.isJump = False
    if player2.isJump == False:
        if keys[pygame.K_w] and player2.jumpcount < 2:
            player2.jumpcount += 1
            player2.isJump = True
        else:
            player2.isJump = False 
    player1.jumpy()
    player2.jumpy()
    pygame.draw.rect(win,color_dict["green"],(player1.square))
    pygame.draw.rect(win,color_dict["red"],(player2.square))
    #Makes the platforms move
    platform1.moves()
    platform2.moves()
    platform3.moves()
    if keys[pygame.K_SPACE]:
        player1.shoot()
    if keys[pygame.K_x]:
        player2.shoot()
    player1.move()
    player2.move()
    player1.shot()
    player2.shot()
    pygame.display.update()
    player1.check_for_platform(platform1,platform2,platform3)
    player2.check_for_platform(platform1,platform2,platform3)
    # if player1.square.x >= platform1.rect.x and player1.square.x <= platform1.rect.x + platform1.width and player1.square.y <= platform1.rect.y - 15 and player1.square.y >= platform1.rect.y - 18:
    #     player1.yvel = 0
    #     player1.xvel = platform1.vel
    #     player1.jumpcount = 0
    # elif player1.square.x >= platform2.rect.x and player1.square.x <= platform2.rect.x + platform2.width and player1.square.y <= platform2.rect.y - 15 and player1.square.y >= platform2.rect.y - 18:
    #     player1.yvel = 0
    #     player1.xvel = platform2.vel
    #     player1.jumpcount = 0
    # elif player1.square.x >= platform3.rect.x and player1.square.x <= platform3.rect.x + platform3.width and player1.square.y <= platform3.rect.y - 15 and player1.square.y >= platform3.rect.y - 18:
    #     player1.yvel = 0
    #     player1.xvel = platform3.vel
    #     player1.jumpcount = 0
    # else:
    #     player1.yvel = 5
    #     player1.xvel = 0
    # if player2.square.x >= platform1.rect.x and player2.square.x <= platform1.rect.x + platform1.width and player2.square.y <= platform1.rect.y - 15 and player2.square.y >= platform1.rect.y - 18:
    #     player2.yvel = 0
    #     player2.xvel = platform1.vel
    #     player2.jumpcount = 0
    # elif player2.square.x >= platform2.rect.x and player2.square.x <= platform2.rect.x + platform2.width and player2.square.y <= platform2.rect.y - 15 and player2.square.y >= platform2.rect.y - 18:
    #     player2.yvel = 0
    #     player2.xvel = platform2.vel
    #     player2.jumpcount = 0
    # elif player2.square.x >= platform3.rect.x and player2.square.x <= platform3.rect.x + platform3.width and player2.square.y <= platform3.rect.y - 15 and player2.square.y >= platform3.rect.y - 18:
    #     player2.yvel = 0
    #     player2.xvel = platform3.vel
    #     player2.jumpcount = 0
    # else:
    #     player2.yvel = 5
    #     player2.xvel = 0
pygame.quit()
