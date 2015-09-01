import bpy, bmesh, time
from math import *
from mathutils import Vector

def FilterObjects(filterEntry, context):

    nameFilterList = []
    typeFilterList = []

    scn = context.scene
    user_preferences = context.user_preferences
    addon_prefs = user_preferences.addons["Blinkey"].preferences

    # Figure out which category the request came from
    preset = addon_prefs.presets[addon_prefs.presets_index]
    category = None

    categoryName = filterEntry.name
    shading = filterEntry.visibility

    for item in preset.categories:
        if item.name == categoryName:
            category = item

    print(">>> Updating", filterEntry.name, "Category <<<")
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
    print("Checking Type Filter.....", category.object_type)

    typeFilter = 'NONE'

    if category.object_type == '1':
        typeFilter = 'NONE'
    elif category.object_type == '2':
        typeFilter = 'MESH'
    elif category.object_type == '3':
        typeFilter = 'CURVE'
    elif category.object_type == '4':
        typeFilter = 'SURFACE'
    elif category.object_type == '5':
        typeFilter = 'META'
    elif category.object_type == '6':
        typeFilter = 'FONT'
    elif category.object_type == '7':
        typeFilter = 'ARMATURE'
    elif category.object_type == '8':
        typeFilter = 'LATTICE'
    elif category.object_type == '9':
        typeFilter = 'EMPTY'
    elif category.object_type == '10':
        typeFilter = 'CAMERA'
    elif category.object_type == '11':
        typeFilter = 'LAMP'
    elif category.object_type == '12':
        typeFilter = 'SPEAKER'

    print("Type Filter Found...", typeFilter)

    if typeFilter == 'NONE':
        for object in nameFilterList:
            print("Checking object...", object.name)
            print("Object matches type filter")
            typeFilterList.append(object)

    else:
        for object in nameFilterList:
            print("Checking object...", object.name)
            if object.type == typeFilter:
                print("Object matches type filter")
                typeFilterList.append(object)

    return typeFilterList

def FocusObject(target):

    # If the target isnt visible, MAKE IT FUCKING VISIBLE.
    if target.hide is True:
        target.hide = False

    if target.hide_select is True:
        target.hide_select = False

    #### Select and make target active
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.scene.objects.active = bpy.data.objects[target.name]
    bpy.ops.object.select_pattern(pattern=target.name)

def SelectObject(target):

    # If the target isnt visible, MAKE IT FUCKING VISIBLE.
    if target.hide is True:
        target.hide = False

    if target.hide_select is True:
        target.hide_select = False

    target.select = True

def ActivateObject(target):

    # If the target isnt visible, MAKE IT FUCKING VISIBLE.
    if target.hide is True:
        target.hide = False

    if target.hide_select is True:
        target.hide_select = False

    bpy.context.scene.objects.active = bpy.data.objects[target.name]


def GenerateObjectShading(target, visibilityEnum):

    #Focus the object to ensure the values can be accessed at this stage if its hidden or unselectable.
    FocusObject(target)

    if visibilityEnum is '1':
        ShadeNormal(target)
        return None
    elif visibilityEnum is '2':
        ShadeNormal(target)
        return None
    elif visibilityEnum is '3':
        ShadeBoxBounds(target)
        return None
    elif visibilityEnum is '4':
        ShadeWireframe(target)
        return None
    elif visibilityEnum is '5':
        ShadeWire(target)
        return None
    elif visibilityEnum is '6':
        ShadeTexture(target)
        return None
    elif visibilityEnum is '7':
        ShadeHide(target)
        return None


#The top one kind of acts like a shading reset, the others perform more nuanced shading.
def ShadeNormal(target):
    #print("Shading Normal")
    FocusObject(target)
    target.draw_type = "TEXTURED"
    target.show_wire = False
    target.show_x_ray = False
    target.hide = False
    bpy.types.SpaceView3D.view_selected = "SOLID"

def ShadeBoxBounds(target):
    #print("Shading Box Bounds")
    ShadeNormal(target)
    target.draw_type = "BOUNDS"

def ShadeWireframe(target):
    #print("Shading Wireframe")
    ShadeNormal(target)
    target.draw_type = "WIRE"

def ShadeWire(target):
    #print("Shading Wire")
    ShadeNormal(target)
    target.show_wire = True

def ShadeTexture(target):
    #print("Shading Texture")
    ShadeNormal(target)
    bpy.types.SpaceView3D.view_selected = "TEXTURED"

def ShadeHide(target):
    #print("Hiding Object")
    ShadeNormal(target)
    target.hide = True

def ShadeHide(target):
    #print("Hiding Object")
    ShadeNormal(target)
    target.hide = True

def CheckSuffix(string, suffix):

    strLength = len(string)
    suffixLength = len(suffix)
    diff = strLength - suffixLength
    index = string.rfind(suffix)

    if index == diff:
        return True

    else:
        return False
