from axinite.tools import AxiniteArgs, string_to_color, Body
from vpython import *
from itertools import cycle
from astropy.coordinates import CartesianRepresentation
  
def to_vec(cartesian_representation: CartesianRepresentation):
    return vector(cartesian_representation.x.value, cartesian_representation.y.value, cartesian_representation.z.value)
    
def vpython_frontend(args: AxiniteArgs, mode: str, **kwargs):
    if mode == "live" or mode == "run":
        return vpython_rt(args, **kwargs)
    elif mode == "show":
        return vpython_static(args, **kwargs)
    
def vpython_rt(args: AxiniteArgs):
    if args.rate is None:
        args.rate = 100
    if args.radius_multiplier is None:
        args.radius_multiplier = 1
    if args.retain is None:
       args.retain = 200
    
    scene = canvas(title=args.name)
    scene.select()

    colors = cycle([color.red, color.blue, color.green, color.orange, color.purple, color.yellow])

    global pause
    pause = False
    def pause_handler():
        global pause
        pause = not pause
    button(text='Pause', bind=pause_handler, pos=scene.caption_anchor)

    spheres = {}
    labels = {}
    lights = {}

    for body in args.bodies:
        body_color = string_to_color(body.color, "vpython") if body.color != "" else next(colors)
        body_retain = body.retain if body.retain != None else args.retain
        spheres[body.name] = sphere(pos=to_vec(body.r[0]), radius=body.radius.value * args.radius_multiplier, color=body_color, make_trail=True, retain=body_retain, interval=10)
        labels[body.name] = label(pos=spheres[body.name].pos, text=body.name, xoffset=15, yoffset=15, space=30, height=10, border=4, font='sans')
        if body.light == True: 
            lights[body.name] = local_light(pos=to_vec(body.r[0]), color=body_color)
            attach_light(spheres[body.name], lights[body.name])

    def fn(t, **kwargs):
        rate(args.rate)
        for body in kwargs["bodies"]:
            spheres[body.name].pos = to_vec(body.r[t.value])
            labels[body.name].pos = spheres[body.name].pos
            try: lights[body.name].pos = spheres[body.name].pos
            except: pass
        print(f"t = {t}", end='\r')
        if pause: 
            while pause: rate(10)

    return fn

def vpython_static(args: AxiniteArgs):
    scene = canvas(title=args.name)
    scene.select()

    colors = cycle([color.red, color.blue, color.green, color.orange, color.purple, color.yellow])

    def fn(body: Body):
        body_color = string_to_color(body.color, "vpython") if body.color != "" else next(colors)
        
        label(pos=to_vec(body.r[0]), text=body.name, xoffset=15, yoffset=15, space=30, height=10, border=4, font='sans', color=body_color)
        curve(pos=[to_vec(r) for r in body.r.values()], color=body_color)
        sphere(pos=to_vec(body.r[0]), radius=body.radius.value * args.radius_multiplier, color=body_color, opacity=0.2, make_trail=False)

    return fn