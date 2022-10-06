#!/usr/bin/env python2.7
# -*- encoding: UTF-8 -*-

import functions
import ovr
import qi
import sys
from arg_parser import parser
import math


# This script receives the position from the Oculus Rift and communicates angles to the head joint of pepper.

def main(session):
    motion_service = session.service("ALMotion")
    posture_service = session.service("ALRobotPosture")

    motion_service.wakeUp()

    posture_service.goToPosture("StandInit", 0.5)
    motion_service.setStiffnesses("Head", 1.0)
    names = ["HeadYaw", "HeadPitch"]

    i = 0

    # initialize ovr
    ovr.initialize(None)
    hmd, luid = ovr.create()

    hmdDesc = ovr.getHmdDesc(hmd)
    print(hmdDesc.ProductName)

    pos_init = motion_service.getRobotPosition(True)
    while True:

        ts = ovr.getTrackingState(hmd, ovr.getTimeInSeconds(), False)
        head = functions.HeadJoint(ts)
        angles = head.run()
        print(angles)
        #angles = angles[0]  + math.pi/2, angles[1]
    
        value = motion_service.getRobotPosition(True)
        print(value)
        adjustment = value[2]
        angles = [angles[0] - adjustment, angles[1]]
        # normalize the angle
        if math.fabs(angles[0]) > math.pi:
            angles[0] =angles[0] - (2 * math.pi * angles[0]) / (math.fabs(angles[0]))
        print(angles)
        if (-2.0857 <= angles[0] <= 2.0857) or (-0.7608 <= angles[1] <= 0.6371):
            #i = i + 1
            check = functions.AngleCheck(angles[0], angles[1])
            # if i == 0:
            if check:
                # first yaw then pitch
                motion_service.angleInterpolation(names, angles, [1, 1], True)
                print("moving head")
        else:
            print("angles too high")

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
