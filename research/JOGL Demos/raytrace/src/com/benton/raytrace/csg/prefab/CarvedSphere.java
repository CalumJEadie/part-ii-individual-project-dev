package com.benton.raytrace.csg.prefab;

import com.benton.framework.math.M3d;
import com.benton.framework.math.M4x4;
import com.benton.framework.math.Ray;
import com.benton.raytrace.csg.CsgBoolean;
import com.benton.raytrace.csg.Difference;
import com.benton.raytrace.csg.Intersection;
import com.benton.raytrace.csg.Union;
import com.benton.raytrace.engine.HitList;
import com.benton.raytrace.primitives.Primitive;
import com.benton.raytrace.primitives.Sphere;
import com.benton.raytrace.primitives.Torus;

public class CarvedSphere extends Primitive {
  
  private final CsgBoolean inner;

  public CarvedSphere() {
    Sphere A = new Sphere(new M3d(0.2,0.5,0.8));
    Torus B = new Torus(new M3d(0.8,0.5,0.2));
    B.setLocalTransform(M4x4.scale(new M3d(0.75,0.75,0.75)));    
    CsgBoolean d = new Difference(A,B);
    CsgBoolean i = new Intersection(A,B);
    i.setLocalTransform(M4x4.scale(new M3d(1.5,0.5,1.5)));
    inner = new Union(i, d);
  }

  @Override
  public boolean testLocalRay(Ray ray, HitList collisions) {
    return inner.testLocalRay(ray, collisions);
  }
}
