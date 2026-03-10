
import math

import pygame

from world.Block import Block
from core.utils import load_sprite



class Character(pygame.sprite.Sprite):
    COLOR=(255,0,0)
    ACCELERATION=3
    GRAVITY=.5
    
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
        self.__index=0
    
    def move(self,dx,dy,blocks):
        print('move->')
        print(f'self.jump_count : {self.jump_count} fall_count : {self.fall_count } self.is_jumping: {self.is_jumping} x_vel : {self.x_vel} y_vel {self.y_vel} self.rect.x: {self.rect.x} self.rect.y: {self.rect.y} dx {dx} dy {dy}')
        self.rect.x+=dx
        self.collided_x(blocks)
        self.rect.y+=dy
        self.collided_y(blocks)
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
    def loop(self,fps,blocks): # Physics of player
        # Apply gravity only when in air
        if self.is_jumping:
            self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)
            self.fall_count += 1
        self.move(self.x_vel,self.y_vel,blocks)
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
        block=self.check_tile_collision(blocks)
        if block is not None:
            if self.y_vel > 0:
                print(f'self.y_vel : {self.y_vel} self.rect.bottom : {self.rect.height} block.rect.top : {block.rect.height}')
                self.rect.y = (block.rect.y-self.rect.height)
                self.landed()
            elif self.y_vel < 0:
                self.rect.y = block.rect.y+self.rect.height
                self.y_vel = 0
                    
                        
    def collided_x(self, blocks:list[Block]):
        #print('collided_x->')
        #grounded = False  # Track if touching any ground block this frame 
        
        block=self.check_tile_collision(blocks)
        if block is not None:
            if self.x_vel > 0:
                print(f'self.y_vel : {self.y_vel} self.rect.bottom : {self.rect.bottom} block.rect.top : {block.rect.top}')
                self.rect.x = block.rect.x-self.rect.width
            elif self.x_vel < 0:
                self.rect.x = block.rect.x+self.rect.width
            self.x_vel=0
    def jump(self):
        print('jump->')
        if self.jump_count == 0:   # only if on ground
            self.y_vel = -self.GRAVITY*10
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

