import bpy, bmesh
from bpy.types import Operator
from .definitions import SelectObject, FocusObject, ActivateObject, CheckSuffix
from mathutils import Vector

class BL_Add_Preset(Operator):
    """Creates a path from the menu"""

    bl_idname = "scene.bl_addpreset"
    bl_label = "Add"

    def execute(self, context):
        print(self)

        user_preferences = context.user_preferences
        addon_prefs = user_preferences.addons["Blinkey"].preferences

        new = addon_prefs.presets.add()
        new.name = "Preset " + str(len(addon_prefs.presets))

        return {'FINISHED'}

class BL_Delete_Preset(Operator):
    """Creates a path from the menu"""

    bl_idname = "scene.bl_delpreset"
    bl_label = "Add"

    def execute(self, context):
        print(self)

        user_preferences = context.user_preferences
        addon_prefs = user_preferences.addons["Blinkey"].preferences

        addon_prefs.presets.remove(addon_prefs.presets_index)

        return {'FINISHED'}

class BL_Add_Category(Operator):
    """Creates a path from the menu"""

    bl_idname = "scene.bl_addcategory"
    bl_label = "Add"

    def execute(self, context):
        print(self)

        user_preferences = context.user_preferences
        addon_prefs = user_preferences.addons["Blinkey"].preferences
        preset = addon_prefs.presets[addon_prefs.presets_index]

        new = preset.categories.add()
        new.name = "Preset " + str(len(preset.categories))

        return {'FINISHED'}

class BL_Delete_Category(Operator):
    """Creates a path from the menu"""

    bl_idname = "scene.bl_delcategory"
    bl_label = "Add"

    def execute(self, context):
        print(self)

        user_preferences = context.user_preferences
        addon_prefs = user_preferences.addons["Blinkey"].preferences
        preset = addon_prefs.presets[addon_prefs.presets_index]

        preset.categories.remove(preset.categories_index)

        return {'FINISHED'}
