 
import math
import pygame
import os
import random
BLACK   = (0, 0, 0)

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




class Lights:
    def __init__(self):
        self.is_dark = False
        self.is_flashing = False

        self.flash_duration = 2000  # milliseconds
        self.flash_interval = 150   # milliseconds

        self.flash_start_time = 0
        self.last_flash_time = 0
        self.flash_visible = False


    def turn_off(self):
        self.is_dark = True
        self.is_flashing = False

    def turn_on(self):
        self.is_dark = False
        self.is_flashing = False

    def start_flash(self, duration=2000, interval=150):
        print("startin flash")
        self.is_flashing = True
        self.is_dark = False

        self.flash_duration = duration
        self.flash_interval = interval

        self.flash_start_time = pygame.time.get_ticks()
        self.last_flash_time = self.flash_start_time
        self.flash_visible = True

    def update(self):
        if self.is_flashing:
            current_time = pygame.time.get_ticks()
            print("We flashin ")
            if current_time - self.flash_start_time >= self.flash_duration:
                self.is_flashing = False
                self.flash_visible = False
                self.is_dark = False
                return

            if current_time - self.last_flash_time >= self.flash_interval:
                self.flash_visible = not self.flash_visible
                self.last_flash_time = current_time
    def draw(self, screen, surface):
        # Always draw the base frame first
        screen.blit(surface, (0, 0))

        if self.is_dark:
            dark = pygame.Surface(screen.get_size())
            dark.fill(BLACK)
            dark.set_alpha(180)
            screen.blit(dark, (0, 0))

        elif self.is_flashing and self.flash_visible:
            flash = pygame.Surface(screen.get_size())
            flash.fill(BLACK)
            flash.set_alpha(120)
            screen.blit(flash, (0, 0))