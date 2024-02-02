# Controls the gear ratio to behave as an automatic transmission. Gear ratios are specified, shift up 
# and down is done based on current RPM

from tools import *
import math
import csv

def on_add_to_universe(self, universe):

    # ICD inputs
    self.Gear_Selection = create_input(self, 'Gear Selection', Types.Type_Int)
    self.Min_Gear_Selection = create_input(self, 'Min Gear Selection', Types.Type_Int)
    self.Park = create_input(self, 'Park', Types.Type_Bool)
    self.Transition_Time = create_input(self, 'Transition Time', Types.Type_VxReal, 0.5)
    self.Shift_Again_Delay = create_input(self, 'Shift Again Delay', Types.Type_VxReal, 1.0)
    self.Low_Shift_Throttle = create_input(self, 'Low Shift Throttle', Types.Type_VxReal, 0.5)
    self.High_Shift_Throttle = create_input(self, 'High Shift Throttle', Types.Type_VxReal, 0.9)
    self.Low_Shift_Down = create_input(self, 'Low Shift Down', Types.Type_VxReal, 0.3)
    self.Low_Shift_Up = create_input(self, 'Low Shift Up', Types.Type_VxReal, 0.5)
    self.High_Shift_Down = create_input(self, 'High Shift Down', Types.Type_VxReal, 0.5)
    self.High_Shift_Up = create_input(self, 'High Shift Up', Types.Type_VxReal, 0.9)
    self.Shift_Scale = create_input(self, 'Shift Scale', Types.Type_VxReal, 3000)
    self.Shaft_Friction = create_input(self, 'Shaft Friction', Types.Type_VxReal)
    self.Efficiency = create_input(self, 'Efficiency', Types.Type_VxReal, 1.0)
    self.Shift_Efficiency = create_input(self, 'Shift Efficiency', Types.Type_VxReal, 0.5)

    # Internal inputs
    self.Input_Shaft_Speed = create_input(self, 'Input Shaft Speed', Types.Type_VxReal)
    self.Throttle = create_input(self, 'Throttle', Types.Type_VxReal)
    self.Gear_Ratio_Torque = create_input(self, 'Gear Ratio Torque', Types.Type_VxReal)
    self.Output_Shaft_Speed = create_input(self, "Output Shaft Speed", Types.Type_VxReal)

    # Parameters
    self.Gear_Ratio_Table = create_parameter(self, "Gear Ratio Table", Types.Type_VxFilename)
    self.Gear_Shift_Schedule = create_parameter(self, "Gear Shift Schedule", Types.Type_VxFilename)

    # ICD outputs
    self.Current_Gear = create_output(self, 'Current Gear', Types.Type_Int)
    self.Gear_Ratio = create_output(self, 'Gear Ratio', Types.Type_VxReal)
    self.Shift_Transition = create_output(self, 'Shift Transition', Types.Type_Bool)
    self.Shift_Up_RPM = create_output(self, 'Shift Up RPM', Types.Type_VxReal)
    self.Shift_Down_RPM = create_output(self, 'Shift Down RPM', Types.Type_VxReal)
    self.Shaft_Speed = create_output(self, "Shaft Speed", Types.Type_VxReal)
    self.Shaft_Torque = create_output(self, "Shaft Torque", Types.Type_VxReal)
    self.Shaft_Power = create_output(self, "Shaft Power", Types.Type_VxReal)

    # Internal outputs
    self.Gear_Constraint_Enable = create_output(self, 'Gear Constraint Enable', Types.Type_Bool)
    self.Hinge_Mode = create_output(self, 'Hinge Mode', Types.Type_Int)
    self.Hinge_Friction = create_output(self, 'Hinge Friction', Types.Type_VxReal)

    # Descriptions
    self.Gear_Selection.setDescription("Selected gear, positive for forward, negative for reverse, zero for neutral")
    self.Min_Gear_Selection.setDescription("If a transmission is prevented from shifting into the lowest gears, this parameter can be set to the number of the lowest allowable gear. Set 0 for full range, negative for reverse.")
    self.Park.setDescription("True to enable parking mode, locking transmission shaft")
    self.Transition_Time.setDescription("Transition time during shift between previous gear and next gear")
    self.Shift_Again_Delay.setDescription("After a gear change has occurred, automatic shifting will be prevented until this amount of time has passed")
    self.Low_Shift_Throttle.setDescription("When current Throttle is at or below this value, Low Shifting values will be used. Between Low and High Shift Throttle, value will be linearly interpolated")
    self.High_Shift_Throttle.setDescription("When current Throttle is at or above this value, Low Shifting values will be used. Between Low and High Shift Throttle, value will be linearly interpolated")
    self.Low_Shift_Up.setDescription("Point to shift up at low shifting throttle position. Shift will happen when input shaft RPM > Shift Up * Shift Scale")
    self.Low_Shift_Down.setDescription("Point to shift down at low shifting throttle position. Shift will happen when input shaft RPM < Shift Down * Shift Scale")
    self.High_Shift_Up.setDescription("Point to shift up at high shifting throttle position. Shift will happen when input shaft RPM > Shift Up * Shift Scale")
    self.High_Shift_Down.setDescription("Point to shift down at high shifting throttle position. Shift will happen when input shaft RPM < Shift Down * Shift Scale")
    self.Shift_Scale.setDescription("Scale that multiplies the shift points. If this is 1, shift points correspond to RPM of engine. If this is set to the max RPM of th engine, shift points correspond to fraction of max RPM.")
    self.Shaft_Friction.setDescription("Add friction on the output shaft of the transmission")
    self.Efficiency.setDescription("Efficiency of coupling. Friction is applied to output shaft proportional to the power transmitted through the transmission")
    self.Shift_Efficiency.setDescription("Efficiency is often lower while shifting gears, so during Transition Time, Shift Efficiency determines friction on output shaft")

    self.Input_Shaft_Speed.setDescription("Speed of shaft feeding into transmission")
    self.Throttle.setDescription("Current throttle position")
    self.Gear_Ratio_Torque.setDescription("Torque of gear ratio constraint")
    self.Output_Shaft_Speed.setDescription("Speed of the output shaft from the hinge of this component")

    self.Gear_Ratio_Table.setDescription(".csv file containing gear ratios of the transmission. Starting with negative values for reverse gears, then zero for neutral, and positive values for forward gears")
    self.Gear_Shift_Schedule.setDescription(".csv file containing a table of shifting points for each gear. If left blank, Low and High shift RPM parameters will be used instead")

    self.Current_Gear.setDescription("Index number of current gear, positive for forward, negative for reverse, zero for neutral")
    self.Gear_Ratio.setDescription("Ratio of current gear")
    self.Shift_Transition.setDescription("True during shift transition")
    self.Shift_Up_RPM.setDescription("Shift Up RPM based on current throttle position")
    self.Shift_Down_RPM.setDescription("Shift Down RPM based on current throttle position")
    self.Shaft_Speed.setDescription("Speed of output shaft in rad/s")
    self.Shaft_Torque.setDescription("Net torque on output shaft in N.m")
    self.Shaft_Power.setDescription("Net power on output shaft in W")

    self.Gear_Constraint_Enable.setDescription("Enable gear ratio constraint. Disabled when in Neutral")
    self.Hinge_Mode.setDescription("Mode of hinge constraint")
    self.Hinge_Friction.setDescription("Friction of hinge constraint")

    # Load gear ratios and put in a dictionary
    try:
        with open(self.Gear_Ratio_Table.value, 'rb') as f:
            reader = csv.reader(f)
            your_list = list(reader)
            
        num_list = [[float(x) for x in rec] for rec in your_list]
        index = map(int, num_list[0])
        gear = num_list[1]
        self.gear_ratios = dict(zip(index, gear))
        self.max_gear = max(index)
        self.min_gear = min(index)
    except:
        self.gear_ratios = None
        self.max_gear = 0
        self.min_gear = 0
        raise ValueError("Unable to load Gear Ratio Table")

    # Load shift schedule. If empty, use input fields instead
    if self.Gear_Shift_Schedule.value:
        # TODO
        self.shift_schedule = None
    else:
        self.shift_schedule = None


    # Current gear
    self.gear = 1
    # Shift-again timer that counts down during shift - Must be larger than transition time
    self.shift_delay = Timer(max(self.Shift_Again_Delay.value, self.Transition_Time.value),
                            self.getApplicationContext().getSimulationTimeStep())
    # Shift transition timer that counts down as gear transition to new ratio
    self.transition = Timer(self.Transition_Time.value, self.getApplicationContext().getSimulationTimeStep())
    # Amount that gear ratio can be changed each time step during transition - updated when shifted
    self.ratio_rate = 0.0


def pre_step(self):

    # If the shift table is blank, define shift RPM based on inputs
    if not self.Gear_Shift_Schedule.value:
        try:
            shift_throttle = [0.0, self.Low_Shift_Throttle.value, self.High_Shift_Throttle.value, 1.0]

            scale = self.Shift_Scale.value
            self.up_shift = LinearInterpolation(shift_throttle, 
                [self.Low_Shift_Up.value * scale, self.Low_Shift_Up.value * scale, 
                 self.High_Shift_Up.value * scale, self.High_Shift_Up.value * scale])
            self.down_shift = LinearInterpolation(shift_throttle,
                [self.Low_Shift_Down.value * scale, self.Low_Shift_Down.value * scale, 
                self.High_Shift_Down.value * scale, self.High_Shift_Down.value * scale])
        except:
            self.up_shift = None
            self.down_shift = None
            raise ValueError("Invalid shift throttle. Must be 0.0 < Low Shift Throttle < High Shift Throttle < 1.0")


    if (self.gear_ratios is None) or (self.up_shift is None):
        return

    # - Shifting Behaviour ---------------------------------

    rpm = self.Input_Shaft_Speed.value *30/math.pi
    gear_selection = clamp(self.Gear_Selection.value, self.min_gear, self.max_gear)
    throttle = self.Throttle.value

    # Minimum gear defined by inputs
    if gear_selection > 0: # for forward, min gear is between 1 and selected gear
        min_gear_selection = clamp(self.Min_Gear_Selection.value, 1, gear_selection)
    elif gear_selection < 0: # for reverse, min gear is between selected gear and -1, but flip to positive for shifting logic
        min_gear_selection = abs(clamp(self.Min_Gear_Selection.value, gear_selection, -1))
    else: # neutral
        min_gear_selection = 0


    if gear_selection == 0: # Neutral
        self.gear = 0
    else:
        # Check if switched between forward and reverse, and reset to min
        # Otherwise if current gear is eg. 4, shifting to reverse will start in -4
        if (self.gear * gear_selection) < 0:
            self.gear = min_gear_selection

        # If shifting out of neutral, shift again delay to prevent sudden shift up if RPM is high
        if self.gear == 0:
            self.shift_delay.restart()

        # Shift up or down, based on current RPM
        # All based on positive gear numbers, since logic is equivalent for foward and reverse
        self.gear = abs(self.gear)

        self.Shift_Up_RPM.value = self.up_shift(throttle)
        self.Shift_Down_RPM.value = self.down_shift(throttle)

        if not self.shift_delay():
            if rpm >= self.up_shift(throttle) and self.gear < abs(gear_selection):
                self.gear += 1
                self.shift_delay.restart()
                self.transition.restart()
                # Calculate rate at which ratio can be changed each step during transition time
                self.ratio_rate = (abs(self.gear_ratios[self.gear - 1] - self.gear_ratios[self.gear])
                                    * self.getApplicationContext().getSimulationTimeStep() / self.Transition_Time.value)
            elif rpm <= self.down_shift(throttle) and self.gear > abs(min_gear_selection):
                self.gear -= 1
                self.shift_delay.restart()
                self.transition.restart()
                # Calculate rate at which ratio can be changed each step during transition time
                self.ratio_rate = (abs(self.gear_ratios[self.gear - 1] - self.gear_ratios[self.gear])
                                    * self.getApplicationContext().getSimulationTimeStep() / self.Transition_Time.value)

        # Recheck the min and max gear, in case they were changed by user
        self.gear = clamp(self.gear, min_gear_selection, abs(gear_selection))
        # Apply sign to match selected direction
        self.gear = int(math.copysign(self.gear, gear_selection))

    # Update timers
    self.shift_delay.update()
    self.transition.update()


    # - Gear Ratios ---------------------------------

    self.Current_Gear.value = self.gear
    if self.transition():
        # Calculate ratio during transition
        # 
        new_ratio = self.gear_ratios[self.gear]
        self.Gear_Ratio.value = clamp(new_ratio, self.Gear_Ratio.value - self.ratio_rate, self.Gear_Ratio.value + self.ratio_rate)
    else:
        self.Gear_Ratio.value = self.gear_ratios[self.gear]

    self.Gear_Constraint_Enable.value = abs(self.gear_ratios[self.gear]) > 0.0001
    self.Shift_Transition.value = self.transition()


    # - Parking Lock ---------------------------------

    if self.Park.value:
        self.Hinge_Mode.value = VxSim.Constraint.kControlLocked
    else:
        self.Hinge_Mode.value = VxSim.Constraint.kControlFree


    # - Friction and Efficiency ---------------------------------

    # Gear ratio constraint reports torque on Part 1 which is input torque
    # Constraint keeps reporting last value when constraint is disabled, so set to 0 in this case
    # Negative due to convention of constraint
    input_torque = - self.Gear_Ratio_Torque.value if self.Gear_Constraint_Enable.value else 0.0
    # Output torque is multiplied by gear ratio
    output_torque = input_torque * self.Gear_Ratio.value
    # Choose efficiency: use shift efficiency if during shift transition
    efficiency = self.Shift_Efficiency.value if self.transition() else self.Efficiency.value
    efficiency_friction = abs(output_torque) * (1.0 - efficiency)

    self.Hinge_Friction.value = efficiency_friction + self.Shaft_Friction.value

    self.Shaft_Speed.value = self.Output_Shaft_Speed.value
    # Field reports net torque, so subtract friction torque from output torque
    # Since friction could be + or -, must use abs for subtraction, then reapply sign.
    self.Shaft_Torque.value = math.copysign(max(abs(output_torque) - self.Hinge_Friction.value, 0), output_torque)
    self.Shaft_Power.value = self.Shaft_Speed.value * self.Shaft_Torque.value
