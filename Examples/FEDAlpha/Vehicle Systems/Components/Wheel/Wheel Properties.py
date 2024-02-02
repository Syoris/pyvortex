# Controls the gear ratio to behave as an automatic transmission. Gear ratios are specified, shift up 
# and down is done based on current RPM

from tools import *
import math

def on_add_to_universe(self, universe):

    # ICD inputs
    create_input(self, 'Radius', Types.Type_VxReal, 0.5)
    create_input(self, 'Width', Types.Type_VxReal, 0.2)
    create_input(self, 'Mass', Types.Type_VxReal, 1.0)
    create_input(self, 'Override Inertia', Types.Type_Bool, False)
    create_input(self, 'Axis Inertia', Types.Type_VxReal, 1.0)
    create_input(self, 'Off Axis Inertia', Types.Type_VxReal, 0.7)

    # Parameters
    create_parameter(self, 'Wheel Part', Types.Type_Part)
    create_parameter(self, 'Wheel Cylinder', Types.Type_CollisionGeometry)


    # Descriptions

    self.inputs.Radius.setDescription("Radius of cylinder representing the wheel")
    self.inputs.Width.setDescription("Width of cylinder representing the wheel")
    self.inputs.Mass.setDescription("Mass of wheel")
    self.inputs.Override_Inertia.setDescription("Normally wheel moment of inertia is calculated automatically from mass and geometry. If Override is true, it is instead manually defined from Axis Inertia and Off Axis Inertia")
    self.inputs.Axis_Inertia.setDescription("The inertia along the axle of the wheel. This inertia is used only if Auto Compute Inertia is false.")
    self.inputs.Off_Axis_Inertia.setDescription("The inertia along the two axes orthogonal to the axle. Those inertias are used only if Auto Compute Inertia is false.")

def paused_update(self):
    set_mass(self)

def pre_step(self):
    set_mass(self)

def set_mass(self):

    # - Collision Geometry ---------------------------------

    self.parameters.Wheel_Cylinder.value.parameterRadius.value = self.inputs.Radius.value
    self.parameters.Wheel_Cylinder.value.parameterHeight.value = self.inputs.Width.value

    # - Mass Properties ---------------------------------

    properties = self.parameters.Wheel_Part.value.parameterMassPropertiesContainer
    properties.mass.value = max(self.inputs.Mass.value, 0.000001)

    if self.inputs.Override_Inertia.value:
        axis_moi = max(self.inputs.Axis_Inertia.value, 0.000001)
        of_axis_moi = max(self.inputs.Off_Axis_Inertia.value, 0.000001)
    else:
        axis_moi = 0.5 * self.inputs.Mass.value * self.inputs.Radius.value**2
        of_axis_moi = 1.0/12.0 * self.inputs.Mass.value * (3 * self.inputs.Radius.value**2 + self.inputs.Width.value**2)

    properties.inertiaTensor.value = Matrix44(of_axis_moi, 0, 0, 0, 
                                              0, axis_moi, 0, 0, 
                                              0, 0, of_axis_moi, 0, 
                                              0, 0, 0, 0)

