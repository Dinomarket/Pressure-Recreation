import pygame
import os
WHITE   = (255, 255, 255)
message_box = pygame.Rect(375, 150, 400, 100)

class message:
    def __init__(self):
        self.char_index = 0
        self.typing_speed = 100
        self.last_time = pygame.time.get_ticks()

        self.font = pygame.font.Font(os.path.join('C:/Users/kinfo/OneDrive/Untitled Battle Game','assets','images','nerdropol lattice.otf'),20)

        self.duration = 4000

        self.start_time = 0
        self.active = False
        self.mail = "Smit Pressure By Sean Kim"


    def displayMessage(self, surface):
        if not self.active:
            return

        current_time = pygame.time.get_ticks()


        if current_time - self.start_time >= self.duration:
            self.active = False
            return

        if (self.char_index < len(self.mail)and current_time - self.last_time >= self.typing_speed):
            self.char_index += 1
            self.last_time = current_time

        visible_text = self.mail[:self.char_index]

        text_surface = self.font.render(visible_text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=message_box.center)

        surface.blit(text_surface, text_rect)

    def start_message(self):
        self.char_index = 0
        self.last_time = pygame.time.get_ticks()


        self.start_time = pygame.time.get_ticks()
        self.active = True