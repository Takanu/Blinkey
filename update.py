import bpy, bmesh, time
from math import *

from .definitions import FocusObject, SelectObject, GenerateObjectShading, CheckSuffix

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

    categoryName = self.name
    shading = self.visibility

    # Figure out which category the request came from
    preset = addon_prefs.presets[addon_prefs.presets_index]
    category = None

    for item in preset.categories:
        if item.name == categoryName:
            category = item

    nameFilterList = []
    typeFilterList = []

    print(">>> Updating", self.name, "Category <<<")
    print(">>> Checking Name Filter <<<")

    # Now collect objects based on the filtering categories
    for object in bpy.data.objects:
        print("Found object...", object.name)

        if category.name_filter != "":
            if category.name_filter_type is '1':
                if CheckSuffix(object.name, category.name_filter) is True:
                    print("Object matches name filter")
                    nameFilterList.append(object)

            elif category.name_filter_type is '2':
                if object.name.find(category.name_filter) == 0:
                    print("Object matches name filter")
                    nameFilterList.append(object)

            elif category.name_filter_type is '3':
                if object.name.find(category.name_filter) != -1:
                    print("Object matches name filter")
                    nameFilterList.append(object)

        else:
            print("Object matches name filter")
            nameFilterList.append(object)

    print("Current object list...", len(nameFilterList))
    print(">>> Checking Type Filter <<<")

    if category.object_type is '2':
        for object in nameFilterList:
            print("Checking object...", object.name)
            if object.type == 'MESH':
                print("Object matches type filter")
                typeFilterList.append(object)

    elif category.object_type is '3':
        for object in nameFilterList:
            print("Checking object...", object.name)
            if object.type == 'ARMATURE':
                print("Object matches type filter")
                typeFilterList.append(object)

    else:
        for object in nameFilterList:
            print("Object matches type filter")
            typeFilterList.append(object)



    for finalItem in typeFilterList:
        print("Processing shading....", finalItem.name)
        GenerateObjectShading(finalItem, shading)

    # Re-select the objects previously selected
    if active is not None:
        FocusObject(active)

    for sel in selected:
        SelectObject(sel)

    #Restore edit state
    if mode == 'EDIT_MESH':
        mode = 'EDIT'
        
    bpy.ops.object.mode_set(mode=mode)
