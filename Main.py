#47 grade max oriz
#-11 grade max oriz
import sys

sys.path.append("./build")
sys.path.append("./Components")
sys.path.append("./Drivers")
sys.path.append("./InstructionsImplemetation")


from Scheduler import Scheduler
import time
from typing import List, Callable, Any, Deque
from collections import deque
import math
from math import fmod

from ClientPhotoSender import ClientPhotoSender
from ServoDriver import Servo
import SmoothBno085
from DriveTrain import DriveTrain


imu = SmoothBno085.SmoothedBNO08x(RefreshFrequency=100)
dt = DriveTrain()
client = ClientPhotoSender()
Claw = Servo(12)
Claw.setAngle(320)
yaw = 0
mapped = 0

kP = -0.025

def getAngleDifference(target, current):
    diff = fmod(target - current + 180.0, 360.0)
    if diff < 0:
        diff += 360.0
    return diff - 180.0

def map_range(x, old_min, old_max, new_min, new_max):
    return new_min + (x - old_min) * (new_max - new_min) / (old_max - old_min)

# Example usage:

doing_what = 0

def align_with_target():
    global yaw, mapped
    yaw = imu.getAngle()[0]
    mapped = map_range(client.result[1][0], -11, 47, -24, 24)
    difference = getAngleDifference(-mapped, yaw)
    dt.drive(0, 0, difference * kP)
    time.sleep(0.02)

def align_with_target_2():
    global yaw, mapped
    yaw = imu.getAngle()[0]
    mapped = map_range(client.result[1][0], -11, 47, -24, 24)
    difference = getAngleDifference(-mapped, yaw)
    dt.drive(0, 0.4, difference * kP)
    time.sleep(0.02)

def change_what(val):
    global doing_what
    doing_what = val

scheduler = Scheduler()\
        .add_task(
            lambda: (
                client.start_sending_packets(),
                time.sleep(1),
            ),
            lambda: len(client.result) > 1
        )\
        .add_task(
            lambda: (
            change_what(1),
            ),
            lambda: getAngleDifference(mapped, yaw) < 1.0
        )\
        .wait_seconds(3)\
        .add_task(
            lambda: (
            change_what(2),
            ),
            lambda: True
        )\
        .wait_seconds(2)\
        .add_task(
            lambda: (
            change_what(0),
            Claw.setAngle(0)
            ),
            lambda: True
        )\
        .wait_seconds(0.5)\
        .add_task(
            lambda: (
            dt.drive(0,-0.2,0)
            ),
            lambda: True
        )\
        .wait_seconds(2)\
        .add_task(
            lambda: (
            dt.drive(0,0,0)
            ),
            lambda: True
        )\


while not scheduler.is_done():

    if doing_what == 1:
        align_with_target()
        print("doing 1")
    elif doing_what == 2:
        align_with_target_2()
        print("doing 2")

    print(doing_what)
    
    scheduler.update()
    imu.update()

print(map_range(client.result[1][0], -11, 47, -29, 29))