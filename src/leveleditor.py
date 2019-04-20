import pygame
import re
import constants
pygame.init()
file = open('levels/level.txt', 'w')
size = width, height = 2000,800
window = pygame.display.set_mode(size)
pygame.display.set_caption( "leveleditor" )

clock = pygame.time.Clock()
fps = 60

to_draw = []
current_color = 0
draw_start = False




running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEMOTION:
            mouse_pos = mouse_x, mouse_y = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = mouse_pos
            draw_start = True

        if event.type == pygame.MOUSEBUTTONUP:
            final_pos = mouse_pos
            draw_start = False
            rect = pygame.Rect(pos,(final_pos[0]- pos[0], final_pos[1]-pos[1]))
            rect.normalize()
            to_draw += [rect]

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            if event.key == pygame.K_RETURN:
                for platform in to_draw:
                    
                    str1=str(platform)
                    str2=re.findall(r'\d+',str1)
                    file.write("%s " % str2[2])
                    file.write("%s " % str2[3])
                    file.write("%s " % str2[0])
                    file.write("%s\n" % str2[1])

            if event.key == pygame.K_BACKSPACE:
                to_draw.pop()
    window.fill(constants.WHITE)


    if draw_start:
        pygame.draw.rect(window,constants.BLACK, pygame.Rect(pos, (mouse_pos[0] - pos[0],mouse_pos[1]- pos[1])))
    for item in to_draw:
        pygame.draw.rect(window,constants.BLACK,item)



    pygame.display.update()
    clock.tick(fps)

file.close()
pygame.quit()