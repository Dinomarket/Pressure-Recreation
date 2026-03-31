
import math
import pygame
import os



img_path = os.path.join('C:/Users/kinfo/OneDrive/Untitled Battle Game','assets','images','enemy.jpg')

class Enemy(object):
    def __init__(self):
        self.image = pygame.image.load(img_path)
        self.x = 1
        self.y = 1
        self.speed = 5
        self.hitbox = pygame.Rect(self.x, self.y, 225, 225)
        self.image = pygame.transform.scale(self.image, (75,225))
        

    def move_towards_player(self, player):
        # Find direction vector (dx, dy) between enemy and player.
        dx, dy = player.hitbox.x - self.hitbox.x, player.hitbox.y - self.hitbox.y
        dist = math.hypot(dx, dy)
        if dist == 0:
            pass
        else:
            dx, dy = dx / dist, dy / dist   # Normalize.
        # Move along this normalized vector towards the player at current speed.
        self.hitbox.x += dx * self.speed
        self.hitbox.y += dy * self.speed
        

    #skibidi-Ansoggi

    # Same thing using only pygame utilities
    def move_towards_player2(self, player):
        # Find direction vector (dx, dy) between enemy and player.
        dirvect = pygame.math.Vector2(player.hitbox.x - self.hitbox.x,
                                      player.hitbox.y - self.hitbox.y)
        dirvect.normalize()
        # Move along this normalized vector towards the player at current speed.
        dirvect.scale_to_length(self.speed)
        self.hitbox.move_ip(dirvect)

    def check_collision(self,player):
        if self.hitbox.colliderect(player.hitbox):
            print("Why yall touching???")
            dead = True
            return dead

    def draw(self, surface):
        """ Draw on surface """
        # blit opponent at your current position
        pygame.draw.rect(surface,(255, 0, 0) , self.hitbox)
        surface.blit(self.image, (self.hitbox.x, self.hitbox.y))
        

class Angler(object):
    def __init__(self):
        self.x = 1
        self.y = 250
        self.speed = 100
        self.hitbox = pygame.Rect(self.x, self.y, 200, 200)

    def rushPath(self):
        self.hitbox.x += self.speed

    def check_collision(self,player):
        if self.hitbox.colliderect(player.hitbox):
            print("Why yall touching???")
            dead = True
            return dead

    def draw(self, surface):
        """ Draw on surface """
        # blit opponent at your current position
        pygame.draw.rect(surface,(255, 255, 0) , self.hitbox)