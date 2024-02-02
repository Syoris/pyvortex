from tools import *
import math
import csv

def on_add_to_universe(self, universe):

    # ICD inputs
    self.Engine_Running = create_input(self, "Engine Running", Types.Type_Bool)
    self.Throttle = create_input(self, "Throttle", Types.Type_VxReal)
    self.Throttle_Delay = create_input(self, "Throttle Delay", Types.Type_VxReal)
    self.Torque_Scale = create_input(self, "Torque Scale", Types.Type_VxReal)
    self.Torque_Added = create_input(self, "Torque Added", Types.Type_VxReal)
    self.Braking_Torque_Scale = create_input(self, "Braking Torque Scale", Types.Type_VxReal)
    self.Braking_Torque_Added = create_input(self, "Braking Torque Added", Types.Type_VxReal)

    # Internal inputs
    self.Hinge_Velocity = create_input(self, "Hinge Velocity", Types.Type_VxReal)
    self.Hinge_Torque = create_input(self, "Hinge Torque", Types.Type_VxReal)
    self.Shaft_Friction = create_input(self, "Shaft Friction", Types.Type_VxReal)

    # Parameters
    self.Torque_Table = create_parameter(self, "Torque Table", Types.Type_VxFilename)
    self.Idle_RPM = create_parameter(self, "Idle RPM", Types.Type_VxReal)

    # ICD outputs
    self.Max_Torque = create_output(self, "Max Torque", Types.Type_VxReal)
    self.Max_RPM = create_output(self, "Max RPM", Types.Type_VxReal)
    self.Max_Power = create_output(self, "Max Power", Types.Type_VxReal)
    self.Max_HP = create_output(self, "Max HP", Types.Type_VxReal)
    self.RPM_at_Max_Power = create_output(self, "RPM at Max Power", Types.Type_VxReal)
    self.RPM_at_Max_Torque = create_output(self, "RPM at Max Torque", Types.Type_VxReal)
    self.Engine_RPM = create_output(self, "Engine RPM", Types.Type_VxReal)
    self.Engine_HP = create_output(self, "Engine HP", Types.Type_VxReal)
    self.Shaft_Speed = create_output(self, "Shaft Speed", Types.Type_VxReal)
    self.Shaft_Torque = create_output(self, "Shaft Torque", Types.Type_VxReal)
    self.Shaft_Power = create_output(self, "Shaft Power", Types.Type_VxReal)

    # Internal outputs
    self.Delayed_Throttle = create_output(self, "Delayed Throttle", Types.Type_VxReal)
    self.Desired_Speed = create_output(self, "Desired Speed", Types.Type_VxReal)
    self.Constraint_Min_Torque = create_output(self, "Constraint Min Torque", Types.Type_VxReal)
    self.Constraint_Max_Torque = create_output(self, "Constraint Max Torque", Types.Type_VxReal)

    self.Engine_Running.setDescription("Set the engine to be running. When False, engine drive torque will be zero, though engine braking torque will still be applied")
    self.Throttle.setDescription("Input throttle between 0 and 1")
    self.Throttle_Delay.setDescription("Set the maximum rate the throttle can be increased, simulating the effect of engine response lag. Throttle rate of change will be limited so it can go from 0 to 1 in the time specified")
    self.Torque_Scale.setDescription("Scaling factor that is multiplied by the current torque from the torque table")
    self.Torque_Added.setDescription("Torque added to the computed engine torque")
    self.Braking_Torque_Scale.setDescription("Scaling factor that is multiplied by the current torque from the braking torque table")
    self.Braking_Torque_Added.setDescription("Torque added to the computed engine braking torque")
    self.Hinge_Velocity.setDescription("Current velocity from hinge constraint")
    self.Hinge_Torque.setDescription("Applied torque from hinge constraint")
    self.Shaft_Friction.setDescription("Friction applied to engine hinge")
    self.Torque_Table.setDescription("Engine torque table csv file with full throttle torque specified at each RPM")
    self.Idle_RPM.setDescription("Idle RPM")
    self.Max_Torque.setDescription("Maximum engine torque that can be delivered by the engine, calculated from the engine torque table")
    self.Max_RPM.setDescription("Maximum engine RPM, calculated from the engine torque table")
    self.Max_Power.setDescription("Maximum engine power in W that can be delivered by the engine, calculated from the engine torque table")
    self.Max_HP.setDescription("Maximum engine power in HP that can be delivered by the engine, calculated from the engine torque table")
    self.RPM_at_Max_Power.setDescription("Engine RPM at max power, calculated from the engine torque table")
    self.RPM_at_Max_Torque.setDescription("Engine RPM at max torque, calculated from the engine torque table")
    self.Engine_RPM.setDescription("Current engine RPM")
    self.Engine_HP.setDescription("Current power applied by engine in HP")
    self.Shaft_Speed.setDescription("Speed of output shaft in rad/s")
    self.Shaft_Torque.setDescription("Net torque on output shaft in N.m")
    self.Shaft_Power.setDescription("Net power on output shaft in W")
    self.Delayed_Throttle.setDescription("Throttle after applying Throttle Delay")
    self.Desired_Speed.setDescription("Desired RPM sent to engine constraint")
    self.Constraint_Min_Torque.setDescription("Min torque sent to engine constraint")
    self.Constraint_Max_Torque.setDescription("Max torque sent to engine constraint")

    # Torque Table
    # Full throttle torque table is defined by user
    try:
        with open(self.Torque_Table.value, 'rb') as f:
            reader = csv.reader(f)
            your_list = list(reader)  
            
        num_list = [[float(x) for x in rec] for rec in your_list[2:]]
        rpm = [x[0] for x in num_list]
        torque = [x[1] for x in num_list]

        # Extract basic values from torque table
        idle_rpm = self.Idle_RPM.value
        max_torque = max(torque)
        max_rpm = rpm[-1]
        power = [x*y for x,y in zip(rpm,torque)]
        max_p = max(power)
        max_power = max_p / 30*math.pi
        max_hp = max_power * 0.00134102
        rpm_at_max_torque = rpm[torque.index(max_torque)]
        rpm_at_max_power = rpm[power.index(max_p)]

        # Add a point a 0 rpm if there is not already
        if rpm[0] > 0:
            rpm.insert(0, 0)
            torque.insert(0, 0.1 * max_torque)

        self.Max_Torque.value = max_torque
        self.Max_RPM.value = max_rpm
        self.Max_Power.value = max_power
        self.Max_HP.value = max_hp
        self.RPM_at_Max_Power.value = rpm_at_max_power
        self.RPM_at_Max_Torque.value = rpm_at_max_torque

        self.torque_table = LinearInterpolation(rpm, torque)

        # Less then full throttle is derived by multiplying by a standard set of curves
        # Defined in spreadsheet
        throttle = [0.0, 0.25, 0.5, 0.75, 1.0]
        rpm =  [ 0.0,   
                 idle_rpm, 
                 idle_rpm + 0.1*(max_rpm - idle_rpm), 
                 idle_rpm + 0.25*(max_rpm - idle_rpm), 
                 idle_rpm + 0.5*(max_rpm - idle_rpm), 
                 max_rpm, 
                 max_rpm + 1]
        torque = [[1.0, 1.0,  1.0 , 1.0 , 1.0],
                  [1.0, 1.0,  1.0 , 1.0 , 1.0],
                  [0.0, 0.8,  0.96, 0.98, 1.0],
                  [0.0, 0.5,  0.9 , 0.95, 1.0],
                  [0.0, 0.0,  0.6 , 0.9 , 1.0],
                  [0.0, 0.0,  0.0 , 0.5 , 1.0],
                  [0.0, 0.0,  0.0 , 0.5 , 1.0]]

        self.throttle_multiplier = BilinearInterpolation(throttle, rpm, torque)

        # Desired RPM curve 
        des = [idle_rpm, idle_rpm + 0.5*(max_rpm - idle_rpm), max_rpm, max_rpm, max_rpm]
        self.desired_rpm = LinearInterpolation(throttle, des)

         # Brake torque table linearly increases to max torque at max rpm
        self.braking_torque_table = LinearInterpolation([-1.0, 0.0, max_rpm], [0.0, 0.0, -max_torque])

    except:
        self.torque_table = None
        self.braking_torque_table = None
        raise ValueError("Unable to load Torque Table")


def pre_step(self):

    if (self.torque_table is None) or (self.desired_rpm is None) or (self.braking_torque_table is None):
        return

    self.throttle_rate = self.getApplicationContext().getSimulationTimeStep() / max(self.Throttle_Delay.value, 0.001)
    self.Delayed_Throttle.value = min(self.Throttle.value, self.Delayed_Throttle.value + self.throttle_rate)
    throttle = self.Delayed_Throttle.value
    rpm = self.Hinge_Velocity.value * 30 / math.pi


    if self.inputs.Engine_Running.value:
        self.Desired_Speed.value = self.desired_rpm(throttle) / 30 * math.pi
        torque_raw = self.torque_table(rpm) * self.throttle_multiplier(throttle, rpm)
        self.Constraint_Max_Torque.value = max(torque_raw * self.Torque_Scale.value 
                                                + self.Torque_Added.value, 0)
        # print "rpm: {}, torq: {}, mult: {}".format(rpm, self.torque_table(rpm), self.throttle_multiplier(throttle, rpm))
    else:
        self.Desired_Speed.value = 0
        self.Constraint_Max_Torque.value = 0

    braking_torque_raw = self.braking_torque_table(max(rpm - self.Desired_Speed.value * 30 / math.pi, 0))
    self.Constraint_Min_Torque.value = min(braking_torque_raw * self.Braking_Torque_Scale.value 
                                            + self.Braking_Torque_Added.value, 0)

    self.Engine_RPM.value = rpm
    self.Shaft_Speed.value = self.Hinge_Velocity.value
    # Field reports net torque, so subtract friction torque from output torque
    # Since friction could be + or -, must use abs for subtraction, then reapply sign.
    self.Shaft_Torque.value = math.copysign(max(abs(self.Hinge_Torque.value) - self.Shaft_Friction.value, 0), self.Hinge_Torque.value)
    self.Shaft_Power.value = self.Shaft_Speed.value * self.Shaft_Torque.value
    self.Engine_HP.value = self.Shaft_Power.value * 0.00134102
