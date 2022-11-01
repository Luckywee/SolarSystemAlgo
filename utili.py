from math import pi
import numpy as np
from PIL import Image
from models import *


def nbToPowerTenStr(nb):
    nb = str(nb)
    result = ""
    result += nb[:1]
    result += "."
    result += nb[1:3]
    result += "e"
    result += str(len(nb[3:]))
    return result


def crossMultiplication(nb1, nb2, nb3):
    return nb3 * nb2 / nb1


def filterFormatAllBodies(
    allBodiesJson,
    w,
    h,
    planets=True,
    sun=True,
    speedMultiplier=1,
    scaledPos=False,
    scaledRadius=False,
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
):
    distanceFromSun = (planet["perihelion"] + planet["aphelion"]) / 2
    secToRotate = planet["sideralOrbit"] * 24 * 60 * 60
    deltaAngleReal = (2 * pi / (secToRotate * FPS)) if secToRotate != 0 else 0
    deltaAngle = deltaAngleReal * speedMultiplier
    print(planet["name"], PlanetColor[planet["id"]].value)
    if scaledRadius:
        radius = crossMultiplication(biggest, 50, planet["meanRadius"])
    else:
        radius = 15

    if scaledPos:
        posX = crossMultiplication(furthest, w / 2 * 0.95, distanceFromSun) + w / 2
        posY = h / 2
    else:
        posX = i_planet * (w / 2 / nbTotal) + w / 2
        posY = h / 2
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
