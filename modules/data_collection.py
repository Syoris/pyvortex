from Vortex import *
from VortexAdvancedDynamics import *

def getTimings(universe) :
    timings = universe.getUniverseTimings()
    return timings.solveDynamics