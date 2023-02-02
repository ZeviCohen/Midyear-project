import pygame
gained = 0
color_dict = {"white":(255, 255, 255),"red":(255, 0, 0), "green":(0, 255, 0), "blue":(0, 0, 255), "black":(0, 0, 0)}
class Player(object):
    def __init__(self,x,y,width,height,yvel,xvel, mass):
        self.lastrecorded = None
        self.yvel = yvel
        self.xvel = xvel
        self.m = mass
        self.y = y
        self.square = pygame.Rect(x,y,width,height)
        self.bulletwidth = 10
        self.bulletheight = 5
        self.bulletvel = 100
        self.bulletx = self.square.x + 20
        self.bullety = self.square.y
    def move(self):
        self.square.y += self.yvel
        self.square.x += self.xvel
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player1.square.x-= 5
            self.lastrecorded = 'LEFT'
        if keys[pygame.K_RIGHT]:
            player1.square.x += 5
            self.lastrecorded = 'RIGHT'
        if keys[pygame.K_DOWN]:
            if (player1.square.x >= platform1.rect.x and player1.square.x <= platform1.rect.x + 70 and player1.square.y <= platform1.rect.y - 15 and player1.square.y >= platform1.rect.y - 18) or (player1.square.x >= platform2.rect.x and player1.square.x <= platform2.rect.x + 70 and player1.square.y <= platform2.rect.y - 15 and player1.square.y >= platform2.rect.y - 18) :
                player1.square.y += 5
        if keys[pygame.K_a]:
            player2.square.x-= 5
        if keys[pygame.K_d]:
            player2.square.x += 5
        if keys[pygame.K_s]:
            if (player2.square.x >= platform1.rect.x and player2.square.x <= platform1.rect.x + 70 and player2.square.y <= platform1.rect.y - 15 and player2.square.y >= platform1.rect.y - 18) or (player2.square.x >= platform2.rect.x and player2.square.x <= platform2.rect.x + 70 and player2.square.y <= platform2.rect.y - 15 and player2.square.y >= platform2.rect.y - 18) :
                player2.square.y += 5
    def shoot(self):
        if self.lastrecorded == 'RIGHT':
            self.bulletx = self.square.x + 20
            self.bulletvel = 100
            pygame.draw.rect(win,(color_dict['white']),(player1.square.x+20,player1.square.y,self.bulletwidth,self.bulletheight))
            while self.bulletx < 600:
                pygame.draw.rect(win,(color_dict['white']),(self.bulletx,player1.square.y,self.bulletwidth,self.bulletheight))
                self.bulletx += self.bulletvel
                pygame.display.update()
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
player1 = Player(300,300,15,15,5,0,1)
player2 = Player(300,300,15,15,5,0,1)
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
    platform1.moves()
    platform2.moves()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        player1.shoot()
    player1.move()
    player2.move()
    pygame.display.update()
    if player1.square.x >= platform1.rect.x and player1.square.x <= platform1.rect.x + 70 and player1.square.y <= platform1.rect.y - 15 and player1.square.y >= platform1.rect.y - 18:
        player1.yvel = 0
        player1.xvel = platform1.vel
    elif player1.square.x >= platform2.rect.x and player1.square.x <= platform2.rect.x + 70 and player1.square.y <= platform2.rect.y - 15 and player1.square.y >= platform2.rect.y - 18:
        player1.yvel = 0
        player1.xvel = platform2.vel
    else:
        player1.yvel = 5
        player1.xvel = 0
    if player2.square.x >= platform1.rect.x and player2.square.x <= platform1.rect.x + 70 and player2.square.y <= platform1.rect.y - 15 and player2.square.y >= platform1.rect.y - 18:
        player2.yvel = 0
        player2.xvel = platform1.vel
    elif player2.square.x >= platform2.rect.x and player2.square.x <= platform2.rect.x + 70 and player2.square.y <= platform2.rect.y - 15 and player2.square.y >= platform2.rect.y - 18:
        player2.yvel = 0
        player2.xvel = platform2.vel
    else:
        player2.yvel = 5
        player2.xvel = 0
pygame.quit()