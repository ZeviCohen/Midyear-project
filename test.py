import pygame

win = pygame.display.set_mode((600, 600))
pygame.display.set_caption("This is pygame")

# <<<<<<< HEAD
x=0
y=550
width=70
height=20
vel=5
x2 = 530
y2 = 550
cx = 300
cy = 300
# =======
# x=41
# y=41
# width=40
# height=60
# vel=20
# >>>>>>> 7252062a6370f7eca53081d683fa56010466519d

run=True
while run:
    pygame.time.delay(100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run=False
    # keys= pygame.key.get_pressed()
    # if keys[pygame.K_LEFT] and x>vel:
    #     x-=vel
    # if keys[pygame.K_RIGHT] and x < 600 - width:
    #     x+= vel
    # if keys[pygame.K_UP]and y>=0:
    #     y-= vel
    # if keys[pygame.K_DOWN]and y < 600 - height:
    #     y+= vel
    # win.fill((0,0,0))
    # pygame.draw.rect(win, (255, 0 , 0), (x, y, width, height))
    # pygame.display.update()
    win.fill((0,0,0))
    pygame.draw.rect(win,(255,0,0), (x,y,width,height))
    pygame.draw.rect(win,(255,0,0),(x2,y2,width,height))
    pygame.draw.circle(win,(255,156,32),(cx,cy), (10))
    pygame.display.update()
    x += vel
    x2 -= vel
    if x > 530:
        vel *= -1
    if x < 0:
        vel *= -1
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        cx-=vel
    if keys[pygame.K_RIGHT]:
        cx += vel
    if keys[pygame.K_UP]:
        cy-= vel
    if keys[pygame.K_DOWN]:
        cy += vel

pygame.quit()