import os
import sys

vortex_installation_path = os.getenv("VORTEX_PATH")
if vortex_installation_path is None:
    raise EnvironmentError(
        "Variable VORTEX_PATH not found in environment variables. Check the installation instructions."
    )
sys.path.append(vortex_installation_path)
sys.path.append(vortex_installation_path + "/bin")
