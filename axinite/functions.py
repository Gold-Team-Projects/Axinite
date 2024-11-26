from astropy.coordinates import CartesianRepresentation
from astropy.units import Quantity
import astropy.units as u
import math
import numpy as np

def apply_to_vector(vector: CartesianRepresentation, function):
    return CartesianRepresentation([function(i) for i in vector.xyz])

def vector_to(vector: CartesianRepresentation, unit: Quantity):
    return apply_to_vector(vector, lambda i: i.to(unit))

def vector_magnitude(vector: CartesianRepresentation):
    return np.sqrt(vector.x**2 + vector.y**2 + vector.z**2)

def unit_vector(vector: CartesianRepresentation):
    return vector / vector_magnitude(vector)

def to_vector(data, unit):
    return CartesianRepresentation(data["x"] * unit, data["y"] * unit, data["z"] * unit)

def array_to_vectors(array, unit):
    arr = []
    for a in array:
        arr.append(to_vector(a, unit))
    return arr

def interpret_time(string: str):
    if string.endswith("min"):
        string = string.removesuffix("min")
        return float(string) * 60 * u.s 
    elif string.endswith("hr"): 
        string = string.removesuffix("hr")
        return float(string) * 3600 * u.s
    elif string.endswith("d"):
        string  = string.removesuffix("d")
        return float(string) * 86400 * u.s