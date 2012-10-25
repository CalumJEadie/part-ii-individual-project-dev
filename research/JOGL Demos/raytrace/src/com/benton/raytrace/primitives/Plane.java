package com.benton.raytrace.primitives;

import com.benton.framework.math.M3d;
import com.benton.framework.math.Ray;
import com.benton.raytrace.engine.HitList;
import com.benton.raytrace.engine.Material;
import com.benton.raytrace.engine.MaterialPrimitive;
import com.benton.raytrace.engine.RayCollision;

public class Plane extends MaterialPrimitive {

  static final M3d YAxis = new M3d(0,1,0);  
  
  public Plane(M3d color) {
    super(color);
  }
  
  protected M3d getNormal(M3d point) {
    return YAxis;
  }

  public boolean testLocalRay(Ray ray, HitList collisions) {
    double t = -ray.origin.getY() / ray.direction.getY();
    RayCollision hit = recordCollision(t, ray, collisions);

    if (hit != null) {
      M3d pt = ray.at(t);
      int x = (int)(Math.floor(pt.getX()));
      int z = (int)(Math.floor(pt.getZ()));
      Material mat = new Material(getMaterial());

      mat.setColor( 
        (pt.length() <= 5) ? 
            mat.getColor().times((x + z) & 0x01) :
        (pt.length() <= 5.25) ? 
            new M3d(0.2f,0.6f,0.8f) : 
            mat.getColor());
      mat.setReflectivity(0.5);
      hit.material = mat;
      return true;
    } else {
      return false;
    }
  }
}
