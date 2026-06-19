
import pygame
import os
import pytmx
import random
from pytmx.util_pygame import load_pygame

dir_path = os.path.dirname(os.path.realpath(__file__))
path = os.path.join(dir_path,'assets','maps')


class MapManager():
    def __init__(self):
        self.roomType = "general"
        self.index = 0
        self.orderOfMaps = ["generalHall.tmx","generalHall.tmx","generalHall.tmx","generalHall.tmx"]
	
    
    def loadNextMap(self,maps):
        currentMap = self.orderOfMaps[self.index]

        # Move index forward
        print("index:",self.index)
        self.index += 1
        print(self.orderOfMaps)
        print(currentMap)
        # If we've reached the end of this room type
        if self.index >= len(self.orderOfMaps):
            if self.roomType == "general":
                self.roomType = random.choice(["ridge", "trenchTunnel","general"])
            else:
                self.roomType = "general"

            self.orderOfMaps = maps[self.roomType]
            print("How did we get here?")
            self.index = 0

        print(f"Loaded: {currentMap}")
        return currentMap
    
class tiles():
    def __init__(self,path):
        self.mapData = load_pygame(path)
        self.walls = []
        self.lockers = []
        self.doors = []
        self.backDoor = []
        self.death = []

        for layer in self.mapData.visible_layers:
            if isinstance(layer, pytmx.TiledObjectGroup):
                for obj in layer:
                    print(f"Object: {obj.name}, Position: ({obj.x}, {obj.y})")
            
                    rect = pygame.Rect(
                        obj.x,
                        obj.y,
                        obj.width,
                        obj.height
                    )


                    if obj.name == "wall":
                        self.walls.append(rect)
                        print(self.walls)
                    elif obj.name == "mainDoor":
                        self.doors.append(rect)
                        print(self.doors)
                    elif obj.name == "backDoor":
                        self.backDoor.append(rect)
                    elif obj.name == "locker":
                        self.lockers.append(rect)
                        print(self.lockers)
                    elif obj.name == "death":
                        self.death.append(rect)



    def draw(self, surface):
        for layer in self.mapData.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = self.mapData.get_tile_image_by_gid(gid)
                    if tile:
                        surface.blit(tile, (x * self.mapData.tilewidth, y * self.mapData.tileheight))

    def is_blocked(self, rect):
        for wall in self.walls:
            if rect.colliderect(wall):
                return True
        return False
    
    def check_doors(self, rect):
        for door in self.doors:
            if rect.colliderect(door):
                return True
        return False
    
    def check_backDoors(self,rect):
        for backDoor in self.backDoors:
            if rect.colliderect(backDoor):
                return True
        return False

    def check_for_locker(self,rect):
        for locker in self.lockers:
            if rect.colliderect(locker):
                return True
        return False
    
    def check_for_death(self,rect):
        for death in self.death:
            if rect.colliderect(death):
                return True
        return False


