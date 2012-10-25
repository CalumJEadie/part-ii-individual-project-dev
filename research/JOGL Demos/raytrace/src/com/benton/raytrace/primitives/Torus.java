package com.benton.raytrace.primitives;

import static com.benton.framework.math.MathUtil.SolveQuartic;

import com.benton.framework.math.M3d;
import com.benton.framework.math.Ray;
import com.benton.raytrace.engine.HitList;
import com.benton.raytrace.engine.MaterialPrimitive;

public class Torus extends MaterialPrimitive {

  static final double r = 0.4;         // Minor radius
  static final double R = 1.6;         // Major radius
  
  public Torus(M3d color) {
    super(color);
  }
  
  protected M3d getNormal(M3d point) {
    M3d proj = (new M3d(point.getX(), 0, point.getZ())).normalized().times(R);
    
    return point.minus(proj).normalized();
  }
  
  /**
   * Notation and maths from Graphics Gems II, p. 252
   */
  public boolean testLocalRay(Ray ray, HitList collisions) {
    double ax = ray.direction.getX();
    double ay = ray.direction.getY();
    double az = ray.direction.getZ();
    double x0 = ray.origin.getX();
    double y0 = ray.origin.getY();
    double z0 = ray.origin.getZ();
    double p = (r*r)/(r*r); // Square of the eliptical ratio x/y
    double A0 = 4*R*R;
    double B0 = (R*R - r*r);
    double C0 = ax*ax + p*ay*ay + az*az;
    double D0 = x0*ax + p*y0*ay + z0*az;
    double E0 = x0*x0 + p*y0*y0 + z0*z0 + B0;
    double[] coefficients = {
        E0*E0 - A0*(x0*x0+z0*z0),
        4*D0*E0 - 2*A0*(x0*ax+z0*az),
        4*D0*D0 + 2*E0*C0 - A0*(ax*ax+az*az),
        4*D0*C0,
        C0*C0
    };
    double[] solutions = new double[4];
    int numSolutions = SolveQuartic(coefficients, solutions);
    boolean success = false;
    
    for (int i = 0; i<numSolutions; i++) {
      success |= (recordCollision(solutions[i], ray, collisions) != null);
    }

    return success;
  }
}
