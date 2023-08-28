import pygame, os

Base_path = 'tiles'

def IMG(path, size):
    loco = Base_path + '/' + path
    img = pygame.image.load(loco).convert_alpha()
    return pygame.transform.scale(img, (size, size))

def IMGS(path, size):
    imgs = []
    loco = Base_path + '/' + path
    for i in sorted(os.listdir(loco)):
        imgs.append(IMG(path + '/' + i, size))
    return imgs
