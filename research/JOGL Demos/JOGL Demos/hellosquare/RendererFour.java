package hellosquare;

import static java.lang.Math.PI;
import static java.lang.Math.cos;
import static java.lang.Math.sin;

import javax.media.opengl.GL;

public class RendererFour extends SimpleRendererBase {
  
  public void vertex(GL gl, double x, double y, double z) {
    gl.glColor3d((x+1)/2.0f,(y+1)/2.0f,(z+1)/2.0f);
    gl.glVertex3d(x, y, z);
  }
  
  public void sphere(GL gl, double u, double v) {
    vertex(gl, cos(u)*cos(v), sin(u)*cos(v), sin(v));
  }
  
  public void render(GL gl) {
    gl.glBegin(GL.GL_QUADS);
    for (double u = 0; u <= 2*PI; u += 0.1) {
      for (double v = 0; v <= PI; v += 0.1) {
        sphere(gl, u, v);
        sphere(gl, u+0.1, v);
        sphere(gl, u+0.1, v+0.1);
        sphere(gl, u, v+0.1);
      }
    }
    gl.glEnd();
  }
}
