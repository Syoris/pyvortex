#--------------------------------------------------
# Created on 1 November 2019
# Author: Shahram Shokouhfar
# Description: Camera Controller
#--------------------------------------------------
from VxSim import *
from math import *
import melibrary.me_tools as me
#--------------------------------------------------
def on_add_to_universe(self, universe):
    # Inputs
    self.i_chassis_transform = me.create_input(self, "Chassis Transform", Types.Type_VxMatrix44)

    # Outputs
    self.o_camera_transform = me.create_output(self, "Camera Transform", Types.Type_VxMatrix44)

    # Parameters
    self.p_filter_enabled = me.create_parameter(self, "Filter Enabled", VxSim.Types.Type_Bool)
    self.p_z_time_constant = me.create_parameter(self, "Z Time Constant", VxSim.Types.Type_VxReal)
    self.p_yaw_time_constant = me.create_parameter(self, "Yaw Time Constant", VxSim.Types.Type_VxReal)

    # Self
    self.filtered_z = 0.0
    self.filtered_yaw = 0.0
    self.prev_yaw = 0.0
    self.wraps = 0

    # time_constant, time_step, initial_value
    self.time_step = self.getApplicationContext().getSimulationTimeStep()
    self.z_lowpass = me.LowpassFilter(self.p_z_time_constant.value, self.time_step, 0.0)
    self.yaw_lowpass = me.LowpassFilter(self.p_yaw_time_constant.value, self.time_step, 0.0)

    set_transform(self, False)
#--------------------------------------------------
def on_remove_from_universe(self, universe):
    pass
#--------------------------------------------------
def pre_step(self):
    self.z_lowpass.time_constant = self.p_z_time_constant.value
    self.yaw_lowpass.time_constant = self.p_yaw_time_constant.value
#--------------------------------------------------
def post_step(self):
    set_transform(self, self.p_filter_enabled.value)
#--------------------------------------------------
def on_state_restore(self, data):
    pass
#--------------------------------------------------
def on_state_save(self, data):
    pass
#--------------------------------------------------
def set_transform(self, filter = False):
    pos = getTranslation(self.i_chassis_transform.value)
    signal_z = pos.z

    rot = getRotation(self.i_chassis_transform.value)
    signal_yaw = rot.z

    # Add count for when rotation wraps around
    if signal_yaw - self.prev_yaw < -pi:
        self.wraps += 1
    elif signal_yaw - self.prev_yaw > pi:
        self.wraps -= 1

    self.prev_yaw = signal_yaw

    signal_yaw += self.wraps * 2.0 * pi

    if filter:
        self.filtered_z = self.z_lowpass.filter(signal_z)
        self.filtered_yaw = self.yaw_lowpass.filter(signal_yaw)
    else:
        self.filtered_z = signal_z
        self.filtered_yaw = signal_yaw

    follow_trans = VxSim.createTranslation(pos.x, pos.y, self.filtered_z)
    follow_trans = rotateTo(follow_trans, VxVector3(0, 0, self.filtered_yaw))
    
    self.o_camera_transform.value = follow_trans
#--------------------------------------------------
#def paused_update(self):
    #set_transform(self, False)
#--------------------------------------------------
