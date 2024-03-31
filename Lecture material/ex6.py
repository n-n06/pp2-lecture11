import pygame

pygame.init()
width, height = 800,600
screen = pygame.display.set_mode((width, height))

fps = 60
clock = pygame.time.Clock()

start_pos = None

screen.fill((0,0,0))
pygame.display.update()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    pressed = pygame.mouse.get_pressed()
    if pressed[0]:
        pos = pygame.mouse.get_pos()

        if start_pos is None:
            start_pos = pos

        rect_w = max(pos[0] - start_pos[0], start_pos[0] - pos[0])
        rect_h = max(pos[1] - start_pos[1], start_pos[1] - pos[1])

        screen.fill((0,0,0))
        pygame.draw.rect(screen, (0,122,0), (min(start_pos[0], pos[0]), min(start_pos[1], pos[1]), rect_w, rect_h))
        pygame.display.update()

    else:
        start_pos = None
