import pygame
pygame.init()

screen = pygame.display.set_mode((800,600))
clock = pygame.time.Clock()
black = (0,0,0)

while True:
    pressed = pygame.mouse.get_pressed()
    print(pressed)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    
    if pressed[0]:
        print("Pressed button : 1")

    screen.fill((black))
    pygame.display.flip()
    clock.tick(10)