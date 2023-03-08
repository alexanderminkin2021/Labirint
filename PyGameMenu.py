import pygame
from pygame.locals import *
pygame.init()

screen_width=1200
screen_height=800

screen=pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("NeroTrainer")

bg_im=pygame.image.load('Folder/bg_start.png')

run=True
while run:
    screen.blit(bg_im,(0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run=False
    pygame.display.update()
pygame.quit()
