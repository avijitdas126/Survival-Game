import os

import pygame
import pytmx

from core.utils import SCREEN_HEIGHT, SCREEN_WIDTH
from entities.player import Character
from world.Block import Block


def load_tmx_map(file_path):
    # Load the Tiled map data
    tmx_data = pytmx.load_pygame(file_path, pixelalpha=True)
    return tmx_data

def draw_map_relative_to_player(surface, tmx_data, player):
    # 1. Calculate the Offset
    # Center the player: Screen center minus player position
    offset_x = (SCREEN_WIDTH // 2) - player.rect.centerx
    offset_y = (SCREEN_HEIGHT // 2) - player.rect.centery

    # 2. Map Dimensions
    map_width = tmx_data.width * tmx_data.tilewidth
    map_height = tmx_data.height * tmx_data.tileheight

    # 3. Clamp the Offset
    # Max offset is 0 (left/top edge)
    # Min offset is Screen Size - Map Size (right/bottom edge)
    if map_width > SCREEN_WIDTH:
        offset_x = max(SCREEN_WIDTH - map_width, min(0, offset_x))
    else:
        offset_x = (SCREEN_WIDTH - map_width) // 2 # Center small maps

    if map_height > SCREEN_HEIGHT:
        offset_y = max(SCREEN_HEIGHT - map_height, min(0, offset_y))
    else:
        offset_y = (SCREEN_HEIGHT - map_height) // 2

    # 4. Draw the Layers
    tile_w = tmx_data.tilewidth
    tile_h = tmx_data.tileheight
    blocks=[]
    for layer in tmx_data.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, gid in layer:
                tile = tmx_data.get_tile_image_by_gid(gid)
                if tile:
                    world_x = x * tile_w
                    world_y = y * tile_h
                    # Clean math: Grid Position + Camera Offset
                    draw_x = world_x + offset_x
                    draw_y = world_y + offset_y
                    blocks.append(Block(world_x,world_y,tile_w,tile_h,tile))
                    # Performance: Only blit if visible (with 1 tile buffer)
                    if -tile_w < draw_x < SCREEN_WIDTH and -tile_h < draw_y < SCREEN_HEIGHT:
                        surface.blit(tile, (draw_x, draw_y))
    
    return offset_x, offset_y,blocks