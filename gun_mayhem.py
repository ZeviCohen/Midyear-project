import pygame, math, random
# copy of previous platform detection code: (self.square.x >= platform1.rect.x and self.square.x <= platform1.rect.x + 70 and self.square.y <= platform1.rect.y - 15 and self.square.y >= platform1.rect.y - 18) or (self.square.x >= platform2.rect.x and self.square.x <= platform2.rect.x + 70 and self.square.y <= platform2.rect.y - 15 and self.square.y >= platform2.rect.y - 18) or (self.square.x >= platform3.rect.x and self.square.x <= platform3.rect.x + 300 and self.square.y <= platform3.rect.y - 15 and self.square.y >= platform3.rect.y - 18)
#Color Palette
color_dict = {"white":(255, 255, 255),"red":(255, 0, 0), "green":(0, 255, 0), "blue":(0, 0, 255), "black":(0, 0, 0), "sky_blue":(138, 206, 251), "olive_green": (95, 107, 47), "coral": (255, 127, 150)}
day_or_night = "day"
pygame.init()
bullet_list = []
upgrade_list = []
upgrade_used_list = []
gunbox_list = []
gunbox_used_list = []
font = pygame.font.SysFont("comicsansms", 17)
win = pygame.display.set_mode((600, 600))
#Images
player1image = pygame.image.load("Images/Meowth-Pokemon-PNG-Transparent-Image.png").convert()
platform3image = pygame.image.load("Images/download.png").convert()
def update_window():

    # Draws the platforms
    pygame.draw.rect(win,color_dict["red"],platform1.rect)
    pygame.draw.rect(win,color_dict["red"],platform2.rect)
    pygame.draw.rect(win,color_dict['red'],platform3.rect)
    pygame.draw.rect(win,color_dict["red"],platform4.rect)
    pygame.draw.rect(win,color_dict["red"],platform5.rect)
    pygame.draw.rect(win,color_dict['red'],platform6.rect)
    #Draws the players
    pygame.draw.rect(win,color_dict["green"],(player1.square))
    pygame.draw.rect(win,color_dict['red'],(player2.square))
class Gun ():
    def __init__(self, owner, ammo, cooldown, bullet_kb, gunid):
        self.cooldown = cooldown
        self.ammo = ammo
        self.last = pygame.time.get_ticks()
        self.owner = owner
        self.bullet_kb = bullet_kb
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
        #Generates a bullet with distance from the owner
        self.bullet_spawn_distance = 30
        #Defines the direction of the bullet
        if self.owner.lastrecorded == 'LEFT':
            self.x = self.owner.square.x - self.bullet_spawn_distance
            self.direction = -1
        if self.owner.lastrecorded == 'RIGHT' or self.owner.lastrecorded == None:
            self.x = self.owner.square.x + self.bullet_spawn_distance
            self.direction = 1
        self.y = owner.square.y
        self.velocity = 20
        self.width = 10
        self.height = 5
        self.xkb = bullet_xkb
        self.ykb = 5.3
        self.hit_enemy = False
    def move(self):
        self.velocity = self.direction * abs(self.velocity)
        self.x += self.velocity
    def check_collision(self, enemy):
        if (self.x + self.width >= enemy.square.x) and (self.x <= enemy.square.x + enemy.square.width) and (self.y + self.height >= enemy.square.y) and (self.y <= enemy.square.y + enemy.square.height) and self.hit_enemy == False:
            enemy.ishit = True
            self.hit_enemy = True
            enemy.bullet = self
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
        self.jumpcount = 2
        self.touching_platform = False
        self.ishit = False
        self.gun = None
        self.maingun = None
        self.bullet = None

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
                        else:
                            self.jvel = 5
                            self.isJump = True
                            self.touching_platform = False
                            self.jumpcount = 2
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
                if (self.square.x >= platform1.rect.x and self.square.x <= platform1.rect.x + platform1.rect.width and self.square.y <= platform1.rect.y and self.square.y >= platform1.rect.y - 20) or (self.square.x >= platform2.rect.x and self.square.x <= platform2.rect.x + platform2.rect.width and self.square.y <= platform2.rect.y and self.square.y >= platform2.rect.y - 20) or (self.square.x >= platform3.rect.x and self.square.x <= platform3.rect.x + platform3.rect.width and self.square.y <= platform3.rect.y and self.square.y >= platform3.rect.y - 20):
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
                        else:
                            self.jvel = 5
                            self.isjump = True
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
        self.ishit = False

    def check_for_platform(self, platform1, platform2, platform3, platform4, platform5, platform6):
        #Detects if player is on platform or not(Platform Collision)
        if self.square.x + self.square.width >= platform1.rect.x and self.square.x <= platform1.rect.x + platform1.rect.width and self.square.y + self.square.height <= platform1.rect.y and self.square.y + self.square.height >= platform1.rect.y - 30:
            self.xvel = platform1.vel
            self.jumpcount = 0
            self.yvel = 0
            if (self.isJump == True and self.jvel <= -6) or self.isJump == False:
                self.square.y = (platform1.rect.y - self.square.height)
                self.touching_platform = True
        elif self.square.x + self.square.width >= platform2.rect.x and self.square.x <= platform2.rect.x + platform2.rect.width and self.square.y + self.square.height <= platform2.rect.y and self.square.y + self.square.height >= platform2.rect.y - 30:
            self.xvel = platform2.vel
            self.jumpcount = 0
            self.yvel = 0
            if (self.isJump == True and self.jvel <= -6) or self.isJump == False:
                self.square.y = (platform2.rect.y - self.square.height)
                self.touching_platform = True
        elif self.square.x + self.square.width >= platform3.rect.x and self.square.x <= platform3.rect.x + platform3.rect.width and self.square.y+self.square.height <= platform3.rect.y and self.square.y + self.square.height >= platform3.rect.y - 30:
            self.xvel = platform3.vel
            self.jumpcount = 0
            self.yvel = 0
            if (self.isJump == True and self.jvel <= -6) or self.isJump == False:
                self.square.y = (platform3.rect.y - self.square.height)
                self.touching_platform = True
        elif self.square.x + self.square.width >= platform4.rect.x and self.square.x <= platform4.rect.x + platform4.rect.width and self.square.y+self.square.height <= platform4.rect.y and self.square.y + self.square.height >= platform4.rect.y - 30:
            self.xvel = platform4.vel
            self.jumpcount = 0
            self.yvel = 0
            if (self.isJump == True and self.jvel <= -6) or self.isJump == False:
                self.square.y = (platform4.rect.y - self.square.height)
                self.touching_platform = True
        elif self.square.x + self.square.width >= platform5.rect.x and self.square.x <= platform5.rect.x + platform5.rect.width and self.square.y+self.square.height <= platform5.rect.y and self.square.y + self.square.height >= platform5.rect.y - 30:
            self.xvel = platform5.vel
            self.jumpcount = 0
            self.yvel = 0
            if (self.isJump == True and self.jvel <= -6) or self.isJump == False:
                self.square.y = (platform5.rect.y - self.square.height)
                self.touching_platform = True
        elif self.square.x + self.square.width >= platform6.rect.x and self.square.x <= platform6.rect.x + platform6.rect.width and self.square.y+self.square.height <= platform6.rect.y and self.square.y + self.square.height >= platform6.rect.y - 30:
            self.xvel = platform6.vel 
            self.jumpcount = 0
            self.yvel = 0
            if (self.isJump == True and self.jvel <= -6) or self.isJump == False:
                self.square.y = (platform6.rect.y - self.square.height)
                self.touching_platform = True
        else:
            self.xvel = 0
            self.yvel = 15
            self.touching_platform = False
    def shot(self, bullet):
        if self.ishit:
            self.isJump = False
            if bullet.ykb >= 0:
                self.yvel = 0
                F = (self.mass ** -1) * (bullet.ykb**2)
                self.square.y-= F
                bullet.ykb -= 1
            else:
                self.yvel = 10
                self.ishit = False
            self.square.x += (bullet.xkb * bullet.direction)
    def upgraded(self, upgrade):
        if upgrade.powerId == 1:
            pass
        if upgrade.powerId == 2:
            pass
        if upgrade.powerId == 3:
            pass
        if upgrade.powerId == 4:
            pass
        if upgrade.powerId == 5:
            pass
        if upgrade.powerId == 6:
            pass
        if upgrade.powerId == 7:
            pass
        if upgrade.powerId == 8:
            pass
        if upgrade.powerId == 9:
            pass
        if upgrade.powerId == 10:
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

class Upgrade(object):
    def __init__(self, platform, gunbox_check):
        self.platform = platform
        #Default width and height
        self.width = 15
        self.height = 15
        self.yvel = 10
        #Default powerID(stays 0 if upgrade is gunbox)
        self.powerId = 0
        if gunbox_check:
            self.y = 100
            self.x = random.randint(20, 580)
            self.width = 30
            self.height = 30
            self.image = pygame.image.load("Images/Gunbox.png").convert_alpha()
        else:
            self.y = platform.rect.y - platform.rect.height
            num1 = platform.rect.x
            num2 = (platform.rect.x + platform.rect.width)- self.width
            self.x = random.randint(num1, num2)
            self.powerId = random.randint(1, 10)
        #Speed up
        if self.powerId == 1:
            self.image = pygame.image.load("Images/speed_power.png").convert()
        if self.powerId == 2:
            self.image = pygame.image.load("Images/speed_power.png").convert()
        if self.powerId == 3:
            self.image = pygame.image.load("Images/speed_power.png").convert()
        if self.powerId == 4:
            self.image = pygame.image.load("Images/speed_power.png").convert()
        if self.powerId == 5:
            self.image = pygame.image.load("Images/speed_power.png").convert()
        if self.powerId == 6:
            self.image = pygame.image.load("Images/speed_power.png").convert()
        if self.powerId == 7:
            self.image = pygame.image.load("Images/speed_power.png").convert()
        if self.powerId == 8:
            self.image = pygame.image.load("Images/speed_power.png").convert()
        if self.powerId == 9:
            self.image = pygame.image.load("Images/speed_power.png").convert()
        if self.powerId == 10:
            self.image = pygame.image.load("Images/speed_power.png").convert()
        self.radius = 10
        #True means getting bigger while false means getting smaller
        self.radius_change_state = True
        self.owner = None
        self.last = None
    def move(self):
        self.y += self.yvel
    def check_for_platform(self, platform1, platform2, platform3):
        #Detecs if player is on platform or not(Platform Collision)
        if self.x >= platform1.rect.x and self.x <= platform1.rect.x + platform1.rect.width and self.y + self.height <= platform1.rect.y and self.y + self.height>= platform1.rect.y - 45:
            self.yvel = 0
            self.y = (platform1.rect.y - self.height)
            self.platform = platform1
        elif self.x >= platform2.rect.x and self.x <= platform2.rect.x + platform2.rect.width and self.y + self.height<= platform2.rect.y and self.y + self.height >= platform2.rect.y - 45:
            self.yvel = 0
            self.y = (platform2.rect.y - self.height)
            self.platform = platform2
        elif self.x >= platform3.rect.x and self.x <= platform3.rect.x + platform3.rect.width and self.y + self.height <= platform3.rect.y and self.y + self.height >= platform3.rect.y - 45:
            self.yvel = 0
            self.y = (platform3.rect.y - self.height)
            self.platform = platform3
    def choose_random_gun(self, player):
            random_gun_index = random.randint(0, 6)
            gun = gun_list[random_gun_index]
            gun.owner = player
            player.maingun = player.gun
            player.gun = gun
    def radius_change(self):
        if self.radius_change_state:
            self.radius += 0.5
        else:
            self.radius -= 0.5
        if self.radius <= 9:
            self.radius_change_state = True
        if self.radius >= 11:
            self.radius_change_state = False
    def platform_move(self):
        self.x += self.platform.vel

        

#Creates all of the objects
#Order goes as follows: x, y, width, height, vel
platform1 = Platform(0,450,70,10, 5)
platform2 = Platform(530,450,70,10, -5)
platform3 = Platform(150,400,300,10,0)
platform4 = Platform(20,350,100,10,0)
platform5 = Platform(500,350,100,10,0)
platform6 = Platform(150,300,300,10,0)
#Order goes as follows: x,y,width,height,yvel,xvel, mass, jvel, player_num, lives
player1 = Player(300,100,18,35,10,0,1,8, 1, 10)
player2 = Player(300,100,18,35,10,0,1,8, 2, 10)
#Order goes as follows: owner, ammo, cooldown, bullet_kb, gunid
maingun1 = Gun(player1, 10, 400, 18, 0)
player1.maingun = maingun1
player1.gun = maingun1
maingun2 = Gun(player2, 10, 400, 18, 0)
player2.maingun = maingun2
player2.gun = maingun2

#Gun List:
#Order goes as follows: owner, ammo, cooldown, bullet_kb, gunid
gun_1 = Gun(None, 50, 200, 25, 1)#Sub machine gun
gun_2 = Gun(None, 5, 500, 35, 1)#Sniper
gun_3 = Gun(None, 5, 500, 35, 1)#Shotgun
gun_4 = Gun(None, 30, 250, 25, 1)#Assault rifle
gun_5 = Gun(None, 50, 200, 25, 1)#Light machine gun
#Special
gun_6 = Gun(None, 100, 100, 25, 1)#Minigun
gun_7 = Gun(None, 3, 750, 4, 1)#Dematerializer
#Gun_list stores all the special guns that arrive in lootboxes
gun_list = [gun_1, gun_2, gun_3, gun_4, gun_5, gun_6, gun_7]
#Sets up the window
win = pygame.display.set_mode((600, 600))
pygame.display.set_caption("This is pygame")
pygame.display.flip()
player1image = pygame.transform.scale(player1image, (player1.square.width, player1.square.height))
platform3image = pygame.transform.scale(platform3image, (platform3.rect.width, platform3.rect.height))
run = True

#Code for upgrade timer
upgrade_last = pygame.time.get_ticks()
#Code for gunbox timer
gunbox_last = pygame.time.get_ticks()

#Main
pygame.display.flip()
last = 0
while run:
    pygame.time.delay(100)
    #To let the user quit the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run=False
    keys = pygame.key.get_pressed()
    #Makes the background and all of the objects
    now = pygame.time.get_ticks()
    #Day-Night Cycle lasts about 100 seconds(day --> night)
    if now - last >= 50000:
        if day_or_night == "day":
            day_or_night = "night"
            last = pygame.time.get_ticks()
        elif day_or_night == "night":
            day_or_night = "day"
            last = pygame.time.get_ticks()
    if day_or_night == "day":
        win.fill(color_dict["sky_blue"])
    else:
        win.fill(color_dict["black"])
    #Lives counter
    player1counter = font.render(f"Player 1: {player1.lives} lives", True, (color_dict["olive_green"]))
    player2counter = font.render(f"Player 2: {player2.lives} lives", True, (color_dict["coral"]))
    win.blit(player1counter, (70 - player1counter.get_width()//2, 560 - player1counter.get_height()//2))
    win.blit(player2counter, (530 - player2counter.get_width()//2, 560 - player2counter.get_height()//2))
    update_window()
    #Makes the platforms move
    win.blit(player1image, (player1.square.x, player1.square.y))
    win.blit(platform3image, (platform3.rect.x, platform3.rect.y))
    platform1.moves()
    platform2.moves()
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
    player1.check_for_platform(platform1, platform2, platform3, platform4, platform5, platform6)
    player2.check_for_platform(platform1, platform2, platform3, platform4, platform5, platform6)
    #Shoots
    if keys[pygame.K_SPACE]:
        player1.gun.shoot()
    if keys[pygame.K_z]:
        player2.gun.shoot()
    for bullet in bullet_list:
        if bullet.x > 600 or bullet.x < 0 or bullet.hit_enemy == True:
            bullet_list.remove(bullet)
        else:
            if bullet.owner == player1:
                bullet.check_collision(player2)
                pygame.draw.rect(win,color_dict['green'],(bullet.x, bullet.y,bullet.width,bullet.height))
            else:
                bullet.check_collision(player1)
                pygame.draw.rect(win,color_dict['red'],(bullet.x, bullet.y,bullet.width,bullet.height))
            bullet.move()
    player1.shot(player1.bullet)
    player2.shot(player2.bullet)
    #Upgrade code
    if now - upgrade_last >= 10000:
        upgrade_last = now
        if len(upgrade_list) < 2:
            randchance = random.randint(1,2)
            if randchance == 1:
                upgrade_platform = random.randint(1, 6)
                if upgrade_platform == 1:
                    upgrade = Upgrade(platform1, False)
                if upgrade_platform == 2:
                    upgrade = Upgrade(platform2, False)
                if upgrade_platform == 3:
                    upgrade = Upgrade(platform3, False)
                if upgrade_platform == 4:
                    upgrade = Upgrade(platform4, False)
                if upgrade_platform == 5:
                    upgrade = Upgrade(platform5, False)
                if upgrade_platform == 6:
                    upgrade = Upgrade(platform6, False)
                upgrade_list.append(upgrade)
    for upgrade in upgrade_list:
        upgrade.radius_change()
        upgrade.platform_move()
        pygame.draw.circle(win, color_dict["blue"], (upgrade.x, upgrade.y), upgrade.radius)
        upgrade.image = pygame.transform.scale(upgrade.image, (upgrade.width, upgrade.height))
        win.blit(upgrade.image, (upgrade.x, upgrade.y))
        if (upgrade.x<=player1.square.x+player1.square.width) and (upgrade.x + upgrade.width >= player1.square.x) and (upgrade.y <= player1.square.y+ player1.square.height) and (upgrade.y + upgrade.width >= player1.square.y):
            upgrade.owner = player1
            upgrade.last = pygame.time.get_ticks()
            upgrade_list.remove(upgrade)
            upgrade_used_list.append(upgrade)
        elif (upgrade.x<=player2.square.x+player2.square.width) and (upgrade.x + upgrade.width >= player2.square.x) and (upgrade.y <= player2.square.y+ player2.square.height) and (upgrade.y + upgrade.width >= player2.square.y):
            upgrade.owner = player2
            upgrade.last = pygame.time.get_ticks()
            upgrade_list.remove(upgrade)
            upgrade_used_list.append(upgrade)
    for upgrade in upgrade_used_list:
        upgrade.owner.upgraded(upgrade)
        if now - upgrade.last >= 3000:
            upgrade_used_list.remove(upgrade)
    #Gunbox code
    if now - gunbox_last >= 7500:
        gunbox_last = now
        gunbox = Upgrade(None, True)
        gunbox_list.append(gunbox)
    for gunbox in gunbox_list:
        gunbox.check_for_platform(platform1, platform2, platform3)
        gunbox.check_for_platform(platform4, platform5, platform6)
        gunbox.move()
        if gunbox.platform != None:
            gunbox.platform_move()
        pygame.draw.rect(win, color_dict["blue"], (gunbox.x, gunbox.y, gunbox.width, gunbox.height))
        gunbox.image = pygame.transform.scale(gunbox.image, (gunbox.width, gunbox.height))
        win.blit(gunbox.image, (gunbox.x, gunbox.y))
        if (gunbox.x<=player1.square.x+player1.square.width) and (gunbox.x + gunbox.width >= player1.square.x) and (gunbox.y <= player1.square.y+ player1.square.height) and (gunbox.y + gunbox.width >= player1.square.y):
            gunbox.choose_random_gun(player1)
            gunbox_list.remove(gunbox)
        elif (gunbox.x<=player2.square.x+player2.square.width) and (gunbox.x + gunbox.width >= player2.square.x) and (gunbox.y <= player2.square.y+ player2.square.height) and (gunbox.y + gunbox.width >= player2.square.y):
            gunbox.choose_random_gun(player2)
            gunbox_list.remove(gunbox)
    pygame.display.update()
pygame.quit()