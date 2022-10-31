from typing import List
import pygame
from utili import *
from models import MyRect


def selectGame(nbButton: int):
    if nbButton == 1:
        telescopeGame()
    elif nbButton == 2:
        planetMapsGame()
    elif nbButton == 3:
        gravityJumpGame()
    else:
        print("Error")
        return


def loadingScreen(screen, clock, font):
    widthTxtRect = 400
    heightTxtRect = 100
    button = Button(
        "Loading...",
        screen.get_width() / 2 - widthTxtRect / 2,
        screen.get_height() / 2 - heightTxtRect / 2,
        widthTxtRect,
        heightTxtRect,
        BLACK,
        False,
        WHITE,
    )
    button.draw(screen, font)
    clock.tick(100)
    pygame.display.flip()


def backgroundTransition(screen, clock, firstImageRects):
    i = 0
    affichage = True
    while affichage:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                affichage = False
                pygame.quit()
                exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    affichage = False
                    pygame.quit()
                    exit()

        for j in range(100):
            i += 1
            if i > len(firstImageRects) - 1:
                affichage = False
                break
            firstImageRects[i].draw(screen)

        clock.tick(100)
        pygame.display.flip()


def mainMenu(screen: pygame.Surface, clock, font, w, h):
    affichage = True
    widthTxtRect = w / 4
    heightTxtRect = h / 10
    buttons: List[Button] = []
    button1 = Button(
        "Telescope",
        w / 2 - widthTxtRect / 2,
        h / 8 * 7 - heightTxtRect / 2,
        widthTxtRect,
        heightTxtRect,
    )
    buttons.append(button1)
    button2 = Button(
        "Planet maps",
        w / 2 - widthTxtRect / 2,
        h / 8 * 5 - heightTxtRect / 2,
        widthTxtRect,
        heightTxtRect,
    )
    buttons.append(button2)
    button3 = Button(
        "Gravity jump",
        w / 2 - widthTxtRect / 2,
        h / 8 * 3 - heightTxtRect / 2,
        widthTxtRect,
        heightTxtRect,
    )
    buttons.append(button3)
    for button in buttons:
        button.draw(screen, font)
    while affichage:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                affichage = False
                pygame.quit()
                exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    affichage = False
                    pygame.quit()
                    exit()
            if event.type == pygame.MOUSEMOTION:
                mousePos = pygame.mouse.get_pos()
                for button in buttons:
                    if button.getRect.collidepoint(mousePos) and not button.selected:
                        button.draw(screen, font, True)
                        button.selected = True
                    elif not button.getRect.collidepoint(mousePos) and button.selected:
                        button.draw(screen, font, False)
                        button.selected = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mousePos = pygame.mouse.get_pos()
                for i_button in range(len(buttons)):
                    if buttons[i_button].getRect.collidepoint(mousePos):
                        selectGame(i_button)

        clock.tick(100)
        pygame.display.flip()


def telescopeGame():

    pass


def planetMapsGame():
    pass


def gravityJumpGame():
    pass
