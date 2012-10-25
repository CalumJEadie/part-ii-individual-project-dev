package com.benton.raytrace.engine;

import com.benton.framework.math.M3d;

public class RayCollision {
  public double t;
  public M3d point;
  public M3d normal;
  public Material material;

  public RayCollision() {
  }
  
  public RayCollision(RayCollision surface) {
    this.t = surface.t;
    this.point = surface.point;
    this.normal = surface.normal;
    this.material = surface.material;
  }
}
