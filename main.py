from cmath import pi
from enum import Enum
from typing import List
import requests
import pygame
from pygame.locals import *
from ctypes import windll
from utili import * 

pygame.init()

windll.user32.SetProcessDPIAware()
w, h = (windll.user32.GetSystemMetrics(0),windll.user32.GetSystemMetrics(1))
center = (w/2, h/2)
screen = pygame.display.set_mode((w, h))

WHITE = (255,255,255)
BLACK = (0,0,0)
YELLOW = (255,255,0)

class PlanetColor(Enum):
    uranus = (106,149,166)
    neptune = (67,102,202)
    jupiter = (153,141,125)
    mars = (252,132,95)
    mercure = (119,119,123)
    saturne = (214,176,116)
    terre = (82,118,155)
    venus = (206,203,196)
    soleil = (255,255,0)

class Planet:
    def __init__(self, name, color = WHITE, distanceFromSun = 0, speed = 0, posX = 0, posY = 0, radius = 10) -> None:
        self.name = name
        self.distanceFromSun = distanceFromSun
        self.speed = speed
        self.color = color
        self.posX = posX
        self.posY = posY
        self.radius = radius
    
    @property
    def pos(self):
        return (self.posX, self.posY)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.pos, self.radius)
    


URL = "https://api.le-systeme-solaire.net/rest/bodies,"
response = requests.get(URL)

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
    print(planet['id'])
    print(posX)
    #, distanceFromSun = distanceFromSun, speed = speed, radius=planet["meanRadius"]
    allPlanets.append(Planet(planet['name'], color = PlanetColor[planet['id']].value,posX=posX, posY=posY, radius=radius))



play= True
clock = pygame.time.Clock()

while play:
    screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False
        if event.type == pygame.KEYUP:
            if event.key==pygame.K_ESCAPE:
                play = False
        
    for planet in allPlanets:
        planet.draw(screen)
    allPlanets[0].draw(screen)
    clock.tick(60)
    pygame.display.flip()