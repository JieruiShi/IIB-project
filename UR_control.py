import time
import os
import rtde_control
import rtde_receive
import math
from typing import List

class URLink(object):

    def __init__(self):
        self.IPaddress = "169.254.123.175"
        self.rtde_c = rtde_control.RTDEControlInterface(self.IPaddress)
        self.rtde_r = rtde_receive.RTDEReceiveInterface(self.IPaddress)
        self.lowering_height = 0.688

    # def moveToSetupPosition(self):
    #     targetJointPosition = [-3.05, -2.43, 2.64, -2.9, 1.51, 0]
    #     self.rtde_c.moveJ(targetJointPosition, 0.1, 0.1)

    # def moveToReadyPosition(self):
    #     targetToolPosition = [0.15, 0.13, 0.47, 0, 0, 1.65]
    #     self.rtde_c.moveL(targetToolPosition, 0.1, 0.1)
    #     targetToolPosition = [0.27, 0.12, 0.66, 0, 0, 1.61]
    #     self.rtde_c.moveL(targetToolPosition, 0.1, 0.1)

    # def moveToCleanUpPosition(self):
    #     self.adjustEndRotation(0)
    #     targetToolPosition = [0.27, 0.10, 0.60, 0, 0, 1.61]
    #     self.rtde_c.moveL(targetToolPosition, 0.1, 0.1)

    def adjustToolPosition(self, relativeCoordinates: List[float]):
        """For small movements, should not exceed 0.01 in x,y direction, adjust frying pan instead of arm for those cases"""
        if len(relativeCoordinates) != 3:
            raise Exception("input format not accepted!")
        elif abs(relativeCoordinates[0]) > 0.01 or abs(relativeCoordinates[1]) > 0.01:
            raise Exception("input a smaller value!")
        elif abs(relativeCoordinates[2]) > 0.1:
            raise Exception("input a smaller value!")

        currentCoordinates = self.rtde_r.getActualTCPPose()
        relativeCoordinates = relativeCoordinates + 3 * [0]
        targetToolPosition = [currentCoordinates[n] + relativeCoordinates[n] for n in range(6)]
        if targetToolPosition[2] >= 0.741:
            raise Exception("The end of the tool is going too low!")
        self.rtde_c.moveL(targetToolPosition, 0.3, 0.3)

    def adjustEndRotation(self, targetAngle: int):
        """rotate end actuator to specified angle, max 180 in both directions"""
        maxRotation = 180
        currentJointPositions = self.rtde_r.getActualQ()
        targetJointPositions = currentJointPositions
        targetJointPositions[5] = targetAngle / 180 * math.pi
        if abs(targetJointPositions[5]) > maxRotation / 180 * math.pi:
            raise Exception("angle of servo should be within 180")
        self.rtde_c.moveJ(targetJointPositions, 0.5, 0.5)

    def normal_position(self):
        targetJointPosition = [0.07, -0.21, self.lowering_height, 0, 0, 0]
        self.rtde_c.moveL(targetJointPosition, 0.1, 0.1)

    def ready_position(self):
        targetJointPosition = [0.07, -0.21, 0.5, 0, 0, 0]
        self.rtde_c.moveL(targetJointPosition, 0.1, 0.1)

    def measure_once(self):
        self.normal_position()
        time.sleep(20)
        self.ready_position()

    def probe_every_30(self):
        while True:
            self.measure_once()
            time.sleep(8)

    def PWM(self, percentage = 0.75, timeCycle = 30, measurePercentage = 0.8):
        self.rtde_c.moveL([0.07, -0.21, self.lowering_height, 0, 0, 0], 0.1, 0.1)
        self.rtde_c.moveL([0.3, -0.21, self.lowering_height, 0, 0, 0], 0.1, 0.1)
        self.rtde_c.moveL([0.29, -0.21, self.lowering_height, 0, 0, 0], 0.1, 0.1)
        time.sleep(timeCycle * percentage - 4)
        self.rtde_c.moveL([0.06, -0.21, self.lowering_height, 0, 0, 0], 0.1, 0.1)
        self.rtde_c.moveL([0.07, -0.21, self.lowering_height, 0, 0, 0], 0.1, 0.1)
        time.sleep(timeCycle * (measurePercentage - percentage))
        self.rtde_c.moveL([0.07, -0.21, 0.5, 0, 0, 0], 0.1, 0.1)
        time.sleep(timeCycle * (1 - measurePercentage))


if __name__ == '__main__':
    URTest = URLink()
    # URTest.ready_position()
    # exit()
    # URTest.normal_position()
    # exit()
    URTest.probe_every_30()
    exit()
    # print(os.getcwd())
    # exit()

    # URTest.measure_once()
    # URTest.probe_every_30()
    # exit()
    while True:
        URTest.PWM()

    exit()


    time.sleep(1)
    URTest.normal_position()
    time.sleep(1)
    targetJointPosition = [0.30, -0.21, self.lowering_height, 0, 0, 0]
    URTest.rtde_c.moveL(targetJointPosition, 0.1, 0.1)
    time.sleep(1)
    targetJointPosition = [0.29, -0.21, self.lowering_height, 0, 0, 0]
    URTest.rtde_c.moveL(targetJointPosition, 0.1, 0.1)
    URTest.normal_position()
    targetJointPosition = [0.07, -0.21, self.lowering_height, 0, 0, 0]

    URTest.ready_position()
    exit()



    targetJointPosition = [0.07, -0.21, self.lowering_height, 0, 0, 0]
    URTest.rtde_c.moveL(targetJointPosition, 0.1, 0.1)
    time.sleep(10)
    targetJointPosition = [0.05, -0.21, self.lowering_height, 0, 0, 0]
    URTest.rtde_c.moveL(targetJointPosition, 0.1, 0.1)
    time.sleep(10)
    targetJointPosition = [0.07, -0.21, self.lowering_height, 0, 0, 0]
    URTest.rtde_c.moveL(targetJointPosition, 0.1, 0.1)
    time.sleep(10)
    targetJointPosition = [0.07, -0.21, 0.5, 0, 0, 0]
    URTest.rtde_c.moveL(targetJointPosition, 0.1, 0.1)
    time.sleep(3)
    exit()

    time.sleep(1)
    URTest.rtde_c.moveL([0.07, -0.21, 0.7, 0, 0, 0], 0.1, 0.1)
    time.sleep(5)
    pwmCycle = 0.5

    while True:
        URTest.rtde_c.moveL([0.3, -0.21, 0.7, 0, 0, 0], 0.1, 0.1)
        time.sleep(30*pwmCycle)
        URTest.rtde_c.moveL([0.06, -0.21, 0.7, 0, 0, 0], 0.1, 0.1)
        URTest.rtde_c.moveL([0.07, -0.21, 0.7, 0, 0, 0], 0.1, 0.1)
        time.sleep(30*(1-pwmCycle))


        # targetJointPosition = [0.06, -0.21, 0.71, 0, 0, 0]
        # URTest.rtde_c.moveL(targetJointPosition, 0.1, 0.1)
        # time.sleep(1)
        # targetJointPosition = [0.06, -0.21, 0.7, 0, 0, 0]
        # URTest.rtde_c.moveL(targetJointPosition, 0.1, 0.1)
        # time.sleep(5)
        # targetJointPosition = [0.06, -0.21, 0.7, 0, 0, 1.57]
        # URTest.rtde_c.moveL(targetJointPosition, 0.1, 0.1)
        # time.sleep(1)
        # targetJointPosition = [0.06, -0.21, 0.71, 0, 0, 1.57]
        # URTest.rtde_c.moveL(targetJointPosition, 0.1, 0.1)
        # time.sleep(5)
        # targetJointPosition = [0.06, -0.21, 0.7, 0, 0, 1.57]
        # URTest.rtde_c.moveL(targetJointPosition, 0.1, 0.1)
        # time.sleep(1)
        # targetJointPosition = [0.06, -0.21, 0.7, 0, 0, 0]
        # URTest.rtde_c.moveL(targetJointPosition, 0.1, 0.1)
        # time.sleep(5)
        # targetJointPosition = [0.06, -0.21, 0.71, 0, 0, 0]
        # URTest.rtde_c.moveL(targetJointPosition, 0.1, 0.1)
        # time.sleep(1)
        # targetJointPosition = [0.06, -0.21, 0.7, 0, 0, 0]
        # URTest.rtde_c.moveL(targetJointPosition, 0.1, 0.1)
        # time.sleep(5)
        # targetJointPosition = [0.06, -0.21, 0.7, 0, 0, -1.57]
        # URTest.rtde_c.moveL(targetJointPosition, 0.1, 0.1)
        # time.sleep(1)
        # targetJointPosition = [0.06, -0.21, 0.71, 0, 0, -1.57]
        # URTest.rtde_c.moveL(targetJointPosition, 0.1, 0.1)
        # time.sleep(5)
        # targetJointPosition = [0.06, -0.21, 0.7, 0, 0, -1.57]
        # URTest.rtde_c.moveL(targetJointPosition, 0.1, 0.1)
        # time.sleep(1)