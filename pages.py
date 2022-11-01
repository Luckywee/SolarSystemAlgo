from typing import List
import pygame
from utili import *
from models import MyRect


def selectGame(nbButton: int, screen, clock, allPlanetsJSON):
    if nbButton == 0:
        telescopeGame(screen, clock, allPlanetsJSON)
    elif nbButton == 1:
        planetMapsGame(screen, clock)
    elif nbButton == 2:
        gravityJumpGame(screen, clock)
    else:
        print("Error")
        return


def loadingScreen(screen, clock, font: pygame.font.Font):
    loadingTxt = font.render("Loading...", True, WHITE)
    screen.blit(
        loadingTxt,
        (
            screen.get_width() / 2 - loadingTxt.get_width() / 2,
            screen.get_height() / 2 - loadingTxt.get_height() / 2,
        ),
    )
    warningTxt = font.render("(do not click anything anywhere)", True, WHITE)
    screen.blit(
        warningTxt,
        (
            screen.get_width() / 2 - warningTxt.get_width() / 2,
            screen.get_height() / 2
            - warningTxt.get_height() / 2
            + loadingTxt.get_height() * 1.5,
        ),
    )
    clock.tick(FPS)
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
            if i > len(firstImageRects):
                affichage = False
                break
            firstImageRects[i - 1].draw(screen)

        clock.tick(FPS)
        pygame.display.flip()


def mainMenu(screen: pygame.Surface, clock, font, w, h, allPlanetsJSON):
    affichage = True
    widthTxtRect = w / 4
    heightTxtRect = h / 10
    buttons: List[Button] = []
    button1 = Button(
        "Telescope",
        w / 2 - widthTxtRect / 2,
        h / 8 * 3 - heightTxtRect / 2,
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
        h / 8 * 7 - heightTxtRect / 2,
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
                        selectGame(i_button, screen, clock, allPlanetsJSON)

        clock.tick(FPS)
        pygame.display.flip()


def telescopeGame(screen: pygame.Surface, clock, allPlanetsJSON: List[Planet]):
    allPlanets = filterFormatAllBodies(
        allPlanetsJSON,
        screen.get_width(),
        screen.get_height(),
    )
    speedMultiplier = 1
    affichage = True
    while affichage:
        screen.fill(BLACK)
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
                if event.key == pygame.K_UP:
                    speedMultiplier *= 10
                    allPlanets = filterFormatAllBodies(
                        allPlanetsJSON,
                        screen.get_width(),
                        screen.get_height(),
                        speedMultiplier=speedMultiplier,
                    )
                if event.key == pygame.K_DOWN:
                    speedMultiplier /= 10
                    allPlanets = filterFormatAllBodies(
                        allPlanetsJSON,
                        screen.get_width(),
                        screen.get_height(),
                        speedMultiplier=speedMultiplier,
                    )
        for planet in allPlanets:
            planet.draw(screen)
            planet.update(screen)
        clock.tick(FPS)
        pygame.display.flip()


def planetMapsGame(screen, clock):
    pass


def gravityJumpGame(screen, clock):
    pass
