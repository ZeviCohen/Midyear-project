import pygame
pygame.init()

win = pygame.display.set_mode((600, 600))
pygame.display.set_caption("This is pygame")

x=50
y=50
width=40
height=60
vel=20

run=True
while run:
    pygame.time.delay(100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run=False
    keys= pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and x>=0:
        x-=vel
    if keys[pygame.K_RIGHT] and x<=500:
        x+= vel
    if keys[pygame.K_UP]and y>=0:
        y-= vel
    if keys[pygame.K_DOWN]and y<=500:
        y+= vel
    win.fill((0,0,0))
    pygame.draw.rect(win, (255, 0 , 0), (x, y, width, height))
    pygame.display.update()

pygame.quit()