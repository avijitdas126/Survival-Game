
import math

import pygame
import pytmx

from world.Block import Block
from core.utils import load_sprite



class Character(pygame.sprite.Sprite):
    COLOR=(255,0,0)
    ACCELERATION=3
    GRAVITY=.5
    JUMP_STRENGTH=25
    
    def __init__(self,x,y,width,height,dir,sprite_name,animations):
        super().__init__()
        self.rect=pygame.Rect(x,y,width,height)
        self.SPRITES=load_sprite(36,64,dir,sprite_name,animations)
        self.x_vel=0
        self.y_vel=0
        self.mask=None
        self.image=None
        self.mode=None
        self.sprite_type=dir
        self.max_hp=30
        self.hp=self.max_hp
        self.damge_no=1
        # self.x=x
        # self.y=y
        # self.width=width
        # self.height=height
        self.direction='right'
        self.animation_count=0
        self.fall_count=0
        self.jump_count=0
        self.x_offset=0
        self.agjust_point=[0,0]
        self.is_jumping=True
        self.y_offset=0
        self.last_hit = 0
        self.is_alive=True
        self.blocks=[]
        self.__index=0
    
    def move(self,dx,dy,map_width_px):
        # print('move->')
        print(f'self.jump_count : {self.jump_count} self.x_offset :{self.x_offset} self.y_offset: {self.y_offset} fall_count : {self.fall_count } self.is_jumping: {self.is_jumping} x_vel : {self.x_vel} y_vel {self.y_vel} self.rect.x: {self.rect.x} self.rect.y: {self.rect.y} dx {dx} dy {dy}')
        self.rect.x+=dx
        self.collided_x(self.blocks)
        self.rect.y+=dy
        self.collided_y(self.blocks)
        if self.rect.right > map_width_px:
            self.rect.right = map_width_px
        elif self.rect.x < 0:
            self.rect.x = 0
    def move_left(self,vel):
        self.x_vel= -vel
        if self.direction!='left':
            self.direction='left'
            self.animation_count=0
    def move_right(self,vel):
        self.x_vel= vel
        if self.direction!='right':
            self.direction='right'
            self.animation_count=0
    def add_gravity(self,fps):
        self.y_vel += self.GRAVITY
        self.fall_count+=1

    def is_on_ground(self, blocks:list[Block]):
        feet_probe = self.rect.move(0, 1)
        for block in blocks:
            if feet_probe.colliderect(block.rect):
                return True
        return False

    def loop(self,fps,tmx_data:pytmx.TiledMap): # Physics of player
        # Apply gravity only when in air
        map_width_px = tmx_data.width * tmx_data.tilewidth   # 2850
        map_height_px = tmx_data.height * tmx_data.tileheight # 1900
        if not self.is_on_ground(self.blocks):
            self.is_jumping = True
        if self.is_jumping:
            self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)
            self.fall_count += 1
            if self.rect.y < 0:
                self.rect.y = 0
            elif self.rect.bottom > map_height_px:
                self.rect.bottom = map_height_px
        self.move(self.x_vel,self.y_vel,map_width_px)
        self.updated_char()

    def landed(self):
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0
        self.is_jumping = False
        
    def update(self):
        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)
    def collided_y(self, blocks:list[Block]):
        for block in blocks:
            if not pygame.sprite.collide_mask(self,block):
                continue
            # Landing: player falling down and block is below player's center
            if self.y_vel > 0 and block.rect.top < self.rect.bottom and block.rect.centery > self.rect.centery:
                self.rect.bottom = block.rect.top
                self.landed()
                break
            # Ceiling hit: player moving up and block is above player's center
            elif self.y_vel < 0 and block.rect.bottom > self.rect.top and block.rect.centery < self.rect.centery:
                self.rect.top = block.rect.bottom
                self.y_vel = 0
                break
                    
                        
    def collided_x(self, blocks:list[Block]):
        for block in blocks:
            if not pygame.sprite.collide_mask(self,block):
                continue
            # Only treat as wall if player's midsection hits the block's side
            # Skip if player is mostly above (jumping over) or below the block
            player_mid = self.rect.centery
            if player_mid < block.rect.top or player_mid > block.rect.bottom:
                continue  # Player center is outside block's vertical span - not a wall hit
            if self.x_vel > 0 and self.rect.right > block.rect.left:
                self.rect.right = block.rect.left
                self.x_vel = 0
                break
            elif self.x_vel < 0 and self.rect.left < block.rect.right:
                self.rect.left = block.rect.right
                self.x_vel = 0
                break
    def jump(self):
        print('jump->')
        if self.jump_count == 0:   # only if on ground
            self.y_vel = -self.GRAVITY*self.JUMP_STRENGTH
            self.jump_count = 1
            self.fall_count = 0
            self.is_jumping = True
    def updated_char(self):
        #print('updated_char->')

        image=self.image
        # player.x_vel=0
        
        if self.y_vel < 0 and self.is_jumping: # jumping up
            if self.sprite_type=='character':
                image=self.SPRITES['jump-all'][math.ceil((self.animation_count // 10)%(len(self.SPRITES['jump-all'])))]
                if self.direction=='left':
                    image=pygame.transform.flip(self.SPRITES['jump-all'][math.ceil((self.animation_count // 10)%(len(self.SPRITES['jump-all'])))],True,False)
            else:
                image=self.SPRITES['jump-all'][math.ceil((self.animation_count // 10)%(len(self.SPRITES['jump-all'])))]
                if self.direction=='left':
                    image=pygame.transform.flip(self.SPRITES['jump-all'][math.ceil((self.animation_count // 10)%(len(self.SPRITES['jump-all'])))],True,False)
        elif self.y_vel > 2 and self.is_jumping:  # falling
            if self.sprite_type=='character':
                image=self.SPRITES['jump-all'][math.ceil((self.animation_count // 10)%(len(self.SPRITES['jump-all'])-6))+6]
                if self.direction=='left':
                    image=pygame.transform.flip(self.SPRITES['jump-all'][math.ceil((self.animation_count // 10)%(len(self.SPRITES['jump-all'])-6))+6],True,False)
                        #agjust_point[1]=-(12*2)
            else:
                image=self.SPRITES['jump-all'][math.ceil((self.animation_count // 10)%(len(self.SPRITES['jump-all'])))]
                if self.direction=='left':
                    image=pygame.transform.flip(self.SPRITES['jump-all'][math.ceil((self.animation_count // 10)%(len(self.SPRITES['jump-all'])))],True,False)
        elif self.hp == 0:
            print(f'type={self.sprite_type}')
            frame = self.animation_count // 10
            if frame >= len(self.SPRITES['die']):
                frame = len(self.SPRITES['die']) - 1
                self.is_alive = False
            self.__index = frame
            image = self.SPRITES['die'][frame]
            if self.direction=='left':
                image=pygame.transform.flip(image,True,False)
            
        elif self.x_vel != 0:
            image=self.SPRITES['run'][math.ceil((self.animation_count // 10)%len(self.SPRITES['run']))]
            if self.direction=='left':
                image=pygame.transform.flip(self.SPRITES['run'][math.ceil((self.animation_count // 10)%len(self.SPRITES['run']))],True,False)
        elif self.mode is not None and self.mode=='attack':
            image=self.SPRITES['attack'][math.ceil((self.animation_count // 10)%len(self.SPRITES['attack']))]
            if self.direction=='left':
                image=pygame.transform.flip(self.SPRITES['attack'][math.ceil((self.animation_count // 10)%len(self.SPRITES['attack']))],True,False)
        elif self.mode is not None and self.mode=='hurt':
            image=self.SPRITES['hurt'][math.ceil((self.animation_count // 10)%len(self.SPRITES['hurt']))]
            if self.direction=='left':
                image=pygame.transform.flip(self.SPRITES['hurt'][math.ceil((self.animation_count // 10)%len(self.SPRITES['hurt']))],True,False)
        else:
            image=self.SPRITES['idle'][math.ceil((self.animation_count // 10)%len(self.SPRITES['idle']))]
            if self.direction=='left':
                image=pygame.transform.flip(self.SPRITES['idle'][math.ceil((self.animation_count // 10)%len(self.SPRITES['idle']))],True,False)
        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.size = self.image.get_size()
         # Restore bottom position
        self.animation_count+=1
        self.update()
    def check_tile_collision(self,tiles):
        for tile in tiles:
            if self.mask and tile.mask:
                if pygame.sprite.collide_mask(self,tile):
                    return tile
        return None
    
    def draw(self,win:pygame.Surface,fps): # render on screen
        win.blit(self.image,(self.rect.x+self.x_offset,self.rect.y+self.y_offset))

