import pygame, random, time

# SETTINGS

rules = {
    'left,True'  : [1, 2, 4],
    'right,True' : [1, 3, 4],
    'up,True'    : [3, 2, 4],
    'down,True'  : [2, 3, 1],
    'left,False'  : [0, 3],
    'right,False' : [0, 2],
    'up,False'    : [0, 1],
    'down,False'  : [0, 4],
    'all' : [0, 1, 2, 3, 4]
}

#properties : left, right, up, down
properties = {
    '0' : [False, False, False, False],
    '1' : [True, True, False, True],
    '2' : [True, False, True, True],
    '3' : [False, True, True, True],
    '4' : [True, True, True, False]
}

Dir = [(1, 0, 'right', 1), (-1, 0, 'left', 0), (0, -1, 'up', 2), (0, 1, 'down', 3)]

# END OF SETTINGS


class Tile:
    def __init__(self, type = 0):
        self.type = type

        self.lefts = []
        self.rights = []
        self.ups = []
        self.downs = []
    
    def Observe(self):
        posib = self.Possibilties()
        self.type = random.choice(posib)
    
    def Possibilties(self):
        if not self.lefts:
            self.lefts = rules['all']
        if not self.rights:
            self.rights = rules['all']
        if not self.ups:
            self.ups = rules['all']
        if not self.downs:
            self.downs = rules['all']
        
        a = list(set(self.lefts).intersection(self.rights))
        a = list(set(a).intersection(self.ups))
        a = list(set(a).intersection(self.downs))
        return a
    
    def UpAtt(self, dir, bit):
        if dir == 'left':
            loco = 'right' + ',' + str(bit)
            self.rights = rules[loco]
        if dir == 'right':
            loco = 'left' + ',' + str(bit)
            self.lefts = rules[loco]
        if dir == 'up' :
            loco = 'down' + ',' + str(bit)
            self.downs = rules[loco]
        if dir == 'down':
            loco = 'up' + ',' + str(bit)
            self.ups = rules[loco]

def Collapse(game, screen_W, screen_h, anim, times):
    open_list = []
    close_list = []
    block = game.tile_types[game.tile_idx]
    timer = time.perf_counter()

    maxw = screen_W // game.tile_size
    maxh = screen_h // game.tile_size

    tiles = [[Tile() for k in range(maxw)] for i in range(maxh)]

    if anim:
        tiles_anim = []

    if len(game.tiles) == 0:
        x = random.randrange(maxw)
        y = random.randrange(maxh)
        # # print(x,y)
        # x, y = 3,0
        variant = random.randrange(len(game.Assets[block]))
        loco = str(x) + ',' + str(y)
        game.tiles[loco] = {'IMG': game.Assets[block][variant], 'Pos' : (x,y), 'Variant' : variant}
    
    for loco in game.tiles:
        tile = game.tiles[loco]
        open_list.append( [tile['Pos'][0], tile['Pos'][1], 'None'] )
        tiles[tile['Pos'][1]][tile['Pos'][0]].type = tile['Variant']
        break
    
    while open_list:
        if open_list[0][2] != 'None':
            current = open_list[0]
            x = current[0]
            y = current[1]
            tiles[y][x].Observe()

        for dir in Dir:
            seen = False
            current = open_list[0]
            x = current[0]
            y = current[1]
            type_loco = str(tiles[y][x].type)
            Prop = properties[type_loco]

            x += dir[0]
            y += dir[1]

            if x < 0 or x > maxw - 1:
                continue
            if y < 0 or y > maxh - 1:
                continue 
            
            tiles[y][x].UpAtt(dir[2], Prop[dir[3]])
            for i in open_list:
                if i[0] == x and i[1] == y:
                        seen = True
                        break
            if not seen:
                for i in close_list:
                    if i[0] == x and i[1] == y:
                            seen = True
                            break
            if not seen:
                open_list.append([x, y, dir[2]])

        item = open_list.pop(0)
        close_list.append(item)

        loco_int = (item[0], item[1])
        loco = str(item[0]) + ',' + str(item[1])
        game.tiles[loco] = {'IMG': game.Assets[block][tiles[loco_int[1]][loco_int[0]].type], 'Pos' : loco_int, 'Variant' : tiles[loco_int[1]][loco_int[0]].type}
        
        if anim:
            tiles_anim.append([game.Assets[block][tiles[loco_int[1]][loco_int[0]].type], loco_int[0], loco_int[1]]) #type: ignore
            Draw_tiles(tiles_anim, game.tile_size, game.screen) #type: ignore

    timer -= time.perf_counter()
    timer = abs(timer)
    times[0] = timer

def Draw_tiles(list, size, screen):
    for i in list:
        screen.blit(i[0], (i[1] * size, i[2] * size))
