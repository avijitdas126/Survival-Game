import math
import os
from time import time
from typing import Dict, List, List

import pygame
import pytmx

# import entities.Enemy 
# import entities.player 






# from entities.Enemy import Enemy
# from entities.player import Character

SCREEN_WIDTH,SCREEN_HEIGHT=800,600
TILE_SIZE = 16
COLS, ROWS = 30, 30
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Survival Game")
clock = pygame.time.Clock()
running = True
SCROLL=0

# Example Map Data (0 = empty, 1 = ground)
# Creating a simple floor on the last row
game_map = [[0 for _ in range(COLS)] for _ in range(ROWS)]
game_map[29] = [1 for _ in range(COLS)]

def load_image(dir =[],img_src:str=''):
    img_path=os.path.join(*dir,img_src)
    try:
        load_img=pygame.image.load(img_path).convert_alpha()
    except pygame as e:
        print("Error loading image: "+ e)
        global running
        running =False
    else:
        return load_img
    
def load_sprite(width:int,height:int,dir,sprite_name,animations)->Dict[str,List[pygame.Surface]]:
    char_animation=animations
    all_sprites:Dict[str,List[pygame.Surface]]={}
    for animation in char_animation:
        sprites=[]
        if animation =='attack':
            width=64
            height=80
        sprite=load_image(['assets',dir],f'{sprite_name}-{animation}.png')
        for i in range(sprite.get_width() // width):
            surface=pygame.Surface((width,height),pygame.SRCALPHA,32)
            rect=pygame.Rect(i*width,0,width,height)
            surface.blit(sprite,(0,0),rect)
            sprites.append(pygame.transform.scale2x(surface))
            # sprites.append(surface)
            all_sprites[animation]=sprites
    
    return all_sprites


                    
def handle_move(FPS,player):
    
    event = pygame.key.get_pressed()
    player.x_vel=0
    if event[pygame.K_RIGHT]:       
        player.move_right(player.ACCELERATION)
    if event[pygame.K_LEFT]:       
        player.move_left(player.ACCELERATION)
    if event[pygame.K_UP]:
        player.jump() 
    # player.collided_x(blocks)
    # player.collided_y(blocks)

def health_bar(player):
    rect = pygame.Rect(20, 10, 400, 20)
    border_rect = rect.inflate(3 * 2, 3 * 2)
    pygame.draw.rect(screen, (0,0,0), border_rect,border_radius=23)

    # 2. Draw the inner filled rectangle on top
    pygame.draw.rect(screen, (0,0,0), rect,border_radius=23)
    rect2 = pygame.Rect(20, 10, 400*(player.hp/player.max_hp), 20) 
    pygame.draw.rect(screen,(0,255,0),rect2,border_radius=23)
    img=load_image(['assets','extra'],'heart.png')
    screen.blit(pygame.transform.scale2x(img),(0,5))
    # pass

def damge(player,enemies):
    enemy=None
    for e in enemies:
        if pygame.sprite.collide_mask(player,e):
            enemy=e
            break
    if enemy is not None:
        print(f"player.hp :{player.hp} enemy.hp: {enemy.hp} enemy.mode: {enemy.mode}  player.mode { player.mode}")
        if enemy.direction=='right':
            if player.mode is not None and time()-enemy.last_hit > 0.5 and  player.mode=='attack' and pygame.sprite.collide_mask(player,enemy) and enemy.hp>0:
                enemy.hp-=enemy.damge_no
                enemy.last_hit = time()
                enemy.mode='hurt'
                print(f"enemy.hp: {enemy.hp}")
            if enemy.mode is not None and time()-player.last_hit > 0.5 and enemy.mode=='attack' and pygame.sprite.collide_mask(player,enemy) and player.hp>0:
                player.hp-=player.damge_no
                player.last_hit = time()
                print(f"player.hp: {player.hp}")
        else:
            if player.mode is not None and time()-enemy.last_hit > 0.5 and  player.mode=='attack' and pygame.sprite.collide_mask(enemy,player) and enemy.hp>0:
                enemy.hp-=enemy.damge_no
                enemy.last_hit = time()
                enemy.mode='hurt'
                print(f"enemy.hp: {enemy.hp}")
            if enemy.mode is not None and time()-player.last_hit > 0.5 and enemy.mode=='attack' and pygame.sprite.collide_mask(enemy,player) and player.hp>0:
                player.hp-=player.damge_no
                player.last_hit = time()
                print(f"player.hp: {player.hp}")
    
    
        


def get_background(bg_img:pygame.Surface):
    bg_width=bg_img.get_width()
    tiles=math.ceil(SCREEN_WIDTH / bg_width ) + 1
    return tiles,bg_width
    
def draw(fps,bg_image,player,tmx_data:pytmx.TiledMap,enemies):
    from tile.tile import draw_map_relative_to_player
    global screen,SCROLL
    tiles,width=get_background(bg_image)
    screen.blit(bg_image,(-1*width,0))
    for i in range(0,tiles):
        screen.blit(bg_image,(i*width+SCROLL,0))
    x_off,y_off,blocks=draw_map_relative_to_player(screen,tmx_data,player)
    player.x_offset=x_off
    player.y_offset=y_off
    player.blocks=blocks
    player.draw(screen,fps)
    for enemy in enemies:
        enemy.x_offset=x_off
        enemy.y_offset=y_off
        enemy.blocks=blocks
        enemy.draw(screen,fps)
    
    health_bar(player)
    print(f"Right Side:{SCREEN_WIDTH-player.rect.x}")
    print(f"Left Side:{player.rect.x}")
    pygame.display.update()
    # scrolling effect like parallex effect 
    if (SCREEN_WIDTH-player.rect.x)<=400 and player.x_vel>0:
        player.rect.x-=.96
        SCROLL-=5
        if abs(SCROLL) > width:
            SCROLL=0



