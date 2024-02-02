from VxSim import *
from Interpolate import *
import time
from bisect import bisect_left

def on_add_to_universe(self, universe):

    """ Create necessary inputs, outputs and parameters"""
    CreateInput(self, 'Target Speed', Types.Type_VxReal)
    CreateInput(self, 'Actual Speed', Types.Type_VxReal)
    CreateInput(self, 'KP', Types.Type_VxReal)
    CreateInput(self, 'KI', Types.Type_VxReal)
    CreateInput(self, 'KD', Types.Type_VxReal)
    CreateInput(self, 'Low Pass Filter', Types.Type_VxReal)
    CreateInput(self, 'Braking Factor', Types.Type_VxReal)
    CreateInput(self, 'SP Change Rate', Types.Type_VxReal)
    CreateInput(self, 'Low Speed', Types.Type_VxReal)
    CreateInput(self, 'High Speed', Types.Type_VxReal)
    CreateInput(self, 'Constant Scale At Low Speed', Types.Type_VxReal)

    CreateOutput(self, 'Throttle', Types.Type_VxReal)
    
    self.inputs.Target_Speed.setDescription('Target vehicle speed in km/h')
    self.inputs.Actual_Speed.setDescription('Actual vehicle speed in km/h')  # vehicle system chassis speed is connected here.
    
    self.PV_prev = 0
    self.I_prev = 0
    self.SP_Prev = 0
    
    self.COMin = -1.0 * self.inputs.Braking_Factor.value
    self.COMax = 1.0
    
    self.kphToMeterPerSec = 1/3.6

    self.constantScale = LinearInterpolation([0.0, self.inputs.Low_Speed.value, self.inputs.High_Speed.value, 120.0], \
                                             [self.inputs.Constant_Scale_At_Low_Speed.value, self.inputs.Constant_Scale_At_Low_Speed.value, 1.0, 1.0] )

            
def pre_step(self):

    dt = 1 / self.getApplicationContext().getSimulationFrameRate()
    
    scale = self.constantScale(self.inputs.Actual_Speed.value)

    KP = self.inputs.KP.value * scale
    KD = self.inputs.KD.value * scale
    KI = self.inputs.KI.value * scale
    Low_Pass_Filter = self.inputs.Low_Pass_Filter.value
    
    PV = self.inputs.Actual_Speed.value * self.kphToMeterPerSec
    PV_Prev = self.PV_prev
    
    PV_Filtered = PV_Prev + Low_Pass_Filter * ( PV - PV_Prev)

    NewSP = self.inputs.Target_Speed.value
    SPIncrement = self.inputs.SP_Change_Rate.value * dt
    SP = min(max(NewSP, self.SP_Prev - SPIncrement), self.SP_Prev + SPIncrement)
    self.SP_Prev = SP
    SP *= self.kphToMeterPerSec

    P = KP * ( SP-PV_Filtered)
    D = KD * ( PV_Prev - PV_Filtered) / dt
    I = self.I_prev + KI * dt * (SP-PV_Filtered)
    
    # Integral anti-windup
    self.I_prev = min(max(I, self.COMin - 0.2*(P+D)), self.COMax - 0.2*(P+D))
    
    CO = P + I + D
    #print 'SP: {:4.2f}, P: {:4.2f}, I: {:4.2f}'.format(SP / self.kphToMeterPerSec, P, I)

    if CO < 0.0:
        CO = CO * self.inputs.Braking_Factor.value

    self.outputs.Throttle.value = min(max(CO, self.COMin), self.COMax);
    #self.outputs.Throttle.value=3.0
	
    self.PV_prev = PV_Filtered
    
    return
   
   
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
