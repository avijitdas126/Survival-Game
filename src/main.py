from time import sleep, time
from turtle import right
from typing import Dict, List

import pygame
import os
import math
import pathlib

import pytmx

from tile.tile import  load_tmx_map
# from tile.tile import tmx_data
from entities.Enemy import Enemy
from entities.player import Character
from core.utils import SCREEN_HEIGHT, SCREEN_WIDTH, TILE_SIZE, damge, draw, handle_move, load_image,screen,clock,running

# pygame setup
pygame.init()

def main():
    global running
    player=Character(100,100,32,32,'character',sprite_name='character',animations=['idle','jump-all','jump','run','run','attack','die'])
    enemy=Enemy(900,100,32,32,'enemy',sprite_name='skeleton',animations=['idle','jump-all','run','hurt','attack','die'])

    enemies=[enemy]
    tmx_data=load_tmx_map('assets/tiles/tiles.tmx')
    
    while running:
        FPS=60 # limits FPS to 60
        COLOR=(255,255,255)
        
        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                running = False
            
            if event.type==pygame.KEYDOWN:
                if event.key == pygame.K_k:
                    player.mode='attack'
            if event.type==pygame.KEYUP:
                player.mode=None
                
        screen.fill(COLOR)
        bg_image=load_image(['assets','background'],'Background.png')
        
        handle_move(FPS,player)
        player.loop(FPS,tmx_data)
        enemies = list(filter(lambda x: x.is_alive == True, enemies))
        for enemy in enemies:
            enemy.loop(FPS,tmx_data)
            enemy.enemy_ai(player)
        damge(player,enemies)
        draw(FPS,bg_image,player,tmx_data,enemies)
        
        
        clock.tick(FPS)  

    pygame.quit()

if __name__ == "__main__":
    main()

