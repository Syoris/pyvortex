from VxSim import *
from math import *

def on_add_to_universe(self, universe):
    create_input(self, 'Test Time', Types.Type_VxReal)
    create_input(self, 'Test Started', Types.Type_Bool)
	
    create_input(self, 'VehicleSpeed', Types.Type_VxReal)
    create_input(self, 'EngineSpeed', Types.Type_VxReal)
    create_input(self, 'EngineTorque', Types.Type_VxReal)
    create_input(self, 'TransmissionGear', Types.Type_Int)

    create_input(self, 'WheelTorqueFL', Types.Type_VxReal)
    create_input(self, 'WheelTorqueFR', Types.Type_VxReal)
    create_input(self, 'WheelTorqueRL', Types.Type_VxReal)
    create_input(self, 'WheelTorqueRR', Types.Type_VxReal)
	
    create_input(self, 'CG Transform', Types.Type_VxMatrix44)
    create_input(self, 'CG Acceleration', Types.Type_VxVector3)
    create_input(self, 'CG Rotational Velocity', Types.Type_VxVector3)
    create_input(self, 'CG Rotational Acceleration', Types.Type_VxVector3)
    create_input(self, 'CG Position Offset', Types.Type_VxVector3)

    create_input(self, 'Wheel RPM FL', Types.Type_VxReal)
    create_input(self, 'Wheel RPM FR', Types.Type_VxReal)
    create_input(self, 'Wheel RPM RL', Types.Type_VxReal)
    create_input(self, 'Wheel RPM RR', Types.Type_VxReal)

    create_input(self, 'LongSlipFL', Types.Type_VxReal)
    create_input(self, 'LongSlipFR', Types.Type_VxReal)
    create_input(self, 'LongSlipRL', Types.Type_VxReal)
    create_input(self, 'LongSlipRR', Types.Type_VxReal)

    create_input(self, 'Wheel Long Fric Bound FL', Types.Type_VxReal)
    create_input(self, 'Wheel Long Fric Bound FR', Types.Type_VxReal)
    create_input(self, 'Wheel Long Fric Bound RL', Types.Type_VxReal)
    create_input(self, 'Wheel Long Fric Bound RR', Types.Type_VxReal)

    create_input(self, 'Wheel Long Fric Ratio FL', Types.Type_VxReal)
    create_input(self, 'Wheel Long Fric Ratio FR', Types.Type_VxReal)
    create_input(self, 'Wheel Long Fric Ratio RL', Types.Type_VxReal)
    create_input(self, 'Wheel Long Fric Ratio RR', Types.Type_VxReal)

    create_input(self, 'Wheel Lat Fric Bound FL', Types.Type_VxReal)
    create_input(self, 'Wheel Lat Fric Bound FR', Types.Type_VxReal)
    create_input(self, 'Wheel Lat Fric Bound RL', Types.Type_VxReal)
    create_input(self, 'Wheel Lat Fric Bound RR', Types.Type_VxReal)

    create_input(self, 'Wheel Lat Fric Ratio FL', Types.Type_VxReal)
    create_input(self, 'Wheel Lat Fric Ratio FR', Types.Type_VxReal)
    create_input(self, 'Wheel Lat Fric Ratio RL', Types.Type_VxReal)
    create_input(self, 'Wheel Lat Fric Ratio RR', Types.Type_VxReal)

    create_input(self, 'TireForceVertFL', Types.Type_VxReal)
    create_input(self, 'TireForceVertFR', Types.Type_VxReal)
    create_input(self, 'TireForceVertRL', Types.Type_VxReal)
    create_input(self, 'TireForceVertRR', Types.Type_VxReal)
	
    create_input(self, 'Wheel Sinkage FL', Types.Type_VxReal)
    create_input(self, 'Wheel Sinkage FR', Types.Type_VxReal)
    create_input(self, 'Wheel Sinkage RL', Types.Type_VxReal)
    create_input(self, 'Wheel Sinkage RR', Types.Type_VxReal)
	
    create_input(self, 'Compaction Resistance Force FL', Types.Type_VxReal)
    create_input(self, 'Compaction Resistance Force FR', Types.Type_VxReal)
    create_input(self, 'Compaction Resistance Force RL', Types.Type_VxReal)
    create_input(self, 'Compaction Resistance Force RR', Types.Type_VxReal)
	
    create_input(self, 'Compaction Resistance Torque FL', Types.Type_VxReal)
    create_input(self, 'Compaction Resistance Torque FR', Types.Type_VxReal)
    create_input(self, 'Compaction Resistance Torque RL', Types.Type_VxReal)
    create_input(self, 'Compaction Resistance Torque RR', Types.Type_VxReal)

    create_input(self, 'DrawbarForce', Types.Type_VxReal, default_value=0.0)

    create_input(self, 'Custom Field 1', Types.Type_VxReal)
    create_input(self, 'Custom Field 2', Types.Type_VxReal)
	
    create_input(self, 'Ground Pressure FL', Types.Type_VxReal)
    create_input(self, 'Ground Pressure FR', Types.Type_VxReal)
    create_input(self, 'Ground Pressure RL', Types.Type_VxReal)
    create_input(self, 'Ground Pressure RR', Types.Type_VxReal)
	
    create_input(self, 'Tire Deflection FL', Types.Type_VxReal)
    create_input(self, 'Tire Deflection FR', Types.Type_VxReal)
    create_input(self, 'Tire Deflection RL', Types.Type_VxReal)
    create_input(self, 'Tire Deflection RR', Types.Type_VxReal)
	
    create_input(self, 'Ground Deflection FL', Types.Type_VxReal)
    create_input(self, 'Ground Deflection FR', Types.Type_VxReal)
    create_input(self, 'Ground Deflection RL', Types.Type_VxReal)
    create_input(self, 'Ground Deflection RR', Types.Type_VxReal)

###################################################################
###################################################################

    create_output(self, 'Test Time', Types.Type_VxReal)
	
    create_output(self, 'VehicleSpeed', Types.Type_VxReal)
    create_output(self, 'EngineSpeed', Types.Type_VxReal)
    create_output(self, 'EngineTorque', Types.Type_VxReal)
    create_output(self, 'TransmissionGear', Types.Type_Int)
	
    create_output(self, 'CGPosX', Types.Type_VxReal)
    create_output(self, 'CGPosY', Types.Type_VxReal)
    create_output(self, 'CGPosZ', Types.Type_VxReal)
    create_output(self, 'CGLongAccel', Types.Type_VxReal)
    create_output(self, 'CGLatAccel', Types.Type_VxReal)
    create_output(self, 'CGVertAccel', Types.Type_VxReal)
    create_output(self, 'CGRollAngle', Types.Type_VxReal)
    create_output(self, 'CGRollRate', Types.Type_VxReal)
    create_output(self, 'CGPitchAngle', Types.Type_VxReal)
    create_output(self, 'CGPitchRate', Types.Type_VxReal)
    create_output(self, 'CGYawAngle', Types.Type_VxReal)
    create_output(self, 'CGYawRate', Types.Type_VxReal)
    create_output(self, 'LoadTransferRatio', Types.Type_VxReal)

    create_output(self, 'WheelTorqueFL', Types.Type_VxReal)
    create_output(self, 'WheelTorqueFR', Types.Type_VxReal)
    create_output(self, 'WheelTorqueRL', Types.Type_VxReal)
    create_output(self, 'WheelTorqueRR', Types.Type_VxReal)

    create_output(self, 'Wheel RPM FL', Types.Type_VxReal)
    create_output(self, 'Wheel RPM FR', Types.Type_VxReal)
    create_output(self, 'Wheel RPM RL', Types.Type_VxReal)
    create_output(self, 'Wheel RPM RR', Types.Type_VxReal)

    create_output(self, 'LongSlipFL', Types.Type_VxReal)
    create_output(self, 'LongSlipFR', Types.Type_VxReal)
    create_output(self, 'LongSlipRL', Types.Type_VxReal)
    create_output(self, 'LongSlipRR', Types.Type_VxReal)

    create_output(self, 'Wheel Long Fric Bound FL', Types.Type_VxReal)
    create_output(self, 'Wheel Long Fric Bound FR', Types.Type_VxReal)
    create_output(self, 'Wheel Long Fric Bound RL', Types.Type_VxReal)
    create_output(self, 'Wheel Long Fric Bound RR', Types.Type_VxReal)

    create_output(self, 'Wheel Long Fric Ratio FL', Types.Type_VxReal)
    create_output(self, 'Wheel Long Fric Ratio FR', Types.Type_VxReal)
    create_output(self, 'Wheel Long Fric Ratio RL', Types.Type_VxReal)
    create_output(self, 'Wheel Long Fric Ratio RR', Types.Type_VxReal)

    create_output(self, 'Wheel Lat Fric Bound FL', Types.Type_VxReal)
    create_output(self, 'Wheel Lat Fric Bound FR', Types.Type_VxReal)
    create_output(self, 'Wheel Lat Fric Bound RL', Types.Type_VxReal)
    create_output(self, 'Wheel Lat Fric Bound RR', Types.Type_VxReal)

    create_output(self, 'Wheel Lat Fric Ratio FL', Types.Type_VxReal)
    create_output(self, 'Wheel Lat Fric Ratio FR', Types.Type_VxReal)
    create_output(self, 'Wheel Lat Fric Ratio RL', Types.Type_VxReal)
    create_output(self, 'Wheel Lat Fric Ratio RR', Types.Type_VxReal)

    create_output(self, 'TireForceVertFL', Types.Type_VxReal)
    create_output(self, 'TireForceVertFR', Types.Type_VxReal)
    create_output(self, 'TireForceVertRL', Types.Type_VxReal)
    create_output(self, 'TireForceVertRR', Types.Type_VxReal)
	
    create_output(self, 'Wheel Sinkage FL', Types.Type_VxReal)
    create_output(self, 'Wheel Sinkage FR', Types.Type_VxReal)
    create_output(self, 'Wheel Sinkage RL', Types.Type_VxReal)
    create_output(self, 'Wheel Sinkage RR', Types.Type_VxReal)
	
    create_output(self, 'Compaction Resistance Force FL', Types.Type_VxReal)
    create_output(self, 'Compaction Resistance Force FR', Types.Type_VxReal)
    create_output(self, 'Compaction Resistance Force RL', Types.Type_VxReal)
    create_output(self, 'Compaction Resistance Force RR', Types.Type_VxReal)
	
    create_output(self, 'Compaction Resistance Torque FL', Types.Type_VxReal)
    create_output(self, 'Compaction Resistance Torque FR', Types.Type_VxReal)
    create_output(self, 'Compaction Resistance Torque RL', Types.Type_VxReal)
    create_output(self, 'Compaction Resistance Torque RR', Types.Type_VxReal)

    create_output(self, 'DrawbarForce', Types.Type_VxReal, default_value=0.0)

    create_output(self, 'Custom Field 1', Types.Type_VxReal)
    create_output(self, 'Custom Field 2', Types.Type_VxReal)
	
    create_output(self, 'RR', Types.Type_VxReal)
    create_output(self, 'AveSlip', Types.Type_VxReal)
    create_output(self, 'MaxSinkage', Types.Type_VxReal)
    create_output(self, 'Thrust', Types.Type_VxReal)
	
    create_output(self, 'Ground Pressure FL', Types.Type_VxReal)
    create_output(self, 'Ground Pressure FR', Types.Type_VxReal)
    create_output(self, 'Ground Pressure RL', Types.Type_VxReal)
    create_output(self, 'Ground Pressure RR', Types.Type_VxReal)
	
    create_output(self, 'Tire Deflection FL', Types.Type_VxReal)
    create_output(self, 'Tire Deflection FR', Types.Type_VxReal)
    create_output(self, 'Tire Deflection RL', Types.Type_VxReal)
    create_output(self, 'Tire Deflection RR', Types.Type_VxReal)
	
    create_output(self, 'Ground Deflection FL', Types.Type_VxReal)
    create_output(self, 'Ground Deflection FR', Types.Type_VxReal)
    create_output(self, 'Ground Deflection RL', Types.Type_VxReal)
    create_output(self, 'Ground Deflection RR', Types.Type_VxReal)

###################################################################
###################################################################
    
    self.initialPositionSaved = False
    self.initialTransform = VxSim.Matrix44()
    self.initialPosition = VxVector3()
    self.FLPositions = [VxSim.VxVector3(), VxSim.VxVector3(), VxSim.VxVector3()]
    self.FRPositions = [VxSim.VxVector3(), VxSim.VxVector3(), VxSim.VxVector3()]

    self.toG = 1.0/9.81
    self.toDeg = 180.0 / pi
    self.toKMpH = 3.6
    self.steeringRatio = 1.0

def pre_step(self):

    transform = self.inputs.CG_Transform.value

    if self.inputs.Test_Started.value and not self.initialPositionSaved:
        self.initialPositionSaved = True
        self.initialTransform = self.inputs.CG_Transform.value
        self.initialPosition = getTranslation(self.initialTransform)
    
    self.outputs.Test_Time.value = self.inputs.Test_Time.value
	
    self.outputs.LoadTransferRatio.value = ((self.inputs.TireForceVertFR.value+self.inputs.TireForceVertRR.value)-(self.inputs.TireForceVertFL.value+self.inputs.TireForceVertRL.value))/max((self.inputs.TireForceVertFL.value+self.inputs.TireForceVertFR.value+self.inputs.TireForceVertRL.value+self.inputs.TireForceVertRR.value),1)
	
    self.outputs.VehicleSpeed.value = self.inputs.VehicleSpeed.value
    self.outputs.EngineSpeed.value = self.inputs.EngineSpeed.value
    self.outputs.EngineTorque.value = self.inputs.EngineTorque.value
    self.outputs.TransmissionGear.value = self.inputs.TransmissionGear.value
	
    [self.outputs.CGPosX.value, self.outputs.CGPosY.value, self.outputs.CGPosZ.value] = getTranslation(self.inputs.CG_Transform.value) - self.initialPosition + self.inputs.CG_Position_Offset.value
    [self.outputs.CGLongAccel.value, self.outputs.CGLatAccel.value, self.outputs.CGVertAccel.value] = self.toG * inverseRotate(transform, self.inputs.CG_Acceleration.value)
    [self.outputs.CGRollRate.value, self.outputs.CGPitchRate.value, self.outputs.CGYawRate.value] = self.toDeg * inverseRotate(transform, self.inputs.CG_Rotational_Velocity.value)

    # Approximation of roll/pitch is angle between side/forward vector and horizontal, which simplifies to just asin of the vector z component
    self.outputs.CGRollAngle.value = self.toDeg * asin(transform[2][1]) 
    self.outputs.CGPitchAngle.value = self.toDeg * asin(transform[2][0]) 
    self.outputs.CGYawAngle.value = - self.toDeg * getRotation(transform).z
	
    self.outputs.WheelTorqueFL.value = self.inputs.WheelTorqueFL.value
    self.outputs.WheelTorqueFR.value = self.inputs.WheelTorqueFR.value
    self.outputs.WheelTorqueRL.value = self.inputs.WheelTorqueRL.value
    self.outputs.WheelTorqueRR.value = self.inputs.WheelTorqueRR.value
	
    self.outputs.Wheel_RPM_FL.value = self.inputs.Wheel_RPM_FL.value
    self.outputs.Wheel_RPM_FR.value = self.inputs.Wheel_RPM_FR.value
    self.outputs.Wheel_RPM_RL.value = self.inputs.Wheel_RPM_RL.value
    self.outputs.Wheel_RPM_RR.value = self.inputs.Wheel_RPM_RR.value
	
    self.outputs.LongSlipFL.value = self.inputs.LongSlipFL.value
    self.outputs.LongSlipFR.value = self.inputs.LongSlipFR.value
    self.outputs.LongSlipRL.value = self.inputs.LongSlipRL.value
    self.outputs.LongSlipRR.value = self.inputs.LongSlipRR.value
	
    self.outputs.Ground_Pressure_FL.value = self.inputs.Ground_Pressure_FL.value
    self.outputs.Ground_Pressure_FR.value = self.inputs.Ground_Pressure_FR.value
    self.outputs.Ground_Pressure_RL.value = self.inputs.Ground_Pressure_RL.value
    self.outputs.Ground_Pressure_RR.value = self.inputs.Ground_Pressure_RR.value
	
    self.outputs.Tire_Deflection_FL.value = self.inputs.Tire_Deflection_FL.value
    self.outputs.Tire_Deflection_FR.value = self.inputs.Tire_Deflection_FR.value
    self.outputs.Tire_Deflection_RL.value = self.inputs.Tire_Deflection_RL.value
    self.outputs.Tire_Deflection_RR.value = self.inputs.Tire_Deflection_RR.value
	
    self.outputs.Ground_Deflection_FL.value = self.inputs.Ground_Deflection_FL.value
    self.outputs.Ground_Deflection_FR.value = self.inputs.Ground_Deflection_FR.value
    self.outputs.Ground_Deflection_RL.value = self.inputs.Ground_Deflection_RL.value
    self.outputs.Ground_Deflection_RR.value = self.inputs.Ground_Deflection_RR.value
	
    self.outputs.Wheel_Long_Fric_Bound_FL.value = self.inputs.Wheel_Long_Fric_Bound_FL.value
    self.outputs.Wheel_Long_Fric_Bound_FR.value = self.inputs.Wheel_Long_Fric_Bound_FR.value
    self.outputs.Wheel_Long_Fric_Bound_RL.value = self.inputs.Wheel_Long_Fric_Bound_RL.value
    self.outputs.Wheel_Long_Fric_Bound_RR.value = self.inputs.Wheel_Long_Fric_Bound_RR.value
	
    self.outputs.Wheel_Long_Fric_Ratio_FL.value = self.inputs.Wheel_Long_Fric_Ratio_FL.value
    self.outputs.Wheel_Long_Fric_Ratio_FR.value = self.inputs.Wheel_Long_Fric_Ratio_FR.value
    self.outputs.Wheel_Long_Fric_Ratio_RL.value = self.inputs.Wheel_Long_Fric_Ratio_RL.value
    self.outputs.Wheel_Long_Fric_Ratio_RR.value = self.inputs.Wheel_Long_Fric_Ratio_RR.value
	
    self.outputs.Wheel_Lat_Fric_Bound_FL.value = self.inputs.Wheel_Lat_Fric_Bound_FL.value
    self.outputs.Wheel_Lat_Fric_Bound_FR.value = self.inputs.Wheel_Lat_Fric_Bound_FR.value
    self.outputs.Wheel_Lat_Fric_Bound_RL.value = self.inputs.Wheel_Lat_Fric_Bound_RL.value
    self.outputs.Wheel_Lat_Fric_Bound_RR.value = self.inputs.Wheel_Lat_Fric_Bound_RR.value
	
    self.outputs.Wheel_Lat_Fric_Ratio_FL.value = self.inputs.Wheel_Lat_Fric_Ratio_FL.value
    self.outputs.Wheel_Lat_Fric_Ratio_FR.value = self.inputs.Wheel_Lat_Fric_Ratio_FR.value
    self.outputs.Wheel_Lat_Fric_Ratio_RL.value = self.inputs.Wheel_Lat_Fric_Ratio_RL.value
    self.outputs.Wheel_Lat_Fric_Ratio_RR.value = self.inputs.Wheel_Lat_Fric_Ratio_RR.value
	
    self.outputs.Thrust.value=self.inputs.Wheel_Long_Fric_Bound_FL.value+self.inputs.Wheel_Long_Fric_Bound_FR.value+self.inputs.Wheel_Long_Fric_Bound_RL.value+self.inputs.Wheel_Long_Fric_Bound_RR.value
	
    self.outputs.TireForceVertFL.value = self.inputs.TireForceVertFL.value
    self.outputs.TireForceVertFR.value = self.inputs.TireForceVertFR.value
    self.outputs.TireForceVertRL.value = self.inputs.TireForceVertRL.value
    self.outputs.TireForceVertRR.value = self.inputs.TireForceVertRR.value
	
    self.outputs.Wheel_Sinkage_FL.value = self.inputs.Wheel_Sinkage_FL.value
    self.outputs.Wheel_Sinkage_FR.value = self.inputs.Wheel_Sinkage_FR.value
    self.outputs.Wheel_Sinkage_RL.value = self.inputs.Wheel_Sinkage_RL.value
    self.outputs.Wheel_Sinkage_RR.value = self.inputs.Wheel_Sinkage_RR.value
	
    self.outputs.Compaction_Resistance_Force_FL.value = self.inputs.Compaction_Resistance_Force_FL.value
    self.outputs.Compaction_Resistance_Force_FR.value = self.inputs.Compaction_Resistance_Force_FR.value
    self.outputs.Compaction_Resistance_Force_RL.value = self.inputs.Compaction_Resistance_Force_RL.value
    self.outputs.Compaction_Resistance_Force_RR.value = self.inputs.Compaction_Resistance_Force_RR.value
	
    self.outputs.Compaction_Resistance_Torque_FL.value = self.inputs.Compaction_Resistance_Torque_FL.value
    self.outputs.Compaction_Resistance_Torque_FR.value = self.inputs.Compaction_Resistance_Torque_FR.value
    self.outputs.Compaction_Resistance_Torque_RL.value = self.inputs.Compaction_Resistance_Torque_RL.value
    self.outputs.Compaction_Resistance_Torque_RR.value = self.inputs.Compaction_Resistance_Torque_RR.value
	
    self.outputs.DrawbarForce.value = self.inputs.DrawbarForce.value
    self.outputs.Custom_Field_1.value = self.inputs.Custom_Field_1.value
    self.outputs.Custom_Field_2.value = self.inputs.Custom_Field_2.value
	
    self.outputs.RR.value = max((self.inputs.Compaction_Resistance_Force_FL.value + self.inputs.Compaction_Resistance_Force_FR.value + self.inputs.Compaction_Resistance_Force_RL.value + self.inputs.Compaction_Resistance_Force_RR.value), 1.0) / \
                max((self.inputs.TireForceVertFL.value + self.inputs.TireForceVertFR.value + self.inputs.TireForceVertRL.value + self.inputs.TireForceVertRR.value), 1.0) *100.
        
    self.outputs.AveSlip.value = (self.inputs.LongSlipFL.value + self.inputs.LongSlipFR.value + self.inputs.LongSlipRL.value + self.inputs.LongSlipRR.value) / 4.0 * 100.
	
    self.outputs.MaxSinkage.value = max([self.inputs.Wheel_Sinkage_FL.value, self.inputs.Wheel_Sinkage_FR.value, self.inputs.Wheel_Sinkage_RL.value, self.inputs.Wheel_Sinkage_RR.value])

# Functions create fields in the Editor
def create_output(extension, name, o_type, default_value=None):
     """Create output field with optional default value, reset on every simulation run."""
     if extension.getOutput(name) is None:
          extension.addOutput(name, o_type)
     if default_value is not None:
          extension.getOutput(name).value = default_value
     return extension.getOutput(name)

def create_parameter(extension, name, p_type, default_value=None):
     """Create parameter field with optional default value set only when the field is created."""
     if extension.getParameter(name) is None:
          field = extension.addParameter(name, p_type)
          if default_value is not None:
                field.value = default_value
     return extension.getParameter(name)

def create_input(extension, name, i_type, default_value=None):
     """Create input field with optional default value set only when the field is created."""
     if extension.getInput(name) is None:
          field = extension.addInput(name, i_type)
          if default_value is not None:
                field.value = default_value
     return extension.getInput(name)

# Rotate vector so it is expressed in a different frame
def inverseRotate(transformation, vector):
    result = VxVector3(transformation[0][0] * vector[0] + transformation[1][0] * vector[1] + transformation[2][0] * vector[2],
                       transformation[0][1] * vector[0] + transformation[1][1] * vector[1] + transformation[2][1] * vector[2],
                       transformation[0][2] * vector[0] + transformation[1][2] * vector[1] + transformation[2][2] * vector[2])
    return result