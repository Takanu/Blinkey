import bpy
from bpy.props import IntProperty, BoolProperty, FloatProperty, EnumProperty, PointerProperty, StringProperty, CollectionProperty
from bpy.types import PropertyGroup

def GetPresets(scene, context):

    items = []

    user_preferences = context.user_preferences
    addon_prefs = user_preferences.addons["Blinkey"].preferences

    u = 1

    for i,x in enumerate(addon_prefs.presets):

        items.append((str(i), x.name, x.name, i))

    return items

class BL_UI_Preferences(PropertyGroup):

    preset_enum = EnumProperty(
        name = "Presets",
        description = "List of available visibility presets.",
        items = GetPresets
    )

    name_dropdown = BoolProperty(
        name = "",
        description = "",
        default = False)




bpy.utils.register_class(BL_UI_Preferences)
bpy.types.Scene.BLUI = PointerProperty(type=BL_UI_Preferences)
