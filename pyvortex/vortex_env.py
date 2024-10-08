"""
To interface with Vortex.

Two main ways to exchange data with the application: its API or the dll.
The API is easier but only works w/ python 3.8.
I dont know where the dll's doc can be found
"""

from pathlib import Path
import sys
import numpy as np

import Vortex  # noqa
import vxatp3  # noqa

from pyvortex.vortex_classes import AppMode
import datetime


def np_to_Mat44(array: np.ndarray) -> Vortex.Matrix44:
    """
    Convert a numpy array to a Vortex Mat44

    Args:
        array (np.ndarray): 4x4 array

    Returns:
        Vortex.Mat44: Vortex Mat44
    """
    if array.shape != (4, 4):
        raise ValueError('Array shape must be (4, 4)')

    if not (array[0:3, 0:3] == np.eye(3)).all():
        raise ValueError('Rotations are not yet supported')

    mat = Vortex.createTranslation(array[0, 3], array[1, 3], array[2, 3])
    return mat


class VortexEnv:
    """
    To interface with Vortex.

    Handles definitions of dll functions and their calling

    """

    def __init__(
        self,
        assets_dir: Path,
        config_file: str,
        content_file: str,
        h=0.01,
        viewpoints: list = [],  # Name of the viewpoints to render. '' for default
        render: bool = True,
    ) -> None:
        print('[VortexEnv.__init__] Initializing VortexEnv')

        """
        Create a vortex application loading the specified scene and config files.

        After the initialization, the application is in SIMULATING mode at time=h.
        """
        self.sim_time = 0.0
        self.step_count = 0  # Step counter

        """Initialize environment (Vortex) parameters"""
        # Vortex
        self.h = h  # Simulation time step
        self._config_file = Path(config_file)
        self._content_file = Path(content_file)

        """ Load Vortex Scene """
        # Define the setup and scene file paths
        self.assets_dir: Path = assets_dir
        self._setup_file_path: Path = self.assets_dir / self._config_file  # 'config_withoutgraphics.vxc'
        self._content_file_path: Path = self.assets_dir / self._content_file  # scene file

        current_time = datetime.datetime.now().strftime('%m-%d-%S')
        self.application_name: str = f'Vortex App_{current_time}'
        print(f'[VortexEnv.__init__] Application name: {self.application_name}')

        # Create the Vortex Application
        self._create_application()
        self._load_scene()

        if self.h != self.get_simulation_time_step():
            raise ValueError(
                f'Simulation time step mismatch between application and config: {self.h} != {self.get_simulation_time_step()}'
            )

        # Displays
        self.render_mode = render
        self.viewpoints_list = []
        self.display_dict = {}
        self._init_displays(viewpoints, render=self.render_mode)

        # Step the simulation
        self.set_app_mode(AppMode.SIMULATING)
        self.step()

        print('[VortexEnv.__init__] Initializion done')

    def __del__(self):
        # Destroy the VxApplication when done
        self.app = None

    def _create_application(self):
        """To create the Vortex application"""
        self.app = Vortex.VxApplication()

        serializer = Vortex.VxObjectSerializer()
        serializer.load(str(self._setup_file_path))

        config = Vortex.ApplicationConfigInterface(serializer.getObject())
        config.parameterPython3.interpreterDirectory.value = sys.exec_prefix
        config.apply(self.app)

        self.set_app_mode(AppMode.EDITING)

    def _load_scene(self):
        """To load the Vortex scene

        Raises:
            RuntimeError: If the scene is not properly loaded
        """
        scene_file_str = str(self._content_file_path)
        self.scene = self.app.getSimulationFileManager().loadObject(scene_file_str)

        # Get the RL Interface VHL
        self.interface = self.scene.findExtensionByName('ML Interface')

        if self.scene is None or self.scene == 0:
            raise RuntimeError('Scene not properly loaded')

    """ Setter/Getter"""

    def set_parameter(self, field_name: str, field_value):
        self.interface.getParameterContainer()[field_name].value = field_value

    def set_input(self, field_name: str, field_value):
        if isinstance(field_value, np.ndarray):
            if field_value.shape == (4, 4):
                field_value = np_to_Mat44(field_value)

        self.interface.getInputContainer()[field_name].value = field_value

    def get_input(self, field_name: str):
        try:
            val = self.interface.getInputContainer()[field_name].value

            if isinstance(val, Vortex.Matrix44):
                val = np.array(val)

        except AttributeError as err:  # If value name invalid
            raise err

        return val

    def get_output(self, field_name: str):
        try:
            val = self.interface.getOutputContainer()[field_name].value

            if isinstance(val, Vortex.Matrix44):
                val = np.array(val)

        except AttributeError as err:  # If value name invalid
            raise err

        return val

    def get_app_mode(self) -> AppMode:
        return AppMode(self.app.getApplicationMode())

    def set_app_mode(self, app_mode: AppMode):
        self.app.pause(True)
        vxatp3.VxATPUtils.requestApplicationModeChangeAndWait(self.app, app_mode.value)
        self.app.pause(False)

    def get_simulation_time_step(self):
        return self.app.getSimulationTimeStep()

    def sim_paused(self):
        return self.app.isPaused()

    def pause_sim(self, pause: bool):
        self.app.pause(pause)
        self.app.update()

    """ Display """

    def _init_displays(self, viewpoints: list, render=True):
        """To initialize the displays"""
        if not viewpoints:
            self.viewpoints_list = ['']
        else:
            self.viewpoints_list = viewpoints

        self.display_dict = {}
        for viewpoint in self.viewpoints_list:
            self.create_display(viewpoint_name=viewpoint)

        self.render(active=render)

        self.saved_key_frame = None

    def create_display(self, viewpoint_name: str):
        """To create a display for a viewpoint

        Args:
            viewpoint_name (str): Name of the viewpoint
        """
        disp_name = f'Display_{viewpoint_name}'
        display = Vortex.VxExtensionFactory.create(Vortex.DisplayICD.kExtensionFactoryKey)
        display.getInput(Vortex.DisplayICD.kPlacementMode).setValue('Windowed')
        display.setName(disp_name)
        display.getInput(Vortex.DisplayICD.kPlacement).setValue(Vortex.VxVector4(50, 50, 1280, 720))

        display.getInput(Vortex.DisplayICD.kViewpointName).setValue(viewpoint_name)

        self.display_dict[disp_name] = display

    def render(self, active=True, real_time=False):
        """To render all the displays if active is True. Otherwise, remove all displays.

        Calling this method doesn't step the simulation time.
        """

        changed_disp = False

        for display_name, display in self.display_dict.items():
            # Find current list of displays
            current_displays = self.app.findExtensionsByName(display_name)

            # If active, add a display and activate Vsync
            if active and len(current_displays) == 0:
                self.app.add(display)
                changed_disp = True

            # If not, remove the current display and deactivate Vsync
            elif not active:
                if len(current_displays) == 1:
                    self.app.remove(current_displays[0])
                    changed_disp = True

        if changed_disp:
            # VSync Mode
            if active:
                if real_time:
                    self.app.setSyncMode(Vortex.kSyncVSync)
                else:
                    self.app.setSyncMode(Vortex.kSyncNone)
            else:
                self.app.setSyncMode(Vortex.kSyncNone)

            self.app.pause(True)
            self.app.update()
            self.app.pause(False)

    """ Simulation """

    def step(self):
        """To step the simulation"""
        self.app.update()
        self.sim_time = self.app.getSimulationTime()

    def save_current_frame(self):
        """To save the current key frame"""
        self.set_app_mode(AppMode.SIMULATING)
        reset_frames_list_name = f'{self.application_name}_ResetFrameList'
        self.key_frame_list = (
            self.app.getContext().getKeyFrameManager().createKeyFrameList(reset_frames_list_name, False)
        )
        self.app.update()

        self.key_frame_list.saveKeyFrame()
        self._wait_for_n_key_frames(1)
        self.saved_key_frame = self.key_frame_list.getKeyFrames()[0]

    def reset_saved_frame(self):
        if self.saved_key_frame is None:
            raise RuntimeError('No saved frame. VortexInterface.save_current_frame my be called before this.')

        self.set_app_mode(AppMode.SIMULATING)

        # Load first key frame
        self.key_frame_list.restore(self.saved_key_frame)
        self.app.update()

    def _wait_for_n_key_frames(self, n_frames):
        """Wait until there are n_frames in self.key_frame_list

        Args:
            n_frames (int):
        """
        maxNbIter = 100
        nbIter = 0
        while len(self.key_frame_list.getKeyFrames()) != n_frames and nbIter < maxNbIter:
            if not self.app.update():
                break
            ++nbIter
