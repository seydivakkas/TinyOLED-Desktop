"""TinyOLED Desktop — 3D Tel Kafes Küp"""
import math
from core.framebuffer import Framebuffer

class Cube3DApp:
    NAME="cube3d"; LABEL="3D"; ICON="cube"
    def __init__(self, on_exit):
        self.on_exit=on_exit; self.ax=0.0; self.ay=0.0; self.az=0.0
        self.verts=[[-1,-1,-1],[1,-1,-1],[1,1,-1],[-1,1,-1],[-1,-1,1],[1,-1,1],[1,1,1],[-1,1,1]]
        self.edges=[(0,1),(1,2),(2,3),(3,0),(4,5),(5,6),(6,7),(7,4),(0,4),(1,5),(2,6),(3,7)]
    def on_up(self): pass
    def on_down(self): pass
    def on_sel(self): pass
    def on_long(self): self.on_exit()
    def _rot(self, x, y, z):
        # Rotate X
        y1=y*math.cos(self.ax)-z*math.sin(self.ax); z1=y*math.sin(self.ax)+z*math.cos(self.ax)
        # Rotate Y
        x1=x*math.cos(self.ay)+z1*math.sin(self.ay); z2=-x*math.sin(self.ay)+z1*math.cos(self.ay)
        # Rotate Z
        x2=x1*math.cos(self.az)-y1*math.sin(self.az); y2=x1*math.sin(self.az)+y1*math.cos(self.az)
        return x2,y2,z2
    def update(self):
        self.ax+=0.05; self.ay+=0.07; self.az+=0.03
    def draw(self, fb: Framebuffer):
        fb.text("3D Wireframe",30,2)
        cx,cy,d=64,36,3.0; scale=20
        pts=[]
        for v in self.verts:
            x,y,z=self._rot(v[0],v[1],v[2])
            f=d/(d+z) if d+z!=0 else 1
            pts.append((int(cx+x*scale*f),int(cy+y*scale*f)))
        for a,b in self.edges:
            fb.line(pts[a][0],pts[a][1],pts[b][0],pts[b][1])
        for p in pts: fb.circle(p[0],p[1],1,fill=True)
