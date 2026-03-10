import math

import pygame

from core.utils import SCREEN_WIDTH

class Object(pygame.sprite.Sprite):
    def __init__(self,x,y,width,height,name=None):
        super().__init__()
        self.rect=pygame.Rect(x,y,width,height)
        self.image=pygame.Surface((width, height),pygame.SRCALPHA)
        self.width=width
        self.height=height
        self.x=x
        self.y=y
        self.name=name
    def draw(self,win:pygame.Surface):
        win.blit(self.image,(self.rect.x,self.rect.y))

class Block(Object):
    def __init__(self, x, y, width, height,image:pygame.Surface):
        super().__init__(x, y, width, height)
        surface=pygame.Surface((width,height),pygame.SRCALPHA,32)
        rect=pygame.Rect(0,0,width,height)
        surface.blit(image,(0,0),rect)
        block=surface
        self.image.blit(block,(0,0))
        self.mask=pygame.mask.from_surface(self.image)
    def get_block_info(self):
        block_tiles=math.ceil(SCREEN_WIDTH / self.rect.width ) + 1
        return block_tiles,self.rect.width