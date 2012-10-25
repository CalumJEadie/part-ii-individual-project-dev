package com.benton.raytrace.primitives;

import static com.benton.raytrace.engine.RayTracer.MIN_TRAVEL;

import com.benton.framework.math.M3d;
import com.benton.framework.math.Ray;
import com.benton.raytrace.engine.HitList;
import com.benton.raytrace.engine.MaterialPrimitive;
import com.benton.raytrace.engine.RayCollision;

public class Cube extends MaterialPrimitive {
  
  public Cube(M3d color) {
    super(color);
  }
  
  protected M3d getNormal(M3d point) {
    return point.toAxis();
  }

  protected RayCollision recordCollision(double t, Ray ray, HitList collisions) {
    if (t > MIN_TRAVEL) {
      M3d pt = ray.at(t);

      if (Math.abs(pt.getX()) <= 1.00001 && 
          Math.abs(pt.getY()) <= 1.00001 && 
          Math.abs(pt.getZ()) <= 1.00001) {
        return super.recordCollision(t, ray, collisions);
      }
    }
    
    return null;
  }
  
  public boolean testLocalRay(Ray ray, HitList collisions) {
    boolean success = false;
    
    success |= (recordCollision(-(ray.origin.getX()-1) / ray.direction.getX(), ray, collisions) != null);
    success |= (recordCollision(-(ray.origin.getX()+1) / ray.direction.getX(), ray, collisions) != null);
    success |= (recordCollision(-(ray.origin.getY()-1) / ray.direction.getY(), ray, collisions) != null);
    success |= (recordCollision(-(ray.origin.getY()+1) / ray.direction.getY(), ray, collisions) != null);
    success |= (recordCollision(-(ray.origin.getZ()-1) / ray.direction.getZ(), ray, collisions) != null);
    success |= (recordCollision(-(ray.origin.getZ()+1) / ray.direction.getZ(), ray, collisions) != null);
    return success;
  }
}
