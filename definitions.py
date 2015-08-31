import bpy, bmesh, time
from math import *
from mathutils import Vector

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

def CheckSuffix(string, suffix):

    strLength = len(string)
    suffixLength = len(suffix)
    diff = strLength - suffixLength
    index = string.rfind(suffix)

    if index == diff:
        return True

    else:
        return False
