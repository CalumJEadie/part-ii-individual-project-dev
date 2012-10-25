package com.benton.raytrace.primitives;

import com.benton.framework.math.M3d;
import com.benton.framework.math.Ray;
import com.benton.raytrace.engine.HitList;
import com.benton.raytrace.engine.MaterialPrimitive;

public class Sphere extends MaterialPrimitive {

  public Sphere(M3d color) {
    super(color);
  }
  
  protected M3d getNormal(M3d point) {
    return point;
  }
  
  public boolean testLocalRay(Ray ray, HitList collisions) {
    double OdotD = ray.origin.dot(ray.direction);
    double DdotD = ray.direction.dot(ray.direction);
    double OdotO = ray.origin.dot(ray.origin);
    double bm4ac = Math.sqrt(OdotD*OdotD - DdotD*(OdotO-1)); 
    double t1 = (-OdotD + bm4ac) / DdotD;
    double t2 = (-OdotD - bm4ac) / DdotD;
    boolean success = false;
    
    success |= (recordCollision(t1, ray, collisions) != null);
    success |= (recordCollision(t2, ray, collisions) != null);
    return success;
  }
}
