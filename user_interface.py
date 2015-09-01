import bpy
from bpy.props import IntProperty, BoolProperty, FloatProperty, EnumProperty, PointerProperty
from bpy.types import Menu, Panel, AddonPreferences, PropertyGroup
from rna_prop_ui import PropertyPanel

class UI_Visibility_Presets(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):

            layout.prop(item, "name", text="", emboss=False)

class UI_Visibility_List_Prefs(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):

        if self.layout_type in {'DEFAULT', 'COMPACT'}:

            layout.prop(item, "name", text="", emboss=False)
            layout.separator()

        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text="", icon_value=icon)

class UI_Visibility_List_3DView(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):

        tempIcon = ""

        tempName = "SOLID"

        if int(item.visibility) is 2:
            tempName = "SOLID"
        elif int(item.visibility) is 3:
            tempName = "GRID"
        elif int(item.visibility) is 4:
            tempName = "LATTICE_DATA"
        elif int(item.visibility) is 5:
            tempName = "WIRE"
        elif int(item.visibility) is 6:
            tempName = "POTATO"
        elif int(item.visibility) is 7:
            tempName = "X"

        if self.layout_type in {'DEFAULT', 'COMPACT'}:

            layout.prop(item, "name", text="", emboss=False)
            layout.prop(item, "visibility", text="", icon=tempName, icon_only=True)

            if item.selectable is True:
                layout.prop(item, "selectable", text="", icon='RESTRICT_SELECT_OFF', emboss=False)

            else:
                layout.prop(item, "selectable", text="", icon='RESTRICT_SELECT_ON', emboss=False)
            layout.separator()

        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text="", icon_value=icon)



class BL_Export(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Blinkey"

    def draw(self, context):
        layout = self.layout

        user_preferences = context.user_preferences
        addon_prefs = user_preferences.addons["Blinkey"].preferences
        ui = context.scene.BLUI

        row = layout.row(align=True)
        row.alignment = 'EXPAND'
        row.prop(ui, "preset_enum", text="")

        layout.separator()

        if len(addon_prefs.presets) > 0 and addon_prefs.presets_index < len(addon_prefs.presets):

            currentPreset = addon_prefs.presets[int(ui.preset_enum)]

            row_categories = layout.row(align=True)
            row_categories.template_list("UI_Visibility_List_3DView", "default", currentPreset, "categories", currentPreset, "categories_index", rows=3, maxrows=6)
            row_categories.separator()

            layout.separator()
