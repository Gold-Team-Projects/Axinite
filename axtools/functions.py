import astropy.units as u
import axinite as ax
from astropy.coordinates import CartesianRepresentation
import vpython as vp
import numpy as np

def interpret_time(string: str):
    if type(string) is float: return string * u.s
    if string.endswith("min"):
        string = string.removesuffix("min")
        return float(string) * 60 * u.s 
    elif string.endswith("hr"): 
        string = string.removesuffix("hr")
        return float(string) * 3600 * u.s
    elif string.endswith("d"):
        string  = string.removesuffix("d")
        return float(string) * 86400 * u.s
    else: return float(string) * u.s

def array_to_vectors(array, unit):
    arr = []
    for a in array:
        arr.append(ax.to_vector(a, unit))
    return arr

def data_to_body(data):
    name = data["name"]
    mass = data["mass"] * u.kg
    
    if "x" in data["r"]:
        position = ax.to_vector(data["r"], u.m)
        velocity = ax.to_vector(data["v"], u.m/u.s)

        return ax.Body(name, mass, position, velocity, data["radius"] * u.m)
    else:
        position = [vector_from_list(r, u.m) for r in data["r"].values()]
        velocity = [vector_from_list(v, u.m/u.s) for v in data["v"].values()]

        body = ax.Body(name, mass, position[0], velocity[0], data["radius"] * u.m)

        for t, r in data["r"].items():
            body.r[to_float(t)] = vector_from_list(r, u.m)
        for t, v in data["v"].items():
            body.v[to_float(t)] = vector_from_list(v, u.m)
        
        return body

def to_vec(vector: CartesianRepresentation):
    return vp.vector(vector.x.value, vector.y.value, vector.z.value)

def vector_from_list(vector: list, unit):
    return CartesianRepresentation(u.Quantity(float(vector[0]), unit), u.Quantity(float(vector[1]), unit), u.Quantity(float(vector[2]), unit))

def to_float(val):
    return np.float64(val)