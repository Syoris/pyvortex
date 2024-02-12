from Vortex import *

def CreateInput(extension, name, type):
    input = extension.getInput(name)
    if input is None:
        input = extension.addInput(name, type)

def CreateParameter(extension, name, type, default = None):
    param = extension.getParameter(name)
    if param is None:
        param = extension.addParameter(name, type)
        if default is not None:
            param.value = default

def CreateOutput(extension, name, type):
    output = extension.getOutput(name)
    if output is None:
        output = extension.addOutput(name, type)

