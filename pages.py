import math
from typing import List
import pygame
from utili import *


def selectGame(nbButton: int, screen, clock, allPlanetsJSON, fonts, firstImageRects):
    if nbButton == 0:
        telescopeGame(screen, fonts, clock, allPlanetsJSON, firstImageRects)
    elif nbButton == 1:
        planetMapsGame(screen, fonts, clock, allPlanetsJSON, firstImageRects)
    elif nbButton == 2:
        gravityJumpGame(screen, fonts, clock, allPlanetsJSON, firstImageRects)


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
            exitButtonEvent(event, screen)
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

        drawExitButton(screen)
        clock.tick(FPS)
        pygame.display.flip()


def mainMenu(
    screen: pygame.Surface, clock, fonts, w, h, allPlanetsJSON, firstImageRects=[]
):
    screen.fill(BLACK)
    for rect in firstImageRects:
        rect.draw(screen)
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
        button.draw(screen, fonts["M"])

    affichage = True
    while affichage:
        for event in pygame.event.get():
            exitButtonEvent(event, screen)
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
                        button.draw(screen, fonts["M"], True)
                        button.selected = True
                    elif not button.getRect.collidepoint(mousePos) and button.selected:
                        button.draw(screen, fonts["M"], False)
                        button.selected = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mousePos = pygame.mouse.get_pos()
                for i_button in range(len(buttons)):
                    if buttons[i_button].getRect.collidepoint(mousePos):
                        selectGame(
                            i_button,
                            screen,
                            clock,
                            allPlanetsJSON,
                            fonts,
                            firstImageRects,
                        )

        drawExitButton(screen)
        clock.tick(FPS)
        pygame.display.flip()


def telescopeGame(
    screen: pygame.Surface,
    fonts,
    clock: pygame.time.Clock,
    allPlanetsJSON: List[Planet],
    firstImageRects,
):
    allPlanets = filterFormatAllBodies(
        allPlanetsJSON,
        screen.get_width(),
        screen.get_height(),
    )
    speedMultiplier = 1
    scaledPos = False
    scaledRadius = False
    cb_pos = Checkbox(0, 0, "Position to scale")
    cb_pos.init(fonts["S"])
    cb_rad = Checkbox(0, cb_pos.getRect.height + 10, "Radius to scale")
    cb_rad.init(fonts["S"])
    totalSecs = 0
    affichage = True
    while affichage:
        screen.fill(BLACK)
        updatePlanets = False
        # Setup for texts
        totalSecs += 1 / FPS * speedMultiplier
        textElapsedTime = fonts["S"].render(
            "Elapsed time: " + getTextTime(totalSecs), True, WHITE
        )
        timeScale = (
            "Time scale: "
            + "1:"
            + str(speedMultiplier)
            + " (1s = "
            + getTextTime(speedMultiplier)
            + ")"
        )
        textTimeScale = fonts["S"].render(timeScale, True, WHITE)
        # Rectangle hitbox for the speed multiplier
        speedDividerRect = pygame.Rect(
            10,
            screen.get_height() - textTimeScale.get_rect().height - 20,
            30,
            20,
        )
        speedMultiplierRect = pygame.Rect(
            90,
            screen.get_height() - textTimeScale.get_rect().height - 20,
            30,
            20,
        )
        speedStopRect = pygame.Rect(
            50,
            screen.get_height() - textTimeScale.get_rect().height - 20,
            30,
            20,
        )
        for event in pygame.event.get():
            exitButtonEvent(event, screen)
            if backButtonEvent(event, screen):
                mainMenu(
                    screen,
                    clock,
                    fonts,
                    screen.get_width(),
                    screen.get_height(),
                    allPlanetsJSON,
                    firstImageRects,
                )
            if event.type == pygame.QUIT:
                affichage = False
                pygame.quit()
                exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    affichage = False
                    pygame.quit()
                    exit()
                if event.key == pygame.K_SPACE:
                    speedMultiplier = 0
                    updatePlanets = True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mousePos = pygame.mouse.get_pos()
                if cb_pos.getRect.collidepoint(mousePos):
                    cb_pos.checked = not cb_pos.checked
                    scaledPos = not scaledPos
                    updatePlanets = True

                elif cb_rad.getRect.collidepoint(mousePos):
                    cb_rad.checked = not cb_rad.checked
                    scaledRadius = not scaledRadius
                    updatePlanets = True

                elif speedDividerRect.collidepoint(mousePos):
                    if speedMultiplier > 1:
                        speedMultiplier = int(speedMultiplier / 10)
                        updatePlanets = True

                elif speedMultiplierRect.collidepoint(mousePos):
                    if speedMultiplier == 0:
                        speedMultiplier = 1
                    elif speedMultiplier < 10**12:
                        speedMultiplier = int(speedMultiplier * 10)
                        updatePlanets = True

                elif speedStopRect.collidepoint(mousePos):
                    speedMultiplier = 0
                    updatePlanets = True

        if updatePlanets:
            allPlanets = filterFormatAllBodies(
                allPlanetsJSON,
                screen.get_width(),
                screen.get_height(),
                speedMultiplier=speedMultiplier,
                scaledPos=scaledPos,
                scaledRadius=scaledRadius,
                oldPlanets=allPlanets,
            )

        for planet in allPlanets:
            planet.update(screen)
            planet.draw(screen)

        mousePos = pygame.mouse.get_pos()
        printPlanetName(screen, mousePos, allPlanets, fonts["M"])

        cb_pos.draw(screen, fonts["S"])
        cb_rad.draw(screen, fonts["S"])

        screen.blit(
            textElapsedTime,
            (
                screen.get_width() - textElapsedTime.get_rect().width,
                screen.get_height() - textElapsedTime.get_rect().height,
            ),
        )
        screen.blit(
            textTimeScale,
            (
                0,
                screen.get_height() - textTimeScale.get_rect().height,
            ),
        )

        # Draw arrows for time scale
        pygame.draw.polygon(
            screen,
            WHITE,
            (
                (30, screen.get_height() - textTimeScale.get_rect().height),
                (30, screen.get_height() - textTimeScale.get_rect().height - 20),
                (10, screen.get_height() - textTimeScale.get_rect().height - 10),
            ),
        )
        pygame.draw.polygon(
            screen,
            WHITE,
            (
                (40, screen.get_height() - textTimeScale.get_rect().height),
                (40, screen.get_height() - textTimeScale.get_rect().height - 20),
                (20, screen.get_height() - textTimeScale.get_rect().height - 10),
            ),
        )

        pygame.draw.rect(
            screen,
            WHITE,
            (
                55,
                screen.get_height() - textTimeScale.get_rect().height - 20,
                20,
                20,
            ),
        )

        pygame.draw.polygon(
            screen,
            WHITE,
            (
                (90, screen.get_height() - textTimeScale.get_rect().height),
                (90, screen.get_height() - textTimeScale.get_rect().height - 20),
                (110, screen.get_height() - textTimeScale.get_rect().height - 10),
            ),
        )
        pygame.draw.polygon(
            screen,
            WHITE,
            (
                (100, screen.get_height() - textTimeScale.get_rect().height),
                (100, screen.get_height() - textTimeScale.get_rect().height - 20),
                (120, screen.get_height() - textTimeScale.get_rect().height - 10),
            ),
        )
        drawExitButton(screen)
        drawBackButton(screen)
        clock.tick(FPS)
        pygame.display.flip()


def planetMapsGame(
    screen: pygame.Surface,
    fonts,
    clock: pygame.time.Clock,
    allPlanetsJSON: List[Planet],
    firstImageRects,
):
    allPlanets = filterFormatAllBodies(
        allPlanetsJSON, screen.get_width(), screen.get_height(), fullLength=True
    )
    affichage = True
    planetsSelected = []
    while affichage:
        screen.fill(BLACK)
        for event in pygame.event.get():
            exitButtonEvent(event, screen)
            if backButtonEvent(event, screen):
                mainMenu(
                    screen,
                    clock,
                    fonts,
                    screen.get_width(),
                    screen.get_height(),
                    allPlanetsJSON,
                    firstImageRects,
                )
            if event.type == pygame.QUIT:
                affichage = False
                pygame.quit()
                exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    affichage = False
                    pygame.quit()
                    exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mousePos = pygame.mouse.get_pos()
                for planet in allPlanets:
                    if planet.collidepoint(mousePos):
                        if planet.selected:
                            planetsSelected.remove(planet)
                            planet.selected = not planet.selected
                        else:
                            if len(planetsSelected) < 2:
                                planetsSelected.append(planet)
                                planet.selected = not planet.selected

        for planet in allPlanets:
            planet.draw(screen)

        if len(planetsSelected) == 2:
            distance = abs(
                planetsSelected[0].realDistanceFromSun
                - planetsSelected[1].realDistanceFromSun
            )
            pygame.draw.polygon(
                screen,
                WHITE,
                (
                    (screen.get_width() / 2 - 5, screen.get_height() - 50),
                    (screen.get_width() / 2 - 5, screen.get_height() - 10),
                    (screen.get_width() / 2 + 25, screen.get_height() - 30),
                ),
            )
            pygame.draw.rect(
                screen,
                WHITE,
                (screen.get_width() / 2 - 25, screen.get_height() - 35, 20, 10),
            )
            kmsByFoot = 4 / 60 / 60
            kmsByCar = 100 / 60 / 60
            kmsByRocket = 30000 / 60 / 60
            kmsByLight = 1080000000 / 60 / 60
            textKmhByFoot = fonts["S"].render(
                getTextTime(distance / kmsByFoot) + " by foot", True, WHITE
            )
            textKmhByCar = fonts["S"].render(
                getTextTime(distance / kmsByCar) + " by car", True, WHITE
            )
            textKmhByRocket = fonts["S"].render(
                getTextTime(distance / kmsByRocket) + " by rocket", True, WHITE
            )
            textKmhByLight = fonts["S"].render(
                getTextTime(distance / kmsByLight) + " in light speed", True, WHITE
            )
            distanceFormated = formatNumber(round(distance))

            textDistance = fonts["S"].render(distanceFormated + " km", True, WHITE)
            textPlanet1 = fonts["M"].render(planetsSelected[0].name, True, WHITE)
            textPlanet2 = fonts["M"].render(planetsSelected[1].name, True, WHITE)
            screen.blit(
                textPlanet1, (10, screen.get_height() - textPlanet1.get_rect().height)
            )
            screen.blit(
                textPlanet2,
                (
                    screen.get_width() - textPlanet2.get_rect().width,
                    screen.get_height() - textPlanet2.get_rect().height - 10,
                ),
            )
            screen.blit(
                textDistance,
                (
                    screen.get_width() / 2 - textDistance.get_rect().width / 2,
                    screen.get_height() - textDistance.get_rect().height - 60,
                ),
            )
            screen.blit(
                textKmhByFoot,
                (
                    (screen.get_width() / 4) * 0,
                    10,
                ),
            )
            screen.blit(
                textKmhByCar,
                (
                    (screen.get_width() / 4) * 1,
                    10,
                ),
            )
            screen.blit(
                textKmhByRocket,
                (
                    (screen.get_width() / 4) * 2,
                    10,
                ),
            )
            screen.blit(
                textKmhByLight,
                (
                    (screen.get_width() / 4) * 3,
                    10,
                ),
            )

        mousePos = pygame.mouse.get_pos()
        printPlanetName(screen, mousePos, allPlanets, fonts["M"])

        drawExitButton(screen)
        drawBackButton(screen)
        clock.tick(FPS)
        pygame.display.flip()


def gravityJumpGame(
    screen: pygame.Surface,
    fonts,
    clock: pygame.time.Clock,
    allPlanetsJSON: List[Planet],
    firstImageRects,
):
    allPlanets = filterFormatAllBodies(
        allPlanetsJSON, screen.get_width(), screen.get_height(), fullLength=True
    )
    affichage = True
    planetSelected = None
    littleGuy = None
    while affichage:
        screen.fill(BLACK)
        for event in pygame.event.get():
            exitButtonEvent(event, screen)
            if backButtonEvent(event, screen):
                if planetSelected != None:
                    planetSelected = None
                else:
                    mainMenu(
                        screen,
                        clock,
                        fonts,
                        screen.get_width(),
                        screen.get_height(),
                        allPlanetsJSON,
                        firstImageRects,
                    )
            if event.type == pygame.QUIT:
                affichage = False
                pygame.quit()
                exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    affichage = False
                    pygame.quit()
                    exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mousePos = pygame.mouse.get_pos()
                for planet in allPlanets:
                    if planet.collidepoint(mousePos) and planet.name != "Le Soleil":
                        planetSelected = planet
                if pygame.Rect(0, screen.get_height() / 2 - 50, 100, 100).collidepoint(
                    mousePos
                ):
                    littleGuy = None

        if not planetSelected:
            for planet in allPlanets:
                planet.draw(screen)
            mousePos = pygame.mouse.get_pos()
            printPlanetName(screen, mousePos, allPlanets, fonts["M"])
            littleGuy = None
        else:
            if littleGuy == None:
                littleGuy = LittleGuy()
                littleGuy.initLittleGuy(screen, planetSelected.gravity)
            pygame.draw.rect(
                screen,
                planetSelected.color,
                (
                    0,
                    screen.get_height() - screen.get_height() / 5,
                    screen.get_width(),
                    screen.get_height() / 5,
                ),
            )

            littleGuy.update(50 / FPS)
            littleGuy.draw(screen)
            textGravity = fonts["M"].render(
                str(
                    round(
                        littleGuy.getHeight,
                        2,
                    )
                )
                + " m",
                True,
                WHITE,
            )
            screen.blit(
                textGravity,
                (screen.get_width() / 2 - textGravity.get_rect().width / 2, 0),
            )

            textMaxHeight = fonts["S"].render(
                "Max height: "
                + str(
                    round(
                        littleGuy.realHeightMax,
                        2,
                    )
                )
                + " m",
                True,
                WHITE,
            )
            screen.blit(
                textMaxHeight,
                (
                    screen.get_width() - textMaxHeight.get_rect().width,
                    screen.get_height() / 2 - textMaxHeight.get_rect().height / 2,
                ),
            )

            pygame.draw.polygon(
                screen,
                WHITE,
                (
                    (30, screen.get_height() / 2 - 50),
                    (30, screen.get_height() / 2 + 50),
                    (100, screen.get_height() / 2),
                ),
            )
        drawExitButton(screen)
        drawBackButton(screen)
        clock.tick(FPS)
        pygame.display.flip()
