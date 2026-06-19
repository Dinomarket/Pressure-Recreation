import os
import pygame

dir_path = os.path.dirname(os.path.realpath(__file__))

imgFront_path = os.path.join(dir_path,'assets','images','playerFront.png')
imgBack_path = os.path.join(dir_path,'assets','images','playerBack.png')
imgLeft_path = os.path.join(dir_path,'assets','images','playerLeft.png')
imgRight_path = os.path.join(dir_path,'assets','images','playerRight.png')

class Player(object): 
    def __init__(self):
        """ The constructor of the class """
        self.image = pygame.image.load(imgFront_path)
        self.image = pygame.transform.scale(self.image, (90, 140))
        self.x = 500
        self.y = 500
        self.oldY = self.y
        self.oldX = self.x
        self.hitbox = pygame.Rect(self.x, self.y, 90, 140)
        self.view_hitbox = pygame.Rect(self.x, self.y , 300, 150)
        self.visible = True
        
    def handle_keys(self, dist = 12):#og dist is 12
        """ Handles Keys """
        if self.visible == True:
            key = pygame.key.get_pressed()
            self.oldY = self.y
            self.oldX = self.x
            # distance moved in 5 frames
            if key[pygame.K_a]:
                self.x -= dist
                self.image = pygame.image.load(imgLeft_path)
                self.image = pygame.transform.scale(self.image, (90, 140))

                self.view_hitbox = pygame.Rect(self.x - 240, self.y , 300, 70)
            if key[pygame.K_d]:
                self.x += dist
                self.image = pygame.image.load(imgRight_path)
                self.image = pygame.transform.scale(self.image, (90, 140))
                self.view_hitbox = pygame.Rect(self.x + 40, self.y, 300, 70)
            if key[pygame.K_w]:
                self.y -= dist
                self.image = pygame.image.load(imgBack_path)
                self.image = pygame.transform.scale(self.image, (90, 140))
                self.view_hitbox = pygame.Rect(self.x, self.y- 240, 70, 300)
            if key[pygame.K_s]:
                self.y += dist
                self.image = pygame.image.load(imgFront_path)
                self.image = pygame.transform.scale(self.image, (90, 140))
                self.view_hitbox = pygame.Rect(self.x, self.y+ 40, 70, 300)
       

            self.hitbox.x = self.x
            self.hitbox.y = self.y

    
    def hide(self):
        self.visible = False
        self.x = -10000
        self.y = 0
        self.hitbox.x = self.x
        self.hitbox.y = self.y

    def leaveLocker(self):
        self.visible = True
        self.x = self.oldX
        self.y = self.oldY
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


        surface.blit(self.image, (self.hitbox.x, self.hitbox.y))
        
    
