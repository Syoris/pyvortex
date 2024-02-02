#--------------------------------------------------
# Created on 14 November 2019
# Author: Shahram Shokouhfar
# Description: In this script, the collision of the chassis (with anything) is detected, and if there is any collision, some of the motion platform parameters are decided.
#--------------------------------------------------
import VxSim
import melibrary.me_tools as me
import melibrary.buttons as buttons
import math
#--------------------------------------------------
def on_add_to_universe(self, universe):
    # Inputs
    self.i_chassis_has_intersected = me.create_input(self, "Chassis Has Intersected", VxSim.Types.Type_Bool)

    self.i_normal_rotation_lpf_constant = me.create_input(self, "Normal Rotation LP Filter Constant", VxSim.Types.Type_VxReal)
    self.i_normal_acceleration_lpf_constant = me.create_input(self, "Normal Acceleration LP Filter Constant", VxSim.Types.Type_VxReal)
    
    self.i_modified_rotation_lpf_constant = me.create_input(self, "Modified Rotation LP Filter Constant", VxSim.Types.Type_VxReal)
    self.i_modified_acceleration_lpf_constant = me.create_input(self, "Modified Acceleration LP Filter Constant", VxSim.Types.Type_VxReal)
    
    # Outputs
    self.o_rotation_lpf_constant = me.create_output(self, "Decided Rotation LP Filter Constant", VxSim.Types.Type_VxReal)
    self.o_acceleration_lpf_constant = me.create_output(self, "Decided Acceleration LP Filter Constant", VxSim.Types.Type_VxReal)
#--------------------------------------------------
def pre_step(self):
    pass
#--------------------------------------------------
def post_step(self):
    if self.i_chassis_has_intersected.value:
        self.o_rotation_lpf_constant.value = self.i_modified_rotation_lpf_constant.value
        self.o_acceleration_lpf_constant.value = self.i_modified_acceleration_lpf_constant.value
    else:
        self.o_rotation_lpf_constant.value = self.i_normal_rotation_lpf_constant.value
        self.o_acceleration_lpf_constant.value = self.i_normal_acceleration_lpf_constant.value
#--------------------------------------------------
