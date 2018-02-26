import pygame, pygame.mixer
from pygame.locals import *
from pygame.key import *

import sys
sys.path.append('../libs/')
sys.path.append('../config/')

from CarModel import CarModel, CarPose
from Visualization import Visualizer
from Config import Config

clock = pygame.time.Clock()

config = Config()

# create car and visualizer inputs. 
car = CarModel(config, CarPose(1000, 800, 0.0))
visualizer = Visualizer(config)

while True:

    #Limit the framerate
    timeDelta = clock.tick(config.fpsLimit)/1000.0

    car.setSlewRate(visualizer.getSlewRate())
    car.setAcceleration(visualizer.getAcceleration())


    car.update(timeDelta)

    visualizer.draw(car.getPose())
    

