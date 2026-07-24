import bpy
import math
from operator import itemgetter

decimal_places = 5

def rnd(val):
    return round(val, decimal_places)
    
def f2s(value):
    return ('%.6f' % value).rstrip('0').rstrip('.')
    
def calc_bounds_radius(min_ext, max_ext):
    x = (max_ext[0] - min_ext[0])/2
    y = (max_ext[1] - min_ext[1])/2
    z = (max_ext[2] - min_ext[2])/2
    return math.sqrt(math.pow(x, 2) + math.pow(y, 2) + math.pow(z, 2))
    
def calc_extents(vertices):
    max_extents = tuple(max(vertices,key=itemgetter(i))[i] for i in range(3))
    min_extents = tuple(min(vertices,key=itemgetter(i))[i] for i in range(3))
    
    return min_extents, max_extents

def iter_action_fcurves(anim_data):
    if not anim_data or not anim_data.action:
        return

    action = anim_data.action
    if hasattr(action, "fcurves"):
        yield from action.fcurves
        return

    action_slot = getattr(anim_data, "action_slot", None)
    for layer in getattr(action, "layers", []):
        for strip in getattr(layer, "strips", []):
            for channelbag in getattr(strip, "channelbags", []):
                if action_slot is not None and getattr(channelbag, "slot", None) != action_slot:
                    continue
                yield from getattr(channelbag, "fcurves", [])

def find_action_fcurve(anim_data, data_path, index=0):
    for curve in iter_action_fcurves(anim_data):
        if curve.data_path == data_path and curve.array_index == index:
            return curve
    return None
	
def get_curve(obj, data_paths):
    if obj.animation_data and obj.animation_data.action:
        for path in data_paths:
            curve = find_action_fcurve(obj.animation_data, path)
            if curve is not None:
                return curve
    return None
    
def get_curves(obj, data_path, indices):
    curves = {}
    if obj.animation_data and obj.animation_data.action:
        for index in indices:
            curve = find_action_fcurve(obj.animation_data, data_path, index=index)
            if curve is not None:
                curves[(data_path.split('.')[-1], index)] = curve # For now, i'm just interested in the type, not the whole data path. Hence, the split returns the name after the last dot. 
    if len(curves):
        return curves
    return None
