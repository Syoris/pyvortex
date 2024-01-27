# This script sets the mass and (spherical) moment of inertia of the specified part

from tools import *

def on_add_to_universe(self, universe):
    create_parameter(self, "Mass", Types.Type_VxReal)
    create_parameter(self, "Moment of Inertia", Types.Type_VxReal)
    create_parameter(self, "Part", Types.Type_Part)

    self.parameters.Mass.setDescription("Mass of output shaft in kg")
    self.parameters.Moment_of_Inertia.setDescription("Moment of inertia of output shaft, assumed spherical in kg.m^2")
    self.parameters.Part.setDescription("Part to apply mass and moment of inertia")

def paused_update(self):
    set_mass(self)

def set_mass(self):
    properties = self.parameters.Part.value.parameterMassPropertiesContainer
    properties.mass.value = max(self.parameters.Mass.value, 0.000001)

    MOI = max(self.parameters.Moment_of_Inertia.value, 0.000001)
    properties.inertiaTensor.value = Matrix44(MOI, 0, 0, 0, 
                                              0, MOI, 0, 0, 
                                              0, 0, MOI, 0, 
                                              0, 0, 0, 0)