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
from pages import *
from utili import *

windll.user32.SetProcessDPIAware()
w, h = (windll.user32.GetSystemMetrics(0), windll.user32.GetSystemMetrics(1))

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((w, h))

# Pygame init stuff
font = pygame.font.Font("data/Roboto-Regular.ttf", 50)
clock = pygame.time.Clock()

loadingScreen(screen, clock, font)

URL = "https://api.le-systeme-solaire.net/rest/bodies"
response = requests.get(URL)
allPlanets = filterFormatAllBodies(
    response.json()["bodies"], w, h, planets=True, sun=True
)

firstImageRects = getRectArrayFromImage("front_page.jpg", w, h, 10)
random.shuffle(firstImageRects)

backgroundTransition(screen, clock, firstImageRects)
mainMenu(screen, clock, font, w, h)
