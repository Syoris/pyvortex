#--------------------------------------------------
# Created on 24 October 2019
# Author: Shahram Shokouhfar
# Description: TWheel Feedback
#--------------------------------------------------
import VxSim
import melibrary.me_tools as me
import melibrary.buttons as buttons
import math
#--------------------------------------------------
def on_add_to_universe(self, universe):
    # Inputs
    self.i_engine_vibration_enabled = me.create_input(self, "Engine Vibration Enabled", VxSim.Types.Type_Bool)
    self.i_engine_rpm = me.create_input(self, "Engine RPM", VxSim.Types.Type_VxReal)
    self.i_min_engine_rpm = me.create_input(self, "Min Engine RPM", VxSim.Types.Type_VxReal)
    self.i_max_engine_rpm = me.create_input(self, "Max Engine RPM", VxSim.Types.Type_VxReal)
    self.i_engine_vibration_amplitude_at_min_engine_rpm = me.create_input(self, "Engine Vibration Amplitude at Min Engine RPM", VxSim.Types.Type_VxReal)
    self.i_engine_vibration_amplitude_at_max_engine_rpm = me.create_input(self, "Engine Vibration Amplitude at Max Engine RPM", VxSim.Types.Type_VxReal)
    self.i_engine_rpm = me.create_input(self, "Engine RPM", VxSim.Types.Type_VxReal)
    
    # Outputs
    self.o_engine_vibration_amplitude = me.create_output(self, "Engine Vibration Amplitude", VxSim.Types.Type_VxReal)
#--------------------------------------------------
def on_remove_from_universe(self, universe):
    pass
#--------------------------------------------------
def pre_step(self):
    self.o_engine_vibration_amplitude.value = 0
    if self.i_engine_vibration_enabled.value:
        x = self.i_engine_rpm.value
        x1 = self.i_min_engine_rpm.value
        x2 = self.i_max_engine_rpm.value
        y1 = self.i_engine_vibration_amplitude_at_min_engine_rpm.value
        y2 = self.i_engine_vibration_amplitude_at_max_engine_rpm.value
        if x1 != x2:
            y = y1 + (y2 - y1)/(x2 - x1) * (x - x1)
            self.o_engine_vibration_amplitude.value = y
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

