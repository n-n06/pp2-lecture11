import pygame
pygame.init()

screen = pygame.display.set_mode((800,600))
clock = pygame.time.Clock()
black = (0,0,0)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print("Pressed button: ", event.button)
        elif event.type == pygame.MOUSEMOTION:
            print("Absolute position: ", event.pos)
            print("Relative position: ", event.rel)
    screen.fill((black))
    pygame.display.flip()
    clock.tick(10)