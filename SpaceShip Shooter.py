import pygame
import time
import random
import os

pygame.init()

dw = 1280
dh = 700

white = (255,255,255)
black = (0,0,0)
red = (200,0,0)
green = (0,200,0)
bright_red = (255,0,0)

clock = pygame.time.Clock()
gameWindow = pygame.display.set_mode((dw, dh))


'''
    All the parameters with the names as follows:

    p  stands for   Player
    pnt    for     Planet
    bgd    for     BackGround
'''
#Music files ----------------
pygame.mixer.music.load("data\\Music\\loop.mp3")
hit = pygame.mixer.Sound("data\\Music\\wav\\hurt.wav")
closing = pygame.mixer.Sound("data\\Music\\wav\\quit.wav")
gameOver = pygame.mixer.Sound("data\\Music\\wav\\game_over.wav")



#BackGround -------------

bg = pygame.transform.scale(pygame.image.load(os.path.join("data\\Images", "space bg.jpg")), (dw, dh))

#Player Ship -----------

ship = pygame.transform.scale(pygame.image.load(os.path.join("data\\Images", "spaceship.png")), (64, 64))

#Bullet ---------------

bullet = pygame.transform.scale(pygame.image.load(os.path.join("data\\Images", "shoot.png")), (24,35))
bullet_speed = 10
enemy_bullet = pygame.image.load('data\\Images\\enemy_shoot.png')

#Icon --------------

icon = pygame.image.load("data\\Images\\spaceship_icon.png")

#Enemies ------------------

ig = "data\\Images\\ufo_{}.png"
ufo = [pygame.image.load(ig.format(1)), pygame.image.load(ig.format(2)), pygame.image.load(ig.format(3))]

#Exhaustion COLOR ---------------------

Effects = []
file_path = os.getcwd() + "\\data\\Images\\Flight effects\\"
for path , subfolders , files in os.walk(file_path):
    effect = []
    for file in files:
        effect.append(pygame.image.load(os.path.join(path, file)))
    Effects.append(effect)

#PLANETS --------------
    
file_path = os.getcwd() + "\\data\\Images\\Planet"
Planets = [pygame.image.load(os.path.join(file_path, x)) for x in os.listdir(file_path)]


pygame.display.set_caption("SpaceShip Shooter")
pygame.display.set_icon(icon)


#MAKING -------------------- 0. Bullets

class Bullets:
    def __init__(self, x ,y ,speed, img = bullet):
        self.x = x
        self.y = y
        self.speed = speed
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)
    def draw(self):
        gameWindow.blit(self.img , (self.x, self.y))
    def move(self):
        self.draw()
        self.y += self.speed
        if self.y > dh or self.y < 0:
            return False
        return True

    

#MAKING ------------------ 1. Player

class Player:
    def __init__(self, x, y, health = 100, effects = [x for x in random.choices(Effects[1:])]):
        self.x = x
        self.y = y
        self.planet_count = 3
        self.enemy_count = 4
        self.health = health
        self.vel = 5
        self.img = ship
        self.cooldown = 30
        self.x_change = 0
        self.y_change = 0
        self.effect_cooldown = 4
        self.standing = True
        self.effects = effects
        self.effects_count = 5
        self.low_health = False
        self.low_health_cooldown = 20
        self.player_upgrade = 1500
        self.mask = pygame.mask.from_surface(self.img)
    def draw(self):
        gameWindow.blit(self.img, (self.x, self.y))
        if self.standing:
            self.draw_effects()

        if self.cooldown < 30:
            self.cooldown += 1
    def shoot(self, bullets):
        if self.cooldown == 30:
            Bullet = Bullets(self.x + 18, self.y - 20, -bullet_speed)
            bullets.append(Bullet)
            self.cooldown = 0
    def collide(self, bullet, enemies):
        for enemy in enemies:
            if collision(bullet, enemy):
                enemies.remove(enemy)
                return True
        return False;
    def draw_effects(self, num = 4):        
        gameWindow.blit(self.effects[0][num], (self.x + self.img.get_width() // 2 - self.effects[0][num].get_width() // 2, self.y + self.img.get_height()))
         
    def check_effects(self):
        if self.effects_count == 0:
            self.draw_effects(0)
            self.effect_cooldown = 0

        if self.effects_count < 4:
            self.draw_effects(self.effects_count)
            if self.effect_cooldown < 4:
                self.effect_cooldown += 1
            else:
                self.effects_count += 1
                self.effect_cooldown = 0
    def health_bar(self):        
        if self.low_health and 10 < self.low_health_cooldown < 20:
            pygame.draw.rect(gameWindow, bright_red,(25,4,101,10))
            self.low_health_cooldown += 1                
        else:
            pygame.draw.rect(gameWindow, red, (25,4,101,10))
            if self.low_health and self.low_health_cooldown < 11:
                self.low_health_cooldown += 1
            else:
                self.low_health_cooldown = 0
            
        pygame.draw.rect(gameWindow, green, (25,4,self.health, 10))
    def check_health_condition(self):
        if self.health < 30 and not self.low_health:
            self.low_health = True
            self.low_health_cooldown = 0       






#MAKING --------------------- 2. Enemy
        
class Enemy:
    def __init__(self, x, y, img):
        self.x = x if x < dw - int(img.get_width()) else dw - int(img.get_width())
        self.y = y
        self.img = img
        self.vel = 1
        self.ammo = []
        self.timer = 360
        self.mask = pygame.mask.from_surface(self.img)
    def move(self):
        gameWindow.blit(self.img, (self.x, self.y))
        self.y += self.vel
    def shoot(self, speed, img):
        Bullet = Bullets(self.x + 20, self.y + 15, speed, img)
        self.ammo.append(Bullet)

        


#MAKING ----------------------- 3. BackGround
        
class BackG:
    def __init__(self):
        self.img = bg
        self.y = 0
        self.vel = 1/2
        self.score = 0
        self.score_cooldown = 0
        self.difficulty = 500
    def draw(self):
        gameWindow.blit(self.img, (0, self.y))
        self.y += self.vel
        if (self.y > 0):
            gameWindow.blit(self.img, (0, self.y - int(self.img.get_height())))
        if (self.y > self.img.get_height()):
            self.y = 0;
    def draw_score(self):
        font = pygame.font.SysFont("comicsansms", 20)
        text = font.render("Score : " + str(self.score), 1, white)
        self.update_score()
        gameWindow.blit(text, (dw - text.get_width() - 2, 0))
    def update_score(self):
        if self.score_cooldown < 20:
            self.score_cooldown += 1
        else:
            self.score += 1
            self.score_cooldown = 0



            
        

#MAKING --------------------------- 4. Planet
            
class Planet:
    def __init__(self, x, y, img):
        self.img = img
        self.x = x if x < dw - img.get_width() else x - img.get_width()
        self.y = y       
        if (self.img.get_width() > 400 and self.img.get_height() > 350):
            self.img = pygame.transform.scale(self.img, (200, 100))
        self.vel = 1/2
    def move(self):        
        gameWindow.blit(self.img, (self.x, self.y))
        self.y += self.vel





#MAKING ---------------------------- 5. Text
        
class Text:
    def __init__(self, x, y, msg, size):
        self.x = x
        self.y = y
        self.msg = msg
        self.font = pygame.font.SysFont("comicsansms",size)
        self.size = size
        self.text = self.font.render(self.msg, 1, white)
        self.hover_size = 25
    def draw(self):
        gameWindow.blit(self.text, (self.x, self.y))
    def IsHovering(self):
        font = pygame.font.SysFont("comicsansms", self.size + self.hover_size)
        text = font.render(self.msg, 1, white)
        gameWindow.blit(text, (self.x, self.y))



        

#CHECKING ------------------------------- 6. All the main events
        
def event(p, pnt, enemies, bullets):
    if (p.health == 0):
        game_over()
    if len(pnt) < p.planet_count - 1:
        for i in range(p.planet_count):
            planet = Planet( random.randint(-10, dw - 10) + 10, random.randrange(-1000, -200), random.choice(Planets))
            pnt.append(planet)

    if len(enemies) < p.enemy_count:
        for i in range(p.enemy_count):
            enemy = Enemy(random.randint(-10, dw - 10) + 10, random.randrange(-500, 0), random.choice(ufo))
            enemy.vel += min(enemy_speed_addition, 3)
            enemies.append(enemy)
            
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                p.effects_count = 0
                p.standing = False
                p.y_change = -p.vel
                if event.key == pygame.K_a:
                    p.x_change = - p.vel
                if event.key == pygame.K_d:
                    p.x_change = p.vel
            if event.key == pygame.K_s:
                p.standing = False
                p.y_change = p.vel
                if event.key == pygame.K_a:
                    p.x_change = - p.vel
                if event.key == pygame.K_d:
                    p.x_change = p.vel
            if event.key == pygame.K_a:
                p.x_change = -p.vel
            if event.key == pygame.K_d:
                p.x_change = p.vel
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_d:
                p.x_change = 0
            if event.key == pygame.K_w:
                p.standing = True
                p.y_change = 0
                p.effects_count = 1
            if event.key == pygame.K_s:
                p.y_change = 0
                p.standing = True
    keys = pygame.key.get_pressed()
    if (keys[pygame.K_SPACE] or keys[pygame.K_j]):
        p.shoot(bullets)
    if (keys[pygame.K_p]):
        paused(True)
    p.x += p.x_change
    p.y += p.y_change
    if p.x + p.img.get_width() > dw:
        p.x = dw - p.img.get_width()
    if p.x < 0:
        p.x = 0
    if p.y + p.img.get_height() > dh:
        p.y = dh - p.img.get_height()
    if p.y < 0:
        p.y = 0


        



#   --------------------------------- 7. Drawing on Screen Mains

    
def draw(p, bgd, pnt, enemies, bullets):
    global bullet, enemy_speed_addition
    bgd.draw()
    
    
    if (bgd.score >= bgd.difficulty):
        bgd.difficulty *= 2
        p.enemy_count += 2
    if (bgd.score >= p.player_upgrade):
        p.health = 100
        p.vel = p.vel + 1 if p.vel != 8 else 8;
        enemy_speed_addition +=1
        p.player_upgrade *= 2

    
    for planet in pnt:
        planet.move()
        if planet.y > dh:
            pnt.remove(planet)
    for enemy in enemies:
        if random.randrange(0, enemy.timer) == 1:
            enemy.shoot(bullet_speed,enemy_bullet)

        for Bullet in enemy.ammo:
            
            Bullet.move()
            if collision(Bullet, p):
                pygame.mixer.Sound.play(hit)
                enemy.ammo.remove(Bullet)
                p.health -= 10
                
        if (collision(p, enemy)):
            pygame.mixer.Sound.play(hit)
            enemies.remove(enemy)
            p.health -= 10
        enemy.move()
            
        if enemy.y > dh:
            enemies.remove(enemy)
    p.check_health_condition()
    for bullet in bullets:
        if bullet.move():
            if p.collide(bullet, enemies):
                bullets.remove(bullet)
                bgd.score += 20
        else:
            bullets.remove(bullet)
        
    p.draw()
    p.check_effects()
    Health = Text (0, 0, "HP", 15)
    Health.draw()
    p.health_bar()
    bgd.draw_score()
    pygame.display.update()





# CHECKING ----------------------------- 8. Mouse Inputs

def buttons(x, y, msg, size):
    global pause
    mouse_pos = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()
    text = Text(x, y, msg, size)
    if x < mouse_pos[0] < x + text.text.get_width() and y < mouse_pos[1] < y + text.text.get_height():
        text.IsHovering()
        if (mouse_click[0] == 1):
            if msg == "Try Again":
                pygame.mixer.Sound.stop(gameOver)
                pygame.mixer.music.play()
                game()
            elif msg == "Play":
                controls()
                game()
            elif msg == "Continue":
                pause = False
                return
            else:
                pygame.mixer.music.stop()
                pygame.mixer.Sound.play(closing)
                time.sleep(3)
                pygame.quit()
                quit()
    else:
        text.draw()



        


#CHECKING ------------------------------ 9. Collisions (PIXEL PERFECT)
                
def collision(player, enemy):
    offset_x = enemy.x - player.x
    offset_y = enemy.y - player.y
    return player.mask.overlap(enemy.mask, (int(offset_x), int(offset_y))) != None




# ----------------------------------------10. Pause menu
pause = False
def paused(condition):
    global pause
    pause = condition
    pygame.mixer.music.pause()
    while(pause):
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameWindow.blit(bg, (0,0))

        pause_text = Text(dw//2, dh//2 - 80 , "PAUSED", 100)
        pause_text.x = pause_text.x - pause_text.text.get_width() // 2
        pause_text.draw()
        
        buttons(dw // 2 - 350, dh // 2 + 120, "Continue", 60)
        buttons(dw // 2 + 280, dh // 2 + 120, "Quit", 60)

        pygame.display.update()
    pygame.mixer.music.unpause()

        


# ------------------------------------------- 11. Controls
def controls():
    gameWindow.blit(bg, (0,0))

    controls = Text(dw // 2, dh // 2 - 300, "CONTROLS", 100)
    controls.x = controls.x - controls.text.get_width() // 2
    controls.draw()
    
    actions_1 = Text(dw // 2 - 400, dh // 2 - 50, "Press W,S,A,D to Move", 70)
    actions_1.draw()

    actions_2 = Text(dw // 2 - 400, dh // 2 + 150, "Press SPACE to Shoot", 70)
    actions_2.draw()

    pygame.display.flip()
    time.sleep(3)





#Main menu start --------------------------------------------------------->>>>
def main():
    run = True
    pygame.mixer.music.play(-1)
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        gameWindow.blit(bg, (0,0))

        game_name = Text(dw // 2, dh // 2 - 200, 'SpaceShip', 95)
        game_name.x = game_name.x - game_name.text.get_width() // 2
        game_name.draw()
        game_name = Text(dw // 2, dh // 2 - 100, 'Shooter', 95)
        game_name.x = game_name.x - game_name.text.get_width() // 2
        game_name.draw()
                
        buttons(dw // 2 - 350, dh // 2 + 120, "Play", 60)
        buttons(dw // 2 + 280, dh // 2 + 120, "Quit", 60)

        pygame.display.update()
        
    pygame.quit()
    quit()


enemy_speed_addition = 0

def game():
    run = True
    player = Player(dw // 2, dh - ship.get_height() - 10)
    planet = []
    enemies = []
    bullets = []
    back_image = BackG()
    
    while run:
        clock.tick(60)
        event(player, planet, enemies, bullets)
        draw(player, back_image, planet, enemies, bullets)


## ------------------------------------------     GAME OVER ------------------------------------------>>

def game_over():
    run = True;
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(gameOver)
    text = Text(dw // 2, dh // 2 - 80, "GAME OVER", 95)
    text.x = text.x - text.text.get_width() // 2
    text.draw()
    pygame.display.update()
    time.sleep(3)
    while run :
        clock.tick(15)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit();
                quit()
        gameWindow.blit(bg, (0,0))
        text.draw()


        buttons(dw // 2 - 450, dh // 2 + 120, "Try Again", 60)
        buttons(dw // 2 + 280, dh // 2 + 120, "Quit", 60)

        pygame.display.update()
        

        
main()

