# This script models a hydrodynamic torque converter, based hydrodynamic theory

from tools import *
import math
import csv

def on_add_to_universe(self, universe):

    # ICD inputs
    self.Coupling_Torque_Scale = create_input(self, "Coupling Torque Scale", Types.Type_VxReal, 1)
    self.Coupling_Torque_Added = create_input(self, "Coupling Torque Added", Types.Type_VxReal, 0)
    self.Stall_RPM = create_input(self, "Stall RPM", Types.Type_VxReal, 1000)
    self.Stall_Torque = create_input(self, "Stall Torque", Types.Type_VxReal, 100)
    self.Torque_Multiplication = create_input(self, "Torque Multiplication", Types.Type_VxReal, 1)
    self.Slip = create_input(self, "Slip", Types.Type_VxReal, 1)

    # Internal inputs
    self.Input_Shaft_Speed = create_input(self, "Input Shaft Speed", Types.Type_VxReal)
    self.Output_Shaft_Speed = create_input(self, "Output Shaft Speed", Types.Type_VxReal)

    # Parameters
    self.Lambda_Table = create_parameter(self, "Lambda Table", Types.Type_VxFilename)

    # ICD outputs
    self.Speed_Ratio = create_output(self, "Speed Ratio", Types.Type_VxReal)
    self.Shaft_RPM = create_output(self, "Shaft RPM", Types.Type_VxReal)
    self.Coupling_Torque = create_output(self, "Coupling Torque", Types.Type_VxReal)
    self.Shaft_Speed = create_output(self, "Shaft Speed", Types.Type_VxReal)
    self.Shaft_Torque = create_output(self, "Shaft Torque", Types.Type_VxReal)
    self.Shaft_Power = create_output(self, "Shaft Power", Types.Type_VxReal)

    # Internal outputs
    self.Coupling_Torque_Negative = create_output(self, "Coupling Torque Negative", Types.Type_VxReal)
    self.Multiplication_Torque = create_output(self, "Multiplication Torque", Types.Type_VxReal)
    self.Multiplication_Desired_RPM = create_output(self, "Multiplication Desired RPM", Types.Type_VxReal)
    self.Constraint_Loss = create_output(self, "Constraint Loss", Types.Type_VxReal)


    self.Coupling_Torque_Scale.setDescription("Multiplies the coupling torque calculated from the torque converter model")
    self.Coupling_Torque_Added.setDescription("Torque that is directly added to the coupling torque. This can be used to simulate a locking mechanism. A negative torque can be used to reduce the overall coupling")
    self.Stall_RPM.setDescription("Stall RPM")
    self.Stall_Torque.setDescription("Stall torque")
    self.Torque_Multiplication.setDescription("Torque multiplication factor at 0 speed ratio")
    self.Slip.setDescription("Amount of slip to allow when speed ratio is near 1. Setting this lower will result in less slip at high speed, but can cause instability")
    self.Input_Shaft_Speed.setDescription("Speed of input shaft, from previous component")
    self.Output_Shaft_Speed.setDescription("Speed of the output shaft from the hinge of this component")
    self.Lambda_Table.setDescription("Torque converter lambda table filename in csv format. If blank, default table will be used")
    self.Speed_Ratio.setDescription("Speed ratio, output shaft / input shaft")
    self.Shaft_RPM.setDescription("Speed of output shaft in RPM")
    self.Coupling_Torque.setDescription("Torque applied to coupling constraint")
    self.Shaft_Speed.setDescription("Speed of output shaft in rad/s")
    self.Shaft_Torque.setDescription("Net torque on output shaft in N.m")
    self.Shaft_Power.setDescription("Net power on output shaft in W")
    self.Coupling_Torque_Negative.setDescription("Negative of torque to be applied to coupling constraint")
    self.Multiplication_Torque.setDescription("Torque to be applied to hinge constraint to simulate torque multiplication")
    self.Multiplication_Desired_RPM.setDescription("Desired RPM of hinge constraint to simulate torque multiplication")
    self.Constraint_Loss.setDescription("Loss to set in gear ratio constraint, based on slip")


    # Generate a lambda curve from a polynomial, since it's smoother than interpolated points
    self.lambda_coefficients = [-2.0037, 1.3181, -0.2758, 1.0]
    # self.lambda_coefficients = [-2.7604, 3.4129, -1.9984, 0.371, 0.978]
    self.lambda_overspeed_table = LinearInterpolation([0, 1, 2], [0, 0, 1])


def pre_step(self):

    # Calculate drag coefficient that corresponds to stall RPM and torque
    if self.Stall_Torque.value <= 0 or self.Stall_RPM.value <= 0:
        self.drag_coeff = 0
        raise ValueError("Stall Torque or Stall RPM invalid")
    else:        
        self.drag_coeff = self.Stall_Torque.value / (self.Stall_RPM.value * math.pi/30.0)**2 / calculate_lambda(self, 0)

    # Torque multiplier is max at 0 speed ratio, reduces to 0 at 0.8 speed ratio
    self.mult_table = LinearInterpolation([0, 0.8, 1], 
                                         [self.Torque_Multiplication.value, 0, 0])

    # Calculate input shaft speed in rad/s, avoid negative rotation or infinite value when used in denominator
    input_speed = max(self.Input_Shaft_Speed.value, 0.0001)
    # Calculate speed ratio, cap at 10 since it's meaningless when high anyway
    sr = min(max(self.Output_Shaft_Speed.value / input_speed, 0), 10.0)
    # Calculate lambda

    # Calculate coupling force from standard TC model, plus lock torque
    coupling = max(input_speed**2 * self.drag_coeff * self.Coupling_Torque_Scale.value * calculate_lambda(self, sr)
                + self.Coupling_Torque_Added.value, 0.001)

    self.Coupling_Torque.value = coupling

    mult_torque = self.Coupling_Torque.value * max(self.mult_table(sr) - 1, 0)


    self.Speed_Ratio.value = sr

    self.Shaft_Speed.value = self.Output_Shaft_Speed.value
    self.Shaft_Torque.value = self.Coupling_Torque.value + self.Multiplication_Torque.value
    self.Shaft_Power.value = self.Shaft_Speed.value * self.Shaft_Torque.value

    self.Coupling_Torque_Negative.value = -self.Coupling_Torque.value
    self.Multiplication_Torque.value = mult_torque
    self.Multiplication_Desired_RPM.value = input_speed

    # Set loss in the gear ratio. This is derived by determining the loss that would estimate the behaviour
    # of the steep part of the lambda curve.
    self.Constraint_Loss.value = self.Slip.value / (self.drag_coeff * self.Stall_RPM.value)
	
    self.Shaft_RPM.value=self.Shaft_Speed.value*30./math.pi

def calculate_lambda(self, sr):
    if sr <= 1:
        return polynomial(sr, self.lambda_coefficients)
    else:
        return self.lambda_overspeed_table(sr)

def polynomial(input, coefficients):
    res = 0
    order = len(coefficients)
    for i, a in enumerate(coefficients):
        # print "a: {:6.2f}, exp: {}".format(a, order-i-1)
        res += a*input**(order-i-1)
    return res
