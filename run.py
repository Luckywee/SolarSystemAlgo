import random
import requests
import pygame
from ctypes import windll
from pygame.locals import *
from pages import *

windll.user32.SetProcessDPIAware()
w, h = (windll.user32.GetSystemMetrics(0), windll.user32.GetSystemMetrics(1))

# Pygame init stuff
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((w, h))
fonts = {
    "S": pygame.font.Font("data/Roboto-Regular.ttf", 25),
    "M": pygame.font.Font("data/Roboto-Regular.ttf", 50),
    "L": pygame.font.Font("data/Roboto-Regular.ttf", 80),
}
clock = pygame.time.Clock()

loadingScreen(screen, clock, fonts["M"])

URL = "https://api.le-systeme-solaire.net/rest/bodies"
response = requests.get(URL)

firstImageRects = getRectArrayFromImage("front_page.jpg", w, h, 10)
random.shuffle(firstImageRects)

backgroundTransition(screen, clock, firstImageRects)
mainMenu(screen, clock, fonts, w, h, response.json()["bodies"], firstImageRects)
