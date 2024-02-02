#--------------------------------------------------
# Created on 16 October 2019
# Author: Shahram Shokouhfar
# Description: This script manages how the weight of the passengers affect the vehicle performance
#--------------------------------------------------
import VxSim
import melibrary.me_tools as me
import melibrary.buttons as buttons
#--------------------------------------------------
def on_add_to_universe(self, universe):
    # Inputs
    self.i_passenger_fr = me.create_input(self, "Passenger FR", VxSim.Types.Type_Bool)
    self.i_passenger_rl = me.create_input(self, "Passenger RL", VxSim.Types.Type_Bool)
    self.i_passenger_rr = me.create_input(self, "Passenger RR", VxSim.Types.Type_Bool)

    # Outputs
    self.o_driver_mass = me.create_output(self, "Driver Mass", VxSim.Types.Type_VxReal)
    self.o_passenger_fr_mass = me.create_output(self, "Passenger FR Mass", VxSim.Types.Type_VxReal)
    self.o_passenger_rl_mass = me.create_output(self, "Passenger RL Mass", VxSim.Types.Type_VxReal)
    self.o_passenger_rr_mass = me.create_output(self, "Passenger RR Mass", VxSim.Types.Type_VxReal)
    self.o_door_open_fr = me.create_output(self, "Door Open FR", VxSim.Types.Type_Bool)
    self.o_door_open_rl = me.create_output(self, "Door Open RL", VxSim.Types.Type_Bool)
    self.o_door_open_rr = me.create_output(self, "Door Open RR", VxSim.Types.Type_Bool)
    self.o_door_close_fr = me.create_output(self, "Door Close FR", VxSim.Types.Type_Bool)
    self.o_door_close_rl = me.create_output(self, "Door Close RL", VxSim.Types.Type_Bool)
    self.o_door_close_rr = me.create_output(self, "Door Close RR", VxSim.Types.Type_Bool)
    
    # Parameters
    self.p_passenger_average_mass = me.create_parameter(self, "Passenger Average Mass", VxSim.Types.Type_VxReal)
    self.p_passenger_huge_mass = me.create_parameter(self, "Passenger Huge Mass", VxSim.Types.Type_VxReal)
    self.p_frames_huge_average = me.create_parameter(self, "Frames from Huge to Average", VxSim.Types.Type_Int)
    self.p_frames_door_open = me.create_parameter(self, "Frames Door Open Takes", VxSim.Types.Type_Int)
    self.p_frames_door_close = me.create_parameter(self, "Frames Door Close Takes", VxSim.Types.Type_Int)

    self.counter_fr = 0
    self.counter_rl = 0
    self.counter_rr = 0
    self.counter_max = 120
    
    self.mass_change_fr = False
    self.mass_change_rl = False
    self.mass_change_rr = False
    
    self.mass_fr = 1
    self.mass_rl = 1
    self.mass_rr = 1
    self.mass_delta = 1

    self.passenger_fr_button = buttons.RisingEdgeButton(initial_state = False)
    self.passenger_rl_button = buttons.RisingEdgeButton(initial_state = False)
    self.passenger_rr_button = buttons.RisingEdgeButton(initial_state = False)

    self.o_door_open_fr.value = False
    self.o_door_open_rl.value = False
    self.o_door_open_rr.value = False
    
    self.o_door_close_fr.value = False
    self.o_door_close_rl.value = False
    self.o_door_close_rr.value = False
#--------------------------------------------------
def on_remove_from_universe(self, universe):
    pass
#--------------------------------------------------
def pre_step(self):
    self.mass_huge = self.p_passenger_huge_mass.value

    self.counter_point_0 = 0
    self.counter_point_1 = self.counter_point_0 + self.p_frames_door_open.value
    self.counter_point_2 = self.counter_point_1 + self.p_frames_huge_average.value
    self.counter_point_3 = self.counter_point_2 + self.p_frames_door_close.value
    
    self.mass_delta = (self.mass_huge - self.p_passenger_average_mass.value) / self.p_frames_huge_average.value
    
    # Driver Mass
    self.o_driver_mass.value = self.p_passenger_average_mass.value

    if self.passenger_fr_button.determine_state(self.i_passenger_fr.value):
        self.counter_fr = self.counter_point_0
        self.o_door_open_fr.value = True
    if self.passenger_rl_button.determine_state(self.i_passenger_rl.value):
        self.counter_rl = self.counter_point_0
        self.o_door_open_rl.value = True
    if self.passenger_rr_button.determine_state(self.i_passenger_rr.value):
        self.counter_rr = self.counter_point_0
        self.o_door_open_rr.value = True

    if self.mass_change_fr == True:
        self.mass_fr -= self.mass_delta
    if self.mass_change_rl == True:
        self.mass_rl -= self.mass_delta
    if self.mass_change_rr == True:
        self.mass_rr -= self.mass_delta

    if self.counter_fr == self.counter_point_1:
        self.mass_change_fr = True
        self.mass_fr = self.mass_huge
    if self.counter_rl == self.counter_point_1:
        self.mass_change_rl = True
        self.mass_rl = self.mass_huge
    if self.counter_rr == self.counter_point_1:
        self.mass_change_rr = True
        self.mass_rr = self.mass_huge
        
    if self.counter_fr >= self.counter_point_2:
        self.mass_change_fr = False
    if self.counter_rl >= self.counter_point_2:
        self.mass_change_rl = False
    if self.counter_rr >= self.counter_point_2:
        self.mass_change_rr = False

    if self.counter_fr == self.counter_point_3:
        self.o_door_close_fr.value = True
    if self.counter_rl == self.counter_point_3:
        self.o_door_close_rl.value = True
    if self.counter_rr == self.counter_point_3:
        self.o_door_close_rr.value = True

    if not self.i_passenger_fr.value:
        self.mass_fr = 1
    if not self.i_passenger_rl.value:
        self.mass_rl = 1
    if not self.i_passenger_rr.value:
        self.mass_rr = 1
        
    if self.o_door_open_fr.value:
        self.counter_fr += 1
    if self.o_door_open_rl.value:
        self.counter_rl += 1
    if self.o_door_open_rr.value:
        self.counter_rr += 1

    self.o_passenger_fr_mass.value = self.mass_fr
    self.o_passenger_rl_mass.value = self.mass_rl
    self.o_passenger_rr_mass.value = self.mass_rr
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

