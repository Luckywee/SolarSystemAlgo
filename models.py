from enum import Enum
import pygame


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
    def __init__(self, name, color = (0,0,0), distanceFromSun = 0, speed = 0, posX = 0, posY = 0, radius = 10) -> None:
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

class MyRect:
    def __init__(self, left, top, color=(0,255,0), width=5, height=5) -> None:
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.left, self.top, self.width, self.height))