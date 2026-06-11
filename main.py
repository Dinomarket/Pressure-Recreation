
import os
import pygame
import random
import math
import time

pygame.init()
global screen
screen = pygame.display.set_mode((1152, 768))

from player import Player
from dialogue import message
from opponent import Dweller, Angler, Pinky
from tilemap import tiles
from overlay import HeartbeatOverlay
from sanityBar import sanity_bar
from lights import lights, Lights


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






panick = HeartbeatOverlay()

#xTile = tiles()
Light = Lights()

# create an instance
wallDweller = Dweller()
pinky = Pinky()
angler = Angler()
clock = pygame.time.Clock()
#world = TileMap(os.path.join("assets", "maps", "startMap.tmj"))
world = tiles(os.path.join('C:/Users/kinfo/OneDrive/Untitled Battle Game','assets','maps','generalHall.tmx'))
sanity = sanity_bar()
text = message()
player = Player() 
#print("tile layers:",xTile.mapData.visible_layers)

transparentSurface = pygame.Surface((1152, 768), pygame.SRCALPHA)
font = pygame.font.Font(os.path.join('C:/Users/kinfo/OneDrive/Untitled Battle Game','assets','images',"Pokemon Classic.ttf"), 20)
basicFont = pygame.font.SysFont("arial",20)
sanityPoints = 0
cameraSurface = pygame.Surface((1152,768))

triggerTime = 0
flashStartTime = 0
delayed_calls = []

activeNode = False

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



def fadeout(speed=5):
    global gameData
    print('''
Calling fadeout
          ''')
    fade_surface = pygame.Surface((screen.get_width(), screen.get_height()))
    fade_surface.fill((0, 0, 0))  # Black color for fadeout
    for alpha in range(0, 255, speed):
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        pygame.display.update()
        pygame.time.delay(10)  # controls speed of fade



def call_after_delay(func, delay_ms):
    trigger_time = pygame.time.get_ticks() + delay_ms
    delayed_calls.append((trigger_time, func))

def update_delayed_calls():
    now = pygame.time.get_ticks()
    for call in delayed_calls[:]:
        trigger_time, func = call
        if now >= trigger_time:
            func()
            delayed_calls.remove(call)



def summonAngler():
    global shaking,shake_start
    global activeNode

    print("mf am I gonna summon myself or what")
    angler.active = True
    if angler.direction == "back":
        angler.hitbox.x = -500
        
    else:
        angler.hitbox.x = 1500

    angler.hitbox.y = 100
    print('RUMBLING RUMBLING ITS COMING')
    print("SUMMON ANGLER")
    shake_start = pygame.time.get_ticks()
    shaking = True
    activeNode = False
    print("twin, how is this possible")

def summonPinky():
    global shaking,shake_start
    global activeNode

    pinky.active = True

    pinky.hitbox.x = -500
        

    pinky.hitbox.y = 100

    print("SUMMON PINKY")
    shake_start = pygame.time.get_ticks()
    shaking = True
    activeNode = False
    print("twin, how is this possible")  
    

def anglerNode():
    global activeNode

    activeNode = True
    Light.start_flash(duration=2000, interval=random.randint(100,120))
    angler.direction = random.choice(["back","front"])
    call_after_delay(summonAngler, random.randint(3000,8000))
    
def pinkyNode():
    global activeNode

    activeNode = True
    sanity.points = 0 

    call_after_delay(summonPinky, random.randint(7000,12000))
    
   
def randomEvents(Score):
    node = random.randint(1,100)
    print(node)
    if node <= 20 and Score > 3000 and activeNode == False:
        anglerNode()
        text.start_message()
        text.mail = "An impending doom approaches..."
    
    elif node >= 20 and node <= 35 and Score > 3000 and activeNode == False:
        pinkyNode()
        text.start_message()
        text.mail = "Whats that noise?"
    
    if random.randint(1,5) == 2 and Score > 3000 and player.hitbox.x > 300:
        wallDweller.alive = True
        wallDweller.x = -50
        wallDweller.y = 1
        wallDweller.hitbox.x = wallDweller.x
        wallDweller.hitbox.y = wallDweller.y

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
    text.start_message()
    while running:
 
        
        # handle every event since the last frame

       
        
        world.draw(cameraSurface)
        sanity.draw(cameraSurface)
        
        #print "poopypants"

        player.handle_keys() # handle the keys
        angler.rushPath()
        pinky.rushPath()
        
        # fill the screen with white
        if wallDweller.alive == True:
            wallDweller.move_towards_player(player=player)
        
        if wallDweller.check_collision(player=player):
            print("slimed")
            return "dead"
        
        if angler.check_collision(player= player):
            print("ur dead gng")
            return "dead"
        if pinky.check_collision(player= player):
            print("ur dead sonion")
            return "dead"

        if world.is_blocked(player.hitbox):
            print("You are hitting a wall!")
            player.x = player.oldX
            player.y = player.oldY

        if world.check_for_locker(player.hitbox) and sanity.points >= 30:
            print("you can get in this locker")
            canEnterLocker = True
        else:
            canEnterLocker = False
        
        if world.check_doors(player.hitbox):
            print("We outta here!")
            fadeout(12)
            Score += 1000
            points = font.render(f"Score: {Score}",False,WHITE)
            world = tiles(os.path.join('C:/Users/kinfo/OneDrive/Untitled Battle Game','assets','maps','generalHall.tmx'))
            player.x = 50
            player.y = 350  
            player.hitbox.x = 50
            player.hitbox.y = 350
            randomEvents(Score)
            


        if not player.visible:
            sanity.decrease(1)
            
            if sanity.points == 0:
                player.leaveLocker()

        else: 
            sanity.increase(0.75)

        player.draw(cameraSurface)
        pinky.draw(cameraSurface)
        angler.draw(cameraSurface)
        update_delayed_calls()
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
                    pinky.active = True
                    pinky.hitbox.x = -500
                    pinky.hitbox.y = 100
                    
                    print('RUMBLING RUMBLING ITS COMING')
                    print("SUMMON PINKIES")
                    shake_start = pygame.time.get_ticks()
                    shaking = True
                    
                if event.key == pygame.K_1:
                    print("I do stuff now ????")
                    text.start_message()
                    text.mail = "peanut butter jelly time!"
                    wallDweller.alive = True
                    wallDweller.x = -700
                    wallDweller.y = 1
                    wallDweller.hitbox.x = wallDweller.x
                    wallDweller.hitbox.y = wallDweller.y


                if event.key == pygame.K_0:
                    print("lights flash like jinglers")
                    Light.start_flash(duration=3000, interval=120)
                if event.key == pygame.K_e:
                    if canEnterLocker:
                        sanity.reset()
                        player.hide()
                        panick.start(duration=5100)
                    else:
                        player.leaveLocker()
                        panick.active = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_4:
                        Light.turn_off()

                    if event.key == pygame.K_2:
                        Light.turn_on()
 
                        
        shaking, offset_x , offset_y = checkShake(shaking, shake_start)
        
        screen.blit(cameraSurface, (0 + offset_x ,0 + offset_y))
        text.displayMessage(surface= screen)
        #light.flashLights(startTime=flashStartTime, screen= screen, surface= transparentSurface) 
        Light.update()
        Light.draw(screen=screen, surface= transparentSurface)
        panick.update()
        panick.draw(screen)
        screen.blit(points,(920,25))
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


def anglerDeathScreen():
    background = pygame.image.load(os.path.join('C:/Users/kinfo/OneDrive/Untitled Battle Game','assets','images','anglerEnd.png'))
    running = True
    shake_start = pygame.time.get_ticks()
    shaking = True
    offset_x = 0
    offset_y = 0

    while running:
        game_surface = pygame.Surface(screen.get_size())
        game_surface.fill((255,255,255))
        game_surface.blit(background,(0,0))
        
        # handle every event since the last frame.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit() # quit the screen
                running = False

        if angler.scale > 1.15:
            return
        print(angler.scale)
        angler.enlarge(dt = clock.tick(60)/1000)
        angler.deathByAngler(screen=game_surface)
        
        
        shaking, offset_x , offset_y = checkShake(shaking, shake_start)
 
        print(offset_x,offset_y)
        screen.blit(game_surface, (0 + offset_x ,0 + offset_y))
        pygame.display.update() # update the screen
        clock.tick(20)



def navigation(page):

    if page == "main":
        print("Starting screen or main screen idk")
        page = game(player,wallDweller,world,clock)
    if page == "dead":
        print("LOL ur dead")
        page = anglerDeathScreen()
        fadeout()

navigation(page="main")