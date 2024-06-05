import pyvortex
from Vortex import *
import sys

# This is a lightweight python application akin to SimApp.exe
# It can by started from the Vortex Director by using python.exe
#
# It can by ran standalone provide the following command line arguments are given:
# --config <vxcFile>, The application setup file
# --confignode <nodename>, The application setup node to be applied to this application.
# --datapath, Path on disk to the data store. Setting it makes this node the Data Provider of the simulator
# --networkbroker, Address and port to use for communication with Vortex Network Broker.
# --simAppsCount <count>, Specifies the total number of simulator applications to expect in the simulator. This will force each simulator node to wait for all other nodes before starting any operation. 1 by default
# --simulationID, Identifies the network simulation to which belongs this simulator (from 1 to 65535, default is 257).
# --simulatorname, Name of the simulator.
#


def main():
    # Extract parameters from command line arguments
    parameters = InitializationParameters(sys.argv)

    # Initialize the VxApplication
    application = VxApplication()

    if application.initialize(parameters):
        # Make sure the application exits when the graphics window is closed.
        Window.exitApplicationWhenWindowCloses(application)

        application.run()
    else:
        print('Invalid Parameters, please see the log for details')


if __name__ == '__main__':
    main()
