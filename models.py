from enum import Enum
from math import cos, sin
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
        realDistanceFromSun=0,
        posX=0,
        posY=0,
        angle=0,
        deltaAngle=0,
        radius=10,
        gravity=0,
        selected=False,
    ) -> None:
        self.name = name
        self.distanceFromSun = distanceFromSun
        self.realDistanceFromSun = realDistanceFromSun
        self.color = color
        self.posX = posX
        self.posY = posY
        self.angle = angle
        self.deltaAngle = deltaAngle
        self.radius = radius
        self.gravity = gravity
        self.selected = selected

    @property
    def pos(self):
        return (self.posX, self.posY)

    def draw(self, screen):
        if self.selected:
            pygame.draw.circle(screen, WHITE, self.pos, self.radius + 5)
        pygame.draw.circle(screen, self.color, self.pos, self.radius)

    def update(self, screen):
        self.angle += self.deltaAngle
        self.posX = screen.get_width() / 2 + self.distanceFromSun * cos(self.angle)
        self.posY = screen.get_height() / 2 + self.distanceFromSun * sin(self.angle)

    def collidepoint(self, mousePos):
        return pygame.Rect(
            self.posX - self.radius,
            self.posY - self.radius,
            self.radius * 2,
            self.radius * 2,
        ).collidepoint(mousePos)


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


class Checkbox:
    widthBox = 20

    def __init__(
        self,
        left,
        top,
        label="",
        color=WHITE,
        checked=False,
    ) -> None:
        self.left = left
        self.top = top
        self.label = label
        self.color = color
        self.checked = checked

    def init(self, font):
        text = font.render(self.label, True, self.color)
        self.widthTxt = text.get_rect().width
        self.heightTxt = text.get_rect().height

    def draw(self, screen, font):
        pygame.draw.rect(
            screen,
            self.color,
            self.getRectBox,
            3,
        )
        if self.checked:
            pygame.draw.rect(
                screen,
                self.color,
                self.getRectBoxInside,
            )

        text = font.render(self.label, True, self.color)
        screen.blit(text, (self.left + self.widthBox + 5, self.top))

    @property
    def getRect(self):
        return pygame.Rect(
            self.left, self.top, self.widthTxt + self.widthBox + 5, self.widthBox
        )

    @property
    def getRectBox(self):
        return pygame.Rect(
            self.left,
            self.top + self.heightTxt / 2 - self.widthBox / 2,
            self.widthBox,
            self.widthBox,
        )

    @property
    def getRectBoxInside(self):
        return pygame.Rect(
            self.left + 5,
            self.top + 5 + self.heightTxt / 2 - self.widthBox / 2,
            self.widthBox - 10,
            self.widthBox - 10,
        )


class LittleGuy:
    winPoseFrames = 0
    winPoseUp = False

    def __init__(
        self,
        left=None,
        bot=None,
        heightMax=None,
        realHeightMax=None,
        percentageDone=0,
        step=0,
    ) -> None:
        self.left = left
        self.bot = bot
        self.realHeightMax = realHeightMax
        self.heightMax = heightMax
        self.percentageDone = percentageDone
        self.step = step  # 0 -> up; 1 -> down; 2 -> finished;

    @property
    def getHeight(self):
        return self.realHeightMax * self.percentageDone / 100

    def initLittleGuy(self, screen, gravity):
        self.realHeightMax = AVERAGE_HEIGHT_JUMP_M * EARTH_GRAVITY / gravity
        self.heightMax = self.realHeightMax * screen.get_height() / 1.5
        self.left = screen.get_width() / 2 - 30
        self.bot = screen.get_height() - screen.get_height() / 5
        self.step = 0

    def update(self, percentageToAdd=1):
        self.winPoseFrames += 1
        if self.winPoseFrames % FPS == 0:
            self.winPoseUp = not self.winPoseUp
        if self.step != 2:
            if self.step == 0:
                self.percentageDone += percentageToAdd
                self.bot = self.bot - self.heightMax * percentageToAdd / 100
                if self.percentageDone >= 100:
                    self.percentageDone = 100
                    self.step = 1
            else:
                self.percentageDone -= percentageToAdd
                self.bot = self.bot + self.heightMax * percentageToAdd / 100
                if self.percentageDone <= 0:
                    self.percentageDone = 0
                    self.step = 2

    def draw(self, screen):
        pygame.draw.polygon(
            screen,
            WHITE,
            (
                (self.left, self.bot),
                (self.left + 25, self.bot - 50),
                (self.left + 35, self.bot - 50),
                (self.left + 10, self.bot),
            ),
        )
        pygame.draw.polygon(
            screen,
            WHITE,
            (
                (self.left + 60, self.bot),
                (self.left + 35, self.bot - 50),
                (self.left + 25, self.bot - 50),
                (self.left + 50, self.bot),
            ),
        )
        pygame.draw.polygon(
            screen,
            WHITE,
            (
                (self.left + 25, self.bot - 50),
                (self.left + 25, self.bot - 100),
                (self.left + 35, self.bot - 100),
                (self.left + 35, self.bot - 50),
            ),
        )
        if self.step == 2 and self.winPoseUp:
            pygame.draw.polygon(
                screen,
                WHITE,
                (
                    (self.left, self.bot - 120),
                    (self.left + 25, self.bot - 80),
                    (self.left + 35, self.bot - 80),
                    (self.left + 10, self.bot - 120),
                ),
            )
            pygame.draw.polygon(
                screen,
                WHITE,
                (
                    (self.left + 60, self.bot - 120),
                    (self.left + 35, self.bot - 80),
                    (self.left + 25, self.bot - 80),
                    (self.left + 50, self.bot - 120),
                ),
            )
        else:
            pygame.draw.polygon(
                screen,
                WHITE,
                (
                    (self.left, self.bot - 60),
                    (self.left + 25, self.bot - 100),
                    (self.left + 35, self.bot - 100),
                    (self.left + 10, self.bot - 60),
                ),
            )
            pygame.draw.polygon(
                screen,
                WHITE,
                (
                    (self.left + 60, self.bot - 60),
                    (self.left + 35, self.bot - 100),
                    (self.left + 25, self.bot - 100),
                    (self.left + 50, self.bot - 60),
                ),
            )
        pygame.draw.circle(screen, WHITE, (self.left + 30, self.bot - 115), 15)
