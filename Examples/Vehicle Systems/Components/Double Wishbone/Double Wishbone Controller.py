# Calculates values from the suspension

from tools import *

def on_add_to_universe(self, universe):

    # ICD inputs
    self.Strut_Reference_Point = create_input(self, 'Strut Reference Point', Types.Type_VxReal)

    # Internal inputs

    # Parameters
    self.Strut_Initial_Length = create_parameter(self, 'Strut Initial Length', Types.Type_VxReal)

    # ICD outputs

    # Internal outputs
    self.Strut_Natural_Length = create_output(self, 'Strut Natural Length', Types.Type_VxReal)


    # Descriptions
    self.Strut_Reference_Point.setDescription("Starting offset of the strut. Positive for longer")
    self.Strut_Initial_Length.setDescription("Initial length of strut from geometry")
    self.Strut_Natural_Length.setDescription("Natural length of strut spring constraint")


    self.initial_length = self.Strut_Initial_Length.value

def pre_step(self):

    self.Strut_Natural_Length.value = self.initial_length + self.Strut_Reference_Point.value
