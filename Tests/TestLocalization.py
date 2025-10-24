import sys
import time
import math
sys.path.append("../build")

from TestEncoder import Encoder
import SmoothBno085
imu = SmoothBno085.SmoothedBNO08x(RefreshFrequency = 100)
Yencoder = Encoder(chan_a=22, chan_b=23)
Xencoder = Encoder(chan_a=17, chan_b=27)

sys.path.append("../Components")

from Localizer import TwoDeadWheelLocalizer,Pose2d

odometry = TwoDeadWheelLocalizer(Pose2d(0,0,0),imu,Yencoder,Xencoder)

while True:

    result = odometry.update()
    sys.stdout.write(f"\rPose: x={result.x_vel:.2f} mm, y={result.y_vel:.2f} mm, heading={math.degrees(result.heading_vel):.1f}°")
    sys.stdout.flush()




