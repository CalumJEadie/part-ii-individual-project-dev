package hellosquare;

import javax.media.opengl.GL;

public class RendererTwo extends SimpleRendererBase {

  public void vertex(GL gl, float x, float y, float z) {
    gl.glColor3f((x+1)/2.0f,(y+1)/2.0f,(z+1)/2.0f);
    gl.glVertex3f(x, y, z);
  }
  
  public void render(GL gl) {
    gl.glBegin(GL.GL_QUADS);
      vertex(gl, -1, -1,  0);
      vertex(gl,  1, -1,  0);
      vertex(gl,  1,  1,  0);
      vertex(gl, -1,  1,  0);
    gl.glEnd();
  }
}
