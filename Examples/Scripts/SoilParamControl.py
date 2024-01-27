from VxSim import *
import csv
import math

def on_add_to_universe(self, universe):

     # Create fields
    create_input(self, 'kphi', Types.Type_VxReal, default_value=505.80)
    create_input(self, 'kc', Types.Type_VxReal, default_value=6.94)
    create_input(self, 'n', Types.Type_VxReal, default_value=0.705)
    create_input(self, 'phi_ext', Types.Type_VxReal, default_value=31.5)
    create_input(self, 'K_ext', Types.Type_VxReal, default_value=2.5)
    create_input(self, 'c_ext', Types.Type_VxReal, default_value=1.15)
    create_input(self, 'phi_int', Types.Type_VxReal, default_value=31.5)
    create_input(self, 'K_int', Types.Type_VxReal, default_value=2.5)
    create_input(self, 'c_int', Types.Type_VxReal, default_value=1.15)
	
    create_input(self, 'k0', Types.Type_VxReal, default_value=800.0)
    create_input(self, 'Au', Types.Type_VxReal, default_value=503000.0)
	
    create_input(self, 'LugHeight', Types.Type_VxReal, default_value=0.016)
    create_input(self, 'LugCarcassWidth', Types.Type_VxReal, default_value=0.24)
    create_input(self, 'LugCarcassArea', Types.Type_VxReal, default_value=0.58)
	
    create_output(self, 'kphi', Types.Type_VxReal)
    create_output(self, 'kc', Types.Type_VxReal)
    create_output(self, 'n', Types.Type_VxReal)
    create_output(self, 'phi_ext', Types.Type_VxReal)
    create_output(self, 'K_ext', Types.Type_VxReal)
    create_output(self, 'c_ext', Types.Type_VxReal)
    create_output(self, 'phi_int', Types.Type_VxReal)
    create_output(self, 'K_int', Types.Type_VxReal)
    create_output(self, 'c_int', Types.Type_VxReal)
	
    # VHLvehicle_ext=get_extension_from_object(self.inputs.Mechanism.value,'Vehicle Interface')
    # VHLvehicle=VHLvehicle_ext.getExtension()
    # VHLterrain_ext=get_extension_from_object(self.inputs.Mechanism.value,'Terrain Interface')
    # VHLterrain=VHLterrain_ext.getExtension()
	
    # K0=VHLterrain.getParameter('K0')
    # K0.setValue(self.outputs.k0.value)
    # AU=VHLterrain.getParameter('Au')
    # AU.setValue(self.outputs.Au.value)
    
	
def on_remove_from_universe(self, universe):   
    
    pass

def pre_step(self):

	#Set terramechanics parameters
    self.outputs.kphi.value = self.inputs.kphi.value
    self.outputs.kc.value = self.inputs.kc.value
    self.outputs.n.value = self.inputs.n.value
    self.outputs.phi_ext.value = self.inputs.phi_ext.value
    self.outputs.K_ext.value = self.inputs.K_ext.value
    self.outputs.c_ext.value = self.inputs.c_ext.value
    self.outputs.phi_int.value = self.inputs.phi_int.value
    self.outputs.K_int.value = self.inputs.K_int.value
    self.outputs.c_int.value = self.inputs.c_int.value
	
	
    VHLterrain_ext=self.inputs.TerrainVHL.value
	
    K0=VHLterrain_ext.getParameter('K0')
    K0.setValue(self.inputs.k0.value)
    AU=VHLterrain_ext.getParameter('Au')
    AU.setValue(self.inputs.Au.value)
	
    LugHeight=VHLterrain_ext.getParameter('Lug Height')
    LugHeight.setValue(self.inputs.LugHeight.value)
    LugCarcassWidth=VHLterrain_ext.getParameter('Lug Carcass Width Ratio')
    LugCarcassWidth.setValue(self.inputs.LugCarcassWidth.value)
    LugCarcassArea=VHLterrain_ext.getParameter('Lug Carcass Area Ratio')
    LugCarcassArea.setValue(self.inputs.LugCarcassArea.value)
    pass

def post_step(self):

    pass

    """ Write data to output CSV file """
		
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
