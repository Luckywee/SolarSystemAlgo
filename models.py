from enum import Enum
from math import cos, pi, sin
import numpy as np
import pygame
from const import *


class PlanetColor(Enum):
    uranus = (106, 149, 166)
    neptune = (67, 102, 202)
    jupiter = (153, 141, 125)
    mars = (252, 132, 95)
    mercure = (119, 119, 123)
    saturne = (214, 176, 116)
    terre = (82, 118, 155)
    venus = (206, 203, 196)
    soleil = (255, 255, 0)


class Planet:
    def __init__(
        self,
        name,
        color=WHITE,
        distanceFromSun=0,
        posX=0,
        posY=0,
        angle=0,
        deltaAngle=0,
        radius=10,
    ) -> None:
        self.name = name
        self.distanceFromSun = distanceFromSun
        self.color = color
        self.posX = posX
        self.posY = posY
        self.angle = angle
        self.deltaAngle = deltaAngle
        self.radius = radius

    @property
    def pos(self):
        return (self.posX, self.posY)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.pos, self.radius)

    def update(self, screen):
        self.angle += self.deltaAngle
        self.posX = screen.get_width() / 2 + self.distanceFromSun * cos(self.angle)
        self.posY = screen.get_height() / 2 + self.distanceFromSun * sin(self.angle)


class MyRect:
    def __init__(self, left, top, color=WHITE, width=5, height=5) -> None:
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.color = color

    def draw(self, screen, border_width=-1):
        pygame.draw.rect(
            screen,
            self.color,
            pygame.Rect(self.left, self.top, self.width, self.height),
            0,
            border_width,
        )


class Button:
    def __init__(
        self,
        text,
        left,
        top,
        width,
        height,
        color=WHITE,
        selected=False,
        colorTxt=BLACK,
    ) -> None:
        self.text = text
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.color = color
        self.selected = selected
        self.colorTxt = colorTxt

    def draw(self, screen, font, selected=False):
        if not selected:
            pygame.draw.rect(screen, self.color, self.getRect)
        else:
            pygame.draw.rect(screen, GRAY, self.getRect)
        pygame.draw.rect(
            screen,
            self.color,
            (self.left + 4, self.top + 4, self.width - 8, self.height - 8),
        )
        text = font.render(self.text, True, self.colorTxt)
        screen.blit(
            text,
            (
                self.left + self.width / 2 - text.get_rect().width / 2,
                self.top + self.height / 2 - text.get_rect().height / 2,
            ),
        )

    @property
    def getRect(self):
        return pygame.Rect(self.left, self.top, self.width, self.height)
