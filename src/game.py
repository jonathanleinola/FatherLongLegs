import pygame
import pygame.freetype
import constants
from spritesheet import SpriteSheet
import random
import os, sys
from math import pi, sin, cos, atan2


def get_angle(origin, destination):
    """
    Palauttaa kulman pisteiden valilta. esimerkiksi (0,0), (1, -1)
    palauttaa pi/4.
    """
    x_dist = destination[0] - origin[0]
    y_dist = destination[1] - origin[1]
    return atan2(-y_dist, x_dist) % (2 * pi)
   
def project(pos, angle, distance):
    """
   Palauttaa monikon jonka avulla vihollinen suunnistaa kohti hahmoa
   """
    return (pos[0] + (cos(angle) * distance),
            pos[1] - (sin(angle) * distance))

class Player(pygame.sprite.Sprite):

 
    def __init__(self):
        # kutsutaan parenttia
        super().__init__()
 
        #luodaan hahmo
        self.walking_frames_r = []
        sprite_sheet = SpriteSheet("fatherlonglegssprite.png")
        image=sprite_sheet.get_image(12, 12, 80, 40)
        self.walking_frames_r.append(image)
        image2=sprite_sheet.get_image(110, 12, 80, 55)
        self.walking_frames_r.append(image2)
        image3=sprite_sheet.get_image(220, 12, 72, 55)
        self.walking_frames_r.append(image3)
        
        self.image=self.walking_frames_r[0]
        
        #luodaan referenssi
        self.rect = self.image.get_rect()
 
        # luodaan nopeudet
        self.change_x = 0
        self.change_y = 0
 
        # 
        self.level = None
 
    def update(self):
        #liikutetaan pelaajaa
        #gravitaatio
        
        self.calc_grav()
        
        #liiku oikealle tai vasemmalle
        self.rect.x += self.change_x
        

        # testataan osutaanko johonkin lisataan se block_hit_listaan
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        
        for block in block_hit_list:
            # jos liikutaan oikealle
            # pistetaan oikea sivu rectin vasemmaksi sivuksi
            
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                # muuten liikutaan vasemmalle
                self.rect.left = block.rect.right
 
        # liikutaan ylos tai alas
        self.rect.y += self.change_y
        
        # tsekataan osutaanko johonkin uudelleen ja lisataan se block_hit listaan
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
 
            # position paivitys
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom
 
        
            self.change_y = 0
 
    def calc_grav(self):
        
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35
 
        # ollaanko maatasossa
        if self.rect.y >= constants.SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = constants.SCREEN_HEIGHT - self.rect.height
 
    def jump(self):
        #liikutetaan 2 pikseli� yl�sp�in ja katsotaan onko p��ll� jotain
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2
        self.image=self.walking_frames_r[2]
 
        # lis�t��n nopeutta jos ok hyp�t�
        if len(platform_hit_list) > 0 or self.rect.bottom >= constants.SCREEN_HEIGHT:
            self.change_y = -15
 
    #Hahmon kontrollit
    def go_left(self):
        self.change_x = -6
        self.image=self.walking_frames_r[1]
 
    def go_right(self):
        self.change_x = 6
        self.image=self.walking_frames_r[2]
 
    def stop(self):
        self.change_x = 0
        self.image=self.walking_frames_r[0]
 
 
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        # kutsutaan parenttia
        super().__init__()
        
        self.image = pygame.Surface([80, 80])
        self.image.fill(constants.GREEN)
 
        self.rect = self.image.get_rect()
        self.rect.y = 0
        self.rect.x = 0
        #luodaan referenssi
        self.rect = self.image.get_rect()
 
        # luodaan nopeudet
        self.change_x = 0
        self.change_y = 0
        
        self.pos = self.rect.center
        self.speed=.1
 
        # 
        self.level = None
        
    def update(self,dt,player):
        angle=get_angle(self.rect.center,player.rect.center)
        self.pos=project(self.pos,angle,self.speed*dt)
        self.rect.center=self.pos
    def getposition(self,x,y):
        return x,y
 
class Platform(pygame.sprite.Sprite):
 
    def __init__(self, width, height):
        super().__init__()
 
        self.image = pygame.Surface([width, height])
        self.image.fill(constants.BLACK)
        
 
        self.rect = self.image.get_rect()
        
        
class MovingPlatform(Platform):
    """ liikkuva taso """
    change_x = 0
    change_y = 0
 
    boundary_top = 0
    boundary_bottom = 0
    boundary_left = 0
    boundary_right = 0
 
    player = None
 
    level = None
 
    def update(self):
 
        # liikutaan horisontaalisesti
        self.rect.x += self.change_x
 
        # Tarkastetaan osuttiinko pelaajaan
        hit = pygame.sprite.collide_rect(self, self.player)
        if hit:
            #Pelaajaan osuttiin
 
            # jos liikutaan oikealle, pelaajan oikea sivu objektin vasen sivu
            if self.change_x < 0:
                self.player.rect.right = self.rect.left
            else:
                # jos liikutaan vasemmalle tee painvastoin
                self.player.rect.left = self.rect.right
 
        # liikutaan ylos tai alas
        self.rect.y += self.change_y
 
        # katsotaan osuttiinko pelaajaan
        hit = pygame.sprite.collide_rect(self, self.player)
        if hit:
            # Jos pelaajaan osutaan
 
            # pelaajan "pohja" on tason ylapuoli
            if self.change_y < 0:
                self.player.rect.bottom = self.rect.top
            else:
                self.player.rect.top = self.rect.bottom
 
        # tarkastetaan rajat ja jos raja on ylitetty niin kaannytaan toiseen suuntaan
        if self.rect.bottom > self.boundary_bottom or self.rect.top < self.boundary_top:
            self.change_y *= -1
 
        cur_pos = self.rect.x - self.level.world_shift
        if cur_pos < self.boundary_left or cur_pos > self.boundary_right:
            self.change_x *= -1
 
 
class Level():
    """ level super-luokka"""
 
    def __init__(self, player):
      
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.player = player
 
        # paljonko mailmaa on liikutettu
        self.world_shift = 0
 
    def update(self):
        """ paivita kaikki"""
        self.platform_list.update()
 
    def draw(self, screen):
        """ piirra kaikki levelilla"""
 
        # piirra tausta
        screen.fill(constants.WHITE)
        
 
        # piirra kaikki spritet
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)
 
    def shift_world(self, shift_x):
 
        self.world_shift += shift_x
 
        for platform in self.platform_list:
            platform.rect.x += shift_x
 
        for enemy in self.enemy_list:
            enemy.rect.x += shift_x
    
    #splitataan level tesktitiedostosta
    def splitlevel(self,filename):
        level = []
        with open(filename) as f:
            for item in f:
                level.append([int(i) for i in item.split()])
        f.close
        return level
 
 

class Level_01(Level):
    

    
    def __init__(self, player):
        
        Level.__init__(self, player)
 
        self.level_limit = -2000
        
        
        # leveys, korkeys, x, y
        level = self.splitlevel('levels/level1.txt')
                
        # kaydaan lapi lista ja lisataan taso
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)
            
         # lisataan liikkuva taso
        block = MovingPlatform(70, 40)
        block.rect.x = 0
        block.rect.y = 280
        block.boundary_left = -50
        block.boundary_right = 50
        block.change_x = 1
        block.change_y = 1
        block.boundary_bottom=800
        block.boundary_top=100
        block.player = self.player
        block.level = self
        self.platform_list.add(block)
        
 
class Level_02(Level):
 
 
    def __init__(self, player):
 
        Level.__init__(self, player)
 
        self.level_limit = -2000
 
        level = self.splitlevel('levels/level2.txt')
 
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)
 
 
def main():
    """ Main ohjelma """
    
    pygame.init()
    
    #initalisoidaan mixeri
    pygame.mixer.init()
    mixer = pygame.mixer.music
    pygame.mixer.Channel(0).play(pygame.mixer.Sound('sounds/fll.wav'))
    pygame.mixer.Channel(0).set_volume(0.5)
    

    size = [constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)
    GAME_FONT = pygame.freetype.Font("font.ttf", 50)
    pygame.display.set_caption("Father Long legs")
 
    # luodaan pelaaja
    player = Player()
    
    #luodaan enemy
    enemy1 =Enemy()
    
    enemy_list = pygame.sprite.Group()
    enemy_list.add(enemy1)
 
 
    # luodaan tasot
    level_list = []
    level_list.append(Level_01(player))
    level_list.append(Level_02(player))
 
    # nykyinen taso
    current_level_no = 0
    current_level = level_list[current_level_no]
 
    active_sprite_list = pygame.sprite.Group()
    player.level = current_level
 
    player.rect.x = 0
    player.rect.y = constants.SCREEN_HEIGHT - player.rect.height
    active_sprite_list.add(player)
 
    #loopataan niin kauan ku pelaaja painaa close nappia
    done = False
 
    #kuinka nopeasti kuvaa paivitetaan
    clock = pygame.time.Clock()

    #startscreen
    end_it=False
    selected="start"
    kill=0
    while (end_it==False):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                end_it=True
            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_RETURN and selected=='start':
                    end_it=True
                elif event.key==pygame.K_RETURN and selected=='quit':
                    done = True
                    end_it=True
                if event.key==pygame.K_UP:
                    selected="start"
                elif event.key==pygame.K_DOWN:
                    selected="quit"
    
        screen.fill(constants.WHITE)
        if selected=="start":
            GAME_FONT.render_to(screen, (50, 200), "START", constants.BLUE)
            GAME_FONT.render_to(screen, (50, 300), "QUIT", constants.BLACK)
        else:
            GAME_FONT.render_to(screen, (50, 200), "START", constants.BLACK)
        if selected=="quit":
            GAME_FONT.render_to(screen, (50, 300), "QUIT", constants.BLUE)
        
        
        GAME_FONT.render_to(screen, (50, 100), "Father Long Legs", constants.BLACK)
       
        
        pygame.display.update()
        
        
        
        
    # -------- paaohjelma -----------
    #alustetaan timeri
    start_time= 0 
    first=0
    time_since_enter=0

    while not done:
        # 60 fps
        dt=clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

 
            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_r:
                    main()
                if event.key == pygame.K_LEFT:
                    player.go_left()
                if event.key == pygame.K_RIGHT:
                    player.go_right()
                    #aloitetaan timeri
                    if first==0:
                        start_time=pygame.time.get_ticks()
                        first=1
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    player.jump()
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound('sounds/sound.wav'))
                    pygame.mixer.Channel(1).set_volume(0.2)
                    
    
 
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.change_x < 0:
                    player.stop()
                if event.key == pygame.K_RIGHT and player.change_x > 0:
                    player.stop()
 
        # paivitetaan player.
        active_sprite_list.update()
 
        # paivitetaan  level
        current_level.update()
        
        enemy1.update(dt,player)
 
        # jos pelaaja on lahella oikeaa puolta siirretaan maailmaa -x suuntaan
        if player.rect.right >= 500:
            diff = player.rect.right - 500
            player.rect.right = 500
            current_level.shift_world(-diff)
 
        # jos vasen puoli niin siirretaan toiseen suuntaan
        if player.rect.left <= 120:
            diff = 120 - player.rect.left
            player.rect.left = 120
            current_level.shift_world(diff)

        # jos paasee ekasta tasosta lapi siirrytaan seuraavaan tasoon
        current_position = player.rect.x + current_level.world_shift
        if current_position < current_level.level_limit:
            player.rect.x = 120
            if current_level_no < len(level_list)-1:
                current_level_no += 1
                current_level = level_list[current_level_no]
                player.level = current_level
 
        # kaikki piirtamiseen tarvittava alapuolella
        current_level.draw(screen)
        active_sprite_list.draw(screen)
        if current_level_no==1:
            enemy_list.draw(screen)
        
        if current_position > 100 and current_level_no==0:
            GAME_FONT.render_to(screen, (40, 350), "level 1", constants.BLACK)

        
        if current_position > 100 and current_level_no==1:
            GAME_FONT.render_to(screen, (40, 350), "level 2", constants.BLACK)
        
        if start_time>0:
            time_since_enter = pygame.time.get_ticks()-start_time
            remainingtime=round(60-time_since_enter/1000,0)
            message = 'Time remaining ' + str(remainingtime)
            GAME_FONT.render_to(screen, (20,20),message,constants.BLACK)
        
 
        # kaikki piirtamiseen tarvittava ylapuolella
        pygame.display.flip()
        #Timerin alustus
        if time_since_enter/1000>60:
            start_time=pygame.time.get_ticks()
            i=0
            while(i<1000):
                GAME_FONT.render_to(screen, (200, 400), "You are too Slow!!", constants.RED)
                pygame.display.update()
                i=i+1
            main()
        
        if current_level_no==1 and current_position<-2100:
            start_time=pygame.time.get_ticks()
            i=0
            while(i<1000):
                GAME_FONT.render_to(screen, (200, 400), "!!YOU HAVE MADE IT!!", constants.GREEN)
                pygame.display.update()
                i=i+1
            main()
            
        if current_level_no==1 and pygame.sprite.spritecollide(player, enemy_list, False):
            i=0
            while(i<1000):
                GAME_FONT.render_to(screen, (200, 400), "!!TRY AGAIN!!", constants.RED)
                pygame.display.update()
                i=i+1
            main()
        
    pygame.quit()
    sys.exit()
  
 
if __name__ == "__main__":
    main()