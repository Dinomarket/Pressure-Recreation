 
import math
import pygame
import os
import random

class lights(object):
    def __init__(self):
        self.On = False
        self.flashInterval = random.randint(120,150)
        self.Duration = 2000
        self.Start = 0
        self.flashOn = False

    def lightsOff(self,screen,surface):
        print("lights off")
        self.On = False
        screen.blit(surface,(0,0)) 
        surface.fill((0,0,0,128))

    def lightsOn(self):
        print("Lights on")
        self.On = True
        


    def flashLights(self, startTime,screen, surface):
        print("flash Lights")
        
            
        elapsed = pygame.time.get_ticks()- startTime 
        if startTime - elapsed > self.Duration:
            self.On = True
            self.flashOn = False

        else:

            if startTime - self.Start >= self.flashInterval:
                self.flashOn = not self.flashOn
                self.Start = startTime
        if self.flashOn == True:
            self.lightsOff(screen,surface)
        


def flashLights(currentTime):
    global lastFlash, flashOn, flashStart, lightsOn
    #add a duration to how long it lasts, and a permeneant value.
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
            screen.blit(transparentSurface,(0,0)) 
            transparentSurface.fill((0,0,0,128))
                