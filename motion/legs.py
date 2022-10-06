#!/usr/bin/env python2.7
# -*- encoding: UTF-8 -*-
import struct

import almath
import functions
import qi
import socket
from arg_parser import parser
import sys


# This script is used to start the UDP socket to communicate with the KatWalk.
# With the received input it calculates the new position and uses pepper commands to move it.

def main(session):
    if args.precise:
        print ("Precise movement is enabled")
    else:
        print("Precise movement is not enabled")
    if args.bool:
        print ( "Movement is every %d messages" % args.range)
    else:
        print("Movement is every step")

    print('########################')
    print('Starting Initialization...')
    localIP = args.socketip
    localPort = args.socketport
    bufferSize = args.buffersize

    msgFromServer = "Hello KatWalk"
    bytesToSend = str.encode(msgFromServer)
    UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDPServerSocket.bind((localIP, localPort))
    print('UDP socket OK')
    motion_service = session.service("ALMotion")
    posture_service = session.service("ALRobotPosture")
    print('Pepper Connection OK')
    motion_service.setExternalCollisionProtectionEnabled("All", False)
    motion_service.wakeUp()
    posture_service.goToPosture("StandInit", 0.5)
    motion_service.moveInit()
    msg = functions.Server(UDPServerSocket, bufferSize, args.range, args.bool)
    init_pos = almath.Pose2D(motion_service.getRobotPosition(False))
    prop_c = functions.ProportionalControl(args.k, motion_service, init_pos)
    message = msg.run()
    calib = message[1]
    position = functions.SplitMessage(args.precise, args.speed, calib)

    x_pos = 0
    y_pos = 0
    pos_pre = 0
    pos_z = 0
    print('Calibration OK')
    print('Finished Initialization.')
    print('########################')

    while True:
        message = msg.run()

        pos = position.run(message[0], message[1], message[2])
    
        x_pos = pos[0]
        y_pos = pos[1]
        print('moving')


        #robot_pos = almath.Pose2D(motion_service.getRobotPosition(False)).theta
        # print(robot_pos)
        # print(pos)
        # x = prop_c.run(robot_pos[0], x_pos)
        # y = prop_c.run(robot_pos[1], y_pos)
        obj = - pos[2]
        target = almath.Pose2D(pos[0], pos[1], obj)
        print(target)
        #init = almath.Pose2D(motion_service.getRobotPosition(False))


            # MOVEMENT INFO
        print('####################')
        vel = prop_c.run(target)
        print('x velocity %f' % vel[1])
        print('y velocity %f' % vel[0])
        check = message[2]
        #print (check)
        print('z velocity %f' % vel[2])
        # print('Target:')
        # print(x_pos, y_pos)
        print('####################')
        #pos_pre = obj

        if check >= 0:
            angle = + 1
        else:
            angle = - 1
        print (angle)
        motion_service.move(vel[1], vel[0], angle * vel[2])





if __name__ == "__main__":

    args = parser.parse_args()
    session = qi.Session()
    try:
        session.connect("tcp://" + args.ip + ":" + str(args.port))
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)
    main(session)