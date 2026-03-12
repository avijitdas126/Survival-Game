import math

import pygame

from core.utils import SCREEN_WIDTH

class Object(pygame.sprite.Sprite):
    def __init__(self,x,y,width,height,tile,name=None):
        super().__init__()
        self.rect=pygame.Rect(x,y,width,height)
        self.image=tile
        self.width=width
        self.height=height
        self.x=x
        self.y=y
        self.name=name

class Block(Object):
    def __init__(self, x, y, width, height,tile:pygame.Surface):
        super().__init__(x, y, width, height,tile)
        self.mask=pygame.mask.from_surface(self.image)


