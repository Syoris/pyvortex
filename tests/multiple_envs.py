"""File to try to run multiple Vortex environments in the same script.

2024/06/05: Not working yet. The 2nd environment is created, but it is not rendering the scene
"""

from pathlib import Path
import sys

import pyvortex
from pyvortex.vortex_classes import AppMode
import Vortex  # noqa
from pyvortex.vortex_env import VortexEnv
import vxatp3  # noqa

config_file = 'config.vxc'
content_file = 'Kinova Gen2 Unjamming/Scenes/kinova_peg-in-hole.vxscene'

assets_dir = Path(__file__).parent / 'assets'
setup_file_path: Path = assets_dir / config_file  # 'config_withoutgraphics.vxc'
content_file_path: Path = assets_dir / content_file  # scene file

args = [
    '--simAppsCount',
    '2',
    '--simulatorname',
    'SimName',
]
Vortex.InitializationParameters(args)


# # print('\n---------- APP 1 ----------')
# app_name: str = 'Vortex App_1'
# print(f'Application name: {app_name}')

# app = Vortex.VxApplication()

# serializer = Vortex.VxObjectSerializer()
# serializer.load(str(setup_file_path))
# config = Vortex.ApplicationConfigInterface(serializer.getObject())
# config.parameterPython3.interpreterDirectory.value = sys.exec_prefix
# config.apply(app)

# scene_file_str = str(content_file_path)
# scene = app.getSimulationFileManager().loadObject(scene_file_str)

# display = Vortex.VxExtensionFactory.create(Vortex.DisplayICD.kExtensionFactoryKey)
# display.getInput(Vortex.DisplayICD.kPlacementMode).setValue('Windowed')
# display.setName('APP 1')
# display.getInput(Vortex.DisplayICD.kPlacement).setValue(Vortex.VxVector4(50, 50, 1280, 720))
# # display.getInput(Vortex.DisplayICD.kViewpointName).setValue(viewpoint_name)
# app.add(display)

# app.update()


# print('\n---------- APP 2 ----------')
# app_name2: str = 'Vortex App_2'
# print(f'Application name: {app_name2}')

# app2 = Vortex.VxApplication()

# # serializer = Vortex.VxObjectSerializer()
# # serializer.load(str(_setup_file_path))
# setup_file_path: Path = assets_dir / 'config.vxc'  # 'config_withoutgraphics.vxc'

# serializer2 = Vortex.VxObjectSerializer()
# serializer2.load(str(setup_file_path))
# config2 = Vortex.ApplicationConfigInterface(serializer.getObject())
# config2.parameterPython3.interpreterDirectory.value = sys.exec_prefix
# config2.apply(app2)

# scene_file_str = str(content_file_path)
# scene2 = app2.getSimulationFileManager().loadObject(scene_file_str)

# display2 = Vortex.VxExtensionFactory.create(Vortex.DisplayICD.kExtensionFactoryKey)
# display2.getInput(Vortex.DisplayICD.kPlacementMode).setValue('Windowed')
# display2.setName('APP 2')
# display2.getInput(Vortex.DisplayICD.kPlacement).setValue(Vortex.VxVector4(50, 50, 1280, 720))
# # display.getInput(Vortex.DisplayICD.kViewpointName).setValue(viewpoint_name)
# app2.add(display2)

# # -------- TESTS --------
# app.pause(True)
# app2.pause(True)

# app.pause(False)
# app2.pause(False)

# vxatp3.VxATPUtils.requestApplicationModeChangeAndWait(app, AppMode.SIMULATING.value)
# vxatp3.VxATPUtils.requestApplicationModeChangeAndWait(app2, AppMode.EDITING.value)

# AppMode(app.getApplicationMode())
# app2.getApplicationMode()

# app.update()
# app2.update()

# print('Done')

print('\n---------- APP 1 ----------')
vortex_env = VortexEnv(
    assets_dir=Path(__file__).parent / 'assets',
    config_file=config_file,
    content_file=content_file,
    viewpoints=['Global', 'Perspective'],
)

vortex_env.set_input('j2_vel_id', 5)
for _ in range(100):
    vortex_env.step()

j2_angle = vortex_env.get_output('j2_pos')
j4_angle = vortex_env.get_output('j4_pos')
j6_angle = vortex_env.get_output('j6_pos')

print('\n---------- APP 2 ----------')
config_file2 = 'config_eval.vxc'
content_file2 = 'Kinova Gen2 Unjamming/Scenes/kinova_peg-in-hole_eval.vxscene'
vortex_env2 = VortexEnv(
    assets_dir=Path(__file__).parent / 'assets',
    config_file=config_file,
    content_file=content_file2,
    viewpoints=['Global'],
)

j2_angle2_in = vortex_env2.get_output('j2_pos')
j4_angle2_in = vortex_env2.get_output('j4_pos')
j6_angle2_in = vortex_env2.get_output('j6_pos')

vortex_env2.set_input('j2_vel_id', 5)
for _ in range(100):
    vortex_env2.step()

j2_angle2 = vortex_env2.get_output('j2_pos')
j4_angle2 = vortex_env2.get_output('j4_pos')
j6_angle2 = vortex_env2.get_output('j6_pos')

print('Done')
