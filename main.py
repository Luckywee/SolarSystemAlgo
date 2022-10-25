from cmath import pi
from enum import Enum
import random
import time
from typing import List
import numpy as np
import requests
import pygame
from PIL import Image
from ctypes import windll
from pygame.locals import *
from utili import * 
from models import * 

URL = "https://api.le-systeme-solaire.net/rest/bodies"
response = requests.get(URL)

windll.user32.SetProcessDPIAware()
w, h = (windll.user32.GetSystemMetrics(0),windll.user32.GetSystemMetrics(1))
center = (w/2, h/2)

WHITE = (255,255,255)
BLACK = (0,0,0)    



planetsJson = []
for planet in response.json()['bodies']:
    # if planet["bodyType"] == 'Planet' or planet["id"] == "soleil":
    if planet["bodyType"] == 'Planet':
        planetsJson.append(planet)

furthest = max(map(lambda x: (x['perihelion']+x["aphelion"])/2, planetsJson))
biggest = max(map(lambda x: x["meanRadius"], planetsJson))
allPlanets: List[Planet] = []
for planet in planetsJson:
    distanceFromSun = (planet['perihelion']+planet["aphelion"])/2
    circonference = 2*pi*distanceFromSun
    timeToRotate = planet['sideralOrbit']*24
    speed = circonference/timeToRotate if timeToRotate > 0 else 0
    radius = crossMultiplication(biggest, 50, planet["meanRadius"])
    posX = crossMultiplication(furthest, w*0.95, distanceFromSun)
    posY = center[1]
    #, distanceFromSun = distanceFromSun, speed = speed, radius=planet["meanRadius"]
    allPlanets.append(Planet(planet['name'], color = PlanetColor[planet['id']].value,posX=posX, posY=posY, radius=radius))


firstImageRects = getRectArrayFromImage("front_page.jpg", w, h)
# Pygame init stuff
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((w, h))

play= True
startTransition= True
clock = pygame.time.Clock()
random.shuffle(firstImageRects)
screen.fill(BLACK)
i = 0
while startTransition:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            startTransition = False
        if event.type == pygame.KEYUP:
            if event.key==pygame.K_ESCAPE:
                startTransition = False

    for j in range(20):
        if i+j > len(firstImageRects)-1:
            startTransition = False
            break
        firstImageRects[i+j].draw(screen)

    i+=20
    clock.tick(100)
    pygame.display.flip()


while play:
#     screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False
        if event.type == pygame.KEYUP:
            if event.key==pygame.K_ESCAPE:
                play = False
        
#     # for planet in allPlanets:
#     #     planet.draw(screen)

#     rect = img.get_rect()
#     pygame.draw.rect(img, (200,200,0), rect, 1)
#     screen.blit(img, (20, 20))

#     clock.tick(60)
#     pygame.display.flip()