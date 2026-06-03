import pygame

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

class sanity_bar(object):
    def __init__(self):
        self.points = 100
        self.outline = (128,128,128)
        self.backColor = self.outline
        self.cap = 100
        self.ratio = 100
        self.filled = 0

    def increase(self,amount):
        if int(self.points) != self.cap:
            self.points += amount
            print(self.points)
    
    def decrease(self,amount):
        if int(self.points) != 0:
            self.points -= amount

    def reset(self):
        self.points = 99

    def draw(self,surface):
        self.filled = self.points/self.cap
        
    
        if self.filled > 0.75:
            color = GREEN
            backColor = (0, 108, 0)
        elif self.filled > 0.55:
            color = YELLOW
            backColor = (220,255,0)
        elif self.filled > 0.25:
            color = ORANGE
            backColor = (220,165,0)

        else:
            color = RED
            backColor = (220,0,0)


        pygame.draw.rect(surface, self.outline, (45,45, 160,45))
        outerRect = pygame.Rect((50,60 - 10, 150,35))
        pygame.draw.rect(surface, backColor, outerRect)
        filledRect = pygame.Rect((50, 60 - 10, self.filled * 150, 35))
        filledRect.bottomleft = outerRect.bottomleft
        pygame.draw.rect(surface, color, filledRect)