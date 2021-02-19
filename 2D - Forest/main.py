import pygame

pygame.init()
screen = pygame.display.set_mode(size=(800, 600), vsync=1)
pygame.display.set_caption("Forest")
icon = pygame.image.load("img/leaves.png")
pygame.display.set_icon(icon)
