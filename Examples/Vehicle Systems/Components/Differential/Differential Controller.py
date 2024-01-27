# This script models a hydrodynamic torque converter, based on the Vehicle Systems C++ implementation

from tools import *
import math
import csv

def on_add_to_universe(self, universe):

    # ICD inputs
    self.Enable_Differential = create_input(self, "Enable Differential", Types.Type_Bool, True)
    self.Gear_Ratio = create_input(self, "Gear Ratio", Types.Type_VxReal, 1.0)
    self.Torque_Bias = create_input(self, "Torque Bias", Types.Type_VxReal, 0.5)
    self.Lock_Torque = create_input(self, "Lock Torque", Types.Type_VxReal, 0.0)
    self.Lock_Ratio = create_input(self, "Lock Ratio", Types.Type_VxReal, 1.0)
    self.Efficiency = create_input(self, "Efficiency", Types.Type_VxReal, 1.0)

    # Internal inputs
    self.Shaft_1_Speed_In = create_input(self, "Shaft 1 Speed", Types.Type_VxReal)
    self.Shaft_2_Speed_In = create_input(self, "Shaft 2 Speed", Types.Type_VxReal)
    self.Differential_Torque = create_input(self, "Differential Torque", Types.Type_VxReal)

    # ICD outputs
    self.Shaft_1_Speed = create_output(self, "Shaft 1 Speed", Types.Type_VxReal)
    self.Shaft_1_Torque = create_output(self, "Shaft 1 Torque", Types.Type_VxReal)
    self.Shaft_1_Power = create_output(self, "Shaft 1 Power", Types.Type_VxReal)
    self.Shaft_2_Speed = create_output(self, "Shaft 2 Speed", Types.Type_VxReal)
    self.Shaft_2_Torque = create_output(self, "Shaft 2 Torque", Types.Type_VxReal)
    self.Shaft_2_Power = create_output(self, "Shaft 2 Power", Types.Type_VxReal)

    # Internal outputs
    self.Enable_Differential_Out = create_output(self, 'Enable Differential', Types.Type_Bool, True)
    self.Gear_Ratio_1 = create_output(self, "Gear Ratio 1", Types.Type_VxReal, 1.0)
    self.Gear_Ratio_2 = create_output(self, "Gear Ratio 2", Types.Type_VxReal, -0.5)
    self.Gear_Ratio_3 = create_output(self, "Gear Ratio 3", Types.Type_VxReal, -0.5)
    self.Lock_Constraint_Enable = create_output(self, 'Lock_Constraint_Enable', Types.Type_Bool)
    self.Lock_Torque_Positive = create_output(self, "Lock_Torque_Positive", Types.Type_VxReal)
    self.Lock_Torque_Negative = create_output(self, "Lock_Torque_Negative", Types.Type_VxReal)
    self.Lock_Ratio_Out = create_output(self, "Lock Ratio", Types.Type_VxReal, 1.0)
    self.Hinge_1_Friction = create_output(self, 'Hinge 1 Friction', Types.Type_VxReal)
    self.Hinge_2_Friction = create_output(self, 'Hinge 2 Friction', Types.Type_VxReal)


    self.Enable_Differential.setDescription("True to enable differential connection between shafts. When False, lock and friction can still be active.")
    self.Gear_Ratio.setDescription("The gear ratio of the differential")
    self.Torque_Bias.setDescription("The torque bias between shaft 1 and shaft 2. Closer to 1 means higher torque on shaft 1, closer to 0 means higher torque on shaft 2")
    self.Lock_Torque.setDescription("Torque of lock constraint between two output shafts. 0 to disable lock")
    self.Lock_Ratio.setDescription("Gear ratio of lock between two output shafts. Higher number means shaft 1 spins faster")
    self.Efficiency.setDescription("Efficiency of coupling. Friction is applied to output shafts proportional to the power transmitted through the differential")
    self.Shaft_1_Speed_In.setDescription("Speed of output shaft 1 from the hinge")
    self.Shaft_2_Speed_In.setDescription("Speed of output shaft 2 from the hinge")
    self.Differential_Torque.setDescription("Torque of differential constraint")

    self.Shaft_1_Speed.setDescription("Speed of output shaft 1 in rad/s")
    self.Shaft_1_Torque.setDescription("Net torque on output shaft 1 in N.m")
    self.Shaft_1_Power.setDescription("Net power on output shaft 1 in W")
    self.Shaft_2_Speed.setDescription("Speed of output shaft 2 in rad/s")
    self.Shaft_2_Torque.setDescription("Net torque on output shaft 2 in N.m")
    self.Shaft_2_Power.setDescription("Net power on output shaft 2 in W")

    self.Enable_Differential_Out.setDescription("Enable differential constraint")
    self.Gear_Ratio_1.setDescription("Ratio of part 1 of differential constraint (input shaft)")
    self.Gear_Ratio_2.setDescription("Ratio of part 2 of differential constraint (output shaft 1)")
    self.Gear_Ratio_3.setDescription("Ratio of part 3 of differential constraint (output shaft 2)")
    self.Lock_Constraint_Enable.setDescription("Enable lock hinge constraint")
    self.Lock_Torque_Positive.setDescription("Torque of lock hinge")
    self.Lock_Torque_Negative.setDescription("Torque of lock hinge")
    self.Lock_Ratio_Out.setDescription("Gear ratio of lock constraint")
    self.Hinge_1_Friction.setDescription("Friction of hinge constraint 1")
    self.Hinge_2_Friction.setDescription("Friction of hinge constraint 2")


def pre_step(self):

    # - Differential ---------------------------------

    self.Enable_Differential_Out.value = self.Enable_Differential.value
    self.Gear_Ratio_1.value = 1.0 / self.Gear_Ratio.value 
    self.Gear_Ratio_2.value = - self.Torque_Bias.value
    self.Gear_Ratio_3.value = self.Torque_Bias.value - 1.0

    # - Lock ---------------------------------

    self.Lock_Constraint_Enable.value = self.Lock_Torque.value > 0.000001
    self.Lock_Torque_Positive.value = self.Lock_Torque.value
    self.Lock_Torque_Negative.value = - self.Lock_Torque.value
    self.Lock_Ratio_Out.value = -self.Lock_Ratio.value


    # - Friction and Efficiency ---------------------------------

    # Differential constraint reports internal torque, which must be multiplied by each ratio for shaft torque
    # Constraint keeps reporting last value when constraint is disabled, so set to 0 in this case
    # Negative due to convention of constraint
    input_torque = self.Differential_Torque.value if self.Enable_Differential_Out.value else 0.0
    # Output torque is scaled by gear ratios
    output_torque_1 = input_torque * self.Gear_Ratio_2.value
    output_torque_2 = input_torque * self.Gear_Ratio_3.value

    self.Hinge_1_Friction.value = abs(output_torque_1) * (1.0 - self.Efficiency.value)
    self.Hinge_2_Friction.value = abs(output_torque_2) * (1.0 - self.Efficiency.value)

    self.Shaft_1_Speed.value = self.Shaft_1_Speed_In.value
    # Field reports net torque, so subtract friction torque from output torque
    # Since friction could be + or -, must use abs for subtraction, then reapply sign.
    self.Shaft_1_Torque.value = math.copysign(max(abs(output_torque_1) - self.Hinge_1_Friction.value, 0), output_torque_1)
    self.Shaft_1_Power.value = self.Shaft_1_Speed.value * self.Shaft_1_Torque.value
    self.Shaft_2_Speed.value = self.Shaft_2_Speed_In.value
    self.Shaft_2_Torque.value = math.copysign(max(abs(output_torque_2) - self.Hinge_2_Friction.value, 0), output_torque_2)
    self.Shaft_2_Power.value = self.Shaft_2_Speed.value * self.Shaft_2_Torque.value
