
import math
import pygame
import os



enemy_img_path = os.path.join('C:/Users/kinfo/OneDrive/Untitled Battle Game','assets','images','sogger.jpg')
angler_img_path = os.path.join('C:/Users/kinfo/OneDrive/Untitled Battle Game','assets','images','angler1.png')

class Dweller(object):
    def __init__(self):
        self.image = pygame.image.load(enemy_img_path)
        self.x = 1
        self.y = 1
        self.speed = 15
        self.hitbox = pygame.Rect(self.x, self.y, 225, 225)
        self.image = pygame.transform.scale(self.image, (75,225))
        self.alive = True
        

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



    def check_collision(self,player):
        if self.hitbox.colliderect(player.hitbox):
            print("Why yall touching???")
            dead = True
            return dead
        
        elif not player.visible:
            self.x = -5000
            self.y = 0
            dead = False
            return dead
        
        elif self.hitbox.colliderect(player.view_hitbox):
            print("He saw me!")
            self.alive = False
            self.hitbox.x = 1
            self.hitbox.y = 10000

            dead = False
            return dead
        


            

        

    

    def draw(self, surface):
        """ Draw on surface """
        # blit opponent at your current position
        pygame.draw.rect(surface,(255, 0, 0) , self.hitbox)
        surface.blit(self.image, (self.hitbox.x, self.hitbox.y))
        

class Angler(object):
    def __init__(self):
        self.image = pygame.image.load(angler_img_path)
        self.speed = 80
        self.hitbox = pygame.Rect(1, 250, 500, 500)
        self.image = pygame.transform.scale(self.image, (500, 500))
        self.active = False

    def rushPath(self):
        self.hitbox.x += self.speed

    def check_collision(self,player):
        if self.hitbox.colliderect(player.hitbox) and self.active == True:
            print("Why yall touching???")
            dead = True
            return dead

    def draw(self, surface):
        """ Draw on surface """

        if self.active == True:

            surface.blit(self.image, (self.hitbox.x,self.hitbox.y))

