# TASY MaxBridge 0.6.1 PERSONAL
# Stable 0.5.1 core + procedural library.
# 3ds Max 2024. ASCII-only source intentionally.

import os, json, traceback
from datetime import datetime
from pymxs import runtime as rt
from PySide2 import QtCore

ROOT=r"E:\TASY_MaxBridge"
CMD=os.path.join(ROOT,"command.json")
RESULT=os.path.join(ROOT,"result.json")
SCENE=os.path.join(ROOT,"scene.json")
STATUS=os.path.join(ROOT,"bridge_status.json")
STATE=os.path.join(ROOT,"bridge_state.json")
VIEW=os.path.join(ROOT,"viewport.png")
LIB=os.path.join(ROOT,"library")
BRIDGE_ID="TASY_MAX_BRIDGE_E_DRIVE_061"
VERSION="0.6.1"

def now():
    return datetime.now().isoformat(timespec="seconds")

# 0.5.1: NO .tmp FILES IN THE GOOGLE DRIVE SYNC FOLDER.
def write_json(path,data):
    with open(path,"w",encoding="utf-8") as f:
        json.dump(data,f,ensure_ascii=False,indent=2)

def read_json(path,default=None):
    try:
        with open(path,"r",encoding="utf-8-sig") as f:
            return json.load(f)
    except Exception:
        return default

def p3(v):
    return [float(v.x),float(v.y),float(v.z)]

def snapshot():
    out=[]
    for o in list(rt.objects):
        try:
            r={"name":str(o.name),"class":str(rt.classOf(o)),
               "position":p3(o.position),"scale":p3(o.scale)}
            try:
                bb=rt.nodeGetBoundingBox(o,o.transform)
                r["bbox"]={"min":p3(bb[0]),"max":p3(bb[1])}
            except Exception: pass
            out.append(r)
        except Exception: pass
    return {"bridge_id":BRIDGE_ID,"version":VERSION,"time":now(),
            "object_count":len(out),"objects":out}

def save_scene():
    write_json(SCENE,snapshot())

def capture_viewport():
    try:
        bmp=rt.viewport.getViewportDib()
        if bmp:
            try:
                bmp.filename=VIEW
                rt.save(bmp)
            finally:
                try: rt.close(bmp)
                except Exception: pass
            return os.path.isfile(VIEW)
    except Exception: pass
    return False

def save_state(cid,state):
    write_json(STATE,{"bridge_id":BRIDGE_ID,"version":VERSION,
                      "last_command_id":str(cid),"command_state":state,"time":now()})

def load_last():
    d=read_json(STATE,{}) or {}
    return str(d.get("last_command_id",""))

def status(last="",last_status=""):
    write_json(STATUS,{"bridge_id":BRIDGE_ID,"version":VERSION,"state":"running",
                       "time":now(),"last_command_id":last,
                       "last_command_status":last_status})

def node(name):
    o=rt.getNodeByName(str(name))
    if o is None: raise RuntimeError("Node not found: "+str(name))
    return o

def point(v,default=(0,0,0)):
    if v is None: v=default
    return rt.Point3(float(v[0]),float(v[1]),float(v[2]))

def safe_library_name(name):
    name=str(name)
    allowed="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-"
    if not name or any(ch not in allowed for ch in name):
        raise RuntimeError("Library name may contain only A-Z, a-z, 0-9, _ and -")
    return name

def library_path(name):
    return os.path.join(LIB,safe_library_name(name)+".py")

def run_one(c):
    a=str(c.get("action",""))
    if a=="ping": return "pong"

    if a=="execute_python":
        code=c.get("code","")
        if not code: raise RuntimeError("execute_python: empty code")
        scope={"rt":rt,"os":os,"json":json,"ROOT":ROOT,"LIB":LIB,
               "__builtins__":__builtins__}
        exec(code,scope,scope)
        return "python executed"

    if a=="library_list":
        if not os.path.isdir(LIB): return []
        return sorted([os.path.splitext(x)[0] for x in os.listdir(LIB)
                       if x.lower().endswith(".py")])

    if a=="library_save":
        name=safe_library_name(c.get("name",""))
        code=c.get("code","")
        if not code: raise RuntimeError("library_save: empty code")
        if not os.path.isdir(LIB): os.makedirs(LIB)
        with open(library_path(name),"w",encoding="utf-8") as f:
            f.write(code)
        return "saved:"+name

    if a=="library_run":
        name=safe_library_name(c.get("name",""))
        path=library_path(name)
        if not os.path.isfile(path):
            raise RuntimeError("Library item not found: "+name)
        params=c.get("params",{}) or {}
        scope={"rt":rt,"os":os,"json":json,"ROOT":ROOT,"LIB":LIB,
               "params":params,"__builtins__":__builtins__}
        with open(path,"r",encoding="utf-8-sig") as f:
            code=f.read()
        exec(code,scope,scope)
        return "ran:"+name

    if a=="create_box":
        s=c.get("size",[c.get("length",100),c.get("width",100),c.get("height",100)])
        o=rt.Box(length=float(s[0]),width=float(s[1]),height=float(s[2]),
                 pos=point(c.get("pos")))
        o.name=str(c.get("name","TASY_Box"))
        return str(o.name)

    if a=="move":
        o=node(c.get("name"))
        if "pos" in c: o.position=point(c["pos"])
        elif "delta" in c: o.position=o.position+point(c["delta"])
        else: raise RuntimeError("move requires pos or delta")
        return str(o.name)

    if a=="scale":
        o=node(c.get("name")); o.scale=point(c.get("scale"),(1,1,1))
        return str(o.name)

    if a=="rotate":
        o=node(c.get("name"))
        e=c.get("euler")
        if e is None: raise RuntimeError("rotate requires euler")
        o.rotation=rt.eulerAnglesToQuat(rt.EulerAngles(float(e[0]),float(e[1]),float(e[2])))
        return str(o.name)

    if a=="delete":
        o=node(c.get("name")); n=str(o.name); rt.delete(o); return n

    if a=="rename":
        o=node(c.get("name")); o.name=str(c.get("new_name")); return str(o.name)

    raise RuntimeError("Unknown action: "+a)

class Bridge(QtCore.QObject):
    def __init__(self):
        super(Bridge,self).__init__()
        if not os.path.isdir(ROOT): os.makedirs(ROOT)
        if not os.path.isdir(LIB): os.makedirs(LIB)
        self.last=load_last()
        self.timer=QtCore.QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.poll)
        self.timer.start()
        status(self.last,"started")
        save_scene()

    def stop(self):
        try: self.timer.stop()
        except Exception: pass

    def poll(self):
        d=read_json(CMD,None)
        if not isinstance(d,dict) or "id" not in d: return
        cid=str(d["id"])
        if cid==self.last: return

        # Consume BEFORE Max mutation: failed commands never repeat every second.
        self.last=cid
        save_state(cid,"processing")

        res=[]; st="ok"; err=None; tb=None
        try:
            cmds=d.get("commands")
            if not isinstance(cmds,list): cmds=[d]
            for c in cmds: res.append(run_one(c))
        except Exception as e:
            st="error"; err=type(e).__name__+": "+str(e); tb=traceback.format_exc()

        try: save_scene()
        except Exception as e:
            if st=="ok":
                st="error"; err="scene_snapshot: "+str(e); tb=traceback.format_exc()

        vp=capture_viewport()
        out={"bridge_id":BRIDGE_ID,"version":VERSION,"command_id":cid,
             "status":st,"time":now(),"results":res,"viewport_saved":vp}
        if err: out["error"]=err
        if tb: out["traceback"]=tb
        write_json(RESULT,out)
        save_state(cid,st)
        status(cid,st)

for n in ("TASY_MAX_BRIDGE","TASY_MAX_BRIDGE_05","TASY_MAX_BRIDGE_051","TASY_MAX_BRIDGE_060","TASY_MAX_BRIDGE_061"):
    try:
        x=globals().get(n)
        if x is not None and hasattr(x,"stop"): x.stop()
    except Exception: pass

TASY_MAX_BRIDGE_061=Bridge()
TASY_MAX_BRIDGE=TASY_MAX_BRIDGE_061
print("TASY MaxBridge 0.6.1 PERSONAL running")
print("ROOT: "+ROOT)
print("LIB:  "+LIB)
