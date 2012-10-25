package hellosquare;

import javax.media.opengl.GL;
import javax.media.opengl.GLAutoDrawable;
import javax.media.opengl.GLEventListener;
import javax.media.opengl.glu.GLU;

public abstract class SimpleRendererBase implements GLEventListener {

  public void init(GLAutoDrawable glDrawable) {
    final GL gl = glDrawable.getGL();

    gl.glClearColor(0.2f, 0.4f, 0.6f, 0.0f);
  }
  
  public abstract void render(GL gl);

  public void display(GLAutoDrawable glDrawable) {
    final GL gl = glDrawable.getGL();

    gl.glClear(GL.GL_COLOR_BUFFER_BIT);
    gl.glLoadIdentity();
    gl.glTranslatef(0, 0, -5);
    
    render(gl);
  }

  public void displayChanged(GLAutoDrawable glDrawable, boolean modeChanged, boolean deviceChanged) {
  }

  public void reshape(GLAutoDrawable gLDrawable, int x, int y, int width, int height) {
    final GL gl = gLDrawable.getGL();
    final float h = (float)width / (float)(height <= 1 ? 1 : height);
    
    gl.glMatrixMode(GL.GL_PROJECTION);
    gl.glLoadIdentity();
    (new GLU()).gluPerspective(50.0f, h, 1.0, 1000.0);
    gl.glMatrixMode(GL.GL_MODELVIEW);
  }
}
