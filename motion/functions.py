#!/usr/bin/env python2.7

from __future__ import division
import sys
import math
from xml.dom.expatbuilder import theDOMImplementation
import numpy as np
import almath

class Server:
    # This class reads the data received from the KatWalk when the user walks and calculates a mean to determine
    # the new position.
    # Returns the mean of the walk power, the yaw and the direction.
    def __init__(self, UDPServerSocket, bufferSize, range, bool):
        self.UDPServerSocket = UDPServerSocket
        self.bufferSize = bufferSize
        self.range = range
        self.bool = bool
        self.i = 1
        self.dir = 0
    def run(self):
        yaw_vector = []
        wp_vector = []
        dir_vector = []
        message_vector = []

        if self.bool:
            for i in range(0, self.range):
                bytesAddressPair = self.UDPServerSocket.recvfrom(self.bufferSize)

                message = bytesAddressPair[0]

                ## Useful data that is not used, left for other developers.
                # address = bytesAddressPair[1]
                # clientMsg = "Message from Client:{}".format(message)
                # clientIP = "Client IP Address:{}".format(address)
                # bytes = len(clientMsg)
                ##

                msg = format(message)

                # print("##########\nmessage received is: %s" % msg)
                # print("\n##########")

                message_vector.append(msg)

                ## This is the message received and is split by ';'.
                # [0] = is just an int for the direction. '1' means forward, '0' means its not moving and '-1' means backward
                # [1] = is just a string that says 'Yaw'.
                # [2] = is the float for the yaw, that goes from 0 to 1024.
                # [3] = is just a string that says 'WalkPower'.
                # [4] = is the WalkPower value.
                # [5] = is a vector with the position the character would reach in the Unreal Engine map.
                ##

                msg_split = msg.split(";")
                direction = msg_split[0]
                yaw_val = msg_split[1]
                walk_pwr_val = msg_split[2]

                # The message is originally a string, so we need to change the numbers fro str to float.
                # This is done here.
                yaw_val = float(yaw_val)
                walk_pwr = float(walk_pwr_val)
                dir_val = float(direction)

                # Here the functions add every value read to an array.
                yaw_vector.append(yaw_val)
                wp_vector.append(walk_pwr)
                dir_vector.append(dir_val)

            mean_wp = np.mean(wp_vector)
            mean_yaw = np.mean(yaw_vector)
            mean_dir = np.mean(dir_vector)
        else:
            while True:
                bytesAddressPair = self.UDPServerSocket.recvfrom(self.bufferSize)

                message = bytesAddressPair[0]

                ## Useful data that is not used, left for other developers.
                # address = bytesAddressPair[1]
                # clientMsg = "Message from Client:{}".format(message)
                # clientIP = "Client IP Address:{}".format(address)
                # bytes = len(clientMsg)
                ##

                msg = format(message)

                # print("##########\nmessage received is: %s" % msg)
                # print("\n##########")

                message_vector.append(msg)

                ## This is the message received and is split by ';'.
                # [0] = is just an int for the direction. '1' means forward, '0' means its not moving and '-1' means backward
                # [1] = is just a string that says 'Yaw'.
                # [2] = is the float for the yaw, that goes from 0 to 1024.
                # [3] = is just a string that says 'WalkPower'.
                # [4] = is the WalkPower value.
                # [5] = is a vector with the position the charcter would reach in the Unreal Engine map.
                ##

                msg_split = msg.split(";")
                direction = msg_split[0]
                yaw_val = msg_split[1]
                walk_pwr_val = msg_split[2]

                # The message is originally a string, so we need to change the numbers fro str to float.
                # This is done here.
                yaw_val = float(yaw_val)
                walk_pwr = float(walk_pwr_val)
                dir_val = float(direction)

                # Here the functions add every value read to an array.
                yaw_vector.append(yaw_val)
                wp_vector.append(walk_pwr)
                dir_vector.append(dir_val)

                ## Uncomment prints for more information/debugging
                # print("new vectors are:\n")
                # print(yaw_vector)
                # print(wp_vector)
                # print("calculating mean...")
                ##

                if walk_pwr == 0:
                    # and when the Walk Power goes to zero it uses the array to calculate the mean.
                    mean_wp = np.mean(wp_vector)
                    mean_yaw = np.mean(yaw_vector)
                    mean_dir = np.mean(dir_vector)

                    ## Uncomment prints for more information/debugging
                    # print("walk power:")
                    # print(mean_wp)
                    # print("yaw:")
                    # print(mean_yaw)
                    ##

                    break

        for self.i in range(len(yaw_vector)):
            if yaw_vector[self.i] >= yaw_vector[self.i - 1]:
                self.dir = self.dir + 1
            else:
                self.dir = self.dir - 1


        angle_verse = self.dir
        self.dir = 0
        return mean_wp, mean_yaw, mean_dir, message_vector, angle_verse

    # def __str__(self):
    #     return 'Reading from KatWalk and calculating the mean of WalkPower, Yaw and Direction'


class SplitMessage:
    # This class takes the input and based off of it decides the new robot position and outputs it.
    def __init__(self, precise, speed, calibration):
        self.precise = precise
        self.speed = speed
        self.calibration = calibration

    def run(self, wp, yaw, direction):

        wp_mean = wp
        # theta2 is a variable I use to update the new yaw of the KatWalk as the new 0 position.
        yaw_mean = yaw - self.calibration
        yaw_2 = yaw - self.calibration
        ## Uncomment prints for more information/debugging
        # print ("###########\n")
        # print("yaw is: %f", yaw_mean)
        # print("walk power is: %f", wp_mean)
        # print ("\n###########")
        ##

        if wp_mean > 0:
            # When the Walk Power is bigger than 0 the robot moves, otherwise it stands still
            move = True
            # modify walk to modify the step lenght
            walk = self.speed

        else:
            move = False
            walk = 0
        # set the first value to 0 to calibrate and update position

        if self.precise:
            # Here the function calculates the rotation precisely.
            if yaw_mean < 0:
                yaw_mean = yaw_mean + 1024
            theta = float((yaw_mean * 2 * math.pi) / 1024)
            if theta > math.pi:
                theta = theta - 2 * math.pi
            print("Direction: %f" % theta)
        else:
            while True:
                # Here the function uses the yaw to move the robot in 8 fixed angles.
                if 0 <= yaw_mean < 64 or 960 <= yaw_mean <= 1024:
                    theta = 0
                    print("dritto")
                    break
                elif 64 <= yaw_mean < 192:
                    theta = -math.pi / 4
                    print("destra 45")
                    break
                elif 192 <= yaw_mean < 320:
                    theta = -math.pi / 2
                    print("destra 90")
                    break
                elif 320 <= yaw_mean < 448:
                    theta = -3 * math.pi / 4
                    print("destra 135")
                    break
                elif 448 <= yaw_mean < 576:
                    theta = math.pi
                    print("indietro")
                    break
                elif 576 <= yaw_mean < 704:
                    theta = 3 * math.pi / 4
                    print("sinistra 135")
                    break
                elif 704 <= yaw_mean < 832:
                    theta = math.pi / 2
                    print("sinistra 90")
                    break
                elif 832 <= yaw_mean < 960:
                    theta = math.pi / 4
                    print("sinistra 45")
                    break
                elif yaw_mean < 0:
                    yaw_mean = yaw_mean + 1024
                else:
                    print("yaw value is out of boundaries. Yaw value is: %f and max value is 1024", yaw_mean)
                    sys.exit()

        if direction > 0:
            pos_x = walk * math.cos(theta)
            pos_y = walk * math.sin(theta)
        elif direction < 0:
            pos_x = -walk * math.cos(theta)
            pos_y = -walk * math.sin(theta)
            theta = theta + math.pi
        elif direction == 0:
            pos_x = 0
            pos_y = 0
        else:
            print("Direction error, check if kat is working properly")
            sys.exit()
        if yaw_2 < 0:
            yaw_2 = yaw_2 + 1024
        angle = float((yaw_2 * 2 * math.pi) / 1024)
        #print(yaw_2)
        #print("ANGLE")

        if angle > math.pi:
            angle = angle - 2 * math.pi
        #print(angle)
        #print(theta)
        return pos_x, pos_y, angle, move


    # def __str__(self):
    #     return 'Reads the input and calculates new robot position'

class HeadJoint:
    # This class gets the position of the oculus and outputs the angles for the joint.
    def __init__(self, ts):
        self.ts = ts

    def run(self):
        q = self.ts.HeadPose.ThePose.Orientation
        # Mathematical formulas to calculate pitch and yaw from a quaternion.
        '''
        pitch = math.atan2(2.0 * (q.x * q.y + q.w * q.z), q.w * q.w - q.z * q.z - q.z * q.z + q.x * q.x)
        yaw = math.asin(-2.0 * (q.z * q.y - q.w * q.x))

        return pitch, yaw 
        '''
        
        #t0 = +2.0 * (w * x + y * z)
        #t1 = +1.0 - 2.0 * (x * x + y * y)
        #roll_x = math.atan2(t0, t1)
     
        t2 = +2.0 * (q.w * q.x - q.y * q.z)
        t2 = +1.0 if t2 > +1.0 else t2
        t2 = -1.0 if t2 < -1.0 else t2
        pitch_y = math.asin(t2)
     
        t3 = +2.0 * (q.w * q.y + q.z * q.x)
        t4 = +1.0 - 2.0 * (q.x * q.x + q.y * q.y)
        yaw_z = math.atan2(t3, t4)
        
        pitch = - pitch_y
        yaw = yaw_z #+ math.pi/2
        
        return  yaw, pitch

    # def __str__(self):
    #    return 'Calculates the angles for the head joint from the quaternion read for the Oculus'


def AngleCheck(yaw_r, pitch_r):
    yaw = math.degrees(yaw_r)
    pitch = math.degrees(pitch_r)

    if yaw == 119.5 and pitch >= -35.0 and pitch >= 13.5:
        return False
    elif yaw == -91.4 and pitch >= -35.1 and pitch >= 13.5:
        return False
    elif yaw == -61.6 and pitch >= -35.2 and pitch >= 20.9:
        return False
    elif yaw == -33.33 and pitch >= -40.5 and pitch >= 36.5:
        return False
    elif yaw == 33.33 and pitch >= -40.5 and pitch >= 36.5:
        return False
    elif yaw == 61.6 and pitch >= -35.2 and pitch >= 20.9:
        return False
    elif yaw == 91.4 and pitch >= -35.1 and pitch >= 13.5:
        return False
    elif yaw == 119.5 and pitch >= -35.0 and pitch >= 13.5:
        return False
    else:
        return True

## Add derivative control for rotation.
class ProportionalControl:
    def __init__(self, k, motion_service, pos_init):
        self.k = k
        self.motion_service = motion_service
        self.pos_init = pos_init
        self.obj = almath.Pose2D(0, 0, 0)
        self.vel = almath.Pose2D(0, 0, 0)
        self.target = almath.Pose2D(0, 0, 0)

        self.pos_theta_pre = 0.0
        self.err_ = 0

    def run(self, obj):

        #pos = np.subtract(almath.Pose2D(self.motion_service.getRobotPosition(False)), self.pos_init)
        pos = almath.Pose2D(self.motion_service.getRobotPosition(True))
        pos.theta = pos.theta - self.pos_init.theta
        #print("initial position is")
        #print(self.pos_init)
        print("position is:")
        print (pos)
        '''
        pos.x = pos.x - self.pos_init.x
        pos.y = pos.y - self.pos_init.y
        pos.theta = pos.theta - self.pos_init.theta
        print (pos)
        #pos = almath.Pose2D(self.motion_service.getRobotPosition(False))
        #obj = np.add(obj, self.obj)
        '''
        #obj.x = obj.x + self.obj.x
        #obj.y = obj.y + self.obj.y
        #obj.theta = obj.theta

        if obj.x != self.obj.x or obj.y != self.obj.y or obj.theta != self.obj.theta:
            target = TransformMatrix(pos.x, pos.y, pos.theta, obj.x, obj.y)
            print("New step received")
            #self.motion_service.stopMove()
        elif self.vel.x == 0.00 and self.vel.y == 0.00 and self.vel.theta == 0.00:
            #target = TransformMatrix(pos.x, pos.y, pos.theta, obj.x, obj.y)
            print("Objective reached")
            self.motion_service.stopMove()
            target = pos
        else:
            print("Still reaching same objective")
            target = self.target

        # Area that checks if the robot wants to move outside of it and stops it from happening without breaking cycle
        #target = TransformMatrix(self.pos_init.x, self.pos_init.y, self.pos_init.theta, obj.x, obj.y)
        print("objective wrt robot is")
        print(obj)
        #print(self.obj)
        print("objective wrt world is")
        print(target.x, target.y, obj.theta)
        err = obj.theta - pos.theta
        theta = err
        #self.err_ = err
        vel = self.k * almath.Pose2D(
            target.y - pos.y, target.x - pos.x, theta/1.2
        )
        vel_x = round(vel.x, 2)
        vel_y = round(vel.y, 2)
        vel_z = round(vel.theta, 2)
        self.obj = obj
        self.target = target
        self.vel.x = vel_x
        self.vel.y = vel_y
        self.vel.theta = vel_z
        self.pos_theta_pre = obj.theta
        return vel_x, vel_y, vel_z


def TransformMatrix(Ox, Oy, theta, x, y):
    matrix = [
        [math.cos(theta), math.sin(theta), Ox],
        [-math.sin(theta), math.cos(theta), Oy],
        [0, 0, 1]
        ]

    pos = np.matmul(matrix, [[x], [y], [1]])
    final_pos = almath.Pose2D(float(pos[0]), float(pos[1]), 0.0)
    return final_pos


def rotation(yaw_1, yaw_2):
    if yaw_1 - yaw_2 < math.pi:
        return +1
    if yaw_1 - yaw_2 > math.pi:
        return -1
    else:
        return 0

