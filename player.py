import os
import pygame


print("Hello world")
img_path = os.path.join('C:/Users/kinfo/OneDrive/Untitled Battle Game','assets','images','player.png')

class Player(object): 
    def __init__(self):
        """ The constructor of the class """
        self.image = pygame.image.load(img_path)
        self.image = pygame.transform.scale(self.image, (125, 125))
        self.x = 500
        self.y = 500
        self.hitbox = pygame.Rect(self.x, self.y, 125, 125)
        print("yo")
    def handle_keys(self, dist = 12):
        """ Handles Keys """
        key = pygame.key.get_pressed()
         # distance moved in 5 frames
        if key[pygame.K_a]:
            self.x -= dist
        if key[pygame.K_d]:
            self.x += dist
        if key[pygame.K_w]:
            self.y -= dist
        if key[pygame.K_s]:
            self.y += dist
        if key[pygame.K_e]:
            print("you pressed e!")

        self.hitbox.x = self.x
        self.hitbox.y = self.y
            


    def dash(self, previous_key):
        print("You dashed!")
        print(previous_key)
        dist = 60
        if previous_key[pygame.K_d]: # right key
            print("You moved right")
            self.x += dist # move right
            self.hitbox.x = self.x
        elif previous_key[pygame.K_a]: # left key
            print("You moved left")
            self.x -= dist # move left
            self.hitbox.x = self.x

    


    def draw(self, surface):
        """ Draw on surface """
        # blit yourself at your current position
        pygame.draw.rect(surface,(255, 0, 0), self.hitbox)
        surface.blit(self.image, (self.hitbox.x, self.hitbox.y))
        
    
