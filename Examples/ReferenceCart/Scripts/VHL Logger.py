import importlib.util
from Vortex import *

def on_simulation_start(extension):

    # passing the file name and path as argument
    spec = importlib.util.spec_from_file_location(
        "vortex_logger", "C:/Users/henryh/Desktop/pyvortex/pyvortex/vortex_logger.py")

    # importing the module as foo
    vortex_logger = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(vortex_logger)

    try:
        print(extension.parameters.Output_File.value)
    except:
        print("cannot find output_file parameter")

    # INPUTS
    vortex_logger.CreateInput(extension, "Logging Active", Types.Type_Bool)

    # PARAMETERS
    vortex_logger.CreateParameter(extension, 'Output File', Types.Type_VxFilename)
    vortex_logger.CreateParameter(extension, "VHL Interface", Types.Type_ExtensionPtr) # VHL interface

    # Check whether VHL is feed into the VHL interface parameter field
    try:
        extension.vhl = VxVHLInterfaceInterface(extension.parameters.VHL_Interface.value)
    except:
        print("VHL Interface extension parameter is not set")
        return

    if not extension.vhl.valid():
        print("VHL Interface extension parameter is not valid")
        return

    # build list of field names and fields for quick access later
    extension.headers = []  # Name of output fields
    extension.fields = []   # Values of output fields

    # TODO: Can refactor the below part
    # TODO: After refactoring, write another version that allows user to specify the entry of a certain field
    # build headers in output file
    for field in extension.vhl.getOutputContainer():
        fieldName = field.getID().asString()
        extension.headers.append(fieldName)
        extension.fields.append(field)

    # build header, no space. Fields are separated by comma
    extension.headerLine = extension.fields[0].getID().asString()
    for field in extension.fields[1:]:  # All but first element
        fieldName = field.getID().asString()
        if type(field.value) is VxVector3:
            extension.headerLine += "," + fieldName + "_X," + fieldName + "_Y," + fieldName + "_Z"
        elif type(field.value) is Matrix44: # I think matrix are default 4x4 in Vortex
            # Print the matrix row by row
            extension.headerLine += "," + fieldName + "[0][0]," + fieldName + "[0][1]," + fieldName + "[0][2]," + fieldName + "[0][3]"
            extension.headerLine += "," + fieldName + "[1][0]," + fieldName + "[1][1]," + fieldName + "[1][2]," + fieldName + "[1][3]"
            extension.headerLine += "," + fieldName + "[2][0]," + fieldName + "[2][1]," + fieldName + "[2][2]," + fieldName + "[2][3]"
            extension.headerLine += "," + fieldName + "[3][0]," + fieldName + "[3][1]," + fieldName + "[3][2]," + fieldName + "[3][3]"
        else:
            extension.headerLine += "," + fieldName

    # replace all spaces by '_' in header line
    extension.headerLine = extension.headerLine.replace(" ", "_")


def on_simulation_stop(extension):
    if hasattr(extension, "OutputFile"):    # Close output file
        extension.OutputFile.close()
        del extension.OutputFile


def pre_step(extension):
    pass

def post_step(extension):
    """Open or creates an output file"""
    # TODO: Modify script so the user can also supply the path to the output file in the script rather than in the editor
    # Need to think how we can refactor this... the parameters is dependent on how we name the parameters when creating it
    # i.e. if we create the parameter Output_File, then we reference that parameter with extension.parameters.Output_File
    if hasattr(extension, "OutputFile") == False:
        # Creates the output file and it requires the user to specify the name and path of the output file
        # so the Python script can create the output file and dump the results into it for the user
        # If the user does not provide a path to the output file, then simply return an error message
        # telling the user to provide one
        if not extension.parameters.Output_File.value:
             print("Please set the name of your output file and the path to the output file")
             return

        # Proceed to creating that file
        extension.OutputFile = open(extension.parameters.Output_File.value, 'w')

        # Write the headers to the output file
        extension.OutputFile.write(extension.headerLine + '\n')

    """Saves the data we are logging to the output file"""
    if hasattr(extension, "OutputFile"):
        for f in extension.fields: # all but last element
            if type(f.value) is VxVector3:
                extension.OutputFile.write("{:f}, ".format(f.value.x))
                extension.OutputFile.write("{:f}, ".format(f.value.y))
                extension.OutputFile.write("{:f}, ".format(f.value.z))
            elif type(f.value) is Matrix44:
                # Write the matrix data row by row. I think matrix you can query from the editor are default 4x4,
                # i.e. the transformation matrix
                for i in range(4):
                    for j in range(4):
                        extension.OutputFile.write("{:f}, ".format(f.value[i][j]))
            else:
                extension.OutputFile.write("{:f}, ".format(f.value))

        # Write a new line
        extension.OutputFile.write("\n")