import pygame

# win = pygame.display.set_mode((600, 600))
# pygame.display.set_caption("This is pygame")

# # <<<<<<< HEAD
# x=0
# y=550
# width=70
# height=20
# vel=5
# x2 = 530
# y2 = 550
# cx = 300
# cy = 300
# cyvel = 5
# # =======
# # x=41
# # y=41
# # width=40
# # height=60
# # vel=20
# # >>>>>>> 7252062a6370f7eca53081d683fa56010466519d

# run=True
# while run:
#     pygame.time.delay(100)
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             run=False
#     # keys= pygame.key.get_pressed()
#     # if keys[pygame.K_LEFT] and x>vel:
#     #     x-=vel
#     # if keys[pygame.K_RIGHT] and x < 600 - width:
#     #     x+= vel
#     # if keys[pygame.K_UP]and y>=0:
#     #     y-= vel
#     # if keys[pygame.K_DOWN]and y < 600 - height:
#     #     y+= vel
#     # win.fill((0,0,0))
#     # pygame.draw.rect(win, (255, 0 , 0), (x, y, width, height))
#     # pygame.display.update()
#     win.fill((0,0,0))
#     pygame.draw.rect(win,(255,0,0), (x,y,width,height))
#     pygame.draw.rect(win,(255,0,0),(x2,y2,width,height))
#     pygame.draw.circle(win,(255,156,32),(cx,cy), (10))
#     pygame.display.update()
#     x += vel
#     x2 -= vel
#     cy += cyvel
    
#     if x > 530:
#         vel *= -1
#     if x < 0:
#         vel *= -1
#     keys = pygame.key.get_pressed()
#     if keys[pygame.K_LEFT]:
#         cx-=5
#     if keys[pygame.K_RIGHT]:
#         cx += 5
#     if keys[pygame.K_UP]:
#         cy-= 5
#         cy-=5
#         cy-=5
#     if keys[pygame.K_DOWN]:
#         cy += 5

# pygame.quit()
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
black = (0, 0, 0)
class Player(object):
    def __init__(self,x,y,radius,yvel,xvel):
        self.x = x
        self.y = y
        self.radius = radius
        self.yvel = yvel
        self.xvel = xvel
    def move(self):
        self.y += self.yvel
        self.x += self.xvel
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x-= 5
        if keys[pygame.K_RIGHT]:
            self.x += 5
        if keys[pygame.K_UP]:
            if player1.x >= platform1.rect.x and player1.x <= platform1.rect.x + 70 and player1.y <= platform1.rect.y - 10 and player1.y >= platform1.rect.y - 12:
                self.y -= 15
        if keys[pygame.K_DOWN]:
            self.y += 5
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
player1 = Player(200,200,10,5,0)
win = pygame.display.set_mode((600, 600))
pygame.display.set_caption("This is pygame")
run=True
while run:
    pygame.time.delay(100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run=False
    win.fill((0,0,0))
    pygame.draw.rect(win,red,platform1.rect)
    pygame.draw.rect(win,red,platform2.rect)
    pygame.draw.circle(win,green,(player1.x,player1.y),player1.radius)
    platform1.moves()
    platform2.moves()
    player1.move()
    pygame.display.update()
    if player1.x >= platform1.rect.x and player1.x <= platform1.rect.x + 70 and player1.y <= platform1.rect.y - 10 and player1.y >= platform1.rect.y - 12:
        player1.yvel = 0
        player1.xvel = platform1.vel
    elif player1.x >= platform2.rect.x and player1.x <= platform2.rect.x + 70 and player1.y <= platform2.rect.y - 10 and player1.y >= platform1.rect.y - 12:
    else:
        player1.yvel = 5
        player1.xvel = 0

pygame.quit()