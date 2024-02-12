from Vortex import *

def get_mechanism_from_scene(scene_to_look_into, mechanism_to_look_for):
    for mechanism in scene_to_look_into.getMechanisms():
        if mechanism_to_look_for == mechanism.getExtension().getName():
            return mechanism

def get_assembly_from_mechanism(mechanism_to_look_into, assembly_to_look_for):
    for assembly in mechanism_to_look_into.getAssemblies():
        if assembly_to_look_for == assembly.getExtension().getName():
            return assembly

def get_part_from_assembly(assembly_to_look_into, part_to_look_for):
    for part in assembly_to_look_into.getParts():
        if part_to_look_for == part.getExtension().getName():
            return part

def get_constraint_from_assembly(assembly_to_look_into, constraint_to_look_for):
    for constraint in assembly_to_look_into.getConstraints():
        if constraint_to_look_for == constraint.getExtension().getName():
            return constraint
