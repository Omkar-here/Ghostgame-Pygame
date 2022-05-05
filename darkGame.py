import pygame
import os
import random
import time
from pygame import mixer
pygame.init()

# Global Constants
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 800
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
#Loading images
score_img=pygame.image.load(os.path.join("Assets/Darkgame", "score_img.png"))
score_img=pygame.transform.scale(score_img,(200,200))
new_ghost=pygame.image.load(os.path.join("Assets/obghost", "ghost.png"))
new_ghost = pygame.transform.scale(new_ghost,(70,70))
ghost=pygame.image.load(os.path.join("Assets/Darkgame", "ghostgame.jpeg"))
ghost=pygame.transform.scale(ghost,(50,50))
obghost = pygame.image.load(os.path.join("Assets/obghost", "obghost.jpg"))
obghost = pygame.transform.scale(obghost,(70,70))
bigghost = pygame.image.load(os.path.join("Assets/bigghost", "bigghost.jpg"))
bigghost = pygame.transform.scale(bigghost,(80,80))
RUNNING = [ghost,
           ghost]
JUMPING = ghost
DUCKING = [ghost,
           ghost]

SMALL_GHOST = [ obghost,obghost,obghost ,new_ghost               
                ]
LARGE_GHOST = [bigghost,bigghost,bigghost,new_ghost]



CLOUD = pygame.image.load(os.path.join("Assets/Other", "Cloud.png"))

BG = pygame.image.load(os.path.join("Assets/Other", "Track.png"))

ghost_BACKGROUND = pygame.image.load(os.path.join("Assets/Darkgame","darkgame.jpeg"))
ghost_BACKGROUND = pygame.transform.scale(ghost_BACKGROUND,(SCREEN_WIDTH,SCREEN_HEIGHT))

class ghostsaur:
    X_POS = 80
    Y_POS = 400
    Y_POS_DUCK = 400
    JUMP_VEL = 8.5

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.ghost_duck = False
        self.ghost_run = True
        self.ghost_jump = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.ghost_rect = self.image.get_rect()
        self.ghost_rect.x = self.X_POS
        self.ghost_rect.y = self.Y_POS

    def update(self, userInput):
        if self.ghost_duck:
            self.duck()
        if self.ghost_run:
            self.run()
        if self.ghost_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0

        if userInput[pygame.K_UP] and not self.ghost_jump:
            self.ghost_duck = False
            self.ghost_run = False
            self.ghost_jump = True
            bulletSound = mixer.Sound("laser.wav")
            bulletSound.play()
        elif userInput[pygame.K_DOWN] and not self.ghost_jump:
            self.ghost_duck = True
            self.ghost_run = False
            self.ghost_jump = False
            bulletSound = mixer.Sound("laser.wav")
            bulletSound.play()
        elif not (self.ghost_jump or userInput[pygame.K_DOWN]):
            self.ghost_duck = False
            self.ghost_run = True
            self.ghost_jump = False

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.ghost_rect = self.image.get_rect()
        self.ghost_rect.x = self.X_POS
        self.ghost_rect.y = self.Y_POS_DUCK
        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.ghost_rect = self.image.get_rect()
        self.ghost_rect.x = self.X_POS
        self.ghost_rect.y = self.Y_POS
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.ghost_jump:
            self.ghost_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < - self.JUMP_VEL:
            self.ghost_jump = False
            self.jump_vel = self.JUMP_VEL

    def draw(self, SCREEN):
        SCREEN.blit(ghost_BACKGROUND, (0,0))
        SCREEN.blit(self.image, (self.ghost_rect.x, self.ghost_rect.y))
        


class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))


class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)


class Smallghost(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 3)
        super().__init__(image, self.type)
        self.rect.y = 400


class Largeghost(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 3)
        super().__init__(image, self.type)
        self.rect.y = 400





def main():
    
    mixer.music.load("scifi.mpeg")
    mixer.music.play()
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles
    run = True
    clock = pygame.time.Clock()
    player = ghostsaur()
    cloud = Cloud()
    game_speed = 20
    x_pos_bg = 0
    y_pos_bg = 430
    points = 0
    font = pygame.font.Font('freesansbold.ttf', 20)
    obstacles = []
    death_count = 0

    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 1

        text = font.render("Points: " + str(points), True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (1000, 40)
        SCREEN.blit(text, textRect)

    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
    #Starting condition
    while run:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        SCREEN.fill((255, 255, 255))
        userInput = pygame.key.get_pressed()

        player.draw(SCREEN)
        player.update(userInput)
    #If no obstacles
        if len(obstacles) == 0:
            if random.randint(0, 2) == 0:
                obstacles.append(Smallghost(SMALL_GHOST))
            elif random.randint(0, 2) == 1:
                obstacles.append(Largeghost(LARGE_GHOST))
        for obstacle in obstacles:
            
            obstacle.draw(SCREEN)
            obstacle.update()
            #if player collides with obstacle
            if player.ghost_rect.colliderect(obstacle.rect):
                #pygame.time.delay(2000)
                death_count += 1
                mixer.music.load("blip.wav")
                mixer.music.play()
                pygame.time.delay(1500)
                mixer.music.stop()
                menu(death_count)
        
        background()

        cloud.draw(SCREEN)
        cloud.update()

        score()

        clock.tick(30)
        pygame.display.update()


def menu(death_count):
    global points
    run = True

    while run:
        SCREEN.fill((255, 255, 255))
        font = pygame.font.Font('freesansbold.ttf', 30)
        #For the first time
        if death_count == 0:
            text = font.render("Press any Key to Start", True, (0, 0, 0))
        #After the first game
        elif death_count > 0:
            mixer.music.stop()
            
            text = font.render("Press any Key to Restart", True, (0, 0, 0))
            score = font.render("Your Score: " + str(points), True, (0, 0, 0))
            scoreRect = score.get_rect()
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 190)
            SCREEN.blit(score, scoreRect)
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2+140)
        SCREEN.blit(text, textRect)
        SCREEN.blit(score_img, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2-150 ))
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main()


menu(death_count=0)
