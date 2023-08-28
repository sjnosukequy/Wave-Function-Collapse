import pygame, sys, threading
from Algo import Collapse
from Utils import IMG, IMGS

class Game:
    def __init__(self):
        #CHANGE TILE_SIZE AT HERE. RECOMMEND >= 10
        self.tile_size = 40

        self.screen_w = Screen_w
        self.screen_h = Screen_h
        self.screen = Screen
        self.Assets = {
            'pipes' : IMGS('pipes', self.tile_size),
            'demo' : IMGS('demo', self.tile_size),
            'demo-tracks' : IMGS('demo-tracks', self.tile_size),
            'mountains' : IMGS('mountains', self.tile_size),
            'polka' : IMGS('polka', self.tile_size),
            'roads' : IMGS('roads', self.tile_size),
        }

        self.tiles = { 
            # '0,0' : {'IMG': self.Assets['Pipes'][2], 'Pos' : (0,0), 'Variant' : 2}
        }
        self.tile_idx = 0
        self.variant = 0
        self.timer = [0]
        self.tile_types = ['demo', 'demo-tracks', 'mountains', 'pipes', 'polka', 'roads']

    def Run(self):
        mouse1 = pygame.mouse.get_pos()
        mouse2 = [mouse1[0]// self.tile_size, mouse1[1] // self.tile_size]
        mouse_loco =  str(mouse2[0]) + ',' + str(mouse2[1])
        if not threads:
            if RClick:
                self.Del_block(mouse_loco)
            if LClick:
                self.Place_block(mouse_loco, mouse2)

        self.Draw_grid(Screen)
        self.Draw_tile(Screen)

        self.UI(Screen)

    def Draw_grid(self, screen):
        w = (Screen_w - 80) // self.tile_size
        h = Screen_h // self.tile_size
        for i in range(w):
            for k in range(h):
                rect = pygame.Rect(i*self.tile_size, k*self.tile_size, self.tile_size- 1, self.tile_size -1)
                pygame.draw.rect(screen, 'white', rect)

    def Draw_tile(self, screen):
        if self.tiles:
            for i in self.tiles.copy():
                tile = self.tiles[i]
                screen.blit(tile['IMG'], (tile['Pos'][0] * self.tile_size, tile['Pos'][1] * self.tile_size))
    
    def UI(self, screen):
        block = self.Assets[self.tile_types[self.tile_idx]][self.variant].copy()
        pygame.transform.scale(block, (70 * 30/ self.tile_size , 70 * 30/ self.tile_size))
        rect = block.get_rect(midtop = (1240, 10))
        screen.blit(block, rect)

        #ANIMATION LABEL
        text = Font.render('ANIM', True, 'white')
        rect = text.get_rect(midbottom = (1240, 680))
        screen.blit(text, rect)

        color = 'red'
        if Ena_Anim:
            color = 'green'
        
        text = Font.render(str(Ena_Anim), True, color)
        rect = text.get_rect(midbottom = (1240, 700))
        screen.blit(text, rect)

        #TIMER LABEL
        self.timer[0] = round(self.timer[0], 2)
        text = Font.render('TIMER', True, color)
        rect = text.get_rect(midbottom = (1240, 620))
        screen.blit(text, rect)

        text = Font.render(str(self.timer[0]), True, color)
        rect = text.get_rect(midbottom = (1240, 640))
        screen.blit(text, rect)

    def Place_block(self, loco, pos):
        if not self.tiles:
            #LIMIT THE PLACED BLOCK MUST BE THE FIRST BLOCK
            global Block_placed
            self.tiles[loco] = { 'IMG': self.Assets[self.tile_types[self.tile_idx]][self.variant], 'Pos' : pos, 'Variant' : self.variant }
            Block_placed = True

    def Del_block(self, loco):
        for i in self.tiles.copy():
            if i == loco:
                del self.tiles[loco]


if __name__ == '__main__':
    pygame.init()
    Screen_w = 1280
    Screen_h = 720
    Screen = pygame.display.set_mode((Screen_w, Screen_h))
    game = Game()

    threads = []
    Font = pygame.font.Font('tiles/04B_03__.TTF', 25)

    Ena_Anim = True
    Block_placed = False
    Ctrl = False
    RClick = False
    LClick = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # if event.type == pygame.VIDEORESIZE:
            #     Screen_w = pygame.display.get_window_size()[0]
            #     Screen_h = pygame.display.get_window_size()[1]
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not threads:
                        if not Block_placed:
                            game.tiles.clear()
                        threads.append( threading.Thread( target= Collapse, args= (game, Screen_w - 80, Screen_h, Ena_Anim, game.timer) ) )
                        threads[0].start()
                        Block_placed = False
                if event.key == pygame.K_c:
                    if not threads:
                        game.tiles.clear()
                if event.key == pygame.K_h:
                    Ena_Anim = not(Ena_Anim)
                if event.key == pygame.K_LCTRL:
                    Ctrl = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LCTRL:
                    Ctrl = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    if game.variant >= len(game.Assets[game.tile_types[game.tile_idx]]):
                        game.variant = 0
                    if Ctrl:
                        game.variant = (game.variant + 1) % len(game.Assets[game.tile_types[game.tile_idx]])
                    else:
                        game.tile_idx = (game.tile_idx + 1)%len(game.Assets)
                if event.button == 5:
                    if game.variant >= len(game.Assets[game.tile_types[game.tile_idx]]):
                        game.variant = 0
                    if Ctrl:
                        game.variant = (game.variant - 1) % len(game.Assets[game.tile_types[game.tile_idx]])
                    else:
                        game.tile_idx = (game.tile_idx - 1)%len(game.Assets)
                if event.button == 1:
                    LClick = True
                if event.button == 3:
                    RClick = True
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    LClick = False
                if event.button == 3:
                    RClick = False

        for t in threads.copy():
            if not t.is_alive():
                threads.clear()
        Screen.fill('black')
        game.Run()
        pygame.display.flip()
