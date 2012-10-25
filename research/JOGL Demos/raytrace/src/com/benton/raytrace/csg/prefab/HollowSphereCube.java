package com.benton.raytrace.csg.prefab;

import com.benton.framework.math.M3d;
import com.benton.framework.math.M4x4;
import com.benton.framework.math.Ray;
import com.benton.raytrace.csg.CsgBoolean;
import com.benton.raytrace.csg.Difference;
import com.benton.raytrace.csg.Intersection;
import com.benton.raytrace.csg.Union;
import com.benton.raytrace.engine.HitList;
import com.benton.raytrace.primitives.Cube;
import com.benton.raytrace.primitives.Primitive;
import com.benton.raytrace.primitives.Sphere;

public class HollowSphereCube extends Primitive {

  private final CsgBoolean inner;
  
  public HollowSphereCube() {
    Sphere A = new Sphere(new M3d(1, 1, 1));
    Sphere B = new Sphere(new M3d(1, 1, 1));
    Sphere C = new Sphere(new M3d(1, 1, 1));
    Cube D = new Cube(new M3d(0.2, 0.5, 0.8));
    Sphere E1 = new Sphere(new M3d(1, 1, 1));
    Sphere E2 = new Sphere(new M3d(1, 1, 1));
    A.getMaterial().setReflectivity(0);
    B.getMaterial().setReflectivity(0);
    C.getMaterial().setReflectivity(0);
    D.getMaterial().setReflectivity(0);
    A.setLocalTransform(M4x4.scale(new M3d(200, 0.55, 0.55)));
    B.setLocalTransform(M4x4.scale(new M3d(0.55, 200, 0.55)));
    C.setLocalTransform(M4x4.scale(new M3d(0.55, 0.55, 200)));
    D.setLocalTransform(M4x4.scale(new M3d(0.7, 0.7, 0.7)));
    E1.setLocalTransform(M4x4.scale(new M3d(1, 1, 1)));
    E2.setLocalTransform(M4x4.scale(new M3d(0.85, 0.85, 0.85)));
    CsgBoolean axes = new Union(A, new Union(B, C));
    CsgBoolean cubeMinusAxes = new Difference(D, axes);
    CsgBoolean shell = new Difference(E1, E2);
    inner = new Intersection(cubeMinusAxes, shell);
  }

  @Override
  public boolean testLocalRay(Ray ray, HitList collisions) {
    return inner.testLocalRay(ray, collisions);
  }
}
