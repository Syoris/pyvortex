from tools import *

def on_add_to_universe(self, universe):

    create_input(self, 'Transmission Shaft Speed', Types.Type_VxReal)
    create_input(self, 'Final Drive Ratio', Types.Type_VxReal)
    create_input(self, 'Wheel Radius', Types.Type_VxReal)

    create_output(self, 'Speed', Types.Type_VxReal)

    self.time_step = self.getApplicationContext().getSimulationTimeStep()
    
def pre_step(self):
    self.outputs.Speed.value = (self.inputs.Transmission_Shaft_Speed.value 
                              / self.inputs.Final_Drive_Ratio.value
                              * self.inputs.Wheel_Radius.value
                              * 3.6)
