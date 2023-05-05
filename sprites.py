# Sprite classes for platform game
import pygame as pg
from settings import *
import random
FPS = 30
class Spritesheet:
    def __init__(self, filemane):
        self.spritesheet = pg.image.load(filemane).convert()

    def get_image(self, x, y, width, height):
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        return image
        

class Player(pg.sprite.Sprite):
    def __init__(self, game, loc, wallPos, bits, ba):
        self._layer = 2
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.walls = wallPos
        self.bit_list = bits
        self.bitAmount = ba
        self.load_images()
        self.image = self.right_frames[0]
        self.rect = self.image.get_rect()
        self.rect.x = loc[0]
        self.rect.y = loc[1]
        self.key = pg.key.get_pressed()
        self.bits_collected = 0
        self.queue = []
        self.move = 2
        self.move_x = 0
        self.move_y = 0
        self.key_pressed = []
        self.queue = []
        self.last_update = 0
        self.current_frame = 0

    def load_images(self):
        self.left_frames = [pg.transform.scale(self.game.pspritesheet.get_image(9, 11, 12, 12), (20, 20)), pg.transform.rotate(pg.transform.scale(self.game.pspritesheet.get_image(40, 11, 12, 12), (20, 20)), 180), pg.transform.rotate(pg.transform.scale(self.game.pspritesheet.get_image(9, 43, 12, 12), (20,20)),180), pg.transform.rotate(pg.transform.scale(self.game.pspritesheet.get_image(40, 43, 12, 12), (20, 20)), 180)]
        self.right_frames = [pg.transform.scale(self.game.pspritesheet.get_image(9, 11, 12, 12), (20,20)), pg.transform.scale(self.game.pspritesheet.get_image(40, 11, 12, 12), (20,20)),  pg.transform.scale(self.game.pspritesheet.get_image(9, 43, 12, 12), (20,20)), pg.transform.scale(self.game.pspritesheet.get_image(40, 43, 12, 12), (20,20))]
        self.up_frames = [pg.transform.scale(self.game.pspritesheet.get_image(9, 11, 12, 12), (20, 20)), pg.transform.rotate(pg.transform.scale(self.game.pspritesheet.get_image(40, 11, 12, 12), (20, 20)), 90), pg.transform.rotate(pg.transform.scale(self.game.pspritesheet.get_image(9, 43, 12, 12), (20,20)),90), pg.transform.rotate(pg.transform.scale(self.game.pspritesheet.get_image(40, 43, 12, 12), (20, 20)), 90)]
        self.down_frames = [pg.transform.scale(self.game.pspritesheet.get_image(9, 11, 12, 12), (20, 20)), pg.transform.rotate(pg.transform.scale(self.game.pspritesheet.get_image(40, 11, 12, 12), (20, 20)), 270), pg.transform.rotate(pg.transform.scale(self.game.pspritesheet.get_image(9, 43, 12, 12), (20,20)),270), pg.transform.rotate(pg.transform.scale(self.game.pspritesheet.get_image(40, 43, 12, 12), (20, 20)), 270)]
        for image in self.left_frames:
            image.set_colorkey(BLACK)
        for image in self.right_frames:
            image.set_colorkey(BLACK)
        for image in self.up_frames:
            image.set_colorkey(BLACK)
        for image in self.down_frames:
            image.set_colorkey(BLACK)

    def animate(self, y, x):
        now = pg.time.get_ticks()
        if self.move_x == -self.move:
            self.sprite_frames = self.left_frames
        elif self.move_x == self.move:
            self.sprite_frames = self.right_frames
        elif self.move_y == self.move:
            self.sprite_frames = self.down_frames
        elif self.move_y == -self.move:
            self.sprite_frames = self.up_frames
        else:
            self.sprite_frames = [self.right_frames[0]]
        if now - self.last_update > 100:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.sprite_frames)
            self.image = self.sprite_frames[self.current_frame]
            self.rect = self.image.get_rect()
            self.rect.y = y
            self.rect.x = x

    def update(self):
##        self.key = pg.key.get_pressed()
##        if self.key[pg.K_LEFT]:
##            self.rect.x -= 20
##        elif self.key[pg.K_RIGHT]:
##            self.rect.x += 20
##        elif self.key[pg.K_UP]:
##            self.rect.y -= 20
##        elif self.key[pg.K_DOWN]:
##            self.rect.y += 20
##        if self.rect.x == 460:
##            self.rect.x = 0
##        if self.rect.x == -20:
##            self.rect.x = 440
##        if pg.sprite.spritecollide(self, self.walls, False):
##            if self.key[pg.K_LEFT]:
##                self.rect.x += 20
##            elif self.key[pg.K_RIGHT]:
##                self.rect.x -= 20
##            elif self.key[pg.K_UP]:
##                self.rect.y += 20
##            elif self.key[pg.K_DOWN]:
##                self.rect.y -= 20
        key = pg.key.get_pressed()
        if len(self.queue) < 1:
            if key[pg.K_LEFT]:
                self.queue.append(key)
            elif key[pg.K_RIGHT]:
                self.queue.append(key)
            elif key[pg.K_UP]:
                self.queue.append(key)
            elif key[pg.K_DOWN]:
                self.queue.append(key)
        if self.rect.y % 20 == 0 and self.rect.x % 20 == 0:
            if len(self.queue) > 0:
                if self.queue[-1][pg.K_LEFT]:
                    self.rect.x -= 2
                    if pg.sprite.spritecollide(self, self.walls, False):
                        self.rect.x += 2
                        self.queue = []
                    else:
                        self.key_pressed.append(self.queue[-1])
                        self.queue = []
                        self.move_x = -self.move
                        self.move_y = 0
                elif self.queue[-1][pg.K_RIGHT]:
                    self.rect.x += 2
                    if pg.sprite.spritecollide(self, self.walls, False):
                        self.rect.x -= 2
                        self.queue = []
                    else:
                        self.key_pressed.append(self.queue[-1])
                        self.queue = []
                        self.move_y = 0
                        self.move_x = self.move
                elif self.queue[-1][pg.K_UP]:
                    self.rect.y -= 2
                    if pg.sprite.spritecollide(self, self.walls, False):
                        self.rect.y += 2
                        self.queue = []
                    else:
                        self.key_pressed.append(self.queue[-1])
                        self.queue = []
                        self.move_y = -self.move
                        self.move_x = 0
                elif self.queue[-1][pg.K_DOWN]:
                    self.rect.y += 2
                    if pg.sprite.spritecollide(self, self.walls, False):
                        self.rect.y -= 2
                        self.queue = []
                    else:
                        self.key_pressed.append(self.queue[-1])
                        self.queue = []
                        self.move_y = self.move
                        self.move_x = 0
        self.animate(self.rect.y, self.rect.x)
        self.rect.x += self.move_x
        self.rect.y += self.move_y
        if self.rect.x == 440:
            self.rect.x = 2
        elif self.rect.x == 0:
            self.rect.x = 438
        if pg.sprite.spritecollide(self, self.walls, False):
            if self.key_pressed[-1][pg.K_LEFT]:
                self.rect.x += 2
                self.move_y = 0
                self.move_x = 0
            elif self.key_pressed[-1][pg.K_RIGHT]:
                self.rect.x -= 2
                self.move_y = 0
                self.move_x = 0
            elif self.key_pressed[-1][pg.K_UP]:
                self.rect.y += 2
                self.move_y = 0
                self.move_x = 0
            else:
                self.rect.y -= 2
                self.move_y = 0
                self.move_x = 0
        
        if pg.sprite.spritecollide(self, self.bit_list, True):
            self.bits_collected += 1
        if self.bits_collected == self.bitAmount:
            pass
            #print("WINNER!")


class Wall(pg.sprite.Sprite):
    def __init__(self, game, pos, color=BLUE):
        self._layer = 0
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.size = 20
        self.image = pg.Surface((self.size, self.size))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

class Entrance(pg.sprite.Sprite):
    def __init__(self, game, pos):
        self._layer = 0
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.size = 20
        self.image = pg.image.load('Entrance.png').convert()
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

class Bit(pg.sprite.Sprite):
    def __init__(self, game, pos):
        self._layer = 0
        self.groups = game.all_sprites, game.bit_list
        pg.sprite.Sprite.__init__(self, self.groups)
        self.size = 10
        self.image = pg.image.load('Bit.png').convert()
        self.rect = self.image.get_rect()
        self.rect.x = pos[0] + self.size / 2
        self.rect.y = pos[1] + self.size / 2

class GhostRED(pg.sprite.Sprite):
    def __init__(self, pos, game):
        self._layer = 1
        self.groups = game.all_sprites, game.ghost_list
        pg.sprite.Sprite.__init__(self, self.groups)
        self.size = 10
        self.last_update = 0
        self.current_frame = 0
        self.game = game
        self.load_images()
        self.move = 2
##        self.image = pg.Surface((self.size, self.size))
##        self.image.fill(RED)
        self.image = self.down_frames[1]
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.xPos = 0
        self.yPos = 0
        self.wt = []
        self.wb = []
        self.wl = []
        self.wr = []
        self.last_move = ['x', -1]
        self.lpos = [0]


    def load_images(self):
        self.left_frames = [self.game.rgspritesheet.get_image(148, 57.5, 20, 20), self.game.rgspritesheet.get_image(20, 57.5, 20, 20)]
        self.right_frames = [self.game.rgspritesheet.get_image(148, 185, 20, 20), self.game.rgspritesheet.get_image(276, 185, 20, 20)]
        self.up_frames = [self.game.rgspritesheet.get_image(20, 185, 20, 20), self.game.rgspritesheet.get_image(276, 57.5, 20, 20)]
        self.down_frames = [self.game.rgspritesheet.get_image(20, 315, 20, 20), self.game.rgspritesheet.get_image(148, 315, 20, 20)]
        for image in self.left_frames:
            image.set_colorkey(BLACK)
        for image in self.right_frames:
            image.set_colorkey(BLACK)
        for image in self.up_frames:
            image.set_colorkey(BLACK)
        for image in self.down_frames:
            image.set_colorkey(BLACK)
            
    def animate(self, y, x):
        now = pg.time.get_ticks()
        if self.last_move == ['x', -1]:
            self.sprite_frames = self.left_frames
        elif self.last_move == ['x', 1]:
            self.sprite_frames = self.right_frames
        elif self.last_move == ['y', 1]:
            self.sprite_frames = self.down_frames
        else:
            self.sprite_frames = self.up_frames
        if now - self.last_update > 100:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.sprite_frames)
            self.image = self.sprite_frames[self.current_frame]
            self.rect = self.image.get_rect()
            self.rect.y = y
            self.rect.x = x
        

    def update(self):
        self.coord = random.choice(['x', 'y'])
        self.movement = random.choice([20, -20])
        self.side = {'bottom':self.rect.bottom, 'top':self.rect.top, 'left':self.rect.left, 'right':self.rect.right}
        self.lpos.append((self.rect.x, self.rect.y))
        #BOTTOM, TOP, LEFT
        if [self.side['bottom'], self.rect.x] in self.wt and [self.side['top'], self.rect.x] in self.wb and [self.side['left'], self.rect.y] in self.wr:
            self.last_move = ['x', 1]
            self.xPos = self.move
            self.yPos = 0
            #print("N1")

        #BOTTOM, TOP, RIGHT
        elif [self.side['bottom'], self.rect.x] in self.wt and [self.side['top'], self.rect.x] in self.wb and [self.side['right'], self.rect.y] in self.wl:
            self.last_move = ['x', -1]
            self.xPos = -self.move
            self.yPos = 0
            #print("N2")

##        #BOTTOM, RIGHT, LEFT
##        elif [self.side['bottom'], self.xPos] in self.wt and [self.side['left'], self.yPos] in self.wr and [self.side['right'], self.yPos] in self.wl:
##            self.last_move = ['y', -1]
##            self.yPos -= 20
##            #print("N3")
##
##        #TOP, RIGHT, LEFT
##        elif [self.side['top'], self.xPos] in self.wb and [self.side['left'], self.yPos] in self.wr and [self.side['right'], self.yPos] in self.wl:
##            self.last_move = ['y', 1]
##            self.yPos += 20
##            #print("N4")
        
        # BOTTOM, TOP
        if [self.side['bottom'], self.rect.x] in self.wt and [self.side['top'], self.rect.x] in self.wb:
            if self.last_move[1] == 1:
                self.xPos = self.move
                self.yPos = 0
                self.last_move = ['x', 1]
            elif self.last_move[1] == -1:
                self.last_move = ['x', -1]
                self.xPos = -self.move
                self.yPos = 0
            else:
                self.last_move = ['x', self.movement/20]
                self.xPos = self.movement/20 * self.move
                self.yPos = 0
            #print("BOTTOM, TOP")
##            #print(self.xPos)
##            #print(self.yPos)
            
        
        # BOTTOM, LEFT
        elif [self.side['bottom'], self.rect.x] in self.wt and [self.side['left'], self.rect.y] in self.wr:
            if self.last_move[0] == 'x':
                self.yPos = -self.move
                self.xPos = 0
                self.last_move = ['y', -1]
            elif self.last_move[0] == 'y':
                self.xPos = self.move
                self.yPos = 0
                self.last_move = ['x', 1]
            #print("BOTTOM, LEFT")
##            #print(self.xPos)
##            #print(self.yPos)


        # BOTTOM, RIGHT
        elif [self.side['bottom'], self.rect.x] in self.wt and [self.side['right'], self.rect.y] in self.wl:
            if self.last_move[0] == 'x':
                self.yPos = -self.move
                self.xPos = 0
                self.last_move = ['y', -1]
            elif self.last_move[0] == 'y':
                self.xPos = -self.move
                self.yPos = 0
                self.last_move = ['x', -1]
            #print("BOTTOM, RIGHT")
##            #print(self.xPos)
##            #print(self.yPos)

        # TOP, LEFT
        elif [self.side['top'], self.rect.x] in self.wb and [self.side['left'], self.rect.y] in self.wr:
            if self.last_move[0] == 'x':
                self.yPos = self.move
                self.xPos = 0
                self.last_move = ['y', 1]
            elif self.last_move[0] == 'y':
                self.xPos = self.move
                self.yPos = 0
                self.last_move = ['x', 1]
            #print("TOP LEFT")
##            #print(self.xPos)
##            #print(self.yPos)
        
        # TOP, RIGHT
        elif [self.side['top'], self.rect.x] in self.wb and [self.side['right'], self.rect.y] in self.wl:
            if self.last_move[0] == 'x':
                self.yPos = self.move
                self.xPos = 0
                self.last_move = ['y', 1]
            elif self.last_move[0] == 'y':
                self.xPos = -self.move
                self.yPos = 0
                self.last_move = ['x', -1]
            #print("TOP, RIGHT")
##            #print(self.xPos)
##            #print(self.yPos)

        # LEFT, RIGHT
        elif [self.side['left'], self.rect.y] in self.wr and [self.side['right'], self.rect.y] in self.wl:
            if self.last_move[1] == 1:
                self.yPos = self.move
                self.xPos = 0
                self.last_move = ['y', 1]
            elif self.last_move[1] == -1:
                self.yPos = -self.move
                self.xPos = 0
                self.last_move = ['y', -1]
            #print("LEFT, RIGHT")
            #print(str(self.rect.x)+' ,'+str(self.rect.y)+':'+str(self.xPos)+' ,'+str(self.yPos))
##            #print(self.xPos)
##            #print(self.yPos)

        # BOTTOM
        elif [self.side['bottom'], self.rect.x] in self.wt:
            if self.last_move[0] == 'x':
                if self.last_move[1] == 1:
                    if self.coord == 'x':
                        self.last_move = ['x', 1]
                        self.xPos = self.move
                        self.yPos = 0
                    elif self.coord == 'y':
                        self.last_move = ['y', -1]
                        self.yPos = -self.move
                        self.xPos = 0
                elif self.last_move[1] == -1:
                    if self.coord == 'x':
                        self.last_move = ['x', -1]
                        self.xPos = -self.move
                        self.yPos = 0
                    elif self.coord == 'y':
                        self.last_move = ['y', -1]
                        self.yPos = -self.move
                        self.xPos = 0
            elif self.last_move[0] == 'y':
                self.last_move = ['x', self.movement/20]
                self.xPos = self.movement/20*self.move
                self.yPos = 0
            #print("BOTTOM")
##            #print(self.xPos)
##            #print(self.yPos)
            
        # TOP
        elif [self.side['top'], self.rect.x] in self.wb:
            if self.last_move[0] == 'x':
                if self.last_move[1] == 1:
                    if self.coord == 'x':
                        self.last_move = ['x', 1]
                        self.xPos = self.move
                        self.yPos = 0
                    elif self.coord == 'y':
                        self.last_move = ['y', 1]
                        self.yPos = self.move
                        self.xPos = 0
                elif self.last_move[1] == -1:
                    if self.coord == 'x':
                        self.last_move = ['x', -1]
                        self.xPos = -self.move
                        self.yPos = 0
                    elif self.coord == 'y':
                        self.last_move = ['y', 1]
                        self.yPos = self.move
                        self.xPos = 0
            elif self.last_move[0] == 'y':
                self.last_move = ['x', self.movement/20]
                self.xPos = self.movement/20 *self.move
                self.yPos = 0
            #print("TOP")
##            #print(self.xPos)
##            #print(self.yPos)
            
        # LEFT
        elif [self.side['left'], self.rect.y] in self.wr:
            if self.last_move[0] == 'y':
                if self.last_move[1] == 1:
                    if self.coord == 'y':
                        self.last_move = ['y', 1]
                        self.yPos = self.move
                        self.xPos = 0
                    elif self.coord == 'x':
                        self.last_move = ['x', 1]
                        self.xPos = self.move
                        self.yPos = 0
                elif self.last_move[1] == -1:
                    if self.coord == 'x':
                        self.last_move = ['x', 1]
                        self.xPos = self.move
                        self.yPos = 0
                    elif self.coord == 'y':
                        self.last_move = ['y', -1]
                        self.yPos = -self.move
                        self.xPos = 0
            elif self.last_move[0] == 'x':
                self.last_move = ['y', self.movement/20]
                self.yPos = self.movement/20 * self.move
                self.xPos = 0
            #print("LEFT")
##            #print(self.xPos)
##            #print(self.yPos)
            
        # RIGHT
        elif [self.side['right'], self.rect.y] in self.wl:
            if self.last_move[0] == 'y':
                if self.last_move[1] == 1:
                    if self.coord == 'y':
                        self.last_move = ['y', 1]
                        self.yPos = self.move
                        self.xPos = 0
                    elif self.coord == 'x':
                        self.last_move = ['x', -1]
                        self.xPos = -self.move
                        self.yPos = 0
                elif self.last_move[1] == -1:
                    if self.coord == 'x':
                        self.last_move = ['x', -1]
                        self.xPos = -self.move
                        self.yPos = 0
                    elif self.coord == 'y':
                        self.last_move = ['y', -1]
                        self.yPos = -self.move
                        self.xPos = 0
            elif self.last_move[0] == 'x':
                self.last_move = ['y', self.movement/20]
                self.yPos = self.movement/20 * self.move
                self.xPos = 0
            #print("RIGHT")
##            #print(self.xPos)
##            #print(self.yPos)

        #NONE
##        else:
##            if self.last_move[0] == 'y':
##                if self.last_move[1] == 1:
##                    if self.coord == 'y':
##                        self.last_move = ['y', 1]
##                        self.yPos = self.move
##                        self.xPOs = 0
##                    elif self.coord == 'x':
##                        self.last_move = ['x', -1]
##                        self.xPos = -self.move
##                        self.yPos = 0
##                elif self.last_move[1] == -1:
##                    if self.coord == 'x':
##                        self.last_move = ['x', -1]
##                        self.xPos = -self.move
##                        self.yPos = 0
##                    elif self.coord == 'y':
##                        self.last_move = ['y', -1]
##                        self.yPos = -self.move
##                        self.xPos = 0
##            elif self.last_move[0] == 'x':
##                if self.last_move[1] == 1:
##                    if self.coord == 'y':
##                        self.last_move = ['y', 1]
##                        self.yPos = self.move
##                        self.xPos = 0
##                    elif self.coord == 'x':
##                        self.last_move = ['x', 1]
##                        self.xPos = self.move
##                        self.yPos = 0
##                elif self.last_move[1] == -1:
##                    if self.coord == 'x':
##                        self.last_move = ['x', -1]
##                        self.xPos = -self.move
##                        self.yPos = 0
##                    elif self.coord == 'y':
##                        self.last_move = ['y', -1]
##                        self.yPos = -self.move
##                        self.xPos = 0
##            #print("NONE")
##            #print(self.xPos)
##            #print(self.yPos)
        self.animate(self.rect.y, self.rect.x)
        self.rect.y += self.yPos
        self.rect.x += self.xPos
        

class GhostORANGE(pg.sprite.Sprite):
    def __init__(self, pos, game):
        self._layer = 1
        self.groups = game.all_sprites, game.ghost_list
        pg.sprite.Sprite.__init__(self, self.groups)
        self.size = 10
        self.last_update = 0
        self.current_frame = 0
        self.game = game
        self.load_images()
        self.move = 2
##        self.image = pg.Surface((self.size, self.size))
##        self.image.fill(RED)
        self.image = self.down_frames[1]
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.xPos = 0
        self.yPos = 0
        self.wt = []
        self.wb = []
        self.wl = []
        self.wr = []
        self.last_move = ['x', -1]
        self.lpos = [0]
        self.not_spawn = False


    def load_images(self):
        self.left_frames = [self.game.ogspritesheet.get_image(148, 57.5, 20, 20), self.game.ogspritesheet.get_image(20, 57.5, 20, 20)]
        self.right_frames = [self.game.ogspritesheet.get_image(148, 185, 20, 20), self.game.ogspritesheet.get_image(276, 185, 20, 20)]
        self.up_frames = [self.game.ogspritesheet.get_image(20, 185, 20, 20), self.game.ogspritesheet.get_image(276, 57.5, 20, 20)]
        self.down_frames = [self.game.ogspritesheet.get_image(20, 315, 20, 20), self.game.ogspritesheet.get_image(148, 315, 20, 20)]
        for image in self.left_frames:
            image.set_colorkey(BLACK)
        for image in self.right_frames:
            image.set_colorkey(BLACK)
        for image in self.up_frames:
            image.set_colorkey(BLACK)
        for image in self.down_frames:
            image.set_colorkey(BLACK)
            
    def animate(self, y, x):
        now = pg.time.get_ticks()
        if self.last_move == ['x', -1]:
            self.sprite_frames = self.left_frames
        elif self.last_move == ['x', 1]:
            self.sprite_frames = self.right_frames
        elif self.last_move == ['y', 1]:
            self.sprite_frames = self.down_frames
        else:
            self.sprite_frames = self.up_frames
        if now - self.last_update > 100:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.sprite_frames)
            self.image = self.sprite_frames[self.current_frame]
            self.rect = self.image.get_rect()
            self.rect.y = y
            self.rect.x = x
        

    def update(self):
        self.coord = random.choice(['x', 'y'])
        self.movement = random.choice([20, -20])
        self.side = {'bottom':self.rect.bottom, 'top':self.rect.top, 'left':self.rect.left, 'right':self.rect.right}
        self.lpos.append((self.rect.x, self.rect.y))
        if self.rect.x == 220 and self.rect.y == 160:
            self.not_spawn = True
        #BOTTOM, TOP, LEFT
        if [self.side['bottom'], self.rect.x] in self.wt and [self.side['top'], self.rect.x] in self.wb and [self.side['left'], self.rect.y] in self.wr:
            self.last_move = ['x', 1]
            self.xPos = self.move
            self.yPos = 0
            #print("N1")

        #BOTTOM, TOP, RIGHT
        elif [self.side['bottom'], self.rect.x] in self.wt and [self.side['top'], self.rect.x] in self.wb and [self.side['right'], self.rect.y] in self.wl:
            self.last_move = ['x', -1]
            self.xPos = -self.move
            self.yPos = 0
            #print("N2")

##        #BOTTOM, RIGHT, LEFT
##        elif [self.side['bottom'], self.xPos] in self.wt and [self.side['left'], self.yPos] in self.wr and [self.side['right'], self.yPos] in self.wl:
##            self.last_move = ['y', -1]
##            self.yPos -= 20
##            #print("N3")
##
##        #TOP, RIGHT, LEFT
##        elif [self.side['top'], self.xPos] in self.wb and [self.side['left'], self.yPos] in self.wr and [self.side['right'], self.yPos] in self.wl:
##            self.last_move = ['y', 1]
##            self.yPos += 20
##            #print("N4")
        
        # BOTTOM, TOP
        if [self.side['bottom'], self.rect.x] in self.wt and [self.side['top'], self.rect.x] in self.wb:
            if self.last_move[1] == 1:
                self.xPos = self.move
                self.yPos = 0
                self.last_move = ['x', 1]
            elif self.last_move[1] == -1:
                #print('HAHAHAHAHAHAH')
                self.last_move = ['x', -1]
                self.xPos = -self.move
                self.yPos = 0
            else:
                self.last_move = ['x', self.movement/20]
                self.xPos = self.movement/20 * self.move
                self.yPos = 0
            #print("BOTTOM, TOP")
##            #print(self.xPos)
##            #print(self.yPos)
            
        
        # BOTTOM, LEFT
        elif [self.side['bottom'], self.rect.x] in self.wt and [self.side['left'], self.rect.y] in self.wr:
            if self.last_move[0] == 'x':
                self.yPos = -self.move
                self.xPos = 0
                self.last_move = ['y', -1]
            elif self.last_move[0] == 'y':
                self.xPos = self.move
                self.yPos = 0
                self.last_move = ['x', 1]
            #print("BOTTOM, LEFT")
##            #print(self.xPos)
##            #print(self.yPos)


        # BOTTOM, RIGHT
        elif [self.side['bottom'], self.rect.x] in self.wt and [self.side['right'], self.rect.y] in self.wl:
            if self.last_move[0] == 'x':
                self.yPos = -self.move
                self.xPos = 0
                self.last_move = ['y', -1]
            elif self.last_move[0] == 'y':
                self.xPos = -self.move
                self.yPos = 0
                self.last_move = ['x', -1]
            #print("BOTTOM, RIGHT")
##            #print(self.xPos)
##            #print(self.yPos)

        # TOP, LEFT
        elif [self.side['top'], self.rect.x] in self.wb and [self.side['left'], self.rect.y] in self.wr:
            if self.last_move[0] == 'x':
                self.yPos = self.move
                self.xPos = 0
                self.last_move = ['y', 1]
            elif self.last_move[0] == 'y':
                self.xPos = self.move
                self.yPos = 0
                self.last_move = ['x', 1]
            #print("TOP LEFT")
##            #print(self.xPos)
##            #print(self.yPos)
        
        # TOP, RIGHT
        elif [self.side['top'], self.rect.x] in self.wb and [self.side['right'], self.rect.y] in self.wl:
            if self.last_move[0] == 'x':
                self.yPos = self.move
                self.xPos = 0
                self.last_move = ['y', 1]
            elif self.last_move[0] == 'y':
                self.xPos = -self.move
                self.yPos = 0
                self.last_move = ['x', -1]
            #print("TOP, RIGHT")
##            #print(self.xPos)
##            #print(self.yPos)

        # LEFT, RIGHT
        elif [self.side['left'], self.rect.y] in self.wr and [self.side['right'], self.rect.y] in self.wl:
            if self.last_move[1] == 1:
                self.yPos = self.move
                self.xPos = 0
                self.last_move = ['y', 1]
            elif self.last_move[1] == -1:
                self.yPos = -self.move
                self.xPos = 0
                self.last_move = ['y', -1]
            #print("LEFT, RIGHT")
            #print(str(self.rect.x)+' ,'+str(self.rect.y)+':'+str(self.xPos)+' ,'+str(self.yPos))
##            #print(self.xPos)
##            #print(self.yPos)

        # BOTTOM
        elif [self.side['bottom'], self.rect.x] in self.wt:
            if self.last_move[0] == 'x':
                if self.last_move[1] == 1:
                    if self.coord == 'x':
                        self.last_move = ['x', 1]
                        self.xPos = self.move
                        self.yPos = 0
                    elif self.coord == 'y':
                        self.last_move = ['y', -1]
                        self.yPos = -self.move
                        self.xPos = 0
                elif self.last_move[1] == -1:
                    if self.coord == 'x':
                        self.last_move = ['x', -1]
                        self.xPos = -self.move
                        self.yPos = 0
                    elif self.coord == 'y':
                        self.last_move = ['y', -1]
                        self.yPos = -self.move
                        self.xPos = 0
            elif self.last_move[0] == 'y':
                self.last_move = ['x', self.movement/20]
                self.xPos = self.movement/20*self.move
                self.yPos = 0
            #print("BOTTOM")
##            #print(self.xPos)
##            #print(self.yPos)
            
        # TOP
        elif [self.side['top'], self.rect.x] in self.wb:
            if self.last_move[0] == 'x':
                if self.last_move[1] == 1:
                    if self.coord == 'x':
                        self.last_move = ['x', 1]
                        self.xPos = self.move
                        self.yPos = 0
                    elif self.coord == 'y':
                        self.last_move = ['y', 1]
                        self.yPos = self.move
                        self.xPos = 0
                elif self.last_move[1] == -1:
                    if self.coord == 'x':
                        self.last_move = ['x', -1]
                        self.xPos = -self.move
                        self.yPos = 0
                    elif self.coord == 'y':
                        self.last_move = ['y', 1]
                        self.yPos = self.move
                        self.xPos = 0
            elif self.last_move[0] == 'y':
                self.last_move = ['x', self.movement/20]
                self.xPos = self.movement/20 *self.move
                self.yPos = 0
            #print("TOP")
##            #print(self.xPos)
##            #print(self.yPos)
            
        # LEFT
        elif [self.side['left'], self.rect.y] in self.wr:
            if self.last_move[0] == 'y':
                if self.last_move[1] == 1:
                    if self.coord == 'y':
                        self.last_move = ['y', 1]
                        self.yPos = self.move
                        self.xPos = 0
                    elif self.coord == 'x':
                        self.last_move = ['x', 1]
                        self.xPos = self.move
                        self.yPos = 0
                elif self.last_move[1] == -1:
                    if self.coord == 'x':
                        self.last_move = ['x', 1]
                        self.xPos = self.move
                        self.yPos = 0
                    elif self.coord == 'y':
                        self.last_move = ['y', -1]
                        self.yPos = -self.move
                        self.xPos = 0
            elif self.last_move[0] == 'x':
                self.last_move = ['y', self.movement/20]
                self.yPos = self.movement/20 * self.move
                self.xPos = 0
            #print("LEFT")
##            #print(self.xPos)
##            #print(self.yPos)
            
        # RIGHT
        elif [self.side['right'], self.rect.y] in self.wl:
            if self.last_move[0] == 'y':
                if self.last_move[1] == 1:
                    if self.coord == 'y':
                        self.last_move = ['y', 1]
                        self.yPos = self.move
                        self.xPos = 0
                    elif self.coord == 'x':
                        self.last_move = ['x', -1]
                        self.xPos = -self.move
                        self.yPos = 0
                elif self.last_move[1] == -1:
                    if self.coord == 'x':
                        self.last_move = ['x', -1]
                        self.xPos = -self.move
                        self.yPos = 0
                    elif self.coord == 'y':
                        self.last_move = ['y', -1]
                        self.yPos = -self.move
                        self.xPos = 0
            elif self.last_move[0] == 'x':
                self.last_move = ['y', self.movement/20]
                self.yPos = self.movement/20 * self.move
                self.xPos = 0
            #print("RIGHT")
##            #print(self.xPos)
##            #print(self.yPos)

        #NONE
##        else:
##            if self.last_move[0] == 'y':
##                if self.last_move[1] == 1:
##                    if self.coord == 'y':
##                        self.last_move = ['y', 1]
##                        self.yPos = self.move
##                        self.xPOs = 0
##                    elif self.coord == 'x':
##                        self.last_move = ['x', -1]
##                        self.xPos = -self.move
##                        self.yPos = 0
##                elif self.last_move[1] == -1:
##                    if self.coord == 'x':
##                        self.last_move = ['x', -1]
##                        self.xPos = -self.move
##                        self.yPos = 0
##                    elif self.coord == 'y':
##                        self.last_move = ['y', -1]
##                        self.yPos = -self.move
##                        self.xPos = 0
##            elif self.last_move[0] == 'x':
##                if self.last_move[1] == 1:
##                    if self.coord == 'y':
##                        self.last_move = ['y', 1]
##                        self.yPos = self.move
##                        self.xPos = 0
##                    elif self.coord == 'x':
##                        self.last_move = ['x', 1]
##                        self.xPos = self.move
##                        self.yPos = 0
##                elif self.last_move[1] == -1:
##                    if self.coord == 'x':
##                        self.last_move = ['x', -1]
##                        self.xPos = -self.move
##                        self.yPos = 0
##                    elif self.coord == 'y':
##                        self.last_move = ['y', -1]
##                        self.yPos = -self.move
##                        self.xPos = 0
##            #print("NONE")
        self.animate(self.rect.y, self.rect.x)          
        self.rect.y += self.yPos
        self.rect.x += self.xPos

class GhostPINK(pg.sprite.Sprite):
    def __init__(self, pos, game):
        self._layer = 1
        self.groups = game.all_sprites, game.ghost_list
        pg.sprite.Sprite.__init__(self, self.groups)
        self.size = 10
        self.last_update = 0
        self.current_frame = 0
        self.game = game
        self.load_images()
        self.move = 2
##        self.image = pg.Surface((self.size, self.size))
##        self.image.fill(RED)
        self.image = self.down_frames[1]
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.xPos = 0
        self.yPos = 0
        self.wt = []
        self.wb = []
        self.wl = []
        self.wr = []
        self.last_move = ['x', -1]
        self.lpos = [0]
        self.not_spawn = False


    def load_images(self):
        self.left_frames = [self.game.pgspritesheet.get_image(148, 57.5, 20, 20), self.game.pgspritesheet.get_image(20, 57.5, 20, 20)]
        self.right_frames = [self.game.pgspritesheet.get_image(148, 185, 20, 20), self.game.pgspritesheet.get_image(276, 185, 20, 20)]
        self.up_frames = [self.game.pgspritesheet.get_image(20, 185, 20, 20), self.game.pgspritesheet.get_image(276, 57.5, 20, 20)]
        self.down_frames = [self.game.pgspritesheet.get_image(20, 315, 20, 20), self.game.pgspritesheet.get_image(148, 315, 20, 20)]
        for image in self.left_frames:
            image.set_colorkey(BLACK)
        for image in self.right_frames:
            image.set_colorkey(BLACK)
        for image in self.up_frames:
            image.set_colorkey(BLACK)
        for image in self.down_frames:
            image.set_colorkey(BLACK)
            
    def animate(self, y, x):
        now = pg.time.get_ticks()
        if self.last_move == ['x', -1]:
            self.sprite_frames = self.left_frames
        elif self.last_move == ['x', 1]:
            self.sprite_frames = self.right_frames
        elif self.last_move == ['y', 1]:
            self.sprite_frames = self.down_frames
        else:
            self.sprite_frames = self.up_frames
        if now - self.last_update > 100:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.sprite_frames)
            self.image = self.sprite_frames[self.current_frame]
            self.rect = self.image.get_rect()
            self.rect.y = y
            self.rect.x = x
        

    def update(self):
        self.coord = random.choice(['x', 'y'])
        self.movement = random.choice([20, -20])
        self.side = {'bottom':self.rect.bottom, 'top':self.rect.top, 'left':self.rect.left, 'right':self.rect.right}
        self.lpos.append((self.rect.x, self.rect.y))
        if self.rect.x == 220 and self.rect.y == 160:
            self.not_spawn = True
        #BOTTOM, TOP, LEFT
        if [self.side['bottom'], self.rect.x] in self.wt and [self.side['top'], self.rect.x] in self.wb and [self.side['left'], self.rect.y] in self.wr:
            self.last_move = ['x', 1]
            self.xPos = self.move
            self.yPos = 0
            #print("N1")

        #BOTTOM, TOP, RIGHT
        elif [self.side['bottom'], self.rect.x] in self.wt and [self.side['top'], self.rect.x] in self.wb and [self.side['right'], self.rect.y] in self.wl:
            self.last_move = ['x', -1]
            self.xPos = -self.move
            self.yPos = 0
            #print("N2")

##        #BOTTOM, RIGHT, LEFT
##        elif [self.side['bottom'], self.xPos] in self.wt and [self.side['left'], self.yPos] in self.wr and [self.side['right'], self.yPos] in self.wl:
##            self.last_move = ['y', -1]
##            self.yPos -= 20
##            #print("N3")
##
##        #TOP, RIGHT, LEFT
##        elif [self.side['top'], self.xPos] in self.wb and [self.side['left'], self.yPos] in self.wr and [self.side['right'], self.yPos] in self.wl:
##            self.last_move = ['y', 1]
##            self.yPos += 20
##            #print("N4")
        
        # BOTTOM, TOP
        if [self.side['bottom'], self.rect.x] in self.wt and [self.side['top'], self.rect.x] in self.wb:
            if self.last_move[1] == 1:
                self.xPos = self.move
                self.yPos = 0
                self.last_move = ['x', 1]
            elif self.last_move[1] == -1:
                self.last_move = ['x', -1]
                self.xPos = -self.move
                self.yPos = 0
            else:
                self.last_move = ['x', self.movement/20]
                self.xPos = self.movement/20 * self.move
                self.yPos = 0
            #print("BOTTOM, TOP")
##            #print(self.xPos)
##            #print(self.yPos)
            
        
        # BOTTOM, LEFT
        elif [self.side['bottom'], self.rect.x] in self.wt and [self.side['left'], self.rect.y] in self.wr:
            if self.last_move[0] == 'x':
                self.yPos = -self.move
                self.xPos = 0
                self.last_move = ['y', -1]
            elif self.last_move[0] == 'y':
                self.xPos = self.move
                self.yPos = 0
                self.last_move = ['x', 1]
            #print("BOTTOM, LEFT")
##            #print(self.xPos)
##            #print(self.yPos)


        # BOTTOM, RIGHT
        elif [self.side['bottom'], self.rect.x] in self.wt and [self.side['right'], self.rect.y] in self.wl:
            if self.last_move[0] == 'x':
                self.yPos = -self.move
                self.xPos = 0
                self.last_move = ['y', -1]
            elif self.last_move[0] == 'y':
                self.xPos = -self.move
                self.yPos = 0
                self.last_move = ['x', -1]
            #print("BOTTOM, RIGHT")
##            #print(self.xPos)
##            #print(self.yPos)

        # TOP, LEFT
        elif [self.side['top'], self.rect.x] in self.wb and [self.side['left'], self.rect.y] in self.wr:
            if self.last_move[0] == 'x':
                self.yPos = self.move
                self.xPos = 0
                self.last_move = ['y', 1]
            elif self.last_move[0] == 'y':
                self.xPos = self.move
                self.yPos = 0
                self.last_move = ['x', 1]
            #print("TOP LEFT")
##            #print(self.xPos)
##            #print(self.yPos)
        
        # TOP, RIGHT
        elif [self.side['top'], self.rect.x] in self.wb and [self.side['right'], self.rect.y] in self.wl:
            if self.last_move[0] == 'x':
                self.yPos = self.move
                self.xPos = 0
                self.last_move = ['y', 1]
            elif self.last_move[0] == 'y':
                self.xPos = -self.move
                self.yPos = 0
                self.last_move = ['x', -1]
            #print("TOP, RIGHT")
##            #print(self.xPos)
##            #print(self.yPos)

        # LEFT, RIGHT
        elif [self.side['left'], self.rect.y] in self.wr and [self.side['right'], self.rect.y] in self.wl:
            if self.last_move[1] == 1:
                self.yPos = self.move
                self.xPos = 0
                self.last_move = ['y', 1]
            elif self.last_move[1] == -1:
                self.yPos = -self.move
                self.xPos = 0
                self.last_move = ['y', -1]
            #print("LEFT, RIGHT")
            #print(str(self.rect.x)+' ,'+str(self.rect.y)+':'+str(self.xPos)+' ,'+str(self.yPos))
##            #print(self.xPos)
##            #print(self.yPos)

        # BOTTOM
        elif [self.side['bottom'], self.rect.x] in self.wt:
            if self.last_move[0] == 'x':
                if self.last_move[1] == 1:
                    if self.coord == 'x':
                        self.last_move = ['x', 1]
                        self.xPos = self.move
                        self.yPos = 0
                    elif self.coord == 'y':
                        self.last_move = ['y', -1]
                        self.yPos = -self.move
                        self.xPos = 0
                elif self.last_move[1] == -1:
                    if self.coord == 'x':
                        self.last_move = ['x', -1]
                        self.xPos = -self.move
                        self.yPos = 0
                    elif self.coord == 'y':
                        self.last_move = ['y', -1]
                        self.yPos = -self.move
                        self.xPos = 0
            elif self.last_move[0] == 'y':
                self.last_move = ['x', self.movement/20]
                self.xPos = self.movement/20*self.move
                self.yPos = 0
            #print("BOTTOM")
##            #print(self.xPos)
##            #print(self.yPos)
            
        # TOP
        elif [self.side['top'], self.rect.x] in self.wb:
            if self.last_move[0] == 'x':
                if self.last_move[1] == 1:
                    if self.coord == 'x':
                        self.last_move = ['x', 1]
                        self.xPos = self.move
                        self.yPos = 0
                    elif self.coord == 'y':
                        self.last_move = ['y', 1]
                        self.yPos = self.move
                        self.xPos = 0
                elif self.last_move[1] == -1:
                    if self.coord == 'x':
                        self.last_move = ['x', -1]
                        self.xPos = -self.move
                        self.yPos = 0
                    elif self.coord == 'y':
                        self.last_move = ['y', 1]
                        self.yPos = self.move
                        self.xPos = 0
            elif self.last_move[0] == 'y':
                self.last_move = ['x', self.movement/20]
                self.xPos = self.movement/20 *self.move
                self.yPos = 0
            #print("TOP")
##            #print(self.xPos)
##            #print(self.yPos)
            
        # LEFT
        elif [self.side['left'], self.rect.y] in self.wr:
            if self.last_move[0] == 'y':
                if self.last_move[1] == 1:
                    if self.coord == 'y':
                        self.last_move = ['y', 1]
                        self.yPos = self.move
                        self.xPos = 0
                    elif self.coord == 'x':
                        self.last_move = ['x', 1]
                        self.xPos = self.move
                        self.yPos = 0
                elif self.last_move[1] == -1:
                    if self.coord == 'x':
                        self.last_move = ['x', 1]
                        self.xPos = self.move
                        self.yPos = 0
                    elif self.coord == 'y':
                        self.last_move = ['y', -1]
                        self.yPos = -self.move
                        self.xPos = 0
            elif self.last_move[0] == 'x':
                self.last_move = ['y', self.movement/20]
                self.yPos = self.movement/20 * self.move
                self.xPos = 0
            #print("LEFT")
##            #print(self.xPos)
##            #print(self.yPos)
            
        # RIGHT
        elif [self.side['right'], self.rect.y] in self.wl:
            if self.last_move[0] == 'y':
                if self.last_move[1] == 1:
                    if self.coord == 'y':
                        self.last_move = ['y', 1]
                        self.yPos = self.move
                        self.xPos = 0
                    elif self.coord == 'x':
                        self.last_move = ['x', -1]
                        self.xPos = -self.move
                        self.yPos = 0
                elif self.last_move[1] == -1:
                    if self.coord == 'x':
                        self.last_move = ['x', -1]
                        self.xPos = -self.move
                        self.yPos = 0
                    elif self.coord == 'y':
                        self.last_move = ['y', -1]
                        self.yPos = -self.move
                        self.xPos = 0
            elif self.last_move[0] == 'x':
                self.last_move = ['y', self.movement/20]
                self.yPos = self.movement/20 * self.move
                self.xPos = 0
            #print("RIGHT")
##            #print(self.xPos)
##            #print(self.yPos)

        #NONE
##        else:
##            if self.last_move[0] == 'y':
##                if self.last_move[1] == 1:
##                    if self.coord == 'y':
##                        self.last_move = ['y', 1]
##                        self.yPos = self.move
##                        self.xPOs = 0
##                    elif self.coord == 'x':
##                        self.last_move = ['x', -1]
##                        self.xPos = -self.move
##                        self.yPos = 0
##                elif self.last_move[1] == -1:
##                    if self.coord == 'x':
##                        self.last_move = ['x', -1]
##                        self.xPos = -self.move
##                        self.yPos = 0
##                    elif self.coord == 'y':
##                        self.last_move = ['y', -1]
##                        self.yPos = -self.move
##                        self.xPos = 0
##            elif self.last_move[0] == 'x':
##                if self.last_move[1] == 1:
##                    if self.coord == 'y':
##                        self.last_move = ['y', 1]
##                        self.yPos = self.move
##                        self.xPos = 0
##                    elif self.coord == 'x':
##                        self.last_move = ['x', 1]
##                        self.xPos = self.move
##                        self.yPos = 0
##                elif self.last_move[1] == -1:
##                    if self.coord == 'x':
##                        self.last_move = ['x', -1]
##                        self.xPos = -self.move
##                        self.yPos = 0
##                    elif self.coord == 'y':
##                        self.last_move = ['y', -1]
##                        self.yPos = -self.move
##                        self.xPos = 0
##            #print("NONE")
##            #print(self.xPos)
##            #print(self.yPos)
        self.animate(self.rect.y, self.rect.x)
        self.rect.y += self.yPos
        self.rect.x += self.xPos

class GhostBLUE(pg.sprite.Sprite):
    def __init__(self, pos, game):
        self._layer = 1
        self.groups = game.all_sprites, game.ghost_list
        pg.sprite.Sprite.__init__(self, self.groups)
        self.size = 10
        self.last_update = 0
        self.current_frame = 0
        self.game = game
        self.load_images()
        self.move = 2
##        self.image = pg.Surface((self.size, self.size))
##        self.image.fill(RED)
        self.image = self.down_frames[1]
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.xPos = 0
        self.yPos = 0
        self.wt = []
        self.wb = []
        self.wl = []
        self.wr = []
        self.last_move = ['x', -1]
        self.lpos = [0]
        self.not_spawn = False


    def load_images(self):
        self.left_frames = [self.game.bgspritesheet.get_image(148, 57.5, 20, 20), self.game.bgspritesheet.get_image(20, 57.5, 20, 20)]
        self.right_frames = [self.game.bgspritesheet.get_image(148, 185, 20, 20), self.game.bgspritesheet.get_image(276, 185, 20, 20)]
        self.up_frames = [self.game.bgspritesheet.get_image(20, 185, 20, 20), self.game.bgspritesheet.get_image(276, 57.5, 20, 20)]
        self.down_frames = [self.game.bgspritesheet.get_image(20, 315, 20, 20), self.game.bgspritesheet.get_image(148, 315, 20, 20)]
        for image in self.left_frames:
            image.set_colorkey(BLACK)
        for image in self.right_frames:
            image.set_colorkey(BLACK)
        for image in self.up_frames:
            image.set_colorkey(BLACK)
        for image in self.down_frames:
            image.set_colorkey(BLACK)
            
    def animate(self, y, x):
        now = pg.time.get_ticks()
        if self.last_move == ['x', -1]:
            self.sprite_frames = self.left_frames
        elif self.last_move == ['x', 1]:
            self.sprite_frames = self.right_frames
        elif self.last_move == ['y', 1]:
            self.sprite_frames = self.down_frames
        else:
            self.sprite_frames = self.up_frames
        if now - self.last_update > 100:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.sprite_frames)
            self.image = self.sprite_frames[self.current_frame]
            self.rect = self.image.get_rect()
            self.rect.y = y
            self.rect.x = x
        

    def update(self): 
        self.coord = random.choice(['x', 'y'])
        self.movement = random.choice([20, -20])
        self.side = {'bottom':self.rect.bottom, 'top':self.rect.top, 'left':self.rect.left, 'right':self.rect.right}
        self.lpos.append((self.rect.x, self.rect.y))
        if self.rect.x == 220 and self.rect.y == 160:
            self.not_spawn = True
        #BOTTOM, TOP, LEFT
        if [self.side['bottom'], self.rect.x] in self.wt and [self.side['top'], self.rect.x] in self.wb and [self.side['left'], self.rect.y] in self.wr:
            self.last_move = ['x', 1]
            self.xPos = self.move
            self.yPos = 0
            #print("N1")

        #BOTTOM, TOP, RIGHT
        elif [self.side['bottom'], self.rect.x] in self.wt and [self.side['top'], self.rect.x] in self.wb and [self.side['right'], self.rect.y] in self.wl:
            self.last_move = ['x', -1]
            self.xPos = -self.move
            self.yPos = 0
            #print("N2")

##        #BOTTOM, RIGHT, LEFT
##        elif [self.side['bottom'], self.xPos] in self.wt and [self.side['left'], self.yPos] in self.wr and [self.side['right'], self.yPos] in self.wl:
##            self.last_move = ['y', -1]
##            self.yPos -= 20
##            #print("N3")
##
##        #TOP, RIGHT, LEFT
##        elif [self.side['top'], self.xPos] in self.wb and [self.side['left'], self.yPos] in self.wr and [self.side['right'], self.yPos] in self.wl:
##            self.last_move = ['y', 1]
##            self.yPos += 20
##            #print("N4")
        
        # BOTTOM, TOP
        if [self.side['bottom'], self.rect.x] in self.wt and [self.side['top'], self.rect.x] in self.wb:
            if self.last_move[1] == 1:
                self.xPos = self.move
                self.yPos = 0
                self.last_move = ['x', 1]
            elif self.last_move[1] == -1:
                self.last_move = ['x', -1]
                self.xPos = -self.move
                self.yPos = 0
            else:
                self.last_move = ['x', self.movement/20]
                self.xPos = self.movement/20 * self.move
                self.yPos = 0
            #print("BOTTOM, TOP")
##            #print(self.xPos)
##            #print(self.yPos)
            
        
        # BOTTOM, LEFT
        elif [self.side['bottom'], self.rect.x] in self.wt and [self.side['left'], self.rect.y] in self.wr:
            if self.last_move[0] == 'x':
                self.yPos = -self.move
                self.xPos = 0
                self.last_move = ['y', -1]
            elif self.last_move[0] == 'y':
                self.xPos = self.move
                self.yPos = 0
                self.last_move = ['x', 1]
            #print("BOTTOM, LEFT")
##            #print(self.xPos)
##            #print(self.yPos)


        # BOTTOM, RIGHT
        elif [self.side['bottom'], self.rect.x] in self.wt and [self.side['right'], self.rect.y] in self.wl:
            if self.last_move[0] == 'x':
                self.yPos = -self.move
                self.xPos = 0
                self.last_move = ['y', -1]
            elif self.last_move[0] == 'y':
                self.xPos = -self.move
                self.yPos = 0
                self.last_move = ['x', -1]
            #print("BOTTOM, RIGHT")
##            #print(self.xPos)
##            #print(self.yPos)

        # TOP, LEFT
        elif [self.side['top'], self.rect.x] in self.wb and [self.side['left'], self.rect.y] in self.wr:
            if self.last_move[0] == 'x':
                self.yPos = self.move
                self.xPos = 0
                self.last_move = ['y', 1]
            elif self.last_move[0] == 'y':
                self.xPos = self.move
                self.yPos = 0
                self.last_move = ['x', 1]
            #print("TOP LEFT")
##            #print(self.xPos)
##            #print(self.yPos)
        
        # TOP, RIGHT
        elif [self.side['top'], self.rect.x] in self.wb and [self.side['right'], self.rect.y] in self.wl:
            if self.last_move[0] == 'x':
                self.yPos = self.move
                self.xPos = 0
                self.last_move = ['y', 1]
            elif self.last_move[0] == 'y':
                self.xPos = -self.move
                self.yPos = 0
                self.last_move = ['x', -1]
            #print("TOP, RIGHT")
##            #print(self.xPos)
##            #print(self.yPos)

        # LEFT, RIGHT
        elif [self.side['left'], self.rect.y] in self.wr and [self.side['right'], self.rect.y] in self.wl:
            if self.last_move[1] == 1:
                self.yPos = self.move
                self.xPos = 0
                self.last_move = ['y', 1]
            elif self.last_move[1] == -1:
                self.yPos = -self.move
                self.xPos = 0
                self.last_move = ['y', -1]
            #print("LEFT, RIGHT")
            #print(str(self.rect.x)+' ,'+str(self.rect.y)+':'+str(self.xPos)+' ,'+str(self.yPos))
##            #print(self.xPos)
##            #print(self.yPos)

        # BOTTOM
        elif [self.side['bottom'], self.rect.x] in self.wt:
            if self.last_move[0] == 'x':
                if self.last_move[1] == 1:
                    if self.coord == 'x':
                        self.last_move = ['x', 1]
                        self.xPos = self.move
                        self.yPos = 0
                    elif self.coord == 'y':
                        self.last_move = ['y', -1]
                        self.yPos = -self.move
                        self.xPos = 0
                elif self.last_move[1] == -1:
                    if self.coord == 'x':
                        self.last_move = ['x', -1]
                        self.xPos = -self.move
                        self.yPos = 0
                    elif self.coord == 'y':
                        self.last_move = ['y', -1]
                        self.yPos = -self.move
                        self.xPos = 0
            elif self.last_move[0] == 'y':
                self.last_move = ['x', self.movement/20]
                self.xPos = self.movement/20*self.move
                self.yPos = 0
            #print("BOTTOM")
##            #print(self.xPos)
##            #print(self.yPos)
            
        # TOP
        elif [self.side['top'], self.rect.x] in self.wb:
            if self.last_move[0] == 'x':
                if self.last_move[1] == 1:
                    if self.coord == 'x':
                        self.last_move = ['x', 1]
                        self.xPos = self.move
                        self.yPos = 0
                    elif self.coord == 'y':
                        self.last_move = ['y', 1]
                        self.yPos = self.move
                        self.xPos = 0
                elif self.last_move[1] == -1:
                    if self.coord == 'x':
                        self.last_move = ['x', -1]
                        self.xPos = -self.move
                        self.yPos = 0
                    elif self.coord == 'y':
                        self.last_move = ['y', 1]
                        self.yPos = self.move
                        self.xPos = 0
            elif self.last_move[0] == 'y':
                self.last_move = ['x', self.movement/20]
                self.xPos = self.movement/20 *self.move
                self.yPos = 0
            #print("TOP")
##            #print(self.xPos)
##            #print(self.yPos)
            
        # LEFT
        elif [self.side['left'], self.rect.y] in self.wr:
            if self.last_move[0] == 'y':
                if self.last_move[1] == 1:
                    if self.coord == 'y':
                        self.last_move = ['y', 1]
                        self.yPos = self.move
                        self.xPos = 0
                    elif self.coord == 'x':
                        self.last_move = ['x', 1]
                        self.xPos = self.move
                        self.yPos = 0
                elif self.last_move[1] == -1:
                    if self.coord == 'x':
                        self.last_move = ['x', 1]
                        self.xPos = self.move
                        self.yPos = 0
                    elif self.coord == 'y':
                        self.last_move = ['y', -1]
                        self.yPos = -self.move
                        self.xPos = 0
            elif self.last_move[0] == 'x':
                self.last_move = ['y', self.movement/20]
                self.yPos = self.movement/20 * self.move
                self.xPos = 0
            #print("LEFT")
##            #print(self.xPos)
##            #print(self.yPos)
            
        # RIGHT
        elif [self.side['right'], self.rect.y] in self.wl:
            if self.last_move[0] == 'y':
                if self.last_move[1] == 1:
                    if self.coord == 'y':
                        self.last_move = ['y', 1]
                        self.yPos = self.move
                        self.xPos = 0
                    elif self.coord == 'x':
                        self.last_move = ['x', -1]
                        self.xPos = -self.move
                        self.yPos = 0
                elif self.last_move[1] == -1:
                    if self.coord == 'x':
                        self.last_move = ['x', -1]
                        self.xPos = -self.move
                        self.yPos = 0
                    elif self.coord == 'y':
                        self.last_move = ['y', -1]
                        self.yPos = -self.move
                        self.xPos = 0
            elif self.last_move[0] == 'x':
                self.last_move = ['y', self.movement/20]
                self.yPos = self.movement/20 * self.move
                self.xPos = 0
            #print("RIGHT")
##            #print(self.xPos)
##            #print(self.yPos)

        #NONE
##        else:
##            if self.last_move[0] == 'y':
##                if self.last_move[1] == 1:
##                    if self.coord == 'y':
##                        self.last_move = ['y', 1]
##                        self.yPos = self.move
##                        self.xPOs = 0
##                    elif self.coord == 'x':
##                        self.last_move = ['x', -1]
##                        self.xPos = -self.move
##                        self.yPos = 0
##                elif self.last_move[1] == -1:
##                    if self.coord == 'x':
##                        self.last_move = ['x', -1]
##                        self.xPos = -self.move
##                        self.yPos = 0
##                    elif self.coord == 'y':
##                        self.last_move = ['y', -1]
##                        self.yPos = -self.move
##                        self.xPos = 0
##            elif self.last_move[0] == 'x':
##                if self.last_move[1] == 1:
##                    if self.coord == 'y':
##                        self.last_move = ['y', 1]
##                        self.yPos = self.move
##                        self.xPos = 0
##                    elif self.coord == 'x':
##                        self.last_move = ['x', 1]
##                        self.xPos = self.move
##                        self.yPos = 0
##                elif self.last_move[1] == -1:
##                    if self.coord == 'x':
##                        self.last_move = ['x', -1]
##                        self.xPos = -self.move
##                        self.yPos = 0
##                    elif self.coord == 'y':
##                        self.last_move = ['y', -1]
##                        self.yPos = -self.move
##                        self.xPos = 0
##            #print("NONE")
##            #print(self.xPos)
##            #print(self.yPos)
        self.animate(self.rect.y, self.rect.x)
        self.rect.y += self.yPos
        self.rect.x += self.xPos
