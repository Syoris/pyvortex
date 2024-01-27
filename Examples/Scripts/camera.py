from VxSim import *
import csv
import math

def on_add_to_universe(self, universe):

     # Create fields
    create_input(self, 'World Transform', Types.Type_VxMatrix44)
    create_output(self, 'Local Transform', Types.Type_VxMatrix44)
	

def on_remove_from_universe(self, universe):
    """ Called when the script is removed from the universe.
    Use this method to define specific dynamics actions that must be taken at shutdown."""
    transform=VxSim.createTranslation(-0., -5., 2.)*VxSim.createRotation(90.*math.pi/180.,0.,0.)
    self.outputs.Local_Transform.value=transform
    pass

def pre_step(self):
    """ Called before the collision detection and before the dynamic solver.
    Use this method to get inputs or set values to dynamics objects.""" 
    rot=VxSim.getRotation(self.inputs.World_Transform.value)
    #print self.inputs.World_Transform.value
    transform=VxSim.createTranslation(-0., -5., 2.)*VxSim.createRotation(90.*math.pi/180.,0.,rot[1])

	
    self.outputs.Local_Transform.value=transform

    pass

def post_step(self):
    """ Called after the collision detection and after the dynamic solver.
    Use this method to set outputs or get values from dynamics objects.""" 
    pass
		
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

def get_extension_from_object(object, extensionName):
    extensions = object.getExtensions()
    for extension in extensions:
        if extension.getName() == extensionName:
            return extension
