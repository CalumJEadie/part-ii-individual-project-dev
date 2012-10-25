package com.benton.framework.math;

public class Ray {
  public M3d origin;
  public M3d direction;
  
  public Ray(M3d origin, M3d direction) {
    this.origin = origin;
    this.direction = direction;
  }
  
  public Ray transformedBy(M4x4 T) {
    return new Ray(T.times(origin), T.extract3x3().times(direction).normalized());
  }
  
  public M3d at(double t) {
    return origin.plus(direction.times(t)); 
  }
}
