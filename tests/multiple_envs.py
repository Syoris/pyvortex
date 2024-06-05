"""File to try to run multiple Vortex environments in the same script.

2024/06/05: Not working yet. The 2nd environment is created, but it is not rendering the scene
"""

from pathlib import Path
import sys

import pyvortex
import Vortex  # noqa
from pyvortex.vortex_env import VortexEnv
import vxatp3  # noqa

config_file = 'config_no_disp.vxc'
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


# print('\n---------- APP 1 ----------')
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

# app2.update()

# ...

print('\n---------- APP 1 ----------')
vortex_env = VortexEnv(
    assets_dir=Path(__file__).parent / 'assets',
    config_file=config_file,
    content_file=content_file,
    viewpoints=['Global', 'Perspective'],
)

print('\n---------- APP 2 ----------')
vortex_env2 = VortexEnv(
    assets_dir=Path(__file__).parent / 'assets',
    config_file=config_file,
    content_file=content_file,
    viewpoints=['Global', 'Perspective'],
)

print('Done')
