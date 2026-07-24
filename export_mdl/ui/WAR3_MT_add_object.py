from bpy.types import Menu

from ..operators.WAR3_OT_add_anim_sequence import WAR3_OT_add_anim_sequence
from ..operators.WAR3_OT_create_collision_shape import WAR3_OT_create_collision_shape
from ..operators.WAR3_OT_create_eventobject import WAR3_OT_create_eventobject


class WAR3_MT_add_object(Menu):
    """Menu class for adding Warcraft MDL objects to the scene."""

    bl_idname = "WAR3_MT_add_object"
    bl_label = "Add MDL object"

    def draw(self, context):
        """Draw the menu options for MDL objects."""
        layout = self.layout

        layout.operator(WAR3_OT_create_collision_shape.bl_idname)
        layout.operator(WAR3_OT_create_eventobject.bl_idname)
        layout.operator(WAR3_OT_add_anim_sequence.bl_idname)


def menu_func(self, context):
    """Append the MDL object menu to Blender's View3D Add menu."""
    self.layout.menu(WAR3_MT_add_object.bl_idname, text="MDL data")
