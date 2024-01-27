# This script provides a simplified interface to define the locations of drivetrain components 
# and wheels of a vehicle. Drivetrain components are placed in a line starting from the 
# specified location. Wheels are positioned symmetrical to the vehicle centre based on the 
# specified dimensions. The script assumes the vehicle is x-forward

from tools import *
import math

def on_add_to_universe(self, universe):

    create_input(self, 'Enable', Types.Type_Bool).setDescription("True to update positions")
    create_parameter(self, 'Drivetrain Position', Types.Type_VxVector3).setDescription("Position relative to the Chassis to place the first drivetrain component")
    create_parameter(self, 'Drivetrain Spacing', Types.Type_VxReal).setDescription("Each successive drivetrain component is placed this distance in front of the previous")
    create_parameter(self, 'Wheel Position Front', Types.Type_VxReal).setDescription("Position of front axle")
    create_parameter(self, 'Wheel Position Rear', Types.Type_VxReal).setDescription("Position of rear axle")
    create_parameter(self, 'Wheel Spacing', Types.Type_VxReal).setDescription("Distance between left and right wheels")
    create_parameter(self, 'Wheel Height', Types.Type_VxReal).setDescription("Vertical position of wheels")

    create_output(self, 'Engine Transform', Types.Type_VxMatrix44)
    create_output(self, 'Clutch Transform', Types.Type_VxMatrix44)
    create_output(self, 'Transmission Transform', Types.Type_VxMatrix44)
    create_output(self, 'Transfer Case Transform', Types.Type_VxMatrix44)
    create_output(self, 'Differential F Transform', Types.Type_VxMatrix44)
    create_output(self, 'Differential R Transform', Types.Type_VxMatrix44)
    create_output(self, 'Double Wishbone F Transform', Types.Type_VxMatrix44)
    create_output(self, 'Double Wishbone R Transform', Types.Type_VxMatrix44)
    create_output(self, 'Wheel FL Transform', Types.Type_VxMatrix44)
    create_output(self, 'Wheel FR Transform', Types.Type_VxMatrix44)
    create_output(self, 'Wheel RL Transform', Types.Type_VxMatrix44)
    create_output(self, 'Wheel RR Transform', Types.Type_VxMatrix44)

def paused_update(self):
    config_update(self)

def config_update(self):
    # Skip update if disabled
    if not self.inputs.Enable.value:
        return

    # Place drivtrain components in a row with fixed spacing between each
    pos = self.parameters.Drivetrain_Position.value
    self.outputs.Engine_Transform.value = createTranslation(pos)
    pos.x += self.parameters.Drivetrain_Spacing.value
    self.outputs.Clutch_Transform.value = createTranslation(pos)
    pos.x += self.parameters.Drivetrain_Spacing.value
    self.outputs.Transmission_Transform.value = createTranslation(pos)
    pos.x += self.parameters.Drivetrain_Spacing.value
    self.outputs.Transfer_Case_Transform.value = createTranslation(pos)

    # Differentials and DW suspension go at the centre of each axle
    pos = VxVector3(self.parameters.Wheel_Position_Front.value, 0.0, self.parameters.Wheel_Height.value)
    self.outputs.Differential_F_Transform.value = createTranslation(pos)
    self.outputs.Double_Wishbone_F_Transform.value = createTranslation(pos)
    pos.x = self.parameters.Wheel_Position_Rear.value
    self.outputs.Differential_R_Transform.value = createTranslation(pos)
    self.outputs.Double_Wishbone_R_Transform.value = createTranslation(pos)

    # Place wheels
    pos = VxVector3(self.parameters.Wheel_Position_Front.value, self.parameters.Wheel_Spacing.value/2.0, self.parameters.Wheel_Height.value)
    self.outputs.Wheel_FL_Transform.value = createTranslation(pos)
    pos.y = -pos.y
    self.outputs.Wheel_FR_Transform.value = createTranslation(pos)
    pos.x = self.parameters.Wheel_Position_Rear.value
    self.outputs.Wheel_RR_Transform.value = createTranslation(pos)
    pos.y = -pos.y
    self.outputs.Wheel_RL_Transform.value = createTranslation(pos)
