import bpy, bmesh, time
from math import *

from .definitions import FilterObjects, FocusObject, SelectObject, GenerateObjectShading, CheckSuffix

def Update_VisibilityCategory(self, context):

    scn = context.scene
    user_preferences = context.user_preferences
    addon_prefs = user_preferences.addons["Blinkey"].preferences

    # Keep a record of the selected and active objects to restore later
    active = None
    selected = []

    for sel in context.selected_objects:
        if sel.name != context.active_object.name:
            selected.append(sel)
    active = context.active_object

    #Preserve edit state
    mode = bpy.context.mode
    bpy.ops.object.mode_set(mode='OBJECT')

    #Now filter through and shade the objects
    finalList = []
    finalList = FilterObjects(self, context)

    for finalItem in finalList:
        print("Processing shading....", finalItem.name)
        GenerateObjectShading(finalItem, self.visibility)

    if self.selectable is False:
        for finalItem in finalList:
            finalItem.hide_select = True

    # Re-select the objects previously selected
    if active is not None:
        FocusObject(active)

    for sel in selected:
        SelectObject(sel)

    #Restore edit state
    if mode == 'EDIT_MESH':
        mode = 'EDIT'

    bpy.ops.object.mode_set(mode=mode)


def Update_Selectable(self, context):

    scn = context.scene
    user_preferences = context.user_preferences
    addon_prefs = user_preferences.addons["Blinkey"].preferences

    # Keep a record of the selected and active objects to restore later
    active = None
    selected = []

    for sel in context.selected_objects:
        if sel.name != context.active_object.name:
            selected.append(sel)
    active = context.active_object

    #Preserve edit state
    mode = bpy.context.mode
    bpy.ops.object.mode_set(mode='OBJECT')

    #Now filter through and shade the objects
    finalList = []
    finalList = FilterObjects(self, context)

    isSelectable = True

    if self.selectable is True:
        isSelectable = False

    for finalItem in finalList:
        print("Editing selection....", finalItem.name)
        finalItem.hide_select = isSelectable

    # Re-select the objects previously selected
    if active is not None:
        FocusObject(active)

    for sel in selected:
        SelectObject(sel)

    #Restore edit state
    if mode == 'EDIT_MESH':
        mode = 'EDIT'

    bpy.ops.object.mode_set(mode=mode)
