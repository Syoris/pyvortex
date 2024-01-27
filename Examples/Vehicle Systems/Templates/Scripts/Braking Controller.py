# This script is calculates the front and rear braking torques based on max torque and bias

from tools import *

def on_add_to_universe(self, universe):

    self.Brake_Input = create_input(self, "Brake Input", Types.Type_VxReal, 0)
    self.Max_Torque = create_input(self, "Max Torque", Types.Type_VxReal, 1000)
    self.Front_Rear_Bias = create_input(self, "Front Rear Bias", Types.Type_VxReal, 0.6)

    self.Braking_Torque_F = create_output(self, "Braking Torque F", Types.Type_VxReal)
    self.Braking_Torque_R = create_output(self, "Braking Torque R", Types.Type_VxReal)
    
def pre_step(self):
    self.Braking_Torque_F.value = self.Max_Torque.value * self.Brake_Input.value
    self.Braking_Torque_R.value = (self.Max_Torque.value * self.Brake_Input.value 
                                   * (1 - self.Front_Rear_Bias.value) / self.Front_Rear_Bias.value)
