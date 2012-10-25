package com.benton.raytrace.engine;

import com.benton.framework.math.M3d;
import com.benton.framework.math.Ray;
import com.benton.raytrace.primitives.Primitive;

public abstract class MaterialPrimitive extends Primitive {
  
  protected Material material = new Material();
  
  protected MaterialPrimitive() {
  }
  
  protected MaterialPrimitive(M3d color) {
    material.setColor(color);
  }
  
  public Material getMaterial() {
    return material;
  }
  
  protected RayCollision recordCollision(double t, Ray ray, HitList collisions) {
    RayCollision hit = super.recordCollision(t, ray, collisions);
   
    if (hit != null) {
      hit.material = material;
    }
    return hit;
  }
}
