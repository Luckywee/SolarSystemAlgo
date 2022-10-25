
import pygame


pygame.init()

startTransition = True

while startTransition:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            startTransition = False
        if event.type == pygame.KEYUP:
            if event.key==pygame.K_ESCAPE:
                startTransition = False

    pygame.draw.rect(screen, (200,200,0), Rect(50,50,50,50))
    clock.tick(20)
    pygame.display.flip()