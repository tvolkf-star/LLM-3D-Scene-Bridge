from pymxs import runtime as rt
import math
rt.resetMaxFile(rt.Name("noPrompt"))
MAT=rt.StandardMaterial(name="MAT_035_WarmTimber"); MAT.diffuse=rt.color(198,166,118)
N=73; length=9000.0; x0=-length/2.0; dx=length/(N-1); made=[]
def ss(a,b,x):
    if x<=a:return 0.0
    if x>=b:return 1.0
    t=(x-a)/(b-a); return t*t*(3-2*t)
def prof(name,x,u):
    wave=math.sin(math.pi*u); sd=560+150*wave
    by=-80+70*math.sin(2*math.pi*u); cy=1180+850*ss(.12,.72,u); cz=2280+520*wave
    pts=[(x,sd-70,95),(x,sd+10,250),(x,sd+35,420),(x,sd-10,455),
         (x,190,463),(x,35,500),(x,by,610),(x,by-25,900),(x,by-35,1450),
         (x,by-20,1900),(x,40,2160),(x,300,cz-70),(x,cy,cz)]
    s=rt.SplineShape(name=name); rt.addNewSpline(s)
    for p in pts: rt.addKnot(s,1,rt.Name("smooth"),rt.Name("curve"),rt.Point3(*p))
    rt.updateShape(s); s.render_renderable=True; s.render_displayRenderMesh=True
    s.render_mapcoords=True; s.render_rectangular=True; s.render_length=72.0; s.render_width=24.0
    s.material=MAT; rt.convertToPoly(s); return s
for i in range(N): made.append(prof("MAF035_%03d"%(i+1),x0+i*dx,i/float(N-1)))
master=made[0]; master.name="MAF035_RibbonSeat"
for o in made[1:]:
    try: rt.polyop.attach(master,o)
    except: pass
base=rt.Box(name="MAF035_Platform",length=length+500,width=1900,height=80)
base.pos=rt.Point3(0,350,40)
bm=rt.StandardMaterial(name="MAT_035_Base"); bm.diffuse=rt.color(105,105,100); base.material=bm
rt.select(master); rt.execute("max tool zoomextents all")
