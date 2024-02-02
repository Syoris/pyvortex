# Calculates some useful values from wheel speed and torque

from tools import *
import math

def on_add_to_universe(self, universe):

    # ICD inputs
    self.Radius = create_input(self, 'Radius', Types.Type_VxReal, 0.5)
    self.Braking_Torque = create_input(self, 'Braking Torque', Types.Type_VxReal, 0.0)

    # Internal inputs
    self.Gear_Ratio_Torque = create_input(self, 'Gear Ratio Torque', Types.Type_VxReal)
    self.Output_Shaft_Speed = create_input(self, 'Output Shaft Speed', Types.Type_VxReal)

    # Parameters

    # ICD outputs
    self.Wheel_Speed = create_output(self, 'Wheel Speed', Types.Type_VxReal)
    self.Shaft_Speed = create_output(self, "Shaft Speed", Types.Type_VxReal)
    self.Shaft_Torque = create_output(self, "Shaft Torque", Types.Type_VxReal)
    self.Shaft_Power = create_output(self, "Shaft Power", Types.Type_VxReal)

    # Internal outputs
    self.Braking_Torque_Positive = create_output(self, "Braking Torque Positive", Types.Type_VxReal)
    self.Braking_Torque_Negative = create_output(self, "Braking Torque Negative", Types.Type_VxReal)

    # Descriptions
    self.Radius.setDescription("Radius of cylinder representing the wheel")
    self.Gear_Ratio_Torque.setDescription("Torque of gear ratio constraint")
    self.Output_Shaft_Speed.setDescription("Speed of the output shaft from the hinge of this component")

    self.Wheel_Speed.setDescription("Effective linear speed of wheel")
    self.Shaft_Speed.setDescription("Speed of output shaft in rad/s")
    self.Shaft_Torque.setDescription("Net torque on output shaft in N.m")
    self.Shaft_Power.setDescription("Net power on output shaft in W")


def pre_step(self):

    self.Braking_Torque_Positive.value = self.Braking_Torque.value
    self.Braking_Torque_Negative.value = -self.Braking_Torque.value

    # - Wheel Speed and Torque ---------------------------------

    # Calculate speeds of wheel
    # Car Wheel constraint velocity is negative for forward rolling
    self.Wheel_Speed.value = - self.Output_Shaft_Speed.value * self.Radius.value
    self.Shaft_Speed.value = self.Output_Shaft_Speed.value
    # Field reports net torque, so subtract friction torque from output torque
    # Since friction could be + or -, must use abs for subtraction, then reapply sign.
    self.Shaft_Torque.value = self.Gear_Ratio_Torque.value
    self.Shaft_Power.value = self.Shaft_Speed.value * self.Shaft_Torque.value
