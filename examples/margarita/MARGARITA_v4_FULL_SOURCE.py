# -*- coding: utf-8 -*-
"""
MARGARITA | Complete reproducible 3ds Max scene
3ds Max 2024 | Python / pymxs | centimeters
4 sculptural lounge chairs with overlapping oversized spline sections, table at 95 cm.
Based on actual MaxBridge scripts and the original scene geometry inspection. Oversized shell reconstruction still requires visual comparison.
Run from 3ds Max: Scripting > Run Script (select this .py).
WARNING: Deletes and rebuilds objects prefixed TASY_GC01_ and TASY_MARGARITA_SET01_.
Save your current scene before running.
"""


# ======================================================================
# STAGE 1: MAXBRIDGE_COMMAND_V10.json
# ======================================================================
from pymxs import runtime as rt
import math
P='TASY_GC01_'
# Rebuild ONLY prefixed scene objects. Scene units: centimetres.
for obj in list(rt.objects):
 if str(obj.name).startswith('TASY_MARGARITA_SET01_'):
  rt.delete(obj)
old=rt.getNodeByName(P+'GardenChair_Group')
if old is not None:
    try: rt.ungroup(old)
    except Exception as e: print('ungroup:',e)
for o in list(rt.objects):
    if str(o.name).startswith(P): rt.delete(o)
wood=rt.StandardMaterial(name=P+'Warm_Oak'); wood.diffuse=rt.color(205,164,104)
steel=rt.StandardMaterial(name=P+'Dark_Steel'); steel.diffuse=rt.color(48,54,53)
segs=[((-63,45.5),(-42,45.7),(-27,42),(-11,41.3)),((-11,41.3),(8.5,40.3),(17.5,48.5),(24.5,68)),((24.5,68),(31.5,85.5),(42,109),(54.5,116))]
def bez(q,t):
 a,b,c,d=q;k=1-t
 return (k**3*a[0]+3*k*k*t*b[0]+3*k*t*t*c[0]+t**3*d[0],k**3*a[1]+3*k*k*t*b[1]+3*k*t*t*c[1]+t**3*d[1])
profile=[]
for si,seg in enumerate(segs):
 for j in range(25):
  if si and j==0:continue
  profile.append(bez(seg,j/24.0))
def spl(name,pts,mat,section='round',a=1.5,b=None):
 s=rt.SplineShape(name=P+name);rt.addNewSpline(s)
 for p in pts:rt.addKnot(s,1,rt.Name('corner'),rt.Name('line'),rt.Point3(*p))
 rt.updateShape(s);s.render_renderable=True;s.render_displayRenderMesh=True
 if section=='round':s.render_radial=True;s.render_thickness=a;s.render_sides=12
 else:s.render_rectangular=True;s.render_length=a;s.render_width=b
 s.material=mat
 return s
for side,x in [('L',-34.5),('R',34.5)]:
 spl('UpperRail_'+side,[(x,y,z-2.5) for y,z in profile],steel,'rect',2.8,3.6)
 def arc(cy,cz,r,a0,a1):
  return [(cy+r*math.cos(math.radians(a0+(a1-a0)*j/8)),cz+r*math.sin(math.radians(a0+(a1-a0)*j/8))) for j in range(9)]
 leg=[(-59,42),(-64.1,10.5)]+arc(-60.1,10.5,4,180,270)[1:]+[(51,6.5)]+arc(51,10.5,4,-90,0)[1:]+[(34.5,83)]
 spl('SledLeg_'+side,[(x,y,z) for y,z in leg],steel,'rect',3,3.5)
for j,(y,z) in enumerate([(-51,6.5),(49,6.5)]):spl('Crossbar_%02d'%(j+1),[(-34.5,y,z),(34.5,y,z)],steel,'rect',2.6,2.8)
dist=[0.]
for i in range(1,len(profile)):
 dist.append(dist[-1]+math.hypot(profile[i][0]-profile[i-1][0],profile[i][1]-profile[i-1][1]))
total=dist[-1]
def at(s):
 for j in range(1,len(dist)):
  if dist[j]>=s:
   f=(s-dist[j-1])/(dist[j]-dist[j-1]);y=profile[j-1][0]*(1-f)+profile[j][0]*f;z=profile[j-1][1]*(1-f)+profile[j][1]*f
   a=math.atan2(profile[j][1]-profile[j-1][1],profile[j][0]-profile[j-1][0]);return y,z,a
 return profile[-1][0],profile[-1][1],0
# 35 closely spaced transverse rods, 1.5 cm diameter, hemispherical ends.
count=35
for i in range(count):
 s=3.8+(total-7.6)*i/(count-1);y,z,theta=at(s)
 # extra ergonomic sag in seat, smooth fade at front and back
 weight=max(0.,1.-abs(s/total-0.32)/0.42)
 sag=0.9+3.6*weight
 pts=[]
 for k in range(25):
  x=-36.75+73.5*k/24.;t=x/36.75
  bend=-sag*(1-t*t)**2
  off=1.3+bend
  pts.append((x,y-math.sin(theta)*off,z+math.cos(theta)*off))
 spl('OakRod_%02d'%(i+1),pts,wood,'round',1.5)
 for label,point in [('L',pts[0]),('R',pts[-1])]:
  cap=rt.Sphere(name=P+'RodCap_%02d_%s'%(i+1,label),radius=0.75,segs=12)
  cap.pos=rt.Point3(*point);cap.material=wood
# Sculptural pizza-box shells: preserve every original 1.5 cm round rod.
# Duplicate each source spline and enlarge ONLY the duplicate's render section.
# These intentionally oversized rectangles overlap to form the folded shell.
for i in range(1,36):
 original=rt.getNodeByName(P+'OakRod_%02d'%i)
 if original is None: raise RuntimeError('Missing source rod %02d'%i)
 shell=rt.copy(original)
 shell.name=P+'PizzaShell_%02d'%i
 shell.render_renderable=True
 shell.render_displayRenderMesh=True
 shell.render_rectangular=True
 shell.render_length=60.0
 shell.render_width=30.0
 shell.render_angle=22.375
 shell.material=wood
print('MARGARITA: 35 thin rods preserved; 35 oversized rectangular shells added.')
parts=[o for o in rt.objects if str(o.name).startswith(P)]
rt.group(parts,name=P+'GardenChair_Group')
rt.execute('max tool zoomextents all');rt.redrawViews()
print('GC01 V10: 35 rounded wooden rods dia 1.5 cm, ergonomic seat sag, all geometry in cm; objects',len(parts))


# ======================================================================
# STAGE 2: MARGARITA_SET01_v02_command.json
# ======================================================================
from pymxs import runtime as rt
import math
P='TASY_GC01_'
S='TASY_MARGARITA_SET01_'
master=rt.getNodeByName(P+'GardenChair_Group')
if master is None: raise RuntimeError('Master chair group missing. No changes made.')
# Group heads copied by rt.copy are empty. Remove only old set elements.
for obj in list(rt.objects):
    if str(obj.name).startswith(S):
        try: rt.delete(obj)
        except Exception as e: print('old set deletion:',str(e))
# Clone actual spline/mesh objects, NOT group head; source geometry stays intact.
originals=[o for o in list(rt.objects) if str(o.name).startswith(P) and not rt.isGroupHead(o)]
if len(originals)<40: raise RuntimeError('Not enough source chair geometry (%d)'%len(originals))
print('Master components:',len(originals))
# Chair faces approximately negative Y in master scene; set each chair's local orientation toward centre.
placements=[(0,150,0),(150,0,90),(0,-150,180),(-150,0,270)]
for index,(cx,cy,deg) in enumerate(placements,1):
    angle=math.radians(deg)
    c=math.cos(angle); s=math.sin(angle)
    members=[]
    for source in originals:
        clone=rt.copy(source)
        clone.name=S+'Chair_%02d_'%index+str(source.name)[len(P):]
        # Rotate local geometry about the master scene origin, then translate.
        pos=source.pos
        px=float(pos.x);py=float(pos.y);pz=float(pos.z)
        rt.rotate(clone,rt.angleAxis(float(deg),rt.Point3(0,0,1)))
        clone.pos=rt.Point3(cx+c*px-s*py,cy+s*px+c*py,pz)
        clone.isHidden=False
        members.append(clone)
    head=rt.group(members,name=S+'Chair_%02d_Group'%index)
    print('Cloned chair',index,'parts',len(members),'group',head.name)
master.isHidden=True
# Sculptural asymmetric oval table, 42cm tall, with rounded perimeter.
wood=rt.StandardMaterial(name=S+'Table_Cardboard');wood.diffuse=rt.color(180,141,93)
steel=rt.StandardMaterial(name=S+'Table_Metal');steel.diffuse=rt.color(50,55,54)
shape=rt.SplineShape(name=S+'Table_Top')
rt.addNewSpline(shape)
for j in range(48):
    t=2*math.pi*j/48
    r=1+.045*math.sin(3*t+.3)+.025*math.cos(5*t-.5)
    rt.addKnot(shape,1,rt.Name('smooth'),rt.Name('curve'),rt.Point3(60*r*math.cos(t),37*r*math.sin(t),38))
rt.close(shape,1);rt.updateShape(shape)
shape.material=wood
ext=rt.Extrude();ext.amount=4;rt.addModifier(shape,ext)
try:
    cham=rt.Chamfer();cham.amount=.8;cham.segments=3;rt.addModifier(shape,cham)
except Exception as e:print('Table edge chamfer skipped:',e)
stem=rt.Cylinder(name=S+'Table_Stem',radius=7,height=36,sides=32);stem.pos=rt.Point3(0,0,18);stem.material=steel
base=rt.Cylinder(name=S+'Table_Base',radius=27,height=2,sides=48);base.pos=rt.Point3(0,0,1);base.material=steel
rt.clearSelection()
rt.execute('max tool zoomextents all')
rt.redrawViews()
print('MARGARITA SET v02: four FULL chair groups and organic table. Master hidden, preserved.')


# ======================================================================
# STAGE 3: MARGARITA_SET01_v03_command.json
# ======================================================================
from pymxs import runtime as rt
S='TASY_MARGARITA_SET01_'
P='TASY_GC01_'
# Preserve every piece of geometry and the table.
# Explicitly hide master geometry, not only its group head.
hidden=[]
for obj in list(rt.objects):
    if str(obj.name).startswith(P):
        try:
            obj.isHidden=True
            hidden.append(str(obj.name))
        except Exception as e: print('hide:',obj.name,e)
master=rt.getNodeByName(P+'GardenChair_Group')
if master is not None:
    try: master.isHidden=True
    except Exception as e: print('master hide:',e)
# Side chairs 02 and 04 are facing away. Reverse each complete group in place.
turned=[]
for i in (2,4):
    name=S+'Chair_%02d_Group'%i
    head=rt.getNodeByName(name)
    if head is None: print('missing group:',name);continue
    before=rt.copy(head.pos)
    rt.rotate(head,rt.angleAxis(180.0,rt.Point3(0,0,1)))
    head.pos=before
    turned.append(name)
rt.clearSelection()
rt.redrawViews()
print('MARGARITA SET v03: master hidden objects',len(hidden),'side chairs turned 180 degrees',turned)


# ======================================================================
# STAGE 4: MARGARITA_SET01_v04_command.json
# ======================================================================
from pymxs import runtime as rt
S='TASY_MARGARITA_SET01_'
# Widen seating circle without changing group orientation or geometry.
for i in range(1,5):
    head=rt.getNodeByName(S+'Chair_%02d_Group'%i)
    if head is None: raise RuntimeError('Missing chair group %02d'%i)
    p=head.pos
    # Original group centers lie on cardinal axes around origin.
    dx=45.0 if p.x>50 else (-45.0 if p.x< -50 else 0.0)
    dy=45.0 if p.y>50 else (-45.0 if p.y< -50 else 0.0)
    head.pos=rt.Point3(p.x+dx,p.y+dy,p.z)
# Top spline was extruded but the stacked chamfer may obscure its surface.
top=rt.getNodeByName(S+'Table_Top')
if top is None: raise RuntimeError('Table top missing')
try:
    # Keep the original asymmetric spline, remove modifiers and re-extrude.
    while top.modifiers.count>0:
        rt.deleteModifier(top,1)
except Exception as e: print('modifier cleanup:',e)
try:
    top.render_renderable=False
    top.render_displayRenderMesh=False
except: pass
ex=rt.Extrude()
ex.amount=4.0
ex.capStart=True
ex.capEnd=True
rt.addModifier(top,ex)
# Original spline knots are at Z=38, extrude upward; lift top to 44-48 cm.
top.pos=rt.Point3(0,0,6)
# A pedestal from the foot (Z=2) to underside of the top (Z=44).
stem=rt.getNodeByName(S+'Table_Stem')
if stem is not None:
    stem.height=42.0
    stem.pos=rt.Point3(0,0,23.0)
base=rt.getNodeByName(S+'Table_Base')
if base is not None: base.pos=rt.Point3(0,0,1)
rt.clearSelection()
rt.redrawViews()
print('MARGARITA v04: chair groups shifted outward 45 cm; table top 44-48 cm, pedestal connected')


# ======================================================================
# STAGE 5: MARGARITA_SET01_v06_command.json
# ======================================================================
from pymxs import runtime as rt
S='TASY_MARGARITA_SET01_'
top=rt.getNodeByName(S+'Table_Top')
stem=rt.getNodeByName(S+'Table_Stem')
base=rt.getNodeByName(S+'Table_Base')
if top is None or stem is None or base is None:
    raise RuntimeError('Table component missing; nothing changed')
def bbox(o):
    return rt.nodeGetBoundingBox(o,rt.matrix3(1))
# Use measured world-space bounding box, not local object position.
lo,hi=bbox(top)
before=float(hi.z)
top.pos=top.pos+rt.Point3(0,0,95.0-before)
lo,hi=bbox(top)
underside=float(lo.z)
footlo,foothi=bbox(base)
foot_top=float(foothi.z)
span=underside-foot_top
if span<=0:
    raise RuntimeError('Invalid table span; inspect coordinates')
# Standard Cylinder pivot is centered on its height.
stem.height=span+0.4
stem.pos=rt.Point3(float(stem.pos.x),float(stem.pos.y),foot_top+span/2)
rt.clearSelection()
rt.redrawViews()
print('MARGARITA v06 table only: tabletop upper Z',round(float(bbox(top)[1].z),2),'base upper Z',round(foot_top,2),'stem height',round(span+0.4,2))


# ======================================================================
# STAGE 6: MARGARITA_SET01_v07_command.json
# ======================================================================
from pymxs import runtime as rt
S='TASY_MARGARITA_SET01_'
top=rt.getNodeByName(S+'Table_Top')
base=rt.getNodeByName(S+'Table_Base')
old=rt.getNodeByName(S+'Table_Stem')
if top is None or base is None:
    raise RuntimeError('Table top or base not found; no changes')
a,b=rt.nodeGetBoundingBox(top,rt.matrix3(1))
underside=float(a.z)
a,b=rt.nodeGetBoundingBox(base,rt.matrix3(1))
foot_top=float(b.z)
height=underside-foot_top
if height<10:
    raise RuntimeError('Invalid pedestal clearance: %.2f cm'%height)
# 3ds Max Cylinder pivot is at its BASE, not halfway up the cylinder.
new=rt.Cylinder(name=S+'Table_Stem_NEW',radius=7.0,height=height+0.4,sides=32,heightsegs=1)
new.pos=rt.Point3(0,0,foot_top-0.2)
if old is not None:
    try: new.material=old.material
    except: pass
# Check real geometry before replacing original.
lo,hi=rt.nodeGetBoundingBox(new,rt.matrix3(1))
print('NEW pedestal bbox Z',float(lo.z),float(hi.z),'target',foot_top,underside)
if abs(float(lo.z)-(foot_top-0.2))>1 or abs(float(hi.z)-(underside+0.2))>1:
    rt.delete(new)
    raise RuntimeError('Cylinder bounding box failed validation; original preserved')
if old is not None: rt.delete(old)
new.name=S+'Table_Stem'
rt.clearSelection()
rt.redrawViews()
print('MARGARITA v07: replaced ONLY cylinder; height %.2f cm; tabletop unchanged'%height)

print("MARGARITA COMPLETE: four chairs and 95 cm table assembled.")

# Optional raised lettering, placed on ground behind the seating circle.
# Text remains editable as spline text; no font dependency beyond Max default.
try:
    signmat=rt.StandardMaterial(name='TASY_MARGARITA_SET01_Signature_Bronze')
    signmat.diffuse=rt.color(204,167,112)
    signlines=[('CREATED BY CHATGPT',9),('IN 3DS MAX VIA MAXBRIDGE',7),('ALWAYS WITH LOVE,',7),('TASY VOLKOVA',11),('TASY.PRO',9)]
    for idx,(message,size) in enumerate(signlines):
        obj=rt.Text(name='TASY_MARGARITA_SET01_Signature_%02d'%(idx+1))
        obj.text=message
        obj.size=size
        obj.pos=rt.Point3(-100,275,105-idx*16)
        obj.rotation=rt.eulerAngles(90,0,0)
        obj.material=signmat
        modifier=rt.Extrude()
        modifier.amount=0.8
        rt.addModifier(obj,modifier)
except Exception as err:
    print('Optional signature creation failed:',err)
rt.redrawViews()
print('MARGARITA PIZZA BOX SCENE: completed; verify in viewport.')
