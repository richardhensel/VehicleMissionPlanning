import math, pygame, pygame.mixer
import euclid
import Functions
from pygame.locals import *

import csv

class CarPose():
    def __init__(self, x, y, heading):

        self.carId = 1
        self.x = x
        self.y = y
        self.heading = heading

class CarModel():

    def __init__(self, config, carPose):

        # Dynamics
        
        self.positionVector = euclid.Vector3()
        #heading angle is measured in radians beginning at a vertical angle and moving clockwise. 
        self.headingVector = euclid.Vector3()

        self.velocity = 0.0             # rate of change of positon in direction of travel ms-1
        self.acceleration = 0.0
        self.steeringAngle =  0.0         #rate of change of yaw with respect to velocity rad/pixel -ve left, +ve right
        self.slewRate = 0.0

        self.maxVelocity = config.carMaxVelocity
        self.maxSteeringAngle = config.carMaxSteeringAngle

        #Define the car geometry
        self.length = config.carLength   #pixels
        self.width = config.carWidth    #pixels 
        self.carRearWheelDist = config.carRearWheelDist

        self.crashed = False

        #obstacles
        self.obstacles = config.obstacles
        self.carBounds = []

        self.setPose(carPose.x, carPose.y,carPose.heading)
    ####
    #set car variables
    ####

    def setPose(self, x, y, heading):
        if heading > math.pi:
            heading = (2*math.pi) - heading

        self.positionVector.x = x
        self.positionVector.y = y
        self.headingVector = euclid.Vector3(0., 1.,0.).rotate_around(euclid.Vector3(0.,0.,1.),heading)
        self.__update_geometry()

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

        #create a carPose Object, 
        #convert the position and headign vectors to fill the objact. 
        #Return the object. 

        #create a 2d version of the heading vector. find the relative angle of the heading vector and the vertical 'north' line on the compass.  
        heading = euclid.Vector2(self.headingVector.x, self.headingVector.y).angle(euclid.Vector2(0.,1.))
        ## this is a bit of a hack. not sure ecactly how this behaviour works yet. May suggest other issues in the heading coordinate system. 
        if self.headingVector.x > 0:
            heading = -1 * heading

        pose = CarPose(self.positionVector.x, self.positionVector.y, heading)

        return pose

    def getCorners(self):

        boundList = []
        for bound in self.carBounds:
            coords = [bound.x, bound.y]
            boundList.append(coords)
            
        return boundList

    
    def update(self, timeDelta):
        #self.__reset_sensors()
        self.__updateDynamics(timeDelta)
        self.__update_geometry()

        self.__detect_collision()


    def __updateDynamics(self, timeDelta):
        
        #positionVector = euclid.Vector3(self.pose.x, self.pose.y,0.0)  # location vectors
        #headingVector = euclid.Vector3(self.pose.heading, 0.0, 0.0)  # orientation vector unit vector centered at the car's origin. 

        # update pose
        self.steeringAngle += self.slewRate * timeDelta
        if abs(self.steeringAngle) > self.maxSteeringAngle:
            # divide actual by absolute to get the sign of the steering angle. multiply by the maximum. 
            self.steeringAngle = self.maxSteeringAngle * (self.steeringAngle)/abs(self.steeringAngle)

        print self.steeringAngle

        self.headingVector = self.headingVector.rotate_around(euclid.Vector3(0.,0.,1.),self.steeringAngle * self.velocity * timeDelta)


        self.velocity += self.acceleration * timeDelta 
        if abs(self.velocity) > self.maxVelocity:
            # divide actual by absolute to get the sign of the steering angle. multiply by the maximum. 
            self.velocity = self.maxVelocity * (self.velocity)/abs(self.velocity)

        # stay still if crashed
        if self.crashed ==True:
            self.velocity = 0.0

        self.positionVector += self.velocity * self.headingVector * timeDelta + 0.5 * (self.acceleration * self.headingVector * (timeDelta**2))


        

    def __update_geometry(self):

        self.carBounds = []
        self.carBounds.append(self.positionVector + self.headingVector.rotate_around( euclid.Vector3(0.,0.,1.), -0.5*math.pi)* self.width/2 - self.headingVector * self.carRearWheelDist)
        self.carBounds.append(self.carBounds[0] + self.headingVector * self.length)
        self.carBounds.append(self.carBounds[1] + self.headingVector.rotate_around( euclid.Vector3(0.,0.,1.), 0.5*math.pi)* self.width)
        self.carBounds.append(self.positionVector + self.headingVector.rotate_around( euclid.Vector3(0.,0.,1.), 0.5*math.pi)* self.width/2 - self.headingVector * self.carRearWheelDist)
        #self.sensorOrigin = positionVector + self.sensor_carRearWheelDist * self.length * headingVector # sensor origin is 1 quarter of the length from the front of the car

    def __detect_collision(self):
        for obstacle in self.obstacles:
            for i in range(0,len(self.carBounds)):
                if i ==0:
                    p1 = (self.carBounds[-1].x, self.carBounds[-1].y)
                else:
                    p1 = (self.carBounds[i-1].x, self.carBounds[i-1].y)
                p2 = (self.carBounds[i].x, self.carBounds[i].y)

                for j in range(0,len(obstacle)):
                    if j ==0:
                        p3 = obstacle[-1]
                    else:
                        p3 = obstacle[j-1]
                    p4 = obstacle[j]
                   
                    #Get intersection point in global frame
                    ix, iy = Functions.getLineIntersection(p1, p2, p3, p4)
                    if ix != None or iy != None:
                        self.crashed = True
                        return 0


