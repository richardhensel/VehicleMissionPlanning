import os, sys, math, pygame, pygame.mixer

from pygame.locals import *
from pygame.key import *

import euclid
import Functions

from CarModel import CarModel, CarPose


class Visualizer():

    def __init__(self, config):


        self.screenSizeVector = euclid.Vector2(config.screenSize[0], config.screenSize[1])

        self.screen = pygame.display.set_mode((config.screenSize[0], config.screenSize[1]))

        self.obstacles = config.obstacles 
        self.carColor = config.carColor
        self.carLineWidth = config.carLineWidth

        self.screenOffsetVector = euclid.Vector3(0.0, 0.0, 0.0)
        self.carModel = CarModel(config, CarPose(0.0, 0.0, 0.0))

        self.carSlewRate = config.carSlewRate
        self.carAcceleration = config.carAcceleration
 
    def draw(self, carPose):
        self.startDrawing()
        self.drawObstacles()
        self.drawCar(carPose)
        self.finishDrawing()


    def startDrawing(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        self.screen.fill((255,255,255))


    def finishDrawing(self):
        self.screen.unlock()
        pygame.display.flip()

 
    def drawCar(self, carPose):
        #screenOffsetVector = euclid.Vector3(self.screenOffset[0], self.screenOffset[1], 0.0)

        carPosVector = euclid.Vector2(carPose.x, carPose.y)
        self.screenOffsetVector = 0.5 * self.screenSizeVector - carPosVector
        
        #back left, front left, front right, back right.

        #Compute offsets
        #poseVector = euclid.Vector3(carPose.x, carPose.y, 0.0) + self.screenOffsetVector
        
        self.carModel.setPose(carPose.x, carPose.y, carPose.heading)
        self.carModel.update(0.0)
        corners = self.carModel.getCorners()

        bl = euclid.Vector2(corners[0][0], corners[0][1]) + self.screenOffsetVector #back left
        fl = euclid.Vector2(corners[1][0], corners[1][1]) + self.screenOffsetVector
        fr = euclid.Vector2(corners[2][0], corners[2][1]) + self.screenOffsetVector
        br = euclid.Vector2(corners[3][0], corners[3][1]) + self.screenOffsetVector #back right

        offsetCarPosVector = carPosVector + self.screenOffsetVector

        #Draw car
        #Draw the offset points
        pointList = [(bl.x, bl.y), (fl.x, fl.y), (fr.x, fr.y), (br.x, br.y)]
        pygame.draw.lines(self.screen, self.carColor, True, pointList, self.carLineWidth)

        #Draw origin
        pygame.draw.circle(self.screen, (255,0,0), (int(offsetCarPosVector.x),int(offsetCarPosVector.y)), 2, 0)


    def drawObstacles(self):

        for obstacle in self.obstacles:

            offsetObstacle = []
            for point in obstacle:
                offsetObstacle.append((point[0]+self.screenOffsetVector.x, point[1]+self.screenOffsetVector.y))

            pygame.draw.lines(self.screen, (0,0,0), False, offsetObstacle, self.carLineWidth)

   # def drawVectors(self):
        #so = self.sensor_origin + screen_offset_vec

        #sensor_vectors = self.__get_sensor_vectors(self.sensor_ranges)
        #sv = []
        #for line in sensor_vectors:
        #    sv.append((line[0]+screen_offset_vec, line[1]+screen_offset_vec))
   #     #Draw sensor vectors
   #     if draw_vectors == True:
   #         sensor_list = []
   #         for line in sv:
   #             point_list = [(line[0].x, line[0].y),(line[1].x, line[1].y)]
   #             pygame.draw.lines(screen_handle, (0,0,255), False, point_list, 1)
   #             sensor_list.append((int(line[1].x), int(line[1].y)))

   #             #Draw the intersection if detected
   #             pygame.draw.circle(screen_handle, (255,0,0), (int(line[1].x), int(line[1].y)), 2, 0)
   #         pygame.draw.lines(screen_handle, (0,0,0), False, sensor_list, self.line_width)

    def getSlewRate(self):

        keys = pygame.key.get_pressed()

        # Sets the quit flags
        if keys[pygame.K_a] == True:
            return -1 * self.carSlewRate
        elif keys[pygame.K_f] == True:
            return self.carSlewRate
        else:
            return 0

        self.carAcceleration = config.carAcceleration
    def getAcceleration(self):

        keys = pygame.key.get_pressed()

        # Sets the quit flags
        if keys[pygame.K_j] == True:
            return -1 * self.carAcceleration
        elif keys[pygame.K_k] == True:
            return self.carAcceleration
        else:
            return 0
