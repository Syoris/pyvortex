#--------------------------------------------------
# Created on 21 October 2019
# Author: Shahram Shokouhfar
# Description: Camera Manager
#--------------------------------------------------
import VxSim
import melibrary.me_tools as me
import melibrary.buttons as buttons
import math
#--------------------------------------------------
def on_add_to_universe(self, universe):
    # Inputs
    self.i_chassis_transform = me.create_input(self, "Chassis Transform", VxSim.Types.Type_VxTransform)

    # Outputs
    self.o_camera_transform = me.create_output(self, "Camera Transform", VxSim.Types.Type_VxTransform)
    
    # Self
    self.counter = 0
    self.frames_behind = 30
    self.transform = range(self.frames_behind)
#--------------------------------------------------
def on_remove_from_universe(self, universe):
    pass
#--------------------------------------------------
def pre_step(self):
    if self.counter < self.frames_behind:
        self.transform[self.counter] = self.i_chassis_transform.value
    else:
        self.o_camera_transform.value = self.transform[0]
        for i in range(1, self.frames_behind):
            self.transform[i - 1] = self.transform[i]
        self.transform[self.frames_behind - 1] = self.i_chassis_transform.value
    self.counter += 1
#--------------------------------------------------
def post_step(self):
    pass
#--------------------------------------------------
def on_state_restore(self, data):
    pass
#--------------------------------------------------
def on_state_save(self, data):
    pass
#--------------------------------------------------

