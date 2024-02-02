#--------------------------------------------------
# Created on 2 October 2019
# Author: Shahram Shokouhfar
# Description: Signal Interpreter Script (to provide signals for the Vehicle Control Interface)
#--------------------------------------------------
import VxSim
import melibrary.me_tools as me
import melibrary.buttons as buttons
import math
#--------------------------------------------------
def on_add_to_universe(self, universe):
    # Inputs (Gamepad)
    self.i_steering = me.create_input(self, "Steering [-1 to 1]", VxSim.Types.Type_VxReal)
    
    # Inputs 
    self.i_throttle = me.create_input(self, "Throttle [0 to 1]", VxSim.Types.Type_VxReal)
    self.i_brake = me.create_input(self, "Brake [0 to 1]", VxSim.Types.Type_VxReal)
    
    # Inputs 
    self.i_steering_wheel_angle = me.create_input(self, "Steering Wheel Angle [0 to 6.28]", VxSim.Types.Type_VxReal)
    self.i_twheel_steering_angle = me.create_input(self, "TWheel Steering Angle [-1 to 1]", VxSim.Types.Type_VxReal)
    self.i_device_initialized = me.create_input(self, "Device Initialized", VxSim.Types.Type_Bool)
    self.i_gear_forward = me.create_input(self, "Gear Forward", VxSim.Types.Type_Bool)
    self.i_gear_neutral = me.create_input(self, "Gear Neutral", VxSim.Types.Type_Bool)
    self.i_gear_reverse = me.create_input(self, "Gear Reverse", VxSim.Types.Type_Bool)
    self.i_turn_signal_left = me.create_input(self, "Turn Signal Left", VxSim.Types.Type_Bool)
    self.i_turn_signal_right = me.create_input(self, "Turn Signal Right", VxSim.Types.Type_Bool)
    self.i_horn = me.create_input(self, "Horn", VxSim.Types.Type_Bool)
    self.i_twheel_error_code = me.create_input(self, "TWheel Error Code", VxSim.Types.Type_Int)

    # Outputs
    self.o_gear = me.create_output(self, "Gear [-1 to 6]", VxSim.Types.Type_Int)
    self.o_throttle = me.create_output(self, "Throttle [0 to 1]", VxSim.Types.Type_VxReal)
    self.o_brake = me.create_output(self, "Brake [0 to 1]", VxSim.Types.Type_VxReal)
    self.o_steering = me.create_output(self, "Steering [-1 to 1]", VxSim.Types.Type_VxReal)
    self.o_turn_signal_left = me.create_output(self, "Turn Signal Left", VxSim.Types.Type_Bool)
    self.o_turn_signal_right = me.create_output(self, "Turn Signal Right", VxSim.Types.Type_Bool)
    self.o_horn = me.create_output(self, "Horn", VxSim.Types.Type_Bool)
    self.o_device_initialized = me.create_output(self, "Device Initialized", VxSim.Types.Type_Bool)
    self.o_steering_wheel_angle_deg = me.create_output(self, "Steering Wheel Angle (in Deg)", VxSim.Types.Type_VxReal)
    
    # Parameters
    self.p_wheel_angle_canbus_turns = me.create_parameter(self, "Steering Wheel Turns To Reach Max", VxSim.Types.Type_VxReal)
    
    # Managing Gear [-1 to 6] [0 means neutral]
    self.min_gear = -1
    self.max_gear = 6
    self.gear_forward_button = buttons.RisingEdgeButton(initial_state = False)
    self.gear_reverse_button = buttons.RisingEdgeButton(initial_state = False)
    self.gear_neutral_button = buttons.RisingEdgeButton(initial_state = False)
    
    # Managing Wheel Angle (CANBUS)
    self.wheel_angle_canbus_result = 0
    self.wheel_angle_canbus_prev = 0
    self.wheel_angle_canbus_jump_limit = math.pi
    self.wheel_angle_canbus_upper_limit = 2.0 * math.pi
    self.wheel_angle_canbus_reference = 0
    self.wheel_angle_canbus_difference = 0
    self.wheel_angle_canbus_infinity = 0
    self.wheel_angle_canbus_shifted = 0
    self.is_first_time = True
    
    self.time_step = self.getApplicationContext().getSimulationTimeStep()
    self.gamepad_steering_lowpass = me.LowpassFilter(1.2, self.time_step, 0.0)

#--------------------------------------------------
def on_remove_from_universe(self, universe):
    pass
#--------------------------------------------------
def pre_step(self):
    # For any device
    
    # Brake
    if self.i_brake.value >= 0:
        self.o_brake.value = (self.i_brake.value) ** 4.0

    # Throttle
    if self.i_throttle.value >= 0:
        self.o_throttle.value = self.i_throttle.value
    
    # Managing Gear
    if self.i_device_initialized.value : # CANBUS Case
        if self.i_gear_neutral.value:
            self.o_gear.value = 0
        elif self.i_gear_reverse.value:
            self.o_gear.value = self.min_gear
        elif self.i_gear_forward.value:
            self.o_gear.value = self.max_gear
    else: # Gamepad Case
        if self.gear_neutral_button.determine_state(self.i_gear_neutral.value):
            self.o_gear.value = 0
        elif self.gear_reverse_button.determine_state(self.i_gear_reverse.value):
            self.o_gear.value = self.min_gear
        elif self.gear_forward_button.determine_state(self.i_gear_forward.value):
            self.o_gear.value = self.max_gear

    # Managing Steering Wheel
    if self.i_twheel_error_code.value == 0:
        self.o_steering.value = self.i_twheel_steering_angle.value * (-1.0)
    elif self.i_device_initialized.value: # CANBUS Case
        if self.is_first_time:
            self.is_first_time = False
            self.wheel_angle_canbus_reference = self.i_steering_wheel_angle.value
            self.wheel_angle_canbus_infinity = self.wheel_angle_canbus_reference
            self.wheel_angle_canbus_prev = self.wheel_angle_canbus_infinity
        else:
            self.wheel_angle_canbus_difference = self.i_steering_wheel_angle.value - self.wheel_angle_canbus_prev
            self.wheel_angle_canbus_prev = self.i_steering_wheel_angle.value
            if self.wheel_angle_canbus_difference < -self.wheel_angle_canbus_jump_limit:
                self.wheel_angle_canbus_difference = self.wheel_angle_canbus_difference + self.wheel_angle_canbus_upper_limit
            if self.wheel_angle_canbus_difference > self.wheel_angle_canbus_jump_limit:
                self.wheel_angle_canbus_difference = self.wheel_angle_canbus_difference - self.wheel_angle_canbus_upper_limit
            self.wheel_angle_canbus_infinity += self.wheel_angle_canbus_difference
            self.wheel_angle_canbus_shifted = self.wheel_angle_canbus_infinity - self.wheel_angle_canbus_reference
            self.wheel_angle_canbus_result = -1.0 + 1.0 / (2.0 * math.pi * self.p_wheel_angle_canbus_turns.value) * (self.wheel_angle_canbus_shifted + 2.0 * math.pi * self.p_wheel_angle_canbus_turns.value)
        # Clamp result in [-1 to 1]
        if self.wheel_angle_canbus_result > 1:
            self.wheel_angle_canbus_result = 1
        if self.wheel_angle_canbus_result < -1:
            self.wheel_angle_canbus_result = -1
        self.o_steering.value = -self.wheel_angle_canbus_result
    else: # Gamepad Case
        self.o_steering.value = self.gamepad_steering_lowpass.filter(self.i_steering.value)
        
        # On Gamepad (only): Negative throttle is used for analog brake
        if self.i_throttle.value < -0.01:
            self.o_brake.value = (abs(self.i_throttle.value)) ** 4.0

    # Managing Turn Signal
    self.o_turn_signal_left.value = self.i_turn_signal_left.value
    self.o_turn_signal_right.value = self.i_turn_signal_right.value
    
    # Managing Horn
    self.o_horn.value = self.i_horn.value
    
    # For animating the steering wheel in Unreal
    self.o_steering_wheel_angle_deg.value = self.o_steering.value * 360.0 * self.p_wheel_angle_canbus_turns.value
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

