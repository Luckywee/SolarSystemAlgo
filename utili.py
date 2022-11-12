import numpy as np
from PIL import Image
from models import *


def formatNumber(nb):
    nb = str(nb)
    if len(nb) <= 3:
        return nb
    newNb = []
    for i in range(len(nb)):
        j = len(nb) - i - 1
        if i != 0 - i and (i) % 3 == 0:
            newNb.insert(0, "'")
        newNb.insert(0, nb[j])
    return "".join(newNb)


def crossMultiplication(nb1, nb2, nb3):
    return nb3 * nb2 / nb1


def exitButtonEvent(event, screen):
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        mousePos = pygame.mouse.get_pos()
        if mousePos[0] > screen.get_width() - 30 and mousePos[1] < 30:
            pygame.quit()
            exit()


def drawExitButton(screen):
    pygame.draw.polygon(
        screen,
        WHITE,
        (
            (screen.get_width() - 30, 0),
            (screen.get_width() - 30, 5),
            (screen.get_width(), 30),
            (screen.get_width(), 30 - 5),
        ),
    )
    pygame.draw.polygon(
        screen,
        WHITE,
        (
            (screen.get_width() - 30, 30),
            (screen.get_width() - 30, 30 - 5),
            (screen.get_width(), 0),
            (screen.get_width(), 0 + 5),
        ),
    )


def backButtonEvent(event, screen):
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        mousePos = pygame.mouse.get_pos()
        return (
            mousePos[0] < screen.get_width() - 30
            and mousePos[0] > screen.get_width() - 50 - 5 - 10
            and mousePos[1] < 30
        )


def drawBackButton(screen):
    pygame.draw.circle(screen, WHITE, (screen.get_width() - 50, 20), 10)
    pygame.draw.circle(screen, BLACK, (screen.get_width() - 50, 20), 6)
    pygame.draw.rect(screen, BLACK, (screen.get_width() - 50 - 15, 0, 15, 30))
    pygame.draw.rect(screen, WHITE, (screen.get_width() - 50 - 5, 10, 5, 4))
    pygame.draw.polygon(
        screen,
        WHITE,
        (
            (screen.get_width() - 50 - 5, 0),
            (screen.get_width() - 50 - 5, 20),
            (screen.get_width() - 50 - 5 - 10, 10),
        ),
    )


def filterFormatAllBodies(
    allBodiesJson,
    w,
    h,
    planets=True,
    sun=True,
    speedMultiplier=1,
    scaledPos=False,
    scaledRadius=False,
    oldPlanets=[],
    fullLength=False,
):
    bodiesJson = []
    for planet in allBodiesJson:
        if planets:
            if planet["bodyType"] == "Planet":
                bodiesJson.append(planet)
        if sun:
            if planet["id"] == "soleil":
                bodiesJson.append(planet)

    furthest = max(map(lambda x: (x["perihelion"] + x["aphelion"]) / 2, bodiesJson))
    biggest = max(map(lambda x: x["meanRadius"], bodiesJson))
    bodiesJson.sort(key=lambda x: (x["perihelion"] + x["aphelion"]), reverse=False)
    allBodies = []
    for i_planet in range(len(bodiesJson)):
        oldPlanet = oldPlanets[i_planet] if len(oldPlanets) > 0 else None
        allBodies.append(
            formatPlanet(
                bodiesJson[i_planet],
                biggest,
                furthest,
                w,
                h,
                i_planet,
                len(bodiesJson),
                speedMultiplier,
                scaledPos,
                scaledRadius,
                oldPlanet=oldPlanet,
                fullLength=fullLength,
            )
        )

    return allBodies


def formatPlanet(
    planet,
    biggest,
    furthest,
    w,
    h,
    i_planet,
    nbTotal,
    speedMultiplier,
    scaledPos,
    scaledRadius,
    oldPlanet=None,
    fullLength=False,
):
    realDistanceFromSun = (planet["perihelion"] + planet["aphelion"]) / 2
    secToRotate = planet["sideralOrbit"] * 24 * 60 * 60
    deltaAngleReal = (2 * pi / (secToRotate * FPS)) if secToRotate != 0 else 0
    deltaAngle = deltaAngleReal * speedMultiplier
    if scaledRadius:
        radius = crossMultiplication(biggest, 50, planet["meanRadius"])
    else:
        radius = 15

    if fullLength:
        posX = i_planet * (w / nbTotal) + (w / nbTotal) / 2
        posY = h / 2
        radius = 25
    else:
        if scaledPos:
            posX = (
                crossMultiplication(furthest, w / 2 * 0.95, realDistanceFromSun) + w / 2
            )
            posY = h / 2
        else:
            posX = i_planet * (w / 2 / nbTotal) + w / 2
            posY = h / 2

    angle = oldPlanet.angle if oldPlanet else 0
    distanceFromSun = posX - w / 2
    posY = h / 2
    return Planet(
        planet["name"],
        color=PlanetColor[planet["id"]].value,
        posX=posX,
        posY=posY,
        radius=radius,
        deltaAngle=deltaAngle,
        distanceFromSun=distanceFromSun,
        realDistanceFromSun=realDistanceFromSun,
        angle=angle,
        gravity=planet["gravity"],
    )


def getRectArrayFromImage(img_name, screenWidth, screenHeight, ratioPixel=10):
    img_array = np.asarray(Image.open("data/" + img_name), dtype="int32")
    w = len(img_array[0])
    h = len(img_array)
    ratioImage = w / h
    ratioScreen = screenWidth / screenHeight
    newImage = []
    if ratioImage < ratioScreen:
        cutAt = (len(img_array) - 1) * (ratioImage / ratioScreen)
        newImage = img_array[: int(cutAt)]
    elif ratioImage > ratioScreen:
        cutAt = (len(img_array[0]) - 1) * (ratioScreen / ratioImage)
        for line in range(len(img_array)):
            newImage.append(img_array[line][: int(cutAt)])
    w = len(newImage[0])
    h = len(newImage)
    allRects = []

    widthRatio = screenWidth / len(newImage[0])
    heightRatio = screenHeight / len(newImage)

    nbBlockWidth = int(w / ratioPixel)
    nbBlockHeight = int(h / ratioPixel)
    blockWidth = int(w / nbBlockWidth)
    blockHeight = int(h / nbBlockHeight)

    for ibloc_h in range(nbBlockHeight):
        for ibloc_w in range(nbBlockWidth):
            offset_h = blockHeight * ibloc_h
            offset_w = blockWidth * ibloc_w
            all_pixels_red = []
            all_pixels_green = []
            all_pixels_blue = []

            for y in range(blockWidth):
                for x in range(blockHeight):
                    pixel = newImage[offset_h + x][offset_w + y]
                    all_pixels_red.append(pixel[0])
                    all_pixels_green.append(pixel[1])
                    all_pixels_blue.append(pixel[2])

            bloc_red = int(sum(all_pixels_red) / len(all_pixels_red))
            bloc_green = int(sum(all_pixels_green) / len(all_pixels_green))
            bloc_blue = int(sum(all_pixels_blue) / len(all_pixels_blue))
            color = (bloc_red, bloc_green, bloc_blue)

            allRects.append(
                MyRect(
                    offset_w * widthRatio,
                    offset_h * heightRatio,
                    color,
                    ratioPixel * widthRatio + 1,
                    ratioPixel * heightRatio + 1,
                )
            )

    return allRects


def getTextTime(secs):
    secs = int(secs)
    txt = ""
    y = int(secs / (3600 * 24 * 365))
    txt += formatNumber(y) + "y" if y > 0 else ""
    d = int((secs - (y * (3600 * 24 * 365))) / (3600 * 24))
    txt += " " + str(d) + "d" if d > 0 else ""
    if y == 0:
        h = int((secs - (d * 3600 * 24) - (y * 3600 * 24 * 365)) / 3600)
        txt += " " + str(h) + "h" if h > 0 else ""
    if y == 0 and d == 0:
        m = int((secs - (d * 3600 * 24) - (y * 3600 * 24 * 365) - (h * 3600)) / 60)
        txt += " " + str(m) + "m" if m > 0 else ""
    if y == 0 and d == 0 and h == 0:
        s = int(secs - (d * 3600 * 24) - (y * 3600 * 24 * 365) - (h * 3600) - (m * 60))
        txt += " " + str(s) + "s"
    return txt


def printPlanetName(screen, mousePos, allPlanets, font):
    for planet in allPlanets:
        if planet.collidepoint(mousePos):
            textPlanetHover = font.render(planet.name, True, WHITE)
            screen.blit(
                textPlanetHover,
                (screen.get_width() / 2 - textPlanetHover.get_rect().width / 2, 10),
            )
            break
