/** TinyOLED Desktop — 3D Wireframe Cube */
export class Cube3DApp {
  static NAME='cube3d'; static LABEL='3D'; static ICON='cube';
  constructor(onExit) {
    this.onExit=onExit; this.ax=0; this.ay=0; this.az=0;
    this.verts=[[-1,-1,-1],[1,-1,-1],[1,1,-1],[-1,1,-1],[-1,-1,1],[1,-1,1],[1,1,1],[-1,1,1]];
    this.edges=[[0,1],[1,2],[2,3],[3,0],[4,5],[5,6],[6,7],[7,4],[0,4],[1,5],[2,6],[3,7]];
  }
  onUp(){} onDown(){} onSel(){} onLong(){this.onExit();}
  _rot(x,y,z) {
    let y1=y*Math.cos(this.ax)-z*Math.sin(this.ax), z1=y*Math.sin(this.ax)+z*Math.cos(this.ax);
    let x1=x*Math.cos(this.ay)+z1*Math.sin(this.ay), z2=-x*Math.sin(this.ay)+z1*Math.cos(this.ay);
    let x2=x1*Math.cos(this.az)-y1*Math.sin(this.az), y2=x1*Math.sin(this.az)+y1*Math.cos(this.az);
    return [x2,y2,z2];
  }
  update() { this.ax+=0.05; this.ay+=0.07; this.az+=0.03; }
  draw(fb) {
    fb.text('3D Wireframe',30,2);
    const cx=64,cy=36,d=3,scale=20, pts=[];
    for(const v of this.verts) {
      const[x,y,z]=this._rot(v[0],v[1],v[2]);
      const f=d+z!==0?d/(d+z):1;
      pts.push([Math.round(cx+x*scale*f),Math.round(cy+y*scale*f)]);
    }
    for(const[a,b] of this.edges) fb.line(pts[a][0],pts[a][1],pts[b][0],pts[b][1]);
    for(const p of pts) fb.circle(p[0],p[1],1,true,true);
  }
}
