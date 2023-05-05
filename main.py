# PyMan - by Liam Lane

import pygame as pg
import random
from settings import *
from sprites import *
from time import sleep

class Game:
    def __init__(self):
        # initialize game window, etc
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.spawn_block = 0
        self.show_logo = True

    def new(self):
        # start a new game
        self.all_sprites = pg.sprite.LayeredUpdates()
        #########CREATE MAP###########
        Level_1 = [
        'WWWWWWWWWWWWWWWWWWWWWWW',
        'W          W          W',
        'W WWW WWWW W WWWW WWW W',
        'W WWW WWWW W WWWW WWW W',
        'W     R               W',
        'W WWW W WWWWWWW W WWW W',
        'W     W    W    W     W',
        'WWWWW WWWWSWSWWWW WWWWW',
        'WWWWW WSSSSSSSSSW WWWWW',
        'WWWWW WSWWWSWWWSW WWWWW',
        'SSSSS SSWSOPBSWSS SSSSS',
        'WWWWW WSWWWWWWWSW WWWWW',
        'WWWWW WSSSS1SSSSW WWWWW',
        'WWWWW WSWWWWWWWSW WWWWW',
        'W          W          W',
        'W WWW WWWW W WWWW WWW W',
        'WE  W             W  EW',
        'WW  W W WWWWWWW W W  WW',
        'W     W    W    W     W',
        'W WWWWWWWW W WWWWWWWW W',
        'W                     W',
        'WWWWWWWWWWWWWWWWWWWWWWW'
        ]
        x = y = 0
        bitAmount = 0
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.walls = pg.sprite.Group()
        self.bit_list = pg.sprite.Group()
        self.ghost_list = pg.sprite.Group()
        wt = []
        wb = []
        wl = []
        wr = []

        for row in Level_1:
            for col in row:
                if col == 'W':
                    wall = Wall(self, (x, y))
                    wt.append([wall.rect.top, wall.rect.x])
                    wb.append([wall.rect.bottom, wall.rect.x])
                    wl.append([wall.rect.left, wall.rect.y])
                    wr.append([wall.rect.right, wall.rect.y])

                elif col == ' ':
                    bit1 = Bit(self, (x,y))
                    bitAmount += 1

                elif col == 'R':
                    self.spawnr = GhostRED((x, y), self)
                    bit1 = Bit(self, (x,y))
                    bitAmount += 1

                elif col == 'O':
                    self.spawno = GhostORANGE((x, y), self)

                elif col == 'P':
                    self.spawnp = GhostPINK((x, y), self)

                elif col == 'B':
                    self.spawnb = GhostBLUE((x, y), self)
                    
                elif col == '1':
                    playerx = x
                    playery = y
                    

                x += 20
            y += 20
            x = 0
        #Two self.walls for Ghost
        wall = Wall(self, (-20, 200), BLACK)
        wr.append([wall.rect.right, wall.rect.y])

        wall = Wall(self, (460, 200), BLACK)
        wl.append([wall.rect.left, wall.rect.y])

##        wall = Wall((220, 180))
##        self.walls.add(wall)
##        self.all_sprites.add(wall)
##        wt.append([wall.rect.top, wall.rect.x])
##        wb.append([wall.rect.bottom, wall.rect.x])
##        wl.append([wall.rect.left, wall.rect.y])
##        wr.append([wall.rect.right, wall.rect.y])
        
        self.spawnr.wt = wt
        self.spawnr.wb = wb
        self.spawnr.wl = wl
        self.spawnr.wr = wr
        self.spawno.wt = wt
        self.spawno.wb = wb
        self.spawno.wl = wl
        self.spawno.wr = wr
        self.spawnp.wt = wt
        self.spawnp.wb = wb
        self.spawnp.wl = wl
        self.spawnp.wr = wr
        self.spawnb.wt = wt
        self.spawnb.wb = wb
        self.spawnb.wl = wl
        self.spawnb.wr = wr
        self.player = Player(self, (playerx, playery), self.walls, self.bit_list, bitAmount)
        ##########FINISH MAP CREATION##########
        self.run()

    def run(self):
        # Game Loop
        self.playing = True
        while self.playing == True:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # Game Loop update
        self.all_sprites.update()
        if self.spawno.not_spawn and self.spawnp.not_spawn and self.spawnb.not_spawn and self.spawn_block == 0:
            wall = Entrance(self, (220, 180))
            self.spawnr.wt.append([wall.rect.top, wall.rect.x])
            self.spawnr.wb.append([wall.rect.bottom, wall.rect.x])
            self.spawnr.wl.append([wall.rect.left, wall.rect.y])
            self.spawnr.wr.append([wall.rect.right, wall.rect.y])
            self.spawno.wt.append([wall.rect.top, wall.rect.x])
            self.spawno.wb.append([wall.rect.bottom, wall.rect.x])
            self.spawno.wl.append([wall.rect.left, wall.rect.y])
            self.spawno.wr.append([wall.rect.right, wall.rect.y])
            self.spawnp.wt.append([wall.rect.top, wall.rect.x])
            self.spawnp.wb.append([wall.rect.bottom, wall.rect.x])
            self.spawnp.wl.append([wall.rect.left, wall.rect.y])
            self.spawnp.wr.append([wall.rect.right, wall.rect.y])
            self.spawnb.wt.append([wall.rect.top, wall.rect.x])
            self.spawnb.wb.append([wall.rect.bottom, wall.rect.x])
            self.spawnb.wl.append([wall.rect.left, wall.rect.y])
            self.spawnb.wr.append([wall.rect.right, wall.rect.y])
            

    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                self.show_go_screen()
        if pg.sprite.spritecollide(self.player, self.ghost_list, False) or self.spawnr.lpos[-1] == (self.player.rect.x, self.player.rect.y):
            count = 0
            times = 0
            done = False
            self.highscores = []
            with open('high.txt', 'r') as f:
                for line in f:
                    if times == 10:
                        break
                    if int(line[line.find(',')+1:]) < self.player.bits_collected and not done:
                        highscore = self.get_name()+', '+str(self.player.bits_collected)
                        self.highscores.append(highscore)
                        times += 1
                        done = True
                    self.highscores.append(line)
                    times += 1
                    count += 1           
                                
                                
            if count < 9 and not done:
                self.highscores.append(self.get_name()+', '+str(self.player.bits_collected))
            with open('high.txt', 'w') as f:
                couuut = 0
                for highscore in self.highscores:
                    if couuut == len(self.highscores)-1:
                        f.write(highscore.strip())
                    else:
                        f.write(highscore.strip() +'\n')
                    couuut += 1
            self.show_start_screen()

    def get_name(self):
        name = []
        waiting = True
        while waiting:
            self.screen.fill(LIGHTBLUE)
            self.draw_text('You got a Highscore, type your name(lowercase+space)', 20, YELLOW, WIDTH/2, 50)
            self.draw_text('max 10 letters (write something)!', 20, YELLOW, WIDTH/2, 70)
            self.draw_text(''.join(name), 30, YELLOW, WIDTH/2, HEIGHT/2)
            pg.display.flip()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.show_go_screen()
                elif event.type == pg.KEYDOWN:
                    if len(name) <= 10:
                        if event.key == pg.K_a:
                            name.append('a')
                        elif event.key == pg.K_b:
                            name.append('b')
                        elif event.key == pg.K_c:
                            name.append('c')
                        elif event.key == pg.K_d:
                            name.append('d')
                        elif event.key == pg.K_e:
                            name.append('e')
                        elif event.key == pg.K_f:
                            name.append('f')
                        elif event.key == pg.K_g:
                            name.append('g')
                        elif event.key == pg.K_h:
                            name.append('h')
                        elif event.key == pg.K_i:
                            name.append('i')
                        elif event.key == pg.K_j:
                            name.append('j')
                        elif event.key == pg.K_k:
                            name.append('k')
                        elif event.key == pg.K_l:
                            name.append('l')
                        elif event.key == pg.K_m:
                            name.append('m')
                        elif event.key == pg.K_n:
                            name.append('n')
                        elif event.key == pg.K_o:
                            name.append('o')
                        elif event.key == pg.K_p:
                            name.append('p')
                        elif event.key == pg.K_q:
                            name.append('q')
                        elif event.key == pg.K_r:
                            name.append('r')    
                        elif event.key == pg.K_s:
                            name.append('s')
                        elif event.key == pg.K_t:
                            name.append('t')
                        elif event.key == pg.K_u:
                            name.append('u')
                        elif event.key == pg.K_v:
                            name.append('v')
                        elif event.key == pg.K_w:
                            name.append('w')
                        elif event.key == pg.K_x:
                            name.append('x')
                        elif event.key == pg.K_y:
                            name.append('y')
                        elif event.key == pg.K_z:
                            name.append('z')
                        elif event.key == pg.K_SPACE:
                            name.append(' ')
                    if event.key == pg.K_BACKSPACE:
                        name = name[:-1]
                    elif event.key == pg.K_RETURN and len(name) > 0:
                        waiting = False
        return ''.join(name)

    def draw(self):
        # Game Loop - draw
        game_screen = pg.image.load('game_screen.png').convert()
        self.screen.blit(game_screen, (0,0))
        self.all_sprites.draw(self.screen)
        self.draw_text('Highscore:', 30, YELLOW, 100, HEIGHT-150)
        count = 0
        firstHigh = 0
        with open('high.txt', 'r') as f:
            for line in f:
                count += 1
                pos = line.find(',')
                firstHigh = int(line[pos+1:].strip())
                highscoreDisp = line[pos+1:].strip()
                break
        if count == 0 or self.player.bits_collected > firstHigh:
            highscoreDisp = self.player.bits_collected
        self.draw_text(str(highscoreDisp), 30, YELLOW, 100, HEIGHT-100)
            
        self.draw_text('Your Score:', 30, YELLOW, 350, HEIGHT-150)
        self.draw_text(str(self.player.bits_collected), 30, YELLOW, 350, HEIGHT-100)
        # *after* drawing everything, flip the display
        pg.display.flip()

    def draw_text(self, text, size, color , x, y, font_name = 'Arial Rounded'):
        font = pg.font.Font(pg.font.match_font(font_name), size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def show_start_screen(self):
        # game splash/start screen
        if self.show_logo:
            self.name = pg.image.load('name.png').convert()
            self.name_rect = self.name.get_rect()
            self.name = pg.transform.scale(self.name, (300, 120))
            self.screen.fill(BLACK)
            self.screen.blit(self.name, (75, 200))
            pg.display.flip()
            self.show_logo = False
            sleep(2)
        key_press = False
        self.waiting_start = True
        full_list = ['P','r','e','s','s',' a',' k','e','y',' t','o',' b','e','g','i','n',' .', '.','.']
        show_list = []
        index = 0
        count = 0
        while not key_press:
            count += 1
            sleep(0.2)
            try:
                show_list.append(full_list[index])
                index += 1
            except:
                show_list = []
                index = 0
            self.screen.fill(BLACK)
            pac_image = pg.image.load('Pacman_Intro.png').convert()
            self.screen.blit(pac_image, (0,0))
            self.draw_text(''.join(show_list), 20, ORANGE, WIDTH / 2, HEIGHT-100)
            pg.display.flip()
            if count > 5:
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        self.show_go_screen()
                    elif event.type == pg.KEYDOWN:
                        key_press = True

        self.screen.fill(BLACK)
        arrowPos = 0
        arrowDict = {0:[WIDTH/2 -100, HEIGHT*1/5], 1:[WIDTH*1/2 -125, HEIGHT*2/5], 2:[WIDTH*1/2 -140, HEIGHT*3/5], 3:[WIDTH*1/2 -165, HEIGHT*4/5]}
        self.draw_text('>', 30, YELLOW, WIDTH*1/2 -100, HEIGHT*1/5)
        while self.waiting_start:
            rect_list = []
            menu_image = pg.image.load('menu_screen.png').convert()
            self.screen.blit(menu_image, (0,0))
            pg.display.flip()
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.show_go_screen()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_DOWN:
                        arrowPos = (arrowPos+1)%4
                    elif event.key == pg.K_UP:
                        arrowPos = (arrowPos-1)%4
                    elif event.key == pg.K_RETURN:
                        if arrowPos == 0:
                            self.new()
                        elif arrowPos == 1:
                            self.show_credits()
                            self.screen.fill(BLACK)
                        elif arrowPos == 2:
                            self.show_settings()
                            self.screen.fill(BLACK)
                        else:
                            self.show_high()
                            self.screen.fill(BLACK)
            pg.draw.rect(self.screen, BLACK, (WIDTH*1/2 - 125, HEIGHT*1/5, 50,50))
            pg.draw.rect(self.screen, BLACK, (WIDTH*1/2 - 150, HEIGHT*2/5, 50,50))
            pg.draw.rect(self.screen, BLACK, (WIDTH*1/2 - 170, HEIGHT*3/5, 50,50))
            pg.draw.rect(self.screen, BLACK, (WIDTH*1/2 - 200, HEIGHT*4/5, 50,50))
            self.draw_text('>', 30, YELLOW, arrowDict[arrowPos][0], arrowDict[arrowPos][1])
            pg.display.flip()
            self.bgspritesheet = Spritesheet('BlueGHOST.png')
            self.rgspritesheet = Spritesheet('RedGHOST.png')
            self.pgspritesheet = Spritesheet('PinkGHOST.png')
            self.ogspritesheet = Spritesheet('OrangeGHOST.png')
            self.pspritesheet = Spritesheet('Pacman.png')

    def show_settings(self):
        instruc_image = pg.image.load('instructions_screen.png').convert()
        self.screen.blit(instruc_image, (0,0))
        pg.display.flip()
        self.wait_for_key()

    def show_high(self):        
        count = 0
        high_image = pg.image.load('highscores_screen.png').convert()
        self.screen.blit(high_image, (0,0))
        pg.display.flip()
        highPos = [40,60,80,100,120,140,160,180,200,220]
        with open('high.txt', 'r') as f:
            for line in f:
                count += 1
                if count > 10:
                    break
                self.draw_text(str(count)+'.'+line.strip(), 25, YELLOW, WIDTH/2, highPos[count-1])
        if count == 0:
            self.draw_text('No highscores yet!', 15, YELLOW, WIDTH/2, 40)
        pg.display.flip()
        self.wait_for_key()

    def show_credits(self):
        credit_image = pg.image.load('credits_screen.png').convert()
        self.screen.blit(credit_image, (0,0))
        pg.display.flip()
        self.wait_for_key()
        
    def show_go_screen(self):
        # game over/continue
        quit_image = pg.image.load('quit_screen.png').convert()
        self.screen.blit(quit_image, (0,0))
        pg.display.flip()
        waiting = True
        while waiting:
            for event in pg.event.get():
                if event.type == pg.QUIT:             
                    pg.quit()
                elif event.type == pg.KEYDOWN:
                    waiting = False


    def wait_for_key(self):
        self.waiting_for_key = True
        while self.waiting_for_key:
            self.clock.tick(FPS)
            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.show_go_screen()
                    self.waiting_for_key = False
                elif event.type == pg.KEYDOWN:
                    self.waiting_for_key = False

g = Game()
g.show_start_screen()
g.show_go_screen()
pg.quit()
