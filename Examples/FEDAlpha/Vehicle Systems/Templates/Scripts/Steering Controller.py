from tools import *
from math import *

def on_add_to_universe(self, universe):

    self.Steering_Input = create_input(self, "Steering Input", Types.Type_VxReal)
    self.Front_Axle_Position = create_input(self, "Front Axle Position", Types.Type_VxReal)
    self.Rear_Axle_Position = create_input(self, "Rear Axle Position", Types.Type_VxReal)
    self.Width = create_input(self, "Width", Types.Type_VxReal)
    self.Max_Angle = create_input(self, "Max Angle", Types.Type_VxReal)

    self.Angle_L = create_output(self, "Angle L", Types.Type_VxReal)
    self.Angle_R = create_output(self, "Angle R", Types.Type_VxReal)


def pre_step(self):

    steeringInput = clamp(self.Steering_Input.value, -1.0, 1.0)
    angle = steeringInput * self.Max_Angle.value
    pos_long = self.Front_Axle_Position.value - self.Rear_Axle_Position.value
    pos_lat = self.Width.value / 2.0


    self.outputs.Angle_L.value = compute_angle(pos_long, pos_lat, angle)
    self.outputs.Angle_R.value = compute_angle(pos_long, -pos_lat, angle)

def compute_angle(pos_long, pos_lat, angle):

    outputAngle = 0.0

    tanAngle = tan(angle)
    if( abs(tanAngle) > 0.0000001 ):
        radius = pos_long / tanAngle
        divider = radius + pos_lat
        if( abs(divider) > 0.0000001 ):
            outputAngle = atan(pos_long/divider)
    return outputAngle;
