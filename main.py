
import os
import pygame
import random
from player import Player
from opponent import Enemy
from tilemap import TileMap

#Colors & Fonts
BLACK   = (0, 0, 0)
WHITE   = (255, 255, 255)
RED     = (255, 0, 0)
LIME    = (0, 255, 0)
BLUE    = (0, 0, 255)
YELLOW  = (255, 255, 0)
CYAN    = (0, 255, 255)
MAGENTA = (255, 0, 255)
SILVER  = (192, 192, 192)
GRAY    = (128, 128, 128)
MAROON  = (128, 0, 0)
OLIVE   = (128, 128, 0)
GREEN   = (0, 128, 0)
PURPLE  = (128, 0, 128)
TEAL    = (0, 128, 128)
NAVY    = (0, 0, 128)
ORANGE = (255, 165, 0)






pygame.init()
global screen
screen = pygame.display.set_mode((1152, 768))

player = Player() # create an instance
enemy = Enemy()
clock = pygame.time.Clock()
world = TileMap(os.path.join("assets", "maps", "startMap.tmj"))


transparentSurface = pygame.Surface((1152, 768), pygame.SRCALPHA)

lightsFlicker_Event = pygame.event.custom_type()
lightsOn = False
flashInterval = random.randint(120,150)
flashDuration = 2000
flickerActive = False
lastFlash = 0
flashStart = lastFlash

cameraSurface = pygame.Surface((1152,768))
shakeAmp = 0

def cameraShake(duration = 4000, magnitude = 4):
    print("Somethings comin")


def flashLights(currentTime):
    global lastFlash, flashOn, flashStart, lightsOn

    if lightsOn == False:
        print("lights off")
        # stop after duration
        if currentTime - flashStart > flashDuration:
            lightsOn = True
            flashOn = False

        else:
                # toggle on/off
            if currentTime - lastFlash >= flashInterval:
                #print(currentTime)
                #print(flashInterval)
                #print(flashDuration)
                flashOn = not flashOn
                lastFlash = currentTime

        if flashOn:
            transparentSurface.fill((0,0,0,128))
            screen.blit(transparentSurface,(0,0))     
        

def game(player,enemy,world,clock):
    global flashOn,lightsOn
    running = True
    flashOn = True
    lightsOn = False
    while running:
        now = pygame.time.get_ticks()
        
        # handle every event since the last frame

        cameraSurface.fill((255,255,255))
        
        world.draw(cameraSurface)

         

        player.handle_keys() # handle the keys
        
        
        # fill the screen with white
        #enemy.move_towards_player(player=player)
        if enemy.check_collision(player= player) == True:
            print("ur dead gng")
            return "dead"
        player.draw(cameraSurface)
        #enemy.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit() # quit the screen
                running = False
            if event.type == lightsFlicker_Event:
                flashOn = True
                lightsOn = False
                flashLights(now)
        flashLights(now)
        screen.blit(cameraSurface, (0,0))
        

        pygame.display.update() # update the screen

        clock.tick(20)

def dead():
    background = pygame.image.load(os.path.join('C:/Users/kinfo/OneDrive/Untitled Battle Game','assets','images','ashesToAshes.jpg'))
    running = True
    while running:
        # handle every event since the last frame.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit() # quit the screen
                running = False
        screen.fill((255,255,255))
        screen.blit(background,(0,0))


 
        
        pygame.display.update() # update the screen

        clock.tick(20)

def navigation(page):

    if page == "main":
        print("Starting screen or main screen idk")
        page = game(player,enemy,world,clock)
    if page == "dead":
        print("LOL ur dead")
        page = dead()

navigation(page="main")