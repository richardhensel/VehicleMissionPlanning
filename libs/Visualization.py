
import os, sys, math, pygame, pygame.mixer

from pygame.locals import *
from pygame.key import *

from CarModel import CarModel


class Visualizer:

    def __init__(self, config):


        self.screenSizeVector = euclid.Vector3(config.screenSize[0], config.screenSize[1], 0.0)

        self.screen = pygame.display.set_mode((config.screenSize[0], config.screenSize[1]))

        self.obstacles = config.obstacles 
        self.carColor = config.carColor
        self.carLineWidth = config.carLineWidth

        self.screenOffsetVector = euclid.Vector3(0.0, 0.0, 0.0)
        self.carModel = CarModel(config, CarPose(0.0, 0.0, 0.0)
 

    def startDrawing(self, carPose, screenCentre):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit = True
                pygame.quit()
                sys.exit()

        screen.fill((255,255,255))


    def finishDrawing(self, carPose, screenCentre):
        self.drawCars()
        self.draw
        screen.unlock()
        pygame.display.flip()


   # def updateCarPosition(self, carPose, screenCentre):
   #     if len(poseList) not == self.config.numCars

 
    def drawCar(self, carPose):
        screenOffsetVector = euclid.Vector3(self.screenOffset[0], self.screenOffset[1], 0.0)

        if carPose.carId == 1:
            screenSizeVector = euclid.Vector3(self.screenSize[0], self.screenSize[1], 0.0)
            carPosVector = euclid.Vector3(carPose.x, carPose.y, 0.0)
            screenOffsetVector = 0.5 * screenSizeVector - carPosVector

        
        #back left, front left, front right, back right.
          

        #Compute offsets
        poseVector = euclid.Vector3(carPose.x, carPose.y, 0.0) + screenOffsetVector
        
        self.carModel.setPose(carPose.x, carPose.y, carPose.heading)
        corners = self.carModel.getCorners():

        bl = corners[0] + screen_offset_vec #back left
        fl = corners[1] + screen_offset_vec
        fr = corners[2] + screen_offset_vec
        br = corners[3] + screen_offset_vec #back right

        #Draw car
        #Draw the offset points
        pointList = [(bl.x, bl.y), (fl.x, fl.y), (fr.x, fr.y), (br.x, br.y)]
        pygame.draw.lines(self.screen, self.carColor, True, pointList, self.carLineWidth)

        #Draw origin
        pygame.draw.circle(self.screen, (255,0,0), (int(poseVector.x),int(poseVector.y)), 2, 0)

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



