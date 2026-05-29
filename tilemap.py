
import pygame
import os
import pytmx
from pytmx.util_pygame import load_pygame


path = os.path.join('C:/Users/kinfo/OneDrive/Untitled Battle Game','assets','maps')

maps = {
    "general":{"startMap":"startMap.tmx",
                "room1":"level2testMap.tmx"}
}

class tiles():
    def __init__(self,path):
        self.mapData = load_pygame(path)
        self.walls = []
        self.lockers = []
        self.doors = []
        self.backDoor = []
        self.order = ["startMap","room1","room2"]
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
                    elif obj.name == "locker":
                        self.lockers.append(rect)
                        print(self.lockers)


        



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
    
    def saveRoomOrder(self):
        if len(self.order) > 3:
            del self.order[0]




	
