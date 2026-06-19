
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
from opponent import Dweller, Angler, Pinky, Blitz,Frogger,Chainsmoker
from tilemap import tiles, MapManager
from overlay import HeartbeatOverlay
from sanityBar import sanity_bar
from lights import lights, Lights
from mapStorage import maps

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




dir_path = os.path.dirname(os.path.realpath(__file__))

panick = HeartbeatOverlay()

#xTile = tiles()
Light = Lights()

# create an instance
wallDweller = Dweller()
frogger = Frogger()
blitz = Blitz()
pinky = Pinky()
angler = Angler()
chainsmoker = Chainsmoker()
clock = pygame.time.Clock()
#world = TileMap(os.path.join("assets", "maps", "startMap.tmj"))
world = tiles(os.path.join(dir_path,'assets','maps','generalHall.tmx'))
sanity = sanity_bar()
text = message()
player = Player() 
mapLoader = MapManager()
#print("tile layers:",xTile.mapData.visible_layers)

transparentSurface = pygame.Surface((1152, 768), pygame.SRCALPHA)
#font = pygame.font.Font(os.path.join('C:/Users/kinfo/OneDrive/Untitled Battle Game','assets','images',"Pokemon Classic.ttf"), 20)
font = text.font
basicFont = pygame.font.SysFont("arial",20)
sanityPoints = 0
cameraSurface = pygame.Surface((1152,768))

triggerTime = 0
flashStartTime = 0
delayed_calls = []

deathAngler = None
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
    
def summonChain():
    global shaking,shake_start,shakeMagnitude
    global activeNode

    chainsmoker.active = True
    shakeMagnitude = 20

    chainsmoker.hitbox.x = -500
    chainsmoker.hitbox.y = 100

    print("SUMMON CHAINSMOKER")
    shake_start = pygame.time.get_ticks()
    shaking = True
    activeNode = False
    
    print("twin, how is this possible")  

def summonBlitz():
    global shaking,shake_start
    global activeNode

    blitz.active = True

    blitz.hitbox.x = -500
    blitz.hitbox.y = 100

    print("SUMMON BLITZ")
    shake_start = pygame.time.get_ticks()
    shaking = True
    activeNode = False
    print("twin, how is this possible")  
    
def summonFrogger():
    global shaking,shake_start
    global activeNode
    if frogger.switchBack == 1 or frogger.switchBack == 3:
        frogger.direction = "back"
        frogger.hitbox.x = -500
    else:
        frogger.direction = "front"
        frogger.hitbox.x = 1500
    frogger.switchBack -= 1
    frogger.active = True
    print(frogger.direction)
   
    frogger.hitbox.y = 100

    print("SUMMON FROGGER")
    shake_start = pygame.time.get_ticks()
    shaking = True
    activeNode = False
    print("twin, how is this possible")  
    

def anglerNode():
    global activeNode

    activeNode = True
    Light.start_flash(duration=2000, interval=random.randint(100,120))
    print("do I work?")
    #angler.direction = random.choice(["back","front"])
    angler.direction = "back"
    call_after_delay(summonAngler, random.randint(4000,8000))
    angler.active = False
    
def pinkyNode():
    global activeNode

    activeNode = True
    sanity.points = 0 

    call_after_delay(summonPinky, random.randint(7000,12000))
    pinky.active = False

def blitzNode():
    global activeNode

    activeNode = True
    Light.start_flash(duration=4000, interval=random.randint(100,120))

    call_after_delay(summonBlitz, random.randint(4500,7000))
    blitz.active = False
   
def froggerNode():
    global activeNode
    frogger.switchBack = 3
    spawnTime = random.randint(4000,8000)
    activeNode = True
    Light.start_flash(duration=2000, interval=random.randint(100,120))


    call_after_delay(summonFrogger, spawnTime)

    call_after_delay(summonFrogger, spawnTime+ random.randint(3000,5000))

    call_after_delay(summonFrogger, spawnTime+ random.randint(8000,12000))
    frogger.active = False

def chainNode():
    global activeNode, shakeMagnitude
    activeNode = True
    Light.start_flash(duration=2000, interval=random.randint(100,120))
    
    call_after_delay(summonChain, random.randint(7000,12000))
    shakeMagnitude = 10
    chainsmoker.active = False
    print("chainsmoker is false gng I repeat he is false",chainsmoker)

def randomEvents(Score):
    node = random.randint(1,100)
    print(node)
    if Score > 2000 and activeNode == False:
        if node <= 20:
            anglerNode()
        elif node >= 21 and node <= 28:
            pinkyNode()
        elif node >= 29 and node <= 36:
            blitzNode()
        elif node >= 37 and node <= 44:
            froggerNode()
        elif node >= 45 and node <= 52:
            chainNode()
    
    if random.randint(1,5) == 2 and Score > 3000 and player.x > 300:
        print("player.x", player.x)
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
    global deathAngler
    global Score
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
        blitz.rushPath()
        frogger.rushPath()
        chainsmoker.rushPath()
        
        # fill the screen with white
        if wallDweller.alive == True:
            wallDweller.move_towards_player(player=player)
        

        if wallDweller.check_collision(player=player) or world.check_for_death(player.hitbox):
            print("slimed")
            fadeout(2)
            return "deadByDweller"
        if angler.check_collision(player= player):
            print("ur dead gng")
            deathAngler = angler
            return "deadByAngler"
        elif pinky.check_collision(player= player):
            print("ur dead sonion")
            deathAngler = pinky
            return "deadByAngler"
        elif blitz.check_collision(player=player):
            print("mmmmmm. Bro died")
            deathAngler = blitz
            return "deadByAngler"
        elif frogger.check_collision(player=player):
            print("aw helllllll nawwwww")
            deathAngler = frogger
            return "deadByAngler"
        elif chainsmoker.check_collision(player=player):
            print("tis unfortunate")
            chainsmoker.active = False
            world = tiles(os.path.join('C:/Users/kinfo/OneDrive/Untitled Battle Game','assets','maps','chainsmokerDeath.tmx'))
            player.x = 500
            player.y = 500
            player.hitbox.x = 500
            player.hitbox.y = 500
        
        

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
            
 
            world = tiles(os.path.join('C:/Users/kinfo/OneDrive/Untitled Battle Game','assets','maps',mapLoader.loadNextMap(maps)))
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
        blitz.draw(cameraSurface)
        frogger.draw(cameraSurface)
        chainsmoker.draw(cameraSurface)

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
                    chainsmoker.active = True
                    chainsmoker.hitbox.x = -500
                    chainsmoker.hitbox.y = 100
                    
                    print('RUMBLING RUMBLING ITS COMING')
                    print("SUMMON CHAINSMOKER")
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
    text.start_message()
    text.mail = f"Final Score: {Score}"
    while running:
        # handle every event since the last frame.
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit() # quit the screen
                running = False
        screen.fill((255,255,255))
        screen.blit(background,(0,0))
        text.displayMessage(surface = screen, color= (0,0,0))
        
        


 
        
        pygame.display.update() # update the screen

        clock.tick(20)


def deathScreen():
    global deathAngler
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

        if deathAngler.scale > 1.15:
            fadeout()
            return "deadByDweller"
        print(deathAngler.scale)
        deathAngler.enlarge(dt = clock.tick(60)/1000)
        deathAngler.deathByAngler(screen=game_surface)
        
        
        shaking, offset_x , offset_y = checkShake(shaking, shake_start)
 
        print(offset_x,offset_y)
        screen.blit(game_surface, (0 + offset_x ,0 + offset_y))
        pygame.display.update() # update the screen
        clock.tick(20)



def navigation(page):

    if page == "main":
        print("Starting screen or main screen idk")
        page = game(player,wallDweller,world,clock)
    if page == "deadByAngler":
        print("LOL ur dead")
        page = deathScreen()
        
    if page == "deadByDweller":
        print("hn")
        page = dead()

navigation(page="main")