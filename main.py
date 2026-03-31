
import os
import pygame
import random
import math
from player import Player
from opponent import Enemy
from tilemap import TileMap
from opponent import Angler

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
angler = Angler()
clock = pygame.time.Clock()
world = TileMap(os.path.join("assets", "maps", "startMap.tmj"))


transparentSurface = pygame.Surface((1152, 768), pygame.SRCALPHA)

lightsFlicker_Event = pygame.event.custom_type()
lightsOn = False
flashInterval = random.randint(120,150)
flashDuration = 2000
lastFlash = 0
flashStart = lastFlash

cameraSurface = pygame.Surface((1152,768))


def checkShake(shaking, shake_start):
    if shaking:
        shaking, offset_x, offset_y = cameraShake(shake_start)
    else:
        offset_x, offset_y = 0, 0
    return shaking, offset_x , offset_y

def cameraShake(start_time, duration=4000, magnitude=16):
    elapsed = pygame.time.get_ticks() - start_time

    if elapsed >= duration:
        return False, 0, 0

    decay = 1 - (elapsed / duration)    

    offset_x = int(magnitude * decay * math.sin(elapsed * 0.05))
    offset_y = int(magnitude * decay * math.cos(elapsed * 0.05))

    return True, offset_x, offset_y

def flashLights(currentTime):
    global lastFlash, flashOn, flashStart, lightsOn

    if lightsOn == False:
        print("flashing stuff")
        # stop after duration
        if currentTime - flashStart > flashDuration:
            lightsOn = True
            flashOn = False

        else:
                # toggle on/off
            if currentTime - lastFlash >= flashInterval:
                print(currentTime)
                #print(flashInterval)
                #print(flashDuration)
                flashOn = not flashOn
                lastFlash = currentTime

        if flashOn:
            print("im flashin")
            transparentSurface.fill((0,0,0,128))
            screen.blit(transparentSurface,(0,0))     
        

def game(player,enemy,world,clock):
    global flashOn,lightsOn
    running = True
    flashOn = True
    lightsOn = False
    shake_start = 0
    shaking = False

    offset_x = 0
    offset_y = 0
    while running:
        now = pygame.time.get_ticks()
        
        # handle every event since the last frame

        cameraSurface.fill((255,255,255))
        
        world.draw(cameraSurface)

         

        player.handle_keys() # handle the keys
        angler.rushPath()
        
        # fill the screen with white
        #enemy.move_towards_player(player=player)
        if angler.check_collision(player= player):
            print("ur dead gng")
            return "dead"
        if world.is_blocked(player.hitbox):
            print("You are hitting a wall!")
        print(world.walls)
        print(world.doors)
        player.draw(cameraSurface)
        angler.draw(cameraSurface)
        #enemy.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit() # quit the screen
                running = False
            if event.type == lightsFlicker_Event:
                flashOn = True
                lightsOn = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE: 
                    print('RUMBLING RUMBLING ITS COMING')
                    shake_start = pygame.time.get_ticks()
                    shaking = True
                if event.key == pygame.K_0:
                    print("LIGHTS FLASH")
                    lightsOn = False
                    flashOn = True   # start flashing
                    
        shaking, offset_x , offset_y = checkShake(shaking, shake_start)
        screen.blit(cameraSurface, (0 + offset_x ,0 + offset_y))
        
        flashLights(now)

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