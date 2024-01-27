from VxSim import *

""" Script extension to log all data in a VHL.
Simulation Time field goes first, irrespective of the order of fields for ease of plotting
Assumes all fields are numbers, or at least can be printed as floats.
A header line is written first based on the set of fields (with spaces converted to _)
A comment line (starting with #) can be added after the header line
(gnuplot ignores lines starting with #)
"""
def on_add_to_universe(self, universe):

    CreateInput(self, 'Logging Active', Types.Type_Bool) # Logging_Active
    CreateInput(self, 'Comment', Types.Type_String) # Comment

    # PARAMETERS
    CreateParameter(self, 'Save Output', Types.Type_Bool) #Save_Output
    CreateParameter(self, 'Output File', Types.Type_VxFilename) #Output_File
    CreateParameter(self, 'VHL Interface', Types.Type_ExtensionPtr) #VHL_Interface
    
    self.inputs.Comment.setDescription('Optional comment to be prefixed by # in output file')
    
    #try:
    self.vhl = VxSim.VxVHLInterfaceInterface(self.parameters.VHL_Interface.value)
    if not self.vhl or not self.vhl.valid():
        print "VHL Interface extension parameter is not set or a VHL interface"
        return
        
    # build list of field names and fields themselves for easy and quick access later
    self.headers = []
    self.fields = []
    for field in self.vhl.getOutputContainer():
        fieldname = field.getID().asString()
        if fieldname == "Simulation Time":  #if there, ensure that "Simulation Time" goes first
            self.headers.insert(0, "Time")
            self.fields.insert(0, field)
        else:
            self.headers.append(fieldname)
            self.fields.append(field)

    #build header, no spaces
    self.header_line = self.fields[0].getID().asString()
    for field in self.fields[1:]:  # all but first element of list
        fieldname = field.getID().asString() 
        if type(field.value) is VxSim.VxVector3:
            self.header_line += ","+fieldname+"_X,"+fieldname+"_Y,"+fieldname+"_Z"
        else:
            self.header_line += ","+fieldname
      
    # replace all spaces by '_' in header line
    self.header_line = self.header_line.replace(" ", "_") 

def on_remove_from_universe(self, universe):
    if hasattr(self, 'OutputFile'): #Close output file
        self.OutputFile.close()
        del self.OutputFile

def pre_step(self):
    pass
    
def post_step(self):
    """ Open output file """
    if hasattr(self, 'OutputFile') == False and self.parameters.Save_Output.value and self.parameters.Output_File.value:
        print self.parameters.Output_File.value
        self.OutputFile = open(self.parameters.Output_File.value, 'w')
        if len(self.inputs.Comment.value) > 0:
            self.OutputFile.write('# '+self.inputs.Comment.value+'\n')
        self.OutputFile.write(self.header_line+'\n')  #Column labels
        #print "Writing header", self.header_line
             
    """ Write data to output CSV file """
    if self.inputs.Logging_Active.value:
        if hasattr(self, 'OutputFile'):
            for f in self.fields[:-1]: # all but last element
                if type(f.value) is VxSim.VxVector3:
                    self.OutputFile.write("{:f}, ".format(f.value.x))
                    self.OutputFile.write("{:f}, ".format(f.value.y))
                    self.OutputFile.write("{:f}, ".format(f.value.z))
                else:
                    self.OutputFile.write("{:f}, ".format(f.value))
            self.OutputFile.write("{:f}\n".format(self.fields[-1].value)) # last element
        
# USER DEFINED FUNCTIONS

def CreateInput(extension, name, type):
    input = extension.getInput(name) 
    if input is None:
        input = extension.addInput(name, type)
    
def CreateOutput(extension, name, type):
    output = extension.getOutput(name)
    if output is None:
        output = extension.addOutput(name, type)

def CreateParameter(extension, name, type, default = None):
    param = extension.getParameter(name)
    if param is None:
       param = extension.addParameter(name, type)  
       if default is not None: 
           param.value = default       