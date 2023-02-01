import pygame
gained = 0
color_dict = {"white":(255, 255, 255),"red":(255, 0, 0), "green":(0, 255, 0), "blue":(0, 0, 255), "black":(0, 0, 0)}
class Player(object):
    def __init__(self,x,y,width,height,yvel,xvel, mass):
        self.yvel = yvel
        self.xvel = xvel
        self.jump = False
        self.m = mass
        self.y = y
        self.square = pygame.Rect(x,y,width,height)
    def move(self):
        self.square.y += self.yvel
        self.square.x += self.xvel
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x-= 5
        if keys[pygame.K_RIGHT]:
            self.x += 5
<<<<<<< HEAD
        if keys[pygame.K_UP]:
            if (player1.square.x >= platform2.rect.x and player1.square.x <= platform2.rect.x + 70 and player1.square.y <= platform2.rect.y - 10 and player1.square.y >= platform2.rect.y - 12) or (player1.square.x >= platform2.rect.x and player1.square.x <= platform2.rect.x + 70 and player1.square.y <= platform2.rect.y - 10 and player1.square.y >= platform2.rect.y - 12):
                self.square.y -= 60
=======
>>>>>>> 7f48f86dd9037cd46d33c1758cb14d9a87a6749a
        if keys[pygame.K_DOWN]:
            if (player1.square.x >= platform1.rect.x and player1.square.x <= platform1.rect.x + 70 and player1.square.y <= platform1.rect.y - 10 and player1.square.y >= platform1.rect.y - 12) or (player1.square.x >= platform2.rect.x and player1.square.x <= platform2.rect.x + 70 and player1.square.y <= platform2.rect.y - 10 and player1.square.y >= platform2.rect.y - 12) :
                self.square.y += 5
    def jumpy(self):
        #This still doesn't work but it is a start
        keys = pygame.key.get_pressed()
        v = 5
        m = self.m
        if self.jump==False:
            if keys[pygame.K_UP]:
                if (player1.square.x >= platform1.rect.x and player1.square.x <= platform1.rect.x + 70 and player1.square.y <= platform1.rect.y - 10 and player1.square.y >= platform1.rect.y - 12) or (player1.square.x >= platform2.rect.x and player1.square.x <= platform2.rect.x + 70 and player1.square.y <= platform2.rect.y - 10 and player1.square.y >= platform2.rect.y - 12):
                    self.jump= True
        if self.jump == True:
            F =(1 / 2)* m *(v**2)
            self.y-= F
            v-=1
            if v<0:
                m *= -1
            if v == -(v+1):
                self.jump = False
                m = self.m
                v = 5
        pygame.time.delay(10)
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
platform1 = Platform(0,550,70,20, 5)
platform2 = Platform(530,550,70,20, -5)
player1 = Player(200,200,10,10,5,0,1)
win = pygame.display.set_mode((600, 600))
pygame.display.set_caption("This is pygame")
run=True
while run:
    pygame.time.delay(100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run=False
    win.fill((0,0,0))
<<<<<<< HEAD
    pygame.draw.rect(win,red,platform1.rect)
    pygame.draw.rect(win,red,platform2.rect)
    pygame.draw.rect(win,green,player1.square)
=======
    pygame.draw.rect(win,color_dict["red"],platform1.rect)
    pygame.draw.rect(win,color_dict["red"],platform2.rect)
    pygame.draw.circle(win,color_dict["green"],(player1.x,player1.y),player1.radius)
>>>>>>> 7f48f86dd9037cd46d33c1758cb14d9a87a6749a
    platform1.moves()
    platform2.moves()
    player1.move()
    player1.jumpy()
    pygame.display.update()
    if player1.square.x >= platform1.rect.x and player1.square.x <= platform1.rect.x + 70 and player1.square.y <= platform1.rect.y - 10 and player1.square.y >= platform1.rect.y - 12:
        player1.yvel = 0
        player1.xvel = platform1.vel
    elif player1.square.x >= platform2.rect.x and player1.square.x <= platform2.rect.x + 70 and player1.square.y <= platform2.rect.y - 10 and player1.square.y >= platform2.rect.y - 12:
        player1.yvel = 0
        player1.xvel = platform2.vel
    else:
        player1.yvel = 5
        player1.xvel = 0
pygame.quit()