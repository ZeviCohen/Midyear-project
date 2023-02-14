import pygame, math
# copy of previous platform detection code: (self.square.x >= platform1.rect.x and self.square.x <= platform1.rect.x + 70 and self.square.y <= platform1.rect.y - 15 and self.square.y >= platform1.rect.y - 18) or (self.square.x >= platform2.rect.x and self.square.x <= platform2.rect.x + 70 and self.square.y <= platform2.rect.y - 15 and self.square.y >= platform2.rect.y - 18) or (self.square.x >= platform3.rect.x and self.square.x <= platform3.rect.x + 300 and self.square.y <= platform3.rect.y - 15 and self.square.y >= platform3.rect.y - 18)
#Color Palette
color_dict = {"white":(255, 255, 255),"red":(255, 0, 0), "green":(0, 255, 0), "blue":(0, 0, 255), "black":(0, 0, 0)}
pygame.init()
gun_list = []
bullet_list = []
upgrade_list = []
gunbox_list = []
scrn = pygame.display.set_mode((600, 600))
player1image = pygame.image.load("Images/Meowth-Pokemon-PNG-Transparent-Image.png").convert()
def update_window():
    #Makes the background and all of the objects
    win.fill((0,0,0))
    #Draws the platforms
    pygame.draw.rect(win,color_dict["red"],platform1.rect)
    pygame.draw.rect(win,color_dict["red"],platform2.rect)
    pygame.draw.rect(win,color_dict['red'],platform3.rect)
    #Draws the players
    pygame.draw.rect(win,color_dict["green"],(player1.square))
    pygame.draw.rect(win,color_dict['red'],(player2.square))
DEFAULT_IMAGE_SIZE = (15,15)
class Gun ():
    def __init__(self, owner, ammo, cooldown, bullet_kb, gunid):
        self.cooldown = cooldown
        self.ammo = ammo
        self.last = pygame.time.get_ticks()
        self.owner = owner
        self.bullet_kb = bullet_kb
        #GunID of 0 is main gun and GunID of 1 is special gun
        self.gunid = gunid
    #Shoot method(Outputs a bullet)
    def shoot(self):
        now = pygame.time.get_ticks()
        #Checks for cooldown
        if now - self.last >= self.cooldown and self.ammo > 0:
            self.last = now
            self.ammo -= 1
            bullet_list.append(Bullet(self.owner, self.bullet_kb))
        #Delays and then reloads the gun
        elif self.ammo <= 0:
            if self.gunid == 0:
                if now - self.last >= 3000:
                    self.last = now
                    self.ammo = 10
                    bullet_list.append(Bullet(self.owner, self.bullet_kb))
            else:
                self.owner.gun = self.owner.maingun

# Bullet Class
class Bullet(object):
    #Constructor
    def __init__(self, owner, bullet_xkb):
        self.owner = owner
        #Defines the direction of the bullet
        if self.owner.lastrecorded == 'LEFT':
            self.x = self.owner.square.x - 20
            self.x = self.owner.square.x - self.bullet_spawn_distance
            self.direction = -1
        if self.owner.lastrecorded == 'RIGHT' or self.owner.lastrecorded == None:
            self.x = self.owner.square.x + 20
            self.direction = 1
        self.y = owner.square.y
        self.velocity = 20
        self.width = 10
        self.height = 5
        self.xkb = bullet_xkb
        self.ykb = 4
        self.hit_once = False
    def move(self):
        self.velocity = self.direction * abs(self.velocity)
        self.x += self.velocity
    def check_collision(self, enemy):
        if (self.x + self.width >= enemy.square.x) and (self.x <= enemy.square.x + enemy.square.width) and (self.y + self.height >= enemy.square.y) and (self.y <= enemy.square.y + enemy.square.height):
            self.hit_once = True
            enemy.ishit = True
        enemy.shot(self)
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
        self.jumpcount = 0
        self.touching_platform = False
        self.ishit = False
        self.gun = None
        self.maingun = None

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
                if self.touching_platform == True:
                    self.square.y += 5
                    self.jumpcount = 2
            #Jumps
            if self.isJump == False:
                if keys[pygame.K_UP]:
                    if self.jumpcount == 0:
                        if self.touching_platform == True:
                            self.jvel = 6
                            self.isJump = True
                            self.touching_platform = False
            elif self.jumpcount == 1:
                if keys[pygame.K_UP]:
                    self.jvel = 5
                    self.jumpcount = 2
                    self.isJump = True
        #Checks for key presses(Player 2)
        elif self.player_num == 2:
            if keys[pygame.K_a]:
                self.square.x-= 10
                self.lastrecorded = 'LEFT'
            if keys[pygame.K_d]:
                self.square.x += 10
                self.lastrecorded = 'RIGHT'
            if keys[pygame.K_s]:
                if self.touching_platform==True:
                    self.square.y += 5
                    self.jumpcount = 2
            #Jumps
            if self.isJump == False:
                if keys[pygame.K_w]:
                    if self.jumpcount == 0:
                        if self.touching_platform == True:
                            self.jvel = 6
                            self.isJump = True
                            self.touching_platform = False
            elif self.jumpcount == 1:
                if keys[pygame.K_w]:
                    self.jvel = 5
                    self.jumpcount = 2
                    self.isJump = True

    def jumpy(self):
        #This kind of works
        if self.isJump:
            if self.touching_platform == False:
                if self.jvel >= 0:
                    F =(1 / 2)* self.mass *(self.jvel**2)
                    if self.jvel == 0:
                        self.jumpcount += 1
                elif self.jvel < 0:
                    F = (1/2) * self.mass * -1 * (self.jvel**2)
                self.square.y-= F
                self.jvel-=1
            else:
                self.isJump = False
                self.jvel = 6

    def respawn(self):
        pygame.time.delay(100)
        self.square.y = 50
        self.square.x = 300 - (self.square.width/2)
        self.lives -= 1
        self.isJump = False
        self.jumpcount = 2
        self.ishit = False

    def check_for_platform(self, platform1, platform2, platform3):
        #Detecs if player is on platform or not(Platform Collision)
        if self.square.x >= platform1.rect.x and self.square.x <= platform1.rect.x + platform1.rect.width and self.square.y <= platform1.rect.y and self.square.y >= platform1.rect.y - 30:
            self.xvel = platform1.vel
            self.jumpcount = 0
            self.yvel = 0
            if (self.isJump == True and self.jvel <= -6) or self.isJump == False:
                self.square.y = (platform1.rect.y - self.square.height)
                self.touching_platform = True
        elif self.square.x >= platform2.rect.x and self.square.x <= platform2.rect.x + platform2.rect.width and self.square.y <= platform2.rect.y and self.square.y >= platform2.rect.y - 30:
            self.xvel = platform2.vel
            self.jumpcount = 0
            self.yvel = 0
            if (self.isJump == True and self.jvel <= -6) or self.isJump == False:
                self.square.y = (platform2.rect.y - self.square.height)
                self.touching_platform = True
        elif self.square.x >= platform3.rect.x and self.square.x <= platform3.rect.x + platform3.rect.width and self.square.y+self.square.height <= platform3.rect.y and self.square.y + self.square.height >= platform3.rect.y - 30:
            self.xvel = platform3.vel
            self.jumpcount = 0
            self.yvel = 0
            if (self.isJump == True and self.jvel <= -6) or self.isJump == False:
                self.square.y = (platform3.rect.y - self.square.height)
                self.touching_platform = True
        else:
            self.xvel = 0
            self.yvel = 15
    def shot(self, bullet):
        if self.ishit:
            if bullet.ykb >= -6:
                if bullet.ykb >= 0:
                    F = (self.mass ** -1) *(bullet.ykb**2)
                elif bullet.ykb < 0:
                    F = (self.mass**-1) * -1 * (bullet.ykb**2)
                self.square.y-= F
                bullet.ykb -= 1
            self.square.x += (bullet.xkb * bullet.direction)
    def upgraded(self, upgrade):
        if self.upgrade.power == 1:
            pass
        if self.upgrade.power == 2:
            pass
        if self.upgrade.power == 3:
            pass
        if self.upgrade.power == 4:
            pass
        if self.upgrade.power == 5:
            pass
        if self.upgrade.power == 6:
            pass
        if self.upgrade.power == 7:
            pass
        if self.upgrade.power == 8:
            pass
        if self.upgrade.power == 9:
            pass
        if self.upgrade.power == 10:
            pass


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

class Upgrade(object):
    def __init__(self):
        self.x = math.random.randint(20, 580)
        self.y = 50
        self.height = 15
        self.width = 15
        self.yvel = 10
        self.powerId = math.random.randint(1, 10)
    def move(self):
        self.y += self.yvel
    def check_for_platform(self, platform1, platform2, platform3):
        #Detecs if player is on platform or not(Platform Collision)
        if self.x >= platform1.rect.x and self.x <= platform1.rect.x + platform1.rect.width and self.y + self.height <= platform1.rect.y and self.y + self.height>= platform1.rect.y - 30:
            self.yvel = 0
            self.y = (platform1.rect.y - self.height)
        elif self.x >= platform2.rect.x and self.x <= platform2.rect.x + platform2.rect.width and self.y + self.height<= platform2.rect.y and self.y + self.height >= platform2.rect.y - 30:
            self.yvel = 0
            self.y = (platform2.rect.y - self.height)
        elif self.x >= platform3.rect.x and self.x <= platform3.rect.x + platform3.rect.width and self.y + self.height <= platform3.rect.y and self.y + self.height >= platform3.rect.y - 30:
            self.yvel = 0
            self.y = (platform3.rect.y - self.height)
    def choose_random_gun(self, player):
            random_gun_index = math.random.randint(0, 10)
            gun = gun_list[random_gun_index]
            gun.owner = player
            player.lastgun = player.gun
            player.gun = gun

#Creates all of the objects
#Order goes as follows: x, y, width, height, vel
platform1 = Platform(0,550,70,10, 5)
platform2 = Platform(530,550,70,10, -5)
platform3 = Platform(150,450,300,10,0)
#Order goes as follows: x,y,width,height,yvel,xvel, mass, jvel, player_num, lives
player1 = Player(300,100,15,15,10,0,1,8, 1, 10)
player2 = Player(300,100,15,15,10,0,1,8, 2, 10)
#Order goes as follows: owner, ammo, bulletvel, cooldown, bullet_kb
gun1 = Gun(player1, 10, 400, 50, 1)
player1.gun = gun1
gun2 = Gun(player2, 10, 400, 50, 1)
player2.gun = gun2

#Gun List:
gun_1 = Gun(None, 50, 400, 10, 3)#Sub machine gun
gun_2 = Gun(None, 5, 400, 100, 10)#Sniper
gun_3 = Gun(None, 5, 400, 100, 10)#Shotgun
gun_4 = Gun(None, 30, 400, 35, 3)#Assault rifle
gun_5 = Gun(None, 50, 400, 10, 3)#Light machine gun
#Special
gun_6 = Gun(None, 100, 400, 0, 3)#Minigun
gun_7 = Gun(None, 3, 400, 150, 4)#Dematerializer
#Gun_list stores all the special guns that arrive in lootboxes
#Sets up the window
win = pygame.display.set_mode((600, 600))
pygame.display.set_caption("This is pygame")
pygame.display.flip()
player1image = pygame.transform.scale(player1image, DEFAULT_IMAGE_SIZE)
run = True

#Code for upgrade timer
upgrade_now = pygame.time.get_ticks()
#Code for gunbox timer
gunbox_now = pygame.time.get_ticks()

#Main
pygame.display.flip()
while run:
    pygame.time.delay(100)
    #To let the user quit the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run=False
    keys = pygame.key.get_pressed()
    update_window()
    #Makes the platforms move
    scrn.blit(player1image, (player1.square.x, player1.square.y))
    platform1.moves()
    platform2.moves()
    platform3.moves()
    #Actions of both players
    #Moves and Jumps
    player1.move()
    player2.move()
    player1.jumpy()
    player2.jumpy()
    #respawn
    if player1.square.y > 600:
        player1.respawn()
    if player2.square.y > 600:
        player2.respawn()
    #Check for platform collision
    player1.check_for_platform(platform1, platform2, platform3)
    player2.check_for_platform(platform1, platform2, platform3)
    #Shoots
    if keys[pygame.K_SPACE]:
        player1.gun.shoot()
    if keys[pygame.K_z]:
        player2.gun.shoot()
    #Bullet code
    for bullet in bullet_list:
        if bullet.x > 600 or bullet.x < 0 or bullet.hit_enemy == True:
            bullet_list.remove(bullet)
        else:
            if bullet.owner == player1:
                bullet.check_collision(player2)
                pygame.draw.rect(win,color_dict['green'],(bullet.x, bullet.y,bullet.width,bullet.height))
            else:
                pygame.draw.rect(win,color_dict['red'],(bullet.x, bullet.y,bullet.width,bullet.height))
                bullet.check_collision(player1)
            bullet.move()
    #Upgrade code
    upgrade_last = pygame.time.get_ticks()
    if upgrade_now - upgrade_last >= 500:
        upgrade_now = upgrade_last
        randchance = math.random.ranint(1,2)
        if randchance == 1:
            upgrade = Upgrade()
            upgrade_list.append(upgrade)
    for upgrade in upgrade_list:
        upgrade.check_for_platform(platform1, platform2, platform3)
        upgrade.move()
        pygame.draw.circle(win, color_dict["blue"], (upgrade.x, upgrade.y, upgrade.width, upgrade.height))
        if (upgrade.x<=player1.square.x+player1.square.width) and (upgrade.x + upgrade.width >= player1.square.x) and (upgrade.y <= player1.square.y+ player1.square.height) and (upgrade.y + upgrade.width >= player1.square.y):
            player1.upgraded()
        elif (upgrade.x<=player2.square.x+player2.square.width) and (upgrade.x + upgrade.width >= player2.square.x) and (upgrade.y <= player2.square.y+ player2.square.height) and (upgrade.y + upgrade.width >= player2.square.y):
            player2.upgraded()
        upgrade_list.remove(upgrade)
    #Gunbox code
    gunbox_last = pygame.time.get_ticks()
    if gunbox_now-gunbox_last >= 300:
        gunbox_now = gunbox_last
        gunbox = Upgrade()
        gunbox_list.append(gunbox)
    for gunbox in gun_list:
        gunbox.check_for_platform(platform1, platform2, platform3)
        gunbox.move()
        pygame.draw.rect(win, color_dict["blue"], (gunbox.x, gunbox.y, gunbox.width, gunbox.height))
        if (gunbox.x<=player1.square.x+player1.square.width) and (gunbox.x + gunbox.width >= player1.square.x) and (gunbox.y <= player1.square.y+ player1.square.height) and (gunbox.y + gunbox.width >= player1.square.y):
            gunbox.choose_random_gun(player1)
        elif (gunbox.x<=player2.square.x+player2.square.width) and (gunbox.x + gunbox.width >= player2.square.x) and (gunbox.y <= player2.square.y+ player2.square.height) and (gunbox.y + gunbox.width >= player2.square.y):
            gunbox.choose_random_gun(player2)
        gunbox_list.remove(gunbox)
    pygame.display.update()
pygame.quit()