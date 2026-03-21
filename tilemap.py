import os
import pygame
import json
import xml.etree.ElementTree as ET

class TileMap:
    def __init__(self, tmj_file):
        # -----------------------------
        # Load map
        # -----------------------------
        with open(tmj_file) as f:
            self.map_data = json.load(f)

        self.tile_size = self.map_data["tilewidth"]
        self.width = self.map_data["width"]
        self.height = self.map_data["height"]

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

    # -----------------------------
    # Check collision for a position
    # -----------------------------
    def is_blocked(self, px, py):
        gx = px // self.tile_size
        gy = py // self.tile_size

        if gx < 0 or gy < 0 or gx >= self.width or gy >= self.height:
            return True

        for layer in self.layers:
            if layer["name"].lower() == "collision":
                index = gy * self.width + gx
                return layer["data"][index] != 0

        return False
