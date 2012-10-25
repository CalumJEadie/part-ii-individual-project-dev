package shaders;

import static java.lang.Math.PI;
import static java.lang.Math.cos;
import static java.lang.Math.sin;

import com.benton.framework.math.M3d;

public class Torus {

  static final int di = 75;
  static final int dj = 25;
  static final float R = 5;
  static final float r = 1.5f;
  
  M3d[][] torusPts;
  M3d[][] torusNormals;

  public Torus() {
    torusPts = new M3d[di][dj];
    torusNormals = new M3d[di][dj];
    for (int i = 0; i<di; i++) {
      for (int j = 0; j<dj; j++) {
        torusPts[i][j] = torus(i, j);
      }
    }
    for (int i = 0; i<di; i++) {
      for (int j = 0; j<dj; j++) {
        torusNormals[i][j] = 
          getVertex(i+1,j).minus(getVertex(i,j)).cross(getVertex(i,j+1).minus(getVertex(i,j)))
          .plus(getVertex(i,j+1).minus(getVertex(i,j)).cross(getVertex(i-1,j).minus(getVertex(i,j))))
          .plus(getVertex(i-1,j).minus(getVertex(i,j)).cross(getVertex(i,j-1).minus(getVertex(i,j))))
          .plus(getVertex(i,j-1).minus(getVertex(i,j)).cross(getVertex(i+1,j).minus(getVertex(i,j))))
          .normalized();
      }
    }
  }

  private M3d torus(double u, double v) {
    M3d pt;

    u = 2 * PI * u / di;
    v = 2 * PI * v / dj + PI;
    pt = new M3d(R+r*cos(v), 0, r*sin(v));
    return new M3d(pt.get(0) * cos(u) - pt.get(1) * sin(u),
                   pt.get(0) * sin(u) + pt.get(1) * cos(u),
                   pt.get(2));
  }
  
  public M3d getVertex(int i, int j) {
    return torusPts[(i+di)%di][(j+dj)%dj];
  }
  
  public M3d getNormal(int i, int j) {
    return torusNormals[(i+di)%di][(j+dj)%dj];
  }
}
