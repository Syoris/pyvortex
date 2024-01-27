# This script could eventually become a full torque converter model, but currently it is a basic automatic clutch that 
# engages linearly between the Engage Min RPM and Engage Max RPM. 

from tools import *
import math

def on_add_to_universe(self, universe):

    # ICD inputs
    create_input(self, 'Engage Min RPM', Types.Type_VxReal).setDescription("RPM to start engaging clutch")
    create_input(self, 'Engage Max RPM', Types.Type_VxReal).setDescription("RPM where clutch is fully engaged and max torque is applied")
    create_input(self, 'Max Torque', Types.Type_VxReal).setDescription("Max torque to apply at Engine Max RPM")

    # Internal inputs
    create_input(self, 'Input RPM', Types.Type_VxReal).setDescription("RPM of input shaft")
    create_input(self, 'Shaft Speed', Types.Type_VxReal).setDescription("Speed of output shaft")

    # ICD outputs
    create_output(self, 'Shaft RPM', Types.Type_VxReal).setDescription("Speed of output shaft in RPM")
    create_output(self, 'Coupling Torque', Types.Type_VxReal).setDescription("Torque applied to coupling constraint")

    # Internal outputs
    create_output(self, 'Coupling Torque Negative', Types.Type_VxReal).setDescription("Min torque to be applied to coupling constraint")

    # Linear interpolation between 0 and Max Torque as RPM goes from Engage Min to Engage Max
    self.engage = LinearInterpolation([0, self.inputs.Engage_Min_RPM.value, self.inputs.Engage_Max_RPM.value, 100000], 
                                         [0, 0, self.inputs.Max_Torque.value, self.inputs.Max_Torque.value])

def pre_step(self):

    torque = self.engage(self.inputs.Input_RPM.value)
    self.outputs.Coupling_Torque_Negative.value = -torque
    self.outputs.Coupling_Torque.value = torque
    self.outputs.Shaft_RPM.value = self.inputs.Shaft_Speed.value * 60 / 2 / math.pi

