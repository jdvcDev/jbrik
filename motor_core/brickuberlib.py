#!/usr/bin/env python
#
# https://www.dexterindustries.com/BrickPi/
# https://github.com/DexterInd/BrickPi3
#
# Copyright (c) 2017 Dexter Industries
# Released under the MIT license (http://choosealicense.com/licenses/mit/).
# For more information, see https://github.com/DexterInd/BrickPi3/blob/master/LICENSE.md
#
# This code is a library of support functions for a Rubik's cube solving robot

from __future__ import print_function # use python 3 syntax but make it compatible with python 2
from __future__ import division       #                           ''

import time     # import the time library for the sleep function
import brickpi3 # import the BrickPi3 drivers
import commands # import system command support

debug_print_commands_on = False
debug_motor_commands_on = False

def debug_print_commands(string_in):
    if debug_print_commands_on:
        print(str(string_in))

def debug_motor_commands(string_in):
    if debug_motor_commands_on:
        print(str(string_in))



# class of methods for reading and manipulating a Rubik's cube.
class BricKuberLib(object):
    # create a BrickPi3 instance
    BP = brickpi3.BrickPi3()

    # define motor ports
    MOTOR_GRAB = 0
    MOTOR_TURN = 1
    MOTOR_PORTS = [BP.PORT_B, BP.PORT_A]

    def __init__(self, robot_style, debug = False):
        self.debug = debug
        if robot_style == "NXT1":
            # turn table gears
            self.TurnTablePinion = 24
            self.TurnTableGear = 56

            # turntable motor direction constant
            self.SPIN_DIRECTION = 1

            # motor position constants
            self.MOTOR_GRAB_POSITION_HOME      = 0
            self.MOTOR_GRAB_POSITION_REST      = -35
            self.MOTOR_GRAB_POSITION_FLIP_PUSH = -90
            self.MOTOR_GRAB_POSITION_GRAB      = -130
            self.MOTOR_GRAB_POSITION_FLIP      = -240

            # motor speed constants
            self.MOTOR_GRAB_SPEED_GRAB = 300
            self.MOTOR_GRAB_SPEED_FLIP = 600
            self.MOTOR_GRAB_SPEED_REST = 400
        elif robot_style == "EV3":
            # turn table gears
            self.TurnTablePinion = 12
            self.TurnTableGear = 36

            # turntable motor direction constant
            self.SPIN_DIRECTION = -1

            # motor position constants
            self.MOTOR_GRAB_POSITION_HOME      = -337
            self.MOTOR_GRAB_POSITION_REST      = -337
            self.MOTOR_GRAB_POSITION_FLIP_PUSH = -280
            self.MOTOR_GRAB_POSITION_GRAB      = -240
            self.MOTOR_GRAB_POSITION_FLIP      = -120

            # motor speed constants
            self.MOTOR_GRAB_SPEED_GRAB = 400
            self.MOTOR_GRAB_SPEED_FLIP = 600
            self.MOTOR_GRAB_SPEED_REST = 400
        else:
            raise ValueError("Unsupported robot style")

        self.BP.set_motor_limits(self.MOTOR_PORTS[self.MOTOR_TURN], 0, ((500 * self.TurnTableGear) / self.TurnTablePinion))

        self.home_all()

    # run a motor to the specified position, and wait for it to get there
    def run_to_position(self, port, position, tolerance = 3):
        debug_motor_commands("Start run to position: " + str(position))
        debug_motor_commands("Current Position: " + str(self.BP.get_motor_encoder(self.MOTOR_PORTS[port])))
        debug_motor_commands("Running Motor: " + str(port))

        self.BP.set_motor_position(self.MOTOR_PORTS[port], position)
        encoder = self.BP.get_motor_encoder(self.MOTOR_PORTS[port])
        while((encoder > (position + tolerance)) or (encoder < (position - tolerance))):
            time.sleep(0.01)
            encoder = self.BP.get_motor_encoder(self.MOTOR_PORTS[port])
            debug_motor_commands("Current Position: " + str(self.BP.get_motor_encoder(self.MOTOR_PORTS[port])))


    # This function is for troubleshooting the arm motor encoder.
    def read_encoder(self):
        encoder = self.BP.get_motor_encoder(self.MOTOR_PORTS[self.MOTOR_GRAB])
        debug_motor_commands("Arm motor encoder: " + str(encoder))

    # find motor home positions for all motors
    def home_all(self):
        self.BP.set_motor_power(self.MOTOR_PORTS[self.MOTOR_GRAB], 15)
        self.read_encoder()
        EncoderLast = self.BP.get_motor_encoder(self.MOTOR_PORTS[self.MOTOR_GRAB])
        time.sleep(0.1)
        EncoderNow = self.BP.get_motor_encoder(self.MOTOR_PORTS[self.MOTOR_GRAB])
        while EncoderNow != EncoderLast:
            EncoderLast = EncoderNow
            time.sleep(0.1)
            EncoderNow = self.BP.get_motor_encoder(self.MOTOR_PORTS[self.MOTOR_GRAB])
        self.BP.offset_motor_encoder(self.MOTOR_PORTS[self.MOTOR_GRAB], (EncoderNow - 25))

        self.BP.set_motor_limits(self.MOTOR_PORTS[self.MOTOR_GRAB], 100, self.MOTOR_GRAB_SPEED_GRAB)
        self.BP.set_motor_position(self.MOTOR_PORTS[self.MOTOR_GRAB], self.MOTOR_GRAB_POSITION_REST)
        self.BP.offset_motor_encoder(self.MOTOR_PORTS[self.MOTOR_TURN], self.BP.get_motor_encoder(self.MOTOR_PORTS[self.MOTOR_TURN]))
        self.TurnTableTarget = 0
        self.spin(0)

    # spin the cube the specified number of degrees. Opionally overshoot and return (helps with the significant mechanical play while making a face turn).
    def spin(self, deg, overshoot = 0):
        debug_motor_commands("Start Spin!")
        deg = deg * self.SPIN_DIRECTION      # NXT and EV3 robot styles require the turntable motor to run in different directions.

        if deg < 0:
            overshoot = -overshoot
        self.TurnTableTarget -= (deg + overshoot)
        self.run_to_position(self.MOTOR_TURN, ((self.TurnTableTarget * self.TurnTableGear) / self.TurnTablePinion))
        if overshoot != 0:
            self.TurnTableTarget += overshoot
            self.run_to_position(self.MOTOR_TURN, ((self.TurnTableTarget * self.TurnTableGear) / self.TurnTablePinion))

    # grab the cube
    def grab(self):
        self.BP.set_motor_limits(self.MOTOR_PORTS[self.MOTOR_GRAB], 0, self.MOTOR_GRAB_SPEED_GRAB)
        self.run_to_position(self.MOTOR_GRAB, self.MOTOR_GRAB_POSITION_GRAB)
        time.sleep(0.2)

    # release the cube
    def release(self):
        debug_motor_commands("Call release")
        self.read_encoder()
        self.BP.set_motor_limits(self.MOTOR_PORTS[self.MOTOR_GRAB], 0, self.MOTOR_GRAB_SPEED_REST)
        self.run_to_position(self.MOTOR_GRAB, self.MOTOR_GRAB_POSITION_REST)
        debug_motor_commands("End release")

    # flip the cube, and optionally release it afterwards
    def flip(self, release = False):
        debug_motor_commands("Call flip.")
        self.run_to_position(self.MOTOR_GRAB, self.MOTOR_GRAB_POSITION_FLIP_PUSH)
        time.sleep(0.05)
        self.grab()
        time.sleep(0.2)

        self.BP.set_motor_limits(self.MOTOR_PORTS[self.MOTOR_GRAB], 0, self.MOTOR_GRAB_SPEED_FLIP)
        self.run_to_position(self.MOTOR_GRAB, self.MOTOR_GRAB_POSITION_FLIP)

        self.run_to_position(self.MOTOR_GRAB, self.MOTOR_GRAB_POSITION_FLIP_PUSH)

        if release:
            self.release()