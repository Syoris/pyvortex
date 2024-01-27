# This script sets the mass, moment of inertia, and center of mass of the specified part

from tools import *
import math

def on_add_to_universe(self, universe):

    # Inputs
    create_input(self, 'Mass', Types.Type_VxReal, 1.0)
    create_input(self, 'Centre of Mass', Types.Type_VxVector3, VxVector3(0.0, 0.0, 0.0))
    create_input(self, 'Inertia', Types.Type_VxVector3, VxVector3(0.1, 0.1, 0.1))

    # Parameters
    create_parameter(self, 'Chassis Part', Types.Type_Part)

    # Descriptions
    self.inputs.Mass.setDescription("Mass of chassis")
    self.inputs.Centre_of_Mass.setDescription("Vector of centre of mass offset")
    self.inputs.Inertia.setDescription("Components of diagonal inertia matrix")

def paused_update(self):
    set_mass(self)

def set_mass(self):

    properties = self.parameters.Chassis_Part.value.parameterMassPropertiesContainer
    properties.mass.value = max(self.inputs.Mass.value, 0.000001)

    properties.centerOfMassOffset.value = self.inputs.Centre_of_Mass.value

    moi_x = max(self.inputs.Inertia.value.x, 0.000001)
    moi_y = max(self.inputs.Inertia.value.y, 0.000001)
    moi_z = max(self.inputs.Inertia.value.z, 0.000001)
    properties.inertiaTensor.value = Matrix44(moi_x, 0, 0, 0, 
                                              0, moi_y, 0, 0, 
                                              0, 0, moi_z, 0, 
                                              0, 0, 0, 0)

