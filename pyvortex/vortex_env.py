"""
To interface with Vortex.

Two main ways to exchange data with the application: its API or the dll.
The API is easier but only works w/ python 3.8.
I dont know where the dll's doc can be found
"""

from pathlib import Path

import Vortex  # noqa
import vxatp3  # noqa

from pyvortex.vortex_classes import AppMode


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
        self.application_name: str = 'Vortex App'

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

    def __del__(self):
        # Destroy the VxApplication when done
        self.app = None

    def _create_application(self):
        """To create the Vortex application"""
        setup_file_str = str(self._setup_file_path)
        self.app = vxatp3.VxATPConfig.createApplication(self, self.application_name, setup_file_str)
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
        self.interface.getInputContainer()[field_name].value = field_value

    def get_input(self, field_name: str):
        val = self.interface.getInputContainer()[field_name].value

        return val

    def get_output(self, field_name: str):
        try:
            val = self.interface.getOutputContainer()[field_name].value

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

    def render(self, active=True):
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
                self.app.setSyncMode(Vortex.kSyncNone)

        if changed_disp:
            # self.set_app_mode(AppMode.EDITING)
            self.app.pause(True)
            self.app.update()
            self.app.pause(False)

            # self.step()

            # self.set_app_mode(AppMode.SIMULATING)
            # self.app.update()

            # self.app.setApplicationMode(AppMode.EDITING.value)
            # self.app.setApplicationMode(AppMode.SIMULATING.value)

    """ Simulation """

    def step(self):
        """To step the simulation"""
        self.app.update()
        self.sim_time = self.app.getSimulationTime()

    def save_current_frame(self):
        """To save the current key frame"""
        self.set_app_mode(AppMode.SIMULATING)
        self.key_frame_list = self.app.getContext().getKeyFrameManager().createKeyFrameList('ResetFrameList', False)
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
