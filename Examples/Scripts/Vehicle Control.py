from VxSim import *
from Interpolate import *
import math

def on_add_to_universe(self, universe):
    # print dir(Types)
    
    CreateInput(self, 'Throttle Input', Types.Type_VxReal)
    CreateInput(self, 'Steering Input', Types.Type_VxReal)
    CreateInput(self, 'Cruise Control Active', Types.Type_Bool)
    CreateInput(self, 'Cruise Control Throttle', Types.Type_VxReal)
    CreateInput(self, 'Direction Control Active', Types.Type_Bool)
    CreateInput(self, 'Direction Control Steering', Types.Type_VxReal)
    CreateInput(self, 'Low Range Active', Types.Type_Bool)
    CreateInput(self, 'Engine RPM', Types.Type_VxReal)
    CreateInput(self, 'TC Output RPM', Types.Type_VxReal)
    CreateInput(self, 'Current Gear', Types.Type_Int)

    CreateOutput(self, 'Throttle Output', Types.Type_VxReal)
    CreateOutput(self, 'Steering Output', Types.Type_VxReal)
    CreateOutput(self, 'Final Gear Ratio', Types.Type_VxReal, default_value=4.88)
    CreateOutput(self, "Torque Converter Scale", Types.Type_VxReal)
    CreateOutput(self, 'Torque Converter Lock', Types.Type_VxReal)

	
    CreateParameter(self, 'High Gear Range', Types.Type_VxReal, default_value=4.88)
	
    self.maxThrottle = 1.0
    self.shiftThrottle = 0.8
    self.shiftTime = 0.8
    self.shiftTimer = 0.0
    
    # Steering
    self.pitmanMaxAngle = 0.489 # Limit of pitman travel

    # Torque Converter Decoupling
    self.TCMax = 0.4
    self.TCRPM = 830.0

    # Torque Converter Locking
    self.TCLockTorque = 800.0
    self.QuickThrottle = 0.9
    self.MaxRPM = 2500.0
	
    quickThrottle = [0.0, 0.5, 0.9, 1.0]

    self.UpShift = [LinearInterpolation(quickThrottle, [1750.0, 1750.0, 2400.0, 2400.0]),
                    LinearInterpolation(quickThrottle, [1750.0, 1750.0, 2400.0, 2400.0]),
                    LinearInterpolation(quickThrottle, [1750.0, 1750.0, 2400.0, 2400.0]),
                    LinearInterpolation(quickThrottle, [1750.0, 1750.0, 2350.0, 2350.0]),
                    LinearInterpolation(quickThrottle, [1750.0, 1750.0, 2350.0, 2350.0]),
                    LinearInterpolation(quickThrottle, [5000.0, 5000.0, 5000.0, 5000.0])]

    self.DownShift = [LinearInterpolation(quickThrottle, [0.0, 0.0, 0.0, 0.0]),
                      LinearInterpolation(quickThrottle, [860.0, 860.0, 860.0, 860.0]),
                      LinearInterpolation(quickThrottle, [1000.0, 1000.0, 1150.0, 1150.0]),
                      LinearInterpolation(quickThrottle, [1100.0, 1100.0, 1350.0, 1350.0]),
                      LinearInterpolation(quickThrottle, [1100.0, 1100.0, 1500.0, 1500.0]),
                      LinearInterpolation(quickThrottle, [1100.0, 1100.0, 1750.0, 1750.0])]

    self.TCLockQuick = LinearInterpolation([1, 2, 3, 4, 5, 6], [23749, 12719, 2370, 2350, 2350, 2350])
    self.TCUnlockQuick = LinearInterpolation([1, 2, 3, 4, 5, 6], [415, 1161, 879, 600, 600, 600])
    self.TCLock = LinearInterpolation([1, 2, 3, 4, 5, 6], [23749, 12719, 2000, 2000, 1700, 1700])
    self.TCUnlock = LinearInterpolation([1, 2, 3, 4, 5, 6], [415, 1000, 879, 600, 600, 600])

    # Low Gear Range
    self.HighGearRange = self.parameters.High_Gear_Range.value
    self.LowGearRange = self.HighGearRange * 2.75
	

def pre_step(self):
    timeStep = self.getApplicationContext().getSimulationTimeStep()
    
    # Throttle input used for throttle (+) and braking (-) signals
    throttleInput = min(self.inputs.Cruise_Control_Throttle.value if self.inputs.Cruise_Control_Active.value else self.inputs.Throttle_Input.value, self.maxThrottle)
        
    # Throttle
    self.outputs.Throttle_Output.value = min(self.inputs.Cruise_Control_Throttle.value if self.inputs.Cruise_Control_Active.value else self.inputs.Throttle_Input.value, self.maxThrottle)
    
    # Steering
    self.outputs.Steering_Output.value = self.inputs.Direction_Control_Steering.value if self.inputs.Direction_Control_Active.value else self.inputs.Steering_Input.value
	
    # Torque converter engages too much at low RPM, so lower the scale 
    self.outputs.Torque_Converter_Scale.value = min(max((self.inputs.Engine_RPM.value - self.TCRPM)/(300.0), 0.0), self.TCMax)
	
    # Torque converter locking based on data provided
    if ((throttleInput >= self.QuickThrottle and self.inputs.Engine_RPM.value >= self.TCLockQuick(self.inputs.Current_Gear.value)) \
            or (throttleInput <  self.QuickThrottle and self.inputs.Engine_RPM.value >= self.TCLock(self.inputs.Current_Gear.value))) \
            and not (self.shiftTimer > 0.0):
        self.outputs.Torque_Converter_Lock.value = self.TCLockTorque
    elif ((throttleInput >= self.QuickThrottle and self.inputs.Engine_RPM.value < self.TCUnlockQuick(self.inputs.Current_Gear.value)) \
            or (throttleInput <  self.QuickThrottle and self.inputs.Engine_RPM.value < self.TCUnlock(self.inputs.Current_Gear.value))) \
            and not (self.shiftTimer > 0.0):
        self.outputs.Torque_Converter_Lock.value = 0.0
		
    # Gear range
    self.outputs.Final_Gear_Ratio.value = self.LowGearRange if self.inputs.Low_Range_Active.value else self.HighGearRange
    

    
# Create functions create fields in the Editor
        
def CreateInput(extension, name, type):
    input = extension.getInput(name)
    if input is None:
        input = extension.addInput(name, type)

def CreateOutput(extension, name, o_type, default_value=None):
    """Create output field with optional default value, reset on every simulation run."""
    if extension.getOutput(name) is None:
        extension.addOutput(name, o_type)
    if default_value is not None:
        extension.getOutput(name).value = default_value
    return extension.getOutput(name)

def CreateParameter(extension, name, p_type, default_value=None):
    """Create parameter field with optional default value set only when the field is created."""
    if extension.getParameter(name) is None:
        field = extension.addParameter(name, p_type)
        if default_value is not None:
            field.value = default_value
    return extension.getParameter(name)
