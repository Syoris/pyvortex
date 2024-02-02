import Vortex


def on_simulation_start(extension):

    # Create fields
    extension.createInput("Material", Vortex.Types.Type_String)
    extension.createParameter("Collision Geometry", Vortex.Types.Type_CollisionGeometry)
    
    material = Vortex.VxMaterial()
    material.setName(extension.inputs.Material.value)
    extension.parameters.Collision_Geometry.value.parameterMaterial.value = material