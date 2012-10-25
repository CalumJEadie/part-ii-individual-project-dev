package abnormals;

import static java.lang.Math.PI;

import javax.media.opengl.GL;

import com.benton.framework.math.M3d;
import com.benton.framework.math.M4x4;

public class Arrow {

  public static void arrow(GL gl, M3d from, M3d to) {
    M3d axis = to.minus(from).normalized();
    M3d pt = axis.cross(new M3d(0,1,0)).normalized().times(0.02);
    gl.glBegin(GL.GL_QUADS);
    for (double t = 0; t <= PI * 2 + 0.0001; t += PI / 16) {
      M4x4 T1 = M4x4.rotation(axis, t);
      M4x4 T2 = M4x4.rotation(axis, t + PI/16);
      gl.glNormal3dv(T1.times(pt).plus(T2.times(pt)).normalized().get(), 0);
      gl.glVertex3dv(to.plus(T1.times(pt)).get(), 0);
      gl.glVertex3dv(from.plus(T1.times(pt)).get(), 0);
      gl.glVertex3dv(from.plus(T2.times(pt)).get(), 0);
      gl.glVertex3dv(to.plus(T2.times(pt)).get(), 0);
    }
    gl.glEnd();
    gl.glBegin(GL.GL_TRIANGLE_FAN);
      gl.glVertex3dv(to.plus(to.minus(from).times(0.5)).get(), 0);
      for (double t = 0; t <= PI * 2 + 0.0001; t += PI / 16) {
        M4x4 T = M4x4.rotation(axis, t);
        M3d p = T.times(pt).times(2);
        
        gl.glNormal3dv(p.cross(axis).cross(p.minus(axis)).normalized().get(), 0);
        gl.glVertex3dv(to.plus(p).get(), 0);
      }
    gl.glEnd();
  }
  
}
