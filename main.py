
import os
import pygame
import random
import math

pygame.init()
global screen
screen = pygame.display.set_mode((1152, 768))

from player import Player
from opponent import Dweller
from tilemap import tiles
from opponent import Angler
from sanityBar import sanity_bar
from lights import lights

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








#xTile = tiles()
light = lights()
player = Player() # create an instance
wallDweller = Dweller()
angler = Angler()
clock = pygame.time.Clock()
#world = TileMap(os.path.join("assets", "maps", "startMap.tmj"))
world = tiles(os.path.join('C:/Users/kinfo/OneDrive/Untitled Battle Game','assets','maps','startMap.tmx'))
sanity = sanity_bar()
#print("tile layers:",xTile.mapData.visible_layers)

transparentSurface = pygame.Surface((1152, 768), pygame.SRCALPHA)
font = pygame.font.Font(os.path.join('C:/Users/kinfo/OneDrive/Untitled Battle Game','assets','images',"Pokemon Classic.ttf"), 20)
basicFont = pygame.font.SysFont("arial",20)
sanityPoints = 0
cameraSurface = pygame.Surface((1152,768))

triggerTime = 0
flashStartTime = 0

def checkShake(shaking, shake_start):
    if shaking:
        shaking, offset_x, offset_y = cameraShake(shake_start)
    else:
        offset_x, offset_y = 0, 0
    return shaking, offset_x , offset_y

def cameraShake(start_time, duration=4000):
    elapsed = pygame.time.get_ticks() - start_time

    if elapsed >= duration:
        return False, 0, 0

    decay = 1 - (elapsed / duration)    
    print(shakeMagnitude)
    offset_x = int(shakeMagnitude * decay * math.sin(elapsed * 0.05))
    offset_y = int(shakeMagnitude * decay * math.cos(elapsed * 0.05))

    return True, offset_x, offset_y




    

def spawnNode():
    print("spawning angler")
    anglerSpawnTime = pygame.time.get_ticks()
    anglerSpawn = True
    return anglerSpawn,anglerSpawnTime




def anglerNode(currentTime):
    global flashOn, lightsOn, flashStart, triggerTime

    lightsOn = False
    flashOn = True

    # set trigger time once
    if triggerTime is None:
        triggerTime = currentTime + random.randint(2000, 4000)

    # check if time has passed
    if pygame.time.get_ticks() >= triggerTime:
        print("Something's coming")
        shaking = True
      
        return shaking
    else:
        return False

   


def game(player,enemy,world,clock):

    global flashStartTime
    global canEnterLocker
    global shakeMagnitude
    global spawnTime, anglerSpawn
    Score = 0
    points = font.render(f"Score: {Score}",False,WHITE)
    running = True
    shake_start = 0
    shaking = False
    shakeMagnitude = 10
    anglerSpawn = False
    

    offset_x = 0
    offset_y = 0
    while running:
 
        
        # handle every event since the last frame

       
        
        world.draw(cameraSurface)
        sanity.draw(cameraSurface)
        
        

        player.handle_keys() # handle the keys
        angler.rushPath()
        
        # fill the screen with white
        if wallDweller.alive == True:
            wallDweller.move_towards_player(player=player)
        
        if wallDweller.check_collision(player=player):
            print("slimed")
            return "dead"
        
        if angler.check_collision(player= player):
            print("ur dead gng")
            return "dead"

        if world.is_blocked(player.hitbox):
            print("You are hitting a wall!")
            player.x = player.oldX
            player.y = player.oldY

        if world.check_for_locker(player.hitbox) and sanity.points <= 70:
            print("you can get in this locker")
            canEnterLocker = True
        else:
            canEnterLocker = False
        
        if world.check_doors(player.hitbox):
            print("We outta here!")
            Score += 1
            points = font.render(f"Score: {Score}",False,WHITE)
            world = tiles(os.path.join('C:/Users/kinfo/OneDrive/Untitled Battle Game','assets','maps','level2TestMap.tmx'))
            
            

        if anglerSpawn == True:
            shaking = anglerNode(spawnTime)

        if not player.visible:
            sanity.increase(1)
            if sanity.points == 100:
                player.leaveLocker()

        else: 
            sanity.decrease(0.75)

        player.draw(cameraSurface)
        
        angler.draw(cameraSurface)

        if wallDweller.alive:
            wallDweller.draw(cameraSurface)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit() # quit the screen
                running = False
  
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    if world.check_for_locker(player.hitbox):
                        print("You can get in this locker!")

                if event.key == pygame.K_SPACE: 
                    print('RUMBLING RUMBLING ITS COMING')
                    shake_start = pygame.time.get_ticks()
                    shaking = True
                if event.key == pygame.K_1:
                    print("SUMMON ANGLER")
                    angler.active = True
                    angler.hitbox.x = 1
                    angler.hitbox.y = 250

                if event.key == pygame.K_0:
                    print("LIGHTS FLASH")
                    flashStartTime = pygame.time.get_ticks()
                if event.key == pygame.K_e:
                    if canEnterLocker:
                        sanity.reset()
                        player.hide()
                    else:
                        player.leaveLocker()
             
        shaking, offset_x , offset_y = checkShake(shaking, shake_start)
        
        screen.blit(cameraSurface, (0 + offset_x ,0 + offset_y))
        
        #light.flashLights(startTime=flashStartTime, screen= screen, surface= transparentSurface) 

        screen.blit(points,(980,25))
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
        page = game(player,wallDweller,world,clock)
    if page == "dead":
        print("LOL ur dead")
        page = dead()

navigation(page="main")