import math, pygame, pygame.mixer
import euclid
import Functions
from pygame.locals import *

import csv

class CarPose:
    def __init__(self):

        self.carId = 1
        self.x = 0.0
        self.y = 0.0
        self.heading = 0.0

class Car():

    def __init__(self, config, carPose):

        # Dynamics

        self.pose = carPose
        self.velocity = 0.0             # rate of change of positon in direction of travel ms-1
        self.acceleartion = 0.0
        self.steeringAngle =  0.0         #rate of change of yaw with respect to velocity rad/pixel -ve left, +ve right
        self.slewRate = 0.0

        #Define the car geometry
        self.length = config.carLength   #pixels
        self.width = config.carWidth    #pixels 
        self.carRearWheelDist = config.carRearWheelDist


    ####
    #set car variables
    ####

    def setPose(self, x, y, heading):
        self.pose.x = x
        self.pose.y = y
        self.pose.heading = heading

    def setSteeringAngle(self, steeringAngle):
        self.steeringAngle = steeringAngle

    def setSlewRate(self, slewRate):
        self.slewRate = slewRate

    def setVelocity(self, velociity):
        self.velocity = velocity

    def setAcceleration(self, acceleration):
        self.acceleration = acceleration

    ####
    # Get car variables
    ####

    def getPose(self):
        return self.pose

    def getCorners(self):
        return self.carBounds

    
    def update(self, timeDelta, obstacles):
        #self.__reset_sensors()
        self.__updateDynamics(timeDelta)
        self.__update_geometry()

        for obstacle in obstacles:
           # self.__sense(obstacle)
            self.__detect_collision(obstacle)


    def __updateDynamics(self, timeDelta):
        
        positionVector = euclid.Vector3(self.pose.x, self.pose.y,0.0)  # location vectors
        headingVector = euclid.Vector3(self.pose.heading, 0.0, 0.0)  # orientation vector unit vector centered at the car's origin. 

       # # stay still if crashed
       # if self.crashed ==True:
       #     self.velocity = 0.0

        # update pose
        self.steeringAngle += self.slewRate * timeDelta

        headingVector = headingVector.rotate_around(euclid.Vector3(0.,0.,1.),self.steeringAngle * self.velocity * timeDelta)
        positionVector += self.velocity * headingVector * timeDelta

        self.pose.x = positionVector.x
        self.pose.y = positionVector.y
        self.pose.heading = headingVector.x
        

    def __update_geometry(self):
    #Geometry points
        positionVector = euclid.Vector3(self.pose.x, self.pose.y,0.0)  # location vectors
        headingVector = euclid.Vector3(self.pose.heading, 0.0, 0.0)  # orientation vector unit vector centered at the car's origin. 

        self.carBounds[0] =  positionVector + headingVector.rotate_around( euclid.Vector3(0.,0.,1.), -0.5*math.pi)* self.width/2 - headingVector * self.carRearWheelDist
        self.carBounds[1] = self.carBounds[0] + headingVector * self.length
        self.carBounds[2] = self.carBounds[3] + headingVector * self.length
        self.carBounds[3] = positionVector + headingVector.rotate_around( euclid.Vector3(0.,0.,1.), 0.5*math.pi)* self.width/2  - headingVector * self.carRearWheelDist
        #self.sensorOrigin = positionVector + self.sensor_carRearWheelDist * self.length * headingVector # sensor origin is 1 quarter of the length from the front of the car

   # def __detect_collision(self, obstacle):
   #     self.carBounds = [self.rear_left, self.front_left, self.front_right, self.rear_right]
   #     for i in range(0,len(carBounds)):
   #         if i ==0:
   #             p1 = (self.carBounds[-1].x, self.carBounds[-1].y)
   #         else:
   #             p1 = (self.carBounds[i-1].x, self.carBounds[i-1].y)
   #         p2 = (self.carBounds[i].x, self.carBounds[i].y)

   #         for j in range(0,len(obstacle)):
   #             if j ==0:
   #                 p3 = obstacle[-1]
   #             else:
   #                 p3 = obstacle[j-1]
   #             p4 = obstacle[j]
   #            
   #             #Get intersection point in global frame
   #             ix, iy = Functions.getLineIntersection(p1, p2, p3, p4)
   #             if ix != None or iy != None:
   #                 self.crashed = True
   #                 return 0


