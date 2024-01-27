from VxSim import *


def on_add_to_universe(self, universe):

    # Create fields
    create_input(self, 'Material', Types.Type_String)
    create_parameter(self, 'Collision Geometry', Types.Type_CollisionGeometry)
    
    material = VxSim.VxMaterial()
    material.setName(self.inputs.Material.value)
    self.parameters.Collision_Geometry.value.parameterMaterial.value = material

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
