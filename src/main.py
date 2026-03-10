from time import sleep, time
from turtle import right
from typing import Dict, List

import pygame
import os
import math
import pathlib

from world.Block import Block

from entities.Enemy import Enemy
from entities.player import Character
from core.utils import SCREEN_HEIGHT, SCREEN_WIDTH, damge, draw, handle_move, load_image,screen,clock,running

# pygame setup
pygame.init()


def main():
    global running
    player=Character(100,100,32,32,'character',sprite_name='character',animations=['idle','jump-all','jump','run','run','attack','die'])
    enemy=Enemy(900,100,32,32,'enemy',sprite_name='skeleton',animations=['idle','jump-all','run','hurt','attack','die'])

    blocks = []
    enemies=[enemy]
    BLOCK_SIZE = 95
    ground_img = load_image(['assets','tiles'], 'tileset_ground.png')

    bs=math.ceil(SCREEN_WIDTH / BLOCK_SIZE ) + 1
    for i in range(bs):  # create 15 blocks
        block = Block(((i * BLOCK_SIZE)-(10*i+1)), SCREEN_HEIGHT-BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE, ground_img)
        blocks.append(block)
    
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
        
        handle_move(FPS,player,blocks)
        player.loop(FPS,blocks)
        enemies = list(filter(lambda x: x.is_alive == True, enemies))
        # print(list(enemies))
        for enemy in enemies:
            enemy.loop(FPS,blocks)
            enemy.enemy_ai(player)
        damge(player,enemies)
        player.collided_y(blocks)
        draw(FPS,bg_image,player,blocks,enemies)
        
        
        clock.tick(FPS)  

    pygame.quit()

if __name__ == "__main__":
    main()

