import os, sys, math, pygame, pygame.mixer
import random
import euclid
from pygame.locals import *
from pygame.key import *

from CarModel import CarModel

display = True

# Set the screen size
if display:

clock = pygame.time.Clock()

while True:

    environment.get_user_input()
    environment.control()

    #Limit the framerate
    dtime_ms = clock.tick(fpsLimit)/1000.0

    environment.update(dtime)
    environment.check_finish()






