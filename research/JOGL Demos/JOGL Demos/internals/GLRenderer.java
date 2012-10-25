package internals;

import static java.lang.Math.PI;

import java.awt.Point;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import java.awt.event.MouseMotionListener;
import java.awt.event.MouseWheelEvent;
import java.awt.event.MouseWheelListener;

import javax.media.opengl.GL;
import javax.media.opengl.GLAutoDrawable;
import javax.media.opengl.GLEventListener;
import javax.media.opengl.glu.GLU;

import com.benton.framework.math.M3d;
import com.benton.framework.math.M4x4;
import com.sun.opengl.util.GLUT;

public abstract class GLRenderer implements GLEventListener, KeyListener, MouseListener, MouseMotionListener, MouseWheelListener {

  protected final GLUT glut = new GLUT();
  
  protected M4x4 cameraTransform = new M4x4();
  protected double cameraDistance = 4;
  protected boolean showAxes = true;
  protected Point lastCapturedMousePosition;
  
  public abstract String getTitle();

  public void init(GLAutoDrawable glDrawable) {
    final GL gl = glDrawable.getGL();
    gl.glClearColor(0.2f, 0.4f, 0.6f, 0.0f);
    gl.glClearDepth(1.0f);
    gl.glEnable(GL.GL_DEPTH_TEST);
    gl.glEnable(GL.GL_LIGHTING);
    gl.glEnable(GL.GL_COLOR_MATERIAL);
    gl.glEnable(GL.GL_LIGHT0);
    gl.glShadeModel(GL.GL_FLAT);
    gl.glColorMaterial(GL.GL_FRONT_AND_BACK, GL.GL_AMBIENT_AND_DIFFUSE);
    gl.glDepthFunc(GL.GL_LEQUAL);
    gl.glHint(GL.GL_PERSPECTIVE_CORRECTION_HINT, GL.GL_NICEST);
    gl.glEnable(GL.GL_ALPHA);
    gl.glEnable(GL.GL_BLEND);
    gl.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA);
    gl.glDisable(GL.GL_DITHER);
    glDrawable.addKeyListener(this);
    glDrawable.addMouseListener(this);
    glDrawable.addMouseMotionListener(this);
    glDrawable.addMouseWheelListener(this);
  }
  
  public void preDisplay(GLAutoDrawable glDrawable) {
    final GL gl = glDrawable.getGL();
    
    gl.glClear(GL.GL_COLOR_BUFFER_BIT);
    gl.glClear(GL.GL_DEPTH_BUFFER_BIT);
    gl.glLoadIdentity();
    gl.glTranslated(0.0, 0.0, -cameraDistance);
    gl.glMultMatrixd(cameraTransform.getData(), 0);

    if (showAxes) {
      gl.glDisable(GL.GL_LIGHTING);
      gl.glBegin(GL.GL_LINES);
      gl.glColor3f(1,1,1);
      gl.glVertex3i(-100, 0, 0);
      gl.glVertex3i(100, 0, 0);
      gl.glVertex3i(0,-100, 0);
      gl.glVertex3i(0,100, 0);
      gl.glVertex3i(0,0,-100);
      gl.glVertex3i(0,0,100);
      gl.glEnd();
      gl.glEnable(GL.GL_LIGHTING);
    }
  }
  
  public void postDisplay(GLAutoDrawable glDrawable) {
    
  }
  
  public void displayChanged(GLAutoDrawable glDrawable, boolean modeChanged, boolean deviceChanged) {
  }

  public void reshape(GLAutoDrawable gLDrawable, int x, int y, int width, int height) {
    final GL gl = gLDrawable.getGL();
    if (height <= 0) {
      height = 1;
    }
    final float h = (float)width / (float)height;
    gl.glMatrixMode(GL.GL_PROJECTION);
    gl.glLoadIdentity();
    (new GLU()).gluPerspective(50.0f, h, 0.005, 100.0);
    gl.glMatrixMode(GL.GL_MODELVIEW);
    gl.glLoadIdentity();
  }

  public void glPrint(GL gl, float x, float y, float z, int font, String string) {
    gl.glPushMatrix();
    gl.glTranslatef(x, y, z);  // Position Text On The Screen
    gl.glScalef(0.005f, 0.005f, 0.005f);
    int width = glut.glutStrokeLength(font, string);
    gl.glTranslatef(-width, 0, 0);    // Right align text with position
    for (int i = 0; i < string.length(); i++) {
      glut.glutStrokeCharacter(font, string.charAt(i));
    }
    gl.glPopMatrix();
  }
  
  public void keyPressed(KeyEvent e) {
    switch (e.getKeyCode()) {
    case KeyEvent.VK_ESCAPE:
      System.exit(0);
      break;
    case KeyEvent.VK_PAGE_DOWN:
      cameraDistance+=0.25;
      break;
    case KeyEvent.VK_PAGE_UP:
      cameraDistance-=0.25;
      break;
    case KeyEvent.VK_1:
      cameraTransform = new M4x4();
      break;
    case KeyEvent.VK_2:
      cameraTransform = M4x4.rotation(new M3d(0,1,0), -PI/8.0);
      cameraTransform.rotate(new M3d(1,0,-1), PI/8.0);
      cameraTransform.rotate(new M3d(0,0,1), 5*PI/64.0);
      break;
    case KeyEvent.VK_3:
      cameraTransform = M4x4.rotation(new M3d(1,0,0), 3.141592/2.0);
      break;
    case KeyEvent.VK_4:
      cameraTransform = M4x4.rotation(new M3d(1,0,0), -3.141592/2.0 * 0.775);
      break;
    }
  }

  public void keyReleased(KeyEvent e) {
  }
  
  public void keyTyped(KeyEvent e) {
  }

  @Override
  public void mouseClicked(MouseEvent e) {
  }

  @Override
  public void mouseEntered(MouseEvent e) {
  }

  @Override
  public void mouseExited(MouseEvent e) {
  }

  @Override
  public void mousePressed(MouseEvent e) {
    lastCapturedMousePosition = e.getLocationOnScreen();
  }

  @Override
  public void mouseReleased(MouseEvent e) {
  }
  
  public double getMouseSpeed() {
    return 1.0;
  }

  @Override
  public void mouseDragged(MouseEvent e) {
    int dx = e.getLocationOnScreen().x - lastCapturedMousePosition.x;
    int dy = e.getLocationOnScreen().y - lastCapturedMousePosition.y;
    double len = Math.sqrt(dx*dx + dy*dy) * getMouseSpeed() / (8.0 * cameraDistance);
    M3d right = cameraTransform.getRow(0);
    M3d up = cameraTransform.getRow(1);
    M3d axis = up.times(dx).plus(right.times(dy)).normalized();
    
    lastCapturedMousePosition = e.getLocationOnScreen();
    cameraTransform.rotate(axis, len);
  }
  
  @Override
  public void mouseWheelMoved(MouseWheelEvent e) {
    double notches = -e.getWheelRotation() / 1.5;

    if (e.getScrollType() == MouseWheelEvent.WHEEL_UNIT_SCROLL) {
      cameraDistance += notches;
    }
  }

  @Override
  public void mouseMoved(MouseEvent e) {
  }
}
