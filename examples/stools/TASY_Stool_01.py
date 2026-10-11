from pymxs import runtime as rt

# TASY Stool 01
# Run in 3ds Max: Scripting -> Run Script
# Creates one editable stool at world origin.

PREFIX = "TASY_Stool_01"

# Seat
seat = rt.Cylinder(radius=175.0, height=28.0, pos=rt.Point3(0, 0, 422))
seat.name = PREFIX + "_Seat"

# Simple birch-like material
mat = rt.StandardMaterial()
mat.name = PREFIX + "_Birch"
mat.diffuse = rt.Color(205, 170, 115)
seat.material = mat

# First curved leg: renderable rectangular spline -> Editable Poly
leg = rt.SplineShape()
leg.name = PREFIX + "_Leg_01_Spline"
rt.addNewSpline(leg)

points = [
    (-105.0, 0.0, 410.0),
    (-120.0, 0.0, 350.0),
    (-145.0, 0.0, 255.0),
    (-165.0, 0.0, 150.0),
    (-170.0, 0.0, 35.0),
]

for x, y, z in points:
    rt.addKnot(
        leg,
        1,
        rt.Name("smooth"),
        rt.Name("curve"),
        rt.Point3(x, y, z)
    )

rt.updateShape(leg)

leg.render_renderable = True
leg.render_displayRenderMesh = True
leg.render_useViewportSettings = False
leg.render_rectangular = True
leg.render_length = 60.0
leg.render_width = 22.0
leg.render_angle = 0.0
leg.render_generateUVs = True

rt.updateShape(leg)
rt.convertToPoly(leg)
leg.name = PREFIX + "_Leg_01"
leg.material = mat

# Three copies around world Z
legs = [leg]

for index, angle in enumerate((90.0, 180.0, 270.0), start=2):
    new_leg = rt.copy(leg)
    new_leg.name = PREFIX + "_Leg_%02d" % index
    rt.rotate(new_leg, rt.AngleAxis(angle, rt.Point3(0, 0, 1)))
    new_leg.material = mat
    legs.append(new_leg)

rt.select([seat] + legs)
rt.redrawViews()
