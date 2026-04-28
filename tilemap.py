import os
import pygame
import json
import xml.etree.ElementTree as ET
import pytmx
from pytmx.util_pygame import load_pygame
import sys


class TileMap:
    def __init__(self, tmj_file):
        # -----------------------------
        # Load map
        # -----------------------------
        with open(tmj_file) as f:
            self.map_data = json.load(f)

        # -----------------------------
        # Load all tilesets
        # -----------------------------
        self.tilesets = []
        for ts_info in self.map_data["tilesets"]:
            tsx_path = os.path.normpath(os.path.join(os.path.dirname(tmj_file), ts_info["source"]))
            print(f"Loading tileset from: {tsx_path}")

            tree = ET.parse(tsx_path)
            root = tree.getroot()
            image_source = root.find("image").attrib["source"]
            image_path = os.path.normpath(os.path.join(os.path.dirname(tsx_path), image_source))

            image = pygame.image.load(image_path).convert_alpha()
            columns = int(root.attrib["columns"])

            self.tilesets.append({
                "firstgid": ts_info["firstgid"],
                "image": image,
                "columns": columns
            })

        # -----------------------------
        # Store layers
        # -----------------------------
        self.layers = self.map_data["layers"]
        self.walls = []
        self.grass = []
        self.doors = []

        for layer in self.layers:
            if layer["type"] == "objectgroup":
                for obj in layer["objects"]:
                    rect = pygame.Rect(
                        obj["x"],
                        obj["y"],
                        obj["width"],
                        obj["height"]
                    )

                    obj_type = obj.get("type", "")

                    if obj_type == "wall":
                        self.walls.append(rect)
                    elif obj_type == "grass":
                        self.grass.append(rect)
                    elif obj_type == "mainDoor":
                        self.doors.append(rect)
                    
        self.tile_size = self.map_data["tilewidth"]
        self.width = self.map_data["width"]
        self.height = self.map_data["height"]


    # -----------------------------
    # Get the correct tile surface for a gid
    # -----------------------------
    def get_tile(self, gid):
        if gid == 0:
            return None

        # Determine which tileset the gid belongs to
        tileset = None
        for ts in reversed(self.tilesets):
            if gid >= ts["firstgid"]:
                tileset = ts
                break

        if not tileset:
            return None

        local_id = gid - tileset["firstgid"]
        ts_image = tileset["image"]
        columns = tileset["columns"]

        x = (local_id % columns) * self.tile_size
        y = (local_id // columns) * self.tile_size

        tile_surface = pygame.Surface((self.tile_size, self.tile_size), pygame.SRCALPHA)
        tile_surface.blit(ts_image, (0, 0), pygame.Rect(x, y, self.tile_size, self.tile_size))

        return tile_surface

    # -----------------------------
    # Draw all layers (except collision)
    # -----------------------------
    def draw(self, screen):
        for layer in self.layers:
            if layer["type"] != "tilelayer":
                continue
            if layer["name"].lower() == "collision":
                continue  # skip collision layer

            data = layer["data"]
            for y in range(self.height):
                for x in range(self.width):
                    index = y * self.width + x
                    gid = data[index]
                    tile = self.get_tile(gid)
                    if tile:
                        screen.blit(tile, (x*self.tile_size, y*self.tile_size))
        for wall in self.walls:
            pygame.draw.rect(screen, (255, 0, 0), wall, 2)



    # -----------------------------
    # Check collision for a position
    # -----------------------------
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
    
class tiles():
    def __init__(self):
        self.mapData = load_pygame(os.path.join('C:/Users/kinfo/OneDrive/Untitled Battle Game','assets','maps','startMap.tmx'))
        self.walls = []
        self.lockers = []
        self.doors = []
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

    def check_for_locker(self,rect):
        for locker in self.lockers:
            if rect.colliderect(locker):
                return True
        return False
  
"""
class Tile(pygame.sprite.Sprite):
	def __init__(self,pos,surf,groups):
		super().__init__(groups)
		self.image = surf
		self.rect = self.image.get_rect(topleft = pos)

# cycle through all layers
for layer in tmx_data.visible_layers:
	# if layer.name in ('Floor', 'Plants and rocks', 'Pipes')
	if hasattr(layer,'data'):
		for x,y,surf in layer.tiles():
			pos = (x * 128, y * 128)
			Tile(pos = pos, surf = surf, groups = sprite_group)

for obj in tmx_data.objects:
	pos = obj.x,obj.y
	if obj.type in ('Building', 'Vegetation'):
		Tile(pos = pos, surf = obj.image, groups = sprite_group)
"""
	
class locker:
    def __init__(self):
        self.hitbox = pygame.Rect()