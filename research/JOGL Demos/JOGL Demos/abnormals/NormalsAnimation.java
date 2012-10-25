package abnormals;

import static abnormals.Arrow.arrow;
import static com.benton.framework.math.MathUtil.intersectPlane;
import static java.lang.Math.PI;
import static java.lang.Math.cos;
import static java.lang.Math.sin;

import internals.GLRenderer;

import java.awt.event.KeyEvent;

import javax.media.opengl.GL;
import javax.media.opengl.GLAutoDrawable;
import javax.media.opengl.glu.GLU;
import javax.media.opengl.glu.GLUquadric;

import com.benton.framework.math.M3d;



public class NormalsAnimation extends GLRenderer {

  private int tick = 0;
  private int displayListId = -1;
  private boolean paused = true;

  public String getTitle() {
    return "Normals animation";
  }

  public void init(GLAutoDrawable glDrawable) {
    super.init(glDrawable);

    final GL gl = glDrawable.getGL();
    GLU glu = new GLU();
    GLUquadric quadric = glu.gluNewQuadric();

    gl.glCullFace(GL.GL_BACK);
    gl.glEnable(GL.GL_CULL_FACE);

    glu.gluQuadricOrientation(quadric, GLU.GLU_OUTSIDE);
    displayListId = gl.glGenLists(1);
    gl.glNewList(displayListId, GL.GL_COMPILE);
    gl.glPushMatrix();
    gl.glRotatef(90, 1, 0, 0);
    glu.gluSphere(quadric, 1, 50, 50);
    gl.glPopMatrix();
    gl.glEndList();
  }

  // Sixteen ticks around the circle
  private M3d getTick(int i, double t) {
    return new M3d(sin(t) * cos(i*PI/8), sin(t) * sin(i*PI/8), cos(t));
  }

  @Override
  public void display(GLAutoDrawable glDrawable) {
    final GL gl = glDrawable.getGL();
    final double t = (sin(tick * PI / 500 + PI / 2) + 1) * PI / 4;
    M3d A, B, C;

    preDisplay(glDrawable);

    A = new M3d(0, 0, 1);
    B = getTick(0,t);
    C = getTick(2,t);

    gl.glLineWidth(3);
    gl.glDisable(GL.GL_LIGHTING);
    gl.glBegin(GL.GL_LINE_STRIP);
    gl.glColor4f(1, 0, 0, 1);
    for (double d = 0; d <= 2 * PI + 0.0001; d += PI / 16) {
      gl.glVertex3d(sin(t) * cos(d), sin(t) * sin(d), cos(t));
    }
    gl.glEnd();

    gl.glColor4f(0.2f, 0.8f, 0.2f, 1);
    gl.glBegin(GL.GL_LINES);
      gl.glVertex3dv(A.get(),0);
      gl.glVertex3dv(B.get(),0);
      gl.glVertex3dv(A.get(),0);
      gl.glVertex3dv(C.get(),0);
    gl.glEnd();

    gl.glBegin(GL.GL_LINE_STRIP);
    for (double u = 0; u<t; u+=0.01) {
      gl.glVertex3dv(A.plus(B.minus(A).times(u/t)).normalized().get(),0);
    }
    gl.glEnd();

    gl.glBegin(GL.GL_LINE_STRIP);
    for (double u = 0; u<t; u+=0.01) {
      gl.glVertex3dv(A.plus(C.minus(A).times(u/t)).normalized().get(),0);
    }
    gl.glEnd();
    
    gl.glEnable(GL.GL_LIGHTING);
    gl.glLineWidth(1);
    
    gl.glColor4f(0.1f, 0.6f, 0.1f, 1);
    gl.glDisable(GL.GL_CULL_FACE);
    gl.glBegin(GL.GL_TRIANGLES);
      gl.glNormal3dv(B.minus(A).cross(C.minus(A)).normalized().get(),0);
      gl.glVertex3dv(A.get(),0);
      gl.glVertex3dv(B.get(),0);
      gl.glVertex3dv(C.get(),0);
    gl.glEnd();
    gl.glEnable(GL.GL_CULL_FACE);

    for (int i = 0; i<8; i++) {
      M3d D = getTick(i*2+1, t/2);
      M3d E = D.times(1.5);

      if (i==0) {
        D = intersectPlane(E,D,A,B,C);
      } else if (i==1) {
        gl.glColor4f(0.2f, 0.2f, 0.8f, 1);  // Set color after first arrow
      }
      if (D != null) {
        arrow(gl,D,E);
      }
    }

    gl.glColor4f(0.8f, 0.8f, 0.8f, 0.6f);
    gl.glCallList(displayListId);

    if (!paused) {
      tick++;
    }
    postDisplay(glDrawable);
  }

  @Override
  public void keyPressed(KeyEvent e) {
    switch (e.getKeyChar()) {
    case ' ':
      paused = !paused;
      break;

    default:
      super.keyPressed(e);
    }
  }
}
