"""
spritesheet moduuli
"""
import pygame
 
import constants
 
class SpriteSheet(object):
    """ luokka jolla saadaan yksittaiset kuvat spritesheetistä"""
 
    def __init__(self, file_name):
        # Load the sprite sheet.
        self.sprite_sheet = pygame.image.load(file_name).convert()
 
 
    def get_image(self, x, y, width, height):
        
        # luodaan blank kuva
        image = pygame.Surface([width, height]).convert()
 
        # kopioi pieni kuva spritesheetistï¿½ pieneksi kuvaksi
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
 
        # tassa pitaisi olla sama kuin taustan vari
        image.set_colorkey(constants.WHITE)
 
        
        return image