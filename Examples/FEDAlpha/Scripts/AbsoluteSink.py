from VxSim import *
from math import *

def on_add_to_universe(self, universe):
    create_input(self, 'FL Transform', Types.Type_VxMatrix44)
    create_input(self, 'FR Transform', Types.Type_VxMatrix44)
    create_input(self, 'RL Transform', Types.Type_VxMatrix44)
    create_input(self, 'RR Transform', Types.Type_VxMatrix44)
	
    create_input(self, 'FL Tire Deflection', Types.Type_VxReal)
    create_input(self, 'FR Tire Deflection', Types.Type_VxReal)
    create_input(self, 'RL Tire Deflection', Types.Type_VxReal)
    create_input(self, 'RR Tire Deflection', Types.Type_VxReal)

    create_input(self, 'Wheel Radius', Types.Type_VxReal)
###################################################################
###################################################################
    create_output(self, 'Wheel Sinkage FL', Types.Type_VxReal)
    create_output(self, 'Wheel Sinkage FR', Types.Type_VxReal)
    create_output(self, 'Wheel Sinkage RL', Types.Type_VxReal)
    create_output(self, 'Wheel Sinkage RR', Types.Type_VxReal)

def pre_step(self):

    self.FL_wheelpos=getTranslation(self.inputs.FL_Transform.value)
    self.FR_wheelpos=getTranslation(self.inputs.FR_Transform.value)
    self.RL_wheelpos=getTranslation(self.inputs.RL_Transform.value)
    self.RR_wheelpos=getTranslation(self.inputs.RR_Transform.value)
   
	
    self.outputs.Wheel_Sinkage_FL.value = self.inputs.Wheel_Radius.value - self.FL_wheelpos[2]
    self.outputs.Wheel_Sinkage_FR.value = self.inputs.Wheel_Radius.value - self.FR_wheelpos[2]
    self.outputs.Wheel_Sinkage_RL.value = self.inputs.Wheel_Radius.value - self.RL_wheelpos[2]
    self.outputs.Wheel_Sinkage_RR.value = self.inputs.Wheel_Radius.value - self.RR_wheelpos[2]
	

# Functions create fields in the Editor
def create_output(extension, name, o_type, default_value=None):
     """Create output field with optional default value, reset on every simulation run."""
     if extension.getOutput(name) is None:
          extension.addOutput(name, o_type)
     if default_value is not None:
          extension.getOutput(name).value = default_value
     return extension.getOutput(name)

def create_parameter(extension, name, p_type, default_value=None):
     """Create parameter field with optional default value set only when the field is created."""
     if extension.getParameter(name) is None:
          field = extension.addParameter(name, p_type)
          if default_value is not None:
                field.value = default_value
     return extension.getParameter(name)

def create_input(extension, name, i_type, default_value=None):
     """Create input field with optional default value set only when the field is created."""
     if extension.getInput(name) is None:
          field = extension.addInput(name, i_type)
          if default_value is not None:
                field.value = default_value
     return extension.getInput(name)