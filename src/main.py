from typing import Dict, List

import pygame
import os
import math
import pathlib

# pygame setup
pygame.init()
SCREEN_WIDTH,SCREEN_HEIGHT=1280,600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Survival Game")
clock = pygame.time.Clock()
running = True
SCROLL=0
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

def load_sprite(width:int,height:int)->Dict[str,List[pygame.Surface]]:
    char_animation=['idle','jump-all','jump','run','attack','run','dead']
    all_sprites:Dict[str,List[pygame.Surface]]={}
    for animation in char_animation:
        sprites=[]
        sprite=load_image(['assets','character'],f'character-{animation}.png')
        for i in range(sprite.get_width() // width):
            surface=pygame.Surface((width,height),pygame.SRCALPHA,32)
            rect=pygame.Rect(i*width,0,width,height)
            surface.blit(sprite,(0,0),rect)
            sprites.append(pygame.transform.scale2x(surface))
            all_sprites[animation]=sprites
    
    return all_sprites

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


class Charater(pygame.sprite.Sprite):
    COLOR=(255,0,0)
    ACCELERATION=3
    GRAVITY=1
    SPRITES=load_sprite(36,64)
    def __init__(self,x,y,width,height):
        super().__init__()
        self.rect=pygame.Rect(x,y,width,height)
        self.x_vel=0
        self.y_vel=0
        self.mask=None
        self.image=None
        # self.x=x
        # self.y=y
        # self.width=width
        # self.height=height
        self.direction='left'
        self.animation_count=0
        self.fall_count=0
        self.jump_count=0
        self.agjust_point=[0,0]
        self.is_grounded=False
    def move(self,dx,dy):
        print(f'self.jump_count : {self.jump_count} fall_count : {self.fall_count } x_vel : {self.x_vel} y_vel {self.y_vel} self.rect.x: {self.rect.x} self.rect.y: {self.rect.y} dx {dx} dy {dy}')
        self.rect.x+=dx
        self.rect.y+=dy
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
        if not self.is_grounded:
            self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)
            self.fall_count+=1

    def loop(self,fps): # Physics of player
        self.add_gravity(fps)
        self.move(self.x_vel,self.y_vel)
        self.updated_char()
    def landed(self):
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0
        self.is_grounded = True
    def hit_head(self):
        self.count = 0
        self.y_vel *= -1
        self.is_grounded = False
    def update(self):
        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)
    def collided(self, blocks:list[Block]):
        grounded = False  # Track if touching any ground block this frame
        for block in blocks:
            if self.mask and block.mask:
                if pygame.sprite.collide_mask(self, block):
                    if self.y_vel > 0:
                        print(f'self.y_vel : {self.y_vel} self.rect.bottom : {self.rect.bottom} block.rect.top : {block.rect.top}')
                        self.landed()
                        grounded = True
        # If not touching any block and was grounded, now falling
        if not grounded and self.is_grounded and self.y_vel >= 0:
            self.is_grounded = False
    def jump(self):
        if self.jump_count == 0:   # only if on ground
            self.y_vel = -10
            self.x_vel+=10
            self.jump_count = 1
            self.fall_count = 0
            self.is_grounded = False
    def updated_char(self):
        image=self.image
        # player.x_vel=0
        if self.y_vel < 0: # jumping up
            image=self.SPRITES['jump-all'][math.ceil((self.animation_count // 10)%6)]
        elif self.y_vel > 2:  # falling
            image=self.SPRITES['jump-all'][math.ceil((self.animation_count // 10)%(len(self.SPRITES['run'])-6))]
            #agjust_point[1]=-(12*2)
        elif self.x_vel != 0:
            image=self.SPRITES['run'][math.ceil((self.animation_count // 10)%len(self.SPRITES['run']))]
            if self.direction=='left':
                image=pygame.transform.flip(self.SPRITES['run'][math.ceil((self.animation_count // 5)%len(self.SPRITES['run']))],True,False)
        else:
            image=self.SPRITES['idle'][math.ceil((self.animation_count // 10)%len(self.SPRITES['idle']))]
        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.size = self.image.get_size()
        self.animation_count+=1
        self.update()

    def draw(self,win:pygame.Surface,fps): # render on screen
        win.blit(self.image,(self.rect.x,self.rect.y))
        
            
def handle_move(FPS,player:Charater):
    event = pygame.key.get_pressed()
    player.x_vel=0
    if event[pygame.K_RIGHT]:       
        player.move_right(Charater.ACCELERATION)
    if event[pygame.K_LEFT]:       
        player.move_left(Charater.ACCELERATION)
    if event[pygame.K_UP]:
        player.jump()


def get_background(bg_img:pygame.Surface):
    bg_width=bg_img.get_width()
    tiles=math.ceil(SCREEN_WIDTH / bg_width ) + 1
    return tiles,bg_width
    
def draw(fps,bg_image,player:Charater,blocks):
    global screen,SCROLL
    tiles,width=get_background(bg_image)
    for i in range(0,tiles):
        screen.blit(bg_image,(i*width+SCROLL,0))
    for block in blocks:
        block.draw(screen)
    player.draw(screen,fps)
    pygame.display.update()
    # scrolling effect like parallex effect 
    # SCROLL-=5
    # if abs(SCROLL) > width:
    #     SCROLL=0




def main():
    global running
    player=Charater(100,100,32,32)

    blocks = []

    BLOCK_SIZE = 95
    ground_img = load_image(['assets','tiles'], 'tileset_ground.png')

    for i in range(2):  # create 15 blocks
        block = Block(((i * BLOCK_SIZE)-(10*i+1)), SCREEN_HEIGHT-BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE, ground_img)
        blocks.append(block)
    for i in range(15):  # create 15 blocks
        block = Block(((i * BLOCK_SIZE)-(10*i+1)), SCREEN_HEIGHT-BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE, ground_img)
        blocks.append(block)

    while running:
        FPS=60 # limits FPS to 60
        COLOR=(255,255,255)
        
        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                running = False

        # fill the screen with a color to wipe away anything from last frame
        screen.fill(COLOR)
        bg_image=load_image(['assets','background'],'Background.png')
        
        handle_move(FPS,player,)
        player.loop(FPS)
        player.collided(blocks)
        draw(FPS,bg_image,player,blocks)
        
        
        clock.tick(FPS)  

    pygame.quit()

if __name__ == "__main__":
    main()

