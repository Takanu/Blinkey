import bpy, bmesh, time
from math import *

from .definitions import GenerateObjectShading, CheckSuffix

def Update_VisibilityCategory(self, context):

    #Preserve scene selection


    #Preserve edit state
    

    scn = context.scene
    user_preferences = context.user_preferences
    addon_prefs = user_preferences.addons["Blinkey"].preferences

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
