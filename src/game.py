import pygame
import pygame.freetype
import constants
from spritesheet import SpriteSheet
import random

def main():
    #p‰‰ohjelma
    pygame.init()
    
    #initalisoidaan mixeri
    pygame.mixer.init()
    mixer=pygame.mixer.music
    filename="sound.wav"
    mixer.load(filename)
    
    #Asetetaan screenin leveys ja korkeus
    size=[constants.SCREEN_WIDTH,constants.SCREEN_HEIGHT]
    screen=pygame.display.set_mode(size)
    
    #Asetetaan fontti
    GAME_FONT=pygame.freetype.Font("font.ttf",50)
    pygame.display.set_caption("Father Long Legs")
    
    
    
if __name__ == "__main__":
    main()