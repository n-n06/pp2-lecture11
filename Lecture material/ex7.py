import pygame

pygame.init()
width, height = 800,600
blue = (0,0,150)
screen = pygame.display.set_mode((width, height))

fps = 60
clock = pygame.time.Clock()

start_pos = None

screen.fill((0,0,0))
pygame.display.update()

pygame.mouse.set_visible(False)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    pos = pygame.mouse.get_pos()
    if pygame.mouse.get_focused():
        pygame.draw.circle(screen, blue, pos,7)

    pressed = pygame.mouse.get_pressed()
    if pressed[0]:
        if start_pos is None:
            start_pos = pos

        rect_w = max(pos[0] - start_pos[0], start_pos[0] - pos[0])
        rect_h = max(pos[1] - start_pos[1], start_pos[1] - pos[1])

        screen.fill((0,0,0))
        pygame.draw.rect(screen, (0,122,0), (min(start_pos[0], pos[0]), min(start_pos[1], pos[1]), rect_w, rect_h))

    else:
        start_pos = None

    pygame.display.update()
    clock.tick(fps)
