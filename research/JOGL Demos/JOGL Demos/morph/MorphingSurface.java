package morph;

import static java.lang.Math.PI;
import static java.lang.Math.cos;
import static java.lang.Math.sin;
import internals.GLRenderer;

import javax.media.opengl.GL;
import javax.media.opengl.GLAutoDrawable;

import com.benton.framework.math.M3d;



public class MorphingSurface extends GLRenderer {
  private static final int di = 32;
  private static final int dj = 32;

  private int tick = 0;
  private MeshPt[][] mesh;

  public String getTitle() {
    return "Parametric Morph";
  }

  ////////////////////////

  class MeshPt extends M3d {
    private int i, j;
    
    MeshPt(M3d pt, int i, int j) { super(pt.get(0), pt.get(1), pt.get(2)); this.i = i; this.j = j; }

    MeshPt getAdjacent(int deltai, int deltaj) { return getMesh(i+deltai,j+deltaj); }
    MeshPt vertex(GL gl) { gl.glVertex3d(get(0), get(1), get(2)); return this; }
    MeshPt color(GL gl) { gl.glColor3d((get(0)+1)/2.0, (get(1)+1)/2.0, (get(2)+1)/2.0); return this; }
    MeshPt normal(GL gl) {
      M3d a = getAdjacent(-1, 0).plus(this.times(-1));
      M3d b = getAdjacent(0, -1).plus(this.times(-1));
      M3d c = getAdjacent(1, 0).plus(this.times(-1));
      M3d d = getAdjacent(0, 1).plus(this.times(-1));
      M3d ab = a.cross(b);
      M3d bc = b.cross(c);
      M3d cd = c.cross(d);
      M3d da = d.cross(a);
      M3d n = ab.plus(bc).plus(cd).plus(da).normalized();
      
      gl.glNormal3d(n.get(0), n.get(1), n.get(2));
      return this;
    }
  }
  
  ////////////////////////
  
  interface Generator {
    M3d get(double u, double v);
  }

  ////////////////////////

  Generator sphere = new Generator() { public M3d get(double u, double v) {
    u = 2 * PI * u;
    v = PI * (v-0.5);
    return new M3d(Math.cos(u) * Math.cos(v),
                   Math.sin(u) * Math.cos(v),
                   Math.sin(v));
  } };
  
  Generator powerSphere = new Generator() { public M3d get(double u, double v) {
    u = 2 * PI * u;
    v = PI * (v-0.5);
    double x = Math.cos(u) * Math.cos(v);
    double y = Math.sin(u) * Math.cos(v);
    double z = Math.sin(v);
    
    return new M3d(x*x*x, y*y*y, z*z*z);
  } };
  
  Generator cylinder = new Generator() { public M3d get(double u, double v) {
    u = 2 * PI * u;
    v = 2 * (v-0.5);
    return new M3d(Math.cos(u),
                   sin(u),
                   v);
  } };
  
  Generator torus = new Generator() { public M3d get(double u, double v) {
    M3d pt;
    
    u = 2 * PI * u;
    v = 2 * PI * v + PI;
    pt = new M3d(1+0.25*cos(v), 0, 0.25*sin(v));
    return new M3d(pt.get(0) * cos(u) - pt.get(1) * sin(u),
                   pt.get(0) * sin(u) + pt.get(1) * cos(u),
                   pt.get(2));
  } };
  
  public void buildMesh() {
    Generator[] generators = { sphere, powerSphere, cylinder, torus };
    int which = tick/500;
    double t = sin(((double)(tick%500))*(PI/2.0)/500.0);
    Generator A = generators[which%generators.length];
    Generator B = generators[(which+1)%generators.length];
    
    mesh = new MeshPt[di][dj];
    for (int i = 0; i<di; i++) {
      for (int j = 0; j<dj; j++) {
        double u = (double)i / (di-1);
        double v = (double)j / (dj-1);
        mesh[i][j] = new MeshPt(A.get(u, v).times(1-t).plus(B.get(u, v).times(t)), i, j);
      }
    }
  }
  
  public MeshPt getMesh(int i, int j) {
    while (i < 0) { i += di; };
    while (j < 0) { j += dj; };
    return mesh[i%di][j%dj];
  }

  public void display(GLAutoDrawable gLDrawable) {
    final GL gl = gLDrawable.getGL();
    float t = ((float)tick)/10.0f;

    gl.glClear(GL.GL_COLOR_BUFFER_BIT);
    gl.glClear(GL.GL_DEPTH_BUFFER_BIT);
    
    gl.glLoadIdentity();
    gl.glTranslatef(0.0f, 0.0f, -4.0f);

    gl.glRotatef(t, 1.0f, 0.0f, 0.0f);
    gl.glRotatef(t, 0.0f, 1.0f, 0.0f);
    gl.glRotatef(t, 0.0f, 0.0f, 1.0f);
    gl.glRotatef(t, 0.0f, 1.0f, 0.0f);

    buildMesh();
    gl.glBegin(GL.GL_QUADS);
    for (int i = 0; i<di-1; i++) {
      for (int j = 0; j<dj-1; j++) {
        getMesh(i,j).normal(gl).color(gl).vertex(gl);
        getMesh(i+1,j).normal(gl).color(gl).vertex(gl);
        getMesh(i+1,j+1).normal(gl).color(gl).vertex(gl);
        getMesh(i,j+1).normal(gl).color(gl).vertex(gl);
      }
    }
    gl.glEnd();
    gl.glTranslatef(0.0f, 0.0f, 0.00001f);
    gl.glColor3i(0,0,0);
    for (int i = 0; i<di-1; i++) {
      for (int j = 0; j<dj-1; j++) {
        gl.glBegin(GL.GL_LINE_LOOP);
        getMesh(i,j).vertex(gl);
        getMesh(i+1,j).vertex(gl);
        getMesh(i+1,j+1).vertex(gl);
        getMesh(i,j+1).vertex(gl);
        gl.glEnd();
      }
    }
    
    tick++;
  }
}
