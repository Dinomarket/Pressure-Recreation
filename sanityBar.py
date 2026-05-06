import pygame

BLACK   = (0, 0, 0)
RED     = (255, 0, 0)
YELLOW  = (255, 255, 0)
ORANGE = (255, 165, 0)

class sanity_bar(object):
    def __init__(self):
        self.points = 0
        self.outline = (0, 0, 0)
        self.cap = 100
        self.ratio = 100
        self.filled = 0

    def increase(self,amount):
        if self.points != self.cap:
            self.points += amount
    
    def decrease(self,amount):
        if self.points != 0:
            self.points -= amount

    def reset(self):
        self.points = 0

    def draw(self,surface):
        self.filled = self.points/self.cap
        if self.filled < 0.25:
            color = YELLOW
        elif self.filled < 0.65:
            color = ORANGE
        else:
            color = RED


        pygame.draw.rect(surface, self.outline, (945,585, 45,160))
        outerRect = pygame.Rect((950,600 - 10, 35, 150))
        pygame.draw.rect(surface, self.outline, outerRect)
        filledRect = pygame.Rect((950, 600 - 10, 35, self.filled * 150))
        filledRect.bottomleft = outerRect.bottomleft
        pygame.draw.rect(surface, color, filledRect)