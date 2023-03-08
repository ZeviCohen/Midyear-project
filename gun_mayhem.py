import pygame, math, random

#Initializes pygame
pygame.init()

#Sets up the window
win = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Gone Mayhem")
pygame.display.flip()

#Defines the current screen
game_state = "start"

#Color Palette
color_dict = {"white":(255, 255, 255),"red":(255, 0, 0), "green":(0, 255, 0), "blue":(0, 0, 255), "black":(0, 0, 0), "sky_blue":(138, 206, 251), "olive_green": (95, 107, 47), "deep_green": (0, 100, 0), "coral": (255, 127, 150), "cardboard_brown": (237, 218, 116), "dusk_orange": (245, 129, 56), "turquoise": (2)}
#Lists that will be used later
bullet_list = []
upgrade_list = []
upgrade_used_list = []
gunbox_list = []
gunbox_used_list = []
#Changes color
def change_colors(color1, color2, time):
    length = 0
    new_color = []
    while length < len(color1):
        new_color.append(color1[length] - (color1[length] - color2[length])/(time/2))
        length += 1
    return new_color

#Fades to black and back
def fade_to_black(current_color, future_color):
    now = last = pygame.time.get_ticks()
    temp_color = current_color
    while now - last <= 1000:
        pygame.time.delay(10)
        temp_color = change_colors(temp_color, color_dict["black"], 100)
        now = pygame.time.get_ticks()
        win.fill(temp_color)
        pygame.display.update()
    now = last = pygame.time.get_ticks()
    while now - last <= 1500:
        pygame.time.delay(10)
        temp_color = change_colors(temp_color, future_color, 200)
        now = pygame.time.get_ticks()
        win.fill(temp_color)
        pygame.display.update()
#This function creates the game's start menu
def create_start_menu():
    run = True
    while run:
        pygame.time.delay(100)
        win.fill(color_dict["sky_blue"])
        #To let the user quit the window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False
        #Title
        title_font = pygame.font.SysFont("timesnewroman", 45)
        titleRender = title_font.render("Gone Mayhem", True, color_dict["deep_green"])
        titleRect = titleRender.get_rect()
        titleRect.center = (175, 75)
        win.blit(titleRender, titleRect.center)
        #Button
        start_font = pygame.font.SysFont("timesnewroman", 30)
        startRender = start_font.render("Left-click to start", True, color_dict["olive_green"])
        startRect = startRender.get_rect()
        startRect.center = (200, 450)
        win.blit(startRender, startRect.center)
        pygame.display.update()
    fade_to_black(color_dict["sky_blue"], color_dict["coral"])
class Gun ():
    def __init__(self, name, owner, ammo, cooldown, bullet_kb, gunid, image_left, image_right):
        #How long between each bullet being fired
        self.cooldown = cooldown
        #To work with cooldown
        self.last = pygame.time.get_ticks()
        #The default ammo so it can be restored on respawn
        self.perm_ammo = ammo
        #The ammo being actively used
        self.ammo = ammo
        #Attributes it will pass down to each bullet it makes
        self.owner = owner
        self.bullet_kb = bullet_kb
        #to see if it is a maingun or not
        self.gunid = gunid
        #For the text at the bottom of the screen
        self.name = name
        #Current image
        self.image = image_left
        self.image_left = image_left
        self.image_right = image_right
        #Dimensions(Original)
        self.width = 20
        self.height = 15
    def image_update(self):
        #If the owner is facing left & isn't upgraded
        if self.owner.lastrecorded == "LEFT":
            self.image = self.image_left
            #Maingun
            if self.gunid == 0:
                win.blit(self.image, (self.owner.square.x - self.width, self.owner.square.y + 5))
            #Specials(because image is slightly misaligned)
            else:
                win.blit(self.image, (self.owner.square.x - self.width - 15, self.owner.square.y - 7))
        if self.owner.lastrecorded == "RIGHT":
            self.image = self.image_right
            #Maingun
            if self.gunid == 0:
                win.blit(self.image, (self.owner.square.x + self.owner.square.width, self.owner.square.y + 5))
            #Specials(because image is slightly misaligned)
            else:
                win.blit(self.image, (self.owner.square.x + self.owner.square.width, self.owner.square.y - 7))
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
            #only reloads if the gun is a main gun
            if self.gunid == 0:
                if now - self.last >= 3000:
                    self.last = now
                    self.ammo = 10
                    bullet_list.append(Bullet(self.owner, self.bullet_kb))
            #If it is not a main gun then the player loses the gun and gets back their main gun
            else:
                self.owner.gun = self.owner.maingun

# Bullet Class
class Bullet(object):
    #Constructor
    def __init__(self, owner, bullet_xkb):
        self.owner = owner
        self.y = owner.square.y + 7.5
        self.vel = 20
        self.width = 10
        self.height = 5
        self.xkb = bullet_xkb
        self.ykb = 5.5
        #When the bullet does hit the enemy, this will become true and affect what the bullet does
        self.hit_enemy = False
        #Defines the direction of the bullet and makes it on that side of the player
        if self.owner.lastrecorded == 'LEFT':
            self.x = self.owner.square.x - 15 - self.width
            self.direction = -1
        if self.owner.lastrecorded == 'RIGHT' or self.owner.lastrecorded == None:
            self.x = self.owner.square.x + 15 + self.owner.square.width
            self.direction = 1
    def move(self):
        self.vel= self.direction * abs(self.vel)
        self.x += self.vel
    def check_collision(self, enemy):
        #Checks for collision with the enemy/opponent
        if (self.x + self.width >= enemy.square.x) and (self.x <= enemy.square.x + enemy.square.width) and (self.y + self.height >= enemy.square.y) and (self.y <= enemy.square.y + enemy.square.height) and self.hit_enemy == False:
            if self.owner.gun.name == "Dematerializer":
                enemy.ishit = False
                self.hit_enemy = True
                enemy.bullet = None
                enemy.respawn()
            else:
                enemy.ishit = True
                self.hit_enemy = True
                enemy.bullet = self
#Our player class
class Player(object):
    def __init__(self,x,y,width,height,yvel,xvel, mass, jvel, player_num, lives, image):
        #Coordinates and dimensions
        self.square = pygame.Rect(x,y,width,height)
        #to determine the players direction
        self.lastrecorded = "RIGHT"
        #Determines how fast the player moves
        self.walkspeed = 10
        #yvel is for gravity while xvel is for moving with the moving platforms
        self.yvel = yvel
        self.xvel = xvel
        #Checks whether the player can jump. It is initialized to false as the player is in the air and hasn't yet touched a platform
        self.isJump = False
        #Changes jump height
        self.mass = mass
        #Affects the curve of the parabola for jump height
        self.jvel = jvel
        #Count for whether the player has already jumped, determening if they can jump again
        self.jumpcount = 2
        #To check whether it is player 1 or player 2. This is more for the code in main to easily differentiate between the two players
        self.player_num = player_num
        #The players lives
        self.lives = lives
        #This is set to true when the player is touching a platform (which is checked for in the function check_for_platform())
        self.touching_platform = False
        #Determines whether the player is taking knockback from a bullet or not
        self.ishit = False
        #The players gun and maingun. The difference is that the players gun is the one they are currently using while the maingun is there to be the default gun when they run out of ammo
        self.gun = None
        self.maingun = None
        #So that there is only one bullet affecting the player at a time
        self.bullet = None
        self.image = image
        #Checks if there is a shield
        self.isShield = False
        self.shield_width = 60
        self.shield_height = 60

    def move(self):
        #Gravity
        if self.isJump == False:
            self.square.y += self.yvel
        self.square.x += self.xvel
        #Checks for key presses(Player 1)
        keys = pygame.key.get_pressed()
        if self.player_num == 1:
            #moves left
            if keys[pygame.K_LEFT]:
                self.square.x += (self.walkspeed * -1)
                self.lastrecorded = 'LEFT'
            #moves right
            if keys[pygame.K_RIGHT]:
                self.square.x += self.walkspeed
                self.lastrecorded = 'RIGHT'
            #goes down through the platform
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
            #For second jump
            elif self.jumpcount == 1:
                if keys[pygame.K_UP]:
                    self.jvel = 5
                    self.jumpcount = 2
                    self.isJump = True
        #Checks for key presses(Player 2)
        elif self.player_num == 2:
            #moves left
            if keys[pygame.K_a]:
                self.square.x += (self.walkspeed * -1)
                self.lastrecorded = 'LEFT'
            #moves right
            if keys[pygame.K_d]:
                self.square.x += self.walkspeed
                self.lastrecorded = 'RIGHT'
            #goes through platform
            if keys[pygame.K_s]:
                if self.touching_platform == True:
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
            #for second jump
            elif self.jumpcount == 1:
                if keys[pygame.K_w]:
                    self.jvel = 5
                    self.jumpcount = 2
                    self.isJump = True

    def jumpy(self):
        #The player is moved vertically in a jump by using a variable to make a parabola. The jump has been set to 6 --> -6 sqaured for first jump and 4 --> -4 for the second jump. These variables can be changed.
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
        #This is called when the player falls off the map. Everything is reset for the player, they are affected by gravity and they are spawned in at a random x-coordinate
        pygame.time.delay(100)
        self.square.y = 50
        self.square.x = 300 - (self.square.width/2)
        self.lives -= 1
        self.isJump = False
        self.ishit = False
        #resets gun and ammo
        self.gun = self.maingun
        self.maingun.ammo = self.maingun.perm_ammo
        #Gets rid of all the players upgrades
        # for upgrade in upgrade_used_list:
        #     if upgrade.owner == self:
        #         self.remove_upgrade(upgrade)
        self.walkspeed = 10
        self.mass = 1
        self.lives = self.lives
        self.square.width = 25
        self.square.height = 45
        self.image = pygame.transform.scale(self.image, (self.square.width, self.square.height))
        self.gun.width = 20
        self.gun.height = 15
        self.gun.image_left = pygame.transform.scale(self.gun.image_left, (self.gun.width, self.gun.height))
        self.gun.image_right = pygame.transform.scale(self.gun.image_right, (self.gun.width, self.gun.height))
        self.shield_width = 10
        self.shield_height = 10
        self.isShield = False


    def check_for_platform(self, platform1, platform2, platform3, platform4, platform5, platform6):
        #Detects if player is on platform or not(Platform Collision) If it is, as long as the player is finished jumping(so they don't get sucked into the platform mid-jump), the player is able to jump again, their xvel is set to the platforms(so they will move with the moving platforms), they are no longer affected by gravity, and it will set the players y coordinate so they are standing on the platform
        #Just as a test. It works but not quite as well. To make it work just make each of the if statements if collide1: or elif collide2: etc.
        # collide1 = self.square.colliderect(platform1.rect)
        # collide2 = self.square.colliderect(platform2.rect)
        # collide3 = self.square.colliderect(platform3.rect)
        # collide4 = self.square.colliderect(platform4.rect)
        # collide5 = self.square.colliderect(platform5.rect)
        # collide6 = self.square.colliderect(platform6.rect)
        if self.square.x + self.square.width >= platform1.rect.x and self.square.x <= platform1.rect.x + platform1.rect.width and self.square.y + self.square.height <= platform1.rect.y and self.square.y + self.square.height >= platform1.rect.y - 30:
            if (self.isJump == True and self.jvel <= -4) or self.isJump == False:
                self.xvel = platform1.vel
                self.jumpcount = 0
                self.yvel = 0
                self.square.y = (platform1.rect.y - self.square.height)
                self.touching_platform = True
        elif self.square.x + self.square.width >= platform2.rect.x and self.square.x <= platform2.rect.x + platform2.rect.width and self.square.y + self.square.height <= platform2.rect.y and self.square.y + self.square.height >= platform2.rect.y - 30:
            if (self.isJump == True and self.jvel <= -4) or self.isJump == False:
                self.xvel = platform2.vel
                self.jumpcount = 0
                self.yvel = 0
                self.square.y = (platform2.rect.y - self.square.height)
                self.touching_platform = True
        elif self.square.x + self.square.width >= platform3.rect.x and self.square.x <= platform3.rect.x + platform3.rect.width and self.square.y+self.square.height <= platform3.rect.y and self.square.y + self.square.height >= platform3.rect.y - 30:
            if (self.isJump == True and self.jvel <= -4) or self.isJump == False:
                self.xvel = platform3.vel
                self.jumpcount = 0
                self.yvel = 0
                self.square.y = (platform3.rect.y - self.square.height)
                self.touching_platform = True
        elif self.square.x + self.square.width >= platform4.rect.x and self.square.x <= platform4.rect.x + platform4.rect.width and self.square.y+self.square.height <= platform4.rect.y and self.square.y + self.square.height >= platform4.rect.y - 30:
            if (self.isJump == True and self.jvel <= -4) or self.isJump == False:
                self.xvel = platform4.vel
                self.jumpcount = 0
                self.yvel = 0
                self.square.y = (platform4.rect.y - self.square.height)
                self.touching_platform = True
        elif self.square.x + self.square.width >= platform5.rect.x and self.square.x <= platform5.rect.x + platform5.rect.width and self.square.y+self.square.height <= platform5.rect.y and self.square.y + self.square.height >= platform5.rect.y - 30:
            if (self.isJump == True and self.jvel <= -4) or self.isJump == False:
                self.xvel = platform5.vel
                self.jumpcount = 0
                self.yvel = 0
                self.square.y = (platform5.rect.y - self.square.height)
                self.touching_platform = True
        elif self.square.x + self.square.width >= platform6.rect.x and self.square.x <= platform6.rect.x + platform6.rect.width and self.square.y+self.square.height <= platform6.rect.y and self.square.y + self.square.height >= platform6.rect.y - 30:
            if (self.isJump == True and self.jvel <= -4) or self.isJump == False:
                self.xvel = platform6.vel 
                self.jumpcount = 0
                self.yvel = 0
                self.square.y = (platform6.rect.y - self.square.height)
                self.touching_platform = True
        else:
            self.xvel = 0
            self.yvel = 15
            self.touching_platform = False
    def shot(self, bullet):
        #This pushes the player back(depending on the xkb which is different depending on its owners gun type) and up a little (almost like a forced jump)
        if not self.isShield:
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
        else:
            self.ishit = False
    def upgraded(self, upgrade):
        #Depending on the powerId of the upgrade, the player is given a different power. 1-5 are buffs while 6-10 are debuffs. They match up in order 1-6, 2-7 etc.
        if upgrade.powerId == 1:
            #Speed up
            self.walkspeed = 15
        elif upgrade.powerId == 2:
            #Jump boost
            self.mass = 2
        elif upgrade.powerId == 3:
            #Extra life
            self.lives += 1
            upgrade_used_list.remove(upgrade)
        elif upgrade.powerId == 4:
            #Minimize
            # x
            self.square.width = 10
            self.square.height = 15
            self.image = pygame.transform.scale(self.image, (self.square.width, self.square.height))
            self.gun.width = 8
            self.gun.height = 6
            self.gun.image_left = pygame.transform.scale(self.gun.image_left, (self.gun.width, self.gun.height))
            self.gun.image_right = pygame.transform.scale(self.gun.image_right, (self.gun.width, self.gun.height))
            self.shield_width = 8
            self.shield_width = 14
            upgrade_used_list.remove(upgrade)
        elif upgrade.powerId == 5:
            self.isShield = True
        elif upgrade.powerId == 6:
            #Speed down
            self.walkspeed = 5
        elif upgrade.powerId == 7:
            #Jump debuff
            self.mass = .7
        elif upgrade.powerId == 8:
            #Lose a life
            self.lives -= 1
            upgrade_used_list.remove(upgrade)
        elif upgrade.powerId == 9:
            #Maximize
            self.square.width = 55
            self.square.height = 75
            self.image = pygame.transform.scale(self.image, (self.square.width, self.square.height))
            # x4 scale factor
            self.gun.width = 60
            self.gun.height = 45
            self.gun.image_left = pygame.transform.scale(self.gun.image_left, (self.gun.width, self.gun.height))
            self.gun.image_right = pygame.transform.scale(self.gun.image_right, (self.gun.width, self.gun.height))
            self.shield_width = 30
            self.shield_width = 50
    def remove_upgrade(self, upgrade):
        #The powerId of the upgrade is used to show what power it gave, and that power is reverted back to the original stats
        if upgrade.powerId == 1 or upgrade.powerId == 6:
            self.walkspeed = 10
        if upgrade.powerId == 2 or upgrade.powerId == 7:
            self.mass = 1
        if upgrade.powerId == 3 or upgrade.powerId == 8:
            self.lives = self.lives
        if upgrade.powerId == 4 or upgrade.powerId == 9:
            self.square.width = 25
            self.square.height = 45
            self.image = pygame.transform.scale(self.image, (self.square.width, self.square.height))
            self.gun.width = 20
            self.gun.height = 15
            self.gun.image_left = pygame.transform.scale(self.gun.image_left, (self.gun.width, self.gun.height))
            self.gun.image_right = pygame.transform.scale(self.gun.image_right, (self.gun.width, self.gun.height))
            self.shield_width = 19
            self.shield_width = 32
        if upgrade.powerId == 5:
            self.isShield = False


class Platform(object):
    def __init__(self,x,y,width,height,vel):
        self.rect = pygame.Rect(x,y,width,height)
        #If the platform is not supposed to move, .vel is set to 0
        self.vel = vel
    def moves(self):
        #This is for the moving platforms to make them move
        self.rect.x += self.vel
        if self.rect.x > 530:
            self.vel *= -1
        if self.rect.x < 0:
            self.vel *= -1

class Upgrade(object):
    def __init__(self, platform, gunbox_check):
        self.platform = platform
        #If it is a gunbox it is given different properties to behave differently
        if gunbox_check:
            self.touching_platform = False
            self.xvel = 0
            self.height = 30
            self.width = 30
            self.y = 100
            self.image = pygame.image.load("Images/Gunbox.png").convert_alpha()
        #If it is just a normal upgrade it gets these properties instead
        else:
            self.touching_platform = True
            self.height = 20
            self.width = 20
            self.y = platform.rect.y - self.height
            #Power id chooses what power the upgrade gives and gives it an image accordingly
            self.powerId = random.randint(1, 9)
            if self.powerId == 1:
                self.image = pygame.image.load("Images/speed_power.png").convert_alpha()
            elif self.powerId == 2:
                self.image = pygame.image.load("Images/mass_power.png").convert_alpha()
            elif self.powerId == 3:
                self.image = pygame.image.load("Images/extra_life.jpeg").convert_alpha()
            elif self.powerId == 4:
                self.image = pygame.image.load("Images/minimize_power.png").convert_alpha()
            elif self.powerId == 5:
                self.image = pygame.image.load("Images/shield_power.png").convert_alpha()
            elif self.powerId == 6:
                self.image = pygame.image.load("Images/speed_power.png").convert_alpha()
            elif self.powerId == 7:
                self.image = pygame.image.load("Images/mass_power.png").convert_alpha()
            elif self.powerId == 8:
                self.image = pygame.image.load("Images/extra_life.jpeg").convert_alpha()
            elif self.powerId == 9:
                self.image = pygame.image.load("Images/maximize_power.png").convert_alpha()
        #Makes it so the gunboxes and upgrades always spawn on/over a platform
        num1 = platform.rect.x
        num2 = (platform.rect.x + platform.rect.width)- self.width
        self.x = random.randint(num1, num2)
        self.yvel = 10
        #self.radius = 10
        #True means getting bigger while false means getting smaller
        #self.radius_change_state = True
        self.owner = None
        self.last = None
    def move(self):
        self.y += self.yvel
    def check_for_platform(self, platform1, platform2, platform3):
        #Detecs if upgrade is on platform or not(Platform Collision). If it is, the y coordinate of the upgrade is set to make the upgrade right on top of the platform, the upgrade is no longer affected by gravity and it is assigned that platform
        if self.x >= platform1.rect.x and self.x <= platform1.rect.x + platform1.rect.width and self.y + self.height <= platform1.rect.y and self.y + self.height>= platform1.rect.y - 45:
            self.yvel = 0
            self.y = (platform1.rect.y - self.height)
            self.platform = platform1
            self.touching_platform = True
        elif self.x >= platform2.rect.x and self.x <= platform2.rect.x + platform2.rect.width and self.y + self.height<= platform2.rect.y and self.y + self.height >= platform2.rect.y - 45:
            self.yvel = 0
            self.y = (platform2.rect.y - self.height)
            self.platform = platform2
            self.touching_platform = True
        elif self.x >= platform3.rect.x and self.x <= platform3.rect.x + platform3.rect.width and self.y + self.height <= platform3.rect.y and self.y + self.height >= platform3.rect.y - 45:
            self.yvel = 0
            self.y = (platform3.rect.y - self.height)
            self.platform = platform3
            self.touching_platform = True
    def choose_random_gun(self, player, gun_list):
            #Gives the player a random gun from a predefined gun list. However, player also has .maingun so when they run out of ammo it will revert back to their main gun
            random_gun_index = random.randint(0, 6)
            gun = gun_list[random_gun_index]
            gun.owner = player
            player.gun = gun
    #This function was for the circle, which was too anoyying and hard to do
    # def radius_change(self):
    #     #This gives the upgrades an effect of pulsing in and out
    #     if self.radius_change_state:
    #         self.radius += 0.5
    #     else:
    #         self.radius -= 0.5
    #     if self.radius <= 9:
    #         self.radius_change_state = True
    #     if self.radius >= 11:
    #         self.radius_change_state = False
    def platform_move(self):
        #Makes the upgrade move with the platform (if it is a moving platform)
        if self.touching_platform:
            self.x += self.platform.vel
    def outline_mask(self, color):
        #This gives the upgrade an outline to tell the user whether it is a buff or debuff
        mask = pygame.mask.from_surface(self.image)
        mask_outline = mask.outline()
        n = 0
        for point in mask_outline:
            mask_outline[n] = (point[0] + self.x, point[1] + self.y)
            n += 1
        outline_color = color
        pygame.draw.polygon(win, outline_color, mask_outline, 2)

        
#Creates start menu
create_start_menu()

def main():
    #Defining Images
    player1image = pygame.image.load("Images/Meowth-Pokemon-PNG-Transparent-Image.png").convert_alpha()
    player2image = pygame.image.load("Images/player2_image.png").convert_alpha()
    platform3image = pygame.image.load("Images/download.png").convert_alpha()
    #Main Gun
    maingun_image1 = maingun_image2 = pygame.image.load("Images/Main_Gun/Main_Gun.png").convert_alpha()
    maingun_image1_left = maingun_image2_left = pygame.image.load("Images/Main_Gun/Main_Gun_Left.png").convert_alpha()
    #Mini Gun
    minigun_image = pygame.image.load("Images/Mini_Gun/Mini_Gun.png").convert_alpha()
    minigun_image_left = pygame.image.load("Images/Mini_Gun/Mini_Gun_Left.png").convert_alpha()
    #Sub Machine Gun
    submachinegun_image = pygame.image.load("Images/Sub_Machine_Gun/Sub_Machine_Gun.png").convert_alpha()
    submachinegun_image_left = pygame.image.load("Images/Sub_Machine_Gun/Sub_Machine_Gun_Left.png").convert_alpha()
    #Shotgun
    shotgun_image = pygame.image.load("Images/Shotgun/Shotgun.png").convert_alpha()
    shotgun_image_left = pygame.image.load("Images/Shotgun/Shotgun_Left.png").convert_alpha()
    #Assault Rifle
    assault_rifle_image = pygame.image.load("Images/Assault_Rifle/Assault_Rifle.png").convert_alpha()
    assault_rifle_image_left = pygame.image.load("Images/Assault_Rifle/Assault_Rifle_Left.png").convert_alpha()
    #Dematerializer
    dematerializer_image = pygame.image.load("Images/Dematerializer/Dematerializer.png").convert_alpha()
    dematerializer_image_left = pygame.image.load("Images/Dematerializer/Dematerializer_Left.png").convert_alpha()
    #Shield
    player1_shield = player2_shield = pygame.image.load("Images/shield.png").convert_alpha()
    #Order goes as follows: x, y, width, height, vel
    #Creates all of the objects
    platform1 = Platform(0,450,70,10, 5)
    platform2 = Platform(530,450,70,10, -5)
    platform3 = Platform(150,400,300,10,0)
    platform4 = Platform(20,350,100,10,0)
    platform5 = Platform(500,350,100,10,0)
    platform6 = Platform(150,300,300,10,0)

    #Order goes as follows: x,y,width,height,yvel,xvel, mass, jvel, player_num, lives, image
    player1 = Player(300,100,25,45,10,0,1,8, 1, 10, player1image)
    player2 = Player(300,100,25,45,10,0,1,8, 2, 10, player2image)

    #Order goes as follows: name, owner, ammo, cooldown, bullet_kb, gunid, image_left, image_right
    maingun_image1_left = pygame.transform.scale(maingun_image1_left, (20,15))
    maingun_image1 = pygame.transform.scale(maingun_image1, (20,15))
    maingun1 = Gun("pistol",player1, 10, 400, 18, 0, maingun_image1_left, maingun_image1)
    player1.maingun = maingun1
    player1.gun = maingun1
    maingun_image2_left = pygame.transform.scale(maingun_image2_left, (20,15))
    maingun_image2 = pygame.transform.scale(maingun_image2, (20,15))
    maingun2 = Gun("pistol",player2, 10, 400, 18, 0, maingun_image2_left, maingun_image2)
    player2.maingun = maingun2
    player2.gun = maingun2

    #Gun List:
    #Order goes as follows: name, owner, ammo, cooldown, bullet_kb, gunid, image
    #For now, the special guns take the image of the maingun
    gun_1 = Gun("Sub machine gun",None, 50, 200, 25, 1, submachinegun_image_left, submachinegun_image)#Sub machine gun
    gun_2 = Gun("Sniper",None, 5, 500, 35, 1, maingun_image1_left, maingun_image1)#Sniper
    gun_3 = Gun("Shotgun",None, 5, 500, 35, 1, shotgun_image_left, shotgun_image)#Shotgun
    gun_4 = Gun("Assault rifle",None, 30, 250, 25, 1, assault_rifle_image_left, assault_rifle_image)#Assault rifle
    gun_5 = Gun("Light machine gun",None, 50, 200, 25, 1, maingun_image1_left, maingun_image1)#Light machine gun
    #Special
    gun_6 = Gun("Minigun",None, 100, 100, 25, 1, minigun_image_left, minigun_image)#Minigun
    gun_7 = Gun("Dematerializer",player1, 1, 750, 50, 1, dematerializer_image_left, dematerializer_image)#Dematerializer
    #Gun_list stores all the special guns that arrive in lootboxes
    gun_list = [gun_1, gun_2, gun_3, gun_4, gun_5, gun_6, gun_7]
    #Makes all of the images fit their objects
    player1.image = pygame.transform.scale(player1.image, (player1.square.width, player1.square.height))
    player2.image = pygame.transform.scale(player2.image, (player2.square.width, player2.square.height))
    platform3image = pygame.transform.scale(platform3image, (platform3.rect.width, platform3.rect.height))
    
    TOD = "dawn"
    #Code for upgrade timer
    upgrade_last = pygame.time.get_ticks()
    #Code for gunbox timer
    gunbox_last = pygame.time.get_ticks()
    #Time for day/night timer
    last = 0
    current_color = [255, 127, 150]
    goal_color = [138, 206, 251]

    #Main
    run = True
    while run:
        pygame.time.delay(100)
        #To let the user quit the window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run=False
        #Gets all the key inputs
        keys = pygame.key.get_pressed()
        now = pygame.time.get_ticks()
        #A full day lasts about 142 seconds
        #Time of day: dawn
        if TOD == "dawn":
            #Lasts 10 seconds
            if now - last >= 10000:
                TOD = "day"
                last = pygame.time.get_ticks()
                #Goal color(set to dusk)
                goal_color = [245, 129, 56]
            elif now - last >= 3000:
                #Function that changes the background color ever so slightly every tick
                current_color = change_colors(current_color, goal_color, 70)
            else: 
                current_color = current_color
        #Time of day: day(8:00am - 5:00pm)
        elif TOD == "day":
            #Lasts 60 seconds
            if now - last >= 60000:
                TOD = "dusk"
                last = pygame.time.get_ticks()
                #Goal color(set to night)
                goal_color = [0, 0, 0]
            elif now - last >= 55000:
                current_color = change_colors(current_color, goal_color, 50)
            else:
                current_color = current_color
        #Time of day: dusk
        elif TOD == "dusk":
            #Lasts 12 seconds
            if now - last >= 12000:
                TOD = "night"
                last = pygame.time.get_ticks()
                #Goal color(set to dawn)
                goal_color = [255, 127, 150]
            elif now - last >= 4000:
                current_color = change_colors(current_color, goal_color, 80)
            else:
                current_color = current_color
        #Time of day: night(6:00pm - 5:00am)
        elif TOD =="night":
            #Lasts 60 seconds
            if now - last >= 60000:
                TOD = "dawn"
                last = pygame.time.get_ticks()
                #Goal color(set to day)
                goal_color = [138, 206, 251]
            elif now - last >= 55000:
                current_color = change_colors(current_color, goal_color, 50)
            else:
                current_color = current_color
        #Makes the background and all of the objects
        win.fill(tuple(current_color))
        #This is the function that redraws all of the stuff in the game
        # Draws the platforms
        pygame.draw.rect(win,color_dict["red"],platform1.rect)
        pygame.draw.rect(win,color_dict["red"],platform2.rect)
        pygame.draw.rect(win,color_dict['red'],platform3.rect)
        pygame.draw.rect(win,color_dict["red"],platform4.rect)
        pygame.draw.rect(win,color_dict["red"],platform5.rect)
        pygame.draw.rect(win,color_dict['red'],platform6.rect)
        #font for the text boxes
        font = pygame.font.SysFont("comicsansms", 14)
        #Rectangle that surrounds the player 1 text
        pygame.draw.rect(win, color_dict["cardboard_brown"],(0, 550, 300, 50))
        #Player 1 text box
        text_in_box1_list = ["Player 1:", f"Lives: {player1.lives}  Gun: {player1.gun.name}  Ammo: {player1.gun.ammo}"]
        text_height_var1 = 65
        #Makes it so that there are multiple lines of text rather than one big line
        for line in text_in_box1_list:
            text1 = font.render(line, True, color_dict["olive_green"], color_dict["white"])
            textRect1 = text1.get_rect()
            textRect1.center = (150, 500+ text_height_var1)
            win.blit(text1, textRect1)
            text_height_var1 += 20
        #Rectangle that surrounds the player 1 text
        pygame.draw.rect(win, color_dict["green"],(300, 550, 300, 50))
        #Player 2 text box
        text_in_box2_list = ["Player 2:", f"Lives: {player2.lives}  Gun: {player2.gun.name}  Ammo: {player2.gun.ammo}"]
        text_height_var2 = 65
        #Makes it so that there are multiple lines of text rather than one big line
        for line in text_in_box2_list:
            text2 = font.render(line, True, color_dict["coral"], color_dict["white"])
            textRect2 = text2.get_rect()
            textRect2.center = (450, 500+ text_height_var2)
            win.blit(text2, textRect2)
            text_height_var2 += 20
        #Blit the images (not in update_window because of referenced before assignment errors)
        win.blit(platform3image, (platform3.rect.x, platform3.rect.y))
        win.blit(player1.image, (player1.square.x, player1.square.y))
        win.blit(player2.image, (player2.square.x, player2.square.y))
        if player1.isShield:
            player1_shield = pygame.transform.scale(player1_shield, (player1.shield_width, player1.shield_height))
            win.blit(player1_shield, (player1.square.x - 17 ,player1.square.y - 7))
        if player2.isShield:
            player2_shield = pygame.transform.scale(player2_shield, (player2.shield_width, player2.shield_height))
            win.blit(player2_shield, (player2.square.x - 17 ,player2.square.y - 7))
        player1.gun.image_update()
        player2.gun.image_update()
        #Makes the platforms move
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
            if player1.lives <= 0:
                run = False
                winScreen(player2)
            for upgrade in upgrade_used_list:
                if upgrade.owner == player1:
                    upgrade_used_list.remove(upgrade)
        if player2.square.y > 600:
            player2.respawn()
            if player2.lives <= 0:
                run = False
                winScreen(player1)
            for upgrade in upgrade_used_list:
                if upgrade.owner == player2:
                    upgrade_used_list.remove(upgrade)
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
        if now - upgrade_last >= 20000:
            upgrade_last = now
            if len(upgrade_list) < 2:
                randchance = random.randint(1,2)
                if randchance == 1:
                    upgrade_platform = random.randint(1, 6)
                    if upgrade_platform == 1:
                        upgrade = Upgrade(platform1, False)
                    elif upgrade_platform == 2:
                        upgrade = Upgrade(platform2, False)
                    elif upgrade_platform == 3:
                        upgrade = Upgrade(platform3, False)
                    elif upgrade_platform == 4:
                        upgrade = Upgrade(platform4, False)
                    elif upgrade_platform == 5:
                        upgrade = Upgrade(platform5, False)
                    elif upgrade_platform == 6:
                        upgrade = Upgrade(platform6, False)
                    upgrade_list.append(upgrade)
        for upgrade in upgrade_list:
            upgrade.platform_move()
            upgrade.image = pygame.transform.scale(upgrade.image, (upgrade.width, upgrade.height))
            win.blit(upgrade.image, (upgrade.x, upgrade.y))
            if upgrade.powerId <= 5:
                upgrade.outline_mask(color_dict["green"])
            else:
                upgrade.outline_mask(color_dict["red"])
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
            for upgrade2 in upgrade_used_list:
                if (upgrade.powerId == upgrade2.powerId + 5) or (upgrade2.powerId == upgrade.powerId + 5):
                    upgrade_used_list.remove(upgrade)
                    upgrade_used_list.remove(upgrade2)
            upgrade.owner.upgraded(upgrade)
            if now - upgrade.last >= 10000:
                upgrade.owner.remove_upgrade(upgrade)
                upgrade_used_list.remove(upgrade)
        #Gunbox code
        if now - gunbox_last >= 30000:
            gunbox_last = now
            gunbox_platform = random.randint(1, 6)
            if gunbox_platform == 1:
                gunbox = Upgrade(platform1, True)
            elif gunbox_platform == 2:
                gunbox = Upgrade(platform2, True)
            elif gunbox_platform == 3:
                gunbox = Upgrade(platform3, True)
            elif gunbox_platform == 4:
                gunbox = Upgrade(platform4, True)
            elif gunbox_platform == 5:
                gunbox = Upgrade(platform5, True)
            elif gunbox_platform == 6:
                gunbox = Upgrade(platform6, True)
            gunbox_list.append(gunbox)
            if len(gunbox_list) >= 3:
                gunbox_list.remove(gunbox_list[0])
        for gunbox in gunbox_list:
            gunbox.check_for_platform(platform1, platform2, platform3)
            gunbox.check_for_platform(platform4, platform5, platform6)
            gunbox.move()
            if gunbox.platform != None:
                gunbox.platform_move()
            gunbox.image = pygame.transform.scale(gunbox.image, (gunbox.width, gunbox.height))
            win.blit(gunbox.image, (gunbox.x, gunbox.y))
            if (gunbox.x<=player1.square.x+player1.square.width) and (gunbox.x + gunbox.width >= player1.square.x) and (gunbox.y <= player1.square.y+ player1.square.height) and (gunbox.y + gunbox.width >= player1.square.y):
                gunbox.choose_random_gun(player1, gun_list)
                gunbox_list.remove(gunbox)
            elif (gunbox.x<=player2.square.x+player2.square.width) and (gunbox.x + gunbox.width >= player2.square.x) and (gunbox.y <= player2.square.y+ player2.square.height) and (gunbox.y + gunbox.width >= player2.square.y):
                gunbox.choose_random_gun(player2, gun_list)
                gunbox_list.remove(gunbox)
        pygame.display.update()
    pygame.quit()

def winScreen(player):
    run = True
    while run:
        win.fill(color_dict["sky_blue"])
        #To let the user quit the window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False
        #Title
        winner_font = pygame.font.SysFont("timesnewroman", 45)
        if player.player_num == 1:
            winnerText = "Winner: Player 1"
        else:
            winnerText = "Winner: Player 2"
        winnerRender = winner_font.render(winnerText, True, color_dict["deep_green"])
        winnerRect = winnerRender.get_rect()
        winnerRect.center = (175, 75)
        win.blit(winnerRender, winnerRect.center)
        #Button
        start_font = pygame.font.SysFont("timesnewroman", 30)
        startRender = start_font.render("Left-click to play again", True, color_dict["olive_green"])
        startRect = startRender.get_rect()
        startRect.center = (200, 450)
        win.blit(startRender, startRect.center)
        pygame.display.update()
    fade_to_black(color_dict["sky_blue"], color_dict["coral"])
    main()
main()