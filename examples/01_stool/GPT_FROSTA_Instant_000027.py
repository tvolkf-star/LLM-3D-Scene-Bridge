from pymxs import runtime as rt

wood = rt.StandardMaterial(name="GPT_FROSTA2_Birch")
wood.diffuse = rt.color(218,190,148)

seat_r = 175.0
seat_t = 28.0
overall_h = 450.0
seat_z = overall_h - seat_t

seat = rt.Cylinder(
    name="GPT_FROSTA2_Seat",
    radius=seat_r,
    height=seat_t,
    sides=64,
    heightsegs=1,
    capsegs=1
)
seat.pos = rt.Point3(0,0,seat_z)
seat.material = wood

def make_leg(name):
    s = rt.SplineShape(name=name)
    rt.addNewSpline(s)
    pts = [
        rt.Point3(-72,0,424),
        rt.Point3(-105,0,421),
        rt.Point3(-132,0,408),
        rt.Point3(-151,0,382),
        rt.Point3(-159,0,345),
        rt.Point3(-160,0,250),
        rt.Point3(-162,0,150),
        rt.Point3(-164,0,32)
    ]
    for p in pts:
        rt.addKnot(s,1,rt.Name("smooth"),rt.Name("curve"),p)
    rt.updateShape(s)
    s.render_renderable = True
    s.render_displayRenderMesh = True
    s.render_rectangular = True
    s.render_length = 48.0
    s.render_width = 24.0
    s.material = wood
    p = rt.convertToPoly(s)
    p.name = name
    p.material = wood
    return p

leg1 = make_leg("GPT_FROSTA2_Leg_01")
legs = [leg1]
for i,a in enumerate((90,180,270), start=2):
    q = rt.copy(leg1)
    q.name = "GPT_FROSTA2_Leg_%02d" % i
    rt.rotate(q,rt.AngleAxis(float(a),rt.Point3(0,0,1)))
    legs.append(q)

rt.select([seat]+legs)
rt.execute("max tool zoomextents all")
rt.redrawViews()
