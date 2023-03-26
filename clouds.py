bl_info = {
    "name": "Create clouds",
    "author": "icantuga",
    "version": (1, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Add > Mesh > Nubes",
    "description": "This pluguin create a volumetric cloud",
    "category": "Add Mesh",
}

import bpy

class CreateClouds(bpy.types.Operator):
    """Create clouds"""
    bl_idname = "mesh.create_clouds"
    bl_label = "Create Clouds"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=2)
        bpy.ops.object.shade_smooth()
        bpy.context.active_object.name = "Nubes"
        bpy.context.active_object.data.materials.append(bpy.data.materials.get("Material Nubes"))
        displace_mod = bpy.context.object.modifiers.new(name="Displace", type='DISPLACE')
        displace_mod.strength = 0.5
        displace_mod.mid_level = 0.5
        displace_mod.texture_coords = 'UV'
        clouds_tex = bpy.data.textures.new('Clouds', type='CLOUDS')
        displace_mod.texture = clouds_tex
        displace_mod = bpy.context.object.modifiers.new(name="Displace2", type='DISPLACE')
        displace_mod.texture = clouds_tex
        displace_mod.texture.noise_depth = 5
        displace_mod.strength = 0.5
        displace_mod.texture.cloud_type = 'GRAYSCALE'
        displace_mod.texture.color_ramp.elements.new(0.25).position = 0.0
        displace_mod.texture.color_ramp.elements.new(0.75).position = 1.0
        displace_mod.texture.contrast = 1.2
        bpy.ops.object.modifier_apply(modifier="Displace")
        bpy.context.object.active_material.blend_method = 'BLEND'
        bpy.context.object.active_material.use_backface_culling = True
        return {'FINISHED'}

def menu_func(self, context):
    self.layout.operator(CreateClouds.bl_idname, icon='MESH_UVSPHERE')

def register():
    bpy.utils.register_class(CreateClouds)
    bpy.types.VIEW3D_MT_mesh_add.append(menu_func)

def unregister():
    bpy.utils.unregister_class(CreateClouds)
    bpy.types.VIEW3D_MT_mesh_add.remove(menu_func)

if __name__ == "__main__":
    register()
