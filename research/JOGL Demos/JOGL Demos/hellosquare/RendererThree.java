package hellosquare;

import static java.lang.Math.PI;
import static java.lang.Math.cos;
import static java.lang.Math.sin;

import javax.media.opengl.GL;

public class RendererThree extends SimpleRendererBase {

  public void vertex(GL gl, double x, double y, double z) {
    gl.glColor3d((x+1)/2.0f,(y+1)/2.0f,(z+1)/2.0f);
    gl.glVertex3d(x, y, z);
  }
  
  public void render(GL gl) {
    gl.glBegin(GL.GL_TRIANGLES);
      for (double u = 0; u <= 2*PI; u += 0.1) {
        vertex(gl, 0, 0, 0);
        vertex(gl, cos(u), sin(u), 0);
        vertex(gl, cos(u+0.1), sin(u+0.1), 0);
      }
    gl.glEnd();
  }
}
