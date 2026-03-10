
from entities.player import Character


class Enemy(Character):
    def __init__(self, x, y, width, height, dir, sprite_name, animations):
        super().__init__(x, y, width, height, dir, sprite_name, animations)
        self.direction='left'
        self.moveCount=1
        self.ACCELERATION=2
        self.near_me=False
        self.change_direction=1
        self.max_hp=3
        self.hp=self.max_hp
        self.damge_no=1
    
    def enemy_ai(self,player:Character):
        if (player.direction=='left' and player.rect.x>self.rect.x) or (player.direction=='right' and player.rect.x>self.rect.x):
            self.direction='right'
            self.x_vel=0
            self.moveCount=2
            self.mode=None
            if not self.near_me and player.rect.x-self.rect.x<=300 and player.rect.x-self.rect.x>=80:
                print(f'self.x_vel : {self.x_vel}')
                print("hello r 1")
                self.move_right(self.ACCELERATION)
                self.near_me=True
            elif player.rect.x-self.rect.x<=70:
                print(f"player.rect.x-self.rect.x : {player.rect.x-self.rect.x}")
                self.x_vel=0
                if not player.is_jumping and self.hp>0:
                    self.mode='attack'
                else:
                    self.mode=None
            elif self.near_me:
                print(f'self.x_vel : {self.x_vel}')
                # print("hello r 2")
                self.move_right(self.ACCELERATION)
            else:
                self.x_vel=0
                # pass
        else:
            self.direction='left'
            self.x_vel=0
            self.moveCount=2
            self.mode=None
            if not self.near_me and self.rect.x-player.rect.x<=150 and self.rect.x-player.rect.x>=50:
                #print(f'self.x_vel : {self.x_vel} self.rect.x-player.rect.x {self.rect.x-player.rect.x}')
                # print("hello l 1")
                self.move_left(self.ACCELERATION)
                self.near_me=True
            elif self.rect.x-player.rect.x<=40 and self.rect.x-player.rect.x>=20:
                # print("hello rj")
                self.x_vel=0
                if not player.is_jumping and self.hp>0:
                    self.mode='attack'
                else:
                    self.mode=None
            elif self.near_me:
                print(f'self.x_vel : {self.x_vel}')
                # print("hello l 2")
                self.move_left(self.ACCELERATION)
            else:
                self.x_vel=0