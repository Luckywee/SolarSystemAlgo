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
    return nb3*nb2/nb1

def formatPlanet(listPlanets):
    pass