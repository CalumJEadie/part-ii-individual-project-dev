package hierarchy;

import internals.GLRenderer;

import java.awt.event.KeyEvent;

import javax.media.opengl.GL;
import javax.media.opengl.GLAutoDrawable;
import javax.media.opengl.glu.GLU;
import javax.media.opengl.glu.GLUquadric;



public class HierarchyDemo extends GLRenderer {
  
  private int numLevels = 0;
  private int tick = 0;
  private int displayListId = -1;
  private boolean paused = true;
  
  public String getTitle() {
    return "Hierarchical model";
  }

  public void init(GLAutoDrawable glDrawable) {
    super.init(glDrawable);
    
    final GL gl = glDrawable.getGL();
    GLU glu = new GLU();
    GLUquadric quadric = glu.gluNewQuadric();
    
    glu.gluQuadricOrientation(quadric, GLU.GLU_OUTSIDE);
    displayListId = gl.glGenLists(1);
    gl.glNewList(displayListId, GL.GL_COMPILE);
    gl.glPushMatrix();
    gl.glRotatef(90, 1, 0, 0);
    glu.gluSphere(quadric, 0.15, 10, 10);
    gl.glPopMatrix();
    gl.glEndList();
  }
  
  void renderLevel(GL gl, int level) {
    float t = ((float)tick)/5.0f;
    
    gl.glPushMatrix();
    gl.glRotatef(t, 0, 1, 0);
    gl.glCallList(displayListId);
    if (level > 0) {
      gl.glScalef(0.75f, 0.75f, 0.75f);

      gl.glDisable(GL.GL_LIGHTING);
      gl.glLineWidth(3);
      gl.glBegin(GL.GL_LINES);
      gl.glColor3f(1, 0, 0);
      gl.glVertex3f(0, 0, 0);
      gl.glVertex3f(1, -0.75f, 0);
      gl.glVertex3f(0, 0, 0);
      gl.glVertex3f(-1, -0.75f, 0);
      gl.glEnd();
      gl.glLineWidth(1);
      gl.glEnable(GL.GL_LIGHTING);

      gl.glColor3f(1, 1, 1);
      
      gl.glPushMatrix();
      gl.glTranslatef(1, -0.75f, 0);
      renderLevel(gl, level-1);
      gl.glPopMatrix();

      gl.glPushMatrix();
      gl.glTranslatef(-1, -0.75f, 0);
      renderLevel(gl, level-1);
      gl.glPopMatrix();
    }
    gl.glPopMatrix();
  }

  @Override
  public void preDisplay(GLAutoDrawable glDrawable) {
    final GL gl = glDrawable.getGL();
    
    super.preDisplay(glDrawable);
    gl.glTranslatef(0, 1, 0);
  }
  
  @Override
  public void display(GLAutoDrawable glDrawable) {
    preDisplay(glDrawable);
    renderLevel(glDrawable.getGL(), numLevels);
    if (!paused) {
      tick++;
    }
    postDisplay(glDrawable);
  }

  @Override
  public void keyPressed(KeyEvent e) {
    switch (e.getKeyChar()) {
    
    case '=':
    case '+':
      if (numLevels < 12) {
        numLevels++;
      }
      break;

    case '-':
    case '_':
      if (numLevels > 0) {
        numLevels--;
      }
      break;
    
    case ' ':
      paused = !paused;
      break;
    
    default:
      super.keyPressed(e);
    }
  }
}
