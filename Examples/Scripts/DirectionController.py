from VxSim import *
import time
import math


def on_add_to_universe(self, universe):

    """ Create necessary inputs, outputs and parameters"""
    CreateInput(self, 'Ground', Types.Type_VxMatrix44)
    CreateInput(self, 'Chassis', Types.Type_VxMatrix44)
    CreateInput(self, 'KP', Types.Type_VxReal)
    CreateInput(self, 'Look Ahead Distance', Types.Type_VxReal)
    CreateInput(self, 'Low Pass Filter', Types.Type_VxReal)
    
    CreateOutput(self, 'Steering', Types.Type_VxReal)

    CreateParameter( self, 'Steering Max Angle', Types.Type_VxReal)
    
    self.PV_prev = 0
    self.b0 = 0
    
    #if self.inputs.Ground != None and self.inputs.Chassis != None:
    #    self.b0 = compute_b(self)
    #    print self.b0


def compute_b(self):

    return getTranslation(self.inputs.Ground.value.inverse() * self.inputs.Chassis.value).y
    #position_ground = getTranslation(self.inputs.Ground.value)
    #position_chassis = getTranslation(self.inputs.Chassis.value)
    #position_c_g = position_chassis - position_ground    
    #axis_y = self.inputs.Ground.value.axis(1)
    #return axis_y.dot(position_c_g)
    
def pre_step(self):

    #dt = self.getApplicationContext().getFrame()

    KP = self.inputs.KP.value
    Low_Pass_Filter = self.inputs.Low_Pass_Filter.value
    
    # offest from vehicle centre to desired line
    offset = compute_b(self)# - self.b0
    # angle from front of vehicle to desired direction
    rot = getRotation(self.inputs.Ground.value.inverse() * self.inputs.Chassis.value).z

    # angle pointing at a point distance L from vehicle position
    PV = math.atan2(offset, max(self.inputs.Look_Ahead_Distance.value, 2.0)) + rot
    
    PV_Prev = self.PV_prev
    
    PV_Filtered = PV_Prev + Low_Pass_Filter * ( PV - PV_Prev)
    
    SP = 0.0 #target
    P = KP * ( SP-PV_Filtered)
    
    self.outputs.Steering.value = - P * 180 / math.pi / max(self.parameters.Steering_Max_Angle.value, 1.0)

    self.PV_prev = PV_Filtered

    
# USER DEFINED FUNCTIONS
   
def CreateInput(extension, name, type):
    input = extension.getInput(name) 
    if input is None:
       input = extension.addInput(name, type)

def CreateOutput(extension, name, type):
    output = extension.getOutput(name)
    if output is None:
       output = extension.addOutput(name, type)

def CreateParameter(extension, name, type):
    param = extension.getParameter(name)
    if param is None:
       param = extension.addParameter(name, type)