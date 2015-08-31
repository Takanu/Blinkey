#This states the metadata for the plugin
bl_info = {
    "name": "Blinkey",
    "author": "Crocadillian/Takanu @ Polarised Games",
    "version": (0,1),
    "blender": (2, 7, 6),
    "api": 39347,
    "location": "3D View > Object Mode > Tools > Blinky",
    "description": "Category-based Visibility Shortcuts",
    "warning": "Beta",
    "tracker_url": "",
    "category": "Scene"
}

# Start importing all the addon files
# The init file just gets things started, no code needs to be placed here.
if "bpy" in locals():
    import imp
    print(">>>>>>>>>>> Reloading Plugin", __name__, "<<<<<<<<<<<<")
    if "definitions" in locals():
        imp.reload(definitions)
    if "properties" in locals():
        imp.reload(properties)
    if "user_interface" in locals():
        imp.reload(user_interface)
    if "operators" in locals():
        imp.reload(operators)
    if "update" in locals():
        imp.reload(update)


print(">>>>>>>>>>> Beginning Import", __name__, "<<<<<<<<<<<<")

import bpy
from . import definitions
from . import properties
from . import user_interface
from . import operators
from . import update
from bpy.props import IntProperty, BoolProperty, StringProperty, PointerProperty, CollectionProperty, EnumProperty
from bpy.types import AddonPreferences, PropertyGroup
from .update import Update_VisibilityCategory

print("End of import")

class BL_VisibilityCategory(PropertyGroup):

    name = StringProperty(
        name="Category Name",
        description="The name of the selected pass."
    )

    name_filter = StringProperty(
        name="Name Filter",
        description="A piece of text used to filter objects for the visibility category."
    )

    name_filter_type = EnumProperty(
        name = "Name Filter Type",
        description = "Decides how the name filter is applied.",
        items=(
        ('1', 'Suffix', ''),
        ('2', 'Prefix', ''),
        ('3', 'Entire Name', ''),
        ),)

    visibility = EnumProperty(
        name="Visibility",
        items=(
            ('1', 'Solid', 'Shades the category using a standard solid appearance.'),
            ('3', 'Box Bounds', 'Changes the display to box bounds for all objects in this category'),
            ('4', 'Wireframe', 'Changes the display to wireframe for all objects in this category'),
            ('5', 'Wire', 'Adds a wire display for all objects in this category'),
            ('6', 'Texture', 'Adds a texture display for all the objects in this category'),
            ('7', 'Hide', 'Changes the display to hide all objects in this category')
            ),
        default='1',
        update=Update_VisibilityCategory
    )

    object_type = EnumProperty(
        name="Object Type",
        items=(
            ('1', 'All', 'Applies to all object types.'),
            ('2', 'Mesh', 'Applies to mesh object types only.'),
            ('3', 'Curve', 'Applies to curve object types only.'),
            ('4', 'Surface', 'Applies to surface object types only.'),
            ('5', 'Meta', 'Applies to meta object types only.'),
            ('6', 'Font', 'Applies to font object types only.'),
            ('7', 'Armature', 'Applies to armature object types only.'),
            ('8', 'Lattice', 'Applies to lattice object types only.'),
            ('9', 'Empty', 'Applies to empty object types only.'),
            ('10', 'Camera', 'Applies to camera object types only.'),
            ('11', 'Lamp', 'Applies to lamp object types only.'),
            ('12', 'Speaker', 'Applies to speaker object types only.')
            ),
        default='1'
    )

class BL_VisibilityPreset(PropertyGroup):
    name = StringProperty(
        name = "Default Name",
        description="The name of the visibility preset",
        default=""
    )

    categories = CollectionProperty(type=BL_VisibilityCategory)
    categories_index = IntProperty(default=0)

class BlinkeyAddonPreferences(AddonPreferences):
    bl_idname = __name__

    presets = CollectionProperty(type=BL_VisibilityPreset)
    presets_index = IntProperty(default=0)

    def draw(self, context):
        layout = self.layout

        user_preferences = context.user_preferences
        addon_prefs = user_preferences.addons[__name__].preferences
        ui = context.scene.BLUI

        row = layout.row(align=True)
        row.alignment = 'EXPAND'
        row.template_list("UI_Visibility_Presets", "default", addon_prefs, "presets", addon_prefs, "presets_index", rows=3, maxrows=6)

        row.separator()

        col = row.column(align=True)
        col.operator("scene.bl_addpreset", text="", icon="ZOOMIN")
        col.operator("scene.bl_delpreset", text="", icon="X")

        layout.separator()

        if len(addon_prefs.presets) > 0 and addon_prefs.presets_index < len(addon_prefs.presets):

            currentPreset = addon_prefs.presets[addon_prefs.presets_index]

            row_categories = layout.row(align=True)
            row_categories.template_list("UI_Visibility_List_Prefs", "default", currentPreset, "categories", currentPreset, "categories_index", rows=3, maxrows=6)
            row_categories.separator()

            col_categories = row_categories.column(align=True)
            col_categories.operator("scene.bl_addcategory", text="", icon="ZOOMIN")
            col_categories.operator("scene.bl_delcategory", text="", icon="X")

            layout.separator()

            if len(currentPreset.categories) > 0 and currentPreset.categories_index < len(currentPreset.categories):

                currentCategory = currentPreset.categories[currentPreset.categories_index]

                if ui.name_dropdown is False:
                    row_names = layout.row(align=True)
                    row_names.prop(ui, "name_dropdown", icon="TRIA_RIGHT")
                    row_names.label(text="Visibility Filters")

                else:
                    row_names = layout.row(align=True)
                    row_names.prop(ui, "name_dropdown", icon="TRIA_DOWN")
                    row_names.label(text="Visibility Filters")

                    col_names = layout.column(align=True)
                    col_names.prop(currentCategory, "name_filter")
                    col_names.prop(currentCategory, "name_filter_type")
                    col_names.prop(currentCategory, "object_type")


def register():
    bpy.utils.register_class(BL_VisibilityCategory)
    bpy.utils.register_class(BL_VisibilityPreset)
    bpy.utils.register_module(__name__)


def unregister():
    bpy.utils.unregister_class(BL_VisibilityPreset)
    bpy.utils.unregister_class(BL_VisibilityCategory)
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()
