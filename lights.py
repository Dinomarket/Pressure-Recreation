 
import math
import pygame
import os
import random

class lights:
    def __init__(self):
        self.On = True
        self.flashInterval = random.randint(120, 150)
        self.Duration = 2000
        self.Start = 0
        self.flashOn = False

    def lightsOff(self, screen, surface):
        self.On = False
        surface.fill((0, 0, 0, 128))  # transparent black
        screen.blit(surface, (0, 0))

    def lightsOn(self):
        self.On = True
        self.flashOn = False

    def flashLights(self, startTime, screen, surface):
        currentTime = pygame.time.get_ticks()
        elapsed = currentTime - startTime

        if elapsed > self.Duration:
            self.lightsOn()

        if currentTime - self.Start >= self.flashInterval+ startTime:
            self.Start = currentTime
            self.lightsOff(screen, surface)