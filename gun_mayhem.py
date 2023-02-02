import pygame

#Color Palette
color_dict = {"white":(255, 255, 255),"red":(255, 0, 0), "green":(0, 255, 0), "blue":(0, 0, 255), "black":(0, 0, 0)}
#Bullet Class
class Bullet(object):
    #Constructor
    def __init__(self,owner,x,y,velocity,direction):
        self.owner = owner
        self.x = x
        self.y = y
        self.velocity = velocity
        self.direction = direction
        self.width = 10
        self.height = 5
        self.bullet = pygame.Rect(self.x,self.y,self.width,self.height)
        self.move()
    def move(self):
        if self.owner.lastrecorded == 'LEFT':
            self.velocity *= -1
        self.x += self.velocity
    def check_collision(self):
        pass
#Our player class
class Player(object):
    #Constructor
    def __init__(self,x,y,width,height,yvel,xvel, m, jvel):
        self.lastrecorded = None
        self.yvel = yvel
        self.xvel = xvel
        self.m = m
        self.y = y
        self.square = pygame.Rect(x,y,width,height)
        self.bulletwidth = 10
        self.bulletheight = 5
        self.bulletvel = 100
        self.bulletx = self.square.x + 20
        self.bullety = self.square.y
        self.ammo = 100
        #Jump velocity
        self.jvel = jvel
        self.jumpcount = 0
    #Moving the character
        
    def move(self):
        self.square.y += self.yvel
        self.square.x += self.xvel
        move_keys = pygame.key.get_pressed()
        if move_keys[pygame.K_LEFT]:
            player1.square.x-= 5
            self.lastrecorded = 'LEFT'
        if move_keys[pygame.K_RIGHT]:
            player1.square.x += 5
            self.lastrecorded = 'RIGHT'
        if move_keys[pygame.K_DOWN]:
            if (player1.square.x >= platform1.rect.x and player1.square.x <= platform1.rect.x + 70 and player1.square.y <= platform1.rect.y - 15 and player1.square.y >= platform1.rect.y - 18) or (player1.square.x >= platform2.rect.x and player1.square.x <= platform2.rect.x + 70 and player1.square.y <= platform2.rect.y - 15 and player1.square.y >= platform2.rect.y - 18) or (player1.square.x >= platform3.rect.x and player1.square.x <= platform3.rect.x + 300 and player1.square.y <= platform3.rect.y - 15 and player1.square.y >= platform3.rect.y - 18):
                player1.square.y += 5
        if move_keys[pygame.K_a]:
            player2.square.x-= 5
        if move_keys[pygame.K_d]:
            player2.square.x += 5
        if move_keys[pygame.K_s]:
            if (player2.square.x >= platform1.rect.x and player2.square.x <= platform1.rect.x + 70 and player2.square.y <= platform1.rect.y - 15 and player2.square.y >= platform1.rect.y - 18) or (player2.square.x >= platform2.rect.x and player2.square.x <= platform2.rect.x + 70 and player2.square.y <= platform2.rect.y - 15 and player2.square.y >= platform2.rect.y - 18) or (player2.square.x >= platform3.rect.x and player2.square.x <= platform3.rect.x + 300 and player2.square.y <= platform3.rect.y - 15 and player2.square.y >= platform3.rect.y - 18):
                player2.square.y += 5
            pygame.display.update()
    #Shoot method(Outputs a bullet)
    def shoot(self):
        if self.lastrecorded == 'RIGHT' and self.ammo > 0:
            self.ammo -= 1
            self.bulletx = self.square.x + 20
            self.bullet = Bullet(self, self.bulletx, self.square.y, self.bulletvel, self.lastrecorded)
            self.bulletvel = 50
            while self.bulletx < 600:
                pygame.draw.rect(win,(color_dict['white']),(self.bulletx,player1.square.y,self.bulletwidth,self.bulletheight))
                self.bulletx += self.bulletvel
                pygame.display.update()
        if self.lastrecorded == 'LEFT' and self.ammo > 0:
            self.ammo -= 1
            self.bulletx = self.square.x - 20
            self.bulletvel = -50
            while self.bulletx > 0:
                pygame.draw.rect(win,(color_dict['white']),(self.bulletx,player1.square.y,self.bulletwidth,self.bulletheight))
                self.bulletx += self.bulletvel
                pygame.display.update()
    # def jumpy(self):
    #     #This still doesn't work but it is a start
    #     keys = pygame.key.get_pressed()
    #     #Jumping Condition
    #     for x in range(self.jvel, -1 * (self.jvel+1), -1):
    #         F =(1 / 2)*self.m*(x**2)
    #         self.y-= 2*F
    #         pygame.draw.rect(win,color_dict["green"],(self.square))
    #         pygame.display.update()
    #         if x < 0:
    #             self.m *= - 1
    #         if x == self.jvel*-1:
    #             self.m *= -1
                    
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
player1 = Player(300,300,15,15,5,0,1,5)
player2 = Player(300,300,15,15,5,0,1,5)
# bullet = Bullet(player1.x + 20, player1.y,10,5,50,player1.lastrecorded)
win = pygame.display.set_mode((600, 600))
pygame.display.set_caption("This is pygame")
run=True
while run:
    pygame.time.delay(100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run=False
    win.fill((0,0,0))
    pygame.draw.rect(win,color_dict["red"],platform1.rect)
    pygame.draw.rect(win,color_dict["red"],platform2.rect)
    pygame.draw.rect(win,color_dict["green"],(player1.square))
    pygame.draw.rect(win,color_dict['red'],(player2.square))
    pygame.draw.rect(win,color_dict['red'],platform3.rect)
    platform1.moves()
    platform2.moves()
    platform3.moves()
    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE]:
        if player1.lastrecorded == 'RIGHT' and player1.ammo > 0:
            player1.ammo -= 1
            player1.bulletx = player1.square.x + 20
            player1.bullet = Bullet(player1, player1.bulletx, player1.square.y, player1.bulletvel, player1.lastrecorded)
            player1.bulletvel = 50
            while player1.bulletx < 600:
                pygame.draw.rect(win,(color_dict['white']),(player1.bulletx,player1.square.y,player1.bulletwidth,player1.bulletheight))
                player1.bulletx += player1.bulletvel
                pygame.display.update()
        elif player1.lastrecorded == 'LEFT' and player1.ammo > 0:
            player1.ammo -= 1
            player1.bulletx = player1.square.x - 20
            player1.bulletvel = -50
            while player1.bulletx > 0:
                pygame.draw.rect(win,(color_dict['white']),(player1.bulletx,player1.square.y,player1.bulletwidth,player1.bulletheight))
                player1.bulletx += player1.bulletvel
                pygame.display.update()
    player1.move()
    player2.move()
    if keys[pygame.K_UP] and player1.jumpcount < 2:
        #This still doesn't work but it is a start
        for x in range(player1.jvel, -1 * (player1.jvel+1), -1):
            F =(1 / 2)*player1.m*(x**2)
            player1.y-= 2*F
            pygame.draw.rect(win,color_dict["green"],(player1.square))
            pygame.display.update()
            if x < 0:
                player1.m *= - 1
            if x == player1.jvel*-1:
                player1.m *= -1
        player1.jumpcount += 1
    pygame.display.update()
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
pygame.quit()