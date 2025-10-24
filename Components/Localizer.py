import math
from dataclasses import dataclass


@dataclass
class Pose2d:
    x: float
    y: float
    heading: float  # radians

    def plus(self, twist):
        """Applies a small twist to update pose."""
        dx, dy, dtheta = twist
        cos_h = math.cos(self.heading)
        sin_h = math.sin(self.heading)
        # rotate local motion into global frame
        global_dx = dx * cos_h - dy * sin_h
        global_dy = dx * sin_h + dy * cos_h
        return Pose2d(self.x + global_dx, self.y + global_dy, self.heading + dtheta)


@dataclass
class PoseVelocity2d:
    x_vel: float
    y_vel: float
    heading_vel: float


class TwoDeadWheelLocalizer:
    """
    Two-dead-wheel localizer using:
    - par encoder: parallel (along robot forward X)
    - perp encoder: perpendicular (along robot sideways Y)
    - imu heading (radians)
    """

    class Params:
        par_y_ticks = 4.039   # y position of parallel encoder (ticks)
        perp_x_ticks = 193.524  # x position of perpendicular encoder (ticks)

    def __init__(self, initial_pose: Pose2d, imu,par,perp):
        self.par = par  # you will handle encoder reading
        self.perp = perp
        self.imu = imu

        self.pose = initial_pose

        self.last_par_pos = 0
        self.last_perp_pos = 0
        self.last_heading = 0.0
        self.initialized = False

        self.last_raw_heading_vel = 0.0
        self.heading_vel_offset = 0.0

        self.PARAMS = self.Params()

    def set_pose(self, pose: Pose2d):
        self.pose = pose

    def get_pose(self) -> Pose2d:
        return self.pose

    def update(self):
        """
        Update odometry using:
          - par_pos, perp_pos (encoder positions in ticks)
          - par_vel, perp_vel (encoder velocities in ticks/sec)
          - heading (radians, from IMU)
          - heading_vel (radians/sec, from IMU)
        Returns current PoseVelocity2d.
        """ 
        
        yaw_vel = math.radians(self.imu.getVelocity()[0])
        yaw = math.radians(self.imu.getAngle()[0])

        if not self.initialized:
            self.last_par_pos = self.par.currpos
            self.last_perp_pos = self.perp.currpos
            self.last_heading = yaw
            self.initialized = True
            return PoseVelocity2d(0.0, 0.0, 0.0)

        # Deltas
        par_delta = self.par.currpos - self.last_par_pos
        perp_delta = self.perp.currpos - self.last_perp_pos
        heading_delta = yaw - self.last_heading

        # Correct for rotation (based on encoder offset distances)
        dx_local = (par_delta - self.PARAMS.par_y_ticks * heading_delta)
        dy_local = (perp_delta - self.PARAMS.perp_x_ticks * heading_delta)

        # Update global pose
        self.pose = self.pose.plus((dx_local, dy_local, heading_delta))

        # Save last states
        self.last_par_pos = self.par.currpos
        self.last_perp_pos = self.perp.currpos
        self.last_heading = yaw

        # Compute velocities (already in ticks/s → convert to mm/s)
        vx_local = (self.par.velocity - self.PARAMS.par_y_ticks * yaw_vel)
        vy_local = (self.perp.velocity - self.PARAMS.perp_x_ticks * yaw_vel)

        # Convert to global frame
        cos_h = math.cos(yaw)
        sin_h = math.sin(yaw)
        vx_global = vx_local * cos_h - vy_local * sin_h
        vy_global = vx_local * sin_h + vy_local * cos_h

        self.imu.update()
        self.par.update()
        self.perp.update()

        return PoseVelocity2d(vx_global, vy_global, yaw_vel)
