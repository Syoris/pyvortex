# This script uses a set of control point inputs and calculates part and 
# constraint positions accordingly

from tools import *
import math

def on_add_to_universe(self, universe):

    create_input(self, 'Enable', Types.Type_Bool).setDescription("True to update calculations")

    create_parameter(self, 'LCA Rear Position', Types.Type_VxVector3).setDescription("Position of lower control arm rear bushing")
    create_parameter(self, 'LCA Front Position', Types.Type_VxVector3).setDescription("Position of lower control arm front bushing")
    create_parameter(self, 'LCA Outer Position', Types.Type_VxVector3).setDescription("Position of lower control arm outer bushing")
    create_parameter(self, 'UCA Rear Position', Types.Type_VxVector3).setDescription("Position of upper control arm rear bushing")
    create_parameter(self, 'UCA Front Position', Types.Type_VxVector3).setDescription("Position of upper control arm front bushing")
    create_parameter(self, 'UCA Outer Position', Types.Type_VxVector3).setDescription("Position of upper control arm outer bushing")
    create_parameter(self, 'Strut Upper Position', Types.Type_VxVector3).setDescription("Position of strut upper bushing")
    create_parameter(self, 'Strut Lower Position', Types.Type_VxVector3).setDescription("Position of strut lower bushing")
    create_parameter(self, 'Reverse Y', Types.Type_Bool).setDescription("Set true to mirror the suspension to the opposite side of the vehicle by reversing all the Y dimenions")

    # Part transforms
    create_output(self, 'LCA Transform', Types.Type_VxMatrix44)
    create_output(self, 'UCA Transform', Types.Type_VxMatrix44)
    create_output(self, 'Knuckle Transform', Types.Type_VxMatrix44)

    # Constraint attachments
    create_output(self, 'LCA Front Offset', Types.Type_VxVector3)
    create_output(self, 'LCA Primary', Types.Type_VxVector3)
    create_output(self, 'LCA Secondary', Types.Type_VxVector3)
    create_output(self, 'UCA Front Offset', Types.Type_VxVector3)
    create_output(self, 'Knuckle Upper Offset', Types.Type_VxVector3)
    create_output(self, 'UCA Primary', Types.Type_VxVector3)
    create_output(self, 'UCA Secondary', Types.Type_VxVector3)
    create_output(self, 'Strut Upper Position', Types.Type_VxVector3)
    create_output(self, 'Strut Lower Position', Types.Type_VxVector3)

    # Starting info
    create_output(self, 'Strut Initial Length', Types.Type_VxReal)

def paused_update(self):
    config_update(self)

def config_update(self):
    # Skip update if disabled
    if not self.inputs.Enable.value:
        return

    # Positions of points
    lcar_pos = self.parameters.LCA_Rear_Position.value
    lcaf_pos = self.parameters.LCA_Front_Position.value
    lcao_pos = self.parameters.LCA_Outer_Position.value
    ucar_pos = self.parameters.UCA_Rear_Position.value
    ucaf_pos = self.parameters.UCA_Front_Position.value
    ucao_pos = self.parameters.UCA_Outer_Position.value
    su_pos = self.parameters.Strut_Upper_Position.value
    sl_pos = self.parameters.Strut_Lower_Position.value

    # Reverse - negate y value to shift from left to right
    if self.parameters.Reverse_Y.value:
        lcar_pos.y = -lcar_pos.y
        lcaf_pos.y = -lcaf_pos.y
        lcao_pos.y = -lcao_pos.y
        ucar_pos.y = -ucar_pos.y
        ucaf_pos.y = -ucaf_pos.y
        ucao_pos.y = -ucao_pos.y
        su_pos.y = -su_pos.y
        sl_pos.y = -sl_pos.y

    # Calculate constraint directions
    # Hinge oriented from rear to front
    lca_prim = lcaf_pos - lcar_pos
    lca_prim.normalize()
    
    uca_prim = ucaf_pos - ucar_pos
    uca_prim.normalize()
    # Secondary direction points to outer point, orthoganal to primary direction
    lca_sec = lcao_pos - lcar_pos
    lca_sec.orthogonalize(lca_prim)
    lca_sec.normalize()
    
    uca_sec = ucao_pos - ucar_pos
    uca_sec.orthogonalize(uca_prim)
    uca_sec.normalize()


    # Part transforms
    self.outputs.LCA_Transform.value = createTranslation(lcar_pos)
    self.outputs.UCA_Transform.value = createTranslation(ucar_pos)
    self.outputs.Knuckle_Transform.value = createTranslation(lcao_pos)

    # Constraint attachments
    self.outputs.LCA_Front_Offset.value = lcaf_pos - lcar_pos # Front position is offset from part origin, which is rear position
    self.outputs.LCA_Primary.value = lca_prim
    self.outputs.LCA_Secondary.value = lca_sec

    self.outputs.UCA_Front_Offset.value = ucaf_pos - ucar_pos # Front position is offset from part origin, which is rear position
    self.outputs.Knuckle_Upper_Offset.value = ucao_pos - lcao_pos # Upper knuckle position is offset from part origin, which is buttom knuckle position
    self.outputs.UCA_Primary.value = uca_prim
    self.outputs.UCA_Secondary.value = uca_sec

    self.outputs.Strut_Upper_Position.value = su_pos - lcar_pos
    self.outputs.Strut_Lower_Position.value = sl_pos - lcar_pos

    self.outputs.Strut_Initial_Length.value = (su_pos - sl_pos).norm()