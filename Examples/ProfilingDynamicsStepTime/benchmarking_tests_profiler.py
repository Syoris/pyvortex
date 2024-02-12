import Vortex
import VortexAdvancedDynamics
import csv
import glob
import os
import numpy
import time


def on_simulation_start(extension):
    extension.logParts = []
    extension.outputs.areLogsDynamic.value = True

    # Get all logs in this mechanism
    mechanism = extension.inputs.logBundle.value
    allAssemblies = mechanism.getAssemblies()

    for assembly in allAssemblies:
        parts = assembly.getParts()
        if parts[0].getName() == 'Log':
            logParts.append(parts[0])


def pre_step(extension):
    pass

    if extension.outputs.areLogsDynamic.value != extension.inputs.dynamicLogs.value:
        if extension.inputs.dynamicLogs.value is True:
            for log in extension.logParts:
                print('setting control static')
                log.inputControlType = Vortex.Part.kControlDynamic
        else:
            for log in extension.logParts:
                print('setting control static')
                log.inputControlType = Vortex.Part.kControlStatic
        extension.outputs.areLogsDynamic = extension.inputs.dynamicLogs

numFrames = 1000
mechanisms = glob.glob("*.vxmechanism")
names = []
pulleys = []
avgTimes = []
sdTimes = []

application = Vortex.VxApplication()

for mechName in mechanisms:

    serializer = Vortex.ApplicationConfigSerializer()

    serializer.load('DynamicsOnly.vxc')
    config = serializer.getApplicationConfig()
    config.apply(application)

    fileManager = application.getSimulationFileManager()

    preName, ext = os.path.splitext(mechName)
    nameBits = preName.split('_')
    names.append(preName)
    pulleys.append(nameBits[-1])
    mechanism = Vortex.MechanismInterface(fileManager.loadObject(mechName))

    application.setApplicationMode(Vortex.kModeSimulating)
    time.sleep(1)

    dynamicsModule = VortexAdvancedDynamics.VxDynamicsModule.instance()
    universe = dynamicsModule.getUniverse()
    times = []
    if(mechanism.valid()):
        for i in range(numFrames):
            application.update()
            timings = universe.getUniverseTimings()
            times.append(timings.solveDynamics)
        avgTimes.append(numpy.mean(times))
        sdTimes.append(numpy.std(times))
        csvName = preName + '.csv'
        with open(csvName, 'w', newline='') as file:
            writer = csv.writer(file)
            for num in times:
                row = [num]
                writer.writerow(row)
            file.close()

    application.clean()
    time.sleep(1)

# Might also not be able to refactor it because the number of arrays we want to save depends on the user...
with open("allStats.csv", 'w', newline='') as file:
    writer = csv.writer(file)
    titles = ["Mechanism", "Number of Pulleys", "Average Solve Time", "SD of Solve Time"]
    writer.writerow(titles)
    for i in range(len(names)):
        row = [names[i], pulleys[i], avgTimes[i], sdTimes[i]]
        writer.writerow(row)
    file.close()


